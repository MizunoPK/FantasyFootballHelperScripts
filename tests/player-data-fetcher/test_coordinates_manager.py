"""
Unit tests for coordinates_manager module

Tests coordinate lookups, caching, and geocoding API integration.

Author: Kai Mizuno
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent / "player-data-fetcher"))

from coordinates_manager import CoordinatesManager


class TestCoordinatesManagerInitialization:
    """Test CoordinatesManager initialization"""

    def test_init_with_existing_file(self, tmp_path):
        """Test initialization with existing coordinates file"""
        coords_file = tmp_path / "coordinates.json"
        coords_data = {
            "nfl_stadiums": {
                "KC": {"lat": 39.0489, "lon": -94.4839, "tz": "America/Chicago", "name": "Arrowhead Stadium"}
            },
            "international_venues": {}
        }
        coords_file.write_text(json.dumps(coords_data))

        manager = CoordinatesManager(coords_file)

        assert "KC" in manager.data.get("nfl_stadiums", {})
        assert manager.data["nfl_stadiums"]["KC"]["lat"] == 39.0489

    def test_init_with_missing_file(self, tmp_path):
        """Test initialization with missing file returns empty data"""
        coords_file = tmp_path / "missing.json"

        manager = CoordinatesManager(coords_file)

        assert manager.data == {"nfl_stadiums": {}, "international_venues": {}}

    def test_init_with_invalid_json(self, tmp_path):
        """Test initialization with invalid JSON returns empty data"""
        coords_file = tmp_path / "invalid.json"
        coords_file.write_text("not valid json {{{")

        manager = CoordinatesManager(coords_file)

        assert manager.data == {"nfl_stadiums": {}, "international_venues": {}}

    def test_init_stores_file_path(self, tmp_path):
        """Test that coordinates file path is stored"""
        coords_file = tmp_path / "coordinates.json"
        coords_file.write_text('{"nfl_stadiums": {}, "international_venues": {}}')

        manager = CoordinatesManager(coords_file)

        assert manager.coordinates_file == coords_file


class TestGetNflStadium:
    """Test get_nfl_stadium method"""

    def test_get_existing_stadium(self, tmp_path):
        """Test getting coordinates for existing NFL stadium"""
        coords_file = tmp_path / "coordinates.json"
        coords_data = {
            "nfl_stadiums": {
                "KC": {"lat": 39.0489, "lon": -94.4839, "tz": "America/Chicago", "name": "Arrowhead Stadium"},
                "SF": {"lat": 37.4033, "lon": -121.9694, "tz": "America/Los_Angeles", "name": "Levi's Stadium"}
            },
            "international_venues": {}
        }
        coords_file.write_text(json.dumps(coords_data))

        manager = CoordinatesManager(coords_file)

        kc = manager.get_nfl_stadium("KC")
        assert kc["lat"] == 39.0489
        assert kc["lon"] == -94.4839
        assert kc["tz"] == "America/Chicago"
        assert kc["name"] == "Arrowhead Stadium"

    def test_get_nonexistent_stadium(self, tmp_path):
        """Test getting coordinates for non-existent team returns None"""
        coords_file = tmp_path / "coordinates.json"
        coords_data = {
            "nfl_stadiums": {
                "KC": {"lat": 39.0489, "lon": -94.4839, "tz": "America/Chicago", "name": "Arrowhead Stadium"}
            },
            "international_venues": {}
        }
        coords_file.write_text(json.dumps(coords_data))

        manager = CoordinatesManager(coords_file)

        result = manager.get_nfl_stadium("XXX")
        assert result is None

    def test_get_all_32_teams(self, tmp_path):
        """Test getting coordinates for all 32 NFL teams"""
        # Create minimal data for all teams
        teams = ["ARI", "ATL", "BAL", "BUF", "CAR", "CHI", "CIN", "CLE",
                 "DAL", "DEN", "DET", "GB", "HOU", "IND", "JAX", "KC",
                 "LV", "LAC", "LA", "MIA", "MIN", "NE", "NO", "NYG",
                 "NYJ", "PHI", "PIT", "SF", "SEA", "TB", "TEN", "WSH"]

        coords_data = {
            "nfl_stadiums": {
                team: {"lat": 40.0 + i, "lon": -90.0 - i, "tz": "America/Chicago", "name": f"Stadium {i}"}
                for i, team in enumerate(teams)
            },
            "international_venues": {}
        }
        coords_file = tmp_path / "coordinates.json"
        coords_file.write_text(json.dumps(coords_data))

        manager = CoordinatesManager(coords_file)

        for team in teams:
            result = manager.get_nfl_stadium(team)
            assert result is not None, f"Failed for team {team}"
            assert "lat" in result
            assert "lon" in result


class TestGetInternationalVenue:
    """Test get_international_venue method"""

    def test_get_existing_venue(self, tmp_path):
        """Test getting coordinates for cached international venue"""
        coords_file = tmp_path / "coordinates.json"
        coords_data = {
            "nfl_stadiums": {},
            "international_venues": {
                "London,United Kingdom": {"lat": 51.5074, "lon": -0.1278, "tz": "Europe/London", "name": "Tottenham Stadium"}
            }
        }
        coords_file.write_text(json.dumps(coords_data))

        manager = CoordinatesManager(coords_file)

        london = manager.get_international_venue("London", "United Kingdom")
        assert london["lat"] == 51.5074
        assert london["lon"] == -0.1278
        assert london["tz"] == "Europe/London"

    def test_get_nonexistent_venue(self, tmp_path):
        """Test getting coordinates for non-cached venue returns None"""
        coords_file = tmp_path / "coordinates.json"
        coords_data = {
            "nfl_stadiums": {},
            "international_venues": {}
        }
        coords_file.write_text(json.dumps(coords_data))

        manager = CoordinatesManager(coords_file)

        result = manager.get_international_venue("Paris", "France")
        assert result is None


class TestGetOrFetchCoordinates:
    """Test get_or_fetch_coordinates method"""

    def test_get_nfl_stadium_via_get_or_fetch(self, tmp_path):
        """Test getting NFL stadium coordinates via get_or_fetch"""
        coords_file = tmp_path / "coordinates.json"
        coords_data = {
            "nfl_stadiums": {
                "KC": {"lat": 39.0489, "lon": -94.4839, "tz": "America/Chicago", "name": "Arrowhead Stadium"}
            },
            "international_venues": {}
        }
        coords_file.write_text(json.dumps(coords_data))

        manager = CoordinatesManager(coords_file)

        result = manager.get_or_fetch_coordinates(team_abbrev="KC")
        assert result["lat"] == 39.0489
        assert result["name"] == "Arrowhead Stadium"

    def test_get_cached_international_via_get_or_fetch(self, tmp_path):
        """Test getting cached international venue via get_or_fetch"""
        coords_file = tmp_path / "coordinates.json"
        coords_data = {
            "nfl_stadiums": {},
            "international_venues": {
                "London,United Kingdom": {"lat": 51.5074, "lon": -0.1278, "tz": "Europe/London", "name": "Tottenham Stadium"}
            }
        }
        coords_file.write_text(json.dumps(coords_data))

        manager = CoordinatesManager(coords_file)

        result = manager.get_or_fetch_coordinates(
            city="London",
            country="United Kingdom",
            is_international=True
        )
        assert result["lat"] == 51.5074

    def test_no_params_returns_none(self, tmp_path):
        """Test get_or_fetch with no params returns None"""
        coords_file = tmp_path / "coordinates.json"
        coords_file.write_text('{"nfl_stadiums": {}, "international_venues": {}}')

        manager = CoordinatesManager(coords_file)

        result = manager.get_or_fetch_coordinates()
        assert result is None

    @patch('coordinates_manager.httpx.get')
    def test_fetch_international_from_api(self, mock_get, tmp_path):
        """Test fetching international venue from geocoding API"""
        coords_file = tmp_path / "coordinates.json"
        coords_file.write_text('{"nfl_stadiums": {}, "international_venues": {}}')

        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [{
                "latitude": -23.5505,
                "longitude": -46.6333,
                "timezone": "America/Sao_Paulo",
                "name": "Sao Paulo"
            }]
        }
        mock_get.return_value = mock_response

        manager = CoordinatesManager(coords_file)

        result = manager.get_or_fetch_coordinates(
            city="Sao Paulo",
            country="Brazil",
            is_international=True
        )

        assert result["lat"] == -23.5505
        assert result["lon"] == -46.6333
        assert result["tz"] == "America/Sao_Paulo"

        # Verify it was cached
        cached = manager.get_international_venue("Sao Paulo", "Brazil")
        assert cached["lat"] == -23.5505

    @patch('coordinates_manager.httpx.get')
    def test_fetch_saves_to_file(self, mock_get, tmp_path):
        """Test that fetched coordinates are saved to file"""
        coords_file = tmp_path / "coordinates.json"
        coords_file.write_text('{"nfl_stadiums": {}, "international_venues": {}}')

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [{
                "latitude": 52.5200,
                "longitude": 13.4050,
                "timezone": "Europe/Berlin",
                "name": "Berlin"
            }]
        }
        mock_get.return_value = mock_response

        manager = CoordinatesManager(coords_file)

        manager.get_or_fetch_coordinates(
            city="Berlin",
            country="Germany",
            is_international=True
        )

        # Read file and verify
        saved_data = json.loads(coords_file.read_text())
        assert "Berlin,Germany" in saved_data["international_venues"]
        assert saved_data["international_venues"]["Berlin,Germany"]["lat"] == 52.5200


class TestFetchCoordinatesFromApi:
    """Test _fetch_coordinates_from_api private method"""

    @patch('coordinates_manager.httpx.get')
    def test_fetch_success(self, mock_get, tmp_path):
        """Test successful API fetch"""
        coords_file = tmp_path / "coordinates.json"
        coords_file.write_text('{"nfl_stadiums": {}, "international_venues": {}}')

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [{
                "latitude": 48.8566,
                "longitude": 2.3522,
                "timezone": "Europe/Paris",
                "name": "Paris"
            }]
        }
        mock_get.return_value = mock_response

        manager = CoordinatesManager(coords_file)
        result = manager._fetch_coordinates_from_api("Paris", "France")

        assert result["lat"] == 48.8566
        assert result["lon"] == 2.3522
        assert result["tz"] == "Europe/Paris"

    @patch('coordinates_manager.httpx.get')
    def test_fetch_api_error(self, mock_get, tmp_path):
        """Test API error handling"""
        coords_file = tmp_path / "coordinates.json"
        coords_file.write_text('{"nfl_stadiums": {}, "international_venues": {}}')

        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        manager = CoordinatesManager(coords_file)
        result = manager._fetch_coordinates_from_api("Paris", "France")

        assert result is None

    @patch('coordinates_manager.httpx.get')
    def test_fetch_no_results(self, mock_get, tmp_path):
        """Test handling of empty results"""
        coords_file = tmp_path / "coordinates.json"
        coords_file.write_text('{"nfl_stadiums": {}, "international_venues": {}}')

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        mock_get.return_value = mock_response

        manager = CoordinatesManager(coords_file)
        result = manager._fetch_coordinates_from_api("Nowhere", "Atlantis")

        assert result is None

    @patch('coordinates_manager.httpx.get')
    def test_fetch_network_error(self, mock_get, tmp_path):
        """Test handling of network errors"""
        coords_file = tmp_path / "coordinates.json"
        coords_file.write_text('{"nfl_stadiums": {}, "international_venues": {}}')

        import httpx
        mock_get.side_effect = httpx.RequestError("Network error")

        manager = CoordinatesManager(coords_file)
        result = manager._fetch_coordinates_from_api("Paris", "France")

        assert result is None

    @patch('coordinates_manager.httpx.get')
    def test_fetch_missing_timezone(self, mock_get, tmp_path):
        """Test handling of missing timezone in response"""
        coords_file = tmp_path / "coordinates.json"
        coords_file.write_text('{"nfl_stadiums": {}, "international_venues": {}}')

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [{
                "latitude": 35.6762,
                "longitude": 139.6503,
                "name": "Tokyo"
                # No timezone field
            }]
        }
        mock_get.return_value = mock_response

        manager = CoordinatesManager(coords_file)
        result = manager._fetch_coordinates_from_api("Tokyo", "Japan")

        assert result["lat"] == 35.6762
        assert result["tz"] == "UTC"  # Default


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_empty_nfl_stadiums(self, tmp_path):
        """Test with empty NFL stadiums"""
        coords_file = tmp_path / "coordinates.json"
        coords_file.write_text('{"nfl_stadiums": {}, "international_venues": {}}')

        manager = CoordinatesManager(coords_file)

        assert manager.get_nfl_stadium("KC") is None

    def test_special_characters_in_city(self, tmp_path):
        """Test city names with special characters"""
        coords_file = tmp_path / "coordinates.json"
        coords_data = {
            "nfl_stadiums": {},
            "international_venues": {
                "São Paulo,Brazil": {"lat": -23.5505, "lon": -46.6333, "tz": "America/Sao_Paulo", "name": "SP Stadium"}
            }
        }
        coords_file.write_text(json.dumps(coords_data, ensure_ascii=False), encoding='utf-8')

        manager = CoordinatesManager(coords_file)

        result = manager.get_international_venue("São Paulo", "Brazil")
        assert result is not None
        assert result["lat"] == -23.5505

    def test_comma_in_key_format(self, tmp_path):
        """Test that city,country key format is consistent"""
        coords_file = tmp_path / "coordinates.json"
        coords_data = {
            "nfl_stadiums": {},
            "international_venues": {
                "London,United Kingdom": {"lat": 51.5, "lon": -0.1, "tz": "Europe/London", "name": "Stadium"}
            }
        }
        coords_file.write_text(json.dumps(coords_data))

        manager = CoordinatesManager(coords_file)

        # Must use exact format
        result = manager.get_international_venue("London", "United Kingdom")
        assert result is not None

    def test_load_and_save_preserve_data(self, tmp_path):
        """Test that load and save preserve all data"""
        coords_file = tmp_path / "coordinates.json"
        original_data = {
            "nfl_stadiums": {
                "KC": {"lat": 39.0489, "lon": -94.4839, "tz": "America/Chicago", "name": "Arrowhead"}
            },
            "international_venues": {
                "London,UK": {"lat": 51.5, "lon": -0.1, "tz": "Europe/London", "name": "Stadium"}
            }
        }
        coords_file.write_text(json.dumps(original_data))

        manager = CoordinatesManager(coords_file)
        manager._save_coordinates()

        # Reload and verify
        saved_data = json.loads(coords_file.read_text())
        assert saved_data["nfl_stadiums"]["KC"]["lat"] == 39.0489
        assert "London,UK" in saved_data["international_venues"]


class TestCountryNormalization:
    """Test country name normalization for geocoding API"""

    def test_england_normalized_to_uk(self, tmp_path):
        """Test that England is normalized to United Kingdom"""
        coords_file = tmp_path / "coordinates.json"
        coords_file.write_text('{"nfl_stadiums": {}, "international_venues": {}}')

        manager = CoordinatesManager(coords_file)

        assert manager.COUNTRY_NORMALIZATION.get("England") == "United Kingdom"

    def test_scotland_normalized_to_uk(self, tmp_path):
        """Test that Scotland is normalized to United Kingdom"""
        coords_file = tmp_path / "coordinates.json"
        coords_file.write_text('{"nfl_stadiums": {}, "international_venues": {}}')

        manager = CoordinatesManager(coords_file)

        assert manager.COUNTRY_NORMALIZATION.get("Scotland") == "United Kingdom"

    def test_usa_not_normalized(self, tmp_path):
        """Test that USA is not in normalization map"""
        coords_file = tmp_path / "coordinates.json"
        coords_file.write_text('{"nfl_stadiums": {}, "international_venues": {}}')

        manager = CoordinatesManager(coords_file)

        assert manager.COUNTRY_NORMALIZATION.get("USA", "USA") == "USA"

    @patch('coordinates_manager.httpx.get')
    def test_fetch_uses_normalized_country(self, mock_get, tmp_path):
        """Test that geocoding API call uses normalized country name"""
        coords_file = tmp_path / "coordinates.json"
        coords_file.write_text('{"nfl_stadiums": {}, "international_venues": {}}')

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [{
                "latitude": 51.5074,
                "longitude": -0.1278,
                "timezone": "Europe/London",
                "name": "London"
            }]
        }
        mock_get.return_value = mock_response

        manager = CoordinatesManager(coords_file)
        result = manager._fetch_coordinates_from_api("London", "England")

        # Verify the API was called with normalized country
        call_args = mock_get.call_args
        params = call_args.kwargs.get('params') or call_args[1].get('params')
        assert "United Kingdom" in params["name"]
        assert "England" not in params["name"]


class TestIntegrationScenarios:
    """Test realistic integration scenarios"""

    def test_workflow_nfl_game(self, tmp_path):
        """Test typical workflow for NFL stadium lookup"""
        coords_file = tmp_path / "coordinates.json"
        coords_data = {
            "nfl_stadiums": {
                "KC": {"lat": 39.0489, "lon": -94.4839, "tz": "America/Chicago", "name": "GEHA Field"},
                "BAL": {"lat": 39.278, "lon": -76.6227, "tz": "America/New_York", "name": "M&T Bank Stadium"}
            },
            "international_venues": {}
        }
        coords_file.write_text(json.dumps(coords_data))

        manager = CoordinatesManager(coords_file)

        # Look up coordinates for home team
        home_coords = manager.get_or_fetch_coordinates(team_abbrev="KC")
        away_coords = manager.get_or_fetch_coordinates(team_abbrev="BAL")

        assert home_coords["lat"] == 39.0489
        assert away_coords["lat"] == 39.278
        assert home_coords["tz"] == "America/Chicago"
        assert away_coords["tz"] == "America/New_York"

    @patch('coordinates_manager.httpx.get')
    def test_workflow_international_game(self, mock_get, tmp_path):
        """Test typical workflow for international game"""
        coords_file = tmp_path / "coordinates.json"
        coords_file.write_text('{"nfl_stadiums": {}, "international_venues": {}}')

        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [{
                "latitude": -23.5505,
                "longitude": -46.6333,
                "timezone": "America/Sao_Paulo",
                "name": "Sao Paulo"
            }]
        }
        mock_get.return_value = mock_response

        manager = CoordinatesManager(coords_file)

        # First lookup - fetches from API
        result1 = manager.get_or_fetch_coordinates(
            city="Sao Paulo",
            country="Brazil",
            is_international=True
        )

        # Second lookup - should use cache
        mock_get.reset_mock()
        result2 = manager.get_or_fetch_coordinates(
            city="Sao Paulo",
            country="Brazil",
            is_international=True
        )

        assert result1["lat"] == result2["lat"]
        mock_get.assert_not_called()  # Second call should use cache

    def test_mixed_stadium_lookups(self, tmp_path):
        """Test looking up multiple stadiums in sequence"""
        coords_file = tmp_path / "coordinates.json"
        teams_data = {
            "nfl_stadiums": {
                "KC": {"lat": 39.0, "lon": -94.0, "tz": "America/Chicago", "name": "A"},
                "SF": {"lat": 37.0, "lon": -122.0, "tz": "America/Los_Angeles", "name": "B"},
                "DAL": {"lat": 32.0, "lon": -97.0, "tz": "America/Chicago", "name": "C"},
            },
            "international_venues": {}
        }
        coords_file.write_text(json.dumps(teams_data))

        manager = CoordinatesManager(coords_file)

        results = {}
        for team in ["KC", "SF", "DAL", "XXX"]:
            results[team] = manager.get_nfl_stadium(team)

        assert results["KC"] is not None
        assert results["SF"] is not None
        assert results["DAL"] is not None
        assert results["XXX"] is None
