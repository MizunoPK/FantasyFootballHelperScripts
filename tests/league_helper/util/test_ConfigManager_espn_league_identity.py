"""
Unit Tests for ConfigManager ESPN League Identity Configuration (D17.1, TD4)

Tests the loading, defaulting, and type-guard validation of the optional
ESPN_LEAGUE_ID / ESPN_TEAM_ID parameters. Asserted against a tmp-path
fixture config the test itself writes -- never against the live
data/configs/league_config.json values -- so the operator's real-season
config swap does not break this test (per review_2026-08-17T0933.md
CONCERN "Testing" on league_helper/util/ConfigManager.py:128-131,304-308,
1080-1090).

Author: Kai Mizuno
"""

import pytest
import json

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
            "ESPN_LEAGUE_ID": "138260302",
            "ESPN_TEAM_ID": 1,
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
                "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 6},
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


class TestEspnLeagueIdentityLoading:
    """Test loading ESPN_LEAGUE_ID and ESPN_TEAM_ID from config."""

    def test_espn_league_id_loads_from_config(self, temp_data_folder, minimal_config):
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert config.espn_league_id == "138260302"

    def test_espn_team_id_loads_from_config(self, temp_data_folder, minimal_config):
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert config.espn_team_id == 1

    def test_espn_league_identity_defaults_when_missing(self, temp_data_folder, minimal_config):
        """Absent keys default to '' / 0 -- every existing config keeps loading."""
        del minimal_config["parameters"]["ESPN_LEAGUE_ID"]
        del minimal_config["parameters"]["ESPN_TEAM_ID"]
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        config = ConfigManager(temp_data_folder)

        assert config.espn_league_id == ""
        assert config.espn_team_id == 0


class TestEspnLeagueIdentityValidation:
    """Test type-guard validation of ESPN_LEAGUE_ID and ESPN_TEAM_ID."""

    def test_espn_league_id_wrong_type_raises_error(self, temp_data_folder, minimal_config):
        minimal_config["parameters"]["ESPN_LEAGUE_ID"] = 138260302
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        with pytest.raises(ValueError, match="ESPN_LEAGUE_ID must be a string"):
            ConfigManager(temp_data_folder)

    def test_espn_team_id_wrong_type_raises_error(self, temp_data_folder, minimal_config):
        minimal_config["parameters"]["ESPN_TEAM_ID"] = "1"
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        with pytest.raises(ValueError, match="ESPN_TEAM_ID must be an integer"):
            ConfigManager(temp_data_folder)

    def test_espn_team_id_bool_raises_error(self, temp_data_folder, minimal_config):
        """isinstance(x, bool) is a subtype of int -- must be explicitly excluded."""
        minimal_config["parameters"]["ESPN_TEAM_ID"] = True
        config_file = temp_data_folder / "league_config.json"
        config_file.write_text(json.dumps(minimal_config))

        with pytest.raises(ValueError, match="ESPN_TEAM_ID must be an integer"):
            ConfigManager(temp_data_folder)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
