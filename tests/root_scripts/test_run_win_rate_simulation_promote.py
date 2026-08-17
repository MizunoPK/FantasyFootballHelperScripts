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
from simulation.win_rate.config_promoter import (
    DEFAULT_PROMOTE_SHORTLIST,
    DEFAULT_PROMOTE_SIMS,
)
from utils.error_handler import ConfigurationError, FileOperationError

MODULE = "run_win_rate_simulation"

# T62: the promote path is seeded and parameterised by shortlist/sims, and the reported shape
# leads with the FRESH re-measurement rather than the store-derived maximum.
_SAMPLE_SEED = 20260720
_SAMPLE_SHORTLIST = 3
_SAMPLE_SIMS = 20

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
    "remeasured_rate": 0.732,
    "remeasured_ci": (0.681, 0.778),
    "remeasured_games": 250,
    "delta": 0.041,
    "z": 3.10,
    "z_adjusted": 2.42,
    "shortlist_size": _SAMPLE_SHORTLIST,
    "seed": _SAMPLE_SEED,
    "max_selected_win_rate": 0.812,
    "max_selected_games": 170,
    "lcb": 0.694,
}

_SAMPLE_PLAN = {
    **_SAMPLE_RESULT,
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
            rws._run_promote_mode(
                tmp_path, Mock(), confirm=True, seed=_SAMPLE_SEED,
                shortlist=_SAMPLE_SHORTLIST, sims=_SAMPLE_SIMS,
            )

        # Writer called once with the constructed store object + data_folder + the threaded
        # re-measurement parameters (T62).
        mock_promote.assert_called_once_with(
            MockStore.return_value, tmp_path,
            seed=_SAMPLE_SEED, shortlist=_SAMPLE_SHORTLIST, sims=_SAMPLE_SIMS,
        )
        out = capsys.readouterr().out
        # Full report content: the re-measured headline leads, the store maximum is labelled.
        assert "data/configs/league_config.json" in out
        assert "2_winner.json" in out
        assert "0.732" in out
        assert "250" in out
        assert f"{_SAMPLE_SHORTLIST}-way re-measurement" in out
        assert "max_selected" in out
        assert "0.812" in out
        assert "delta=+0.0410" in out
        for name in _SAMPLE_RESULT["param_values"]:
            assert name in out

    def test_promote_mode_config_error_exits(self, tmp_path, capsys):
        mock_logger = Mock()
        with patch(f"{MODULE}.SweepResultsManager"), \
             patch(f"{MODULE}.promote_best_combination",
                   side_effect=ConfigurationError("No sweep combinations to promote")):
            with pytest.raises(SystemExit) as exc:
                rws._run_promote_mode(
                    tmp_path, mock_logger, confirm=True, seed=_SAMPLE_SEED,
                    shortlist=_SAMPLE_SHORTLIST, sims=_SAMPLE_SIMS,
                )
        assert exc.value.code == 1
        assert mock_logger.error.called
        assert capsys.readouterr().out == ""  # no report printed

    def test_promote_mode_file_error_exits(self, tmp_path, capsys):
        mock_logger = Mock()
        with patch(f"{MODULE}.SweepResultsManager"), \
             patch(f"{MODULE}.promote_best_combination",
                   side_effect=FileOperationError("disk full")):
            with pytest.raises(SystemExit) as exc:
                rws._run_promote_mode(
                    tmp_path, mock_logger, confirm=True, seed=_SAMPLE_SEED,
                    shortlist=_SAMPLE_SHORTLIST, sims=_SAMPLE_SIMS,
                )
        assert exc.value.code == 1
        assert mock_logger.error.called
        assert capsys.readouterr().out == ""

    def test_promote_mode_preview_no_write(self, tmp_path, capsys):
        # confirm=False -> compute the preview, NEVER call the writer.
        with patch(f"{MODULE}.SweepResultsManager") as MockStore, \
             patch(f"{MODULE}.compute_promotion", return_value=_SAMPLE_PLAN) as mock_compute, \
             patch(f"{MODULE}.promote_best_combination") as mock_promote:
            rws._run_promote_mode(
                tmp_path, Mock(), confirm=False, seed=_SAMPLE_SEED,
                shortlist=_SAMPLE_SHORTLIST, sims=_SAMPLE_SIMS,
            )

        mock_compute.assert_called_once_with(
            MockStore.return_value, tmp_path,
            seed=_SAMPLE_SEED, shortlist=_SAMPLE_SHORTLIST, sims=_SAMPLE_SIMS,
        )
        mock_promote.assert_not_called()
        out = capsys.readouterr().out
        assert "DRY RUN" in out
        assert "Re-run with --promote --confirm to apply." in out

    def test_promote_mode_preview_shows_diff(self, tmp_path, capsys):
        with patch(f"{MODULE}.SweepResultsManager"), \
             patch(f"{MODULE}.compute_promotion", return_value=_SAMPLE_PLAN), \
             patch(f"{MODULE}.promote_best_combination"):
            rws._run_promote_mode(
                tmp_path, Mock(), confirm=False, seed=_SAMPLE_SEED,
                shortlist=_SAMPLE_SHORTLIST, sims=_SAMPLE_SIMS,
            )

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
                rws._run_promote_mode(
                    tmp_path, mock_logger, confirm=False, seed=_SAMPLE_SEED,
                    shortlist=_SAMPLE_SHORTLIST, sims=_SAMPLE_SIMS,
                )
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

    def test_promote_shortlist_defaults_to_module_constant(self):
        args = rws._build_parser().parse_args([])
        assert args.promote_shortlist == DEFAULT_PROMOTE_SHORTLIST

    def test_promote_sims_defaults_to_module_constant(self):
        args = rws._build_parser().parse_args([])
        assert args.promote_sims == DEFAULT_PROMOTE_SIMS

    def test_promote_shortlist_and_sims_are_overridable(self):
        args = rws._build_parser().parse_args(
            ["--promote", "--promote-shortlist", "1", "--promote-sims", "1"]
        )
        assert args.promote_shortlist == 1
        assert args.promote_sims == 1


class TestHonestHeadlineLabels:
    """T62: the winner-of-K label (K printed) and the headline ORDERING, in BOTH printers.

    spec.md "New coverage required", bullet 7. Step 21 asserts the label appears on the WRITE
    path through _run_promote_mode; this class pins it on the PREVIEW path too and pins the
    required ordering (re-measured rate + CI first, delta/z beneath, max_selected last), which
    the spec states as a requirement rather than a preference.
    """

    def test_write_report_labels_the_winner_of_k(self, capsys):
        rws._print_promotion(_SAMPLE_RESULT)
        out = capsys.readouterr().out
        assert f"winner of a {_SAMPLE_SHORTLIST}-way re-measurement" in out
        assert "uncorrected" in out

    def test_preview_labels_the_winner_of_k(self, capsys):
        rws._print_promotion_preview(_SAMPLE_PLAN)
        out = capsys.readouterr().out
        assert f"winner of a {_SAMPLE_SHORTLIST}-way re-measurement" in out
        assert "uncorrected" in out
        # The preview still shows the diff and the apply hint it always did.
        assert "PRIMARY_BONUS" in out
        assert "Re-run with --promote --confirm to apply." in out

    def test_headline_ordering_remeasured_then_evidence_then_max_selected(self, capsys):
        rws._print_promotion(_SAMPLE_RESULT)
        out = capsys.readouterr().out
        assert out.index("Re-measured win rate") < out.index("delta=")
        assert out.index("delta=") < out.index("max_selected")
        assert "not an estimate" in out
        # The Wilson interval is printed alongside the headline, not buried.
        assert "[0.681, 0.778]" in out

    def test_seed_is_reported_so_the_run_is_reproducible(self, capsys):
        rws._print_promotion(_SAMPLE_RESULT)
        out = capsys.readouterr().out
        assert str(_SAMPLE_SEED) in out
