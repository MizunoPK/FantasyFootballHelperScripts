"""
Parallel processing support for accuracy simulation using ProcessPoolExecutor.

This module provides parallel evaluation of configs across multiple horizons
to speed up tournament optimization. Each config is evaluated across all 5
horizons (ROS, week 1-5, 6-9, 10-13, 14-17) to calculate MAE.

Author: Kai Mizuno
"""

import logging
from pathlib import Path
from typing import Dict, List, Any, Tuple
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed

# Add parent directory to path for imports
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from simulation.accuracy.AccuracyCalculator import AccuracyCalculator, AccuracyResult
from utils.LoggingManager import get_logger


def _evaluate_config_tournament_process(
    config_dict: Dict[str, Any],
    data_folder: Path,
    available_seasons: List[str]
) -> Tuple[Dict[str, Any], Dict[str, AccuracyResult]]:
    """
    Module-level function to evaluate single config across all 5 horizons.

    Must be module-level for ProcessPoolExecutor pickling.

    Args:
        config_dict: Configuration to evaluate
        data_folder: Path to simulation data folder (sim_data/)
        available_seasons: List of season folders to use

    Returns:
        Tuple of (config_dict, results_dict) where results_dict maps horizon to AccuracyResult.
        Uses underscore keys to match AccuracyResultsManager expectations:
        {'ros': result_ros, 'week_1_5': result_1_5, 'week_6_9': result_6_9, 'week_10_13': result_10_13, 'week_14_17': result_14_17}
    """
    # Create calculator (stateless except logger - safe for parallel)
    calculator = AccuracyCalculator(data_folder, available_seasons)

    # Horizon key mapping: dash format (ConfigGenerator) -> underscore format (AccuracyResultsManager)
    horizon_key_map = {
        'ros': 'ros',
        '1-5': 'week_1_5',
        '6-9': 'week_6_9',
        '10-13': 'week_10_13',
        '14-17': 'week_14_17'
    }

    results = {}

    # Evaluate ROS horizon
    ros_result = calculator.calculate_ros_mae(data_folder, config_dict)
    results['ros'] = ros_result

    # Evaluate all 4 weekly horizons
    for week_horizon_dash in ['1-5', '6-9', '10-13', '14-17']:
        result = calculator.calculate_weekly_mae(data_folder, config_dict, week_horizon_dash)
        week_horizon_underscore = horizon_key_map[week_horizon_dash]
        results[week_horizon_underscore] = result

    return (config_dict, results)


class ParallelAccuracyRunner:
    """
    Manages parallel evaluation of accuracy configs using ProcessPoolExecutor.

    Evaluates multiple configs in parallel across all 5 horizons to speed up
    tournament optimization. Each config gets 5 MAE calculations (one per horizon).
    """

    def __init__(
        self,
        data_folder: Path,
        available_seasons: List[str],
        max_workers: int = 8,
        use_processes: bool = True
    ):
        """
        Initialize parallel runner.

        Args:
            data_folder: Path to simulation data folder
            available_seasons: List of season folders to use
            max_workers: Number of parallel workers (default: 8)
            use_processes: Use ProcessPoolExecutor (True) or ThreadPoolExecutor (False)
        """
        self.data_folder = data_folder
        self.available_seasons = available_seasons
        self.max_workers = max_workers
        self.use_processes = use_processes
        self.logger = get_logger()

    def evaluate_configs_parallel(
        self,
        configs: List[Dict[str, Any]],
        progress_callback = None
    ) -> List[Tuple[Dict[str, Any], Dict[str, AccuracyResult]]]:
        """
        Evaluate multiple configs in parallel across all 5 horizons.

        Args:
            configs: List of config dicts to evaluate
            progress_callback: Optional callback(completed_count) to track progress

        Returns:
            List of (config_dict, results_dict) tuples in same order as input
        """
        if len(configs) == 0:
            return []

        # Choose executor type
        executor_class = ProcessPoolExecutor if self.use_processes else ThreadPoolExecutor
        executor_name = "ProcessPoolExecutor" if self.use_processes else "ThreadPoolExecutor"

        self.logger.info(f"Starting parallel evaluation: {len(configs)} configs × 5 horizons = {len(configs) * 5} total evaluations")
        self.logger.info(f"Using {executor_name} with {self.max_workers} workers")

        results = []
        completed = 0

        with executor_class(max_workers=self.max_workers) as executor:
            # Submit all configs
            future_to_config = {
                executor.submit(
                    _evaluate_config_tournament_process,
                    config,
                    self.data_folder,
                    self.available_seasons
                ): config
                for config in configs
            }

            # Collect results as they complete
            for future in as_completed(future_to_config):
                config = future_to_config[future]
                try:
                    result = future.result()
                    results.append(result)
                    completed += 1

                    # Progress callback
                    if progress_callback is not None:
                        progress_callback(completed)

                except Exception as e:
                    self.logger.error(f"Config evaluation failed: {e}", exc_info=True)
                    raise  # Fail-fast

        # Sort results to match input order (futures complete in arbitrary order)
        config_to_result = {str(cfg): res for cfg, res in results}
        ordered_results = [(cfg, config_to_result[str(cfg)][1]) for cfg in configs]

        return ordered_results
