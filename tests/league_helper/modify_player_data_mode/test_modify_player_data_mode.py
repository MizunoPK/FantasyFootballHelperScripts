"""
Tests for ModifyPlayerDataModeManager.

Author: Kai Mizuno
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, call
from league_helper.modify_player_data_mode.ModifyPlayerDataModeManager import ModifyPlayerDataModeManager
from utils.FantasyPlayer import FantasyPlayer


class TestModifyPlayerDataModeManagerInit:
    """Test suite for ModifyPlayerDataModeManager initialization."""

    @pytest.fixture
    def mock_player_manager(self):
        """Create mock PlayerManager."""
        manager = Mock()
        manager.players = []
        return manager

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.DraftedDataWriter')
    def test_init_stores_player_manager(self, mock_writer_class, mock_player_manager):
        """Test that __init__ stores the player_manager reference."""
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        assert mode_manager.player_manager == mock_player_manager

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.DraftedDataWriter')
    def test_init_creates_logger(self, mock_writer_class, mock_player_manager):
        """Test that __init__ creates a logger."""
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        assert mode_manager.logger is not None

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.DraftedDataWriter')
    def test_init_creates_drafted_data_writer(self, mock_writer_class, mock_player_manager, tmp_path):
        """Test that __init__ creates a DraftedDataWriter."""
        data_folder = tmp_path / "data"
        data_folder.mkdir()
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager, data_folder)
        assert mode_manager.drafted_data_writer is not None
        mock_writer_class.assert_called_once_with(data_folder / "drafted_data.csv")

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.DraftedDataWriter')
    def test_set_managers_updates_player_manager(self, mock_writer_class, mock_player_manager):
        """Test that set_managers updates player_manager reference."""
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        new_manager = Mock()
        mode_manager.set_managers(new_manager)
        assert mode_manager.player_manager == new_manager


class TestMarkPlayerAsDrafted:
    """Test suite for _mark_player_as_drafted() method."""

    @pytest.fixture
    def sample_players(self):
        """Create sample players for testing."""
        return [
            FantasyPlayer(id=1, name="Patrick Mahomes", team="KC", position="QB", bye_week=7, drafted_by="", locked=0, score=95.0, fantasy_points=350.0),
            FantasyPlayer(id=2, name="Tyreek Hill", team="MIA", position="WR", bye_week=8, drafted_by="Opponent Team", locked=0, score=85.0, fantasy_points=280.0),
            FantasyPlayer(id=3, name="Travis Kelce", team="KC", position="TE", bye_week=7, drafted_by="Sea Sharp", locked=0, score=80.0, fantasy_points=250.0),
        ]

    @pytest.fixture
    def mock_player_manager(self, sample_players):
        """Create mock PlayerManager with sample players."""
        manager = Mock()
        manager.players = sample_players
        manager.update_players_file = Mock()
        return manager

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.Constants')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.DraftedDataWriter')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_mark_player_as_drafted_sets_drafted_to_one_for_other_team(
        self, mock_search_class, mock_writer_class, mock_show_list, mock_constants, mock_player_manager, sample_players
    ):
        """Test that marking a player as drafted by another team sets drafted=1."""
        # Setup
        mock_constants.FANTASY_TEAM_NAME = "Sea Sharp"
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        available_player = sample_players[0]  # Patrick Mahomes, drafted=0

        # Mock DraftedDataWriter
        mock_writer = Mock()
        mock_writer.get_all_team_names.return_value = ["Annihilators", "Sea Sharp", "The Eskimo Brothers"]
        mock_writer.add_player.return_value = True
        mode_manager.drafted_data_writer = mock_writer

        # Mock interactive_search to return the available player
        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = available_player
        mock_search_class.return_value = mock_searcher

        # Mock team selection - user selects "Annihilators" (index 0, choice 1)
        mock_show_list.return_value = 1

        # Execute
        mode_manager._mark_player_as_drafted()

        # Verify
        assert available_player.drafted_by == "Annihilators"
        mock_writer.add_player.assert_called_once_with(available_player, "Annihilators")
        mock_player_manager.update_players_file.assert_called_once()
        mock_searcher.interactive_search.assert_called_once_with(
            drafted_filter=0,
            prompt="Enter player name to mark as drafted (or press Enter to return): "
        )

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.Constants')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.DraftedDataWriter')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_mark_player_as_drafted_sets_drafted_to_two_for_user_team(
        self, mock_search_class, mock_writer_class, mock_show_list, mock_constants, mock_player_manager, sample_players
    ):
        """Test that marking a player as drafted by user's team sets drafted=2."""
        # Setup
        mock_constants.FANTASY_TEAM_NAME = "Sea Sharp"
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        available_player = sample_players[0]  # Patrick Mahomes, drafted=0

        # Mock DraftedDataWriter
        mock_writer = Mock()
        mock_writer.get_all_team_names.return_value = ["Annihilators", "Sea Sharp", "The Eskimo Brothers"]
        mock_writer.add_player.return_value = True
        mode_manager.drafted_data_writer = mock_writer

        # Mock interactive_search to return the available player
        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = available_player
        mock_search_class.return_value = mock_searcher

        # Mock team selection - user selects "Sea Sharp" (index 1, choice 2)
        mock_show_list.return_value = 2

        # Execute
        mode_manager._mark_player_as_drafted()

        # Verify
        assert available_player.drafted_by == "Sea Sharp"
        mock_writer.add_player.assert_called_once_with(available_player, "Sea Sharp")
        mock_player_manager.update_players_file.assert_called_once()

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.DraftedDataWriter')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_mark_player_as_drafted_handles_user_exit_from_player_search(self, mock_search_class, mock_writer_class, mock_player_manager):
        """Test that mark as drafted handles user exit from player search gracefully."""
        # Setup
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)

        # Mock interactive_search to return None (user exited)
        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = None
        mock_search_class.return_value = mock_searcher

        # Execute
        mode_manager._mark_player_as_drafted()

        # Verify - no exception raised, no file update called
        mock_player_manager.update_players_file.assert_not_called()

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.DraftedDataWriter')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_mark_player_as_drafted_handles_user_cancel_from_team_selection(
        self, mock_search_class, mock_writer_class, mock_show_list, mock_player_manager, sample_players
    ):
        """Test that mark as drafted handles user cancel from team selection gracefully."""
        # Setup
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        available_player = sample_players[0]

        # Mock DraftedDataWriter
        mock_writer = Mock()
        mock_writer.get_all_team_names.return_value = ["Annihilators", "Sea Sharp", "The Eskimo Brothers"]
        mode_manager.drafted_data_writer = mock_writer

        # Mock interactive_search to return player
        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = available_player
        mock_search_class.return_value = mock_searcher

        # Mock team selection - user cancels (choice 4, which is len(team_names) + 1)
        mock_show_list.return_value = 4

        # Execute
        mode_manager._mark_player_as_drafted()

        # Verify - player not modified, no file update
        assert available_player.is_free_agent()  # Still available
        mock_writer.add_player.assert_not_called()
        mock_player_manager.update_players_file.assert_not_called()

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.DraftedDataWriter')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_mark_player_as_drafted_handles_no_teams_in_csv(
        self, mock_search_class, mock_writer_class, mock_show_list, mock_player_manager, sample_players
    ):
        """Test that mark as drafted handles empty team list gracefully."""
        # Setup
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        available_player = sample_players[0]

        # Mock DraftedDataWriter to return empty team list
        mock_writer = Mock()
        mock_writer.get_all_team_names.return_value = []
        mode_manager.drafted_data_writer = mock_writer

        # Mock interactive_search to return player
        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = available_player
        mock_search_class.return_value = mock_searcher

        # Execute
        mode_manager._mark_player_as_drafted()

        # Verify - exits early, no team selection shown
        mock_show_list.assert_not_called()
        mock_player_manager.update_players_file.assert_not_called()


class TestDropPlayer:
    """Test suite for _drop_player() method."""

    @pytest.fixture
    def sample_players(self):
        """Create sample players for testing."""
        return [
            FantasyPlayer(id=1, name="Patrick Mahomes", team="KC", position="QB", bye_week=7, drafted_by="Sea Sharp", locked=0, score=95.0, fantasy_points=350.0),
            FantasyPlayer(id=2, name="Tyreek Hill", team="MIA", position="WR", bye_week=8, drafted_by="Opponent Team", locked=0, score=85.0, fantasy_points=280.0),
            FantasyPlayer(id=3, name="Josh Allen", team="BUF", position="QB", bye_week=10, drafted_by="", locked=0, score=90.0, fantasy_points=330.0),
        ]

    @pytest.fixture
    def mock_player_manager(self, sample_players):
        """Create mock PlayerManager."""
        manager = Mock()
        manager.players = sample_players
        manager.update_players_file = Mock()
        return manager

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.DraftedDataWriter')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_drop_player_sets_drafted_to_zero_from_roster(self, mock_search_class, mock_writer_class, mock_player_manager, sample_players):
        """Test that dropping a rostered player sets drafted=0 and removes from CSV."""
        # Setup
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        rostered_player = sample_players[0]  # Patrick Mahomes, drafted=2

        # Mock DraftedDataWriter
        mock_writer = Mock()
        mock_writer.remove_player.return_value = True
        mode_manager.drafted_data_writer = mock_writer

        # Mock interactive_search
        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = rostered_player
        mock_search_class.return_value = mock_searcher

        # Execute
        mode_manager._drop_player()

        # Verify
        assert rostered_player.drafted_by == ""
        mock_writer.remove_player.assert_called_once_with(rostered_player)
        mock_player_manager.update_players_file.assert_called_once()
        mock_searcher.interactive_search.assert_called_once_with(
            drafted_filter=None,
            prompt="Enter player name to drop (or press Enter to return): ",
            not_available=True
        )

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.DraftedDataWriter')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_drop_player_sets_drafted_to_zero_from_drafted(self, mock_search_class, mock_writer_class, mock_player_manager, sample_players):
        """Test that dropping a drafted player sets drafted=0 and removes from CSV."""
        # Setup
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        drafted_player = sample_players[1]  # Tyreek Hill, drafted=1

        # Mock DraftedDataWriter
        mock_writer = Mock()
        mock_writer.remove_player.return_value = True
        mode_manager.drafted_data_writer = mock_writer

        # Mock interactive_search
        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = drafted_player
        mock_search_class.return_value = mock_searcher

        # Execute
        mode_manager._drop_player()

        # Verify
        assert drafted_player.drafted_by == ""
        mock_writer.remove_player.assert_called_once_with(drafted_player)
        mock_player_manager.update_players_file.assert_called_once()

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.DraftedDataWriter')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_drop_player_handles_user_exit(self, mock_search_class, mock_writer_class, mock_player_manager):
        """Test that drop player handles user exit gracefully."""
        # Setup
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)

        # Mock interactive_search to return None
        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = None
        mock_search_class.return_value = mock_searcher

        # Execute
        mode_manager._drop_player()

        # Verify
        mock_player_manager.update_players_file.assert_not_called()

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.DraftedDataWriter')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_drop_player_continues_even_if_csv_removal_fails(self, mock_search_class, mock_writer_class, mock_player_manager, sample_players):
        """Test that drop player continues even if CSV removal fails."""
        # Setup
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        drafted_player = sample_players[1]  # Tyreek Hill, drafted=1

        # Mock DraftedDataWriter to fail removal
        mock_writer = Mock()
        mock_writer.remove_player.return_value = False
        mode_manager.drafted_data_writer = mock_writer

        # Mock interactive_search
        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = drafted_player
        mock_search_class.return_value = mock_searcher

        # Execute
        mode_manager._drop_player()

        # Verify - player still dropped even though CSV removal failed
        assert drafted_player.drafted_by == ""
        mock_player_manager.update_players_file.assert_called_once()


class TestLockPlayer:
    """Test suite for _lock_player() method."""

    @pytest.fixture
    def sample_players(self):
        """Create sample players for testing."""
        return [
            FantasyPlayer(id=1, name="Patrick Mahomes", team="KC", position="QB", bye_week=7, drafted_by="Sea Sharp", locked=0, score=95.0, fantasy_points=350.0),
            FantasyPlayer(id=2, name="Travis Kelce", team="KC", position="TE", bye_week=7, drafted_by="Sea Sharp", locked=1, score=80.0, fantasy_points=250.0),
        ]

    @pytest.fixture
    def mock_player_manager(self, sample_players):
        """Create mock PlayerManager."""
        manager = Mock()
        manager.players = sample_players
        manager.update_players_file = Mock()
        return manager

    @patch('builtins.print')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_lock_player_toggles_from_zero_to_one(self, mock_search_class, mock_print, mock_player_manager, sample_players):
        """Test that locking a player toggles locked from 0 to 1."""
        # Setup
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        unlocked_player = sample_players[0]  # Patrick Mahomes, locked=0

        # Mock interactive_search
        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = unlocked_player
        mock_search_class.return_value = mock_searcher

        # Execute
        mode_manager._lock_player()

        # Verify
        assert unlocked_player.locked == 1
        mock_player_manager.update_players_file.assert_called_once()
        mock_searcher.interactive_search.assert_called_once_with(
            drafted_filter=None,
            prompt="Enter player name to lock/unlock (or press Enter to return): "
        )

    @patch('builtins.print')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_lock_player_toggles_from_one_to_zero(self, mock_search_class, mock_print, mock_player_manager, sample_players):
        """Test that unlocking a player toggles locked from 1 to 0."""
        # Setup
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        locked_player = sample_players[1]  # Travis Kelce, locked=1

        # Mock interactive_search
        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = locked_player
        mock_search_class.return_value = mock_searcher

        # Execute
        mode_manager._lock_player()

        # Verify
        assert locked_player.locked == 0
        mock_player_manager.update_players_file.assert_called_once()

    @patch('builtins.print')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_lock_player_displays_locked_players_list(self, mock_search_class, mock_print, mock_player_manager, sample_players):
        """Test that _lock_player() displays list of currently locked players."""
        # Setup
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        # Travis Kelce is locked=1, Patrick Mahomes is locked=0

        # Mock interactive_search to return None (user exits)
        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = None
        mock_search_class.return_value = mock_searcher

        # Execute
        mode_manager._lock_player()

        # Verify that locked players header was printed
        print_calls = [str(call) for call in mock_print.call_args_list]
        printed_output = ' '.join(print_calls)

        # Check that the locked players section was displayed
        assert any('CURRENTLY LOCKED PLAYERS' in str(call) for call in print_calls)
        # Check that Travis Kelce (locked=1) appears in output
        assert any('Travis Kelce' in str(call) for call in print_calls)
        # Check that total locked players count appears
        assert any('Total locked players: 1' in str(call) for call in print_calls)

    @patch('builtins.print')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_lock_player_displays_no_locked_players_message(self, mock_search_class, mock_print):
        """Test that _lock_player() displays 'no locked players' message when none are locked."""
        # Setup - create players with all locked=0
        unlocked_players = [
            FantasyPlayer(id=1, name="Patrick Mahomes", team="KC", position="QB", bye_week=7, drafted_by="Sea Sharp", locked=0, score=95.0, fantasy_points=350.0),
            FantasyPlayer(id=2, name="Josh Allen", team="BUF", position="QB", bye_week=10, drafted_by="Opponent Team", locked=0, score=90.0, fantasy_points=330.0),
        ]
        mock_player_manager = Mock()
        mock_player_manager.players = unlocked_players

        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)

        # Mock interactive_search to return None (user exits)
        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = None
        mock_search_class.return_value = mock_searcher

        # Execute
        mode_manager._lock_player()

        # Verify that "NO LOCKED PLAYERS" message was displayed
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any('NO LOCKED PLAYERS' in str(call) for call in print_calls)
        assert any('No players are currently locked' in str(call) for call in print_calls)

    @patch('builtins.print')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_lock_player_handles_user_exit(self, mock_search_class, mock_print, mock_player_manager):
        """Test that lock player handles user exit gracefully."""
        # Setup
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)

        # Mock interactive_search to return None
        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = None
        mock_search_class.return_value = mock_searcher

        # Execute
        mode_manager._lock_player()

        # Verify
        mock_player_manager.update_players_file.assert_not_called()


class TestStartInteractiveMode:
    """Test suite for start_interactive_mode() method."""

    @pytest.fixture
    def mock_player_manager(self):
        """Create mock PlayerManager."""
        manager = Mock()
        manager.players = []
        return manager

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.DraftedDataWriter')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    def test_start_interactive_mode_exits_on_choice_4(self, mock_show_list, mock_writer_class, mock_player_manager):
        """Test that choice 4 exits the interactive mode."""
        # Setup
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        mock_show_list.return_value = 4  # Return to Main Menu choice (now 4 instead of 5)

        # Execute
        mode_manager.start_interactive_mode(mock_player_manager)

        # Verify - should have called show_list_selection once and then exited
        mock_show_list.assert_called_once()

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.DraftedDataWriter')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    def test_start_interactive_mode_calls_mark_as_drafted_for_choice_1(self, mock_show_list, mock_writer_class, mock_player_manager):
        """Test that choice 1 calls _mark_player_as_drafted()."""
        # Setup
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        mode_manager._mark_player_as_drafted = Mock()
        mock_show_list.side_effect = [1, 4]  # First choice 1, then exit (now 4 instead of 5)

        # Execute
        mode_manager.start_interactive_mode(mock_player_manager)

        # Verify
        mode_manager._mark_player_as_drafted.assert_called_once()

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.DraftedDataWriter')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    def test_start_interactive_mode_calls_drop_player_for_choice_2(self, mock_show_list, mock_writer_class, mock_player_manager):
        """Test that choice 2 calls _drop_player() (was choice 3, now choice 2)."""
        # Setup
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        mode_manager._drop_player = Mock()
        mock_show_list.side_effect = [2, 4]  # First choice 2, then exit

        # Execute
        mode_manager.start_interactive_mode(mock_player_manager)

        # Verify
        mode_manager._drop_player.assert_called_once()

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.DraftedDataWriter')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    def test_start_interactive_mode_calls_lock_player_for_choice_3(self, mock_show_list, mock_writer_class, mock_player_manager):
        """Test that choice 3 calls _lock_player() (was choice 4, now choice 3)."""
        # Setup
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        mode_manager._lock_player = Mock()
        mock_show_list.side_effect = [3, 4]  # First choice 3, then exit

        # Execute
        mode_manager.start_interactive_mode(mock_player_manager)

        # Verify
        mode_manager._lock_player.assert_called_once()

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.DraftedDataWriter')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    def test_start_interactive_mode_handles_keyboard_interrupt(self, mock_show_list, mock_writer_class, mock_player_manager):
        """Test that KeyboardInterrupt in interactive mode exits gracefully."""
        # Setup
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        mock_show_list.side_effect = KeyboardInterrupt()

        # Execute - should not raise exception
        mode_manager.start_interactive_mode(mock_player_manager)

        # Verify - exited cleanly
        assert True  # If we get here, KeyboardInterrupt was handled

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.DraftedDataWriter')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    def test_start_interactive_mode_handles_general_exception(self, mock_show_list, mock_writer_class, mock_player_manager):
        """Test that general exceptions in interactive mode exit gracefully."""
        # Setup
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        mock_show_list.side_effect = Exception("Test exception")

        # Execute - should not raise exception
        mode_manager.start_interactive_mode(mock_player_manager)

        # Verify - exited cleanly
        assert True  # If we get here, exception was handled

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.DraftedDataWriter')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    def test_start_interactive_mode_handles_invalid_choice(self, mock_show_list, mock_writer_class, mock_player_manager):
        """Test that invalid choices print error message and continue."""
        # Setup
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        mock_show_list.side_effect = [999, 4]  # Invalid choice, then exit

        # Execute
        mode_manager.start_interactive_mode(mock_player_manager)

        # Verify - should have called show_list_selection twice (invalid + exit)
        assert mock_show_list.call_count == 2

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.DraftedDataWriter')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    def test_start_interactive_mode_updates_player_manager(self, mock_show_list, mock_writer_class):
        """Test that start_interactive_mode updates player_manager reference."""
        # Setup
        old_manager = Mock()
        new_manager = Mock()
        mode_manager = ModifyPlayerDataModeManager(old_manager)
        mock_show_list.return_value = 4  # Exit immediately

        # Execute
        mode_manager.start_interactive_mode(new_manager)

        # Verify
        assert mode_manager.player_manager == new_manager


class TestEdgeCases:
    """Test suite for edge cases and error handling."""

    @pytest.fixture
    def sample_players(self):
        """Create sample players for testing."""
        return [
            FantasyPlayer(id=1, name="Patrick Mahomes", team="KC", position="QB", bye_week=7, drafted_by="", locked=0, score=95.0, fantasy_points=350.0),
            FantasyPlayer(id=2, name="Tyreek Hill", team="MIA", position="WR", bye_week=8, drafted_by="Opponent Team", locked=0, score=85.0, fantasy_points=280.0),
        ]

    @pytest.fixture
    def mock_player_manager(self, sample_players):
        """Create mock PlayerManager."""
        manager = Mock()
        manager.players = sample_players
        manager.update_players_file = Mock()
        return manager

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.Constants')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.DraftedDataWriter')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_mark_player_as_drafted_handles_csv_add_failure(
        self, mock_search_class, mock_writer_class, mock_show_list, mock_constants, mock_player_manager, sample_players
    ):
        """Test that mark as drafted handles CSV add failure gracefully."""
        # Setup
        mock_constants.FANTASY_TEAM_NAME = "Sea Sharp"
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        available_player = sample_players[0]

        # Mock DraftedDataWriter to fail add_player
        mock_writer = Mock()
        mock_writer.get_all_team_names.return_value = ["Annihilators", "Sea Sharp"]
        mock_writer.add_player.return_value = False  # Failure
        mode_manager.drafted_data_writer = mock_writer

        # Mock interactive_search
        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = available_player
        mock_search_class.return_value = mock_searcher

        # Mock team selection
        mock_show_list.return_value = 1

        # Execute
        mode_manager._mark_player_as_drafted()

        # Verify - player still marked as drafted despite CSV failure
        assert available_player.drafted_by == "Annihilators"
        mock_player_manager.update_players_file.assert_called_once()

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.DraftedDataWriter')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_drop_player_handles_csv_remove_failure(self, mock_search_class, mock_writer_class, mock_player_manager, sample_players):
        """Test that drop player handles CSV remove failure gracefully."""
        # Setup
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        drafted_player = sample_players[1]  # drafted=1

        # Mock DraftedDataWriter to fail remove_player
        mock_writer = Mock()
        mock_writer.remove_player.return_value = False  # Failure
        mode_manager.drafted_data_writer = mock_writer

        # Mock interactive_search
        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = drafted_player
        mock_search_class.return_value = mock_searcher

        # Execute
        mode_manager._drop_player()

        # Verify - player still dropped despite CSV failure
        assert drafted_player.drafted_by == ""
        mock_player_manager.update_players_file.assert_called_once()

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.Constants')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.DraftedDataWriter')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_mark_player_as_drafted_with_single_team(
        self, mock_search_class, mock_writer_class, mock_show_list, mock_constants, mock_player_manager, sample_players
    ):
        """Test marking player as drafted when only one team exists."""
        # Setup
        mock_constants.FANTASY_TEAM_NAME = "Sea Sharp"
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        available_player = sample_players[0]

        # Mock DraftedDataWriter with single team
        mock_writer = Mock()
        mock_writer.get_all_team_names.return_value = ["Sea Sharp"]
        mock_writer.add_player.return_value = True
        mode_manager.drafted_data_writer = mock_writer

        # Mock interactive_search
        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = available_player
        mock_search_class.return_value = mock_searcher

        # Mock team selection - only option is user's team
        mock_show_list.return_value = 1

        # Execute
        mode_manager._mark_player_as_drafted()

        # Verify - should be drafted_by="Sea Sharp" (user's team)
        assert available_player.drafted_by == "Sea Sharp"

    @patch('builtins.print')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.DraftedDataWriter')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_lock_player_preserves_drafted_status(self, mock_search_class, mock_writer_class, mock_print, mock_player_manager, sample_players):
        """Test that locking a player doesn't change drafted status."""
        # Setup
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        player = sample_players[1]  # drafted_by="Opponent Team", locked=0
        original_drafted_by = player.drafted_by

        # Mock interactive_search
        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = player
        mock_search_class.return_value = mock_searcher

        # Execute
        mode_manager._lock_player()

        # Verify - drafted status unchanged, only locked changed
        assert player.drafted_by == original_drafted_by
        assert player.locked == 1

    @pytest.fixture
    def player_with_extreme_values(self):
        """Create player with boundary/extreme values."""
        return FantasyPlayer(
            id=999999,
            name="Test Player With Very Long Name That Exceeds Normal Length Boundaries",
            team="ABC",
            position="QB",
            bye_week=18,  # Beyond normal bye week range
            drafted_by="",
            locked=0,
            score=0.0,  # Minimum score
            fantasy_points=0.0
        )

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.Constants')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.DraftedDataWriter')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_mark_player_with_extreme_values(
        self, mock_search_class, mock_writer_class, mock_show_list, mock_constants, mock_player_manager, player_with_extreme_values
    ):
        """Test marking player with boundary/extreme attribute values."""
        # Setup
        mock_constants.FANTASY_TEAM_NAME = "Sea Sharp"
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)

        # Mock DraftedDataWriter
        mock_writer = Mock()
        mock_writer.get_all_team_names.return_value = ["Team1"]
        mock_writer.add_player.return_value = True
        mode_manager.drafted_data_writer = mock_writer

        # Mock interactive_search
        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = player_with_extreme_values
        mock_search_class.return_value = mock_searcher

        # Mock team selection
        mock_show_list.return_value = 1

        # Execute - should handle extreme values without errors
        mode_manager._mark_player_as_drafted()

        # Verify
        assert player_with_extreme_values.drafted_by == "Team1"
        mock_writer.add_player.assert_called_once()

    @patch('builtins.print')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.DraftedDataWriter')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_lock_player_multiple_times(self, mock_search_class, mock_writer_class, mock_print, mock_player_manager, sample_players):
        """Test locking the same player multiple times toggles correctly."""
        # Setup
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        player = sample_players[0]  # locked=0 initially

        # Mock interactive_search to return same player multiple times
        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = player
        mock_search_class.return_value = mock_searcher

        # Execute - lock, unlock, lock again
        mode_manager._lock_player()
        assert player.locked == 1

        mode_manager._lock_player()
        assert player.locked == 0

        mode_manager._lock_player()
        assert player.locked == 1

        # Verify file updated 3 times
        assert mock_player_manager.update_players_file.call_count == 3
