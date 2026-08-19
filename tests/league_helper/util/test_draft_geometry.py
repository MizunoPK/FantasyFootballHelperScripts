"""
Unit tests for draft_geometry module

Tests the pure draft-geometry reader against D17.3's committed offline replay corpus
(tests/fixtures/espn_api/league_draft/) and constructed LeagueSnapshot fixtures for states
the corpus does not exhibit (duplicate pickOrder, k=1 direction decidability, a
partial-round corruption guard, and a round-boundary reversal).

Author: Kai Mizuno
"""

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
    def test_stale_but_internally_consistent_grid_passes_parity(self, step_002_snapshot):
        # A stale-but-internally-consistent grid is, by definition, indistinguishable from
        # a fresh one by this guard alone (spike F13b / ticket.md Success Criteria) — this
        # test documents that the guard's silence is expected, not a gap: it asserts the
        # same fixture used elsewhere as "fresh" raises nothing, because staleness is not a
        # property the served-team-id comparison can observe.
        read_geometry(step_002_snapshot, 4)  # does not raise


class TestPurity:
    def test_read_geometry_does_not_mutate_or_carry_state(self, step_002_snapshot):
        before = step_002_snapshot.model_dump()

        first = read_geometry(step_002_snapshot, 4)
        second = read_geometry(step_002_snapshot, 4)

        after = step_002_snapshot.model_dump()
        assert before == after  # input snapshot untouched
        assert first == second  # no hidden state changes the second call's result


class TestNoNetworkOrAsyncio:
    def test_module_imports_no_network_or_asyncio_symbols(self):
        import league_helper.util.draft_geometry as module

        source = Path(module.__file__).read_text()
        assert "asyncio" not in source
        assert "httpx" not in source
        assert "espn_client" not in source
