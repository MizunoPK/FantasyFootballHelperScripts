"""
Configuration optimization for testing different parameter combinations.

Handles preliminary testing, full grid search, and identifying optimal configurations.
"""

import itertools
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
import copy
import sys
import os

# Add current directory to path for local imports
sys.path.append(os.path.dirname(__file__))
from config import TOP_CONFIGS_PERCENTAGE
from parameter_loader import expand_parameter_combinations

@dataclass
class ConfigResult:
    """Results from testing a specific configuration"""
    config_params: Dict[str, Any]
    avg_win_percentage: float
    avg_total_points: float
    avg_points_per_game: float
    avg_consistency: float
    simulations_run: int
    user_team_rankings: List[int]  # Rankings across all simulations

class ConfigurationOptimizer:
    """Manages configuration parameter testing and optimization"""

    def __init__(self, parameter_config: Dict[str, List] = None):
        """
        Initialize the optimizer with parameter configuration.

        Args:
            parameter_config: Dictionary of parameter names to value lists.
                            If None, must call set_parameter_config() before generating configs.
        """
        self.parameter_config = parameter_config
        self.preliminary_results: List[ConfigResult] = []
        self.full_results: List[ConfigResult] = []

    def set_parameter_config(self, parameter_config: Dict[str, List]) -> None:
        """
        Set the parameter configuration for optimization.

        Args:
            parameter_config: Dictionary of parameter names to value lists
        """
        self.parameter_config = parameter_config

    def generate_preliminary_configs(self) -> List[Dict[str, Any]]:
        """
        Generate all parameter combinations for testing.

        Returns:
            List of configuration dictionaries, each representing one parameter combination

        Raises:
            ValueError: If parameter_config has not been set
        """
        if self.parameter_config is None:
            raise ValueError("Parameter configuration not set. Call set_parameter_config() first.")

        # Use parameter_loader to expand all combinations
        config_combinations = expand_parameter_combinations(self.parameter_config)

        # Handle DRAFT_ORDER weights if present (legacy support)
        processed_configs = []
        for config in config_combinations:
            if 'DRAFT_ORDER_WEIGHTS' in config:
                config = self._apply_draft_order_weights(config)
            processed_configs.append(config)

        return processed_configs

    def generate_full_configs(self, top_configs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate full parameter ranges around top performing configurations"""

        # For each top config, generate variations with finer granularity
        full_configs = []

        for base_config in top_configs:
            variations = self._generate_config_variations(base_config)
            full_configs.extend(variations)

        # Remove duplicates
        unique_configs = []
        for config in full_configs:
            if config not in unique_configs:
                unique_configs.append(config)

        return unique_configs

    def _apply_draft_order_weights(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Apply weight modifications to DRAFT_ORDER configuration"""

        # Import the base draft order
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        from draft_helper_config import DRAFT_ORDER

        weight_multiplier = config.get('DRAFT_ORDER_WEIGHTS', 1.0)

        # Create modified draft order
        modified_draft_order = []
        for round_priorities in DRAFT_ORDER:
            modified_round = {}
            for position, weight in round_priorities.items():
                modified_round[position] = weight * weight_multiplier
            modified_draft_order.append(modified_round)

        # Add the modified draft order to config
        config['DRAFT_ORDER'] = modified_draft_order

        return config

    def _generate_config_variations(self, base_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate fine-grained variations around a base configuration"""

        variations = [base_config.copy()]

        # Define fine-grained ranges around base values
        fine_ranges = {
            'INJURY_PENALTIES_MEDIUM': [-10, -5, 0, 5, 10],
            'INJURY_PENALTIES_HIGH': [-15, -10, -5, 0, 5, 10, 15],
            # DEPRECATED: Legacy scoring weights (no longer used)
            # 'POS_NEEDED_SCORE': [-15, -10, -5, 0, 5, 10, 15],
            # 'PROJECTION_BASE_SCORE': [-15, -10, -5, 0, 5, 10, 15],
            'BASE_BYE_PENALTY': [-10, -5, 0, 5, 10],
            'DRAFT_ORDER_WEIGHTS': [-0.2, -0.1, 0, 0.1, 0.2]
        }

        # Generate variations for each parameter
        for param_name, offsets in fine_ranges.items():
            if param_name in base_config:
                base_value = base_config[param_name]

                for offset in offsets:
                    new_config = base_config.copy()
                    new_value = base_value + offset

                    # Apply bounds checking
                    if param_name in ['INJURY_PENALTIES_MEDIUM', 'INJURY_PENALTIES_HIGH']:
                        new_value = max(0, min(100, new_value))
                    # DEPRECATED: Legacy scoring weights (no longer used)
                    # elif param_name == 'POS_NEEDED_SCORE':
                    #     new_value = max(0, min(150, new_value))
                    # elif param_name == 'PROJECTION_BASE_SCORE':
                    #     new_value = max(50, min(200, new_value))
                    elif param_name == 'BASE_BYE_PENALTY':
                        new_value = max(0, min(100, new_value))
                    elif param_name == 'DRAFT_ORDER_WEIGHTS':
                        new_value = max(0.1, min(2.0, new_value))

                    new_config[param_name] = new_value

                    # Handle DRAFT_ORDER weights
                    if param_name == 'DRAFT_ORDER_WEIGHTS':
                        new_config = self._apply_draft_order_weights(new_config)

                    variations.append(new_config)

        return variations

    def identify_top_configs(self, results: List[ConfigResult]) -> List[Dict[str, Any]]:
        """Identify top performing configurations from preliminary results"""

        if not results:
            return []

        # Sort by average win percentage descending
        sorted_results = sorted(results, key=lambda x: x.avg_win_percentage, reverse=True)

        # Take top percentage
        top_count = max(1, int(len(sorted_results) * TOP_CONFIGS_PERCENTAGE))
        top_results = sorted_results[:top_count]

        return [result.config_params for result in top_results]

    def analyze_config_performance(self, config_params: Dict[str, Any],
                                 simulation_results: List[Dict[str, Any]]) -> ConfigResult:
        """Analyze performance metrics for a specific configuration"""

        if not simulation_results:
            return ConfigResult(
                config_params=config_params,
                avg_win_percentage=0.0,
                avg_total_points=0.0,
                avg_points_per_game=0.0,
                avg_consistency=0.0,
                simulations_run=0,
                user_team_rankings=[]
            )

        # Extract user team performance from each simulation
        win_percentages = []
        total_points = []
        points_per_game = []
        consistencies = []
        rankings = []

        for sim_result in simulation_results:
            user_team_index = sim_result.get('user_team_index', 0)
            season_stats = sim_result.get('season_stats', {})
            team_rankings = sim_result.get('team_rankings', [])

            if user_team_index in season_stats:
                user_stats = season_stats[user_team_index]
                win_percentages.append(user_stats.win_percentage)
                total_points.append(user_stats.total_points)
                points_per_game.append(user_stats.points_per_game)
                consistencies.append(user_stats.score_consistency)

                # Find user team ranking
                user_rank = None
                for rank_info in team_rankings:
                    if rank_info['team_index'] == user_team_index:
                        user_rank = rank_info['rank']
                        break

                if user_rank:
                    rankings.append(user_rank)

        # Calculate averages
        avg_win_percentage = sum(win_percentages) / len(win_percentages) if win_percentages else 0.0
        avg_total_points = sum(total_points) / len(total_points) if total_points else 0.0
        avg_points_per_game = sum(points_per_game) / len(points_per_game) if points_per_game else 0.0
        avg_consistency = sum(consistencies) / len(consistencies) if consistencies else 0.0

        return ConfigResult(
            config_params=config_params,
            avg_win_percentage=avg_win_percentage,
            avg_total_points=avg_total_points,
            avg_points_per_game=avg_points_per_game,
            avg_consistency=avg_consistency,
            simulations_run=len(simulation_results),
            user_team_rankings=rankings
        )

    def get_optimal_config(self) -> Optional[ConfigResult]:
        """Get the best performing configuration from all results"""

        all_results = self.full_results if self.full_results else self.preliminary_results

        if not all_results:
            return None

        # Sort by win percentage, then by total points
        best_result = max(all_results, key=lambda x: (x.avg_win_percentage, x.avg_total_points))

        return best_result