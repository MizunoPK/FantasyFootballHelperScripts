#!/usr/bin/env python3
"""
Unit tests for ByeWeekVisualizer module.

Tests the bye week visualization and conflict detection functionality.

Author: Kai Mizuno
Last Updated: October 2025
"""

import unittest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from league_helper.util.bye_week_visualizer import ByeWeekVisualizer
from shared_files.FantasyPlayer import FantasyPlayer


class TestByeWeekVisualizer(unittest.TestCase):
    """Test ByeWeekVisualizer class"""

    def setUp(self):
        """Set up test fixtures"""
        self.visualizer = ByeWeekVisualizer()

    def _create_mock_player(self, name, position, bye_week=None):
        """Helper to create a mock FantasyPlayer"""
        player = Mock(spec=FantasyPlayer)
        player.name = name
        player.position = position
        player.bye_week = bye_week
        player.team = "TEST"
        return player

    # =========================================================================
    # Tests for generate_bye_week_summary()
    # =========================================================================

    def test_generate_bye_week_summary_empty_roster(self):
        """Test with empty roster"""
        summary = self.visualizer.generate_bye_week_summary([], current_week=5)
        self.assertIn("Bye Week Summary", summary)
        self.assertIn("No players in roster", summary)

    def test_generate_bye_week_summary_single_player(self):
        """Test with single player"""
        players = [self._create_mock_player("Patrick Mahomes", "QB", bye_week=7)]
        summary = self.visualizer.generate_bye_week_summary(players, current_week=5)

        self.assertIn("Week 7: Patrick Mahomes (QB)", summary)
        self.assertIn("Week 5: None", summary)  # Should show all weeks
        self.assertIn("Week 6: None", summary)

    def test_generate_bye_week_summary_multiple_players_same_week(self):
        """Test multiple players with same bye week sorted correctly"""
        players = [
            self._create_mock_player("Tyreek Hill", "WR", bye_week=7),
            self._create_mock_player("Travis Kelce", "TE", bye_week=7),
            self._create_mock_player("Patrick Mahomes", "QB", bye_week=7),
        ]
        summary = self.visualizer.generate_bye_week_summary(players, current_week=5)

        # Should be sorted by position (QB, WR, TE) then alphabetically
        self.assertIn("Week 7: Patrick Mahomes (QB), Tyreek Hill (WR), Travis Kelce (TE)", summary)

    def test_generate_bye_week_summary_multiple_weeks(self):
        """Test players in different weeks display in order"""
        players = [
            self._create_mock_player("Player1", "RB", bye_week=10),
            self._create_mock_player("Player2", "WR", bye_week=7),
            self._create_mock_player("Player3", "QB", bye_week=12),
        ]
        summary = self.visualizer.generate_bye_week_summary(players, current_week=5)

        # Check all weeks are present in order
        lines = summary.split('\n')
        week_lines = [l for l in lines if l.startswith('Week')]

        # Should have weeks 5-18
        self.assertEqual(len(week_lines), 14)  # Weeks 5 through 18

        # Verify specific weeks have correct content
        self.assertTrue(any("Week 7: Player2 (WR)" in line for line in week_lines))
        self.assertTrue(any("Week 10: Player1 (RB)" in line for line in week_lines))
        self.assertTrue(any("Week 12: Player3 (QB)" in line for line in week_lines))

    def test_generate_bye_week_summary_shows_none_for_empty_weeks(self):
        """Test that weeks with no byes show 'None'"""
        players = [self._create_mock_player("Player1", "QB", bye_week=10)]
        summary = self.visualizer.generate_bye_week_summary(players, current_week=5)

        self.assertIn("Week 5: None", summary)
        self.assertIn("Week 6: None", summary)
        self.assertIn("Week 7: None", summary)
        self.assertIn("Week 10: Player1 (QB)", summary)

    def test_generate_bye_week_summary_filters_past_weeks(self):
        """Test that weeks before current_week are not shown"""
        players = [
            self._create_mock_player("Player1", "QB", bye_week=3),  # Past
            self._create_mock_player("Player2", "RB", bye_week=10),  # Future
        ]
        summary = self.visualizer.generate_bye_week_summary(players, current_week=5)

        # Should not show week 3
        self.assertNotIn("Week 3", summary)
        self.assertNotIn("Player1", summary)

        # Should show week 10
        self.assertIn("Week 10: Player2 (RB)", summary)

    def test_generate_bye_week_summary_includes_week_18(self):
        """Test that week 18 is included in the summary"""
        players = [self._create_mock_player("Player1", "QB", bye_week=18)]
        summary = self.visualizer.generate_bye_week_summary(players, current_week=10)

        self.assertIn("Week 18: Player1 (QB)", summary)

    def test_generate_bye_week_summary_alphabetical_within_position(self):
        """Test players are sorted alphabetically within same position"""
        players = [
            self._create_mock_player("Zach Wilson", "QB", bye_week=7),
            self._create_mock_player("Aaron Rodgers", "QB", bye_week=7),
            self._create_mock_player("Mac Jones", "QB", bye_week=7),
        ]
        summary = self.visualizer.generate_bye_week_summary(players, current_week=5)

        # Should be alphabetically sorted
        self.assertIn("Week 7: Aaron Rodgers (QB), Mac Jones (QB), Zach Wilson (QB)", summary)

    # =========================================================================
    # Tests for _get_players_by_bye_week()
    # =========================================================================

    def test_get_players_by_bye_week_empty_roster(self):
        """Test with empty roster returns empty dict"""
        result = self.visualizer._get_players_by_bye_week([], current_week=5)
        self.assertEqual(result, {})

    def test_get_players_by_bye_week_filters_past_weeks(self):
        """Test that past weeks are filtered out"""
        players = [
            self._create_mock_player("Player1", "QB", bye_week=3),
            self._create_mock_player("Player2", "RB", bye_week=5),
            self._create_mock_player("Player3", "WR", bye_week=10),
        ]
        result = self.visualizer._get_players_by_bye_week(players, current_week=5)

        # Should not include week 3
        self.assertNotIn(3, result)
        # Should include weeks 5 and 10
        self.assertIn(5, result)
        self.assertIn(10, result)

    def test_get_players_by_bye_week_groups_correctly(self):
        """Test players are grouped by bye week correctly"""
        players = [
            self._create_mock_player("Player1", "QB", bye_week=7),
            self._create_mock_player("Player2", "RB", bye_week=7),
            self._create_mock_player("Player3", "WR", bye_week=10),
        ]
        result = self.visualizer._get_players_by_bye_week(players, current_week=5)

        self.assertEqual(len(result[7]), 2)
        self.assertEqual(len(result[10]), 1)
        self.assertIn("Player1", [p.name for p in result[7]])
        self.assertIn("Player2", [p.name for p in result[7]])

    def test_get_players_by_bye_week_handles_none(self):
        """Test players with None bye_week are excluded"""
        players = [
            self._create_mock_player("Player1", "QB", bye_week=None),
            self._create_mock_player("Player2", "RB", bye_week=10),
        ]
        result = self.visualizer._get_players_by_bye_week(players, current_week=5)

        self.assertNotIn(None, result)
        self.assertNotIn(0, result)
        self.assertIn(10, result)

    def test_get_players_by_bye_week_handles_zero(self):
        """Test players with 0 bye_week are excluded"""
        players = [
            self._create_mock_player("Player1", "QB", bye_week=0),
            self._create_mock_player("Player2", "RB", bye_week=10),
        ]
        result = self.visualizer._get_players_by_bye_week(players, current_week=5)

        self.assertNotIn(0, result)
        self.assertIn(10, result)

    # =========================================================================
    # Tests for _sort_players()
    # =========================================================================

    def test_sort_players_position_order(self):
        """Test players are sorted by position order"""
        players = [
            self._create_mock_player("Player1", "DST", bye_week=7),
            self._create_mock_player("Player2", "QB", bye_week=7),
            self._create_mock_player("Player3", "RB", bye_week=7),
            self._create_mock_player("Player4", "WR", bye_week=7),
            self._create_mock_player("Player5", "TE", bye_week=7),
            self._create_mock_player("Player6", "K", bye_week=7),
        ]
        sorted_players = self.visualizer._sort_players(players)

        # Should be in order: QB, RB, WR, TE, K, DST
        expected_positions = ["QB", "RB", "WR", "TE", "K", "DST"]
        actual_positions = [p.position for p in sorted_players]
        self.assertEqual(actual_positions, expected_positions)

    def test_sort_players_alphabetical_within_position(self):
        """Test alphabetical sorting within same position"""
        players = [
            self._create_mock_player("Zach", "QB", bye_week=7),
            self._create_mock_player("Aaron", "QB", bye_week=7),
            self._create_mock_player("Mac", "QB", bye_week=7),
        ]
        sorted_players = self.visualizer._sort_players(players)

        expected_names = ["Aaron", "Mac", "Zach"]
        actual_names = [p.name for p in sorted_players]
        self.assertEqual(actual_names, expected_names)

    def test_sort_players_unknown_position_last(self):
        """Test unknown positions are sorted to the end"""
        players = [
            self._create_mock_player("Player1", "UNKNOWN", bye_week=7),
            self._create_mock_player("Player2", "QB", bye_week=7),
        ]
        sorted_players = self.visualizer._sort_players(players)

        # QB should come before UNKNOWN
        self.assertEqual(sorted_players[0].position, "QB")
        self.assertEqual(sorted_players[1].position, "UNKNOWN")

    # =========================================================================
    # Tests for _detect_bye_conflicts()
    # =========================================================================

    def test_detect_bye_conflicts_no_conflict_single_player(self):
        """Test no conflict with single player per week"""
        bye_week_dict = {
            7: [self._create_mock_player("Player1", "QB", bye_week=7)],
            10: [self._create_mock_player("Player2", "RB", bye_week=10)],
        }
        conflicts = self.visualizer._detect_bye_conflicts(bye_week_dict)
        self.assertEqual(len(conflicts), 0)

    def test_detect_bye_conflicts_two_rbs_same_week(self):
        """Test conflict detected for 2 RBs in same week"""
        bye_week_dict = {
            7: [
                self._create_mock_player("RB1", "RB", bye_week=7),
                self._create_mock_player("RB2", "RB", bye_week=7),
            ]
        }
        conflicts = self.visualizer._detect_bye_conflicts(bye_week_dict)
        self.assertIn(7, conflicts)

    def test_detect_bye_conflicts_two_wrs_same_week(self):
        """Test conflict detected for 2 WRs in same week"""
        bye_week_dict = {
            7: [
                self._create_mock_player("WR1", "WR", bye_week=7),
                self._create_mock_player("WR2", "WR", bye_week=7),
            ]
        }
        conflicts = self.visualizer._detect_bye_conflicts(bye_week_dict)
        self.assertIn(7, conflicts)

    def test_detect_bye_conflicts_two_qbs_same_week(self):
        """Test conflict detected for 2 QBs in same week"""
        bye_week_dict = {
            7: [
                self._create_mock_player("QB1", "QB", bye_week=7),
                self._create_mock_player("QB2", "QB", bye_week=7),
            ]
        }
        conflicts = self.visualizer._detect_bye_conflicts(bye_week_dict)
        self.assertIn(7, conflicts)

    def test_detect_bye_conflicts_two_tes_same_week(self):
        """Test conflict detected for 2 TEs in same week"""
        bye_week_dict = {
            7: [
                self._create_mock_player("TE1", "TE", bye_week=7),
                self._create_mock_player("TE2", "TE", bye_week=7),
            ]
        }
        conflicts = self.visualizer._detect_bye_conflicts(bye_week_dict)
        self.assertIn(7, conflicts)

    def test_detect_bye_conflicts_different_positions_no_conflict(self):
        """Test no conflict when different positions have same bye week"""
        bye_week_dict = {
            7: [
                self._create_mock_player("Player1", "QB", bye_week=7),
                self._create_mock_player("Player2", "RB", bye_week=7),
                self._create_mock_player("Player3", "WR", bye_week=7),
            ]
        }
        conflicts = self.visualizer._detect_bye_conflicts(bye_week_dict)
        # No conflict because all different positions (only 1 of each)
        self.assertEqual(len(conflicts), 0)

    def test_detect_bye_conflicts_multiple_weeks(self):
        """Test conflicts detected across multiple weeks"""
        bye_week_dict = {
            7: [
                self._create_mock_player("RB1", "RB", bye_week=7),
                self._create_mock_player("RB2", "RB", bye_week=7),
            ],
            10: [
                self._create_mock_player("WR1", "WR", bye_week=10),
                self._create_mock_player("WR2", "WR", bye_week=10),
            ],
        }
        conflicts = self.visualizer._detect_bye_conflicts(bye_week_dict)
        self.assertIn(7, conflicts)
        self.assertIn(10, conflicts)

    def test_detect_bye_conflicts_three_rbs_same_week(self):
        """Test conflict with 3+ players at same position"""
        bye_week_dict = {
            7: [
                self._create_mock_player("RB1", "RB", bye_week=7),
                self._create_mock_player("RB2", "RB", bye_week=7),
                self._create_mock_player("RB3", "RB", bye_week=7),
            ]
        }
        conflicts = self.visualizer._detect_bye_conflicts(bye_week_dict)
        self.assertIn(7, conflicts)

    # =========================================================================
    # Tests for get_player_bye_week_string()
    # =========================================================================

    def test_get_player_bye_week_string_normal(self):
        """Test bye week string for player with bye week"""
        player = self._create_mock_player("Player1", "QB", bye_week=7)
        result = self.visualizer.get_player_bye_week_string(player)
        self.assertEqual(result, "Bye: Week 7")

    def test_get_player_bye_week_string_none(self):
        """Test bye week string for player with None bye week"""
        player = self._create_mock_player("Player1", "QB", bye_week=None)
        result = self.visualizer.get_player_bye_week_string(player)
        self.assertEqual(result, "Bye: None")

    def test_get_player_bye_week_string_zero(self):
        """Test bye week string for player with 0 bye week"""
        player = self._create_mock_player("Player1", "QB", bye_week=0)
        result = self.visualizer.get_player_bye_week_string(player)
        self.assertEqual(result, "Bye: None")

    def test_bye_week_conflict_marker_in_summary(self):
        """Test that conflict marker appears in summary"""
        players = [
            self._create_mock_player("RB1", "RB", bye_week=7),
            self._create_mock_player("RB2", "RB", bye_week=7),
        ]
        summary = self.visualizer.generate_bye_week_summary(players, current_week=5)
        self.assertIn("⚠️ BYE WEEK CONFLICT", summary)
        self.assertIn("Week 7:", summary)


if __name__ == '__main__':
    unittest.main()
