"""
Unit tests for SaveCalculatedPointsManager

Tests the Save Calculated Points mode manager functionality including:
- Initialization
- Weekly and season-long scoring
- JSON output with correct precision
- Idempotent behavior
- File copying logic
- Error handling for missing files
"""

import pytest
import json
from unittest.mock import Mock
from league_helper.save_calculated_points_mode.SaveCalculatedPointsManager import SaveCalculatedPointsManager
from league_helper.util.ConfigManager import ConfigManager
from league_helper.util.PlayerManager import PlayerManager
from utils.FantasyPlayer import FantasyPlayer


class TestSaveCalculatedPointsManager:
    """Test SaveCalculatedPointsManager class"""

    @pytest.fixture
    def mock_config(self):
        """Create mock ConfigManager"""
        config = Mock(spec=ConfigManager)
        config.current_nfl_week = 5
        config.nfl_season = 2024
        return config

    @pytest.fixture
    def mock_player_manager(self):
        """Create mock PlayerManager"""
        pm = Mock(spec=PlayerManager)
        pm.players = []
        return pm

    @pytest.fixture
    def temp_data_folder(self, tmp_path):
        """Create temporary data folder with test files"""
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        (data_folder / "players.csv").write_text("Name,Position,Team\nPlayer1,QB,KC\n")
        (data_folder / "players_projected.csv").write_text("Name,Position\nPlayer1,QB\n")
        (data_folder / "game_data.csv").write_text("Week,Team\n1,KC\n")
        (data_folder / "drafted_data.csv").write_text("Name,Drafted\nPlayer1,0\n")

        configs = data_folder / "configs"
        configs.mkdir()
        (configs / "league_config.json").write_text('{"test": "data"}')

        team_data = data_folder / "team_data"
        team_data.mkdir()
        (team_data / "KC.csv").write_text("Week,Rank\n1,5\n")

        return data_folder

    def test_init_stores_dependencies(self, mock_config, mock_player_manager, temp_data_folder):
        """Test SaveCalculatedPointsManager initialization stores dependencies"""
        manager = SaveCalculatedPointsManager(mock_config, mock_player_manager, temp_data_folder)

        assert manager.config == mock_config
        assert manager.player_manager == mock_player_manager
        assert manager.data_folder == temp_data_folder
        assert manager.logger is not None

    def test_execute_weekly_scoring(self, mock_config, mock_player_manager, temp_data_folder):
        """Test execute() collects weekly projections for week > 0 (UPDATED for Sub-feature 2)"""
        mock_config.current_nfl_week = 5
        mock_config.nfl_season = 2024

        projected = [0.0] * 17
        projected[4] = 25.3
        actual = projected.copy()
        test_player = FantasyPlayer(
            id=1, name="Patrick Mahomes", team="KC", position="QB",
            projected_points=projected, actual_points=actual
        )
        mock_player_manager.players = [test_player]

        manager = SaveCalculatedPointsManager(mock_config, mock_player_manager, temp_data_folder)

        manager.execute()

        json_path = temp_data_folder / "historical_data" / "2024" / "05" / "calculated_projected_points.json"
        assert json_path.exists()

        with open(json_path) as f:
            data = json.load(f)

        assert "1" in data
        assert data["1"] == 25.3

    def test_execute_season_long_scoring(self, mock_config, mock_player_manager, temp_data_folder):
        """Test execute() collects season-long projections for week == 0"""
        mock_config.current_nfl_week = 0
        mock_config.nfl_season = 2024

        test_player = FantasyPlayer(
            id=1, name="Patrick Mahomes", team="KC", position="QB",
            fantasy_points=342.57
        )
        mock_player_manager.players = [test_player]

        manager = SaveCalculatedPointsManager(mock_config, mock_player_manager, temp_data_folder)

        manager.execute()

        json_path = temp_data_folder / "historical_data" / "2024" / "calculated_season_long_projected_points.json"
        assert json_path.exists()

        with open(json_path) as f:
            data = json.load(f)

        assert "1" in data
        assert data["1"] == 342.57

    def test_execute_rounds_to_2_decimals(self, mock_config, mock_player_manager, temp_data_folder):
        """Test execute() rounds projected points to 2 decimal places (UPDATED for Sub-feature 2)"""
        mock_config.current_nfl_week = 1
        mock_config.nfl_season = 2024

        projected = [0.0] * 17
        projected[0] = 26.56789
        actual = projected.copy()
        test_player = FantasyPlayer(
            id=1, name="Patrick Mahomes", team="KC", position="QB",
            projected_points=projected, actual_points=actual
        )
        mock_player_manager.players = [test_player]

        manager = SaveCalculatedPointsManager(mock_config, mock_player_manager, temp_data_folder)

        manager.execute()

        json_path = temp_data_folder / "historical_data" / "2024" / "01" / "calculated_projected_points.json"
        with open(json_path) as f:
            data = json.load(f)

        player_id = "1"
        assert player_id in data
        assert data[player_id] == 26.57

    def test_execute_skips_if_folder_exists(self, mock_config, mock_player_manager, temp_data_folder, capsys):
        """Test execute() skips operation if folder already exists (idempotent) (UPDATED for Sub-feature 2)"""
        mock_config.current_nfl_week = 5
        mock_config.nfl_season = 2024

        output_folder = temp_data_folder / "historical_data" / "2024" / "05"
        output_folder.mkdir(parents=True)

        projected = [0.0] * 17
        projected[4] = 25.0
        actual = projected.copy()
        test_player = FantasyPlayer(
            id=1, name="Player", team="KC", position="QB",
            projected_points=projected, actual_points=actual
        )
        mock_player_manager.players = [test_player]

        manager = SaveCalculatedPointsManager(mock_config, mock_player_manager, temp_data_folder)

        manager.execute()

        json_path = temp_data_folder / "historical_data" / "2024" / "05" / "calculated_projected_points.json"
        assert not json_path.exists()

        captured = capsys.readouterr()
        assert "already exists" in captured.out.lower()

    def test_execute_warns_on_missing_files(self, mock_config, mock_player_manager, temp_data_folder, capsys):
        """Test execute() warns but continues when optional files are missing (UPDATED for Sub-feature 2)"""
        mock_config.current_nfl_week = 1
        mock_config.nfl_season = 2024

        projected = [0.0] * 17
        projected[0] = 24.5
        actual = projected.copy()
        test_player = FantasyPlayer(
            id=1, name="Player", team="KC", position="QB",
            projected_points=projected, actual_points=actual
        )
        mock_player_manager.players = [test_player]

        (temp_data_folder / "game_data.csv").unlink()
        (temp_data_folder / "drafted_data.csv").unlink()

        manager = SaveCalculatedPointsManager(mock_config, mock_player_manager, temp_data_folder)

        manager.execute()

        json_path = temp_data_folder / "historical_data" / "2024" / "01" / "calculated_projected_points.json"
        assert json_path.exists()

        assert not (temp_data_folder / "historical_data" / "2024" / "01" / "players.csv").exists()
        assert not (temp_data_folder / "historical_data" / "2024" / "01" / "players_projected.csv").exists()

    def test_execute_copies_all_4_file_types(self, mock_config, mock_player_manager, temp_data_folder):
        """Test execute() copies all 4 file types to historical_data (UPDATED for feature_02: CSV deprecation)"""
        mock_config.current_nfl_week = 1
        mock_config.nfl_season = 2024

        projected = [0.0] * 17
        projected[0] = 22.3
        actual = projected.copy()
        test_player = FantasyPlayer(
            id=1, name="Player", team="KC", position="QB",
            projected_points=projected, actual_points=actual
        )
        mock_player_manager.players = [test_player]

        manager = SaveCalculatedPointsManager(mock_config, mock_player_manager, temp_data_folder)

        manager.execute()

        output_folder = temp_data_folder / "historical_data" / "2024" / "01"

        assert (output_folder / "game_data.csv").exists()
        assert (output_folder / "drafted_data.csv").exists()
        assert (output_folder / "configs" / "league_config.json").exists()
        assert (output_folder / "team_data" / "KC.csv").exists()

        assert not (output_folder / "players.csv").exists()
        assert not (output_folder / "players_projected.csv").exists()

    def test_execute_creates_correct_folder_structure(self, mock_config, mock_player_manager, temp_data_folder):
        """Test execute() creates correct folder structure (UPDATED for Sub-feature 2)"""
        mock_config.current_nfl_week = 12
        mock_config.nfl_season = 2024

        projected = [0.0] * 17
        projected[11] = 23.8
        actual = projected.copy()
        test_player = FantasyPlayer(
            id=1, name="Player", team="KC", position="QB",
            projected_points=projected, actual_points=actual
        )
        mock_player_manager.players = [test_player]

        manager = SaveCalculatedPointsManager(mock_config, mock_player_manager, temp_data_folder)

        manager.execute()

        assert (temp_data_folder / "historical_data").exists()
        assert (temp_data_folder / "historical_data" / "2024").exists()
        assert (temp_data_folder / "historical_data" / "2024" / "12").exists()
        assert (temp_data_folder / "historical_data" / "2024" / "12" / "calculated_projected_points.json").exists()


