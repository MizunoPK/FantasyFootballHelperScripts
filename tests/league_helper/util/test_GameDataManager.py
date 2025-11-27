"""
Unit tests for GameDataManager.

Tests the loading and retrieval of game condition data
(temperature, wind, location) from game_data.csv.

Author: Kai Mizuno
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
import tempfile
import csv

import sys
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent.parent / "league_helper"))
sys.path.append(str(Path(__file__).parent.parent.parent.parent / "league_helper" / "util"))

from league_helper.util.GameDataManager import GameDataManager
from league_helper.util.upcoming_game_model import UpcomingGame


class TestGameDataManagerInitialization:
    """Tests for GameDataManager initialization."""

    @pytest.fixture
    def temp_data_folder(self, tmp_path):
        """Create a temp folder for tests."""
        return tmp_path

    @pytest.fixture
    def sample_game_data_csv(self, temp_data_folder):
        """Create a sample game_data.csv file."""
        csv_content = [
            {'week': '1', 'home_team': 'KC', 'away_team': 'BAL',
             'temperature': '75', 'gust': '10', 'indoor': 'False',
             'neutral_site': 'False', 'country': 'USA'},
            {'week': '1', 'home_team': 'PHI', 'away_team': 'NYG',
             'temperature': '80', 'gust': '5', 'indoor': 'False',
             'neutral_site': 'False', 'country': 'USA'},
            {'week': '2', 'home_team': 'KC', 'away_team': 'CIN',
             'temperature': '70', 'gust': '15', 'indoor': 'False',
             'neutral_site': 'False', 'country': 'USA'},
            {'week': '2', 'home_team': 'PHI', 'away_team': 'GB',
             'temperature': '', 'gust': '', 'indoor': 'True',
             'neutral_site': 'False', 'country': 'USA'},
        ]

        csv_path = temp_data_folder / 'game_data.csv'
        with open(csv_path, 'w', newline='') as f:
            fieldnames = ['week', 'home_team', 'away_team', 'temperature',
                         'gust', 'indoor', 'neutral_site', 'country']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_content)

        return csv_path

    def test_init_with_game_data_file(self, temp_data_folder, sample_game_data_csv):
        """Test initialization with game_data.csv present."""
        manager = GameDataManager(temp_data_folder, current_week=1)

        assert manager.has_game_data() is True
        assert len(manager.all_games) == 2  # 2 weeks of data
        assert len(manager.games_by_team) == 4  # 4 teams in week 1

    def test_init_without_game_data_file(self, temp_data_folder):
        """Test initialization without game_data.csv (graceful degradation)."""
        manager = GameDataManager(temp_data_folder, current_week=1)

        assert manager.has_game_data() is False
        assert len(manager.all_games) == 0
        assert len(manager.games_by_team) == 0

    def test_init_without_current_week(self, temp_data_folder, sample_game_data_csv):
        """Test initialization without specifying current_week."""
        manager = GameDataManager(temp_data_folder)

        assert manager.has_game_data() is True
        assert len(manager.all_games) == 2
        assert len(manager.games_by_team) == 0  # No current week set


class TestGameDataManagerGetGame:
    """Tests for get_game method."""

    @pytest.fixture
    def manager_with_data(self, tmp_path):
        """Create a manager with sample data."""
        csv_content = [
            {'week': '5', 'home_team': 'KC', 'away_team': 'BAL',
             'temperature': '60', 'gust': '20', 'indoor': 'False',
             'neutral_site': 'False', 'country': 'USA'},
            {'week': '5', 'home_team': 'DAL', 'away_team': 'NYG',
             'temperature': '', 'gust': '', 'indoor': 'True',
             'neutral_site': 'False', 'country': 'USA'},
            {'week': '6', 'home_team': 'KC', 'away_team': 'MIA',
             'temperature': '55', 'gust': '10', 'indoor': 'False',
             'neutral_site': 'False', 'country': 'USA'},
        ]

        csv_path = tmp_path / 'game_data.csv'
        with open(csv_path, 'w', newline='') as f:
            fieldnames = ['week', 'home_team', 'away_team', 'temperature',
                         'gust', 'indoor', 'neutral_site', 'country']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_content)

        return GameDataManager(tmp_path, current_week=5)

    def test_get_game_home_team(self, manager_with_data):
        """Test getting game for home team."""
        game = manager_with_data.get_game('KC')

        assert game is not None
        assert game.home_team == 'KC'
        assert game.away_team == 'BAL'
        assert game.temperature == 60
        assert game.wind_gust == 20

    def test_get_game_away_team(self, manager_with_data):
        """Test getting game for away team."""
        game = manager_with_data.get_game('BAL')

        assert game is not None
        assert game.home_team == 'KC'
        assert game.away_team == 'BAL'

    def test_get_game_indoor_stadium(self, manager_with_data):
        """Test getting game for indoor stadium."""
        game = manager_with_data.get_game('DAL')

        assert game is not None
        assert game.indoor is True
        assert game.temperature is None
        assert game.wind_gust is None

    def test_get_game_with_explicit_week(self, manager_with_data):
        """Test getting game with explicit week parameter."""
        game = manager_with_data.get_game('KC', week=6)

        assert game is not None
        assert game.away_team == 'MIA'  # Week 6 opponent
        assert game.temperature == 55

    def test_get_game_bye_week(self, manager_with_data):
        """Test getting game for team on bye week."""
        game = manager_with_data.get_game('GB')  # GB not playing in week 5

        assert game is None

    def test_get_game_case_insensitive(self, manager_with_data):
        """Test team lookup is case insensitive."""
        game = manager_with_data.get_game('kc')

        assert game is not None
        assert game.home_team == 'KC'

    def test_get_game_without_week_or_current_week(self, tmp_path):
        """Test get_game when no week is specified and no current_week set."""
        csv_path = tmp_path / 'game_data.csv'
        with open(csv_path, 'w', newline='') as f:
            f.write('week,home_team,away_team,temperature,gust,indoor,neutral_site,country\n')
            f.write('1,KC,BAL,70,10,False,False,USA\n')

        manager = GameDataManager(tmp_path)  # No current_week

        game = manager.get_game('KC')  # No week parameter
        assert game is None  # Should return None with warning


class TestGameDataManagerSetCurrentWeek:
    """Tests for set_current_week method."""

    @pytest.fixture
    def manager_with_multiweek_data(self, tmp_path):
        """Create manager with multiple weeks of data."""
        csv_content = [
            {'week': '1', 'home_team': 'KC', 'away_team': 'BAL',
             'temperature': '75', 'gust': '10', 'indoor': 'False',
             'neutral_site': 'False', 'country': 'USA'},
            {'week': '2', 'home_team': 'KC', 'away_team': 'CIN',
             'temperature': '65', 'gust': '15', 'indoor': 'False',
             'neutral_site': 'False', 'country': 'USA'},
            {'week': '3', 'home_team': 'KC', 'away_team': 'DEN',
             'temperature': '50', 'gust': '25', 'indoor': 'False',
             'neutral_site': 'False', 'country': 'USA'},
        ]

        csv_path = tmp_path / 'game_data.csv'
        with open(csv_path, 'w', newline='') as f:
            fieldnames = ['week', 'home_team', 'away_team', 'temperature',
                         'gust', 'indoor', 'neutral_site', 'country']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_content)

        return GameDataManager(tmp_path, current_week=1)

    def test_set_current_week_updates_games_by_team(self, manager_with_multiweek_data):
        """Test that set_current_week updates games_by_team index."""
        manager = manager_with_multiweek_data

        # Initially week 1
        game = manager.get_game('KC')
        assert game.away_team == 'BAL'

        # Change to week 2
        manager.set_current_week(2)
        game = manager.get_game('KC')
        assert game.away_team == 'CIN'

        # Change to week 3
        manager.set_current_week(3)
        game = manager.get_game('KC')
        assert game.away_team == 'DEN'

    def test_set_current_week_nonexistent_week(self, manager_with_multiweek_data):
        """Test set_current_week with week that has no games."""
        manager = manager_with_multiweek_data

        manager.set_current_week(10)  # No games in week 10

        game = manager.get_game('KC')
        assert game is None  # No game found


class TestUpcomingGameModel:
    """Tests for UpcomingGame dataclass."""

    def test_is_home_game_true(self):
        """Test is_home_game returns True for home team."""
        game = UpcomingGame(
            week=1, home_team='KC', away_team='BAL',
            temperature=70, wind_gust=10, indoor=False,
            neutral_site=False, country='USA'
        )

        assert game.is_home_game('KC') is True
        assert game.is_home_game('BAL') is False

    def test_is_home_game_neutral_site(self):
        """Test is_home_game returns False for neutral site games."""
        game = UpcomingGame(
            week=1, home_team='KC', away_team='BAL',
            temperature=70, wind_gust=10, indoor=False,
            neutral_site=True, country='UK'
        )

        # Both teams are "away" at neutral site
        assert game.is_home_game('KC') is False
        assert game.is_home_game('BAL') is False

    def test_is_international(self):
        """Test is_international detection."""
        usa_game = UpcomingGame(
            week=1, home_team='KC', away_team='BAL',
            temperature=70, wind_gust=10, indoor=False,
            neutral_site=False, country='USA'
        )

        uk_game = UpcomingGame(
            week=1, home_team='JAX', away_team='ATL',
            temperature=50, wind_gust=5, indoor=False,
            neutral_site=True, country='UK'
        )

        mexico_game = UpcomingGame(
            week=1, home_team='LAC', away_team='MIA',
            temperature=80, wind_gust=0, indoor=False,
            neutral_site=True, country='Mexico'
        )

        assert usa_game.is_international() is False
        assert uk_game.is_international() is True
        assert mexico_game.is_international() is True

    def test_get_team_opponent(self):
        """Test get_team_opponent returns the opposing team."""
        game = UpcomingGame(
            week=1, home_team='KC', away_team='BAL',
            temperature=70, wind_gust=10, indoor=False,
            neutral_site=False, country='USA'
        )

        assert game.get_team_opponent('KC') == 'BAL'
        assert game.get_team_opponent('BAL') == 'KC'
        assert game.get_team_opponent('PHI') is None  # Not in this game


class TestGameDataParsing:
    """Tests for edge cases in game data parsing."""

    @pytest.fixture
    def create_csv_with_data(self, tmp_path):
        """Factory fixture to create CSV with specific data."""
        def _create(csv_content):
            csv_path = tmp_path / 'game_data.csv'
            with open(csv_path, 'w', newline='') as f:
                f.write(csv_content)
            return GameDataManager(tmp_path, current_week=1)
        return _create

    def test_handles_empty_temperature(self, create_csv_with_data):
        """Test handling of empty temperature values (indoor games)."""
        csv = "week,home_team,away_team,temperature,gust,indoor,neutral_site,country\n"
        csv += "1,DAL,NYG,,5,True,False,USA\n"

        manager = create_csv_with_data(csv)
        game = manager.get_game('DAL')

        assert game.temperature is None
        assert game.indoor is True

    def test_handles_float_temperature(self, create_csv_with_data):
        """Test handling of float temperature values."""
        csv = "week,home_team,away_team,temperature,gust,indoor,neutral_site,country\n"
        csv += "1,KC,BAL,72.5,10.5,False,False,USA\n"

        manager = create_csv_with_data(csv)
        game = manager.get_game('KC')

        assert game.temperature == 72
        assert game.wind_gust == 10

    def test_handles_missing_country_defaults_usa(self, create_csv_with_data):
        """Test that missing country defaults to USA."""
        csv = "week,home_team,away_team,temperature,gust,indoor,neutral_site,country\n"
        csv += "1,KC,BAL,70,10,False,False,\n"

        manager = create_csv_with_data(csv)
        game = manager.get_game('KC')

        assert game.country == 'USA'

    def test_handles_lowercase_team_names(self, create_csv_with_data):
        """Test that lowercase team names are normalized to uppercase."""
        csv = "week,home_team,away_team,temperature,gust,indoor,neutral_site,country\n"
        csv += "1,kc,bal,70,10,False,False,USA\n"

        manager = create_csv_with_data(csv)
        game = manager.get_game('KC')

        assert game is not None
        assert game.home_team == 'KC'
        assert game.away_team == 'BAL'

    def test_handles_whitespace_in_values(self, create_csv_with_data):
        """Test that whitespace in values is trimmed."""
        csv = "week,home_team,away_team,temperature,gust,indoor,neutral_site,country\n"
        csv += "1, KC , BAL ,70,10,False,False, USA \n"

        manager = create_csv_with_data(csv)
        game = manager.get_game('KC')

        assert game is not None
        assert game.home_team == 'KC'
        assert game.country == 'USA'
