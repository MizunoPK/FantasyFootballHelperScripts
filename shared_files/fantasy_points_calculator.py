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

import logging
import math
from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))


@dataclass
class FantasyPointsConfig:
    """Configuration for fantasy points calculation"""

    # Priority settings
    prefer_actual_over_projected: bool = True  # Always prefer appliedTotal over projectedTotal
    include_negative_dst_points: bool = True   # Allow negative points for DST positions

    # Fallback settings
    use_historical_fallback: bool = True       # Use previous season data when current unavailable
    use_adp_estimation: bool = True            # Use ADP-based estimation as last resort

    # ADP estimation parameters (from player-data-fetcher constants)
    min_fantasy_points_bound_factor: float = 0.8
    max_fantasy_points_bound_factor: float = 1.2
    uncertainty_adjustment_factor: float = 0.05

    # Position-specific fallback configurations
    position_fallback_configs: Dict[str, Dict[str, float]] = None

    def __post_init__(self):
        """Initialize default position fallback configs if not provided"""
        if self.position_fallback_configs is None:
            self.position_fallback_configs = {
                'QB': {'base_points': 280.0, 'multiplier': 4.5},
                'RB': {'base_points': 220.0, 'multiplier': 3.8},
                'WR': {'base_points': 200.0, 'multiplier': 3.5},
                'TE': {'base_points': 160.0, 'multiplier': 2.8},
                'K': {'base_points': 140.0, 'multiplier': 1.2},
                'DST': {'base_points': 120.0, 'multiplier': 1.0},
                'DEFAULT': {'base_points': 100.0, 'multiplier': 2.0}
            }


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
        self.logger = logging.getLogger(__name__)

    def extract_week_points(
        self,
        player_data: Dict[str, Any],
        week: int,
        position: str,
        player_name: str = "Unknown",
        fallback_data: Optional[Dict[str, Any]] = None,
        current_nfl_week: Optional[int] = None
    ) -> float:
        """
        Extract fantasy points for a specific week from ESPN player data

        This is the main entry point that consolidates logic from both modules.

        Args:
            player_data: ESPN player data dictionary containing stats array
            week: NFL week number (1-18 for regular season, 19-22 for playoffs)
            position: Player position (QB, RB, WR, TE, K, DST)
            player_name: Player name for logging purposes
            fallback_data: Optional fallback data (ADP, previous season data, etc.)

        Returns:
            Fantasy points for the specified week
        """
        try:
            # Primary extraction from ESPN stats
            points = self._extract_from_stats_array(player_data, week, position, current_nfl_week)

            if points is not None:
                self.logger.debug(f"Extracted {points:.1f} points for {player_name} week {week}")
                return points

            # Fallback mechanisms
            if self.config.use_historical_fallback and fallback_data:
                points = self._extract_historical_fallback(fallback_data, week, position)
                if points is not None:
                    self.logger.info(f"Using historical fallback for {player_name} week {week}: {points:.1f} points")
                    return points

            if self.config.use_adp_estimation and fallback_data:
                points = self._estimate_from_adp(fallback_data, position)
                if points is not None:
                    self.logger.info(f"Using ADP estimation for {player_name} week {week}: {points:.1f} points")
                    return points

            # Final fallback - position-based default
            points = self._get_position_default(position)
            self.logger.warning(f"Using position default for {player_name} week {week}: {points:.1f} points")
            return points

        except Exception as e:
            self.logger.error(f"Error extracting week points for {player_name} week {week}: {str(e)}")
            return self._get_position_default(position)

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

            current_season_entries = []
            historical_entries = []

            for stat in stats:
                # Validate stat entry structure
                if not isinstance(stat, dict):
                    continue

                season_id = stat.get('seasonId')
                scoring_period = stat.get('scoringPeriodId')
                stat_entry = stat  # ESPN data has appliedTotal/projectedTotal directly in stat, not nested

                if scoring_period == week:
                    points = None

                    # WEEK-BASED PRIORITY LOGIC (when current_nfl_week is provided):
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

                    # Validate points (allow negative for DST, filter negative for others)
                    if points is not None:
                        if position == 'DST' and self.config.include_negative_dst_points:
                            # Allow any DST points (including negative)
                            pass
                        elif points < 0:
                            # Skip negative points for non-DST positions
                            self.logger.debug(f"Skipping negative points {points} for non-DST position {position}")
                            continue

                        # Categorize by season
                        if season_id == self.season:
                            current_season_entries.append(points)
                        elif season_id == self.season - 1:
                            historical_entries.append(points)

            # Return current season data if available
            if current_season_entries:
                # Use the most recent entry (in case of multiple)
                return current_season_entries[-1]

            # Historical fallback only if configured
            if historical_entries and self.config.use_historical_fallback:
                self.logger.debug("Using historical data fallback")
                return historical_entries[-1]

            return None

        except (ValueError, TypeError, KeyError) as e:
            self.logger.warning(f"Error parsing stats array: {str(e)}")
            return None

    def _extract_historical_fallback(
        self,
        fallback_data: Dict[str, Any],
        week: int,
        position: str
    ) -> Optional[float]:
        """
        Extract points from historical/fallback data

        Args:
            fallback_data: Dictionary containing historical player data
            week: Target week number
            position: Player position

        Returns:
            Historical fantasy points if available
        """
        try:
            # Try to extract from previous season data in fallback_data
            historical_stats = fallback_data.get('historical_stats', [])

            for stat in historical_stats:
                if stat.get('scoringPeriodId') == week:
                    stat_entry = stat.get('stats', {})

                    if 'appliedTotal' in stat_entry and stat_entry['appliedTotal'] is not None:
                        return float(stat_entry['appliedTotal'])
                    elif 'projectedTotal' in stat_entry and stat_entry['projectedTotal'] is not None:
                        return float(stat_entry['projectedTotal'])

            return None

        except (ValueError, TypeError, KeyError) as e:
            self.logger.warning(f"Error extracting historical fallback: {str(e)}")
            return None

    def _estimate_from_adp(
        self,
        fallback_data: Dict[str, Any],
        position: str
    ) -> Optional[float]:
        """
        Estimate fantasy points from ADP (Average Draft Position)

        This uses the sophisticated ADP-based estimation from player-data-fetcher

        Args:
            fallback_data: Dictionary containing ADP and position mapping data
            position: Player position

        Returns:
            Estimated fantasy points based on ADP
        """
        try:
            adp = fallback_data.get('adp')
            position_mappings = fallback_data.get('position_mappings', {})

            if adp is None:
                return None

            if position not in position_mappings:
                # Use position-specific fallback configuration
                config = self.config.position_fallback_configs.get(
                    position,
                    self.config.position_fallback_configs['DEFAULT']
                )
                return max(1.0, config['base_points'] - (adp * config['multiplier']))

            mapping = position_mappings[position]

            # Position-adjusted scaling: normalize ADP within position range, then scale to fantasy points
            normalized_adp = (adp - mapping['min_adp']) / mapping['adp_range']

            # Clamp normalized ADP to [0, 1] range to handle players outside observed range
            normalized_adp = max(0.0, min(1.0, normalized_adp))

            # Convert to fantasy points: lower ADP (normalized closer to 0) = higher fantasy points
            estimated_points = mapping['max_points'] - (normalized_adp * mapping['points_range'])

            # Apply reasonable bounds with some flexibility
            min_bound = max(1.0, mapping['min_points'] * self.config.min_fantasy_points_bound_factor)
            max_bound = mapping['max_points'] * self.config.max_fantasy_points_bound_factor

            estimated_points = max(min_bound, min(max_bound, estimated_points))

            # Add uncertainty adjustment based on correlation strength
            uncertainty_factor = 1.0 - abs(mapping.get('correlation', 0.0))
            adjustment = estimated_points * uncertainty_factor * self.config.uncertainty_adjustment_factor
            estimated_points = max(min_bound, estimated_points - adjustment)

            return float(estimated_points)

        except (ValueError, TypeError, KeyError) as e:
            self.logger.warning(f"Error estimating from ADP: {str(e)}")
            return None

    def _get_position_default(self, position: str) -> float:
        """
        Get default fantasy points for a position when all else fails

        Args:
            position: Player position

        Returns:
            Default fantasy points for the position
        """
        defaults = {
            'QB': 15.0,
            'RB': 8.0,
            'WR': 6.0,
            'TE': 4.0,
            'K': 7.0,
            'DST': 5.0
        }

        return defaults.get(position, 3.0)

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