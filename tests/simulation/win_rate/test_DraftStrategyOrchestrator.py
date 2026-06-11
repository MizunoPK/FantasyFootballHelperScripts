"""
Tests for simulation.win_rate.DraftStrategyOrchestrator's routing through the
shared CombinationEvaluator (behavior parity is covered by the integration/e2e
suites; these confirm the wiring).

Author: Kai Mizuno
"""

# Standard library
import json
from unittest.mock import Mock, patch

# Local
from simulation.win_rate.DraftStrategyOrchestrator import DraftStrategyOrchestrator

MODULE = "simulation.win_rate.DraftStrategyOrchestrator"


def _fake_base_config():
    return {
        "parameters": {
            "DRAFT_NORMALIZATION_MAX_SCALE": 150,
            "SAME_POS_BYE_WEIGHT": 0.07,
            "DIFF_POS_BYE_WEIGHT": 0.01,
            "DRAFT_ORDER_BONUSES": {"PRIMARY": 67, "SECONDARY": 69},
            "ADP_SCORING": {"WEIGHT": 4.76},
            "PLAYER_RATING_SCORING": {"WEIGHT": 3.52},
        }
    }


class TestOrchestratorRouting:
    def test_init_constructs_evaluator_and_extracts_baseline(self, tmp_path):
        with patch(f"{MODULE}.CombinationEvaluator") as MockEval:
            MockEval.return_value.base_config = _fake_base_config()
            orch = DraftStrategyOrchestrator(tmp_path, num_simulations=10, max_workers=2,
                                             meta_data_manager=Mock())
            MockEval.assert_called_once()
            assert orch._evaluator is MockEval.return_value
            assert len(orch._baseline_params) == 7
            assert orch._baseline_params["ADP_SCORING_WEIGHT"] == 4.76

    def test_run_calls_evaluate_per_strategy(self, tmp_path):
        sd = tmp_path / "draft_order_possibilities"
        sd.mkdir()
        for n in (1, 2):
            (sd / f"{n}_t.json").write_text(json.dumps({"name": f"s{n}", "DRAFT_ORDER": []}))

        meta = Mock()
        meta.get_all_strategies.return_value = {}
        with patch(f"{MODULE}.CombinationEvaluator") as MockEval, \
             patch(f"{MODULE}.load_valid_strategies") as MockLoad:
            MockEval.return_value.base_config = _fake_base_config()
            MockEval.return_value.evaluate.return_value = (10, 17, 10 / 17)
            MockLoad.return_value = (
                [("1_t.json", [], "s1"), ("2_t.json", [], "s2")],
                0
            )
            orch = DraftStrategyOrchestrator(tmp_path, num_simulations=10, max_workers=2,
                                             meta_data_manager=meta)
            orch.run()

        assert MockEval.return_value.evaluate.call_count == 2
        assert meta.update.call_count == 2
