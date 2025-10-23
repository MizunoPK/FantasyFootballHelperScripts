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
            "SAME_POS_BYE_WEIGHT": 1.0,
            "DIFF_POS_BYE_WEIGHT": 1.0,
            "INJURY_PENALTIES": {"LOW": 0, "MEDIUM": 10.0, "HIGH": 75.0},
            "DRAFT_ORDER_BONUSES": {"PRIMARY": 50, "SECONDARY": 30},
            "DRAFT_ORDER": [{"FLEX": "P", "QB": "S"}],
            "MAX_POSITIONS": {"QB": 2, "RB": 4, "WR": 4, "FLEX": 2, "TE": 1, "K": 1, "DST": 1},
            "FLEX_ELIGIBLE_POSITIONS": ["RB", "WR"],
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
            },
            "SCHEDULE_SCORING": {
                "THRESHOLDS": {
                    "VERY_POOR": 8,
                    "POOR": 12,
                    "GOOD": 20,
                    "EXCELLENT": 24
                },
                "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
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
            "SAME_POS_BYE_WEIGHT": 1.0,
            "DIFF_POS_BYE_WEIGHT": 1.0,
            "INJURY_PENALTIES": {"LOW": 0, "MEDIUM": 10.0, "HIGH": 75.0},
            "DRAFT_ORDER_BONUSES": {"PRIMARY": 50, "SECONDARY": 30},
            "DRAFT_ORDER": [{"FLEX": "P", "QB": "S"}],
            "MAX_POSITIONS": {"QB": 2, "RB": 4, "WR": 4, "FLEX": 2, "TE": 1, "K": 1, "DST": 1},
            "FLEX_ELIGIBLE_POSITIONS": ["RB", "WR"],
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
            },
            "SCHEDULE_SCORING": {
                "THRESHOLDS": {
                    "BASE_POSITION": 16,
                    "DIRECTION": "INCREASING",
                    "STEPS": 8
                },
                "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
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

    def test_get_schedule_multiplier_with_calculated_thresholds(self, parameterized_config):
        """get_schedule_multiplier() should work with calculated thresholds"""
        config = ConfigManager(parameterized_config)

        # SCHEDULE thresholds: BASE=16, DIRECTION=INCREASING, STEPS=8
        # VERY_POOR = 24, POOR = 32, GOOD = 40, EXCELLENT = 48
        # Higher rank = worse defense = easier schedule = better for player
        # For rising_thresholds: EXCELLENT if >=48, GOOD if >=40, POOR if <=32, VERY_POOR if <=24

        mult, label = config.get_schedule_multiplier(50.0)  # Should be EXCELLENT (>= 48)
        assert label == "EXCELLENT"
        assert mult == 1.05

        mult, label = config.get_schedule_multiplier(44.0)  # Should be GOOD (>= 40, < 48)
        assert label == "GOOD"
        assert mult == 1.025

        mult, label = config.get_schedule_multiplier(30.0)  # Should be POOR (<= 32, > 24)
        assert label == "POOR"
        assert mult == 0.975

        mult, label = config.get_schedule_multiplier(20.0)  # Should be VERY_POOR (<= 24)
        assert label == "VERY_POOR"
        assert mult == 0.95


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestExtractParametersIntegration:
    """Test _extract_parameters() pre-calculation integration"""

    def test_all_scoring_types_calculated(self, parameterized_config):
        """All 6 scoring types should have calculated thresholds"""
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

        # SCHEDULE
        assert "EXCELLENT" in config.schedule_scoring["THRESHOLDS"]
        assert config.schedule_scoring["THRESHOLDS"]["EXCELLENT"] == 48

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


# ============================================================================
# EDGE CASE TESTS
# ============================================================================

class TestConfigStructureEdgeCases:
    """Test edge cases for config structure validation"""

    def test_missing_config_name(self, temp_data_folder):
        """Missing config_name should raise ValueError"""
        config_content = {
            "description": "Test config",
            "parameters": {}
        }
        config_file = temp_data_folder / "league_config.json"
        with open(config_file, 'w') as f:
            json.dump(config_content, f)

        with pytest.raises(ValueError, match="Configuration missing required fields.*config_name"):
            ConfigManager(temp_data_folder)

    def test_missing_description(self, temp_data_folder):
        """Missing description should raise ValueError"""
        config_content = {
            "config_name": "Test",
            "parameters": {}
        }
        config_file = temp_data_folder / "league_config.json"
        with open(config_file, 'w') as f:
            json.dump(config_content, f)

        with pytest.raises(ValueError, match="Configuration missing required fields.*description"):
            ConfigManager(temp_data_folder)

    def test_missing_parameters(self, temp_data_folder):
        """Missing parameters should raise ValueError"""
        config_content = {
            "config_name": "Test",
            "description": "Test config"
        }
        config_file = temp_data_folder / "league_config.json"
        with open(config_file, 'w') as f:
            json.dump(config_content, f)

        with pytest.raises(ValueError, match="Configuration missing required fields.*parameters"):
            ConfigManager(temp_data_folder)

    def test_parameters_not_dict(self, temp_data_folder):
        """parameters field must be a dictionary"""
        config_content = {
            "config_name": "Test",
            "description": "Test config",
            "parameters": []  # List instead of dict
        }
        config_file = temp_data_folder / "league_config.json"
        with open(config_file, 'w') as f:
            json.dump(config_content, f)

        with pytest.raises(ValueError, match="'parameters' field must be a dictionary"):
            ConfigManager(temp_data_folder)

    def test_malformed_json(self, temp_data_folder):
        """Malformed JSON should raise JSONDecodeError"""
        config_file = temp_data_folder / "league_config.json"
        with open(config_file, 'w') as f:
            f.write("{invalid json content")

        with pytest.raises(json.JSONDecodeError):
            ConfigManager(temp_data_folder)

    def test_config_file_not_found(self, temp_data_folder):
        """Missing config file should raise FileNotFoundError"""
        # Don't create the config file
        with pytest.raises(FileNotFoundError, match="Configuration file not found"):
            ConfigManager(temp_data_folder)


class TestMissingRequiredParameters:
    """Test missing required parameters in config"""

    def test_missing_current_nfl_week(self, temp_data_folder):
        """Missing CURRENT_NFL_WEEK should raise ValueError"""
        config_content = {
            "config_name": "Test",
            "description": "Test config",
            "parameters": {
                "NFL_SEASON": 2025,
                "NFL_SCORING_FORMAT": "ppr"
            }
        }
        config_file = temp_data_folder / "league_config.json"
        with open(config_file, 'w') as f:
            json.dump(config_content, f)

        with pytest.raises(ValueError, match="Config missing required parameters.*CURRENT_NFL_WEEK"):
            ConfigManager(temp_data_folder)

    def test_missing_injury_penalty_level(self, minimal_hardcoded_config):
        """Missing injury penalty level should raise ValueError"""
        config_file = minimal_hardcoded_config / "league_config.json"
        with open(config_file, 'r') as f:
            data = json.load(f)

        # Remove HIGH level
        del data["parameters"]["INJURY_PENALTIES"]["HIGH"]

        with open(config_file, 'w') as f:
            json.dump(data, f)

        with pytest.raises(ValueError, match="INJURY_PENALTIES missing levels.*HIGH"):
            ConfigManager(minimal_hardcoded_config)

    def test_missing_draft_bonus_type(self, minimal_hardcoded_config):
        """Missing draft bonus type should raise ValueError"""
        config_file = minimal_hardcoded_config / "league_config.json"
        with open(config_file, 'r') as f:
            data = json.load(f)

        # Remove PRIMARY bonus
        del data["parameters"]["DRAFT_ORDER_BONUSES"]["PRIMARY"]

        with open(config_file, 'w') as f:
            json.dump(data, f)

        with pytest.raises(ValueError, match="DRAFT_ORDER_BONUSES missing types.*PRIMARY"):
            ConfigManager(minimal_hardcoded_config)

    def test_draft_order_not_list(self, minimal_hardcoded_config):
        """DRAFT_ORDER must be a list"""
        config_file = minimal_hardcoded_config / "league_config.json"
        with open(config_file, 'r') as f:
            data = json.load(f)

        # Make DRAFT_ORDER a dict instead of list
        data["parameters"]["DRAFT_ORDER"] = {"FLEX": "P"}

        with open(config_file, 'w') as f:
            json.dump(data, f)

        with pytest.raises(ValueError, match="DRAFT_ORDER must be a list"):
            ConfigManager(minimal_hardcoded_config)


class TestGetterMethodEdgeCases:
    """Test edge cases for getter methods"""

    def test_get_parameter_with_default(self, minimal_hardcoded_config):
        """get_parameter should return default for non-existent key"""
        config = ConfigManager(minimal_hardcoded_config)
        result = config.get_parameter("NON_EXISTENT_KEY", default="default_value")
        assert result == "default_value"

    def test_get_parameter_none_default(self, minimal_hardcoded_config):
        """get_parameter should return None if no default provided"""
        config = ConfigManager(minimal_hardcoded_config)
        result = config.get_parameter("NON_EXISTENT_KEY")
        assert result is None

    def test_has_parameter_exists(self, minimal_hardcoded_config):
        """has_parameter should return True for existing parameter"""
        config = ConfigManager(minimal_hardcoded_config)
        assert config.has_parameter("CURRENT_NFL_WEEK") is True

    def test_has_parameter_not_exists(self, minimal_hardcoded_config):
        """has_parameter should return False for non-existent parameter"""
        config = ConfigManager(minimal_hardcoded_config)
        assert config.has_parameter("NON_EXISTENT_KEY") is False

    def test_get_draft_position_round_too_low(self, minimal_hardcoded_config):
        """get_draft_position_for_round with round < 1 should raise IndexError"""
        config = ConfigManager(minimal_hardcoded_config)
        with pytest.raises(IndexError, match="Round number 0 out of range"):
            config.get_draft_position_for_round(0)

    def test_get_draft_position_round_too_high(self, minimal_hardcoded_config):
        """get_draft_position_for_round with round > max should raise IndexError"""
        config = ConfigManager(minimal_hardcoded_config)
        max_round = len(config.draft_order)
        with pytest.raises(IndexError, match=f"Round number {max_round + 1} out of range"):
            config.get_draft_position_for_round(max_round + 1)

    def test_get_draft_position_valid_round(self, minimal_hardcoded_config):
        """get_draft_position_for_round with valid round should return dict"""
        config = ConfigManager(minimal_hardcoded_config)
        result = config.get_draft_position_for_round(1)
        assert isinstance(result, dict)
        assert "FLEX" in result

    def test_get_injury_penalty_invalid_level(self, minimal_hardcoded_config):
        """get_injury_penalty with invalid level should fall back to HIGH"""
        config = ConfigManager(minimal_hardcoded_config)
        result = config.get_injury_penalty("INVALID_LEVEL")
        expected = config.injury_penalties["HIGH"]
        assert result == expected

    def test_get_bye_week_penalty_same_position_only(self, minimal_hardcoded_config):
        """get_bye_week_penalty with only same position conflicts (median-based)"""
        from utils.FantasyPlayer import FantasyPlayer

        config = ConfigManager(minimal_hardcoded_config)

        # Create mock players with weekly points
        player1 = FantasyPlayer(id=1, name="RB1", team="KC", position="RB")
        player1.week_1_points = 10.0
        player1.week_2_points = 15.0
        player1.week_3_points = 12.0
        # Median = 12.0

        player2 = FantasyPlayer(id=2, name="RB2", team="DAL", position="RB")
        player2.week_1_points = 20.0
        player2.week_2_points = 18.0
        player2.week_3_points = 22.0
        # Median = 20.0

        same_pos_players = [player1, player2]
        diff_pos_players = []

        result = config.get_bye_week_penalty(same_pos_players, diff_pos_players)
        # Expected = (12 + 20) ** 1.0 + 0 ** 1.0 = 32.0
        expected = 32.0
        assert abs(result - expected) < 0.01

    def test_get_bye_week_penalty_different_position(self, minimal_hardcoded_config):
        """get_bye_week_penalty with different position conflicts (median-based)"""
        from utils.FantasyPlayer import FantasyPlayer

        config = ConfigManager(minimal_hardcoded_config)

        # Create mock players
        same_pos_player = FantasyPlayer(id=1, name="RB1", team="KC", position="RB")
        same_pos_player.week_1_points = 10.0
        same_pos_player.week_2_points = 15.0
        same_pos_player.week_3_points = 12.0
        # Median = 12.0

        diff_pos_player1 = FantasyPlayer(id=2, name="WR1", team="DAL", position="WR")
        diff_pos_player1.week_1_points = 8.0
        diff_pos_player1.week_2_points = 10.0
        diff_pos_player1.week_3_points = 12.0
        # Median = 10.0

        diff_pos_player2 = FantasyPlayer(id=3, name="TE1", team="SF", position="TE")
        diff_pos_player2.week_1_points = 5.0
        diff_pos_player2.week_2_points = 7.0
        diff_pos_player2.week_3_points = 6.0
        # Median = 6.0

        same_pos_players = [same_pos_player]
        diff_pos_players = [diff_pos_player1, diff_pos_player2]

        result = config.get_bye_week_penalty(same_pos_players, diff_pos_players)
        # Expected = 12 ** 1.0 + (10 + 6) ** 1.0 = 12 + 16 = 28.0
        expected = 28.0
        assert abs(result - expected) < 0.01

    def test_get_ideal_draft_position_out_of_range(self, minimal_hardcoded_config):
        """get_ideal_draft_position with round >= len(draft_order) should return FLEX"""
        config = ConfigManager(minimal_hardcoded_config)
        result = config.get_ideal_draft_position(round_num=999)
        assert result == 'FLEX'


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
