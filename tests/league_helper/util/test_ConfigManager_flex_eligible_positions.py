"""
Unit Tests for ConfigManager FLEX_ELIGIBLE_POSITIONS Configuration

Tests the loading, validation, and usage of FLEX_ELIGIBLE_POSITIONS parameter.

Author: Kai Mizuno
"""

import pytest
import json
from pathlib import Path
from unittest.mock import Mock

import sys
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from league_helper.util.ConfigManager import ConfigManager


@pytest.fixture
def temp_data_folder(tmp_path):
    """Create temporary data folder for testing."""
    data_folder = tmp_path / "data"
    data_folder.mkdir()
    return data_folder


@pytest.fixture
def minimal_config():
    """Minimal valid configuration for testing."""
    return {
        "config_name": "test",
        "description": "test config",
        "parameters": {
            "CURRENT_NFL_WEEK": 1,
            "NFL_SEASON": 2025,
            "NFL_SCORING_FORMAT": "ppr",
            "NORMALIZATION_MAX_SCALE": 100.0,
            "DRAFT_NORMALIZATION_MAX_SCALE": 163,
            "SAME_POS_BYE_WEIGHT": 1.0,
            "DIFF_POS_BYE_WEIGHT": 1.0,
            "DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY": 5.0,
            "INJURY_PENALTIES": {"LOW": 0, "MEDIUM": 10, "HIGH": 75},
            "DRAFT_ORDER_BONUSES": {"PRIMARY": 50, "SECONDARY": 30},
            "DRAFT_ORDER": [{"FLEX": "P"}],
            "MAX_POSITIONS": {"QB": 2, "RB": 4, "WR": 4, "FLEX": 2, "TE": 1, "K": 1, "DST": 1},
            "FLEX_ELIGIBLE_POSITIONS": ["RB", "WR"],
            "ADP_SCORING": {
                "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 35},
                "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                "WEIGHT": 1.0
            },
            "PLAYER_RATING_SCORING": {
                "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 22},
                "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                "WEIGHT": 1.0
            },
            "TEAM_QUALITY_SCORING": {
                "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 5},
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
                "IMPACT_SCALE": 150.0,
                "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "BI_EXCELLENT_HI", "STEPS": 6},
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


class TestFlexEligiblePositionsLoading:
    """Test loading FLEX_ELIGIBLE_POSITIONS from config."""

    def test_flex_eligible_positions_loads_from_config(self, temp_data_folder, minimal_config):
        """Test that flex_eligible_positions attribute is populated from config."""
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert hasattr(config, 'flex_eligible_positions')
        assert config.flex_eligible_positions == ["RB", "WR"]

    def test_flex_eligible_positions_is_list(self, temp_data_folder, minimal_config):
        """Test that flex_eligible_positions is a list type."""
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert isinstance(config.flex_eligible_positions, list)


class TestFlexEligiblePositionsValidation:
    """Test validation of FLEX_ELIGIBLE_POSITIONS parameter."""

    def test_flex_eligible_positions_missing_raises_error(self, temp_data_folder, minimal_config):
        """Test that missing FLEX_ELIGIBLE_POSITIONS raises ValueError."""
        del minimal_config["parameters"]["FLEX_ELIGIBLE_POSITIONS"]
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        with pytest.raises(ValueError, match="FLEX_ELIGIBLE_POSITIONS"):
            ConfigManager(temp_data_folder)

    def test_flex_eligible_positions_empty_list_raises_error(self, temp_data_folder, minimal_config):
        """Test that empty FLEX_ELIGIBLE_POSITIONS list raises ValueError."""
        minimal_config["parameters"]["FLEX_ELIGIBLE_POSITIONS"] = []
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        with pytest.raises(ValueError, match="must contain at least one position"):
            ConfigManager(temp_data_folder)

    def test_flex_eligible_positions_not_list_raises_error(self, temp_data_folder, minimal_config):
        """Test that non-list FLEX_ELIGIBLE_POSITIONS raises ValueError."""
        minimal_config["parameters"]["FLEX_ELIGIBLE_POSITIONS"] = "RB,WR"  # string instead of list
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        with pytest.raises(ValueError, match="must be a list"):
            ConfigManager(temp_data_folder)

    def test_flex_eligible_positions_contains_flex_raises_error(self, temp_data_folder, minimal_config):
        """Test that FLEX in FLEX_ELIGIBLE_POSITIONS raises ValueError (circular reference)."""
        minimal_config["parameters"]["FLEX_ELIGIBLE_POSITIONS"] = ["RB", "WR", "FLEX"]
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        with pytest.raises(ValueError, match="cannot contain 'FLEX'"):
            ConfigManager(temp_data_folder)

    def test_flex_eligible_positions_invalid_position_raises_error(self, temp_data_folder, minimal_config):
        """Test that invalid position in FLEX_ELIGIBLE_POSITIONS raises ValueError."""
        minimal_config["parameters"]["FLEX_ELIGIBLE_POSITIONS"] = ["RB", "INVALID"]
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        with pytest.raises(ValueError, match="invalid positions"):
            ConfigManager(temp_data_folder)

    def test_flex_eligible_positions_all_valid_positions_allowed(self, temp_data_folder, minimal_config):
        """Test that all valid positions are accepted."""
        minimal_config["parameters"]["FLEX_ELIGIBLE_POSITIONS"] = ["QB", "RB", "WR", "TE", "K", "DST"]
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert len(config.flex_eligible_positions) == 6


class TestGetPositionWithFlexMethod:
    """Test the get_position_with_flex() method."""

    def test_rb_returns_flex(self, temp_data_folder, minimal_config):
        """Test that RB position returns FLEX when RB is flex-eligible."""
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert config.get_position_with_flex('RB') == 'FLEX'

    def test_wr_returns_flex(self, temp_data_folder, minimal_config):
        """Test that WR position returns FLEX when WR is flex-eligible."""
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert config.get_position_with_flex('WR') == 'FLEX'

    def test_qb_returns_qb(self, temp_data_folder, minimal_config):
        """Test that QB position returns QB when QB is not flex-eligible."""
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert config.get_position_with_flex('QB') == 'QB'

    def test_te_returns_te(self, temp_data_folder, minimal_config):
        """Test that TE position returns TE when TE is not flex-eligible."""
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert config.get_position_with_flex('TE') == 'TE'

    def test_te_returns_flex_when_configured(self, temp_data_folder, minimal_config):
        """Test that TE returns FLEX when TE is added to flex_eligible_positions."""
        minimal_config["parameters"]["FLEX_ELIGIBLE_POSITIONS"] = ["RB", "WR", "TE"]
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert config.get_position_with_flex('TE') == 'FLEX'


class TestFlexEligiblePositionsEdgeCases:
    """Test edge cases for FLEX_ELIGIBLE_POSITIONS."""

    def test_single_position_allowed(self, temp_data_folder, minimal_config):
        """Test that a single position in list is valid."""
        minimal_config["parameters"]["FLEX_ELIGIBLE_POSITIONS"] = ["RB"]
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert config.flex_eligible_positions == ["RB"]

    def test_all_positions_except_flex_allowed(self, temp_data_folder, minimal_config):
        """Test that all positions except FLEX can be flex-eligible."""
        minimal_config["parameters"]["FLEX_ELIGIBLE_POSITIONS"] = ["QB", "RB", "WR", "TE", "K", "DST"]
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert len(config.flex_eligible_positions) == 6
        assert "FLEX" not in config.flex_eligible_positions


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
