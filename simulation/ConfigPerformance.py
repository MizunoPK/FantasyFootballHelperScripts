"""
Configuration Performance Tracker

Tracks performance metrics for a single configuration across multiple
league simulations. Aggregates wins, losses, and total points to calculate
win rate and average performance.

Used by ResultsManager to compare different configurations and identify
the optimal parameter settings.

Author: Kai Mizuno
Date: 2024
"""

from typing import Dict, Optional
import json


class ConfigPerformance:
    """
    Tracks performance of a single configuration across multiple simulations.

    Aggregates results from multiple league simulations to calculate overall
    performance metrics including win rate and average points per league.

    Attributes:
        config_id (str): Unique identifier for this configuration
        config_dict (dict): Full configuration dictionary
        total_wins (int): Total wins across all simulations
        total_losses (int): Total losses across all simulations
        total_points (float): Total points scored across all simulations
        num_simulations (int): Number of simulations completed
    """

    def __init__(self, config_id: str, config_dict: dict) -> None:
        """
        Initialize ConfigPerformance tracker.

        Args:
            config_id (str): Unique identifier (e.g., "config_0001")
            config_dict (dict): Full configuration dictionary
        """
        self.config_id = config_id
        self.config_dict = config_dict
        self.total_wins = 0
        self.total_losses = 0
        self.total_points = 0.0
        self.num_simulations = 0

    def add_league_result(self, wins: int, losses: int, points: float) -> None:
        """
        Add results from a single league simulation.

        Args:
            wins (int): Number of wins in this league
            losses (int): Number of losses in this league
            points (float): Total points scored in this league

        Example:
            >>> perf = ConfigPerformance("config_0001", config_dict)
            >>> perf.add_league_result(10, 7, 1404.62)
            >>> perf.add_league_result(12, 5, 1523.45)
            >>> perf.get_win_rate()
            0.6470588235294118  # (10+12)/(17+17) = 22/34
        """
        self.total_wins += wins
        self.total_losses += losses
        self.total_points += points
        self.num_simulations += 1

    @property
    def total_games(self) -> int:
        """Total games played across all simulations."""
        return self.total_wins + self.total_losses

    def get_win_rate(self) -> float:
        """
        Calculate win rate across all simulations.

        Returns:
            float: Win rate (total_wins / total_games), or 0.0 if no games

        Example:
            >>> perf.total_wins = 220
            >>> perf.total_losses = 140
            >>> perf.get_win_rate()
            0.6111111111111112  # 220/360
        """
        if self.total_games == 0:
            return 0.0
        return self.total_wins / self.total_games

    def get_avg_points_per_league(self) -> float:
        """
        Calculate average points per league simulation.

        Returns:
            float: Average points per league, or 0.0 if no simulations

        Example:
            >>> perf.total_points = 150000.0
            >>> perf.num_simulations = 100
            >>> perf.get_avg_points_per_league()
            1500.0
        """
        if self.num_simulations == 0:
            return 0.0
        return self.total_points / self.num_simulations

    def compare_to(self, other: 'ConfigPerformance') -> int:
        """
        Compare this config's performance to another.

        Comparison logic:
        1. Higher win rate is better
        2. If win rates equal (within 0.0001), higher avg points is better

        Args:
            other (ConfigPerformance): Other configuration to compare against

        Returns:
            int: 1 if self is better, -1 if other is better, 0 if tied

        Example:
            >>> config1 = ConfigPerformance("c1", {})
            >>> config1.add_league_result(12, 5, 1500.0)
            >>> config2 = ConfigPerformance("c2", {})
            >>> config2.add_league_result(10, 7, 1450.0)
            >>> config1.compare_to(config2)
            1  # config1 has higher win rate (12/17 > 10/17)
        """
        self_win_rate = self.get_win_rate()
        other_win_rate = other.get_win_rate()

        # Compare win rates (primary metric)
        win_rate_diff = self_win_rate - other_win_rate
        if abs(win_rate_diff) > 0.0001:  # Not essentially equal
            return 1 if win_rate_diff > 0 else -1

        # Win rates are essentially equal, use points as tiebreaker
        self_avg_points = self.get_avg_points_per_league()
        other_avg_points = other.get_avg_points_per_league()

        points_diff = self_avg_points - other_avg_points
        if abs(points_diff) > 0.01:  # Not essentially equal
            return 1 if points_diff > 0 else -1

        # Both metrics essentially equal
        return 0

    def to_dict(self) -> dict:
        """
        Convert to dictionary for serialization.

        Returns:
            dict: All performance data in dict format

        Example:
            >>> perf.to_dict()
            {
                'config_id': 'config_0001',
                'total_wins': 220,
                'total_losses': 140,
                'total_points': 150000.0,
                'num_simulations': 100,
                'win_rate': 0.6111,
                'avg_points_per_league': 1500.0
            }
        """
        return {
            'config_id': self.config_id,
            'total_wins': self.total_wins,
            'total_losses': self.total_losses,
            'total_points': self.total_points,
            'num_simulations': self.num_simulations,
            'total_games': self.total_games,
            'win_rate': self.get_win_rate(),
            'avg_points_per_league': self.get_avg_points_per_league()
        }

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"ConfigPerformance(id={self.config_id}, "
            f"win_rate={self.get_win_rate():.4f}, "
            f"avg_pts={self.get_avg_points_per_league():.2f}, "
            f"sims={self.num_simulations})"
        )

    def __str__(self) -> str:
        """Human-readable string representation."""
        return (
            f"{self.config_id}: "
            f"{self.total_wins}W-{self.total_losses}L "
            f"({self.get_win_rate():.1%}), "
            f"avg {self.get_avg_points_per_league():.1f} pts/league "
            f"({self.num_simulations} sims)"
        )
