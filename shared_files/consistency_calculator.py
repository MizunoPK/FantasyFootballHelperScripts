#!/usr/bin/env python3
"""
Consistency/Volatility Calculator for Fantasy Football

This module calculates player consistency metrics based on week-to-week performance
variance. Uses coefficient of variation (CV) to categorize players as LOW, MEDIUM,
or HIGH volatility.

Key Concepts:
- Coefficient of Variation (CV) = Standard Deviation / Mean
- CV measures relative variability (lower = more consistent)
- Only uses weeks that have already occurred (weeks < CURRENT_NFL_WEEK)
- Minimum 3 weeks of data required for reliable CV calculation

Volatility Categories:
- LOW: CV < 0.3 (consistent weekly performer)
- MEDIUM: 0.3 <= CV <= 0.6 (moderate variance)
- HIGH: CV > 0.6 (boom/bust player)

Author: Claude AI
Last Updated: 2025-10-05
"""

import statistics
from typing import Dict, Any, Optional, List
from shared_files.FantasyPlayer import FantasyPlayer
from shared_files.configs.shared_config import CURRENT_NFL_WEEK
from shared_files.configs.draft_helper_config import (
    CONSISTENCY_CV_LOW_THRESHOLD,
    CONSISTENCY_CV_HIGH_THRESHOLD,
    MINIMUM_WEEKS_FOR_CONSISTENCY
)


class ConsistencyCalculator:
    """
    Calculator for player consistency/volatility analysis.

    Uses coefficient of variation (CV) to measure week-to-week performance variance.
    Only analyzes weeks that have already occurred based on CURRENT_NFL_WEEK.
    """

    def __init__(self, logger=None):
        """
        Initialize the ConsistencyCalculator.

        Args:
            logger: Optional logger for debugging
        """
        self.logger = logger

    def calculate_consistency_score(self, player: FantasyPlayer) -> Dict[str, Any]:
        """
        Calculate consistency metrics for a player based on weekly projections.

        Only uses weeks < CURRENT_NFL_WEEK (weeks that have already occurred).
        Requires minimum 3 weeks of data for reliable calculation.

        Args:
            player: FantasyPlayer object with weekly projection data

        Returns:
            Dictionary with:
                - mean_points: Average points per week
                - std_dev: Standard deviation of weekly points
                - coefficient_of_variation: CV (std_dev / mean)
                - volatility_category: 'LOW', 'MEDIUM', or 'HIGH'
                - weeks_analyzed: Number of weeks used in calculation
        """
        # Extract weekly projections for weeks that have occurred
        weekly_points = self._get_weekly_projections(player)

        # Handle insufficient data
        if len(weekly_points) < MINIMUM_WEEKS_FOR_CONSISTENCY:
            if self.logger:
                self.logger.debug(
                    f"Insufficient data for {player.name}: {len(weekly_points)} weeks "
                    f"(need {MINIMUM_WEEKS_FOR_CONSISTENCY}), defaulting to MEDIUM"
                )
            return {
                'mean_points': 0.0,
                'std_dev': 0.0,
                'coefficient_of_variation': 0.0,
                'volatility_category': 'MEDIUM',
                'weeks_analyzed': len(weekly_points)
            }

        # Calculate statistics
        mean_points = statistics.mean(weekly_points)

        # Handle zero mean (avoid division by zero)
        if mean_points == 0:
            if self.logger:
                self.logger.debug(f"Zero mean for {player.name}, defaulting to MEDIUM")
            return {
                'mean_points': 0.0,
                'std_dev': 0.0,
                'coefficient_of_variation': 0.0,
                'volatility_category': 'MEDIUM',
                'weeks_analyzed': len(weekly_points)
            }

        # Calculate standard deviation
        if len(weekly_points) == 1:
            std_dev = 0.0
        else:
            std_dev = statistics.stdev(weekly_points)

        # Calculate coefficient of variation
        cv = std_dev / mean_points if mean_points > 0 else 0.0

        # Categorize volatility
        volatility_category = self._categorize_volatility(cv)

        if self.logger:
            self.logger.debug(
                f"Consistency for {player.name}: mean={mean_points:.2f}, "
                f"std_dev={std_dev:.2f}, CV={cv:.3f}, category={volatility_category}"
            )

        return {
            'mean_points': round(mean_points, 2),
            'std_dev': round(std_dev, 2),
            'coefficient_of_variation': round(cv, 3),
            'volatility_category': volatility_category,
            'weeks_analyzed': len(weekly_points)
        }

    def _get_weekly_projections(self, player: FantasyPlayer) -> List[float]:
        """
        Extract weekly projections for weeks that have already occurred.

        Only includes weeks < CURRENT_NFL_WEEK.
        Filters out None values (missing projections).

        Args:
            player: FantasyPlayer object

        Returns:
            List of weekly projection values (floats)
        """
        weekly_points = []

        # Only analyze weeks that have occurred (weeks < CURRENT_NFL_WEEK)
        for week in range(1, CURRENT_NFL_WEEK):
            week_attr = f'week_{week}_points'
            if hasattr(player, week_attr):
                points = getattr(player, week_attr)
                # Include 0.0 values (they represent real variance)
                # Only filter out None values
                if points is not None:
                    weekly_points.append(float(points))

        return weekly_points

    def _categorize_volatility(self, cv: float) -> str:
        """
        Categorize volatility based on coefficient of variation.

        Args:
            cv: Coefficient of variation (std_dev / mean)

        Returns:
            'LOW', 'MEDIUM', or 'HIGH'
        """
        if cv < CONSISTENCY_CV_LOW_THRESHOLD:
            return 'LOW'
        elif cv <= CONSISTENCY_CV_HIGH_THRESHOLD:
            return 'MEDIUM'
        else:
            return 'HIGH'


# Convenience function for single player calculations
def calculate_player_consistency(
    player: FantasyPlayer,
    logger=None
) -> Dict[str, Any]:
    """
    Calculate consistency for a single player (simplified interface).

    Args:
        player: FantasyPlayer object
        logger: Optional logger

    Returns:
        Dictionary with consistency metrics
    """
    calculator = ConsistencyCalculator(logger=logger)
    return calculator.calculate_consistency_score(player)


# Example usage and testing
if __name__ == "__main__":
    import sys
    from pathlib import Path

    # Add parent directory to path for imports
    sys.path.append(str(Path(__file__).parent.parent))

    print("ConsistencyCalculator Test")
    print("=" * 60)
    print(f"Current NFL Week: {CURRENT_NFL_WEEK}")
    print(f"Minimum weeks required: {MINIMUM_WEEKS_FOR_CONSISTENCY}")
    print(f"LOW threshold: CV < {CONSISTENCY_CV_LOW_THRESHOLD}")
    print(f"HIGH threshold: CV > {CONSISTENCY_CV_HIGH_THRESHOLD}")
    print("=" * 60)

    # Test with mock player data
    class MockPlayer:
        def __init__(self, name):
            self.name = name
            # Set up weekly projections
            for week in range(1, 18):
                setattr(self, f'week_{week}_points', None)

    # Create test players
    consistent_player = MockPlayer("Consistent Player")
    for week in range(1, CURRENT_NFL_WEEK):
        setattr(consistent_player, f'week_{week}_points', 12.0)  # Same every week

    volatile_player = MockPlayer("Volatile Player")
    for week in range(1, CURRENT_NFL_WEEK):
        # Alternating high/low
        setattr(volatile_player, f'week_{week}_points', 24.0 if week % 2 == 0 else 2.0)

    calculator = ConsistencyCalculator()

    print("\n1. Consistent Player (same points every week):")
    result1 = calculator.calculate_consistency_score(consistent_player)
    print(f"   Mean: {result1['mean_points']}, CV: {result1['coefficient_of_variation']}")
    print(f"   Category: {result1['volatility_category']} (expected: LOW)")

    print("\n2. Volatile Player (alternating high/low):")
    result2 = calculator.calculate_consistency_score(volatile_player)
    print(f"   Mean: {result2['mean_points']}, CV: {result2['coefficient_of_variation']}")
    print(f"   Category: {result2['volatility_category']} (expected: HIGH)")

    print("\n" + "=" * 60)
    print("Test complete!")
