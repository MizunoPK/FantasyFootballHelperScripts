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
        # Deliberately overlaps the sample_players drafted_by names on one entry
        # ("Annihilators") and diverges on the rest, so the menu union is exercised:
        # config-only, data-only, and both-sources names all appear exactly once.
        manager.config.opponent_teams = ["Annihilators", "Pidgin", "Striking Shibas"]
        return manager

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.Constants')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_mark_player_as_drafted_sets_drafted_to_one_for_other_team(
        self, mock_search_class, mock_show_list, mock_constants, mock_player_manager, sample_players
    ):
        """Test that marking a player as drafted by another team sets drafted_by=team_name."""
        mock_constants.FANTASY_TEAM_NAME = "Sea Sharp"
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        available_player = sample_players[0]

        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = available_player
        mock_search_class.return_value = mock_searcher

        mock_show_list.return_value = 1

        mode_manager._mark_player_as_drafted()

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
        mock_constants.FANTASY_TEAM_NAME = "Sea Sharp"
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        available_player = sample_players[0]

        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = available_player
        mock_search_class.return_value = mock_searcher

        # Sorted union is: 1 Annihilators, 2 Pidgin, 3 Sea Sharp, 4 Striking Shibas, 5 The Eskimo Brothers
        mock_show_list.return_value = 3

        mode_manager._mark_player_as_drafted()

        assert available_player.drafted_by == "Sea Sharp"
        mock_player_manager.update_players_file.assert_called_once()

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_mark_player_as_drafted_handles_user_exit_from_player_search(self, mock_search_class, mock_player_manager):
        """Test that mark as drafted handles user exit from player search gracefully."""
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)

        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = None
        mock_search_class.return_value = mock_searcher

        mode_manager._mark_player_as_drafted()

        mock_player_manager.update_players_file.assert_not_called()

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.Constants')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_mark_player_as_drafted_selects_the_user_team_by_index(
        self, mock_search_class, mock_show_list, mock_constants, mock_player_manager, sample_players
    ):
        """Test that selecting the user's team row by index sets drafted_by=FANTASY_TEAM_NAME."""
        mock_constants.FANTASY_TEAM_NAME = "Sea Sharp"
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        available_player = sample_players[0]

        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = available_player
        mock_search_class.return_value = mock_searcher

        # Sorted union is: 1 Annihilators, 2 Pidgin, 3 Sea Sharp, 4 Striking Shibas, 5 The Eskimo Brothers
        mock_show_list.return_value = 3

        mode_manager._mark_player_as_drafted()

        assert available_player.drafted_by == "Sea Sharp"

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.Constants')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_mark_player_as_drafted_cancels_on_the_sentinel_index(
        self, mock_search_class, mock_show_list, mock_constants, mock_player_manager, sample_players
    ):
        """Test that the Cancel entry (len(options) + 1) aborts without mutating or saving."""
        mock_constants.FANTASY_TEAM_NAME = "Sea Sharp"
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        available_player = sample_players[0]

        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = available_player
        mock_search_class.return_value = mock_searcher

        # Derive the Cancel sentinel from the menu actually presented, so the test
        # stays correct no matter how many teams the config/data union produces.
        captured_options = []

        def _pick_cancel(_title, options, _cancel_label):
            captured_options.extend(options)
            return len(options) + 1

        mock_show_list.side_effect = _pick_cancel

        mode_manager._mark_player_as_drafted()

        assert captured_options, "TEAM SELECTION menu should not be empty"
        assert available_player.drafted_by == ""
        mock_player_manager.update_players_file.assert_not_called()

    @patch('builtins.print')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_lock_player_preserves_drafted_status(self, mock_search_class, mock_print, mock_player_manager, sample_players):
        """Test that locking a player doesn't change drafted status."""
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        player = sample_players[1]
        original_drafted_by = player.drafted_by

        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = player
        mock_search_class.return_value = mock_searcher

        mode_manager._lock_player()

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
            bye_week=18,
            drafted_by="",
            locked=0,
            score=0.0,
            fantasy_points=0.0
        )

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.Constants')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_mark_player_with_extreme_values(
        self, mock_search_class, mock_show_list, mock_constants, mock_player_manager, player_with_extreme_values
    ):
        """Test marking player with boundary/extreme attribute values."""
        mock_constants.FANTASY_TEAM_NAME = "Sea Sharp"
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)

        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = player_with_extreme_values
        mock_search_class.return_value = mock_searcher

        mock_show_list.return_value = 1

        mode_manager._mark_player_as_drafted()

        assert player_with_extreme_values.drafted_by == "Annihilators"
        mock_player_manager.update_players_file.assert_called_once()

    @patch('builtins.print')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_lock_player_multiple_times(self, mock_search_class, mock_print, mock_player_manager, sample_players):
        """Test locking the same player multiple times toggles correctly."""
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        player = sample_players[0]

        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = player
        mock_search_class.return_value = mock_searcher

        mode_manager._lock_player()
        assert player.locked == 1

        mode_manager._lock_player()
        assert player.locked == 0

        mode_manager._lock_player()
        assert player.locked == 1

        assert mock_player_manager.update_players_file.call_count == 3


class TestMarkPlayerAsDraftedTeamMenuSources:
    """Test suite for where the TEAM SELECTION menu's team list comes from (T80)."""

    CONFIGURED_OPPONENTS = [
        "Fishoutawater",
        "Chase-ing points",
        "Annihilators",
        "The Injury Report",
        "Striking Shibas",
        "Bo Him-ian Rhapsody",
        "Saquon Deez",
        "The Eskimo Brothers",
        "Pidgin",
    ]

    @pytest.fixture
    def undrafted_players(self):
        """Create sample players with NO drafted_by value - the start-of-draft state."""
        return [
            FantasyPlayer(id=1, name="Patrick Mahomes", team="KC", position="QB", bye_week=7, drafted_by="", locked=0, score=95.0, fantasy_points=350.0),
            FantasyPlayer(id=2, name="Tyreek Hill", team="MIA", position="WR", bye_week=8, drafted_by="", locked=0, score=85.0, fantasy_points=280.0),
        ]

    @pytest.fixture
    def undrafted_player_manager(self, undrafted_players):
        """Create mock PlayerManager whose whole pool is undrafted."""
        manager = Mock()
        manager.players = undrafted_players
        manager.update_players_file = Mock()
        manager.config.opponent_teams = list(self.CONFIGURED_OPPONENTS)
        return manager

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.Constants')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_team_menu_lists_full_league_when_no_player_is_drafted(
        self, mock_search_class, mock_show_list, mock_constants, undrafted_player_manager, undrafted_players
    ):
        """Test that a fully-undrafted pool still offers every configured opponent plus the user's team."""
        mock_constants.FANTASY_TEAM_NAME = "Sea Sharp"
        mode_manager = ModifyPlayerDataModeManager(undrafted_player_manager)

        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = undrafted_players[0]
        mock_search_class.return_value = mock_searcher

        # Index 1 is valid for a menu of any non-empty length, so this test does not
        # depend on the menu's length and never reaches the unvalidated index path.
        mock_show_list.return_value = 1

        mode_manager._mark_player_as_drafted()

        offered_teams = mock_show_list.call_args[0][1]
        assert offered_teams == sorted(self.CONFIGURED_OPPONENTS + ["Sea Sharp"])

    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.Constants')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch')
    def test_team_menu_unions_configured_opponents_with_data_present_names(
        self, mock_search_class, mock_show_list, mock_constants, undrafted_player_manager, undrafted_players
    ):
        """Test that a data-only team name survives and an overlapping name is not duplicated."""
        # "Saint Nix" is data-only (never configured); "Annihilators" is in BOTH sources.
        undrafted_players[0].drafted_by = "Saint Nix"
        undrafted_players[1].drafted_by = "Annihilators"
        mock_constants.FANTASY_TEAM_NAME = "Sea Sharp"
        mode_manager = ModifyPlayerDataModeManager(undrafted_player_manager)

        mock_searcher = Mock()
        mock_searcher.interactive_search.return_value = undrafted_players[0]
        mock_search_class.return_value = mock_searcher

        mock_show_list.return_value = 1

        mode_manager._mark_player_as_drafted()

        offered_teams = mock_show_list.call_args[0][1]
        assert offered_teams == sorted(self.CONFIGURED_OPPONENTS + ["Sea Sharp", "Saint Nix"])
        assert offered_teams.count("Annihilators") == 1
        assert len(offered_teams) == len(set(offered_teams))


