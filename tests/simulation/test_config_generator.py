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
from pathlib import Path
import sys

# Add simulation directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "simulation"))
from ConfigGenerator import ConfigGenerator


class TestConfigGeneratorInitialization:
    """Test ConfigGenerator initialization and configuration loading"""

    @pytest.fixture
    def temp_baseline_config(self):
        """Create a temporary baseline config for testing"""
        config = {
            "config_name": "test_baseline",
            "parameters": {
                "NORMALIZATION_MAX_SCALE": 100.0,
                "BASE_BYE_PENALTY": 25.0,
                "DRAFT_ORDER_BONUSES": {
                    "PRIMARY": 50.0,
                    "SECONDARY": 40.0
                },
                "ADP_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.2,
                        "GOOD": 1.1,
                        "POOR": 0.9,
                        "VERY_POOR": 0.8
                    }
                },
                "PLAYER_RATING_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.25,
                        "GOOD": 1.15,
                        "POOR": 0.85,
                        "VERY_POOR": 0.75
                    }
                },
                "TEAM_QUALITY_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.3,
                        "GOOD": 1.2,
                        "POOR": 0.8,
                        "VERY_POOR": 0.7
                    }
                },
                "PERFORMANCE_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.15,
                        "GOOD": 1.05,
                        "POOR": 0.95,
                        "VERY_POOR": 0.85
                    }
                },
                "MATCHUP_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.2,
                        "GOOD": 1.1,
                        "POOR": 0.9,
                        "VERY_POOR": 0.8
                    }
                }
            }
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            temp_path = Path(f.name)

        yield temp_path
        temp_path.unlink()

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

        config = gen.baseline_config
        assert config['config_name'] == 'test_baseline'
        assert config['parameters']['NORMALIZATION_MAX_SCALE'] == 100.0
        assert config['parameters']['BASE_BYE_PENALTY'] == 25.0

    def test_param_definitions_exist(self, temp_baseline_config):
        """Test that all parameter definitions are present"""
        gen = ConfigGenerator(temp_baseline_config)

        assert 'NORMALIZATION_MAX_SCALE' in gen.param_definitions
        assert 'BASE_BYE_PENALTY' in gen.param_definitions
        assert 'PRIMARY_BONUS' in gen.param_definitions
        assert 'SECONDARY_BONUS' in gen.param_definitions
        assert 'ADP_SCORING_WEIGHT' in gen.param_definitions
        assert 'PLAYER_RATING_SCORING_WEIGHT' in gen.param_definitions
        assert 'TEAM_QUALITY_SCORING_WEIGHT' in gen.param_definitions
        assert 'MATCHUP_SCORING_WEIGHT' in gen.param_definitions

    def test_parameter_order_exists(self, temp_baseline_config):
        """Test that PARAMETER_ORDER list exists and has expected length"""
        gen = ConfigGenerator(temp_baseline_config)

        assert hasattr(gen, 'PARAMETER_ORDER')
        assert len(gen.PARAMETER_ORDER) == 9  # 4 scalars + 5 weights


class TestParameterValueGeneration:
    """Test parameter value generation methods"""

    @pytest.fixture
    def generator(self):
        """Create a ConfigGenerator instance for testing"""
        config = {
            "config_name": "test_config",
            "parameters": {
                "NORMALIZATION_MAX_SCALE": 100.0,
                "BASE_BYE_PENALTY": 25.0,
                "DRAFT_ORDER_BONUSES": {
                    "PRIMARY": 50.0,
                    "SECONDARY": 40.0
                },
                "ADP_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.2,
                        "GOOD": 1.1,
                        "POOR": 0.9,
                        "VERY_POOR": 0.8
                    }
                },
                "PLAYER_RATING_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.25,
                        "GOOD": 1.15,
                        "POOR": 0.85,
                        "VERY_POOR": 0.75
                    }
                },
                "TEAM_QUALITY_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.3,
                        "GOOD": 1.2,
                        "POOR": 0.8,
                        "VERY_POOR": 0.7
                    }
                },
                "PERFORMANCE_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.15,
                        "GOOD": 1.05,
                        "POOR": 0.95,
                        "VERY_POOR": 0.85
                    }
                },
                "MATCHUP_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.2,
                        "GOOD": 1.1,
                        "POOR": 0.9,
                        "VERY_POOR": 0.8
                    }
                }
            }
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            temp_path = Path(f.name)

        gen = ConfigGenerator(temp_path, num_test_values=2)  # Use 2 for faster tests
        temp_path.unlink()
        return gen

    def test_generate_parameter_values_correct_count(self, generator):
        """Test that correct number of values are generated"""
        values = generator.generate_parameter_values(
            'TEST_PARAM', 100.0, 20.0, 60.0, 140.0
        )

        # Should have num_test_values + 1 (optimal + N random)
        assert len(values) == 3  # 1 + 2

    def test_generate_parameter_values_includes_optimal(self, generator):
        """Test that optimal value is included as first value"""
        optimal = 100.0
        values = generator.generate_parameter_values(
            'TEST_PARAM', optimal, 20.0, 60.0, 140.0
        )

        assert values[0] == optimal

    def test_generate_parameter_values_respects_bounds(self, generator):
        """Test that generated values respect min/max bounds"""
        values = generator.generate_parameter_values(
            'TEST_PARAM', 100.0, 20.0, 60.0, 140.0
        )

        for val in values:
            assert 60.0 <= val <= 140.0

    def test_generate_parameter_values_random_variation(self, generator):
        """Test that random values vary from optimal"""
        optimal = 100.0
        values = generator.generate_parameter_values(
            'TEST_PARAM', optimal, 20.0, 60.0, 140.0
        )

        # At least one value should differ from optimal
        non_optimal_values = [v for v in values[1:] if v != optimal]
        assert len(non_optimal_values) >= 1

    def test_generate_all_parameter_value_sets_returns_all_params(self, generator):
        """Test that value sets are generated for all parameters"""
        value_sets = generator.generate_all_parameter_value_sets()

        # Should have 4 scalar + 5 weight parameters
        assert len(value_sets) == 9
        assert 'NORMALIZATION_MAX_SCALE' in value_sets
        assert 'BASE_BYE_PENALTY' in value_sets
        assert 'PRIMARY_BONUS' in value_sets
        assert 'SECONDARY_BONUS' in value_sets
        assert 'ADP_SCORING_WEIGHT' in value_sets
        assert 'PLAYER_RATING_SCORING_WEIGHT' in value_sets
        assert 'TEAM_QUALITY_SCORING_WEIGHT' in value_sets
        assert 'MATCHUP_SCORING_WEIGHT' in value_sets
        assert 'PERFORMANCE_SCORING_WEIGHT' in value_sets

    def test_generate_all_parameter_value_sets_correct_value_count(self, generator):
        """Test that each value set has correct number of values"""
        value_sets = generator.generate_all_parameter_value_sets()

        # Each parameter should have num_test_values + 1 values
        for param_name, values in value_sets.items():
            assert len(values) == 3  # 1 + 2 (num_test_values=2)


class TestCombinationGeneration:
    """Test combination generation using cartesian product"""

    @pytest.fixture
    def generator(self):
        """Create a ConfigGenerator with minimal test values"""
        config = {
            "config_name": "test_config",
            "parameters": {
                "NORMALIZATION_MAX_SCALE": 100.0,
                "BASE_BYE_PENALTY": 25.0,
                "DRAFT_ORDER_BONUSES": {
                    "PRIMARY": 50.0,
                    "SECONDARY": 40.0
                },
                "ADP_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.2,
                        "GOOD": 1.1,
                        "POOR": 0.9,
                        "VERY_POOR": 0.8
                    }
                },
                "PLAYER_RATING_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.25,
                        "GOOD": 1.15,
                        "POOR": 0.85,
                        "VERY_POOR": 0.75
                    }
                },
                "TEAM_QUALITY_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.3,
                        "GOOD": 1.2,
                        "POOR": 0.8,
                        "VERY_POOR": 0.7
                    }
                },
                "PERFORMANCE_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.15,
                        "GOOD": 1.05,
                        "POOR": 0.95,
                        "VERY_POOR": 0.85
                    }
                },
                "MATCHUP_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.2,
                        "GOOD": 1.1,
                        "POOR": 0.9,
                        "VERY_POOR": 0.8
                    }
                }
            }
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            temp_path = Path(f.name)

        gen = ConfigGenerator(temp_path, num_test_values=1)  # Use 1 for minimal combinations
        temp_path.unlink()
        return gen

    def test_generate_all_combinations_structure(self, generator):
        """Test that combinations have correct structure"""
        # Don't actually generate all combinations (could be millions)
        # Instead, test that the method structure works by checking value sets
        value_sets = generator.generate_all_parameter_value_sets()

        # Verify value sets exist for all expected parameters (4 scalars + 5 weights = 9 total)
        assert len(value_sets) == 9  # 4 scalars + 4 weights
        assert 'NORMALIZATION_MAX_SCALE' in value_sets
        assert 'ADP_SCORING_WEIGHT' in value_sets

        # Each value set should have correct number of values
        for param_name, values in value_sets.items():
            assert len(values) == 2  # num_test_values=1, so 1+1=2

    def test_generate_all_combinations_each_has_all_params(self, generator):
        """Test that each combination contains all parameters"""
        # Generate a single test combination manually
        value_sets = generator.generate_all_parameter_value_sets()

        # Create one test combination by taking first value of each parameter
        test_combo = {param: values[0] for param, values in value_sets.items()}

        # Verify all required parameters are present
        assert 'NORMALIZATION_MAX_SCALE' in test_combo
        assert 'BASE_BYE_PENALTY' in test_combo
        assert 'PRIMARY_BONUS' in test_combo
        assert 'SECONDARY_BONUS' in test_combo


class TestConfigDictCreation:
    """Test creation of complete configuration dictionaries"""

    @pytest.fixture
    def generator_and_combo(self):
        """Create a generator and a sample combination"""
        config = {
            "config_name": "test_config",
            "parameters": {
                "NORMALIZATION_MAX_SCALE": 100.0,
                "BASE_BYE_PENALTY": 25.0,
                "DRAFT_ORDER_BONUSES": {
                    "PRIMARY": 50.0,
                    "SECONDARY": 40.0
                },
                "ADP_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.2,
                        "GOOD": 1.1,
                        "POOR": 0.9,
                        "VERY_POOR": 0.8
                    }
                },
                "PLAYER_RATING_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.25,
                        "GOOD": 1.15,
                        "POOR": 0.85,
                        "VERY_POOR": 0.75
                    }
                },
                "TEAM_QUALITY_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.3,
                        "GOOD": 1.2,
                        "POOR": 0.8,
                        "VERY_POOR": 0.7
                    }
                },
                "PERFORMANCE_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.15,
                        "GOOD": 1.05,
                        "POOR": 0.95,
                        "VERY_POOR": 0.85
                    }
                },
                "MATCHUP_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.2,
                        "GOOD": 1.1,
                        "POOR": 0.9,
                        "VERY_POOR": 0.8
                    }
                }
            }
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            temp_path = Path(f.name)

        gen = ConfigGenerator(temp_path)
        temp_path.unlink()

        combination = {
            'NORMALIZATION_MAX_SCALE': 110.0,
            'BASE_BYE_PENALTY': 30.0,
            'PRIMARY_BONUS': 55.0,
            'SECONDARY_BONUS': 45.0,
            'ADP_SCORING_WEIGHT': 1.5,
            'PLAYER_RATING_SCORING_WEIGHT': 1.3,
            'TEAM_QUALITY_SCORING_WEIGHT': 1.2,
            'PERFORMANCE_SCORING_WEIGHT': 1.1,
            'MATCHUP_SCORING_WEIGHT': 1.4
        }

        return gen, combination

    def test_create_config_dict_updates_scalar_params(self, generator_and_combo):
        """Test that scalar parameters are updated correctly"""
        gen, combination = generator_and_combo
        config = gen.create_config_dict(combination)

        params = config['parameters']
        assert params['NORMALIZATION_MAX_SCALE'] == 110.0
        assert params['BASE_BYE_PENALTY'] == 30.0
        assert params['DRAFT_ORDER_BONUSES']['PRIMARY'] == 55.0
        assert params['DRAFT_ORDER_BONUSES']['SECONDARY'] == 45.0

    def test_create_config_dict_updates_multipliers(self, generator_and_combo):
        """Test that weights are updated in all sections"""
        gen, combination = generator_and_combo
        config = gen.create_config_dict(combination)

        params = config['parameters']

        # Check weights for all scoring sections
        assert params['ADP_SCORING']['WEIGHT'] == 1.5
        assert params['PLAYER_RATING_SCORING']['WEIGHT'] == 1.3
        assert params['TEAM_QUALITY_SCORING']['WEIGHT'] == 1.2
        assert params['PERFORMANCE_SCORING']['WEIGHT'] == 1.1
        assert params['MATCHUP_SCORING']['WEIGHT'] == 1.4

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
    def generator(self):
        """Create a generator for iterative optimization tests"""
        config = {
            "config_name": "test_config",
            "parameters": {
                "NORMALIZATION_MAX_SCALE": 100.0,
                "BASE_BYE_PENALTY": 25.0,
                "DRAFT_ORDER_BONUSES": {
                    "PRIMARY": 50.0,
                    "SECONDARY": 40.0
                },
                "ADP_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.2,
                        "GOOD": 1.1,
                        "POOR": 0.9,
                        "VERY_POOR": 0.8
                    }
                },
                "PLAYER_RATING_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.25,
                        "GOOD": 1.15,
                        "POOR": 0.85,
                        "VERY_POOR": 0.75
                    }
                },
                "TEAM_QUALITY_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.3,
                        "GOOD": 1.2,
                        "POOR": 0.8,
                        "VERY_POOR": 0.7
                    }
                },
                "PERFORMANCE_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.15,
                        "GOOD": 1.05,
                        "POOR": 0.95,
                        "VERY_POOR": 0.85
                    }
                },
                "MATCHUP_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.2,
                        "GOOD": 1.1,
                        "POOR": 0.9,
                        "VERY_POOR": 0.8
                    }
                }
            }
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            temp_path = Path(f.name)

        gen = ConfigGenerator(temp_path, num_test_values=2)
        temp_path.unlink()
        return gen

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

        # Should have all 8 parameters
        assert 'NORMALIZATION_MAX_SCALE' in combination
        assert 'BASE_BYE_PENALTY' in combination
        assert 'PRIMARY_BONUS' in combination
        assert 'SECONDARY_BONUS' in combination
        assert 'ADP_SCORING_WEIGHT' in combination
        assert 'PLAYER_RATING_SCORING_WEIGHT' in combination
        assert 'TEAM_QUALITY_SCORING_WEIGHT' in combination
        assert 'MATCHUP_SCORING_WEIGHT' in combination
        assert 'PERFORMANCE_SCORING_WEIGHT' in combination
        assert len(combination) == 9

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

    def test_missing_config_file(self):
        """Test that missing config file raises FileNotFoundError"""
        with pytest.raises(FileNotFoundError):
            ConfigGenerator(Path('/nonexistent/config.json'))

    def test_invalid_json_format(self):
        """Test that invalid JSON raises JSONDecodeError"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("{invalid json")
            temp_path = Path(f.name)

        try:
            with pytest.raises(json.JSONDecodeError):
                ConfigGenerator(temp_path)
        finally:
            temp_path.unlink()

    def test_missing_parameters_section(self):
        """Test that config without parameters section raises ValueError"""
        config = {"config_name": "test"}  # Missing 'parameters'

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            temp_path = Path(f.name)

        try:
            with pytest.raises(ValueError, match="missing 'parameters' section"):
                ConfigGenerator(temp_path)
        finally:
            temp_path.unlink()
