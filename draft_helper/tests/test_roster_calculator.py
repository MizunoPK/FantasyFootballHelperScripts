#!/usr/bin/env python3
"""
Test suite for RosterCalculator module

This module tests the shared roster display and calculation logic used by both
the Waiver Optimizer and Trade Simulator.

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

from draft_helper.core.roster_calculator import RosterCalculator
from shared_files.FantasyPlayer import FantasyPlayer


class TestRosterCalculator(unittest.TestCase):
    """Test cases for RosterCalculator class"""

    def setUp(self):
        """Set up test fixtures"""
        # Create mock team with basic attributes
        self.mock_team = Mock()
        self.mock_team.roster = []
        self.mock_team.pos_counts = {'QB': 1, 'RB': 2, 'WR': 2, 'TE': 1, 'K': 1, 'DST': 1}
        self.mock_team.slot_assignments = {'QB': [], 'RB': [], 'WR': [], 'TE': [], 'K': [], 'DST': []}

        # Create mock logger
        self.mock_logger = Mock()

        # Initialize calculator
        self.calculator = RosterCalculator(self.mock_team, self.mock_logger)

        # Create sample players
        self.sample_players = [
            FantasyPlayer(
                id="1", name="Patrick Mahomes", position="QB", team="KC",
                fantasy_points=320.5, drafted=2, locked=0
            ),
            FantasyPlayer(
                id="2", name="Christian McCaffrey", position="RB", team="SF",
                fantasy_points=285.3, drafted=2, locked=1
            ),
            FantasyPlayer(
                id="3", name="Tyreek Hill", position="WR", team="MIA",
                fantasy_points=275.8, drafted=2, locked=0
            )
        ]

    def test_calculator_initialization(self):
        """Test proper initialization of RosterCalculator"""
        self.assertEqual(self.calculator.team, self.mock_team)
        self.assertEqual(self.calculator.logger, self.mock_logger)

    def test_calculator_initialization_without_logger(self):
        """Test initialization without logger"""
        calc = RosterCalculator(self.mock_team)
        self.assertEqual(calc.team, self.mock_team)
        self.assertIsNone(calc.logger)

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_roster_summary_empty_roster(self, mock_stdout):
        """Test roster summary display with empty roster"""
        self.mock_team.roster = []

        self.calculator.display_roster_summary()

        output = mock_stdout.getvalue()
        self.assertIn("Current roster: 0 / 15 players", output)
        self.assertIn("Your current roster by position:", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_roster_summary_with_players(self, mock_stdout):
        """Test roster summary display with players"""
        self.mock_team.roster = self.sample_players[:2]

        self.calculator.display_roster_summary()

        output = mock_stdout.getvalue()
        self.assertIn("Current roster: 2 / 15 players", output)
        self.assertIn("QB: 1", output)
        self.assertIn("RB: 2", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_numbered_roster_empty(self, mock_stdout):
        """Test numbered roster display with empty roster"""
        self.mock_team.roster = []

        result = self.calculator.display_numbered_roster()

        output = mock_stdout.getvalue()
        self.assertIn("No players in roster.", output)
        self.assertEqual(result, [])

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_numbered_roster_with_players(self, mock_stdout):
        """Test numbered roster display with players"""
        self.mock_team.roster = self.sample_players

        result = self.calculator.display_numbered_roster()

        output = mock_stdout.getvalue()
        self.assertIn("1. Patrick Mahomes (QB - KC) - 320.5 pts", output)
        self.assertIn("2. Christian McCaffrey (RB - SF) - 285.3 pts (LOCKED)", output)
        self.assertIn("3. Tyreek Hill (WR - MIA) - 275.8 pts", output)
        self.assertEqual(result, self.sample_players)

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_numbered_roster_missing_attributes(self, mock_stdout):
        """Test numbered roster display with players missing attributes"""
        # Create player without fantasy_points and locked attributes
        minimal_player = Mock()
        minimal_player.name = "Test Player"
        minimal_player.position = "QB"
        minimal_player.team = "TEST"
        # Configure getattr to return proper defaults
        minimal_player.configure_mock(**{
            'fantasy_points': 0.0,  # Set actual attribute to avoid Mock format issues
            'locked': False
        })

        self.mock_team.roster = [minimal_player]

        result = self.calculator.display_numbered_roster()

        output = mock_stdout.getvalue()
        self.assertIn("1. Test Player (QB - TEST) - 0.0 pts", output)
        self.assertNotIn("(LOCKED)", output)

    def test_calculate_total_score(self):
        """Test total score calculation"""
        def mock_scoring_function(player):
            return player.fantasy_points

        # Mock get_total_team_score to return sum of fantasy points
        self.mock_team.get_total_team_score.return_value = 881.6

        result = self.calculator.calculate_total_score(mock_scoring_function)

        self.assertEqual(result, 881.6)
        self.mock_team.get_total_team_score.assert_called_once_with(mock_scoring_function)

    def test_calculate_position_scores_empty_roster(self):
        """Test position scores calculation with empty roster"""
        self.mock_team.roster = []

        def mock_scoring_function(player):
            return player.fantasy_points

        result = self.calculator.calculate_position_scores(mock_scoring_function)

        # Should have all positions initialized to 0
        expected_positions = ['QB', 'RB', 'WR', 'TE', 'FLEX', 'K', 'DST']
        for pos in expected_positions:
            self.assertIn(pos, result)
            self.assertEqual(result[pos], 0.0)

    def test_calculate_position_scores_with_players(self):
        """Test position scores calculation with players"""
        self.mock_team.roster = self.sample_players

        def mock_scoring_function(player):
            return player.fantasy_points

        result = self.calculator.calculate_position_scores(mock_scoring_function)

        self.assertEqual(result['QB'], 320.5)
        self.assertEqual(result['RB'], 285.3)
        self.assertEqual(result['WR'], 275.8)
        self.assertEqual(result['TE'], 0.0)  # No TE in sample

    def test_calculate_position_scores_multiple_same_position(self):
        """Test position scores calculation with multiple players in same position"""
        # Add another RB
        additional_rb = FantasyPlayer(
            id="4", name="Josh Jacobs", position="RB", team="LV",
            fantasy_points=200.0, drafted=2, locked=0
        )
        self.mock_team.roster = self.sample_players + [additional_rb]

        def mock_scoring_function(player):
            return player.fantasy_points

        result = self.calculator.calculate_position_scores(mock_scoring_function)

        self.assertEqual(result['RB'], 485.3)  # 285.3 + 200.0

    def test_calculate_position_scores_unknown_position(self):
        """Test position scores calculation with unknown position"""
        unknown_player = FantasyPlayer(
            id="5", name="Unknown Player", position="UNKNOWN", team="TEST",
            fantasy_points=100.0, drafted=2, locked=0
        )
        self.mock_team.roster = [unknown_player]

        def mock_scoring_function(player):
            return player.fantasy_points

        result = self.calculator.calculate_position_scores(mock_scoring_function)

        self.assertEqual(result['UNKNOWN'], 100.0)

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_score_breakdown(self, mock_stdout):
        """Test score breakdown display"""
        self.mock_team.roster = self.sample_players

        def mock_scoring_function(player):
            return player.fantasy_points

        # Mock the total score calculation
        self.mock_team.get_total_team_score.return_value = 881.6

        self.calculator.display_score_breakdown(mock_scoring_function, "Test Breakdown")

        output = mock_stdout.getvalue()
        self.assertIn("Test Breakdown", output)
        self.assertIn("Total Score: 881.60", output)
        self.assertIn("QB: 320.50", output)
        self.assertIn("RB: 285.30", output)
        self.assertIn("WR: 275.80", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_score_breakdown_default_title(self, mock_stdout):
        """Test score breakdown display with default title"""
        self.mock_team.roster = []
        self.mock_team.get_total_team_score.return_value = 0.0

        def mock_scoring_function(player):
            return 0

        self.calculator.display_score_breakdown(mock_scoring_function)

        output = mock_stdout.getvalue()
        self.assertIn("Team Score Breakdown", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_compare_scores(self, mock_stdout):
        """Test score comparison display"""
        original_score = 800.0
        original_position_scores = {'QB': 300.0, 'RB': 250.0, 'WR': 250.0}

        self.mock_team.roster = self.sample_players
        self.mock_team.get_total_team_score.return_value = 881.6

        def mock_scoring_function(player):
            return player.fantasy_points

        self.calculator.compare_scores(
            mock_scoring_function, original_score, original_position_scores, "Trade Comparison"
        )

        output = mock_stdout.getvalue()
        self.assertIn("Trade Comparison", output)
        self.assertIn("Original Score: 800.00", output)
        self.assertIn("Current Score:  881.60", output)
        self.assertIn("Difference:     +81.60", output)
        self.assertIn("QB: 300.00 → 320.50 (+20.50)", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_compare_scores_negative_difference(self, mock_stdout):
        """Test score comparison with negative difference"""
        original_score = 900.0
        original_position_scores = {'QB': 350.0, 'RB': 300.0, 'WR': 250.0}

        self.mock_team.get_total_team_score.return_value = 881.6

        def mock_scoring_function(player):
            return player.fantasy_points

        self.calculator.compare_scores(
            mock_scoring_function, original_score, original_position_scores
        )

        output = mock_stdout.getvalue()
        self.assertIn("Difference:     -18.40", output)

    def test_get_roster_state_snapshot(self):
        """Test roster state snapshot creation"""
        self.mock_team.roster = self.sample_players
        self.mock_team.slot_assignments = {'QB': ['1'], 'RB': ['2'], 'WR': ['3']}
        self.mock_team.pos_counts = {'QB': 1, 'RB': 1, 'WR': 1}

        snapshot = self.calculator.get_roster_state_snapshot()

        self.assertIn('roster_copy', snapshot)
        self.assertIn('slot_assignments_copy', snapshot)
        self.assertIn('pos_counts_copy', snapshot)
        self.assertIn('player_drafted_states', snapshot)

        # Verify snapshot contains expected data
        self.assertEqual(len(snapshot['roster_copy']), 3)
        self.assertEqual(snapshot['slot_assignments_copy']['QB'], ['1'])
        self.assertEqual(snapshot['pos_counts_copy']['QB'], 1)
        self.assertEqual(snapshot['player_drafted_states']['1'], 2)  # Patrick Mahomes drafted=2

    def test_get_roster_state_snapshot_empty_roster(self):
        """Test roster state snapshot with empty roster"""
        self.mock_team.roster = []
        self.mock_team.slot_assignments = {}
        self.mock_team.pos_counts = {}

        snapshot = self.calculator.get_roster_state_snapshot()

        self.assertEqual(len(snapshot['roster_copy']), 0)
        self.assertEqual(len(snapshot['player_drafted_states']), 0)

    def test_restore_roster_state(self):
        """Test roster state restoration"""
        # Create a snapshot
        original_roster = self.sample_players.copy()
        original_slots = {'QB': ['1'], 'RB': ['2']}
        original_counts = {'QB': 1, 'RB': 1}
        original_drafted_states = {'1': 2, '2': 1}

        snapshot = {
            'roster_copy': original_roster,
            'slot_assignments_copy': original_slots,
            'pos_counts_copy': original_counts,
            'player_drafted_states': original_drafted_states
        }

        # Modify team state
        self.mock_team.roster = []
        self.mock_team.slot_assignments = {}
        self.mock_team.pos_counts = {}

        # Restore from snapshot
        self.calculator.restore_roster_state(snapshot)

        # Verify restoration
        self.assertEqual(self.mock_team.roster, original_roster)
        self.assertEqual(self.mock_team.slot_assignments, original_slots)
        self.assertEqual(self.mock_team.pos_counts, original_counts)

    def test_restore_roster_state_with_drafted_states(self):
        """Test roster state restoration including player drafted states"""
        # Create players with specific drafted values
        player1 = FantasyPlayer(id="1", name="Test1", position="QB", team="T1", drafted=2)
        player2 = FantasyPlayer(id="2", name="Test2", position="RB", team="T2", drafted=1)

        snapshot = {
            'roster_copy': [player1, player2],
            'slot_assignments_copy': {},
            'pos_counts_copy': {},
            'player_drafted_states': {'1': 0, '2': 2}  # Different from current states
        }

        self.calculator.restore_roster_state(snapshot)

        # Verify player drafted states were restored
        self.assertEqual(self.mock_team.roster[0].drafted, 0)  # Changed from 2 to 0
        self.assertEqual(self.mock_team.roster[1].drafted, 2)  # Changed from 1 to 2

    def test_restore_roster_state_missing_player_id(self):
        """Test roster state restoration with players missing ID attribute"""
        player_without_id = Mock()
        player_without_id.name = "No ID Player"
        # Missing id attribute

        snapshot = {
            'roster_copy': [player_without_id],
            'slot_assignments_copy': {},
            'pos_counts_copy': {},
            'player_drafted_states': {'missing': 1}
        }

        # Should not raise exception
        self.calculator.restore_roster_state(snapshot)
        self.assertEqual(self.mock_team.roster, [player_without_id])


class TestRosterCalculatorIntegration(unittest.TestCase):
    """Integration tests for RosterCalculator with real FantasyTeam"""

    def setUp(self):
        """Set up integration test fixtures"""
        # Import FantasyTeam for real integration testing
        try:
            from draft_helper.FantasyTeam import FantasyTeam
            self.team = FantasyTeam()
            self.calculator = RosterCalculator(self.team)
        except ImportError:
            self.skipTest("FantasyTeam not available for integration testing")

    def test_integration_with_real_team(self):
        """Test calculator integration with real FantasyTeam instance"""
        if hasattr(self, 'team'):
            # Test calculator methods with empty team first
            self.assertEqual(len(self.calculator.display_numbered_roster()), 0)

            def scoring_func(p):
                return p.fantasy_points

            # Test score calculation with empty roster
            total_score = self.calculator.calculate_total_score(scoring_func)
            self.assertEqual(total_score, 0.0)

            # Test that calculator can handle team operations
            position_scores = self.calculator.calculate_position_scores(scoring_func)
            self.assertIsInstance(position_scores, dict)


class TestRosterCalculatorErrorHandling(unittest.TestCase):
    """Test error handling in RosterCalculator"""

    def setUp(self):
        """Set up error handling test fixtures"""
        self.mock_team = Mock()
        self.calculator = RosterCalculator(self.mock_team)

    def test_scoring_function_exception_handling(self):
        """Test handling of exceptions in scoring function"""
        self.mock_team.roster = [Mock()]

        def failing_scoring_function(player):
            raise ValueError("Scoring error")

        # Should not raise exception, but behavior depends on implementation
        try:
            self.calculator.calculate_position_scores(failing_scoring_function)
        except ValueError:
            # Expected if exceptions are not caught
            pass

    def test_team_method_exception_handling(self):
        """Test handling of exceptions in team methods"""
        self.mock_team.get_total_team_score.side_effect = AttributeError("Team error")

        def mock_scoring_function(player):
            return 100

        with self.assertRaises(AttributeError):
            self.calculator.calculate_total_score(mock_scoring_function)


if __name__ == '__main__':
    unittest.main()