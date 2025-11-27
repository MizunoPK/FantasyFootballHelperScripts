"""
Unit tests for game_data_models module

Tests Pydantic models, validation, and data conversion methods.

Author: Kai Mizuno
"""

import pytest
from pydantic import ValidationError
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent / "player-data-fetcher"))

from game_data_models import GameData, GAME_DATA_CSV_COLUMNS


class TestGameDataInitialization:
    """Test GameData model initialization"""

    def test_init_with_required_fields(self):
        """Test initialization with all required fields"""
        game = GameData(
            week=1,
            home_team="KC",
            away_team="BAL",
            indoor=False,
            city="Kansas City",
            date="2024-09-05T00:20Z"
        )

        assert game.week == 1
        assert game.home_team == "KC"
        assert game.away_team == "BAL"
        assert game.indoor is False
        assert game.city == "Kansas City"
        assert game.date == "2024-09-05T00:20Z"

    def test_init_with_all_fields(self):
        """Test initialization with all fields"""
        game = GameData(
            week=1,
            home_team="KC",
            away_team="BAL",
            temperature=76,
            gust=10,
            precipitation=0.0,
            home_team_score=27,
            away_team_score=20,
            indoor=False,
            neutral_site=False,
            country="USA",
            city="Kansas City",
            state="MO",
            date="2024-09-05T00:20Z"
        )

        assert game.temperature == 76
        assert game.gust == 10
        assert game.precipitation == 0.0
        assert game.home_team_score == 27
        assert game.away_team_score == 20
        assert game.neutral_site is False
        assert game.country == "USA"
        assert game.state == "MO"

    def test_init_default_values(self):
        """Test default values for optional fields"""
        game = GameData(
            week=1,
            home_team="KC",
            away_team="BAL",
            indoor=False,
            city="Kansas City",
            date="2024-09-05T00:20Z"
        )

        assert game.temperature is None
        assert game.gust is None
        assert game.precipitation is None
        assert game.home_team_score is None
        assert game.away_team_score is None
        assert game.neutral_site is False
        assert game.country == "USA"
        assert game.state is None

    def test_init_indoor_game_no_weather(self):
        """Test indoor game with no weather data"""
        game = GameData(
            week=5,
            home_team="DAL",
            away_team="NYG",
            temperature=None,
            gust=None,
            precipitation=None,
            indoor=True,
            city="Arlington",
            state="TX",
            date="2024-10-01T12:00Z"
        )

        assert game.indoor is True
        assert game.temperature is None
        assert game.gust is None
        assert game.precipitation is None


class TestGameDataValidation:
    """Test Pydantic validation"""

    def test_validates_week_range_min(self):
        """Test that week >= 1 is required"""
        with pytest.raises(ValidationError):
            GameData(
                week=0,
                home_team="KC",
                away_team="BAL",
                indoor=False,
                city="Kansas City",
                date="2024-09-05T00:20Z"
            )

    def test_validates_week_range_max(self):
        """Test that week <= 18 is required"""
        with pytest.raises(ValidationError):
            GameData(
                week=19,
                home_team="KC",
                away_team="BAL",
                indoor=False,
                city="Kansas City",
                date="2024-09-05T00:20Z"
            )

    def test_validates_week_boundary_1(self):
        """Test week 1 is valid"""
        game = GameData(
            week=1,
            home_team="KC",
            away_team="BAL",
            indoor=False,
            city="Kansas City",
            date="2024-09-05T00:20Z"
        )
        assert game.week == 1

    def test_validates_week_boundary_18(self):
        """Test week 18 is valid"""
        game = GameData(
            week=18,
            home_team="KC",
            away_team="BAL",
            indoor=False,
            city="Kansas City",
            date="2025-01-05T12:00Z"
        )
        assert game.week == 18

    def test_validates_home_team_min_length(self):
        """Test home_team minimum length"""
        with pytest.raises(ValidationError):
            GameData(
                week=1,
                home_team="K",  # Too short
                away_team="BAL",
                indoor=False,
                city="Kansas City",
                date="2024-09-05T00:20Z"
            )

    def test_validates_home_team_max_length(self):
        """Test home_team maximum length"""
        with pytest.raises(ValidationError):
            GameData(
                week=1,
                home_team="KCMO",  # Too long
                away_team="BAL",
                indoor=False,
                city="Kansas City",
                date="2024-09-05T00:20Z"
            )

    def test_validates_team_abbreviation_length_2(self):
        """Test 2-character team abbreviation is valid"""
        game = GameData(
            week=1,
            home_team="KC",
            away_team="SF",
            indoor=False,
            city="Kansas City",
            date="2024-09-05T00:20Z"
        )
        assert game.home_team == "KC"
        assert game.away_team == "SF"

    def test_validates_team_abbreviation_length_3(self):
        """Test 3-character team abbreviation is valid"""
        game = GameData(
            week=1,
            home_team="BAL",
            away_team="WSH",
            indoor=False,
            city="Baltimore",
            date="2024-09-05T00:20Z"
        )
        assert game.home_team == "BAL"
        assert game.away_team == "WSH"

    def test_validates_score_non_negative(self):
        """Test that scores must be non-negative"""
        with pytest.raises(ValidationError):
            GameData(
                week=1,
                home_team="KC",
                away_team="BAL",
                home_team_score=-1,
                indoor=False,
                city="Kansas City",
                date="2024-09-05T00:20Z"
            )

    def test_validates_score_zero_is_valid(self):
        """Test that zero score is valid"""
        game = GameData(
            week=1,
            home_team="KC",
            away_team="BAL",
            home_team_score=0,
            away_team_score=0,
            indoor=False,
            city="Kansas City",
            date="2024-09-05T00:20Z"
        )
        assert game.home_team_score == 0
        assert game.away_team_score == 0


class TestGameDataToCsvRow:
    """Test to_csv_row method"""

    def test_to_csv_row_full_data(self):
        """Test CSV row conversion with all fields"""
        game = GameData(
            week=1,
            home_team="KC",
            away_team="BAL",
            temperature=76,
            gust=10,
            precipitation=0.0,
            home_team_score=27,
            away_team_score=20,
            indoor=False,
            neutral_site=False,
            country="USA",
            city="Kansas City",
            state="MO",
            date="2024-09-05T00:20Z"
        )

        row = game.to_csv_row()

        assert row["week"] == 1
        assert row["home_team"] == "KC"
        assert row["away_team"] == "BAL"
        assert row["temperature"] == 76
        assert row["gust"] == 10
        assert row["precipitation"] == 0.0
        assert row["home_team_score"] == 27
        assert row["away_team_score"] == 20
        assert row["indoor"] is False
        assert row["neutral_site"] is False
        assert row["country"] == "USA"
        assert row["city"] == "Kansas City"
        assert row["state"] == "MO"
        assert row["date"] == "2024-09-05T00:20Z"

    def test_to_csv_row_none_values_empty_string(self):
        """Test that None values become empty strings"""
        game = GameData(
            week=1,
            home_team="KC",
            away_team="BAL",
            temperature=None,
            gust=None,
            precipitation=None,
            home_team_score=None,
            away_team_score=None,
            indoor=True,
            city="Arlington",
            state=None,
            date="2024-09-05T00:20Z"
        )

        row = game.to_csv_row()

        assert row["temperature"] == ""
        assert row["gust"] == ""
        assert row["precipitation"] == ""
        assert row["home_team_score"] == ""
        assert row["away_team_score"] == ""
        assert row["state"] == ""

    def test_to_csv_row_international_game(self):
        """Test CSV row for international game"""
        game = GameData(
            week=5,
            home_team="MIA",
            away_team="JAX",
            temperature=72,
            gust=5,
            precipitation=0.1,
            indoor=False,
            neutral_site=True,
            country="Brazil",
            city="Sao Paulo",
            state=None,
            date="2024-10-05T18:00Z"
        )

        row = game.to_csv_row()

        assert row["neutral_site"] is True
        assert row["country"] == "Brazil"
        assert row["city"] == "Sao Paulo"
        assert row["state"] == ""


class TestGameDataFromEspnData:
    """Test from_espn_data class method"""

    def test_from_espn_data_completed_game(self):
        """Test creating GameData from ESPN API response for completed game"""
        espn_event = {
            "date": "2024-09-05T00:20Z",
            "competitions": [{
                "venue": {
                    "indoor": False,
                    "address": {
                        "city": "Kansas City",
                        "state": "MO",
                        "country": "USA"
                    }
                },
                "neutralSite": False,
                "status": {
                    "type": {"completed": True}
                },
                "competitors": [
                    {
                        "homeAway": "home",
                        "team": {"abbreviation": "KC"},
                        "score": "27"
                    },
                    {
                        "homeAway": "away",
                        "team": {"abbreviation": "BAL"},
                        "score": "20"
                    }
                ]
            }]
        }

        weather = {"temperature": 76, "gust": 10, "precipitation": 0.0}

        game = GameData.from_espn_data(1, espn_event, weather)

        assert game.week == 1
        assert game.home_team == "KC"
        assert game.away_team == "BAL"
        assert game.home_team_score == 27
        assert game.away_team_score == 20
        assert game.indoor is False
        assert game.city == "Kansas City"
        assert game.state == "MO"
        assert game.country == "USA"
        assert game.temperature == 76
        assert game.gust == 10
        assert game.precipitation == 0.0

    def test_from_espn_data_future_game(self):
        """Test creating GameData from ESPN API response for future game"""
        espn_event = {
            "date": "2024-12-05T00:00Z",
            "competitions": [{
                "venue": {
                    "indoor": True,
                    "address": {
                        "city": "Arlington",
                        "state": "TX",
                        "country": "USA"
                    }
                },
                "neutralSite": False,
                "status": {
                    "type": {"completed": False}
                },
                "competitors": [
                    {
                        "homeAway": "home",
                        "team": {"abbreviation": "DAL"}
                    },
                    {
                        "homeAway": "away",
                        "team": {"abbreviation": "NYG"}
                    }
                ]
            }]
        }

        game = GameData.from_espn_data(13, espn_event, None)

        assert game.week == 13
        assert game.home_team == "DAL"
        assert game.away_team == "NYG"
        assert game.home_team_score is None
        assert game.away_team_score is None
        assert game.indoor is True
        assert game.temperature is None

    def test_from_espn_data_indoor_no_weather(self):
        """Test that indoor games have no weather data even if provided"""
        espn_event = {
            "date": "2024-10-05T12:00Z",
            "competitions": [{
                "venue": {
                    "indoor": True,
                    "address": {
                        "city": "Las Vegas",
                        "state": "NV",
                        "country": "USA"
                    }
                },
                "neutralSite": False,
                "status": {
                    "type": {"completed": True}
                },
                "competitors": [
                    {
                        "homeAway": "home",
                        "team": {"abbreviation": "LV"},
                        "score": "21"
                    },
                    {
                        "homeAway": "away",
                        "team": {"abbreviation": "DEN"},
                        "score": "17"
                    }
                ]
            }]
        }

        # Weather provided but should be ignored for indoor
        weather = {"temperature": 95, "gust": 15, "precipitation": 0.0}

        game = GameData.from_espn_data(5, espn_event, weather)

        assert game.indoor is True
        assert game.temperature is None
        assert game.gust is None
        assert game.precipitation is None

    def test_from_espn_data_was_to_wsh_mapping(self):
        """Test that WAS team abbreviation is mapped to WSH"""
        espn_event = {
            "date": "2024-09-08T12:00Z",
            "competitions": [{
                "venue": {
                    "indoor": False,
                    "address": {
                        "city": "Landover",
                        "state": "MD",
                        "country": "USA"
                    }
                },
                "neutralSite": False,
                "status": {
                    "type": {"completed": True}
                },
                "competitors": [
                    {
                        "homeAway": "home",
                        "team": {"abbreviation": "WAS"},  # Old abbreviation
                        "score": "24"
                    },
                    {
                        "homeAway": "away",
                        "team": {"abbreviation": "NYG"},
                        "score": "17"
                    }
                ]
            }]
        }

        game = GameData.from_espn_data(1, espn_event, None)

        assert game.home_team == "WSH"  # Should be mapped
        assert game.away_team == "NYG"

    def test_from_espn_data_international_game(self):
        """Test creating GameData for international game"""
        espn_event = {
            "date": "2024-09-06T18:00Z",
            "competitions": [{
                "venue": {
                    "indoor": False,
                    "address": {
                        "city": "Sao Paulo",
                        "country": "Brazil"
                    }
                },
                "neutralSite": True,
                "status": {
                    "type": {"completed": True}
                },
                "competitors": [
                    {
                        "homeAway": "home",
                        "team": {"abbreviation": "MIA"},
                        "score": "20"
                    },
                    {
                        "homeAway": "away",
                        "team": {"abbreviation": "JAX"},
                        "score": "17"
                    }
                ]
            }]
        }

        weather = {"temperature": 72, "gust": 5, "precipitation": 0.0}

        game = GameData.from_espn_data(1, espn_event, weather)

        assert game.neutral_site is True
        assert game.country == "Brazil"
        assert game.city == "Sao Paulo"
        assert game.state is None


class TestGameDataCsvColumns:
    """Test GAME_DATA_CSV_COLUMNS constant"""

    def test_csv_columns_count(self):
        """Test correct number of columns"""
        assert len(GAME_DATA_CSV_COLUMNS) == 14

    def test_csv_columns_required_present(self):
        """Test all required columns are present"""
        required = [
            "week", "home_team", "away_team",
            "temperature", "gust", "precipitation",
            "home_team_score", "away_team_score",
            "indoor", "neutral_site",
            "country", "city", "state", "date"
        ]
        for col in required:
            assert col in GAME_DATA_CSV_COLUMNS

    def test_csv_columns_order(self):
        """Test column order matches expected"""
        expected_order = [
            "week", "home_team", "away_team",
            "temperature", "gust", "precipitation",
            "home_team_score", "away_team_score",
            "indoor", "neutral_site",
            "country", "city", "state", "date"
        ]
        assert GAME_DATA_CSV_COLUMNS == expected_order


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_high_score_game(self):
        """Test game with high scores"""
        game = GameData(
            week=10,
            home_team="KC",
            away_team="BUF",
            home_team_score=70,
            away_team_score=63,
            indoor=False,
            city="Kansas City",
            date="2024-11-05T00:00Z"
        )
        assert game.home_team_score == 70
        assert game.away_team_score == 63

    def test_extreme_weather(self):
        """Test extreme weather values"""
        game = GameData(
            week=17,
            home_team="GB",
            away_team="MIN",
            temperature=-10,
            gust=45,
            precipitation=2.5,
            indoor=False,
            city="Green Bay",
            state="WI",
            date="2024-12-29T12:00Z"
        )
        assert game.temperature == -10
        assert game.gust == 45
        assert game.precipitation == 2.5

    def test_zero_precipitation(self):
        """Test zero precipitation"""
        game = GameData(
            week=3,
            home_team="LA",
            away_team="SF",
            temperature=75,
            gust=5,
            precipitation=0.0,
            indoor=False,
            city="Inglewood",
            date="2024-09-22T16:00Z"
        )
        assert game.precipitation == 0.0

    def test_empty_city_name(self):
        """Test handling of edge case with minimal city"""
        game = GameData(
            week=1,
            home_team="KC",
            away_team="BAL",
            indoor=False,
            city="A",  # Single character city
            date="2024-09-05T00:20Z"
        )
        assert game.city == "A"


class TestIntegrationScenarios:
    """Test realistic integration scenarios"""

    def test_full_week_of_games(self):
        """Test creating multiple games for a full week"""
        games = []
        matchups = [
            ("KC", "BAL"), ("SF", "NYJ"), ("DAL", "PHI"),
            ("GB", "CHI"), ("BUF", "MIA")
        ]

        for i, (home, away) in enumerate(matchups):
            game = GameData(
                week=1,
                home_team=home,
                away_team=away,
                home_team_score=21 + i * 3,
                away_team_score=17 + i * 2,
                indoor=(home in ["DAL"]),  # Only DAL is indoor
                city=f"City{i}",
                date=f"2024-09-08T{12 + i}:00Z"
            )
            games.append(game)

        assert len(games) == 5
        assert all(g.week == 1 for g in games)

    def test_convert_and_back(self):
        """Test round-trip conversion to CSV row and validation"""
        original = GameData(
            week=5,
            home_team="KC",
            away_team="BAL",
            temperature=65,
            gust=12,
            precipitation=0.05,
            home_team_score=31,
            away_team_score=24,
            indoor=False,
            neutral_site=False,
            country="USA",
            city="Kansas City",
            state="MO",
            date="2024-10-08T00:20Z"
        )

        row = original.to_csv_row()

        # Create new GameData from row
        reconstructed = GameData(
            week=row["week"],
            home_team=row["home_team"],
            away_team=row["away_team"],
            temperature=row["temperature"] if row["temperature"] != "" else None,
            gust=row["gust"] if row["gust"] != "" else None,
            precipitation=row["precipitation"] if row["precipitation"] != "" else None,
            home_team_score=row["home_team_score"] if row["home_team_score"] != "" else None,
            away_team_score=row["away_team_score"] if row["away_team_score"] != "" else None,
            indoor=row["indoor"],
            neutral_site=row["neutral_site"],
            country=row["country"],
            city=row["city"],
            state=row["state"] if row["state"] != "" else None,
            date=row["date"]
        )

        assert original.week == reconstructed.week
        assert original.home_team == reconstructed.home_team
        assert original.temperature == reconstructed.temperature
        assert original.home_team_score == reconstructed.home_team_score
