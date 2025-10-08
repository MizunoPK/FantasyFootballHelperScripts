#!/usr/bin/env python3
"""
Unit Tests for Week-Based Prioritization Logic

Tests the new week-based prioritization system that was added as part of the
fantasy points calculation update. This ensures appliedTotal vs projectedTotal
prioritization works correctly based on current NFL week.

Author: Generated for NFL Fantasy Data Collection
Last Updated: September 2025
"""

import pytest
import sys
from pathlib import Path

# Add shared_files directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from fantasy_points_calculator import FantasyPointsExtractor, FantasyPointsConfig


class TestWeekBasedPrioritization:
    """Test week-based prioritization logic for fantasy points extraction"""

    @pytest.fixture
    def extractor(self):
        """Create fantasy points extractor with default config"""
        return FantasyPointsExtractor()

    @pytest.fixture
    def sample_player_data(self):
        """Sample player data with both appliedTotal and projectedTotal"""
        return {
            'player': {
                'stats': [
                    {
                        'seasonId': 2025,
                        'scoringPeriodId': 1,
                        'appliedTotal': 25.5,  # Actual score
                        'projectedTotal': 23.0  # Projected score
                    },
                    {
                        'seasonId': 2025,
                        'scoringPeriodId': 5,
                        'appliedTotal': 18.3,  # Actual score
                        'projectedTotal': 20.5  # Projected score
                    }
                ]
            }
        }

    def test_past_week_prioritization(self, extractor, sample_player_data):
        """Test that past weeks prefer appliedTotal over projectedTotal"""
        # When current NFL week is 3, week 1 is in the past
        points = extractor._extract_from_stats_array(
            sample_player_data, week=1, position="RB", current_nfl_week=3
        )

        # Should prefer appliedTotal (25.5) for past week
        assert points == 25.5

    def test_current_week_prioritization(self, extractor, sample_player_data):
        """Test that current week prefers projectedTotal over appliedTotal"""
        # When current NFL week is 1, week 1 is current
        points = extractor._extract_from_stats_array(
            sample_player_data, week=1, position="RB", current_nfl_week=1
        )

        # Should prefer projectedTotal (23.0) for current week
        assert points == 23.0

    def test_future_week_prioritization(self, extractor, sample_player_data):
        """Test that future weeks prefer projectedTotal over appliedTotal"""
        # When current NFL week is 3, week 5 is in the future
        points = extractor._extract_from_stats_array(
            sample_player_data, week=5, position="RB", current_nfl_week=3
        )

        # Should prefer projectedTotal (20.5) for future week
        assert points == 20.5

    def test_legacy_behavior_without_current_week(self, extractor, sample_player_data):
        """Test that legacy behavior is preserved when current_nfl_week is None"""
        # Without current_nfl_week, should use legacy behavior (prefer appliedTotal)
        points = extractor._extract_from_stats_array(
            sample_player_data, week=1, position="RB", current_nfl_week=None
        )

        # Should prefer appliedTotal (25.5) for legacy compatibility
        assert points == 25.5

    def test_extract_week_points_with_current_week(self, extractor, sample_player_data):
        """Test complete extract_week_points workflow with current_nfl_week"""
        # Test past week
        past_points = extractor.extract_week_points(
            sample_player_data, week=1, position="RB", player_name="Test",
            current_nfl_week=3
        )
        assert past_points == 25.5  # appliedTotal preferred for past week

        # Test current/future week
        future_points = extractor.extract_week_points(
            sample_player_data, week=5, position="RB", player_name="Test",
            current_nfl_week=3
        )
        assert future_points == 20.5  # projectedTotal preferred for future week

    def test_missing_applied_total_fallback(self, extractor):
        """Test fallback to projectedTotal when appliedTotal is missing"""
        player_data = {
            'player': {
                'stats': [
                    {
                        'seasonId': 2025,
                        'scoringPeriodId': 1,
                        # No appliedTotal
                        'projectedTotal': 15.0
                    }
                ]
            }
        }

        # Past week with missing appliedTotal should fall back to projectedTotal
        points = extractor._extract_from_stats_array(
            player_data, week=1, position="RB", current_nfl_week=3
        )
        assert points == 15.0

    def test_missing_projected_total_fallback(self, extractor):
        """Test fallback to appliedTotal when projectedTotal is missing"""
        player_data = {
            'player': {
                'stats': [
                    {
                        'seasonId': 2025,
                        'scoringPeriodId': 5,
                        'appliedTotal': 12.5,
                        # No projectedTotal
                    }
                ]
            }
        }

        # Future week with missing projectedTotal should fall back to appliedTotal
        points = extractor._extract_from_stats_array(
            player_data, week=5, position="RB", current_nfl_week=3
        )
        assert points == 12.5

    def test_week_boundary_conditions(self, extractor, sample_player_data):
        """Test exact boundary conditions for week comparison"""
        # Week exactly equal to current should use projectedTotal
        points_equal = extractor._extract_from_stats_array(
            sample_player_data, week=3, position="RB", current_nfl_week=3
        )
        # No week 3 data in sample, should return None
        assert points_equal is None

        # Test with data that exists at boundary
        boundary_data = {
            'player': {
                'stats': [
                    {
                        'seasonId': 2025,
                        'scoringPeriodId': 3,
                        'appliedTotal': 30.0,
                        'projectedTotal': 28.0
                    }
                ]
            }
        }

        points_boundary = extractor._extract_from_stats_array(
            boundary_data, week=3, position="RB", current_nfl_week=3
        )
        # Week 3 with current_nfl_week=3 should prefer projectedTotal
        assert points_boundary == 28.0

    def test_dst_negative_points_handling(self, extractor):
        """Test that DST negative points are handled correctly with week logic"""
        dst_data = {
            'player': {
                'stats': [
                    {
                        'seasonId': 2025,
                        'scoringPeriodId': 1,
                        'appliedTotal': -2.0,  # Negative actual score
                        'projectedTotal': 8.0   # Positive projected score
                    }
                ]
            }
        }

        # Past week for DST should prefer appliedTotal even if negative
        points = extractor._extract_from_stats_array(
            dst_data, week=1, position="DST", current_nfl_week=3
        )
        assert points == -2.0  # Should allow negative DST points

    def test_non_dst_negative_points_filtering(self, extractor):
        """Test that negative points are filtered for non-DST positions"""
        rb_data = {
            'player': {
                'stats': [
                    {
                        'seasonId': 2025,
                        'scoringPeriodId': 1,
                        'appliedTotal': -1.0,  # Negative actual score
                        'projectedTotal': 5.0   # Positive projected score
                    }
                ]
            }
        }

        # Negative appliedTotal should be filtered out for RB
        points = extractor._extract_from_stats_array(
            rb_data, week=1, position="RB", current_nfl_week=3
        )
        # Should skip negative appliedTotal and return None (no valid positive data)
        assert points is None