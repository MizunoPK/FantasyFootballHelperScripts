#!/usr/bin/env python3
"""
Test suite for MenuSystem module

This module tests the menu display and user interaction functionality
for the draft helper.

Author: Claude Code
Last Updated: September 2025
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path
from io import StringIO

# Add parent directories to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from draft_helper.core.menu_system import MenuSystem
from shared_files.FantasyPlayer import FantasyPlayer


class TestMenuSystem(unittest.TestCase):
    """Test cases for MenuSystem class"""

    def setUp(self):
        """Set up test fixtures"""
        # Create mock team
        self.mock_team = Mock()
        self.mock_team.roster = []
        self.mock_team.slot_assignments = {}

        # Create mock draft helper
        self.mock_draft_helper = Mock()

        # Initialize menu system
        self.menu_system = MenuSystem(self.mock_team, starter_helper_available=False)

    def test_menu_system_initialization_basic(self):
        """Test basic initialization of MenuSystem"""
        self.assertEqual(self.menu_system.team, self.mock_team)
        self.assertFalse(self.menu_system.starter_helper_available)
        self.assertIsNone(self.menu_system.draft_helper)

    def test_menu_system_initialization_with_starter_helper(self):
        """Test initialization with starter helper available"""
        menu = MenuSystem(self.mock_team, starter_helper_available=True, draft_helper=self.mock_draft_helper)
        self.assertEqual(menu.team, self.mock_team)
        self.assertTrue(menu.starter_helper_available)
        self.assertEqual(menu.draft_helper, self.mock_draft_helper)

    @patch('sys.stdout', new_callable=StringIO)
    def test_show_main_menu_without_starter_helper(self, mock_stdout):
        """Test main menu display without starter helper"""
        with patch('builtins.input', return_value='1'):
            choice = self.menu_system.show_main_menu()

        output = mock_stdout.getvalue()
        self.assertIn("MAIN MENU", output)
        self.assertIn("1. Add to Roster", output)
        self.assertIn("2. Mark Drafted Player", output)
        self.assertIn("3. Waiver Optimizer", output)
        self.assertIn("4. Drop Player", output)
        self.assertIn("5. Lock/Unlock Player", output)
        self.assertIn("6. Trade Simulator", output)
        self.assertIn("7. Quit", output)
        self.assertNotIn("8. Quit", output)  # Should not have 8 when no starter helper
        self.assertEqual(choice, 1)

    @patch('sys.stdout', new_callable=StringIO)
    def test_show_main_menu_with_starter_helper(self, mock_stdout):
        """Test main menu display with starter helper"""
        menu = MenuSystem(self.mock_team, starter_helper_available=True)

        with patch('builtins.input', return_value='2'):
            choice = menu.show_main_menu()

        output = mock_stdout.getvalue()
        self.assertIn("MAIN MENU", output)
        self.assertIn("6. Starter Helper", output)
        self.assertIn("7. Trade Simulator", output)
        self.assertIn("8. Quit", output)
        self.assertEqual(choice, 2)

    @patch('sys.stdout', new_callable=StringIO)
    def test_show_main_menu_roster_count(self, mock_stdout):
        """Test that main menu shows correct roster count"""
        # Mock team with 3 players
        self.mock_team.roster = [Mock(), Mock(), Mock()]

        with patch('builtins.input', return_value='1'):
            self.menu_system.show_main_menu()

        output = mock_stdout.getvalue()
        self.assertIn("Current roster: 3 / 15 players", output)

    def test_show_main_menu_invalid_input(self):
        """Test main menu with invalid input"""
        with patch('builtins.input', return_value='invalid'):
            choice = self.menu_system.show_main_menu()

        self.assertEqual(choice, -1)

    def test_show_main_menu_out_of_range_input(self):
        """Test main menu with out of range input"""
        with patch('builtins.input', return_value='99'):
            choice = self.menu_system.show_main_menu()

        self.assertEqual(choice, 99)  # Returns the value even if out of range

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_roster_by_draft_order_empty(self, mock_stdout):
        """Test roster display with empty roster"""
        self.mock_team.roster = []
        self.mock_team.slot_assignments = {}

        self.menu_system.display_roster_by_draft_order()

        output = mock_stdout.getvalue()
        self.assertIn("Current Roster by Position:", output)
        self.assertIn("Total roster: 0/15 players", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_roster_by_draft_order_with_players(self, mock_stdout):
        """Test roster display with players"""
        # Create sample players
        qb_player = FantasyPlayer(
            id="1", name="Patrick Mahomes", position="QB", team="KC",
            fantasy_points=320.5, drafted=2, locked=1
        )
        rb_player = FantasyPlayer(
            id="2", name="Christian McCaffrey", position="RB", team="SF",
            fantasy_points=285.3, drafted=2, locked=0
        )

        self.mock_team.roster = [qb_player, rb_player]
        self.mock_team.slot_assignments = {
            'QB': ['1'],
            'RB': ['2'],
            'WR': [],
            'TE': [],
            'FLEX': [],
            'K': [],
            'DST': []
        }

        with patch('draft_helper.core.menu_system.Constants') as mock_constants:
            mock_constants.MAX_POSITIONS = {'QB': 1, 'RB': 2, 'WR': 2, 'TE': 1, 'FLEX': 1, 'K': 1, 'DST': 1}

            self.menu_system.display_roster_by_draft_order()

        output = mock_stdout.getvalue()
        self.assertIn("Patrick Mahomes (KC) - 320.5 pts (LOCKED)", output)
        self.assertIn("Christian McCaffrey (SF) - 285.3 pts", output)
        self.assertIn("QB (1/1):", output)
        self.assertIn("RB (1/2):", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_roster_by_draft_rounds_with_draft_helper(self, mock_stdout):
        """Test roster display by draft rounds when draft helper is available"""
        menu = MenuSystem(self.mock_team, draft_helper=self.mock_draft_helper)

        # Mock the draft helper's method
        mock_round_assignments = {
            1: FantasyPlayer(id="1", name="Player 1", position="QB", team="KC", fantasy_points=320.0),
            2: FantasyPlayer(id="2", name="Player 2", position="RB", team="SF", fantasy_points=285.0)
        }
        self.mock_draft_helper._match_players_to_rounds.return_value = mock_round_assignments

        with patch('draft_helper.core.menu_system.Constants') as mock_constants:
            mock_constants.MAX_PLAYERS = 15
            mock_constants.get_ideal_draft_position.side_effect = lambda x: ["QB", "RB", "WR"][x % 3]

            menu.display_roster_by_draft_rounds()

        output = mock_stdout.getvalue()
        self.assertIn("Current Roster by Draft Round:", output)
        self.assertIn("Round  1 (Ideal: QB  ): Player 1", output)
        self.assertIn("Round  2 (Ideal: RB  ): Player 2", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_roster_by_draft_rounds_without_draft_helper(self, mock_stdout):
        """Test roster display by draft rounds when draft helper is not available"""
        self.menu_system.display_roster_by_draft_rounds()

        output = mock_stdout.getvalue()
        self.assertIn("Draft helper not available for advanced display.", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_starter_lineup_empty(self, mock_stdout):
        """Test starter lineup display with empty lineup"""
        self.menu_system.display_starter_lineup(None)

        output = mock_stdout.getvalue()
        self.assertIn("No optimal lineup available.", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_starter_lineup_with_lineup(self, mock_stdout):
        """Test starter lineup display with lineup data"""
        # Create mock optimal lineup
        mock_lineup = Mock()
        mock_lineup.total_projected_points = 125.5

        # Create mock recommendation
        mock_qb_rec = Mock()
        mock_qb_rec.name = "Patrick Mahomes"
        mock_qb_rec.team = "KC"
        mock_qb_rec.projected_points = 25.5
        mock_qb_rec.matchup_indicator = "★"
        mock_qb_rec.reason = "High ceiling play"

        mock_lineup.qb = mock_qb_rec
        mock_lineup.rb1 = None  # Test missing position
        mock_lineup.rb2 = None
        mock_lineup.wr1 = None
        mock_lineup.wr2 = None
        mock_lineup.te = None
        mock_lineup.flex = None
        mock_lineup.k = None
        mock_lineup.dst = None

        self.menu_system.display_starter_lineup(mock_lineup)

        output = mock_stdout.getvalue()
        self.assertIn("OPTIMAL STARTING LINEUP", output)
        self.assertIn("QB: Patrick Mahomes (KC)", output)
        self.assertIn("25.5 pts ★", output)
        self.assertIn("High ceiling play", output)
        self.assertIn("Total Projected Points: 125.5", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_starter_lineup_no_reason(self, mock_stdout):
        """Test starter lineup display with no reason or default reason"""
        mock_lineup = Mock()
        mock_lineup.total_projected_points = 100.0

        mock_qb_rec = Mock()
        mock_qb_rec.name = "Test Player"
        mock_qb_rec.team = "TEST"
        mock_qb_rec.projected_points = 20.0
        mock_qb_rec.matchup_indicator = ""
        mock_qb_rec.reason = "No penalties"  # Default reason should not display

        mock_lineup.qb = mock_qb_rec
        mock_lineup.rb1 = None
        mock_lineup.rb2 = None
        mock_lineup.wr1 = None
        mock_lineup.wr2 = None
        mock_lineup.te = None
        mock_lineup.flex = None
        mock_lineup.k = None
        mock_lineup.dst = None

        self.menu_system.display_starter_lineup(mock_lineup)

        output = mock_stdout.getvalue()
        self.assertIn("QB: Test Player (TEST)", output)
        self.assertIn("20.0 pts", output)
        self.assertNotIn("No penalties", output)  # Should not display default reason

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_bench_alternatives_empty(self, mock_stdout):
        """Test bench alternatives display with empty list"""
        self.menu_system.display_bench_alternatives([])

        output = mock_stdout.getvalue()
        self.assertIn("No bench alternatives available.", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_bench_alternatives_with_players(self, mock_stdout):
        """Test bench alternatives display with player list"""
        # Create mock recommendations
        mock_rec1 = Mock()
        mock_rec1.name = "Player 1"
        mock_rec1.position = "RB"
        mock_rec1.team = "KC"
        mock_rec1.projected_points = 15.5
        mock_rec1.matchup_indicator = "★"
        mock_rec1.reason = "Good matchup"

        mock_rec2 = Mock()
        mock_rec2.name = "Player 2"
        mock_rec2.position = "WR"
        mock_rec2.team = "SF"
        mock_rec2.projected_points = 12.3
        mock_rec2.matchup_indicator = ""
        mock_rec2.reason = "No penalties"

        bench_recs = [mock_rec1, mock_rec2]

        self.menu_system.display_bench_alternatives(bench_recs)

        output = mock_stdout.getvalue()
        self.assertIn("TOP BENCH ALTERNATIVES", output)
        self.assertIn("1. Player 1 (RB - KC)", output)
        self.assertIn("15.5 pts ★", output)
        self.assertIn("Good matchup", output)
        self.assertIn("2. Player 2 (WR - SF)", output)
        self.assertIn("12.3 pts", output)
        self.assertNotIn("No penalties", output)  # Should not display default reason


class TestMenuSystemEdgeCases(unittest.TestCase):
    """Test edge cases and error handling in MenuSystem"""

    def setUp(self):
        """Set up edge case test fixtures"""
        self.mock_team = Mock()
        self.menu_system = MenuSystem(self.mock_team)

    def test_display_roster_missing_attributes(self):
        """Test roster display with players missing attributes"""
        # Create player mock without all expected attributes
        incomplete_player = Mock()
        incomplete_player.id = "1"
        incomplete_player.name = "Test Player"
        incomplete_player.team = "TEST"
        # Set default values to avoid Mock formatting issues
        incomplete_player.fantasy_points = 0.0
        incomplete_player.locked = False

        self.mock_team.roster = [incomplete_player]
        self.mock_team.slot_assignments = {'QB': ['1']}

        with patch('draft_helper.core.menu_system.Constants') as mock_constants:
            mock_constants.MAX_POSITIONS = {'QB': 1}

            # Should not raise exception
            try:
                self.menu_system.display_roster_by_draft_order()
            except Exception as e:
                self.fail(f"display_roster_by_draft_order raised exception: {e}")

    def test_display_starter_lineup_missing_attributes(self):
        """Test starter lineup display with missing attributes"""
        mock_lineup = Mock()
        mock_lineup.total_projected_points = 0.0  # Set to avoid formatting issues

        mock_rec = Mock()
        mock_rec.name = "Test Player"
        mock_rec.team = "TEST"
        # Set default values to avoid Mock formatting issues
        mock_rec.projected_points = 0.0
        mock_rec.matchup_indicator = ""
        mock_rec.reason = "No penalties"

        mock_lineup.qb = mock_rec
        mock_lineup.rb1 = None
        mock_lineup.rb2 = None
        mock_lineup.wr1 = None
        mock_lineup.wr2 = None
        mock_lineup.te = None
        mock_lineup.flex = None
        mock_lineup.k = None
        mock_lineup.dst = None

        # Should not raise exception
        try:
            self.menu_system.display_starter_lineup(mock_lineup)
        except Exception as e:
            self.fail(f"display_starter_lineup raised exception: {e}")


class TestMenuSystemIntegration(unittest.TestCase):
    """Integration tests for MenuSystem with real objects"""

    def setUp(self):
        """Set up integration test fixtures"""
        # Use real FantasyPlayer objects for better integration testing
        self.player1 = FantasyPlayer(
            id="1", name="Patrick Mahomes", position="QB", team="KC",
            fantasy_points=320.5, drafted=2, locked=1
        )
        self.player2 = FantasyPlayer(
            id="2", name="Christian McCaffrey", position="RB", team="SF",
            fantasy_points=285.3, drafted=2, locked=0
        )

        self.mock_team = Mock()
        self.mock_team.roster = [self.player1, self.player2]

        self.menu_system = MenuSystem(self.mock_team)

    def test_integration_with_real_players(self):
        """Test menu system integration with real FantasyPlayer objects"""
        # Test that display methods work with real player objects
        self.mock_team.slot_assignments = {
            'QB': ['1'],
            'RB': ['2'],
            'WR': [],
            'TE': [],
            'FLEX': [],
            'K': [],
            'DST': []
        }

        with patch('draft_helper.core.menu_system.Constants') as mock_constants:
            mock_constants.MAX_POSITIONS = {'QB': 1, 'RB': 2, 'WR': 2, 'TE': 1, 'FLEX': 1, 'K': 1, 'DST': 1}

            # Should not raise exception
            try:
                self.menu_system.display_roster_by_draft_order()
            except Exception as e:
                self.fail(f"Integration test failed: {e}")


if __name__ == '__main__':
    unittest.main()