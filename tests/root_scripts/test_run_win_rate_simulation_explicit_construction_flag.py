"""
Unit tests for the --explicit-construction-snapshot CLI flag and its TRUE-path threading.

Covers D1.1's CLI surface and every forwarding hop the flag's value travels, with the value
set to TRUE — the peer shape is tests/root_scripts/test_run_win_rate_simulation_naive_flag.py
(--naive-opponents is the precedent DEPLOYMENT_STANDARDS.md cites), extended here to the
sweep and promote dispatch arms and the engine chain.

The flag parses to args.explicit_construction_snapshot (store_true; absent -> False), and
True is forwarded verbatim along:

    main() -> DraftStrategyOrchestrator -> CombinationEvaluator -> ParallelLeagueRunner
              -> SimulatedLeague
    main() -> _run_sweep_mode -> CombinationEvaluator
    main() -> _run_promote_mode -> compute_promotion / promote_best_combination

Every assertion pins one specific hop's call kwargs, so deleting any single forwarding site
fails at least one test here. Composition/wiring only — the True path's own snapshot-selection
behavior is covered in tests/simulation/test_SimulatedLeague.py.

Author: Kai Mizuno
"""

# Standard library
from argparse import Namespace
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

# Local
import run_win_rate_simulation as rws
from run_win_rate_simulation import _build_parser, main
from simulation.win_rate.CombinationEvaluator import CombinationEvaluator
from simulation.win_rate.DraftStrategyOrchestrator import DraftStrategyOrchestrator
from simulation.win_rate.ParallelLeagueRunner import ParallelLeagueRunner

MODULE = "run_win_rate_simulation"


class TestExplicitConstructionSnapshotFlagParsing:
    """--explicit-construction-snapshot is a store_true flag defaulting to False."""

    def test_default_is_false(self):
        args = _build_parser().parse_args([])
        assert args.explicit_construction_snapshot is False

    def test_store_true(self):
        args = _build_parser().parse_args(["--explicit-construction-snapshot"])
        assert args.explicit_construction_snapshot is True


class TestFlagThreadsToOrchestrator:
    """main() passes args.explicit_construction_snapshot into DraftStrategyOrchestrator."""

    def test_flag_true_threads_true(self, tmp_path):
        with (
            patch("sys.argv", ["prog", "--explicit-construction-snapshot", "--data", str(tmp_path)]),
            patch(f"{MODULE}.setup_logger"),
            patch(f"{MODULE}.get_logger") as mock_get_logger,
            patch(f"{MODULE}.WinRateMetaDataManager") as mock_mdm_cls,
            patch(f"{MODULE}.DraftStrategyOrchestrator") as mock_orch_cls,
        ):
            mock_get_logger.return_value = MagicMock()
            mock_mdm_cls.return_value.get_all_strategies.return_value = {}
            main()
            assert mock_orch_cls.call_args.kwargs["explicit_construction_snapshot"] is True

    def test_flag_absent_threads_false(self, tmp_path):
        with (
            patch("sys.argv", ["prog", "--data", str(tmp_path)]),
            patch(f"{MODULE}.setup_logger"),
            patch(f"{MODULE}.get_logger") as mock_get_logger,
            patch(f"{MODULE}.WinRateMetaDataManager") as mock_mdm_cls,
            patch(f"{MODULE}.DraftStrategyOrchestrator") as mock_orch_cls,
        ):
            mock_get_logger.return_value = MagicMock()
            mock_mdm_cls.return_value.get_all_strategies.return_value = {}
            main()
            assert mock_orch_cls.call_args.kwargs["explicit_construction_snapshot"] is False


class TestFlagThreadsToSweepAndPromoteDispatch:
    """The sweep and promote arms are separate forwarding sites from the strategy arm."""

    def _sweep_args(self, tmp_path):
        return Namespace(
            data=str(tmp_path), config="data/configs/league_config.json",
            sims=10, workers=2, endless=False, strategy=None,
            log_level="INFO", enable_log_file=False, sweep=True,
            num_values=5, promote=False, fresh=False, naive_opponents=False,
            explicit_construction_snapshot=True,
            seed=None,
        )

    def test_run_sweep_mode_threads_true_to_evaluator(self, tmp_path):
        args = self._sweep_args(tmp_path)
        triples = [("1_a.json", [{"QB": "P"}], "A")]
        with patch(f"{MODULE}.load_valid_strategies", return_value=(triples, 0)), \
             patch(f"{MODULE}.CombinationEvaluator") as MockEval, \
             patch(f"{MODULE}.extract_draft_param_values", return_value={"PRIMARY_BONUS": 67}), \
             patch(f"{MODULE}.SweepResultsManager") as MockStore, \
             patch(f"{MODULE}.SweepTournament"), \
             patch(f"{MODULE}.rank_combinations", return_value=[]), \
             patch(f"{MODULE}.format_summary", return_value="summary"), \
             patch(f"{MODULE}.write_sweep_report"):
            MockEval.return_value.base_config = {"parameters": {}}
            MockEval.return_value.season_count = 1
            MockStore.return_value.get_all_combinations.return_value = {}
            rws._run_sweep_mode(args, Path(args.data), Mock())

        assert MockEval.call_args.kwargs["explicit_construction_snapshot"] is True

    def test_main_promote_dispatch_threads_true(self, tmp_path):
        with (
            patch("sys.argv", ["prog", "--promote", "--explicit-construction-snapshot",
                               "--data", str(tmp_path)]),
            patch(f"{MODULE}.setup_logger"),
            patch(f"{MODULE}.get_logger", return_value=MagicMock()),
            patch(f"{MODULE}._resolve_sweep_seed", return_value=7),
            patch(f"{MODULE}._run_promote_mode") as mock_promote_mode,
        ):
            main()

        assert mock_promote_mode.call_args.kwargs["explicit_construction_snapshot"] is True

    def test_run_promote_mode_threads_true_to_writer(self, tmp_path):
        with patch(f"{MODULE}.SweepResultsManager"), \
             patch(f"{MODULE}.promote_best_combination", return_value={}) as mock_promote, \
             patch(f"{MODULE}._print_promotion"):
            rws._run_promote_mode(
                tmp_path, Mock(), confirm=True, seed=7, shortlist=3, sims=20,
                explicit_construction_snapshot=True,
            )

        assert mock_promote.call_args.kwargs["explicit_construction_snapshot"] is True

    def test_run_promote_mode_threads_true_to_preview(self, tmp_path):
        with patch(f"{MODULE}.SweepResultsManager"), \
             patch(f"{MODULE}.compute_promotion", return_value={}) as mock_compute, \
             patch(f"{MODULE}._print_promotion_preview"):
            rws._run_promote_mode(
                tmp_path, Mock(), confirm=False, seed=7, shortlist=3, sims=20,
                explicit_construction_snapshot=True,
            )

        assert mock_compute.call_args.kwargs["explicit_construction_snapshot"] is True


class TestEngineChainForwardsTrue:
    """Each engine-chain hop forwards True to the next constructor / league."""

    def test_orchestrator_threads_true_to_evaluator(self, tmp_path):
        with patch("simulation.win_rate.DraftStrategyOrchestrator.CombinationEvaluator") as MockEval, \
             patch("simulation.win_rate.DraftStrategyOrchestrator.extract_draft_param_values",
                   return_value={}):
            MockEval.return_value.base_config = {"parameters": {}}
            DraftStrategyOrchestrator(
                data_folder=tmp_path,
                num_simulations=10,
                max_workers=2,
                meta_data_manager=Mock(),
                explicit_construction_snapshot=True,
            )

        assert MockEval.call_args.kwargs["explicit_construction_snapshot"] is True

    def test_evaluator_threads_true_to_runner(self, tmp_path):
        (tmp_path / "2024").mkdir()
        with patch("simulation.win_rate.CombinationEvaluator.ConfigManager") as MockCM, \
             patch("simulation.win_rate.CombinationEvaluator.ParallelLeagueRunner") as MockRunner:
            MockCM.return_value.config_name = "c"
            MockCM.return_value.description = "d"
            MockCM.return_value.parameters = {}
            CombinationEvaluator(
                data_folder=tmp_path,
                num_simulations=10,
                explicit_construction_snapshot=True,
            )

        assert MockRunner.call_args.kwargs["explicit_construction_snapshot"] is True

    def test_runner_threads_true_to_simulated_league(self, tmp_path):
        runner = ParallelLeagueRunner(
            max_workers=1, data_folder=tmp_path, explicit_construction_snapshot=True
        )
        with patch("simulation.win_rate.ParallelLeagueRunner.SimulatedLeague") as MockLeague:
            MockLeague.return_value.get_draft_helper_results.return_value = (1, 2, 3.0)
            runner.run_single_simulation({}, 0)

        assert MockLeague.call_args.kwargs["explicit_construction_snapshot"] is True

    def test_runner_with_weeks_threads_true_to_simulated_league(self, tmp_path):
        runner = ParallelLeagueRunner(
            max_workers=1, data_folder=tmp_path, explicit_construction_snapshot=True
        )
        with patch("simulation.win_rate.ParallelLeagueRunner.SimulatedLeague") as MockLeague:
            MockLeague.return_value.get_draft_helper_results_by_week.return_value = []
            runner.run_single_simulation_with_weeks({}, 0)

        assert MockLeague.call_args.kwargs["explicit_construction_snapshot"] is True


class TestPromotePathForwardsTrue:
    """The promote path's paired A/B comparison forwards True down to each arm's league."""

    def test_paired_comparison_arm_threads_true_to_simulated_league(self, tmp_path):
        from simulation.win_rate import paired_comparison

        with patch.object(paired_comparison, "SimulatedLeague") as MockLeague:
            MockLeague.return_value.get_draft_helper_results.return_value = (1, 2, 3.0)
            paired_comparison._run_arm(
                {"parameters": {}}, {"parameters": {}}, tmp_path, {}, 7,
                explicit_construction_snapshot=True,
            )

        assert MockLeague.call_args.kwargs["explicit_construction_snapshot"] is True

    def test_run_paired_ab_comparison_threads_true_to_both_arms(self, tmp_path):
        from simulation.win_rate import paired_comparison

        season = tmp_path / "2024"
        season.mkdir()
        with patch.object(paired_comparison, "SimDataLoader") as MockLoader, \
             patch.object(paired_comparison, "_run_arm", return_value=(1, 2)) as mock_arm:
            MockLoader.return_value.is_valid = True
            MockLoader.return_value.week_data_cache = {}
            paired_comparison.run_paired_ab_comparison(
                {"parameters": {}}, {"parameters": {}}, tmp_path,
                num_simulations=1, seed=7,
                explicit_construction_snapshot=True,
            )

        assert mock_arm.call_count == 2
        for call in mock_arm.call_args_list:
            assert call.kwargs["explicit_construction_snapshot"] is True

    def test_compute_promotion_threads_true_to_paired_comparison(self, tmp_path):
        from simulation.win_rate import config_promoter

        store = Mock()
        store.get_discriminating.return_value = True
        store.get_all_combinations.return_value = {"a": {}}
        measured = Mock(delta=0.05, z=100.0, games=200, recommended_rate=0.7,
                        current_rate=0.65, ci=(0.6, 0.8))
        row = {"strategy_id": "1_a.json", "param_values": {}, "win_rate": 0.7,
               "games": 200, "lcb": 0.6}

        with patch.object(config_promoter, "rank_combinations", return_value=[row]), \
             patch.object(config_promoter, "_resolve_draft_order", return_value=[]), \
             patch.object(config_promoter, "_read_config", return_value={"parameters": {}}), \
             patch.object(config_promoter, "_build_simulation_base_config",
                          return_value={"parameters": {}}), \
             patch.object(config_promoter, "apply_draft_overrides",
                          return_value={"parameters": {}}), \
             patch.object(config_promoter, "_build_promotion_diff", return_value={}), \
             patch.object(config_promoter, "run_paired_ab_comparison",
                          return_value=measured) as mock_ab:
            config_promoter.compute_promotion(
                store, tmp_path, seed=7, shortlist=1, sims=1,
                explicit_construction_snapshot=True,
            )

        assert mock_ab.call_args.kwargs["explicit_construction_snapshot"] is True

    def test_promote_best_combination_threads_true_to_compute_promotion(self, tmp_path):
        from simulation.win_rate import config_promoter

        plan = {
            "new_config": {"parameters": {}}, "diff": {},
            "strategy_id": "1_a.json", "remeasured_rate": 0.7,
            "remeasured_ci": (0.6, 0.8), "remeasured_games": 200,
            "shortlist_size": 1, "seed": 7, "delta": 0.05, "z": 3.1,
            "z_adjusted": 2.4, "max_selected_win_rate": 0.8,
            "max_selected_games": 170, "param_values": {}, "lcb": 0.6,
        }
        with patch.object(config_promoter, "compute_promotion",
                          return_value=dict(plan)) as mock_compute, \
             patch.object(config_promoter, "_has_uncommitted_changes", return_value=False), \
             patch.object(config_promoter, "_atomic_write_json"):
            config_promoter.promote_best_combination(
                Mock(), tmp_path, seed=7, shortlist=1, sims=1,
                explicit_construction_snapshot=True,
            )

        assert mock_compute.call_args.kwargs["explicit_construction_snapshot"] is True
