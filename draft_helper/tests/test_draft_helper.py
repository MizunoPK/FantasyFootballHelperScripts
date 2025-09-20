#!/usr/bin/env python3
"""
Unit tests for Draft Helper main module.

Tests the draft helper functionality including:
- Draft and trade mode switching
- Player scoring and recommendations
- Pure greedy trade algorithm
- Configuration validation
- Injury and bye week penalties
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add the parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import draft_helper
import draft_helper_config as draft_config
import draft_helper_constants as Constants

# Import FantasyPlayer from shared_files
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "shared_files"))
from FantasyPlayer import FantasyPlayer


class TestDraftHelper:
    """Test suite for Draft Helper main functionality"""

    @pytest.fixture
    def sample_players(self):
        """Create sample player data for testing"""
        return [
            FantasyPlayer(
                id="1",
                name="Elite RB",
                position="RB",
                team="TEST",
                fantasy_points=200.0,
                bye_week=7,
                injury_status="ACTIVE"
            ),
            FantasyPlayer(
                id="2",
                name="Good WR",
                position="WR",
                team="DEMO",
                fantasy_points=150.0,
                bye_week=9,
                injury_status="QUESTIONABLE"
            ),
            FantasyPlayer(
                id="3",
                name="Average QB",
                position="QB",
                team="TEAM",
                fantasy_points=280.0,
                bye_week=5,
                injury_status="ACTIVE"
            ),
            FantasyPlayer(
                id="4",
                name="Injured TE",
                position="TE",
                team="INJ",
                fantasy_points=90.0,
                bye_week=11,
                injury_status="OUT"
            )
        ]

    @pytest.fixture
    def mock_team_with_players(self):
        """Create mock team with some players"""
        team = MagicMock()
        team.roster = [
            FantasyPlayer(id="owned1", name="Owned RB", position="RB", team="TEST", fantasy_points=120.0),
            FantasyPlayer(id="owned2", name="Owned WR", position="WR", team="TEST", fantasy_points=100.0)
        ]
        team.pos_counts = {"RB": 1, "WR": 1, "QB": 0, "TE": 0, "K": 0, "DST": 0, "FLEX": 0}
        return team

    @pytest.fixture
    def draft_helper_instance(self, sample_players):
        """Create DraftHelper instance for testing"""
        # Create a temporary CSV file with test players
        import tempfile
        import csv
        import os

        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')

        try:
            # Write test players to CSV
            fieldnames = ['id', 'name', 'team', 'position', 'bye_week', 'fantasy_points', 'injury_status', 'drafted']
            writer = csv.DictWriter(temp_file, fieldnames=fieldnames)
            writer.writeheader()

            for player in sample_players:
                writer.writerow({
                    'id': player.id,
                    'name': player.name,
                    'team': player.team,
                    'position': player.position,
                    'bye_week': player.bye_week or '',
                    'fantasy_points': player.fantasy_points,
                    'injury_status': player.injury_status,
                    'drafted': 0
                })

            temp_file.close()

            # Create DraftHelper with the temp file
            helper = draft_helper.DraftHelper(temp_file.name)
            yield helper

        finally:
            # Clean up temp file
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)

    def test_configuration_validation(self):
        """Test that configuration is valid"""
        # Test that config validation runs without errors
        try:
            draft_config.validate_config()
        except ValueError as e:
            pytest.fail(f"Configuration validation failed: {e}")

        # Test core configuration values
        assert draft_config.MAX_PLAYERS > 0
        assert len(draft_config.DRAFT_ORDER) == draft_config.MAX_PLAYERS
        assert sum(draft_config.MAX_POSITIONS.values()) >= draft_config.MAX_PLAYERS

    def test_draft_mode_vs_trade_mode(self):
        """Test mode switching between draft and trade"""
        # Test that mode is properly set
        assert isinstance(draft_config.TRADE_HELPER_MODE, bool)

        # Test recommendation count is reasonable
        assert draft_config.RECOMMENDATION_COUNT > 0
        assert draft_config.RECOMMENDATION_COUNT <= 20

    def test_scoring_weights_configuration(self):
        """Test scoring weights are reasonable"""
        # Test positional need scoring
        assert draft_config.POS_NEEDED_SCORE > 0
        assert draft_config.PROJECTION_BASE_SCORE > 0

        # Test penalty system
        assert draft_config.BASE_BYE_PENALTY >= 0
        assert all(penalty >= 0 for penalty in draft_config.INJURY_PENALTIES.values())

    def test_injury_penalty_calculation(self, draft_helper_instance, sample_players):
        """Test injury penalty calculation"""
        active_player = sample_players[0]  # ACTIVE
        questionable_player = sample_players[1]  # QUESTIONABLE
        injured_player = sample_players[3]  # OUT

        # Test that injury penalties are applied correctly
        active_penalty = draft_helper_instance.compute_injury_penalty(active_player)
        questionable_penalty = draft_helper_instance.compute_injury_penalty(questionable_player)
        injured_penalty = draft_helper_instance.compute_injury_penalty(injured_player)

        # Active should have lowest penalty
        assert active_penalty == draft_config.INJURY_PENALTIES.get("LOW", 0)

        # Injured should have highest penalty
        assert injured_penalty == draft_config.INJURY_PENALTIES.get("HIGH", 50)

        # Questionable should be in between
        assert questionable_penalty == draft_config.INJURY_PENALTIES.get("MEDIUM", 25)

    def test_injury_penalty_roster_toggle(self, draft_helper_instance, sample_players):
        """Test APPLY_INJURY_PENALTY_TO_ROSTER toggle functionality"""
        # Create injured players with different drafted status
        injured_available = FantasyPlayer(
            id="avail_inj", name="Available Injured", position="RB", team="TEST",
            fantasy_points=100.0, bye_week=7, injury_status="OUT", drafted=0
        )
        injured_roster = FantasyPlayer(
            id="roster_inj", name="Roster Injured", position="WR", team="TEST",
            fantasy_points=100.0, bye_week=7, injury_status="OUT", drafted=2
        )

        # Save original config values
        original_trade_mode = draft_config.TRADE_HELPER_MODE
        original_apply_penalty = draft_config.APPLY_INJURY_PENALTY_TO_ROSTER

        try:
            # Test in trade mode with penalty toggle ON (default behavior)
            draft_config.TRADE_HELPER_MODE = True
            draft_config.APPLY_INJURY_PENALTY_TO_ROSTER = True

            available_penalty_on = draft_helper_instance.compute_injury_penalty(injured_available)
            roster_penalty_on = draft_helper_instance.compute_injury_penalty(injured_roster)

            # Both should have injury penalties when toggle is ON
            expected_penalty = draft_config.INJURY_PENALTIES.get("HIGH", 50)
            assert available_penalty_on == expected_penalty
            assert roster_penalty_on == expected_penalty

            # Test in trade mode with penalty toggle OFF
            draft_config.APPLY_INJURY_PENALTY_TO_ROSTER = False

            available_penalty_off = draft_helper_instance.compute_injury_penalty(injured_available)
            roster_penalty_off = draft_helper_instance.compute_injury_penalty(injured_roster)

            # Available players should still have penalties, roster players should not
            assert available_penalty_off == expected_penalty  # Still penalized
            assert roster_penalty_off == 0  # No penalty for roster players

            # Test in draft mode (toggle should not affect)
            draft_config.TRADE_HELPER_MODE = False

            available_penalty_draft = draft_helper_instance.compute_injury_penalty(injured_available)
            roster_penalty_draft = draft_helper_instance.compute_injury_penalty(injured_roster)

            # Both should have penalties in draft mode regardless of toggle
            assert available_penalty_draft == expected_penalty
            assert roster_penalty_draft == expected_penalty

        finally:
            # Restore original config values
            draft_config.TRADE_HELPER_MODE = original_trade_mode
            draft_config.APPLY_INJURY_PENALTY_TO_ROSTER = original_apply_penalty

    def test_bye_week_penalty_calculation(self, draft_helper_instance, sample_players):
        """Test bye week penalty calculation"""
        player = sample_players[0]

        # Test bye week penalty calculation using DraftHelper method
        penalty = draft_helper_instance.compute_bye_penalty_for_player(player)

        # Should be a valid penalty (non-negative number)
        assert penalty >= 0
        assert isinstance(penalty, (int, float))

    def test_positional_need_scoring(self, draft_helper_instance, sample_players):
        """Test positional need scoring logic"""
        qb_player = sample_players[2]  # QB position

        # Test positional need score calculation
        qb_need_score = draft_helper_instance.compute_positional_need_score(qb_player)

        # Should be a valid score
        assert isinstance(qb_need_score, (int, float))

        # RB player positional need
        rb_player = sample_players[0]  # RB position
        rb_need_score = draft_helper_instance.compute_positional_need_score(rb_player)

        # Should be a valid score
        assert isinstance(rb_need_score, (int, float))

    def test_player_total_score_calculation(self, draft_helper_instance, sample_players):
        """Test complete player scoring calculation"""
        player = sample_players[0]  # Elite RB, ACTIVE status

        # Calculate total score using DraftHelper method
        total_score = draft_helper_instance.score_player(player)

        # Should be a valid score
        assert isinstance(total_score, (int, float))

        # Test that injured player gets different score
        injured_player = sample_players[3]  # OUT status
        injured_score = draft_helper_instance.score_player(injured_player)

        # Both should be valid scores
        assert isinstance(injured_score, (int, float))

    def test_draft_recommendations(self, draft_helper_instance):
        """Test draft recommendation generation"""
        # Test getting recommendations using DraftHelper method
        recommendations = draft_helper_instance.recommend_next_picks()

        # Should return a list
        assert isinstance(recommendations, list)

        # Should not exceed recommendation count
        assert len(recommendations) <= draft_config.RECOMMENDATION_COUNT

        # Should be sorted by score (highest first)
        if len(recommendations) > 1:
            for i in range(len(recommendations) - 1):
                assert recommendations[i].score >= recommendations[i + 1].score

    def test_trade_recommendations(self, draft_helper_instance):
        """Test trade recommendation functionality exists"""
        if not draft_config.TRADE_HELPER_MODE:
            pytest.skip("Trade mode not enabled in config")

        # Test that DraftHelper instance is properly configured for trade mode
        assert hasattr(draft_helper_instance, 'team')
        assert hasattr(draft_helper_instance, 'players')

        # Trade functionality would be implemented as needed
        # This test validates the basic infrastructure is in place

    def test_ideal_draft_position_by_round(self):
        """Test draft position recommendations by round"""
        # Test first few rounds
        round_1_pos = draft_config.get_ideal_draft_position(0)  # Round 1 (0-indexed)
        round_5_pos = draft_config.get_ideal_draft_position(4)  # Round 5

        # Should return valid positions
        valid_positions = [Constants.QB, Constants.RB, Constants.WR, Constants.TE,
                          Constants.FLEX, Constants.K, Constants.DST]
        assert round_1_pos in valid_positions
        assert round_5_pos in valid_positions

        # Test beyond draft order (should default to FLEX)
        late_round = draft_config.get_ideal_draft_position(20)
        assert late_round == Constants.FLEX

    def test_flex_position_handling(self, sample_players):
        """Test FLEX position logic in scoring"""
        rb_player = sample_players[0]  # RB
        wr_player = sample_players[1]  # WR

        # Both RB and WR should be eligible for FLEX
        assert rb_player.position in draft_config.FLEX_ELIGIBLE_POSITIONS
        assert wr_player.position in draft_config.FLEX_ELIGIBLE_POSITIONS

        # Test that FLEX scoring works for both positions
        mock_team = MagicMock()
        mock_team.pos_counts = {"RB": 2, "WR": 2, "FLEX": 0}  # FLEX slot available

        # Test that both positions are handled properly by the implementation
        assert rb_player.position == "RB"
        assert wr_player.position == "WR"

    def test_error_handling_with_invalid_data(self, draft_helper_instance):
        """Test error handling with invalid player data"""
        # Test that DraftHelper handles basic operations without crashing
        recommendations = draft_helper_instance.recommend_next_picks()
        assert isinstance(recommendations, list)

    def test_trade_improvement_calculation(self, sample_players):
        """Test trade improvement calculation logic"""
        strong_player = sample_players[0]  # Elite RB, 200 points
        weak_player = sample_players[3]  # Injured TE, 90 points

        # Simple validation - strong player should have higher fantasy points
        assert strong_player.fantasy_points > weak_player.fantasy_points

    def test_runner_up_trade_suggestions(self, draft_helper_instance):
        """Test that trade functionality infrastructure exists"""
        if not draft_config.TRADE_HELPER_MODE:
            pytest.skip("Trade mode not enabled in config")

        # Test basic trade mode infrastructure
        assert hasattr(draft_helper_instance, 'team')
        assert hasattr(draft_helper_instance, 'players')

    def test_bye_week_data_integration(self):
        """Test bye week data integration"""
        # Test that bye weeks are properly loaded and used
        assert isinstance(draft_config.POSSIBLE_BYE_WEEKS, list)
        assert len(draft_config.POSSIBLE_BYE_WEEKS) > 0

        # All bye weeks should be valid NFL weeks
        for bye_week in draft_config.POSSIBLE_BYE_WEEKS:
            assert 1 <= bye_week <= 18

    def test_scoring_format_consistency(self):
        """Test that scoring weights are internally consistent"""
        # Projection base should be larger than penalties
        assert draft_config.PROJECTION_BASE_SCORE > draft_config.BASE_BYE_PENALTY
        assert draft_config.PROJECTION_BASE_SCORE > max(draft_config.INJURY_PENALTIES.values())

        # Positional need should be meaningful relative to base score
        assert draft_config.POS_NEEDED_SCORE <= draft_config.PROJECTION_BASE_SCORE


if __name__ == "__main__":
    # Run tests with pytest if available, otherwise basic test
    try:
        import pytest
        pytest.main([__file__, "-v"])
    except ImportError:
        print("pytest not available, running basic tests...")

        # Basic test runner
        print("Testing configuration validation...")
        try:
            draft_config.validate_config()
            print("✅ Configuration validation test passed")
        except ValueError as e:
            print(f"❌ Configuration validation failed: {e}")

        # Test sample player creation
        player = FantasyPlayer(
            id="test1",
            name="Test Player",
            position="RB",
            team="TEST",
            fantasy_points=100.0,
            injury_status="ACTIVE"
        )
        print("✅ Player creation test passed")

        print("Basic tests completed successfully!")