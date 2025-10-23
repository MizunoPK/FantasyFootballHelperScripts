"""
Unit Tests for ConfigManager MAX_POSITIONS System

Tests the MAX_POSITIONS configuration parameter:
- Loading max_positions from config file
- Validation of required positions
- Validation of positive integer values
- max_players property calculation

Author: Claude Code
Date: 2025-10-22
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
def valid_config(temp_data_folder):
    """Create valid config with MAX_POSITIONS"""
    config_content = {
        "config_name": "Test Config",
        "description": "Test configuration with MAX_POSITIONS",
        "parameters": {
            "CURRENT_NFL_WEEK": 6,
            "NFL_SEASON": 2025,
            "NFL_SCORING_FORMAT": "ppr",
            "NORMALIZATION_MAX_SCALE": 100.0,
            "BASE_BYE_PENALTY": 25.0,
            "DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY": 2.0,
            "INJURY_PENALTIES": {"LOW": 0, "MEDIUM": 10.0, "HIGH": 75.0},
            "DRAFT_ORDER_BONUSES": {"PRIMARY": 50, "SECONDARY": 30},
            "DRAFT_ORDER": [{"FLEX": "P", "QB": "S"}],
            "MAX_POSITIONS": {
                "QB": 2,
                "RB": 4,
                "WR": 4,
                "FLEX": 2,
                "TE": 1,
                "K": 1,
                "DST": 1
            },
            "ADP_SCORING": {
                "THRESHOLDS": {
                    "BASE_POSITION": 0,
                    "DIRECTION": "DECREASING",
                    "STEPS": 35.0
                },
                "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                "WEIGHT": 1.0
            },
            "PLAYER_RATING_SCORING": {
                "THRESHOLDS": {
                    "BASE_POSITION": 0,
                    "DIRECTION": "INCREASING",
                    "STEPS": 22.0
                },
                "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                "WEIGHT": 1.0
            },
            "TEAM_QUALITY_SCORING": {
                "THRESHOLDS": {
                    "BASE_POSITION": 0,
                    "DIRECTION": "DECREASING",
                    "STEPS": 5.0
                },
                "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                "WEIGHT": 1.0
            },
            "PERFORMANCE_SCORING": {
                "MIN_WEEKS": 3,
                "THRESHOLDS": {
                    "BASE_POSITION": 0.0,
                    "DIRECTION": "BI_EXCELLENT_HI",
                    "STEPS": 0.15
                },
                "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                "WEIGHT": 1.0
            },
            "MATCHUP_SCORING": {
                "THRESHOLDS": {
                    "BASE_POSITION": 0,
                    "DIRECTION": "BI_EXCELLENT_HI",
                    "STEPS": 6.0
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
# TESTS
# ============================================================================

class TestMaxPositionsLoading:
    """Test MAX_POSITIONS loading from config file"""

    def test_max_positions_loads_from_config(self, valid_config):
        """Test that max_positions attribute is populated from config file"""
        config = ConfigManager(valid_config)

        assert hasattr(config, 'max_positions')
        assert isinstance(config.max_positions, dict)
        assert len(config.max_positions) == 7

    def test_max_positions_contains_all_required_positions(self, valid_config):
        """Test that all required positions (QB, RB, WR, TE, K, DST, FLEX) are present"""
        config = ConfigManager(valid_config)

        required_positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DST', 'FLEX']
        for position in required_positions:
            assert position in config.max_positions

    def test_max_positions_values_are_positive_integers(self, valid_config):
        """Test that all MAX_POSITIONS values are positive integers"""
        config = ConfigManager(valid_config)

        for position, limit in config.max_positions.items():
            assert isinstance(limit, int), f"{position} limit should be int, got {type(limit)}"
            assert limit > 0, f"{position} limit should be positive, got {limit}"


class TestMaxPositionsValidation:
    """Test MAX_POSITIONS validation logic"""

    def test_max_positions_missing_position_raises_error(self, temp_data_folder):
        """Test that missing required position raises ValueError"""
        config_content = {
            "config_name": "Test Config Missing QB",
            "description": "Test config missing QB position",
            "parameters": {
                "CURRENT_NFL_WEEK": 6,
                "NFL_SEASON": 2025,
                "NFL_SCORING_FORMAT": "ppr",
                "NORMALIZATION_MAX_SCALE": 100.0,
                "BASE_BYE_PENALTY": 25.0,
                "DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY": 2.0,
                "INJURY_PENALTIES": {"LOW": 0, "MEDIUM": 10.0, "HIGH": 75.0},
                "DRAFT_ORDER_BONUSES": {"PRIMARY": 50, "SECONDARY": 30},
                "DRAFT_ORDER": [{"FLEX": "P"}],
                "MAX_POSITIONS": {
                    "RB": 4,
                    "WR": 4,
                    "FLEX": 2,
                    "TE": 1,
                    "K": 1,
                    "DST": 1
                },
                "ADP_SCORING": {
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 35.0},
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "WEIGHT": 1.0
                },
                "PLAYER_RATING_SCORING": {
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 22.0},
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "WEIGHT": 1.0
                },
                "TEAM_QUALITY_SCORING": {
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 5.0},
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "WEIGHT": 1.0
                },
                "PERFORMANCE_SCORING": {
                    "MIN_WEEKS": 3,
                    "THRESHOLDS": {"BASE_POSITION": 0.0, "DIRECTION": "BI_EXCELLENT_HI", "STEPS": 0.15},
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "WEIGHT": 1.0
                },
                "MATCHUP_SCORING": {
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "BI_EXCELLENT_HI", "STEPS": 6.0},
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "WEIGHT": 1.0
                }
            }
        }

        config_file = temp_data_folder / "league_config.json"
        with open(config_file, 'w') as f:
            json.dump(config_content, f, indent=2)

        with pytest.raises(ValueError, match="MAX_POSITIONS missing required positions"):
            ConfigManager(temp_data_folder)

    def test_max_positions_negative_value_raises_error(self, temp_data_folder):
        """Test that negative position limit raises ValueError"""
        config_content = {
            "config_name": "Test Config Negative Value",
            "description": "Test config with negative MAX_POSITIONS value",
            "parameters": {
                "CURRENT_NFL_WEEK": 6,
                "NFL_SEASON": 2025,
                "NFL_SCORING_FORMAT": "ppr",
                "NORMALIZATION_MAX_SCALE": 100.0,
                "BASE_BYE_PENALTY": 25.0,
                "DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY": 2.0,
                "INJURY_PENALTIES": {"LOW": 0, "MEDIUM": 10.0, "HIGH": 75.0},
                "DRAFT_ORDER_BONUSES": {"PRIMARY": 50, "SECONDARY": 30},
                "DRAFT_ORDER": [{"FLEX": "P"}],
                "MAX_POSITIONS": {
                    "QB": 2,
                    "RB": 4,
                    "WR": 4,
                    "FLEX": 2,
                    "TE": -1,
                    "K": 1,
                    "DST": 1
                },
                "ADP_SCORING": {
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 35.0},
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "WEIGHT": 1.0
                },
                "PLAYER_RATING_SCORING": {
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 22.0},
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "WEIGHT": 1.0
                },
                "TEAM_QUALITY_SCORING": {
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 5.0},
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "WEIGHT": 1.0
                },
                "PERFORMANCE_SCORING": {
                    "MIN_WEEKS": 3,
                    "THRESHOLDS": {"BASE_POSITION": 0.0, "DIRECTION": "BI_EXCELLENT_HI", "STEPS": 0.15},
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "WEIGHT": 1.0
                },
                "MATCHUP_SCORING": {
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "BI_EXCELLENT_HI", "STEPS": 6.0},
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "WEIGHT": 1.0
                }
            }
        }

        config_file = temp_data_folder / "league_config.json"
        with open(config_file, 'w') as f:
            json.dump(config_content, f, indent=2)

        with pytest.raises(ValueError, match="MAX_POSITIONS\\[TE\\] must be a positive integer"):
            ConfigManager(temp_data_folder)

    def test_max_positions_zero_value_raises_error(self, temp_data_folder):
        """Test that zero position limit raises ValueError"""
        config_content = {
            "config_name": "Test Config Zero Value",
            "description": "Test config with zero MAX_POSITIONS value",
            "parameters": {
                "CURRENT_NFL_WEEK": 6,
                "NFL_SEASON": 2025,
                "NFL_SCORING_FORMAT": "ppr",
                "NORMALIZATION_MAX_SCALE": 100.0,
                "BASE_BYE_PENALTY": 25.0,
                "DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY": 2.0,
                "INJURY_PENALTIES": {"LOW": 0, "MEDIUM": 10.0, "HIGH": 75.0},
                "DRAFT_ORDER_BONUSES": {"PRIMARY": 50, "SECONDARY": 30},
                "DRAFT_ORDER": [{"FLEX": "P"}],
                "MAX_POSITIONS": {
                    "QB": 2,
                    "RB": 4,
                    "WR": 4,
                    "FLEX": 2,
                    "TE": 1,
                    "K": 0,
                    "DST": 1
                },
                "ADP_SCORING": {
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 35.0},
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "WEIGHT": 1.0
                },
                "PLAYER_RATING_SCORING": {
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 22.0},
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "WEIGHT": 1.0
                },
                "TEAM_QUALITY_SCORING": {
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 5.0},
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "WEIGHT": 1.0
                },
                "PERFORMANCE_SCORING": {
                    "MIN_WEEKS": 3,
                    "THRESHOLDS": {"BASE_POSITION": 0.0, "DIRECTION": "BI_EXCELLENT_HI", "STEPS": 0.15},
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "WEIGHT": 1.0
                },
                "MATCHUP_SCORING": {
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "BI_EXCELLENT_HI", "STEPS": 6.0},
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "WEIGHT": 1.0
                }
            }
        }

        config_file = temp_data_folder / "league_config.json"
        with open(config_file, 'w') as f:
            json.dump(config_content, f, indent=2)

        with pytest.raises(ValueError, match="MAX_POSITIONS\\[K\\] must be a positive integer"):
            ConfigManager(temp_data_folder)


class TestMaxPlayersProperty:
    """Test max_players property calculation"""

    def test_max_players_property_calculates_sum(self, valid_config):
        """Test that max_players property returns sum of max_positions values"""
        config = ConfigManager(valid_config)

        expected_sum = sum(config.max_positions.values())
        assert config.max_players == expected_sum

    def test_max_players_property_equals_15(self, valid_config):
        """Test that max_players equals 15 with default position limits"""
        config = ConfigManager(valid_config)

        # Default values: QB=2, RB=4, WR=4, FLEX=2, TE=1, K=1, DST=1 = 15 total
        assert config.max_players == 15
