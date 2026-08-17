"""
Unit tests for NFL Team Penalty feature (Step 14 in player scoring).

Tests the _apply_nfl_team_penalty() method which applies penalty multiplier
to player scores in Add to Roster mode.
"""

import pytest
from unittest.mock import Mock
from league_helper.util.player_scoring import PlayerScoringCalculator
from utils.FantasyPlayer import FantasyPlayer


class TestNFLTeamPenaltyLogic:
    """Test the _apply_nfl_team_penalty() helper method - core functionality."""

    @pytest.fixture
    def mock_config(self):
        """Create mock config with penalty settings."""
        config = Mock()
        config.nfl_team_penalty = ["LV", "NYJ", "NYG", "KC"]
        config.nfl_team_penalty_weight = 0.75
        return config

    @pytest.fixture
    def calculator(self, mock_config):
        """Create PlayerScoringCalculator with mocked dependencies."""
        mock_player_manager = Mock()
        mock_team_data_manager = Mock()
        mock_season_schedule_manager = Mock()

        calc = PlayerScoringCalculator(
            config=mock_config,
            player_manager=mock_player_manager,
            max_projection=400.0,
            team_data_manager=mock_team_data_manager,
            season_schedule_manager=mock_season_schedule_manager,
            current_nfl_week=1
        )
        return calc

    @pytest.fixture
    def player_penalized(self):
        """Create player on penalized team (LV)."""
        player = Mock(spec=FantasyPlayer)
        player.name = "Davante Adams"
        player.team = "LV"
        player.position = "WR"
        return player

    @pytest.fixture
    def player_not_penalized(self):
        """Create player NOT on penalized team (DEN)."""
        player = Mock(spec=FantasyPlayer)
        player.name = "Russell Wilson"
        player.team = "DEN"
        player.position = "QB"
        return player

    def test_penalty_applied_team_in_list(self, calculator, player_penalized):
        """Test 1: Penalty applied when player team in penalty list."""
        initial_score = 100.0

        new_score, reason = calculator._apply_nfl_team_penalty(player_penalized, initial_score)

        assert new_score == 75.0
        assert reason == "NFL Team Penalty: LV (0.75x)"

    def test_no_penalty_team_not_in_list(self, calculator, player_not_penalized):
        """Test 2: No penalty when player team NOT in penalty list."""
        initial_score = 100.0

        new_score, reason = calculator._apply_nfl_team_penalty(player_not_penalized, initial_score)

        assert new_score == 100.0
        assert reason == ""

    def test_no_penalty_empty_list(self, calculator, player_penalized):
        """Test 3: No penalty when penalty list is empty."""
        calculator.config.nfl_team_penalty = []
        initial_score = 100.0

        new_score, reason = calculator._apply_nfl_team_penalty(player_penalized, initial_score)

        assert new_score == 100.0
        assert reason == ""

    def test_weight_075_calculation(self, calculator, player_penalized):
        """Test 4: Weight 0.75 produces correct score."""
        calculator.config.nfl_team_penalty_weight = 0.75
        initial_score = 120.5

        new_score, reason = calculator._apply_nfl_team_penalty(player_penalized, initial_score)

        assert new_score == 90.375
        assert reason == "NFL Team Penalty: LV (0.75x)"

    def test_weight_10_no_effect(self, calculator, player_penalized):
        """Test 5: Weight 1.0 produces unchanged score (edge case)."""
        calculator.config.nfl_team_penalty_weight = 1.0
        initial_score = 100.0

        new_score, reason = calculator._apply_nfl_team_penalty(player_penalized, initial_score)

        assert new_score == 100.0
        assert reason == "NFL Team Penalty: LV (1.00x)"

    def test_weight_00_zero_score(self, calculator, player_penalized):
        """Test 6: Weight 0.0 produces score of 0.0 (edge case)."""
        calculator.config.nfl_team_penalty_weight = 0.0
        initial_score = 100.0

        new_score, reason = calculator._apply_nfl_team_penalty(player_penalized, initial_score)

        assert new_score == 0.0
        assert reason == "NFL Team Penalty: LV (0.00x)"

    def test_reason_string_format(self, calculator, player_penalized):
        """Test 7: Reason string has correct format when penalty applied."""
        calculator.config.nfl_team_penalty_weight = 0.75
        initial_score = 100.0

        new_score, reason = calculator._apply_nfl_team_penalty(player_penalized, initial_score)

        assert reason == "NFL Team Penalty: LV (0.75x)"
        assert "NFL Team Penalty:" in reason
        assert "LV" in reason
        assert "(0.75x)" in reason

    def test_reason_empty_no_penalty(self, calculator, player_not_penalized):
        """Test 8: Reason string empty when no penalty applied."""
        initial_score = 100.0

        new_score, reason = calculator._apply_nfl_team_penalty(player_not_penalized, initial_score)

        assert reason == ""

    def test_multiple_teams_penalty(self, calculator):
        """Test 9: Penalty works for all teams in penalty list."""
        calculator.config.nfl_team_penalty = ["LV", "NYJ", "NYG", "KC"]
        calculator.config.nfl_team_penalty_weight = 0.75
        initial_score = 100.0

        teams_to_test = ["LV", "NYJ", "NYG", "KC"]

        for team_abbr in teams_to_test:
            player = Mock(spec=FantasyPlayer)
            player.team = team_abbr
            new_score, reason = calculator._apply_nfl_team_penalty(player, initial_score)

            assert new_score == 75.0, f"{team_abbr} should be penalized"
            assert reason == f"NFL Team Penalty: {team_abbr} (0.75x)"

    def test_different_weight_values(self, calculator, player_penalized):
        """Test 10: Different weight values produce correct scores."""
        test_cases = [
            (0.0, 0.0),
            (0.25, 25.0),
            (0.5, 50.0),
            (0.75, 75.0),
            (0.9, 90.0),
            (1.0, 100.0),
        ]

        initial_score = 100.0

        for weight, expected_score in test_cases:
            calculator.config.nfl_team_penalty_weight = weight

            new_score, reason = calculator._apply_nfl_team_penalty(player_penalized, initial_score)

            assert new_score == expected_score, f"Weight {weight} should produce score {expected_score}"
            assert reason == f"NFL Team Penalty: LV ({weight:.2f}x)"


