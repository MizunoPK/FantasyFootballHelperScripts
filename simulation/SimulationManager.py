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

import time
import copy
import json
import re
import signal
from pathlib import Path
from typing import Optional, Tuple

import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.LoggingManager import get_logger

sys.path.append(str(Path(__file__).parent))
from ConfigGenerator import ConfigGenerator
from ParallelLeagueRunner import ParallelLeagueRunner
from ResultsManager import ResultsManager
from ProgressTracker import MultiLevelProgressTracker


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
        num_test_values: int = 5,
        num_parameters_to_test: int = 1,
        auto_update_league_config: bool = True
    ) -> None:
        """
        Initialize SimulationManager.

        Args:
            baseline_config_path (Path): Path to baseline configuration JSON
            output_dir (Path): Directory to save results (default: simulation/results)
            num_simulations_per_config (int): Simulations per config (default: 100)
            max_workers (int): Number of parallel workers (default: 8)
            data_folder (Path): Data folder, defaults to simulation/sim_data
            num_test_values (int): Number of test values per parameter (default: 5)
                Creates (num_test_values + 1)^6 total configurations
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

        # Track current optimal config for graceful shutdown
        self._current_optimal_config_path: Optional[Path] = None
        self._original_sigint_handler = None
        self._original_sigterm_handler = None

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self.config_generator = ConfigGenerator(baseline_config_path, num_test_values=num_test_values, num_parameters_to_test=num_parameters_to_test)
        self.parallel_runner = ParallelLeagueRunner(
            max_workers=max_workers,
            data_folder=data_folder
        )
        self.results_manager = ResultsManager()

        total_configs = (num_test_values + 1) ** 6
        self.logger.info(
            f"SimulationManager initialized: {total_configs:,} configs, "
            f"{num_simulations_per_config} sims/config, {max_workers} workers"
        )

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

    def run_full_optimization(self) -> Path:
        """
        Run complete optimization process for all 46,656 configurations.

        This is the main entry point for the simulation system. It:
        1. Generates all parameter combinations
        2. Runs simulations for each configuration in parallel
        3. Tracks performance across all configs
        4. Saves optimal configuration and full results

        Returns:
            Path: Path to saved optimal configuration file

        Example:
            >>> mgr = SimulationManager(baseline_path, num_simulations_per_config=100)
            >>> optimal_config_path = mgr.run_full_optimization()
            >>> print(f"Optimal config saved to: {optimal_config_path}")
        """
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

        Scans the output directory for intermediate_*.json files and determines
        whether to resume optimization from where it left off or start fresh.

        Returns:
            Tuple[bool, int, Optional[Path]]: A tuple containing:
                - should_resume (bool): True if resuming, False if starting fresh
                - start_idx (int): Index to start from (0 if starting fresh)
                - last_config_path (Optional[Path]): Path to last intermediate file if resuming

        Logic:
            - No intermediate files → (False, 0, None) - start from beginning
            - Files for all parameters → (False, 0, None) - completed, cleanup and restart
            - Files for some parameters → (True, highest_idx, path) - resume from next parameter
            - Parameter order mismatch → (False, 0, None) - validation failed, start fresh
            - Corrupted files → Skip invalid files, use highest valid index found
        """
        # Get all intermediate files
        intermediate_files = list(self.output_dir.glob("intermediate_*.json"))

        if not intermediate_files:
            self.logger.debug("No intermediate files found")
            return (False, 0, None)

        # Parse all files and collect valid ones
        valid_files = []
        param_order = self.config_generator.PARAMETER_ORDER
        pattern = r'intermediate_(\d+)_(.+)\.json'

        for filepath in intermediate_files:
            filename = filepath.name
            match = re.match(pattern, filename)

            if not match:
                self.logger.warning(f"Skipping file with invalid name format: {filename}")
                continue

            try:
                param_idx = int(match.group(1))
                param_name = match.group(2)

                # Validate parameter order (strict validation per user preference)
                if param_idx > len(param_order):
                    # Index exceeds parameter count - treat as completed run
                    self.logger.debug(f"File {filename}: idx {param_idx} > {len(param_order)} (completed run)")
                    continue

                # Check parameter name matches expected parameter at this index
                expected_param = param_order[param_idx - 1]  # idx is 1-based in filename
                if param_name != expected_param:
                    self.logger.warning(
                        f"Parameter order mismatch in {filename}: "
                        f"expected '{expected_param}', found '{param_name}'. "
                        f"Starting fresh."
                    )
                    return (False, 0, None)

                # Try to parse JSON to ensure file is not corrupted
                with open(filepath, 'r') as f:
                    config = json.load(f)

                # Validate required fields
                if 'config_name' not in config or 'parameters' not in config:
                    self.logger.warning(f"Skipping corrupted intermediate file (missing fields): {filename}")
                    continue

                # File is valid
                valid_files.append((param_idx, param_name, filepath))

            except json.JSONDecodeError:
                self.logger.warning(f"Skipping corrupted intermediate file (invalid JSON): {filename}")
                continue
            except Exception as e:
                self.logger.warning(f"Error processing {filename}: {e}")
                continue

        # No valid files found
        if not valid_files:
            self.logger.debug("No valid intermediate files found after validation")
            return (False, 0, None)

        # Find highest valid index
        valid_files.sort(key=lambda x: x[0])
        highest_idx, highest_param, highest_path = valid_files[-1]

        # Check if all parameters are complete
        if highest_idx >= len(param_order):
            self.logger.debug(f"All parameters complete (idx {highest_idx} >= {len(param_order)})")
            return (False, 0, None)

        # Resume from next parameter
        self.logger.debug(
            f"Found {len(valid_files)} valid intermediate files, "
            f"highest: {highest_param} (idx {highest_idx})"
        )
        return (True, highest_idx, highest_path)

    def run_iterative_optimization(self) -> Path:
        """
        Run iterative parameter optimization (coordinate descent) with auto-resume support.

        Optimizes one parameter at a time in sequence, fixing previously optimized
        parameters. Much faster than full grid search but finds local optimum only.

        **Auto-Resume Feature:**
            If interrupted mid-optimization, automatically resumes from the last completed
            parameter based on existing intermediate_*.json files in the output directory.
            - Detects partial runs and continues where it left off
            - Validates parameter order consistency before resuming
            - Cleans up intermediate files when optimization completes

        Process:
            1. Detect resume state from intermediate files (if any)
            2. Start with baseline config (or resume from last intermediate config)
            3. For each parameter in PARAMETER_ORDER (starting from resume point):
               - Generate configs varying only that parameter
               - Run simulations for each config
               - Select best performing value
               - Update current optimal config
               - Save intermediate result
            4. Save final optimal config and cleanup intermediate files

        Returns:
            Path: Path to saved optimal configuration file

        Example:
            >>> mgr = SimulationManager(baseline_path, num_simulations_per_config=100)
            >>> optimal_config_path = mgr.run_iterative_optimization()
            >>> # Optimizes 24 params × 6 values = 144 configs total
            >>> # If interrupted, restart will resume from last completed parameter
        """
        self.logger.info("=" * 80)
        self.logger.info("STARTING ITERATIVE PARAMETER OPTIMIZATION")
        self.logger.info("=" * 80)

        # Set up signal handlers for graceful shutdown
        if self.auto_update_league_config:
            self._setup_signal_handlers()

        start_time = time.time()

        # Get parameter order
        param_order = self.config_generator.PARAMETER_ORDER
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

        if should_resume:
            # Resume from previous run
            self.logger.info(f"Found {len(list(self.output_dir.glob('intermediate_*.json')))} intermediate files, "
                           f"resuming from parameter {start_idx + 1} of {num_params}")

            # Load config from last intermediate file
            try:
                with open(last_config_path, 'r') as f:
                    current_optimal_config = json.load(f)
                self.logger.info(f"✓ Loaded config from {last_config_path.name}")
            except Exception as e:
                self.logger.warning(f"Failed to load resume config: {e}. Starting fresh.")
                should_resume = False
                start_idx = 0
                current_optimal_config = copy.deepcopy(self.config_generator.baseline_config)
        else:
            # Starting fresh - cleanup any existing intermediate files
            intermediate_files = list(self.output_dir.glob("intermediate_*.json"))
            if intermediate_files:
                reason = "completed run detected" if intermediate_files else "no intermediate files"
                self.logger.info(f"Starting optimization from beginning ({reason})")
                self.logger.info(f"Cleaning up {len(intermediate_files)} intermediate files from completed run")
                for intermediate_file in intermediate_files:
                    try:
                        intermediate_file.unlink()
                        self.logger.debug(f"  Deleted: {intermediate_file.name}")
                    except Exception as e:
                        self.logger.warning(f"  Failed to delete {intermediate_file.name}: {e}")
                self.logger.info("✓ Cleanup complete")
            else:
                self.logger.info("Starting optimization from beginning (no intermediate files)")

            # Start with baseline config as current optimal
            current_optimal_config = copy.deepcopy(self.config_generator.baseline_config)
            start_idx = 0

        self.logger.info("=" * 80)
        win_percentage = 0.0

        # Iterate through each parameter (starting from start_idx if resuming)
        for param_idx, param_name in enumerate(param_order[start_idx:], start=start_idx + 1):
            self.logger.info("=" * 80)
            self.logger.info(f"OPTIMIZING PARAMETER {param_idx}/{num_params}: {param_name}")
            self.logger.info("=" * 80)

            # Generate configs for this parameter
            configs = self.config_generator.generate_iterative_combinations(
                param_name,
                current_optimal_config
            )

            self.logger.info(f"Testing {len(configs)} configurations...")

            # Clear previous results for clean comparison
            self.results_manager = ResultsManager()

            # Run simulations for each config
            for config_idx, config in enumerate(configs):
                config_id = f"{param_name}_{config_idx}"

                # Register config
                self.results_manager.register_config(config_id, config)

                # Run simulations
                results = self.parallel_runner.run_simulations_for_config(
                    config,
                    self.num_simulations_per_config
                )

                # Record results
                for wins, losses, points in results:
                    self.results_manager.record_result(config_id, wins, losses, points)

                self.logger.info(f"  Completed config {config_idx + 1}/{len(configs)}")

            # Get best config for this parameter
            best_result = self.results_manager.get_best_config()

            if best_result:
                self.logger.info("=" * 80)
                self.logger.info(f"BEST VALUE FOR {param_name}:")
                self.logger.info(f"  Win Rate: {best_result.get_win_rate():.2%}")
                self.logger.info(f"  Avg Points: {best_result.get_avg_points_per_league():.2f}")
                self.logger.info(f"  Record: {best_result.total_wins}W-{best_result.total_losses}L")

                # Update current optimal config
                current_optimal_config = best_result.config_dict

                # Save intermediate result
                intermediate_path = self.output_dir / f"intermediate_{param_idx:02d}_{param_name}.json"
                current_optimal_config["config_name"] = str(intermediate_path)
                win_percentage = best_result.get_win_rate()
                current_optimal_config["description"] = f"Win Rate: {win_percentage:.2f}"
                with open(intermediate_path, 'w') as f:
                    json.dump(current_optimal_config, f, indent=2)
                self.logger.info(f"  Saved intermediate config: {intermediate_path.name}")

                # Track for graceful shutdown
                self._current_optimal_config_path = intermediate_path
            else:
                self.logger.warning(f"No results for {param_name} - keeping previous optimal")

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

        # Save final optimal config
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        optimal_config_path = self.output_dir / f"optimal_iterative_{timestamp}.json"
        current_optimal_config["config_name"] = str(optimal_config_path)

        with open(optimal_config_path, 'w') as f:
            json.dump(current_optimal_config, f, indent=2)

        self.logger.info(f"✓ Final optimal config saved: {optimal_config_path}")

        # Track final config for graceful shutdown
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

        self.logger.info("=" * 80)
        self.logger.info("ITERATIVE OPTIMIZATION COMPLETE")
        self.logger.info("=" * 80)

        return optimal_config_path

    def run_single_config_test(self, config_id: str = "test") -> None:
        """
        Run simulations for a single configuration (for debugging).

        Args:
            config_id (str): Identifier for this test config (default: "test")

        Example:
            >>> mgr = SimulationManager(baseline_path, num_simulations_per_config=5)
            >>> mgr.run_single_config_test(config_id="baseline_test")
            >>> # Runs 5 simulations with baseline config
        """
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
