"""
Tests for the T16/KDD-3 logger-binding fix: SweepTournament and CombinationEvaluator resolve
their logger at call time via get_logger(), so a setup_logger("win_rate_simulation", ...) done
at runtime (after import) governs their output — instead of capturing the stale "default"
logger at import time.

Author: Kai Mizuno
"""

# Standard library
from unittest.mock import Mock, patch

# Local
from simulation.win_rate.SweepTournament import SweepTournament
from simulation.win_rate.SweepResultsManager import SweepResultsManager


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


def _evaluator():
    ev = Mock()
    ev.evaluate.side_effect = lambda do, pv: (6, 10, 0.6)  # flat landscape -> immediate convergence
    return ev


class TestSweepTournamentLoggerBinding:
    """KDD-3: run() resolves the logger at call time, so a runtime-configured logger governs it."""

    def test_run_resolves_logger_at_call_time(self, tmp_path):
        # Patch get_logger at the SweepTournament usage site; assert run() calls it and logs
        # through the returned (configured) logger — proving call-time resolution, not an
        # import-time capture.
        store = SweepResultsManager(tmp_path / "win_rate_sweep_results.json")
        configured_logger = Mock()
        with patch(
            "simulation.win_rate.SweepTournament.get_logger", return_value=configured_logger
        ) as mock_get_logger:
            t = SweepTournament(_evaluator(), store)
            t.run([("s1", [{"s": "1"}])], _baseline())
        mock_get_logger.assert_called()  # resolved at call time inside run()
        # The configured logger received the per-config converged INFO line.
        assert any(
            "converged" in str(c.args[0]) for c in configured_logger.info.call_args_list if c.args
        )

    def test_module_has_no_import_time_logger_global(self):
        # The import-time module global must be gone (it captured the stale "default" logger).
        import simulation.win_rate.SweepTournament as st
        assert not hasattr(st, "logger")


class TestCombinationEvaluatorLoggerBinding:
    """KDD-3: CombinationEvaluator resolves its logger at call time inside __init__."""

    def test_module_has_no_import_time_logger_global(self):
        import simulation.win_rate.CombinationEvaluator as ce
        assert not hasattr(ce, "logger")
