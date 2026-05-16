"""
Unit tests for run_win_rate_simulation.py.

Covers CLI flag parity, summary table formatting, and main() instantiation
flow for the FF-2 Feature 3 CLI rewrite.
"""
import subprocess
import sys
from unittest.mock import MagicMock, patch

import pytest

from run_win_rate_simulation import _build_parser, _print_summary, main


class TestNewCLIFlags:
    """Verify all 6 new CLI flags are present with correct behavior."""

    def test_help_shows_all_new_flags(self):
        result = subprocess.run(
            [sys.executable, "run_win_rate_simulation.py", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"--help failed: {result.stderr}"
        for flag in ["--sims", "--workers", "--endless", "--data", "--log-level", "--enable-log-file"]:
            assert flag in result.stdout

    def test_sims_default_is_10(self):
        args = _build_parser().parse_args([])
        assert args.sims == 10

    def test_workers_default_is_8(self):
        args = _build_parser().parse_args([])
        assert args.workers == 8

    def test_endless_default_is_false(self):
        args = _build_parser().parse_args([])
        assert args.endless is False

    def test_data_default(self):
        args = _build_parser().parse_args([])
        assert args.data == "simulation/sim_data"

    def test_log_level_default_is_info(self):
        args = _build_parser().parse_args([])
        assert args.log_level == "INFO"

    def test_enable_log_file_default_is_false(self):
        args = _build_parser().parse_args([])
        assert args.enable_log_file is False

    def test_log_level_accepts_debug(self):
        args = _build_parser().parse_args(["--log-level", "DEBUG"])
        assert args.log_level == "DEBUG"

    def test_endless_is_store_true(self):
        args = _build_parser().parse_args(["--endless"])
        assert args.endless is True


class TestRemovedCLIFlags:
    """Verify old subcommands and coordinate-descent flags are removed."""

    def _get_help_output(self) -> str:
        return _build_parser().format_help()

    def test_no_single_subcommand(self):
        result = subprocess.run(
            [sys.executable, "run_win_rate_simulation.py", "single"],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0
        assert "unrecognized arguments" in result.stderr or "invalid choice" in result.stderr

    def test_no_full_subcommand(self):
        assert "{single,full,iterative}" not in self._get_help_output()

    def test_no_baseline_flag(self):
        assert "--baseline" not in self._get_help_output()

    def test_no_output_flag(self):
        assert "--output" not in self._get_help_output()

    def test_no_test_values_flag(self):
        assert "--test-values" not in self._get_help_output()


class TestSummaryTable:
    """Verify _print_summary output format and sorting."""

    def test_empty_strategies_prints_no_evaluated(self, capsys):
        mock_mdm = MagicMock()
        mock_mdm.get_all_strategies.return_value = {}
        _print_summary(mock_mdm)
        captured = capsys.readouterr()
        assert "No strategies evaluated yet." in captured.out

    def test_sorted_by_win_rate_descending(self, capsys):
        mock_mdm = MagicMock()
        mock_mdm.get_all_strategies.return_value = {
            "1_strategy_a.json": {
                "name": "Strategy A",
                "best_win_rate": 0.500,
                "total_runs": 5,
                "last_run": "2026-01-01",
            },
            "2_strategy_b.json": {
                "name": "Strategy B",
                "best_win_rate": 0.700,
                "total_runs": 5,
                "last_run": "2026-01-01",
            },
        }
        _print_summary(mock_mdm)
        captured = capsys.readouterr()
        assert captured.out.index("Strategy B") < captured.out.index("Strategy A")

    def test_win_rate_formatted_as_3_decimal(self, capsys):
        mock_mdm = MagicMock()
        mock_mdm.get_all_strategies.return_value = {
            "1_strategy.json": {
                "name": "Strategy",
                "best_win_rate": 0.6234,
                "total_runs": 5,
                "last_run": "2026-01-01",
            },
        }
        _print_summary(mock_mdm)
        captured = capsys.readouterr()
        assert "0.623" in captured.out

    def test_header_and_footer_printed(self, capsys):
        mock_mdm = MagicMock()
        mock_mdm.get_all_strategies.return_value = {
            "1_strategy.json": {
                "name": "Strategy",
                "best_win_rate": 0.500,
                "total_runs": 1,
                "last_run": "2026-01-01",
            },
        }
        _print_summary(mock_mdm)
        captured = capsys.readouterr()
        assert "Strategy Win Rate Summary" in captured.out
        assert "──────────────────────────────────────────────────────" in captured.out


class TestMainFlow:
    """Verify main() instantiation and flow with mocked dependencies."""

    def test_meta_data_manager_instantiated_with_correct_path(self, tmp_path):
        with (
            patch("sys.argv", ["prog", "--data", str(tmp_path)]),
            patch("run_win_rate_simulation.setup_logger"),
            patch("run_win_rate_simulation.get_logger") as mock_get_logger,
            patch("run_win_rate_simulation.WinRateMetaDataManager") as mock_mdm_cls,
            patch("run_win_rate_simulation.DraftStrategyOrchestrator"),
        ):
            mock_get_logger.return_value = MagicMock()
            mock_mdm_cls.return_value.get_all_strategies.return_value = {}
            main()
            mock_mdm_cls.assert_called_once_with(tmp_path / "win_rate_meta_data.json")

    def test_orchestrator_instantiated_with_args(self, tmp_path):
        with (
            patch("sys.argv", ["prog", "--sims", "3", "--workers", "2", "--data", str(tmp_path)]),
            patch("run_win_rate_simulation.setup_logger"),
            patch("run_win_rate_simulation.get_logger") as mock_get_logger,
            patch("run_win_rate_simulation.WinRateMetaDataManager") as mock_mdm_cls,
            patch("run_win_rate_simulation.DraftStrategyOrchestrator") as mock_orch_cls,
        ):
            mock_get_logger.return_value = MagicMock()
            mock_mdm_cls.return_value.get_all_strategies.return_value = {}
            main()
            mock_orch_cls.assert_called_once_with(
                data_folder=tmp_path,
                num_simulations=3,
                max_workers=2,
                meta_data_manager=mock_mdm_cls.return_value,
            )

    def test_keyboard_interrupt_exits_zero(self, tmp_path):
        with (
            patch("sys.argv", ["prog", "--data", str(tmp_path)]),
            patch("run_win_rate_simulation.setup_logger"),
            patch("run_win_rate_simulation.get_logger") as mock_get_logger,
            patch("run_win_rate_simulation.WinRateMetaDataManager"),
            patch("run_win_rate_simulation.DraftStrategyOrchestrator") as mock_orch_cls,
            patch("run_win_rate_simulation._print_summary") as mock_summary,
        ):
            mock_logger = MagicMock()
            mock_get_logger.return_value = mock_logger
            mock_orch_cls.return_value.run.side_effect = KeyboardInterrupt
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0
            mock_summary.assert_called()
            mock_logger.info.assert_called_with(
                "Received interrupt — exiting after current strategy"
            )

    def test_single_run_calls_run_exactly_once(self, tmp_path):
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
            assert mock_orch_cls.return_value.run.call_count == 1

    def test_endless_loops_until_interrupt(self, tmp_path):
        with (
            patch("sys.argv", ["prog", "--endless", "--data", str(tmp_path)]),
            patch("run_win_rate_simulation.setup_logger"),
            patch("run_win_rate_simulation.get_logger") as mock_get_logger,
            patch("run_win_rate_simulation.WinRateMetaDataManager") as mock_mdm_cls,
            patch("run_win_rate_simulation.DraftStrategyOrchestrator") as mock_orch_cls,
            patch("run_win_rate_simulation._print_summary") as mock_summary,
        ):
            mock_get_logger.return_value = MagicMock()
            mock_mdm_cls.return_value.get_all_strategies.return_value = {}
            mock_orch_cls.return_value.run.side_effect = [None, KeyboardInterrupt]
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0
            assert mock_orch_cls.return_value.run.call_count == 2
            assert mock_summary.call_count >= 2

    def test_setup_logger_called_before_construction(self, tmp_path):
        call_order = []
        with (
            patch("sys.argv", ["prog", "--data", str(tmp_path)]),
            patch(
                "run_win_rate_simulation.setup_logger",
                side_effect=lambda *a, **kw: call_order.append("setup_logger"),
            ),
            patch("run_win_rate_simulation.get_logger") as mock_get_logger,
            patch("run_win_rate_simulation.WinRateMetaDataManager") as mock_mdm_cls,
            patch("run_win_rate_simulation.DraftStrategyOrchestrator") as mock_orch_cls,
        ):
            mock_get_logger.return_value = MagicMock()
            mock_mdm_cls.side_effect = (
                lambda *a, **kw: call_order.append("WinRateMetaDataManager")
                or MagicMock(get_all_strategies=MagicMock(return_value={}))
            )
            mock_orch_cls.side_effect = (
                lambda *a, **kw: call_order.append("DraftStrategyOrchestrator")
                or MagicMock()
            )
            main()
            assert call_order.index("setup_logger") < call_order.index("WinRateMetaDataManager")
            assert call_order.index("setup_logger") < call_order.index("DraftStrategyOrchestrator")
