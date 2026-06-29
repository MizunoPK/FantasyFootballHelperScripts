"""
Unit tests for SimulatedLeague deterministic seeding (T29: deterministic-seeding).

Covers:
(a) same-seed reproducibility: same seed -> identical RNG state and draws.
(c) different-seed divergence: distinct seeds produce distinct draws.
(f) entropy default: no seed -> stochastic behavior preserved (runs differ).
Site routing:
  - site #1 (_initialize_teams strategy shuffle) advances self._rng.
  - site #2 (run_draft draft-order shuffle) advances self._rng.
  - site #3 (SimulatedOpponent._apply_human_error) uses league._rng (naive mode only).

Uses real committed data from simulation/sim_data/2025/ following the pattern of
test_SimulatedLeague_composition.py. Exercises both self-play and naive-opponents
compositions so all 3 random.* sites are reachable.

Author: Kai Mizuno
"""

import random
from pathlib import Path

import pytest

from league_helper.util.ConfigManager import ConfigManager
from simulation.win_rate.SimulatedLeague import SimulatedLeague
from simulation.win_rate.SimulatedOpponent import SimulatedOpponent


# FIXTURES

REAL_DATA_FOLDER = Path("simulation/sim_data/2025")


@pytest.fixture
def base_config_dict():
    """Full reference config dict (merged ConfigManager shape, as CombinationEvaluator builds it)."""
    cm = ConfigManager(Path("data"))
    return {
        "config_name": cm.config_name,
        "description": cm.description,
        "parameters": dict(cm.parameters),
    }


# HELPERS

def _make_league(config, seed=None, naive=False):
    """Construct a SimulatedLeague, returning it for use in a try/finally block."""
    return SimulatedLeague(config, REAL_DATA_FOLDER, seed=seed, naive_opponents=naive)


class TestSameSeedReproducibility:
    """(a) same seed -> identical RNG state and draws (self-play and naive compositions)."""

    def test_same_seed_yields_same_rng_state_self_play(self, base_config_dict):
        """Two leagues with identical seeds are in identical RNG state after init (self-play)."""
        league1 = league2 = None
        try:
            league1 = _make_league(base_config_dict, seed=42)
            league2 = _make_league(base_config_dict, seed=42)
            # Same seed -> same sequence; next random() draw is identical.
            assert league1._rng.random() == league2._rng.random()
        finally:
            for lg in (league1, league2):
                if lg is not None:
                    lg.cleanup()

    def test_same_seed_yields_same_rng_state_naive(self, base_config_dict):
        """Same seed -> identical RNG state after init (naive-opponents; exercises site #3 path)."""
        league1 = league2 = None
        try:
            league1 = _make_league(base_config_dict, seed=7, naive=True)
            league2 = _make_league(base_config_dict, seed=7, naive=True)
            assert league1._rng.random() == league2._rng.random()
        finally:
            for lg in (league1, league2):
                if lg is not None:
                    lg.cleanup()

    def test_same_seed_yields_same_draft_order(self, base_config_dict):
        """Same seed -> same shuffled draft order after run_draft (site #2)."""
        league1 = league2 = None
        try:
            league1 = _make_league(base_config_dict, seed=99)
            league2 = _make_league(base_config_dict, seed=99)
            league1.run_draft()
            league2.run_draft()
            # Compare draft slot order by team index within each league's teams list.
            order1 = [league1.teams.index(t) for t in league1.draft_order]
            order2 = [league2.teams.index(t) for t in league2.draft_order]
            assert order1 == order2
        finally:
            for lg in (league1, league2):
                if lg is not None:
                    lg.cleanup()


class TestSiteRoutingThroughLeagueRng:
    """Verify sites #1 and #2 consume draws from self._rng, not the global random module."""

    def test_initialize_teams_site1_advances_rng_by_one_shuffle_of_10(self, base_config_dict):
        """_initialize_teams calls self._rng.shuffle(strategies) on 10 items (site #1).

        After init, league._rng is in the same state as a fresh Random(seed) that has
        also done exactly one shuffle of a 10-item list — if and only if site #1 routes
        through self._rng (not the global random module).
        """
        seed = 5
        # Reference: advance a clean Random(seed) by one 10-item shuffle.
        reference_rng = random.Random(seed)
        reference_rng.shuffle(list(range(10)))
        reference_next = reference_rng.random()

        league = None
        try:
            league = _make_league(base_config_dict, seed=seed)
            # league._rng should be in the same post-one-shuffle-of-10 state.
            assert league._rng.random() == reference_next
        finally:
            if league is not None:
                league.cleanup()

    def test_run_draft_site2_keeps_rngs_in_sync_across_same_seed_leagues(self, base_config_dict):
        """run_draft calls self._rng.shuffle(draft_order) (site #2), keeping seeded leagues in sync."""
        seed = 17
        league1 = league2 = None
        try:
            league1 = _make_league(base_config_dict, seed=seed)
            league2 = _make_league(base_config_dict, seed=seed)
            league1.run_draft()
            league2.run_draft()
            # Both used the same seeded RNG for the draft shuffle; next draw is identical.
            assert league1._rng.random() == league2._rng.random()
        finally:
            for lg in (league1, league2):
                if lg is not None:
                    lg.cleanup()


class TestNaiveOpponentsRngForwarding:
    """site #3: SimulatedOpponent._apply_human_error receives the league's RNG in naive mode."""

    def test_simulated_opponents_hold_league_rng_reference(self, base_config_dict):
        """Every SimulatedOpponent in naive mode holds a reference to the league's self._rng."""
        league = None
        try:
            league = _make_league(base_config_dict, seed=3, naive=True)
            opponents = [t for t in league.teams if isinstance(t, SimulatedOpponent)]
            assert len(opponents) > 0, "naive mode must produce at least one SimulatedOpponent"
            for opp in opponents:
                assert opp._rng is league._rng, (
                    f"SimulatedOpponent with strategy={opp.strategy!r} does not hold "
                    "a reference to league._rng (site #3 not wired)"
                )
        finally:
            if league is not None:
                league.cleanup()


class TestDifferentSeedDivergence:
    """(c) distinct seeds produce distinct draws (with overwhelming probability)."""

    def test_different_seeds_diverge_after_init(self, base_config_dict):
        """Two leagues with different seeds are in different RNG states after init."""
        league1 = league2 = None
        try:
            league1 = _make_league(base_config_dict, seed=1)
            league2 = _make_league(base_config_dict, seed=2)
            draws1 = [league1._rng.random() for _ in range(10)]
            draws2 = [league2._rng.random() for _ in range(10)]
            assert draws1 != draws2, "Different seeds should produce different draw sequences"
        finally:
            for lg in (league1, league2):
                if lg is not None:
                    lg.cleanup()


class TestEntropyDefault:
    """(f) no seed -> OS entropy -> stochastic: repeated instances differ with overwhelming probability."""

    def test_unseeded_leagues_have_different_rng_states(self, base_config_dict):
        """Two leagues constructed with no seed are in different RNG states (entropy default, D3)."""
        league1 = league2 = None
        try:
            league1 = _make_league(base_config_dict)  # no seed
            league2 = _make_league(base_config_dict)  # no seed
            draws1 = [league1._rng.random() for _ in range(5)]
            draws2 = [league2._rng.random() for _ in range(5)]
            # Collision probability over 5 draws from independent entropy-seeded RNGs is negligible.
            assert draws1 != draws2, (
                "Unseeded leagues should have different RNG states (entropy default, D3). "
                "If this fails spuriously, re-run — probability is ~2^-160."
            )
        finally:
            for lg in (league1, league2):
                if lg is not None:
                    lg.cleanup()
