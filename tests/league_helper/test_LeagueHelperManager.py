#!/usr/bin/env python3
"""
Tests for LeagueHelperManager

Tests the main orchestrator for the League Helper application,
including initialization, manager coordination, menu routing, and mode delegation.

Author: Kai Mizuno
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, call
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))
from league_helper.LeagueHelperManager import LeagueHelperManager


class TestLeagueHelperManagerInit:
    """Test suite for LeagueHelperManager initialization."""

    @pytest.fixture
    def mock_data_folder(self, tmp_path):
        """Create a mock data folder path."""
        return tmp_path / "data"

    @pytest.fixture
    def mock_managers(self):
        """Create mock manager instances."""
        with patch('league_helper.LeagueHelperManager.ConfigManager') as mock_config, \
             patch('league_helper.LeagueHelperManager.TeamDataManager') as mock_team_data, \
             patch('league_helper.LeagueHelperManager.SeasonScheduleManager') as mock_season_schedule, \
             patch('league_helper.LeagueHelperManager.PlayerManager') as mock_player, \
             patch('league_helper.LeagueHelperManager.AddToRosterModeManager') as mock_add_roster, \
             patch('league_helper.LeagueHelperManager.StarterHelperModeManager') as mock_starter, \
             patch('league_helper.LeagueHelperManager.TradeSimulatorModeManager') as mock_trade, \
             patch('league_helper.LeagueHelperManager.ModifyPlayerDataModeManager') as mock_modify, \
             patch('league_helper.LeagueHelperManager.get_logger') as mock_logger:

            # Setup config mock
            config_instance = Mock()
            config_instance.config_name = "Test League"
            config_instance.current_nfl_week = 5
            mock_config.return_value = config_instance

            # Setup player manager mock
            player_instance = Mock()
            player_instance.players = []
            mock_player.return_value = player_instance

            # Setup logger mock
            logger_instance = Mock()
            mock_logger.return_value = logger_instance

            yield {
                'config': mock_config,
                'team_data': mock_team_data,
                'season_schedule': mock_season_schedule,
                'player': mock_player,
                'add_roster': mock_add_roster,
                'starter': mock_starter,
                'trade': mock_trade,
                'modify': mock_modify,
                'logger': mock_logger,
                'config_instance': config_instance,
                'player_instance': player_instance,
                'logger_instance': logger_instance
            }

    def test_init_creates_config_manager(self, mock_data_folder, mock_managers):
        """Test that initialization creates ConfigManager with correct path."""
        manager = LeagueHelperManager(mock_data_folder)

        mock_managers['config'].assert_called_once_with(mock_data_folder)
        assert manager.config == mock_managers['config_instance']

    def test_init_creates_team_data_manager(self, mock_data_folder, mock_managers):
        """Test that initialization creates TeamDataManager with correct dependencies."""
        manager = LeagueHelperManager(mock_data_folder)

        # TeamDataManager now requires season_schedule_manager and current_nfl_week
        mock_managers['team_data'].assert_called_once_with(
            mock_data_folder,
            mock_managers['season_schedule'].return_value,
            mock_managers['config_instance'].current_nfl_week
        )
        assert manager.team_data_manager is not None

    def test_init_creates_player_manager(self, mock_data_folder, mock_managers):
        """Test that initialization creates PlayerManager with correct dependencies."""
        manager = LeagueHelperManager(mock_data_folder)

        mock_managers['player'].assert_called_once_with(
            mock_data_folder,
            mock_managers['config_instance'],
            mock_managers['team_data'].return_value,
            mock_managers['season_schedule'].return_value
        )
        assert manager.player_manager == mock_managers['player_instance']

    def test_init_creates_all_mode_managers(self, mock_data_folder, mock_managers):
        """Test that initialization creates all four mode managers."""
        manager = LeagueHelperManager(mock_data_folder)

        # Verify Add to Roster mode manager
        mock_managers['add_roster'].assert_called_once_with(
            mock_managers['config_instance'],
            mock_managers['player_instance'],
            mock_managers['team_data'].return_value
        )

        # Verify Starter Helper mode manager
        mock_managers['starter'].assert_called_once_with(
            mock_managers['config_instance'],
            mock_managers['player_instance'],
            mock_managers['team_data'].return_value
        )

        # Verify Trade Simulator mode manager
        mock_managers['trade'].assert_called_once_with(
            mock_data_folder,
            mock_managers['player_instance'],
            mock_managers['config_instance']
        )

        # Verify Modify Player Data mode manager
        mock_managers['modify'].assert_called_once_with(
            mock_managers['player_instance'],
            mock_data_folder
        )

    def test_init_logs_initialization_steps(self, mock_data_folder, mock_managers):
        """Test that initialization logs all major steps."""
        manager = LeagueHelperManager(mock_data_folder)

        logger = mock_managers['logger_instance']

        # Check for key log messages
        assert logger.debug.call_count >= 4  # Multiple debug messages
        assert logger.info.call_count >= 2   # Config loaded, mode managers initialized


class TestStartInteractiveMode:
    """Test suite for start_interactive_mode method."""

    @pytest.fixture
    def mock_manager(self, tmp_path):
        """Create a LeagueHelperManager with mocked dependencies."""
        with patch('league_helper.LeagueHelperManager.ConfigManager'), \
             patch('league_helper.LeagueHelperManager.TeamDataManager'), \
             patch('league_helper.LeagueHelperManager.PlayerManager') as mock_player, \
             patch('league_helper.LeagueHelperManager.AddToRosterModeManager'), \
             patch('league_helper.LeagueHelperManager.StarterHelperModeManager'), \
             patch('league_helper.LeagueHelperManager.TradeSimulatorModeManager'), \
             patch('league_helper.LeagueHelperManager.ModifyPlayerDataModeManager'), \
             patch('league_helper.LeagueHelperManager.get_logger'):

            # Setup player manager mock with proper list for players
            player_instance = Mock()
            player_instance.players = []  # Empty list so len() works
            player_instance.get_roster_len.return_value = 5
            player_instance.display_scored_roster = Mock()
            player_instance.reload_player_data = Mock()
            mock_player.return_value = player_instance

            manager = LeagueHelperManager(tmp_path / "data")
            yield manager

    @patch('league_helper.LeagueHelperManager.show_list_selection')
    @patch('builtins.print')
    def test_start_interactive_mode_displays_welcome(self, mock_print, mock_show_list, mock_manager):
        """Test that start_interactive_mode displays welcome message."""
        # Mock to exit immediately
        mock_show_list.return_value = 5  # Quit option

        mock_manager.start_interactive_mode()

        # Check welcome message
        welcome_calls = [call for call in mock_print.call_args_list
                        if "Welcome to the Start 7 Fantasy League Helper!" in str(call)]
        assert len(welcome_calls) > 0

    @patch('league_helper.LeagueHelperManager.show_list_selection')
    def test_start_interactive_mode_displays_roster_status(self, mock_show_list, mock_manager):
        """Test that start_interactive_mode displays scored roster."""
        # Mock to exit immediately
        mock_show_list.return_value = 5  # Quit option

        mock_manager.start_interactive_mode()

        mock_manager.player_manager.display_scored_roster.assert_called_once()

    @patch('league_helper.LeagueHelperManager.show_list_selection')
    def test_start_interactive_mode_reloads_data_before_menu(self, mock_show_list, mock_manager):
        """Test that player data is reloaded before each menu display."""
        # Mock to show menu twice then quit
        mock_show_list.side_effect = [1, 5]  # Add to roster, then quit

        # Mock the mode method to do nothing
        mock_manager._run_add_to_roster_mode = Mock()

        mock_manager.start_interactive_mode()

        # Should reload before first menu (1 time) and before second menu (1 time) = 2 times
        assert mock_manager.player_manager.reload_player_data.call_count == 2

    @patch('league_helper.LeagueHelperManager.show_list_selection')
    def test_start_interactive_mode_routes_to_add_roster(self, mock_show_list, mock_manager):
        """Test that choice 1 routes to Add to Roster mode."""
        mock_show_list.side_effect = [1, 5]  # Add to roster, then quit
        mock_manager._run_add_to_roster_mode = Mock()

        mock_manager.start_interactive_mode()

        mock_manager._run_add_to_roster_mode.assert_called_once()

    @patch('league_helper.LeagueHelperManager.show_list_selection')
    def test_start_interactive_mode_routes_to_starter_helper(self, mock_show_list, mock_manager):
        """Test that choice 2 routes to Starter Helper mode."""
        mock_show_list.side_effect = [2, 5]  # Starter helper, then quit
        mock_manager._run_starter_helper_mode = Mock()

        mock_manager.start_interactive_mode()

        mock_manager._run_starter_helper_mode.assert_called_once()

    @patch('league_helper.LeagueHelperManager.show_list_selection')
    def test_start_interactive_mode_routes_to_trade_simulator(self, mock_show_list, mock_manager):
        """Test that choice 3 routes to Trade Simulator mode."""
        mock_show_list.side_effect = [3, 5]  # Trade simulator, then quit
        mock_manager._run_trade_simulator_mode = Mock()

        mock_manager.start_interactive_mode()

        mock_manager._run_trade_simulator_mode.assert_called_once()

    @patch('league_helper.LeagueHelperManager.show_list_selection')
    def test_start_interactive_mode_routes_to_modify_player_data(self, mock_show_list, mock_manager):
        """Test that choice 4 routes to Modify Player Data mode."""
        mock_show_list.side_effect = [4, 5]  # Modify player data, then quit
        mock_manager.run_modify_player_data_mode = Mock()

        mock_manager.start_interactive_mode()

        mock_manager.run_modify_player_data_mode.assert_called_once()

    @patch('league_helper.LeagueHelperManager.show_list_selection')
    @patch('builtins.print')
    def test_start_interactive_mode_exits_on_quit(self, mock_print, mock_show_list, mock_manager):
        """Test that choice 5 exits the application."""
        mock_show_list.return_value = 5  # Quit

        mock_manager.start_interactive_mode()

        # Check for goodbye message
        goodbye_calls = [call for call in mock_print.call_args_list
                        if "Goodbye!" in str(call)]
        assert len(goodbye_calls) > 0

    @patch('league_helper.LeagueHelperManager.show_list_selection')
    @patch('builtins.print')
    def test_start_interactive_mode_handles_invalid_choice(self, mock_print, mock_show_list, mock_manager):
        """Test that invalid menu choices are handled gracefully."""
        mock_show_list.side_effect = [99, 5]  # Invalid choice, then quit

        mock_manager.start_interactive_mode()

        # Check for invalid choice message
        invalid_calls = [call for call in mock_print.call_args_list
                        if "Invalid choice" in str(call)]
        assert len(invalid_calls) > 0


class TestModeDelegation:
    """Test suite for mode delegation methods."""

    @pytest.fixture
    def mock_manager(self, tmp_path):
        """Create a LeagueHelperManager with mocked mode managers."""
        with patch('league_helper.LeagueHelperManager.ConfigManager'), \
             patch('league_helper.LeagueHelperManager.TeamDataManager'), \
             patch('league_helper.LeagueHelperManager.PlayerManager'), \
             patch('league_helper.LeagueHelperManager.AddToRosterModeManager') as mock_add, \
             patch('league_helper.LeagueHelperManager.StarterHelperModeManager') as mock_starter, \
             patch('league_helper.LeagueHelperManager.TradeSimulatorModeManager') as mock_trade, \
             patch('league_helper.LeagueHelperManager.ModifyPlayerDataModeManager') as mock_modify, \
             patch('league_helper.LeagueHelperManager.get_logger'):

            manager = LeagueHelperManager(tmp_path / "data")

            # Store mock instances for verification
            manager.add_to_roster_mode_manager.start_interactive_mode = Mock()
            manager.starter_helper_mode_manager.show_recommended_starters = Mock()
            manager.trade_simulator_mode_manager.run_interactive_mode = Mock()
            manager.modify_player_data_mode_manager.start_interactive_mode = Mock()

            yield manager

    def test_run_add_to_roster_mode_delegates_correctly(self, mock_manager):
        """Test that _run_add_to_roster_mode passes correct managers."""
        mock_manager._run_add_to_roster_mode()

        mock_manager.add_to_roster_mode_manager.start_interactive_mode.assert_called_once_with(
            mock_manager.player_manager,
            mock_manager.team_data_manager
        )

    def test_run_starter_helper_mode_delegates_correctly(self, mock_manager):
        """Test that _run_starter_helper_mode passes correct managers."""
        mock_manager._run_starter_helper_mode()

        mock_manager.starter_helper_mode_manager.show_recommended_starters.assert_called_once_with(
            mock_manager.player_manager,
            mock_manager.team_data_manager
        )

    def test_run_trade_simulator_mode_delegates_correctly(self, mock_manager):
        """Test that _run_trade_simulator_mode calls mode manager method."""
        mock_manager._run_trade_simulator_mode()

        mock_manager.trade_simulator_mode_manager.run_interactive_mode.assert_called_once()

    def test_run_modify_player_data_mode_delegates_correctly(self, mock_manager):
        """Test that run_modify_player_data_mode passes player manager."""
        mock_manager.run_modify_player_data_mode()

        mock_manager.modify_player_data_mode_manager.start_interactive_mode.assert_called_once_with(
            mock_manager.player_manager
        )


class TestEdgeCases:
    """Test suite for edge cases and error handling."""

    def test_init_handles_missing_data_folder(self):
        """Test that initialization with missing data folder raises error."""
        with patch('league_helper.LeagueHelperManager.ConfigManager') as mock_config:
            mock_config.side_effect = FileNotFoundError("Data folder not found")

            with pytest.raises(FileNotFoundError):
                LeagueHelperManager(Path("/nonexistent/path"))

    def test_init_handles_invalid_config(self):
        """Test that initialization with invalid config raises error."""
        with patch('league_helper.LeagueHelperManager.ConfigManager') as mock_config:
            mock_config.side_effect = ValueError("Invalid configuration")

            with pytest.raises(ValueError):
                LeagueHelperManager(Path("/some/path"))

    @patch('league_helper.LeagueHelperManager.show_list_selection')
    def test_multiple_mode_executions(self, mock_show_list):
        """Test that multiple modes can be executed in sequence."""
        with patch('league_helper.LeagueHelperManager.ConfigManager'), \
             patch('league_helper.LeagueHelperManager.TeamDataManager'), \
             patch('league_helper.LeagueHelperManager.PlayerManager') as mock_player, \
             patch('league_helper.LeagueHelperManager.AddToRosterModeManager'), \
             patch('league_helper.LeagueHelperManager.StarterHelperModeManager'), \
             patch('league_helper.LeagueHelperManager.TradeSimulatorModeManager'), \
             patch('league_helper.LeagueHelperManager.ModifyPlayerDataModeManager'), \
             patch('league_helper.LeagueHelperManager.get_logger'):

            # Setup player manager mock with proper list for players
            player_instance = Mock()
            player_instance.players = []  # Empty list so len() works
            player_instance.get_roster_len.return_value = 5
            player_instance.display_scored_roster = Mock()
            player_instance.reload_player_data = Mock()
            mock_player.return_value = player_instance

            manager = LeagueHelperManager(Path("/some/path"))

            # Mock mode methods
            manager._run_add_to_roster_mode = Mock()
            manager._run_starter_helper_mode = Mock()
            manager._run_trade_simulator_mode = Mock()
            manager.run_modify_player_data_mode = Mock()

            # Run all modes in sequence, then quit
            mock_show_list.side_effect = [1, 2, 3, 4, 5]

            manager.start_interactive_mode()

            # Verify all modes were called
            manager._run_add_to_roster_mode.assert_called_once()
            manager._run_starter_helper_mode.assert_called_once()
            manager._run_trade_simulator_mode.assert_called_once()
            manager.run_modify_player_data_mode.assert_called_once()

            # Verify data was reloaded before each menu (5 times total)
            assert player_instance.reload_player_data.call_count == 5
