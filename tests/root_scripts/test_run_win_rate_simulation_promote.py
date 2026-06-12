"""
Tests for run_win_rate_simulation.py promote-mode dispatch (--promote),
_run_promote_mode, _print_promotion, and the --promote flag parsing.

Author: Kai Mizuno
"""

# Standard library
from pathlib import Path
from unittest.mock import Mock, patch

# Third-party
import pytest

# Local
import run_win_rate_simulation as rws
from utils.error_handler import ConfigurationError, FileOperationError

MODULE = "run_win_rate_simulation"

_SAMPLE_RESULT = {
    "strategy_id": "2_winner.json",
    "param_values": {
        "DRAFT_NORMALIZATION_MAX_SCALE": 130,
        "SAME_POS_BYE_WEIGHT": 0.20,
        "DIFF_POS_BYE_WEIGHT": 0.05,
        "PRIMARY_BONUS": 90,
        "SECONDARY_BONUS": 100,
        "ADP_SCORING_WEIGHT": 3.00,
        "PLAYER_RATING_SCORING_WEIGHT": 2.00,
    },
    "win_rate": 0.732,
    "games": 250,
}


class TestRunPromoteMode:
    def test_promote_mode_invokes_writer_and_reports(self, tmp_path, capsys):
        with patch(f"{MODULE}.SweepResultsManager") as MockStore, \
             patch(f"{MODULE}.promote_best_combination", return_value=_SAMPLE_RESULT) as mock_promote:
            rws._run_promote_mode(tmp_path, Mock())

        # Writer called once with the constructed store object + data_folder.
        mock_promote.assert_called_once_with(MockStore.return_value, tmp_path)
        out = capsys.readouterr().out
        # Full D3 report content.
        assert "data/configs/league_config.json" in out
        assert "2_winner.json" in out
        assert "0.732" in out
        assert "250" in out
        for name in _SAMPLE_RESULT["param_values"]:
            assert name in out

    def test_promote_mode_config_error_exits(self, tmp_path, capsys):
        mock_logger = Mock()
        with patch(f"{MODULE}.SweepResultsManager"), \
             patch(f"{MODULE}.promote_best_combination",
                   side_effect=ConfigurationError("No sweep combinations to promote")):
            with pytest.raises(SystemExit) as exc:
                rws._run_promote_mode(tmp_path, mock_logger)
        assert exc.value.code == 1
        assert mock_logger.error.called
        assert capsys.readouterr().out == ""  # no report printed

    def test_promote_mode_file_error_exits(self, tmp_path, capsys):
        mock_logger = Mock()
        with patch(f"{MODULE}.SweepResultsManager"), \
             patch(f"{MODULE}.promote_best_combination",
                   side_effect=FileOperationError("disk full")):
            with pytest.raises(SystemExit) as exc:
                rws._run_promote_mode(tmp_path, mock_logger)
        assert exc.value.code == 1
        assert mock_logger.error.called
        assert capsys.readouterr().out == ""


class TestPromoteDispatch:
    def test_dispatch_promote_only(self, tmp_path):
        with patch("sys.argv", ["prog", "--promote", "--data", str(tmp_path)]), \
             patch(f"{MODULE}.setup_logger"), patch(f"{MODULE}.get_logger", return_value=Mock()), \
             patch(f"{MODULE}._run_sweep_mode") as mock_sweep, \
             patch(f"{MODULE}._run_promote_mode") as mock_promote, \
             patch(f"{MODULE}.WinRateMetaDataManager") as MockMeta, \
             patch(f"{MODULE}.DraftStrategyOrchestrator") as MockOrch:
            rws.main()
        mock_promote.assert_called_once()
        mock_sweep.assert_not_called()
        MockOrch.assert_not_called()
        MockMeta.assert_not_called()

    def test_dispatch_sweep_then_promote(self, tmp_path):
        parent = Mock()
        with patch("sys.argv", ["prog", "--sweep", "--promote", "--data", str(tmp_path)]), \
             patch(f"{MODULE}.setup_logger"), patch(f"{MODULE}.get_logger", return_value=Mock()), \
             patch(f"{MODULE}._run_sweep_mode") as mock_sweep, \
             patch(f"{MODULE}._run_promote_mode") as mock_promote:
            parent.attach_mock(mock_sweep, "sweep")
            parent.attach_mock(mock_promote, "promote")
            rws.main()
        mock_sweep.assert_called_once()
        mock_promote.assert_called_once()
        # Sweep runs before promote.
        order = [c[0] for c in parent.mock_calls]
        assert order == ["sweep", "promote"]

    def test_dispatch_endless_promote_rejected(self, tmp_path):
        with patch("sys.argv", ["prog", "--promote", "--endless", "--data", str(tmp_path)]), \
             patch(f"{MODULE}.setup_logger"), patch(f"{MODULE}.get_logger", return_value=Mock()), \
             patch(f"{MODULE}._run_sweep_mode") as mock_sweep, \
             patch(f"{MODULE}._run_promote_mode") as mock_promote:
            with pytest.raises(SystemExit) as exc:
                rws.main()
        assert exc.value.code == 2
        mock_sweep.assert_not_called()
        mock_promote.assert_not_called()


class TestPromoteFlagParsing:
    def test_promote_flag_default_false(self):
        args = rws._build_parser().parse_args([])
        assert args.promote is False

    def test_promote_flag_present_true(self):
        args = rws._build_parser().parse_args(["--promote"])
        assert args.promote is True
