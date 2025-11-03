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
    config.max_positions = {'QB': 2, 'RB': 4, 'WR': 4, 'FLEX': 2, 'TE': 1, 'K': 1, 'DST': 1}
    config.max_players = 15
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

    def test_init_raises_error_if_file_not_found(self, tmp_path, mock_config):
        """Test that __init__ raises FileNotFoundError if file doesn't exist."""
        # Create empty data folder without players_projected.csv
        empty_data_folder = tmp_path / "empty_data"
        empty_data_folder.mkdir()

        with pytest.raises(FileNotFoundError, match="Projected points file not found"):
            ProjectedPointsManager(mock_config, empty_data_folder)


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


class TestEdgeCases:
    """Test suite for edge cases and boundary conditions."""

    @patch('league_helper.util.ProjectedPointsManager.Path')
    @patch('league_helper.util.ProjectedPointsManager.pd.read_csv')
    def test_get_projected_points_week_zero(
        self, mock_read_csv, mock_path, mock_config, mock_player, sample_projected_data
    ):
        """Test getting projected points for week 0 (invalid)."""
        mock_path.return_value.exists.return_value = True
        mock_read_csv.return_value = sample_projected_data

        manager = ProjectedPointsManager(mock_config)
        projected = manager.get_projected_points(mock_player, 0)

        # Week 0 doesn't exist - should return None
        assert projected is None

    @patch('league_helper.util.ProjectedPointsManager.Path')
    @patch('league_helper.util.ProjectedPointsManager.pd.read_csv')
    def test_get_projected_points_week_negative(
        self, mock_read_csv, mock_path, mock_config, mock_player, sample_projected_data
    ):
        """Test getting projected points for negative week."""
        mock_path.return_value.exists.return_value = True
        mock_read_csv.return_value = sample_projected_data

        manager = ProjectedPointsManager(mock_config)
        projected = manager.get_projected_points(mock_player, -1)

        # Negative week doesn't exist - should return None
        assert projected is None

    @patch('league_helper.util.ProjectedPointsManager.Path')
    @patch('league_helper.util.ProjectedPointsManager.pd.read_csv')
    def test_get_projected_points_week_beyond_17(
        self, mock_read_csv, mock_path, mock_config, mock_player, sample_projected_data
    ):
        """Test getting projected points for week > 17."""
        mock_path.return_value.exists.return_value = True
        mock_read_csv.return_value = sample_projected_data

        manager = ProjectedPointsManager(mock_config)
        projected = manager.get_projected_points(mock_player, 18)

        # Week 18 data doesn't exist in sample - should return None
        assert projected is None

    @patch('league_helper.util.ProjectedPointsManager.Path')
    @patch('league_helper.util.ProjectedPointsManager.pd.read_csv')
    def test_get_projected_points_player_with_special_characters(
        self, mock_read_csv, mock_path, mock_config, sample_projected_data
    ):
        """Test getting projected points for player with special characters in name."""
        mock_path.return_value.exists.return_value = True
        mock_read_csv.return_value = sample_projected_data

        manager = ProjectedPointsManager(mock_config)

        # Player name has hyphen and apostrophe in sample data
        special_player = Mock()
        special_player.name = "Amon-Ra St. Brown"

        projected = manager.get_projected_points(special_player, 1)

        # Should find match despite special characters
        assert projected == 17.2

    @patch('league_helper.util.ProjectedPointsManager.Path')
    @patch('league_helper.util.ProjectedPointsManager.pd.read_csv')
    def test_get_projected_points_player_with_whitespace(
        self, mock_read_csv, mock_path, mock_config, sample_projected_data
    ):
        """Test that player name matching handles leading/trailing whitespace."""
        mock_path.return_value.exists.return_value = True
        mock_read_csv.return_value = sample_projected_data

        manager = ProjectedPointsManager(mock_config)

        whitespace_player = Mock()
        whitespace_player.name = "  Saquon Barkley  "

        projected = manager.get_projected_points(whitespace_player, 1)

        # Should match despite whitespace
        assert projected == 18.4

    @patch('league_helper.util.ProjectedPointsManager.Path')
    @patch('league_helper.util.ProjectedPointsManager.pd.read_csv')
    def test_get_projected_points_array_reversed_range(
        self, mock_read_csv, mock_path, mock_config, mock_player, sample_projected_data
    ):
        """Test get_projected_points_array with start > end (reversed range)."""
        mock_path.return_value.exists.return_value = True
        mock_read_csv.return_value = sample_projected_data

        manager = ProjectedPointsManager(mock_config)
        projected_array = manager.get_projected_points_array(mock_player, 5, 3)

        # Reversed range should return empty list
        assert projected_array == []

    @patch('league_helper.util.ProjectedPointsManager.Path')
    @patch('league_helper.util.ProjectedPointsManager.pd.read_csv')
    def test_get_projected_points_array_full_season(
        self, mock_read_csv, mock_path, mock_config, mock_player, sample_projected_data
    ):
        """Test get_projected_points_array for entire season (weeks 1-17)."""
        mock_path.return_value.exists.return_value = True

        # Extend sample data to have weeks 8-17
        for week in range(8, 18):
            sample_projected_data[f'week_{week}_points'] = [15.0 + week, 14.0 + week, 16.0 + week]

        mock_read_csv.return_value = sample_projected_data

        manager = ProjectedPointsManager(mock_config)
        projected_array = manager.get_projected_points_array(mock_player, 1, 17)

        # Should return 17 weeks of data
        assert len(projected_array) == 17
        assert projected_array[0] == 18.4  # Week 1
        assert projected_array[6] == 20.2  # Week 7
        assert projected_array[16] == 32.0  # Week 17

    @patch('league_helper.util.ProjectedPointsManager.Path')
    @patch('league_helper.util.ProjectedPointsManager.pd.read_csv')
    def test_get_historical_projected_points_week_18(
        self, mock_read_csv, mock_path, mock_config, mock_player, sample_projected_data
    ):
        """Test get_historical_projected_points at week 18 (end of season)."""
        mock_path.return_value.exists.return_value = True

        # Extend sample data to have weeks 8-17
        for week in range(8, 18):
            sample_projected_data[f'week_{week}_points'] = [15.0 + week, 14.0 + week, 16.0 + week]

        mock_read_csv.return_value = sample_projected_data
        mock_config.current_nfl_week = 18

        manager = ProjectedPointsManager(mock_config)
        historical = manager.get_historical_projected_points(mock_player)

        # Should return weeks 1-17 (all historical data)
        assert len(historical) == 17
        assert historical[0] == 18.4  # Week 1
        assert historical[16] == 32.0  # Week 17

    @patch('league_helper.util.ProjectedPointsManager.Path')
    @patch('league_helper.util.ProjectedPointsManager.pd.read_csv')
    def test_get_projected_points_array_with_partial_nans(
        self, mock_read_csv, mock_path, mock_config, mock_player, sample_projected_data
    ):
        """Test get_projected_points_array when some weeks have NaN values."""
        mock_path.return_value.exists.return_value = True

        # Add some NaN values
        sample_projected_data.loc[0, 'week_2_points'] = pd.NA
        sample_projected_data.loc[0, 'week_4_points'] = pd.NA

        mock_read_csv.return_value = sample_projected_data

        manager = ProjectedPointsManager(mock_config)
        projected_array = manager.get_projected_points_array(mock_player, 1, 5)

        # Should have None for NaN weeks
        assert len(projected_array) == 5
        assert projected_array[0] == 18.4  # Week 1
        assert projected_array[1] is None  # Week 2 (NaN)
        assert projected_array[2] == 19.3  # Week 3
        assert projected_array[3] is None  # Week 4 (NaN)
        assert projected_array[4] == 18.0  # Week 5
