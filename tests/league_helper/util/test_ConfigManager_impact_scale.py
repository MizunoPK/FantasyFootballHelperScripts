"""
Unit Tests for ConfigManager IMPACT_SCALE Validation

Tests the required IMPACT_SCALE parameter validation for additive scoring system:
- ValueError when MATCHUP_SCORING missing IMPACT_SCALE
- ValueError when SCHEDULE_SCORING missing IMPACT_SCALE
- Successful loading when both present

Author: Claude Code
Date: 2025-10-28
"""

import pytest
from pathlib import Path
import json
import tempfile

# Imports work via conftest.py which adds the necessary paths
from util.ConfigManager import ConfigManager


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def temp_data_folder():
    """Create temporary data folder for testing"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def base_config_dict():
    """Base config structure that's valid except for IMPACT_SCALE"""
    return {
        "config_name": "Test Config",
        "description": "Test configuration for IMPACT_SCALE validation",
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
                "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 10},
                "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                "WEIGHT": 1.0
            },
            "PLAYER_RATING_SCORING": {
                "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 10},
                "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                "WEIGHT": 1.0
            },
            "TEAM_QUALITY_SCORING": {
                "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 5},
                "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                "WEIGHT": 0.0
            },
            "PERFORMANCE_SCORING": {
                "MIN_WEEKS": 3,
                "THRESHOLDS": {"BASE_POSITION": 0.0, "DIRECTION": "BI_EXCELLENT_HI", "STEPS": 0.1},
                "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.925, "VERY_POOR": 0.96},
                "WEIGHT": 1.0
            },
            "MATCHUP_SCORING": {
                "IMPACT_SCALE": 150.0,
                "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "BI_EXCELLENT_HI", "STEPS": 7.5},
                "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                "WEIGHT": 1.0
            },
            "SCHEDULE_SCORING": {
                "IMPACT_SCALE": 80.0,
                "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 8},
                "MULTIPLIERS": {"EXCELLENT": 1.0, "GOOD": 1.0, "POOR": 1.0, "VERY_POOR": 1.0},
                "WEIGHT": 0.0
            }
        }
    }


def create_config_file(temp_data_folder, config_dict):
    """Helper to create league_config.json in temp folder"""
    config_file = temp_data_folder / "league_config.json"
    with open(config_file, 'w') as f:
        json.dump(config_dict, f)
    return config_file


# ============================================================================
# TESTS
# ============================================================================

class TestIMPACT_SCALEValidation:
    """Test IMPACT_SCALE parameter validation"""

    def test_valid_config_with_both_impact_scales(self, temp_data_folder, base_config_dict):
        """Test config loads successfully when both IMPACT_SCALE params present"""
        # Arrange
        create_config_file(temp_data_folder, base_config_dict)

        # Act
        config = ConfigManager(temp_data_folder)

        # Assert
        assert config.matchup_scoring['IMPACT_SCALE'] == 150.0
        assert config.schedule_scoring['IMPACT_SCALE'] == 80.0

    def test_missing_matchup_impact_scale_raises_error(self, temp_data_folder, base_config_dict):
        """Test ValueError raised when MATCHUP_SCORING missing IMPACT_SCALE"""
        # Arrange
        del base_config_dict['parameters']['MATCHUP_SCORING']['IMPACT_SCALE']
        create_config_file(temp_data_folder, base_config_dict)

        # Act & Assert
        with pytest.raises(ValueError, match="MATCHUP_SCORING missing required parameter: IMPACT_SCALE"):
            ConfigManager(temp_data_folder)

    def test_missing_schedule_impact_scale_raises_error(self, temp_data_folder, base_config_dict):
        """Test ValueError raised when SCHEDULE_SCORING missing IMPACT_SCALE"""
        # Arrange
        del base_config_dict['parameters']['SCHEDULE_SCORING']['IMPACT_SCALE']
        create_config_file(temp_data_folder, base_config_dict)

        # Act & Assert
        with pytest.raises(ValueError, match="SCHEDULE_SCORING missing required parameter: IMPACT_SCALE"):
            ConfigManager(temp_data_folder)

    def test_missing_both_impact_scales_raises_error(self, temp_data_folder, base_config_dict):
        """Test ValueError raised when both IMPACT_SCALE params missing"""
        # Arrange
        del base_config_dict['parameters']['MATCHUP_SCORING']['IMPACT_SCALE']
        del base_config_dict['parameters']['SCHEDULE_SCORING']['IMPACT_SCALE']
        create_config_file(temp_data_folder, base_config_dict)

        # Act & Assert - Should fail on first missing parameter (MATCHUP)
        with pytest.raises(ValueError, match="MATCHUP_SCORING missing required parameter: IMPACT_SCALE"):
            ConfigManager(temp_data_folder)

    def test_impact_scale_values_accessible(self, temp_data_folder, base_config_dict):
        """Test IMPACT_SCALE values are accessible through config object"""
        # Arrange
        base_config_dict['parameters']['MATCHUP_SCORING']['IMPACT_SCALE'] = 200.0
        base_config_dict['parameters']['SCHEDULE_SCORING']['IMPACT_SCALE'] = 100.0
        create_config_file(temp_data_folder, base_config_dict)

        # Act
        config = ConfigManager(temp_data_folder)

        # Assert
        assert config.matchup_scoring['IMPACT_SCALE'] == 200.0
        assert config.schedule_scoring['IMPACT_SCALE'] == 100.0
