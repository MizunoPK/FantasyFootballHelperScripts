#!/usr/bin/env python3
"""
Coordinates Manager for NFL Game Data Collection

This module manages stadium coordinates for weather data lookups.
Coordinates are stored in a JSON file and can be dynamically extended
via geocoding API for unknown venues (e.g., international games).

Author: Kai Mizuno
"""

import json
import sys
from pathlib import Path
from typing import Dict, Optional, Any

import httpx

# Add parent directory to path for utils access
sys.path.append(str(Path(__file__).parent.parent))
from utils.LoggingManager import get_logger


class CoordinatesManager:
    """
    Manages stadium coordinates with dynamic lookup and caching.

    Loads coordinates from a JSON file and provides lookup methods for
    NFL stadiums and international venues. Unknown international venues
    are looked up via the Open-Meteo Geocoding API and cached.

    Attributes:
        coordinates_file: Path to the coordinates JSON file
        data: Dictionary containing stadium coordinates
    """

    GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/search"

    # Country name normalization for geocoding API compatibility
    # ESPN uses country subdivisions (England, Scotland, Wales) but geocoding API needs full country
    COUNTRY_NORMALIZATION = {
        "England": "United Kingdom",
        "Scotland": "United Kingdom",
        "Wales": "United Kingdom",
        "Northern Ireland": "United Kingdom",
    }

    def __init__(self, coordinates_file: Path):
        """
        Initialize the CoordinatesManager.

        Args:
            coordinates_file: Path to the coordinates JSON file
        """
        self.coordinates_file = Path(coordinates_file)
        self.logger = get_logger()
        self.data = self._load_coordinates()

    def _load_coordinates(self) -> Dict[str, Any]:
        """
        Load coordinates from JSON file, create if doesn't exist.

        Returns:
            Dictionary with nfl_stadiums and international_venues
        """
        if self.coordinates_file.exists():
            try:
                with open(self.coordinates_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.logger.info(f"Loaded coordinates for {len(data.get('nfl_stadiums', {}))} NFL stadiums")
                    return data
            except (json.JSONDecodeError, IOError) as e:
                self.logger.error(f"Error loading coordinates file: {e}")
                return {"nfl_stadiums": {}, "international_venues": {}}
        else:
            self.logger.warning(f"Coordinates file not found: {self.coordinates_file}")
            return {"nfl_stadiums": {}, "international_venues": {}}

    def _save_coordinates(self) -> None:
        """Save coordinates to JSON file."""
        try:
            with open(self.coordinates_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2)
            self.logger.debug(f"Saved coordinates to {self.coordinates_file}")
        except IOError as e:
            self.logger.error(f"Error saving coordinates file: {e}")

    def get_nfl_stadium(self, team_abbrev: str) -> Optional[Dict[str, Any]]:
        """
        Get coordinates for an NFL team's home stadium.

        Args:
            team_abbrev: Team abbreviation (e.g., "KC", "BUF")

        Returns:
            Dictionary with lat, lon, tz, name or None if not found
        """
        return self.data.get("nfl_stadiums", {}).get(team_abbrev)

    def get_international_venue(self, city: str, country: str) -> Optional[Dict[str, Any]]:
        """
        Get coordinates for an international venue.

        Args:
            city: City name
            country: Country name

        Returns:
            Dictionary with lat, lon, tz, name or None if not found
        """
        key = f"{city},{country}"
        return self.data.get("international_venues", {}).get(key)

    def get_or_fetch_coordinates(
        self,
        team_abbrev: Optional[str] = None,
        city: Optional[str] = None,
        country: Optional[str] = None,
        is_international: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Get coordinates from cache or fetch from geocoding API.

        For NFL stadiums: provide team_abbrev
        For international venues: provide city and country, set is_international=True

        Args:
            team_abbrev: Team abbreviation for NFL stadiums
            city: City name for international venues
            country: Country name for international venues
            is_international: True if looking up an international venue

        Returns:
            Dictionary with lat, lon, tz, name or None if not found
        """
        if is_international and city and country:
            # Check cache first
            coords = self.get_international_venue(city, country)
            if coords:
                self.logger.debug(f"Found cached coordinates for {city}, {country}")
                return coords

            # Fetch from geocoding API
            self.logger.info(f"Fetching coordinates for international venue: {city}, {country}")
            coords = self._fetch_coordinates_from_api(city, country)
            if coords:
                # Cache the result
                key = f"{city},{country}"
                if "international_venues" not in self.data:
                    self.data["international_venues"] = {}
                self.data["international_venues"][key] = coords
                self._save_coordinates()
                self.logger.info(f"Cached coordinates for {city}, {country}")
            return coords
        elif team_abbrev:
            coords = self.get_nfl_stadium(team_abbrev)
            if not coords:
                self.logger.warning(f"NFL stadium not found for team: {team_abbrev}")
            return coords
        else:
            self.logger.warning("No team_abbrev or city/country provided for coordinate lookup")
            return None

    def _fetch_coordinates_from_api(self, city: str, country: str) -> Optional[Dict[str, Any]]:
        """
        Fetch coordinates from Open-Meteo Geocoding API.

        Args:
            city: City name
            country: Country name

        Returns:
            Dictionary with lat, lon, tz, name or None if API fails
        """
        try:
            # Normalize country name for geocoding API compatibility
            # ESPN returns "England" but API needs "United Kingdom"
            normalized_country = self.COUNTRY_NORMALIZATION.get(country, country)

            params = {
                "name": f"{city}, {normalized_country}",
                "count": 1,
                "language": "en",
                "format": "json"
            }

            response = httpx.get(
                self.GEOCODING_API_URL,
                params=params,
                timeout=30
            )

            if response.status_code != 200:
                self.logger.error(f"Geocoding API error: {response.status_code}")
                return None

            data = response.json()
            results = data.get("results", [])

            if not results:
                self.logger.warning(f"No geocoding results for {city}, {country}")
                return None

            result = results[0]
            return {
                "lat": result["latitude"],
                "lon": result["longitude"],
                "tz": result.get("timezone", "UTC"),
                "name": result.get("name", f"{city} Stadium")
            }

        except httpx.RequestError as e:
            self.logger.error(f"Geocoding API request failed: {e}")
            return None
        except (KeyError, ValueError) as e:
            self.logger.error(f"Error parsing geocoding response: {e}")
            return None
