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
        num_values=5, promote=False, fresh=False, naive_opponents=False,
        seed=None,
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
            # T61: the pre-flight reads evaluator.season_count, so it must be a real int.
            MockEval.return_value.season_count = 1
            MockStore.return_value.get_all_combinations.return_value = {}
            # Mocked store: get_input_fingerprint() returns a truthy Mock != fp_now -> mismatch -> resume=False.
            rws._run_sweep_mode(args, Path(args.data), Mock())
        # T61/D3: the pre-flight count (17 weeks x 10 sims x 1 season = 170) is plumbed through.
        MockTour.assert_called_once_with(
            MockEval.return_value, MockStore.return_value,
            num_values=args.num_values, games_per_evaluation=170,
        )
        run_args, run_kwargs = MockTour.return_value.run.call_args
        assert run_args == ([("1_a.json", [{"QB": "P"}])], {"PRIMARY_BONUS": 67})
        assert run_kwargs["resume"] is False
        assert run_kwargs["carry_over_seeds"] is None
        assert callable(run_kwargs["progress_callback"])  # T16: progress callback wired through

    def test_run_sweep_mode_empty_strategies_exits(self, tmp_path):
        from pathlib import Path
        args = _sweep_args(tmp_path)
        with patch(f"{MODULE}.load_valid_strategies", return_value=([], 0)):
            with pytest.raises(SystemExit):
                rws._run_sweep_mode(args, Path(args.data), Mock())

    def _patches_for_run(self, season_count=1):
        """Common patch set for _run_sweep_mode happy-path tests; returns a context list.

        season_count pins the patched evaluator's T61 season_count so the games-per-evaluation
        pre-flight has a real int to multiply (a bare MagicMock raises TypeError on the
        comparison). The default 1 x the default --sims 10 = 170 games/eval, comfortably above
        the floor, so the pre-flight stays silent for every pre-existing test.
        """
        triples = [("1_a.json", [{"QB": "P"}], "A")]
        return [
            patch(f"{MODULE}.load_valid_strategies", return_value=(triples, 0)),
            patch(f"{MODULE}.CombinationEvaluator", **{"return_value.season_count": season_count}),
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
            write_report = stack.enter_context(patch(f"{MODULE}.write_sweep_report"))
            with pytest.raises(SystemExit):
                rws._run_sweep_mode(args, Path(args.data), Mock())
        assert MockTour.return_value.run.call_count == 2  # accumulated across passes
        # T10: the interrupt path still writes a final summary (resumable state preserved:
        # the engine's atomic mark_config_progress checkpoint is independent of this exit).
        assert write_report.call_count >= 1

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

    def test_endless_carry_over_none_on_pass1_then_map_on_pass2(self, tmp_path):
        # T10/D1+D3: pass 1 runs with carry_over_seeds=None; pass 2 runs with a seed map
        # built from the store's converged params. Bound the loop by interrupting on pass 3.
        from contextlib import ExitStack
        from pathlib import Path
        args = _sweep_args(tmp_path)
        args.endless = True
        with ExitStack() as stack:
            for p in self._patches_for_run():
                stack.enter_context(p)
            MockTour = stack.enter_context(patch(f"{MODULE}.SweepTournament"))
            MockStore = stack.enter_context(patch(f"{MODULE}.SweepResultsManager"))
            MockStore.return_value.get_input_fingerprint.return_value = ""
            # Convergence lookup used to build the carry-over map after each pass.
            MockStore.return_value.get_config_convergence.return_value = {
                "best_param_values": {"PRIMARY_BONUS": 80}
            }
            MockTour.return_value.run.side_effect = [None, None, KeyboardInterrupt()]
            with pytest.raises(SystemExit):
                rws._run_sweep_mode(args, Path(args.data), Mock())
            calls = MockTour.return_value.run.call_args_list
            # Pass 1: carry_over_seeds=None.
            assert calls[0].kwargs["carry_over_seeds"] is None
            # Pass 2: carry_over_seeds is a dict built from converged params.
            assert calls[1].kwargs["carry_over_seeds"] == {"1_a.json": {"PRIMARY_BONUS": 80}}

    def test_endless_pass_header_printed_in_endless_absent_in_single(self, tmp_path, capsys):
        # T10/D2: endless mode prints the "=== Endless sweep pass N ===" header; the
        # single-pass non-endless path prints no such header.
        from contextlib import ExitStack
        from pathlib import Path
        # Endless: header present (interrupt on pass 2 to bound).
        args = _sweep_args(tmp_path)
        args.endless = True
        with ExitStack() as stack:
            for p in self._patches_for_run():
                stack.enter_context(p)
            MockTour = stack.enter_context(patch(f"{MODULE}.SweepTournament"))
            MockTour.return_value.run.side_effect = [None, KeyboardInterrupt()]
            with pytest.raises(SystemExit):
                rws._run_sweep_mode(args, Path(args.data), Mock())
        out_endless = capsys.readouterr().out
        assert "=== Endless sweep pass 1 ===" in out_endless
        # Single-pass: no header.
        args2 = _sweep_args(tmp_path)
        args2.endless = False
        with ExitStack() as stack:
            for p in self._patches_for_run():
                stack.enter_context(p)
            stack.enter_context(patch(f"{MODULE}.SweepTournament"))
            rws._run_sweep_mode(args2, Path(args2.data), Mock())
        out_single = capsys.readouterr().out
        assert "=== Endless sweep pass" not in out_single

    def test_resume_then_carry_over_ordering(self, tmp_path):
        # T10/D3: on a resumed endless run, pass 1 carries resume=True + carry_over_seeds=None;
        # pass 2 carries resume=False + a carry-over map. Interrupt on pass 3 to bound the loop.
        from contextlib import ExitStack
        from pathlib import Path
        args = _sweep_args(tmp_path)
        args.endless = True
        with ExitStack() as stack:
            for p in self._patches_for_run():
                stack.enter_context(p)
            MockTour = stack.enter_context(patch(f"{MODULE}.SweepTournament"))
            MockStore = stack.enter_context(patch(f"{MODULE}.SweepResultsManager"))
            MockStore.return_value.get_input_fingerprint.return_value = "abc123"
            MockStore.return_value.is_all_converged.return_value = False
            MockStore.return_value.get_config_convergence.return_value = {
                "best_param_values": {"PRIMARY_BONUS": 80}
            }
            MockTour.return_value.run.side_effect = [None, None, KeyboardInterrupt()]
            with patch.object(
                rws.SweepResultsManager, "compute_input_fingerprint", return_value="abc123"
            ):
                with pytest.raises(SystemExit):
                    rws._run_sweep_mode(args, Path(args.data), Mock())
            calls = MockTour.return_value.run.call_args_list
            # Pass 1: resume honored, no carry-over.
            assert calls[0].kwargs["resume"] is True
            assert calls[0].kwargs["carry_over_seeds"] is None
            # Pass 2: resume cleared, carry-over governs.
            assert calls[1].kwargs["resume"] is False
            assert calls[1].kwargs["carry_over_seeds"] == {"1_a.json": {"PRIMARY_BONUS": 80}}


class TestSweepStarvationPreflight:
    """T61: the games-per-evaluation reachability pre-flight and the starved resume bucket."""

    def _patches_for_run(self, season_count=1):
        """Reuse the sibling class's patch set (same helper, same defaults)."""
        return TestSweepDispatch._patches_for_run(self, season_count=season_count)

    def test_preflight_errors_when_starved_and_the_run_still_proceeds(self, tmp_path):
        # T61/D1+D2: 17 weeks x 1 sim x 1 valid season = 17 < DEFAULT_MIN_GAMES (30). Exactly one
        # ERROR naming the computed count, the three factors, the floor, the consequence, and a
        # --sims remedy — and the run still reaches tournament.run (warn-and-continue, not abort).
        from contextlib import ExitStack
        from pathlib import Path
        args = _sweep_args(tmp_path)
        args.sims = 1
        logger = Mock()
        with ExitStack() as stack:
            for p in self._patches_for_run():
                stack.enter_context(p)
            MockTour = stack.enter_context(patch(f"{MODULE}.SweepTournament"))
            rws._run_sweep_mode(args, Path(args.data), logger)
        assert logger.error.call_count == 1
        msg = logger.error.call_args.args[0]
        assert "17 games per evaluation" in msg          # the computed count
        assert "17 weeks x 1 sims x 1 valid season(s)" in msg  # the three factors
        assert str(rws.DEFAULT_MIN_GAMES) in msg         # the configured floor
        assert "'starved'" in msg                        # the consequence
        assert "raise --sims to at least 2" in msg       # the remedy
        MockTour.return_value.run.assert_called_once()   # the run proceeded

    def test_preflight_silent_when_adequately_provisioned(self, tmp_path):
        # 17 x 2 sims x 1 season = 34 >= 30 -> no new output at all.
        from contextlib import ExitStack
        from pathlib import Path
        args = _sweep_args(tmp_path)
        args.sims = 2
        logger = Mock()
        with ExitStack() as stack:
            for p in self._patches_for_run():
                stack.enter_context(p)
            stack.enter_context(patch(f"{MODULE}.SweepTournament"))
            rws._run_sweep_mode(args, Path(args.data), logger)
        assert logger.error.call_count == 0

    def test_preflight_zero_seasons_names_only_the_season_lever(self, tmp_path):
        # T61: season_count == 0 is reachable (folders present, none pass validation). The
        # minimum-viable---sims arithmetic is undefined there, so the branch must not divide by
        # zero and must name the season-folder lever alone.
        from contextlib import ExitStack
        from pathlib import Path
        args = _sweep_args(tmp_path)
        logger = Mock()
        with ExitStack() as stack:
            for p in self._patches_for_run(season_count=0):
                stack.enter_context(p)
            stack.enter_context(patch(f"{MODULE}.SweepTournament"))
            rws._run_sweep_mode(args, Path(args.data), logger)  # must not raise ZeroDivisionError
        assert logger.error.call_count == 1
        msg = logger.error.call_args.args[0]
        assert "0 games per evaluation" in msg
        assert "0 valid season(s)" in msg
        assert "season folders" in msg
        assert "--sims" not in msg  # no minimum-sims term in the zero-season branch

    def test_preflight_passes_zero_games_per_evaluation_to_the_tournament(self, tmp_path):
        # The zero product is still plumbed through, so the tournament marks configs starved.
        from contextlib import ExitStack
        from pathlib import Path
        args = _sweep_args(tmp_path)
        with ExitStack() as stack:
            for p in self._patches_for_run(season_count=0):
                stack.enter_context(p)
            MockTour = stack.enter_context(patch(f"{MODULE}.SweepTournament"))
            rws._run_sweep_mode(args, Path(args.data), Mock())
        assert MockTour.call_args.kwargs["games_per_evaluation"] == 0

    def test_resume_breakdown_counts_starved_configs(self, tmp_path):
        # T61/D4: a starved entry belongs to none of converged / in-progress / not-started, so
        # the breakdown gains its own bucket rather than silently dropping it.
        from contextlib import ExitStack
        from pathlib import Path
        args = _sweep_args(tmp_path)
        logger = Mock()
        with ExitStack() as stack:
            for p in self._patches_for_run():
                stack.enter_context(p)
            stack.enter_context(patch(f"{MODULE}.SweepTournament"))
            MockStore = stack.enter_context(patch(f"{MODULE}.SweepResultsManager"))
            MockStore.return_value.get_input_fingerprint.return_value = "abc123"
            MockStore.return_value.is_all_converged.return_value = False
            MockStore.return_value.get_config_convergence.return_value = {
                "status": "starved",
                "best_param_values": {"PRIMARY_BONUS": 67},
            }
            with patch.object(
                rws.SweepResultsManager, "compute_input_fingerprint", return_value="abc123"
            ):
                rws._run_sweep_mode(args, Path(args.data), logger)
        assert any(
            "1 starved" in str(c.args[0]) for c in logger.info.call_args_list if c.args
        )
        # T61 regression — no resume poisoning, DRIVER half (spec §Test Strategy case 5). The
        # driver's short-circuit branch is literally `if store.is_all_converged(...)`, so with a
        # store reporting False (which SweepResultsManager genuinely does for a "starved" entry —
        # proved at the store level by test_is_all_converged_false_when_one_starved) the run must
        # reach the breakdown, never the "Sweep already complete" early exit.
        assert not any(
            "Sweep already complete" in str(c.args[0])
            for c in logger.info.call_args_list if c.args
        )
