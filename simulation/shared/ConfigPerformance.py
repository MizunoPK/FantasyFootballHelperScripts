"""
Configuration Performance Tracker

Tracks performance metrics for a single configuration across multiple
league simulations. Aggregates wins, losses, and total points to calculate
win rate and average performance.

Now includes per-week-range tracking for week-by-week config optimization:
- Week ranges: 1-5, 6-9, 10-13, 14-17
- Tracks wins/losses/points per range for optimal config selection

Used by ResultsManager to compare different configurations and identify
the optimal parameter settings.

Author: Kai Mizuno
"""

from typing import Dict, List, Tuple, Optional
import json


# Week range definitions
WEEK_RANGES = ["1-5", "6-9", "10-13", "14-17"]

# Horizon definitions for 6-file configuration structure
# 'ros' = Rest of Season (draft/season-long projections)
# Week ranges align with WEEK_RANGES above
HORIZONS = ['ros', '1-5', '6-9', '10-13', '14-17']

# Maps horizon names to their corresponding configuration filenames
# Used for loading and saving 6-file configuration structure
HORIZON_FILES = {
    'ros': 'draft_config.json',
    '1-5': 'week1-5.json',
    '6-9': 'week6-9.json',
    '10-13': 'week10-13.json',
    '14-17': 'week14-17.json'
}


def get_week_range(week: int) -> str:
    """
    Get the week range string for a given week number.

    Args:
        week (int): NFL week number (1-17)

    Returns:
        str: Week range string ("1-5", "6-9", "10-13", or "14-17")

    Raises:
        ValueError: If week is outside valid range (1-17)
    """
    if 1 <= week <= 5:
        return "1-5"
    elif 6 <= week <= 9:
        return "6-9"
    elif 10 <= week <= 13:
        return "10-13"
    elif 14 <= week <= 17:
        return "14-17"
    else:
        raise ValueError(f"Invalid week number: {week}. Must be between 1 and 17.")


class ConfigPerformance:
    """
    Tracks performance of a single configuration across multiple simulations.

    Aggregates results from multiple league simulations to calculate overall
    performance metrics including win rate and average points per league.

    Also tracks per-week-range performance for week-by-week optimization:
    - Week ranges: 1-5, 6-9, 10-13, 14-17
    - Each range tracks wins, losses, and points separately

    Attributes:
        config_id (str): Unique identifier for this configuration
        config_dict (dict): Full configuration dictionary
        total_wins (int): Total wins across all simulations
        total_losses (int): Total losses across all simulations
        total_points (float): Total points scored across all simulations
        num_simulations (int): Number of simulations completed
        week_range_wins (Dict[str, int]): Wins per week range
        week_range_losses (Dict[str, int]): Losses per week range
        week_range_points (Dict[str, float]): Points per week range
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

        # Per-week-range tracking
        self.week_range_wins: Dict[str, int] = {r: 0 for r in WEEK_RANGES}
        self.week_range_losses: Dict[str, int] = {r: 0 for r in WEEK_RANGES}
        self.week_range_points: Dict[str, float] = {r: 0.0 for r in WEEK_RANGES}

    def add_league_result(self, wins: int, losses: int, points: float) -> None:
        """
        Add results from a single league simulation (aggregate mode).

        This is the legacy method that adds aggregate results without
        per-week breakdown. Use add_week_results() for per-week tracking.

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

    def add_week_results(self, week_results: List[Tuple[int, bool, float]]) -> None:
        """
        Add results from a single league simulation with per-week breakdown.

        Updates both overall totals and per-week-range tracking.

        Args:
            week_results: List of (week, won, points) tuples for each week played
                - week (int): Week number (1-16)
                - won (bool): True if won that week
                - points (float): Points scored that week

        Example:
            >>> perf = ConfigPerformance("config_0001", config_dict)
            >>> week_results = [
            ...     (1, True, 120.5),   # Week 1: Win with 120.5 pts
            ...     (2, False, 95.3),   # Week 2: Loss with 95.3 pts
            ...     # ... weeks 3-16
            ... ]
            >>> perf.add_week_results(week_results)
        """
        total_wins = 0
        total_losses = 0
        total_points = 0.0

        for week, won, points in week_results:
            # Get the week range for this week
            week_range = get_week_range(week)

            # Update per-range tracking
            if won:
                self.week_range_wins[week_range] += 1
                total_wins += 1
            else:
                self.week_range_losses[week_range] += 1
                total_losses += 1

            self.week_range_points[week_range] += points
            total_points += points

        # Update overall totals
        self.total_wins += total_wins
        self.total_losses += total_losses
        self.total_points += total_points
        self.num_simulations += 1

    def get_week_range_games(self, week_range: str) -> int:
        """Get total games played in a specific week range."""
        return self.week_range_wins[week_range] + self.week_range_losses[week_range]

    def get_win_rate_for_range(self, week_range: str) -> float:
        """
        Calculate win rate for a specific week range.

        Args:
            week_range (str): Week range string ("1-5", "6-9", "10-13", or "14-17")

        Returns:
            float: Win rate for that range, or 0.0 if no games

        Example:
            >>> perf.get_win_rate_for_range("1-5")
            0.75  # 75% win rate in weeks 1-5
        """
        total_games = self.get_week_range_games(week_range)
        if total_games == 0:
            return 0.0
        return self.week_range_wins[week_range] / total_games

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
                'avg_points_per_league': 1500.0,
                'week_range_performance': {
                    '1-5': {'wins': 80, 'losses': 20, 'win_rate': 0.80},
                    '6-9': {'wins': 60, 'losses': 40, 'win_rate': 0.60},
                    '10-13': {'wins': 55, 'losses': 45, 'win_rate': 0.55},
                    '14-17': {'wins': 50, 'losses': 50, 'win_rate': 0.50}
                }
            }
        """
        result = {
            'config_id': self.config_id,
            'total_wins': self.total_wins,
            'total_losses': self.total_losses,
            'total_points': self.total_points,
            'num_simulations': self.num_simulations,
            'total_games': self.total_games,
            'win_rate': self.get_win_rate(),
            'avg_points_per_league': self.get_avg_points_per_league(),
            'week_range_performance': {}
        }

        # Add per-week-range performance
        for week_range in WEEK_RANGES:
            result['week_range_performance'][week_range] = {
                'wins': self.week_range_wins[week_range],
                'losses': self.week_range_losses[week_range],
                'points': self.week_range_points[week_range],
                'win_rate': self.get_win_rate_for_range(week_range)
            }

        return result

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
