"""
Tests for ModifyPlayerDataModeManager.

Author: Kai Mizuno
"""

import re
import pytest
from io import StringIO
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


class TestStartInteractiveModeLoop:
    """Test suite for start_interactive_mode()'s loop control flow (T81)."""

    @pytest.fixture
    def mock_player_manager(self):
        """Create a mock PlayerManager sufficient to enter the mode loop."""
        manager = Mock()
        manager.players = []
        manager.update_players_file = Mock()
        manager.config.opponent_teams = ["Annihilators"]
        return manager

    @patch('builtins.print')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    def test_eof_terminates_the_loop_rather_than_reprompting_forever(
        self, mock_show_list, mock_print, mock_player_manager
    ):
        """Test that EOF on stdin breaks the mode loop instead of looping unboundedly.

        This is a TERMINATION test, and it is deliberately built so the mock CANNOT
        supply the exit. `side_effect` is an unbounded generator raising EOFError on
        every call, so if the loop ever treats EOF as recoverable and `continue`s, this
        test hangs rather than passing -- which is exactly the regression it guards.

        The sibling recoverable-error test above cannot catch that: its finite
        side_effect list means termination always comes from the mock running out, so
        it would stay green against an unbounded loop.
        """
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        mode_manager.logger = Mock()

        def _always_eof(*args, **kwargs):
            raise EOFError("EOF when reading a line")

        mock_show_list.side_effect = _always_eof

        mode_manager.start_interactive_mode(mock_player_manager)

        # Exactly one call: EOF is terminal, so there is no second prompt.
        assert mock_show_list.call_count == 1
        printed = " ".join(str(c) for c in mock_print.call_args_list)
        assert "Input stream closed" in printed
        # The broad recoverable-error path must NOT have handled it.
        assert "Error in Modify Player Data mode" not in printed

    @patch('builtins.print')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    def test_recoverable_error_reprompts_instead_of_exiting_the_mode(
        self, mock_show_list, mock_print, mock_player_manager
    ):
        """Test that an exception inside the loop re-prompts rather than ejecting the user"""
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        mode_manager.logger = Mock()
        mode_manager._mark_player_as_drafted = Mock(side_effect=RuntimeError("boom"))

        mock_show_list.side_effect = [1, 4]

        mode_manager.start_interactive_mode(mock_player_manager)

        # Two menu renders: the failing attempt, then the re-prompt the fix introduces.
        # Pre-fix this was 1 - the broad handler broke out of the whole mode.
        assert mock_show_list.call_count == 2
        mode_manager._mark_player_as_drafted.assert_called_once()
        printed = " ".join(str(c) for c in mock_print.call_args_list)
        assert "Error in Modify Player Data mode: boom" in printed
        mode_manager.logger.error.assert_called_once_with(
            "Error in Modify Player Data mode: boom"
        )

    @patch('builtins.print')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    def test_repeated_recoverable_errors_keep_reprompting(
        self, mock_show_list, mock_print, mock_player_manager
    ):
        """Test that consecutive errors each re-prompt rather than compounding into an exit

        NOT termination coverage. The `side_effect` list is FINITE, so the exit always
        comes from the mock running out, never from the code under test -- this test
        stays green against a loop that can never terminate. Termination is pinned
        separately by `test_eof_terminates_the_loop_rather_than_reprompting_forever`,
        which uses an unbounded side_effect so only a `break` can end the loop.
        """
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        mode_manager.logger = Mock()
        mode_manager._mark_player_as_drafted = Mock(side_effect=RuntimeError("boom"))

        mock_show_list.side_effect = [1, 1, 4]

        mode_manager.start_interactive_mode(mock_player_manager)

        assert mock_show_list.call_count == 3
        assert mode_manager._mark_player_as_drafted.call_count == 2
        assert mode_manager.logger.error.call_count == 2

    @patch('builtins.print')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    def test_keyboard_interrupt_still_exits_the_mode(
        self, mock_show_list, mock_print, mock_player_manager
    ):
        """Test that Ctrl+C still breaks out of the mode (unchanged by the continue fix)"""
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        mode_manager.logger = Mock()

        mock_show_list.side_effect = KeyboardInterrupt()

        mode_manager.start_interactive_mode(mock_player_manager)

        assert mock_show_list.call_count == 1
        printed = " ".join(str(c) for c in mock_print.call_args_list)
        assert "Returning to Main Menu..." in printed

    @patch('builtins.print')
    @patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.show_list_selection')
    def test_return_to_main_menu_option_exits_the_mode(
        self, mock_show_list, mock_print, mock_player_manager
    ):
        """Test that the user's own exit option still leaves the mode on the first pass"""
        mode_manager = ModifyPlayerDataModeManager(mock_player_manager)
        mode_manager.logger = Mock()

        mock_show_list.side_effect = [4]

        mode_manager.start_interactive_mode(mock_player_manager)

        assert mock_show_list.call_count == 1
        printed = " ".join(str(c) for c in mock_print.call_args_list)
        assert "Returning to Main Menu..." in printed


class TestTeamSelectionRejectsOutOfRangeWithoutWriting:
    """Test that an out-of-range TEAM SELECTION index never reaches update_players_file (T81).

    These cases deliberately do NOT patch show_list_selection - they patch builtins.input
    so the REAL helper loop runs. The suite's other caller-side tests patch the helper
    wholesale, so they never exercise its validation and are not coverage of this fix.
    """

    @pytest.fixture
    def available_player(self):
        """Create a single undrafted player for the mark-as-drafted path."""
        return FantasyPlayer(id=1, name="Patrick Mahomes", team="KC", position="QB",
                             bye_week=7, drafted_by="", locked=0, score=95.0,
                             fantasy_points=350.0)

    @pytest.fixture
    def mock_player_manager(self, available_player):
        """Create a mock PlayerManager - update_players_file is a Mock, so no file is written."""
        manager = Mock()
        manager.players = [available_player]
        manager.update_players_file = Mock()
        manager.config.opponent_teams = ["Annihilators", "Pidgin", "Striking Shibas"]
        manager.config.max_search_results = 10
        return manager

    @staticmethod
    def _answer_then_cancel(queued):
        """Answer with the queued values, then the Cancel sentinel.

        The sentinel is read out of the prompt the helper actually rendered
        ("Enter your choice (1-N): "), so no menu length is ever hard-coded and
        the union of configured + data-present team names is never re-implemented.
        """
        pending = list(queued)

        def _answer(prompt):
            if pending:
                return pending.pop(0)
            match = re.search(r"\(1-(\d+)\)", prompt)
            assert match, f"unexpected prompt: {prompt!r}"
            return match.group(1)

        return _answer

    def _run(self, mock_player_manager, available_player, queued):
        """Drive _mark_player_as_drafted with the real helper and the queued inputs."""
        with patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.Constants') as mock_constants, \
             patch('league_helper.modify_player_data_mode.ModifyPlayerDataModeManager.PlayerSearch') as mock_search_class, \
             patch('builtins.input', side_effect=self._answer_then_cancel(queued)), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            mock_constants.FANTASY_TEAM_NAME = "Sea Sharp"
            mock_searcher = Mock()
            mock_searcher.interactive_search.return_value = available_player
            mock_search_class.return_value = mock_searcher

            ModifyPlayerDataModeManager(mock_player_manager)._mark_player_as_drafted()

            return mock_stdout.getvalue()

    def test_zero_at_team_selection_persists_nothing(self, mock_player_manager, available_player):
        """Test that entering 0 at TEAM SELECTION writes nothing (pre-fix it wrote the last team)"""
        output = self._run(mock_player_manager, available_player, ['0'])

        assert available_player.drafted_by == ""
        mock_player_manager.update_players_file.assert_not_called()
        assert "Invalid choice. Please try again." in output
        assert "as drafted by" not in output

    def test_high_out_of_range_at_team_selection_persists_nothing(self, mock_player_manager, available_player):
        """Test that a too-high index writes nothing and raises nothing (pre-fix it raised IndexError)"""
        output = self._run(mock_player_manager, available_player, ['99'])

        assert available_player.drafted_by == ""
        mock_player_manager.update_players_file.assert_not_called()
        assert "Invalid choice. Please try again." in output
        assert "as drafted by" not in output

    def test_cancel_sentinel_still_cancels_without_writing(self, mock_player_manager, available_player):
        """Test that the Cancel sentinel still cancels cleanly with no retry message"""
        output = self._run(mock_player_manager, available_player, [])

        assert available_player.drafted_by == ""
        mock_player_manager.update_players_file.assert_not_called()
        assert "Cancelled." in output
        assert "Invalid choice. Please try again." not in output

    def test_valid_team_index_still_persists(self, mock_player_manager, available_player):
        """Test the positive control - a valid index still marks and saves exactly once"""
        output = self._run(mock_player_manager, available_player, ['1'])

        # Sorted union of config + FANTASY_TEAM_NAME: Annihilators, Pidgin, Sea Sharp, Striking Shibas
        assert available_player.drafted_by == "Annihilators"
        mock_player_manager.update_players_file.assert_called_once()
        assert "as drafted by Annihilators" in output
        assert "Invalid choice. Please try again." not in output


