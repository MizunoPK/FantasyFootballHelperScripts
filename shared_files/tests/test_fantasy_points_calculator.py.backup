#!/usr/bin/env python3
"""
Unit tests for Fantasy Points Calculator module.

Tests the shared fantasy points calculation functionality including:
- Week-specific fantasy points extraction from ESPN data
- Fallback mechanisms (historical, ADP-based)
- Configuration-driven behavior
- Position-specific handling
- Error handling and validation
"""

import pytest
import sys
import math
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add the parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from fantasy_points_calculator import (
    FantasyPointsConfig, FantasyPointsExtractor,
    extract_week_fantasy_points, extract_stat_entry_fantasy_points
)


class TestFantasyPointsConfig:
    """Test suite for FantasyPointsConfig dataclass"""

    def test_config_initialization_defaults(self):
        """Test config initialization with default values"""
        config = FantasyPointsConfig()

        # Test default settings
        assert config.prefer_actual_over_projected is True
        assert config.include_negative_dst_points is True
        assert config.use_historical_fallback is True
        assert config.use_adp_estimation is True

        # Test default position configs were created
        assert config.position_fallback_configs is not None
        assert 'QB' in config.position_fallback_configs
        assert 'DST' in config.position_fallback_configs
        assert 'DEFAULT' in config.position_fallback_configs

    def test_config_initialization_custom(self):
        """Test config initialization with custom values"""
        custom_configs = {
            'QB': {'base_points': 300.0, 'multiplier': 5.0},
            'DEFAULT': {'base_points': 50.0, 'multiplier': 1.0}
        }

        config = FantasyPointsConfig(
            prefer_actual_over_projected=False,
            include_negative_dst_points=False,
            position_fallback_configs=custom_configs
        )

        assert config.prefer_actual_over_projected is False
        assert config.include_negative_dst_points is False
        assert config.position_fallback_configs == custom_configs

    def test_config_position_fallback_validation(self):
        """Test position fallback configurations are reasonable"""
        config = FantasyPointsConfig()

        # Verify all expected positions have configs
        expected_positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DST', 'DEFAULT']
        for position in expected_positions:
            assert position in config.position_fallback_configs
            assert 'base_points' in config.position_fallback_configs[position]
            assert 'multiplier' in config.position_fallback_configs[position]

        # Verify reasonable values
        qb_config = config.position_fallback_configs['QB']
        assert qb_config['base_points'] > 200  # QBs should have high base
        assert qb_config['multiplier'] > 3     # Reasonable multiplier


class TestFantasyPointsExtractor:
    """Test suite for FantasyPointsExtractor class"""

    @pytest.fixture
    def extractor(self):
        """Create FantasyPointsExtractor instance"""
        return FantasyPointsExtractor()

    @pytest.fixture
    def custom_config_extractor(self):
        """Create extractor with custom config"""
        config = FantasyPointsConfig(
            include_negative_dst_points=False,
            use_historical_fallback=False,
            use_adp_estimation=False
        )
        return FantasyPointsExtractor(config)

    @pytest.fixture
    def sample_espn_player_data(self):
        """Create sample ESPN player data with stats array"""
        return {
            'player': {
                'stats': [
                    {
                        'seasonId': 2025,
                        'scoringPeriodId': 1,
                        'appliedTotal': 25.5,
                        'projectedTotal': 23.0
                    },
                    {
                        'seasonId': 2025,
                        'scoringPeriodId': 2,
                        'appliedTotal': 18.3,
                        'projectedTotal': 20.5
                    },
                    {
                        'seasonId': 2024,  # Historical data
                        'scoringPeriodId': 1,
                        'appliedTotal': 22.0,
                        'projectedTotal': 21.0
                    }
                ]
            }
        }

    def test_extractor_initialization(self):
        """Test extractor initialization"""
        extractor = FantasyPointsExtractor()

        assert extractor.season == 2025
        assert extractor.config is not None
        assert extractor.logger is not None

        # Test with custom season
        extractor_2024 = FantasyPointsExtractor(season=2024)
        assert extractor_2024.season == 2024

    def test_extract_from_stats_array_applied_total(self, extractor, sample_espn_player_data):
        """Test extracting appliedTotal from stats array"""
        points = extractor._extract_from_stats_array(
            sample_espn_player_data, week=1, position="RB"
        )

        # Should prefer appliedTotal (25.5) over projectedTotal (23.0)
        assert points == 25.5

    def test_extract_from_stats_array_projected_total(self, extractor):
        """Test extracting projectedTotal when appliedTotal not available"""
        player_data = {
            'player': {
                'stats': [
                    {
                        'seasonId': 2025,
                        'scoringPeriodId': 1,
                        # No appliedTotal
                        'projectedTotal': 23.0
                    }
                ]
            }
        }

        points = extractor._extract_from_stats_array(
            player_data, week=1, position="RB"
        )

        assert points == 23.0

    def test_extract_from_stats_array_no_data(self, extractor):
        """Test extraction when no relevant data exists"""
        # Empty stats
        player_data = {'player': {'stats': []}}
        points = extractor._extract_from_stats_array(player_data, week=1, position="RB")
        assert points is None

        # No matching week
        player_data = {
            'player': {
                'stats': [
                    {'seasonId': 2025, 'scoringPeriodId': 5, 'appliedTotal': 20.0}
                ]
            }
        }
        points = extractor._extract_from_stats_array(player_data, week=1, position="RB")
        assert points is None

    def test_extract_from_stats_array_negative_dst_allowed(self, extractor):
        """Test that negative points are allowed for DST"""
        player_data = {
            'player': {
                'stats': [
                    {
                        'seasonId': 2025,
                        'scoringPeriodId': 1,
                        'appliedTotal': -5.0  # Negative DST points
                    }
                ]
            }
        }

        points = extractor._extract_from_stats_array(player_data, week=1, position="DST")
        assert points == -5.0

    def test_extract_from_stats_array_negative_non_dst_filtered(self, extractor):
        """Test that negative points are filtered for non-DST positions"""
        player_data = {
            'player': {
                'stats': [
                    {
                        'seasonId': 2025,
                        'scoringPeriodId': 1,
                        'appliedTotal': -5.0  # Negative points for RB
                    }
                ]
            }
        }

        points = extractor._extract_from_stats_array(player_data, week=1, position="RB")
        assert points is None  # Should be filtered out

    def test_extract_from_stats_array_historical_fallback(self, extractor, sample_espn_player_data):
        """Test historical data fallback when current season not available"""
        # Request week that only exists in historical data
        points = extractor._extract_from_stats_array(
            sample_espn_player_data, week=3, position="RB"
        )

        # No current season week 3, should return None (historical handled separately)
        assert points is None

    def test_extract_historical_fallback(self, extractor):
        """Test historical fallback data extraction"""
        fallback_data = {
            'historical_stats': [
                {
                    'scoringPeriodId': 1,
                    'stats': {
                        'appliedTotal': 20.0,
                        'projectedTotal': 18.5
                    }
                }
            ]
        }

        points = extractor._extract_historical_fallback(
            fallback_data, week=1, position="RB"
        )

        assert points == 20.0

    def test_extract_historical_fallback_no_data(self, extractor):
        """Test historical fallback with no matching data"""
        fallback_data = {'historical_stats': []}

        points = extractor._extract_historical_fallback(
            fallback_data, week=1, position="RB"
        )

        assert points is None

    def test_estimate_from_adp_with_mappings(self, extractor):
        """Test ADP estimation with position mappings"""
        fallback_data = {
            'adp': 15.0,
            'position_mappings': {
                'RB': {
                    'min_adp': 1.0,
                    'max_adp': 50.0,
                    'adp_range': 49.0,
                    'min_points': 100.0,
                    'max_points': 300.0,
                    'points_range': 200.0,
                    'correlation': 0.8
                }
            }
        }

        points = extractor._estimate_from_adp(fallback_data, position="RB")

        # Should return reasonable estimated points
        assert points is not None
        assert isinstance(points, float)
        assert points > 0

    def test_estimate_from_adp_without_mappings(self, extractor):
        """Test ADP estimation without position mappings (fallback config)"""
        fallback_data = {
            'adp': 25.0,
            'position_mappings': {}  # No mappings
        }

        points = extractor._estimate_from_adp(fallback_data, position="QB")

        # Should use position fallback config
        assert points is not None
        assert isinstance(points, float)
        assert points > 0

    def test_estimate_from_adp_no_adp(self, extractor):
        """Test ADP estimation with no ADP data"""
        fallback_data = {'position_mappings': {}}

        points = extractor._estimate_from_adp(fallback_data, position="RB")

        assert points is None

    def test_get_position_default(self, extractor):
        """Test position default values"""
        # Test known positions
        assert extractor._get_position_default("QB") == 15.0
        assert extractor._get_position_default("RB") == 8.0
        assert extractor._get_position_default("WR") == 6.0
        assert extractor._get_position_default("TE") == 4.0
        assert extractor._get_position_default("K") == 7.0
        assert extractor._get_position_default("DST") == 5.0

        # Test unknown position
        assert extractor._get_position_default("UNKNOWN") == 3.0

    def test_extract_week_points_complete_workflow(self, extractor, sample_espn_player_data):
        """Test complete week points extraction workflow"""
        points = extractor.extract_week_points(
            sample_espn_player_data, week=1, position="RB", player_name="Test Player"
        )

        # Should extract from current season appliedTotal
        assert points == 25.5

    def test_extract_week_points_with_fallbacks(self, extractor):
        """Test week points extraction with fallback mechanisms"""
        # Player data with no current season data
        player_data = {
            'player': {
                'stats': []  # No current season stats
            }
        }

        fallback_data = {
            'adp': 20.0,
            'position_mappings': {
                'RB': {
                    'min_adp': 1.0,
                    'max_adp': 50.0,
                    'adp_range': 49.0,
                    'min_points': 100.0,
                    'max_points': 300.0,
                    'points_range': 200.0,
                    'correlation': 0.8
                }
            }
        }

        points = extractor.extract_week_points(
            player_data, week=1, position="RB", player_name="Test Player",
            fallback_data=fallback_data
        )

        # Should use ADP estimation
        assert points > 0
        assert isinstance(points, float)

    def test_extract_week_points_position_default_fallback(self, extractor):
        """Test final fallback to position defaults"""
        # Empty player data, no fallback data
        player_data = {'player': {'stats': []}}

        points = extractor.extract_week_points(
            player_data, week=1, position="QB", player_name="Test Player"
        )

        # Should use position default
        assert points == 15.0  # QB default

    def test_extract_week_points_error_handling(self, extractor):
        """Test error handling in week points extraction"""
        # Malformed player data
        malformed_data = {"invalid": "structure"}

        points = extractor.extract_week_points(
            malformed_data, week=1, position="RB", player_name="Test Player"
        )

        # Should return position default on error
        assert points == 8.0  # RB default

    def test_extract_stat_entry_points_applied_total(self, extractor):
        """Test extracting points from stat entry with appliedTotal"""
        stat_entry = {
            'appliedTotal': 25.5,
            'projectedTotal': 23.0
        }

        points = extractor.extract_stat_entry_points(stat_entry)
        assert points == 25.5

    def test_extract_stat_entry_points_projected_total(self, extractor):
        """Test extracting points from stat entry with only projectedTotal"""
        stat_entry = {
            'projectedTotal': 23.0
        }

        points = extractor.extract_stat_entry_points(stat_entry)
        assert points == 23.0

    def test_extract_stat_entry_points_no_data(self, extractor):
        """Test extracting points from empty stat entry"""
        stat_entry = {}
        points = extractor.extract_stat_entry_points(stat_entry)
        assert points == 0.0

        # Test with None
        points = extractor.extract_stat_entry_points(None)
        assert points == 0.0

    def test_extract_stat_entry_points_invalid_data(self, extractor):
        """Test extracting points from stat entry with invalid data"""
        stat_entry = {
            'appliedTotal': 'invalid',
            'projectedTotal': None
        }

        points = extractor.extract_stat_entry_points(stat_entry)
        assert points == 0.0

    def test_custom_config_behavior(self, custom_config_extractor):
        """Test extractor behavior with custom configuration"""
        # Config has use_historical_fallback=False and use_adp_estimation=False

        player_data = {'player': {'stats': []}}
        fallback_data = {
            'adp': 20.0,
            'historical_stats': [{'scoringPeriodId': 1, 'stats': {'appliedTotal': 15.0}}]
        }

        points = custom_config_extractor.extract_week_points(
            player_data, week=1, position="RB", player_name="Test Player",
            fallback_data=fallback_data
        )

        # Should skip historical and ADP, go to position default
        assert points == 8.0  # RB default

    def test_negative_dst_config_behavior(self):
        """Test DST negative points configuration"""
        # Config allowing negative DST points
        config_allow = FantasyPointsConfig(include_negative_dst_points=True)
        extractor_allow = FantasyPointsExtractor(config_allow)

        # Config disallowing negative DST points
        config_disallow = FantasyPointsConfig(include_negative_dst_points=False)
        extractor_disallow = FantasyPointsExtractor(config_disallow)

        player_data = {
            'player': {
                'stats': [
                    {
                        'seasonId': 2025,
                        'scoringPeriodId': 1,
                        'appliedTotal': -3.0
                    }
                ]
            }
        }

        # Allow negative should return -3.0
        points_allow = extractor_allow._extract_from_stats_array(player_data, week=1, position="DST")
        assert points_allow == -3.0

        # Disallow negative should filter it out
        points_disallow = extractor_disallow._extract_from_stats_array(player_data, week=1, position="DST")
        assert points_disallow is None

    def test_season_filtering(self):
        """Test season-specific data filtering"""
        extractor_2024 = FantasyPointsExtractor(season=2024)

        player_data = {
            'player': {
                'stats': [
                    {
                        'seasonId': 2024,
                        'scoringPeriodId': 1,
                        'appliedTotal': 20.0
                    },
                    {
                        'seasonId': 2025,
                        'scoringPeriodId': 1,
                        'appliedTotal': 25.0
                    }
                ]
            }
        }

        points = extractor_2024._extract_from_stats_array(player_data, week=1, position="RB")

        # Should extract 2024 data (20.0) not 2025 data (25.0)
        assert points == 20.0


class TestConvenienceFunctions:
    """Test suite for convenience functions"""

    def test_extract_week_fantasy_points_function(self):
        """Test extract_week_fantasy_points convenience function"""
        player_data = {
            'player': {
                'stats': [
                    {
                        'seasonId': 2025,
                        'scoringPeriodId': 1,
                        'appliedTotal': 25.5
                    }
                ]
            }
        }

        points = extract_week_fantasy_points(
            player_data, week=1, position="RB", player_name="Test Player"
        )

        assert points == 25.5

    def test_extract_week_fantasy_points_with_custom_config(self):
        """Test convenience function with custom config"""
        config = FantasyPointsConfig(include_negative_dst_points=False)

        player_data = {
            'player': {
                'stats': [
                    {
                        'seasonId': 2025,
                        'scoringPeriodId': 1,
                        'appliedTotal': -5.0
                    }
                ]
            }
        }

        points = extract_week_fantasy_points(
            player_data, week=1, position="DST", config=config
        )

        # Should use position default due to negative filtering
        assert points == 5.0  # DST default

    def test_extract_stat_entry_fantasy_points_function(self):
        """Test extract_stat_entry_fantasy_points convenience function"""
        stat_entry = {
            'appliedTotal': 18.5,
            'projectedTotal': 16.0
        }

        points = extract_stat_entry_fantasy_points(stat_entry)
        assert points == 18.5

    def test_module_exports(self):
        """Test that expected classes and functions are exported"""
        from fantasy_points_calculator import __all__

        expected_exports = [
            'FantasyPointsConfig',
            'FantasyPointsExtractor',
            'extract_week_fantasy_points',
            'extract_stat_entry_fantasy_points'
        ]

        for export in expected_exports:
            assert export in __all__


if __name__ == "__main__":
    # Run tests with pytest if available, otherwise basic test
    try:
        import pytest
        pytest.main([__file__, "-v"])
    except ImportError:
        print("pytest not available, running basic tests...")

        # Basic test runner
        print("Testing FantasyPointsConfig...")
        config = FantasyPointsConfig()
        assert config.prefer_actual_over_projected is True
        assert 'QB' in config.position_fallback_configs
        print("✅ FantasyPointsConfig test passed")

        print("Testing FantasyPointsExtractor...")
        extractor = FantasyPointsExtractor()
        assert extractor.season == 2025

        # Test position defaults
        assert extractor._get_position_default("QB") == 15.0
        assert extractor._get_position_default("RB") == 8.0
        print("✅ FantasyPointsExtractor initialization test passed")

        # Test stat entry extraction
        stat_entry = {'appliedTotal': 25.5, 'projectedTotal': 23.0}
        points = extractor.extract_stat_entry_points(stat_entry)
        assert points == 25.5
        print("✅ Stat entry extraction test passed")

        # Test with empty data
        points = extractor.extract_stat_entry_points({})
        assert points == 0.0
        print("✅ Empty stat entry handling test passed")

        # Test convenience functions
        points = extract_stat_entry_fantasy_points(stat_entry)
        assert points == 25.5
        print("✅ Convenience function test passed")

        print("Basic tests completed successfully!")