#!/usr/bin/env python3
"""
Game Data Fetcher for Historical Data Compiler

Fetches game-level data from ESPN Scoreboard API and weather data from
Open-Meteo Historical API for completed NFL seasons.

Adapted from player-data-fetcher/game_data_fetcher.py.

Author: Kai Mizuno
"""

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from .http_client import BaseHTTPClient
from .constants import (
    ESPN_SCOREBOARD_API_URL,
    OPEN_METEO_ARCHIVE_URL,
    REGULAR_SEASON_WEEKS,
    GAME_DATA_FILE,
    normalize_team_abbrev,
)

import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.LoggingManager import get_logger


# CSV column order for game_data.csv
GAME_DATA_CSV_COLUMNS = [
    "week",
    "home_team",
    "away_team",
    "temperature",
    "gust",
    "precipitation",
    "home_team_score",
    "away_team_score",
    "indoor",
    "neutral_site",
    "country",
    "city",
    "state",
    "date"
]


@dataclass
class GameData:
    """
    NFL game data with venue, weather, and score information.

    Attributes:
        week: NFL week number (1-17)
        home_team: Home team abbreviation
        away_team: Away team abbreviation
        temperature: Temperature in Fahrenheit (None for indoor)
        gust: Wind gust speed in mph (None for indoor)
        precipitation: Precipitation in inches (None for indoor)
        home_team_score: Home team final score
        away_team_score: Away team final score
        indoor: Whether stadium is indoor
        neutral_site: Whether game is at neutral site
        country: Country of venue
        city: City of venue
        state: State of venue (None for international)
        date: Game date in ISO 8601 format
    """
    week: int
    home_team: str
    away_team: str
    temperature: Optional[int]
    gust: Optional[int]
    precipitation: Optional[float]
    home_team_score: Optional[int]
    away_team_score: Optional[int]
    indoor: bool
    neutral_site: bool
    country: str
    city: str
    state: Optional[str]
    date: str

    def to_csv_row(self) -> Dict[str, Any]:
        """Convert to CSV row dict with empty strings for None values."""
        return {
            "week": self.week,
            "home_team": self.home_team,
            "away_team": self.away_team,
            "temperature": self.temperature if self.temperature is not None else "",
            "gust": self.gust if self.gust is not None else "",
            "precipitation": self.precipitation if self.precipitation is not None else "",
            "home_team_score": self.home_team_score if self.home_team_score is not None else "",
            "away_team_score": self.away_team_score if self.away_team_score is not None else "",
            "indoor": self.indoor,
            "neutral_site": self.neutral_site,
            "country": self.country,
            "city": self.city,
            "state": self.state if self.state is not None else "",
            "date": self.date
        }


class GameDataFetcher:
    """
    Fetches NFL game data from ESPN API and weather from Open-Meteo.

    For historical data compilation, uses:
    - ESPN Scoreboard API for game schedules, scores, venues
    - Open-Meteo Historical API for weather (archive-api)
    """

    # Country name normalization for geocoding
    COUNTRY_NORMALIZATION = {
        "England": "United Kingdom",
        "Scotland": "United Kingdom",
        "Wales": "United Kingdom",
        "Northern Ireland": "United Kingdom",
    }

    def __init__(self, http_client: BaseHTTPClient):
        """
        Initialize GameDataFetcher.

        Args:
            http_client: Shared HTTP client instance
        """
        self.http_client = http_client
        self.logger = get_logger()
        self.coordinates = self._load_coordinates()

    def _load_coordinates(self) -> Dict[str, Any]:
        """Load stadium coordinates from JSON file."""
        coords_file = Path(__file__).parent / "coordinates.json"
        if coords_file.exists():
            try:
                with open(coords_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.logger.debug(f"Loaded coordinates for {len(data.get('nfl_stadiums', {}))} stadiums")
                    return data
            except (json.JSONDecodeError, IOError) as e:
                self.logger.error(f"Error loading coordinates: {e}")
        return {"nfl_stadiums": {}, "international_venues": {}}

    def _get_coordinates(
        self,
        team_abbrev: str,
        city: str,
        country: str,
        is_international: bool
    ) -> Optional[Dict[str, Any]]:
        """
        Get coordinates for a venue.

        Args:
            team_abbrev: Home team abbreviation
            city: City name
            country: Country name
            is_international: Whether this is an international game

        Returns:
            Dict with lat, lon, tz or None
        """
        if is_international:
            key = f"{city},{country}"
            return self.coordinates.get("international_venues", {}).get(key)
        else:
            return self.coordinates.get("nfl_stadiums", {}).get(team_abbrev)

    async def fetch_game_data(self, year: int) -> List[GameData]:
        """
        Fetch complete season game data.

        Args:
            year: NFL season year

        Returns:
            List of GameData for all regular season games
        """
        self.logger.info(f"Fetching game data for {year} season (weeks 1-{REGULAR_SEASON_WEEKS})")

        all_games: List[GameData] = []

        for week in range(1, REGULAR_SEASON_WEEKS + 1):
            self.logger.debug(f"Fetching game data for week {week}/{REGULAR_SEASON_WEEKS}")

            params = {
                "seasontype": 2,  # Regular season
                "week": week,
                "dates": year
            }

            try:
                data = await self.http_client.get(ESPN_SCOREBOARD_API_URL, params=params)
                week_games = await self._parse_week_games(data, week)
                all_games.extend(week_games)
            except Exception as e:
                self.logger.error(f"Error fetching week {week}: {e}")
                raise  # Fail-completely approach

        self.logger.info(f"Fetched {len(all_games)} games for {year} season")
        return all_games

    async def _parse_week_games(self, data: dict, week: int) -> List[GameData]:
        """
        Parse games from ESPN API response for a single week.

        Args:
            data: ESPN API response
            week: Week number

        Returns:
            List of GameData objects
        """
        games: List[GameData] = []
        events = data.get('events', [])

        for event in events:
            try:
                game = await self._parse_game_event(event, week)
                if game:
                    games.append(game)
            except Exception as e:
                self.logger.error(f"Error parsing game in week {week}: {e}")
                raise  # Fail-completely

        return games

    async def _parse_game_event(self, event: dict, week: int) -> Optional[GameData]:
        """
        Parse a single game event from ESPN API.

        Args:
            event: ESPN API event object
            week: Week number

        Returns:
            GameData object or None
        """
        competition = event.get("competitions", [{}])[0]
        venue = competition.get("venue", {})
        address = venue.get("address", {})
        status = competition.get("status", {}).get("type", {})

        # Venue info
        is_indoor = venue.get("indoor", False)
        neutral_site = competition.get("neutralSite", False)
        country = address.get("country", "USA")
        city = address.get("city", "")
        state = address.get("state") if country == "USA" else None
        is_international = neutral_site and country != "USA"

        # Game date
        game_date = event.get("date", "")

        # Extract competitors
        competitors = competition.get("competitors", [])
        home_data = None
        away_data = None

        for competitor in competitors:
            if competitor.get("homeAway") == "home":
                home_data = competitor
            else:
                away_data = competitor

        if not home_data or not away_data:
            self.logger.warning(f"Missing competitor data for game in week {week}")
            return None

        # Get team abbreviations
        home_team = normalize_team_abbrev(
            home_data.get("team", {}).get("abbreviation", "")
        )
        away_team = normalize_team_abbrev(
            away_data.get("team", {}).get("abbreviation", "")
        )

        # Get scores (historical data should always have scores)
        home_score = None
        away_score = None
        is_completed = status.get("completed", False)

        if is_completed:
            try:
                home_score = int(home_data.get("score", 0))
                away_score = int(away_data.get("score", 0))
            except (ValueError, TypeError):
                pass

        # Fetch weather for outdoor games
        weather = {"temperature": None, "gust": None, "precipitation": None}
        if not is_indoor and game_date:
            weather = await self._fetch_weather(
                home_team=home_team,
                game_date=game_date,
                city=city,
                country=country,
                is_international=is_international
            )

        return GameData(
            week=week,
            home_team=home_team,
            away_team=away_team,
            temperature=weather.get("temperature"),
            gust=weather.get("gust"),
            precipitation=weather.get("precipitation"),
            home_team_score=home_score,
            away_team_score=away_score,
            indoor=is_indoor,
            neutral_site=neutral_site,
            country=country,
            city=city,
            state=state,
            date=game_date
        )

    async def _fetch_weather(
        self,
        home_team: str,
        game_date: str,
        city: str,
        country: str,
        is_international: bool
    ) -> Dict[str, Optional[int]]:
        """
        Fetch weather from Open-Meteo Historical API.

        Args:
            home_team: Home team abbreviation
            game_date: Game date in ISO 8601 format
            city: City name
            country: Country name
            is_international: Whether international game

        Returns:
            Dict with temperature, gust, precipitation (or None values)
        """
        coords = self._get_coordinates(home_team, city, country, is_international)
        if not coords:
            self.logger.info("No coordinates available for game, skipping weather data")
            return {"temperature": None, "gust": None, "precipitation": None}

        self.logger.debug(f"Fetching weather for {game_date} at {coords['lat']},{coords['lon']}")

        try:
            # Parse date
            date_only = game_date.split('T')[0]

            # Historical API parameters
            params = {
                "latitude": coords["lat"],
                "longitude": coords["lon"],
                "start_date": date_only,
                "end_date": date_only,
                "hourly": "temperature_2m,wind_gusts_10m,precipitation",
                "temperature_unit": "fahrenheit",
                "wind_speed_unit": "mph",
                "precipitation_unit": "inch",
                "timezone": coords.get("tz", "UTC")
            }

            data = await self.http_client.get(OPEN_METEO_ARCHIVE_URL, params=params)

            hourly = data.get("hourly", {})
            temps = hourly.get("temperature_2m", [])
            gusts = hourly.get("wind_gusts_10m", [])
            precip = hourly.get("precipitation", [])

            if not temps:
                return {"temperature": None, "gust": None, "precipitation": None}

            # Get game hour (approximate from UTC time)
            try:
                from zoneinfo import ZoneInfo
                from datetime import datetime
                game_dt_utc = datetime.fromisoformat(game_date.replace('Z', '+00:00'))
                local_tz = ZoneInfo(coords.get("tz", "UTC"))
                game_dt_local = game_dt_utc.astimezone(local_tz)
                hour_index = game_dt_local.hour
            except Exception:
                # Fallback: use 13:00 (common game time)
                hour_index = 13

            hour_index = min(hour_index, len(temps) - 1)

            return {
                "temperature": round(temps[hour_index]) if hour_index < len(temps) else None,
                "gust": round(gusts[hour_index]) if hour_index < len(gusts) else None,
                "precipitation": round(precip[hour_index], 2) if hour_index < len(precip) else None
            }

        except Exception as e:
            self.logger.warning(f"Error fetching weather for {game_date}: {e}")
            return {"temperature": None, "gust": None, "precipitation": None}

    def write_game_data_csv(
        self,
        games: List[GameData],
        output_path: Path
    ) -> None:
        """
        Write game_data.csv.

        Args:
            games: List of GameData objects
            output_path: Path to output CSV file
        """
        self.logger.info(f"Writing game data to {output_path}")

        # Sort by week, then date
        games_sorted = sorted(games, key=lambda g: (g.week, g.date))

        # Write CSV
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=GAME_DATA_CSV_COLUMNS)
            writer.writeheader()
            for game in games_sorted:
                writer.writerow(game.to_csv_row())

        self.logger.info(f"Wrote {len(games)} games to {output_path}")


async def fetch_and_write_game_data(
    year: int,
    output_dir: Path,
    http_client: BaseHTTPClient
) -> List[GameData]:
    """
    Convenience function to fetch game data and write CSV.

    Args:
        year: NFL season year
        output_dir: Output directory
        http_client: HTTP client instance

    Returns:
        List of GameData for use by other modules
    """
    fetcher = GameDataFetcher(http_client)
    games = await fetcher.fetch_game_data(year)

    output_path = output_dir / GAME_DATA_FILE
    fetcher.write_game_data_csv(games, output_path)

    return games
