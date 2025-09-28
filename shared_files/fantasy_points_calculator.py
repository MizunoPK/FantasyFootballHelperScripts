#!/usr/bin/env python3
"""
Shared Fantasy Points Calculator

This module provides standardized logic for extracting and calculating fantasy points
from ESPN API data. Used by both player-data-fetcher and starter-helper to ensure
consistent fantasy points calculations across the entire system.

Key Features:
- Standardized priority: appliedTotal (actual) → projectedTotal (projected) → fallbacks
- Comprehensive fallback logic including ADP-based estimation
- Configurable behavior for different use cases
- Robust error handling and logging
- Week-specific data extraction

Author: Generated for NFL Fantasy Data Collection
Last Updated: September 2025
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import sys
from shared_files.logging_utils import setup_module_logging

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))


@dataclass
class FantasyPointsConfig:
    """Configuration for fantasy points calculation - Pure week-by-week system only"""

    # Priority settings
    prefer_actual_over_projected: bool = True  # Always prefer appliedTotal over projectedTotal
    include_negative_dst_points: bool = True   # Allow negative points for DST positions

    # Pure week-by-week system: No fallbacks, returns 0.0 when no ESPN data available


class FantasyPointsExtractor:
    """
    Shared utility for extracting fantasy points from ESPN API data

    This class standardizes the logic for extracting fantasy points from ESPN's
    stat entries, with comprehensive fallback mechanisms and configurable behavior.
    """

    def __init__(self, config: Optional[FantasyPointsConfig] = None, season: int = 2025):
        """
        Initialize the fantasy points extractor

        Args:
            config: Configuration object. If None, uses default settings
            season: Current NFL season year
        """
        self.config = config or FantasyPointsConfig()
        self.season = season
        self.logger = setup_module_logging(__name__)

    def extract_week_points(
        self,
        player_data: Dict[str, Any],
        week: int,
        position: str,
        player_name: str = "Unknown",
        fallback_data: Optional[Dict[str, Any]] = None,  # Kept for compatibility but ignored
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
            self.logger.info(f"No week-by-week data available for {player_name} week {week}, returning 0.0 points")
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

        Standardized logic: appliedTotal (actual) → projectedTotal (projected) → None

        Args:
            player_data: ESPN player data dictionary
            week: Target week number
            position: Player position for validation

        Returns:
            Fantasy points if found, None if not available
        """
        try:
            stats = player_data.get('player', {}).get('stats', [])

            if not stats:
                self.logger.debug("No stats array found in player data")
                return None

            for stat in stats:
                # Validate stat entry structure
                if not isinstance(stat, dict):
                    continue

                season_id = stat.get('seasonId')
                scoring_period = stat.get('scoringPeriodId')
                stat_entry = stat  # ESPN data has appliedTotal/projectedTotal directly in stat, not nested

                # Only use current season data - no historical fallback
                if scoring_period == week and season_id == self.season:
                    points = None

                    # WEEK-BASED PRIORITY LOGIC:
                    # Past weeks (week < current): appliedTotal → projectedTotal
                    # Current/Future weeks (week >= current): projectedTotal → appliedTotal
                    # Legacy behavior (when current_nfl_week is None): appliedTotal → projectedTotal

                    if current_nfl_week is not None:
                        if week < current_nfl_week:
                            # Past weeks: prefer appliedTotal (actual scores)
                            if 'appliedTotal' in stat_entry and stat_entry['appliedTotal'] is not None:
                                points = float(stat_entry['appliedTotal'])
                                self.logger.debug(f"Found appliedTotal for past week {week}: {points}")
                            elif 'projectedTotal' in stat_entry and stat_entry['projectedTotal'] is not None:
                                points = float(stat_entry['projectedTotal'])
                                self.logger.debug(f"Found projectedTotal fallback for past week {week}: {points}")
                        else:
                            # Current/Future weeks: prefer projectedTotal (projected scores)
                            if 'projectedTotal' in stat_entry and stat_entry['projectedTotal'] is not None:
                                points = float(stat_entry['projectedTotal'])
                                self.logger.debug(f"Found projectedTotal for current/future week {week}: {points}")
                            elif 'appliedTotal' in stat_entry and stat_entry['appliedTotal'] is not None:
                                points = float(stat_entry['appliedTotal'])
                                self.logger.debug(f"Found appliedTotal fallback for current/future week {week}: {points}")
                    else:
                        # Legacy behavior: prefer appliedTotal (for backward compatibility)
                        if 'appliedTotal' in stat_entry and stat_entry['appliedTotal'] is not None:
                            points = float(stat_entry['appliedTotal'])
                            self.logger.debug(f"Found appliedTotal (legacy mode): {points}")
                        elif 'projectedTotal' in stat_entry and stat_entry['projectedTotal'] is not None:
                            points = float(stat_entry['projectedTotal'])
                            self.logger.debug(f"Found projectedTotal fallback (legacy mode): {points}")

                    # Validate points (handle negative points based on position and config)
                    if points is not None:
                        if points < 0:
                            # Handle negative points
                            if position == 'DST' and self.config.include_negative_dst_points:
                                # Allow negative DST points if configured
                                return points
                            else:
                                # Skip negative points for non-DST or when DST negatives disabled
                                self.logger.debug(f"Skipping negative points {points} for {position} position")
                                continue
                        else:
                            # Non-negative points are always allowed
                            return points

            # No current season data found
            return None

        except (ValueError, TypeError, KeyError) as e:
            self.logger.warning(f"Error parsing stats array: {str(e)}")
            return None

    # Fallback methods removed - pure week-by-week system only

    def extract_stat_entry_points(self, stat_entry: Dict[str, Any]) -> float:
        """
        Extract fantasy points directly from a single ESPN stat entry

        This method is for the simpler use case where you already have the stat entry
        and just need to extract points with standardized priority.

        Args:
            stat_entry: ESPN stat entry dictionary

        Returns:
            Fantasy points from the stat entry
        """
        try:
            # Handle None stat_entry
            if stat_entry is None:
                return 0.0

            # STANDARDIZED PRIORITY: appliedTotal → projectedTotal → 0.0
            if 'appliedTotal' in stat_entry and stat_entry['appliedTotal'] is not None:
                return float(stat_entry['appliedTotal'])
            elif 'projectedTotal' in stat_entry and stat_entry['projectedTotal'] is not None:
                return float(stat_entry['projectedTotal'])
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
    season: int = 2025,
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