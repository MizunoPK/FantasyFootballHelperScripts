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
            FantasyPlayer(id=1, name="Patrick Mahomes", team="KC", position="QB", bye_week=7, drafted_by="", locked=0, score=95.0, fantasy_points=350.0),
            FantasyPlayer(id=2, name="Tyreek Hill", team="MIA", position="WR", bye_week=8, drafted_by="Annihilators", locked=0, score=85.0, fantasy_points=280.0),
            FantasyPlayer(id=3, name="Travis Kelce", team="KC", position="TE", bye_week=7, drafted_by="Sea Sharp", locked=0, score=80.0, fantasy_points=250.0),
            FantasyPlayer(id=4, name="Justin Jefferson", team="MIN", position="WR", bye_week=6, drafted_by="The Eskimo Brothers", locked=0, score=90.0, fantasy_points=320.0),
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
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_mark_player_as_drafted_sets_drafted_to_one_for_other_team(
        self, mock_search_class, mock_show_list, mock_constants, mock_player_manager, sample_players
    ):
        """Test that marking a player as drafted by another team sets drafted_by=team_name."""
        # Setup
        mock_constants.FANTASY_TEAM_NAME = "Sea Sharp"
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        available_player = sample_players[0]  # Patrick Mahomes, drafted_by=""

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
        mock_player_manager.update_players_file.assert_called_once()
        mock_searcher.interactive_search.assert_called_once()

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.Constants')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_mark_player_as_drafted_sets_drafted_to_two_for_user_team(
        self, mock_search_class, mock_show_list, mock_constants, mock_player_manager, sample_players
    ):
        """Test that marking a player as drafted by user's team sets drafted_by=FANTASY_TEAM_NAME."""
        # Setup
        mock_constants.FANTASY_TEAM_NAME = "Sea Sharp"
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        available_player = sample_players[0]  # Patrick Mahomes, drafted_by=""

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
        mock_player_manager.update_players_file.assert_called_once()

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_mark_player_as_drafted_handles_user_exit_from_player_search(self, mock_search_class, mock_player_manager):
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

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.Constants')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_mark_player_as_drafted_handles_user_cancel_from_team_selection(
        self, mock_search_class, mock_show_list, mock_constants, mock_player_manager, sample_players
    ):
        """Test that mark as drafted handles user cancel from team selection gracefully."""
        # Setup
        mock_constants.FANTASY_TEAM_NAME = "Sea Sharp"
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        available_player = sample_players[0]

        # Mock interactive_search
        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = available_player
        mock_search_class.return_value = mock_searcher

        # Mock team selection - select "Sea Sharp" (index 2 in sorted list)
        mock_show_list.return_value = 2

        # Execute
        mode_manager._mark_player_as_drafted()

        # Verify - should be drafted_by="Sea Sharp" (user's team)
        assert available_player.drafted_by == "Sea Sharp"

    @patch('builtins.print')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_lock_player_preserves_drafted_status(self, mock_search_class, mock_print, mock_player_manager, sample_players):
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
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_mark_player_with_extreme_values(
        self, mock_search_class, mock_show_list, mock_constants, mock_player_manager, player_with_extreme_values
    ):
        """Test marking player with boundary/extreme attribute values."""
        # Setup
        mock_constants.FANTASY_TEAM_NAME = "Sea Sharp"
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)

        # Mock interactive_search
        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = player_with_extreme_values
        mock_search_class.return_value = mock_searcher

        # Mock team selection
        mock_show_list.return_value = 1

        # Execute - should handle extreme values without errors
        mode_manager._mark_player_as_drafted()

        # Verify - should be marked as drafted by first team in sorted list
        assert player_with_extreme_values.drafted_by == "Annihilators"
        mock_player_manager.update_players_file.assert_called_once()

    @patch('builtins.print')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_lock_player_multiple_times(self, mock_search_class, mock_print, mock_player_manager, sample_players):
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
