"""
Unit tests for Week module

Tests matchup simulation, result tracking, and week management.

Author: Kai Mizuno
"""

import pytest
from unittest.mock import Mock, MagicMock
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))
from simulation.Week import Week, WeekResult


class TestWeekResult:
    """Test WeekResult functionality"""

    def test_week_result_initialization(self):
        """Test WeekResult initialization with all parameters"""
        team = Mock()
        team.name = "TestTeam"

        result = WeekResult(team, 125.5, 98.3, True)

        assert result.team == team
        assert result.points_scored == 125.5
        assert result.points_against == 98.3
        assert result.won is True

    def test_week_result_loss(self):
        """Test WeekResult for a loss"""
        team = Mock()

        result = WeekResult(team, 85.2, 102.7, False)

        assert result.points_scored == 85.2
        assert result.points_against == 102.7
        assert result.won is False

    def test_week_result_repr_win(self):
        """Test __repr__ for winning result"""
        team = Mock()

        result = WeekResult(team, 125.5, 98.3, True)

        repr_str = repr(result)
        assert "W" in repr_str
        assert "125.50" in repr_str
        assert "98.30" in repr_str

    def test_week_result_repr_loss(self):
        """Test __repr__ for losing result"""
        team = Mock()

        result = WeekResult(team, 85.2, 102.7, False)

        repr_str = repr(result)
        assert "L" in repr_str
        assert "85.20" in repr_str
        assert "102.70" in repr_str

    def test_week_result_tie_treated_as_loss(self):
        """Test that tied scores are treated as losses"""
        team = Mock()

        # In ties, both teams should have won=False
        result = WeekResult(team, 100.0, 100.0, False)

        assert result.points_scored == result.points_against
        assert result.won is False


class TestWeek:
    """Test Week functionality"""

    def test_week_initialization(self):
        """Test Week initialization with valid parameters"""
        team1 = Mock()
        team2 = Mock()
        matchups = [(team1, team2)]

        week = Week(1, matchups)

        assert week.week_number == 1
        assert week.matchups == matchups
        assert week.results == {}

    def test_week_number_validation_min(self):
        """Test week number validation - too low"""
        matchups = []

        with pytest.raises(ValueError, match="Week number must be between 1 and 17"):
            Week(0, matchups)

    def test_week_number_validation_max(self):
        """Test week number validation - too high"""
        matchups = []

        with pytest.raises(ValueError, match="Week number must be between 1 and 17"):
            Week(18, matchups)

    def test_week_number_validation_negative(self):
        """Test week number validation - negative"""
        matchups = []

        with pytest.raises(ValueError, match="Week number must be between 1 and 17"):
            Week(-1, matchups)

    def test_week_number_edge_cases_valid(self):
        """Test week number edge cases - valid boundaries"""
        matchups = []

        # Week 1 should be valid
        week1 = Week(1, matchups)
        assert week1.week_number == 1

        # Week 17 should be valid (updated from 16)
        week17 = Week(17, matchups)
        assert week17.week_number == 17

    def test_simulate_week_single_matchup_team1_wins(self):
        """Test simulating a week with one matchup - team1 wins"""
        team1 = Mock()
        team1.set_weekly_lineup = Mock(return_value=125.5)

        team2 = Mock()
        team2.set_weekly_lineup = Mock(return_value=98.3)

        matchups = [(team1, team2)]
        week = Week(5, matchups)

        results = week.simulate_week()

        # Verify both teams set their lineup
        team1.set_weekly_lineup.assert_called_once_with(5)
        team2.set_weekly_lineup.assert_called_once_with(5)

        # Verify results
        assert len(results) == 2
        assert results[team1].won is True
        assert results[team1].points_scored == 125.5
        assert results[team1].points_against == 98.3
        assert results[team2].won is False
        assert results[team2].points_scored == 98.3
        assert results[team2].points_against == 125.5

    def test_simulate_week_single_matchup_team2_wins(self):
        """Test simulating a week with one matchup - team2 wins"""
        team1 = Mock()
        team1.set_weekly_lineup = Mock(return_value=85.2)

        team2 = Mock()
        team2.set_weekly_lineup = Mock(return_value=110.7)

        matchups = [(team1, team2)]
        week = Week(8, matchups)

        results = week.simulate_week()

        # Verify results
        assert results[team1].won is False
        assert results[team2].won is True

    def test_simulate_week_tie_both_lose(self):
        """Test simulating a week with tie - both teams lose"""
        team1 = Mock()
        team1.set_weekly_lineup = Mock(return_value=100.0)

        team2 = Mock()
        team2.set_weekly_lineup = Mock(return_value=100.0)

        matchups = [(team1, team2)]
        week = Week(3, matchups)

        results = week.simulate_week()

        # In a tie, both teams should lose
        assert results[team1].won is False
        assert results[team2].won is False
        assert results[team1].points_scored == 100.0
        assert results[team2].points_scored == 100.0

    def test_simulate_week_multiple_matchups(self):
        """Test simulating a week with multiple matchups"""
        team1 = Mock()
        team1.set_weekly_lineup = Mock(return_value=120.0)

        team2 = Mock()
        team2.set_weekly_lineup = Mock(return_value=105.0)

        team3 = Mock()
        team3.set_weekly_lineup = Mock(return_value=95.0)

        team4 = Mock()
        team4.set_weekly_lineup = Mock(return_value=110.0)

        matchups = [(team1, team2), (team3, team4)]
        week = Week(10, matchups)

        results = week.simulate_week()

        # Verify all teams have results
        assert len(results) == 4

        # Matchup 1: team1 wins
        assert results[team1].won is True
        assert results[team2].won is False

        # Matchup 2: team4 wins
        assert results[team3].won is False
        assert results[team4].won is True

    def test_simulate_week_very_close_scores(self):
        """Test simulating with very close but not tied scores"""
        team1 = Mock()
        team1.set_weekly_lineup = Mock(return_value=100.01)

        team2 = Mock()
        team2.set_weekly_lineup = Mock(return_value=100.00)

        matchups = [(team1, team2)]
        week = Week(7, matchups)

        results = week.simulate_week()

        # Team1 should win by the smallest margin
        assert results[team1].won is True
        assert results[team2].won is False

    def test_get_result_valid_team(self):
        """Test getting result for a team that played"""
        team1 = Mock()
        team1.set_weekly_lineup = Mock(return_value=120.0)

        team2 = Mock()
        team2.set_weekly_lineup = Mock(return_value=100.0)

        matchups = [(team1, team2)]
        week = Week(4, matchups)
        week.simulate_week()

        result = week.get_result(team1)

        assert result.team == team1
        assert result.points_scored == 120.0
        assert result.won is True

    def test_get_result_team_not_in_week(self):
        """Test getting result for team that didn't play"""
        team1 = Mock()
        team1.set_weekly_lineup = Mock(return_value=120.0)

        team2 = Mock()
        team2.set_weekly_lineup = Mock(return_value=100.0)

        team3 = Mock()  # Not in matchups

        matchups = [(team1, team2)]
        week = Week(6, matchups)
        week.simulate_week()

        with pytest.raises(ValueError, match="Team did not play in week 6"):
            week.get_result(team3)

    def test_get_all_results(self):
        """Test getting all results returns copy"""
        team1 = Mock()
        team1.set_weekly_lineup = Mock(return_value=120.0)

        team2 = Mock()
        team2.set_weekly_lineup = Mock(return_value=100.0)

        matchups = [(team1, team2)]
        week = Week(9, matchups)
        week.simulate_week()

        all_results = week.get_all_results()

        # Verify it's a copy
        assert all_results == week.results
        assert all_results is not week.results

        # Verify contents
        assert len(all_results) == 2
        assert team1 in all_results
        assert team2 in all_results

    def test_get_matchups(self):
        """Test getting matchups returns copy"""
        team1 = Mock()
        team2 = Mock()
        team3 = Mock()
        team4 = Mock()

        matchups = [(team1, team2), (team3, team4)]
        week = Week(12, matchups)

        returned_matchups = week.get_matchups()

        # Verify it's a copy
        assert returned_matchups == matchups
        assert returned_matchups is not matchups

        # Verify contents
        assert len(returned_matchups) == 2

    def test_week_repr(self):
        """Test Week __repr__ method"""
        team1 = Mock()
        team2 = Mock()
        matchups = [(team1, team2)]

        week = Week(15, matchups)

        repr_str = repr(week)
        assert "15" in repr_str
        assert "1" in repr_str  # 1 matchup

    def test_simulate_week_idempotency(self):
        """Test that simulating same week twice overwrites results"""
        team1 = Mock()
        team1.set_weekly_lineup = Mock(side_effect=[120.0, 130.0])

        team2 = Mock()
        team2.set_weekly_lineup = Mock(side_effect=[100.0, 110.0])

        matchups = [(team1, team2)]
        week = Week(11, matchups)

        # First simulation
        results1 = week.simulate_week()
        assert results1[team1].points_scored == 120.0

        # Second simulation - should overwrite
        results2 = week.simulate_week()
        assert results2[team1].points_scored == 130.0

        # Final results should match second simulation
        final = week.get_result(team1)
        assert final.points_scored == 130.0

    def test_simulate_week_zero_scores(self):
        """Test simulating with zero scores (edge case)"""
        team1 = Mock()
        team1.set_weekly_lineup = Mock(return_value=0.0)

        team2 = Mock()
        team2.set_weekly_lineup = Mock(return_value=0.0)

        matchups = [(team1, team2)]
        week = Week(2, matchups)

        results = week.simulate_week()

        # Both teams scored 0, should be tie (both lose)
        assert results[team1].won is False
        assert results[team2].won is False

    def test_simulate_week_negative_scores_not_allowed(self):
        """Test that negative scores work (though shouldn't happen in practice)"""
        team1 = Mock()
        team1.set_weekly_lineup = Mock(return_value=-10.0)

        team2 = Mock()
        team2.set_weekly_lineup = Mock(return_value=-5.0)

        matchups = [(team1, team2)]
        week = Week(13, matchups)

        results = week.simulate_week()

        # team2 has "higher" score (-5 > -10)
        assert results[team2].won is True
        assert results[team1].won is False

    def test_simulate_week_high_scores(self):
        """Test simulating with very high scores"""
        team1 = Mock()
        team1.set_weekly_lineup = Mock(return_value=250.75)

        team2 = Mock()
        team2.set_weekly_lineup = Mock(return_value=248.50)

        matchups = [(team1, team2)]
        week = Week(14, matchups)

        results = week.simulate_week()

        assert results[team1].won is True
        assert results[team1].points_scored == 250.75
        assert results[team2].points_scored == 248.50

    def test_empty_matchups(self):
        """Test week with no matchups"""
        week = Week(16, [])

        results = week.simulate_week()

        assert len(results) == 0
        assert week.get_all_results() == {}

    def test_week_stores_results_internally(self):
        """Test that week stores results in self.results"""
        team1 = Mock()
        team1.set_weekly_lineup = Mock(return_value=100.0)

        team2 = Mock()
        team2.set_weekly_lineup = Mock(return_value=90.0)

        matchups = [(team1, team2)]
        week = Week(16, matchups)

        # Before simulation
        assert len(week.results) == 0

        # After simulation
        week.simulate_week()
        assert len(week.results) == 2
        assert team1 in week.results
        assert team2 in week.results
