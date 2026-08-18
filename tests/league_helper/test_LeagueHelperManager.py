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
from league_helper import constants
from league_helper.LeagueHelperManager import LeagueHelperManager, main
from utils.LoggingManager import setup_logger


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
             patch('league_helper.LeagueHelperManager.DraftModeManager') as mock_draft, \
             patch('league_helper.LeagueHelperManager.StarterHelperModeManager') as mock_starter, \
             patch('league_helper.LeagueHelperManager.TradeSimulatorModeManager') as mock_trade, \
             patch('league_helper.LeagueHelperManager.ModifyPlayerDataModeManager') as mock_modify, \
             patch('league_helper.LeagueHelperManager.SaveCalculatedPointsManager') as mock_save_points, \
             patch('league_helper.LeagueHelperManager.get_logger') as mock_logger:

            config_instance = Mock()
            config_instance.config_name = "Test League"
            config_instance.current_nfl_week = 5
            mock_config.return_value = config_instance

            player_instance = Mock()
            player_instance.players = []
            mock_player.return_value = player_instance

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
                'save_points': mock_save_points,
                'logger': mock_logger,
                'config_instance': config_instance,
                'player_instance': player_instance,
                'logger_instance': logger_instance
            }

    def test_init_creates_config_managers(self, mock_data_folder, mock_managers):
        """Test that initialization creates ConfigManager with correct path."""
        manager = LeagueHelperManager(mock_data_folder)

        assert mock_managers['config'].call_count == 1
        mock_managers['config'].assert_called_once_with(mock_data_folder)
        assert manager.config == mock_managers['config_instance']

    def test_init_creates_team_data_manager(self, mock_data_folder, mock_managers):
        """Test that initialization creates TeamDataManager with correct dependencies."""
        manager = LeagueHelperManager(mock_data_folder)

        mock_managers['team_data'].assert_called_once_with(
            mock_data_folder,
            mock_managers['config_instance'],
            mock_managers['season_schedule'].return_value,
            mock_managers['config_instance'].current_nfl_week
        )
        assert manager.team_data_manager is not None

    def test_init_creates_player_managers(self, mock_data_folder, mock_managers):
        """Test that initialization creates PlayerManager with correct dependencies."""
        manager = LeagueHelperManager(mock_data_folder)

        assert mock_managers['player'].call_count == 1
        mock_managers['player'].assert_called_once_with(
            mock_data_folder,
            mock_managers['config_instance'],
            mock_managers['team_data'].return_value,
            mock_managers['season_schedule'].return_value
        )
        assert manager.player_manager == mock_managers['player_instance']

    def test_init_creates_all_mode_managers(self, mock_data_folder, mock_managers):
        """Test that initialization creates all five mode managers."""
        manager = LeagueHelperManager(mock_data_folder)

        mock_managers['add_roster'].assert_called_once_with(
            mock_managers['config_instance'],
            mock_managers['player_instance'],
            mock_managers['team_data'].return_value
        )

        mock_managers['starter'].assert_called_once_with(
            mock_managers['config_instance'],
            mock_managers['player_instance'],
            mock_managers['team_data'].return_value
        )

        mock_managers['trade'].assert_called_once_with(
            mock_data_folder,
            mock_managers['player_instance'],
            mock_managers['config_instance']
        )

        mock_managers['modify'].assert_called_once_with(
            mock_managers['player_instance'],
            mock_data_folder
        )

        mock_managers['save_points'].assert_called_once_with(
            mock_managers['config_instance'],
            mock_managers['player_instance'],
            mock_data_folder
        )

    def test_init_logs_initialization_steps(self, mock_data_folder, mock_managers):
        """Test that initialization logs all major steps."""
        manager = LeagueHelperManager(mock_data_folder)

        logger = mock_managers['logger_instance']

        assert logger.debug.call_count >= 2
        assert logger.info.call_count >= 2


class TestStartInteractiveMode:
    """Test suite for start_interactive_mode method."""

    @pytest.fixture
    def mock_manager(self, tmp_path):
        """Create a LeagueHelperManager with mocked dependencies."""
        with patch('league_helper.LeagueHelperManager.ConfigManager'), \
             patch('league_helper.LeagueHelperManager.TeamDataManager'), \
             patch('league_helper.LeagueHelperManager.PlayerManager') as mock_player, \
             patch('league_helper.LeagueHelperManager.DraftModeManager'), \
             patch('league_helper.LeagueHelperManager.StarterHelperModeManager'), \
             patch('league_helper.LeagueHelperManager.TradeSimulatorModeManager'), \
             patch('league_helper.LeagueHelperManager.ModifyPlayerDataModeManager'), \
             patch('league_helper.LeagueHelperManager.SaveCalculatedPointsManager'), \
             patch('league_helper.LeagueHelperManager.get_logger'):

            player_instance = Mock()
            player_instance.players = []
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
        mock_show_list.return_value = 6

        mock_manager.start_interactive_mode()

        welcome_calls = [call for call in mock_print.call_args_list
                        if "Welcome to the Start 7 Fantasy League Helper!" in str(call)]
        assert len(welcome_calls) > 0

    @patch('league_helper.LeagueHelperManager.show_list_selection')
    def test_start_interactive_mode_displays_roster_status(self, mock_show_list, mock_manager):
        """Test that start_interactive_mode displays scored roster."""
        mock_show_list.return_value = 6

        mock_manager.start_interactive_mode()

        mock_manager.player_manager.display_scored_roster.assert_called_once()

    @patch('league_helper.LeagueHelperManager.show_list_selection')
    def test_start_interactive_mode_reloads_data_before_menu(self, mock_show_list, mock_manager):
        """Test that player data is reloaded before each menu display."""
        mock_show_list.side_effect = [1, 6]

        mock_manager._run_draft_mode = Mock()

        mock_manager.start_interactive_mode()

        assert mock_manager.player_manager.reload_player_data.call_count == 2

    @patch('league_helper.LeagueHelperManager.show_list_selection')
    def test_start_interactive_mode_routes_to_add_roster(self, mock_show_list, mock_manager):
        """Test that choice 1 routes to Draft Mode."""
        mock_show_list.side_effect = [1, 6]
        mock_manager._run_draft_mode = Mock()

        mock_manager.start_interactive_mode()

        mock_manager._run_draft_mode.assert_called_once()

    @patch('league_helper.LeagueHelperManager.show_list_selection')
    def test_start_interactive_mode_routes_to_starter_helper(self, mock_show_list, mock_manager):
        """Test that choice 2 routes to Starter Helper mode."""
        mock_show_list.side_effect = [2, 6]
        mock_manager._run_starter_helper_mode = Mock()

        mock_manager.start_interactive_mode()

        mock_manager._run_starter_helper_mode.assert_called_once()

    @patch('league_helper.LeagueHelperManager.show_list_selection')
    def test_start_interactive_mode_routes_to_trade_simulator(self, mock_show_list, mock_manager):
        """Test that choice 3 routes to Trade Simulator mode."""
        mock_show_list.side_effect = [3, 6]
        mock_manager._run_trade_simulator_mode = Mock()

        mock_manager.start_interactive_mode()

        mock_manager._run_trade_simulator_mode.assert_called_once()

    @patch('league_helper.LeagueHelperManager.show_list_selection')
    def test_start_interactive_mode_routes_to_modify_player_data(self, mock_show_list, mock_manager):
        """Test that choice 4 routes to Modify Player Data mode."""
        mock_show_list.side_effect = [4, 6]
        mock_manager.run_modify_player_data_mode = Mock()

        mock_manager.start_interactive_mode()

        mock_manager.run_modify_player_data_mode.assert_called_once()

    @patch('league_helper.LeagueHelperManager.show_list_selection')
    def test_start_interactive_mode_routes_to_save_calculated_points(self, mock_show_list, mock_manager):
        """Test that choice 5 routes to Save Calculated Points mode."""
        mock_show_list.side_effect = [5, 6]
        mock_manager.save_calculated_points_manager = Mock()
        mock_manager.save_calculated_points_manager.execute = Mock()

        mock_manager.start_interactive_mode()

        mock_manager.save_calculated_points_manager.execute.assert_called_once()

    @patch('league_helper.LeagueHelperManager.show_list_selection')
    @patch('builtins.print')
    def test_start_interactive_mode_exits_on_quit(self, mock_print, mock_show_list, mock_manager):
        """Test that choice 6 exits the application."""
        mock_show_list.return_value = 6

        mock_manager.start_interactive_mode()

        goodbye_calls = [call for call in mock_print.call_args_list
                        if "Goodbye!" in str(call)]
        assert len(goodbye_calls) > 0

    @patch('league_helper.LeagueHelperManager.show_list_selection')
    @patch('builtins.print')
    def test_start_interactive_mode_handles_invalid_choice(self, mock_print, mock_show_list, mock_manager):
        """Test that invalid menu choices are handled gracefully."""
        mock_show_list.side_effect = [99, 6]

        mock_manager.start_interactive_mode()

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
             patch('league_helper.LeagueHelperManager.DraftModeManager') as mock_draft, \
             patch('league_helper.LeagueHelperManager.StarterHelperModeManager') as mock_starter, \
             patch('league_helper.LeagueHelperManager.TradeSimulatorModeManager') as mock_trade, \
             patch('league_helper.LeagueHelperManager.ModifyPlayerDataModeManager') as mock_modify, \
             patch('league_helper.LeagueHelperManager.SaveCalculatedPointsManager') as mock_save_points, \
             patch('league_helper.LeagueHelperManager.get_logger'):

            manager = LeagueHelperManager(tmp_path / "data")

            manager.draft_mode_manager.start_interactive_mode = Mock()
            manager.starter_helper_mode_manager.show_recommended_starters = Mock()
            manager.trade_simulator_mode_manager.run_interactive_mode = Mock()
            manager.modify_player_data_mode_manager.start_interactive_mode = Mock()

            yield manager

    def test_run_draft_mode_delegates_correctly(self, mock_manager):
        """Test that _run_draft_mode passes player manager to mode manager."""
        mock_manager._run_draft_mode()

        mock_manager.draft_mode_manager.start_interactive_mode.assert_called_once_with(
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
             patch('league_helper.LeagueHelperManager.DraftModeManager'), \
             patch('league_helper.LeagueHelperManager.StarterHelperModeManager'), \
             patch('league_helper.LeagueHelperManager.TradeSimulatorModeManager'), \
             patch('league_helper.LeagueHelperManager.ModifyPlayerDataModeManager'), \
             patch('league_helper.LeagueHelperManager.SaveCalculatedPointsManager'), \
             patch('league_helper.LeagueHelperManager.get_logger'):

            player_instance = Mock()
            player_instance.players = []
            player_instance.get_roster_len.return_value = 5
            player_instance.display_scored_roster = Mock()
            player_instance.reload_player_data = Mock()
            mock_player.return_value = player_instance

            manager = LeagueHelperManager(Path("/some/path"))

            manager._run_draft_mode = Mock()
            manager._run_starter_helper_mode = Mock()
            manager._run_trade_simulator_mode = Mock()
            manager.run_modify_player_data_mode = Mock()
            manager.save_calculated_points_manager = Mock()
            manager.save_calculated_points_manager.execute = Mock()

            mock_show_list.side_effect = [1, 2, 3, 4, 5, 6]

            manager.start_interactive_mode()

            manager._run_draft_mode.assert_called_once()
            manager._run_starter_helper_mode.assert_called_once()
            manager._run_trade_simulator_mode.assert_called_once()
            manager.run_modify_player_data_mode.assert_called_once()
            manager.save_calculated_points_manager.execute.assert_called_once()

            assert player_instance.reload_player_data.call_count == 6


class TestMainEofAndInterruptHandling:
    """Test main()'s EOF / Ctrl+C handler -- the single owner of the exit status (T83).

    LoggingManager writes console output to stdout via StreamHandler(sys.stdout)
    (utils/LoggingManager.py:82) and prefixes every line with
    "{timestamp} - {logger} - {LEVEL} - {func}:{line} - ", so every notice assertion
    below SUBSTRING-matches. Equality-matching the bare notice text would fail
    against correct code.
    """

    @patch('sys.argv', ['run_league_helper.py'])
    @patch('league_helper.LeagueHelperManager.LeagueHelperManager')
    def test_main_exits_1_with_a_single_notice_on_eof(self, mock_manager_cls, capsys):
        """Test EOF out of the interactive loop -> one-line notice, exit 1, no traceback (R1)."""
        mock_manager_cls.return_value.start_interactive_mode.side_effect = EOFError(
            "EOF when reading a line"
        )

        with pytest.raises(SystemExit) as exc:
            main()

        assert exc.value.code == 1
        assert "No input available on stdin — exiting." in capsys.readouterr().out

    @patch('sys.argv', ['run_league_helper.py'])
    @patch('league_helper.LeagueHelperManager.LeagueHelperManager')
    def test_main_exits_130_on_keyboard_interrupt_in_the_loop(self, mock_manager_cls, capsys):
        """Test Ctrl+C at the main menu -> one-line notice and exit 130 (R3, D2)."""
        mock_manager_cls.return_value.start_interactive_mode.side_effect = KeyboardInterrupt()

        with pytest.raises(SystemExit) as exc:
            main()

        assert exc.value.code == 130
        assert "Interrupted — exiting." in capsys.readouterr().out

    @patch('sys.argv', ['run_league_helper.py'])
    @patch('league_helper.LeagueHelperManager.LeagueHelperManager')
    def test_main_exits_130_on_keyboard_interrupt_during_construction(self, mock_manager_cls, capsys):
        """Test Ctrl+C raised from the CONSTRUCTOR is still caught (R3a).

        This is the case that pins the try's EXTENT. The constructor loads the player
        pool, the season schedule, and team data -- several seconds of work -- so a
        Ctrl+C landing there is a realistic timing. A try scoped to
        start_interactive_mode() alone passes the sibling loop case above and FAILS
        this one, dumping a traceback instead.
        """
        mock_manager_cls.side_effect = KeyboardInterrupt()

        with pytest.raises(SystemExit) as exc:
            main()

        assert exc.value.code == 130
        assert "Interrupted — exiting." in capsys.readouterr().out
        # Proof the catch came from construction, not the loop: the loop never ran.
        mock_manager_cls.return_value.start_interactive_mode.assert_not_called()

    @patch('sys.argv', ['run_league_helper.py'])
    @patch('league_helper.LeagueHelperManager.LeagueHelperManager')
    def test_main_returns_normally_when_the_session_quits(self, mock_manager_cls, capsys):
        """Test the normal Quit path is unchanged -- no SystemExit, no notice (R5)."""
        mock_manager_cls.return_value.start_interactive_mode.return_value = None

        assert main() is None

        out = capsys.readouterr().out
        assert "No input available on stdin — exiting." not in out
        assert "Interrupted — exiting." not in out

    @pytest.mark.parametrize("side_effect,expected_code,notice", [
        (EOFError("EOF when reading a line"), 1, "No input available on stdin — exiting."),
        (KeyboardInterrupt(), 130, "Interrupted — exiting."),
    ])
    @patch('sys.argv', ['run_league_helper.py'])
    @patch('league_helper.LeagueHelperManager.LeagueHelperManager')
    def test_both_notices_survive_a_raised_logging_level(
        self, mock_manager_cls, capsys, side_effect, expected_code, notice
    ):
        """Test neither notice is visibility-coupled to constants.LOGGING_LEVEL (T83 Polish).

        main() configures the logger from constants.LOGGING_LEVEL ('INFO' today), so a
        notice emitted below WARNING would silently disappear if that constant were ever
        raised -- and R1/R3 ("prints exactly one line carrying ...") would become false
        with no failing test. This pins the PROPERTY (the notice survives a WARNING-level
        run) rather than the exact level, so it does not re-litigate D4's level choice.
        """
        mock_manager_cls.return_value.start_interactive_mode.side_effect = side_effect

        original_level = constants.LOGGING_LEVEL
        try:
            with patch.object(constants, 'LOGGING_LEVEL', 'WARNING'):
                with pytest.raises(SystemExit) as exc:
                    main()

            assert exc.value.code == expected_code
            # LoggingManager prefixes the line and writes it to stdout -- substring match only.
            assert notice in capsys.readouterr().out
        finally:
            # setup_logger mutates the process-wide 'league_helper' logger; restore it so a
            # later test in the same session is not left running at WARNING.
            setup_logger(
                constants.LOG_NAME,
                original_level,
                log_to_file=False,
                log_file_path=None,
                log_format=constants.LOGGING_FORMAT,
            )

    def test_main_documents_both_new_exit_statuses(self):
        """Test main()'s docstring records the two SystemExit statuses (R11)."""
        doc = main.__doc__

        assert "Raises:" in doc
        assert "SystemExit" in doc
        assert "130" in doc


