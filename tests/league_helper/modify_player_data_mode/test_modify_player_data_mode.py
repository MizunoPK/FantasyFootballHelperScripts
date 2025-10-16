"""
Tests for ModifyPlayerDataModeManager.

Author: Kai Mizuno
"""

import pytest
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

    def test_init_stores_player_manager(self, mock_player_manager):
        """Test that __init__ stores the player_manager reference."""
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        assert mode_manager.player_manager == mock_player_manager

    def test_init_creates_logger(self, mock_player_manager):
        """Test that __init__ creates a logger."""
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        assert mode_manager.logger is not None

    def test_set_managers_updates_player_manager(self, mock_player_manager):
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
            FantasyPlayer(id=1, name="Patrick Mahomes", team="KC", position="QB", bye_week=7, drafted=0, locked=0, score=95.0, fantasy_points=350.0),
            FantasyPlayer(id=2, name="Tyreek Hill", team="MIA", position="WR", bye_week=8, drafted=1, locked=0, score=85.0, fantasy_points=280.0),
            FantasyPlayer(id=3, name="Travis Kelce", team="KC", position="TE", bye_week=7, drafted=2, locked=0, score=80.0, fantasy_points=250.0),
        ]

    @pytest.fixture
    def mock_player_manager(self, sample_players):
        """Create mock PlayerManager with sample players."""
        manager = Mock()
        manager.players = sample_players
        manager.update_players_file = Mock()
        return manager

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_mark_player_as_drafted_sets_drafted_to_one(self, mock_search_class, mock_player_manager, sample_players):
        """Test that marking a player as drafted sets drafted=1."""
        # Setup
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        available_player = sample_players[0]  # Patrick Mahomes, drafted=0

        # Mock interactive_search to return the available player
        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = available_player
        mock_search_class.return_value = mock_searcher

        # Execute
        mode_manager._mark_player_as_drafted()

        # Verify
        assert available_player.drafted == 1
        mock_player_manager.update_players_file.assert_called_once()
        mock_searcher.interactive_search.assert_called_once_with(
            drafted_filter=0,
            prompt="Enter player name to mark as drafted (or press Enter to return): "
        )

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_mark_player_as_drafted_handles_user_exit(self, mock_search_class, mock_player_manager):
        """Test that mark as drafted handles user exit gracefully."""
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


class TestMarkPlayerAsRostered:
    """Test suite for _mark_player_as_rostered() method."""

    @pytest.fixture
    def sample_players(self):
        """Create sample players for testing."""
        return [
            FantasyPlayer(id=1, name="Josh Allen", team="BUF", position="QB", bye_week=10, drafted=0, locked=0, score=90.0, fantasy_points=330.0),
            FantasyPlayer(id=2, name="Christian McCaffrey", team="SF", position="RB", bye_week=9, drafted=0, locked=0, score=92.0, fantasy_points=320.0),
        ]

    @pytest.fixture
    def mock_player_manager(self, sample_players):
        """Create mock PlayerManager."""
        manager = Mock()
        manager.players = sample_players
        manager.update_players_file = Mock()
        return manager

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_mark_player_as_rostered_sets_drafted_to_two(self, mock_search_class, mock_player_manager, sample_players):
        """Test that marking a player as rostered sets drafted=2."""
        # Setup
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        available_player = sample_players[0]  # Josh Allen, drafted=0

        # Mock interactive_search
        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = available_player
        mock_search_class.return_value = mock_searcher

        # Execute
        mode_manager._mark_player_as_rostered()

        # Verify
        assert available_player.drafted == 2
        mock_player_manager.update_players_file.assert_called_once()
        mock_searcher.interactive_search.assert_called_once_with(
            drafted_filter=0,
            prompt="Enter player name to add to your roster (or press Enter to return): "
        )

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_mark_player_as_rostered_handles_user_exit(self, mock_search_class, mock_player_manager):
        """Test that mark as rostered handles user exit gracefully."""
        # Setup
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)

        # Mock interactive_search to return None
        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = None
        mock_search_class.return_value = mock_searcher

        # Execute
        mode_manager._mark_player_as_rostered()

        # Verify
        mock_player_manager.update_players_file.assert_not_called()


class TestDropPlayer:
    """Test suite for _drop_player() method."""

    @pytest.fixture
    def sample_players(self):
        """Create sample players for testing."""
        return [
            FantasyPlayer(id=1, name="Patrick Mahomes", team="KC", position="QB", bye_week=7, drafted=2, locked=0, score=95.0, fantasy_points=350.0),
            FantasyPlayer(id=2, name="Tyreek Hill", team="MIA", position="WR", bye_week=8, drafted=1, locked=0, score=85.0, fantasy_points=280.0),
            FantasyPlayer(id=3, name="Josh Allen", team="BUF", position="QB", bye_week=10, drafted=0, locked=0, score=90.0, fantasy_points=330.0),
        ]

    @pytest.fixture
    def mock_player_manager(self, sample_players):
        """Create mock PlayerManager."""
        manager = Mock()
        manager.players = sample_players
        manager.update_players_file = Mock()
        return manager

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_drop_player_sets_drafted_to_zero_from_roster(self, mock_search_class, mock_player_manager, sample_players):
        """Test that dropping a rostered player sets drafted=0."""
        # Setup
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        rostered_player = sample_players[0]  # Patrick Mahomes, drafted=2

        # Mock interactive_search
        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = rostered_player
        mock_search_class.return_value = mock_searcher

        # Execute
        mode_manager._drop_player()

        # Verify
        assert rostered_player.drafted == 0
        mock_player_manager.update_players_file.assert_called_once()
        mock_searcher.interactive_search.assert_called_once_with(
            drafted_filter=None,
            prompt="Enter player name to drop (or press Enter to return): ",
            not_available=True
        )

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_drop_player_sets_drafted_to_zero_from_drafted(self, mock_search_class, mock_player_manager, sample_players):
        """Test that dropping a drafted player sets drafted=0."""
        # Setup
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        drafted_player = sample_players[1]  # Tyreek Hill, drafted=1

        # Mock interactive_search
        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = drafted_player
        mock_search_class.return_value = mock_searcher

        # Execute
        mode_manager._drop_player()

        # Verify
        assert drafted_player.drafted == 0
        mock_player_manager.update_players_file.assert_called_once()

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_drop_player_handles_user_exit(self, mock_search_class, mock_player_manager):
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


class TestLockPlayer:
    """Test suite for _lock_player() method."""

    @pytest.fixture
    def sample_players(self):
        """Create sample players for testing."""
        return [
            FantasyPlayer(id=1, name="Patrick Mahomes", team="KC", position="QB", bye_week=7, drafted=2, locked=0, score=95.0, fantasy_points=350.0),
            FantasyPlayer(id=2, name="Travis Kelce", team="KC", position="TE", bye_week=7, drafted=2, locked=1, score=80.0, fantasy_points=250.0),
        ]

    @pytest.fixture
    def mock_player_manager(self, sample_players):
        """Create mock PlayerManager."""
        manager = Mock()
        manager.players = sample_players
        manager.update_players_file = Mock()
        return manager

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_lock_player_toggles_from_zero_to_one(self, mock_search_class, mock_player_manager, sample_players):
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

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_lock_player_toggles_from_one_to_zero(self, mock_search_class, mock_player_manager, sample_players):
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

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_lock_player_handles_user_exit(self, mock_search_class, mock_player_manager):
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

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    def test_start_interactive_mode_exits_on_choice_5(self, mock_show_list, mock_player_manager):
        """Test that choice 5 exits the interactive mode."""
        # Setup
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        mock_show_list.return_value = 5  # Return to Main Menu choice

        # Execute
        mode_manager.start_interactive_mode(mock_player_manager)

        # Verify - should have called show_list_selection once and then exited
        mock_show_list.assert_called_once()

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    def test_start_interactive_mode_calls_mark_as_drafted_for_choice_1(self, mock_show_list, mock_player_manager):
        """Test that choice 1 calls _mark_player_as_drafted()."""
        # Setup
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        mode_manager._mark_player_as_drafted = Mock()
        mock_show_list.side_effect = [1, 5]  # First choice 1, then exit

        # Execute
        mode_manager.start_interactive_mode(mock_player_manager)

        # Verify
        mode_manager._mark_player_as_drafted.assert_called_once()

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    def test_start_interactive_mode_calls_mark_as_rostered_for_choice_2(self, mock_show_list, mock_player_manager):
        """Test that choice 2 calls _mark_player_as_rostered()."""
        # Setup
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        mode_manager._mark_player_as_rostered = Mock()
        mock_show_list.side_effect = [2, 5]  # First choice 2, then exit

        # Execute
        mode_manager.start_interactive_mode(mock_player_manager)

        # Verify
        mode_manager._mark_player_as_rostered.assert_called_once()

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    def test_start_interactive_mode_calls_drop_player_for_choice_3(self, mock_show_list, mock_player_manager):
        """Test that choice 3 calls _drop_player()."""
        # Setup
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        mode_manager._drop_player = Mock()
        mock_show_list.side_effect = [3, 5]  # First choice 3, then exit

        # Execute
        mode_manager.start_interactive_mode(mock_player_manager)

        # Verify
        mode_manager._drop_player.assert_called_once()

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    def test_start_interactive_mode_calls_lock_player_for_choice_4(self, mock_show_list, mock_player_manager):
        """Test that choice 4 calls _lock_player()."""
        # Setup
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        mode_manager._lock_player = Mock()
        mock_show_list.side_effect = [4, 5]  # First choice 4, then exit

        # Execute
        mode_manager.start_interactive_mode(mock_player_manager)

        # Verify
        mode_manager._lock_player.assert_called_once()
