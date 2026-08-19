"""
Unit tests for draft_geometry module

Tests the pure draft-geometry reader against D17.3's committed offline replay corpus
(tests/fixtures/espn_api/league_draft/) and constructed LeagueSnapshot fixtures for states
the corpus does not exhibit (duplicate pickOrder, k=1 direction decidability, a
partial-round corruption guard, and a round-boundary reversal). The snake-reversal
coverage runs against the real 10-team corpus grid as well as the constructed 3-team
fixture, by progressively marking step_160.json's pre-allocated picks complete.

Author: Kai Mizuno
"""

import ast
import copy
import json
from pathlib import Path

import pytest

from league_helper.util.draft_geometry import DraftGeometry, read_geometry
from player_data_fetcher.espn_league_snapshot_models import LeagueSnapshot


# FIXTURES

FIXTURE_DIR = Path(__file__).parent.parent.parent / "fixtures" / "espn_api" / "league_draft"


def _load_snapshot(filename: str) -> LeagueSnapshot:
    payload = json.loads((FIXTURE_DIR / filename).read_text())
    return LeagueSnapshot.model_validate(payload)


def _team(team_id: int) -> dict:
    return {"id": team_id}


def _pick(overall: int, player_id: int, team_id: int, round_id: int) -> dict:
    return {
        "overallPickNumber": overall,
        "playerId": player_id,
        "teamId": team_id,
        "roundId": round_id,
        "lineupSlotId": 0,
    }


@pytest.fixture
def step_002_snapshot() -> LeagueSnapshot:
    """Real corpus step: round 1, 2 served rows (k=2), pick 1 complete, pick 2 open."""
    return _load_snapshot("step_002.json")


@pytest.fixture
def step_160_snapshot() -> LeagueSnapshot:
    """Real corpus step: round 1 fully served (k=10), only 3 picks completed overall."""
    return _load_snapshot("step_160.json")


def _corpus_grid_completed_through(overall: int) -> LeagueSnapshot:
    """Real corpus grid (step_160.json), advanced to a chosen point in the draft.

    step_160.json pre-allocates all 160 picks of the real 10-team / 16-round grid with the
    live pickOrder [1, 4, 9, 6, 2, 3, 10, 8, 5, 7] and ESPN's own pre-computed snake
    reversal (round 2's served teamIds are that order reversed). The captured corpus never
    completes round 1 -- only overall picks 1, 5 and 6 are ever filled across all 161 steps
    -- so no captured step reaches a round boundary and `snake_direction == "reverse"` is
    never exercised against real data. This helper marks every row with
    `overallPickNumber <= overall` complete (and every later row sentinel), which advances
    the *same* real grid past a turn without inventing any geometry: teamId, roundId and
    overallPickNumber are the corpus's own values throughout.
    """
    payload = copy.deepcopy(json.loads((FIXTURE_DIR / "step_160.json").read_text()))
    for pick in payload["draftDetail"]["picks"]:
        if pick["overallPickNumber"] <= overall:
            # Distinct per row: LeagueSnapshot rejects duplicate completed playerIds.
            pick["playerId"] = 1_000_000 + pick["overallPickNumber"]
        else:
            pick["playerId"] = -1
    return LeagueSnapshot.model_validate(payload)


@pytest.fixture
def corpus_round_1_complete() -> LeagueSnapshot:
    """Real corpus grid with round 1 (overall 1-10) complete -- current pick is overall 11,
    round 2, which ESPN serves in REVERSE order [7, 5, 8, 10, 3, 2, 6, 9, 4, 1]."""
    return _corpus_grid_completed_through(10)


@pytest.fixture
def corpus_round_2_complete() -> LeagueSnapshot:
    """Real corpus grid with rounds 1-2 (overall 1-20) complete -- current pick is overall
    21, round 3, back to FORWARD order. Team 1 sits at slot 0, so it holds both overall 20
    (last of reverse round 2) and overall 21 (first of forward round 3): the back-to-back
    turn the snake exists to produce."""
    return _corpus_grid_completed_through(20)


@pytest.fixture
def stale_but_consistent_snapshot() -> LeagueSnapshot:
    """Constructed: a SUPERSEDED-but-internally-consistent grid. context.md records the real
    league's pickOrder changing from [1..10] to [1, 4, 9, 6, 2, 3, 10, 8, 5, 7] -- both are
    valid snake orders, so a snapshot carrying the OLD order in both pickOrder and its
    served rows is internally consistent and the parity guard cannot see that it is stale."""
    payload = {
        "draftDetail": {
            "drafted": True,
            "inProgress": True,
            "picks": [_pick(1, 111, 1, 1), _pick(2, -1, 2, 1), _pick(3, -1, 3, 1)],
        },
        "teams": [_team(1), _team(2), _team(3)],
        "settings": {"draftSettings": {"pickOrder": [1, 2, 3]}},
    }
    return LeagueSnapshot.model_validate(payload)


@pytest.fixture
def step_001_snapshot() -> LeagueSnapshot:
    """Real corpus step: picks[] non-empty (1 row), zero rows with playerId == -1 —
    the ALL-SENTINEL boundary (draft-complete / placeholder-lag, indistinguishable)."""
    return _load_snapshot("step_001.json")


@pytest.fixture
def round_boundary_snapshot() -> LeagueSnapshot:
    """Constructed: 3-team draft, round 1 fully complete (forward order [100, 200, 300]),
    round 2 fully served in reverse order [300, 200, 100] with no picks yet completed —
    exercises the round N -> N+1 snake-reversal boundary the real corpus never reaches
    (its round 1 never fully completes across all 161 captured steps)."""
    payload = {
        "draftDetail": {
            "drafted": True,
            "inProgress": True,
            "picks": [
                _pick(1, 111, 100, 1),
                _pick(2, 222, 200, 1),
                _pick(3, 333, 300, 1),
                _pick(4, -1, 300, 2),
                _pick(5, -1, 200, 2),
                _pick(6, -1, 100, 2),
            ],
        },
        "teams": [_team(100), _team(200), _team(300)],
        "settings": {"draftSettings": {"pickOrder": [100, 200, 300]}},
    }
    return LeagueSnapshot.model_validate(payload)


@pytest.fixture
def duplicate_pick_order_snapshot() -> LeagueSnapshot:
    """Constructed: pickOrder carries a duplicate team id. LeagueSnapshot's own models
    enforce no distinctness constraint on pickOrder, so model_validate() accepts this
    payload — the duplicate guard is this reader's own (D7)."""
    payload = {
        "draftDetail": {
            "drafted": True,
            "inProgress": True,
            "picks": [_pick(1, 111, 100, 1), _pick(2, 222, 200, 1), _pick(3, -1, 100, 1)],
        },
        "teams": [_team(100), _team(200)],
        "settings": {"draftSettings": {"pickOrder": [100, 200, 100]}},
    }
    return LeagueSnapshot.model_validate(payload)


@pytest.fixture
def k1_snapshot() -> LeagueSnapshot:
    """Constructed: exactly one served row in the current round (k=1). The real corpus's
    pickOrder is already distinct at every captured step, so no real fixture ever exercises
    a genuine k=1 direction-decidability case; this fixture is the one this AC requires."""
    payload = {
        "draftDetail": {"drafted": True, "inProgress": True, "picks": [_pick(1, -1, 100, 1)]},
        "teams": [_team(100), _team(200), _team(300)],
        "settings": {"draftSettings": {"pickOrder": [100, 200, 300]}},
    }
    return LeagueSnapshot.model_validate(payload)


@pytest.fixture
def field_level_sentinel_snapshot() -> LeagueSnapshot:
    """Constructed: our team (100) has no remaining incomplete pick, but team 200's round-1
    pick is still open — the FIELD-LEVEL sentinel (only picks_until_our_next_turn is None)."""
    payload = {
        "draftDetail": {
            "drafted": True,
            "inProgress": True,
            "picks": [_pick(1, 111, 100, 1), _pick(2, -1, 200, 1)],
        },
        "teams": [_team(100), _team(200), _team(300)],
        "settings": {"draftSettings": {"pickOrder": [100, 200, 300]}},
    }
    return LeagueSnapshot.model_validate(payload)


@pytest.fixture
def corrupt_partial_round_snapshot() -> LeagueSnapshot:
    """Constructed: k=1 served row whose team id (200) matches neither pickOrder[:1]
    ([100]) nor reversed pickOrder[:1] ([300]) — the corruption guard at a partial round."""
    payload = {
        "draftDetail": {"drafted": True, "inProgress": True, "picks": [_pick(1, -1, 200, 1)]},
        "teams": [_team(100), _team(200), _team(300)],
        "settings": {"draftSettings": {"pickOrder": [100, 200, 300]}},
    }
    return LeagueSnapshot.model_validate(payload)


@pytest.fixture
def empty_picks_snapshot() -> LeagueSnapshot:
    """Constructed: picks[] entirely empty — draft not started. Exercises
    LeagueSnapshot.round_count's own inherited ValueError, not a guard this reader adds."""
    payload = {
        "draftDetail": {"drafted": False, "inProgress": False, "picks": []},
        "teams": [_team(100), _team(200), _team(300)],
        "settings": {"draftSettings": {"pickOrder": [100, 200, 300]}},
    }
    return LeagueSnapshot.model_validate(payload)


# TESTS

class TestOurSlotAndCorpusReads:
    """Real committed-corpus reads — the common-path behavior."""

    def test_partial_round_k2_forward(self, step_002_snapshot):
        result = read_geometry(step_002_snapshot, 4)

        assert result == DraftGeometry(
            our_slot=1,
            current_round=1,
            overall_pick_number=2,
            snake_direction="forward",
            picks_until_our_next_turn=0,
        )

    def test_full_round_k10_forward(self, step_160_snapshot):
        result = read_geometry(step_160_snapshot, 1)

        assert result == DraftGeometry(
            our_slot=0,
            current_round=1,
            overall_pick_number=2,
            snake_direction="forward",
            picks_until_our_next_turn=18,
        )

    def test_our_slot_resolved_from_live_payload_not_config(self, step_002_snapshot):
        # our_slot is pickOrder.index(our_team_id), never a config constant — team 9 sits
        # at pickOrder index 2 in this corpus's pickOrder [1, 4, 9, 6, 2, 3, 10, 8, 5, 7].
        result = read_geometry(step_002_snapshot, 9)

        assert result.our_slot == 2


class TestAllSentinelBoundary:
    def test_no_incomplete_pick_anywhere_returns_all_sentinel(self, step_001_snapshot):
        result = read_geometry(step_001_snapshot, 1)

        assert result == DraftGeometry(
            our_slot=0,
            current_round=None,
            overall_pick_number=None,
            snake_direction=None,
            picks_until_our_next_turn=None,
        )


class TestFieldLevelSentinel:
    def test_our_team_done_other_team_still_incomplete(self, field_level_sentinel_snapshot):
        result = read_geometry(field_level_sentinel_snapshot, 100)

        assert result == DraftGeometry(
            our_slot=0,
            current_round=1,
            overall_pick_number=2,
            snake_direction="forward",
            picks_until_our_next_turn=None,
        )


class TestSnakeReversalBoundary:
    def test_round_1_to_2_reversal(self, round_boundary_snapshot):
        result = read_geometry(round_boundary_snapshot, 200)

        assert result == DraftGeometry(
            our_slot=1,
            current_round=2,
            overall_pick_number=4,
            snake_direction="reverse",
            picks_until_our_next_turn=1,
        )

    def test_corpus_round_2_is_reverse_at_slot_0(self, corpus_round_1_complete):
        # Real 10-team corpus grid, round 1 complete. Round 2 is served in reverse order,
        # so team 1 (pickOrder slot 0) picks LAST in it, at overall 20 -- the maximum wait.
        result = read_geometry(corpus_round_1_complete, 1)

        assert result == DraftGeometry(
            our_slot=0,
            current_round=2,
            overall_pick_number=11,
            snake_direction="reverse",
            picks_until_our_next_turn=9,
        )

    def test_corpus_round_2_is_reverse_at_last_slot(self, corpus_round_1_complete):
        # Team 7 is pickOrder[-1], so the reversal hands it the FIRST pick of round 2 --
        # overall 11, the pick that is current. Zero wait.
        result = read_geometry(corpus_round_1_complete, 7)

        assert result == DraftGeometry(
            our_slot=9,
            current_round=2,
            overall_pick_number=11,
            snake_direction="reverse",
            picks_until_our_next_turn=0,
        )

    def test_corpus_round_3_returns_to_forward_at_slot_0(self, corpus_round_2_complete):
        # Rounds 1-2 complete. Round 3 reverts to forward order, and slot 0's overall-20
        # pick (last of reverse round 2) is immediately followed by its overall-21 pick --
        # the back-to-back turn. picks_until_our_next_turn is 0 at both.
        result = read_geometry(corpus_round_2_complete, 1)

        assert result == DraftGeometry(
            our_slot=0,
            current_round=3,
            overall_pick_number=21,
            snake_direction="forward",
            picks_until_our_next_turn=0,
        )

    def test_corpus_round_3_forward_at_last_slot(self, corpus_round_2_complete):
        # The slot-9 counterpart: forward round 3 makes team 7 wait the full 9 picks.
        result = read_geometry(corpus_round_2_complete, 7)

        assert result == DraftGeometry(
            our_slot=9,
            current_round=3,
            overall_pick_number=21,
            snake_direction="forward",
            picks_until_our_next_turn=9,
        )


class TestKEqualsOneDecidability:
    def test_direction_decided_from_single_served_pick(self, k1_snapshot):
        result = read_geometry(k1_snapshot, 100)

        assert result.snake_direction == "forward"
        assert result.current_round == 1
        assert result.overall_pick_number == 1


class TestErrorArms:
    def test_our_team_id_absent_from_pick_order_raises(self, step_002_snapshot):
        with pytest.raises(ValueError, match="not found in pickOrder"):
            read_geometry(step_002_snapshot, 9999)

    def test_duplicate_pick_order_raises(self, duplicate_pick_order_snapshot):
        with pytest.raises(ValueError, match="duplicate team ids"):
            read_geometry(duplicate_pick_order_snapshot, 100)

    def test_corrupt_partial_round_raises(self, corrupt_partial_round_snapshot):
        with pytest.raises(ValueError, match="matches neither"):
            read_geometry(corrupt_partial_round_snapshot, 100)

    def test_empty_picks_raises_inherited_round_count_error(self, empty_picks_snapshot):
        with pytest.raises(ValueError, match="Cannot derive round_count"):
            read_geometry(empty_picks_snapshot, 100)


class TestParityGuardDoesNotEstablishFreshness:
    def test_stale_but_internally_consistent_grid_passes_parity(
        self, stale_but_consistent_snapshot
    ):
        # A stale-but-internally-consistent grid is, by definition, indistinguishable from
        # a fresh one by this guard alone (spike F13b / ticket.md Success Criteria). The
        # fixture carries the league's SUPERSEDED pickOrder [1, 2, 3] in both pickOrder and
        # its served rows, so the guard stays silent...
        result = read_geometry(stale_but_consistent_snapshot, 2)

        assert result.snake_direction == "forward"  # guard did not raise

        # ...and the geometry it returns is WRONG for the real draft, whose live pickOrder
        # is [1, 4, 9, 6, 2, 3, 10, 8, 5, 7] -- there team 2 sits at slot 4, not slot 1.
        # That divergence is precisely what the parity guard cannot observe: it establishes
        # internal consistency, never freshness.
        assert result.our_slot == 1


class TestPurity:
    def test_read_geometry_does_not_mutate_or_carry_state(self, step_002_snapshot):
        before = step_002_snapshot.model_dump()

        first = read_geometry(step_002_snapshot, 4)
        second = read_geometry(step_002_snapshot, 4)

        after = step_002_snapshot.model_dump()
        assert before == after  # input snapshot untouched
        assert first == second  # no hidden state changes the second call's result


class TestNoNetworkOrAsyncio:
    def test_module_imports_only_stdlib_and_the_snapshot_model(self):
        # A structurally-anchored WHITELIST, not a denylist of named strings: it parses the
        # module's imports rather than searching its text, so it cannot be tripped by prose
        # in a docstring and is not blind to the routes it does not happen to name
        # (requests, urllib, http.client, socket, aiohttp, ...). Any new dependency at all
        # fails it, which is the property the unit's "no network call, no client
        # construction, no asyncio" claim actually needs.
        import league_helper.util.draft_geometry as module

        tree = ast.parse(Path(module.__file__).read_text())
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imported.add(node.module)

        # Coverage assertion: proves the parse found imports at all, so the equality below
        # cannot pass vacuously against an empty set.
        assert imported

        assert imported == {
            "dataclasses",
            "typing",
            "player_data_fetcher.espn_league_snapshot_models",
        }

    def test_transitive_imports_reach_no_network_module(self):
        # The whitelist above bounds this module's OWN imports; this bounds what those
        # imports drag in. Importing draft_geometry in a fresh interpreter must not place
        # any network or async transport module into sys.modules.
        import subprocess
        import sys

        probe = (
            "import sys; import league_helper.util.draft_geometry; "
            "forbidden = {'asyncio', 'socket', 'ssl', 'requests', 'urllib.request', "
            "'http.client', 'httpx', 'aiohttp', 'httpcore'}; "
            "print(sorted(forbidden & set(sys.modules)))"
        )
        result = subprocess.run(
            [sys.executable, "-c", probe],
            cwd=Path(__file__).parent.parent.parent.parent,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, result.stderr
        assert result.stdout.strip() == "[]", (
            f"draft_geometry transitively imports network/async modules: {result.stdout}"
        )
