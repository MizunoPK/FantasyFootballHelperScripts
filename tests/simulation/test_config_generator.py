"""
Comprehensive Unit Tests for ConfigGenerator

Tests all functionality of the ConfigGenerator class including:
- Initialization and configuration loading (5-file horizon folder structure)
- DRAFT_ORDER_FILE parameter definition
- The horizon-based interface: generate_horizon_test_values, get_config_for_horizon,
  update_baseline_for_horizon
- Edge cases and error handling

Author: Kai Mizuno
Date: 2025
"""

import pytest
import json
import tempfile
import shutil
import copy
from pathlib import Path

from simulation.shared.ConfigGenerator import ConfigGenerator

TEST_PARAMETER_ORDER = [
    'NORMALIZATION_MAX_SCALE',
    'SAME_POS_BYE_WEIGHT',
    'DIFF_POS_BYE_WEIGHT',
    'PRIMARY_BONUS',
    'SECONDARY_BONUS',
    'ADP_SCORING_WEIGHT',
    'PLAYER_RATING_SCORING_WEIGHT',
    'TEAM_QUALITY_SCORING_WEIGHT',
    'TEAM_QUALITY_MIN_WEEKS',
    'PERFORMANCE_SCORING_WEIGHT',
    'PERFORMANCE_SCORING_STEPS',
    'PERFORMANCE_MIN_WEEKS',
    'MATCHUP_IMPACT_SCALE',
    'MATCHUP_SCORING_WEIGHT',
    'MATCHUP_MIN_WEEKS',
    'TEMPERATURE_IMPACT_SCALE',
    'TEMPERATURE_SCORING_WEIGHT',
    'WIND_IMPACT_SCALE',
    'WIND_SCORING_WEIGHT',
    'LOCATION_HOME',
    'LOCATION_AWAY',
    'LOCATION_INTERNATIONAL',
]


def create_test_config_folder(base_config: dict, tmp_path: Path) -> Path:
    """
    Create a test config folder with all required files.

    Creates the folder structure required by ConfigGenerator:
    - league_config.json (base parameters)
    - week1-5.json (week-specific params)
    - week6-9.json (week-specific params)
    - week10-13.json (week-specific params)
    - week14-17.json (week-specific params)

    Args:
        base_config: The base configuration dictionary
        tmp_path: Temporary directory path

    Returns:
        Path to the created config folder
    """
    config_folder = tmp_path / "test_configs"
    config_folder.mkdir(parents=True, exist_ok=True)

    params = base_config.get('parameters', {})

    base_params = {
        'NORMALIZATION_MAX_SCALE': params.get('NORMALIZATION_MAX_SCALE', 100.0),
        'SAME_POS_BYE_WEIGHT': params.get('SAME_POS_BYE_WEIGHT', 1.0),
        'DIFF_POS_BYE_WEIGHT': params.get('DIFF_POS_BYE_WEIGHT', 1.0),
        'DRAFT_ORDER_BONUSES': params.get('DRAFT_ORDER_BONUSES', {'PRIMARY': 50.0, 'SECONDARY': 40.0}),
        'DRAFT_ORDER_FILE': params.get('DRAFT_ORDER_FILE', 1),
        'DRAFT_ORDER': params.get('DRAFT_ORDER', [{"FLEX": "P", "QB": "S"}] * 15),
        'MAX_POSITIONS': params.get('MAX_POSITIONS', {"QB": 2, "RB": 4, "WR": 4, "FLEX": 2, "TE": 1, "K": 1, "DST": 1}),
        'FLEX_ELIGIBLE_POSITIONS': params.get('FLEX_ELIGIBLE_POSITIONS', ["RB", "WR"]),
        'ADP_SCORING': params.get('ADP_SCORING', {
            'WEIGHT': 1.0,
            'MULTIPLIERS': {'EXCELLENT': 1.2, 'GOOD': 1.1, 'POOR': 0.9, 'VERY_POOR': 0.8},
            'THRESHOLDS': {'BASE_POSITION': 0, 'DIRECTION': 'DECREASING', 'STEPS': 37.5}
        }),
    }

    week_params = {
        'PLAYER_RATING_SCORING': params.get('PLAYER_RATING_SCORING', {
            'WEIGHT': 1.0,
            'MULTIPLIERS': {'EXCELLENT': 1.25, 'GOOD': 1.15, 'POOR': 0.85, 'VERY_POOR': 0.75},
            'THRESHOLDS': {'BASE_POSITION': 0, 'DIRECTION': 'INCREASING', 'STEPS': 20.0}
        }),
        'TEAM_QUALITY_SCORING': params.get('TEAM_QUALITY_SCORING', {
            'MIN_WEEKS': 5,
            'WEIGHT': 1.0,
            'MULTIPLIERS': {'EXCELLENT': 1.3, 'GOOD': 1.2, 'POOR': 0.8, 'VERY_POOR': 0.7},
            'THRESHOLDS': {'BASE_POSITION': 0, 'DIRECTION': 'DECREASING', 'STEPS': 6.25}
        }),
        'PERFORMANCE_SCORING': params.get('PERFORMANCE_SCORING', {
            'WEIGHT': 1.0,
            'MULTIPLIERS': {'EXCELLENT': 1.15, 'GOOD': 1.05, 'POOR': 0.95, 'VERY_POOR': 0.85},
            'THRESHOLDS': {'BASE_POSITION': 0, 'DIRECTION': 'BI_EXCELLENT_HI', 'STEPS': 0.1}
        }),
        'MATCHUP_SCORING': params.get('MATCHUP_SCORING', {
            'MIN_WEEKS': 5,
            'IMPACT_SCALE': 150.0,
            'WEIGHT': 1.0,
            'MULTIPLIERS': {'EXCELLENT': 1.2, 'GOOD': 1.1, 'POOR': 0.9, 'VERY_POOR': 0.8},
            'THRESHOLDS': {'BASE_POSITION': 0, 'DIRECTION': 'INCREASING', 'STEPS': 7.5}
        }),
        'SCHEDULE_SCORING': params.get('SCHEDULE_SCORING', {
            'IMPACT_SCALE': 80.0,
            'WEIGHT': 1.0,
            'MULTIPLIERS': {'EXCELLENT': 1.05, 'GOOD': 1.025, 'POOR': 0.975, 'VERY_POOR': 0.95},
            'THRESHOLDS': {'BASE_POSITION': 0, 'DIRECTION': 'INCREASING', 'STEPS': 6}
        }),
        'TEMPERATURE_SCORING': params.get('TEMPERATURE_SCORING', {
            'IDEAL_TEMPERATURE': 60,
            'IMPACT_SCALE': 50.0,
            'WEIGHT': 1.0,
            'THRESHOLDS': {'BASE_POSITION': 0, 'DIRECTION': 'DECREASING', 'STEPS': 10},
            'MULTIPLIERS': {'EXCELLENT': 1.05, 'GOOD': 1.025, 'POOR': 0.975, 'VERY_POOR': 0.95}
        }),
        'WIND_SCORING': params.get('WIND_SCORING', {
            'IMPACT_SCALE': 60.0,
            'WEIGHT': 1.0,
            'THRESHOLDS': {'BASE_POSITION': 0, 'DIRECTION': 'DECREASING', 'STEPS': 8},
            'MULTIPLIERS': {'EXCELLENT': 1.05, 'GOOD': 1.025, 'POOR': 0.975, 'VERY_POOR': 0.95}
        }),
        'LOCATION_MODIFIERS': params.get('LOCATION_MODIFIERS', {
            'HOME': 2.0,
            'AWAY': -2.0,
            'INTERNATIONAL': -5.0
        }),
    }

    league_config = {
        'config_name': base_config.get('config_name', 'test_baseline'),
        'description': 'Test base config',
        'parameters': base_params
    }
    with open(config_folder / 'league_config.json', 'w') as f:
        json.dump(league_config, f, indent=2)

    for week_file in ['week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']:
        week_config = {
            'config_name': f'Test {week_file}',
            'description': f'Test week config for {week_file}',
            'parameters': week_params
        }
        with open(config_folder / week_file, 'w') as f:
            json.dump(week_config, f, indent=2)

    return config_folder


class TestConfigGeneratorInitialization:
    """Test ConfigGenerator initialization and configuration loading"""

    @pytest.fixture
    def temp_baseline_config(self, tmp_path):
        """Create a temporary baseline config folder for testing"""
        config = {
            "config_name": "test_baseline",
            "parameters": {
                "NORMALIZATION_MAX_SCALE": 100.0,
                "DRAFT_NORMALIZATION_MAX_SCALE": 163,
                "SAME_POS_BYE_WEIGHT": 1.0,
                "DIFF_POS_BYE_WEIGHT": 1.0,
                "DRAFT_ORDER_BONUSES": {
                    "PRIMARY": 50.0,
                    "SECONDARY": 40.0
                },
                "MAX_POSITIONS": {"QB": 2, "RB": 4, "WR": 4, "FLEX": 2, "TE": 1, "K": 1, "DST": 1},
                "FLEX_ELIGIBLE_POSITIONS": ["RB", "WR"],
                "ADP_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.2,
                        "GOOD": 1.1,
                        "POOR": 0.9,
                        "VERY_POOR": 0.8
                    },
                    "THRESHOLDS": {
                        "BASE_POSITION": 0,
                        "DIRECTION": "DECREASING",
                        "STEPS": 37.5
                    }
                },
                "PLAYER_RATING_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.25,
                        "GOOD": 1.15,
                        "POOR": 0.85,
                        "VERY_POOR": 0.75
                    },
                    "THRESHOLDS": {
                        "BASE_POSITION": 0,
                        "DIRECTION": "INCREASING",
                        "STEPS": 20.0
                    }
                },
                "TEAM_QUALITY_SCORING": {
                    "MIN_WEEKS": 5,
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.3,
                        "GOOD": 1.2,
                        "POOR": 0.8,
                        "VERY_POOR": 0.7
                    },
                    "THRESHOLDS": {
                        "BASE_POSITION": 0,
                        "DIRECTION": "DECREASING",
                        "STEPS": 6.25
                    }
                },
                "PERFORMANCE_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.15,
                        "GOOD": 1.05,
                        "POOR": 0.95,
                        "VERY_POOR": 0.85
                    },
                    "THRESHOLDS": {
                        "BASE_POSITION": 0,
                        "DIRECTION": "BI_EXCELLENT_HI",
                        "STEPS": 0.1
                    }
                },
                "MATCHUP_SCORING": {
                    "MIN_WEEKS": 5,
                    "IMPACT_SCALE": 150.0,
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.2,
                        "GOOD": 1.1,
                        "POOR": 0.9,
                        "VERY_POOR": 0.8
                    },
                    "THRESHOLDS": {
                        "BASE_POSITION": 0,
                        "DIRECTION": "BI_EXCELLENT_HI",
                        "STEPS": 7.5
                    }
                },
                "SCHEDULE_SCORING": {
                    "IMPACT_SCALE": 80.0,
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.05,
                        "GOOD": 1.025,
                        "POOR": 0.975,
                        "VERY_POOR": 0.95
                    },
                    "THRESHOLDS": {
                        "BASE_POSITION": 16,
                        "DIRECTION": "INCREASING",
                        "STEPS": 8.0
                    }
                }
            }
        }

        return create_test_config_folder(config, tmp_path)

    def test_initialization_default_num_test_values(self, temp_baseline_config):
        """Test initialization with default num_test_values"""
        gen = ConfigGenerator(temp_baseline_config)

        assert gen.num_test_values == 5
        assert gen.baseline_configs['1-5'] is not None
        assert 'parameters' in gen.baseline_configs['1-5']

    def test_initialization_custom_num_test_values(self, temp_baseline_config):
        """Test initialization with custom num_test_values"""
        gen = ConfigGenerator(temp_baseline_config, num_test_values=3)

        assert gen.num_test_values == 3
        assert gen.baseline_configs['1-5'] is not None

    def test_baseline_configs_populated_from_folder(self, temp_baseline_config):
        """Test successful loading of baseline configuration"""
        gen = ConfigGenerator(temp_baseline_config)

        config = gen.baseline_configs['1-5']
        assert config['config_name'] == 'Test week1-5.json'
        assert config['parameters']['NORMALIZATION_MAX_SCALE'] == 100.0
        assert config['parameters']['SAME_POS_BYE_WEIGHT'] == 1.0
        assert config['parameters']['DIFF_POS_BYE_WEIGHT'] == 1.0

    def test_param_definitions_exist(self, temp_baseline_config):
        """Test that param_definitions dict exists and is non-empty"""
        gen = ConfigGenerator(temp_baseline_config)

        assert hasattr(gen, 'param_definitions')
        assert isinstance(gen.param_definitions, dict)
        assert len(gen.param_definitions) > 0

        for param_name, definition in gen.param_definitions.items():
            assert isinstance(definition, tuple), f"{param_name} should be a tuple"
            assert len(definition) == 3, f"{param_name} should have (min, max, precision)"
            min_val, max_val, precision = definition
            assert isinstance(precision, int), f"{param_name} precision should be int"
            assert precision >= 0, f"{param_name} precision should be >= 0"


class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_missing_config_folder(self):
        """Test that missing config folder raises ValueError"""
        with pytest.raises(ValueError, match="does not exist"):
            ConfigGenerator(Path('/nonexistent/config_folder'))

    def test_config_file_instead_of_folder(self, tmp_path):
        """Test that passing a file instead of folder raises ValueError"""
        config_file = tmp_path / "config.json"
        config_file.write_text('{"config_name": "test"}')

        with pytest.raises(ValueError, match="requires a folder path"):
            ConfigGenerator(config_file)

    def test_missing_required_files_in_folder(self, tmp_path):
        """Test that folder missing required files raises ValueError"""
        config_folder = tmp_path / "incomplete_config"
        config_folder.mkdir()

        league_config = {"config_name": "test", "parameters": {}}
        with open(config_folder / "league_config.json", 'w') as f:
            json.dump(league_config, f)

        with pytest.raises(ValueError, match="Missing required config files"):
            ConfigGenerator(config_folder)

    def test_invalid_json_in_folder(self, tmp_path):
        """Test that invalid JSON in folder raises JSONDecodeError"""
        config_folder = tmp_path / "bad_config"
        config_folder.mkdir()

        (config_folder / "league_config.json").write_text("{invalid json")
        for week_file in ['week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']:
            with open(config_folder / week_file, 'w') as f:
                json.dump({"config_name": week_file, "parameters": {}}, f)

        with pytest.raises(json.JSONDecodeError):
            ConfigGenerator(config_folder)



class TestDraftOrderFile:
    """Test DRAFT_ORDER_FILE parameter functionality"""

    def test_draft_order_file_in_param_definitions(self):
        """Test DRAFT_ORDER_FILE is in PARAM_DEFINITIONS with correct range and precision"""
        assert 'DRAFT_ORDER_FILE' in ConfigGenerator.PARAM_DEFINITIONS
        min_val, max_val, precision = ConfigGenerator.PARAM_DEFINITIONS['DRAFT_ORDER_FILE']
        assert min_val == 1
        assert max_val == 100
        assert precision == 0

    def test_draft_order_file_not_in_parameter_order(self):
        """Test DRAFT_ORDER_FILE is NOT in PARAMETER_ORDER (handled by separate script)"""
        assert 'DRAFT_ORDER_FILE' not in TEST_PARAMETER_ORDER
        assert 'DRAFT_ORDER_FILE' in ConfigGenerator.PARAM_DEFINITIONS


class TestHorizonBasedInterface:
    """Test new horizon-based ConfigGenerator interface for 6-file structure"""

    def create_6_file_config_folder(self, tmp_path):
        """Helper to create 6-file config structure for testing"""
        config_folder = tmp_path / "test_configs"
        config_folder.mkdir()

        base_config = {
            "config_name": "Test Config",
            "parameters": {
                "CURRENT_NFL_WEEK": 10,
                "NFL_SEASON": 2025,
                "ADP_SCORING": {"WEIGHT": 1.5, "STEPS": 10},
                "NORMALIZATION_MAX_SCALE": 100
            }
        }

        week_config_template = {
            "config_name": "Test Week Config",
            "parameters": {
                "PLAYER_RATING_SCORING": {"WEIGHT": 2.0},
                "TEAM_QUALITY_SCORING": {"WEIGHT": 1.5, "MIN_WEEKS": 4}
            }
        }

        (config_folder / "league_config.json").write_text(json.dumps(base_config, indent=2))
        (config_folder / "week1-5.json").write_text(json.dumps({**week_config_template, "config_name": "Week 1-5"}, indent=2))
        (config_folder / "week6-9.json").write_text(json.dumps({**week_config_template, "config_name": "Week 6-9"}, indent=2))
        (config_folder / "week10-13.json").write_text(json.dumps({**week_config_template, "config_name": "Week 10-13"}, indent=2))
        (config_folder / "week14-17.json").write_text(json.dumps({**week_config_template, "config_name": "Week 14-17"}, indent=2))

        return config_folder

    def test_init_with_5_file_structure(self, tmp_path):
        """__init__ should load 5-file structure successfully"""
        config_folder = self.create_6_file_config_folder(tmp_path)

        generator = ConfigGenerator(config_folder, num_test_values=5)

        assert hasattr(generator, 'baseline_configs')
        assert len(generator.baseline_configs) == 4
        assert '1-5' in generator.baseline_configs
        assert '6-9' in generator.baseline_configs
        assert '10-13' in generator.baseline_configs
        assert '14-17' in generator.baseline_configs

    def test_init_requires_all_weekly_files(self, tmp_path):
        """__init__ should fail if a weekly config file is missing"""
        config_folder = tmp_path / "test_configs"
        config_folder.mkdir()

        base_config = {"parameters": {}}
        (config_folder / "league_config.json").write_text(json.dumps(base_config))
        (config_folder / "week1-5.json").write_text(json.dumps(base_config))
        (config_folder / "week6-9.json").write_text(json.dumps(base_config))
        (config_folder / "week10-13.json").write_text(json.dumps(base_config))

        with pytest.raises(ValueError, match="week14-17.json"):
            ConfigGenerator(config_folder, num_test_values=5)

    def test_baseline_configs_separated_by_horizon(self, tmp_path):
        """Each horizon should have its own baseline config"""
        config_folder = self.create_6_file_config_folder(tmp_path)
        generator = ConfigGenerator(config_folder, num_test_values=5)

        for horizon in ['1-5', '6-9', '10-13', '14-17']:
            config = generator.baseline_configs[horizon]
            assert 'parameters' in config
            assert 'ADP_SCORING' in config['parameters']
            assert 'PLAYER_RATING_SCORING' in config['parameters']

    def test_generate_horizon_test_values_for_shared_param(self, tmp_path):
        """Shared params should return single 'shared' array"""
        config_folder = self.create_6_file_config_folder(tmp_path)
        generator = ConfigGenerator(config_folder, num_test_values=5)

        test_values = generator.generate_horizon_test_values('ADP_SCORING_WEIGHT')

        assert 'shared' in test_values
        assert len(test_values) == 1

        assert len(test_values['shared']) == 6

        assert test_values['shared'][0] == 1.5

    def test_generate_horizon_test_values_for_horizon_param(self, tmp_path):
        """Horizon params should return 4 separate arrays"""
        config_folder = self.create_6_file_config_folder(tmp_path)
        generator = ConfigGenerator(config_folder, num_test_values=5)

        test_values = generator.generate_horizon_test_values('TEAM_QUALITY_SCORING_WEIGHT')

        assert '1-5' in test_values
        assert '6-9' in test_values
        assert '10-13' in test_values
        assert '14-17' in test_values
        assert len(test_values) == 4

        for horizon in ['1-5', '6-9', '10-13', '14-17']:
            assert len(test_values[horizon]) == 6
            assert test_values[horizon][0] == 1.5

    def test_get_config_for_horizon_with_shared_param(self, tmp_path):
        """get_config_for_horizon should apply shared param to specified horizon"""
        config_folder = self.create_6_file_config_folder(tmp_path)
        generator = ConfigGenerator(config_folder, num_test_values=5)

        test_values = generator.generate_horizon_test_values('ADP_SCORING_WEIGHT')

        config = generator.get_config_for_horizon('1-5', 'ADP_SCORING_WEIGHT', 1)

        assert config['parameters']['ADP_SCORING']['WEIGHT'] == test_values['shared'][1]

        assert 'PLAYER_RATING_SCORING' in config['parameters']

    def test_get_config_for_horizon_with_horizon_param(self, tmp_path):
        """get_config_for_horizon should apply horizon-specific param"""
        config_folder = self.create_6_file_config_folder(tmp_path)
        generator = ConfigGenerator(config_folder, num_test_values=5)

        test_values = generator.generate_horizon_test_values('TEAM_QUALITY_SCORING_WEIGHT')

        config = generator.get_config_for_horizon('1-5', 'TEAM_QUALITY_SCORING_WEIGHT', 2)

        assert config['parameters']['TEAM_QUALITY_SCORING']['WEIGHT'] == test_values['1-5'][2]

    def test_update_baseline_for_horizon_with_shared_param(self, tmp_path):
        """update_baseline should update shared param in all horizons"""
        config_folder = self.create_6_file_config_folder(tmp_path)
        generator = ConfigGenerator(config_folder, num_test_values=5)

        new_config = copy.deepcopy(generator.baseline_configs['1-5'])
        new_config['parameters']['ADP_SCORING']['WEIGHT'] = 3.5

        generator.update_baseline_for_horizon('1-5', new_config)

        for horizon in ['1-5', '6-9', '10-13', '14-17']:
            assert generator.baseline_configs[horizon]['parameters']['ADP_SCORING']['WEIGHT'] == 3.5

    def test_update_baseline_for_horizon_with_horizon_param(self, tmp_path):
        """update_baseline should update only specified horizon for horizon params"""
        config_folder = self.create_6_file_config_folder(tmp_path)
        generator = ConfigGenerator(config_folder, num_test_values=5)

        new_config = copy.deepcopy(generator.baseline_configs['1-5'])
        new_config['parameters']['TEAM_QUALITY_SCORING']['WEIGHT'] = 5.0

        generator.update_baseline_for_horizon('1-5', new_config)

        assert generator.baseline_configs['1-5']['parameters']['TEAM_QUALITY_SCORING']['WEIGHT'] == 5.0

        assert generator.baseline_configs['6-9']['parameters']['TEAM_QUALITY_SCORING']['WEIGHT'] == 1.5
        assert generator.baseline_configs['10-13']['parameters']['TEAM_QUALITY_SCORING']['WEIGHT'] == 1.5
        assert generator.baseline_configs['14-17']['parameters']['TEAM_QUALITY_SCORING']['WEIGHT'] == 1.5

    def test_deprecated_parameter_order_removed(self, tmp_path):
        """__init__ should not accept parameter_order parameter"""
        config_folder = self.create_6_file_config_folder(tmp_path)

        with pytest.raises(TypeError):
            ConfigGenerator(config_folder, ['NORMALIZATION_MAX_SCALE'], num_test_values=5)

    def test_deprecated_num_parameters_to_test_removed(self, tmp_path):
        """__init__ should not accept num_parameters_to_test parameter"""
        config_folder = self.create_6_file_config_folder(tmp_path)

        with pytest.raises(TypeError):
            ConfigGenerator(config_folder, num_test_values=5, num_parameters_to_test=2)

    def test_nested_param_handling(self, tmp_path):
        """Nested params should be handled correctly"""
        config_folder = self.create_6_file_config_folder(tmp_path)
        generator = ConfigGenerator(config_folder, num_test_values=5)

        test_values = generator.generate_horizon_test_values('TEAM_QUALITY_MIN_WEEKS')

        for horizon in ['1-5', '6-9', '10-13', '14-17']:
            assert test_values[horizon][0] == 4

    def test_test_values_deterministic_with_seed(self, tmp_path):
        """Two generators built with the same explicit seed produce equal arrays.

        Re-expressed for the T51 private-RNG design: candidate draws come from the
        per-generator ConfigGenerator._rng (seeded from the constructor's `seed`
        argument), not the process-global `random` module. Determinism therefore
        holds without any external random.seed() call; two generators sharing an
        explicit seed match, and a generator with a different seed differs.
        """
        config_folder = self.create_6_file_config_folder(tmp_path)

        generator1 = ConfigGenerator(config_folder, num_test_values=5, seed=42)
        values1 = generator1.generate_horizon_test_values('ADP_SCORING_WEIGHT')

        generator2 = ConfigGenerator(config_folder, num_test_values=5, seed=42)
        values2 = generator2.generate_horizon_test_values('ADP_SCORING_WEIGHT')

        generator3 = ConfigGenerator(config_folder, num_test_values=5, seed=7)
        values3 = generator3.generate_horizon_test_values('ADP_SCORING_WEIGHT')

        assert values1['shared'] == values2['shared']
        assert values1['shared'] != values3['shared']


