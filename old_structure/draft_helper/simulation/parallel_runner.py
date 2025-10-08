"""
Parallel processing runner for draft simulations.

Handles concurrent execution of multiple simulations to improve performance.
"""

import concurrent.futures
import logging
import time
from typing import List, Dict, Any, Callable, Optional
import multiprocessing
import threading
from dataclasses import dataclass
import sys
import os

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# Import from local simulation config
# Add current directory to path for local imports
import sys
import os
sys.path.append(os.path.dirname(__file__))

from shared_files.configs.simulation_config import SIMULATIONS_PER_CONFIG, PRELIMINARY_SIMULATIONS_PER_CONFIG, MAX_PARALLEL_THREADS, SIMULATION_LOG_LEVEL

# Configure logging level for all threads
logging.getLogger().setLevel(getattr(logging, SIMULATION_LOG_LEVEL, logging.WARNING))
# Specifically suppress noisy loggers
logging.getLogger('shared_files.positional_ranking_calculator').setLevel(logging.WARNING)

@dataclass
class SimulationTask:
    """Represents a single simulation task"""
    config_params: Dict[str, Any]
    simulation_id: int
    is_preliminary: bool

@dataclass
class SimulationProgress:
    """Tracks simulation progress"""
    total_configs: int
    completed_configs: int
    total_simulations: int
    completed_simulations: int
    start_time: float
    estimated_completion_time: Optional[float] = None

class ParallelSimulationRunner:
    """Manages parallel execution of draft simulations"""

    def __init__(self, max_workers: Optional[int] = None):
        # Use provided value, config setting, or auto-detect (in that order)
        if max_workers is not None:
            self.max_workers = max_workers
        elif MAX_PARALLEL_THREADS is not None:
            self.max_workers = MAX_PARALLEL_THREADS
        else:
            self.max_workers = min(6, multiprocessing.cpu_count())
        self.progress = SimulationProgress(0, 0, 0, 0, 0.0)
        self.results_lock = threading.Lock()
        self.progress_lock = threading.Lock()

    def run_preliminary_simulations(self, configs: List[Dict[str, Any]],
                                  simulation_function: Callable) -> Dict[str, List[Dict[str, Any]]]:
        """Run preliminary simulations for all configurations"""

        print(f"Starting preliminary testing with {len(configs)} configurations...")
        print(f"Running {PRELIMINARY_SIMULATIONS_PER_CONFIG} simulations per configuration")
        print(f"Using {self.max_workers} parallel workers")

        # Initialize progress tracking
        total_simulations = len(configs) * PRELIMINARY_SIMULATIONS_PER_CONFIG
        self.progress = SimulationProgress(
            total_configs=len(configs),
            completed_configs=0,
            total_simulations=total_simulations,
            completed_simulations=0,
            start_time=time.time()
        )

        # Create simulation tasks
        tasks = []
        for config_idx, config in enumerate(configs):
            for sim_idx in range(PRELIMINARY_SIMULATIONS_PER_CONFIG):
                task = SimulationTask(
                    config_params=config,
                    simulation_id=config_idx * PRELIMINARY_SIMULATIONS_PER_CONFIG + sim_idx,
                    is_preliminary=True
                )
                tasks.append(task)

        # Run simulations in parallel
        results_by_config = {}

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_task = {
                executor.submit(self._run_single_simulation, task, simulation_function): task
                for task in tasks
            }

            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_task):
                task = future_to_task[future]

                try:
                    result = future.result()

                    # Group results by configuration
                    config_key = self._config_to_key(task.config_params)
                    if config_key not in results_by_config:
                        results_by_config[config_key] = {
                            'config': task.config_params,
                            'results': []
                        }
                    results_by_config[config_key]['results'].append(result)

                    # Update progress
                    self._update_progress()

                except Exception as e:
                    print(f"Simulation failed for config {task.simulation_id}: {e}")

        self._print_completion_summary("Preliminary")
        return results_by_config

    def run_full_simulations(self, configs: List[Dict[str, Any]],
                           simulation_function: Callable) -> Dict[str, List[Dict[str, Any]]]:
        """Run full simulations for top configurations"""

        print(f"Starting full testing with {len(configs)} top configurations...")
        print(f"Running {SIMULATIONS_PER_CONFIG} simulations per configuration")
        print(f"Using {self.max_workers} parallel workers")

        # Initialize progress tracking
        total_simulations = len(configs) * SIMULATIONS_PER_CONFIG
        self.progress = SimulationProgress(
            total_configs=len(configs),
            completed_configs=0,
            total_simulations=total_simulations,
            completed_simulations=0,
            start_time=time.time()
        )

        # Create simulation tasks
        tasks = []
        for config_idx, config in enumerate(configs):
            for sim_idx in range(SIMULATIONS_PER_CONFIG):
                task = SimulationTask(
                    config_params=config,
                    simulation_id=config_idx * SIMULATIONS_PER_CONFIG + sim_idx,
                    is_preliminary=False
                )
                tasks.append(task)

        # Run simulations in parallel
        results_by_config = {}

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_task = {
                executor.submit(self._run_single_simulation, task, simulation_function): task
                for task in tasks
            }

            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_task):
                task = future_to_task[future]

                try:
                    result = future.result()

                    # Group results by configuration
                    config_key = self._config_to_key(task.config_params)
                    if config_key not in results_by_config:
                        results_by_config[config_key] = {
                            'config': task.config_params,
                            'results': []
                        }
                    results_by_config[config_key]['results'].append(result)

                    # Update progress
                    self._update_progress()

                except Exception as e:
                    print(f"Simulation failed for config {task.simulation_id}: {e}")

        self._print_completion_summary("Full")
        return results_by_config

    def _run_single_simulation(self, task: SimulationTask, simulation_function: Callable) -> Dict[str, Any]:
        """Run a single simulation task"""

        try:
            # Call the simulation function with the config parameters
            result = simulation_function(task.config_params)
            return result

        except Exception as e:
            print(f"Error in simulation {task.simulation_id}: {e}", flush=True)
            raise

    def _update_progress(self) -> None:
        """Update progress tracking and print status"""

        with self.progress_lock:
            self.progress.completed_simulations += 1

            # Calculate progress percentage
            progress_pct = (self.progress.completed_simulations / self.progress.total_simulations) * 100

            # Estimate completion time
            elapsed_time = time.time() - self.progress.start_time
            if self.progress.completed_simulations > 0:
                avg_time_per_sim = elapsed_time / self.progress.completed_simulations
                remaining_sims = self.progress.total_simulations - self.progress.completed_simulations
                estimated_remaining_time = remaining_sims * avg_time_per_sim
                self.progress.estimated_completion_time = time.time() + estimated_remaining_time

            # Print progress more frequently at the start (first 10 sims), then every 5% or every 50 simulations
            # This helps confirm simulations are running early on
            should_print = (
                self.progress.completed_simulations <= 10 or  # First 10 simulations
                self.progress.completed_simulations % 50 == 0 or  # Every 50 sims
                self.progress.completed_simulations % max(1, self.progress.total_simulations // 20) == 0  # Every 5%
            )

            if should_print:
                elapsed_minutes = elapsed_time / 60
                if self.progress.estimated_completion_time:
                    remaining_minutes = (self.progress.estimated_completion_time - time.time()) / 60
                    print(f"Progress: {self.progress.completed_simulations}/{self.progress.total_simulations} "
                          f"({progress_pct:.1f}%) - {elapsed_minutes:.1f}m elapsed, ~{remaining_minutes:.1f}m remaining", flush=True)
                else:
                    print(f"Progress: {self.progress.completed_simulations}/{self.progress.total_simulations} "
                          f"({progress_pct:.1f}%) - {elapsed_minutes:.1f}m elapsed", flush=True)

    def _config_to_key(self, config: Dict[str, Any]) -> str:
        """Convert configuration to a unique string key"""

        # Create a sorted string representation of the config
        key_parts = []
        for param_name in sorted(config.keys()):
            if param_name != 'DRAFT_ORDER':  # Skip complex object
                value = config[param_name]
                key_parts.append(f"{param_name}={value}")

        return "|".join(key_parts)

    def _print_completion_summary(self, phase: str) -> None:
        """Print completion summary"""

        total_time = time.time() - self.progress.start_time
        total_minutes = total_time / 60

        print(f"\n{phase} simulation phase completed!")
        print(f"Total time: {total_minutes:.1f} minutes")
        print(f"Total simulations: {self.progress.completed_simulations}")
        print(f"Average time per simulation: {total_time / self.progress.completed_simulations:.2f} seconds")
        print(f"Simulations per minute: {self.progress.completed_simulations / total_minutes:.1f}")
        print()

class BatchProcessor:
    """Processes simulation results in batches to manage memory usage"""

    def __init__(self, batch_size: int = 100):
        self.batch_size = batch_size

    def process_results_in_batches(self, all_results: Dict[str, List[Dict[str, Any]]],
                                 processing_function: Callable) -> List[Any]:
        """Process simulation results in batches to manage memory"""

        processed_results = []
        config_keys = list(all_results.keys())

        # Process configurations in batches
        for i in range(0, len(config_keys), self.batch_size):
            batch_keys = config_keys[i:i + self.batch_size]
            batch_results = {key: all_results[key] for key in batch_keys}

            print(f"Processing batch {i // self.batch_size + 1} "
                  f"({len(batch_keys)} configurations)...")

            batch_processed = processing_function(batch_results)
            processed_results.extend(batch_processed)

        return processed_results