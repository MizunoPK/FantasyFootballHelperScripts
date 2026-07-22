"""
Accuracy Simulation Manager

Orchestrates accuracy simulation to find optimal scoring algorithm configurations.
Selection optimizes pairwise ranking accuracy (how often the config orders any two
players the same way their actual fantasy points do); MAE (Mean Absolute Error)
between calculated projected points and actual player performance is also computed,
but only as a reported diagnostic.

Mode:
- Weekly: Evaluates per-week projection accuracy
  - Optimizes week1-5.json, week6-9.json, week10-13.json, week14-17.json
  - Used for Starter Helper and Trade Simulator modes

Unlike win-rate simulation:
- No randomness (deterministic ranking-metric / MAE calculation, no random draws)
- Selection optimizes pairwise ranking accuracy (higher is better); MAE is a reported diagnostic
- Tests prediction parameters (PARAMETER_ORDER in run_accuracy_simulation.py) not strategy parameters

Selection optimizes pairwise ranking accuracy, NOT MAE — do not revert `is_better_than` to an
MAE comparison; the League Helper's decisions are ordinal. MAE is a reported diagnostic only.

Author: Kai Mizuno
"""

import re
import shutil
import signal
import tempfile
import time
from pathlib import Path
from typing import List, Optional, Tuple

from utils.LoggingManager import get_logger
from simulation.shared.ConfigGenerator import ConfigGenerator, DEFAULT_ACCURACY_SEED
from simulation.shared.ProgressTracker import ProgressTracker
from simulation.shared.config_cleanup import cleanup_accuracy_intermediate_folders
from simulation.accuracy.AccuracyCalculator import AccuracyCalculator
from simulation.accuracy.AccuracyResultsManager import (
    AccuracyResultsManager,
    WEEK_RANGES,
    format_metric_pct,
    format_metric_corr,
)

PAIRWISE_ACCURACY_WARN_THRESHOLD = 0.65
TOP_10_ACCURACY_WARN_THRESHOLD = 0.70


class AccuracySimulationManager:
    """
    Manages accuracy simulation for scoring algorithm optimization.

    Coordinates ConfigGenerator, AccuracyCalculator, and AccuracyResultsManager
    to test parameter combinations and identify optimal settings.

    Attributes:
        baseline_config_path (Path): Path to baseline configuration
        output_dir (Path): Directory to save results
        data_folder (Path): Path to sim_data folder
        config_generator (ConfigGenerator): Generates parameter combinations
        accuracy_calculator (AccuracyCalculator): Calculates MAE
        results_manager (AccuracyResultsManager): Tracks results
        logger: Logger instance
    """

    ORPHANED_DIR_MAX_AGE_HOURS = 24

    def __init__(
        self,
        baseline_config_path: Path,
        output_dir: Path,
        data_folder: Path,
        parameter_order: List[str],
        num_test_values: int = 5,
        num_parameters_to_test: int = 1,
        max_workers: int = 8,
        use_processes: bool = True,
        seed: int = DEFAULT_ACCURACY_SEED
    ) -> None:
        """
        Initialize AccuracySimulationManager.

        Args:
            baseline_config_path (Path): Path to baseline configuration JSON
            output_dir (Path): Directory to save results
            data_folder (Path): Path to sim_data folder
            parameter_order (List[str]): List of parameter names defining optimization order
            num_test_values (int): Number of test values per parameter
            num_parameters_to_test (int): Number of parameters to test at once
            max_workers (int): Number of parallel workers for config evaluation
            use_processes (bool): Use ProcessPoolExecutor (True) or ThreadPoolExecutor (False)
            seed (int): Seed threaded into ConfigGenerator's private candidate-value RNG
                (default: DEFAULT_ACCURACY_SEED) so config selection is reproducible run-to-run.
        """
        self.logger = get_logger()
        self.logger.info("Initializing AccuracySimulationManager")

        self.baseline_config_path = baseline_config_path
        self.output_dir = output_dir
        self.data_folder = data_folder
        self.parameter_order = parameter_order
        self.num_test_values = num_test_values
        self.num_parameters_to_test = num_parameters_to_test

        self.max_workers = max_workers
        self.use_processes = use_processes
        self.parallel_runner = None
        self.progress_tracker = None

        self._current_optimal_config_path: Optional[Path] = None
        self._original_sigint_handler = None
        self._original_sigterm_handler = None

        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.config_generator = ConfigGenerator(
            baseline_config_path,
            num_test_values=num_test_values,
            seed=seed
        )
        self.accuracy_calculator = AccuracyCalculator()
        self.results_manager = AccuracyResultsManager(output_dir, baseline_config_path)

        self.available_seasons = self._discover_seasons()
        self.logger.info(
            f"Discovered {len(self.available_seasons)} historical seasons: "
            f"{[s.name for s in self.available_seasons]}"
        )

        candidate_values = num_test_values + 1
        configs_per_param = candidate_values * 4
        self.logger.info(
            f"AccuracySimulationManager initialized: "
            f"Candidate values per parameter per horizon: {candidate_values:,}; "
            f"Configs per horizon-specific parameter: {candidate_values:,} × 4 horizons "
            f"= {configs_per_param:,}"
        )

    def _sweep_orphaned_temp_dirs(self) -> None:
        """
        Delete stale accuracy_sim_* temp dirs from the system temp folder.

        Scans tempfile.gettempdir() for directories matching accuracy_sim_*
        that are older than ORPHANED_DIR_MAX_AGE_HOURS hours. Each stale
        directory is deleted with a warning log. Deletion failures are logged
        and skipped without aborting the sweep.
        """
        temp_root = Path(tempfile.gettempdir())
        current_time = time.time()
        threshold_seconds = self.ORPHANED_DIR_MAX_AGE_HOURS * 3600
        deleted_count = 0

        for candidate in temp_root.glob("accuracy_sim_*"):
            if not candidate.is_dir():
                continue
            try:
                mtime = candidate.stat().st_mtime
            except OSError as e:
                self.logger.warning(f"Could not stat orphaned temp dir candidate {candidate}: {e}")
                continue
            age_seconds = current_time - mtime
            if age_seconds > threshold_seconds:
                age_hours = age_seconds / 3600
                try:
                    shutil.rmtree(candidate)
                    self.logger.warning(
                        f"Deleted orphaned temp dir {candidate} (age: {age_hours:.1f}h)"
                    )
                    deleted_count += 1
                except OSError as e:
                    self.logger.warning(f"Failed to delete orphaned temp dir {candidate}: {e}")

        if deleted_count > 0:
            self.logger.info(
                f"Orphan sweep: deleted {deleted_count} stale accuracy_sim_* "
                f"temp dir(s) older than {self.ORPHANED_DIR_MAX_AGE_HOURS}h"
            )

    def _discover_seasons(self) -> List[Path]:
        """
        Find all valid historical season folders (20XX/) in data_folder.

        Returns:
            List[Path]: Sorted list of valid season folder paths
        """
        seasons = []
        for folder in self.data_folder.iterdir():
            if folder.is_dir() and folder.name.isdigit() and len(folder.name) == 4:
                weeks_folder = folder / "weeks"
                if weeks_folder.exists():
                    seasons.append(folder)

        if not seasons:
            raise ValueError(
                f"No valid season folders found in {self.data_folder}. "
                "Expected folders like '2024/' with 'weeks/' subfolder."
            )

        return sorted(seasons)

    def _setup_signal_handlers(self) -> None:
        """Set up signal handlers for graceful shutdown."""
        self._original_sigint_handler = signal.getsignal(signal.SIGINT)
        self._original_sigterm_handler = signal.getsignal(signal.SIGTERM)

        def graceful_shutdown(signum, frame):
            """Handle SIGINT/SIGTERM signals for graceful shutdown with current best config save."""
            self.logger.warning(f"Received signal {signum}, initiating graceful shutdown...")
            if self._current_optimal_config_path:
                self.logger.info(f"Current best config saved at: {self._current_optimal_config_path}")
            raise KeyboardInterrupt("Graceful shutdown requested")

        signal.signal(signal.SIGINT, graceful_shutdown)
        signal.signal(signal.SIGTERM, graceful_shutdown)

    def _restore_signal_handlers(self) -> None:
        """Restore original signal handlers."""
        if self._original_sigint_handler:
            signal.signal(signal.SIGINT, self._original_sigint_handler)
        if self._original_sigterm_handler:
            signal.signal(signal.SIGTERM, self._original_sigterm_handler)

    def _detect_resume_state(self, mode: str = 'weekly') -> Tuple[bool, int, Optional[Path]]:
        """
        Detect if optimization should resume from a previous run.

        Scans the output directory for accuracy_intermediate_*/ folders and determines
        whether to resume optimization from where it left off or start fresh.

        Args:
            mode: 'weekly' or 'ros' - affects folder name pattern matching

        Returns:
            Tuple[bool, int, Optional[Path]]: A tuple containing:
                - should_resume (bool): True if resuming, False if starting fresh
                - start_idx (int): Parameter index to start from (0 if starting fresh)
                - last_config_path (Optional[Path]): Path to last intermediate folder if resuming

        Logic:
            - No intermediate folders → (False, 0, None) - start from beginning
            - Folders for all parameters → (False, 0, None) - completed, cleanup and restart
            - Folders for some parameters → (True, highest_idx + 1, path) - resume from next (first not-yet-optimized) parameter
            - Parameter order mismatch → (False, 0, None) - validation failed, start fresh
        """
        self.logger.debug(f"_detect_resume_state: mode={mode}, output_dir={self.output_dir}")

        intermediate_folders = [
            p for p in self.output_dir.glob("accuracy_intermediate_*")
            if p.is_dir()
        ]

        if not intermediate_folders:
            self.logger.debug("No intermediate folders found")
            self.logger.debug("_detect_resume_state exit: should_resume=False, start_idx=0, last_config=None")
            return (False, 0, None)

        valid_folders = []
        param_order = self.parameter_order

        pattern = r'accuracy_intermediate_(\d+)_(.+)'

        for folder_path in intermediate_folders:
            folder_name = folder_path.name
            match = re.match(pattern, folder_name)

            if not match:
                self.logger.warning(f"Skipping folder with invalid name format: {folder_name}")
                continue

            try:
                param_idx = int(match.group(1))
                param_suffix = match.group(2)

                if mode == 'weekly':
                    for week_key in ['week1-5', 'week6-9', 'week10-13', 'week14-17']:
                        if param_suffix.startswith(f"{week_key}_"):
                            param_name = param_suffix[len(week_key) + 1:]
                            break
                    else:
                        param_name = param_suffix
                else:
                    param_name = param_suffix

                if param_name not in param_order:
                    self.logger.debug(f"Folder {folder_name}: param '{param_name}' not in parameter order")
                    continue

                config_files = ['week1-5.json', 'week6-9.json',
                               'week10-13.json', 'week14-17.json']
                has_config = any((folder_path / f).exists() for f in config_files)
                if not has_config:
                    self.logger.warning(f"Skipping incomplete folder {folder_name}: no config files")
                    continue

                valid_folders.append((param_idx, param_name, folder_path))

            except Exception as e:
                self.logger.warning(f"Error processing {folder_name}: {e}")
                continue

        if not valid_folders:
            self.logger.debug("No valid intermediate folders found after validation")
            self.logger.debug("_detect_resume_state exit: should_resume=False, start_idx=0, last_config=None")
            return (False, 0, None)

        valid_folders.sort(key=lambda x: x[0])
        highest_idx, highest_param, highest_path = valid_folders[-1]

        if highest_idx >= len(param_order) - 1:
            self.logger.debug(f"All parameters complete (idx {highest_idx} >= {len(param_order) - 1})")
            self.logger.debug("_detect_resume_state exit: should_resume=False, start_idx=0, last_config=None (all complete)")
            return (False, 0, None)

        self.logger.debug(
            f"Found {len(valid_folders)} valid intermediate folders, "
            f"highest: {highest_param} (idx {highest_idx})"
        )
        self.logger.debug(f"_detect_resume_state exit: should_resume=True, start_idx={highest_idx + 1}, last_config={highest_path}")
        return (True, highest_idx + 1, highest_path)

    def run_both(self) -> Path:
        """
        Run tournament optimization: each parameter optimizes across ALL 4 weekly horizons.

        For each parameter:
        - Generate test configs from 4 baseline configs (one per horizon)
        - Evaluate each config across all 4 horizons
        - Track best config for each horizon independently
        - Save intermediate results (all 4 best configs)
        - Update baselines for next parameter

        Returns:
            Path: Path to optimal configuration folder
        """
        self._sweep_orphaned_temp_dirs()
        total_params = len(self.parameter_order)
        self.logger.info(
            f"Starting tournament optimization: {total_params} parameters × "
            f"{self.config_generator.num_test_values} test values × 4 horizons "
            f"(each config evaluated across all 4 week ranges)"
        )

        self._setup_signal_handlers()

        try:
            should_resume, resume_param_idx, last_config_path = self._detect_resume_state()

            baseline_to_use = None
            if should_resume and last_config_path:
                baseline_to_use = last_config_path
                all_intermediate = sorted(
                    p.name for p in self.output_dir.glob("accuracy_intermediate_*")
                    if p.is_dir()
                )
                self.logger.info(
                    f"Intermediate folders found ({len(all_intermediate)}): {all_intermediate}"
                )
                self.logger.info(
                    f"Resuming from parameter {resume_param_idx + 1}. "
                    f"Selected: {last_config_path.name}"
                )
                self.results_manager.load_intermediate_results(last_config_path)
            else:
                required_files = ['league_config.json', 'week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']
                optimal_folders = sorted(
                    (p for p in self.output_dir.glob("accuracy_optimal_*")
                     if p.is_dir() and all((p / f).exists() for f in required_files)),
                    key=lambda p: p.stat().st_mtime
                )
                if optimal_folders:
                    baseline_to_use = optimal_folders[-1]
                    self.logger.info(f"Using latest optimal config as baseline: {baseline_to_use.name}")

            if baseline_to_use:
                self.logger.info(f"Reloading baseline configs from {baseline_to_use}")
                self.config_generator.baseline_configs = ConfigGenerator.load_baseline_from_folder(baseline_to_use)
                self.logger.info(f"Loaded {len(self.config_generator.baseline_configs)} horizon configs from {baseline_to_use.name}")

            for param_idx, param_name in enumerate(self.parameter_order):
                if should_resume and param_idx < resume_param_idx:
                    continue

                test_values_dict = self.config_generator.generate_horizon_test_values(param_name)

                for horizon, test_values in test_values_dict.items():
                    if len(test_values) == 0:
                        raise ValueError(f"No test values generated for parameter {param_name}, horizon {horizon}")

                total_configs = sum(len(vals) for vals in test_values_dict.values())
                total_evaluations = total_configs * 4

                self.logger.info(f"Optimizing parameter {param_idx + 1}/{len(self.parameter_order)}: {param_name}")
                self.logger.info(f"  Evaluating {total_configs} configs × 4 horizons = {total_evaluations} total evaluations")

                self.progress_tracker = ProgressTracker(
                    total=total_configs,
                    description="Configs (each tests 4 horizons)"
                )

                configs_to_evaluate = []
                config_metadata = []

                for horizon, test_values in test_values_dict.items():
                    for test_idx, test_value in enumerate(test_values):
                        config_dict = self.config_generator.get_config_for_horizon(horizon, param_name, test_idx)

                        config_dict['_eval_metadata'] = {
                            'param_name': param_name,
                            'param_value': test_value,
                            'horizon': horizon,
                            'test_idx': test_idx
                        }

                        configs_to_evaluate.append(config_dict)
                        config_metadata.append((horizon, test_idx))

                if self.parallel_runner is None:
                    from simulation.accuracy.ParallelAccuracyRunner import ParallelAccuracyRunner
                    self.parallel_runner = ParallelAccuracyRunner(
                        self.data_folder,
                        self.available_seasons,
                        max_workers=self.max_workers,
                        use_processes=self.use_processes
                    )

                def progress_update(completed):
                    self.progress_tracker.update()

                evaluation_results = self.parallel_runner.evaluate_configs_parallel(
                    configs_to_evaluate,
                    progress_callback=progress_update
                )

                self.progress_tracker.finish()

                for (config_dict, results_dict), (horizon, test_idx) in zip(evaluation_results, config_metadata):
                    for result_horizon, result in results_dict.items():
                        is_new_best = self.results_manager.add_result(
                            result_horizon,
                            config_dict,
                            result,
                            param_name=param_name,
                            test_idx=test_idx,
                            base_horizon=horizon
                        )

                        if is_new_best:
                            self.logger.info(f"    New best for {result_horizon}: MAE={result.mae:.4f} (test_{test_idx})")

                self.results_manager.save_intermediate_results(
                    param_idx,
                    param_name
                )

                horizon_map = {
                    'week_1_5': '1-5',
                    'week_6_9': '6-9',
                    'week_10_13': '10-13',
                    'week_14_17': '14-17'
                }
                for week_key, horizon_key in horizon_map.items():
                    best_perf = self.results_manager.best_configs.get(week_key)
                    if best_perf is not None:
                        self.config_generator.update_baseline_for_horizon(horizon_key, best_perf.config_dict)
                    else:
                        self.logger.warning(f"No best config found for {week_key} after parameter {param_name}")

                self._log_parameter_summary(param_name)

            optimal_path = self.results_manager.save_optimal_configs()

            self._warn_low_accuracy_promoted()

            deleted_count = cleanup_accuracy_intermediate_folders(self.output_dir)
            if deleted_count > 0:
                self.logger.info(f"Cleaned up {deleted_count} intermediate folders")

            self.logger.info(
                f"Tournament optimization complete: Optimized {total_params} parameters "
                f"across 4 week ranges. Results saved to: {optimal_path}"
            )

            return optimal_path

        finally:
            self._restore_signal_handlers()

    def _warn_low_accuracy_promoted(self) -> None:
        """Warn once per horizon when the promoted config scores below the accuracy bar.

        Reads the winning AccuracyConfigPerformance for each horizon straight from
        results_manager.best_configs at the moment save_optimal_configs() has written
        them, so each warning names the config the run is actually shipping. Emits at
        most one line per threshold per horizon (<= 8 lines per run, 0 when healthy).
        """
        for week_key in WEEK_RANGES.keys():
            best_perf = self.results_manager.best_configs.get(week_key)
            if not best_perf or not best_perf.overall_metrics:
                continue

            metrics = best_perf.overall_metrics

            if (metrics.pairwise_accuracy is not None
                    and metrics.pairwise_accuracy < PAIRWISE_ACCURACY_WARN_THRESHOLD):
                self.logger.warning(
                    f"[{week_key}] Low pairwise accuracy: "
                    f"{metrics.pairwise_accuracy:.1%} (threshold: {PAIRWISE_ACCURACY_WARN_THRESHOLD:.0%})"
                )

            if (metrics.top_10_accuracy is not None
                    and metrics.top_10_accuracy < TOP_10_ACCURACY_WARN_THRESHOLD):
                self.logger.warning(
                    f"[{week_key}] Low top-10 accuracy: "
                    f"{metrics.top_10_accuracy:.1%} (threshold: {TOP_10_ACCURACY_WARN_THRESHOLD:.0%})"
                )

    def _log_parameter_summary(self, param_name: str) -> None:
        """Log summary of best results for all horizons after parameter completes."""
        self.logger.info(f"Parameter {param_name} complete:")

        for week_key in ['week_1_5', 'week_6_9', 'week_10_13', 'week_14_17']:
            best_perf = self.results_manager.best_configs.get(week_key)
            if best_perf:
                test_idx = best_perf.test_idx if best_perf.test_idx is not None else '?'

                if best_perf.overall_metrics:
                    self.logger.info(
                        f"  {week_key}: "
                        f"Pairwise={format_metric_pct(best_perf.overall_metrics.pairwise_accuracy)} | "
                        f"Top-10={format_metric_pct(best_perf.overall_metrics.top_10_accuracy)} | "
                        f"Spearman={format_metric_corr(best_perf.overall_metrics.spearman_correlation)} | "
                        f"MAE={best_perf.mae:.4f} (diag) "
                        f"(test_{test_idx})"
                    )
                else:
                    self.logger.info(f"  {week_key}: MAE={best_perf.mae:.4f} (test_{test_idx})")
            else:
                self.logger.info(f"  {week_key}: No results yet")


