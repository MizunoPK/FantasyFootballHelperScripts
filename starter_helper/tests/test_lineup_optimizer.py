#!/usr/bin/env python3
"""
Unit tests for Lineup Optimizer module.

Tests the lineup optimization functionality including:
- Starting recommendation creation and validation
- Position candidate ranking and selection
- Optimal lineup generation with FLEX handling
- Injury and bye week penalty calculations
- Bench recommendations
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
import pandas as pd

# Add the parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from lineup_optimizer import LineupOptimizer, OptimalLineup, StartingRecommendation
from shared_files.configs.starter_helper_config import (
    STARTING_LINEUP_REQUIREMENTS, FLEX_ELIGIBLE_POSITIONS,
    INJURY_PENALTIES, BYE_WEEK_PENALTY, CURRENT_NFL_WEEK,
    QB, RB, WR, TE, K, DST, FLEX
)


class TestStartingRecommendation:
    """Test suite for StartingRecommendation dataclass"""

    def test_starting_recommendation_creation(self):
        """Test creating a StartingRecommendation"""
        rec = StartingRecommendation(
            player_id="123",
            name="Test Player",
            position="RB",
            team="TEST",
            projected_points=15.5,
            injury_status="ACTIVE",
            bye_week=7,
            adjusted_score=15.5,
            reason="No penalties"
        )

        assert rec.player_id == "123"
        assert rec.name == "Test Player"
        assert rec.position == "RB"
        assert rec.projected_points == 15.5
        assert rec.adjusted_score == 15.5
        assert rec.reason == "No penalties"

    def test_starting_recommendation_with_penalties(self):
        """Test StartingRecommendation with injury and bye week penalties"""
        rec = StartingRecommendation(
            player_id="456",
            name="Injured Player",
            position="WR",
            team="INJ",
            projected_points=20.0,
            injury_status="QUESTIONABLE",
            bye_week=CURRENT_NFL_WEEK,
            adjusted_score=10.0,  # After penalties
            reason="-5 injury penalty (QUESTIONABLE); -5 bye week penalty"
        )

        assert rec.projected_points == 20.0
        assert rec.adjusted_score == 10.0
        assert "injury penalty" in rec.reason
        assert "bye week penalty" in rec.reason


class TestOptimalLineup:
    """Test suite for OptimalLineup dataclass"""

    @pytest.fixture
    def sample_lineup(self):
        """Create sample optimal lineup"""
        lineup = OptimalLineup()
        lineup.qb = StartingRecommendation("1", "QB1", "QB", "QB", 25.0, "ACTIVE", 5, 25.0)
        lineup.rb1 = StartingRecommendation("2", "RB1", "RB", "RB", 20.0, "ACTIVE", 6, 20.0)
        lineup.rb2 = StartingRecommendation("3", "RB2", "RB", "RB", 18.0, "ACTIVE", 7, 18.0)
        lineup.wr1 = StartingRecommendation("4", "WR1", "WR", "WR", 16.0, "ACTIVE", 8, 16.0)
        lineup.wr2 = StartingRecommendation("5", "WR2", "WR", "WR", 14.0, "ACTIVE", 9, 14.0)
        lineup.te = StartingRecommendation("6", "TE1", "TE", "TE", 12.0, "ACTIVE", 10, 12.0)
        lineup.flex = StartingRecommendation("7", "FLEX", "WR", "WR", 13.0, "ACTIVE", 11, 13.0)
        lineup.k = StartingRecommendation("8", "K1", "K", "K", 10.0, "ACTIVE", 12, 10.0)
        lineup.dst = StartingRecommendation("9", "DST1", "DST", "DST", 8.0, "ACTIVE", 13, 8.0)
        return lineup

    def test_optimal_lineup_total_projected_points(self, sample_lineup):
        """Test total projected points calculation"""
        expected_total = 25.0 + 20.0 + 18.0 + 16.0 + 14.0 + 12.0 + 13.0 + 10.0 + 8.0
        assert sample_lineup.total_projected_points == expected_total

    def test_optimal_lineup_get_all_starters(self, sample_lineup):
        """Test getting all starters in order"""
        starters = sample_lineup.get_all_starters()

        assert len(starters) == 9
        assert starters[0] == sample_lineup.qb
        assert starters[1] == sample_lineup.rb1
        assert starters[2] == sample_lineup.rb2
        assert starters[6] == sample_lineup.flex
        assert starters[8] == sample_lineup.dst

    def test_optimal_lineup_with_missing_positions(self):
        """Test lineup with some missing positions"""
        lineup = OptimalLineup()
        lineup.qb = StartingRecommendation("1", "QB1", "QB", "QB", 25.0, "ACTIVE", 5, 25.0)
        # Missing other positions

        assert lineup.total_projected_points == 25.0
        starters = lineup.get_all_starters()
        assert starters[0] is not None  # QB exists
        assert starters[1] is None  # RB1 missing


class TestLineupOptimizer:
    """Test suite for LineupOptimizer class"""

    @pytest.fixture
    def param_manager(self):
        """Create ParameterJsonManager instance"""
        from shared_files.parameter_json_manager import ParameterJsonManager
        import os
        param_path = os.path.join(os.path.dirname(__file__), '..', '..', 'shared_files', 'parameters.json')
        return ParameterJsonManager(param_path)

    @pytest.fixture
    def optimizer(self, param_manager):
        """Create LineupOptimizer instance"""
        return LineupOptimizer(param_manager=param_manager)

    @pytest.fixture
    def sample_roster_data(self):
        """Create sample roster DataFrame"""
        data = {
            'id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'name': ['Josh Allen', 'CMC', 'Breece Hall', 'Tyreek Hill', 'Davante Adams',
                    'Travis Kelce', 'Jaylen Waddle', 'Justin Tucker', 'Bills DST', 'Backup RB'],
            'position': ['QB', 'RB', 'RB', 'WR', 'WR', 'TE', 'WR', 'K', 'DST', 'RB'],
            'team': ['BUF', 'SF', 'NYJ', 'MIA', 'LV', 'KC', 'MIA', 'BAL', 'BUF', 'BENCH'],
            'injury_status': ['ACTIVE', 'ACTIVE', 'QUESTIONABLE', 'ACTIVE', 'ACTIVE',
                            'ACTIVE', 'OUT', 'ACTIVE', 'ACTIVE', 'ACTIVE'],
            'bye_week': [12, 9, 11, 6, 13, 10, 6, 14, 12, 5]
        }
        return pd.DataFrame(data)

    @pytest.fixture
    def sample_projections(self):
        """Create sample projections dictionary"""
        return {
            '1': 28.5,  # Josh Allen
            '2': 22.3,  # CMC
            '3': 18.7,  # Breece Hall
            '4': 19.2,  # Tyreek Hill
            '5': 16.8,  # Davante Adams
            '6': 14.1,  # Travis Kelce
            '7': 15.4,  # Jaylen Waddle
            '8': 9.2,   # Justin Tucker
            '9': 11.5,  # Bills DST
            '10': 8.3   # Backup RB
        }

    def test_calculate_adjusted_score_no_penalties(self, optimizer):
        """Test adjusted score calculation with no penalties (ACTIVE player)"""
        adjusted_score, reason = optimizer.calculate_adjusted_score(20.0, "ACTIVE", 5)

        assert adjusted_score == 20.0
        assert "No adjustments" in reason

    def test_calculate_adjusted_score_questionable_allowed(self, optimizer):
        """Test that QUESTIONABLE players are allowed to play (binary injury system)"""
        adjusted_score, reason = optimizer.calculate_adjusted_score(20.0, "QUESTIONABLE", 5)

        # QUESTIONABLE is in STARTER_HELPER_ACTIVE_STATUSES, so full score
        assert adjusted_score == 20.0
        assert "No adjustments" in reason

    def test_calculate_adjusted_score_inactive_zeroed(self, optimizer):
        """Test that inactive players get zeroed out (binary injury system)"""
        # Test various inactive statuses
        inactive_statuses = ["OUT", "DOUBTFUL", "INJURY_RESERVE", "SUSPENSION", "HIGH"]

        for status in inactive_statuses:
            adjusted_score, reason = optimizer.calculate_adjusted_score(20.0, status, 5)

            # All non-ACTIVE/QUESTIONABLE players should be zeroed out
            assert adjusted_score == 0.0, f"Player with status {status} should be zeroed"
            assert "Inactive" in reason, f"Reason should mention inactive for status {status}"
            assert status in reason, f"Reason should include status {status}"

    def test_calculate_adjusted_score_out_player(self, optimizer):
        """Test adjusted score for OUT player (should be zero)"""
        adjusted_score, reason = optimizer.calculate_adjusted_score(15.0, "OUT", 5)

        # OUT players should be zeroed out
        assert adjusted_score == 0.0
        assert "Inactive" in reason
        assert "OUT" in reason

    def test_calculate_adjusted_score_bye_week_ignored(self, optimizer):
        """Test that bye week is ignored in new scoring system"""
        # Bye week should not affect score anymore
        adjusted_score, reason = optimizer.calculate_adjusted_score(20.0, "ACTIVE", CURRENT_NFL_WEEK)

        # Score should remain unchanged (no bye week penalty)
        assert adjusted_score == 20.0
        assert "No adjustments" in reason
        assert "bye" not in reason.lower()

    def test_create_starting_recommendation(self, optimizer, sample_roster_data):
        """Test creating a starting recommendation from player data"""
        player_data = sample_roster_data.iloc[0].to_dict()  # Josh Allen
        projected_points = 28.5

        rec = optimizer.create_starting_recommendation(player_data, projected_points)

        assert rec.player_id == "1"
        assert rec.name == "Josh Allen"
        assert rec.position == "QB"
        assert rec.team == "BUF"
        assert rec.projected_points == 28.5
        assert rec.injury_status == "ACTIVE"
        assert rec.bye_week == 12
        # Adjusted score may include positional ranking adjustments
        assert rec.adjusted_score >= 28.5  # Should be at least the base score

    def test_get_position_candidates_regular_position(self, optimizer, sample_roster_data, sample_projections):
        """Test getting candidates for a regular position"""
        candidates = optimizer.get_position_candidates(sample_roster_data, sample_projections, "RB")

        # Should find 3 RBs (CMC, Breece Hall, Backup RB)
        assert len(candidates) == 3

        # Should be sorted by adjusted score (highest first)
        assert candidates[0].projected_points >= candidates[1].projected_points

        # Verify all are RBs
        for candidate in candidates:
            assert candidate.position == "RB"

    def test_get_position_candidates_flex_position(self, optimizer, sample_roster_data, sample_projections):
        """Test getting candidates for FLEX position"""
        candidates = optimizer.get_position_candidates(sample_roster_data, sample_projections, FLEX)

        # Should find all RBs and WRs
        rb_wr_count = len(sample_roster_data[sample_roster_data['position'].isin(['RB', 'WR'])])
        assert len(candidates) == rb_wr_count

        # Verify all are FLEX-eligible
        for candidate in candidates:
            assert candidate.position in FLEX_ELIGIBLE_POSITIONS

    def test_optimize_lineup_complete(self, optimizer, sample_roster_data, sample_projections):
        """Test complete lineup optimization"""
        lineup = optimizer.optimize_lineup(sample_roster_data, sample_projections)

        # Verify all positions are filled (we have enough players)
        assert lineup.qb is not None
        assert lineup.rb1 is not None
        assert lineup.rb2 is not None
        assert lineup.wr1 is not None
        assert lineup.wr2 is not None
        assert lineup.te is not None
        assert lineup.flex is not None
        assert lineup.k is not None
        assert lineup.dst is not None

        # Verify no duplicate players
        used_ids = set()
        for starter in lineup.get_all_starters():
            if starter:
                assert starter.player_id not in used_ids
                used_ids.add(starter.player_id)

    def test_optimize_lineup_position_constraints(self, optimizer, sample_roster_data, sample_projections):
        """Test that lineup optimization respects position constraints"""
        lineup = optimizer.optimize_lineup(sample_roster_data, sample_projections)

        # Verify position constraints
        assert lineup.qb.position == "QB"
        assert lineup.rb1.position == "RB"
        assert lineup.rb2.position == "RB"
        assert lineup.wr1.position == "WR"
        assert lineup.wr2.position == "WR"
        assert lineup.te.position == "TE"
        assert lineup.flex.position in FLEX_ELIGIBLE_POSITIONS
        assert lineup.k.position == "K"
        assert lineup.dst.position == "DST"

    def test_optimize_lineup_with_limited_players(self, optimizer):
        """Test lineup optimization with limited players"""
        # Create minimal roster
        minimal_data = {
            'id': [1, 2],
            'name': ['Only QB', 'Only RB'],
            'position': ['QB', 'RB'],
            'team': ['TEST', 'TEST'],
            'injury_status': ['ACTIVE', 'ACTIVE'],
            'bye_week': [5, 6]
        }
        minimal_roster = pd.DataFrame(minimal_data)
        minimal_projections = {'1': 20.0, '2': 15.0}

        lineup = optimizer.optimize_lineup(minimal_roster, minimal_projections)

        # Should fill available positions
        assert lineup.qb is not None
        assert lineup.rb1 is not None

        # Missing positions should be None
        assert lineup.rb2 is None
        assert lineup.wr1 is None
        assert lineup.te is None

    def test_get_bench_recommendations(self, optimizer, sample_roster_data, sample_projections):
        """Test getting bench recommendations"""
        # Simulate used players (starting lineup)
        used_player_ids = {'1', '2', '3', '4', '5', '6', '8', '9'}  # Missing one for bench

        bench_recs = optimizer.get_bench_recommendations(
            sample_roster_data, sample_projections, used_player_ids, count=3
        )

        # Should return available bench players
        assert len(bench_recs) > 0
        assert len(bench_recs) <= 3

        # Verify none are in used_player_ids
        for rec in bench_recs:
            assert rec.player_id not in used_player_ids

        # Should be sorted by adjusted score
        if len(bench_recs) > 1:
            for i in range(len(bench_recs) - 1):
                assert bench_recs[i].adjusted_score >= bench_recs[i + 1].adjusted_score

    def test_injury_status_handling(self, optimizer):
        """Test that injury status uses binary system (OUT players zeroed)"""
        player_data = {
            'id': 1,
            'name': 'Test Player',
            'position': 'RB',
            'team': 'TEST',
            'injury_status': 'OUT',
            'bye_week': 5
        }

        rec = optimizer.create_starting_recommendation(player_data, 20.0)

        assert rec.injury_status == 'OUT'
        # Binary injury system: OUT players get zero score
        assert rec.adjusted_score == 0.0
        assert "Inactive" in rec.reason

    def test_bye_week_current_week_handling(self, optimizer):
        """Test that bye week is ignored in new scoring system"""
        player_data = {
            'id': 1,
            'name': 'Bye Week Player',
            'position': 'WR',
            'team': 'BYE',
            'injury_status': 'ACTIVE',
            'bye_week': CURRENT_NFL_WEEK
        }

        rec = optimizer.create_starting_recommendation(player_data, 15.0)

        assert rec.bye_week == CURRENT_NFL_WEEK
        # Bye week should NOT affect score in new system
        assert rec.adjusted_score == 15.0
        assert "bye" not in rec.reason.lower()

    def test_negative_adjusted_score_handling(self, optimizer):
        """Test that adjusted scores don't go below 0"""
        player_data = {
            'id': 1,
            'name': 'Heavily Penalized',
            'position': 'RB',
            'team': 'PEN',
            'injury_status': 'OUT',
            'bye_week': CURRENT_NFL_WEEK
        }

        # Low projected points that would go negative after penalties
        rec = optimizer.create_starting_recommendation(player_data, 2.0)

        # Adjusted score should not be negative
        assert rec.adjusted_score >= 0.0

    def test_flex_optimization_logic(self, optimizer, sample_roster_data, sample_projections):
        """Test that FLEX gets the best available RB or WR"""
        lineup = optimizer.optimize_lineup(sample_roster_data, sample_projections)

        # FLEX should be the best remaining RB or WR after filling required positions
        flex_player = lineup.flex
        assert flex_player is not None
        assert flex_player.position in FLEX_ELIGIBLE_POSITIONS

        # Get all RB/WR candidates
        all_flex_candidates = optimizer.get_position_candidates(sample_roster_data, sample_projections, FLEX)

        # FLEX should be among the top candidates (accounting for already used players)
        used_ids = {lineup.rb1.player_id, lineup.rb2.player_id, lineup.wr1.player_id, lineup.wr2.player_id}
        available_flex = [c for c in all_flex_candidates if c.player_id not in used_ids]

        if available_flex:
            # FLEX should be the best available
            assert flex_player.player_id == available_flex[0].player_id


if __name__ == "__main__":
    # Run tests with pytest if available, otherwise basic test
    try:
        import pytest
        pytest.main([__file__, "-v"])
    except ImportError:
        print("pytest not available, running basic tests...")

        # Basic test runner
        optimizer = LineupOptimizer()

        # Test basic functionality
        # Use bye week different from CURRENT_NFL_WEEK to avoid bye penalty
        bye_week_no_penalty = CURRENT_NFL_WEEK + 3 if CURRENT_NFL_WEEK < 15 else CURRENT_NFL_WEEK - 3
        adjusted_score, reason = optimizer.calculate_adjusted_score(20.0, "ACTIVE", bye_week_no_penalty)
        assert adjusted_score == 20.0
        assert reason == "No penalties"
        print("✅ Basic adjusted score calculation test passed")

        # Test with penalties
        adjusted_score, reason = optimizer.calculate_adjusted_score(15.0, "QUESTIONABLE", CURRENT_NFL_WEEK)
        assert adjusted_score < 15.0
        assert "penalty" in reason
        print("✅ Penalty calculation test passed")

        # Test OptimalLineup
        lineup = OptimalLineup()
        lineup.qb = StartingRecommendation("1", "Test QB", "QB", "TEST", 25.0, "ACTIVE", 5, 25.0)
        assert lineup.total_projected_points == 25.0
        print("✅ OptimalLineup test passed")

        # Test starting recommendation creation
        player_data = {
            'id': 1,
            'name': 'Test Player',
            'position': 'RB',
            'team': 'TEST',
            'injury_status': 'ACTIVE',
            'bye_week': 5
        }
        rec = optimizer.create_starting_recommendation(player_data, 18.0)
        assert rec.name == 'Test Player'
        assert rec.projected_points == 18.0
        print("✅ Starting recommendation creation test passed")

        print("Basic tests completed successfully!")