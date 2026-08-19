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
from pydantic import ValidationError as PydanticValidationError
from utils.error_handler import ConfigurationError
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


@pytest.fixture(autouse=True)
def unpatched_seam_is_fatal():
    """Make the module docstring's no-network claim STRUCTURALLY true, not aspirational.

    test_no_test_constructs_an_espn_client is a static scan of THIS file's own source,
    so it is blind to the actual risk shape: a future test calling
    `manager._cockpit_poll(...)` or `_run_cockpit_session()` without wrapping it in
    `patch.object(cockpit_module, "get_league_snapshot_sync", ...)`. That test would
    issue a real ESPN request. This autouse fixture replaces the seam for every test in
    the module with one that raises instead, so reaching it unpatched is a loud test
    failure rather than a live network call. A test that patches the seam itself simply
    patches over this one.
    """
    def _fatal(*args, **kwargs):
        raise AssertionError(
            "unpatched seam reached: a cockpit test tried to call "
            "get_league_snapshot_sync for real"
        )

    with patch.object(cockpit_module, "get_league_snapshot_sync", side_effect=_fatal):
        yield


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

    def test_a_divergent_poll_that_loses_a_rendered_pick_is_ignored(self, manager, capsys):
        # THE SHAPE A PROPER-SUBSET GUARD MISSES. Rendered {1,2,3}; this poll carries
        # {1,2,4} -- a pick we have already shown is GONE and a new one has appeared, so
        # it is neither a subset nor equal. Under `pick_ids < self._rendered_pick_ids` it
        # fell through to the TOTAL reconciliation, which reset pick 3's player to free
        # agent, and the reduced set was then latched as the new baseline so the board
        # could never self-correct. Ownership walking backwards is precisely what the
        # idempotence acceptance criterion forbids.
        #
        # Mutation: restoring `pick_ids < self._rendered_pick_ids` fails this test on
        # BOTH the ownership assertion and the latched-baseline assertion.
        self._poll(manager, _snapshot(3))
        after_advance = {p.id: p.drafted_by for p in manager.player_manager.players}
        assert after_advance[1003] == "Team 3"
        capsys.readouterr()

        rows = [_pick(1, 1001, 1, 1), _pick(2, 1002, 2, 1),
                _pick(3, -1, 3, 1), _pick(4, 1004, 4, 1)]
        rows += [_pick(n, -1, n, 1) for n in range(5, TEAM_COUNT + 1)]
        rows += [_pick(TEAM_COUNT + i + 1, -1, team, 2)
                 for i, team in enumerate(reversed(range(1, TEAM_COUNT + 1)))]
        divergent = LeagueSnapshot.model_validate({
            "draftDetail": {"drafted": True, "inProgress": True, "picks": rows},
            "teams": [{"id": i, "name": f"Team {i}"} for i in range(1, TEAM_COUNT + 1)],
            "settings": {"draftSettings": {"pickOrder": list(range(1, TEAM_COUNT + 1))}},
        })

        terminated = self._poll(manager, divergent)

        out = capsys.readouterr().out
        assert terminated is False
        assert "stale poll ignored" in out
        assert {p.id: p.drafted_by for p in manager.player_manager.players} == after_advance
        assert manager._rendered_pick_ids == frozenset({1, 2, 3})

    def test_a_duplicated_pick_leaves_cockpit_state_byte_identical(self, manager):
        # IDEMPOTENCE SATISFIER (b), asserted AT THE COCKPIT rather than against
        # LeagueSnapshot's validator. The validator is a D18.4 subject and asserting
        # "it raises" says nothing about what the cockpit does with the raise. In
        # production the validation failure surfaces as an ESPNAPIError from the seam,
        # so this drives exactly that and asserts the cockpit's state -- ownership AND
        # the rendered pick set -- is byte-identical to the prior poll.
        self._poll(manager, _snapshot(7))
        before_owners = {p.id: p.drafted_by for p in manager.player_manager.players}
        before_ids = manager._rendered_pick_ids
        assert len([owner for owner in before_owners.values() if owner]) == 7

        with patch.object(cockpit_module, "get_league_snapshot_sync",
                          side_effect=ESPNAPIError(
                              "Duplicate completed playerId(s) in draftDetail.picks[]: [1001]")):
            terminated = manager._cockpit_poll(138260302, 2026, OUR_TEAM_ID)

        assert terminated is True
        assert {p.id: p.drafted_by for p in manager.player_manager.players} == before_owners
        assert manager._rendered_pick_ids == before_ids

    def test_duplicate_completed_player_id_is_rejected_before_the_cockpit_sees_it(self):
        picks = [_pick(1, 1001, 1, 1), _pick(2, 1001, 2, 1)]
        # NARROWED from pytest.raises(Exception): pydantic raises ValidationError, and
        # the broad form would have been satisfied by any failure at all -- a typo in the
        # fixture included. Only the message assertion was doing any work.
        with pytest.raises(PydanticValidationError) as excinfo:
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

        # POSITIVE CONTROL, matching the three sibling AST scans in this file. Without
        # it, `comparisons == [] and conditionals == []` is satisfied by ANY body with no
        # Compare/If node -- including `pass` -- so the test would stay green if the
        # method were gutted. These two assert the scan ran over the real body AND that
        # our_team_id is genuinely present in it, which is what makes the two empties
        # mean "present but never branched on".
        assert "our_team_id" in source
        assert sum(1 for _ in ast.walk(tree)) > 30

        assert comparisons == [], f"reconciliation branches on our own team: {comparisons}"
        assert conditionals == [], f"reconciliation branches on our own team: {conditionals}"

    def test_advanced_poll_reassigns_every_player_totally(self, manager):
        # THE ONE PLACE TOTAL ASSIGNMENT AND A MERGE DIFFER is a player ABSENT from the
        # attribution map, and this test is the only thing pinning it. players[0] (id
        # 1001) IS in the map, so seeding a stale owner there discriminates nothing -- a
        # merge overwrites it identically. players[10] (id 1011) is NOT in _snapshot(7)'s
        # map (it covers 1001..1007), so only a TOTAL assignment resets it to "".
        # Mutation-verified: replacing the loop in
        # _reconcile_ownership_from_snapshot with
        # `if key in attribution: player.drafted_by = attribution[key]` fails THIS test.
        # Before the seed on players[10], that same mutant left all 60 tests in this file
        # green -- the load-bearing line of the unit's idempotence argument was unpinned.
        manager.player_manager.players[0].drafted_by = "Stale Team"
        manager.player_manager.players[10].drafted_by = "Ghost Team"
        assert manager.player_manager.players[10].id == 1011

        self._poll(manager, _snapshot(7))

        drafted = [p for p in manager.player_manager.players if p.drafted_by]
        assert len(drafted) == 7
        assert manager.player_manager.players[0].drafted_by == Constants.FANTASY_TEAM_NAME
        assert manager.player_manager.players[10].drafted_by == "", (
            "a player absent from the attribution map kept a stale owner: the "
            "reconciliation merged rather than assigned totally"
        )
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
        """Drive one poll whose fetch raises; returns (terminated, fetch_mock).

        The fetch mock is RETURNED rather than discarded so a caller can assert the
        call COUNT. Without it, `side_effect=error` makes an implementation that
        retried three times before rendering indistinguishable from one that did not
        retry at all -- both render once and both return True.
        """
        with patch.object(cockpit_module, "get_league_snapshot_sync",
                          side_effect=error) as fetch:
            return manager._cockpit_poll(138260302, 2026, OUR_TEAM_ID), fetch

    def _poll_with(self, manager, snapshot, our_team_id=OUR_TEAM_ID):
        with patch.object(cockpit_module, "get_league_snapshot_sync", return_value=snapshot):
            return manager._cockpit_poll(138260302, 2026, our_team_id)

    def test_espn_api_error_terminates_loudly_and_is_not_retried(self, manager, capsys):
        terminated, fetch = self._poll_raising(manager, ESPNAPIError("auth cookie expired"))

        out = capsys.readouterr().out
        assert terminated is True
        assert "DRAFT MODE STOPPED: " + cockpit_module.ESPN_FAILURE_HEADLINE in out
        assert "ESPNAPIError: auth cookie expired" in out
        assert "espn_s2" in out
        # THE "NOT RETRIED" HALF, which the name promises and nothing else asserted.
        # The transport already exhausted tenacity's attempts before the seam raised, so
        # a second attempt here would silently retry an exhausted failure. Fails on the
        # mutant that wraps the fetch in `for _ in range(3): ...`.
        assert fetch.call_count == 1

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
        # HEADLINE, not just the message body: _render_cockpit_failure prints the
        # exception text under ANY headline, so the substring alone does not separate
        # the geometry arm from the broad `except Exception`. This assertion is what
        # fails on the mutant that moves the broad arm to the front of the fetch try.
        assert cockpit_module.GEOMETRY_FAILURE_HEADLINE in out

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
        # Same reason as test_duplicate_pick_order_entry_terminates: without the
        # headline this passes under the broad arm too.
        assert cockpit_module.GEOMETRY_FAILURE_HEADLINE in out

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

    @pytest.mark.parametrize("headline,action", [
        ("ESPN_FAILURE_HEADLINE", "ESPN_FAILURE_ACTION"),
        ("GEOMETRY_FAILURE_HEADLINE", "GEOMETRY_FAILURE_ACTION"),
        ("OWNERSHIP_FAILURE_HEADLINE", "OWNERSHIP_FAILURE_ACTION"),
        ("UNEXPECTED_FAILURE_HEADLINE", "UNEXPECTED_FAILURE_ACTION"),
    ])
    def test_every_failure_render_names_an_action(self, manager, capsys, headline, action):
        # The name promises ALL FOUR arms. Driving only the ESPN one made this a strict
        # subset of test_espn_api_error_terminates_loudly_and_is_not_retried, which
        # already asserts a fragment of the same action string -- so it added nothing.
        # Parametrized over the real pairing instead: each case fails if its arm is
        # rendered with the wrong action line or with none.
        self._render_failure(manager, headline)

        out = capsys.readouterr().out
        assert getattr(cockpit_module, headline) in out
        assert getattr(cockpit_module, action) in out

    def _render_failure(self, manager, headline):
        """Drive the poll down the arm that renders `headline`."""
        if headline == "ESPN_FAILURE_HEADLINE":
            self._poll_raising(manager, ESPNAPIError("boom"))
        elif headline == "GEOMETRY_FAILURE_HEADLINE":
            self._poll_with(manager, _snapshot(3), our_team_id=99)
        elif headline == "OWNERSHIP_FAILURE_HEADLINE":
            manager.player_manager.players = _pool(2)
            self._poll_with(manager, _snapshot(7))
        else:
            manager.player_manager.load_team = Mock(side_effect=KeyError("WEIGHT"))
            self._poll_with(manager, _snapshot(7))

    def test_an_unexpected_fetch_error_is_rendered_rather_than_crashing_the_cli(self, manager, capsys):
        # D18.5 polish, the STRUCTURAL half. Before the fix the fetch try caught only
        # ESPNAPIError and ValueError, so ANY other type from the seam -- which is the
        # half of the poll that touches the network, the filesystem and the credential
        # store -- escaped _cockpit_poll, unwound through main() and killed the CLI
        # mid-draft with a traceback at exit 1. ConfigurationError is the exact type the
        # user-simulator walked into (user test plan scenario 7, espn_credentials.py:105)
        # and is neither an ESPNAPIError nor a ValueError, so it reaches the new broad
        # arm and nothing else.
        #
        # NOT VACUOUS: with the broad arm removed this exception PROPAGATES out of
        # _poll_raising and the test ERRORS before a single assertion runs -- it cannot
        # pass by its subject being skipped. The three assertions then pin the three
        # things the arm must do: terminate the loop, render the failure block, and name
        # the real exception type rather than a tailored-but-wrong headline.
        error = ConfigurationError("Missing required ESPN credential(s): espn_s2, SWID.")

        terminated, _ = self._poll_raising(manager, error)

        out = capsys.readouterr().out
        assert terminated is True
        assert "DRAFT MODE STOPPED: " + cockpit_module.UNEXPECTED_FAILURE_HEADLINE in out
        assert "ConfigurationError: Missing required ESPN credential(s)" in out
        assert cockpit_module.UNEXPECTED_FAILURE_ACTION in out

    def test_the_specific_fetch_arms_keep_their_headlines_beside_the_broad_one(self, manager, capsys):
        # DISCRIMINATING CONTROL for the test above: the broad arm is placed LAST, so a
        # fetch failure that IS classifiable must still get its tailored headline. A
        # broad arm accidentally placed first would make the test above pass and this
        # one fail, which is what makes the pair meaningful rather than duplicative.
        self._poll_raising(manager, ESPNAPIError("auth cookie expired"))

        out = capsys.readouterr().out
        assert cockpit_module.ESPN_FAILURE_HEADLINE in out
        assert cockpit_module.UNEXPECTED_FAILURE_HEADLINE not in out

    def test_an_unexpected_fetch_error_ends_the_session_instead_of_looping(self, manager, capsys):
        # The same arm one level up: `return True` must actually END the session. An arm
        # that rendered but returned False would scroll the same block every 15s forever.
        # side_effect is a SINGLE-element list deliberately: a second poll would raise
        # StopIteration and fail this test, so "the loop stopped" is proved by the run
        # completing, not merely asserted.
        with patch.object(cockpit_module, "get_league_snapshot_sync",
                          side_effect=[ConfigurationError("no credentials")]), \
             patch.object(cockpit_module.time, "sleep") as sleep:
            manager._run_cockpit_session()

        out = capsys.readouterr().out
        assert cockpit_module.UNEXPECTED_FAILURE_HEADLINE in out
        sleep.assert_not_called()


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
        # This pins the CONTRACT (spec D8): the mode has no local EOFError HANDLER, so
        # one arriving from below PROPAGATES to LeagueHelperManager.main(), which owns
        # the notice and the exit status. It is never masked as a geometry failure and
        # never swallowed by either broad arm. D18.5 polish made this test load-bearing
        # rather than incidental: the fetch try now carries a broad `except Exception`
        # too, and EOFError is an Exception subclass, so the ONLY thing keeping this
        # green is the re-raising `except EOFError` clause deliberately placed above it.
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
    """Draft Mode is entered WITHOUT an ESPN setup: a setup notice, not a traceback.

    TWO setup classes are gated here, and they have DIFFERENT homes: the identity keys
    live in data/configs/league_config.json, the credentials in the process environment
    or a local .env file. The tests below hold each half to its own home, because
    sending an operator to the wrong file is the failure this notice exists to prevent.
    """

    @pytest.fixture(autouse=True)
    def espn_credentials_present(self, monkeypatch):
        """Both credentials set, so an IDENTITY test isolates the identity dimension.

        Placeholders, never a real credential: the pre-flight only ever tests presence,
        so any non-blank value exercises the same path, and no test in this file makes a
        network call. Without this fixture every identity test below would silently
        depend on whatever the developer's own environment happens to carry.
        """
        monkeypatch.setenv("espn_s2", "OFFLINE-PLACEHOLDER-S2")
        monkeypatch.setenv("SWID", "{OFFLINE-PLACEHOLDER-SWID}")

    @pytest.fixture(autouse=True)
    def no_dotenv(self):
        """Neutralize the real .env load, so these tests state what THEY control.

        start_interactive_mode calls load_espn_env() before the pre-flight, which reads
        the repository-root .env -- a file that exists on a developer machine, is absent
        in CI, and is not tracked. Left live, every `monkeypatch.delenv` above would be
        silently undone on a machine whose .env defines espn_s2/SWID, and this class's
        verdicts would depend on the developer's untracked files.

        The load itself is NOT untested by this patch: TestESPNEnvIsLoadedBeforeThe
        Preflight below drives the real call site with the loader patched to a
        controlled side effect, so the wiring is pinned there rather than here.
        """
        with patch.object(cockpit_module, "load_espn_env") as loader:
            yield loader

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

    # D18.5 polish -- the CREDENTIAL half of the pre-flight. Identity was gated from the
    # start; credentials were not, so a user with a configured league and no espn_s2/SWID
    # walked past this notice and died on an unhandled ConfigurationError at exit 1
    # (user test plan scenario 7). These tests gate the adjacent door.

    def test_missing_credentials_are_reported_and_the_session_is_never_entered(
            self, manager, monkeypatch, capsys):
        # NOT VACUOUS: the identity keys are LEFT VALID here, so nothing but the
        # credential check can produce this notice -- and the sibling control
        # test_the_preflight_is_silent_once_the_credentials_are_restored proves the same
        # manager passes the pre-flight the moment the credentials come back. If the
        # credential check were deleted the cockpit would be entered and every assertion
        # below would fail.
        monkeypatch.delenv("espn_s2", raising=False)
        monkeypatch.delenv("SWID", raising=False)

        session = self._enter(manager)

        out = capsys.readouterr().out
        assert cockpit_module.ESPN_CREDENTIAL_HEADLINE in out
        assert "espn_s2 is not set" in out
        assert "SWID is not set" in out
        session.assert_not_called()
        assert "DRAFT MODE - LIVE COCKPIT" not in out
        assert "Traceback" not in out

    def test_the_credential_notice_names_the_environment_not_the_league_config_file(
            self, manager, monkeypatch, capsys):
        # THE POINT OF THE WHOLE HALF. Credentials are read from os.environ / .env and
        # are never written to data/configs/league_config.json, so re-using the identity
        # action line verbatim would send the operator to a file that must not hold them.
        monkeypatch.delenv("espn_s2", raising=False)
        monkeypatch.delenv("SWID", raising=False)

        self._enter(manager)

        out = capsys.readouterr().out
        assert cockpit_module.ESPN_CREDENTIAL_ACTION in out
        assert ".env" in out
        assert "PROCESS ENVIRONMENT" in out
        # The identity action line -- the one that points at the config file as the place
        # to ADD the missing key -- must not appear for a credential-only gap.
        assert cockpit_module.ESPN_CONFIG_ACTION not in out
        assert cockpit_module.ESPN_CONFIG_HEADLINE not in out

    def test_a_single_missing_credential_is_named_alone(self, manager, monkeypatch, capsys):
        # Discriminating: an implementation that reported "credentials are missing"
        # wholesale, without naming WHICH, would fail the second assertion.
        monkeypatch.delenv("SWID", raising=False)

        self._enter(manager)

        out = capsys.readouterr().out
        assert "SWID is not set" in out
        assert "espn_s2 is not set" not in out

    def test_a_blank_credential_counts_as_missing_like_the_credential_reader(
            self, manager, monkeypatch, capsys):
        # The pre-flight must share get_espn_credentials' blank rule, or it would wave a
        # whitespace-only cookie through and the fetch would raise anyway.
        monkeypatch.setenv("espn_s2", "   ")

        self._enter(manager)

        out = capsys.readouterr().out
        assert "espn_s2 is not set" in out

    def test_no_credential_value_is_ever_printed(self, manager, monkeypatch, capsys):
        # Only ONE credential is missing, so the OTHER one's value is in the environment
        # and available to leak. It must not appear in the notice or anywhere on stdout.
        monkeypatch.setenv("espn_s2", "SENTINEL_S2_MUST_NOT_LEAK")
        monkeypatch.delenv("SWID", raising=False)

        self._enter(manager)

        out = capsys.readouterr().out
        assert "SWID is not set" in out
        assert "SENTINEL_S2_MUST_NOT_LEAK" not in out

    def test_missing_identity_and_credentials_are_named_in_one_notice_with_both_homes(
            self, manager, monkeypatch, capsys):
        # A brand-new user has NEITHER. One notice, one pass, both homes named -- the
        # same "not sent round the loop twice" rule the identity half already kept.
        manager.config.espn_league_id = ""
        manager.config.espn_team_id = 0
        monkeypatch.delenv("espn_s2", raising=False)
        monkeypatch.delenv("SWID", raising=False)

        session = self._enter(manager)

        out = capsys.readouterr().out
        assert cockpit_module.ESPN_IDENTITY_AND_CREDENTIAL_HEADLINE in out
        assert out.count(cockpit_module.ESPN_IDENTITY_AND_CREDENTIAL_HEADLINE) == 1
        for named in ("ESPN_LEAGUE_ID is not set", "ESPN_TEAM_ID is not a team id: 0",
                      "espn_s2 is not set", "SWID is not set"):
            assert named in out
        assert cockpit_module.ESPN_CONFIG_ACTION in out
        assert cockpit_module.ESPN_CREDENTIAL_ACTION in out
        session.assert_not_called()

    def test_the_credential_notice_is_distinguishable_from_a_cockpit_failure(
            self, manager, monkeypatch, capsys):
        # Same contract the identity half already keeps: a SETUP gap must not read like
        # the DRAFT MODE STOPPED failure block, and must not crash the CLI. This is the
        # positive statement of what scenario 7 observed the absence of.
        #
        # NON-VACUITY. The three negatives below are all satisfied when the notice is
        # never rendered at all -- _run_cockpit_session is stubbed, so none of those
        # strings can appear on this path under any implementation -- and the bare
        # `"DRAFT MODE" in out` was ALSO satisfied by the cockpit banner
        # "DRAFT MODE - LIVE COCKPIT". So this test survived deleting the credential half
        # of the pre-flight outright (mutation-verified: 7 of its 8 siblings failed and
        # this one did not). The three assertions added below are what make it fail on
        # that mutant, exactly as its identity-side twin already did.
        monkeypatch.delenv("espn_s2", raising=False)
        monkeypatch.delenv("SWID", raising=False)

        session = self._enter(manager)

        out = capsys.readouterr().out
        assert "DRAFT MODE STOPPED" not in out
        assert "!" * 50 not in out
        assert "ConfigurationError" not in out
        assert "DRAFT MODE" in out
        assert cockpit_module.ESPN_CREDENTIAL_HEADLINE in out
        assert "DRAFT MODE - LIVE COCKPIT" not in out
        session.assert_not_called()

    def test_the_preflight_is_silent_once_the_credentials_are_restored(
            self, manager, monkeypatch):
        # NON-VACUITY CONTROL for the credential tests above, stated as a PAIR on one
        # manager: absent -> a problem naming the credential; present -> None. A check
        # that always fired, or one that never fired, breaks one half of this.
        monkeypatch.delenv("espn_s2", raising=False)
        monkeypatch.delenv("SWID", raising=False)
        problem = manager._espn_configuration_error()
        assert problem is not None
        assert problem.headline == cockpit_module.ESPN_CREDENTIAL_HEADLINE
        assert problem.detail == "espn_s2 is not set; SWID is not set"

        monkeypatch.setenv("espn_s2", "OFFLINE-PLACEHOLDER-S2")
        monkeypatch.setenv("SWID", "{OFFLINE-PLACEHOLDER-SWID}")

        assert manager._espn_configuration_error() is None


class TestSharedPlayerStateIsRestoredOnExit:
    """The cockpit hands the SHARED player pool back to disk state on every exit.

    THE DEFECT THIS CLASS EXISTS FOR was silent data loss, not a cosmetic leak.
    PlayerManager is a single instance shared by every mode, and
    _reconcile_ownership_from_snapshot writes drafted_by across ALL of it from the ESPN
    snapshot. The menu loop's reload_player_data() (LeagueHelperManager.py:118) used to
    undo that, because the pre-cutover mode wrote the position files and so changed
    their mtimes -- but this mode deliberately writes nothing, so the mtime check
    short-circuits (PlayerManager.py:489-491) and the ESPN-derived state SURVIVED into
    the menu. The next Modify Player Data write then flushed it to disk, erasing every
    locally-recorded pick ESPN did not show. Entering the cockpit before the ESPN draft
    started was the worst case: an empty attribution map blanked the whole pool.
    """

    @pytest.fixture(autouse=True)
    def espn_setup_present(self, monkeypatch):
        """A usable ESPN setup, so the pre-flight never short-circuits the entry."""
        monkeypatch.setenv("espn_s2", "OFFLINE-PLACEHOLDER-S2")
        monkeypatch.setenv("SWID", "{OFFLINE-PLACEHOLDER-SWID}")

    @pytest.fixture(autouse=True)
    def no_dotenv(self):
        """See TestESPNConfigurationPreflight.no_dotenv -- same hermeticity reason."""
        with patch.object(cockpit_module, "load_espn_env"):
            yield

    def _enter(self, manager, session_effect=None):
        with patch.object(manager, "_run_cockpit_session", side_effect=session_effect):
            manager.start_interactive_mode(manager.player_manager,
                                           Mock(spec=TeamDataManager))

    def test_a_completed_session_forces_a_reload_of_the_shared_pool(self, manager):
        # Mutation: deleting the `finally: self._restore_shared_player_state()` leaves
        # reload_player_data uncalled and fails here. Dropping `force=True` from the
        # call fails the assert_called_once_with -- and force is the ENTIRE point, since
        # an unforced reload short-circuits on the unchanged mtimes this mode guarantees.
        self._enter(manager)

        manager.player_manager.reload_player_data.assert_called_once_with(force=True)

    def test_a_terminated_session_still_forces_the_reload(self, manager):
        # A failure arm returns normally from _run_cockpit_session, so it exits through
        # the same path -- but it is the arm most likely to be forgotten, and it dirties
        # state exactly as much as a completed draft does.
        self._enter(manager, session_effect=None)

        manager.player_manager.reload_player_data.assert_called_once_with(force=True)

    def test_an_exception_unwinding_out_of_the_session_still_forces_the_reload(self, manager):
        # WHY IT IS A `finally` AND NOT A TRAILING CALL. EOFError propagates through
        # start_interactive_mode by contract (main() owns the notice and the exit
        # status), and a trailing call would be skipped on exactly that path.
        with pytest.raises(EOFError):
            self._enter(manager, session_effect=EOFError())

        manager.player_manager.reload_player_data.assert_called_once_with(force=True)

    def test_the_preflight_early_return_pays_for_no_reload(self, manager, monkeypatch):
        # THE SCOPE CLAIM, asserted rather than asserted-in-a-comment: the restore is
        # deliberately inside the session's try/finally and not above the pre-flight,
        # because the pre-flight cannot dirty the pool -- it reads config and the
        # environment and prints. A reload there would cost a full re-read of six
        # position files on every mis-configured entry for nothing.
        monkeypatch.delenv("espn_s2", raising=False)
        monkeypatch.delenv("SWID", raising=False)

        self._enter(manager)

        manager.player_manager.reload_player_data.assert_not_called()


class TestOverCapacityESPNRoster:
    """An ESPN roster the LOCAL slot ladder cannot lay out must not kill the cockpit.

    load_team() builds a FantasyTeam from every player attributed to us and
    FantasyTeam._assign_player_to_slot raises ValueError past the local MAX_POSITIONS.
    The pre-cutover path could not reach that state -- it drafted through can_draft(),
    which returns False rather than raising. Reconciling from ESPN bypasses that gate by
    design, because ESPN already decided what we own; a real draft is constrained by
    ESPN's roster settings, not by data/configs/league_config.json. Uncaught, the
    ValueError reached the render broad arm and TERMINATED the cockpit mid-draft under
    "either a bug or an environment problem" -- none of which is true.
    """

    OVERFLOW = ("Cannot assign Drake Maye (QB) to any available slot. "
                "Slots full: QB=2/2, FLEX=0/1")

    def _poll(self, manager, snapshot):
        with patch.object(cockpit_module, "get_league_snapshot_sync", return_value=snapshot):
            return manager._cockpit_poll(138260302, 2026, OUR_TEAM_ID)

    def test_an_over_capacity_roster_does_not_terminate_the_cockpit(self, manager, capsys):
        # Mutation: removing the `except ValueError` around load_team() sends this
        # straight to the render broad arm -- `terminated` becomes True and
        # UNEXPECTED_FAILURE_HEADLINE appears. Both assertions fail.
        manager.player_manager.load_team = Mock(side_effect=ValueError(self.OVERFLOW))

        terminated = self._poll(manager, _snapshot(7))

        out = capsys.readouterr().out
        assert terminated is False
        assert cockpit_module.UNEXPECTED_FAILURE_HEADLINE not in out
        assert "DRAFT MODE STOPPED" not in out
        assert cockpit_module.ROSTER_OVERFLOW_HEADLINE in out
        assert self.OVERFLOW in out

    def test_ownership_and_the_board_survive_the_degraded_slot_view(self, manager, capsys):
        # The point of continuing: what the operator actually needs -- who owns what,
        # the recent picks, the recommendations -- is all still correct. Only the local
        # roster-by-round LAYOUT is degraded.
        manager.player_manager.load_team = Mock(side_effect=ValueError(self.OVERFLOW))

        self._poll(manager, _snapshot(7))

        out = capsys.readouterr().out
        by_id = {p.id: p.drafted_by for p in manager.player_manager.players}
        assert by_id[1001] == Constants.FANTASY_TEAM_NAME
        assert by_id[1002] == "Team 2"
        assert len([owner for owner in by_id.values() if owner]) == 7
        assert "Recent picks" in out
        assert "Top draft recommendations" in out

    def test_the_notice_is_printed_once_per_session_not_once_per_poll(self, manager, capsys):
        # Reconciliation runs on EVERY non-stale poll, so an unlatched notice would
        # print every 15 seconds and destroy the fixed line height the board's column
        # alignment depends on. Mutation: deleting the `if self._roster_overflow_
        # reported: return` guard makes the count 3.
        manager.player_manager.load_team = Mock(side_effect=ValueError(self.OVERFLOW))

        self._poll(manager, _snapshot(7))
        self._poll(manager, _snapshot(7))
        self._poll(manager, _snapshot(8))

        out = capsys.readouterr().out
        assert out.count(cockpit_module.ROSTER_OVERFLOW_HEADLINE) == 1

    def test_a_re_entered_session_reports_the_overflow_again(self, manager, capsys):
        # The latch's OTHER half. Mutation: deleting the reset in _run_cockpit_session
        # makes the second session silent about a condition that is still true.
        manager.player_manager.load_team = Mock(side_effect=ValueError(self.OVERFLOW))
        self._poll(manager, _snapshot(7))
        capsys.readouterr()

        snapshots = [_snapshot(7), _snapshot(20, in_progress=False)]
        with patch.object(cockpit_module, "get_league_snapshot_sync", side_effect=snapshots), \
             patch.object(cockpit_module.time, "sleep"):
            manager._run_cockpit_session()

        out = capsys.readouterr().out
        assert cockpit_module.ROSTER_OVERFLOW_HEADLINE in out

    def test_a_non_value_error_from_load_team_still_reaches_the_broad_arm(self, manager, capsys):
        # NON-VACUITY CONTROL for the whole class: the catch is ValueError ONLY, so a
        # genuinely unexpected type is still loud and still terminal. A blanket
        # `except Exception` around load_team() would fail this.
        manager.player_manager.load_team = Mock(side_effect=KeyError("WEIGHT"))

        terminated = self._poll(manager, _snapshot(7))

        out = capsys.readouterr().out
        assert terminated is True
        assert cockpit_module.UNEXPECTED_FAILURE_HEADLINE in out
        assert cockpit_module.ROSTER_OVERFLOW_HEADLINE not in out


class TestESPNEnvIsLoadedBeforeThePreflight:
    """Credentials supplied the way this project documents them must actually work.

    load_espn_env() -- the repository's only load_dotenv call site -- had exactly one
    production caller, generate_espn_draft_corpus.py. Nothing on the
    run_league_helper.py -> LeagueHelperManager -> Draft Mode path called it, so the
    pre-flight and get_espn_credentials() both saw the process environment alone. An
    operator whose espn_s2/SWID lived in the repository-root .env -- where
    ESPN_CREDENTIAL_ACTION tells them to put it -- got
    "DRAFT MODE UNAVAILABLE: ESPN credentials are not configured" followed by an action
    line instructing them to do what they had already done.
    """

    def _enter(self, manager):
        with patch.object(manager, "_run_cockpit_session") as session:
            manager.start_interactive_mode(manager.player_manager,
                                           Mock(spec=TeamDataManager))
        return session

    def test_credentials_reaching_the_environment_only_via_dotenv_pass_the_preflight(
            self, manager, monkeypatch, capsys):
        # THE BLOCKING CASE, hermetically. The process environment starts EMPTY of both
        # credentials, and the only thing that supplies them is the loader at its real
        # production call site -- standing in for python-dotenv reading a .env, with a
        # controlled side effect so the test does not depend on an untracked file.
        #
        # Mutation, both directions: deleting the `load_espn_env()` call, OR moving it
        # BELOW `self._espn_configuration_error()`, leaves the pre-flight reading an
        # empty environment -- the credential notice is rendered, the cockpit is never
        # entered, and every assertion below fails.
        monkeypatch.delenv("espn_s2", raising=False)
        monkeypatch.delenv("SWID", raising=False)

        def _load_dotenv_stand_in(*args, **kwargs):
            monkeypatch.setenv("espn_s2", "FROM-DOTENV-S2")
            monkeypatch.setenv("SWID", "{FROM-DOTENV-SWID}")

        with patch.object(cockpit_module, "load_espn_env",
                          side_effect=_load_dotenv_stand_in) as loader:
            session = self._enter(manager)

        out = capsys.readouterr().out
        loader.assert_called_once_with()
        assert cockpit_module.ESPN_CREDENTIAL_HEADLINE not in out
        assert "DRAFT MODE - LIVE COCKPIT" in out
        session.assert_called_once_with()

    def test_the_loader_is_called_with_no_override_so_the_process_environment_wins(
            self, manager, monkeypatch):
        # load_espn_env's `override` defaults to False, so a credential exported into
        # the process environment still beats .env. Passing override=True would silently
        # invert that precedence, so the call must stay argument-free. Mutation:
        # `load_espn_env(override=True)` fails this.
        monkeypatch.setenv("espn_s2", "OFFLINE-PLACEHOLDER-S2")
        monkeypatch.setenv("SWID", "{OFFLINE-PLACEHOLDER-SWID}")

        with patch.object(cockpit_module, "load_espn_env") as loader:
            self._enter(manager)

        loader.assert_called_once_with()

    def test_both_credential_helpers_are_the_seam_re_exports(self):
        # TD1 BINDING #1, pinned as a test rather than left to the plan's W2 grep. The
        # ticket writes it as a bright line: "A unit that imports ESPNClient, httpx, or
        # espn_credentials from inside league_helper/ has violated TD1, not made an
        # implementation choice." A previous polish pass imported
        # missing_espn_credentials straight from espn_credentials and broke it; nothing
        # in the suite noticed. Mutation: restoring that direct import fails
        # test_no_league_helper_module_imports_below_the_seam below.
        from player_data_fetcher import espn_league_snapshot_seam as seam

        assert cockpit_module.load_espn_env is seam.load_espn_env
        assert cockpit_module.missing_espn_credentials is seam.missing_espn_credentials
        assert "load_espn_env" in seam.__all__
        assert "missing_espn_credentials" in seam.__all__

    def test_the_seam_re_exports_rather_than_reimplements(self):
        # SINGLE OWNER. A re-export keeps espn_credentials the one place the .env load,
        # the os.environ read and the blank rule live, so the seam cannot disagree with
        # the read it fronts. A reimplementation in the seam would fail this.
        from player_data_fetcher import espn_credentials, espn_league_snapshot_seam

        assert espn_league_snapshot_seam.load_espn_env is espn_credentials.load_espn_env
        assert (espn_league_snapshot_seam.missing_espn_credentials
                is espn_credentials.missing_espn_credentials)

    def test_no_league_helper_module_imports_below_the_seam(self):
        # The plan's W2 gate, executable. An AST scan over every module under
        # league_helper/ for an import of espn_client, espn_credentials or httpx --
        # the three names TD1 names. Fails on the exact regression a previous polish
        # pass shipped.
        import ast
        from pathlib import Path

        forbidden = {"espn_client", "espn_credentials", "httpx"}
        root = Path(cockpit_module.__file__).resolve().parent.parent
        assert root.name == "league_helper", root

        modules_scanned = 0
        offenders = []
        for path in sorted(root.rglob("*.py")):
            modules_scanned += 1
            tree = ast.parse(path.read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module:
                    named = node.module.split(".")[-1]
                elif isinstance(node, ast.Import):
                    named = None
                    for alias in node.names:
                        if alias.name.split(".")[-1] in forbidden:
                            named = alias.name.split(".")[-1]
                            break
                else:
                    continue
                if named in forbidden:
                    offenders.append(f"{path.relative_to(root)}:{node.lineno}: {named}")

        # Coverage assertion: an empty `offenders` cannot pass vacuously on an empty walk.
        assert modules_scanned > 10, f"only {modules_scanned} modules scanned"
        assert offenders == [], (
            "league_helper/ names the ESPN transport directly (TD1 binding #1): "
            + "; ".join(offenders)
        )
