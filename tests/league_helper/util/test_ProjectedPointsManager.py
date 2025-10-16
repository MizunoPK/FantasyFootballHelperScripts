"""
Unit tests for ProjectedPointsManager.
"""

import pytest
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from league_helper.util.ProjectedPointsManager import ProjectedPointsManager


@pytest.fixture
def mock_config():
    """Create a mock ConfigManager."""
    config = Mock()
    config.current_nfl_week = 7
    return config


@pytest.fixture
def mock_player():
    """Create a mock FantasyPlayer."""
    player = Mock()
    player.name = "Saquon Barkley"
    player.id = "3929630"
    return player


@pytest.fixture
def sample_projected_data():
    """Create sample projected points data."""
    data = {
        'id': ['3929630', '4374302', '4429795'],
        'name': ['Saquon Barkley', 'Amon-Ra St. Brown', 'Jahmyr Gibbs'],
        'week_1_points': [18.4, 17.2, 18.4],
        'week_2_points': [18.0, 13.8, 16.6],
        'week_3_points': [19.3, 13.3, 17.0],
        'week_4_points': [18.2, 13.6, 18.1],
        'week_5_points': [18.0, 17.7, 22.1],
        'week_6_points': [17.7, 18.3, 18.4],
        'week_7_points': [20.2, 17.8, 19.9],
    }
    return pd.DataFrame(data)


class TestProjectedPointsManagerInit:
    """Test ProjectedPointsManager initialization."""

    @patch('league_helper.util.ProjectedPointsManager.Path')
    @patch('league_helper.util.ProjectedPointsManager.pd.read_csv')
    def test_init_loads_data(self, mock_read_csv, mock_path, mock_config, sample_projected_data):
        """Test that __init__ loads projected data."""
        mock_path.return_value.exists.return_value = True
        mock_read_csv.return_value = sample_projected_data

        manager = ProjectedPointsManager(mock_config)

        assert manager.projected_data is not None
        assert 'name_lower' in manager.projected_data.columns
        mock_read_csv.assert_called_once()

    @patch('league_helper.util.ProjectedPointsManager.Path')
    def test_init_raises_error_if_file_not_found(self, mock_path, mock_config):
        """Test that __init__ raises FileNotFoundError if file doesn't exist."""
        mock_path.return_value.exists.return_value = False

        with pytest.raises(FileNotFoundError, match="Projected points file not found"):
            ProjectedPointsManager(mock_config)


class TestGetProjectedPoints:
    """Test get_projected_points method."""

    @patch('league_helper.util.ProjectedPointsManager.Path')
    @patch('league_helper.util.ProjectedPointsManager.pd.read_csv')
    def test_get_projected_points_returns_correct_value(
        self, mock_read_csv, mock_path, mock_config, mock_player, sample_projected_data
    ):
        """Test getting projected points for a specific week."""
        mock_path.return_value.exists.return_value = True
        mock_read_csv.return_value = sample_projected_data

        manager = ProjectedPointsManager(mock_config)
        projected = manager.get_projected_points(mock_player, 1)

        assert projected == 18.4

    @patch('league_helper.util.ProjectedPointsManager.Path')
    @patch('league_helper.util.ProjectedPointsManager.pd.read_csv')
    def test_get_projected_points_different_weeks(
        self, mock_read_csv, mock_path, mock_config, mock_player, sample_projected_data
    ):
        """Test getting projected points for different weeks."""
        mock_path.return_value.exists.return_value = True
        mock_read_csv.return_value = sample_projected_data

        manager = ProjectedPointsManager(mock_config)

        assert manager.get_projected_points(mock_player, 1) == 18.4
        assert manager.get_projected_points(mock_player, 2) == 18.0
        assert manager.get_projected_points(mock_player, 3) == 19.3

    @patch('league_helper.util.ProjectedPointsManager.Path')
    @patch('league_helper.util.ProjectedPointsManager.pd.read_csv')
    def test_get_projected_points_player_not_found(
        self, mock_read_csv, mock_path, mock_config, sample_projected_data
    ):
        """Test getting projected points for non-existent player."""
        mock_path.return_value.exists.return_value = True
        mock_read_csv.return_value = sample_projected_data

        manager = ProjectedPointsManager(mock_config)

        unknown_player = Mock()
        unknown_player.name = "Unknown Player"

        projected = manager.get_projected_points(unknown_player, 1)
        assert projected is None

    @patch('league_helper.util.ProjectedPointsManager.Path')
    @patch('league_helper.util.ProjectedPointsManager.pd.read_csv')
    def test_get_projected_points_handles_case_insensitive(
        self, mock_read_csv, mock_path, mock_config, sample_projected_data
    ):
        """Test that player name matching is case-insensitive."""
        mock_path.return_value.exists.return_value = True
        mock_read_csv.return_value = sample_projected_data

        manager = ProjectedPointsManager(mock_config)

        player_lowercase = Mock()
        player_lowercase.name = "saquon barkley"

        player_uppercase = Mock()
        player_uppercase.name = "SAQUON BARKLEY"

        assert manager.get_projected_points(player_lowercase, 1) == 18.4
        assert manager.get_projected_points(player_uppercase, 1) == 18.4

    @patch('league_helper.util.ProjectedPointsManager.Path')
    @patch('league_helper.util.ProjectedPointsManager.pd.read_csv')
    def test_get_projected_points_handles_nan(
        self, mock_read_csv, mock_path, mock_config, sample_projected_data
    ):
        """Test that NaN values are handled correctly."""
        mock_path.return_value.exists.return_value = True

        # Add NaN value
        sample_projected_data.loc[0, 'week_7_points'] = pd.NA
        mock_read_csv.return_value = sample_projected_data

        manager = ProjectedPointsManager(mock_config)
        projected = manager.get_projected_points(mock_player, 7)

        assert projected is None


class TestGetProjectedPointsArray:
    """Test get_projected_points_array method."""

    @patch('league_helper.util.ProjectedPointsManager.Path')
    @patch('league_helper.util.ProjectedPointsManager.pd.read_csv')
    def test_get_projected_points_array_returns_list(
        self, mock_read_csv, mock_path, mock_config, mock_player, sample_projected_data
    ):
        """Test getting array of projected points."""
        mock_path.return_value.exists.return_value = True
        mock_read_csv.return_value = sample_projected_data

        manager = ProjectedPointsManager(mock_config)
        projected_array = manager.get_projected_points_array(mock_player, 1, 3)

        assert isinstance(projected_array, list)
        assert len(projected_array) == 3
        assert projected_array == [18.4, 18.0, 19.3]

    @patch('league_helper.util.ProjectedPointsManager.Path')
    @patch('league_helper.util.ProjectedPointsManager.pd.read_csv')
    def test_get_projected_points_array_single_week(
        self, mock_read_csv, mock_path, mock_config, mock_player, sample_projected_data
    ):
        """Test getting array for a single week."""
        mock_path.return_value.exists.return_value = True
        mock_read_csv.return_value = sample_projected_data

        manager = ProjectedPointsManager(mock_config)
        projected_array = manager.get_projected_points_array(mock_player, 2, 2)

        assert len(projected_array) == 1
        assert projected_array == [18.0]

    @patch('league_helper.util.ProjectedPointsManager.Path')
    @patch('league_helper.util.ProjectedPointsManager.pd.read_csv')
    def test_get_projected_points_array_with_missing_data(
        self, mock_read_csv, mock_path, mock_config, sample_projected_data
    ):
        """Test getting array when some weeks have no data."""
        mock_path.return_value.exists.return_value = True
        mock_read_csv.return_value = sample_projected_data

        manager = ProjectedPointsManager(mock_config)

        unknown_player = Mock()
        unknown_player.name = "Unknown Player"

        projected_array = manager.get_projected_points_array(unknown_player, 1, 3)

        assert len(projected_array) == 3
        assert all(p is None for p in projected_array)


class TestGetHistoricalProjectedPoints:
    """Test get_historical_projected_points method."""

    @patch('league_helper.util.ProjectedPointsManager.Path')
    @patch('league_helper.util.ProjectedPointsManager.pd.read_csv')
    def test_get_historical_projected_points_returns_correct_range(
        self, mock_read_csv, mock_path, mock_config, mock_player, sample_projected_data
    ):
        """Test getting historical projected points up to current week - 1."""
        mock_path.return_value.exists.return_value = True
        mock_read_csv.return_value = sample_projected_data
        mock_config.current_nfl_week = 7

        manager = ProjectedPointsManager(mock_config)
        historical = manager.get_historical_projected_points(mock_player)

        # Should return weeks 1-6 (current week is 7)
        assert len(historical) == 6
        assert historical == [18.4, 18.0, 19.3, 18.2, 18.0, 17.7]

    @patch('league_helper.util.ProjectedPointsManager.Path')
    @patch('league_helper.util.ProjectedPointsManager.pd.read_csv')
    def test_get_historical_projected_points_week_1_returns_empty(
        self, mock_read_csv, mock_path, mock_config, mock_player, sample_projected_data
    ):
        """Test that week 1 returns empty list (no historical data yet)."""
        mock_path.return_value.exists.return_value = True
        mock_read_csv.return_value = sample_projected_data
        mock_config.current_nfl_week = 1

        manager = ProjectedPointsManager(mock_config)
        historical = manager.get_historical_projected_points(mock_player)

        assert historical == []

    @patch('league_helper.util.ProjectedPointsManager.Path')
    @patch('league_helper.util.ProjectedPointsManager.pd.read_csv')
    def test_get_historical_projected_points_week_2_returns_week_1(
        self, mock_read_csv, mock_path, mock_config, mock_player, sample_projected_data
    ):
        """Test that week 2 returns only week 1 data."""
        mock_path.return_value.exists.return_value = True
        mock_read_csv.return_value = sample_projected_data
        mock_config.current_nfl_week = 2

        manager = ProjectedPointsManager(mock_config)
        historical = manager.get_historical_projected_points(mock_player)

        assert len(historical) == 1
        assert historical == [18.4]
