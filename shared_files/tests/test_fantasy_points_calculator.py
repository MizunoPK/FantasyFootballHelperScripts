#!/usr/bin/env python3
"""
Unit tests for Fantasy Points Calculator module - Pure Week-by-Week System.

Tests the fantasy points calculation functionality including:
- Week-specific fantasy points extraction from ESPN data
- Pure week-by-week system (no fallbacks)
- Configuration-driven behavior
- Position-specific handling
- Error handling and validation
"""

import pytest
import sys
from pathlib import Path

# Add the parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from fantasy_points_calculator import (
    FantasyPointsConfig, FantasyPointsExtractor,
    extract_week_fantasy_points, extract_stat_entry_fantasy_points
)


class TestFantasyPointsConfig:
    """Test suite for FantasyPointsConfig dataclass"""

    def test_config_initialization_defaults(self):
        """Test config initialization with default values - pure week-by-week system"""
        config = FantasyPointsConfig()

        # Test default settings (pure week-by-week system)
        assert config.prefer_actual_over_projected is True
        assert config.include_negative_dst_points is True

    def test_config_initialization_custom(self):
        """Test config initialization with custom values"""
        config = FantasyPointsConfig(
            prefer_actual_over_projected=False,
            include_negative_dst_points=False
        )

        assert config.prefer_actual_over_projected is False
        assert config.include_negative_dst_points is False


class TestFantasyPointsExtractor:
    """Test suite for FantasyPointsExtractor class"""

    @pytest.fixture
    def extractor(self):
        """Create a FantasyPointsExtractor instance for testing"""
        return FantasyPointsExtractor()

    def test_extractor_initialization(self, extractor):
        """Test extractor initialization with default config"""
        assert isinstance(extractor.config, FantasyPointsConfig)
        assert extractor.season == 2025

        # Test default config values
        assert extractor.config.prefer_actual_over_projected is True
        assert extractor.config.include_negative_dst_points is True

    def test_extract_from_stats_array_applied_total(self, extractor):
        """Test extracting appliedTotal from stats array"""
        player_data = {
            'player': {
                'stats': [{
                    'seasonId': 2025,
                    'scoringPeriodId': 1,
                    'appliedTotal': 25.5,
                    'projectedTotal': 20.0
                }]
            }
        }

        points = extractor._extract_from_stats_array(player_data, week=1, position="QB")
        assert points == 25.5

    def test_extract_from_stats_array_projected_total(self, extractor):
        """Test extracting projectedTotal when appliedTotal is not available"""
        player_data = {
            'player': {
                'stats': [{
                    'seasonId': 2025,
                    'scoringPeriodId': 1,
                    'projectedTotal': 18.5
                }]
            }
        }

        points = extractor._extract_from_stats_array(player_data, week=1, position="QB")
        assert points == 18.5

    def test_extract_from_stats_array_no_data(self, extractor):
        """Test extracting from stats array with no data"""
        player_data = {'player': {'stats': []}}

        points = extractor._extract_from_stats_array(player_data, week=1, position="QB")
        assert points is None

    def test_extract_from_stats_array_negative_dst_allowed(self, extractor):
        """Test that negative points are allowed for DST positions"""
        player_data = {
            'player': {
                'stats': [{
                    'seasonId': 2025,
                    'scoringPeriodId': 1,
                    'appliedTotal': -5.0
                }]
            }
        }

        points = extractor._extract_from_stats_array(player_data, week=1, position="DST")
        assert points == -5.0

    def test_extract_from_stats_array_negative_non_dst_filtered(self, extractor):
        """Test that negative points are filtered for non-DST positions"""
        player_data = {
            'player': {
                'stats': [{
                    'seasonId': 2025,
                    'scoringPeriodId': 1,
                    'appliedTotal': -3.0
                }]
            }
        }

        points = extractor._extract_from_stats_array(player_data, week=1, position="QB")
        assert points is None

    def test_extract_week_points_complete_workflow(self, extractor):
        """Test complete workflow with ESPN data available"""
        player_data = {
            'player': {
                'stats': [{
                    'seasonId': 2025,
                    'scoringPeriodId': 3,
                    'appliedTotal': 22.8
                }]
            }
        }

        points = extractor.extract_week_points(
            player_data, week=3, position="RB", player_name="Test Player"
        )
        assert points == 22.8

    def test_extract_week_points_no_data_returns_zero(self, extractor):
        """Test that extract_week_points returns 0.0 when no ESPN data available (pure week-by-week)"""
        empty_player_data = {'player': {'stats': []}}

        points = extractor.extract_week_points(
            empty_player_data, week=1, position="QB", player_name="Test Player"
        )

        # Pure week-by-week system: should return 0.0, not position default
        assert points == 0.0

    def test_extract_week_points_error_handling(self, extractor):
        """Test error handling returns 0.0 (pure week-by-week system)"""
        malformed_data = {'invalid': 'data'}

        points = extractor.extract_week_points(
            malformed_data, week=1, position="RB", player_name="Test Player"
        )

        # Should return 0.0 on error, not position default
        assert points == 0.0

    def test_extract_stat_entry_points_applied_total(self, extractor):
        """Test extracting points from a single stat entry with appliedTotal"""
        stat_entry = {'appliedTotal': 15.2, 'projectedTotal': 12.0}

        points = extractor.extract_stat_entry_points(stat_entry)
        assert points == 15.2

    def test_extract_stat_entry_points_projected_total(self, extractor):
        """Test extracting points from a single stat entry with only projectedTotal"""
        stat_entry = {'projectedTotal': 10.5}

        points = extractor.extract_stat_entry_points(stat_entry)
        assert points == 10.5

    def test_extract_stat_entry_points_no_data(self, extractor):
        """Test extracting from stat entry with no points data"""
        stat_entry = {'someOtherField': 'value'}

        points = extractor.extract_stat_entry_points(stat_entry)
        assert points == 0.0

    def test_extract_stat_entry_points_invalid_data(self, extractor):
        """Test extracting from invalid stat entry"""
        points = extractor.extract_stat_entry_points({})
        assert points == 0.0

    def test_negative_dst_config_behavior(self):
        """Test DST negative points configuration with position-aware extraction"""
        # Test with negative DST points allowed (default) using position-aware method
        config = FantasyPointsConfig(include_negative_dst_points=True)
        extractor = FantasyPointsExtractor(config)

        player_data = {
            'player': {
                'stats': [{
                    'seasonId': 2025,
                    'scoringPeriodId': 1,
                    'appliedTotal': -3.0
                }]
            }
        }

        # For DST position, negative points should be allowed
        points = extractor._extract_from_stats_array(player_data, week=1, position="DST")
        assert points == -3.0

        # Test with negative DST points disabled
        config = FantasyPointsConfig(include_negative_dst_points=False)
        extractor = FantasyPointsExtractor(config)

        # For DST position with disabled negative points, should return None (filtered out)
        points = extractor._extract_from_stats_array(player_data, week=1, position="DST")
        assert points is None

        # Note: extract_stat_entry_points doesn't know position, so it always returns the raw value

    def test_season_filtering(self, extractor):
        """Test that only current season data is used (no historical fallback)"""
        player_data = {
            'player': {
                'stats': [
                    {
                        'seasonId': 2024,  # Previous season - should be ignored
                        'scoringPeriodId': 1,
                        'appliedTotal': 30.0
                    },
                    {
                        'seasonId': 2025,  # Current season - should be used
                        'scoringPeriodId': 1,
                        'appliedTotal': 20.0
                    }
                ]
            }
        }

        points = extractor._extract_from_stats_array(player_data, week=1, position="QB")
        # Should only use current season data (20.0), not historical (30.0)
        assert points == 20.0


class TestConvenienceFunctions:
    """Test suite for module-level convenience functions"""

    def test_extract_week_fantasy_points_function(self):
        """Test the module-level extract_week_fantasy_points function"""
        player_data = {
            'player': {
                'stats': [{
                    'seasonId': 2025,
                    'scoringPeriodId': 5,
                    'appliedTotal': 18.7
                }]
            }
        }

        points = extract_week_fantasy_points(player_data, week=5, position="WR")
        assert points == 18.7

    def test_extract_week_fantasy_points_no_data_returns_zero(self):
        """Test convenience function returns 0.0 when no data (pure week-by-week)"""
        empty_data = {'player': {'stats': []}}

        points = extract_week_fantasy_points(empty_data, week=1, position="RB")

        # Pure week-by-week system: should return 0.0
        assert points == 0.0

    def test_extract_stat_entry_fantasy_points_function(self):
        """Test the module-level extract_stat_entry_fantasy_points function"""
        stat_entry = {'projectedTotal': 14.3}

        points = extract_stat_entry_fantasy_points(stat_entry)
        assert points == 14.3

    def test_module_exports(self):
        """Test that all expected classes and functions are exported"""
        from fantasy_points_calculator import FantasyPointsConfig, FantasyPointsExtractor
        from fantasy_points_calculator import extract_week_fantasy_points, extract_stat_entry_fantasy_points

        # Test classes exist and are callable
        assert callable(FantasyPointsConfig)
        assert callable(FantasyPointsExtractor)

        # Test functions exist and are callable
        assert callable(extract_week_fantasy_points)
        assert callable(extract_stat_entry_fantasy_points)

        print("✅ All fantasy points calculator tests passed - pure week-by-week system working!")


# Test configuration for pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v"])