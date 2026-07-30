"""
Unit Tests for ConfigManager OPPONENT_TEAMS Configuration

Tests the loading, defaulting, and validation of the OPPONENT_TEAMS parameter -
the league opponent roster that sources the Mark Player as Drafted TEAM SELECTION
menu and the Trade Simulator opponent filter.

Author: Kai Mizuno
Created: 2026-07-29
"""

import pytest
import json

import league_helper.constants as Constants
from league_helper.util.ConfigManager import ConfigManager


# FIXTURES

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
            "OPPONENT_TEAMS": ["Fishoutawater", "Chase-ing points", "Annihilators"],
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


class TestOpponentTeamsLoading:
    """Test loading OPPONENT_TEAMS from config."""

    def test_opponent_teams_loads_from_config(self, temp_data_folder, minimal_config):
        """Test that opponent_teams attribute is populated from config."""
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert hasattr(config, 'opponent_teams')
        assert config.opponent_teams == ["Fishoutawater", "Chase-ing points", "Annihilators"]

    def test_opponent_teams_preserves_order_and_exact_names(self, temp_data_folder, minimal_config):
        """Test that names are not sorted, trimmed, or case-folded on load."""
        minimal_config["parameters"]["OPPONENT_TEAMS"] = ["  Padded Name  ", "lowercase team", "Zeta", "Alpha"]
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert config.opponent_teams == ["  Padded Name  ", "lowercase team", "Zeta", "Alpha"]

    def test_opponent_teams_defaults_when_missing(self, temp_data_folder, minimal_config):
        """Test that a config lacking OPPONENT_TEAMS loads with an empty list and no raise."""
        del minimal_config["parameters"]["OPPONENT_TEAMS"]
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert config.opponent_teams == []


class TestOpponentTeamsValidation:
    """Test validation of the OPPONENT_TEAMS parameter."""

    def test_opponent_teams_not_list_raises_error(self, temp_data_folder, minimal_config):
        """Test that a non-list OPPONENT_TEAMS raises ValueError."""
        minimal_config["parameters"]["OPPONENT_TEAMS"] = "Fishoutawater,Pidgin"
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        with pytest.raises(ValueError, match="OPPONENT_TEAMS must be a list"):
            ConfigManager(temp_data_folder)

    def test_opponent_teams_non_string_element_raises_error(self, temp_data_folder, minimal_config):
        """Test that a non-string element in OPPONENT_TEAMS raises ValueError."""
        minimal_config["parameters"]["OPPONENT_TEAMS"] = ["Fishoutawater", 3]
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        with pytest.raises(ValueError, match="OPPONENT_TEAMS entries must be non-empty strings"):
            ConfigManager(temp_data_folder)

    def test_opponent_teams_empty_string_element_raises_error(self, temp_data_folder, minimal_config):
        """Test that an empty-string element in OPPONENT_TEAMS raises ValueError."""
        minimal_config["parameters"]["OPPONENT_TEAMS"] = ["Fishoutawater", ""]
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        with pytest.raises(ValueError, match="OPPONENT_TEAMS entries must be non-empty strings"):
            ConfigManager(temp_data_folder)

    def test_opponent_teams_whitespace_only_element_raises_error(self, temp_data_folder, minimal_config):
        """Test that a whitespace-only element in OPPONENT_TEAMS raises ValueError."""
        minimal_config["parameters"]["OPPONENT_TEAMS"] = ["Fishoutawater", "   "]
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        with pytest.raises(ValueError, match="OPPONENT_TEAMS entries must be non-empty strings"):
            ConfigManager(temp_data_folder)

    def test_opponent_teams_containing_own_team_raises_error(self, temp_data_folder, minimal_config):
        """Test that including FANTASY_TEAM_NAME in OPPONENT_TEAMS raises ValueError."""
        minimal_config["parameters"]["OPPONENT_TEAMS"] = ["Fishoutawater", Constants.FANTASY_TEAM_NAME]
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        with pytest.raises(ValueError, match="OPPONENT_TEAMS must contain opponents only"):
            ConfigManager(temp_data_folder)


class TestOpponentTeamsEdgeCases:
    """Test edge cases for OPPONENT_TEAMS."""

    def test_opponent_teams_empty_list_allowed(self, temp_data_folder, minimal_config):
        """Test that an explicitly empty OPPONENT_TEAMS list is valid (no opponents configured)."""
        minimal_config["parameters"]["OPPONENT_TEAMS"] = []
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert config.opponent_teams == []

    def test_opponent_teams_is_not_a_required_parameter(self, temp_data_folder, minimal_config):
        """Test that omitting OPPONENT_TEAMS does not trip required-parameter validation."""
        del minimal_config["parameters"]["OPPONENT_TEAMS"]
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert config.opponent_teams == []
        assert config.nfl_team_penalty == ["LV", "NYJ", "NYG", "KC"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
