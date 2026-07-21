"""
Tests for run_win_rate_simulation.py sweep-mode progress wiring (T16): the TTY vs non-TTY
callback branch, the fresh-tracker-per-pass construction, and tracker.finish() after each pass.

Author: Kai Mizuno
"""

# Standard library
from argparse import Namespace
from contextlib import ExitStack
from pathlib import Path
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
        num_values=5, promote=False, fresh=False, naive_opponents=False,
        seed=None,
    )


def _patches_for_run():
    """Common patch set for _run_sweep_mode happy-path tests (mirrors the sibling sweep test)."""
    triples = [("1_a.json", [{"QB": "P"}], "A"), ("2_b.json", [{"QB": "Q"}], "B")]
    return [
        patch(f"{MODULE}.load_valid_strategies", return_value=(triples, 0)),
        # T61: pin season_count to a real int — the pre-flight multiplies it and compares the
        # product to the floor, which a bare MagicMock cannot satisfy. 17 x 10 sims x 1 = 170,
        # above the floor, so the pre-flight stays silent and these tests are unaffected.
        patch(f"{MODULE}.CombinationEvaluator", **{"return_value.season_count": 1}),
        patch(f"{MODULE}.extract_draft_param_values", return_value={"PRIMARY_BONUS": 67}),
        patch(f"{MODULE}.SweepResultsManager"),
        patch(f"{MODULE}.rank_combinations", return_value=[]),
        patch(f"{MODULE}.format_summary", return_value="summary"),
        patch(f"{MODULE}.write_sweep_report"),
    ]


class TestSweepProgressWiring:
    """T16/KDD-1+KDD-4: the per-config progress callback wired into _run_sweep_mode."""

    def test_tty_callback_advances_the_bar(self, tmp_path):
        # On a TTY the wired callback calls tracker.update() (and NOT logger.info for progress).
        args = _sweep_args(tmp_path)
        logger = Mock()
        with ExitStack() as stack:
            for p in _patches_for_run():
                stack.enter_context(p)
            MockTracker = stack.enter_context(patch(f"{MODULE}.ProgressTracker"))
            MockTour = stack.enter_context(patch(f"{MODULE}.SweepTournament"))
            stack.enter_context(patch("sys.stdout.isatty", return_value=True))

            def fake_run(strategies, baseline_params, resume, carry_over_seeds, progress_callback):
                for sid, _ in strategies:
                    progress_callback(sid)

            MockTour.return_value.run.side_effect = fake_run
            rws._run_sweep_mode(args, Path(args.data), logger)

        tracker = MockTracker.return_value
        assert tracker.update.call_count == 2  # one per config, via the TTY branch
        # No per-config progress line was logged on the TTY path.
        assert not any(
            "config " in str(c.args[0]) for c in logger.info.call_args_list if c.args
        )

    def test_non_tty_callback_logs_a_line_and_builds_no_tracker(self, tmp_path):
        # Off a TTY the wired callback emits a logger.info line and NO ProgressTracker is built at
        # all (so finish()'s stdout banner never fires) — a per-pass counter drives the 1-based lines.
        args = _sweep_args(tmp_path)
        logger = Mock()
        with ExitStack() as stack:
            for p in _patches_for_run():
                stack.enter_context(p)
            MockTracker = stack.enter_context(patch(f"{MODULE}.ProgressTracker"))
            MockTour = stack.enter_context(patch(f"{MODULE}.SweepTournament"))
            stack.enter_context(patch("sys.stdout.isatty", return_value=False))

            def fake_run(strategies, baseline_params, resume, carry_over_seeds, progress_callback):
                for sid, _ in strategies:
                    progress_callback(sid)

            MockTour.return_value.run.side_effect = fake_run
            rws._run_sweep_mode(args, Path(args.data), logger)

        # Off a TTY no ProgressTracker is constructed, so neither update() nor finish() can fire.
        assert MockTracker.call_count == 0
        progress_lines = [
            c.args[0] for c in logger.info.call_args_list
            if c.args and str(c.args[0]).startswith("config ")
        ]
        assert len(progress_lines) == 2  # one INFO line per config
        assert str(progress_lines[0]).startswith("config 1/2 (")  # 1-based, per-pass counter
        assert str(progress_lines[1]).startswith("config 2/2 (")

    def test_progress_callback_passed_to_tournament_run(self, tmp_path):
        # The callback is wired through as the progress_callback kwarg of tournament.run.
        args = _sweep_args(tmp_path)
        with ExitStack() as stack:
            for p in _patches_for_run():
                stack.enter_context(p)
            stack.enter_context(patch(f"{MODULE}.ProgressTracker"))
            MockTour = stack.enter_context(patch(f"{MODULE}.SweepTournament"))
            stack.enter_context(patch("sys.stdout.isatty", return_value=True))
            rws._run_sweep_mode(args, Path(args.data), Mock())
        _, run_kwargs = MockTour.return_value.run.call_args
        assert callable(run_kwargs["progress_callback"])

    def test_fresh_tracker_per_pass_and_finish_called(self, tmp_path):
        # Endless mode builds a FRESH ProgressTracker(total=len(strategies)) each pass and
        # calls tracker.finish() after each pass. Interrupt on pass 3 to bound the loop.
        args = _sweep_args(tmp_path)
        args.endless = True
        with ExitStack() as stack:
            for p in _patches_for_run():
                stack.enter_context(p)
            MockTracker = stack.enter_context(patch(f"{MODULE}.ProgressTracker"))
            MockTour = stack.enter_context(patch(f"{MODULE}.SweepTournament"))
            stack.enter_context(patch("sys.stdout.isatty", return_value=True))
            MockTour.return_value.run.side_effect = [None, None, KeyboardInterrupt()]
            with pytest.raises(SystemExit):
                rws._run_sweep_mode(args, Path(args.data), Mock())
        # Three passes attempted -> three trackers constructed, each total=2 (the two strategies).
        assert MockTracker.call_count == 3
        for call in MockTracker.call_args_list:
            assert call.kwargs["total"] == 2
        # finish() called once per completed pass (2 passes completed before the pass-3 interrupt).
        assert MockTracker.return_value.finish.call_count == 2

    def test_single_pass_constructs_one_tracker_and_finishes(self, tmp_path):
        # Non-endless: exactly one tracker is built (total=2) and finished.
        args = _sweep_args(tmp_path)
        with ExitStack() as stack:
            for p in _patches_for_run():
                stack.enter_context(p)
            MockTracker = stack.enter_context(patch(f"{MODULE}.ProgressTracker"))
            stack.enter_context(patch(f"{MODULE}.SweepTournament"))
            stack.enter_context(patch("sys.stdout.isatty", return_value=True))
            rws._run_sweep_mode(args, Path(args.data), Mock())
        assert MockTracker.call_count == 1
        assert MockTracker.call_args.kwargs["total"] == 2
        assert MockTracker.return_value.finish.call_count == 1
