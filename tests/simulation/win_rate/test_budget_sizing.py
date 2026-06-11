"""
Tests for simulation.win_rate.budget_sizing.

compute_sizing is pure (numeric inputs); measure_unit_cost is tested with a Mock
evaluator and patched time.monotonic (deterministic, no real timing).

Author: Kai Mizuno
"""

# Standard library
from unittest.mock import Mock, patch

# Third-party
import pytest

# Local
from simulation.win_rate import budget_sizing
from simulation.win_rate.budget_sizing import compute_sizing, measure_unit_cost, MIN_SIMULATIONS
from utils.error_handler import ConfigurationError


class TestBudgetSizing:
    """Tests for compute_sizing and measure_unit_cost."""

    def test_maximizes_simulations_within_budget(self):
        # combinations = 49 + 7*5 = 84; budget 8h; unit_cost small enough to be feasible.
        result = compute_sizing(unit_cost=0.001, num_strategies=49, num_values=5)
        combinations = 49 + 7 * 5
        # num_simulations is the largest that fits.
        assert result["feasible"] is True
        assert result["estimated_seconds"] <= 8 * 3600
        # one more sim would exceed the budget
        assert combinations * (result["num_simulations"] + 1) * 0.001 > 8 * 3600

    def test_num_values_fixed(self):
        result = compute_sizing(unit_cost=0.001, num_strategies=49, num_values=7)
        assert result["num_values"] == 7  # returned unchanged

    def test_infeasible_flagged(self):
        # Huge unit cost -> even MIN_SIMULATIONS over budget.
        result = compute_sizing(unit_cost=10_000.0, num_strategies=49, num_values=5)
        assert result["feasible"] is False
        assert result["num_simulations"] == MIN_SIMULATIONS
        assert result["estimated_seconds"] > 8 * 3600

    def test_respects_min_simulations_floor(self):
        # A budget that allows only a few sims still floors at MIN_SIMULATIONS.
        result = compute_sizing(unit_cost=5.0, num_strategies=49, num_values=5,
                                budget_seconds=1000)
        assert result["num_simulations"] >= MIN_SIMULATIONS

    def test_deterministic(self):
        a = compute_sizing(unit_cost=0.002, num_strategies=49, num_values=5)
        b = compute_sizing(unit_cost=0.002, num_strategies=49, num_values=5)
        assert a == b

    def test_raises_on_bad_inputs(self):
        with pytest.raises(ConfigurationError):
            compute_sizing(unit_cost=0.0, num_strategies=49)
        with pytest.raises(ConfigurationError):
            compute_sizing(unit_cost=0.001, num_strategies=0, num_values=0)

    def test_measure_calls_evaluate_and_divides(self):
        ev = Mock()
        ev.evaluate.return_value = (5, 10, 0.5)
        # Patch time.monotonic to return start=100.0 then end=104.0 -> elapsed 4.0s.
        with patch.object(budget_sizing.time, "monotonic", side_effect=[100.0, 104.0]):
            unit = measure_unit_cost(ev, [{"QB": "P"}], {"PRIMARY_BONUS": 67}, sims_per_eval=2)
        ev.evaluate.assert_called_once()
        assert unit == 2.0  # 4.0s / 2 sims
