"""
Tests for ConfigManager week-specific config loading.

Tests the new config folder structure where:
- Base config: data/configs/league_config.json
- Week-specific: data/configs/week{N}-{M}.json (e.g., week1-5.json, week6-9.json, week10-13.json, week14-17.json)

Author: Kai Mizuno
"""

import json
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch

import sys
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from league_helper.util.ConfigManager import ConfigManager


# ============================================================================
# Test Fixtures
# ============================================================================

def get_base_config_content(week: int = 6) -> dict:
    """Create minimal base config content."""
    return {
        "config_name": "Test Base Config",
        "description": "Test config for week-specific loading",
        "parameters": {
            "CURRENT_NFL_WEEK": week,
            "NFL_SEASON": 2025,
            "NFL_SCORING_FORMAT": "ppr",
            "NORMALIZATION_MAX_SCALE": 140.0,
            "SAME_POS_BYE_WEIGHT": 0.2,
            "DIFF_POS_BYE_WEIGHT": 0.05,
            "INJURY_PENALTIES": {"LOW": 0, "MEDIUM": 5, "HIGH": 100},
            "DRAFT_ORDER_BONUSES": {"PRIMARY": 60, "SECONDARY": 90},
            "DRAFT_ORDER_FILE": 1,
            "DRAFT_ORDER": [{"FLEX": "P"}] * 15,
            "MAX_POSITIONS": {"QB": 1, "RB": 4, "WR": 4, "FLEX": 2, "TE": 2, "K": 1, "DST": 1},
            "FLEX_ELIGIBLE_POSITIONS": ["RB", "WR"],
            "ADP_SCORING": {
                "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 20},
                "MULTIPLIERS": {"VERY_POOR": 0.95, "POOR": 0.975, "GOOD": 1.025, "EXCELLENT": 1.05},
                "WEIGHT": 3.0
            }
        }
    }


def get_week_config_content(weight_value: float = 2.0) -> dict:
    """Create week-specific config content."""
    return {
        "config_name": "Week-Specific Config",
        "description": "Week-specific scoring parameters",
        "parameters": {
            "PLAYER_RATING_SCORING": {
                "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 20},
                "MULTIPLIERS": {"VERY_POOR": 0.95, "POOR": 0.975, "GOOD": 1.025, "EXCELLENT": 1.05},
                "WEIGHT": weight_value
            },
            "TEAM_QUALITY_SCORING": {
                "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 8},
                "MULTIPLIERS": {"VERY_POOR": 0.95, "POOR": 0.975, "GOOD": 1.025, "EXCELLENT": 1.05},
                "WEIGHT": 0.5,
                "MIN_WEEKS": 4
            },
            "PERFORMANCE_SCORING": {
                "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "BI_EXCELLENT_HI", "STEPS": 0.1},
                "MULTIPLIERS": {"VERY_POOR": 0.95, "POOR": 0.975, "GOOD": 1.025, "EXCELLENT": 1.05},
                "WEIGHT": 3.0,
                "MIN_WEEKS": 5
            },
            "MATCHUP_SCORING": {
                "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 8},
                "MULTIPLIERS": {"VERY_POOR": 0.95, "POOR": 0.975, "GOOD": 1.025, "EXCELLENT": 1.05},
                "WEIGHT": 1.0,
                "MIN_WEEKS": 4,
                "IMPACT_SCALE": 100.0
            },
            "SCHEDULE_SCORING": {
                "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 8},
                "MULTIPLIERS": {"VERY_POOR": 0.95, "POOR": 0.975, "GOOD": 1.025, "EXCELLENT": 1.05},
                "WEIGHT": 0.0,
                "MIN_WEEKS": 5,
                "IMPACT_SCALE": 100.0
            },
            "TEMPERATURE_SCORING": {
                "IDEAL_TEMPERATURE": 60,
                "IMPACT_SCALE": 50.0,
                "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 10},
                "MULTIPLIERS": {"VERY_POOR": 0.95, "POOR": 0.975, "GOOD": 1.025, "EXCELLENT": 1.05},
                "WEIGHT": 0.7
            },
            "WIND_SCORING": {
                "IMPACT_SCALE": 60.0,
                "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 8},
                "MULTIPLIERS": {"VERY_POOR": 0.95, "POOR": 0.975, "GOOD": 1.025, "EXCELLENT": 1.05},
                "WEIGHT": 0.6
            },
            "LOCATION_MODIFIERS": {"HOME": 2.0, "AWAY": -3.0, "INTERNATIONAL": -2.0}
        }
    }


def create_configs_folder(temp_path: Path, week: int = 6, week_weight: float = 2.0) -> Path:
    """Create complete configs folder structure for testing."""
    configs_folder = temp_path / 'configs'
    configs_folder.mkdir()

    # Create base config
    base_config = get_base_config_content(week)
    (configs_folder / 'league_config.json').write_text(json.dumps(base_config, indent=2))

    # Create all week-specific configs
    for filename in ['week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']:
        week_config = get_week_config_content(week_weight)
        (configs_folder / filename).write_text(json.dumps(week_config, indent=2))

    return temp_path


@pytest.fixture
def temp_data_folder():
    """Create temporary data folder."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def configs_folder_week6(temp_data_folder):
    """Create configs folder with CURRENT_NFL_WEEK=6."""
    return create_configs_folder(temp_data_folder, week=6)


@pytest.fixture
def configs_folder_week1(temp_data_folder):
    """Create configs folder with CURRENT_NFL_WEEK=1."""
    return create_configs_folder(temp_data_folder, week=1)


@pytest.fixture
def configs_folder_week12(temp_data_folder):
    """Create configs folder with CURRENT_NFL_WEEK=12."""
    return create_configs_folder(temp_data_folder, week=12)


# ============================================================================
# Test: Week Config Filename Detection
# ============================================================================

class TestGetWeekConfigFilename:
    """Test _get_week_config_filename method."""

    def test_weeks_1_to_5_return_week1_5(self, configs_folder_week1):
        """Weeks 1-5 should return week1-5.json."""
        config = ConfigManager(configs_folder_week1)
        for week in range(1, 6):
            assert config._get_week_config_filename(week) == "week1-5.json"

    def test_weeks_6_to_9_return_week6_9(self, configs_folder_week6):
        """Weeks 6-9 should return week6-9.json."""
        config = ConfigManager(configs_folder_week6)
        for week in range(6, 10):
            assert config._get_week_config_filename(week) == "week6-9.json"

    def test_weeks_10_to_13_return_week10_13(self, configs_folder_week6):
        """Weeks 10-13 should return week10-13.json."""
        config = ConfigManager(configs_folder_week6)
        for week in range(10, 14):
            assert config._get_week_config_filename(week) == "week10-13.json"

    def test_weeks_14_to_17_return_week14_17(self, configs_folder_week12):
        """Weeks 14-17 should return week14-17.json."""
        config = ConfigManager(configs_folder_week12)
        for week in range(14, 18):
            assert config._get_week_config_filename(week) == "week14-17.json"

    def test_week_0_raises_error(self, configs_folder_week6):
        """Week 0 should raise ValueError."""
        config = ConfigManager(configs_folder_week6)
        with pytest.raises(ValueError, match="Invalid week number: 0"):
            config._get_week_config_filename(0)

    def test_week_18_raises_error(self, configs_folder_week6):
        """Week 18 should raise ValueError."""
        config = ConfigManager(configs_folder_week6)
        with pytest.raises(ValueError, match="Invalid week number: 18"):
            config._get_week_config_filename(18)

    def test_negative_week_raises_error(self, configs_folder_week6):
        """Negative week should raise ValueError."""
        config = ConfigManager(configs_folder_week6)
        with pytest.raises(ValueError, match="Invalid week number: -1"):
            config._get_week_config_filename(-1)


# ============================================================================
# Test: Configs Folder Detection
# ============================================================================

class TestConfigsFolderDetection:
    """Test detection of configs folder structure."""

    def test_detects_new_structure(self, configs_folder_week6):
        """ConfigManager should detect configs folder and set configs_folder attribute."""
        config = ConfigManager(configs_folder_week6)
        assert config.configs_folder is not None
        assert config.configs_folder.name == "configs"

    def test_detects_legacy_structure(self, temp_data_folder):
        """ConfigManager should use legacy mode when no configs folder exists."""
        # Create legacy config directly in data folder
        base = get_base_config_content(6)
        week = get_week_config_content()
        # Merge for legacy format
        base['parameters'].update(week['parameters'])
        (temp_data_folder / 'league_config.json').write_text(json.dumps(base, indent=2))

        config = ConfigManager(temp_data_folder)
        assert config.configs_folder is None

    def test_config_path_points_to_correct_file(self, configs_folder_week6):
        """Config path should point to configs/league_config.json for new structure."""
        config = ConfigManager(configs_folder_week6)
        assert config.config_path.parent.name == "configs"
        assert config.config_path.name == "league_config.json"


# ============================================================================
# Test: Week Config Merging
# ============================================================================

class TestWeekConfigMerging:
    """Test merging of week-specific config parameters."""

    def test_week_params_merged_into_parameters(self, configs_folder_week6):
        """Week-specific parameters should be merged into self.parameters."""
        config = ConfigManager(configs_folder_week6)
        # PLAYER_RATING_SCORING comes from week config
        assert "PLAYER_RATING_SCORING" in config.parameters
        assert config.player_rating_scoring is not None

    def test_base_params_preserved(self, configs_folder_week6):
        """Base parameters should still be accessible after merge."""
        config = ConfigManager(configs_folder_week6)
        # These come from base config
        assert config.current_nfl_week == 6
        assert config.nfl_season == 2025
        assert config.normalization_max_scale == 140.0

    def test_correct_week_file_loaded_for_week1(self, configs_folder_week1):
        """Week 1 should load week1-5.json."""
        config = ConfigManager(configs_folder_week1)
        assert config.current_nfl_week == 1
        # Verify week-specific params loaded
        assert config.player_rating_scoring is not None

    def test_correct_week_file_loaded_for_week6(self, configs_folder_week6):
        """Week 6 should load week6-9.json."""
        config = ConfigManager(configs_folder_week6)
        assert config.current_nfl_week == 6
        assert config.player_rating_scoring is not None

    def test_correct_week_file_loaded_for_week12(self, configs_folder_week12):
        """Week 12 should load week10-13.json."""
        config = ConfigManager(configs_folder_week12)
        assert config.current_nfl_week == 12
        assert config.player_rating_scoring is not None

    def test_different_week_configs_have_different_values(self, temp_data_folder):
        """Different week ranges should load different values if configured."""
        configs_folder = temp_data_folder / 'configs'
        configs_folder.mkdir()

        # Create base config for week 6
        base = get_base_config_content(6)
        (configs_folder / 'league_config.json').write_text(json.dumps(base, indent=2))

        # Create week configs with different WEIGHT values
        week1_5 = get_week_config_content(weight_value=1.5)
        week6_9 = get_week_config_content(weight_value=2.5)
        week10_13 = get_week_config_content(weight_value=3.0)
        week14_17 = get_week_config_content(weight_value=3.5)

        (configs_folder / 'week1-5.json').write_text(json.dumps(week1_5, indent=2))
        (configs_folder / 'week6-9.json').write_text(json.dumps(week6_9, indent=2))
        (configs_folder / 'week10-13.json').write_text(json.dumps(week10_13, indent=2))
        (configs_folder / 'week14-17.json').write_text(json.dumps(week14_17, indent=2))

        # Load with week 6 (should get weight 2.5)
        config = ConfigManager(temp_data_folder)
        assert config.player_rating_scoring['WEIGHT'] == 2.5


# ============================================================================
# Test: Error Handling
# ============================================================================

class TestWeekConfigErrorHandling:
    """Test error handling for week config loading."""

    def test_missing_week_config_logs_warning(self, temp_data_folder, caplog):
        """Missing week config should log warning but still work."""
        configs_folder = temp_data_folder / 'configs'
        configs_folder.mkdir()

        # Create base config with week 6
        base = get_base_config_content(6)
        # Add week-specific params directly to base (fallback)
        week = get_week_config_content()
        base['parameters'].update(week['parameters'])
        (configs_folder / 'league_config.json').write_text(json.dumps(base, indent=2))

        # Only create week1-5.json, not week6-9.json
        (configs_folder / 'week1-5.json').write_text(json.dumps(get_week_config_content(), indent=2))

        # Should still work (params in base config)
        config = ConfigManager(temp_data_folder)
        assert config.current_nfl_week == 6

    def test_malformed_week_config_raises_error(self, temp_data_folder):
        """Malformed week config JSON should raise error."""
        configs_folder = temp_data_folder / 'configs'
        configs_folder.mkdir()

        base = get_base_config_content(6)
        (configs_folder / 'league_config.json').write_text(json.dumps(base, indent=2))
        (configs_folder / 'week6-9.json').write_text("{invalid json")
        (configs_folder / 'week1-5.json').write_text(json.dumps(get_week_config_content(), indent=2))
        (configs_folder / 'week10-13.json').write_text(json.dumps(get_week_config_content(), indent=2))
        (configs_folder / 'week14-17.json').write_text(json.dumps(get_week_config_content(), indent=2))

        with pytest.raises(json.JSONDecodeError):
            ConfigManager(temp_data_folder)

    def test_missing_current_nfl_week_in_base_raises_error(self, temp_data_folder):
        """Missing CURRENT_NFL_WEEK in base config should raise error."""
        configs_folder = temp_data_folder / 'configs'
        configs_folder.mkdir()

        base = get_base_config_content(6)
        del base['parameters']['CURRENT_NFL_WEEK']
        (configs_folder / 'league_config.json').write_text(json.dumps(base, indent=2))
        (configs_folder / 'week6-9.json').write_text(json.dumps(get_week_config_content(), indent=2))

        with pytest.raises(ValueError, match="Base config missing required parameter: CURRENT_NFL_WEEK"):
            ConfigManager(temp_data_folder)


# ============================================================================
# Test: Legacy Compatibility
# ============================================================================

class TestLegacyCompatibility:
    """Test backward compatibility with legacy config structure."""

    def test_legacy_structure_still_works(self, temp_data_folder):
        """Legacy config structure should continue to work."""
        # Create merged config directly in data folder
        base = get_base_config_content(6)
        week = get_week_config_content()
        base['parameters'].update(week['parameters'])
        (temp_data_folder / 'league_config.json').write_text(json.dumps(base, indent=2))

        config = ConfigManager(temp_data_folder)
        assert config.current_nfl_week == 6
        assert config.player_rating_scoring is not None
        assert config.configs_folder is None

    def test_legacy_no_week_config_methods_called(self, temp_data_folder):
        """In legacy mode, _load_week_config should return empty dict."""
        base = get_base_config_content(6)
        week = get_week_config_content()
        base['parameters'].update(week['parameters'])
        (temp_data_folder / 'league_config.json').write_text(json.dumps(base, indent=2))

        config = ConfigManager(temp_data_folder)
        # Should return empty dict in legacy mode
        result = config._load_week_config(6)
        assert result == {}


# ============================================================================
# Test: Week Boundary Cases
# ============================================================================

class TestWeekBoundaryCases:
    """Test boundary cases at week transitions."""

    def test_week_5_uses_week1_5_config(self, temp_data_folder):
        """Week 5 (boundary) should use week1-5.json."""
        create_configs_folder(temp_data_folder, week=5)
        config = ConfigManager(temp_data_folder)
        assert config.current_nfl_week == 5
        assert config._get_week_config_filename(5) == "week1-5.json"

    def test_week_6_uses_week6_9_config(self, temp_data_folder):
        """Week 6 (boundary) should use week6-9.json."""
        create_configs_folder(temp_data_folder, week=6)
        config = ConfigManager(temp_data_folder)
        assert config.current_nfl_week == 6
        assert config._get_week_config_filename(6) == "week6-9.json"

    def test_week_9_uses_week6_9_config(self, temp_data_folder):
        """Week 9 (boundary) should use week6-9.json."""
        create_configs_folder(temp_data_folder, week=9)
        config = ConfigManager(temp_data_folder)
        assert config.current_nfl_week == 9
        assert config._get_week_config_filename(9) == "week6-9.json"

    def test_week_10_uses_week10_13_config(self, temp_data_folder):
        """Week 10 (boundary) should use week10-13.json."""
        create_configs_folder(temp_data_folder, week=10)
        config = ConfigManager(temp_data_folder)
        assert config.current_nfl_week == 10
        assert config._get_week_config_filename(10) == "week10-13.json"

    def test_week_13_uses_week10_13_config(self, temp_data_folder):
        """Week 13 (boundary) should use week10-13.json."""
        create_configs_folder(temp_data_folder, week=13)
        config = ConfigManager(temp_data_folder)
        assert config.current_nfl_week == 13
        assert config._get_week_config_filename(13) == "week10-13.json"

    def test_week_14_uses_week14_17_config(self, temp_data_folder):
        """Week 14 (boundary) should use week14-17.json."""
        create_configs_folder(temp_data_folder, week=14)
        config = ConfigManager(temp_data_folder)
        assert config.current_nfl_week == 14
        assert config._get_week_config_filename(14) == "week14-17.json"

    def test_week_17_uses_week14_17_config(self, temp_data_folder):
        """Week 17 (max) should use week14-17.json."""
        create_configs_folder(temp_data_folder, week=17)
        config = ConfigManager(temp_data_folder)
        assert config.current_nfl_week == 17
        assert config._get_week_config_filename(17) == "week14-17.json"
