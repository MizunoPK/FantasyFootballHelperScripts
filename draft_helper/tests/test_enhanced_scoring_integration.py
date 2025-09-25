#!/usr/bin/env python3
"""
Unit tests for enhanced scoring integration with draft helper.

This module tests the integration between the enhanced scoring system
and the draft helper, ensuring proper calculation and fallback behavior.
"""

import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared_files.FantasyPlayer import FantasyPlayer
from shared_files.enhanced_scoring import EnhancedScoringCalculator
from draft_helper import DraftHelper
import draft_helper_constants as Constants


class TestDraftHelperEnhancedScoringIntegration:
    """Test enhanced scoring integration in draft helper"""

    def setup_method(self):
        """Set up test data for each test method"""
        # Create test players with and without enhanced data
        self.enhanced_player = FantasyPlayer(
            id="1001", name="Enhanced Player", team="KC", position="RB",
            fantasy_points=120.0, average_draft_position=50.0, player_rating=75.0,
            team_offensive_rank=5, team_defensive_rank=None
        )

        self.basic_player = FantasyPlayer(
            id="1002", name="Basic Player", team="NE", position="RB",
            fantasy_points=100.0, weighted_projection=100.0
        )

        self.zero_score_player = FantasyPlayer(
            id="1003", name="Zero Player", team="JAX", position="WR",
            fantasy_points=0.0
        )

    @patch('draft_helper.load_players_from_csv')
    def test_draft_helper_initialization_with_enhanced_scoring(self, mock_load_players):
        """Test that DraftHelper properly initializes enhanced scoring calculator"""
        mock_load_players.return_value = [self.enhanced_player, self.basic_player]

        draft_helper = DraftHelper()

        assert hasattr(draft_helper, 'enhanced_scorer')
        assert isinstance(draft_helper.enhanced_scorer, EnhancedScoringCalculator)

    @patch('draft_helper.load_players_from_csv')
    def test_compute_projection_score_with_enhanced_data(self, mock_load_players):
        """Test compute_projection_score with player that has enhanced data"""
        mock_load_players.return_value = [self.enhanced_player]

        draft_helper = DraftHelper()

        score = draft_helper.compute_projection_score(self.enhanced_player)

        # Should be enhanced score, not just fantasy_points
        assert score > self.enhanced_player.fantasy_points
        assert score == pytest.approx(131.04, rel=1e-2)  # Expected enhanced score

    @patch('draft_helper.load_players_from_csv')
    def test_compute_projection_score_without_enhanced_data(self, mock_load_players):
        """Test compute_projection_score with player that lacks enhanced data"""
        mock_load_players.return_value = [self.basic_player]

        draft_helper = DraftHelper()

        score = draft_helper.compute_projection_score(self.basic_player)

        # Should fall back to weighted_projection
        assert score == self.basic_player.weighted_projection

    @patch('draft_helper.load_players_from_csv')
    def test_compute_projection_score_zero_fantasy_points(self, mock_load_players):
        """Test compute_projection_score with zero fantasy points"""
        mock_load_players.return_value = [self.zero_score_player]

        draft_helper = DraftHelper()

        score = draft_helper.compute_projection_score(self.zero_score_player)

        # Should return 0 regardless of enhanced scoring
        assert score == 0.0

    @patch('draft_helper.load_players_from_csv')
    def test_compute_projection_score_fallback_to_fantasy_points(self, mock_load_players):
        """Test fallback to fantasy_points when weighted_projection is unavailable"""
        player_no_weighted = FantasyPlayer(
            id="1004", name="No Weighted Player", team="DAL", position="QB",
            fantasy_points=150.0, weighted_projection=0.0  # No weighted projection
        )
        mock_load_players.return_value = [player_no_weighted]

        draft_helper = DraftHelper()

        score = draft_helper.compute_projection_score(player_no_weighted)

        # Should fall back to fantasy_points
        assert score == player_no_weighted.fantasy_points

    @patch('draft_helper.load_players_from_csv')
    def test_enhanced_scoring_with_different_positions(self, mock_load_players):
        """Test enhanced scoring works correctly for different positions"""
        # Create players for different positions with enhanced data
        qb_player = FantasyPlayer(
            id="2001", name="Test QB", team="KC", position="QB",
            fantasy_points=300.0, average_draft_position=15.0, player_rating=85.0,
            team_offensive_rank=3, team_defensive_rank=None
        )

        dst_player = FantasyPlayer(
            id="2002", name="Test DST", team="SF", position="DST",
            fantasy_points=80.0, average_draft_position=120.0, player_rating=60.0,
            team_offensive_rank=None, team_defensive_rank=2
        )

        mock_load_players.return_value = [qb_player, dst_player]

        draft_helper = DraftHelper()

        qb_score = draft_helper.compute_projection_score(qb_player)
        dst_score = draft_helper.compute_projection_score(dst_player)

        # Both should get enhanced scores
        assert qb_score > qb_player.fantasy_points
        assert dst_score > dst_player.fantasy_points

        # DST should use defensive rank, QB should use offensive rank
        assert qb_score == pytest.approx(414.72, rel=1e-2)  # Expected QB score
        assert dst_score == pytest.approx(95.14, rel=1e-2)  # Expected DST score

    @patch('draft_helper.load_players_from_csv')
    def test_score_player_integration(self, mock_load_players):
        """Test that enhanced scoring properly integrates into overall player scoring"""
        mock_load_players.return_value = [self.enhanced_player]

        draft_helper = DraftHelper()

        # Mock other scoring methods to isolate enhanced scoring impact
        with patch.object(draft_helper, 'compute_positional_need_score', return_value=50.0), \
             patch.object(draft_helper, 'compute_bye_penalty_for_player', return_value=10.0), \
             patch.object(draft_helper, 'compute_injury_penalty', return_value=5.0):

            total_score = draft_helper.score_player(self.enhanced_player)

            # Total = positional(50) + enhanced_projection(131.04) - bye_penalty(10) - injury_penalty(5) = 166.04
            expected_total = 50.0 + 131.04 - 10.0 - 5.0
            assert total_score == pytest.approx(expected_total, rel=1e-2)

    @patch('draft_helper.load_players_from_csv')
    @patch('draft_helper.logging.getLogger')
    def test_enhanced_scoring_logging(self, mock_logger, mock_load_players):
        """Test that enhanced scoring logs adjustments properly"""
        mock_logger_instance = MagicMock()
        mock_logger.return_value = mock_logger_instance

        mock_load_players.return_value = [self.enhanced_player]

        draft_helper = DraftHelper()

        # Enable info logging to capture enhancement messages
        mock_logger_instance.info = MagicMock()

        score = draft_helper.compute_projection_score(self.enhanced_player)

        # Should have logged the enhancement
        mock_logger_instance.info.assert_called()

        # Check that the logged message contains expected content
        logged_calls = mock_logger_instance.info.call_args_list
        enhancement_logged = any("Enhanced scoring for" in str(call) for call in logged_calls)
        assert enhancement_logged

    @patch('draft_helper.load_players_from_csv')
    def test_enhanced_scoring_disabled_fallback(self, mock_load_players):
        """Test fallback behavior when enhanced scoring is disabled"""
        mock_load_players.return_value = [self.enhanced_player]

        # Create DraftHelper with enhanced scoring disabled
        with patch('shared_files.enhanced_scoring.DEFAULT_SCORING_CONFIG', {
            **EnhancedScoringCalculator().config,
            'enable_adp_adjustment': False,
            'enable_player_rating_adjustment': False,
            'enable_team_quality_adjustment': False
        }):
            draft_helper = DraftHelper()

            score = draft_helper.compute_projection_score(self.enhanced_player)

            # Should be just the base fantasy points (no enhancement)
            assert score == self.enhanced_player.fantasy_points

    @patch('draft_helper.load_players_from_csv')
    def test_enhanced_scoring_with_missing_attributes(self, mock_load_players):
        """Test enhanced scoring when player is missing some enhanced attributes"""
        # Player with only some enhanced data
        partial_player = FantasyPlayer(
            id="3001", name="Partial Player", team="GB", position="WR",
            fantasy_points=90.0, average_draft_position=60.0  # Only has ADP
            # Missing: player_rating, team_offensive_rank, team_defensive_rank
        )

        mock_load_players.return_value = [partial_player]

        draft_helper = DraftHelper()

        score = draft_helper.compute_projection_score(partial_player)

        # Should apply ADP adjustment only
        expected_score = 90.0 * 1.08  # ADP adjustment for 60.0
        assert score == pytest.approx(expected_score, rel=1e-2)

    @patch('draft_helper.load_players_from_csv')
    def test_enhanced_scoring_error_handling(self, mock_load_players):
        """Test that enhanced scoring errors are handled gracefully"""
        mock_load_players.return_value = [self.enhanced_player]

        draft_helper = DraftHelper()

        # Mock enhanced scorer to raise an exception
        with patch.object(draft_helper.enhanced_scorer, 'calculate_enhanced_score',
                         side_effect=Exception("Test error")):

            # Should not crash and fall back to basic scoring
            score = draft_helper.compute_projection_score(self.enhanced_player)

            # Should fall back to weighted_projection or fantasy_points
            assert score == self.enhanced_player.fantasy_points

    @patch('draft_helper.load_players_from_csv')
    def test_hunt_vs_henderson_integration(self, mock_load_players):
        """Test the specific Hunt vs Henderson scenario in draft helper context"""
        hunt = FantasyPlayer(
            id='3059915', name='Kareem Hunt', team='KC', position='RB',
            fantasy_points=135.54, average_draft_position=120.0, player_rating=45.0,
            team_offensive_rank=8, team_defensive_rank=None
        )

        henderson = FantasyPlayer(
            id='4432710', name='TreVeyon Henderson', team='NE', position='RB',
            fantasy_points=121.97, average_draft_position=85.0, player_rating=65.0,
            team_offensive_rank=18, team_defensive_rank=None
        )

        mock_load_players.return_value = [hunt, henderson]

        draft_helper = DraftHelper()

        hunt_score = draft_helper.compute_projection_score(hunt)
        henderson_score = draft_helper.compute_projection_score(henderson)

        # Henderson should score higher after enhancement
        assert henderson_score > hunt_score

        # Verify specific expected scores
        assert hunt_score == pytest.approx(143.67, rel=1e-2)
        assert henderson_score == pytest.approx(144.90, rel=1e-2)

    @patch('draft_helper.load_players_from_csv')
    def test_enhanced_scoring_performance(self, mock_load_players):
        """Test that enhanced scoring doesn't significantly impact performance"""
        import time

        # Create many players to test performance
        players = []
        for i in range(100):
            player = FantasyPlayer(
                id=f"perf_{i}", name=f"Player {i}", team="TEST", position="RB",
                fantasy_points=100.0 + i, average_draft_position=50.0 + i,
                player_rating=60.0, team_offensive_rank=10
            )
            players.append(player)

        mock_load_players.return_value = players

        draft_helper = DraftHelper()

        # Time the enhanced scoring calculations
        start_time = time.time()
        for player in players:
            draft_helper.compute_projection_score(player)
        end_time = time.time()

        elapsed = end_time - start_time

        # Should complete 100 calculations in reasonable time (< 1 second)
        assert elapsed < 1.0

    @patch('draft_helper.load_players_from_csv')
    def test_enhanced_scoring_consistency(self, mock_load_players):
        """Test that enhanced scoring produces consistent results"""
        mock_load_players.return_value = [self.enhanced_player]

        draft_helper = DraftHelper()

        # Calculate score multiple times
        scores = []
        for _ in range(5):
            score = draft_helper.compute_projection_score(self.enhanced_player)
            scores.append(score)

        # All scores should be identical
        assert all(score == scores[0] for score in scores)

    @patch('draft_helper.load_players_from_csv')
    def test_enhanced_scoring_with_various_data_combinations(self, mock_load_players):
        """Test enhanced scoring with various combinations of available data"""
        test_cases = [
            # Only ADP
            FantasyPlayer(id="tc1", name="ADP Only", team="TEST", position="RB",
                         fantasy_points=100.0, average_draft_position=50.0),
            # Only rating
            FantasyPlayer(id="tc2", name="Rating Only", team="TEST", position="RB",
                         fantasy_points=100.0, player_rating=70.0),
            # Only team rank
            FantasyPlayer(id="tc3", name="Team Only", team="TEST", position="RB",
                         fantasy_points=100.0, team_offensive_rank=8),
            # ADP + Rating
            FantasyPlayer(id="tc4", name="ADP + Rating", team="TEST", position="RB",
                         fantasy_points=100.0, average_draft_position=50.0, player_rating=70.0),
            # All data
            FantasyPlayer(id="tc5", name="All Data", team="TEST", position="RB",
                         fantasy_points=100.0, average_draft_position=50.0,
                         player_rating=70.0, team_offensive_rank=8),
        ]

        mock_load_players.return_value = test_cases

        draft_helper = DraftHelper()

        scores = []
        for player in test_cases:
            score = draft_helper.compute_projection_score(player)
            scores.append(score)

        # Each should have different scores based on available data
        assert len(set(scores)) == len(scores)  # All scores should be different

        # Score with all data should be highest (most enhancements)
        assert scores[-1] == max(scores)

        # Base case (no enhancements) should be lowest
        # Note: We don't have a no-enhancement case here, but scores[0] (ADP only) should be lower than scores[-1]
        assert scores[0] < scores[-1]


class TestEnhancedScoringConfigurationIntegration:
    """Test configuration aspects of enhanced scoring integration"""

    @patch('draft_helper.load_players_from_csv')
    def test_custom_configuration_integration(self, mock_load_players):
        """Test that draft helper can use custom enhanced scoring configuration"""
        player = FantasyPlayer(
            id="cfg1", name="Config Test", team="TEST", position="RB",
            fantasy_points=100.0, average_draft_position=50.0
        )

        mock_load_players.return_value = [player]

        # Create draft helper and modify the enhanced scorer config
        draft_helper = DraftHelper()
        draft_helper.enhanced_scorer.config['adp_good_multiplier'] = 1.20  # Increase boost

        score = draft_helper.compute_projection_score(player)

        # Should use the modified configuration
        expected_score = 100.0 * 1.20  # Custom multiplier
        assert score == pytest.approx(expected_score, rel=1e-2)

    @patch('draft_helper.load_players_from_csv')
    def test_enhanced_scoring_toggle_integration(self, mock_load_players):
        """Test that enhanced scoring can be toggled on/off"""
        player = FantasyPlayer(
            id="toggle1", name="Toggle Test", team="TEST", position="RB",
            fantasy_points=100.0, average_draft_position=25.0,  # Would give boost
            player_rating=80.0  # Would give boost
        )

        mock_load_players.return_value = [player]

        draft_helper = DraftHelper()

        # Get enhanced score
        enhanced_score = draft_helper.compute_projection_score(player)

        # Disable all enhancements
        draft_helper.enhanced_scorer.config['enable_adp_adjustment'] = False
        draft_helper.enhanced_scorer.config['enable_player_rating_adjustment'] = False
        draft_helper.enhanced_scorer.config['enable_team_quality_adjustment'] = False

        # Get basic score
        basic_score = draft_helper.compute_projection_score(player)

        # Enhanced should be higher than basic
        assert enhanced_score > basic_score
        assert basic_score == player.fantasy_points  # Should be base points when disabled


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])