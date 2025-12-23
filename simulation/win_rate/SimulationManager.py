"""
Simulation Manager

Orchestrates the complete configuration optimization process. Coordinates
ConfigGenerator, ParallelLeagueRunner, and ResultsManager to test all 46,656
configurations and identify the optimal parameter settings.

The full process:
1. Load baseline configuration
2. Generate 46,656 parameter combinations
3. For each configuration:
   - Run N simulations in parallel
   - Collect results (wins, losses, points)
4. Aggregate results and identify best configuration
5. Save optimal config and full results

Author: Kai Mizuno
"""

import csv
import copy
import json
import re
import signal
import shutil
import time
import warnings
from pathlib import Path
from typing import Optional, Tuple, Dict, List

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.LoggingManager import get_logger

# Import from shared folder
sys.path.append(str(Path(__file__).parent.parent / "shared"))
from ConfigGenerator import ConfigGenerator
from ResultsManager import ResultsManager
from ProgressTracker import MultiLevelProgressTracker
from ConfigPerformance import WEEK_RANGES
from config_cleanup import cleanup_old_optimal_folders, cleanup_intermediate_folders

# Import from same folder (win_rate/)
sys.path.append(str(Path(__file__).parent))
from ParallelLeagueRunner import ParallelLeagueRunner


class SimulationManager:
    """
    Manages the complete configuration optimization process.

    Coordinates all simulation components to test thousands of configurations
    and identify the optimal parameter settings for the DraftHelper system.

    Attributes:
        baseline_config_path (Path): Path to baseline configuration
        output_dir (Path): Directory to save results
        num_simulations_per_config (int): Number of simulations per configuration
        max_workers (int): Number of parallel worker threads
        config_generator (ConfigGenerator): Generates parameter combinations
        parallel_runner (ParallelLeagueRunner): Runs simulations in parallel
        results_manager (ResultsManager): Tracks and aggregates results
        logger: Logger instance
    """

    def __init__(
        self,
        baseline_config_path: Path,
        output_dir: Path,
        num_simulations_per_config : int,
        max_workers : int,
        data_folder: Path,
        parameter_order: List[str],
        num_test_values: int = 5,
        num_parameters_to_test: int = 1,
        auto_update_league_config: bool = True,
        use_processes: bool = False
    ) -> None:
        """
        Initialize SimulationManager.

        Args:
            baseline_config_path (Path): Path to baseline configuration JSON
            output_dir (Path): Directory to save results (default: simulation/results)
            num_simulations_per_config (int): Simulations per config (default: 100)
            max_workers (int): Number of parallel workers (default: 8)
            data_folder (Path): Data folder, defaults to simulation/sim_data
            parameter_order (List[str]): List of parameter names defining optimization order.
                Each name must exist in ConfigGenerator.PARAM_DEFINITIONS.
            num_test_values (int): Number of test values per parameter (default: 5)
                Creates (num_test_values + 1)^6 total configurations
            use_processes (bool): If True, use ProcessPoolExecutor for true parallelism.
                Default False uses ThreadPoolExecutor. ProcessPoolExecutor bypasses
                Python's GIL, providing real speedup on multi-core systems for
                CPU-bound simulation work.
        """
        self.logger = get_logger()
        self.logger.info("Initializing SimulationManager")

        self.baseline_config_path = baseline_config_path
        self.output_dir = output_dir
        self.num_simulations_per_config = num_simulations_per_config
        self.max_workers = max_workers
        self.num_test_values = num_test_values
        self.num_parameters_to_test = num_parameters_to_test
        self.data_folder = data_folder
        self.auto_update_league_config = auto_update_league_config
        self.use_processes = use_processes

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
        self.parallel_runner = ParallelLeagueRunner(
            max_workers=max_workers,
            data_folder=data_folder,
            use_processes=use_processes
        )
        self.results_manager = ResultsManager()

        total_configs = (num_test_values + 1) ** 6
        executor_type = "ProcessPoolExecutor" if use_processes else "ThreadPoolExecutor"
        self.logger.info(
            f"SimulationManager initialized: {total_configs:,} configs, "
            f"{num_simulations_per_config} sims/config, {max_workers} workers ({executor_type})"
        )

        # Discover available historical seasons
        self.available_seasons = self._discover_seasons()
        self.logger.info(f"Discovered {len(self.available_seasons)} historical seasons: {[s.name for s in self.available_seasons]}")

    def _discover_seasons(self) -> List[Path]:
        """
        Find all valid historical season folders (20XX/) in data_folder.

        Validates each folder has required structure before including.
        Fails loudly if no valid seasons are found.

        Returns:
            List[Path]: Sorted list of valid season folder paths

        Raises:
            FileNotFoundError: If no historical season folders exist
        """
        season_folders = sorted(self.data_folder.glob("20*/"))

        if not season_folders:
            raise FileNotFoundError(
                f"No historical season folders (20XX/) found in {self.data_folder}. "
                "Run compile_historical_data.py first."
            )

        valid = []
        for folder in season_folders:
            self._validate_season_strict(folder)  # Raises on invalid
            valid.append(folder)

        return valid

    def _validate_season_strict(self, folder: Path) -> None:
        """
        Validate season folder has all required structure.

        Checks for:
        - season_schedule.csv
        - game_data.csv
        - team_data/ folder
        - weeks/ folder with all 17 week subfolders
        - players.csv in each week folder

        Args:
            folder (Path): Season folder to validate

        Raises:
            FileNotFoundError: If any required file/folder is missing
        """
        year = folder.name

        # Check required root files
        required_files = [folder / "season_schedule.csv", folder / "game_data.csv"]
        for req_file in required_files:
            if not req_file.exists():
                raise FileNotFoundError(f"Season {year} missing: {req_file.name}")

        # Check team_data folder
        if not (folder / "team_data").exists():
            raise FileNotFoundError(f"Season {year} missing team_data/")

        # Check weeks folder
        weeks_folder = folder / "weeks"
        if not weeks_folder.exists():
            raise FileNotFoundError(f"Season {year} missing weeks/")

        # Check all 17 weeks exist with required files
        for week_num in range(1, 18):
            week_folder = weeks_folder / f"week_{week_num:02d}"
            if not week_folder.exists():
                raise FileNotFoundError(f"Season {year} missing week_{week_num:02d}/")
            if not (week_folder / "players.csv").exists():
                raise FileNotFoundError(f"Season {year} week_{week_num:02d}/ missing players.csv")

    def _validate_season_data(self, season_folder: Path) -> bool:
        """
        Validate season has sufficient valid player data for simulation.

        A season needs at least 150 valid players (drafted=0 AND fantasy_points>0)
        to support a 10-team draft with 15 picks each.

        Args:
            season_folder (Path): Path to season folder

        Returns:
            bool: True if season has sufficient data, False otherwise
        """
        MIN_VALID_PLAYERS = 150  # 10 teams × 15 picks

        # Check week 1 players_projected.csv for valid player count
        players_file = season_folder / "weeks" / "week_01" / "players_projected.csv"
        if not players_file.exists():
            players_file = season_folder / "weeks" / "week_01" / "players.csv"

        if not players_file.exists():
            self.logger.warning(f"Season {season_folder.name}: No player CSV found")
            return False

        try:
            with open(players_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                valid_count = 0
                for row in reader:
                    drafted = row.get('drafted', '0')
                    fp = row.get('fantasy_points', '')
                    try:
                        fp_val = float(fp) if fp else 0
                    except (ValueError, TypeError):
                        fp_val = 0
                    if drafted == '0' and fp_val > 0:
                        valid_count += 1

                if valid_count < MIN_VALID_PLAYERS:
                    self.logger.warning(
                        f"Season {season_folder.name}: Only {valid_count} valid players "
                        f"(need {MIN_VALID_PLAYERS}+ for draft)"
                    )
                    return False

                self.logger.debug(f"Season {season_folder.name}: {valid_count} valid players - OK")
                return True

        except Exception as e:
            self.logger.warning(f"Season {season_folder.name}: Error reading player data: {e}")
            return False

    def _setup_signal_handlers(self) -> None:
        """
        Set up signal handlers for graceful shutdown.

        Registers handlers for SIGINT (Ctrl+C) and SIGTERM to ensure
        league_config.json is updated before the process exits.
        """
        self._original_sigint_handler = signal.signal(signal.SIGINT, self._handle_shutdown_signal)
        self._original_sigterm_handler = signal.signal(signal.SIGTERM, self._handle_shutdown_signal)

    def _restore_signal_handlers(self) -> None:
        """Restore original signal handlers."""
        if self._original_sigint_handler is not None:
            signal.signal(signal.SIGINT, self._original_sigint_handler)
        if self._original_sigterm_handler is not None:
            signal.signal(signal.SIGTERM, self._original_sigterm_handler)

    def _handle_shutdown_signal(self, signum: int, frame) -> None:
        """
        Handle shutdown signal by updating league config before exiting.

        Args:
            signum: Signal number received
            frame: Current stack frame (unused)
        """
        signal_name = "SIGINT" if signum == signal.SIGINT else "SIGTERM"
        self.logger.info(f"\nReceived {signal_name} - performing graceful shutdown...")

        # Update league config if we have an optimal config saved
        if self.auto_update_league_config and self._current_optimal_config_path:
            league_config_path = Path(__file__).parent.parent / "data" / "league_config.json"
            if league_config_path.exists() and self._current_optimal_config_path.exists():
                self.logger.info(f"Updating league config before shutdown...")
                self.results_manager.update_league_config(
                    self._current_optimal_config_path,
                    league_config_path
                )
                self.logger.info(f"✓ Updated league config: {league_config_path}")

        # Restore original handlers and re-raise signal
        self._restore_signal_handlers()
        self.logger.info("Shutdown complete. Exiting...")
        raise SystemExit(0)

    def _run_season_simulations_with_weeks(
        self,
        config_dict: dict,
        num_simulations_per_season: int
    ) -> List[List[Tuple[int, bool, float]]]:
        """
        Run simulations across ALL historical seasons with per-week tracking.

        This method runs the specified number of simulations for each discovered
        historical season and aggregates the results. Each season uses its own
        data folder with week-specific player data.

        Args:
            config_dict (dict): Configuration dictionary
            num_simulations_per_season (int): Number of simulations per season

        Returns:
            List[List[Tuple[int, bool, float]]]: Aggregated per-week results from
                all seasons and simulations. Each inner list is a single simulation's
                week results: [(week_num, won, points), ...]

        Note:
            Win rate should be calculated as: Total wins / Total games
            across ALL seasons, not averaged per season.
        """
        all_results = []
        total_seasons = len(self.available_seasons)

        self.logger.info(f"Running simulations across {total_seasons} historical seasons")

        for season_idx, season_folder in enumerate(self.available_seasons):
            # Validate season has sufficient player data
            if not self._validate_season_data(season_folder):
                self.logger.warning(f"Skipping season {season_folder.name} - insufficient valid player data")
                continue
            season_name = season_folder.name
            self.logger.debug(f"Season {season_idx + 1}/{total_seasons}: {season_name}")

            # OPTIMIZATION: Reuse existing runner, just update data folder
            # This avoids recreating ThreadPoolExecutor for each season
            self.parallel_runner.set_data_folder(season_folder)

            # Run simulations for this season
            season_results = self.parallel_runner.run_simulations_for_config_with_weeks(
                config_dict,
                num_simulations_per_season
            )

            # Add to aggregated results
            all_results.extend(season_results)

            self.logger.debug(
                f"  Season {season_name}: {len(season_results)} simulations complete"
            )

        total_simulations = len(all_results)
        self.logger.info(
            f"Multi-season simulations complete: {total_simulations} total "
            f"({num_simulations_per_season} x {total_seasons} seasons)"
        )

        return all_results

    def run_full_optimization(self) -> Path:
        """
        Run complete optimization process for all 46,656 configurations.

        .. deprecated::
            This method uses single-season data only. Use `run_iterative_optimization()`
            instead for multi-season validation across all historical data.

        This is the main entry point for the simulation system. It:
        1. Generates all parameter combinations
        2. Runs simulations for each configuration in parallel
        3. Tracks performance across all configs
        4. Saves optimal configuration and full results

        Returns:
            Path: Path to saved optimal configuration file

        Example:
            >>> mgr = SimulationManager(baseline_path, output_dir, num_sims, workers, data, param_order)
            >>> optimal_config_path = mgr.run_full_optimization()
            >>> print(f"Optimal config saved to: {optimal_config_path}")
        """
        warnings.warn(
            "run_full_optimization() uses single-season data only. "
            "Use run_iterative_optimization() for multi-season validation.",
            DeprecationWarning,
            stacklevel=2
        )

        self.logger.info("=" * 80)
        self.logger.info("STARTING FULL CONFIGURATION OPTIMIZATION")
        self.logger.info("=" * 80)

        # Set up signal handlers for graceful shutdown
        if self.auto_update_league_config:
            self._setup_signal_handlers()

        start_time = time.time()

        # Generate all configurations
        self.logger.info("Generating parameter combinations...")
        combinations = self.config_generator.generate_all_combinations()
        self.logger.info(f"Generated {len(combinations)} parameter combinations")

        # Register all configs with ResultsManager
        self.logger.info("Registering configurations...")
        for idx, combo in enumerate(combinations):
            config_id = f"config_{idx:05d}"
            config_dict = self.config_generator.create_config_dict(combo)
            self.results_manager.register_config(config_id, config_dict)
        self.logger.info(f"Registered {len(combinations)} configurations")

        # Run simulations for all configs
        self.logger.info("=" * 80)
        self.logger.info(f"Running {self.num_simulations_per_config} simulations per config")
        self.logger.info(f"Total simulations: {len(combinations) * self.num_simulations_per_config}")
        self.logger.info("=" * 80)

        # Create progress tracker
        progress_tracker = MultiLevelProgressTracker(
            outer_total=len(combinations),
            inner_total=self.num_simulations_per_config,
            outer_desc="Configs",
            inner_desc="Sims"
        )

        def progress_callback(completed: int, total: int) -> None:
            """Callback for inner progress updates."""
            progress_tracker.update_inner(completed)

        self.parallel_runner.progress_callback = progress_callback

        # Run simulations for each config
        for idx, combo in enumerate(combinations):
            config_id = f"config_{idx:05d}"
            config_dict = self.config_generator.create_config_dict(combo)

            # Run simulations for this config
            results = self.parallel_runner.run_simulations_for_config(
                config_dict,
                self.num_simulations_per_config
            )

            # Record results
            for wins, losses, points in results:
                self.results_manager.record_result(config_id, wins, losses, points)

            # Move to next config
            progress_tracker.next_outer()

        progress_tracker.finish()

        # Calculate elapsed time
        elapsed = time.time() - start_time

        # Display results summary
        self.logger.info("=" * 80)
        self.logger.info("OPTIMIZATION COMPLETE")
        self.logger.info("=" * 80)
        self.logger.info(f"Total time: {self._format_time(elapsed)}")
        self.logger.info(
            f"Processed {len(combinations)} configs × "
            f"{self.num_simulations_per_config} sims = "
            f"{len(combinations) * self.num_simulations_per_config} total simulations"
        )

        self.results_manager.print_summary(top_n=10)

        # Save results
        self.logger.info("=" * 80)
        self.logger.info("SAVING RESULTS")
        self.logger.info("=" * 80)

        # Save optimal config
        optimal_config_path = self.results_manager.save_optimal_config(self.output_dir)
        self.logger.info(f"✓ Saved optimal config: {optimal_config_path}")

        # Track for graceful shutdown
        self._current_optimal_config_path = optimal_config_path

        # Update league_config.json in the root data folder with optimal parameters
        if self.auto_update_league_config:
            league_config_path = Path(__file__).parent.parent / "data" / "league_config.json"
            if league_config_path.exists():
                self.results_manager.update_league_config(optimal_config_path, league_config_path)
                self.logger.info(f"✓ Updated league config: {league_config_path}")
            else:
                self.logger.warning(f"league_config.json not found at {league_config_path}, skipping update")

            # Restore signal handlers now that we're done
            self._restore_signal_handlers()

        # Save all results
        all_results_path = self.output_dir / "all_results.json"
        self.results_manager.save_all_results(all_results_path)
        self.logger.info(f"✓ Saved all results: {all_results_path}")

        self.logger.info("=" * 80)
        self.logger.info("OPTIMIZATION PROCESS COMPLETE")
        self.logger.info("=" * 80)

        return optimal_config_path

    def _detect_resume_state(self) -> Tuple[bool, int, Optional[Path]]:
        """
        Detect if iterative optimization should resume from a previous run.

        Scans the output directory for intermediate_*/ folders and determines
        whether to resume optimization from where it left off or start fresh.

        Per Q3 answer: If old intermediate_*.json files are detected (from the old
        system), raises an error requiring manual cleanup.

        Returns:
            Tuple[bool, int, Optional[Path]]: A tuple containing:
                - should_resume (bool): True if resuming, False if starting fresh
                - start_idx (int): Index to start from (0 if starting fresh)
                - last_config_path (Optional[Path]): Path to last intermediate folder if resuming

        Logic:
            - No intermediate folders → (False, 0, None) - start from beginning
            - Folders for all parameters → (False, 0, None) - completed, cleanup and restart
            - Folders for some parameters → (True, highest_idx, path) - resume from next parameter
            - Parameter order mismatch → (False, 0, None) - validation failed, start fresh
            - Invalid folders → Skip invalid folders, use highest valid index found
            - Old .json files detected → Raise ValueError requiring cleanup
        """
        # Check for old-style JSON files (per Q3: error and stop)
        old_json_files = list(self.output_dir.glob("intermediate_*.json"))
        if old_json_files:
            raise ValueError(
                f"Found {len(old_json_files)} old intermediate_*.json files in {self.output_dir}. "
                f"The new system uses folder structure. Please delete these files manually and restart."
            )

        # Get all intermediate folders
        intermediate_folders = [
            p for p in self.output_dir.glob("intermediate_*")
            if p.is_dir()
        ]

        if not intermediate_folders:
            self.logger.debug("No intermediate folders found")
            return (False, 0, None)

        # Parse all folders and collect valid ones
        valid_folders = []
        param_order = self.parameter_order
        pattern = r'intermediate_(\d+)_(.+)'

        for folder_path in intermediate_folders:
            folder_name = folder_path.name
            match = re.match(pattern, folder_name)

            if not match:
                self.logger.warning(f"Skipping folder with invalid name format: {folder_name}")
                continue

            try:
                param_idx = int(match.group(1))
                param_name = match.group(2)

                # Validate parameter order (strict validation per user preference)
                if param_idx > len(param_order):
                    self.logger.debug(f"Folder {folder_name}: idx {param_idx} > {len(param_order)} (completed run)")
                    continue

                # Check parameter name matches expected parameter at this index
                expected_param = param_order[param_idx - 1]  # idx is 1-based in folder name
                if param_name != expected_param:
                    self.logger.warning(
                        f"Parameter order mismatch in {folder_name}: "
                        f"expected '{expected_param}', found '{param_name}'. "
                        f"Starting fresh."
                    )
                    return (False, 0, None)

                # Check that folder contains required files
                required_files = ['league_config.json', 'week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']
                missing_files = [f for f in required_files if not (folder_path / f).exists()]

                if missing_files:
                    self.logger.warning(
                        f"Skipping incomplete folder {folder_name}: missing {', '.join(missing_files)}"
                    )
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
        if highest_idx >= len(param_order):
            self.logger.debug(f"All parameters complete (idx {highest_idx} >= {len(param_order)})")
            return (False, 0, None)

        # Resume from next parameter
        self.logger.debug(
            f"Found {len(valid_folders)} valid intermediate folders, "
            f"highest: {highest_param} (idx {highest_idx})"
        )
        return (True, highest_idx, highest_path)

    def run_iterative_optimization(self) -> Path:
        """
        Run iterative parameter optimization (coordinate descent) with auto-resume support.

        Optimizes one parameter at a time in sequence, fixing previously optimized
        parameters. Much faster than full grid search but finds local optimum only.

        **Week-by-Week Optimization:**
            - BASE parameters are optimized for overall best performance
            - WEEK-SPECIFIC parameters are optimized per week range (1-5, 6-9, 10-13, 14-17)
            - Output is a folder with 5 config files

        **Auto-Resume Feature:**
            If interrupted mid-optimization, automatically resumes from the last completed
            parameter based on existing intermediate_*/ folders in the output directory.

        Returns:
            Path: Path to saved optimal configuration folder

        Example:
            >>> mgr = SimulationManager(baseline_path, output_dir, num_sims, workers, data, param_order)
            >>> optimal_config_folder = mgr.run_iterative_optimization()
        """
        self.logger.info("=" * 80)
        self.logger.info("STARTING ITERATIVE PARAMETER OPTIMIZATION (WEEK-BY-WEEK)")
        self.logger.info("=" * 80)

        # Set up signal handlers for graceful shutdown
        if self.auto_update_league_config:
            self._setup_signal_handlers()

        start_time = time.time()

        # Get parameter order
        param_order = self.parameter_order
        num_params = len(param_order)
        configs_per_param = self.num_test_values + 1
        total_configs = num_params * configs_per_param

        self.logger.info(f"Parameters to optimize: {num_params}")
        self.logger.info(f"Configs per parameter: {configs_per_param}")
        self.logger.info(f"Total configs: {total_configs}")
        self.logger.info(f"Total simulations: {total_configs * self.num_simulations_per_config}")
        self.logger.info("=" * 80)

        # Detect if we should resume from a previous run
        should_resume, start_idx, last_config_path = self._detect_resume_state()

        # Initialize base_config and week_configs
        if should_resume:
            # Resume from previous run - load from folder
            self.logger.info(f"Found intermediate folders, resuming from parameter {start_idx + 1} of {num_params}")

            try:
                base_config, week_configs = ResultsManager.load_configs_from_folder(last_config_path)
                self.logger.info(f"✓ Loaded configs from {last_config_path.name}")
            except Exception as e:
                self.logger.warning(f"Failed to load resume config: {e}. Starting fresh.")
                should_resume = False
                start_idx = 0
                base_config, week_configs = self._initialize_configs_from_baseline()
        else:
            # Starting fresh - cleanup any existing intermediate folders
            intermediate_folders = [p for p in self.output_dir.glob("intermediate_*") if p.is_dir()]
            if intermediate_folders:
                self.logger.info(f"Cleaning up {len(intermediate_folders)} intermediate folders")
                for folder in intermediate_folders:
                    try:
                        shutil.rmtree(folder)
                        self.logger.debug(f"  Deleted: {folder.name}")
                    except Exception as e:
                        self.logger.warning(f"  Failed to delete {folder.name}: {e}")
                self.logger.info("✓ Cleanup complete")
            else:
                self.logger.info("Starting optimization from beginning (no intermediate folders)")

            # Initialize from baseline
            base_config, week_configs = self._initialize_configs_from_baseline()
            start_idx = 0

        self.logger.info("=" * 80)

        # Iterate through each parameter (starting from start_idx if resuming)
        for param_idx, param_name in enumerate(param_order[start_idx:], start=start_idx + 1):
            self.logger.info("=" * 80)
            self.logger.info(f"OPTIMIZING PARAMETER {param_idx}/{num_params}: {param_name}")

            # Check if this is a base or week-specific parameter
            is_week_specific = self.config_generator.is_week_specific_param(param_name)
            param_type = "WEEK-SPECIFIC" if is_week_specific else "BASE"
            self.logger.info(f"  Type: {param_type}")
            self.logger.info("=" * 80)

            # Generate test values for this parameter
            test_values_dict = self.config_generator.generate_horizon_test_values(param_name)

            # For BASE_CONFIG_PARAMS, win-rate sim tests each value across all 4 horizons
            # For WEEK_SPECIFIC_PARAMS (not used by win-rate sim), would test per-horizon
            if 'shared' in test_values_dict:
                # Shared parameter: test each value across all 4 horizons
                test_values = test_values_dict['shared']
                horizons = ['1-5', '6-9', '10-13', '14-17']
            else:
                # Week-specific parameter: currently not used by win-rate sim
                # If this path is taken, log warning and skip
                self.logger.warning(f"Parameter {param_name} is week-specific but win-rate sim only optimizes BASE_CONFIG_PARAMS")
                continue

            self.logger.info(f"Testing {len(test_values)} values across {len(horizons)} horizons...")

            # Clear previous results for clean comparison
            self.results_manager = ResultsManager()

            # Test each value across all horizons
            for test_idx, test_value in enumerate(test_values):
                # For each horizon, get config with this test value
                for horizon in horizons:
                    config = self.config_generator.get_config_for_horizon(horizon, param_name, test_idx)
                    config_id = f"{param_name}_{test_idx}_horizon_{horizon}"

                    # Register config
                    self.results_manager.register_config(config_id, config)

                    # Run simulations WITH WEEK TRACKING across ALL historical seasons
                    week_results_list = self._run_season_simulations_with_weeks(
                        config,
                        self.num_simulations_per_config
                    )

                    # Record per-week results
                    for week_results in week_results_list:
                        self.results_manager.record_week_results(config_id, week_results)

                self.logger.info(f"  Completed test value {test_idx + 1}/{len(test_values)}")

            # Update configs based on results and collect performance metrics
            overall_performance = None
            week_range_performance = {}

            # For BASE_CONFIG_PARAMS (shared params), find overall best across all horizons
            # Win-rate sim only optimizes BASE_CONFIG_PARAMS, so this path is always taken
            best_result = self.results_manager.get_best_config()

            if best_result:
                self.logger.info("=" * 80)
                self.logger.info(f"BEST VALUE FOR {param_name}:")
                self.logger.info(f"  Win Rate: {best_result.get_win_rate():.2%}")
                self.logger.info(f"  Avg Points: {best_result.get_avg_points_per_league():.2f}")
                self.logger.info(f"  Best Config ID: {best_result.config_id}")

                # Collect overall performance metrics
                overall_performance = {
                    'win_rate': best_result.get_win_rate(),
                    'total_wins': best_result.total_wins,
                    'total_losses': best_result.total_losses,
                    'config_id': best_result.config_id
                }

                # Update ConfigGenerator's baseline for ALL horizons (shared param)
                # Extract which test_idx won by parsing config_id (format: "{param_name}_{test_idx}_horizon_{horizon}")
                # The best config_id tells us which test value performed best
                # Find the test_idx by looking for the pattern: _NUMBER_horizon_
                match = re.search(r'_(\d+)_horizon_', best_result.config_id)
                if match:
                    best_test_idx = int(match.group(1))

                    # Update baseline for all horizons with the best test value
                    # For shared params, update_baseline_for_horizon updates all 5 horizons
                    for horizon in horizons:
                        best_config = self.config_generator.get_config_for_horizon(horizon, param_name, best_test_idx)
                        self.config_generator.update_baseline_for_horizon(horizon, best_config)

                    self.logger.info(f"  Updated all horizon baselines with test value at index {best_test_idx}")

                # Also update legacy base_config and week_configs for intermediate folder saving
                # These are maintained for backward compatibility with save logic
                self._update_base_config_param(base_config, param_name, best_result.config_dict)

            # Also collect current best overall performance for reference in all configs
            current_best = self.results_manager.get_best_config()
            if current_best and not overall_performance:
                overall_performance = {
                    'win_rate': current_best.get_win_rate(),
                    'total_wins': current_best.total_wins,
                    'total_losses': current_best.total_losses,
                    'config_id': current_best.config_id
                }

            # Collect week range performance if not already collected
            if not week_range_performance:
                for week_range in WEEK_RANGES:
                    best_for_range = self.results_manager.get_best_config_for_range(week_range)
                    if best_for_range:
                        week_range_performance[week_range] = {
                            'win_rate': best_for_range.get_win_rate_for_range(week_range),
                            'config_id': best_for_range.config_id
                        }

            # Save intermediate result as folder with performance metrics
            self.results_manager.save_intermediate_folder(
                self.output_dir,
                param_idx,
                param_name,
                base_config,
                week_configs,
                overall_performance=overall_performance,
                week_range_performance=week_range_performance
            )
            self.logger.info(f"  Saved intermediate folder: intermediate_{param_idx:02d}_{param_name}/")

        # Calculate elapsed time
        elapsed = time.time() - start_time

        # Display final summary
        self.logger.info("=" * 80)
        self.logger.info("ITERATIVE OPTIMIZATION COMPLETE")
        self.logger.info("=" * 80)
        self.logger.info(f"Total time: {self._format_time(elapsed)}")
        self.logger.info(f"Optimized {num_params} parameters")
        self.logger.info(f"Total configs tested: {total_configs}")
        self.logger.info(f"Total simulations: {total_configs * self.num_simulations_per_config}")

        # Save final optimal config as folder
        # Clean up old optimal folders if we're at the limit
        cleanup_old_optimal_folders(self.output_dir)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        final_folder = self.output_dir / f"optimal_iterative_{timestamp}"
        final_folder.mkdir(parents=True, exist_ok=True)

        # Collect final performance metrics
        final_best = self.results_manager.get_best_config()
        final_overall_performance = None
        if final_best:
            final_overall_performance = {
                'win_rate': final_best.get_win_rate(),
                'total_wins': final_best.total_wins,
                'total_losses': final_best.total_losses,
                'config_id': final_best.config_id
            }

        final_week_range_performance = {}
        for week_range in WEEK_RANGES:
            best_for_range = self.results_manager.get_best_config_for_range(week_range)
            if best_for_range:
                final_week_range_performance[week_range] = {
                    'win_rate': best_for_range.get_win_rate_for_range(week_range),
                    'config_id': best_for_range.config_id
                }

        # Add metadata and performance metrics to base config
        base_config['config_name'] = f"Optimal Base Config ({timestamp})"
        base_config['description'] = 'Optimized base parameters for all weeks'
        if final_overall_performance:
            base_config['performance_metrics'] = {
                'overall_win_rate': final_overall_performance['win_rate'],
                'total_wins': final_overall_performance['total_wins'],
                'total_losses': final_overall_performance['total_losses'],
                'config_id': final_overall_performance['config_id'],
                'total_parameters_optimized': num_params,
                'total_configs_tested': total_configs,
                'optimization_time_seconds': elapsed,
                'timestamp': timestamp
            }

        # Save league_config.json (base/shared params)
        with open(final_folder / 'league_config.json', 'w') as f:
            json.dump(base_config, f, indent=2)

        # Save all 4 horizon files (5-file structure: 1 base + 4 week files)
        # Map horizons to filenames
        from simulation.shared.ConfigPerformance import HORIZON_FILES

        for horizon, filename in HORIZON_FILES.items():
            # Get the optimized config for this horizon from ConfigGenerator
            horizon_config = copy.deepcopy(self.config_generator.baseline_configs[horizon])

            # Add metadata
            horizon_config['config_name'] = f"Optimal {filename} ({timestamp})"
            horizon_config['description'] = f'Optimized parameters for weeks {horizon} horizon'

            # Add performance metrics if available
            # For now, use overall performance since we optimized shared params only
            if final_overall_performance and horizon in ['1-5', '6-9', '10-13', '14-17']:
                # Try to get week-range specific performance
                if horizon in final_week_range_performance:
                    perf = final_week_range_performance[horizon]
                    horizon_config['performance_metrics'] = {
                        'horizon': horizon,
                        'win_rate_for_horizon': perf['win_rate'],
                        'config_id': perf['config_id'],
                        'timestamp': timestamp
                    }

            with open(final_folder / filename, 'w') as f:
                json.dump(horizon_config, f, indent=2)

        self.logger.info(f"✓ Final optimal configs saved: {final_folder}")

        # Clean up intermediate folders now that optimization is complete
        deleted_count = cleanup_intermediate_folders(self.output_dir)
        if deleted_count > 0:
            self.logger.info(f"✓ Cleaned up {deleted_count} intermediate folders")

        # Update data/configs folder (per Q5: update folder)
        if self.auto_update_league_config:
            data_configs_path = Path(__file__).parent.parent / "data" / "configs"
            if data_configs_path.exists():
                # Use smart update that preserves user-maintained parameters
                self.results_manager.update_configs_folder(final_folder, data_configs_path)
            else:
                self.logger.warning(f"data/configs folder not found at {data_configs_path}, skipping update")

            # Restore signal handlers now that we're done
            self._restore_signal_handlers()

        self.logger.info("=" * 80)
        self.logger.info("ITERATIVE OPTIMIZATION COMPLETE")
        self.logger.info("=" * 80)

        return final_folder

    def _initialize_configs_from_baseline(self) -> Tuple[dict, Dict[str, dict]]:
        """
        Initialize base_config and week_configs from the baseline configs (5-file structure).

        Returns:
            Tuple[dict, Dict[str, dict]]: (base_config, week_configs)
                week_configs includes all 4 weekly horizons
        """
        # Get all 4 horizon baselines from ConfigGenerator
        # For now, use the '1-5' horizon as the "baseline" for extracting shared params
        baseline = copy.deepcopy(self.config_generator.baseline_configs['1-5'])

        # Extract base params (shared across all horizons)
        base_config = self.results_manager._extract_base_params(baseline)

        # Extract week params from each horizon
        week_configs = {}
        for horizon in ['1-5', '6-9', '10-13', '14-17']:
            horizon_baseline = copy.deepcopy(self.config_generator.baseline_configs[horizon])
            week_params = self.results_manager._extract_week_params(horizon_baseline)
            week_configs[horizon] = week_params

        return base_config, week_configs

    def _merge_configs(self, base_config: dict, week_configs: Dict[str, dict]) -> dict:
        """
        Merge base_config and week_configs into a single config for generating variations.

        Uses week 1-5 config as representative for week-specific params.

        Args:
            base_config: Base configuration
            week_configs: Week-specific configurations

        Returns:
            dict: Merged configuration
        """
        merged = copy.deepcopy(base_config)
        if 'parameters' not in merged:
            merged['parameters'] = {}

        # Merge in week-specific params from week 1-5
        week1_5_params = week_configs.get('1-5', {}).get('parameters', {})
        merged['parameters'].update(week1_5_params)

        return merged

    def _update_base_config_param(self, base_config: dict, param_name: str, best_config: dict) -> None:
        """
        Update a parameter in base_config from the best configuration.

        Args:
            base_config: Base configuration to update
            param_name: Parameter name (from PARAMETER_ORDER)
            best_config: Best performing configuration
        """
        # Map parameter name to config section
        section = self.config_generator.PARAM_TO_SECTION_MAP.get(param_name)
        if not section:
            return

        best_params = best_config.get('parameters', {})
        if 'parameters' not in base_config:
            base_config['parameters'] = {}

        # Handle nested params
        if param_name in ['PRIMARY_BONUS', 'SECONDARY_BONUS']:
            if section not in base_config['parameters']:
                base_config['parameters'][section] = {}
            key = 'PRIMARY' if 'PRIMARY' in param_name else 'SECONDARY'
            if section in best_params:
                base_config['parameters'][section][key] = best_params[section].get(key)
        elif param_name in ['ADP_SCORING_WEIGHT', 'ADP_SCORING_STEPS']:
            if section not in base_config['parameters']:
                base_config['parameters'][section] = {}
            key = 'WEIGHT' if 'WEIGHT' in param_name else 'STEPS'
            if section in best_params and 'THRESHOLDS' in best_params[section]:
                if key == 'STEPS':
                    base_config['parameters'][section].setdefault('THRESHOLDS', {})['STEPS'] = \
                        best_params[section]['THRESHOLDS'].get('STEPS')
                else:
                    base_config['parameters'][section]['WEIGHT'] = best_params[section].get('WEIGHT')
        elif param_name == 'DRAFT_ORDER_FILE':
            # Special case: DRAFT_ORDER_FILE requires updating both the file number
            # AND the DRAFT_ORDER array (which is loaded from the file)
            if 'DRAFT_ORDER_FILE' in best_params:
                base_config['parameters']['DRAFT_ORDER_FILE'] = best_params['DRAFT_ORDER_FILE']
            if 'DRAFT_ORDER' in best_params:
                base_config['parameters']['DRAFT_ORDER'] = best_params['DRAFT_ORDER']
        elif section == param_name:
            # Direct param (not nested)
            if section in best_params:
                base_config['parameters'][section] = best_params[section]

    def _update_week_config_param(self, week_config: dict, param_name: str, best_config: dict) -> None:
        """
        Update a week-specific parameter in week_config from the best configuration.

        Args:
            week_config: Week configuration to update
            param_name: Parameter name (from PARAMETER_ORDER)
            best_config: Best performing configuration for this week range
        """
        section = self.config_generator.PARAM_TO_SECTION_MAP.get(param_name)
        if not section:
            return

        best_params = best_config.get('parameters', {})
        if 'parameters' not in week_config:
            week_config['parameters'] = {}

        # All week-specific params are nested in their section
        if section in best_params:
            if section not in week_config['parameters']:
                week_config['parameters'][section] = {}

            # Extract the specific key being optimized
            if 'WEIGHT' in param_name:
                week_config['parameters'][section]['WEIGHT'] = best_params[section].get('WEIGHT')
            elif 'MIN_WEEKS' in param_name:
                week_config['parameters'][section]['MIN_WEEKS'] = best_params[section].get('MIN_WEEKS')
            elif 'IMPACT_SCALE' in param_name:
                week_config['parameters'][section]['IMPACT_SCALE'] = best_params[section].get('IMPACT_SCALE')
            elif 'STEPS' in param_name:
                week_config['parameters'][section].setdefault('THRESHOLDS', {})['STEPS'] = \
                    best_params[section].get('THRESHOLDS', {}).get('STEPS')
            elif 'HOME' in param_name or 'AWAY' in param_name or 'INTERNATIONAL' in param_name:
                key = param_name.replace('LOCATION_', '')
                week_config['parameters'][section][key] = best_params[section].get(key)

    def run_single_config_test(self, config_id: str = "test") -> None:
        """
        Run simulations for a single configuration (for debugging).

        .. deprecated::
            This method uses single-season data only. Use `run_iterative_optimization()`
            instead for multi-season validation across all historical data.

        Args:
            config_id (str): Identifier for this test config (default: "test")

        Example:
            >>> mgr = SimulationManager(baseline_path, output_dir, num_sims, workers, data, param_order)
            >>> mgr.run_single_config_test(config_id="baseline_test")
            >>> # Runs 5 simulations with baseline config
        """
        warnings.warn(
            "run_single_config_test() uses single-season data only. "
            "Use run_iterative_optimization() for multi-season validation.",
            DeprecationWarning,
            stacklevel=2
        )

        self.logger.info("=" * 80)
        self.logger.info("RUNNING SINGLE CONFIG TEST")
        self.logger.info("=" * 80)

        # Use baseline config directly
        config_dict = self.config_generator.baseline_config

        # Register config
        self.results_manager.register_config(config_id, config_dict)

        # Run simulations
        self.logger.info(f"Running {self.num_simulations_per_config} simulations...")

        results = self.parallel_runner.run_simulations_for_config(
            config_dict,
            self.num_simulations_per_config
        )

        # Record results
        for wins, losses, points in results:
            self.results_manager.record_result(config_id, wins, losses, points)

        # Display results
        best = self.results_manager.get_best_config()
        if best:
            self.logger.info("=" * 80)
            self.logger.info("TEST RESULTS")
            self.logger.info("=" * 80)
            self.logger.info(f"Config: {best.config_id}")
            self.logger.info(f"Simulations: {best.num_simulations}")
            self.logger.info(f"Record: {best.total_wins}W-{best.total_losses}L ({best.total_games} games)")
            self.logger.info(f"Win Rate: {best.get_win_rate():.2%}")
            self.logger.info(f"Avg Points/League: {best.get_avg_points_per_league():.2f}")

    def _format_time(self, seconds: float) -> str:
        """
        Format seconds as human-readable time string.

        Args:
            seconds (float): Time in seconds

        Returns:
            str: Formatted time string
        """
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
        else:
            hours = int(seconds / 3600)
            minutes = int((seconds % 3600) / 60)
            return f"{hours}h {minutes}m"
