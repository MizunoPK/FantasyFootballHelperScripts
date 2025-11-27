"""
Game Data Manager

Manages loading and access to game condition data (temperature, wind, location)
from game_data.csv. Provides O(1) lookup of game conditions by team for use
in scoring calculations.

Author: Kai Mizuno
"""

import csv
from pathlib import Path
from typing import Dict, Optional

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.LoggingManager import get_logger

from util.upcoming_game_model import UpcomingGame


class GameDataManager:
    """
    Manages game condition data for scoring calculations.

    Loads game_data.csv and provides efficient lookup of game conditions
    (temperature, wind, location) by team. Used by PlayerScoringCalculator
    to apply weather and location adjustments.

    Attributes:
        data_folder (Path): Path to data folder containing game_data.csv
        games_by_team (Dict[str, UpcomingGame]): Games indexed by team abbreviation
        all_games (Dict[int, List[UpcomingGame]]): All games indexed by week
        logger: Logger instance

    Example:
        >>> manager = GameDataManager(Path('./data'), current_week=6)
        >>> game = manager.get_game('KC')
        >>> if game:
        ...     print(f"KC vs {game.away_team}, temp: {game.temperature}")
    """

    def __init__(self, data_folder: Path, current_week: Optional[int] = None) -> None:
        """
        Initialize GameDataManager and load game data.

        Args:
            data_folder (Path): Path to folder containing game_data.csv
            current_week (Optional[int]): If provided, only games for this week
                are indexed by team. If None, all games are loaded but get_game()
                requires a week parameter.

        Note:
            If game_data.csv doesn't exist, manager initializes with empty data
            (graceful degradation for backwards compatibility).
        """
        self.logger = get_logger()
        self.data_folder = data_folder
        self.current_week = current_week

        # Games indexed by team (for current week lookup)
        self.games_by_team: Dict[str, UpcomingGame] = {}

        # All games indexed by week (for simulation week-by-week lookup)
        self.all_games: Dict[int, Dict[str, UpcomingGame]] = {}

        self._load_game_data()

    def _load_game_data(self) -> None:
        """Load game data from CSV file."""
        game_data_path = self.data_folder / 'game_data.csv'

        if not game_data_path.exists():
            self.logger.debug(f"game_data.csv not found at {game_data_path}, "
                            "game conditions scoring will be disabled")
            return

        try:
            with open(game_data_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    game = self._parse_game_row(row)
                    if game is None:
                        continue

                    # Index by week
                    if game.week not in self.all_games:
                        self.all_games[game.week] = {}

                    # Index by both home and away team
                    self.all_games[game.week][game.home_team] = game
                    self.all_games[game.week][game.away_team] = game

                    # If current week is set, also populate games_by_team for fast lookup
                    if self.current_week and game.week == self.current_week:
                        self.games_by_team[game.home_team] = game
                        self.games_by_team[game.away_team] = game

            game_count = sum(len(games) // 2 for games in self.all_games.values())  # Divide by 2 since each game indexed twice
            self.logger.debug(f"Loaded {game_count} games from game_data.csv "
                            f"({len(self.all_games)} weeks)")

            if self.current_week:
                self.logger.debug(f"Current week {self.current_week}: "
                                f"{len(self.games_by_team) // 2} games indexed")

        except Exception as e:
            self.logger.error(f"Error loading game_data.csv: {e}")
            # Graceful degradation - continue with empty data

    def _parse_game_row(self, row: Dict[str, str]) -> Optional[UpcomingGame]:
        """
        Parse a CSV row into an UpcomingGame object.

        Args:
            row (Dict[str, str]): CSV row as dictionary

        Returns:
            Optional[UpcomingGame]: Parsed game object, or None if invalid
        """
        try:
            week = int(row['week'])
            home_team = row['home_team'].strip().upper()
            away_team = row['away_team'].strip().upper()

            # Parse temperature (empty string = indoor/no data)
            temp_str = row.get('temperature', '').strip()
            temperature = int(float(temp_str)) if temp_str else None

            # Parse wind gust (empty string = indoor/no data)
            gust_str = row.get('gust', '').strip()
            wind_gust = int(float(gust_str)) if gust_str else None

            # Parse indoor flag
            indoor_str = row.get('indoor', 'False').strip()
            indoor = indoor_str.lower() == 'true'

            # Parse neutral site flag
            neutral_str = row.get('neutral_site', 'False').strip()
            neutral_site = neutral_str.lower() == 'true'

            # Parse country (default to USA)
            country = row.get('country', 'USA').strip() or 'USA'

            return UpcomingGame(
                week=week,
                home_team=home_team,
                away_team=away_team,
                temperature=temperature,
                wind_gust=wind_gust,
                indoor=indoor,
                neutral_site=neutral_site,
                country=country
            )

        except (ValueError, KeyError) as e:
            self.logger.warning(f"Error parsing game row: {e}, row={row}")
            return None

    def get_game(self, team: str, week: Optional[int] = None) -> Optional[UpcomingGame]:
        """
        Get game data for a team.

        Args:
            team (str): Team abbreviation (e.g., 'KC', 'PHI')
            week (Optional[int]): Week number. If None, uses current_week set at init.

        Returns:
            Optional[UpcomingGame]: Game object if team has a game, None if bye week
                or team not found.

        Example:
            >>> game = manager.get_game('KC')  # Uses current_week
            >>> game = manager.get_game('KC', week=5)  # Specific week
        """
        team = team.strip().upper()
        target_week = week if week is not None else self.current_week

        if target_week is None:
            self.logger.warning("get_game called without week and no current_week set")
            return None

        # Try week-specific lookup first (supports simulation)
        if target_week in self.all_games:
            return self.all_games[target_week].get(team)

        # Fall back to games_by_team (only populated if current_week matches)
        if target_week == self.current_week:
            return self.games_by_team.get(team)

        return None

    def set_current_week(self, week: int) -> None:
        """
        Update the current week and rebuild the games_by_team index.

        Args:
            week (int): New current week number

        Note:
            This is useful for simulation where the week changes frequently.
        """
        self.current_week = week
        self.games_by_team.clear()

        if week in self.all_games:
            self.games_by_team = self.all_games[week].copy()
            self.logger.debug(f"Updated current week to {week}, "
                            f"{len(self.games_by_team) // 2} games indexed")

    def has_game_data(self) -> bool:
        """
        Check if any game data is loaded.

        Returns:
            bool: True if game data is available, False otherwise
        """
        return len(self.all_games) > 0
