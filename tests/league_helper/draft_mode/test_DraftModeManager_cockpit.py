"""
Unit tests for DraftModeManager's live draft cockpit

Covers the poll loop introduced by the draft-cockpit cutover: poll classification
(advanced / unchanged / stale), every outcome the draft-geometry reader can produce
(four ValueError arms and two sentinel states), the four terminal failure arms, the
three idempotence satisfiers, the exact rendered heartbeat / pick-marker / board-context
strings, and the proof that the survival signal is genuinely live rather than merely
wired.

Fully offline: the fetch seam is patched at its DraftModeManager import site in every
test, and a whole-file guard asserts no test can reach the network.

Author: Kai Mizuno
"""

import json
from unittest.mock import Mock, patch

import pytest

from league_helper.draft_mode import DraftModeManager as cockpit_module
from league_helper.draft_mode.DraftModeManager import (
    POLL_INTERVAL_SECONDS,
    RECENT_PICK_WINDOW,
    DraftModeManager,
)
from league_helper.util.ConfigManager import ConfigManager
from league_helper.util.PlayerManager import PlayerManager
from league_helper.util.TeamDataManager import TeamDataManager
from league_helper.util.ScoredPlayer import ScoredPlayer
from league_helper.util.draft_geometry import read_geometry
from league_helper.util.FantasyTeam import FantasyTeam
from player_data_fetcher.espn_client import ESPNAPIError
from player_data_fetcher.espn_league_snapshot_models import LeagueSnapshot
from utils.FantasyPlayer import FantasyPlayer
import league_helper.constants as Constants


# FIXTURES

OUR_TEAM_ID = 1
TEAM_COUNT = 10


def _pick(overall, player_id, team_id, round_id):
    """One draftDetail.picks[] row. lineupSlotId is REQUIRED by the model."""
    return {
        "overallPickNumber": overall,
        "playerId": player_id,
        "teamId": team_id,
        "roundId": round_id,
        "lineupSlotId": 0,
    }


def _snapshot(completed_through, in_progress=True, rounds=2,
              pick_order=None, teams=None):
    """A real 10-team snake board with picks 1..completed_through filled.

    teamId per row follows pickOrder forward in round 1 and reversed in round 2,
    which is what the geometry reader's parity guard requires; a mismatched
    pickOrder length makes it raise on a perfectly healthy-looking fixture.
    """
    order = pick_order if pick_order is not None else list(range(1, TEAM_COUNT + 1))
    picks = []
    overall = 0
    for round_id in range(1, rounds + 1):
        served = order if round_id % 2 == 1 else list(reversed(order))
        for team_id in served:
            overall += 1
            player_id = 1000 + overall if overall <= completed_through else -1
            picks.append(_pick(overall, player_id, team_id, round_id))
    return LeagueSnapshot.model_validate({
        "draftDetail": {"drafted": True, "inProgress": in_progress, "picks": picks},
        "teams": teams if teams is not None else [
            {"id": i, "name": f"Team {i}"} for i in range(1, TEAM_COUNT + 1)
        ],
        "settings": {"draftSettings": {"pickOrder": order}},
    })


def _pool(count=40):
    """A local player pool whose int ids match the snapshot's completed playerIds.

    ADPs run 1.0..40.0 deliberately: against the shipped SURVIVAL_SCORING ladder and a
    picks_until_next_turn of 12, `margin = adp - 12` then spans -11 (EXCELLENT, past the
    -10 threshold) to +28 (VERY_POOR, past +10), so a pool-wide scoring pass reaches BOTH
    extreme tiers rather than sitting entirely in the neutral band -- which is what keeps
    the survival-signal assertions in TestSurvivalSignalIsLive from passing vacuously.
    """
    players = []
    for n in range(1, count + 1):
        players.append(FantasyPlayer(
            id=1000 + n,
            name=f"Player {n}",
            team="NYG",
            position="RB",
            projected_points=[(100.0 - n) / 17.0] * 17,
            average_draft_position=float(n),
        ))
    return players


@pytest.fixture
def config(tmp_path):
    """Real ConfigManager over a tmp league_config.json (no SURVIVAL_SCORING)."""
    data_folder = tmp_path / "data"
    data_folder.mkdir()
    (data_folder / "league_config.json").write_text(json.dumps({
        "config_name": "cockpit test",
        "description": "cockpit test",
        "parameters": _cockpit_parameters(),
    }))
    return ConfigManager(data_folder)


def _cockpit_parameters():
    """The parameter block ConfigManager requires, plus this league's ESPN identity.

    ConfigManager REJECTS a config missing TEAM_QUALITY_SCORING, PERFORMANCE_SCORING or
    MATCHUP_SCORING ("Config missing required parameters", ConfigManager.py:1057), so
    this is not a minimal hand-picked subset -- it mirrors the shape
    tests/league_helper/util/test_player_scoring_survival_estimate.py::_base_parameters
    already establishes for a real-ConfigManager fixture, with DRAFT_ORDER and the ESPN
    identity keys this module additionally needs.
    """
    return {
        "CURRENT_NFL_WEEK": 1,
        "NFL_SEASON": 2026,
        "NFL_SCORING_FORMAT": "ppr",
        "NORMALIZATION_MAX_SCALE": 100.0,
        "DRAFT_NORMALIZATION_MAX_SCALE": 150,
        "SAME_POS_BYE_WEIGHT": 1.0,
        "DIFF_POS_BYE_WEIGHT": 1.0,
        "INJURY_PENALTIES": {"LOW": 0, "MEDIUM": 10, "HIGH": 75},
        "DRAFT_ORDER_BONUSES": {"PRIMARY": 50, "SECONDARY": 30},
        "DRAFT_ORDER": [{"RB": "P", "WR": "S"}],
        "MAX_POSITIONS": {"QB": 2, "RB": 4, "WR": 4, "FLEX": 2, "TE": 1, "K": 1, "DST": 1},
        "FLEX_ELIGIBLE_POSITIONS": ["RB", "WR"],
        "ADP_SCORING": {
            "THRESHOLDS": {"EXCELLENT": 20, "GOOD": 50, "POOR": 100, "VERY_POOR": 150},
            "MULTIPLIERS": {"EXCELLENT": 1.2, "GOOD": 1.1, "POOR": 0.9, "VERY_POOR": 0.7},
            "WEIGHT": 1.0,
        },
        "PLAYER_RATING_SCORING": {
            "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 22},
            "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
            "WEIGHT": 1.0,
        },
        "TEAM_QUALITY_SCORING": {
            "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 5},
            "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
            "WEIGHT": 1.0,
        },
        "PERFORMANCE_SCORING": {
            "MIN_WEEKS": 3,
            "THRESHOLDS": {"BASE_POSITION": 0.0, "DIRECTION": "BI_EXCELLENT_HI", "STEPS": 0.15},
            "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
            "WEIGHT": 1.0,
        },
        "MATCHUP_SCORING": {
            "IMPACT_SCALE": 150.0,
            "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 6},
            "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
            "WEIGHT": 1.0,
        },
        "SCHEDULE_SCORING": {
            "IMPACT_SCALE": 80.0,
            "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 8},
            "MULTIPLIERS": {"EXCELLENT": 1.0, "GOOD": 1.0, "POOR": 1.0, "VERY_POOR": 1.0},
            "WEIGHT": 0.0,
        },
        "ESPN_LEAGUE_ID": "138260302",
        "ESPN_TEAM_ID": OUR_TEAM_ID,
    }


@pytest.fixture
def player_manager(config):
    """A PlayerManager-shaped double over a real player pool.

    score_player is a recording pass-through, NOT a value stub: Step 7 replaces it with
    a real PlayerScoringCalculator delegation so the survival sink runs un-stubbed.
    """
    manager = Mock(spec=PlayerManager)
    manager.config = config
    manager.players = _pool()
    manager.team = Mock(spec=FantasyTeam)
    manager.team.roster = []
    manager.get_roster_len = Mock(return_value=0)
    manager.load_team = Mock()
    manager.get_player_list = Mock(
        side_effect=lambda **kw: [p for p in manager.players if p.is_free_agent()]
    )
    manager.score_player = Mock(
        side_effect=lambda p, **kw: ScoredPlayer(p, p.fantasy_points, reasons=[])
    )
    return manager


@pytest.fixture
def manager(config, player_manager):
    return DraftModeManager(config, player_manager, Mock(spec=TeamDataManager))


@pytest.fixture
def frozen_clock():
    """Freeze the cockpit's wall clock at 12:34:56 for exact-string assertions."""
    with patch.object(cockpit_module, "datetime") as fake:
        fake.now.return_value.strftime.return_value = "12:34:56"
        yield fake


class TestPollClassification:
    """The three poll classes, and the three idempotence satisfiers."""

    def _poll(self, manager, snapshot):
        with patch.object(cockpit_module, "get_league_snapshot_sync", return_value=snapshot):
            return manager._cockpit_poll(138260302, 2026, OUR_TEAM_ID)

    def test_first_poll_renders_the_board_and_records_the_pick_set(self, manager, capsys):
        manager._rendered_pick_ids = None

        terminated = self._poll(manager, _snapshot(7))

        out = capsys.readouterr().out
        assert terminated is False
        assert "LIVE BOARD - pick 8" in out
        # spec D3: the roster-by-round display is RETAINED, not replaced by the board.
        assert "Current Roster by Draft Round:" in out
        assert manager._rendered_pick_ids == frozenset(range(1, 8))

    def test_repeated_identical_poll_renders_a_heartbeat_not_a_re_render(self, manager, capsys):
        snapshot = _snapshot(7)
        self._poll(manager, snapshot)
        capsys.readouterr()

        terminated = self._poll(manager, snapshot)

        out = capsys.readouterr().out
        assert terminated is False
        assert "no change" in out
        assert "Recent picks" not in out
        assert "Top draft recommendations" not in out

    def test_repeated_poll_leaves_ownership_byte_identical(self, manager):
        snapshot = _snapshot(7)
        first_terminated = self._poll(manager, snapshot)
        first = {p.id: p.drafted_by for p in manager.player_manager.players}

        # D18.5 NON-VACUITY GUARD. The equality at the end is evidence of
        # idempotence only if the FIRST poll actually attributed the board. Without these
        # three assertions, a poll that aborted into _cockpit_poll's broad `except
        # Exception` arm leaves every drafted_by empty and the comparison is between two
        # empty results -- green while its whole subject was skipped. 7 is _snapshot(7)'s
        # completed-pick count; 1001 is overall pick 1, which the fixture's pickOrder
        # assigns to OUR team, so the our-team normalization is asserted too.
        assert first_terminated is False
        assert len([owner for owner in first.values() if owner]) == 7
        assert first[1001] == Constants.FANTASY_TEAM_NAME

        second_terminated = self._poll(manager, snapshot)

        assert second_terminated is False
        assert {p.id: p.drafted_by for p in manager.player_manager.players} == first

    def test_out_of_order_poll_is_ignored_and_ownership_does_not_regress(self, manager, capsys):
        self._poll(manager, _snapshot(7))
        after_advance = {p.id: p.drafted_by for p in manager.player_manager.players}
        capsys.readouterr()

        terminated = self._poll(manager, _snapshot(3))

        out = capsys.readouterr().out
        assert terminated is False
        assert "stale poll ignored" in out
        assert {p.id: p.drafted_by for p in manager.player_manager.players} == after_advance
        assert manager._rendered_pick_ids == frozenset(range(1, 8))

    def test_duplicate_completed_player_id_is_rejected_before_the_cockpit_sees_it(self):
        picks = [_pick(1, 1001, 1, 1), _pick(2, 1001, 2, 1)]
        with pytest.raises(Exception) as excinfo:
            LeagueSnapshot.model_validate({
                "draftDetail": {"drafted": True, "inProgress": True, "picks": picks},
                "teams": [{"id": 1, "name": "Team 1"}, {"id": 2, "name": "Team 2"}],
                "settings": {"draftSettings": {"pickOrder": [1, 2]}},
            })
        assert "Duplicate completed playerId" in str(excinfo.value)

    def test_our_picks_and_opponents_follow_the_identical_reconciliation_path(self, manager):
        # unit.md AC: "our picks and opponents' picks follow the same reconciliation
        # path". Asserted behaviourally: one poll, one pass, and BOTH our own pick
        # (overall 1, teamId == OUR_TEAM_ID) and an opponent's (overall 2) are attributed
        # -- neither needs a confirming action and neither takes a different route.
        with patch.object(cockpit_module, "get_league_snapshot_sync", return_value=_snapshot(7)):
            manager._cockpit_poll(138260302, 2026, OUR_TEAM_ID)

        by_id = {p.id: p.drafted_by for p in manager.player_manager.players}
        assert by_id[1001] == Constants.FANTASY_TEAM_NAME
        assert by_id[1002] == "Team 2"
        assert by_id[1007] == "Team 7"

    def test_reconciliation_body_contains_no_our_team_id_comparison(self):
        # The structural half of the same criterion: the reconciliation itself must not
        # branch on whose pick it is. Our team id reaches it only as an argument FORWARDED
        # to the shared attribution owner, which uses it to pick the ownership TOKEN --
        # a naming decision, not a second code path. An AST scan of just this method's
        # body is the assertion; a whole-file text search would match the forwarding call
        # and the docstrings and could never pass.
        import ast
        import inspect
        import textwrap

        # D18.5: dedent is REQUIRED, not decorative. inspect.getsource of a
        # METHOD returns its source at class-body indentation, and ast.parse raises
        # IndentationError: unexpected indent on it. A module-level function needs no
        # dedent -- which is exactly why the peer scan used as this assertion's negative
        # control (normalize_our_team_attribution, a module-level function) ran clean and
        # did not reveal the problem at plan time.
        source = textwrap.dedent(
            inspect.getsource(DraftModeManager._reconcile_ownership_from_snapshot)
        )
        tree = ast.parse(source)
        comparisons = [
            ast.unparse(node)
            for node in ast.walk(tree)
            if isinstance(node, ast.Compare) and "our_team_id" in ast.unparse(node)
        ]
        conditionals = [
            ast.unparse(node.test)
            for node in ast.walk(tree)
            if isinstance(node, ast.If) and "our_team_id" in ast.unparse(node.test)
        ]

        assert comparisons == [], f"reconciliation branches on our own team: {comparisons}"
        assert conditionals == [], f"reconciliation branches on our own team: {conditionals}"

    def test_advanced_poll_reassigns_every_player_totally(self, manager):
        manager.player_manager.players[0].drafted_by = "Stale Team"

        self._poll(manager, _snapshot(7))

        drafted = [p for p in manager.player_manager.players if p.drafted_by]
        assert len(drafted) == 7
        assert manager.player_manager.players[0].drafted_by == Constants.FANTASY_TEAM_NAME
        assert all(p.drafted_by == "" for p in manager.player_manager.players[7:])


class TestNonInteractive:
    """Once the session is entered, nothing reads stdin and nothing is drafted locally."""

    def test_cockpit_source_contains_no_input_call(self):
        import ast
        import inspect

        source = inspect.getsource(cockpit_module)
        tree = ast.parse(source)
        nodes_scanned = 0
        input_calls = []
        for node in ast.walk(tree):
            nodes_scanned += 1
            if isinstance(node, ast.Call) and ast.unparse(node.func) == "input":
                input_calls.append(node.lineno)

        # Coverage assertion: proves the walk actually visited a parsed module, so an
        # empty result cannot pass vacuously on an empty or unparsed source.
        assert nodes_scanned > 100, f"only {nodes_scanned} AST nodes scanned"
        assert input_calls == [], (
            f"DraftModeManager calls input() at line(s) {input_calls}; the cockpit is "
            f"non-interactive after entry."
        )

    def test_poll_never_drafts_locally_or_writes_the_player_file(self, manager):
        with patch.object(cockpit_module, "get_league_snapshot_sync", return_value=_snapshot(7)):
            terminated = manager._cockpit_poll(138260302, 2026, OUR_TEAM_ID)

        # D18.5 NON-VACUITY GUARD. Two assert_not_called()s are satisfied by a
        # poll that did nothing at all -- including one that aborted into the broad
        # `except Exception` arm. These two positive assertions pin that the poll ran to
        # completion and attributed the board FIRST, so the two negatives below are
        # evidence about a poll that actually happened. 7 == _snapshot(7)'s completed
        # picks, observed.
        assert terminated is False
        assert len([p for p in manager.player_manager.players if p.drafted_by]) == 7
        manager.player_manager.draft_player.assert_not_called()
        manager.player_manager.update_players_file.assert_not_called()

    def test_recommendation_render_offers_no_back_to_main_menu_entry(self, manager, capsys):
        with patch.object(cockpit_module, "get_league_snapshot_sync", return_value=_snapshot(7)):
            manager._cockpit_poll(138260302, 2026, OUR_TEAM_ID)

        out = capsys.readouterr().out
        assert "Top draft recommendations" in out
        assert "Back to Main Menu" not in out


class TestHeartbeatRendering:
    """D10's one-line heartbeat, asserted as an exact whole line."""

    def _lines(self, capsys):
        return [line for line in capsys.readouterr().out.splitlines() if line.strip()]

    def test_unchanged_poll_prints_the_exact_heartbeat_line(self, manager, frozen_clock, capsys):
        snapshot = _snapshot(7)
        with patch.object(cockpit_module, "get_league_snapshot_sync", return_value=snapshot):
            manager._cockpit_poll(138260302, 2026, OUR_TEAM_ID)
            capsys.readouterr()
            manager._cockpit_poll(138260302, 2026, OUR_TEAM_ID)

        assert self._lines(capsys) == ["[12:34:56] no change - pick 8, 12 until your turn"]

    def test_heartbeat_omits_the_countdown_at_the_field_level_sentinel(self, manager, frozen_clock, capsys):
        order = [2, 3, 4, 5, 6, 7, 8, 9, 10, 1]
        snapshot = _snapshot(11, pick_order=order)
        with patch.object(cockpit_module, "get_league_snapshot_sync", return_value=snapshot):
            manager._cockpit_poll(138260302, 2026, OUR_TEAM_ID)
            capsys.readouterr()
            manager._cockpit_poll(138260302, 2026, OUR_TEAM_ID)

        line = self._lines(capsys)[0]
        assert line == "[12:34:56] no change - pick 12"
        assert "None" not in line


class TestBoardContext:
    """D11's fixed recent-pick window, on-the-clock line and pick-count countdown."""

    def _render(self, manager, snapshot, capsys):
        geometry = read_geometry(snapshot, OUR_TEAM_ID)
        completed = [p for p in snapshot.draftDetail.picks if p.playerId != -1]
        manager._render_board_context(snapshot, completed, geometry)
        return capsys.readouterr().out

    def test_window_is_exactly_the_configured_size_once_enough_picks_exist(self, manager, capsys):
        out = self._render(manager, _snapshot(7), capsys)

        pick_lines = [line for line in out.splitlines() if line.startswith("Pick ")]
        assert len(pick_lines) == RECENT_PICK_WINDOW
        assert pick_lines[0].startswith("Pick   3:")
        assert pick_lines[-1].startswith("Pick   7:")

    def test_window_shows_the_true_count_and_is_never_padded_when_fewer_exist(self, manager, capsys):
        out = self._render(manager, _snapshot(3), capsys)

        pick_lines = [line for line in out.splitlines() if line.startswith("Pick ")]
        assert len(pick_lines) == 3
        assert "[EMPTY" not in out
        assert "player -1" not in out

    def test_empty_board_says_so_rather_than_rendering_an_empty_window(self, manager, capsys):
        out = self._render(manager, _snapshot(0), capsys)

        assert [line for line in out.splitlines() if line.startswith("Pick ")] == []
        assert "No picks made yet." in out

    def test_on_the_clock_line_names_the_current_pick_and_its_team(self, manager, capsys):
        out = self._render(manager, _snapshot(7), capsys)

        assert "On the clock: pick 8 (round 1) - Team 8" in out

    def test_countdown_is_a_pick_count_with_no_time_unit(self, manager, capsys):
        out = self._render(manager, _snapshot(7), capsys)

        assert "12 until your turn" in out
        for forbidden in ("min", "sec", "~", "minute", "second"):
            assert forbidden not in out, f"countdown leaked a time unit: {forbidden!r}"

    def test_countdown_is_omitted_at_the_field_level_sentinel(self, manager, capsys):
        order = [2, 3, 4, 5, 6, 7, 8, 9, 10, 1]
        out = self._render(manager, _snapshot(11, pick_order=order), capsys)

        assert "until your turn" not in out
        assert "On the clock: pick 12 (round 2) - Team 10" in out


class TestPickLandedMarker:
    """D10's two-line pick marker, and that it replaces the heartbeat."""

    def _advance(self, manager, capsys):
        with patch.object(cockpit_module, "get_league_snapshot_sync", return_value=_snapshot(7)):
            manager._cockpit_poll(138260302, 2026, OUR_TEAM_ID)
        capsys.readouterr()
        with patch.object(cockpit_module, "get_league_snapshot_sync", return_value=_snapshot(8)):
            manager._cockpit_poll(138260302, 2026, OUR_TEAM_ID)
        return capsys.readouterr().out

    def test_pick_landed_prints_the_exact_two_line_marker(self, manager, frozen_clock, capsys):
        out = self._advance(manager, capsys)

        lines = out.splitlines()
        assert "[12:34:56] PICK 8: Player 8 -> Team 8" in lines
        assert "           11 until your turn" in lines

    def test_second_marker_line_aligns_under_PICK(self, manager, frozen_clock, capsys):
        out = self._advance(manager, capsys)

        lines = out.splitlines()
        first = next(line for line in lines if "PICK 8:" in line)
        second = lines[lines.index(first) + 1]
        assert first.index("PICK") == len(second) - len(second.lstrip())

    def test_pick_landed_replaces_the_heartbeat_and_is_followed_by_a_full_render(self, manager, frozen_clock, capsys):
        out = self._advance(manager, capsys)

        assert "no change" not in out
        assert "Recent picks" in out
        assert "Top draft recommendations" in out


class TestSurvivalSignalIsLive:
    """The survival estimate genuinely changes the ranking, through the REAL scorer."""

    SHIPPED_LADDER = {
        "THRESHOLDS": {"EXCELLENT": -10, "GOOD": -3, "POOR": 3, "VERY_POOR": 10},
        "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
        "WEIGHT": 1.0,
    }

    def _manager_with(self, tmp_path, survival_block, name):
        from league_helper.util.player_scoring import PlayerScoringCalculator

        data_folder = tmp_path / name
        data_folder.mkdir()
        params = _cockpit_parameters()
        if survival_block is not None:
            params["SURVIVAL_SCORING"] = survival_block
        (data_folder / "league_config.json").write_text(json.dumps({
            "config_name": name, "description": name, "parameters": params,
        }))
        config = ConfigManager(data_folder)

        season_schedule_manager = Mock()
        season_schedule_manager.get_future_opponents.return_value = []
        inner_player_manager = Mock()
        inner_player_manager.get_projected_points.return_value = None
        calculator = PlayerScoringCalculator(
            config=config,
            player_manager=inner_player_manager,
            max_projection=250.0,
            team_data_manager=Mock(),
            season_schedule_manager=season_schedule_manager,
            current_nfl_week=1,
        )

        pool = _pool()
        pm = Mock(spec=PlayerManager)
        pm.config = config
        pm.players = pool
        pm.team = Mock(spec=FantasyTeam)
        pm.team.roster = []
        pm.get_roster_len = Mock(return_value=0)
        pm.load_team = Mock()
        pm.get_player_list = Mock(side_effect=lambda **kw: list(pool))

        def forward(player, **kwargs):
            # The REAL sink, invoked exactly as PlayerManager.score_player forwards:
            # team_roster positionally, every other argument by keyword.
            return calculator.score_player(player, pm.team.roster, **kwargs)

        pm.score_player = Mock(side_effect=forward)
        return DraftModeManager(config, pm, Mock(spec=TeamDataManager))

    def test_ranking_differs_with_the_survival_key_present_vs_absent(self, tmp_path):
        geometry = read_geometry(_snapshot(7), OUR_TEAM_ID)

        without = self._manager_with(tmp_path, None, "no_survival")
        with_key = self._manager_with(tmp_path, self.SHIPPED_LADDER, "with_survival")

        scores_without = [round(sp.score, 6) for sp in without.get_recommendations(geometry)]
        scores_with = [round(sp.score, 6) for sp in with_key.get_recommendations(geometry)]

        assert scores_without != scores_with, (
            "SURVIVAL_SCORING is on disk and picks_until_next_turn is passed, yet the "
            "scores are identical -- the signal is wired but inert."
        )

    def test_survival_reason_is_emitted_only_with_the_key_present(self, tmp_path):
        geometry = read_geometry(_snapshot(7), OUR_TEAM_ID)

        without = self._manager_with(tmp_path, None, "no_survival_reason")
        with_key = self._manager_with(tmp_path, self.SHIPPED_LADDER, "with_survival_reason")

        reasons_without = " ".join(
            r for sp in without.get_recommendations(geometry) for r in sp.reason
        )
        reasons_with = " ".join(
            r for sp in with_key.get_recommendations(geometry) for r in sp.reason
        )

        assert "Survival:" not in reasons_without
        assert "Survival:" in reasons_with

    def test_the_geometry_value_actually_reaches_the_scorer(self, tmp_path):
        geometry = read_geometry(_snapshot(7), OUR_TEAM_ID)
        with_key = self._manager_with(tmp_path, self.SHIPPED_LADDER, "reaches")

        with_key.get_recommendations(geometry)

        passed = {
            call.kwargs.get("picks_until_next_turn")
            for call in with_key.player_manager.score_player.call_args_list
        }
        assert passed == {geometry.picks_until_our_next_turn}
        assert passed == {12}

    def test_no_geometry_means_no_survival_adjustment(self, tmp_path):
        with_key = self._manager_with(tmp_path, self.SHIPPED_LADDER, "no_geometry")

        with_key.get_recommendations()

        passed = {
            call.kwargs.get("picks_until_next_turn")
            for call in with_key.player_manager.score_player.call_args_list
        }
        assert passed == {None}


class TestFailureArms:
    """Every terminal arm renders loudly, names an action, and stops the session."""

    def _poll_raising(self, manager, error):
        with patch.object(cockpit_module, "get_league_snapshot_sync", side_effect=error):
            return manager._cockpit_poll(138260302, 2026, OUR_TEAM_ID)

    def _poll_with(self, manager, snapshot, our_team_id=OUR_TEAM_ID):
        with patch.object(cockpit_module, "get_league_snapshot_sync", return_value=snapshot):
            return manager._cockpit_poll(138260302, 2026, our_team_id)

    def test_espn_api_error_terminates_loudly_and_is_not_retried(self, manager, capsys):
        terminated = self._poll_raising(manager, ESPNAPIError("auth cookie expired"))

        out = capsys.readouterr().out
        assert terminated is True
        assert "DRAFT MODE STOPPED: " + cockpit_module.ESPN_FAILURE_HEADLINE in out
        assert "ESPNAPIError: auth cookie expired" in out
        assert "espn_s2" in out

    def test_our_team_absent_from_pick_order_terminates(self, manager, capsys):
        terminated = self._poll_with(manager, _snapshot(3), our_team_id=99)

        out = capsys.readouterr().out
        assert terminated is True
        assert cockpit_module.GEOMETRY_FAILURE_HEADLINE in out
        assert "not found in pickOrder" in out

    def test_duplicate_pick_order_entry_terminates(self, manager, capsys):
        snapshot = _snapshot(3, pick_order=[1, 1, 3, 4, 5, 6, 7, 8, 9, 10])

        terminated = self._poll_with(manager, snapshot)

        out = capsys.readouterr().out
        assert terminated is True
        assert "duplicate team ids" in out

    def test_parity_corruption_terminates_and_names_the_traded_pick_case_first(self, manager, capsys):
        # A traded pick makes a team select outside its slot. Simulated by swapping two
        # served teamIds inside a round -- exactly the shape the reader's parity guard
        # cannot distinguish from corruption, which is why the copy leads with it.
        base = _snapshot(3)
        rows = [
            _pick(p.overallPickNumber, p.playerId, p.teamId, p.roundId)
            for p in base.draftDetail.picks
        ]
        rows[4]["teamId"], rows[5]["teamId"] = rows[5]["teamId"], rows[4]["teamId"]
        snapshot = LeagueSnapshot.model_validate({
            "draftDetail": {"drafted": True, "inProgress": True, "picks": rows},
            "teams": [{"id": i, "name": f"Team {i}"} for i in range(1, TEAM_COUNT + 1)],
            "settings": {"draftSettings": {"pickOrder": list(range(1, TEAM_COUNT + 1))}},
        })

        terminated = self._poll_with(manager, snapshot)

        out = capsys.readouterr().out
        assert terminated is True
        assert "matches neither pickOrder prefix" in out
        assert "draft PICK TRADE" in out

    def test_empty_picks_terminates(self, manager, capsys):
        snapshot = LeagueSnapshot.model_validate({
            "draftDetail": {"drafted": False, "inProgress": False, "picks": []},
            "teams": [{"id": 1, "name": "Team 1"}],
            "settings": {"draftSettings": {"pickOrder": [1]}},
        })

        terminated = self._poll_with(manager, snapshot)

        out = capsys.readouterr().out
        assert terminated is True
        assert "empty picks[] list" in out

    def test_unresolvable_player_id_fails_closed_without_mutating_ownership(self, manager, capsys):
        manager.player_manager.players = _pool(2)
        # D18.5: SEEDED, not empty. An unpolled pool has drafted_by == "" for
        # every member, so the `== before` equality at the end would compare two
        # all-empty maps and would hold even if the arm mutated nothing because it never
        # ran. Seeding one non-empty owner makes the equality discriminating: a fail-OPEN
        # implementation that reconciled before raising would blank this value.
        manager.player_manager.players[0].drafted_by = "Stale Team"
        before = {p.id: p.drafted_by for p in manager.player_manager.players}
        assert len([owner for owner in before.values() if owner]) == 1

        terminated = self._poll_with(manager, _snapshot(7))

        out = capsys.readouterr().out
        assert terminated is True
        assert cockpit_module.OWNERSHIP_FAILURE_HEADLINE in out
        assert "have no local player match" in out
        assert {p.id: p.drafted_by for p in manager.player_manager.players} == before

    def test_unexpected_error_is_rendered_loudly_rather_than_escaping(self, manager, capsys):
        manager.player_manager.load_team = Mock(side_effect=KeyError("WEIGHT"))

        terminated = self._poll_with(manager, _snapshot(7))

        out = capsys.readouterr().out
        assert terminated is True
        assert cockpit_module.UNEXPECTED_FAILURE_HEADLINE in out
        assert "KeyError" in out

    def test_every_failure_render_names_an_action(self, manager, capsys):
        self._poll_raising(manager, ESPNAPIError("boom"))

        out = capsys.readouterr().out
        assert cockpit_module.ESPN_FAILURE_ACTION.split(".")[0] in out


class TestSessionLifecycle:
    """Termination, the two sentinel states, cadence, and interrupt ownership."""

    def test_all_sentinel_with_draft_not_in_progress_renders_a_summary_and_ends(self, manager, capsys):
        snapshot = _snapshot(20, in_progress=False)

        with patch.object(cockpit_module, "get_league_snapshot_sync", return_value=snapshot):
            terminated = manager._cockpit_poll(138260302, 2026, OUR_TEAM_ID)

        out = capsys.readouterr().out
        assert terminated is True
        assert "DRAFT COMPLETE" in out
        assert "Recent picks" in out

    def test_all_sentinel_with_draft_in_progress_keeps_polling(self, manager, capsys):
        snapshot = _snapshot(20, in_progress=True)

        with patch.object(cockpit_module, "get_league_snapshot_sync", return_value=snapshot):
            terminated = manager._cockpit_poll(138260302, 2026, OUR_TEAM_ID)

        out = capsys.readouterr().out
        assert terminated is False
        assert "DRAFT COMPLETE" not in out
        assert "waiting for ESPN to serve the current pick" in out
        assert "Top draft recommendations" not in out

    def test_field_level_sentinel_skips_recommendations_but_keeps_the_board(self, manager, capsys):
        order = [2, 3, 4, 5, 6, 7, 8, 9, 10, 1]

        with patch.object(cockpit_module, "get_league_snapshot_sync",
                          return_value=_snapshot(11, pick_order=order)):
            terminated = manager._cockpit_poll(138260302, 2026, OUR_TEAM_ID)

        out = capsys.readouterr().out
        assert terminated is False
        assert "Your draft is complete - no further recommendations." in out
        assert "Top draft recommendations" not in out
        assert "Recent picks" in out

    def test_poll_interval_constant_is_fifteen(self):
        assert POLL_INTERVAL_SECONDS == 15

    def test_session_sleeps_the_constant_once_per_iteration(self, manager):
        snapshots = [_snapshot(3), _snapshot(4), _snapshot(20, in_progress=False)]

        with patch.object(cockpit_module, "get_league_snapshot_sync", side_effect=snapshots), \
             patch.object(cockpit_module.time, "sleep") as sleep:
            manager._run_cockpit_session()

        assert [c.args for c in sleep.call_args_list] == [(POLL_INTERVAL_SECONDS,)] * 2
        assert sleep.call_count == len(snapshots) - 1

    def test_session_does_not_swallow_keyboard_interrupt(self, manager):
        with patch.object(cockpit_module, "get_league_snapshot_sync",
                          side_effect=KeyboardInterrupt), \
             patch.object(cockpit_module.time, "sleep"):
            with pytest.raises(KeyboardInterrupt):
                manager._run_cockpit_session()

    def test_session_does_not_swallow_eof_error(self, manager, capsys):
        # There is no stdin read in the cockpit, so an EOFError cannot ORIGINATE here.
        # This pins the CONTRACT (spec D8): the mode has no local EOFError clause, so one
        # arriving from below PROPAGATES to LeagueHelperManager.main(), which owns the
        # notice and the exit status. It is never masked as a geometry failure and never
        # swallowed by the broad arm, which guards only the render/score path BELOW the
        # fetch call.
        with patch.object(cockpit_module, "get_league_snapshot_sync", side_effect=EOFError), \
             patch.object(cockpit_module.time, "sleep"):
            with pytest.raises(EOFError):
                manager._run_cockpit_session()

        out = capsys.readouterr().out
        assert cockpit_module.UNEXPECTED_FAILURE_HEADLINE not in out
        assert cockpit_module.GEOMETRY_FAILURE_HEADLINE not in out


class TestOfflineGuards:
    """This module never touches the network and carries no live_api marker."""

    def test_module_declares_no_live_api_marker(self):
        # AST over DECORATORS, not a text search for the marker name -- a text search
        # would match this very test's own source and could never pass.
        import ast
        import inspect

        source = inspect.getsource(__import__(__name__, fromlist=["_"]))
        tree = ast.parse(source)
        marked = [
            node.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.ClassDef))
            for decorator in node.decorator_list
            if "live_api" in ast.unparse(decorator)
        ]
        definitions_scanned = sum(
            1 for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.ClassDef))
        )

        # Coverage assertion: an empty `marked` cannot pass vacuously on an empty parse.
        assert definitions_scanned > 20, f"only {definitions_scanned} definitions scanned"
        assert marked == [], f"live_api-marked definitions in an offline module: {marked}"

    def test_no_test_constructs_an_espn_client(self):
        import ast
        import inspect

        source = inspect.getsource(__import__(__name__, fromlist=["_"]))
        tree = ast.parse(source)
        nodes_scanned = 0
        offenders = []
        for node in ast.walk(tree):
            nodes_scanned += 1
            if isinstance(node, ast.Call) and ast.unparse(node.func) in {
                "ESPNClient", "httpx.AsyncClient", "asyncio.run",
                "get_league_snapshot_sync",
            }:
                offenders.append(f"line {node.lineno}: {ast.unparse(node.func)}")

        assert nodes_scanned > 100, f"only {nodes_scanned} AST nodes scanned"
        assert offenders == [], (
            "A cockpit test would issue a real ESPN call: " + "; ".join(offenders)
        )


class TestESPNConfigurationPreflight:
    """Draft Mode is entered WITHOUT an ESPN identity: a setup notice, not a traceback."""

    def _enter(self, manager):
        """Enter Draft Mode with the session loop stubbed; returns the stub."""
        with patch.object(manager, "_run_cockpit_session") as session:
            manager.start_interactive_mode(manager.player_manager, Mock(spec=TeamDataManager))
        return session

    def test_unset_league_id_is_reported_and_the_session_is_never_entered(self, manager, capsys):
        manager.config.espn_league_id = ""

        session = self._enter(manager)

        out = capsys.readouterr().out
        assert cockpit_module.ESPN_CONFIG_HEADLINE in out
        assert "ESPN_LEAGUE_ID is not set" in out
        assert "data/configs/league_config.json" in out
        session.assert_not_called()

    def test_malformed_league_id_is_reported_as_invalid_rather_than_missing(self, manager, capsys):
        manager.config.espn_league_id = "138260302x"

        session = self._enter(manager)

        out = capsys.readouterr().out
        assert "ESPN_LEAGUE_ID is not a league number: '138260302x'" in out
        assert "ESPN_LEAGUE_ID is not set" not in out
        session.assert_not_called()

    def test_unset_team_id_is_caught_too_rather_than_misread_as_a_geometry_failure(self, manager, capsys):
        # The QUIETER half of the same gap: 0 is ConfigManager's default for an absent
        # ESPN_TEAM_ID, it survives int() and reaches read_geometry, which raises
        # "not found in pickOrder" -- rendered by the poll loop as a GEOMETRY failure
        # whose copy talks about traded picks and corrupt boards. Pre-flight names the key.
        manager.config.espn_team_id = 0

        session = self._enter(manager)

        out = capsys.readouterr().out
        assert "ESPN_TEAM_ID is not a team id: 0" in out
        assert cockpit_module.GEOMETRY_FAILURE_HEADLINE not in out
        session.assert_not_called()

    def test_both_unset_keys_are_named_in_one_notice(self, manager, capsys):
        manager.config.espn_league_id = ""
        manager.config.espn_team_id = 0

        session = self._enter(manager)

        out = capsys.readouterr().out
        assert "ESPN_LEAGUE_ID is not set" in out
        assert "ESPN_TEAM_ID is not a team id: 0" in out
        assert out.count(cockpit_module.ESPN_CONFIG_HEADLINE) == 1
        session.assert_not_called()

    def test_the_notice_is_distinguishable_from_a_cockpit_failure(self, manager, capsys):
        manager.config.espn_league_id = ""

        self._enter(manager)

        out = capsys.readouterr().out
        # A cockpit failure says DRAFT MODE STOPPED inside a "!" rule and prints an
        # exception type. This is none of those -- and it still carries the "DRAFT MODE"
        # token tests/integration/test_league_helper_e2e.py asserts on stdout.
        assert "DRAFT MODE STOPPED" not in out
        assert "!" * 50 not in out
        assert "ValueError" not in out
        assert "DRAFT MODE" in out
        assert "DRAFT MODE - LIVE COCKPIT" not in out

    def test_a_configured_league_enters_the_session_normally(self, manager, capsys):
        # NON-VACUITY CONTROL for all five above: with the fixture's real 138260302 /
        # team 1 the pre-flight is silent and the cockpit is entered.
        assert manager._espn_configuration_error() is None

        session = self._enter(manager)

        out = capsys.readouterr().out
        assert cockpit_module.ESPN_CONFIG_HEADLINE not in out
        assert "DRAFT MODE - LIVE COCKPIT" in out
        session.assert_called_once_with()
