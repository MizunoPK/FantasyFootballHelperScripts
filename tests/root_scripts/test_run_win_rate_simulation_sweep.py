"""
Tests for run_win_rate_simulation.py sweep-mode dispatch (--sweep) and _run_sweep_mode.

Author: Kai Mizuno
"""

# Standard library
from argparse import Namespace
from unittest.mock import Mock, patch

# Third-party
import pytest

# Local
import run_win_rate_simulation as rws

MODULE = "run_win_rate_simulation"


def _sweep_args(tmp_path):
    return Namespace(
        data=str(tmp_path), sims=10, workers=2, endless=False, strategy=None,
        log_level="INFO", enable_log_file=False, sweep=True,
        num_values=5, promote=False, fresh=False,
    )


class TestSweepDispatch:
    def test_sweep_flag_dispatches_to_sweep_mode(self, tmp_path):
        args = _sweep_args(tmp_path)
        with patch(f"{MODULE}._build_parser") as MockParser, \
             patch(f"{MODULE}.setup_logger"), patch(f"{MODULE}.get_logger"), \
             patch(f"{MODULE}._run_sweep_mode") as mock_sweep, \
             patch(f"{MODULE}.DraftStrategyOrchestrator") as MockOrch:
            MockParser.return_value.parse_args.return_value = args
            rws.main()
        mock_sweep.assert_called_once()
        MockOrch.assert_not_called()

    def test_no_sweep_runs_strategy_only(self, tmp_path):
        args = _sweep_args(tmp_path)
        args.sweep = False
        with patch(f"{MODULE}._build_parser") as MockParser, \
             patch(f"{MODULE}.setup_logger"), patch(f"{MODULE}.get_logger"), \
             patch(f"{MODULE}._run_sweep_mode") as mock_sweep, \
             patch(f"{MODULE}.WinRateMetaDataManager"), \
             patch(f"{MODULE}.DraftStrategyOrchestrator") as MockOrch, \
             patch(f"{MODULE}._print_summary"):
            MockParser.return_value.parse_args.return_value = args
            rws.main()
        mock_sweep.assert_not_called()
        MockOrch.assert_called_once()

    def test_run_sweep_mode_builds_and_runs_tournament(self, tmp_path):
        from pathlib import Path
        args = _sweep_args(tmp_path)
        triples = [("1_a.json", [{"QB": "P"}], "A")]
        with patch(f"{MODULE}.load_valid_strategies", return_value=(triples, 0)), \
             patch(f"{MODULE}.CombinationEvaluator") as MockEval, \
             patch(f"{MODULE}.extract_draft_param_values", return_value={"PRIMARY_BONUS": 67}), \
             patch(f"{MODULE}.SweepResultsManager") as MockStore, \
             patch(f"{MODULE}.SweepTournament") as MockTour, \
             patch(f"{MODULE}.rank_combinations", return_value=[]), \
             patch(f"{MODULE}.format_summary", return_value="summary"), \
             patch(f"{MODULE}.write_sweep_report"):
            MockEval.return_value.base_config = {"parameters": {}}
            MockStore.return_value.get_all_combinations.return_value = {}
            # Mocked store: get_input_fingerprint() returns a truthy Mock != fp_now -> mismatch -> resume=False.
            rws._run_sweep_mode(args, Path(args.data), Mock())
        MockTour.assert_called_once_with(MockEval.return_value, MockStore.return_value, num_values=args.num_values)
        MockTour.return_value.run.assert_called_once_with(
            [("1_a.json", [{"QB": "P"}])], {"PRIMARY_BONUS": 67}, resume=False
        )

    def test_run_sweep_mode_empty_strategies_exits(self, tmp_path):
        from pathlib import Path
        args = _sweep_args(tmp_path)
        with patch(f"{MODULE}.load_valid_strategies", return_value=([], 0)):
            with pytest.raises(SystemExit):
                rws._run_sweep_mode(args, Path(args.data), Mock())

    def _patches_for_run(self):
        """Common patch set for _run_sweep_mode happy-path tests; returns a context list."""
        triples = [("1_a.json", [{"QB": "P"}], "A")]
        return [
            patch(f"{MODULE}.load_valid_strategies", return_value=(triples, 0)),
            patch(f"{MODULE}.CombinationEvaluator"),
            patch(f"{MODULE}.extract_draft_param_values", return_value={"PRIMARY_BONUS": 67}),
            patch(f"{MODULE}.SweepResultsManager"),
            patch(f"{MODULE}.rank_combinations", return_value=[]),
            patch(f"{MODULE}.format_summary", return_value="summary"),
            patch(f"{MODULE}.write_sweep_report"),
        ]

    def test_run_sweep_mode_endless_until_interrupt(self, tmp_path):
        from contextlib import ExitStack
        from pathlib import Path
        args = _sweep_args(tmp_path)
        args.endless = True
        with ExitStack() as stack:
            for p in self._patches_for_run():
                stack.enter_context(p)
            MockTour = stack.enter_context(patch(f"{MODULE}.SweepTournament"))
            # First pass returns, second pass interrupts the endless loop.
            MockTour.return_value.run.side_effect = [None, KeyboardInterrupt()]
            with pytest.raises(SystemExit):
                rws._run_sweep_mode(args, Path(args.data), Mock())
        assert MockTour.return_value.run.call_count == 2  # accumulated across passes

    def test_fresh_flag_forces_no_resume(self, tmp_path):
        from contextlib import ExitStack
        from pathlib import Path
        args = _sweep_args(tmp_path)
        args.fresh = True
        with ExitStack() as stack:
            for p in self._patches_for_run():
                stack.enter_context(p)
            MockTour = stack.enter_context(patch(f"{MODULE}.SweepTournament"))
            MockStore = stack.enter_context(patch(f"{MODULE}.SweepResultsManager"))
            # Even with a matching stored fingerprint, --fresh forces resume=False.
            MockStore.return_value.get_input_fingerprint.return_value = "deadbeef"
            with patch.object(
                rws.SweepResultsManager, "compute_input_fingerprint", return_value="deadbeef"
            ):
                rws._run_sweep_mode(args, Path(args.data), Mock())
            _, run_kwargs = MockTour.return_value.run.call_args
            assert run_kwargs["resume"] is False

    def test_fingerprint_match_drives_resume_true(self, tmp_path):
        from contextlib import ExitStack
        from pathlib import Path
        args = _sweep_args(tmp_path)
        with ExitStack() as stack:
            for p in self._patches_for_run():
                stack.enter_context(p)
            MockTour = stack.enter_context(patch(f"{MODULE}.SweepTournament"))
            MockStore = stack.enter_context(patch(f"{MODULE}.SweepResultsManager"))
            MockStore.return_value.get_input_fingerprint.return_value = "abc123"
            MockStore.return_value.is_all_converged.return_value = False
            MockStore.return_value.get_config_convergence.return_value = None
            with patch.object(
                rws.SweepResultsManager, "compute_input_fingerprint", return_value="abc123"
            ):
                rws._run_sweep_mode(args, Path(args.data), Mock())
            _, run_kwargs = MockTour.return_value.run.call_args
            assert run_kwargs["resume"] is True

    def test_fingerprint_mismatch_warns_and_runs_fresh(self, tmp_path):
        from contextlib import ExitStack
        from pathlib import Path
        args = _sweep_args(tmp_path)
        logger = Mock()
        with ExitStack() as stack:
            for p in self._patches_for_run():
                stack.enter_context(p)
            MockTour = stack.enter_context(patch(f"{MODULE}.SweepTournament"))
            MockStore = stack.enter_context(patch(f"{MODULE}.SweepResultsManager"))
            MockStore.return_value.get_input_fingerprint.return_value = "stale"
            with patch.object(
                rws.SweepResultsManager, "compute_input_fingerprint", return_value="current"
            ):
                rws._run_sweep_mode(args, Path(args.data), logger)
            _, run_kwargs = MockTour.return_value.run.call_args
            assert run_kwargs["resume"] is False
            assert logger.warning.call_count == 1

    def test_fingerprint_written_on_launch(self, tmp_path):
        from contextlib import ExitStack
        from pathlib import Path
        args = _sweep_args(tmp_path)
        with ExitStack() as stack:
            for p in self._patches_for_run():
                stack.enter_context(p)
            stack.enter_context(patch(f"{MODULE}.SweepTournament"))
            MockStore = stack.enter_context(patch(f"{MODULE}.SweepResultsManager"))
            MockStore.return_value.get_input_fingerprint.return_value = ""
            with patch.object(
                rws.SweepResultsManager, "compute_input_fingerprint", return_value="newfp"
            ):
                rws._run_sweep_mode(args, Path(args.data), Mock())
            MockStore.return_value.set_input_fingerprint.assert_called_once_with("newfp")
