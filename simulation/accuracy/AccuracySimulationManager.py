"""
Accuracy Simulation Manager

Orchestrates accuracy simulation to find optimal scoring algorithm configurations.
Evaluates prediction accuracy by comparing calculated projected points to actual
player performance using MAE (Mean Absolute Error).

Mode:
- Weekly: Evaluates per-week projection accuracy
  - Optimizes week1-5.json, week6-9.json, week10-13.json, week14-17.json
  - Used for Starter Helper and Trade Simulator modes

Unlike win-rate simulation:
- No randomness (deterministic MAE calculation)
- Lower MAE is better
- Tests prediction parameters (17 params) not strategy parameters

Author: Kai Mizuno
"""

import copy
import json
import re
import shutil
import signal
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

import numpy as np

from utils.LoggingManager import get_logger
from simulation.shared.ConfigGenerator import ConfigGenerator
from simulation.shared.ProgressTracker import ProgressTracker
from simulation.shared.config_cleanup import cleanup_old_accuracy_optimal_folders, cleanup_accuracy_intermediate_folders
from simulation.accuracy.AccuracyCalculator import AccuracyCalculator, AccuracyResult
from simulation.accuracy.AccuracyResultsManager import AccuracyResultsManager, WEEK_RANGES
from simulation.accuracy.accuracy_types import RankingMetrics
from league_helper.util.PlayerManager import PlayerManager
from league_helper.util.ConfigManager import ConfigManager
from league_helper.util.TeamDataManager import TeamDataManager
from league_helper.util.SeasonScheduleManager import SeasonScheduleManager

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

    def __init__(
        self,
        baseline_config_path: Path,
        output_dir: Path,
        data_folder: Path,
        parameter_order: List[str],
        num_test_values: int = 5,
        num_parameters_to_test: int = 1,
        max_workers: int = 8,
        use_processes: bool = True
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
            num_test_values=num_test_values
        )
        self.parameter_order = parameter_order
        self.accuracy_calculator = AccuracyCalculator()
        self.results_manager = AccuracyResultsManager(output_dir, baseline_config_path)

        self.available_seasons = self._discover_seasons()
        self.logger.info(
            f"Discovered {len(self.available_seasons)} historical seasons: "
            f"{[s.name for s in self.available_seasons]}"
        )

        total_configs = (num_test_values + 1) ** 6
        self.logger.info(
            f"AccuracySimulationManager initialized: {total_configs:,} configs/param"
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
            - Folders for some parameters → (True, highest_idx, path) - resume from next parameter
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

    def _load_season_data(
        self,
        season_path: Path,
        week_num: int
    ) -> Tuple[Optional[Path], Optional[Path]]:
        """
        Load data paths for a specific week in a season.

        For accuracy calculations, we need TWO week folders:
        - week_N folder: Contains projected_points for week N
        - week_N+1 folder: Contains actual_points for week N

        This is because week_N folder represents data "as of" week N's start,
        so week N's actual results aren't known until week N+1.

        Args:
            season_path: Path to season folder (e.g., sim_data/2024/)
            week_num: Week number (1-17)

        Returns:
            Tuple of (projected_folder, actual_folder) or (None, None) if folders not found
            - projected_folder: week_N folder (for projected_points)
            - actual_folder: week_N+1 folder (for actual_points)
        """
        self.logger.debug(f"_load_season_data: season_path={season_path}, week_num={week_num}")

        projected_folder = season_path / "weeks" / f"week_{week_num:02d}"

        actual_week_num = week_num + 1
        actual_folder = season_path / "weeks" / f"week_{actual_week_num:02d}"

        if not projected_folder.exists():
            self.logger.warning(f"Projected folder not found: {projected_folder}")
            self.logger.debug("_load_season_data exit: projected=None, actual=None (projected folder missing)")
            return None, None

        if not actual_folder.exists():
            self.logger.warning(
                f"Actual folder not found: {actual_folder} "
                f"(needed for week {week_num} actuals). Using projected data as fallback."
            )
            self.logger.debug(f"_load_season_data exit: projected={projected_folder}, actual={projected_folder} (fallback)")
            return projected_folder, projected_folder

        self.logger.debug(f"_load_season_data exit: projected={projected_folder}, actual={actual_folder}")
        return projected_folder, actual_folder

    def _create_player_manager(
        self,
        config_dict: dict,
        week_data_path: Path,
        season_path: Path,
        week_num: int
    ) -> PlayerManager:
        """
        Create a PlayerManager with the given configuration.

        Args:
            config_dict: Configuration dictionary
            week_data_path: Path to week folder containing position JSON files
            season_path: Path to season folder containing season_schedule.csv, team_data/
            week_num: NFL week number being simulated (1-17)

        Returns:
            PlayerManager: Configured player manager
        """
        import tempfile
        import shutil

        temp_dir = Path(tempfile.mkdtemp(prefix="accuracy_sim_"))

        player_data_dir = temp_dir / "player_data"
        player_data_dir.mkdir(exist_ok=True)

        position_files = ['qb_data.json', 'rb_data.json', 'wr_data.json',
                          'te_data.json', 'k_data.json', 'dst_data.json']
        for filename in position_files:
            source_file = week_data_path / filename
            if source_file.exists():
                shutil.copy(source_file, player_data_dir / filename)
            else:
                self.logger.warning(f"Missing position file: {filename} in {week_data_path}")

        season_schedule = season_path / "season_schedule.csv"
        if season_schedule.exists():
            shutil.copy(season_schedule, temp_dir / "season_schedule.csv")

        game_data = season_path / "game_data.csv"
        if game_data.exists():
            shutil.copy(game_data, temp_dir / "game_data.csv")

        team_data_source = season_path / "team_data"
        if team_data_source.exists():
            shutil.copytree(team_data_source, temp_dir / "team_data")

        config_dict_copy = copy.deepcopy(config_dict)
        config_dict_copy['parameters']['CURRENT_NFL_WEEK'] = week_num

        config_path = temp_dir / "league_config.json"
        with open(config_path, 'w') as f:
            json.dump(config_dict_copy, f, indent=2)

        config_mgr = ConfigManager(temp_dir)
        schedule_mgr = SeasonScheduleManager(temp_dir)
        team_data_mgr = TeamDataManager(temp_dir, config_mgr, schedule_mgr, config_mgr.current_nfl_week)
        player_mgr = PlayerManager(temp_dir, config_mgr, team_data_mgr, schedule_mgr)

        player_mgr._temp_dir = temp_dir

        return player_mgr

    def _cleanup_player_manager(self, player_mgr: PlayerManager) -> None:
        """Clean up temporary files from player manager."""
        if hasattr(player_mgr, '_temp_dir') and player_mgr._temp_dir.exists():
            import shutil
            shutil.rmtree(player_mgr._temp_dir)

    def _evaluate_config_weekly(
        self,
        config_dict: dict,
        week_range: Tuple[int, int]
    ) -> AccuracyResult:
        """
        Evaluate a configuration for weekly mode.

        Args:
            config_dict: Configuration to evaluate
            week_range: (start_week, end_week) inclusive

        Returns:
            AccuracyResult: MAE result for the week range across all seasons
        """
        start_week, end_week = week_range
        season_results = []

        for season_path in self.available_seasons:
            week_projections = {}
            week_actuals = {}
            player_data_by_week = {}

            for week_num in range(start_week, end_week + 1):
                projected_path, actual_path = self._load_season_data(season_path, week_num)
                if not projected_path or not actual_path:
                    continue

                projected_mgr = self._create_player_manager(config_dict, projected_path, season_path, week_num)
                actual_mgr = self._create_player_manager(config_dict, actual_path, season_path, week_num)

                try:
                    projections = {}
                    actuals = {}
                    player_data = []

                    max_weekly = projected_mgr.calculate_max_weekly_projection(week_num)
                    projected_mgr.scoring_calculator.max_weekly_projection = max_weekly

                    for player in projected_mgr.players:
                        scored = projected_mgr.score_player(
                            player,
                            use_weekly_projection=True,
                            adp=False,
                            player_rating=False,
                            team_quality=True,
                            performance=True,
                            matchup=True,
                            schedule=False,
                            bye=False,
                            injury=False,
                            temperature=True,
                            wind=True,
                            location=True
                        )
                        if scored:
                            projections[player.id] = scored.projected_points

                    for player in actual_mgr.players:
                        if 1 <= week_num <= 17:
                            actual = player.actual_points[week_num - 1] if len(player.actual_points) > week_num - 1 else 0.0
                            if actual is not None:
                                actuals[player.id] = actual

                                if player.id in projections:
                                    player_data.append({
                                        'name': player.name,
                                        'position': player.position,
                                        'projected': projections[player.id],
                                        'actual': actual
                                    })

                    week_projections[week_num] = projections
                    week_actuals[week_num] = actuals
                    player_data_by_week[week_num] = player_data

                finally:
                    self._cleanup_player_manager(projected_mgr)
                    self._cleanup_player_manager(actual_mgr)

            result = self.accuracy_calculator.calculate_weekly_mae(
                week_projections, week_actuals, week_range
            )

            overall_metrics, by_position = self.accuracy_calculator.calculate_ranking_metrics_for_season(player_data_by_week)
            result.overall_metrics = overall_metrics
            result.by_position = by_position

            if overall_metrics and overall_metrics.pairwise_accuracy < PAIRWISE_ACCURACY_WARN_THRESHOLD:
                self.logger.warning(
                    f"[{season_path.name}] Low pairwise accuracy: "
                    f"{overall_metrics.pairwise_accuracy:.1%} (threshold: 65%)"
                )

            if overall_metrics and overall_metrics.top_10_accuracy < TOP_10_ACCURACY_WARN_THRESHOLD:
                self.logger.warning(
                    f"[{season_path.name}] Low top-10 accuracy: "
                    f"{overall_metrics.top_10_accuracy:.1%} (threshold: 70%)"
                )

            season_results.append((season_path.name, result))

        return self.accuracy_calculator.aggregate_season_results(season_results)

    def _evaluate_config_tournament(
        self,
        config_dict: dict,
        horizon: str
    ) -> Dict[str, AccuracyResult]:
        """
        Evaluate single config across all 4 weekly horizons for tournament optimization.

        Args:
            config_dict: Configuration to evaluate
            horizon: Base horizon this config was generated from ('1-5', '6-9', etc.)

        Returns:
            Dict mapping each horizon to its AccuracyResult (using week_key format for add_result()):
            {'week_1_5': result_1_5, 'week_6_9': result_6_9, 'week_10_13': result_10_13, 'week_14_17': result_14_17}
        """
        results = {}


        for week_key, week_range in WEEK_RANGES.items():
            results[week_key] = self._evaluate_config_weekly(config_dict, week_range)

        return results

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
                self.logger.info(f"Resuming from parameter {resume_param_idx + 1}")
                self.results_manager.load_intermediate_results(last_config_path)
            else:
                optimal_folders = sorted(self.output_dir.glob("accuracy_optimal_*"))
                if optimal_folders:
                    baseline_to_use = optimal_folders[-1]
                    self.logger.info(f"Using latest optimal config as baseline: {baseline_to_use.name}")

            if baseline_to_use:
                self.logger.info(f"Reloading baseline configs from {baseline_to_use}")
                self.config_generator.baseline_configs = ConfigGenerator.load_baseline_from_folder(baseline_to_use)
                self.logger.info(f"Loaded {len(self.config_generator.baseline_configs)} horizon configs from {baseline_to_use.name}")

            for param_idx, param_name in enumerate(self.parameter_order):
                if should_resume and param_idx <= resume_param_idx:
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
                        f"Pairwise={best_perf.overall_metrics.pairwise_accuracy:.1%} | "
                        f"Top-10={best_perf.overall_metrics.top_10_accuracy:.1%} | "
                        f"Spearman={best_perf.overall_metrics.spearman_correlation:.3f} | "
                        f"MAE={best_perf.mae:.4f} (diag) "
                        f"(test_{test_idx})"
                    )
                else:
                    self.logger.info(f"  {week_key}: MAE={best_perf.mae:.4f} (test_{test_idx})")
            else:
                self.logger.info(f"  {week_key}: No results yet")


