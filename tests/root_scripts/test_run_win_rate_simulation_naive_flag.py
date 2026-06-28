"""
Unit tests for the --naive-opponents CLI flag and its threading into the simulation chain.

Covers D2's CLI surface: --naive-opponents parses to args.naive_opponents (store_true; absent ->
False), and main() threads args.naive_opponents into DraftStrategyOrchestrator. The deeper
engine-chain threading (orchestrator -> evaluator -> runner -> SimulatedLeague) is covered by the
per-link unit tests in test_DraftStrategyOrchestrator.py / test_CombinationEvaluator.py /
test_ParallelLeagueRunner.py. Composition/wiring only — no win-rate magnitude (D3).

Author: Kai Mizuno
"""
from unittest.mock import MagicMock, patch

from run_win_rate_simulation import _build_parser, main


class TestNaiveOpponentsFlagParsing:
    """--naive-opponents is a store_true flag defaulting to False."""

    def test_naive_opponents_default_is_false(self):
        args = _build_parser().parse_args([])
        assert args.naive_opponents is False

    def test_naive_opponents_store_true(self):
        args = _build_parser().parse_args(["--naive-opponents"])
        assert args.naive_opponents is True


class TestNaiveOpponentsThreadsToOrchestrator:
    """main() passes args.naive_opponents into DraftStrategyOrchestrator (strategy mode)."""

    def test_flag_true_threads_naive_opponents_true(self, tmp_path):
        with (
            patch("sys.argv", ["prog", "--naive-opponents", "--data", str(tmp_path)]),
            patch("run_win_rate_simulation.setup_logger"),
            patch("run_win_rate_simulation.get_logger") as mock_get_logger,
            patch("run_win_rate_simulation.WinRateMetaDataManager") as mock_mdm_cls,
            patch("run_win_rate_simulation.DraftStrategyOrchestrator") as mock_orch_cls,
        ):
            mock_get_logger.return_value = MagicMock()
            mock_mdm_cls.return_value.get_all_strategies.return_value = {}
            main()
            assert mock_orch_cls.call_args.kwargs["naive_opponents"] is True

    def test_flag_absent_threads_naive_opponents_false(self, tmp_path):
        with (
            patch("sys.argv", ["prog", "--data", str(tmp_path)]),
            patch("run_win_rate_simulation.setup_logger"),
            patch("run_win_rate_simulation.get_logger") as mock_get_logger,
            patch("run_win_rate_simulation.WinRateMetaDataManager") as mock_mdm_cls,
            patch("run_win_rate_simulation.DraftStrategyOrchestrator") as mock_orch_cls,
        ):
            mock_get_logger.return_value = MagicMock()
            mock_mdm_cls.return_value.get_all_strategies.return_value = {}
            main()
            assert mock_orch_cls.call_args.kwargs["naive_opponents"] is False
