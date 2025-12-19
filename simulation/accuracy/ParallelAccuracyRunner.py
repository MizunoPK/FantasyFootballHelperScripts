"""
Parallel processing support for accuracy simulation using ProcessPoolExecutor.

This module provides parallel evaluation of configs across multiple horizons
to speed up tournament optimization. Each config is evaluated across all 5
horizons (ROS, week 1-5, 6-9, 10-13, 14-17) to calculate MAE.

Author: Kai Mizuno
"""

import json
import logging
import shutil
import tempfile
from pathlib import Path
from typing import Dict, List, Any, Tuple
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed

# Add parent directory to path for imports
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from simulation.accuracy.AccuracyCalculator import AccuracyCalculator, AccuracyResult
from utils.LoggingManager import get_logger
from league_helper.util.ConfigManager import ConfigManager
from league_helper.util.PlayerManager import PlayerManager
from league_helper.util.TeamDataManager import TeamDataManager
from league_helper.util.SeasonScheduleManager import SeasonScheduleManager


def _evaluate_config_tournament_process(
    config_dict: Dict[str, Any],
    data_folder: Path,
    available_seasons: List[Path]
) -> Tuple[Dict[str, Any], Dict[str, AccuracyResult]]:
    """
    Module-level function to evaluate single config across all 5 horizons.

    Must be module-level for ProcessPoolExecutor pickling.

    Args:
        config_dict: Configuration to evaluate
        data_folder: Path to simulation data folder (sim_data/)
        available_seasons: List of season folder Paths to use

    Returns:
        Tuple of (config_dict, results_dict) where results_dict maps horizon to AccuracyResult.
        Uses underscore keys to match AccuracyResultsManager expectations:
        {'ros': result_ros, 'week_1_5': result_1_5, 'week_6_9': result_6_9, 'week_10_13': result_10_13, 'week_14_17': result_14_17}
    """
    # Create calculator instance
    calculator = AccuracyCalculator()

    # Week ranges for horizons (tuple format for compatibility with evaluation logic)
    WEEK_RANGES = {
        'week_1_5': (1, 5),
        'week_6_9': (6, 9),
        'week_10_13': (10, 13),
        'week_14_17': (14, 17)
    }

    results = {}

    # Evaluate ROS horizon
    results['ros'] = _evaluate_config_ros_worker(calculator, config_dict, data_folder, available_seasons)

    # Evaluate all 4 weekly horizons
    for week_key, week_range in WEEK_RANGES.items():
        results[week_key] = _evaluate_config_weekly_worker(calculator, config_dict, data_folder, available_seasons, week_range)

    return (config_dict, results)


def _evaluate_config_ros_worker(
    calculator: AccuracyCalculator,
    config_dict: dict,
    data_folder: Path,
    available_seasons: List[Path]
) -> AccuracyResult:
    """
    Worker function to evaluate ROS configuration.

    Replicates AccuracySimulationManager._evaluate_config_ros() logic for parallel execution.
    """
    season_results = []

    for season_path in available_seasons:
        # Load week 1 data
        projected_path, actual_path = _load_season_data(season_path, 1)
        if not projected_path:
            continue

        # Create player manager with this config
        player_mgr = _create_player_manager(config_dict, projected_path.parent, season_path)

        try:
            # Calculate projections for all players
            projections = {}
            actuals = {}

            for player in player_mgr.get_all_players():
                # Week 1 projection
                projected = player.total_score
                if projected > 0:
                    projections[player.id] = projected

                # Calculate actual season total
                actual_total = 0.0
                has_any_week = False

                for week_num in range(1, 18):
                    week_actual = player.get_points_for_week(week_num)
                    if week_actual is not None and week_actual > 0:
                        actual_total += week_actual
                        has_any_week = True

                if has_any_week and actual_total > 0:
                    actuals[player.id] = actual_total

            # Calculate MAE for this season
            result = calculator.calculate_mae(projections, actuals)
            season_results.append((season_path.name, result))

        finally:
            _cleanup_player_manager(player_mgr)

    # Aggregate across seasons
    return calculator.aggregate_season_results(season_results)


def _evaluate_config_weekly_worker(
    calculator: AccuracyCalculator,
    config_dict: dict,
    data_folder: Path,
    available_seasons: List[Path],
    week_range: Tuple[int, int]
) -> AccuracyResult:
    """
    Worker function to evaluate weekly configuration.

    Replicates AccuracySimulationManager._evaluate_config_weekly() logic for parallel execution.
    """
    season_results = []
    start_week, end_week = week_range

    for season_path in available_seasons:
        # Load data for start week
        projected_path, actual_path = _load_season_data(season_path, start_week)
        if not projected_path:
            continue

        # Create player manager
        player_mgr = _create_player_manager(config_dict, projected_path.parent, season_path)

        try:
            # Calculate week-range projections vs actuals
            week_projections = {}
            week_actuals = {}

            for player in player_mgr.get_all_players():
                # Use start week projection
                projected = player.total_score
                if projected > 0:
                    week_projections[player.id] = projected

                # Sum actuals across week range
                actual_total = 0.0
                has_any_week = False

                for week_num in range(start_week, end_week + 1):
                    week_actual = player.get_points_for_week(week_num)
                    if week_actual is not None and week_actual > 0:
                        actual_total += week_actual
                        has_any_week = True

                if has_any_week and actual_total > 0:
                    week_actuals[player.id] = actual_total

            # Calculate MAE for this season's week range
            result = calculator.calculate_mae(week_projections, week_actuals)
            season_results.append((season_path.name, result))

        finally:
            _cleanup_player_manager(player_mgr)

    # Aggregate across seasons
    return calculator.aggregate_season_results(season_results)


def _load_season_data(season_path: Path, week_num: int) -> Tuple[Path, Path]:
    """Load projected and actual data paths for a given week."""
    projected_path = season_path / f"players_week{week_num}.csv"
    actual_path = season_path / "players_actual.csv"

    if not projected_path.exists() or not actual_path.exists():
        return None, None

    return projected_path, actual_path


def _create_player_manager(config_dict: dict, data_dir: Path, season_path: Path) -> PlayerManager:
    """Create PlayerManager with temporary config file."""
    # Create temp directory
    temp_dir = Path(tempfile.mkdtemp(prefix="accuracy_sim_"))

    # Copy required files
    players_csv = data_dir / "players_week1.csv"
    if players_csv.exists():
        shutil.copy(players_csv, temp_dir / "players.csv")

    actual_csv = data_dir / "players_actual.csv"
    if actual_csv.exists():
        shutil.copy(actual_csv, temp_dir / "players_actual.csv")

    game_data = season_path / "game_data.csv"
    if game_data.exists():
        shutil.copy(game_data, temp_dir / "game_data.csv")

    # Copy team_data folder
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


def _cleanup_player_manager(player_mgr: PlayerManager) -> None:
    """Clean up temporary files from player manager."""
    if hasattr(player_mgr, '_temp_dir') and player_mgr._temp_dir.exists():
        shutil.rmtree(player_mgr._temp_dir)


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
        # Use JSON serialization for proper dict keys
        import json
        config_to_result = {json.dumps(cfg, sort_keys=True): res for cfg, res in results}
        ordered_results = [(cfg, config_to_result[json.dumps(cfg, sort_keys=True)]) for cfg in configs]

        return ordered_results
