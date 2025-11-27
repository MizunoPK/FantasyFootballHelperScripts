#!/usr/bin/env python3
"""
Game Data Fetcher for NFL Fantasy Football

This module fetches game-level data from ESPN API and weather data from
Open-Meteo API, producing a game_data.csv file with venue, weather, and
score information.

Uses sync HTTP (httpx) and dual Open-Meteo API approach:
- Historical API for games >5 days old
- Forecast API for recent/upcoming games

Author: Kai Mizuno
"""

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional, Set, Any

import httpx
import pandas as pd

# Add parent directory to path for utils access
sys.path.append(str(Path(__file__).parent.parent))
from utils.LoggingManager import get_logger

from game_data_models import GameData, GAME_DATA_CSV_COLUMNS
from coordinates_manager import CoordinatesManager
from config import (
    CURRENT_NFL_WEEK, NFL_SEASON, GAME_DATA_CSV, COORDINATES_JSON,
    REQUEST_TIMEOUT, RATE_LIMIT_DELAY
)


class GameDataFetcher:
    """
    Fetches NFL game data from ESPN API and weather from Open-Meteo.

    Handles:
    - Fetching game schedules and scores from ESPN Scoreboard API
    - Fetching weather from Open-Meteo (dual API: Historical + Forecast)
    - Week detection to avoid re-fetching existing data
    - Score backfill for previously fetched games that are now complete
    - CSV I/O with proper None handling
    """

    ESPN_SCOREBOARD_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
    OPEN_METEO_HISTORICAL_URL = "https://archive-api.open-meteo.com/v1/archive"
    OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(
        self,
        data_folder: Path,
        season: int = NFL_SEASON,
        current_week: int = CURRENT_NFL_WEEK
    ):
        """
        Initialize the GameDataFetcher.

        Args:
            data_folder: Path to the data folder for output
            season: NFL season year
            current_week: Current NFL week (1-18)
        """
        self.data_folder = Path(data_folder)
        self.season = season
        self.current_week = current_week
        self.logger = get_logger()

        # Initialize coordinates manager
        script_dir = Path(__file__).parent
        coords_file = script_dir / COORDINATES_JSON
        self.coords_manager = CoordinatesManager(coords_file)

        # Output file path
        self.output_file = self.data_folder / "game_data.csv"

        self.logger.info(f"GameDataFetcher initialized for season {season}, week {current_week}")

    def _load_existing_data(self) -> List[GameData]:
        """
        Load existing game data from CSV file.

        Returns:
            List of GameData objects from existing file, or empty list
        """
        if not self.output_file.exists():
            self.logger.info("No existing game_data.csv found, will create new file")
            return []

        try:
            df = pd.read_csv(self.output_file)
            games = []

            for _, row in df.iterrows():
                # Convert CSV row to GameData, handling empty strings as None
                game = GameData(
                    week=int(row["week"]),
                    home_team=row["home_team"],
                    away_team=row["away_team"],
                    temperature=int(row["temperature"]) if pd.notna(row["temperature"]) and row["temperature"] != "" else None,
                    gust=int(row["gust"]) if pd.notna(row["gust"]) and row["gust"] != "" else None,
                    precipitation=float(row["precipitation"]) if pd.notna(row["precipitation"]) and row["precipitation"] != "" else None,
                    home_team_score=int(row["home_team_score"]) if pd.notna(row["home_team_score"]) and row["home_team_score"] != "" else None,
                    away_team_score=int(row["away_team_score"]) if pd.notna(row["away_team_score"]) and row["away_team_score"] != "" else None,
                    indoor=bool(row["indoor"]) if isinstance(row["indoor"], bool) else str(row["indoor"]).lower() == "true",
                    neutral_site=bool(row["neutral_site"]) if isinstance(row["neutral_site"], bool) else str(row["neutral_site"]).lower() == "true",
                    country=row["country"],
                    city=row["city"],
                    state=row["state"] if pd.notna(row["state"]) and row["state"] != "" else None,
                    date=row["date"]
                )
                games.append(game)

            self.logger.info(f"Loaded {len(games)} existing games from {self.output_file}")
            return games

        except Exception as e:
            self.logger.error(f"Error loading existing game data: {e}")
            return []

    def _get_existing_weeks(self, games: List[GameData]) -> Set[int]:
        """
        Get set of weeks that already have data.

        Args:
            games: List of existing GameData objects

        Returns:
            Set of week numbers with existing data
        """
        return {game.week for game in games}

    def _determine_weeks_to_fetch(self, existing_weeks: Set[int]) -> List[int]:
        """
        Determine which weeks need to be fetched.

        Args:
            existing_weeks: Set of weeks already in the file

        Returns:
            List of week numbers to fetch
        """
        weeks_to_fetch = []
        for week in range(1, self.current_week + 1):
            if week not in existing_weeks:
                weeks_to_fetch.append(week)

        self.logger.info(f"Weeks to fetch: {weeks_to_fetch}")
        return weeks_to_fetch

    def _fetch_espn_scoreboard(self, week: int) -> Dict[str, Any]:
        """
        Fetch scoreboard data from ESPN API for a specific week.

        Args:
            week: NFL week number

        Returns:
            ESPN API response as dictionary
        """
        params = {
            "seasontype": 2,  # Regular season
            "week": week,
            "dates": self.season
        }

        try:
            response = httpx.get(
                self.ESPN_SCOREBOARD_URL,
                params=params,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            self.logger.error(f"ESPN API request failed for week {week}: {e}")
            return {"events": []}
        except Exception as e:
            self.logger.error(f"Error fetching ESPN scoreboard for week {week}: {e}")
            return {"events": []}

    def _get_weather_api_endpoint(self, game_date: str) -> str:
        """
        Determine which Open-Meteo API endpoint to use based on game date.

        Args:
            game_date: Game date in ISO 8601 format

        Returns:
            API endpoint URL (Historical or Forecast)
        """
        try:
            # Parse ISO 8601 date
            game_dt = datetime.fromisoformat(game_date.replace('Z', '+00:00'))
            five_days_ago = datetime.now(timezone.utc) - timedelta(days=5)

            if game_dt < five_days_ago:
                return self.OPEN_METEO_HISTORICAL_URL
            else:
                return self.OPEN_METEO_FORECAST_URL
        except (ValueError, TypeError):
            # Default to forecast API if date parsing fails
            return self.OPEN_METEO_FORECAST_URL

    def _fetch_weather_for_game(
        self,
        home_team: str,
        game_date: str,
        is_indoor: bool,
        is_international: bool,
        city: str,
        country: str
    ) -> Dict[str, Optional[int]]:
        """
        Fetch weather data from Open-Meteo for a game.

        Args:
            home_team: Home team abbreviation
            game_date: Game date in ISO 8601 format
            is_indoor: Whether the stadium is indoor (from ESPN API)
            is_international: Whether this is an international game
            city: City name for international games
            country: Country name for international games

        Returns:
            Dict with temperature, gust, precipitation (or None values for indoor)
        """
        # Skip weather for indoor games
        if is_indoor:
            return {"temperature": None, "gust": None, "precipitation": None}

        # Get coordinates
        coords = self.coords_manager.get_or_fetch_coordinates(
            team_abbrev=home_team,
            city=city,
            country=country,
            is_international=is_international
        )

        if not coords:
            self.logger.warning(f"No coordinates found for {home_team} / {city}, {country}")
            return {"temperature": None, "gust": None, "precipitation": None}

        try:
            # Parse date and time
            date_only = game_date.split('T')[0]  # "2024-09-05"

            # Determine API endpoint
            api_url = self._get_weather_api_endpoint(game_date)

            # Build request parameters
            params = {
                "latitude": coords["lat"],
                "longitude": coords["lon"],
                "hourly": "temperature_2m,wind_gusts_10m,precipitation",
                "temperature_unit": "fahrenheit",
                "wind_speed_unit": "mph",
                "precipitation_unit": "inch",
                "timezone": coords.get("tz", "UTC")
            }

            # Add date parameters based on API type
            if api_url == self.OPEN_METEO_HISTORICAL_URL:
                params["start_date"] = date_only
                params["end_date"] = date_only
            else:
                # Forecast API uses different parameters
                # Calculate days from today
                game_dt = datetime.fromisoformat(game_date.replace('Z', '+00:00'))
                today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
                days_diff = (game_dt - today).days

                if days_diff < 0:
                    # Past game within 5 days - use past_days
                    params["past_days"] = abs(days_diff) + 1
                    params["forecast_days"] = 1
                else:
                    # Future game
                    params["forecast_days"] = min(days_diff + 1, 16)
                    params["past_days"] = 0
                # Note: Forecast API uses past_days/forecast_days, NOT start_date/end_date
                # These parameters are mutually exclusive

            response = httpx.get(api_url, params=params, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            data = response.json()

            hourly = data.get("hourly", {})
            times = hourly.get("time", [])
            temps = hourly.get("temperature_2m", [])
            gusts = hourly.get("wind_gusts_10m", [])
            precip = hourly.get("precipitation", [])

            if not times or not temps:
                self.logger.warning(f"No weather data returned for {game_date}")
                return {"temperature": None, "gust": None, "precipitation": None}

            # Find the closest hour to game time
            # API returns times in local timezone, so we need to convert game_date UTC to local
            # Parse the game datetime in UTC and convert to local timezone
            try:
                from zoneinfo import ZoneInfo
                game_dt_utc = datetime.fromisoformat(game_date.replace('Z', '+00:00'))
                local_tz = ZoneInfo(coords.get("tz", "UTC"))
                game_dt_local = game_dt_utc.astimezone(local_tz)
                game_hour_local = game_dt_local.hour
            except Exception:
                # Fallback: extract UTC hour if timezone conversion fails
                time_part = game_date.split('T')[1] if 'T' in game_date else "00:00Z"
                game_hour_local = int(time_part.split(':')[0])

            hour_index = min(game_hour_local, len(temps) - 1)

            return {
                "temperature": round(temps[hour_index]) if hour_index < len(temps) else None,
                "gust": round(gusts[hour_index]) if hour_index < len(gusts) else None,
                "precipitation": round(precip[hour_index], 2) if hour_index < len(precip) else None
            }

        except Exception as e:
            self.logger.warning(f"Error fetching weather for {game_date}: {e}")
            return {"temperature": None, "gust": None, "precipitation": None}

    def _fetch_games_for_week(self, week: int) -> List[GameData]:
        """
        Fetch all games for a specific week.

        Args:
            week: NFL week number

        Returns:
            List of GameData objects for the week
        """
        self.logger.info(f"Fetching games for week {week}")

        scoreboard = self._fetch_espn_scoreboard(week)
        events = scoreboard.get("events", [])
        games = []

        for event in events:
            try:
                competition = event.get("competitions", [{}])[0]
                venue = competition.get("venue", {})
                address = venue.get("address", {})

                # Get indoor and neutral site flags
                is_indoor = venue.get("indoor", False)
                neutral_site = competition.get("neutralSite", False)
                country = address.get("country", "USA")

                # Determine if international
                is_international = neutral_site and country != "USA"

                # Get home team for coordinate lookup
                competitors = competition.get("competitors", [])
                home_team = ""
                for competitor in competitors:
                    if competitor.get("homeAway") == "home":
                        home_team = competitor.get("team", {}).get("abbreviation", "")
                        home_team = "WSH" if home_team == "WAS" else home_team
                        break

                # Fetch weather
                game_date = event.get("date", "")
                city = address.get("city", "")

                weather = self._fetch_weather_for_game(
                    home_team=home_team,
                    game_date=game_date,
                    is_indoor=is_indoor,
                    is_international=is_international,
                    city=city,
                    country=country
                )

                # Create GameData from ESPN data + weather
                game = GameData.from_espn_data(week, event, weather)
                games.append(game)

            except Exception as e:
                self.logger.error(f"Error processing game in week {week}: {e}")
                continue

        self.logger.info(f"Fetched {len(games)} games for week {week}")
        return games

    def _backfill_previous_week_scores(
        self,
        games: List[GameData]
    ) -> List[GameData]:
        """
        Backfill scores for games from previous week that now have scores.

        Args:
            games: List of existing GameData objects

        Returns:
            Updated list with backfilled scores
        """
        previous_week = self.current_week - 1
        if previous_week < 1:
            return games

        # Find games from previous week with missing scores
        games_to_update = [
            (i, g) for i, g in enumerate(games)
            if g.week == previous_week and (g.home_team_score is None or g.away_team_score is None)
        ]

        if not games_to_update:
            return games

        self.logger.info(f"Backfilling scores for {len(games_to_update)} games from week {previous_week}")

        # Fetch current data for previous week
        scoreboard = self._fetch_espn_scoreboard(previous_week)

        for event in scoreboard.get("events", []):
            try:
                competition = event.get("competitions", [{}])[0]
                status = competition.get("status", {}).get("type", {})

                if not status.get("completed", False):
                    continue

                competitors = competition.get("competitors", [])
                home_data = None
                away_data = None

                for competitor in competitors:
                    if competitor.get("homeAway") == "home":
                        home_data = competitor
                    else:
                        away_data = competitor

                if not home_data or not away_data:
                    continue

                home_team = home_data.get("team", {}).get("abbreviation", "")
                home_team = "WSH" if home_team == "WAS" else home_team

                # Find matching game in our list
                for idx, game in games_to_update:
                    if game.home_team == home_team:
                        try:
                            games[idx].home_team_score = int(home_data.get("score", 0))
                            games[idx].away_team_score = int(away_data.get("score", 0))
                            self.logger.debug(f"Updated scores for {game.home_team} vs {game.away_team}")
                        except (ValueError, TypeError):
                            pass
                        break

            except Exception as e:
                self.logger.warning(f"Error backfilling score: {e}")
                continue

        return games

    def save_to_csv(self, games: List[GameData]) -> Path:
        """
        Save games to CSV file.

        Args:
            games: List of GameData objects to save

        Returns:
            Path to the saved file
        """
        # Sort by week, then by date
        games_sorted = sorted(games, key=lambda g: (g.week, g.date))

        # Convert to rows
        rows = [game.to_csv_row() for game in games_sorted]

        # Create DataFrame with proper column order
        df = pd.DataFrame(rows, columns=GAME_DATA_CSV_COLUMNS)

        # Ensure directory exists
        self.output_file.parent.mkdir(parents=True, exist_ok=True)

        # Save to CSV
        df.to_csv(self.output_file, index=False)
        self.logger.info(f"Saved {len(games)} games to {self.output_file}")

        return self.output_file

    def fetch_all(self) -> List[GameData]:
        """
        Main method to fetch all game data.

        Fetches missing weeks and backfills previous week scores.

        Returns:
            List of all GameData objects
        """
        # Load existing data
        existing_games = self._load_existing_data()
        existing_weeks = self._get_existing_weeks(existing_games)

        # Determine weeks to fetch
        weeks_to_fetch = self._determine_weeks_to_fetch(existing_weeks)

        # Fetch new weeks
        all_games = existing_games.copy()
        for week in weeks_to_fetch:
            new_games = self._fetch_games_for_week(week)
            all_games.extend(new_games)

        # Backfill scores for previous week
        all_games = self._backfill_previous_week_scores(all_games)

        return all_games


def fetch_game_data(
    output_path: Optional[Path] = None,
    season: int = NFL_SEASON,
    current_week: int = CURRENT_NFL_WEEK,
    weeks: Optional[List[int]] = None
) -> Path:
    """
    Convenience function to fetch game data.

    Args:
        output_path: Custom output path (default: data/game_data.csv)
        season: NFL season year
        current_week: Current NFL week
        weeks: Specific weeks to fetch (default: 1 to current_week)

    Returns:
        Path to the saved CSV file
    """
    logger = get_logger()

    # Determine output folder
    if output_path:
        data_folder = output_path.parent
        output_file = output_path
    else:
        script_dir = Path(__file__).parent
        data_folder = script_dir.parent / "data"
        output_file = data_folder / "game_data.csv"

    # Create fetcher
    fetcher = GameDataFetcher(
        data_folder=data_folder,
        season=season,
        current_week=current_week
    )

    # Override output file if custom path provided
    if output_path:
        fetcher.output_file = output_path

    # Fetch data
    if weeks:
        # Fetch specific weeks
        all_games = []
        for week in weeks:
            games = fetcher._fetch_games_for_week(week)
            all_games.extend(games)
    else:
        # Use default fetch_all logic
        all_games = fetcher.fetch_all()

    # Save and return path
    return fetcher.save_to_csv(all_games)
