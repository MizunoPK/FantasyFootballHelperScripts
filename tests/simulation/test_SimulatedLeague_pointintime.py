"""
Point-in-time regression tests for the win-rate simulation
(story: winrate-sim-lookahead-frozen-snapshot).

Proves, on a concrete 3-week fixture, the acceptance core:
  1. The per-week data swap FIRES — projected_pm projections track the loaded folder and
     change as _load_week_data advances (no longer frozen at one week_18 snapshot).
  2. Per-folder sourcing — projected_pm <- week_N, actual_pm <- week_{N+1}.
  3. Win-tallying still sources real completed-week actuals via actual_pm (not the
     post-swap 0.0 projected_pm value) for BOTH DraftHelperTeam and SimulatedOpponent.
Also guards that the two byte-for-byte _parse_players_json copies stay in sync (D4).

Fixture (weeks/week_01..18, 6 position files each — T73/R12: the loaders now require the
complete 18-week tree, since week_N+1 supplies week N's actuals):
  projected_points: folder-distinct constant — week_0K = 5.0 + (K-1)*10.0
                    (week_01=5.0, week_02=15.0, week_03=25.0, ... unchanged for 1..3)
  actual_points:    real for completed weeks, 0.0 for current/future —
                    week_01 -> all 0.0
                    week_02 -> actual_points[0] (week 1) = 12.0, rest 0.0
                    week_03 -> actual_points[0] = 12.0, actual_points[1] (week 2) = 8.0, rest 0.0
                    week_0K -> actual_points[j-1] = WEEK_ACTUAL[j] for every completed week j < K

Author: Kai Mizuno
"""

import inspect
import json
import types
from unittest.mock import Mock, patch

import pytest

from league_helper.util.PlayerManager import PlayerManager
from simulation.win_rate.SimulatedLeague import SimulatedLeague, load_week_player_data
from simulation.win_rate.SimDataLoader import SimDataLoader
from simulation.win_rate.DraftHelperTeam import DraftHelperTeam
from simulation.win_rate.SimulatedOpponent import SimulatedOpponent
from utils.FantasyPlayer import FantasyPlayer


# Fixture constants (also reused as the expected post-swap values in TestWinTallyingSourcesActualPm).
# T73/R12: generalised from the original 3-week literals to the full 18-folder tree the loaders
# now require. The week-1/2/3 values are byte-equivalent to the originals (5.0/15.0/25.0), so
# every pre-existing offset assertion below is preserved exactly.
FIXTURE_WEEK_FOLDERS = 18
WEEK_PROJECTED = {k: 5.0 + (k - 1) * 10.0 for k in range(1, FIXTURE_WEEK_FOLDERS + 1)}
WEEK1_ACTUAL = 12.0   # real week-1 result — lives in the week_02 folder
WEEK2_ACTUAL = 8.0    # real week-2 result — lives in the week_03 folder
# Real result for each completed week, indexed by the week number it belongs to. Weeks 1 and 2
# keep the original fixture values the per-folder-sourcing assertions pin.
WEEK_ACTUAL = {1: WEEK1_ACTUAL, 2: WEEK2_ACTUAL}
WEEK_ACTUAL.update({k: 100.0 + k for k in range(3, FIXTURE_WEEK_FOLDERS)})

POSITIONS = [
    ("qb_data.json", "QB", [1]),
    ("rb_data.json", "RB", [2, 3, 4]),
    ("wr_data.json", "WR", [5, 6, 7]),
    ("te_data.json", "TE", [8, 9]),
    ("k_data.json", "K", [10, 11]),
    ("dst_data.json", "DST", [12]),
]
ALL_IDS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]


def _actual_array_for(folder_week):
    """actual_points array a week_0K folder carries (real for weeks < K, 0.0 otherwise)."""
    arr = [0.0] * 17
    for completed_week in range(1, min(folder_week, FIXTURE_WEEK_FOLDERS)):
        arr[completed_week - 1] = WEEK_ACTUAL[completed_week]
    return arr


def _write_week_folder(weeks_folder, folder_week):
    week_dir = weeks_folder / f"week_{folder_week:02d}"
    week_dir.mkdir()
    projected = [WEEK_PROJECTED[folder_week]] * 17
    actual = _actual_array_for(folder_week)
    for filename, position, ids in POSITIONS:
        players = [
            {
                "id": str(pid),
                "name": f"{position} {pid}",
                "position": position,
                "drafted_by": "",
                "locked": False,
                "projected_points": list(projected),
                "actual_points": list(actual),
            }
            for pid in ids
        ]
        key = filename.removesuffix(".json")
        (week_dir / filename).write_text(json.dumps({key: players}))


@pytest.fixture
def season_folder(tmp_path):
    """Build a complete 18-folder fixture season (week_01..week_18) under tmp_path."""
    weeks_folder = tmp_path / "weeks"
    weeks_folder.mkdir()
    for fw in range(1, FIXTURE_WEEK_FOLDERS + 1):
        _write_week_folder(weeks_folder, fw)
    return tmp_path


def _make_bare_pm():
    """Real PlayerManager exposing only what set_player_data touches, one FantasyPlayer per id."""
    players = [
        FantasyPlayer(
            id=pid, name=f"P{pid}", team="KC", position="RB",
            projected_points=[0.0] * 17, actual_points=[0.0] * 17,
        )
        for pid in ALL_IDS
    ]
    pm = PlayerManager.__new__(PlayerManager)
    pm.logger = Mock()
    pm.players = players
    pm.max_projection = 0.0
    pm.max_weekly_projections = {}
    pm.scoring_calculator = Mock()
    pm.scoring_calculator.weight_projection = lambda fp: fp
    return pm


def _by_id(pm, pid):
    return next(p for p in pm.players if p.id == pid)


def _make_bare_parser():
    """A stand-in for the bound _parse_players_json, so the helper can be driven directly."""
    return lambda week_folder, week_num, week_num_for_actual=None: {}


def _make_league_with_bare_teams(season_folder):
    """
    Minimal SimulatedLeague pointed at the fixture (teams/schedule stubbed). __init__ runs
    _preload_all_weeks() for real against the fixture, so week_data_cache is populated
    {1..17}. One team carries two real (bare) PlayerManagers for the swap to write into.
    """
    config = {"config_name": "test", "description": "test", "parameters": {}}
    with patch.object(SimulatedLeague, '_initialize_teams'), \
         patch.object(SimulatedLeague, '_generate_schedule'):
        league = SimulatedLeague(config, season_folder)
    team = types.SimpleNamespace(projected_pm=_make_bare_pm(), actual_pm=_make_bare_pm())
    league.teams = [team]
    return league, team


class TestPerWeekSwap:
    """Assertions 1 & 2 — real end-to-end swap on the fixture."""

    def test_swap_fires_projection_tracks_loaded_folder(self, season_folder):
        league, team = _make_league_with_bare_teams(season_folder)

        league._load_week_data(1)
        assert _by_id(team.projected_pm, 1).projected_points == [5.0] * 17

        league._load_week_data(2)
        # Changed 5.0 -> 15.0 as N advanced: the value is NOT frozen at one snapshot.
        assert _by_id(team.projected_pm, 1).projected_points == [15.0] * 17

    def test_per_folder_sourcing_projected_and_actual(self, season_folder):
        league, team = _make_league_with_bare_teams(season_folder)

        league._load_week_data(1)
        # projected_pm <- week_01: its own actual for the current week is 0.0 ...
        assert _by_id(team.projected_pm, 1).actual_points[0] == 0.0
        # ... while actual_pm <- week_02 carries the real week-1 result.
        assert _by_id(team.actual_pm, 1).actual_points[0] == WEEK1_ACTUAL

        league._load_week_data(2)
        # actual_pm <- week_03 carries the real week-2 result.
        assert _by_id(team.actual_pm, 1).actual_points[1] == WEEK2_ACTUAL


class TestWinTallyingSourcesActualPm:
    """Assertion 3 — win-tallying reads real actuals via actual_pm, both team types."""

    @patch('simulation.win_rate.DraftHelperTeam.StarterHelperModeManager')
    def test_draft_helper_team_scores_from_actual_pm(self, mock_shm):
        # projected_pm lineup player holds the POST-SWAP current-week value (0.0);
        # the real result must come from actual_pm, proving the D2 redirect.
        proj_player = Mock(spec=FantasyPlayer)
        proj_player.id = 1
        proj_player.actual_points = [0.0] * 17

        starter = Mock()
        starter.player = proj_player
        lineup = Mock()
        lineup.qb = starter
        for slot in ('rb1', 'rb2', 'wr1', 'wr2', 'te', 'flex', 'k', 'dst'):
            setattr(lineup, slot, None)

        shm_instance = Mock()
        shm_instance.optimize_lineup.return_value = lineup
        mock_shm.return_value = shm_instance

        actual_player = Mock(spec=FantasyPlayer)
        actual_player.id = 1
        actual_player.actual_points = [WEEK1_ACTUAL] + [0.0] * 16

        projected_pm = Mock()
        projected_pm.players = [proj_player]
        actual_pm = Mock()
        actual_pm.players = [actual_player]
        actual_pm.calculate_max_weekly_projection.return_value = 100.0

        config = Mock()
        config.current_nfl_week = 1
        team = DraftHelperTeam(projected_pm, actual_pm, config, Mock())

        total = team.set_weekly_lineup(week=1)

        assert total == WEEK1_ACTUAL  # 12.0 from actual_pm, NOT 0.0 from projected_pm

    def test_simulated_opponent_scores_from_actual_pm(self):
        def make_roster_player(pid, position):
            p = Mock(spec=FantasyPlayer)
            p.id = pid
            p.position = position
            p.actual_points = [0.0] * 17  # POST-SWAP projected_pm value for the current week
            return p

        roster = [
            make_roster_player(1, "QB"),
            make_roster_player(2, "RB"), make_roster_player(3, "RB"),
            make_roster_player(5, "WR"), make_roster_player(6, "WR"),
            make_roster_player(8, "TE"),
            make_roster_player(4, "RB"),   # FLEX candidate
            make_roster_player(10, "K"),
            make_roster_player(12, "DST"),
        ]

        actual_players = []
        for p in roster:
            ap = Mock(spec=FantasyPlayer)
            ap.id = p.id
            ap.actual_points = [WEEK1_ACTUAL] + [0.0] * 16  # real week-1 result from week_02
            actual_players.append(ap)

        projected_pm = Mock()
        projected_pm.players = roster
        projected_pm.calculate_max_weekly_projection.return_value = 100.0
        projected_pm.get_weekly_projection.return_value = (10.0, 0.0)
        actual_pm = Mock()
        actual_pm.players = actual_players
        actual_pm.calculate_max_weekly_projection.return_value = 100.0

        config = Mock()
        config.current_nfl_week = 1
        opponent = SimulatedOpponent(
            projected_pm, actual_pm, config, Mock(),
            strategy='projected_points_aggressive',
        )
        opponent.roster = roster

        total = opponent.set_weekly_lineup(week=1)

        # 9 starters, each scored 12.0 from actual_pm (NOT the 0.0 projected_pm value).
        assert total == pytest.approx(9 * WEEK1_ACTUAL)


class TestParserCopiesInSync:
    """D4: the two _parse_players_json copies stay byte-for-byte identical."""

    def test_parse_players_json_copies_byte_for_byte_identical(self):
        src_league = inspect.getsource(SimulatedLeague._parse_players_json)
        src_loader = inspect.getsource(SimDataLoader._parse_players_json)
        assert src_league == src_loader


class TestPreloadCopiesShareOneImplementation:
    """
    T73/D4+R6: the per-week resolve-and-parse block exists exactly once, as the module-level
    load_week_player_data helper. Same inspect.getsource idiom as TestParserCopiesInSync —
    a single implementation cannot be compared against itself, so the pin asserts instead that
    each _preload_all_weeks copy DELEGATES and that neither re-inlines the deleted fabricating
    fallback.
    """

    def test_both_preload_copies_call_the_shared_helper(self):
        for owner in (SimulatedLeague, SimDataLoader):
            src = inspect.getsource(owner._preload_all_weeks)
            assert "load_week_player_data(" in src, f"{owner.__name__} no longer delegates"

    def test_neither_preload_copy_reinlines_the_fabricating_fallback(self):
        for owner in (SimulatedLeague, SimDataLoader):
            src = inspect.getsource(owner._preload_all_weeks)
            assert "actual_data = projected_data" not in src, f"{owner.__name__} re-inlined it"
            assert "Using projected data as fallback" not in src, f"{owner.__name__} re-inlined it"

    def test_shared_helper_raises_when_actual_folder_missing(self, tmp_path):
        weeks_folder = tmp_path / "weeks"
        weeks_folder.mkdir()
        _write_week_folder(weeks_folder, 1)  # week_01 only: week 1's actuals need week_02
        with pytest.raises(FileNotFoundError):
            load_week_player_data(weeks_folder, 1, _make_bare_parser(), Mock())

    def test_shared_helper_returns_none_when_projected_folder_missing(self, tmp_path):
        weeks_folder = tmp_path / "weeks"
        weeks_folder.mkdir()
        assert load_week_player_data(weeks_folder, 5, _make_bare_parser(), Mock()) is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
