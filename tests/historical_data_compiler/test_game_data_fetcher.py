#!/usr/bin/env python3
"""
Tests for historical_data_compiler/game_data_fetcher.py

Tests game data fetching and CSV output.
"""

import csv
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from historical_data_compiler.game_data_fetcher import (
    GameData,
    GameDataFetcher,
    GAME_DATA_CSV_COLUMNS,
)


class TestGameData:
    """Tests for GameData dataclass"""

    def test_create_game_data(self):
        """Should create GameData with required fields"""
        game = GameData(
            week=1,
            home_team="KC",
            away_team="DEN",
            temperature=75,
            gust=10,
            precipitation=0.0,
            home_team_score=27,
            away_team_score=20,
            indoor=False,
            neutral_site=False,
            country="USA",
            city="Kansas City",
            state="MO",
            date="2024-09-08T13:00Z"
        )

        assert game.week == 1
        assert game.home_team == "KC"
        assert game.away_team == "DEN"
        assert game.temperature == 75
        assert game.indoor is False

    def test_indoor_game_no_weather(self):
        """Indoor game should have None weather values"""
        game = GameData(
            week=1,
            home_team="LV",
            away_team="KC",
            temperature=None,
            gust=None,
            precipitation=None,
            home_team_score=17,
            away_team_score=28,
            indoor=True,
            neutral_site=False,
            country="USA",
            city="Las Vegas",
            state="NV",
            date="2024-09-08T16:25Z"
        )

        assert game.indoor is True
        assert game.temperature is None
        assert game.gust is None
        assert game.precipitation is None

    def test_to_csv_row(self):
        """to_csv_row should return dict with all fields"""
        game = GameData(
            week=1,
            home_team="KC",
            away_team="DEN",
            temperature=75,
            gust=10,
            precipitation=0.5,
            home_team_score=27,
            away_team_score=20,
            indoor=False,
            neutral_site=False,
            country="USA",
            city="Kansas City",
            state="MO",
            date="2024-09-08T13:00Z"
        )

        row = game.to_csv_row()

        assert row['week'] == 1
        assert row['home_team'] == 'KC'
        assert row['temperature'] == 75
        assert row['indoor'] is False

    def test_to_csv_row_none_values(self):
        """None values should become empty strings in CSV"""
        game = GameData(
            week=1,
            home_team="LV",
            away_team="KC",
            temperature=None,
            gust=None,
            precipitation=None,
            home_team_score=None,  # Future game
            away_team_score=None,
            indoor=True,
            neutral_site=False,
            country="USA",
            city="Las Vegas",
            state="NV",
            date="2024-09-08T16:25Z"
        )

        row = game.to_csv_row()

        assert row['temperature'] == ''
        assert row['gust'] == ''
        assert row['home_team_score'] == ''

    def test_international_game(self):
        """International game should have state=None"""
        game = GameData(
            week=5,
            home_team="JAX",
            away_team="BUF",
            temperature=65,
            gust=5,
            precipitation=0.0,
            home_team_score=20,
            away_team_score=24,
            indoor=False,
            neutral_site=True,
            country="England",
            city="London",
            state=None,
            date="2024-10-13T09:30Z"
        )

        row = game.to_csv_row()

        assert row['neutral_site'] is True
        assert row['country'] == 'England'
        assert row['state'] == ''


class TestGameDataCSVColumns:
    """Tests for CSV column definitions"""

    def test_required_columns(self):
        """All required columns should be present"""
        required = [
            "week", "home_team", "away_team",
            "temperature", "gust", "precipitation",
            "home_team_score", "away_team_score",
            "indoor", "neutral_site",
            "country", "city", "state", "date"
        ]
        for col in required:
            assert col in GAME_DATA_CSV_COLUMNS

    def test_column_count(self):
        """Should have 14 columns"""
        assert len(GAME_DATA_CSV_COLUMNS) == 14


class TestGameDataFetcher:
    """Tests for GameDataFetcher class"""

    def test_initialization(self):
        """Fetcher should initialize with HTTP client"""
        mock_client = Mock()
        fetcher = GameDataFetcher(mock_client)

        assert fetcher.http_client == mock_client
        assert hasattr(fetcher, 'logger')
        assert hasattr(fetcher, 'coordinates')

    def test_coordinates_loaded(self):
        """Should load coordinates from JSON file"""
        mock_client = Mock()
        fetcher = GameDataFetcher(mock_client)

        # Should have loaded NFL stadiums
        assert 'nfl_stadiums' in fetcher.coordinates
        assert 'KC' in fetcher.coordinates['nfl_stadiums']


class TestWriteGameDataCSV:
    """Tests for writing game data CSV"""

    def test_write_game_data_csv(self, tmp_path):
        """Should write game data CSV correctly"""
        mock_client = Mock()
        fetcher = GameDataFetcher(mock_client)

        games = [
            GameData(
                week=2,
                home_team="KC",
                away_team="DEN",
                temperature=75,
                gust=10,
                precipitation=0.0,
                home_team_score=27,
                away_team_score=20,
                indoor=False,
                neutral_site=False,
                country="USA",
                city="Kansas City",
                state="MO",
                date="2024-09-15T13:00Z"
            ),
            GameData(
                week=1,
                home_team="BAL",
                away_team="NYG",
                temperature=80,
                gust=5,
                precipitation=0.0,
                home_team_score=34,
                away_team_score=17,
                indoor=False,
                neutral_site=False,
                country="USA",
                city="Baltimore",
                state="MD",
                date="2024-09-08T13:00Z"
            ),
        ]

        output_path = tmp_path / "game_data.csv"
        fetcher.write_game_data_csv(games, output_path)

        assert output_path.exists()

        # Verify contents
        with open(output_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        assert len(rows) == 2
        assert rows[0]['home_team'] == 'BAL'  # Week 1 comes first (sorted by week then date)
        assert rows[1]['home_team'] == 'KC'   # Week 2


class TestGetCoordinates:
    """Tests for coordinate lookup"""

    def test_get_nfl_stadium_coordinates(self):
        """Should return coordinates for NFL stadiums"""
        mock_client = Mock()
        fetcher = GameDataFetcher(mock_client)

        coords = fetcher._get_coordinates('KC', '', '', False)

        assert coords is not None
        assert 'lat' in coords
        assert 'lon' in coords

    def test_get_international_coordinates(self):
        """Should return coordinates for international venues"""
        mock_client = Mock()
        fetcher = GameDataFetcher(mock_client)

        coords = fetcher._get_coordinates('JAX', 'London', 'England', True)

        # Should find London coordinates
        assert coords is not None

    def test_unknown_venue_returns_none(self):
        """Should return None for unknown venues"""
        mock_client = Mock()
        fetcher = GameDataFetcher(mock_client)

        coords = fetcher._get_coordinates('UNKNOWN', 'Unknown City', 'Unknown Country', True)

        assert coords is None
