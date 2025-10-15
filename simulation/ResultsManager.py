"""
Results Manager

Aggregates and manages performance results across all configuration tests.
Tracks results for all 46,656 configurations, identifies the best performing
configuration, and saves optimal configs to disk.

Author: Kai Mizuno
Date: 2024
"""

import json
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime

import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.LoggingManager import get_logger

sys.path.append(str(Path(__file__).parent))
from ConfigPerformance import ConfigPerformance


class ResultsManager:
    """
    Manages performance results for all configuration tests.

    Tracks ConfigPerformance objects for each configuration, identifies
    the best performing config, and saves results to disk.

    Attributes:
        results (Dict[str, ConfigPerformance]): {config_id: performance}
        logger: Logger instance
    """

    def __init__(self):
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

    def save_optimal_config(self, output_dir: Path) -> Path:
        """
        Save the best configuration to a JSON file with timestamp.

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
