"""
Parallel League Runner

Runs multiple league simulations in parallel using ThreadPoolExecutor or
ProcessPoolExecutor. Coordinates simulation execution and result collection
with thread-safe progress tracking.

Key Features:
- Multi-threaded simulation execution (ThreadPoolExecutor, default)
- Multi-process simulation execution (ProcessPoolExecutor, optional)
- Thread-safe result collection
- Progress tracking callbacks
- Exception handling and error reporting
- Configurable worker pool

Author: Kai Mizuno
"""

from pathlib import Path
from typing import Dict, Callable, Optional, Tuple, List
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Future, as_completed
import threading
import gc
import multiprocessing

import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.LoggingManager import get_logger

sys.path.append(str(Path(__file__).parent))
from SimulatedLeague import SimulatedLeague


# Garbage collection frequency - force GC every N simulations to prevent memory accumulation
# Lower value = more aggressive memory management, slightly more overhead
GC_FREQUENCY = 5


# =============================================================================
# Module-level functions for ProcessPoolExecutor (can't pickle instance methods)
# =============================================================================

def _run_simulation_process(args: Tuple[dict, int, Path]) -> Tuple[int, int, float]:
    """
    Run a single simulation in a separate process.

    This is a module-level function required for ProcessPoolExecutor,
    which cannot pickle instance methods.

    Args:
        args: Tuple of (config_dict, simulation_id, data_folder)

    Returns:
        Tuple[int, int, float]: (wins, losses, total_points) for DraftHelperTeam
    """
    config_dict, simulation_id, data_folder = args
    league = None
    try:
        league = SimulatedLeague(config_dict, data_folder)
        league.run_draft()
        league.run_season()
        wins, losses, total_points = league.get_draft_helper_results()
        return wins, losses, total_points
    finally:
        if league:
            league.cleanup()
            del league


def _run_simulation_with_weeks_process(args: Tuple[dict, int, Path]) -> List[Tuple[int, bool, float]]:
    """
    Run a single simulation with week tracking in a separate process.

    This is a module-level function required for ProcessPoolExecutor.

    Args:
        args: Tuple of (config_dict, simulation_id, data_folder)

    Returns:
        List[Tuple[int, bool, float]]: Per-week results as list of
            (week_number, won, points) tuples
    """
    config_dict, simulation_id, data_folder = args
    league = None
    try:
        league = SimulatedLeague(config_dict, data_folder)
        league.run_draft()
        league.run_season()
        week_results = league.get_draft_helper_results_by_week()
        return week_results
    finally:
        if league:
            league.cleanup()
            del league


class ParallelLeagueRunner:
    """
    Runs multiple league simulations in parallel.

    Uses ThreadPoolExecutor (default) or ProcessPoolExecutor to run simulations
    concurrently, with thread-safe progress tracking and result collection.
    Each simulation runs in isolation with its own temporary data directories.

    ThreadPoolExecutor (default):
        - Lower overhead, shared memory
        - Limited by Python GIL for CPU-bound work
        - Best for I/O-bound or mixed workloads

    ProcessPoolExecutor (use_processes=True):
        - True parallelism, bypasses GIL
        - Higher overhead (process creation, serialization)
        - Best for CPU-bound simulations on multi-core systems

    Attributes:
        max_workers (int): Number of concurrent workers
        data_folder (Path): Base folder containing season data
        use_processes (bool): If True, use ProcessPoolExecutor for true parallelism
        logger: Logger instance
        progress_callback (Optional[Callable]): Function called after each simulation
        lock (threading.Lock): Lock for thread-safe progress updates
    """

    def __init__(
        self,
        max_workers: int = 4,
        data_folder: Optional[Path] = None,
        progress_callback: Optional[Callable[[int, int], None]] = None,
        use_processes: bool = False
    ) -> None:
        """
        Initialize ParallelLeagueRunner.

        Args:
            max_workers (int): Number of concurrent workers (default 4)
            data_folder (Optional[Path]): Base data folder, defaults to simulation/sim_data
            progress_callback (Optional[Callable]): Function(completed, total) called
                after each simulation completes
            use_processes (bool): If True, use ProcessPoolExecutor for true parallelism.
                Default False uses ThreadPoolExecutor. ProcessPoolExecutor bypasses
                Python's GIL, providing real speedup on multi-core systems for
                CPU-bound simulation work.
        """
        self.max_workers = max_workers
        self.data_folder = data_folder or Path("simulation/sim_data")
        self.use_processes = use_processes
        self.logger = get_logger()
        self.progress_callback = progress_callback
        self.lock = threading.Lock()

        executor_type = "ProcessPoolExecutor" if use_processes else "ThreadPoolExecutor"
        self.logger.info(f"ParallelLeagueRunner initialized with {max_workers} workers ({executor_type})")

    def set_data_folder(self, data_folder: Path) -> None:
        """
        Update the data folder for subsequent simulations.

        This allows reusing the same runner across multiple seasons/datasets
        without recreating the ThreadPoolExecutor.

        Args:
            data_folder (Path): New data folder path
        """
        self.data_folder = data_folder
        self.logger.debug(f"ParallelLeagueRunner data_folder updated to: {data_folder}")

    def run_single_simulation(
        self,
        config_dict: dict,
        simulation_id: int
    ) -> Tuple[int, int, float]:
        """
        Run a single league simulation (thread-safe).

        This method is executed by worker threads. It creates a SimulatedLeague,
        runs the draft and season, and returns the DraftHelperTeam's results.

        Args:
            config_dict (dict): Configuration dictionary for this simulation
            simulation_id (int): Unique ID for this simulation run

        Returns:
            Tuple[int, int, float]: (wins, losses, total_points) for DraftHelperTeam

        Raises:
            Exception: Any exception during simulation is logged and re-raised
        """
        try:
            self.logger.debug(f"[Sim {simulation_id}] Starting simulation")

            # Create league with this config
            league = SimulatedLeague(config_dict, self.data_folder)

            # Run draft
            self.logger.debug(f"[Sim {simulation_id}] Running draft")
            league.run_draft()

            # Run season
            self.logger.debug(f"[Sim {simulation_id}] Running season")
            league.run_season()

            # Get results
            wins, losses, total_points = league.get_draft_helper_results()

            self.logger.debug(
                f"[Sim {simulation_id}] Complete: {wins}W-{losses}L, {total_points:.2f} pts"
            )

            return wins, losses, total_points

        except Exception as e:
            self.logger.error(f"[Sim {simulation_id}] Failed: {e}", exc_info=True)
            raise
        finally:
            # Explicit cleanup to prevent memory accumulation
            # Previously relied on __del__() which caused OOM when Python GC delayed cleanup
            league.cleanup()
            # Explicitly delete to help garbage collector free memory immediately
            del league
            self.logger.debug(f"[Sim {simulation_id}] Cleanup complete")

    def run_single_simulation_with_weeks(
        self,
        config_dict: dict,
        simulation_id: int
    ) -> List[Tuple[int, bool, float]]:
        """
        Run a single league simulation and return per-week results (thread-safe).

        Like run_single_simulation, but returns per-week breakdown for
        week-by-week config optimization.

        Args:
            config_dict (dict): Configuration dictionary for this simulation
            simulation_id (int): Unique ID for this simulation run

        Returns:
            List[Tuple[int, bool, float]]: Per-week results as list of
                (week_number, won, points) tuples

        Raises:
            Exception: Any exception during simulation is logged and re-raised
        """
        try:
            self.logger.debug(f"[Sim {simulation_id}] Starting simulation (with week data)")

            # Create league with this config
            league = SimulatedLeague(config_dict, self.data_folder)

            # Run draft
            self.logger.debug(f"[Sim {simulation_id}] Running draft")
            league.run_draft()

            # Run season
            self.logger.debug(f"[Sim {simulation_id}] Running season")
            league.run_season()

            # Get per-week results
            week_results = league.get_draft_helper_results_by_week()

            # Log summary
            wins = sum(1 for _, won, _ in week_results if won)
            losses = len(week_results) - wins
            total_pts = sum(pts for _, _, pts in week_results)

            self.logger.debug(
                f"[Sim {simulation_id}] Complete: {wins}W-{losses}L, {total_pts:.2f} pts"
            )

            return week_results

        except Exception as e:
            self.logger.error(f"[Sim {simulation_id}] Failed: {e}", exc_info=True)
            raise
        finally:
            # Explicit cleanup to prevent memory accumulation
            league.cleanup()
            del league
            self.logger.debug(f"[Sim {simulation_id}] Cleanup complete")

    def run_simulations_for_config(
        self,
        config_dict: dict,
        num_simulations: int
    ) -> list[Tuple[int, int, float]]:
        """
        Run multiple simulations for a single configuration in parallel.

        Uses ThreadPoolExecutor (default) or ProcessPoolExecutor based on
        the use_processes setting.

        Args:
            config_dict (dict): Configuration dictionary
            num_simulations (int): Number of simulations to run

        Returns:
            list[Tuple[int, int, float]]: List of (wins, losses, points) tuples

        Example:
            >>> runner = ParallelLeagueRunner(max_workers=8)
            >>> results = runner.run_simulations_for_config(config, 100)
            >>> # Returns num_simulations results: [(10, 7, 1404.62), (12, 5, 1523.45), ...]
        """
        executor_type = "processes" if self.use_processes else "threads"
        self.logger.info(
            f"Running {num_simulations} simulations with {self.max_workers} {executor_type}"
        )

        results = []
        completed_count = 0

        # Choose executor type based on use_processes flag
        ExecutorClass = ProcessPoolExecutor if self.use_processes else ThreadPoolExecutor

        with ExecutorClass(max_workers=self.max_workers) as executor:
            if self.use_processes:
                # ProcessPoolExecutor: use module-level function with args tuple
                sim_args = [
                    (config_dict, sim_id, self.data_folder)
                    for sim_id in range(num_simulations)
                ]
                future_to_sim_id = {
                    executor.submit(_run_simulation_process, args): args[1]
                    for args in sim_args
                }
            else:
                # ThreadPoolExecutor: use instance method (can access self)
                future_to_sim_id = {
                    executor.submit(self.run_single_simulation, config_dict, sim_id): sim_id
                    for sim_id in range(num_simulations)
                }

            # Collect results as they complete
            for future in as_completed(future_to_sim_id):
                sim_id = future_to_sim_id[future]

                try:
                    result = future.result()
                    results.append(result)

                    # Update progress (thread-safe)
                    with self.lock:
                        completed_count += 1
                        if self.progress_callback:
                            self.progress_callback(completed_count, num_simulations)

                        # Force garbage collection periodically to prevent memory accumulation
                        # Note: GC in main process doesn't affect worker processes
                        if completed_count % GC_FREQUENCY == 0:
                            gc.collect()
                            self.logger.debug(f"Forced GC after {completed_count} simulations")

                except Exception as e:
                    self.logger.error(f"Simulation {sim_id} failed: {e}")
                    # Continue with other simulations even if one fails

        self.logger.info(
            f"Completed {len(results)}/{num_simulations} simulations successfully"
        )

        return results

    def run_simulations_for_config_with_weeks(
        self,
        config_dict: dict,
        num_simulations: int
    ) -> list[List[Tuple[int, bool, float]]]:
        """
        Run multiple simulations for a single configuration with per-week tracking.

        Like run_simulations_for_config, but returns per-week results for
        week-by-week config optimization. Uses ThreadPoolExecutor (default) or
        ProcessPoolExecutor based on the use_processes setting.

        Args:
            config_dict (dict): Configuration dictionary
            num_simulations (int): Number of simulations to run

        Returns:
            list[List[Tuple[int, bool, float]]]: List of per-week results,
                where each inner list contains (week, won, points) tuples

        Example:
            >>> runner = ParallelLeagueRunner(max_workers=8)
            >>> results = runner.run_simulations_for_config_with_weeks(config, 100)
            >>> # Returns num_simulations results, each with 16 week entries:
            >>> # [[(1, True, 125.5), (2, False, 98.3), ...], ...]
        """
        executor_type = "processes" if self.use_processes else "threads"
        self.logger.info(
            f"Running {num_simulations} simulations with week tracking ({self.max_workers} {executor_type})"
        )

        results = []
        completed_count = 0

        # Choose executor type based on use_processes flag
        ExecutorClass = ProcessPoolExecutor if self.use_processes else ThreadPoolExecutor

        with ExecutorClass(max_workers=self.max_workers) as executor:
            if self.use_processes:
                # ProcessPoolExecutor: use module-level function with args tuple
                sim_args = [
                    (config_dict, sim_id, self.data_folder)
                    for sim_id in range(num_simulations)
                ]
                future_to_sim_id = {
                    executor.submit(_run_simulation_with_weeks_process, args): args[1]
                    for args in sim_args
                }
            else:
                # ThreadPoolExecutor: use instance method (can access self)
                future_to_sim_id = {
                    executor.submit(self.run_single_simulation_with_weeks, config_dict, sim_id): sim_id
                    for sim_id in range(num_simulations)
                }

            # Collect results as they complete
            for future in as_completed(future_to_sim_id):
                sim_id = future_to_sim_id[future]

                try:
                    result = future.result()
                    results.append(result)

                    # Update progress (thread-safe)
                    with self.lock:
                        completed_count += 1
                        if self.progress_callback:
                            self.progress_callback(completed_count, num_simulations)

                        # Force garbage collection periodically
                        if completed_count % GC_FREQUENCY == 0:
                            gc.collect()
                            self.logger.debug(f"Forced GC after {completed_count} simulations")

                except Exception as e:
                    self.logger.error(f"Simulation {sim_id} failed: {e}")

        self.logger.info(
            f"Completed {len(results)}/{num_simulations} simulations successfully (with weeks)"
        )

        return results

    def run_multiple_configs(
        self,
        config_dicts: list[dict],
        simulations_per_config: int
    ) -> Dict[str, list[Tuple[int, int, float]]]:
        """
        Run simulations for multiple configurations.

        This method runs simulations for each config sequentially, but each
        config's simulations run in parallel. This approach ensures fair
        comparison between configs (all get same treatment).

        Args:
            config_dicts (list[dict]): List of configuration dictionaries
            simulations_per_config (int): Number of simulations per config

        Returns:
            Dict[str, list[Tuple[int, int, float]]]: {config_name: [results]}

        Example:
            >>> configs = [config1, config2, config3]
            >>> results = runner.run_multiple_configs(configs, 100)
            >>> # Returns {'config_0001': [(10, 7, 1404.62), ...], 'config_0002': [...]}
        """
        self.logger.info(
            f"Running {len(config_dicts)} configs with {simulations_per_config} "
            f"simulations each (total: {len(config_dicts) * simulations_per_config})"
        )

        all_results = {}

        for idx, config_dict in enumerate(config_dicts, 1):
            config_name = config_dict.get('config_name', f'config_{idx:04d}')

            self.logger.info(
                f"[{idx}/{len(config_dicts)}] Running simulations for {config_name}"
            )

            # Run simulations for this config
            results = self.run_simulations_for_config(config_dict, simulations_per_config)
            all_results[config_name] = results

        self.logger.info(f"All {len(config_dicts)} configs completed")
        return all_results

    def test_single_run(self, config_dict: dict) -> Tuple[int, int, float]:
        """
        Test a single simulation run (synchronous, for debugging).

        Args:
            config_dict (dict): Configuration dictionary

        Returns:
            Tuple[int, int, float]: (wins, losses, points) for DraftHelperTeam

        Example:
            >>> runner = ParallelLeagueRunner()
            >>> wins, losses, points = runner.test_single_run(config)
            >>> print(f"Result: {wins}W-{losses}L, {points:.2f} pts")
        """
        self.logger.info("Running single test simulation")
        return self.run_single_simulation(config_dict, simulation_id=0)
