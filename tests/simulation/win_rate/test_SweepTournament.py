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
from simulation.win_rate.SweepTournament import SweepTournament, DEFAULT_EPSILON
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
    """Tests for SweepTournament.run (per-config convergent coordinate ascent)."""

    def test_tunes_every_config_independently(self, tmp_path):
        # Each config's win rate depends on its own draft_order; every config is tuned.
        ev = _evaluator(lambda do, pv: 0.9 if do == [{"s": "2"}] else 0.5)
        t = SweepTournament(ev, _store(tmp_path))
        result = t.run(
            [("s1", [{"s": "1"}]), ("s2", [{"s": "2"}]), ("s3", [{"s": "3"}])],
            _baseline(),
        )
        assert set(result.keys()) == {"s1", "s2", "s3"}
        for entry in result.values():
            assert set(entry.keys()) == {"param_values", "win_rate"}
            assert set(entry["param_values"].keys()) == set(DRAFT_SWEEP_PARAMS)

    def test_sweeps_and_selects_best_value(self, tmp_path):
        # Higher PRIMARY_BONUS -> higher win rate (scaled so each step clears epsilon).
        # Coordinate ascent should converge on the max candidate for PRIMARY_BONUS.
        ev = _evaluator(lambda do, pv: pv["PRIMARY_BONUS"] / 200.0)
        t = SweepTournament(ev, _store(tmp_path))
        result = t.run([("s1", [{"s": "1"}])], _baseline())
        max_candidate = max(generate_candidate_values(_baseline(), 5)["PRIMARY_BONUS"])
        assert result["s1"]["param_values"]["PRIMARY_BONUS"] == max_candidate

    def test_epsilon_gate_blocks_submargin_gain(self, tmp_path):
        # Baseline scores 0.50; every non-baseline candidate scores 0.502 — a 0.002 gain,
        # below default epsilon=0.005, so the strict ε-gate adopts nothing.
        baseline = _baseline()

        def rate_fn(do, pv):
            return 0.50 if pv == baseline else 0.502

        t = SweepTournament(_evaluator(rate_fn), _store(tmp_path))
        result = t.run([("s1", [{"s": "1"}])], baseline)
        assert result["s1"]["param_values"] == baseline

    def test_converges_on_flat_landscape(self, tmp_path):
        # Constant win rate -> no candidate ever beats the best by more than epsilon, so a
        # full pass moves nothing and the loop terminates at the baseline.
        ev = _evaluator(lambda do, pv: 0.6)
        t = SweepTournament(ev, _store(tmp_path))
        result = t.run([("s1", [{"s": "1"}]), ("s2", [{"s": "2"}])], _baseline())
        for entry in result.values():
            assert entry["param_values"] == _baseline()

    def test_records_all_evaluations_to_store(self, tmp_path):
        ev = _evaluator(lambda do, pv: 0.6)
        store = _store(tmp_path)
        t = SweepTournament(ev, store)
        t.run([("s1", [{"s": "1"}]), ("s2", [{"s": "2"}])], _baseline())
        combos = store.get_all_combinations()
        assert len(combos) > 0
        # Both configs were evaluated -> both strategy_ids appear in the store.
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

    def test_default_epsilon_constant_matches_init_default(self, tmp_path):
        # D5: the module constant must be the value used as the __init__ epsilon default,
        # so the driver's fingerprint (built with DEFAULT_EPSILON) and the engine's ε-gate
        # never drift (a drift would spuriously mismatch every resume).
        import inspect
        sig = inspect.signature(SweepTournament.__init__)
        assert sig.parameters["epsilon"].default == DEFAULT_EPSILON
        assert DEFAULT_EPSILON == 0.005

    def test_resume_skips_converged_config(self, tmp_path):
        # A pre-marked converged config is skipped (evaluator not called for it) when resume=True.
        store = _store(tmp_path)
        baseline = _baseline()
        store.mark_config_progress("s1", "converged", baseline, 0.8)
        ev = _evaluator(lambda do, pv: 0.6)
        t = SweepTournament(ev, store)
        result = t.run([("s1", [{"s": "1"}])], baseline, resume=True)
        # Evaluator never called (the only config was skipped).
        assert ev.evaluate.call_count == 0
        # The skipped config's checkpointed best is surfaced in the result map.
        assert result["s1"]["win_rate"] == 0.8
        assert result["s1"]["param_values"] == baseline

    def test_resume_seeds_in_progress_config_from_checkpoint(self, tmp_path):
        # An in_progress config starts coordinate ascent from its checkpointed best_param_values,
        # not from baseline. Seed a non-baseline PRIMARY_BONUS and assert the first evaluated
        # trial carries the seeded value (proving the start point moved).
        store = _store(tmp_path)
        baseline = _baseline()
        seeded = dict(baseline)
        seeded["PRIMARY_BONUS"] = 91
        store.mark_config_progress("s1", "in_progress", seeded, 0.7)
        # Flat landscape so nothing moves -> coordinate ascent converges immediately on the seed.
        ev = _evaluator(lambda do, pv: 0.6)
        t = SweepTournament(ev, store)
        result = t.run([("s1", [{"s": "1"}])], baseline, resume=True)
        # No baseline re-eval: every trial seen by the evaluator carries the seeded PRIMARY_BONUS
        # except where coordinate ascent varies PRIMARY_BONUS itself.
        first_pv = ev.evaluate.call_args_list[0].args[1]
        assert first_pv["PRIMARY_BONUS"] == 91  # seeded start, not baseline 67
        assert result["s1"]["param_values"]["PRIMARY_BONUS"] == 91

    def test_marks_in_progress_then_converged_per_config(self, tmp_path):
        # mark_config_progress is written in_progress then converged for each tuned config.
        store = _store(tmp_path)
        ev = _evaluator(lambda do, pv: 0.6)
        t = SweepTournament(ev, store)
        t.run([("s1", [{"s": "1"}])], _baseline())
        conv = store.get_config_convergence("s1")
        assert conv is not None
        assert conv["status"] == "converged"  # final mark is converged

    def test_resume_false_reproduces_all_from_baseline(self, tmp_path):
        # Regression guard: with resume=False (default), a pre-marked converged config is NOT
        # skipped — every config is re-evaluated from baseline as in the pre-T9 behavior.
        store = _store(tmp_path)
        baseline = _baseline()
        store.mark_config_progress("s1", "converged", baseline, 0.8)
        ev = _evaluator(lambda do, pv: 0.6)
        t = SweepTournament(ev, store)
        t.run([("s1", [{"s": "1"}])], baseline, resume=False)
        # Evaluator WAS called (config not skipped) -> resume=False ignores convergence.
        assert ev.evaluate.call_count > 0
