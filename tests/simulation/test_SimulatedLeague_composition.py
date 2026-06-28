"""
Unit Tests for SimulatedLeague opponent composition (self-play default vs naive flag).

Covers D1/D2: the DEFAULT SimulatedLeague composition is self-play (10 DraftHelperTeams,
no SimulatedOpponents), and naive_opponents=True selects the legacy naive field
(1 DraftHelperTeam + 9 SimulatedOpponents with the 2/2/2/3 strategy distribution).

Like test_SimulatedLeague_measured.py, these tests run the REAL _initialize_teams against the
committed simulation/sim_data/2025/ data, so they do NOT patch _initialize_teams. They assert
COMPOSITION ONLY (team types/counts) — no win-rate magnitude — so they stay deterministic and
fast in the always-green offline suite. The ~0.50 baseline-band check is an agent-as-user
Phase-6 measurement, not an offline unit test (D3).

Author: Kai Mizuno
"""

from collections import Counter
from pathlib import Path

import pytest

from league_helper.util.ConfigManager import ConfigManager
from simulation.win_rate.SimulatedLeague import SimulatedLeague
from simulation.win_rate.DraftHelperTeam import DraftHelperTeam
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


class TestDefaultCompositionIsSelfPlay:
    """D1: the default opponent composition is self-play — 10 DraftHelperTeams, 0 SimulatedOpponents."""

    def test_default_league_is_ten_draft_helper_teams(self, base_config_dict):
        # Arrange / Act: default construction (no naive_opponents -> self-play).
        league = None
        try:
            league = SimulatedLeague(base_config_dict, REAL_DATA_FOLDER)

            # Assert: 10 teams, all DraftHelperTeam, no SimulatedOpponent.
            assert len(league.teams) == 10
            assert all(isinstance(t, DraftHelperTeam) for t in league.teams)
            assert not any(isinstance(t, SimulatedOpponent) for t in league.teams)
            assert league.draft_helper_team is not None
        finally:
            if league is not None:
                league.cleanup()


class TestNaiveOpponentsFlagSelectsNaiveField:
    """D2: naive_opponents=True selects the legacy 1 DraftHelperTeam + 9 SimulatedOpponents field."""

    def test_naive_opponents_true_uses_naive_distribution(self, base_config_dict):
        # Arrange / Act
        league = None
        try:
            league = SimulatedLeague(base_config_dict, REAL_DATA_FOLDER, naive_opponents=True)

            draft_helpers = [t for t in league.teams if isinstance(t, DraftHelperTeam)]
            opponents = [t for t in league.teams if isinstance(t, SimulatedOpponent)]

            # Assert: 10 teams = 1 DraftHelperTeam + 9 SimulatedOpponents.
            assert len(league.teams) == 10
            assert len(draft_helpers) == 1
            assert len(opponents) == 9

            # The opponents reproduce the original 2/2/2/3 strategy distribution.
            distribution = Counter(o.strategy for o in opponents)
            assert distribution == {
                'adp_aggressive': 2,
                'projected_points_aggressive': 2,
                'adp_with_draft_order': 2,
                'projected_points_with_draft_order': 3,
            }
        finally:
            if league is not None:
                league.cleanup()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
