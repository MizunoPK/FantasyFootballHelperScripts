"""
Comprehensive Unit Tests for ConfigGenerator

Tests all functionality of the ConfigGenerator class including:
- Initialization and configuration loading
- Parameter value generation
- Combination generation (cartesian product)
- Config dictionary creation
- Iterative optimization support
- Edge cases and error handling

Author: Kai Mizuno
Date: 2025
"""

import pytest
import json
import tempfile
import shutil
import random
import copy
from pathlib import Path
from unittest.mock import patch, Mock
import sys

# Add simulation/shared directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "simulation" / "shared"))
from ConfigGenerator import ConfigGenerator

# Standard parameter order for testing
# This mirrors the production PARAMETER_ORDER from run_simulation.py
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

    # Split base config into base and week-specific parts
    params = base_config.get('parameters', {})

    # Base parameters (non-week-specific)
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

    # Week-specific parameters
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
            'THRESHOLDS': {'BASE_POSITION': 0, 'DIRECTION': 'BI_EXCELLENT_HI', 'STEPS': 7.5}
        }),
        'SCHEDULE_SCORING': params.get('SCHEDULE_SCORING', {
            'IMPACT_SCALE': 80.0,
            'WEIGHT': 1.0,
            'MULTIPLIERS': {'EXCELLENT': 1.05, 'GOOD': 1.025, 'POOR': 0.975, 'VERY_POOR': 0.95},
            'THRESHOLDS': {'BASE_POSITION': 16, 'DIRECTION': 'INCREASING', 'STEPS': 8.0}
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

    # Write league_config.json
    league_config = {
        'config_name': base_config.get('config_name', 'test_baseline'),
        'description': 'Test base config',
        'parameters': base_params
    }
    with open(config_folder / 'league_config.json', 'w') as f:
        json.dump(league_config, f, indent=2)

    # Write draft_config.json (ROS horizon - same as week-specific for testing)
    draft_config = {
        'config_name': 'Test draft_config.json',
        'description': 'Test ROS/draft config',
        'parameters': week_params
    }
    with open(config_folder / 'draft_config.json', 'w') as f:
        json.dump(draft_config, f, indent=2)

    # Write week-specific files (all with same params for testing)
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
        assert gen.baseline_config is not None
        assert 'parameters' in gen.baseline_config

    def test_initialization_custom_num_test_values(self, temp_baseline_config):
        """Test initialization with custom num_test_values"""
        gen = ConfigGenerator(temp_baseline_config, num_test_values=3)

        assert gen.num_test_values == 3
        assert gen.baseline_config is not None

    def test_load_baseline_config_success(self, temp_baseline_config):
        """Test successful loading of baseline configuration"""
        gen = ConfigGenerator(temp_baseline_config)

        config = gen.baseline_config  # Backward compat property returns '1-5' horizon config
        # New API loads separate horizons (no merging), baseline_config returns '1-5' horizon
        assert config['config_name'] == 'Test week1-5.json'
        assert config['parameters']['NORMALIZATION_MAX_SCALE'] == 100.0
        assert config['parameters']['SAME_POS_BYE_WEIGHT'] == 1.0
        assert config['parameters']['DIFF_POS_BYE_WEIGHT'] == 1.0

    def test_param_definitions_exist(self, temp_baseline_config):
        """Test that param_definitions dict exists and is non-empty"""
        gen = ConfigGenerator(temp_baseline_config)

        # param_definitions should exist and contain entries
        assert hasattr(gen, 'param_definitions')
        assert isinstance(gen.param_definitions, dict)
        assert len(gen.param_definitions) > 0

        # Each param definition should be a tuple of (min_val, max_val, precision)
        for param_name, definition in gen.param_definitions.items():
            assert isinstance(definition, tuple), f"{param_name} should be a tuple"
            assert len(definition) == 3, f"{param_name} should have (min, max, precision)"
            min_val, max_val, precision = definition
            assert isinstance(precision, int), f"{param_name} precision should be int"
            assert precision >= 0, f"{param_name} precision should be >= 0"

    @pytest.mark.skip(reason="New API: parameter_order is deprecated (backward compat returns empty list). Parameter order now passed to manager, not generator.")
    def test_parameter_order_exists(self, temp_baseline_config):
        """Test that parameter_order instance variable exists"""
        gen = ConfigGenerator(temp_baseline_config)

        assert hasattr(gen, 'parameter_order')
        assert isinstance(gen.parameter_order, list)
        assert gen.parameter_order == TEST_PARAMETER_ORDER


class TestParameterValueGeneration:
    """Test parameter value generation methods"""

    @pytest.fixture
    def generator(self, tmp_path):
        """Create a ConfigGenerator instance for testing"""
        config = {"config_name": "test_config", "parameters": {}}
        config_folder = create_test_config_folder(config, tmp_path)
        return ConfigGenerator(config_folder, num_test_values=2)  # Use 2 for faster tests

    def test_generate_parameter_values_correct_count(self, generator):
        """Test that correct number of values are generated"""
        # With precision=0 (integers) for range 60-140, there are 81 possible values
        # Since num_test_values=2 < 81, we get 3 values (optimal + 2 random)
        values = generator.generate_parameter_values(
            'TEST_PARAM', 100, 60, 140, 0
        )

        # Should have num_test_values + 1 (optimal + N random)
        assert len(values) == 3  # 1 + 2

    def test_generate_parameter_values_includes_optimal(self, generator):
        """Test that optimal value is included as first value"""
        optimal = 100
        values = generator.generate_parameter_values(
            'TEST_PARAM', optimal, 60, 140, 0
        )

        assert values[0] == optimal

    def test_generate_parameter_values_respects_bounds(self, generator):
        """Test that generated values respect min/max bounds"""
        values = generator.generate_parameter_values(
            'TEST_PARAM', 100, 60, 140, 0
        )

        for val in values:
            assert 60 <= val <= 140

    def test_generate_parameter_values_random_variation(self, generator):
        """Test that random values vary from optimal"""
        optimal = 100
        values = generator.generate_parameter_values(
            'TEST_PARAM', optimal, 60, 140, 0
        )

        # At least one value should differ from optimal
        non_optimal_values = [v for v in values[1:] if v != optimal]
        assert len(non_optimal_values) >= 1

    def test_generate_parameter_values_precision_0_returns_integers(self, generator):
        """Test that precision=0 generates integer values"""
        values = generator.generate_parameter_values(
            'TEST_PARAM', 100, 60, 140, 0
        )

        for val in values:
            assert isinstance(val, int), f"Expected int, got {type(val)}: {val}"

    def test_generate_parameter_values_precision_1(self, generator):
        """Test that precision=1 generates 0.1 step values"""
        values = generator.generate_parameter_values(
            'TEST_PARAM', 0.3, 0.0, 0.5, 1
        )

        # With 6 possible values [0.0, 0.1, 0.2, 0.3, 0.4, 0.5] and num_test_values=2,
        # we get 3 values (optimal + 2 random)
        assert len(values) == 3
        assert values[0] == 0.3
        for val in values:
            # Check each value is at 0.1 precision
            assert round(val, 1) == val

    def test_generate_parameter_values_precision_2(self, generator):
        """Test that precision=2 generates 0.01 step values"""
        values = generator.generate_parameter_values(
            'TEST_PARAM', 1.50, 1.00, 2.00, 2
        )

        assert values[0] == 1.50
        for val in values:
            # Check each value is at 0.01 precision
            assert round(val, 2) == val

    def test_generate_parameter_values_full_enumeration(self, generator):
        """Test that when num_test_values >= possible values, all values returned"""
        # Range 0.0 to 0.5 with precision 1 = 6 possible values
        # num_test_values = 2, but if we bump it higher, we should get all 6
        config = {"config_name": "test_config", "parameters": {}}
        import tempfile
        from tests.simulation.test_config_generator import create_test_config_folder
        with tempfile.TemporaryDirectory() as tmp:
            from pathlib import Path
            config_folder = create_test_config_folder(config, Path(tmp))
            gen = ConfigGenerator(config_folder, num_test_values=10)  # > 6 possible values
            values = gen.generate_parameter_values('TEST_PARAM', 0.3, 0.0, 0.5, 1)

        # Should return all 6 possible values
        assert len(values) == 6
        # Optimal should be first
        assert values[0] == 0.3
        # Should contain all possible values
        assert set(values) == {0.0, 0.1, 0.2, 0.3, 0.4, 0.5}

    def test_generate_discrete_range_precision_0(self, generator):
        """Test _generate_discrete_range with precision=0 (integers)"""
        values = generator._generate_discrete_range(100, 105, 0)

        assert values == [100, 101, 102, 103, 104, 105]
        for v in values:
            assert isinstance(v, int)

    def test_generate_discrete_range_precision_1(self, generator):
        """Test _generate_discrete_range with precision=1 (0.1 steps)"""
        values = generator._generate_discrete_range(0.0, 0.5, 1)

        assert values == [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
        for v in values:
            assert round(v, 1) == v

    def test_generate_discrete_range_precision_2(self, generator):
        """Test _generate_discrete_range with precision=2 (0.01 steps)"""
        values = generator._generate_discrete_range(0.10, 0.15, 2)

        assert values == [0.10, 0.11, 0.12, 0.13, 0.14, 0.15]
        for v in values:
            assert round(v, 2) == v

    def test_generate_discrete_range_negative_values(self, generator):
        """Test _generate_discrete_range handles negative values"""
        # precision=1 means 0.1 steps, so -10.0 to 0.0 has 101 values
        values = generator._generate_discrete_range(-10.0, 0.0, 1)

        assert len(values) == 101  # (-10.0, -9.9, ..., -0.1, 0.0)
        assert values[0] == -10.0
        assert values[-1] == 0.0  # -0.0 equals 0.0

    def test_generate_discrete_range_integer_negative(self, generator):
        """Test _generate_discrete_range with precision=0 for negative integers"""
        values = generator._generate_discrete_range(-5, 0, 0)

        assert len(values) == 6  # [-5, -4, -3, -2, -1, 0]
        assert values == [-5, -4, -3, -2, -1, 0]

    def test_generate_all_parameter_value_sets_returns_all_params(self, generator):
        """Test that value sets are generated with valid structure"""
        value_sets = generator.generate_all_parameter_value_sets()

        # Should return a non-empty dict with value sets
        assert isinstance(value_sets, dict)
        assert len(value_sets) > 0

        # Each value set should be a list of numeric values
        for param_name, values in value_sets.items():
            assert isinstance(values, list), f"{param_name} should be a list"
            assert len(values) > 0, f"{param_name} should have values"
            # Values should be numeric
            for val in values:
                assert isinstance(val, (int, float)), f"{param_name} values should be numeric"

    def test_generate_all_parameter_value_sets_correct_value_count(self, generator):
        """Test that each value set has correct number of values"""
        value_sets = generator.generate_all_parameter_value_sets()

        # Each parameter should have num_test_values + 1 values
        expected_count = generator.num_test_values + 1
        for param_name, values in value_sets.items():
            assert len(values) == expected_count, f"{param_name} has {len(values)} values, expected {expected_count}"


class TestCombinationGeneration:
    """Test combination generation using cartesian product"""

    @pytest.fixture
    def generator(self, tmp_path):
        """Create a ConfigGenerator with minimal test values"""
        config = {"config_name": "test_config", "parameters": {}}
        config_folder = create_test_config_folder(config, tmp_path)
        return ConfigGenerator(config_folder, num_test_values=1)  # Use 1 for minimal combinations

    def test_generate_all_combinations_structure(self, generator):
        """Test that combinations have correct structure"""
        # Don't actually generate all combinations (could be millions)
        # Instead, test that the method structure works by checking value sets
        value_sets = generator.generate_all_parameter_value_sets()

        # Verify value sets are generated (number may vary based on enabled params)
        assert isinstance(value_sets, dict)
        assert len(value_sets) > 0

        # Each value set should have correct number of values
        expected_count = generator.num_test_values + 1
        for param_name, values in value_sets.items():
            assert len(values) == expected_count, f"{param_name} has {len(values)} values, expected {expected_count}"

    def test_generate_all_combinations_each_has_all_params(self, generator):
        """Test that each combination contains all generated value set params"""
        # Generate a single test combination manually
        value_sets = generator.generate_all_parameter_value_sets()

        # Create one test combination by taking first value of each parameter
        test_combo = {param: values[0] for param, values in value_sets.items()}

        # Verify all parameters that have value sets are in the combination
        # (not all param_definitions are extractable from every config)
        for param_name in value_sets:
            assert param_name in test_combo, f"Missing {param_name} in test combination"

        # Verify test_combo has valid structure
        assert isinstance(test_combo, dict)
        assert len(test_combo) > 0


class TestConfigDictCreation:
    """Test creation of complete configuration dictionaries"""

    @pytest.fixture
    def generator_and_combo(self, tmp_path):
        """Create a generator and a sample combination"""
        config = {"config_name": "test_config", "parameters": {}}
        config_folder = create_test_config_folder(config, tmp_path)
        gen = ConfigGenerator(config_folder)

        combination = {
            'NORMALIZATION_MAX_SCALE': 110.0,
            'SAME_POS_BYE_WEIGHT': 1.5,
            'DIFF_POS_BYE_WEIGHT': 1.2,
            'PRIMARY_BONUS': 55.0,
            'SECONDARY_BONUS': 45.0,
            'DRAFT_ORDER_FILE': 1,
            'ADP_SCORING_WEIGHT': 1.5,
            'PLAYER_RATING_SCORING_WEIGHT': 1.3,
            'TEAM_QUALITY_SCORING_WEIGHT': 1.2,
            'TEAM_QUALITY_MIN_WEEKS': 5,
            'PERFORMANCE_SCORING_WEIGHT': 1.1,
            'PERFORMANCE_MIN_WEEKS': 5,
            'MATCHUP_SCORING_WEIGHT': 1.4,
            'MATCHUP_MIN_WEEKS': 5,
            'ADP_SCORING_STEPS': 40.0,
            'PERFORMANCE_SCORING_STEPS': 0.12,
            'MATCHUP_IMPACT_SCALE': 175.0,
            'TEMPERATURE_IMPACT_SCALE': 50.0,
            'TEMPERATURE_SCORING_WEIGHT': 1.0,
            'WIND_IMPACT_SCALE': 60.0,
            'WIND_SCORING_WEIGHT': 1.0,
            'LOCATION_HOME': 2.0,
            'LOCATION_AWAY': -2.0,
            'LOCATION_INTERNATIONAL': -5.0,
        }

        return gen, combination

    def test_create_config_dict_updates_scalar_params(self, generator_and_combo):
        """Test that scalar parameters are updated correctly"""
        gen, combination = generator_and_combo
        config = gen.create_config_dict(combination)

        params = config['parameters']
        assert params['NORMALIZATION_MAX_SCALE'] == 110.0
        assert params['SAME_POS_BYE_WEIGHT'] == 1.5
        assert params['DIFF_POS_BYE_WEIGHT'] == 1.2
        assert params['DRAFT_ORDER_BONUSES']['PRIMARY'] == 55.0
        assert params['DRAFT_ORDER_BONUSES']['SECONDARY'] == 45.0
        assert params['MATCHUP_SCORING']['IMPACT_SCALE'] == 175.0
        # SCHEDULE_SCORING.IMPACT_SCALE not tested (not optimized)

    def test_create_config_dict_updates_multipliers(self, generator_and_combo):
        """Test that weights are updated in all sections"""
        gen, combination = generator_and_combo
        config = gen.create_config_dict(combination)

        params = config['parameters']

        # Check weights for optimized scoring sections
        assert params['ADP_SCORING']['WEIGHT'] == 1.5
        assert params['PLAYER_RATING_SCORING']['WEIGHT'] == 1.3
        assert params['TEAM_QUALITY_SCORING']['WEIGHT'] == 1.2
        assert params['PERFORMANCE_SCORING']['WEIGHT'] == 1.1
        assert params['MATCHUP_SCORING']['WEIGHT'] == 1.4
        # SCHEDULE_SCORING.WEIGHT not tested (not optimized)

    def test_create_config_dict_immutability(self, generator_and_combo):
        """Test that creating configs doesn't mutate baseline"""
        gen, combination = generator_and_combo
        original_baseline = gen.baseline_config['parameters']['NORMALIZATION_MAX_SCALE']

        # Create a config with different values
        config = gen.create_config_dict(combination)

        # Baseline should remain unchanged
        assert gen.baseline_config['parameters']['NORMALIZATION_MAX_SCALE'] == original_baseline


class TestIterativeOptimizationSupport:
    """Test methods that support iterative optimization"""

    @pytest.fixture
    def generator(self, tmp_path):
        """Create a generator for iterative optimization tests"""
        config = {"config_name": "test_config", "parameters": {}}
        config_folder = create_test_config_folder(config, tmp_path)
        return ConfigGenerator(config_folder, num_test_values=2)

    def test_generate_single_parameter_configs_correct_count(self, generator):
        """Test that correct number of configs are generated"""
        base_config = generator.baseline_config
        configs = generator.generate_single_parameter_configs('NORMALIZATION_MAX_SCALE', base_config)

        # Should have num_test_values + 1 configs
        assert len(configs) == 3  # 1 + 2

    def test_generate_single_parameter_configs_varies_target_param(self, generator):
        """Test that target parameter varies across configs"""
        base_config = generator.baseline_config
        configs = generator.generate_single_parameter_configs('NORMALIZATION_MAX_SCALE', base_config)

        # Extract values of target parameter
        values = [c['parameters']['NORMALIZATION_MAX_SCALE'] for c in configs]

        # Should have variation in values
        assert len(set(values)) > 1

    def test_extract_combination_from_config(self, generator):
        """Test extraction of combination dict from config"""
        config = generator.baseline_config
        combination = generator._extract_combination_from_config(config)

        # Should return a non-empty dict with parameter values
        assert isinstance(combination, dict)
        assert len(combination) > 0

        # All extracted values should be numeric
        for param_name, value in combination.items():
            assert isinstance(value, (int, float)), f"{param_name} should be numeric"

        # Core parameters should always be present
        core_params = [
            'NORMALIZATION_MAX_SCALE',
            'SAME_POS_BYE_WEIGHT',
            'DIFF_POS_BYE_WEIGHT',
            'PRIMARY_BONUS',
            'SECONDARY_BONUS',
        ]
        for param in core_params:
            assert param in combination, f"Core param {param} should be in combination"

    def test_generate_single_parameter_configs_for_multiplier(self, generator):
        """Test generating configs for a weight parameter"""
        base_config = generator.baseline_config
        configs = generator.generate_single_parameter_configs('ADP_SCORING_WEIGHT', base_config)

        assert len(configs) == 3  # num_test_values + 1

        # Extract weight values
        values = [c['parameters']['ADP_SCORING']['WEIGHT'] for c in configs]
        assert len(set(values)) > 1  # Should have variation


class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_missing_config_folder(self):
        """Test that missing config folder raises ValueError"""
        with pytest.raises(ValueError, match="does not exist"):
            ConfigGenerator(Path('/nonexistent/config_folder'))

    def test_config_file_instead_of_folder(self, tmp_path):
        """Test that passing a file instead of folder raises ValueError"""
        # Create a single JSON file (not a folder)
        config_file = tmp_path / "config.json"
        config_file.write_text('{"config_name": "test"}')

        with pytest.raises(ValueError, match="requires a folder path"):
            ConfigGenerator(config_file)

    def test_missing_required_files_in_folder(self, tmp_path):
        """Test that folder missing required files raises ValueError"""
        # Create folder with only league_config.json (missing week files)
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

        # Write invalid JSON
        (config_folder / "league_config.json").write_text("{invalid json")
        # Write valid draft_config and week files (6-file structure)
        with open(config_folder / "draft_config.json", 'w') as f:
            json.dump({"config_name": "draft_config", "parameters": {}}, f)
        for week_file in ['week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']:
            with open(config_folder / week_file, 'w') as f:
                json.dump({"config_name": week_file, "parameters": {}}, f)

        with pytest.raises(json.JSONDecodeError):
            ConfigGenerator(config_folder)

    # NOTE: parameter_order validation tests removed - parameter_order is no longer
    # passed to ConfigGenerator.__init__() in the new API. It's managed by the
    # simulation managers (SimulationManager, AccuracySimulationManager) instead.


@pytest.mark.skip(reason="Old API tests - generate_iterative_combinations and num_parameters_to_test are deprecated")
class TestGenerateIterativeCombinations:
    """Test generate_iterative_combinations with random parameter exploration

    NOTE: This class tests the OLD API (generate_iterative_combinations) which is deprecated.
    The new API uses:
    - generate_horizon_test_values(param_name) → returns test values
    - get_config_for_horizon(horizon, param_name, test_idx) → returns config
    - update_baseline_for_horizon(horizon, config) → updates baseline

    These tests are skipped but kept for reference. New tests for the new API
    are in TestHorizonBasedInterface below.
    """

    @pytest.fixture
    def baseline_config_dict(self):
        """Create baseline config dictionary for testing"""
        return {"config_name": "test_baseline", "parameters": {}}

    @pytest.fixture
    def test_config_generator(self, baseline_config_dict, tmp_path):
        """Create ConfigGenerator instance for testing"""
        config_folder = create_test_config_folder(baseline_config_dict, tmp_path)
        return ConfigGenerator(config_folder, num_test_values=5)

    def test_with_num_parameters_1_base_only(self, baseline_config_dict, tmp_path):
        """Test with NUM_PARAMETERS_TO_TEST=1 (base parameter only)"""
        if not TEST_PARAMETER_ORDER:
            return

        config_folder = create_test_config_folder(baseline_config_dict, tmp_path)
        generator = ConfigGenerator(config_folder, num_test_values=5, num_parameters_to_test=1)
        first_param = TEST_PARAMETER_ORDER[0]
        configs = generator.generate_iterative_combinations(first_param, generator.baseline_config)

        expected_count = generator.num_test_values + 1
        assert len(configs) == expected_count

        for config in configs:
            assert 'parameters' in config
            assert 'config_name' in config

    def test_with_num_parameters_2_base_plus_one_random(self, baseline_config_dict, tmp_path):
        """Test with NUM_PARAMETERS_TO_TEST=2 (base + 1 random)"""
        if len(TEST_PARAMETER_ORDER) < 2:
            return

        config_folder = create_test_config_folder(baseline_config_dict, tmp_path)
        generator = ConfigGenerator(config_folder, num_test_values=5, num_parameters_to_test=2)
        first_param = TEST_PARAMETER_ORDER[0]
        configs = generator.generate_iterative_combinations(first_param, generator.baseline_config)

        n = generator.num_test_values
        expected_count = 2 * (n + 1) + (n + 1) ** 2
        assert len(configs) == expected_count

        for config in configs:
            assert 'parameters' in config

    def test_with_num_parameters_3_base_plus_two_random(self, baseline_config_dict, tmp_path):
        """Test with NUM_PARAMETERS_TO_TEST=3 (base + 2 random)"""
        if len(TEST_PARAMETER_ORDER) < 3:
            return

        config_folder = create_test_config_folder(baseline_config_dict, tmp_path)
        generator = ConfigGenerator(config_folder, num_test_values=5, num_parameters_to_test=3)
        first_param = TEST_PARAMETER_ORDER[0]
        configs = generator.generate_iterative_combinations(first_param, generator.baseline_config)

        n = generator.num_test_values
        expected_count = 3 * (n + 1) + (n + 1) ** 3
        assert len(configs) == expected_count

        for config in configs:
            assert 'parameters' in config

    def test_edge_case_num_parameters_exceeds_available(self, baseline_config_dict, tmp_path):
        """Test that num_parameters_to_test is capped at PARAMETER_ORDER length"""
        config_folder = create_test_config_folder(baseline_config_dict, tmp_path)
        num_params = min(4, len(TEST_PARAMETER_ORDER)) if TEST_PARAMETER_ORDER else 1
        generator = ConfigGenerator(config_folder, num_test_values=1, num_parameters_to_test=num_params)

        if not TEST_PARAMETER_ORDER:
            return

        first_param = TEST_PARAMETER_ORDER[0]
        configs = generator.generate_iterative_combinations(first_param, generator.baseline_config)

        assert len(configs) > 0
        assert all('parameters' in config for config in configs)

        # Create another generator with 100 params - should cap at PARAMETER_ORDER length
        generator2 = ConfigGenerator(config_folder, num_test_values=1, num_parameters_to_test=100)
        assert len(generator2.parameter_order) == len(TEST_PARAMETER_ORDER)

    def test_edge_case_invalid_param_name(self, test_config_generator):
        """Test with invalid parameter name (should raise ValueError)"""
        with pytest.raises(ValueError, match="Unknown parameter: INVALID_PARAM"):
            test_config_generator.generate_iterative_combinations('INVALID_PARAM', test_config_generator.baseline_config)

    def test_randomness_varies_parameter_selection(self, baseline_config_dict, tmp_path):
        """Test that random parameter selection varies between runs"""
        if not TEST_PARAMETER_ORDER:
            return

        config_folder = create_test_config_folder(baseline_config_dict, tmp_path)
        num_params = min(2, len(TEST_PARAMETER_ORDER))
        generator = ConfigGenerator(config_folder, num_test_values=5, num_parameters_to_test=num_params)

        first_param = TEST_PARAMETER_ORDER[0]
        configs1 = generator.generate_iterative_combinations(first_param, generator.baseline_config)
        configs2 = generator.generate_iterative_combinations(first_param, generator.baseline_config)

        assert len(configs1) == len(configs2)
        assert len(configs1) > 0
        assert all('parameters' in config for config in configs1)
        assert all('parameters' in config for config in configs2)

    def test_config_structure_is_valid(self, test_config_generator):
        """Test that all returned configs have valid structure"""
        if not TEST_PARAMETER_ORDER:
            return

        first_param = TEST_PARAMETER_ORDER[0]
        configs = test_config_generator.generate_iterative_combinations(
            first_param,
            test_config_generator.baseline_config
        )

        for config in configs:
            assert 'config_name' in config
            assert 'parameters' in config
            assert isinstance(config['parameters'], dict)

    def test_combination_configs_have_multiple_params_varied(self, baseline_config_dict, tmp_path):
        """Test that combination configs actually vary multiple parameters"""
        if len(TEST_PARAMETER_ORDER) < 2:
            return

        config_folder = create_test_config_folder(baseline_config_dict, tmp_path)
        generator = ConfigGenerator(config_folder, num_test_values=2, num_parameters_to_test=2)
        first_param = TEST_PARAMETER_ORDER[0]
        configs = generator.generate_iterative_combinations(first_param, generator.baseline_config)

        assert len(configs) > 0
        for config in configs:
            assert 'parameters' in config
            assert isinstance(config['parameters'], dict)

    def test_edge_case_num_parameters_zero_defaults_to_one(self, baseline_config_dict, tmp_path):
        """Test that num_parameters_to_test=0 defaults to 1"""
        if not TEST_PARAMETER_ORDER:
            return

        config_folder = create_test_config_folder(baseline_config_dict, tmp_path)
        generator = ConfigGenerator(config_folder, num_test_values=5, num_parameters_to_test=0)
        first_param = TEST_PARAMETER_ORDER[0]
        configs = generator.generate_iterative_combinations(first_param, generator.baseline_config)

        expected_count = generator.num_test_values + 1
        assert len(configs) == expected_count


class TestDraftOrderFile:
    """Test DRAFT_ORDER_FILE parameter functionality"""

    @pytest.fixture
    def baseline_config_with_draft_order(self):
        """Create baseline config with DRAFT_ORDER_FILE"""
        return {
            "config_name": "test_baseline",
            "parameters": {
                "DRAFT_ORDER_FILE": 1,
                "DRAFT_ORDER": [{"FLEX": "P", "QB": "S"}] * 15,
            }
        }

    def test_draft_order_file_in_param_definitions(self):
        """Test DRAFT_ORDER_FILE is in PARAM_DEFINITIONS with correct range and precision"""
        assert 'DRAFT_ORDER_FILE' in ConfigGenerator.PARAM_DEFINITIONS
        min_val, max_val, precision = ConfigGenerator.PARAM_DEFINITIONS['DRAFT_ORDER_FILE']
        assert min_val == 1
        assert max_val == 100  # Range expanded to include 100 draft order strategies
        assert precision == 0  # Integers

    def test_draft_order_file_not_in_parameter_order(self):
        """Test DRAFT_ORDER_FILE is NOT in PARAMETER_ORDER (handled by separate script)"""
        # DRAFT_ORDER_FILE is intentionally excluded from PARAMETER_ORDER
        # because it's optimized by the dedicated run_draft_order_simulation.py script
        assert 'DRAFT_ORDER_FILE' not in TEST_PARAMETER_ORDER
        # But it IS in PARAM_DEFINITIONS for use by the draft order simulation
        assert 'DRAFT_ORDER_FILE' in ConfigGenerator.PARAM_DEFINITIONS

    def test_generate_parameter_values_for_draft_order(self, baseline_config_with_draft_order, tmp_path):
        """Test discrete integer value generation for DRAFT_ORDER_FILE (precision=0)"""
        config_folder = create_test_config_folder(baseline_config_with_draft_order, tmp_path)
        generator = ConfigGenerator(config_folder, num_test_values=5)
        # Use unified method with precision=0 for integers
        values = generator.generate_parameter_values('DRAFT_ORDER_FILE', 1, 1, 30, 0)

        assert len(values) == 6
        assert values[0] == 1
        for v in values:
            assert isinstance(v, int)
            assert 1 <= v <= 30
        assert len(set(values)) == 6

    def test_extract_combination_includes_draft_order_file(self, baseline_config_with_draft_order, tmp_path):
        """Test _extract_combination_from_config includes DRAFT_ORDER_FILE"""
        config_folder = create_test_config_folder(baseline_config_with_draft_order, tmp_path)
        generator = ConfigGenerator(config_folder)
        combination = generator._extract_combination_from_config(generator.baseline_config)

        assert 'DRAFT_ORDER_FILE' in combination
        assert combination['DRAFT_ORDER_FILE'] == 1

    def test_generate_single_parameter_configs_draft_order_file(self, baseline_config_with_draft_order, tmp_path):
        """Test generating configs for DRAFT_ORDER_FILE parameter"""
        config_folder = create_test_config_folder(baseline_config_with_draft_order, tmp_path)
        generator = ConfigGenerator(config_folder, num_test_values=3)

        # Mock _load_draft_order_from_file to avoid file system dependency
        mock_draft_order = [{"FLEX": "P", "QB": "S"}] * 15
        with patch.object(generator, '_load_draft_order_from_file', return_value=mock_draft_order):
            configs = generator.generate_single_parameter_configs(
                'DRAFT_ORDER_FILE',
                generator.baseline_config
            )

        assert len(configs) == 4

        for config in configs:
            assert 'DRAFT_ORDER_FILE' in config['parameters']
            assert 'DRAFT_ORDER' in config['parameters']
            assert isinstance(config['parameters']['DRAFT_ORDER'], list)

    def test_create_config_dict_loads_draft_order(self, baseline_config_with_draft_order, tmp_path):
        """Test create_config_dict loads DRAFT_ORDER from file"""
        config_folder = create_test_config_folder(baseline_config_with_draft_order, tmp_path)
        generator = ConfigGenerator(config_folder)
        combination = generator._extract_combination_from_config(generator.baseline_config)

        combination['DRAFT_ORDER_FILE'] = 1
        config = generator.create_config_dict(combination)

        assert config['parameters']['DRAFT_ORDER_FILE'] == 1
        assert isinstance(config['parameters']['DRAFT_ORDER'], list)
        assert len(config['parameters']['DRAFT_ORDER']) == 15

    def test_load_draft_order_from_file_not_found(self, baseline_config_with_draft_order, tmp_path):
        """Test _load_draft_order_from_file raises error for invalid file number"""
        config_folder = create_test_config_folder(baseline_config_with_draft_order, tmp_path)
        generator = ConfigGenerator(config_folder)
        with pytest.raises(FileNotFoundError):
            generator._load_draft_order_from_file(999)


# ============================================================================
# NEW: Horizon-Based Interface Tests (6-File Structure)
# ============================================================================

class TestHorizonBasedInterface:
    """Test new horizon-based ConfigGenerator interface for 6-file structure"""

    def create_6_file_config_folder(self, tmp_path):
        """Helper to create 6-file config structure for testing"""
        config_folder = tmp_path / "test_configs"
        config_folder.mkdir()

        # Base config (league_config.json)
        base_config = {
            "config_name": "Test Config",
            "parameters": {
                "CURRENT_NFL_WEEK": 10,
                "NFL_SEASON": 2025,
                "ADP_SCORING": {"WEIGHT": 1.5, "STEPS": 10},
                "NORMALIZATION_MAX_SCALE": 100
            }
        }

        # Week-specific configs (draft_config.json + 4 week files)
        week_config_template = {
            "config_name": "Test Week Config",
            "parameters": {
                "PLAYER_RATING_SCORING": {"WEIGHT": 2.0},
                "TEAM_QUALITY_SCORING": {"WEIGHT": 1.5, "MIN_WEEKS": 4}
            }
        }

        # Save all 6 files
        (config_folder / "league_config.json").write_text(json.dumps(base_config, indent=2))
        (config_folder / "draft_config.json").write_text(json.dumps({**week_config_template, "config_name": "Draft Config"}, indent=2))
        (config_folder / "week1-5.json").write_text(json.dumps({**week_config_template, "config_name": "Week 1-5"}, indent=2))
        (config_folder / "week6-9.json").write_text(json.dumps({**week_config_template, "config_name": "Week 6-9"}, indent=2))
        (config_folder / "week10-13.json").write_text(json.dumps({**week_config_template, "config_name": "Week 10-13"}, indent=2))
        (config_folder / "week14-17.json").write_text(json.dumps({**week_config_template, "config_name": "Week 14-17"}, indent=2))

        return config_folder

    def test_init_with_6_file_structure(self, tmp_path):
        """__init__ should load 6-file structure successfully"""
        config_folder = self.create_6_file_config_folder(tmp_path)

        generator = ConfigGenerator(config_folder, num_test_values=5)

        # Should have 5 baseline configs (one per horizon)
        assert hasattr(generator, 'baseline_configs')
        assert len(generator.baseline_configs) == 5
        assert 'ros' in generator.baseline_configs
        assert '1-5' in generator.baseline_configs
        assert '6-9' in generator.baseline_configs
        assert '10-13' in generator.baseline_configs
        assert '14-17' in generator.baseline_configs

    def test_init_requires_6_files(self, tmp_path):
        """__init__ should fail if draft_config.json is missing"""
        config_folder = tmp_path / "test_configs"
        config_folder.mkdir()

        # Create only 5 files (missing draft_config.json)
        base_config = {"parameters": {}}
        (config_folder / "league_config.json").write_text(json.dumps(base_config))
        (config_folder / "week1-5.json").write_text(json.dumps(base_config))
        (config_folder / "week6-9.json").write_text(json.dumps(base_config))
        (config_folder / "week10-13.json").write_text(json.dumps(base_config))
        (config_folder / "week14-17.json").write_text(json.dumps(base_config))

        with pytest.raises(ValueError, match="draft_config.json"):
            ConfigGenerator(config_folder, num_test_values=5)

    def test_baseline_configs_separated_by_horizon(self, tmp_path):
        """Each horizon should have its own baseline config"""
        config_folder = self.create_6_file_config_folder(tmp_path)
        generator = ConfigGenerator(config_folder, num_test_values=5)

        # Each horizon config should have both base and week-specific params
        for horizon in ['ros', '1-5', '6-9', '10-13', '14-17']:
            config = generator.baseline_configs[horizon]
            assert 'parameters' in config
            # Base params from league_config.json
            assert 'ADP_SCORING' in config['parameters']
            # Week-specific params from horizon file
            assert 'PLAYER_RATING_SCORING' in config['parameters']

    def test_generate_horizon_test_values_for_shared_param(self, tmp_path):
        """Shared params should return single 'shared' array"""
        config_folder = self.create_6_file_config_folder(tmp_path)
        generator = ConfigGenerator(config_folder, num_test_values=5)

        # ADP_SCORING_WEIGHT is a base/shared param
        test_values = generator.generate_horizon_test_values('ADP_SCORING_WEIGHT')

        # Should have 'shared' key only
        assert 'shared' in test_values
        assert len(test_values) == 1

        # Should have 6 values (baseline + 5 test values)
        assert len(test_values['shared']) == 6

        # First value should be baseline
        assert test_values['shared'][0] == 1.5

    def test_generate_horizon_test_values_for_horizon_param(self, tmp_path):
        """Horizon params should return 5 separate arrays"""
        config_folder = self.create_6_file_config_folder(tmp_path)
        generator = ConfigGenerator(config_folder, num_test_values=5)

        # PLAYER_RATING_SCORING_WEIGHT is week-specific
        test_values = generator.generate_horizon_test_values('PLAYER_RATING_SCORING_WEIGHT')

        # Should have all 5 horizon keys
        assert 'ros' in test_values
        assert '1-5' in test_values
        assert '6-9' in test_values
        assert '10-13' in test_values
        assert '14-17' in test_values
        assert len(test_values) == 5

        # Each horizon should have 6 values
        for horizon in ['ros', '1-5', '6-9', '10-13', '14-17']:
            assert len(test_values[horizon]) == 6
            # First value should be baseline (2.0)
            assert test_values[horizon][0] == 2.0

    def test_get_config_for_horizon_with_shared_param(self, tmp_path):
        """get_config_for_horizon should apply shared param to specified horizon"""
        config_folder = self.create_6_file_config_folder(tmp_path)
        generator = ConfigGenerator(config_folder, num_test_values=5)

        # Generate test values first
        test_values = generator.generate_horizon_test_values('ADP_SCORING_WEIGHT')

        # Get config for horizon '1-5' with test_index 1
        config = generator.get_config_for_horizon('1-5', 'ADP_SCORING_WEIGHT', 1)

        # Should have the test value applied
        assert config['parameters']['ADP_SCORING']['WEIGHT'] == test_values['shared'][1]

        # Should still have week-specific params from week1-5.json
        assert 'PLAYER_RATING_SCORING' in config['parameters']

    def test_get_config_for_horizon_with_horizon_param(self, tmp_path):
        """get_config_for_horizon should apply horizon-specific param"""
        config_folder = self.create_6_file_config_folder(tmp_path)
        generator = ConfigGenerator(config_folder, num_test_values=5)

        test_values = generator.generate_horizon_test_values('PLAYER_RATING_SCORING_WEIGHT')

        # Get config for 'ros' horizon with test_index 2
        config = generator.get_config_for_horizon('ros', 'PLAYER_RATING_SCORING_WEIGHT', 2)

        # Should have the test value from 'ros' array
        assert config['parameters']['PLAYER_RATING_SCORING']['WEIGHT'] == test_values['ros'][2]

    def test_update_baseline_for_horizon_with_shared_param(self, tmp_path):
        """update_baseline should update shared param in all horizons"""
        config_folder = self.create_6_file_config_folder(tmp_path)
        generator = ConfigGenerator(config_folder, num_test_values=5)

        # Create new config with updated shared param
        new_config = copy.deepcopy(generator.baseline_configs['1-5'])
        new_config['parameters']['ADP_SCORING']['WEIGHT'] = 3.5

        # Update baseline (horizon doesn't matter for shared params)
        generator.update_baseline_for_horizon('1-5', new_config)

        # All horizons should have updated value
        for horizon in ['ros', '1-5', '6-9', '10-13', '14-17']:
            assert generator.baseline_configs[horizon]['parameters']['ADP_SCORING']['WEIGHT'] == 3.5

    def test_update_baseline_for_horizon_with_horizon_param(self, tmp_path):
        """update_baseline should update only specified horizon for horizon params"""
        config_folder = self.create_6_file_config_folder(tmp_path)
        generator = ConfigGenerator(config_folder, num_test_values=5)

        # Create new config with updated horizon param
        new_config = copy.deepcopy(generator.baseline_configs['ros'])
        new_config['parameters']['PLAYER_RATING_SCORING']['WEIGHT'] = 5.0

        # Update only 'ros' horizon
        generator.update_baseline_for_horizon('ros', new_config)

        # Only 'ros' should be updated
        assert generator.baseline_configs['ros']['parameters']['PLAYER_RATING_SCORING']['WEIGHT'] == 5.0

        # Other horizons should still have original value (2.0)
        assert generator.baseline_configs['1-5']['parameters']['PLAYER_RATING_SCORING']['WEIGHT'] == 2.0
        assert generator.baseline_configs['6-9']['parameters']['PLAYER_RATING_SCORING']['WEIGHT'] == 2.0

    def test_deprecated_parameter_order_removed(self, tmp_path):
        """__init__ should not accept parameter_order parameter"""
        config_folder = self.create_6_file_config_folder(tmp_path)

        # Old signature had parameter_order as second param
        # New signature should not accept it
        with pytest.raises(TypeError):
            ConfigGenerator(config_folder, ['NORMALIZATION_MAX_SCALE'], num_test_values=5)

    def test_deprecated_num_parameters_to_test_removed(self, tmp_path):
        """__init__ should not accept num_parameters_to_test parameter"""
        config_folder = self.create_6_file_config_folder(tmp_path)

        # Old signature had num_parameters_to_test param
        # New signature should not accept it
        with pytest.raises(TypeError):
            ConfigGenerator(config_folder, num_test_values=5, num_parameters_to_test=2)

    def test_nested_param_handling(self, tmp_path):
        """Nested params should be handled correctly"""
        config_folder = self.create_6_file_config_folder(tmp_path)
        generator = ConfigGenerator(config_folder, num_test_values=5)

        # TEAM_QUALITY_MIN_WEEKS is nested in TEAM_QUALITY_SCORING
        test_values = generator.generate_horizon_test_values('TEAM_QUALITY_MIN_WEEKS')

        # Should extract nested value correctly (4 from baseline)
        for horizon in ['ros', '1-5', '6-9', '10-13', '14-17']:
            assert test_values[horizon][0] == 4

    def test_test_values_deterministic_with_seed(self, tmp_path):
        """Test values should be deterministic when using same seed"""
        config_folder = self.create_6_file_config_folder(tmp_path)

        generator1 = ConfigGenerator(config_folder, num_test_values=5)
        random.seed(42)
        values1 = generator1.generate_horizon_test_values('ADP_SCORING_WEIGHT')

        generator2 = ConfigGenerator(config_folder, num_test_values=5)
        random.seed(42)
        values2 = generator2.generate_horizon_test_values('ADP_SCORING_WEIGHT')

        # Should be identical
        assert values1['shared'] == values2['shared']
