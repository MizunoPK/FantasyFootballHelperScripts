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
from pathlib import Path
from typing import Optional

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
        num_parameters_to_test: int = 1
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

        # Save all results
        all_results_path = self.output_dir / "all_results.json"
        self.results_manager.save_all_results(all_results_path)
        self.logger.info(f"✓ Saved all results: {all_results_path}")

        self.logger.info("=" * 80)
        self.logger.info("OPTIMIZATION PROCESS COMPLETE")
        self.logger.info("=" * 80)

        return optimal_config_path

    def run_iterative_optimization(self) -> Path:
        """
        Run iterative parameter optimization (coordinate descent).

        Optimizes one parameter at a time in sequence, fixing previously optimized
        parameters. Much faster than full grid search but finds local optimum only.

        Process:
            1. Start with baseline config
            2. For each parameter in PARAMETER_ORDER:
               - Generate configs varying only that parameter
               - Run simulations for each config
               - Select best performing value
               - Update current optimal config
            3. Save final optimal config

        Returns:
            Path: Path to saved optimal configuration file

        Example:
            >>> mgr = SimulationManager(baseline_path, num_simulations_per_config=100)
            >>> optimal_config_path = mgr.run_iterative_optimization()
            >>> # Optimizes 24 params × 6 values = 144 configs total
        """
        self.logger.info("=" * 80)
        self.logger.info("STARTING ITERATIVE PARAMETER OPTIMIZATION")
        self.logger.info("=" * 80)

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

        # Clean up any existing intermediate files from previous runs
        intermediate_files = list(self.output_dir.glob("intermediate_*.json"))
        if intermediate_files:
            self.logger.info(f"Cleaning up {len(intermediate_files)} intermediate files from previous runs...")
            for intermediate_file in intermediate_files:
                try:
                    intermediate_file.unlink()
                    self.logger.debug(f"  Deleted: {intermediate_file.name}")
                except Exception as e:
                    self.logger.warning(f"  Failed to delete {intermediate_file.name}: {e}")
            self.logger.info("✓ Cleanup complete")
            self.logger.info("=" * 80)

        # Start with baseline config as current optimal
        current_optimal_config = copy.deepcopy(self.config_generator.baseline_config)
        win_percentage = 0.0

        # Iterate through each parameter
        for param_idx, param_name in enumerate(param_order, 1):
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

        self.logger.info("=" * 80)
        self.logger.info(f"✓ Final optimal config saved: {optimal_config_path}")
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
