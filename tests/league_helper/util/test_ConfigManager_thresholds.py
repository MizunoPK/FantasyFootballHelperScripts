"""
Unit Tests for ConfigManager Threshold Calculation System

Tests the parameterized threshold calculation system:
- validate_threshold_params() validation logic
- calculate_thresholds() for all 4 direction types
- Threshold caching behavior
- _extract_parameters() pre-calculation
- Backward compatibility with hardcoded thresholds

Author: Claude Code
Date: 2025-10-16
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
import json
import tempfile

# Imports work via conftest.py which adds the necessary paths
from util.ConfigManager import ConfigManager, ConfigKeys


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def config_keys():
    """Provide ConfigKeys instance for tests"""
    return ConfigKeys()


@pytest.fixture
def temp_data_folder():
    """Create temporary data folder for testing"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def minimal_hardcoded_config(temp_data_folder):
    """Create minimal config with hardcoded thresholds (old format)"""
    config_content = {
        "config_name": "Test Hardcoded Config",
        "description": "Test configuration with hardcoded thresholds",
        "parameters": {
            "CURRENT_NFL_WEEK": 6,
            "NFL_SEASON": 2025,
            "NFL_SCORING_FORMAT": "ppr",
            "NORMALIZATION_MAX_SCALE": 100.0,
            "BASE_BYE_PENALTY": 25.0,
            "INJURY_PENALTIES": {"LOW": 0, "MEDIUM": 10.0, "HIGH": 75.0},
            "DRAFT_ORDER_BONUSES": {"PRIMARY": 50, "SECONDARY": 30},
            "DRAFT_ORDER": [{"FLEX": "P", "QB": "S"}],
            "ADP_SCORING": {
                "THRESHOLDS": {
                    "VERY_POOR": 150,
                    "POOR": 100,
                    "GOOD": 50,
                    "EXCELLENT": 20
                },
                "MULTIPLIERS": {"EXCELLENT": 1.20, "GOOD": 1.10, "POOR": 0.90, "VERY_POOR": 0.70},
                "WEIGHT": 1.0
            },
            "PLAYER_RATING_SCORING": {
                "THRESHOLDS": {
                    "VERY_POOR": 20,
                    "POOR": 40,
                    "GOOD": 60,
                    "EXCELLENT": 80
                },
                "MULTIPLIERS": {"EXCELLENT": 1.25, "GOOD": 1.15, "POOR": 0.95, "VERY_POOR": 0.75},
                "WEIGHT": 1.0
            },
            "TEAM_QUALITY_SCORING": {
                "THRESHOLDS": {
                    "VERY_POOR": 25,
                    "POOR": 18,
                    "GOOD": 10,
                    "EXCELLENT": 5
                },
                "MULTIPLIERS": {"EXCELLENT": 1.30, "GOOD": 1.15, "POOR": 0.85, "VERY_POOR": 0.70},
                "WEIGHT": 1.0
            },
            "PERFORMANCE_SCORING": {
                "MIN_WEEKS": 3,
                "THRESHOLDS": {
                    "VERY_POOR": -0.2,
                    "POOR": -0.1,
                    "GOOD": 0.1,
                    "EXCELLENT": 0.2
                },
                "MULTIPLIERS": {"VERY_POOR": 0.60, "POOR": 0.80, "GOOD": 1.20, "EXCELLENT": 1.50},
                "WEIGHT": 1.0
            },
            "MATCHUP_SCORING": {
                "THRESHOLDS": {
                    "VERY_POOR": -15,
                    "POOR": -6,
                    "GOOD": 6,
                    "EXCELLENT": 15
                },
                "MULTIPLIERS": {"EXCELLENT": 1.25, "GOOD": 1.10, "POOR": 0.90, "VERY_POOR": 0.75},
                "WEIGHT": 1.0
            }
        }
    }

    config_file = temp_data_folder / "league_config.json"
    with open(config_file, 'w') as f:
        json.dump(config_content, f, indent=2)

    return temp_data_folder


@pytest.fixture
def parameterized_config(temp_data_folder):
    """Create config with parameterized thresholds (new format)"""
    config_content = {
        "config_name": "Test Parameterized Config",
        "description": "Test configuration with parameterized thresholds",
        "parameters": {
            "CURRENT_NFL_WEEK": 6,
            "NFL_SEASON": 2025,
            "NFL_SCORING_FORMAT": "ppr",
            "NORMALIZATION_MAX_SCALE": 100.0,
            "BASE_BYE_PENALTY": 25.0,
            "INJURY_PENALTIES": {"LOW": 0, "MEDIUM": 10.0, "HIGH": 75.0},
            "DRAFT_ORDER_BONUSES": {"PRIMARY": 50, "SECONDARY": 30},
            "DRAFT_ORDER": [{"FLEX": "P", "QB": "S"}],
            "ADP_SCORING": {
                "THRESHOLDS": {
                    "BASE_POSITION": 0,
                    "DIRECTION": "DECREASING",
                    "STEPS": 37.5
                },
                "MULTIPLIERS": {"EXCELLENT": 1.20, "GOOD": 1.10, "POOR": 0.90, "VERY_POOR": 0.70},
                "WEIGHT": 1.0
            },
            "PLAYER_RATING_SCORING": {
                "THRESHOLDS": {
                    "BASE_POSITION": 0,
                    "DIRECTION": "INCREASING",
                    "STEPS": 20
                },
                "MULTIPLIERS": {"EXCELLENT": 1.25, "GOOD": 1.15, "POOR": 0.95, "VERY_POOR": 0.75},
                "WEIGHT": 1.0
            },
            "TEAM_QUALITY_SCORING": {
                "THRESHOLDS": {
                    "BASE_POSITION": 0,
                    "DIRECTION": "DECREASING",
                    "STEPS": 6.25
                },
                "MULTIPLIERS": {"EXCELLENT": 1.30, "GOOD": 1.15, "POOR": 0.85, "VERY_POOR": 0.70},
                "WEIGHT": 1.0
            },
            "PERFORMANCE_SCORING": {
                "MIN_WEEKS": 3,
                "THRESHOLDS": {
                    "BASE_POSITION": 0.0,
                    "DIRECTION": "BI_EXCELLENT_HI",
                    "STEPS": 0.1
                },
                "MULTIPLIERS": {"VERY_POOR": 0.60, "POOR": 0.80, "GOOD": 1.20, "EXCELLENT": 1.50},
                "WEIGHT": 1.0
            },
            "MATCHUP_SCORING": {
                "THRESHOLDS": {
                    "BASE_POSITION": 0,
                    "DIRECTION": "BI_EXCELLENT_HI",
                    "STEPS": 7.5
                },
                "MULTIPLIERS": {"EXCELLENT": 1.25, "GOOD": 1.10, "POOR": 0.90, "VERY_POOR": 0.75},
                "WEIGHT": 1.0
            }
        }
    }

    config_file = temp_data_folder / "league_config.json"
    with open(config_file, 'w') as f:
        json.dump(config_content, f, indent=2)

    return temp_data_folder


# ============================================================================
# VALIDATION TESTS
# ============================================================================

class TestValidateThresholdParams:
    """Test validate_threshold_params() validation logic"""

    def test_valid_params_increasing(self, minimal_hardcoded_config):
        """Valid parameters should return True"""
        config = ConfigManager(minimal_hardcoded_config)
        assert config.validate_threshold_params(0, "INCREASING", 20) is True

    def test_valid_params_decreasing(self, minimal_hardcoded_config):
        """Valid DECREASING parameters should return True"""
        config = ConfigManager(minimal_hardcoded_config)
        assert config.validate_threshold_params(0, "DECREASING", 37.5) is True

    def test_valid_params_bi_excellent_hi(self, minimal_hardcoded_config):
        """Valid BI_EXCELLENT_HI parameters should return True"""
        config = ConfigManager(minimal_hardcoded_config)
        assert config.validate_threshold_params(0.0, "BI_EXCELLENT_HI", 0.1) is True

    def test_valid_params_bi_excellent_low(self, minimal_hardcoded_config):
        """Valid BI_EXCELLENT_LOW parameters should return True"""
        config = ConfigManager(minimal_hardcoded_config)
        assert config.validate_threshold_params(0, "BI_EXCELLENT_LOW", 10) is True

    def test_invalid_negative_steps(self, minimal_hardcoded_config):
        """Negative STEPS should raise ValueError"""
        config = ConfigManager(minimal_hardcoded_config)
        with pytest.raises(ValueError, match="STEPS must be positive"):
            config.validate_threshold_params(0, "INCREASING", -5)

    def test_invalid_zero_steps(self, minimal_hardcoded_config):
        """Zero STEPS should raise ValueError"""
        config = ConfigManager(minimal_hardcoded_config)
        with pytest.raises(ValueError, match="STEPS must be positive"):
            config.validate_threshold_params(0, "INCREASING", 0)

    def test_invalid_infinite_base_pos(self, minimal_hardcoded_config):
        """Infinite BASE_POSITION should raise ValueError"""
        config = ConfigManager(minimal_hardcoded_config)
        with pytest.raises(ValueError, match="must be finite"):
            config.validate_threshold_params(float('inf'), "INCREASING", 20)

    def test_invalid_infinite_steps(self, minimal_hardcoded_config):
        """Infinite STEPS should raise ValueError"""
        config = ConfigManager(minimal_hardcoded_config)
        with pytest.raises(ValueError, match="must be finite"):
            config.validate_threshold_params(0, "INCREASING", float('inf'))

    def test_invalid_direction(self, minimal_hardcoded_config):
        """Invalid DIRECTION should raise ValueError"""
        config = ConfigManager(minimal_hardcoded_config)
        with pytest.raises(ValueError, match="DIRECTION must be one of"):
            config.validate_threshold_params(0, "INVALID_DIR", 20)


# ============================================================================
# CALCULATION TESTS
# ============================================================================

class TestCalculateThresholds:
    """Test calculate_thresholds() for all direction types"""

    def test_increasing_direction(self, minimal_hardcoded_config):
        """INCREASING direction: VP=base+1s, P=base+2s, G=base+3s, E=base+4s"""
        config = ConfigManager(minimal_hardcoded_config)
        result = config.calculate_thresholds(0, "INCREASING", 20)

        assert result["VERY_POOR"] == 20
        assert result["POOR"] == 40
        assert result["GOOD"] == 60
        assert result["EXCELLENT"] == 80

    def test_decreasing_direction(self, minimal_hardcoded_config):
        """DECREASING direction: E=base+1s, G=base+2s, P=base+3s, VP=base+4s"""
        config = ConfigManager(minimal_hardcoded_config)
        result = config.calculate_thresholds(0, "DECREASING", 37.5)

        assert result["EXCELLENT"] == 37.5
        assert result["GOOD"] == 75.0
        assert result["POOR"] == 112.5
        assert result["VERY_POOR"] == 150.0

    def test_bi_excellent_hi_direction(self, minimal_hardcoded_config):
        """BI_EXCELLENT_HI direction: VP=base-2s, P=base-1s, G=base+1s, E=base+2s"""
        config = ConfigManager(minimal_hardcoded_config)
        result = config.calculate_thresholds(0, "BI_EXCELLENT_HI", 0.1)

        assert result["VERY_POOR"] == -0.2
        assert result["POOR"] == -0.1
        assert result["GOOD"] == 0.1
        assert result["EXCELLENT"] == 0.2

    def test_bi_excellent_low_direction(self, minimal_hardcoded_config):
        """BI_EXCELLENT_LOW direction: E=base-2s, G=base-1s, P=base+1s, VP=base+2s"""
        config = ConfigManager(minimal_hardcoded_config)
        result = config.calculate_thresholds(0, "BI_EXCELLENT_LOW", 5)

        assert result["EXCELLENT"] == -10
        assert result["GOOD"] == -5
        assert result["POOR"] == 5
        assert result["VERY_POOR"] == 10

    def test_non_zero_base_position(self, minimal_hardcoded_config):
        """Non-zero BASE_POSITION should offset all thresholds"""
        config = ConfigManager(minimal_hardcoded_config)
        result = config.calculate_thresholds(100, "INCREASING", 10)

        assert result["VERY_POOR"] == 110
        assert result["POOR"] == 120
        assert result["GOOD"] == 130
        assert result["EXCELLENT"] == 140

    def test_fractional_steps(self, minimal_hardcoded_config):
        """Fractional STEPS should work correctly"""
        config = ConfigManager(minimal_hardcoded_config)
        result = config.calculate_thresholds(0, "DECREASING", 6.25)

        assert result["EXCELLENT"] == 6.25
        assert result["GOOD"] == 12.5
        assert result["POOR"] == 18.75
        assert result["VERY_POOR"] == 25.0


# ============================================================================
# CACHING TESTS
# ============================================================================

class TestThresholdCaching:
    """Test threshold calculation caching behavior"""

    def test_cache_hit(self, minimal_hardcoded_config):
        """Second call with same params should return cached result"""
        config = ConfigManager(minimal_hardcoded_config)

        # First call - cache miss
        result1 = config.calculate_thresholds(0, "INCREASING", 20, "TEST_SCORING")

        # Second call - should hit cache
        result2 = config.calculate_thresholds(0, "INCREASING", 20, "TEST_SCORING")

        # Results should be identical
        assert result1 == result2
        assert result1 is result2  # Should be same object from cache

    def test_cache_different_scoring_types(self, minimal_hardcoded_config):
        """Different scoring_type with same params should be cached separately"""
        config = ConfigManager(minimal_hardcoded_config)

        result1 = config.calculate_thresholds(0, "INCREASING", 20, "ADP_SCORING")
        result2 = config.calculate_thresholds(0, "INCREASING", 20, "PLAYER_RATING_SCORING")

        # Results should be equal but different objects
        assert result1 == result2
        assert result1 is not result2

    def test_cache_different_steps(self, minimal_hardcoded_config):
        """Different STEPS should not hit cache"""
        config = ConfigManager(minimal_hardcoded_config)

        result1 = config.calculate_thresholds(0, "INCREASING", 20)
        result2 = config.calculate_thresholds(0, "INCREASING", 25)

        assert result1 != result2
        assert result1 is not result2


# ============================================================================
# BACKWARD COMPATIBILITY TESTS
# ============================================================================

class TestBackwardCompatibility:
    """Test backward compatibility with hardcoded thresholds"""

    def test_hardcoded_format_loads(self, minimal_hardcoded_config):
        """Old hardcoded format should load without errors"""
        config = ConfigManager(minimal_hardcoded_config)

        # Should load successfully
        assert config.config_name == "Test Hardcoded Config"

        # Hardcoded thresholds should be accessible
        assert config.adp_scoring["THRESHOLDS"]["EXCELLENT"] == 20
        assert config.adp_scoring["THRESHOLDS"]["GOOD"] == 50
        assert config.adp_scoring["THRESHOLDS"]["POOR"] == 100
        assert config.adp_scoring["THRESHOLDS"]["VERY_POOR"] == 150

    def test_parameterized_format_loads(self, parameterized_config):
        """New parameterized format should load and calculate thresholds"""
        config = ConfigManager(parameterized_config)

        # Should load successfully
        assert config.config_name == "Test Parameterized Config"

        # Thresholds should be calculated and accessible
        assert config.adp_scoring["THRESHOLDS"]["EXCELLENT"] == 37.5
        assert config.adp_scoring["THRESHOLDS"]["GOOD"] == 75.0
        assert config.adp_scoring["THRESHOLDS"]["POOR"] == 112.5
        assert config.adp_scoring["THRESHOLDS"]["VERY_POOR"] == 150.0

    def test_parameterized_player_rating(self, parameterized_config):
        """PLAYER_RATING with INCREASING should calculate correctly"""
        config = ConfigManager(parameterized_config)

        assert config.player_rating_scoring["THRESHOLDS"]["VERY_POOR"] == 20
        assert config.player_rating_scoring["THRESHOLDS"]["POOR"] == 40
        assert config.player_rating_scoring["THRESHOLDS"]["GOOD"] == 60
        assert config.player_rating_scoring["THRESHOLDS"]["EXCELLENT"] == 80

    def test_parameterized_performance(self, parameterized_config):
        """PERFORMANCE with BI_EXCELLENT_HI should calculate correctly"""
        config = ConfigManager(parameterized_config)

        assert config.performance_scoring["THRESHOLDS"]["VERY_POOR"] == -0.2
        assert config.performance_scoring["THRESHOLDS"]["POOR"] == -0.1
        assert config.performance_scoring["THRESHOLDS"]["GOOD"] == 0.1
        assert config.performance_scoring["THRESHOLDS"]["EXCELLENT"] == 0.2

    def test_parameterized_matchup(self, parameterized_config):
        """MATCHUP with BI_EXCELLENT_HI should calculate correctly"""
        config = ConfigManager(parameterized_config)

        assert config.matchup_scoring["THRESHOLDS"]["VERY_POOR"] == -15.0
        assert config.matchup_scoring["THRESHOLDS"]["POOR"] == -7.5
        assert config.matchup_scoring["THRESHOLDS"]["GOOD"] == 7.5
        assert config.matchup_scoring["THRESHOLDS"]["EXCELLENT"] == 15.0

    def test_get_multiplier_works_with_calculated_thresholds(self, parameterized_config):
        """_get_multiplier() should work with calculated thresholds"""
        config = ConfigManager(parameterized_config)

        # Test ADP multiplier with calculated thresholds
        mult, label = config.get_adp_multiplier(30.0)  # Should be EXCELLENT (< 37.5)
        assert label == "EXCELLENT"

        mult, label = config.get_adp_multiplier(60.0)  # Should be GOOD (< 75)
        assert label == "GOOD"


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestExtractParametersIntegration:
    """Test _extract_parameters() pre-calculation integration"""

    def test_all_scoring_types_calculated(self, parameterized_config):
        """All 5 scoring types should have calculated thresholds"""
        config = ConfigManager(parameterized_config)

        # ADP
        assert "EXCELLENT" in config.adp_scoring["THRESHOLDS"]
        assert config.adp_scoring["THRESHOLDS"]["EXCELLENT"] == 37.5

        # PLAYER_RATING
        assert "EXCELLENT" in config.player_rating_scoring["THRESHOLDS"]
        assert config.player_rating_scoring["THRESHOLDS"]["EXCELLENT"] == 80

        # TEAM_QUALITY
        assert "EXCELLENT" in config.team_quality_scoring["THRESHOLDS"]
        assert config.team_quality_scoring["THRESHOLDS"]["EXCELLENT"] == 6.25

        # PERFORMANCE
        assert "EXCELLENT" in config.performance_scoring["THRESHOLDS"]
        assert config.performance_scoring["THRESHOLDS"]["EXCELLENT"] == 0.2

        # MATCHUP
        assert "EXCELLENT" in config.matchup_scoring["THRESHOLDS"]
        assert config.matchup_scoring["THRESHOLDS"]["EXCELLENT"] == 15.0

    def test_original_params_preserved(self, parameterized_config):
        """Original BASE_POSITION, DIRECTION, STEPS should be preserved"""
        config = ConfigManager(parameterized_config)

        # Check ADP original params are still there
        assert config.adp_scoring["THRESHOLDS"]["BASE_POSITION"] == 0
        assert config.adp_scoring["THRESHOLDS"]["DIRECTION"] == "DECREASING"
        assert config.adp_scoring["THRESHOLDS"]["STEPS"] == 37.5

        # And calculated values added
        assert config.adp_scoring["THRESHOLDS"]["EXCELLENT"] == 37.5
        assert config.adp_scoring["THRESHOLDS"]["VERY_POOR"] == 150.0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
