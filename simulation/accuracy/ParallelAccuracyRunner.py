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

    # Extract metadata for logging (if available)
    metadata = config_dict.get('_eval_metadata', {})
    param_name = metadata.get('param_name', 'unknown')
    param_value = metadata.get('param_value', 'unknown')
    config_horizon = metadata.get('horizon', 'unknown')

    # Evaluate all 4 weekly horizons
    for week_key, week_range in WEEK_RANGES.items():
        results[week_key] = _evaluate_config_weekly_worker(
            calculator, config_dict, data_folder, available_seasons, week_range, week_key,
            param_name, param_value, config_horizon
        )

    # Log summary of all horizons for this config
    logger = calculator.logger
    config_label = f"{param_name}={param_value} [{config_horizon}]"
    logger.info(f"━━━ Config Complete: {config_label} ━━━")
    logger.info(f"  week_1_5:   MAE={results['week_1_5'].mae:.4f} (players={results['week_1_5'].player_count})")
    logger.info(f"  week_6_9:   MAE={results['week_6_9'].mae:.4f} (players={results['week_6_9'].player_count})")
    logger.info(f"  week_10_13: MAE={results['week_10_13'].mae:.4f} (players={results['week_10_13'].player_count})")
    logger.info(f"  week_14_17: MAE={results['week_14_17'].mae:.4f} (players={results['week_14_17'].player_count})")

    return (config_dict, results)


def _evaluate_config_weekly_worker(
    calculator: AccuracyCalculator,
    config_dict: dict,
    data_folder: Path,
    available_seasons: List[Path],
    week_range: Tuple[int, int],
    horizon: str,
    param_name: str,
    param_value: Any,
    config_horizon: str
) -> AccuracyResult:
    """
    Worker function to evaluate weekly configuration.

    Replicates AccuracySimulationManager._evaluate_config_weekly() logic for parallel execution.
    """
    start_week, end_week = week_range
    season_results = []

    for season_path in available_seasons:
        week_projections = {}
        week_actuals = {}
        player_data_by_week = {}  # For ranking metrics

        for week_num in range(start_week, end_week + 1):
            projected_path, actual_path = _load_season_data(season_path, week_num)
            if not projected_path or not actual_path:
                # Skip if either folder missing
                continue

            # Create TWO player managers:
            # 1. projected_mgr (from week_N folder) for projections
            # 2. actual_mgr (from week_N+1 folder) for actuals
            projected_mgr = _create_player_manager(config_dict, projected_path, season_path, week_num)
            actual_mgr = _create_player_manager(config_dict, actual_path, season_path, week_num)

            try:
                projections = {}
                actuals = {}
                player_data = []  # Player metadata for ranking metrics

                # Calculate and set max weekly projection for this week's normalization
                # This is required before scoring with use_weekly_projection=True
                max_weekly = projected_mgr.calculate_max_weekly_projection(week_num)
                projected_mgr.scoring_calculator.max_weekly_projection = max_weekly

                # Get projections from week_N folder (projected_mgr)
                for player in projected_mgr.players:
                    # Get scored player with projected points
                    # Use same flags as StarterHelperModeManager with
                    # use_weekly_projection=True for weekly projections
                    scored = projected_mgr.score_player(
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

                # Get actuals from week_N+1 folder (actual_mgr)
                # week_N+1 has actual_points[N-1] populated (week N complete)
                for player in actual_mgr.players:
                    # Get actual points for this specific week (from actual_points array)
                    # Array index: week 1 = index 0, week N = index N-1
                    if 1 <= week_num <= 17 and len(player.actual_points) >= week_num:
                        actual = player.actual_points[week_num - 1]
                        if actual is not None and actual > 0:
                            actuals[player.id] = actual

                            # Match with projection by player ID
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
                _cleanup_player_manager(projected_mgr)
                _cleanup_player_manager(actual_mgr)

        # Calculate MAE for this season's week range
        result = calculator.calculate_weekly_mae(
            week_projections, week_actuals, week_range
        )

        # Calculate ranking metrics for this season
        overall_metrics, by_position = calculator.calculate_ranking_metrics_for_season(
            player_data_by_week
        )
        result.overall_metrics = overall_metrics
        result.by_position = by_position

        season_results.append((season_path.name, result))

    # Aggregate across seasons with config context
    config_label = f"{param_name}={param_value} [{config_horizon}]"
    return calculator.aggregate_season_results(season_results, horizon, config_label)


def _load_season_data(season_path: Path, week_num: int) -> Tuple[Path, Path]:
    """Load data paths for a specific week in a season.

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
    logger = get_logger()

    # Week N folder for projections
    projected_folder = season_path / "weeks" / f"week_{week_num:02d}"

    # Week N+1 folder for actuals
    # For week 1: use week_02, for week 17: use week_18
    actual_week_num = week_num + 1
    actual_folder = season_path / "weeks" / f"week_{actual_week_num:02d}"

    # Both folders must exist
    if not projected_folder.exists():
        logger.warning(f"Projected folder not found: {projected_folder}")
        return None, None

    if not actual_folder.exists():
        logger.warning(
            f"Actual folder not found: {actual_folder} "
            f"(needed for week {week_num} actuals)"
        )
        return None, None

    return projected_folder, actual_folder


def _create_player_manager(config_dict: dict, week_data_path: Path, season_path: Path, week_num: int) -> PlayerManager:
    """
    Create PlayerManager with temporary config file.

    Args:
        config_dict: Configuration dictionary
        week_data_path: Path to week folder containing position JSON files
        season_path: Path to season folder containing season_schedule.csv, team_data/
        week_num: NFL week number being simulated (1-17)
    """
    logger = get_logger()

    # Create temp directory
    temp_dir = Path(tempfile.mkdtemp(prefix="accuracy_sim_"))

    # Create player_data subfolder for JSON files
    player_data_dir = temp_dir / "player_data"
    player_data_dir.mkdir(exist_ok=True)

    # Copy 6 position JSON files from week folder to player_data/
    position_files = ['qb_data.json', 'rb_data.json', 'wr_data.json',
                      'te_data.json', 'k_data.json', 'dst_data.json']
    for filename in position_files:
        source_file = week_data_path / filename
        if source_file.exists():
            shutil.copy(source_file, player_data_dir / filename)
        else:
            logger.warning(f"Missing position file: {filename} in {week_data_path}")

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

    # FIX: Update CURRENT_NFL_WEEK to match the week being simulated
    # This ensures get_weekly_projections() returns projected_points (not actual_points)
    # for the week we're analyzing
    import copy
    config_dict_copy = copy.deepcopy(config_dict)
    config_dict_copy['parameters']['CURRENT_NFL_WEEK'] = week_num

    # Write config
    config_path = temp_dir / "league_config.json"
    with open(config_path, 'w') as f:
        json.dump(config_dict_copy, f, indent=2)

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
            try:
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

            except KeyboardInterrupt:
                self.logger.warning("\nKeyboardInterrupt received - cancelling all workers...")
                # Cancel all pending futures
                for future in future_to_config:
                    future.cancel()
                # Shutdown executor immediately
                executor.shutdown(wait=False, cancel_futures=True)
                self.logger.info("All workers cancelled")
                raise

        # Sort results to match input order (futures complete in arbitrary order)
        # Use JSON serialization for proper dict keys
        import json
        config_to_result = {json.dumps(cfg, sort_keys=True): res for cfg, res in results}
        ordered_results = [(cfg, config_to_result[json.dumps(cfg, sort_keys=True)]) for cfg in configs]

        return ordered_results
