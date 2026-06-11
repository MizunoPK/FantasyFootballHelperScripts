"""
Tests for simulation.win_rate.SweepTournament.

Unit-only: a mocked CombinationEvaluator returns canned (wins, games, win_rate) keyed
on its inputs (controlling which strategy/value "wins"); a real SweepResultsManager on
tmp_path exercises the store; generate_candidate_values is the committed function.

Author: Kai Mizuno
"""

# Standard library
from unittest.mock import Mock

# Third-party
import pytest

# Local
from simulation.win_rate.SweepTournament import SweepTournament
from simulation.win_rate.SweepResultsManager import SweepResultsManager
from simulation.win_rate.param_value_generation import generate_candidate_values, DRAFT_SWEEP_PARAMS
from utils.error_handler import ConfigurationError


def _baseline():
    return {
        "DRAFT_NORMALIZATION_MAX_SCALE": 150,
        "SAME_POS_BYE_WEIGHT": 0.07,
        "DIFF_POS_BYE_WEIGHT": 0.01,
        "PRIMARY_BONUS": 67,
        "SECONDARY_BONUS": 69,
        "ADP_SCORING_WEIGHT": 4.76,
        "PLAYER_RATING_SCORING_WEIGHT": 3.52,
    }


def _evaluator(rate_fn):
    """Mock evaluator: rate_fn(draft_order, param_values) -> win_rate in [0,1]."""
    ev = Mock()

    def side_effect(draft_order, param_values):
        wr = rate_fn(draft_order, param_values)
        return (int(round(wr * 10)), 10, wr)

    ev.evaluate.side_effect = side_effect
    return ev


def _store(tmp_path, name="win_rate_sweep_results.json"):
    return SweepResultsManager(tmp_path / name)


class TestSweepTournament:
    """Tests for SweepTournament.run."""

    def test_locks_best_strategy(self, tmp_path):
        # s2's draft_order scores highest at baseline.
        ev = _evaluator(lambda do, pv: 0.9 if do == [{"s": "2"}] else 0.5)
        t = SweepTournament(ev, _store(tmp_path))
        result = t.run(
            [("s1", [{"s": "1"}]), ("s2", [{"s": "2"}]), ("s3", [{"s": "3"}])],
            _baseline(),
        )
        assert result["strategy_id"] == "s2"

    def test_sweeps_and_selects_best_value(self, tmp_path):
        # Higher PRIMARY_BONUS -> higher win rate; greedy should keep the max candidate.
        ev = _evaluator(lambda do, pv: pv["PRIMARY_BONUS"] / 200.0)
        t = SweepTournament(ev, _store(tmp_path))
        result = t.run([("s1", [{"s": "1"}])], _baseline())
        max_candidate = max(generate_candidate_values(_baseline(), 5)["PRIMARY_BONUS"])
        assert result["param_values"]["PRIMARY_BONUS"] == max_candidate

    def test_run_returns_converged_best(self, tmp_path):
        ev = _evaluator(lambda do, pv: 0.6)
        t = SweepTournament(ev, _store(tmp_path))
        result = t.run([("s1", [{"s": "1"}])], _baseline())
        assert set(result.keys()) == {"strategy_id", "param_values", "win_rate"}
        assert result["strategy_id"] == "s1"
        assert set(result["param_values"].keys()) == set(DRAFT_SWEEP_PARAMS)

    def test_records_all_evaluations_to_store(self, tmp_path):
        ev = _evaluator(lambda do, pv: 0.6)
        store = _store(tmp_path)
        t = SweepTournament(ev, store)
        t.run([("s1", [{"s": "1"}]), ("s2", [{"s": "2"}])], _baseline())
        combos = store.get_all_combinations()
        assert len(combos) > 0
        # Both strategies were evaluated at baseline -> both appear.
        strategy_ids = {entry["strategy_id"] for entry in combos.values()}
        assert {"s1", "s2"} <= strategy_ids

    def test_rerun_accumulates_in_store(self, tmp_path):
        ev = _evaluator(lambda do, pv: 0.6)
        store = _store(tmp_path)
        t = SweepTournament(ev, store)
        t.run([("s1", [{"s": "1"}])], _baseline())
        t.run([("s1", [{"s": "1"}])], _baseline())
        # At least one combination was evaluated twice across the two runs.
        assert any(entry["total_runs"] >= 2 for entry in store.get_all_combinations().values())

    def test_num_values_controls_candidates(self, tmp_path):
        ev_small = _evaluator(lambda do, pv: 0.6)
        SweepTournament(ev_small, _store(tmp_path, "a.json"), num_values=3).run([("s1", [{"s": "1"}])], _baseline())
        ev_large = _evaluator(lambda do, pv: 0.6)
        SweepTournament(ev_large, _store(tmp_path, "b.json"), num_values=8).run([("s1", [{"s": "1"}])], _baseline())
        assert ev_large.evaluate.call_count > ev_small.evaluate.call_count

    def test_empty_strategies_raises(self, tmp_path):
        ev = _evaluator(lambda do, pv: 0.6)
        t = SweepTournament(ev, _store(tmp_path))
        with pytest.raises(ConfigurationError):
            t.run([], _baseline())
