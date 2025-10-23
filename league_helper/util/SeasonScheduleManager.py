#!/usr/bin/env python3
"""
Season Schedule Manager

Manages full season NFL schedule data from season_schedule.csv.
Provides helper methods for looking up opponents and future games.

Author: Kai Mizuno
"""

from pathlib import Path
from typing import Optional, List, Dict
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.LoggingManager import get_logger
from utils.csv_utils import read_csv_with_validation


class SeasonScheduleManager:
    """
    Manages NFL season schedule data for all teams.

    Loads schedule data from season_schedule.csv and provides helper methods
    for querying opponents, future matchups, and remaining schedules.
    """

    def __init__(self, data_folder: Path):
        """
        Initialize the Season Schedule Manager.

        Args:
            data_folder: Path to data directory containing season_schedule.csv

        Note:
            If season_schedule.csv is not found, manager initializes with empty cache.
            Use is_schedule_available() to check if schedule data loaded successfully.
        """
        self.logger = get_logger()
        self.logger.debug("Initializing Season Schedule Manager")

        # Load season_schedule.csv
        self.schedule_file = data_folder / 'season_schedule.csv'
        self.schedule_cache: Dict[tuple, Optional[str]] = {}  # {(team, week): opponent}

        try:
            self._load_schedule()
            self.logger.debug(f"Loaded {len(self.schedule_cache)} schedule entries")
        except FileNotFoundError:
            self.logger.warning(f"season_schedule.csv not found at {self.schedule_file}")
            self.schedule_cache = {}
        except Exception as e:
            self.logger.error(f"Error loading schedule: {e}")
            self.schedule_cache = {}

    def _load_schedule(self):
        """
        Load schedule from CSV into cache.

        Reads season_schedule.csv and populates internal cache for fast lookups.
        Empty opponent strings are converted to None (bye weeks).

        Raises:
            FileNotFoundError: If season_schedule.csv doesn't exist
            Exception: If CSV format is invalid
        """
        import pandas as pd

        df = read_csv_with_validation(
            self.schedule_file,
            required_columns=['week', 'team', 'opponent']
        )

        for _, row in df.iterrows():
            week = int(row['week'])
            team = row['team']
            opponent = row['opponent']

            # Handle NaN values (pandas converts empty strings to NaN)
            if pd.isna(opponent):
                opponent = None
            elif isinstance(opponent, str) and not opponent.strip():
                # Empty string = bye week (convert to None)
                opponent = None
            # else: opponent is a valid string, keep it as-is

            self.schedule_cache[(team, week)] = opponent

    def get_opponent(self, team: str, week: int) -> Optional[str]:
        """
        Get opponent for a team in a specific week.

        Args:
            team: Team abbreviation (e.g., 'KC', 'PHI', 'BAL')
            week: NFL week number (1-17)

        Returns:
            Opponent team abbreviation, or None if bye week or not found

        Example:
            >>> manager.get_opponent('KC', 1)
            'BAL'
            >>> manager.get_opponent('KC', 7)  # Bye week
            None
        """
        if week < 1 or week > 17:
            self.logger.debug(f"Invalid week number: {week}")
            return None

        opponent = self.schedule_cache.get((team, week))

        if opponent is None:
            self.logger.debug(f"No opponent found for {team} in week {week}")

        return opponent

    def get_future_opponents(self, team: str, current_week: int) -> List[str]:
        """
        Get list of future opponents (excluding bye weeks).

        Args:
            team: Team abbreviation (e.g., 'KC', 'PHI', 'BAL')
            current_week: Current NFL week number

        Returns:
            List of opponent abbreviations for weeks current_week+1 through 17.
            Bye weeks are excluded from the list.

        Example:
            >>> manager.get_future_opponents('KC', 5)
            ['DEN', 'LV', 'BAL', 'BUF', 'CIN', 'LAC']
            # Week 7 bye is excluded
        """
        future_opponents = []

        for week in range(current_week + 1, 18):  # Weeks current+1 to 17
            opponent = self.get_opponent(team, week)
            if opponent:  # Skip None (bye weeks)
                future_opponents.append(opponent)

        return future_opponents

    def get_remaining_schedule(self, team: str, current_week: int) -> Dict[int, Optional[str]]:
        """
        Get remaining schedule including bye weeks.

        Args:
            team: Team abbreviation (e.g., 'KC', 'PHI', 'BAL')
            current_week: Current NFL week number

        Returns:
            Dict mapping week number to opponent (None for bye weeks).
            Includes all weeks from current_week+1 through 17.

        Example:
            >>> manager.get_remaining_schedule('KC', 5)
            {6: 'DEN', 7: None, 8: 'LV', 9: 'BAL', ...}
            # Week 7 is None (bye week)
        """
        remaining = {}

        for week in range(current_week + 1, 18):
            remaining[week] = self.get_opponent(team, week)

        return remaining

    def is_schedule_available(self) -> bool:
        """
        Check if schedule data loaded successfully.

        Returns:
            True if schedule data is available, False otherwise

        Example:
            >>> if manager.is_schedule_available():
            ...     opponents = manager.get_future_opponents('KC', 8)
            ... else:
            ...     print("Schedule data not available")
        """
        return len(self.schedule_cache) > 0
