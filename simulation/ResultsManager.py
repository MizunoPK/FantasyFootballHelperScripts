"""
Results Manager

Aggregates and manages performance results across all configuration tests.
Tracks results for all 46,656 configurations, identifies the best performing
configuration, and saves optimal configs to disk.

Author: Kai Mizuno
"""

import json
from pathlib import Path
from typing import Dict, Optional, List, Tuple
from datetime import datetime

import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.LoggingManager import get_logger

sys.path.append(str(Path(__file__).parent))
from ConfigPerformance import ConfigPerformance, WEEK_RANGES
from config_cleanup import cleanup_old_optimal_folders


class ResultsManager:
    """
    Manages performance results for all configuration tests.

    Tracks ConfigPerformance objects for each configuration, identifies
    the best performing config, and saves results to disk.

    Attributes:
        results (Dict[str, ConfigPerformance]): {config_id: performance}
        logger: Logger instance
    """

    def __init__(self) -> None:
        """Initialize ResultsManager with empty results."""
        self.results: Dict[str, ConfigPerformance] = {}
        self.logger = get_logger()
        self.logger.info("ResultsManager initialized")

    def register_config(self, config_id: str, config_dict: dict) -> None:
        """
        Register a new configuration for tracking.

        Args:
            config_id (str): Unique identifier for this config
            config_dict (dict): Full configuration dictionary

        Example:
            >>> mgr = ResultsManager()
            >>> mgr.register_config("config_0001", config_dict)
        """
        if config_id in self.results:
            self.logger.warning(f"Config {config_id} already registered, overwriting")

        self.results[config_id] = ConfigPerformance(config_id, config_dict)
        self.logger.debug(f"Registered config {config_id}")

    def record_result(self, config_id: str, wins: int, losses: int, points: float) -> None:
        """
        Record results from a single league simulation.

        Args:
            config_id (str): Configuration identifier
            wins (int): Number of wins
            losses (int): Number of losses
            points (float): Total points scored

        Raises:
            KeyError: If config_id not registered

        Example:
            >>> mgr.record_result("config_0001", 10, 7, 1404.62)
        """
        if config_id not in self.results:
            raise KeyError(f"Config {config_id} not registered. Call register_config() first.")

        self.results[config_id].add_league_result(wins, losses, points)
        self.logger.debug(f"Recorded result for {config_id}: {wins}W-{losses}L, {points:.2f} pts")

    def record_week_results(
        self,
        config_id: str,
        week_results: List[Tuple[int, bool, float]]
    ) -> None:
        """
        Record per-week results from a single league simulation.

        This enables per-week-range performance tracking for week-by-week
        config optimization.

        Args:
            config_id (str): Configuration identifier
            week_results: List of (week, won, points) tuples for each week

        Raises:
            KeyError: If config_id not registered

        Example:
            >>> week_data = [
            ...     (1, True, 125.5),   # Week 1: Won
            ...     (2, False, 98.3),   # Week 2: Lost
            ...     # ... weeks 3-16
            ... ]
            >>> mgr.record_week_results("config_0001", week_data)
        """
        if config_id not in self.results:
            raise KeyError(f"Config {config_id} not registered. Call register_config() first.")

        self.results[config_id].add_week_results(week_results)

        # Log summary
        wins = sum(1 for _, won, _ in week_results if won)
        losses = len(week_results) - wins
        points = sum(pts for _, _, pts in week_results)
        self.logger.debug(
            f"Recorded week results for {config_id}: {wins}W-{losses}L, {points:.2f} pts"
        )

    def get_best_config_for_range(self, week_range: str) -> Optional[ConfigPerformance]:
        """
        Get the best performing configuration for a specific week range.

        Args:
            week_range (str): Week range string ("1-5", "6-9", "10-13", or "14-17")

        Returns:
            Optional[ConfigPerformance]: Best config for that range, or None

        Example:
            >>> best_early = mgr.get_best_config_for_range("1-5")
            >>> print(f"Best for weeks 1-5: {best_early.config_id}")
        """
        if not self.results:
            self.logger.warning("No results available to compare")
            return None

        if week_range not in WEEK_RANGES:
            raise ValueError(f"Invalid week range: {week_range}. Must be one of {WEEK_RANGES}")

        best_config = None
        best_win_rate = -1.0

        for config_perf in self.results.values():
            win_rate = config_perf.get_win_rate_for_range(week_range)
            if win_rate > best_win_rate:
                best_win_rate = win_rate
                best_config = config_perf

        if best_config:
            self.logger.info(
                f"Best config for {week_range}: {best_config.config_id} "
                f"(win_rate={best_win_rate:.4f})"
            )

        return best_config

    def get_best_configs_per_range(self) -> Dict[str, Optional[ConfigPerformance]]:
        """
        Get the best performing configuration for each week range.

        Returns:
            Dict[str, Optional[ConfigPerformance]]: {week_range: best_config}

        Example:
            >>> best_per_range = mgr.get_best_configs_per_range()
            >>> for range_name, config in best_per_range.items():
            ...     print(f"{range_name}: {config.config_id}")
        """
        return {
            week_range: self.get_best_config_for_range(week_range)
            for week_range in WEEK_RANGES
        }

    def get_best_config(self) -> Optional[ConfigPerformance]:
        """
        Get the best performing configuration.

        Comparison:
        1. Highest win rate
        2. Highest average points per league (tiebreaker)

        Returns:
            Optional[ConfigPerformance]: Best config, or None if no results

        Example:
            >>> best = mgr.get_best_config()
            >>> print(f"Best config: {best.config_id}, win rate: {best.get_win_rate():.1%}")
        """
        if not self.results:
            self.logger.warning("No results available to compare")
            return None

        best_config = None
        for config_perf in self.results.values():
            if best_config is None:
                best_config = config_perf
            elif config_perf.compare_to(best_config) > 0:
                best_config = config_perf

        self.logger.info(
            f"Best config: {best_config.config_id} "
            f"(win_rate={best_config.get_win_rate():.4f}, "
            f"avg_pts={best_config.get_avg_points_per_league():.2f})"
        )
        return best_config

    def get_top_n_configs(self, n: int = 10) -> List[ConfigPerformance]:
        """
        Get top N performing configurations.

        Args:
            n (int): Number of top configs to return (default 10)

        Returns:
            List[ConfigPerformance]: Top N configs, sorted best to worst

        Example:
            >>> top_10 = mgr.get_top_n_configs(10)
            >>> for i, config in enumerate(top_10, 1):
            ...     print(f"{i}. {config}")
        """
        if not self.results:
            return []

        # Sort by win rate (descending), then by avg points (descending)
        sorted_configs = sorted(
            self.results.values(),
            key=lambda c: (c.get_win_rate(), c.get_avg_points_per_league()),
            reverse=True
        )

        return sorted_configs[:n]

    # Parameters that belong in base config (not week-specific)
    BASE_CONFIG_PARAMS = [
        'CURRENT_NFL_WEEK',
        'NFL_SEASON',
        'NFL_SCORING_FORMAT',
        'SAME_POS_BYE_WEIGHT',
        'DIFF_POS_BYE_WEIGHT',
        'INJURY_PENALTIES',
        'DRAFT_ORDER_BONUSES',
        'DRAFT_ORDER_FILE',
        'DRAFT_ORDER',
        'MAX_POSITIONS',
        'FLEX_ELIGIBLE_POSITIONS',
        'ADP_SCORING'
    ]

    # Parameters that belong in week-specific configs
    WEEK_SPECIFIC_PARAMS = [
        'NORMALIZATION_MAX_SCALE',
        'PLAYER_RATING_SCORING',
        'TEAM_QUALITY_SCORING',
        'PERFORMANCE_SCORING',
        'MATCHUP_SCORING',
        'SCHEDULE_SCORING',
        'TEMPERATURE_SCORING',
        'WIND_SCORING',
        'LOCATION_MODIFIERS'
    ]

    def _extract_base_params(self, config_dict: dict) -> dict:
        """
        Extract base (non-week-specific) parameters from a config.

        Args:
            config_dict (dict): Full configuration dictionary

        Returns:
            dict: Config dict with only base parameters
        """
        params = config_dict.get('parameters', {})
        base_params = {
            key: params[key]
            for key in self.BASE_CONFIG_PARAMS
            if key in params
        }

        return {
            'config_name': config_dict.get('config_name', 'Optimal Base Config'),
            'description': 'Base configuration (non-week-specific parameters)',
            'parameters': base_params
        }

    def _extract_week_params(self, config_dict: dict) -> dict:
        """
        Extract week-specific parameters from a config.

        Args:
            config_dict (dict): Full configuration dictionary

        Returns:
            dict: Config dict with only week-specific parameters
        """
        params = config_dict.get('parameters', {})
        week_params = {
            key: params[key]
            for key in self.WEEK_SPECIFIC_PARAMS
            if key in params
        }

        return {
            'config_name': config_dict.get('config_name', 'Week-Specific Config'),
            'description': 'Week-specific scoring parameters',
            'parameters': week_params
        }

    def save_optimal_config(self, output_dir: Path) -> Path:
        """
        Save the best configuration to a JSON file with timestamp.

        This is the legacy method that saves a single config file.
        For week-by-week configs, use save_optimal_configs_folder().

        Args:
            output_dir (Path): Directory to save config to

        Returns:
            Path: Path to saved config file

        Raises:
            ValueError: If no results available

        Example:
            >>> output_path = mgr.save_optimal_config(Path("simulation/optimal_configs"))
            >>> print(f"Saved optimal config to {output_path}")
        """
        best_config = self.get_best_config()
        if best_config is None:
            raise ValueError("No results available to save")

        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"optimal_{timestamp}.json"
        output_path = output_dir / filename

        # Add performance metadata to config
        config_to_save = best_config.config_dict.copy()
        config_to_save['performance_metrics'] = {
            'config_id': best_config.config_id,
            'win_rate': best_config.get_win_rate(),
            'total_wins': best_config.total_wins,
            'total_losses': best_config.total_losses,
            'total_games': best_config.total_games,
            'avg_points_per_league': best_config.get_avg_points_per_league(),
            'total_points': best_config.total_points,
            'num_simulations': best_config.num_simulations,
            'timestamp': timestamp
        }

        # Save to file
        with open(output_path, 'w') as f:
            json.dump(config_to_save, f, indent=2)

        self.logger.info(f"Saved optimal config to {output_path}")
        return output_path

    def save_optimal_configs_folder(self, output_dir: Path) -> Path:
        """
        Save optimal configs as a folder with 4 config files.

        Creates a folder containing:
        - league_config.json: Base config from best OVERALL config
        - week1-5.json: Week-specific params from best config for weeks 1-5
        - week6-9.json: Week-specific params from best config for weeks 6-9
        - week10-13.json: Week-specific params from best config for weeks 10-13
        - week14-17.json: Week-specific params from best config for weeks 14-17

        Args:
            output_dir (Path): Parent directory to create folder in

        Returns:
            Path: Path to created folder

        Raises:
            ValueError: If no results available

        Example:
            >>> folder_path = mgr.save_optimal_configs_folder(Path("simulation/optimal_configs"))
            >>> print(f"Saved configs to {folder_path}")
        """
        # Get best overall config (for base params)
        best_overall = self.get_best_config()
        if best_overall is None:
            raise ValueError("No results available to save")

        # Get best config for each week range
        best_per_range = self.get_best_configs_per_range()

        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)

        # Clean up old optimal folders if we're at the limit
        cleanup_old_optimal_folders(output_dir)

        # Generate folder name with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder_name = f"optimal_{timestamp}"
        folder_path = output_dir / folder_name
        folder_path.mkdir(parents=True, exist_ok=True)

        # Save base config (from best overall)
        base_config = self._extract_base_params(best_overall.config_dict)
        base_config['performance_metrics'] = {
            'config_id': best_overall.config_id,
            'overall_win_rate': best_overall.get_win_rate(),
            'total_wins': best_overall.total_wins,
            'total_losses': best_overall.total_losses,
            'num_simulations': best_overall.num_simulations,
            'timestamp': timestamp
        }

        with open(folder_path / 'league_config.json', 'w') as f:
            json.dump(base_config, f, indent=2)
        self.logger.info(f"Saved base config from {best_overall.config_id}")

        # Save week-specific configs
        week_range_files = {
            '1-5': 'week1-5.json',
            '6-9': 'week6-9.json',
            '10-13': 'week10-13.json',
            '14-17': 'week14-17.json'
        }

        for week_range, filename in week_range_files.items():
            best_for_range = best_per_range.get(week_range)

            if best_for_range:
                week_config = self._extract_week_params(best_for_range.config_dict)
                week_config['performance_metrics'] = {
                    'config_id': best_for_range.config_id,
                    'week_range': week_range,
                    'win_rate_for_range': best_for_range.get_win_rate_for_range(week_range),
                    'overall_win_rate': best_for_range.get_win_rate(),
                    'timestamp': timestamp
                }

                with open(folder_path / filename, 'w') as f:
                    json.dump(week_config, f, indent=2)

                self.logger.info(
                    f"Saved {filename} from {best_for_range.config_id} "
                    f"(win_rate={best_for_range.get_win_rate_for_range(week_range):.4f})"
                )

        self.logger.info(f"Saved optimal configs folder to {folder_path}")
        return folder_path

    def save_intermediate_folder(
        self,
        output_dir: Path,
        param_index: int,
        param_name: str,
        base_config: dict,
        week_configs: Dict[str, dict],
        overall_performance: Optional[Dict[str, Any]] = None,
        week_range_performance: Optional[Dict[str, Dict[str, Any]]] = None
    ) -> Path:
        """
        Save intermediate optimization state as a folder with 4 config files.

        This is called during iterative optimization to save progress after
        each parameter is optimized. The folder can be used to resume
        optimization if interrupted.

        Args:
            output_dir (Path): Parent directory to create folder in
            param_index (int): Index of parameter being optimized (for naming)
            param_name (str): Name of parameter being optimized (for naming)
            base_config (dict): Current best base config
            week_configs (Dict[str, dict]): Current best week configs
                Keys: "1-5", "6-9", "10-13", "14-17"
            overall_performance (Optional[Dict]): Overall performance metrics
                Keys: 'win_rate', 'total_wins', 'total_losses', 'config_id'
            week_range_performance (Optional[Dict]): Per-range performance metrics
                Keys: "1-5", "6-9", "10-13", "14-17" each containing win_rate and config_id

        Returns:
            Path: Path to created folder

        Example:
            >>> folder_path = mgr.save_intermediate_folder(
            ...     Path("simulation/optimal_configs"),
            ...     5,
            ...     "PLAYER_RATING_SCORING_WEIGHT",
            ...     base_config,
            ...     {"1-5": week1_5_config, "6-9": week6_9_config, "10-13": week10_13_config, "14-17": week14_17_config},
            ...     overall_performance={'win_rate': 0.65, 'config_id': 'config_001'},
            ...     week_range_performance={'1-5': {'win_rate': 0.70}, '6-9': {'win_rate': 0.65}, '10-13': {'win_rate': 0.62}, '14-17': {'win_rate': 0.60}}
            ... )
        """
        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate folder name with index and parameter name
        folder_name = f"intermediate_{param_index:02d}_{param_name}"
        folder_path = output_dir / folder_name
        folder_path.mkdir(parents=True, exist_ok=True)

        # Add performance metrics to base config if provided
        if overall_performance:
            base_config['performance_metrics'] = {
                'optimized_parameter': param_name,
                'parameter_index': param_index,
                'overall_win_rate': overall_performance.get('win_rate'),
                'total_wins': overall_performance.get('total_wins'),
                'total_losses': overall_performance.get('total_losses'),
                'config_id': overall_performance.get('config_id'),
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

        # Save base config (league_config.json)
        with open(folder_path / 'league_config.json', 'w') as f:
            json.dump(base_config, f, indent=2)
        self.logger.debug(f"Saved intermediate base config to {folder_path / 'league_config.json'}")

        # Save week-specific configs
        week_range_files = {
            '1-5': 'week1-5.json',
            '6-9': 'week6-9.json',
            '10-13': 'week10-13.json',
            '14-17': 'week14-17.json'
        }

        for week_range, filename in week_range_files.items():
            if week_range in week_configs:
                week_config = week_configs[week_range]

                # Add week-specific performance metrics if provided
                if week_range_performance and week_range in week_range_performance:
                    perf = week_range_performance[week_range]
                    week_config['performance_metrics'] = {
                        'optimized_parameter': param_name,
                        'week_range': week_range,
                        'win_rate_for_range': perf.get('win_rate'),
                        'config_id': perf.get('config_id'),
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }

                with open(folder_path / filename, 'w') as f:
                    json.dump(week_config, f, indent=2)
                self.logger.debug(f"Saved intermediate {filename}")

        self.logger.info(f"Saved intermediate configs to {folder_path}")
        return folder_path

    @staticmethod
    def load_configs_from_folder(folder_path: Path) -> Tuple[dict, Dict[str, dict]]:
        """
        Load all config files from a folder.

        Loads the folder structure created by save_intermediate_folder()
        or save_optimal_configs_folder():
        - league_config.json (base parameters)
        - week1-5.json, week6-9.json, week10-13.json, week14-17.json (week-specific params)

        Args:
            folder_path (Path): Path to folder containing config files

        Returns:
            Tuple[dict, Dict[str, dict]]: (base_config, week_configs)
                - base_config: The league_config.json contents
                - week_configs: {"1-5": config, "6-9": config, "10-13": config, "14-17": config}

        Raises:
            ValueError: If folder doesn't exist or required files are missing

        Example:
            >>> base_config, week_configs = ResultsManager.load_configs_from_folder(
            ...     Path("simulation/optimal_configs/intermediate_05_PLAYER_RATING")
            ... )
            >>> print(f"Base config: {base_config['config_name']}")
            >>> print(f"Week 1-5: {week_configs['1-5']['config_name']}")
        """
        logger = get_logger()
        folder_path = Path(folder_path)

        if not folder_path.exists():
            raise ValueError(f"Config folder does not exist: {folder_path}")

        if not folder_path.is_dir():
            raise ValueError(f"Path is not a directory: {folder_path}")

        # Required files
        required_files = ['league_config.json', 'week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']
        missing_files = []

        for filename in required_files:
            if not (folder_path / filename).exists():
                missing_files.append(filename)

        if missing_files:
            raise ValueError(
                f"Missing required config files in {folder_path}: {', '.join(missing_files)}"
            )

        # Load base config
        with open(folder_path / 'league_config.json', 'r') as f:
            base_config = json.load(f)
        logger.debug(f"Loaded base config from {folder_path / 'league_config.json'}")

        # Load week-specific configs
        week_configs = {}
        week_file_mapping = {
            'week1-5.json': '1-5',
            'week6-9.json': '6-9',
            'week10-13.json': '10-13',
            'week14-17.json': '14-17'
        }

        for filename, week_range in week_file_mapping.items():
            with open(folder_path / filename, 'r') as f:
                week_configs[week_range] = json.load(f)
            logger.debug(f"Loaded {filename}")

        logger.info(f"Loaded configs from folder: {folder_path}")
        return base_config, week_configs

    def save_all_results(self, output_path: Path) -> None:
        """
        Save all configuration results to a JSON file.

        Args:
            output_path (Path): Path to save results file

        Example:
            >>> mgr.save_all_results(Path("simulation/results/all_results.json"))
        """
        results_data = {
            'total_configs': len(self.results),
            'configs': {
                config_id: perf.to_dict()
                for config_id, perf in self.results.items()
            }
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(results_data, f, indent=2)

        self.logger.info(f"Saved all results ({len(self.results)} configs) to {output_path}")

    def update_league_config(
        self,
        optimal_config_path: Path,
        league_config_path: Path
    ) -> None:
        """
        Update league_config.json with values from optimal config.

        Preserves certain parameters from the original config while updating
        the rest from the optimal config. Also maps MATCHUP_SCORING values
        to SCHEDULE_SCORING.

        Args:
            optimal_config_path (Path): Path to optimal_*.json file
            league_config_path (Path): Path to data/league_config.json

        Preserved parameters (from original):
            - CURRENT_NFL_WEEK
            - NFL_SEASON
            - MAX_POSITIONS
            - FLEX_ELIGIBLE_POSITIONS
            - INJURY_PENALTIES

        MATCHUP -> SCHEDULE mapping:
            - SCHEDULE_SCORING.MIN_WEEKS = MATCHUP_SCORING.MIN_WEEKS
            - SCHEDULE_SCORING.IMPACT_SCALE = MATCHUP_SCORING.IMPACT_SCALE
            - SCHEDULE_SCORING.WEIGHT = MATCHUP_SCORING.WEIGHT

        Example:
            >>> mgr.update_league_config(
            ...     Path("simulation/optimal_2024.json"),
            ...     Path("data/league_config.json")
            ... )
        """
        # Parameters to preserve from original config
        PRESERVE_KEYS = [
            'CURRENT_NFL_WEEK',
            'NFL_SEASON',
            'MAX_POSITIONS',
            'FLEX_ELIGIBLE_POSITIONS',
            'INJURY_PENALTIES'
        ]

        # Load optimal config
        with open(optimal_config_path, 'r') as f:
            optimal_config = json.load(f)

        # Load original league config
        with open(league_config_path, 'r') as f:
            original_config = json.load(f)

        self.logger.info(f"Updating league config from {optimal_config_path.name}")

        # Start with optimal config (copy config_name and description as-is)
        updated_config = {
            'config_name': optimal_config.get('config_name', ''),
            'description': optimal_config.get('description', ''),
            'parameters': optimal_config['parameters'].copy()
        }

        # Preserve specific keys from original config
        for key in PRESERVE_KEYS:
            if key in original_config['parameters']:
                updated_config['parameters'][key] = original_config['parameters'][key]
                self.logger.debug(f"Preserved {key} from original config")

        # Apply MATCHUP -> SCHEDULE mapping
        if 'MATCHUP_SCORING' in updated_config['parameters']:
            matchup = updated_config['parameters']['MATCHUP_SCORING']
            schedule = updated_config['parameters'].get('SCHEDULE_SCORING', {})

            schedule['MIN_WEEKS'] = matchup.get('MIN_WEEKS', schedule.get('MIN_WEEKS'))
            schedule['IMPACT_SCALE'] = matchup.get('IMPACT_SCALE', schedule.get('IMPACT_SCALE'))
            schedule['WEIGHT'] = matchup.get('WEIGHT', schedule.get('WEIGHT'))

            updated_config['parameters']['SCHEDULE_SCORING'] = schedule
            self.logger.debug("Applied MATCHUP -> SCHEDULE mapping")

        # Remove performance_metrics if present (not part of league config)
        if 'performance_metrics' in updated_config:
            del updated_config['performance_metrics']

        # Write updated config
        with open(league_config_path, 'w') as f:
            json.dump(updated_config, f, indent=2)

        self.logger.info(f"Updated {league_config_path} with optimal parameters")
        self.logger.info(f"  Preserved: {', '.join(PRESERVE_KEYS)}")
        self.logger.info(f"  MATCHUP->SCHEDULE: MIN_WEEKS, IMPACT_SCALE, WEIGHT")

    def update_configs_folder(
        self,
        optimal_folder: Path,
        target_folder: Path
    ) -> None:
        """
        Update target config folder with values from optimal folder.

        Updates all config files (league_config.json and week-specific files)
        while preserving user-maintained parameters and applying MATCHUP->SCHEDULE
        mapping for week files.

        Args:
            optimal_folder: Path to optimal_* folder with source configs
            target_folder: Path to data/configs folder to update

        Preserved parameters (in league_config.json only):
            - CURRENT_NFL_WEEK
            - NFL_SEASON
            - MAX_POSITIONS
            - FLEX_ELIGIBLE_POSITIONS
            - INJURY_PENALTIES

        MATCHUP -> SCHEDULE mapping (in week files):
            - SCHEDULE_SCORING.MIN_WEEKS = MATCHUP_SCORING.MIN_WEEKS
            - SCHEDULE_SCORING.IMPACT_SCALE = MATCHUP_SCORING.IMPACT_SCALE
            - SCHEDULE_SCORING.WEIGHT = MATCHUP_SCORING.WEIGHT
        """
        # Parameters to preserve from original league_config.json
        PRESERVE_KEYS = [
            'CURRENT_NFL_WEEK',
            'NFL_SEASON',
            'MAX_POSITIONS',
            'FLEX_ELIGIBLE_POSITIONS',
            'INJURY_PENALTIES'
        ]

        # Config files to process
        CONFIG_FILES = ['league_config.json', 'week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']

        # Ensure target folder exists
        target_folder.mkdir(parents=True, exist_ok=True)

        for config_file in CONFIG_FILES:
            optimal_path = optimal_folder / config_file
            target_path = target_folder / config_file

            if not optimal_path.exists():
                self.logger.warning(f"Optimal config not found: {optimal_path}")
                continue

            # Load optimal config
            with open(optimal_path, 'r') as f:
                optimal_config = json.load(f)

            # Check if target exists (for preservation)
            if target_path.exists():
                with open(target_path, 'r') as f:
                    original_config = json.load(f)

                if config_file == 'league_config.json':
                    # Preserve specified keys from original
                    updated_config = optimal_config.copy()
                    if 'parameters' not in updated_config:
                        updated_config['parameters'] = {}

                    for key in PRESERVE_KEYS:
                        if 'parameters' in original_config and key in original_config['parameters']:
                            updated_config['parameters'][key] = original_config['parameters'][key]
                            self.logger.debug(f"Preserved {key} from original config")
                else:
                    # Week files: apply MATCHUP -> SCHEDULE mapping
                    updated_config = optimal_config.copy()
                    self._apply_matchup_to_schedule_mapping(updated_config)
            else:
                # Target doesn't exist - use optimal directly
                updated_config = optimal_config.copy()
                if config_file != 'league_config.json':
                    self._apply_matchup_to_schedule_mapping(updated_config)
                self.logger.info(f"Created new config (no original to preserve): {config_file}")

            # Write updated config
            with open(target_path, 'w') as f:
                json.dump(updated_config, f, indent=2)

            self.logger.info(f"Updated {config_file}")

        self.logger.info(f"✓ Updated configs folder: {target_folder}")

    def _apply_matchup_to_schedule_mapping(self, config: dict) -> None:
        """
        Apply MATCHUP_SCORING values to SCHEDULE_SCORING in a config.

        Args:
            config: Config dict to modify in place
        """
        if 'parameters' not in config:
            return

        params = config['parameters']
        if 'MATCHUP_SCORING' not in params:
            self.logger.warning("MATCHUP_SCORING not found, skipping SCHEDULE mapping")
            return

        matchup = params['MATCHUP_SCORING']
        schedule = params.get('SCHEDULE_SCORING', {})

        # Apply mapping
        if 'MIN_WEEKS' in matchup:
            schedule['MIN_WEEKS'] = matchup['MIN_WEEKS']
        if 'IMPACT_SCALE' in matchup:
            schedule['IMPACT_SCALE'] = matchup['IMPACT_SCALE']
        if 'WEIGHT' in matchup:
            schedule['WEIGHT'] = matchup['WEIGHT']

        params['SCHEDULE_SCORING'] = schedule
        self.logger.debug("Applied MATCHUP -> SCHEDULE mapping")

    def print_summary(self, top_n: int = 10) -> None:
        """
        Print summary of results to console.

        Args:
            top_n (int): Number of top configs to display (default 10)

        Example:
            >>> mgr.print_summary(top_n=5)
        """
        if not self.results:
            print("No results available")
            return

        print("\n" + "=" * 80)
        print("SIMULATION RESULTS SUMMARY")
        print("=" * 80)
        print(f"\nTotal configurations tested: {len(self.results)}")

        # Get best config
        best_config = self.get_best_config()
        if best_config:
            print(f"\nBest Configuration:")
            print(f"  ID: {best_config.config_id}")
            print(f"  Win Rate: {best_config.get_win_rate():.2%}")
            print(f"  Record: {best_config.total_wins}W-{best_config.total_losses}L")
            print(f"  Avg Points/League: {best_config.get_avg_points_per_league():.2f}")
            print(f"  Simulations: {best_config.num_simulations}")

        # Show top N configs
        print(f"\nTop {top_n} Configurations:")
        print("-" * 80)
        print(f"{'Rank':<6} {'Config ID':<15} {'Win Rate':<12} {'Record':<15} {'Avg Pts':<12} {'Sims':<8}")
        print("-" * 80)

        top_configs = self.get_top_n_configs(top_n)
        for rank, config in enumerate(top_configs, 1):
            print(
                f"{rank:<6} "
                f"{config.config_id:<15} "
                f"{config.get_win_rate():<12.2%} "
                f"{config.total_wins}W-{config.total_losses}L{'':<8} "
                f"{config.get_avg_points_per_league():<12.2f} "
                f"{config.num_simulations:<8}"
            )

        print("=" * 80 + "\n")

    def get_stats(self) -> dict:
        """
        Get aggregate statistics across all configurations.

        Returns:
            dict: Statistics including min/max/avg win rates and points

        Example:
            >>> stats = mgr.get_stats()
            >>> print(f"Average win rate: {stats['avg_win_rate']:.2%}")
        """
        if not self.results:
            return {}

        win_rates = [c.get_win_rate() for c in self.results.values()]
        avg_points = [c.get_avg_points_per_league() for c in self.results.values()]

        return {
            'total_configs': len(self.results),
            'min_win_rate': min(win_rates) if win_rates else 0.0,
            'max_win_rate': max(win_rates) if win_rates else 0.0,
            'avg_win_rate': sum(win_rates) / len(win_rates) if win_rates else 0.0,
            'min_avg_points': min(avg_points) if avg_points else 0.0,
            'max_avg_points': max(avg_points) if avg_points else 0.0,
            'avg_avg_points': sum(avg_points) / len(avg_points) if avg_points else 0.0
        }
