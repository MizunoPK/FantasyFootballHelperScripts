"""
Accuracy Simulation Manager

Orchestrates accuracy simulation to find optimal scoring algorithm configurations.
Evaluates prediction accuracy by comparing calculated projected points to actual
player performance using MAE (Mean Absolute Error).

Two modes:
1. ROS (Rest of Season): Evaluates season-long projection accuracy
   - Optimizes draft_config.json for Add to Roster Mode
2. Weekly: Evaluates per-week projection accuracy
   - Optimizes week1-5.json, week6-9.json, etc. for Starter Helper/Trade Simulator

Unlike win-rate simulation:
- No randomness (deterministic MAE calculation)
- Lower MAE is better
- Tests prediction parameters (17 params) not strategy parameters

Author: Kai Mizuno
"""

import copy
import csv
import json
import re
import shutil
import signal
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.LoggingManager import get_logger

# Import from shared folder
sys.path.append(str(Path(__file__).parent.parent / "shared"))
from ConfigGenerator import ConfigGenerator
from ProgressTracker import ProgressTracker
from config_cleanup import cleanup_old_accuracy_optimal_folders

# Import from same folder (accuracy/)
sys.path.append(str(Path(__file__).parent))
from AccuracyCalculator import AccuracyCalculator, AccuracyResult
from AccuracyResultsManager import AccuracyResultsManager, WEEK_RANGES

# Import league helper components for scoring
sys.path.append(str(Path(__file__).parent.parent.parent / "league_helper"))
sys.path.append(str(Path(__file__).parent.parent.parent / "league_helper" / "util"))
from league_helper.util.PlayerManager import PlayerManager
from league_helper.util.ConfigManager import ConfigManager
from league_helper.util.TeamDataManager import TeamDataManager
from league_helper.util.SeasonScheduleManager import SeasonScheduleManager


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

        # Parallel processing
        self.max_workers = max_workers
        self.use_processes = use_processes
        self.parallel_runner = None  # Lazy initialization
        self.progress_tracker = None  # Created per parameter

        # Track current optimal config for graceful shutdown
        self._current_optimal_config_path: Optional[Path] = None
        self._original_sigint_handler = None
        self._original_sigterm_handler = None

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self.config_generator = ConfigGenerator(
            baseline_config_path,
            num_test_values=num_test_values
        )
        # Store parameter_order on manager (not passed to ConfigGenerator anymore)
        self.parameter_order = parameter_order
        self.accuracy_calculator = AccuracyCalculator()
        self.results_manager = AccuracyResultsManager(output_dir, baseline_config_path)

        # Discover available historical seasons
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
        # Get all intermediate folders for accuracy simulation
        intermediate_folders = [
            p for p in self.output_dir.glob("accuracy_intermediate_*")
            if p.is_dir()
        ]

        if not intermediate_folders:
            self.logger.debug("No intermediate folders found")
            return (False, 0, None)

        # Parse all folders and collect valid ones
        valid_folders = []
        param_order = self.parameter_order

        # Pattern: accuracy_intermediate_XX_paramname or accuracy_intermediate_XX_weekrange_paramname
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

                # For weekly mode, the suffix might be "week1-5_PARAM_NAME"
                # Extract just the param name part
                if mode == 'weekly':
                    # Check if any week range prefix exists
                    for week_key in ['week1-5', 'week6-9', 'week10-13', 'week14-17']:
                        if param_suffix.startswith(f"{week_key}_"):
                            param_name = param_suffix[len(week_key) + 1:]
                            break
                    else:
                        param_name = param_suffix
                else:
                    param_name = param_suffix

                # Validate parameter is in our parameter order
                if param_name not in param_order:
                    self.logger.debug(f"Folder {folder_name}: param '{param_name}' not in parameter order")
                    continue

                # Check that folder contains expected config files
                # Standard config files: draft_config.json and/or week1-5.json, etc.
                config_files = ['draft_config.json', 'week1-5.json', 'week6-9.json',
                               'week10-13.json', 'week14-17.json']
                has_config = any((folder_path / f).exists() for f in config_files)
                if not has_config:
                    self.logger.warning(f"Skipping incomplete folder {folder_name}: no config files")
                    continue

                # Folder is valid
                valid_folders.append((param_idx, param_name, folder_path))

            except Exception as e:
                self.logger.warning(f"Error processing {folder_name}: {e}")
                continue

        # No valid folders found
        if not valid_folders:
            self.logger.debug("No valid intermediate folders found after validation")
            return (False, 0, None)

        # Find highest valid index
        valid_folders.sort(key=lambda x: x[0])
        highest_idx, highest_param, highest_path = valid_folders[-1]

        # Check if all parameters are complete
        if highest_idx >= len(param_order) - 1:
            self.logger.debug(f"All parameters complete (idx {highest_idx} >= {len(param_order) - 1})")
            return (False, 0, None)

        # Resume from next parameter
        self.logger.debug(
            f"Found {len(valid_folders)} valid intermediate folders, "
            f"highest: {highest_param} (idx {highest_idx})"
        )
        return (True, highest_idx + 1, highest_path)

    def _load_season_data(
        self,
        season_path: Path,
        week_num: int
    ) -> Tuple[Optional[Path], Optional[Path]]:
        """
        Load data paths for a specific week in a season.

        Args:
            season_path: Path to season folder (e.g., sim_data/2024/)
            week_num: Week number (1-17)

        Returns:
            Tuple of (projected_csv_path, actual_csv_path) or (None, None) if not found
        """
        week_folder = season_path / "weeks" / f"week_{week_num:02d}"

        if not week_folder.exists():
            return None, None

        projected_path = week_folder / "players_projected.csv"
        actual_path = week_folder / "players.csv"

        if not projected_path.exists() or not actual_path.exists():
            return None, None

        return projected_path, actual_path

    def _create_player_manager(
        self,
        config_dict: dict,
        week_data_path: Path,
        season_path: Path
    ) -> PlayerManager:
        """
        Create a PlayerManager with the given configuration.

        Args:
            config_dict: Configuration dictionary
            week_data_path: Path to week folder containing players.csv, players_projected.csv
            season_path: Path to season folder containing season_schedule.csv, team_data/

        Returns:
            PlayerManager: Configured player manager
        """
        import tempfile
        import shutil

        temp_dir = Path(tempfile.mkdtemp(prefix="accuracy_sim_"))

        # Copy player data files from week folder
        for file in week_data_path.iterdir():
            if file.suffix == '.csv':
                shutil.copy(file, temp_dir / file.name)

        # Copy season_schedule.csv from season folder
        season_schedule = season_path / "season_schedule.csv"
        if season_schedule.exists():
            shutil.copy(season_schedule, temp_dir / "season_schedule.csv")

        # Copy game_data.csv from season folder if exists
        game_data = season_path / "game_data.csv"
        if game_data.exists():
            shutil.copy(game_data, temp_dir / "game_data.csv")

        # Copy team_data folder from season folder
        team_data_source = season_path / "team_data"
        if team_data_source.exists():
            shutil.copytree(team_data_source, temp_dir / "team_data")

        # Write config
        config_path = temp_dir / "league_config.json"
        with open(config_path, 'w') as f:
            json.dump(config_dict, f, indent=2)

        # Create managers
        config_mgr = ConfigManager(temp_dir)
        schedule_mgr = SeasonScheduleManager(temp_dir)
        team_data_mgr = TeamDataManager(temp_dir, config_mgr, schedule_mgr, config_mgr.current_nfl_week)
        player_mgr = PlayerManager(temp_dir, config_mgr, team_data_mgr, schedule_mgr)

        # Store temp_dir for cleanup
        player_mgr._temp_dir = temp_dir

        return player_mgr

    def _cleanup_player_manager(self, player_mgr: PlayerManager) -> None:
        """Clean up temporary files from player manager."""
        if hasattr(player_mgr, '_temp_dir') and player_mgr._temp_dir.exists():
            import shutil
            shutil.rmtree(player_mgr._temp_dir)

    def _evaluate_config_ros(
        self,
        config_dict: dict
    ) -> AccuracyResult:
        """
        Evaluate a configuration for ROS (Rest of Season) mode.

        Uses week 1 projections vs actual season totals.

        Args:
            config_dict: Configuration to evaluate

        Returns:
            AccuracyResult: MAE result across all seasons
        """
        season_results = []

        for season_path in self.available_seasons:
            # Load week 1 data (pre-season projections)
            projected_path, actual_path = self._load_season_data(season_path, 1)
            if not projected_path:
                continue

            # Create player manager with this config
            player_mgr = self._create_player_manager(config_dict, projected_path.parent, season_path)

            try:
                # Calculate projections for all players
                projections = {}
                actuals = {}

                for player in player_mgr.players:
                    # Get scored player with projected points
                    # Use same flags as StarterHelperModeManager but with
                    # use_weekly_projection=False for season-long projections
                    scored = player_mgr.score_player(
                        player,
                        use_weekly_projection=False,  # Season-long projection
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

                    # Get actual season total by summing week_N_points
                    actual_total = 0.0
                    has_any_week = False
                    for week_num in range(1, 18):
                        week_attr = f'week_{week_num}_points'
                        if hasattr(player, week_attr):
                            week_val = getattr(player, week_attr)
                            if week_val is not None:
                                actual_total += week_val
                                has_any_week = True

                    if has_any_week and actual_total > 0:
                        actuals[player.id] = actual_total

                # Calculate MAE for this season
                result = self.accuracy_calculator.calculate_ros_mae(projections, actuals)
                season_results.append((season_path.name, result))

            finally:
                self._cleanup_player_manager(player_mgr)

        # Aggregate across seasons
        return self.accuracy_calculator.aggregate_season_results(season_results)

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

            for week_num in range(start_week, end_week + 1):
                projected_path, actual_path = self._load_season_data(season_path, week_num)
                if not projected_path:
                    continue

                # Create player manager with this config
                player_mgr = self._create_player_manager(config_dict, projected_path.parent, season_path)

                try:
                    projections = {}
                    actuals = {}

                    for player in player_mgr.players:
                        # Get scored player with projected points
                        # Use same flags as StarterHelperModeManager with
                        # use_weekly_projection=True for weekly projections
                        scored = player_mgr.score_player(
                            player,
                            use_weekly_projection=True,  # Weekly projection
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

                        # Get actual points for this specific week
                        week_points_attr = f'week_{week_num}_points'
                        if hasattr(player, week_points_attr):
                            actual = getattr(player, week_points_attr)
                            if actual is not None and actual > 0:
                                actuals[player.id] = actual

                    week_projections[week_num] = projections
                    week_actuals[week_num] = actuals

                finally:
                    self._cleanup_player_manager(player_mgr)

            # Calculate MAE for this season's week range
            result = self.accuracy_calculator.calculate_weekly_mae(
                week_projections, week_actuals, week_range
            )
            season_results.append((season_path.name, result))

        # Aggregate across seasons
        return self.accuracy_calculator.aggregate_season_results(season_results)

    def _evaluate_config_tournament(
        self,
        config_dict: dict,
        horizon: str
    ) -> Dict[str, AccuracyResult]:
        """
        Evaluate single config across all 5 horizons for tournament optimization.

        Args:
            config_dict: Configuration to evaluate
            horizon: Base horizon this config was generated from ('ros', '1-5', etc.)

        Returns:
            Dict mapping each horizon to its AccuracyResult (using week_key format for add_result()):
            {'ros': result_ros, 'week_1_5': result_1_5, 'week_6_9': result_6_9, 'week_10_13': result_10_13, 'week_14_17': result_14_17}
        """
        results = {}

        # Evaluate ROS horizon
        results['ros'] = self._evaluate_config_ros(config_dict)

        # Evaluate all 4 weekly horizons
        # CRITICAL: _evaluate_config_weekly() takes Tuple[int, int] not string!
        # CRITICAL: Use week_key format (with underscores) to match add_result() expectations
        # NOTE: WEEK_RANGES already imported at module level (line 45)

        for week_key, week_range in WEEK_RANGES.items():
            results[week_key] = self._evaluate_config_weekly(config_dict, week_range)

        return results

    def run_ros_optimization(self) -> Path:
        """
        Run ROS (Rest of Season) optimization with auto-resume support.

        Iteratively tests configurations to find optimal parameters
        for predicting season-long player performance.

        **Auto-Resume Feature:**
            If interrupted mid-optimization, automatically resumes from the last completed
            parameter based on existing accuracy_intermediate_*/ folders.

        Returns:
            Path: Path to optimal configuration folder
        """
        self.logger.info("Starting ROS accuracy optimization")
        self._setup_signal_handlers()

        try:
            # Get total configs for progress tracking
            total_params = len(self.parameter_order)

            # Detect if we should resume from a previous run
            should_resume, start_idx, last_config_path = self._detect_resume_state('ros')

            if should_resume:
                self.logger.info(f"Resuming from parameter {start_idx + 1}/{total_params}")
                # Load intermediate results into results_manager
                if last_config_path and self.results_manager.load_intermediate_results(last_config_path):
                    self.logger.info(f"Loaded intermediate results from {last_config_path.name}")
                    # Get current best config from loaded results
                    best_perf = self.results_manager.get_best_config('ros')
                    if best_perf:
                        current_base_config = copy.deepcopy(best_perf.config_dict)
                    else:
                        # Use 'ros' horizon baseline
                        current_base_config = copy.deepcopy(self.config_generator.baseline_configs['ros'])
                else:
                    self.logger.warning("Failed to load intermediate results, starting fresh")
                    should_resume = False
                    start_idx = 0
                    # Use 'ros' horizon baseline
                    current_base_config = copy.deepcopy(self.config_generator.baseline_configs['ros'])
            else:
                # Starting fresh - cleanup any existing intermediate folders
                intermediate_folders = [p for p in self.output_dir.glob("accuracy_intermediate_*") if p.is_dir()]
                if intermediate_folders:
                    self.logger.info(f"Cleaning up {len(intermediate_folders)} intermediate folders")
                    for folder in intermediate_folders:
                        try:
                            shutil.rmtree(folder)
                            self.logger.debug(f"  Deleted: {folder.name}")
                        except Exception as e:
                            self.logger.warning(f"  Failed to delete {folder.name}: {e}")
                    self.logger.info("Cleanup complete")

                # Track current best config (starts from 'ros' baseline)
                current_base_config = copy.deepcopy(self.config_generator.baseline_configs['ros'])

            # Iterative optimization
            for param_idx, param_name in enumerate(self.parameter_order):
                # Skip already-completed parameters when resuming
                if should_resume and param_idx < start_idx:
                    self.logger.debug(f"Skipping already-completed parameter {param_idx}: {param_name}")
                    continue

                self.logger.info(f"Optimizing parameter {param_idx + 1}/{total_params}: {param_name}")

                # Generate test values for this parameter (ROS uses 'ros' horizon only)
                test_values_dict = self.config_generator.generate_horizon_test_values(param_name)

                # For accuracy sim, all params are WEEK_SPECIFIC_PARAMS, so we get per-horizon values
                # For ROS mode, we only care about 'ros' horizon
                if 'ros' in test_values_dict:
                    test_values = test_values_dict['ros']
                else:
                    # Fallback for shared params (shouldn't happen in accuracy sim)
                    test_values = test_values_dict['shared']

                progress = ProgressTracker(len(test_values), f"Parameter {param_idx + 1}/{total_params}")

                for test_idx, test_value in enumerate(test_values):
                    # Get config for 'ros' horizon with this test value
                    config_dict = self.config_generator.get_config_for_horizon('ros', param_name, test_idx)

                    # Evaluate configuration
                    result = self._evaluate_config_ros(config_dict)

                    # Record result
                    is_new_best = self.results_manager.add_result('ros', config_dict, result)

                    progress.update()

                # Save intermediate results after all test values evaluated (once per parameter)
                self._current_optimal_config_path = self.results_manager.save_intermediate_results(
                    param_idx, param_name
                )

                # Update ConfigGenerator baseline with best config for next parameter
                best_perf = self.results_manager.get_best_config('ros')
                if best_perf:
                    # Update 'ros' horizon baseline
                    self.config_generator.update_baseline_for_horizon('ros', best_perf.config_dict)
                    current_base_config = copy.deepcopy(best_perf.config_dict)

            # Clean up old optimal folders before creating new one (same pattern as win-rate simulation)
            cleanup_old_accuracy_optimal_folders(self.output_dir)

            # Save final optimal configs
            optimal_path = self.results_manager.save_optimal_configs()
            self._current_optimal_config_path = optimal_path

            self.logger.info(f"ROS optimization complete. Results saved to: {optimal_path}")
            return optimal_path

        finally:
            self._restore_signal_handlers()

    def run_weekly_optimization(self) -> Path:
        """
        Run weekly optimization for all week ranges with auto-resume support.

        Iteratively tests configurations to find optimal parameters
        for predicting weekly player performance.

        **Auto-Resume Feature:**
            If interrupted mid-optimization, automatically resumes from the last completed
            parameter based on existing accuracy_intermediate_*/ folders.

        Returns:
            Path: Path to optimal configuration folder
        """
        self.logger.info("Starting weekly accuracy optimization")
        self._setup_signal_handlers()

        try:
            total_params = len(self.parameter_order)

            # Detect if we should resume from a previous run
            should_resume, start_idx, last_config_path = self._detect_resume_state('weekly')

            if should_resume:
                self.logger.info(f"Resuming from parameter {start_idx + 1}/{total_params}")
                # Load intermediate results into results_manager
                if last_config_path and self.results_manager.load_intermediate_results(last_config_path):
                    self.logger.info(f"Loaded intermediate results from {last_config_path.name}")
                else:
                    self.logger.warning("Failed to load intermediate results, starting fresh")
                    should_resume = False
                    start_idx = 0
            else:
                # Starting fresh - cleanup any existing intermediate folders
                intermediate_folders = [p for p in self.output_dir.glob("accuracy_intermediate_*") if p.is_dir()]
                if intermediate_folders:
                    self.logger.info(f"Cleaning up {len(intermediate_folders)} intermediate folders")
                    for folder in intermediate_folders:
                        try:
                            shutil.rmtree(folder)
                            self.logger.debug(f"  Deleted: {folder.name}")
                        except Exception as e:
                            self.logger.warning(f"  Failed to delete {folder.name}: {e}")
                    self.logger.info("Cleanup complete")

            # Run for each week range
            for week_key, week_range in WEEK_RANGES.items():
                self.logger.info(f"Optimizing for {week_key} (weeks {week_range[0]}-{week_range[1]})")

                # Map week_key to horizon name
                # week_1_5 -> '1-5', week_6_9 -> '6-9', etc.
                horizon = week_key.replace('week_', '').replace('_', '-')

                # Get current base config - either from results_manager or baseline
                if should_resume:
                    best_perf = self.results_manager.get_best_config(week_key)
                    if best_perf:
                        current_base_config = copy.deepcopy(best_perf.config_dict)
                    else:
                        current_base_config = copy.deepcopy(self.config_generator.baseline_configs[horizon])
                else:
                    # Reset to original baseline for each week range
                    current_base_config = copy.deepcopy(self.config_generator.baseline_configs[horizon])

                for param_idx, param_name in enumerate(self.parameter_order):
                    # Skip already-completed parameters when resuming
                    if should_resume and param_idx < start_idx:
                        self.logger.debug(f"Skipping already-completed parameter {param_idx}: {param_name}")
                        continue

                    self.logger.info(
                        f"[{week_key}] Optimizing parameter {param_idx + 1}/{total_params}: {param_name}"
                    )

                    # Generate test values for this parameter (per-horizon for WEEK_SPECIFIC_PARAMS)
                    test_values_dict = self.config_generator.generate_horizon_test_values(param_name)

                    # Get test values for this specific horizon
                    if horizon in test_values_dict:
                        test_values = test_values_dict[horizon]
                    else:
                        # Fallback for shared params (shouldn't happen in accuracy sim)
                        test_values = test_values_dict['shared']

                    progress = ProgressTracker(len(test_values), f"[{week_key}] Param {param_idx + 1}/{total_params}")

                    for test_idx, test_value in enumerate(test_values):
                        # Get config for this horizon with this test value
                        config_dict = self.config_generator.get_config_for_horizon(horizon, param_name, test_idx)

                        # Evaluate configuration for this week range
                        result = self._evaluate_config_weekly(config_dict, week_range)

                        # Record result
                        is_new_best = self.results_manager.add_result(week_key, config_dict, result)

                        if is_new_best:
                            self._current_optimal_config_path = self.results_manager.save_intermediate_results(
                                param_idx, f"{week_key}_{param_name}"
                            )

                        progress.update()

                    # Update ConfigGenerator baseline with best config for next parameter
                    best_perf = self.results_manager.get_best_config(week_key)
                    if best_perf:
                        self.config_generator.update_baseline_for_horizon(horizon, best_perf.config_dict)
                        current_base_config = copy.deepcopy(best_perf.config_dict)

                # After completing all params for this week range, clear resume flag
                # (next week range should not skip any params)
                should_resume = False
                start_idx = 0

            # Clean up old optimal folders before creating new one (same pattern as win-rate simulation)
            cleanup_old_accuracy_optimal_folders(self.output_dir)

            # Save final optimal configs
            optimal_path = self.results_manager.save_optimal_configs()
            self._current_optimal_config_path = optimal_path

            self.logger.info(f"Weekly optimization complete. Results saved to: {optimal_path}")
            return optimal_path

        finally:
            self._restore_signal_handlers()

    def run_both(self) -> Path:
        """
        Run tournament optimization: each parameter optimizes across ALL 5 horizons.

        For each parameter:
        - Generate test configs from 5 baseline configs (one per horizon)
        - Evaluate each config across all 5 horizons
        - Track best config for each horizon independently
        - Save intermediate results (all 5 best configs)
        - Update baselines for next parameter

        Returns:
            Path: Path to optimal configuration folder
        """
        # Setup signal handlers (existing pattern)
        self._setup_signal_handlers()

        try:
            # Auto-resume detection
            should_resume, resume_param_idx, last_config_path = self._detect_resume_state()
            if should_resume:
                self.logger.info(f"Resuming from parameter {resume_param_idx + 1}")
                self.results_manager.load_intermediate_results(last_config_path)

            # Main optimization loop
            for param_idx, param_name in enumerate(self.parameter_order):
                # Skip if resuming and before resume point
                if should_resume and param_idx <= resume_param_idx:
                    continue

                # Generate test values for all 5 horizons
                test_values_dict = self.config_generator.generate_horizon_test_values(param_name)
                # Returns: {'ros': [...], '1-5': [...], '6-9': [...], '10-13': [...], '14-17': [...]}

                # Check for empty test values (fail fast)
                for horizon, test_values in test_values_dict.items():
                    if len(test_values) == 0:
                        raise ValueError(f"No test values generated for parameter {param_name}, horizon {horizon}")

                # Calculate total configs and evaluations for progress tracking
                total_configs = sum(len(vals) for vals in test_values_dict.values())
                total_evaluations = total_configs * 5  # Each config × 5 horizons

                self.logger.info(f"Optimizing parameter {param_idx + 1}/{len(self.parameter_order)}: {param_name}")
                self.logger.info(f"  Evaluating {total_configs} configs × 5 horizons = {total_evaluations} total evaluations")

                # Create progress tracker
                from simulation.shared.ProgressTracker import MultiLevelProgressTracker
                self.progress_tracker = MultiLevelProgressTracker(
                    outer_total=total_configs,
                    inner_total=5,
                    outer_desc="Configs",
                    inner_desc="Horizons"
                )

                # Collect all configs to evaluate
                configs_to_evaluate = []
                config_metadata = []  # Track (horizon, test_idx) for each config

                for horizon, test_values in test_values_dict.items():
                    for test_idx, test_value in enumerate(test_values):
                        config_dict = self.config_generator.get_config_for_horizon(horizon, param_name, test_idx)
                        configs_to_evaluate.append(config_dict)
                        config_metadata.append((horizon, test_idx))

                # Initialize parallel runner (lazy)
                if self.parallel_runner is None:
                    from simulation.accuracy.ParallelAccuracyRunner import ParallelAccuracyRunner
                    self.parallel_runner = ParallelAccuracyRunner(
                        self.data_folder,
                        self.available_seasons,
                        max_workers=self.max_workers,
                        use_processes=self.use_processes
                    )

                # Progress callback
                def progress_update(completed):
                    self.progress_tracker.next_outer()  # Increment outer level

                # Evaluate all configs in parallel with progress tracking
                evaluation_results = self.parallel_runner.evaluate_configs_parallel(
                    configs_to_evaluate,
                    progress_callback=progress_update
                )

                # Close progress tracker
                self.progress_tracker.close()

                # Record all results
                for (config_dict, results_dict), (horizon, test_idx) in zip(evaluation_results, config_metadata):
                    # Record results for each horizon
                    for result_horizon, result in results_dict.items():
                        is_new_best = self.results_manager.add_result(
                            result_horizon,
                            config_dict,
                            result,
                            param_name=param_name,
                            test_idx=test_idx,
                            base_horizon=horizon
                        )

                        # Log new bests
                        if is_new_best:
                            self.logger.info(f"    New best for {result_horizon}: MAE={result.mae:.4f} (test_{test_idx})")

                # After all configs tested, save intermediate results
                self.results_manager.save_intermediate_results(
                    param_idx,
                    param_name
                )

                # Update baselines for all 5 horizons
                for week_key in ['ros', 'week_1_5', 'week_6_9', 'week_10_13', 'week_14_17']:
                    best_perf = self.results_manager.best_configs.get(week_key)
                    if best_perf is not None:
                        self.config_generator.update_baseline_for_horizon(week_key, best_perf.config_dict)
                    else:
                        self.logger.warning(f"No best config found for {week_key} after parameter {param_name}")

                # Log parameter summary (Q25, Q44 decisions)
                self._log_parameter_summary(param_name)

            # Save optimal configs
            optimal_path = self.results_manager.save_optimal_configs()
            self.logger.info(f"Tournament optimization complete. Results saved to {optimal_path}")

            return optimal_path

        finally:
            self._restore_signal_handlers()

    def _log_parameter_summary(self, param_name: str) -> None:
        """Log summary of best results for all horizons after parameter completes."""
        self.logger.info(f"Parameter {param_name} complete:")

        # Use underscore keys to match best_configs dict
        for week_key in ['ros', 'week_1_5', 'week_6_9', 'week_10_13', 'week_14_17']:
            best_perf = self.results_manager.best_configs.get(week_key)
            if best_perf:
                test_idx = best_perf.test_idx if best_perf.test_idx is not None else '?'
                self.logger.info(f"  {week_key}: MAE={best_perf.mae:.4f} (test_{test_idx})")
            else:
                self.logger.info(f"  {week_key}: No results yet")
