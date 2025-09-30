#!/usr/bin/env python3
"""
Matchup Calculator for Fantasy Football Starter Helper

Calculates matchup-based multipliers for player projections based on team
offensive ranking vs opponent defensive ranking.

Formula: (Opponent Defensive Rank) - (Player's Team Offensive Rank)
Positive difference = favorable matchup (good offense vs weak defense)
Negative difference = unfavorable matchup (weak offense vs strong defense)

Author: Kai Mizuno
Last Updated: September 2025
"""

import logging
from typing import Dict, Optional, Tuple
import pandas as pd

from starter_helper_config import (
    MATCHUP_MULTIPLIERS,
    MATCHUP_ENABLED_POSITIONS,
    QB, RB, WR, TE, K, DST
)
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from shared_files.csv_utils import safe_csv_read


class MatchupCalculator:
    """
    Calculates matchup multipliers for player projections based on team rankings.

    The matchup system applies multipliers to projected points based on the
    matchup quality between a player's team offense and their opponent's defense.

    Only applies to QB, RB, WR, TE positions (not K or DST).
    """

    def __init__(self, teams_csv_path: str = '../shared_files/teams.csv'):
        """
        Initialize the matchup calculator.

        Args:
            teams_csv_path: Path to teams.csv file with rankings and matchups
        """
        self.logger = logging.getLogger(__name__)
        self.teams_csv_path = teams_csv_path
        self.team_data: Optional[pd.DataFrame] = None
        self._load_team_data()

    def _load_team_data(self) -> None:
        """Load team ranking and matchup data from CSV file."""
        try:
            df = safe_csv_read(self.teams_csv_path)

            if df is None or df.empty:
                self.logger.warning(f"Failed to load team data from {self.teams_csv_path}")
                return

            # Validate required columns
            required_columns = ['team', 'offensive_rank', 'defensive_rank', 'opponent']
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                self.logger.error(f"Missing required columns in teams.csv: {missing_columns}")
                return

            self.team_data = df
            self.logger.info(f"Loaded team data for matchup calculations: {len(df)} teams")

        except Exception as e:
            self.logger.error(f"Error loading team data: {e}")
            self.team_data = None

    def is_matchup_available(self) -> bool:
        """
        Check if matchup calculations are available.

        Returns:
            True if team data is loaded and valid, False otherwise
        """
        return self.team_data is not None and not self.team_data.empty

    def get_rank_difference(self, player_team: str) -> Optional[int]:
        """
        Calculate rank difference for a player's team matchup.

        Formula: (Opponent Defensive Rank) - (Player's Team Offensive Rank)

        Args:
            player_team: Team abbreviation (e.g., 'KC', 'BUF')

        Returns:
            Rank difference integer, or None if data unavailable
        """
        if not self.is_matchup_available():
            return None

        # Find player's team data
        team_row = self.team_data[self.team_data['team'] == player_team]

        if team_row.empty:
            self.logger.debug(f"Team not found in matchup data: {player_team}")
            return None

        team_offense_rank = team_row.iloc[0]['offensive_rank']
        opponent_abbr = team_row.iloc[0]['opponent']

        # Find opponent's defensive rank
        opponent_row = self.team_data[self.team_data['team'] == opponent_abbr]

        if opponent_row.empty:
            self.logger.debug(f"Opponent not found in matchup data: {opponent_abbr}")
            return None

        opponent_defense_rank = opponent_row.iloc[0]['defensive_rank']

        # Calculate rank difference
        rank_diff = int(opponent_defense_rank) - int(team_offense_rank)

        self.logger.debug(
            f"Matchup for {player_team} vs {opponent_abbr}: "
            f"OFF#{team_offense_rank} vs DEF#{opponent_defense_rank} = {rank_diff:+d}"
        )

        return rank_diff

    def get_multiplier_for_rank_difference(self, rank_diff: int) -> float:
        """
        Get the matchup multiplier for a given rank difference.

        Args:
            rank_diff: Rank difference (opponent defense - team offense)

        Returns:
            Multiplier value (e.g., 0.8, 1.0, 1.2)
        """
        # Check each range to find where rank_diff belongs
        # Note: Ranges defined in config as tuples (lower, upper)
        # (-inf, -14): very poor (0.8x)
        # (-15, -5): poor (0.9x)
        # (-5, 6): neutral (1.0x)
        # (6, 15): good (1.1x)
        # (15, inf): excellent (1.2x)

        if rank_diff <= -15:
            return 0.8
        elif rank_diff <= -6:
            return 0.9
        elif rank_diff <= 5:
            return 1.0
        elif rank_diff <= 14:
            return 1.1
        else:  # rank_diff >= 15
            return 1.2

    def calculate_matchup_adjustment(
        self,
        player_team: str,
        position: str,
        base_points: float
    ) -> Tuple[float, str]:
        """
        Calculate matchup-adjusted points for a player.

        Args:
            player_team: Player's team abbreviation
            position: Player position (QB, RB, WR, TE, K, DST)
            base_points: Base projected points before matchup adjustment

        Returns:
            Tuple of (adjusted_points, explanation_string)
        """
        # Check if position is eligible for matchup adjustments
        if position not in MATCHUP_ENABLED_POSITIONS:
            self.logger.debug(f"Position {position} not eligible for matchup adjustments")
            return base_points, ""

        # Check if matchup data is available
        if not self.is_matchup_available():
            self.logger.debug("Matchup data not available, no adjustment applied")
            return base_points, ""

        # Get rank difference
        rank_diff = self.get_rank_difference(player_team)

        if rank_diff is None:
            self.logger.debug(f"Could not calculate rank difference for {player_team}")
            return base_points, ""

        # Get multiplier for this rank difference
        multiplier = self.get_multiplier_for_rank_difference(rank_diff)

        # Apply multiplier
        adjusted_points = base_points * multiplier

        # Create explanation string
        adjustment = adjusted_points - base_points
        sign = "+" if adjustment > 0 else ""

        # Determine matchup quality descriptor
        if rank_diff >= 15:
            quality = "excellent"
        elif rank_diff >= 6:
            quality = "good"
        elif rank_diff >= -5:
            quality = "neutral"
        elif rank_diff >= -14:
            quality = "poor"
        else:
            quality = "very poor"

        explanation = f"{sign}{adjustment:.1f} matchup ({quality}: {multiplier:.1f}x)"

        self.logger.debug(
            f"Matchup adjustment for {player_team}: {base_points:.1f} -> "
            f"{adjusted_points:.1f} ({quality} matchup, rank_diff={rank_diff:+d})"
        )

        return adjusted_points, explanation

    def get_matchup_quality(self, player_team: str) -> Optional[str]:
        """
        Get the matchup quality descriptor for a team.

        Args:
            player_team: Team abbreviation

        Returns:
            Quality descriptor string or None if unavailable
        """
        rank_diff = self.get_rank_difference(player_team)

        if rank_diff is None:
            return None

        if rank_diff >= 15:
            return "excellent"
        elif rank_diff >= 6:
            return "good"
        elif rank_diff >= -5:
            return "neutral"
        elif rank_diff >= -14:
            return "poor"
        else:
            return "very poor"


if __name__ == "__main__":
    # Example usage and testing
    logging.basicConfig(level=logging.DEBUG)

    calculator = MatchupCalculator()

    if calculator.is_matchup_available():
        print("Matchup calculator initialized successfully")

        # Test with some example teams
        test_teams = ['KC', 'BUF', 'SF', 'DAL']

        for team in test_teams:
            rank_diff = calculator.get_rank_difference(team)
            quality = calculator.get_matchup_quality(team)

            if rank_diff is not None:
                print(f"{team}: rank_diff={rank_diff:+d}, quality={quality}")

                # Test adjustment calculation
                adjusted, explanation = calculator.calculate_matchup_adjustment(
                    team, 'QB', 20.0
                )
                print(f"  QB with 20.0 base points -> {adjusted:.1f} ({explanation})")
    else:
        print("Failed to initialize matchup calculator")