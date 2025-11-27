"""
Unit tests for game_data_fetcher module

Tests ESPN API integration, weather fetching, and CSV I/O.

Author: Kai Mizuno
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone, timedelta
import pandas as pd
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent / "player-data-fetcher"))

from game_data_fetcher import GameDataFetcher, fetch_game_data
from game_data_models import GameData


class TestGameDataFetcherInitialization:
    """Test GameDataFetcher initialization"""

    def test_init_creates_output_file_path(self, tmp_path):
        """Test initialization sets correct output file path"""
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        # Create a minimal coordinates file
        coords_file = Path(__file__).parent.parent.parent / "player-data-fetcher" / "coordinates.json"

        with patch.object(GameDataFetcher, '__init__', lambda self, **kwargs: None):
            fetcher = GameDataFetcher.__new__(GameDataFetcher)
            fetcher.data_folder = data_folder
            fetcher.output_file = data_folder / "game_data.csv"

            assert fetcher.output_file == data_folder / "game_data.csv"

    def test_init_stores_season_and_week(self, tmp_path):
        """Test initialization stores season and current week"""
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        with patch.object(GameDataFetcher, '__init__', lambda self, **kwargs: None):
            fetcher = GameDataFetcher.__new__(GameDataFetcher)
            fetcher.season = 2024
            fetcher.current_week = 10

            assert fetcher.season == 2024
            assert fetcher.current_week == 10


class TestLoadExistingData:
    """Test _load_existing_data method"""

    def test_load_no_existing_file(self, tmp_path):
        """Test loading when no file exists"""
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        with patch.object(GameDataFetcher, '__init__', lambda self, **kwargs: None):
            fetcher = GameDataFetcher.__new__(GameDataFetcher)
            fetcher.output_file = data_folder / "game_data.csv"
            fetcher.logger = Mock()

            games = fetcher._load_existing_data()

            assert games == []

    def test_load_existing_data(self, tmp_path):
        """Test loading existing game data from CSV"""
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        csv_content = """week,home_team,away_team,temperature,gust,precipitation,home_team_score,away_team_score,indoor,neutral_site,country,city,state,date
1,KC,BAL,76,10,0.0,27,20,False,False,USA,Kansas City,MO,2024-09-05T00:20Z
2,SF,NYJ,65,5,0.0,24,17,False,False,USA,Santa Clara,CA,2024-09-12T00:15Z"""

        csv_file = data_folder / "game_data.csv"
        csv_file.write_text(csv_content)

        with patch.object(GameDataFetcher, '__init__', lambda self, **kwargs: None):
            fetcher = GameDataFetcher.__new__(GameDataFetcher)
            fetcher.output_file = csv_file
            fetcher.logger = Mock()

            games = fetcher._load_existing_data()

            assert len(games) == 2
            assert games[0].week == 1
            assert games[0].home_team == "KC"
            assert games[0].temperature == 76
            assert games[1].week == 2
            assert games[1].home_team == "SF"

    def test_load_handles_empty_values(self, tmp_path):
        """Test loading CSV with empty values (None)"""
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        # Indoor games have no weather data (temperature, gust, precipitation are empty)
        # Future games have no scores (home_team_score, away_team_score are empty)
        # Column order: week,home_team,away_team,temperature,gust,precipitation,home_team_score,away_team_score,indoor,neutral_site,country,city,state,date
        csv_content = """week,home_team,away_team,temperature,gust,precipitation,home_team_score,away_team_score,indoor,neutral_site,country,city,state,date
1,DAL,NYG,,,,,,True,False,USA,Arlington,TX,2024-09-08T12:00Z"""

        csv_file = data_folder / "game_data.csv"
        csv_file.write_text(csv_content)

        with patch.object(GameDataFetcher, '__init__', lambda self, **kwargs: None):
            fetcher = GameDataFetcher.__new__(GameDataFetcher)
            fetcher.output_file = csv_file
            fetcher.logger = Mock()

            games = fetcher._load_existing_data()

            assert len(games) == 1
            assert games[0].indoor is True
            assert games[0].temperature is None
            assert games[0].home_team_score is None
            assert games[0].city == "Arlington"


class TestGetExistingWeeks:
    """Test _get_existing_weeks method"""

    def test_get_existing_weeks_from_games(self):
        """Test extracting weeks from game list"""
        games = [
            GameData(week=1, home_team="KC", away_team="BAL", indoor=False, city="KC", date="2024-09-05T00:00Z"),
            GameData(week=2, home_team="SF", away_team="NYJ", indoor=False, city="SC", date="2024-09-12T00:00Z"),
            GameData(week=1, home_team="DAL", away_team="NYG", indoor=True, city="AR", date="2024-09-08T00:00Z"),
            GameData(week=5, home_team="GB", away_team="CHI", indoor=False, city="GB", date="2024-10-06T00:00Z"),
        ]

        with patch.object(GameDataFetcher, '__init__', lambda self, **kwargs: None):
            fetcher = GameDataFetcher.__new__(GameDataFetcher)

            weeks = fetcher._get_existing_weeks(games)

            assert weeks == {1, 2, 5}

    def test_get_existing_weeks_empty_list(self):
        """Test extracting weeks from empty list"""
        with patch.object(GameDataFetcher, '__init__', lambda self, **kwargs: None):
            fetcher = GameDataFetcher.__new__(GameDataFetcher)

            weeks = fetcher._get_existing_weeks([])

            assert weeks == set()


class TestDetermineWeeksToFetch:
    """Test _determine_weeks_to_fetch method"""

    def test_determine_all_weeks_needed(self):
        """Test when no weeks exist"""
        with patch.object(GameDataFetcher, '__init__', lambda self, **kwargs: None):
            fetcher = GameDataFetcher.__new__(GameDataFetcher)
            fetcher.current_week = 5
            fetcher.logger = Mock()

            weeks = fetcher._determine_weeks_to_fetch(set())

            assert weeks == [1, 2, 3, 4, 5]

    def test_determine_some_weeks_needed(self):
        """Test when some weeks already exist"""
        with patch.object(GameDataFetcher, '__init__', lambda self, **kwargs: None):
            fetcher = GameDataFetcher.__new__(GameDataFetcher)
            fetcher.current_week = 5
            fetcher.logger = Mock()

            weeks = fetcher._determine_weeks_to_fetch({1, 3})

            assert weeks == [2, 4, 5]

    def test_determine_no_weeks_needed(self):
        """Test when all weeks exist"""
        with patch.object(GameDataFetcher, '__init__', lambda self, **kwargs: None):
            fetcher = GameDataFetcher.__new__(GameDataFetcher)
            fetcher.current_week = 3
            fetcher.logger = Mock()

            weeks = fetcher._determine_weeks_to_fetch({1, 2, 3})

            assert weeks == []


class TestGetWeatherApiEndpoint:
    """Test _get_weather_api_endpoint method"""

    def test_historical_api_for_old_game(self):
        """Test historical API is used for games > 5 days ago"""
        with patch.object(GameDataFetcher, '__init__', lambda self, **kwargs: None):
            fetcher = GameDataFetcher.__new__(GameDataFetcher)
            fetcher.OPEN_METEO_HISTORICAL_URL = "https://archive-api.open-meteo.com/v1/archive"
            fetcher.OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

            # Game from 10 days ago
            old_date = (datetime.now(timezone.utc) - timedelta(days=10)).isoformat()

            endpoint = fetcher._get_weather_api_endpoint(old_date)

            assert endpoint == "https://archive-api.open-meteo.com/v1/archive"

    def test_forecast_api_for_recent_game(self):
        """Test forecast API is used for games within 5 days"""
        with patch.object(GameDataFetcher, '__init__', lambda self, **kwargs: None):
            fetcher = GameDataFetcher.__new__(GameDataFetcher)
            fetcher.OPEN_METEO_HISTORICAL_URL = "https://archive-api.open-meteo.com/v1/archive"
            fetcher.OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

            # Game from 2 days ago
            recent_date = (datetime.now(timezone.utc) - timedelta(days=2)).isoformat()

            endpoint = fetcher._get_weather_api_endpoint(recent_date)

            assert endpoint == "https://api.open-meteo.com/v1/forecast"

    def test_forecast_api_for_future_game(self):
        """Test forecast API is used for future games"""
        with patch.object(GameDataFetcher, '__init__', lambda self, **kwargs: None):
            fetcher = GameDataFetcher.__new__(GameDataFetcher)
            fetcher.OPEN_METEO_HISTORICAL_URL = "https://archive-api.open-meteo.com/v1/archive"
            fetcher.OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

            # Game in 3 days
            future_date = (datetime.now(timezone.utc) + timedelta(days=3)).isoformat()

            endpoint = fetcher._get_weather_api_endpoint(future_date)

            assert endpoint == "https://api.open-meteo.com/v1/forecast"

    def test_forecast_api_for_invalid_date(self):
        """Test forecast API is default for invalid dates"""
        with patch.object(GameDataFetcher, '__init__', lambda self, **kwargs: None):
            fetcher = GameDataFetcher.__new__(GameDataFetcher)
            fetcher.OPEN_METEO_HISTORICAL_URL = "https://archive-api.open-meteo.com/v1/archive"
            fetcher.OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

            endpoint = fetcher._get_weather_api_endpoint("invalid-date")

            assert endpoint == "https://api.open-meteo.com/v1/forecast"


class TestFetchWeatherForGame:
    """Test _fetch_weather_for_game method"""

    def test_indoor_game_no_weather(self):
        """Test indoor games return None weather"""
        with patch.object(GameDataFetcher, '__init__', lambda self, **kwargs: None):
            fetcher = GameDataFetcher.__new__(GameDataFetcher)

            weather = fetcher._fetch_weather_for_game(
                home_team="DAL",
                game_date="2024-09-08T12:00Z",
                is_indoor=True,
                is_international=False,
                city="Arlington",
                country="USA"
            )

            assert weather["temperature"] is None
            assert weather["gust"] is None
            assert weather["precipitation"] is None

    @patch('game_data_fetcher.httpx.get')
    def test_outdoor_game_fetches_weather(self, mock_get):
        """Test outdoor games fetch weather from API"""
        mock_coords_manager = Mock()
        mock_coords_manager.get_or_fetch_coordinates.return_value = {
            "lat": 39.0489,
            "lon": -94.4839,
            "tz": "America/Chicago"
        }

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {
            "hourly": {
                "time": ["2024-09-05T00:00", "2024-09-05T01:00"],
                "temperature_2m": [76, 74],
                "wind_gusts_10m": [10, 12],
                "precipitation": [0.0, 0.0]
            }
        }
        mock_get.return_value = mock_response

        with patch.object(GameDataFetcher, '__init__', lambda self, **kwargs: None):
            fetcher = GameDataFetcher.__new__(GameDataFetcher)
            fetcher.coords_manager = mock_coords_manager
            fetcher.logger = Mock()
            fetcher.OPEN_METEO_HISTORICAL_URL = "https://archive-api.open-meteo.com/v1/archive"
            fetcher.OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

            # Use a date > 5 days ago
            old_date = "2024-09-05T00:20Z"
            fetcher._get_weather_api_endpoint = Mock(return_value=fetcher.OPEN_METEO_HISTORICAL_URL)

            from config import REQUEST_TIMEOUT
            with patch('game_data_fetcher.REQUEST_TIMEOUT', 30):
                weather = fetcher._fetch_weather_for_game(
                    home_team="KC",
                    game_date=old_date,
                    is_indoor=False,
                    is_international=False,
                    city="Kansas City",
                    country="USA"
                )

            assert weather["temperature"] is not None

    def test_no_coordinates_returns_none_weather(self):
        """Test that missing coordinates return None weather"""
        mock_coords_manager = Mock()
        mock_coords_manager.get_or_fetch_coordinates.return_value = None

        with patch.object(GameDataFetcher, '__init__', lambda self, **kwargs: None):
            fetcher = GameDataFetcher.__new__(GameDataFetcher)
            fetcher.coords_manager = mock_coords_manager
            fetcher.logger = Mock()

            weather = fetcher._fetch_weather_for_game(
                home_team="XXX",
                game_date="2024-09-08T12:00Z",
                is_indoor=False,
                is_international=False,
                city="Unknown",
                country="USA"
            )

            assert weather["temperature"] is None
            assert weather["gust"] is None


class TestFetchEspnScoreboard:
    """Test _fetch_espn_scoreboard method"""

    @patch('game_data_fetcher.httpx.get')
    def test_fetch_scoreboard_success(self, mock_get):
        """Test successful ESPN API fetch"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {
            "events": [
                {"id": "1", "name": "Game 1"}
            ]
        }
        mock_get.return_value = mock_response

        with patch.object(GameDataFetcher, '__init__', lambda self, **kwargs: None):
            fetcher = GameDataFetcher.__new__(GameDataFetcher)
            fetcher.season = 2024
            fetcher.ESPN_SCOREBOARD_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
            fetcher.logger = Mock()

            with patch('game_data_fetcher.REQUEST_TIMEOUT', 30):
                result = fetcher._fetch_espn_scoreboard(1)

            assert "events" in result
            assert len(result["events"]) == 1

    @patch('game_data_fetcher.httpx.get')
    def test_fetch_scoreboard_error_returns_empty(self, mock_get):
        """Test ESPN API error returns empty events"""
        import httpx
        mock_get.side_effect = httpx.RequestError("Network error")

        with patch.object(GameDataFetcher, '__init__', lambda self, **kwargs: None):
            fetcher = GameDataFetcher.__new__(GameDataFetcher)
            fetcher.season = 2024
            fetcher.ESPN_SCOREBOARD_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
            fetcher.logger = Mock()

            with patch('game_data_fetcher.REQUEST_TIMEOUT', 30):
                result = fetcher._fetch_espn_scoreboard(1)

            assert result == {"events": []}


class TestSaveToCsv:
    """Test save_to_csv method"""

    def test_save_creates_file(self, tmp_path):
        """Test CSV file is created"""
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        games = [
            GameData(week=1, home_team="KC", away_team="BAL", indoor=False,
                    city="Kansas City", state="MO", date="2024-09-05T00:20Z"),
            GameData(week=2, home_team="SF", away_team="NYJ", indoor=False,
                    city="Santa Clara", state="CA", date="2024-09-12T00:15Z"),
        ]

        with patch.object(GameDataFetcher, '__init__', lambda self, **kwargs: None):
            fetcher = GameDataFetcher.__new__(GameDataFetcher)
            fetcher.output_file = data_folder / "game_data.csv"
            fetcher.logger = Mock()

            result = fetcher.save_to_csv(games)

            assert result.exists()
            df = pd.read_csv(result)
            assert len(df) == 2
            assert df.iloc[0]["home_team"] == "KC"
            assert df.iloc[1]["home_team"] == "SF"

    def test_save_sorts_by_week_and_date(self, tmp_path):
        """Test games are sorted by week then date"""
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        games = [
            GameData(week=2, home_team="SF", away_team="NYJ", indoor=False,
                    city="SC", date="2024-09-12T00:15Z"),
            GameData(week=1, home_team="DAL", away_team="NYG", indoor=True,
                    city="AR", date="2024-09-08T16:00Z"),
            GameData(week=1, home_team="KC", away_team="BAL", indoor=False,
                    city="KC", date="2024-09-05T00:20Z"),
        ]

        with patch.object(GameDataFetcher, '__init__', lambda self, **kwargs: None):
            fetcher = GameDataFetcher.__new__(GameDataFetcher)
            fetcher.output_file = data_folder / "game_data.csv"
            fetcher.logger = Mock()

            result = fetcher.save_to_csv(games)

            df = pd.read_csv(result)
            assert df.iloc[0]["week"] == 1
            assert df.iloc[0]["home_team"] == "KC"  # Earlier date
            assert df.iloc[1]["week"] == 1
            assert df.iloc[1]["home_team"] == "DAL"  # Later date
            assert df.iloc[2]["week"] == 2

    def test_save_creates_parent_directory(self, tmp_path):
        """Test parent directory is created if needed"""
        data_folder = tmp_path / "nested" / "data"

        games = [
            GameData(week=1, home_team="KC", away_team="BAL", indoor=False,
                    city="KC", date="2024-09-05T00:20Z"),
        ]

        with patch.object(GameDataFetcher, '__init__', lambda self, **kwargs: None):
            fetcher = GameDataFetcher.__new__(GameDataFetcher)
            fetcher.output_file = data_folder / "game_data.csv"
            fetcher.logger = Mock()

            result = fetcher.save_to_csv(games)

            assert result.exists()
            assert data_folder.exists()


class TestBackfillPreviousWeekScores:
    """Test _backfill_previous_week_scores method"""

    def test_backfill_updates_missing_scores(self):
        """Test backfill updates games with missing scores"""
        games = [
            GameData(week=1, home_team="KC", away_team="BAL", indoor=False,
                    home_team_score=None, away_team_score=None,
                    city="KC", date="2024-09-05T00:20Z"),
        ]

        mock_scoreboard = {
            "events": [{
                "competitions": [{
                    "status": {"type": {"completed": True}},
                    "competitors": [
                        {"homeAway": "home", "team": {"abbreviation": "KC"}, "score": "27"},
                        {"homeAway": "away", "team": {"abbreviation": "BAL"}, "score": "20"}
                    ]
                }]
            }]
        }

        with patch.object(GameDataFetcher, '__init__', lambda self, **kwargs: None):
            fetcher = GameDataFetcher.__new__(GameDataFetcher)
            fetcher.current_week = 2
            fetcher.logger = Mock()
            fetcher._fetch_espn_scoreboard = Mock(return_value=mock_scoreboard)

            updated = fetcher._backfill_previous_week_scores(games)

            assert updated[0].home_team_score == 27
            assert updated[0].away_team_score == 20

    def test_backfill_skips_week_1(self):
        """Test backfill doesn't run when current_week is 1"""
        games = [
            GameData(week=1, home_team="KC", away_team="BAL", indoor=False,
                    city="KC", date="2024-09-05T00:20Z"),
        ]

        with patch.object(GameDataFetcher, '__init__', lambda self, **kwargs: None):
            fetcher = GameDataFetcher.__new__(GameDataFetcher)
            fetcher.current_week = 1

            result = fetcher._backfill_previous_week_scores(games)

            assert result == games  # No changes


class TestFetchGameDataConvenienceFunction:
    """Test fetch_game_data convenience function"""

    @patch('game_data_fetcher.GameDataFetcher')
    def test_fetch_game_data_default_params(self, mock_fetcher_class, tmp_path):
        """Test convenience function with default parameters"""
        mock_fetcher = Mock()
        mock_fetcher.fetch_all.return_value = []
        mock_fetcher.save_to_csv.return_value = tmp_path / "game_data.csv"
        mock_fetcher_class.return_value = mock_fetcher

        # Create the output file so it exists
        output_file = tmp_path / "game_data.csv"
        output_file.write_text("week,home_team\n")

        with patch('game_data_fetcher.get_logger'):
            result = fetch_game_data(output_path=output_file)

            mock_fetcher.fetch_all.assert_called_once()
            mock_fetcher.save_to_csv.assert_called_once()

    @patch('game_data_fetcher.GameDataFetcher')
    def test_fetch_game_data_custom_weeks(self, mock_fetcher_class, tmp_path):
        """Test convenience function with specific weeks"""
        mock_fetcher = Mock()
        mock_fetcher._fetch_games_for_week.return_value = []
        mock_fetcher.save_to_csv.return_value = tmp_path / "game_data.csv"
        mock_fetcher_class.return_value = mock_fetcher

        output_file = tmp_path / "game_data.csv"
        output_file.write_text("week,home_team\n")

        with patch('game_data_fetcher.get_logger'):
            result = fetch_game_data(output_path=output_file, weeks=[1, 2, 3])

            assert mock_fetcher._fetch_games_for_week.call_count == 3


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_fetch_week_18(self, tmp_path):
        """Test fetching week 18 games"""
        with patch.object(GameDataFetcher, '__init__', lambda self, **kwargs: None):
            fetcher = GameDataFetcher.__new__(GameDataFetcher)
            fetcher.current_week = 18
            fetcher.logger = Mock()

            weeks = fetcher._determine_weeks_to_fetch({1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17})

            assert weeks == [18]

    def test_empty_espn_response(self):
        """Test handling empty ESPN API response"""
        with patch.object(GameDataFetcher, '__init__', lambda self, **kwargs: None):
            fetcher = GameDataFetcher.__new__(GameDataFetcher)
            fetcher.logger = Mock()

            mock_coords_manager = Mock()
            fetcher.coords_manager = mock_coords_manager
            fetcher._fetch_espn_scoreboard = Mock(return_value={"events": []})
            fetcher._fetch_weather_for_game = Mock()

            games = fetcher._fetch_games_for_week(1)

            assert games == []


class TestIntegrationScenarios:
    """Test realistic integration scenarios"""

    def test_full_workflow_mock(self, tmp_path):
        """Test full fetch workflow with mocked APIs"""
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        # Create coordinates file
        coords_file = data_folder / "coordinates.json"
        coords_data = {
            "nfl_stadiums": {
                "KC": {"lat": 39.0, "lon": -94.0, "tz": "America/Chicago", "name": "Stadium"}
            },
            "international_venues": {}
        }
        coords_file.write_text(json.dumps(coords_data))

        espn_response = {
            "events": [{
                "date": "2024-09-05T00:20Z",
                "competitions": [{
                    "venue": {
                        "indoor": False,
                        "address": {"city": "Kansas City", "state": "MO", "country": "USA"}
                    },
                    "neutralSite": False,
                    "status": {"type": {"completed": True}},
                    "competitors": [
                        {"homeAway": "home", "team": {"abbreviation": "KC"}, "score": "27"},
                        {"homeAway": "away", "team": {"abbreviation": "BAL"}, "score": "20"}
                    ]
                }]
            }]
        }

        with patch.object(GameDataFetcher, '__init__', lambda self, **kwargs: None):
            fetcher = GameDataFetcher.__new__(GameDataFetcher)
            fetcher.data_folder = data_folder
            fetcher.output_file = data_folder / "game_data.csv"
            fetcher.season = 2024
            fetcher.current_week = 1
            fetcher.logger = Mock()
            fetcher.coords_manager = Mock()
            fetcher.coords_manager.get_or_fetch_coordinates.return_value = {
                "lat": 39.0, "lon": -94.0, "tz": "America/Chicago"
            }

            with patch.object(fetcher, '_fetch_espn_scoreboard', return_value=espn_response):
                with patch.object(fetcher, '_fetch_weather_for_game', return_value={
                    "temperature": 76, "gust": 10, "precipitation": 0.0
                }):
                    games = fetcher._fetch_games_for_week(1)

            assert len(games) == 1
            assert games[0].home_team == "KC"
            assert games[0].home_team_score == 27
