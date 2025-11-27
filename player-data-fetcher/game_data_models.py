#!/usr/bin/env python3
"""
Data Models for NFL Game Data Collection

This module contains Pydantic data models for game-level data including
venue information, weather, and scores.

Author: Kai Mizuno
"""

from datetime import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field


class GameData(BaseModel):
    """
    NFL game data model with venue, weather, and score information.

    This model represents a single NFL game with all associated metadata
    for use in fantasy football analysis.

    Attributes:
        week: NFL week number (1-18)
        home_team: Home team abbreviation (e.g., "KC")
        away_team: Away team abbreviation (e.g., "BUF")
        temperature: Temperature in Fahrenheit (None for indoor games)
        gust: Wind gust speed in mph (None for indoor games)
        precipitation: Precipitation in inches (None for indoor games)
        home_team_score: Home team final score (None for future games)
        away_team_score: Away team final score (None for future games)
        indoor: Whether the stadium is indoor
        neutral_site: Whether the game is at a neutral site
        country: Country of venue (e.g., "USA", "Brazil")
        city: City of venue
        state: State of venue (None for international games)
        date: Game date in ISO 8601 format
    """

    # Game identification
    week: int = Field(..., ge=1, le=18, description="NFL week number (1-18)")
    home_team: str = Field(..., min_length=2, max_length=3, description="Home team abbreviation")
    away_team: str = Field(..., min_length=2, max_length=3, description="Away team abbreviation")

    # Weather data (None for indoor games)
    temperature: Optional[int] = Field(None, description="Temperature in Fahrenheit")
    gust: Optional[int] = Field(None, description="Wind gust speed in mph")
    precipitation: Optional[float] = Field(None, description="Precipitation in inches")

    # Scores (None for future/in-progress games)
    home_team_score: Optional[int] = Field(None, ge=0, description="Home team final score")
    away_team_score: Optional[int] = Field(None, ge=0, description="Away team final score")

    # Venue information
    indoor: bool = Field(..., description="Whether stadium is indoor")
    neutral_site: bool = Field(default=False, description="Whether game is at neutral site")
    country: str = Field(default="USA", description="Country of venue")
    city: str = Field(..., description="City of venue")
    state: Optional[str] = Field(None, description="State of venue (None for international)")
    date: str = Field(..., description="Game date in ISO 8601 format")

    model_config = {
        "json_schema_extra": {
            "example": {
                "week": 1,
                "home_team": "KC",
                "away_team": "BAL",
                "temperature": 76,
                "gust": 10,
                "precipitation": 0.0,
                "home_team_score": 27,
                "away_team_score": 20,
                "indoor": False,
                "neutral_site": False,
                "country": "USA",
                "city": "Kansas City",
                "state": "MO",
                "date": "2024-09-05T00:20Z"
            }
        }
    }

    def to_csv_row(self) -> Dict[str, Any]:
        """
        Convert GameData to a dictionary suitable for CSV export.

        Returns:
            Dict with all fields, None values as empty strings for CSV compatibility
        """
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

    @classmethod
    def from_espn_data(
        cls,
        week: int,
        event: Dict[str, Any],
        weather: Optional[Dict[str, Any]] = None
    ) -> "GameData":
        """
        Create GameData from ESPN API event data.

        Args:
            week: NFL week number
            event: ESPN API event object
            weather: Optional weather data dict with temperature, gust, precipitation

        Returns:
            GameData instance populated from ESPN data
        """
        competition = event.get("competitions", [{}])[0]
        venue = competition.get("venue", {})
        address = venue.get("address", {})
        status = competition.get("status", {}).get("type", {})
        is_completed = status.get("completed", False)

        # Extract competitors
        competitors = competition.get("competitors", [])
        home_data = None
        away_data = None

        for competitor in competitors:
            if competitor.get("homeAway") == "home":
                home_data = competitor
            else:
                away_data = competitor

        # Get team abbreviations with WAS -> WSH mapping
        home_team = home_data.get("team", {}).get("abbreviation", "") if home_data else ""
        away_team = away_data.get("team", {}).get("abbreviation", "") if away_data else ""
        home_team = "WSH" if home_team == "WAS" else home_team
        away_team = "WSH" if away_team == "WAS" else away_team

        # Get scores (convert from string to int)
        home_score = None
        away_score = None
        if is_completed and home_data and away_data:
            try:
                home_score = int(home_data.get("score", 0))
                away_score = int(away_data.get("score", 0))
            except (ValueError, TypeError):
                pass

        # Get venue info
        indoor = venue.get("indoor", False)
        neutral_site = competition.get("neutralSite", False)
        country = address.get("country", "USA")
        city = address.get("city", "")
        state = address.get("state") if country == "USA" else None

        # Get game date
        game_date = event.get("date", "")

        # Get weather data if provided
        temperature = None
        gust = None
        precipitation = None
        if weather and not indoor:
            temperature = weather.get("temperature")
            gust = weather.get("gust")
            precipitation = weather.get("precipitation")

        return cls(
            week=week,
            home_team=home_team,
            away_team=away_team,
            temperature=temperature,
            gust=gust,
            precipitation=precipitation,
            home_team_score=home_score,
            away_team_score=away_score,
            indoor=indoor,
            neutral_site=neutral_site,
            country=country,
            city=city,
            state=state,
            date=game_date
        )


# CSV column order for export
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
