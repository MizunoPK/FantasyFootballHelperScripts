"""
Unit Tests for ConfigManager NFL_TEAM_PENALTY Configuration

Tests the loading, validation, and usage of NFL_TEAM_PENALTY and NFL_TEAM_PENALTY_WEIGHT parameters.

Author: Kai Mizuno
Created: 2026-01-13
"""

import pytest
import json
from pathlib import Path

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
            "NFL_TEAM_PENALTY": ["LV", "NYJ", "NYG", "KC"],
            "NFL_TEAM_PENALTY_WEIGHT": 0.75,
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


class TestNFLTeamPenaltyLoading:
    """Test loading NFL_TEAM_PENALTY and NFL_TEAM_PENALTY_WEIGHT from config."""

    def test_nfl_team_penalty_loads_from_config(self, temp_data_folder, minimal_config):
        """Test that nfl_team_penalty attribute is populated from config."""
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert hasattr(config, 'nfl_team_penalty')
        assert config.nfl_team_penalty == ["LV", "NYJ", "NYG", "KC"]

    def test_nfl_team_penalty_weight_loads_from_config(self, temp_data_folder, minimal_config):
        """Test that nfl_team_penalty_weight attribute is populated from config."""
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert hasattr(config, 'nfl_team_penalty_weight')
        assert config.nfl_team_penalty_weight == 0.75

    def test_nfl_team_penalty_defaults_when_missing(self, temp_data_folder, minimal_config):
        """Test that nfl_team_penalty defaults to empty list when missing (backward compatible)."""
        del minimal_config["parameters"]["NFL_TEAM_PENALTY"]
        del minimal_config["parameters"]["NFL_TEAM_PENALTY_WEIGHT"]
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert config.nfl_team_penalty == []
        assert config.nfl_team_penalty_weight == 1.0


class TestNFLTeamPenaltyValidation:
    """Test validation of NFL_TEAM_PENALTY parameter."""

    def test_nfl_team_penalty_not_list_raises_error(self, temp_data_folder, minimal_config):
        """Test that non-list NFL_TEAM_PENALTY raises ValueError."""
        minimal_config["parameters"]["NFL_TEAM_PENALTY"] = "LV,NYJ"  # string instead of list
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        with pytest.raises(ValueError, match="NFL_TEAM_PENALTY must be a list"):
            ConfigManager(temp_data_folder)

    def test_nfl_team_penalty_invalid_team_raises_error(self, temp_data_folder, minimal_config):
        """Test that invalid team abbreviation in NFL_TEAM_PENALTY raises ValueError."""
        minimal_config["parameters"]["NFL_TEAM_PENALTY"] = ["LV", "INVALID", "NYJ"]
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        with pytest.raises(ValueError, match="invalid team abbreviations"):
            ConfigManager(temp_data_folder)

    def test_nfl_team_penalty_empty_list_allowed(self, temp_data_folder, minimal_config):
        """Test that empty NFL_TEAM_PENALTY list is valid (no penalties)."""
        minimal_config["parameters"]["NFL_TEAM_PENALTY"] = []
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert config.nfl_team_penalty == []


class TestNFLTeamPenaltyWeightValidation:
    """Test validation of NFL_TEAM_PENALTY_WEIGHT parameter."""

    def test_nfl_team_penalty_weight_not_numeric_raises_error(self, temp_data_folder, minimal_config):
        """Test that non-numeric NFL_TEAM_PENALTY_WEIGHT raises ValueError."""
        minimal_config["parameters"]["NFL_TEAM_PENALTY_WEIGHT"] = "0.75"  # string instead of number
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        with pytest.raises(ValueError, match="must be a number"):
            ConfigManager(temp_data_folder)

    def test_nfl_team_penalty_weight_below_range_raises_error(self, temp_data_folder, minimal_config):
        """Test that NFL_TEAM_PENALTY_WEIGHT below 0.0 raises ValueError."""
        minimal_config["parameters"]["NFL_TEAM_PENALTY_WEIGHT"] = -0.1
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        with pytest.raises(ValueError, match="must be between 0.0 and 1.0"):
            ConfigManager(temp_data_folder)

    def test_nfl_team_penalty_weight_above_range_raises_error(self, temp_data_folder, minimal_config):
        """Test that NFL_TEAM_PENALTY_WEIGHT above 1.0 raises ValueError."""
        minimal_config["parameters"]["NFL_TEAM_PENALTY_WEIGHT"] = 1.5
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        with pytest.raises(ValueError, match="must be between 0.0 and 1.0"):
            ConfigManager(temp_data_folder)


class TestNFLTeamPenaltyEdgeCases:
    """Test edge cases for NFL_TEAM_PENALTY and NFL_TEAM_PENALTY_WEIGHT."""

    def test_nfl_team_penalty_weight_zero_allowed(self, temp_data_folder, minimal_config):
        """Test that NFL_TEAM_PENALTY_WEIGHT = 0.0 is valid (maximum penalty)."""
        minimal_config["parameters"]["NFL_TEAM_PENALTY_WEIGHT"] = 0.0
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert config.nfl_team_penalty_weight == 0.0

    def test_nfl_team_penalty_weight_one_allowed(self, temp_data_folder, minimal_config):
        """Test that NFL_TEAM_PENALTY_WEIGHT = 1.0 is valid (no penalty)."""
        minimal_config["parameters"]["NFL_TEAM_PENALTY_WEIGHT"] = 1.0
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert config.nfl_team_penalty_weight == 1.0

    def test_nfl_team_penalty_weight_accepts_int(self, temp_data_folder, minimal_config):
        """Test that NFL_TEAM_PENALTY_WEIGHT accepts int values (0 or 1)."""
        minimal_config["parameters"]["NFL_TEAM_PENALTY_WEIGHT"] = 1  # int instead of float
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert config.nfl_team_penalty_weight == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
