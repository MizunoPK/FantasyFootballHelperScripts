"""
ProjectedPointsManager - Utility for accessing projected points data.

This manager loads and provides access to historical projected points data
from players_projected.csv, which contains week-by-week projection values
that were made at the start of each week.
"""

import pandas as pd
from pathlib import Path


class ProjectedPointsManager:
    """Manages access to projected points data for performance calculations."""

    def __init__(self, config):
        """
        Initialize the ProjectedPointsManager.

        Args:
            config: ConfigManager instance for accessing CURRENT_NFL_WEEK
        """
        self.config = config
        self.projected_data = None
        self._load_projected_data()

    def _load_projected_data(self):
        """Load the projected points CSV file."""
        projected_file = Path('data/players_projected.csv')

        if not projected_file.exists():
            raise FileNotFoundError(
                f"Projected points file not found: {projected_file}. "
                "Run player data fetcher to generate this file."
            )

        self.projected_data = pd.read_csv(projected_file)

        # Create a lowercase name lookup for faster matching
        self.projected_data['name_lower'] = (
            self.projected_data['name'].str.lower().str.strip()
        )

    def get_projected_points(self, player, week_num):
        """
        Get projected points for a specific player and week.

        Args:
            player: FantasyPlayer object
            week_num: Week number (1-17)

        Returns:
            float: Projected points for the week, or None if not available
        """
        if self.projected_data is None:
            return None

        player_name_lower = player.name.lower().strip()
        week_col = f'week_{week_num}_points'

        # Find matching player
        match = self.projected_data[
            self.projected_data['name_lower'] == player_name_lower
        ]

        if match.empty or week_col not in match.columns:
            return None

        projected_value = match.iloc[0][week_col]

        # Handle NaN or invalid values
        if pd.isna(projected_value):
            return None

        return float(projected_value)

    def get_projected_points_array(self, player, start_week, end_week):
        """
        Get array of projected points for a range of weeks.

        Args:
            player: FantasyPlayer object
            start_week: Starting week number (inclusive)
            end_week: Ending week number (inclusive)

        Returns:
            list: List of projected points (floats) for each week.
                  None values indicate unavailable data.
        """
        projected_array = []

        for week_num in range(start_week, end_week + 1):
            projected = self.get_projected_points(player, week_num)
            projected_array.append(projected)

        return projected_array

    def get_historical_projected_points(self, player):
        """
        Get all historical projected points up to current week - 1.

        This is a convenience method for performance calculations that need
        projected points for weeks 1 through (CURRENT_NFL_WEEK - 1).

        Args:
            player: FantasyPlayer object

        Returns:
            list: List of projected points for weeks 1 to (CURRENT_NFL_WEEK - 1)
        """
        current_week = self.config.current_nfl_week

        if current_week <= 1:
            return []

        return self.get_projected_points_array(player, 1, current_week - 1)
