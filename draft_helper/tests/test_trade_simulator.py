#!/usr/bin/env python3
"""
Unit tests for Trade Simulator functionality

Author: Kai Mizuno
Last Updated: September 2025
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from FantasyTeam import FantasyTeam
from core.trade_simulator import TradeSimulator
from shared_files.FantasyPlayer import FantasyPlayer
import draft_helper_constants as Constants


class TestTradeSimulator(unittest.TestCase):
    """Test cases for Trade Simulator functionality"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        # Create mock players
        self.mock_players = []

        # Create roster players (drafted=2)
        self.qb1 = FantasyPlayer("mahomes_qb_kc", "Mahomes", "KC", "QB", 200.0)
        self.qb1.drafted = 2

        self.rb1 = FantasyPlayer("hunt_rb_kc", "Hunt", "KC", "RB", 180.0)
        self.rb1.drafted = 2

        # Create available players (drafted=0)
        self.qb_available = FantasyPlayer("allen_qb_buf", "Allen", "BUF", "QB", 220.0)
        self.qb_available.drafted = 0

        self.rb_available = FantasyPlayer("taylor_rb_ind", "Taylor", "IND", "RB", 200.0)
        self.rb_available.drafted = 0

        # Create drafted by others players (drafted=1)
        self.qb_drafted = FantasyPlayer("herbert_qb_lac", "Herbert", "LAC", "QB", 210.0)
        self.qb_drafted.drafted = 1

        self.all_players = [
            self.qb1, self.rb1, self.qb_available,
            self.rb_available, self.qb_drafted
        ]

        # Create team with roster
        self.team = FantasyTeam([self.qb1, self.rb1])

        # Mock scoring function
        self.mock_scoring_function = Mock()
        self.mock_scoring_function.side_effect = lambda player: player.fantasy_points

        # Mock logger
        self.mock_logger = Mock()

        # Create trade simulator
        self.trade_simulator = TradeSimulator(
            team=self.team,
            all_players=self.all_players,
            scoring_function=self.mock_scoring_function,
            logger=self.mock_logger
        )

    def test_trade_simulator_initialization(self):
        """Test TradeSimulator initializes correctly"""
        self.assertEqual(self.trade_simulator.team, self.team)
        self.assertEqual(self.trade_simulator.all_players, self.all_players)
        self.assertEqual(len(self.trade_simulator.trade_history), 0)

        # Check that original state is captured
        self.assertIsNotNone(self.trade_simulator.original_state)
        self.assertIsNotNone(self.trade_simulator.original_player_states)

    def test_calculate_original_score(self):
        """Test calculation of original roster score"""
        original_score = self.trade_simulator._calculate_original_score()
        expected_score = self.qb1.fantasy_points + self.rb1.fantasy_points
        self.assertEqual(original_score, expected_score)

    def test_calculate_original_position_scores(self):
        """Test calculation of original position breakdown"""
        position_scores = self.trade_simulator._calculate_original_position_scores()

        self.assertEqual(position_scores['QB'], self.qb1.fantasy_points)
        self.assertEqual(position_scores['RB'], self.rb1.fantasy_points)
        self.assertEqual(position_scores['WR'], 0.0)  # No WR players

    def test_validate_trade_compatibility_same_position(self):
        """Test trade validation for same position trades"""
        # Should be valid: QB for QB
        is_valid = self.trade_simulator._validate_trade_compatibility(
            self.qb1, self.qb_available
        )
        self.assertTrue(is_valid)

    def test_validate_trade_compatibility_different_position(self):
        """Test trade validation for different position trades"""
        # Should be invalid: QB for RB (unless FLEX eligible)
        is_valid = self.trade_simulator._validate_trade_compatibility(
            self.qb1, self.rb_available
        )
        self.assertFalse(is_valid)

    @patch('builtins.input', side_effect=['4'])  # Exit option
    @patch('builtins.print')
    def test_run_trade_simulator_empty_roster(self, mock_print, mock_input):
        """Test trade simulator with empty roster"""
        empty_team = FantasyTeam([])
        empty_simulator = TradeSimulator(
            team=empty_team,
            all_players=self.all_players,
            scoring_function=self.mock_scoring_function,
            logger=self.mock_logger
        )

        empty_simulator.run_trade_simulator()

        # Should print empty roster message
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any("No players in roster" in call for call in print_calls))

    def test_execute_simulated_trade_success(self):
        """Test successful execution of a simulated trade"""
        # Mock team.replace_player to return True
        with patch.object(self.team, 'replace_player', return_value=True):
            success = self.trade_simulator._execute_simulated_trade(
                self.qb1, self.qb_available
            )

            self.assertTrue(success)
            self.assertEqual(len(self.trade_simulator.trade_history), 1)

            # Check trade history
            trade = self.trade_simulator.trade_history[0]
            self.assertEqual(trade['player_out'], self.qb1)
            self.assertEqual(trade['player_in'], self.qb_available)

    def test_execute_simulated_trade_failure(self):
        """Test failed execution of a simulated trade"""
        # Mock team.replace_player to return False
        with patch.object(self.team, 'replace_player', return_value=False):
            success = self.trade_simulator._execute_simulated_trade(
                self.qb1, self.qb_available
            )

            self.assertFalse(success)
            self.assertEqual(len(self.trade_simulator.trade_history), 0)

    def test_undo_last_trade_success(self):
        """Test successful undo of last trade"""
        # First execute a trade
        with patch.object(self.team, 'replace_player', return_value=True):
            self.trade_simulator._execute_simulated_trade(self.qb1, self.qb_available)

        # Then undo it
        with patch.object(self.team, 'replace_player', return_value=True):
            self.trade_simulator._undo_last_trade()

            self.assertEqual(len(self.trade_simulator.trade_history), 0)

    def test_undo_last_trade_no_trades(self):
        """Test undo when no trades have been made"""
        with patch('builtins.print') as mock_print:
            self.trade_simulator._undo_last_trade()
            mock_print.assert_called_with("No trades to undo.")

    def test_reset_to_original_no_trades(self):
        """Test reset when no trades have been made"""
        with patch('builtins.print') as mock_print:
            self.trade_simulator._reset_to_original()
            mock_print.assert_called_with("Roster is already in original state.")

    def test_reset_to_original_with_trades(self):
        """Test reset after trades have been made"""
        # Execute a trade first
        with patch.object(self.team, 'replace_player', return_value=True):
            self.trade_simulator._execute_simulated_trade(self.qb1, self.qb_available)

        # Then reset
        with patch('builtins.print') as mock_print:
            self.trade_simulator._reset_to_original()

            # Should clear trade history
            self.assertEqual(len(self.trade_simulator.trade_history), 0)

            # Should print reset message
            mock_print.assert_called_with("Roster reset to original state.")

    def test_restore_original_state(self):
        """Test restoration of original state on exit"""
        # Execute a trade to change state
        with patch.object(self.team, 'replace_player', return_value=True):
            self.trade_simulator._execute_simulated_trade(self.qb1, self.qb_available)

        # Restore original state
        self.trade_simulator._restore_original_state()

        # Check that logger was called
        self.mock_logger.info.assert_called_with(
            "Trade simulator: original state restored on exit"
        )

    def test_roster_calculator_integration(self):
        """Test integration with RosterCalculator"""
        # Test that roster calculator is properly initialized
        self.assertIsNotNone(self.trade_simulator.roster_calculator)

        # Test display methods work
        with patch('builtins.print'):
            roster_list = self.trade_simulator.roster_calculator.display_numbered_roster()
            self.assertEqual(len(roster_list), 2)  # Should have 2 players

    def test_player_search_integration(self):
        """Test integration with PlayerSearch"""
        # Test that player search is properly initialized
        self.assertIsNotNone(self.trade_simulator.player_search)

        # Test search functionality
        matches = self.trade_simulator.player_search.search_players_by_name(
            "Allen", drafted_filter=0
        )
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0], self.qb_available)

    def test_search_for_replacement_player_integration(self):
        """Test search for replacement player functionality"""
        # Mock the search process
        with patch('builtins.input', side_effect=['back']):  # Cancel search
            result = self.trade_simulator._search_for_replacement_player(self.qb1)
            self.assertIsNone(result)

    @patch('builtins.input', side_effect=['4'])  # Exit option
    @patch('builtins.print')
    def test_show_simulator_menu(self, mock_print, mock_input):
        """Test simulator menu display and choice handling"""
        choice = self.trade_simulator._show_simulator_menu()
        self.assertEqual(choice, 4)

    def test_menu_options_validation(self):
        """Test that all required menu options are implemented"""
        # Test invalid menu choice
        with patch('builtins.input', side_effect=['invalid']):
            choice = self.trade_simulator._show_simulator_menu()
            self.assertEqual(choice, -1)

    def test_state_management_consistency(self):
        """Test that state management maintains consistency"""
        original_roster_size = len(self.team.roster)
        original_player_count = len([p for p in self.all_players if p.drafted == 2])

        # Execute and undo a trade
        with patch.object(self.team, 'replace_player', return_value=True):
            self.trade_simulator._execute_simulated_trade(self.qb1, self.qb_available)
            self.trade_simulator._undo_last_trade()

        # State should be restored
        final_roster_size = len(self.team.roster)
        final_player_count = len([p for p in self.all_players if p.drafted == 2])

        self.assertEqual(original_roster_size, final_roster_size)
        self.assertEqual(original_player_count, final_player_count)


class TestTradeSimulatorError(unittest.TestCase):
    """Test error handling in Trade Simulator"""

    def test_trade_simulator_with_invalid_team(self):
        """Test trade simulator with invalid team object"""
        with self.assertRaises(AttributeError):
            TradeSimulator(
                team=None,
                all_players=[],
                scoring_function=lambda x: 0,
                logger=None
            )

    def test_trade_simulator_with_invalid_players(self):
        """Test trade simulator with invalid players list"""
        team = FantasyTeam([])
        simulator = TradeSimulator(
            team=team,
            all_players=None,
            scoring_function=lambda x: 0,
            logger=None
        )

        # Should handle None players list gracefully
        self.assertIsNotNone(simulator)


if __name__ == '__main__':
    unittest.main()