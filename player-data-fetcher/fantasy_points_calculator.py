#!/usr/bin/env python3
"""
Shared Fantasy Points Calculator

This module provides standardized logic for extracting and calculating fantasy points
from ESPN API data. Used by both player-data-fetcher and starter-helper to ensure
consistent fantasy points calculations across the entire system.

Key Features:
- Standardized extraction using ESPN's statSourceId + appliedTotal structure
- statSourceId=0 + appliedTotal = Actual game scores
- statSourceId=1 + appliedTotal = ESPN projections
- Configurable behavior for different use cases
- Robust error handling and logging
- Week-specific data extraction

Author: Kai Mizuno
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
from pathlib import Path
import sys
from utils.LoggingManager import get_logger

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

# Import NFL season from centralized config
from config import NFL_SEASON


@dataclass
class FantasyPointsConfig:
    """Configuration for fantasy points calculation - Pure week-by-week system only"""

    # Priority settings
    prefer_actual_over_projected: bool = True  # Prefer statSourceId=0 (actuals) over statSourceId=1 (projections)
    include_negative_dst_points: bool = True   # Allow negative points for DST positions

    # Pure week-by-week system: No fallbacks, returns 0.0 when no ESPN data available


class FantasyPointsExtractor:
    """
    Shared utility for extracting fantasy points from ESPN API data

    This class standardizes the logic for extracting fantasy points from ESPN's
    stat entries, with comprehensive fallback mechanisms and configurable behavior.
    """

    def __init__(self, config: Optional[FantasyPointsConfig] = None, season: int = NFL_SEASON):
        """
        Initialize the fantasy points extractor

        Args:
            config: Configuration object. If None, uses default settings
            season: Current NFL season year (defaults to NFL_SEASON from config)
        """
        self.config = config or FantasyPointsConfig()
        self.season = season
        self.logger = get_logger()

    def extract_week_points(
        self,
        player_data: Dict[str, Any],
        week: int,
        position: str,
        player_name: str = "Unknown",
        current_nfl_week: Optional[int] = None
    ) -> float:
        """
        Extract fantasy points for a specific week from ESPN player data

        Pure week-by-week system: Returns actual ESPN data or 0.0 (no fallbacks)

        Args:
            player_data: ESPN player data dictionary containing stats array
            week: NFL week number (1-18 for regular season, 19-22 for playoffs)
            position: Player position (QB, RB, WR, TE, K, DST)
            player_name: Player name for logging purposes
            fallback_data: Ignored (kept for compatibility)
            current_nfl_week: Current NFL week for prioritizing actual vs projected data

        Returns:
            Fantasy points for the specified week, or 0.0 if no ESPN data available
        """
        try:
            # Extract from ESPN stats (only source of data)
            points = self._extract_from_stats_array(player_data, week, position, current_nfl_week)

            if points is not None:
                self.logger.debug(f"Extracted {points:.1f} points for {player_name} week {week}")
                return points

            # No ESPN data available - return 0.0 (pure week-by-week system)
            self.logger.debug(f"No week-by-week data available for {player_name} week {week}, returning 0.0 points")
            return 0.0

        except Exception as e:
            self.logger.error(f"Error extracting week points for {player_name} week {week}: {str(e)}")
            return 0.0

    def _extract_from_stats_array(
        self,
        player_data: Dict[str, Any],
        week: int,
        position: str,
        current_nfl_week: Optional[int] = None
    ) -> Optional[float]:
        """
        Extract fantasy points from ESPN stats array

        ESPN API Structure:
        - statSourceId=0 + appliedTotal = Actual game scores
        - statSourceId=1 + appliedTotal = ESPN projections
        - NOTE: The 'projectedTotal' field does NOT exist in ESPN's current API

        Args:
            player_data: ESPN player data dictionary
            week: Target week number
            position: Player position for validation
            current_nfl_week: Current NFL week (used for smart priority selection)

        Returns:
            Fantasy points if found, None if not available
        """
        try:
            stats = player_data.get('player', {}).get('stats', [])

            if not stats:
                self.logger.debug("No stats array found in player data")
                return None

            # Separate entries by statSourceId
            actual_points = None  # statSourceId=0
            projected_points = None  # statSourceId=1

            for stat in stats:
                # Validate stat entry structure
                if not isinstance(stat, dict):
                    continue

                season_id = stat.get('seasonId')
                scoring_period = stat.get('scoringPeriodId')
                stat_source_id = stat.get('statSourceId')

                # Only use current season data for the target week
                if scoring_period == week and season_id == self.season:
                    # Extract appliedTotal (the only points field in ESPN's API)
                    if 'appliedTotal' in stat and stat['appliedTotal'] is not None:
                        try:
                            points = float(stat['appliedTotal'])
                        except (ValueError, TypeError):
                            continue

                        if stat_source_id == 0:
                            actual_points = points
                            self.logger.debug(f"Found actual (statSourceId=0) for week {week}: {points}")
                        elif stat_source_id == 1:
                            projected_points = points
                            self.logger.debug(f"Found projection (statSourceId=1) for week {week}: {points}")

            # SMART PRIORITY LOGIC based on week
            # For past weeks: prefer actual scores
            # For current/future weeks: prefer projections
            # Legacy mode (no current_nfl_week): prefer actuals
            points = None

            if current_nfl_week is not None:
                if week < current_nfl_week:
                    # Past weeks: prefer actual, fallback to projection
                    points = actual_points if actual_points is not None else projected_points
                else:
                    # Current/Future weeks: prefer projection, fallback to actual
                    points = projected_points if projected_points is not None else actual_points
            else:
                # Legacy behavior: prefer actual (for backward compatibility)
                points = actual_points if actual_points is not None else projected_points

            # Validate points (handle negative points based on position and config)
            if points is not None:
                if points < 0:
                    # Handle negative points
                    if position == 'DST' and self.config.include_negative_dst_points:
                        return points
                    else:
                        self.logger.debug(f"Skipping negative points {points} for {position} position")
                        return None
                else:
                    return points

            # No data found for this week
            return None

        except (ValueError, TypeError, KeyError) as e:
            self.logger.warning(f"Error parsing stats array: {str(e)}")
            return None

    # Fallback methods removed - pure week-by-week system only

    def extract_stat_entry_points(self, stat_entry: Dict[str, Any]) -> float:
        """
        Extract fantasy points directly from a single ESPN stat entry

        This method is for the simpler use case where you already have the stat entry
        and just need to extract points.

        ESPN API uses appliedTotal for both actual scores and projections.
        The distinction is made via statSourceId (0=actual, 1=projection).

        Args:
            stat_entry: ESPN stat entry dictionary

        Returns:
            Fantasy points from the stat entry (appliedTotal value)
        """
        try:
            # Handle None stat_entry
            if stat_entry is None:
                return 0.0

            # Extract appliedTotal (the only points field in ESPN's API)
            if 'appliedTotal' in stat_entry and stat_entry['appliedTotal'] is not None:
                return float(stat_entry['appliedTotal'])
            else:
                return 0.0

        except (ValueError, TypeError) as e:
            self.logger.warning(f"Error extracting fantasy points from stat entry: {str(e)}")
            return 0.0


# Convenience functions for quick usage
def extract_week_fantasy_points(
    player_data: Dict[str, Any],
    week: int,
    position: str,
    player_name: str = "Unknown",
    config: Optional[FantasyPointsConfig] = None,
    season: int = NFL_SEASON,
    fallback_data: Optional[Dict[str, Any]] = None
) -> float:
    """
    Convenience function to extract fantasy points for a specific week

    Args:
        player_data: ESPN player data dictionary
        week: NFL week number
        position: Player position
        player_name: Player name for logging
        config: Optional configuration object
        season: NFL season year
        fallback_data: Optional fallback data for ADP estimation

    Returns:
        Fantasy points for the specified week
    """
    extractor = FantasyPointsExtractor(config, season)
    return extractor.extract_week_points(player_data, week, position, player_name, fallback_data)


def extract_stat_entry_fantasy_points(stat_entry: Dict[str, Any]) -> float:
    """
    Convenience function to extract fantasy points from a stat entry

    Args:
        stat_entry: ESPN stat entry dictionary

    Returns:
        Fantasy points from the stat entry
    """
    extractor = FantasyPointsExtractor()
    return extractor.extract_stat_entry_points(stat_entry)


# Export main classes and functions
__all__ = [
    'FantasyPointsConfig',
    'FantasyPointsExtractor',
    'extract_week_fantasy_points',
    'extract_stat_entry_fantasy_points'
]