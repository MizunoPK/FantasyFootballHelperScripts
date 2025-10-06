#!/usr/bin/env python3
"""
Normalization Calculator Module

This module handles normalization of fantasy points to a 0-N scale for consistent
scoring across draft modes (Add to Roster, Waiver Optimizer, Trade Simulator).

The normalization system provides:
- Consistent baseline across all draft modes
- Configurable scale for simulation optimization
- Fair comparison between players regardless of absolute point values

Author: Kai Mizuno
Last Updated: September 2025
"""

import logging
from typing import List, Optional

try:
    from ...shared_files.FantasyPlayer import FantasyPlayer
except ImportError:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from shared_files.FantasyPlayer import FantasyPlayer


class NormalizationCalculator:
    """
    Calculates normalized fantasy points for players on 0-N scale.

    The normalization scale is configurable for simulation optimization.
    Formula: normalized_score = (player_points / max_player_points) * scale

    Example (scale=100, max=350):
        - Player with 350 pts → 100.0 (best player)
        - Player with 175 pts → 50.0 (half as good)
        - Player with 70 pts → 20.0 (20% as good)
    """

    def __init__(self, normalization_scale: float = 100.0, logger: Optional[logging.Logger] = None):
        """
        Initialize the normalization calculator.

        Args:
            normalization_scale: Maximum value for normalized scores (default: 100.0)
            logger: Logger instance for debugging
        """
        self.normalization_scale = normalization_scale
        self.logger = logger or logging.getLogger(__name__)
        self._max_player_points_cache = None

        self.logger.info(f"NormalizationCalculator initialized with scale: {self.normalization_scale}")

    def calculate_max_player_points(self, players: List[FantasyPlayer]) -> float:
        """
        Find the maximum seasonal fantasy points among all available players.

        Args:
            players: List of all players to consider

        Returns:
            float: Maximum seasonal fantasy points value
        """
        # Filter to available players only (drafted=0)
        available_players = [p for p in players if p.drafted == 0]

        if not available_players:
            self.logger.warning("No available players found for normalization, returning fallback value 1.0")
            return 1.0  # Avoid division by zero

        # Find max using remaining_season_projection if available, else fantasy_points
        max_points = 0.0
        max_player_name = None

        for p in available_players:
            # Prefer remaining_season_projection, fallback to fantasy_points
            player_points = (
                getattr(p, 'remaining_season_projection', None) or
                getattr(p, 'fantasy_points', 0.0)
            )

            if player_points > max_points:
                max_points = player_points
                max_player_name = p.name

        self.logger.debug(
            f"Maximum player points for normalization: {max_points:.1f} "
            f"(player: {max_player_name})"
        )

        return max_points if max_points > 0 else 1.0

    def normalize_player_score(
        self,
        player_points: float,
        max_player_points: float
    ) -> float:
        """
        Normalize a player's fantasy points to 0-N scale.

        Args:
            player_points: Player's seasonal fantasy points
            max_player_points: Maximum points among all players

        Returns:
            float: Normalized score on 0-N scale
        """
        if max_player_points <= 0:
            self.logger.warning("Invalid max_player_points (<= 0), returning 0")
            return 0.0

        if player_points < 0:
            self.logger.debug(f"Negative player_points ({player_points}), setting to 0")
            player_points = 0.0

        normalized = (player_points / max_player_points) * self.normalization_scale

        self.logger.debug(
            f"Normalized: {player_points:.1f} / {max_player_points:.1f} "
            f"* {self.normalization_scale} = {normalized:.2f}"
        )

        return normalized

    def normalize_player(
        self,
        player: FantasyPlayer,
        all_players: List[FantasyPlayer]
    ) -> float:
        """
        Convenience method to normalize a player using the full player pool.

        This method automatically handles:
        - Extracting player's points (prefers remaining_season_projection)
        - Calculating or using cached max value
        - Computing normalized score

        Args:
            player: Player to normalize
            all_players: All players for finding max

        Returns:
            float: Normalized score on 0-N scale
        """
        # Get player's points (prefer remaining_season_projection)
        player_points = (
            getattr(player, 'remaining_season_projection', None) or
            getattr(player, 'fantasy_points', 0.0)
        )

        # Calculate or use cached max
        if self._max_player_points_cache is None:
            self._max_player_points_cache = self.calculate_max_player_points(all_players)

        max_points = self._max_player_points_cache

        normalized = self.normalize_player_score(player_points, max_points)

        self.logger.debug(
            f"Normalized {player.name}: {player_points:.1f} → {normalized:.2f} "
            f"(max: {max_points:.1f}, scale: {self.normalization_scale})"
        )

        return normalized

    def invalidate_cache(self):
        """
        Invalidate the cached max player points.

        Call this when the player pool changes (e.g., after a draft pick).
        The next normalize_player() call will recalculate the max value.
        """
        self._max_player_points_cache = None
        self.logger.debug("Max player points cache invalidated")

    def get_normalization_info(self, player: FantasyPlayer, all_players: List[FantasyPlayer]) -> dict:
        """
        Get detailed normalization information for debugging/logging.

        Args:
            player: Player to analyze
            all_players: All players for context

        Returns:
            dict: Normalization details including raw points, max, scale, and normalized score
        """
        player_points = (
            getattr(player, 'remaining_season_projection', None) or
            getattr(player, 'fantasy_points', 0.0)
        )

        if self._max_player_points_cache is None:
            self._max_player_points_cache = self.calculate_max_player_points(all_players)

        max_points = self._max_player_points_cache
        normalized = self.normalize_player_score(player_points, max_points)

        return {
            'player_name': player.name,
            'raw_points': player_points,
            'max_points': max_points,
            'scale': self.normalization_scale,
            'normalized_score': normalized,
            'percentage': (player_points / max_points * 100) if max_points > 0 else 0
        }