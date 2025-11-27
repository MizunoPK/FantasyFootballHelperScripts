"""
Game Data Models

Data classes for representing game condition information used in scoring calculations.
These models encapsulate weather and location data for NFL games.

Author: Kai Mizuno
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class UpcomingGame:
    """
    Represents an upcoming NFL game with weather and location data.

    This dataclass holds all relevant game condition information used
    for scoring adjustments based on temperature, wind, and location.

    Attributes:
        week (int): NFL week number (1-18)
        home_team (str): Home team abbreviation (e.g., 'KC', 'PHI')
        away_team (str): Away team abbreviation
        temperature (Optional[int]): Game temperature in Fahrenheit (None for indoor)
        wind_gust (Optional[int]): Wind gust speed in mph (None for indoor)
        indoor (bool): True if game is played in a dome/indoor stadium
        neutral_site (bool): True if game is at a neutral location
        country (str): Country where game is played (default 'USA')

    Example:
        >>> game = UpcomingGame(
        ...     week=1,
        ...     home_team='KC',
        ...     away_team='BAL',
        ...     temperature=68,
        ...     wind_gust=15,
        ...     indoor=False,
        ...     neutral_site=False,
        ...     country='USA'
        ... )
        >>> game.is_home_game('KC')
        True
        >>> game.is_international()
        False
    """
    week: int
    home_team: str
    away_team: str
    temperature: Optional[int]
    wind_gust: Optional[int]
    indoor: bool
    neutral_site: bool
    country: str = "USA"

    def is_home_game(self, team: str) -> bool:
        """
        Check if a team is playing at home.

        For neutral site games, both teams are considered "away" (no home advantage).

        Args:
            team (str): Team abbreviation to check

        Returns:
            bool: True if team is the home team and not neutral site, False otherwise
        """
        if self.neutral_site:
            return False  # Neither team is home at neutral site
        return team == self.home_team

    def is_international(self) -> bool:
        """
        Check if game is played outside the USA.

        International games include:
        - London games (England)
        - Frankfurt games (Germany)
        - Sao Paulo games (Brazil)
        - Mexico City games (Mexico)

        Returns:
            bool: True if game is outside USA, False otherwise
        """
        return self.country != "USA"

    def get_team_opponent(self, team: str) -> Optional[str]:
        """
        Get the opponent for a given team.

        Args:
            team (str): Team abbreviation

        Returns:
            Optional[str]: Opponent team abbreviation, or None if team not in game
        """
        if team == self.home_team:
            return self.away_team
        elif team == self.away_team:
            return self.home_team
        return None
