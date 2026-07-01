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

_SAMPLE_PLAN = {
    "strategy_id": "2_winner.json",
    "param_values": _SAMPLE_RESULT["param_values"],
    "win_rate": 0.732,
    "games": 250,
    "new_config": {"parameters": {"DRAFT_ORDER": [{"round": 1, "position": "RB"}]}},
    "diff": {
        "PRIMARY_BONUS": {"current": 67, "proposed": 90},
        "DRAFT_ORDER": {"current": [], "proposed": [{"round": 1, "position": "RB"}]},
    },
}


class TestRunPromoteMode:
    def test_promote_mode_invokes_writer_and_reports(self, tmp_path, capsys):
        with patch(f"{MODULE}.SweepResultsManager") as MockStore, \
             patch(f"{MODULE}.promote_best_combination", return_value=_SAMPLE_RESULT) as mock_promote:
            rws._run_promote_mode(tmp_path, Mock(), confirm=True)

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
                rws._run_promote_mode(tmp_path, mock_logger, confirm=True)
        assert exc.value.code == 1
        assert mock_logger.error.called
        assert capsys.readouterr().out == ""  # no report printed

    def test_promote_mode_file_error_exits(self, tmp_path, capsys):
        mock_logger = Mock()
        with patch(f"{MODULE}.SweepResultsManager"), \
             patch(f"{MODULE}.promote_best_combination",
                   side_effect=FileOperationError("disk full")):
            with pytest.raises(SystemExit) as exc:
                rws._run_promote_mode(tmp_path, mock_logger, confirm=True)
        assert exc.value.code == 1
        assert mock_logger.error.called
        assert capsys.readouterr().out == ""

    def test_promote_mode_preview_no_write(self, tmp_path, capsys):
        # confirm=False -> compute the preview, NEVER call the writer.
        with patch(f"{MODULE}.SweepResultsManager") as MockStore, \
             patch(f"{MODULE}.compute_promotion", return_value=_SAMPLE_PLAN) as mock_compute, \
             patch(f"{MODULE}.promote_best_combination") as mock_promote:
            rws._run_promote_mode(tmp_path, Mock(), confirm=False)

        mock_compute.assert_called_once_with(MockStore.return_value, tmp_path)
        mock_promote.assert_not_called()
        out = capsys.readouterr().out
        assert "DRY RUN" in out
        assert "Re-run with --promote --confirm to apply." in out

    def test_promote_mode_preview_shows_diff(self, tmp_path, capsys):
        with patch(f"{MODULE}.SweepResultsManager"), \
             patch(f"{MODULE}.compute_promotion", return_value=_SAMPLE_PLAN), \
             patch(f"{MODULE}.promote_best_combination"):
            rws._run_promote_mode(tmp_path, Mock(), confirm=False)

        out = capsys.readouterr().out
        # current -> proposed shown for a changed param, plus DRAFT_ORDER.
        assert "PRIMARY_BONUS" in out
        assert "67" in out and "90" in out
        assert "DRAFT_ORDER" in out

    def test_promote_mode_preview_config_error_exits(self, tmp_path, capsys):
        mock_logger = Mock()
        with patch(f"{MODULE}.SweepResultsManager"), \
             patch(f"{MODULE}.compute_promotion",
                   side_effect=ConfigurationError("No sweep combinations to promote")), \
             patch(f"{MODULE}.promote_best_combination") as mock_promote:
            with pytest.raises(SystemExit) as exc:
                rws._run_promote_mode(tmp_path, mock_logger, confirm=False)
        assert exc.value.code == 1
        assert mock_logger.error.called
        mock_promote.assert_not_called()


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
        # Bare --promote threads confirm=False (preview, no write).
        assert mock_promote.call_args.kwargs["confirm"] is False
        mock_sweep.assert_not_called()
        MockOrch.assert_not_called()
        MockMeta.assert_not_called()

    def test_dispatch_promote_confirm_sets_true(self, tmp_path):
        with patch("sys.argv", ["prog", "--promote", "--confirm", "--data", str(tmp_path)]), \
             patch(f"{MODULE}.setup_logger"), patch(f"{MODULE}.get_logger", return_value=Mock()), \
             patch(f"{MODULE}._run_sweep_mode") as mock_sweep, \
             patch(f"{MODULE}._run_promote_mode") as mock_promote:
            rws.main()
        mock_promote.assert_called_once()
        assert mock_promote.call_args.kwargs["confirm"] is True
        mock_sweep.assert_not_called()

    def test_dispatch_bare_promote_non_tty_no_write(self, tmp_path):
        # Bare --promote in a non-TTY context still previews (no write): the flag,
        # not the TTY, is the gate. _run_promote_mode runs for real here; the writer
        # must never be reached. No capsys — patching sys.stdout.isatty (the proven
        # project pattern, see test_run_win_rate_simulation_sweep_progress.py) and a
        # capsys-replaced stdout do not mix.
        with patch("sys.argv", ["prog", "--promote", "--data", str(tmp_path)]), \
             patch(f"{MODULE}.setup_logger"), patch(f"{MODULE}.get_logger", return_value=Mock()), \
             patch("sys.stdout.isatty", return_value=False), \
             patch(f"{MODULE}.SweepResultsManager"), \
             patch(f"{MODULE}.compute_promotion", return_value=_SAMPLE_PLAN), \
             patch(f"{MODULE}.promote_best_combination") as mock_promote:
            rws.main()
        mock_promote.assert_not_called()

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
        # Chained promote threads confirm=False (preview, no write) by default.
        assert mock_promote.call_args.kwargs["confirm"] is False
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

    def test_confirm_flag_default_false(self):
        args = rws._build_parser().parse_args([])
        assert args.confirm is False

    def test_confirm_flag_present_true(self):
        args = rws._build_parser().parse_args(["--promote", "--confirm"])
        assert args.confirm is True
