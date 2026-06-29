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
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from concurrent.futures.process import BrokenProcessPool
import hashlib
import threading
import gc

from utils.LoggingManager import get_logger
from simulation.win_rate.SimulatedLeague import SimulatedLeague


GC_FREQUENCY = 5
_WORKER_PRELOADED_WEEK_DATA: Optional[Dict[int, Dict]] = None


def _init_worker_process(week_data: Optional[Dict[int, Dict]]) -> None:
    global _WORKER_PRELOADED_WEEK_DATA
    _WORKER_PRELOADED_WEEK_DATA = week_data


def _run_simulation_process(args: Tuple[dict, int, Path, bool, Optional[int]]) -> Tuple[int, int, float]:
    """
    Run a single simulation in a separate process.

    This is a module-level function required for ProcessPoolExecutor,
    which cannot pickle instance methods. preloaded_week_data is read
    from the module-level _WORKER_PRELOADED_WEEK_DATA set once per
    worker by _init_worker_process, avoiding per-simulation pickling.

    Args:
        args: Tuple of (config_dict, simulation_id, data_folder, naive_opponents, seed)
            where seed is the per-task deterministic seed (None → entropy default).

    Returns:
        Tuple[int, int, float]: (wins, losses, total_points) for DraftHelperTeam
    """
    config_dict, simulation_id, data_folder, naive_opponents, seed = args
    league = None
    try:
        league = SimulatedLeague(config_dict, data_folder, _WORKER_PRELOADED_WEEK_DATA, naive_opponents=naive_opponents, seed=seed)
        league.run_draft()
        league.run_season()
        wins, losses, total_points = league.get_draft_helper_results()
        return wins, losses, total_points
    finally:
        if league:
            league.cleanup()
            del league


def _run_simulation_with_weeks_process(args: Tuple[dict, int, Path, bool, Optional[int]]) -> List[Tuple[int, bool, float]]:
    """
    Run a single simulation with week tracking in a separate process.

    This is a module-level function required for ProcessPoolExecutor.
    preloaded_week_data is read from the module-level
    _WORKER_PRELOADED_WEEK_DATA set once per worker by
    _init_worker_process, avoiding per-simulation pickling.

    Args:
        args: Tuple of (config_dict, simulation_id, data_folder, naive_opponents, seed)
            where seed is the per-task deterministic seed (None → entropy default).

    Returns:
        List[Tuple[int, bool, float]]: Per-week results as list of
            (week_number, won, points) tuples
    """
    config_dict, simulation_id, data_folder, naive_opponents, seed = args
    league = None
    try:
        league = SimulatedLeague(config_dict, data_folder, _WORKER_PRELOADED_WEEK_DATA, naive_opponents=naive_opponents, seed=seed)
        league.run_draft()
        league.run_season()
        week_results = league.get_draft_helper_results_by_week()
        return week_results
    finally:
        if league:
            league.cleanup()
            del league


def _derive_task_seed(base_seed: int, data_folder: Path, sim_id: int) -> int:
    """Derive a per-task seed deterministic on (base_seed, data_folder, sim_id).

    Uses SHA-256 for cross-process stability — avoids PYTHONHASHSEED non-determinism
    of Python's built-in hash() for non-integer objects. Key is config-independent (D2):
    two different configs evaluated under the same base_seed see the same per-(season,
    sim_id) draws, which is the property the dependent T30 paired/CRN story consumes.

    Args:
        base_seed: The run's base seed (from --seed N).
        data_folder: The active season folder (e.g., Path("simulation/sim_data/2025")).
        sim_id: The simulation index (0 … num_simulations-1).

    Returns:
        A 32-bit unsigned integer suitable as a random.Random seed.
    """
    key = f"{base_seed}:{data_folder.name}:{sim_id}".encode()
    return int(hashlib.sha256(key).hexdigest(), 16) % (2 ** 32)


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
        use_processes: bool = False,
        naive_opponents: bool = False,
        seed: Optional[int] = None
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
            naive_opponents (bool): Forwarded verbatim to every SimulatedLeague this runner
                builds (thread-mode and process-mode workers alike). False (default) selects the
                self-play composition; True selects the legacy naive composition.
            seed (Optional[int]): Base seed for deterministic evaluation (D1/T29). When provided,
                each simulation task receives a per-task seed derived from
                (base_seed, season_folder, sim_id) via _derive_task_seed, making every league's
                RNG deterministic and config-independent (D2). Default None → OS entropy (D3).
        """
        self.max_workers = max_workers
        self.data_folder = data_folder or Path("simulation/sim_data")
        self.use_processes = use_processes
        self.naive_opponents = naive_opponents
        self.seed = seed
        self.logger = get_logger()
        self.progress_callback = progress_callback
        self.lock = threading.Lock()

        # Drop-surfacing counters (KDD-1): reset+set per run_simulations_for_config[/_with_weeks]
        # call so a caller can read the dropped count immediately after the call it just made.
        self.last_requested_count = 0
        self.last_completed_count = 0
        self.last_dropped_count = 0
        # Drop-rate threshold (KDD-2): default 0.0 so any drop already logs at ERROR; when the
        # observed drop rate exceeds this, the ERROR message uses elevated phrasing.
        self.drop_rate_threshold = 0.0

        executor_type = "ProcessPoolExecutor" if use_processes else "ThreadPoolExecutor"
        self.logger.debug(f"ParallelLeagueRunner initialized with {max_workers} workers ({executor_type})")

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
        simulation_id: int,
        preloaded_week_data: Optional[Dict[int, Dict]] = None,
        seed: Optional[int] = None
    ) -> Tuple[int, int, float]:
        """
        Run a single league simulation (thread-safe).

        This method is executed by worker threads. It creates a SimulatedLeague,
        runs the draft and season, and returns the DraftHelperTeam's results.

        Args:
            config_dict (dict): Configuration dictionary for this simulation
            simulation_id (int): Unique ID for this simulation run
            preloaded_week_data (Optional[Dict[int, Dict]]): Pre-loaded week data from
                SimDataLoader. If provided, passed to SimulatedLeague to skip file reads.
            seed (Optional[int]): Per-task deterministic seed derived by the caller (D1/T29).
                None → OS entropy, preserving stochastic behavior (D3).

        Returns:
            Tuple[int, int, float]: (wins, losses, total_points) for DraftHelperTeam

        Raises:
            Exception: Any exception during simulation is logged and re-raised
        """
        league = None
        try:
            league = SimulatedLeague(config_dict, self.data_folder, preloaded_week_data, naive_opponents=self.naive_opponents, seed=seed)

            league.run_draft()
            league.run_season()

            wins, losses, total_points = league.get_draft_helper_results()

            return wins, losses, total_points

        except Exception as e:
            self.logger.error(f"[Sim {simulation_id}] Failed: {e}", exc_info=True)
            raise
        finally:
            if league:
                league.cleanup()
                del league

    def run_single_simulation_with_weeks(
        self,
        config_dict: dict,
        simulation_id: int,
        preloaded_week_data: Optional[Dict[int, Dict]] = None,
        seed: Optional[int] = None
    ) -> List[Tuple[int, bool, float]]:
        """
        Run a single league simulation and return per-week results (thread-safe).

        Like run_single_simulation, but returns per-week breakdown for
        week-by-week config optimization.

        Args:
            config_dict (dict): Configuration dictionary for this simulation
            simulation_id (int): Unique ID for this simulation run
            preloaded_week_data (Optional[Dict[int, Dict]]): Pre-loaded week data from
                SimDataLoader. If provided, passed to SimulatedLeague to skip file reads.
            seed (Optional[int]): Per-task deterministic seed derived by the caller (D1/T29).
                None → OS entropy, preserving stochastic behavior (D3).

        Returns:
            List[Tuple[int, bool, float]]: Per-week results as list of
                (week_number, won, points) tuples

        Raises:
            Exception: Any exception during simulation is logged and re-raised
        """
        league = None
        try:
            league = SimulatedLeague(config_dict, self.data_folder, preloaded_week_data, naive_opponents=self.naive_opponents, seed=seed)

            league.run_draft()
            league.run_season()

            week_results = league.get_draft_helper_results_by_week()

            return week_results

        except Exception as e:
            self.logger.error(f"[Sim {simulation_id}] Failed: {e}", exc_info=True)
            raise
        finally:
            if league:
                league.cleanup()
                del league

    def _derive_task_seeds(self, num_simulations: int) -> List[Optional[int]]:
        """Derive the per-task seed list for a run (D2/T29).

        Config-independent key (base_seed, season, sim_index); returns None for each
        task when self.seed is None, preserving the entropy-default (D3). Shared by
        run_simulations_for_config and run_simulations_for_config_with_weeks so the
        derivation lives in one place.

        Args:
            num_simulations (int): Number of simulation tasks in this run.

        Returns:
            List[Optional[int]]: Per-task seeds aligned to sim_id in range(num_simulations).
        """
        return [
            _derive_task_seed(self.seed, self.data_folder, sim_id) if self.seed is not None else None
            for sim_id in range(num_simulations)
        ]

    def run_simulations_for_config(
        self,
        config_dict: dict,
        num_simulations: int,
        preloaded_week_data: Optional[Dict[int, Dict]] = None
    ) -> list[Tuple[int, int, float]]:
        """
        Run multiple simulations for a single configuration in parallel.

        Uses ThreadPoolExecutor (default) or ProcessPoolExecutor based on
        the use_processes setting.

        Args:
            config_dict (dict): Configuration dictionary
            num_simulations (int): Number of simulations to run
            preloaded_week_data (Optional[Dict[int, Dict]]): Pre-loaded week data from SimDataLoader. If provided, skips per-simulation file reads.

        Returns:
            list[Tuple[int, int, float]]: List of (wins, losses, points) tuples

        Example:
            >>> runner = ParallelLeagueRunner(max_workers=8)
            >>> results = runner.run_simulations_for_config(config, 100)
            >>> # Returns num_simulations results: [(10, 7, 1404.62), (12, 5, 1523.45), ...]
        """
        executor_type = "processes" if self.use_processes else "threads"
        self.logger.debug(
            f"Running {num_simulations} simulations with {self.max_workers} {executor_type}"
        )

        # KDD-1: reset per-call drop counters at the start of every call so they describe
        # exactly this call's outcome (no carry-over from a prior reuse of the runner).
        self.last_requested_count = num_simulations
        self.last_completed_count = 0
        self.last_dropped_count = 0

        results = []
        completed_count = 0

        # Per-task seed derivation (D2/T29) — see _derive_task_seeds.
        task_seeds = self._derive_task_seeds(num_simulations)

        ExecutorClass = ProcessPoolExecutor if self.use_processes else ThreadPoolExecutor
        """Win rate sim uses ThreadPoolExecutor (I/O-bound — disk reads dominate); accuracy sim uses ProcessPoolExecutor (CPU-bound — score computation dominates). ThreadPoolExecutor: lower overhead, sufficient for I/O-bound simulation setup; ProcessPoolExecutor: bypasses GIL for CPU-bound parallelism at the cost of pickling overhead and higher process-creation latency."""
        if self.use_processes:
            executor = ProcessPoolExecutor(
                max_workers=self.max_workers,
                initializer=_init_worker_process,
                initargs=(preloaded_week_data,)
            )
            sim_args = [
                (config_dict, sim_id, self.data_folder, self.naive_opponents, task_seeds[sim_id])
                for sim_id in range(num_simulations)
            ]
            future_to_sim_id = {
                executor.submit(_run_simulation_process, args): args[1]
                for args in sim_args
            }
        else:
            executor = ExecutorClass(max_workers=self.max_workers)
            future_to_sim_id = {
                executor.submit(self.run_single_simulation, config_dict, sim_id, preloaded_week_data, task_seeds[sim_id]): sim_id
                for sim_id in range(num_simulations)
            }

        try:
            for future in as_completed(future_to_sim_id):
                sim_id = future_to_sim_id[future]

                try:
                    result = future.result()
                    results.append(result)

                    with self.lock:
                        completed_count += 1
                        if self.progress_callback:
                            self.progress_callback(completed_count, num_simulations)

                        if completed_count % GC_FREQUENCY == 0:
                            gc.collect()
                            self.logger.debug(f"Forced GC after {completed_count} simulations")

                except BrokenProcessPool:
                    self.logger.error("Process pool crashed — stopping simulations")
                    break
                except Exception as e:
                    self.logger.error(f"Simulation {sim_id} failed: {e}")
        except KeyboardInterrupt:
            self.logger.warning("Simulation interrupted by user")
            raise
        finally:
            executor.shutdown(wait=False, cancel_futures=True)

        self.last_completed_count = len(results)
        self.last_dropped_count = num_simulations - len(results)

        if self.last_dropped_count > 0:
            drop_rate = self.last_dropped_count / num_simulations if num_simulations else 0.0
            msg = (
                f"{self.last_dropped_count}/{num_simulations} leagues dropped "
                f"({len(results)}/{num_simulations} completed, rate={drop_rate:.1%})"
            )
            # KDD-2: prepend the elevated label only when an operator has configured a
            # non-zero drop_rate_threshold AND this drop rate exceeds it. At the default
            # threshold (0.0) every drop still logs at ERROR, with the neutral phrasing.
            if self.drop_rate_threshold > 0.0 and drop_rate > self.drop_rate_threshold:
                msg = f"HIGH DROP RATE: {msg}"
            self.logger.error(msg)

        self.logger.debug(
            f"Completed {len(results)}/{num_simulations} simulations successfully"
        )

        return results

    def run_simulations_for_config_with_weeks(
        self,
        config_dict: dict,
        num_simulations: int,
        preloaded_week_data: Optional[Dict[int, Dict]] = None
    ) -> list[List[Tuple[int, bool, float]]]:
        """
        Run multiple simulations for a single configuration with per-week tracking.

        Like run_simulations_for_config, but returns per-week results for
        week-by-week config optimization. Uses ThreadPoolExecutor (default) or
        ProcessPoolExecutor based on the use_processes setting.

        Args:
            config_dict (dict): Configuration dictionary
            num_simulations (int): Number of simulations to run
            preloaded_week_data (Optional[Dict[int, Dict]]): Pre-loaded week data from SimDataLoader. If provided, skips per-simulation file reads.

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
        self.logger.debug(
            f"Running {num_simulations} simulations with week tracking ({self.max_workers} {executor_type})"
        )

        # KDD-1: reset per-call drop counters at the start of every call so they describe
        # exactly this call's outcome (no carry-over from a prior reuse of the runner).
        self.last_requested_count = num_simulations
        self.last_completed_count = 0
        self.last_dropped_count = 0

        results = []
        completed_count = 0

        # Per-task seed derivation (D2/T29) — see _derive_task_seeds.
        task_seeds = self._derive_task_seeds(num_simulations)

        ExecutorClass = ProcessPoolExecutor if self.use_processes else ThreadPoolExecutor
        """Win rate sim uses ThreadPoolExecutor (I/O-bound — disk reads dominate); accuracy sim uses ProcessPoolExecutor (CPU-bound — score computation dominates). ThreadPoolExecutor: lower overhead, sufficient for I/O-bound simulation setup; ProcessPoolExecutor: bypasses GIL for CPU-bound parallelism at the cost of pickling overhead and higher process-creation latency."""
        if self.use_processes:
            executor = ProcessPoolExecutor(
                max_workers=self.max_workers,
                initializer=_init_worker_process,
                initargs=(preloaded_week_data,)
            )
            sim_args = [
                (config_dict, sim_id, self.data_folder, self.naive_opponents, task_seeds[sim_id])
                for sim_id in range(num_simulations)
            ]
            future_to_sim_id = {
                executor.submit(_run_simulation_with_weeks_process, args): args[1]
                for args in sim_args
            }
        else:
            executor = ExecutorClass(max_workers=self.max_workers)
            future_to_sim_id = {
                executor.submit(self.run_single_simulation_with_weeks, config_dict, sim_id, preloaded_week_data, task_seeds[sim_id]): sim_id
                for sim_id in range(num_simulations)
            }

        try:
            for future in as_completed(future_to_sim_id):
                sim_id = future_to_sim_id[future]

                try:
                    result = future.result()
                    results.append(result)

                    with self.lock:
                        completed_count += 1
                        if self.progress_callback:
                            self.progress_callback(completed_count, num_simulations)

                        if completed_count % GC_FREQUENCY == 0:
                            gc.collect()
                            self.logger.debug(f"Forced GC after {completed_count} simulations")

                except BrokenProcessPool:
                    self.logger.error("Process pool crashed — stopping simulations")
                    break
                except Exception as e:
                    self.logger.error(f"Simulation {sim_id} failed: {e}")
        except KeyboardInterrupt:
            self.logger.warning("Simulation interrupted by user")
            raise
        finally:
            executor.shutdown(wait=False, cancel_futures=True)

        self.last_completed_count = len(results)
        self.last_dropped_count = num_simulations - len(results)

        if self.last_dropped_count > 0:
            drop_rate = self.last_dropped_count / num_simulations if num_simulations else 0.0
            msg = (
                f"{self.last_dropped_count}/{num_simulations} leagues dropped "
                f"({len(results)}/{num_simulations} completed, rate={drop_rate:.1%})"
            )
            # KDD-2: prepend the elevated label only when an operator has configured a
            # non-zero drop_rate_threshold AND this drop rate exceeds it. At the default
            # threshold (0.0) every drop still logs at ERROR, with the neutral phrasing.
            if self.drop_rate_threshold > 0.0 and drop_rate > self.drop_rate_threshold:
                msg = f"HIGH DROP RATE: {msg}"
            self.logger.error(msg)

        self.logger.debug(
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
        self.logger.debug(
            f"Running {len(config_dicts)} configs with {simulations_per_config} "
            f"simulations each (total: {len(config_dicts) * simulations_per_config})"
        )

        all_results = {}

        for idx, config_dict in enumerate(config_dicts, 1):
            config_name = config_dict.get('config_name', f'config_{idx:04d}')

            self.logger.debug(
                f"[{idx}/{len(config_dicts)}] Running simulations for {config_name}"
            )

            results = self.run_simulations_for_config(config_dict, simulations_per_config)
            all_results[config_name] = results

        self.logger.debug(f"All {len(config_dicts)} configs completed")
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
        self.logger.debug("Running single test simulation")
        return self.run_single_simulation(config_dict, simulation_id=0)


