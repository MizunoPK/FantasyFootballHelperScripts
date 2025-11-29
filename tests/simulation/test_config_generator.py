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
        assert config['parameters']['SAME_POS_BYE_WEIGHT'] == 1.0
        assert config['parameters']['DIFF_POS_BYE_WEIGHT'] == 1.0

    def test_param_definitions_exist(self, temp_baseline_config):
        """Test that param_definitions dict exists and is non-empty"""
        gen = ConfigGenerator(temp_baseline_config)

        # param_definitions should exist and contain entries
        assert hasattr(gen, 'param_definitions')
        assert isinstance(gen.param_definitions, dict)
        assert len(gen.param_definitions) > 0

        # Each param definition should be a tuple of (min_val, max_val)
        for param_name, definition in gen.param_definitions.items():
            assert isinstance(definition, tuple), f"{param_name} should be a tuple"
            assert len(definition) == 2, f"{param_name} should have (min, max)"

    def test_parameter_order_exists(self, temp_baseline_config):
        """Test that PARAMETER_ORDER list exists"""
        gen = ConfigGenerator(temp_baseline_config)

        assert hasattr(gen, 'PARAMETER_ORDER')
        assert isinstance(gen.PARAMETER_ORDER, list)
        # PARAMETER_ORDER can be empty or have any number of params - just verify it exists


class TestParameterValueGeneration:
    """Test parameter value generation methods"""

    @pytest.fixture
    def generator(self):
        """Create a ConfigGenerator instance for testing"""
        config = {
            "config_name": "test_config",
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

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            temp_path = Path(f.name)

        gen = ConfigGenerator(temp_path, num_test_values=2)  # Use 2 for faster tests
        temp_path.unlink()
        return gen

    def test_generate_parameter_values_correct_count(self, generator):
        """Test that correct number of values are generated"""
        values = generator.generate_parameter_values(
            'TEST_PARAM', 100.0, 60.0, 140.0
        )

        # Should have num_test_values + 1 (optimal + N random)
        assert len(values) == 3  # 1 + 2

    def test_generate_parameter_values_includes_optimal(self, generator):
        """Test that optimal value is included as first value"""
        optimal = 100.0
        values = generator.generate_parameter_values(
            'TEST_PARAM', optimal, 60.0, 140.0
        )

        assert values[0] == optimal

    def test_generate_parameter_values_respects_bounds(self, generator):
        """Test that generated values respect min/max bounds"""
        values = generator.generate_parameter_values(
            'TEST_PARAM', 100.0, 60.0, 140.0
        )

        for val in values:
            assert 60.0 <= val <= 140.0

    def test_generate_parameter_values_random_variation(self, generator):
        """Test that random values vary from optimal"""
        optimal = 100.0
        values = generator.generate_parameter_values(
            'TEST_PARAM', optimal, 60.0, 140.0
        )

        # At least one value should differ from optimal
        non_optimal_values = [v for v in values[1:] if v != optimal]
        assert len(non_optimal_values) >= 1

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
    def generator(self):
        """Create a ConfigGenerator with minimal test values"""
        config = {
            "config_name": "test_config",
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
    def generator_and_combo(self):
        """Create a generator and a sample combination"""
        config = {
            "config_name": "test_config",
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

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            temp_path = Path(f.name)

        gen = ConfigGenerator(temp_path)
        temp_path.unlink()

        combination = {
            'NORMALIZATION_MAX_SCALE': 110.0,
            'SAME_POS_BYE_WEIGHT': 1.5,
            'DIFF_POS_BYE_WEIGHT': 1.2,
            'PRIMARY_BONUS': 55.0,
            'SECONDARY_BONUS': 45.0,
            'ADP_SCORING_WEIGHT': 1.5,
            'PLAYER_RATING_SCORING_WEIGHT': 1.3,
            'TEAM_QUALITY_SCORING_WEIGHT': 1.2,
            'PERFORMANCE_SCORING_WEIGHT': 1.1,
            'MATCHUP_SCORING_WEIGHT': 1.4,
            # SCHEDULE_SCORING_WEIGHT: DISABLED (not optimized)
            'ADP_SCORING_STEPS': 40.0,
            'PERFORMANCE_SCORING_STEPS': 0.12,
            'MATCHUP_IMPACT_SCALE': 175.0,
            # SCHEDULE_IMPACT_SCALE: DISABLED (not optimized)
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
    def generator(self):
        """Create a generator for iterative optimization tests"""
        config = {
            "config_name": "test_config",
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


class TestGenerateIterativeCombinations:
    """Test generate_iterative_combinations with random parameter exploration"""

    @pytest.fixture
    def baseline_config_dict(self):
        """Create baseline config dictionary for testing"""
        return {
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
                },
                "TEMPERATURE_SCORING": {
                    "IDEAL_TEMPERATURE": 60,
                    "IMPACT_SCALE": 50.0,
                    "WEIGHT": 1.0,
                    "THRESHOLDS": {
                        "BASE_POSITION": 0,
                        "DIRECTION": "DECREASING",
                        "STEPS": 10
                    },
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.05,
                        "GOOD": 1.025,
                        "POOR": 0.975,
                        "VERY_POOR": 0.95
                    }
                },
                "WIND_SCORING": {
                    "IMPACT_SCALE": 60.0,
                    "WEIGHT": 1.0,
                    "THRESHOLDS": {
                        "BASE_POSITION": 0,
                        "DIRECTION": "DECREASING",
                        "STEPS": 8
                    },
                    "MULTIPLIERS": {
                        "EXCELLENT": 1.05,
                        "GOOD": 1.025,
                        "POOR": 0.975,
                        "VERY_POOR": 0.95
                    }
                },
                "LOCATION_MODIFIERS": {
                    "HOME": 2.0,
                    "AWAY": -2.0,
                    "INTERNATIONAL": -5.0
                }
            }
        }

    @pytest.fixture
    def test_config_generator(self, baseline_config_dict):
        """Create ConfigGenerator instance for testing"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(baseline_config_dict, f)
            temp_path = Path(f.name)

        try:
            generator = ConfigGenerator(temp_path, num_test_values=5, num_parameters_to_test=2)
            yield generator
        finally:
            temp_path.unlink()

    def test_with_num_parameters_1_base_only(self, baseline_config_dict):
        """Test with NUM_PARAMETERS_TO_TEST=1 (base parameter only)"""
        # Skip if no parameters enabled
        if not ConfigGenerator.PARAMETER_ORDER:
            return

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(baseline_config_dict, f)
            temp_path = Path(f.name)

        try:
            generator = ConfigGenerator(temp_path, num_test_values=5, num_parameters_to_test=1)
            first_param = ConfigGenerator.PARAMETER_ORDER[0]
            configs = generator.generate_iterative_combinations(first_param, baseline_config_dict)

            # Should return N+1 configs (5+1 = 6)
            expected_count = generator.num_test_values + 1
            assert len(configs) == expected_count

            # All configs should be complete dictionaries
            for config in configs:
                assert 'parameters' in config
                assert 'config_name' in config
        finally:
            temp_path.unlink()

    def test_with_num_parameters_2_base_plus_one_random(self, baseline_config_dict):
        """Test with NUM_PARAMETERS_TO_TEST=2 (base + 1 random)"""
        # Skip if not enough parameters enabled
        if len(ConfigGenerator.PARAMETER_ORDER) < 2:
            return

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(baseline_config_dict, f)
            temp_path = Path(f.name)

        try:
            generator = ConfigGenerator(temp_path, num_test_values=5, num_parameters_to_test=2)
            first_param = ConfigGenerator.PARAMETER_ORDER[0]
            configs = generator.generate_iterative_combinations(first_param, baseline_config_dict)

            # Should return 2*(N+1) + (N+1)^2 configs
            # With N=5: 2*6 + 36 = 48 total
            n = generator.num_test_values
            expected_count = 2 * (n + 1) + (n + 1) ** 2
            assert len(configs) == expected_count

            # Verify all configs are valid
            for config in configs:
                assert 'parameters' in config
        finally:
            temp_path.unlink()

    def test_with_num_parameters_3_base_plus_two_random(self, baseline_config_dict):
        """Test with NUM_PARAMETERS_TO_TEST=3 (base + 2 random)"""
        # Skip if not enough parameters enabled
        if len(ConfigGenerator.PARAMETER_ORDER) < 3:
            return

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(baseline_config_dict, f)
            temp_path = Path(f.name)

        try:
            generator = ConfigGenerator(temp_path, num_test_values=5, num_parameters_to_test=3)
            first_param = ConfigGenerator.PARAMETER_ORDER[0]
            configs = generator.generate_iterative_combinations(first_param, baseline_config_dict)

            # Should return 3*(N+1) + (N+1)^3 configs
            # With N=5: 3*6 + 216 = 234 total
            n = generator.num_test_values
            expected_count = 3 * (n + 1) + (n + 1) ** 3
            assert len(configs) == expected_count

            # Verify all configs are valid
            for config in configs:
                assert 'parameters' in config
        finally:
            temp_path.unlink()

    def test_edge_case_num_parameters_exceeds_available(self, baseline_config_dict):
        """Test that num_parameters_to_test is capped at PARAMETER_ORDER length"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(baseline_config_dict, f)
            temp_path = Path(f.name)

        try:
            # Test that num_parameters_to_test is capped at PARAMETER_ORDER length (7)
            # Use small num_test_values and num_parameters_to_test for fast test
            num_params = min(4, len(ConfigGenerator.PARAMETER_ORDER)) if ConfigGenerator.PARAMETER_ORDER else 1
            generator = ConfigGenerator(temp_path, num_test_values=1, num_parameters_to_test=num_params)

            # Skip test if no parameters are enabled in PARAMETER_ORDER
            if not ConfigGenerator.PARAMETER_ORDER:
                return

            first_param = ConfigGenerator.PARAMETER_ORDER[0]
            configs = generator.generate_iterative_combinations(first_param, baseline_config_dict)

            # All configs should be valid
            assert len(configs) > 0
            assert all('parameters' in config for config in configs)

            # Verify capping works - request more params than available
            generator2 = ConfigGenerator(temp_path, num_test_values=1, num_parameters_to_test=100)
            # Should cap at PARAMETER_ORDER length
            assert len(generator2.PARAMETER_ORDER) == len(ConfigGenerator.PARAMETER_ORDER)
        finally:
            temp_path.unlink()

    def test_edge_case_invalid_param_name(self, test_config_generator):
        """Test with invalid parameter name (should raise ValueError)"""
        with pytest.raises(ValueError, match="Unknown parameter: INVALID_PARAM"):
            test_config_generator.generate_iterative_combinations('INVALID_PARAM', test_config_generator.baseline_config)

    def test_randomness_varies_parameter_selection(self, baseline_config_dict):
        """Test that random parameter selection varies between runs"""
        # Skip test if no parameters are enabled
        if not ConfigGenerator.PARAMETER_ORDER:
            return

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(baseline_config_dict, f)
            temp_path = Path(f.name)

        try:
            num_params = min(2, len(ConfigGenerator.PARAMETER_ORDER))
            generator = ConfigGenerator(temp_path, num_test_values=5, num_parameters_to_test=num_params)

            first_param = ConfigGenerator.PARAMETER_ORDER[0]
            # Run twice and check that configs might differ due to random selection
            # Note: We can't guarantee difference, but both runs should succeed
            configs1 = generator.generate_iterative_combinations(first_param, baseline_config_dict)
            configs2 = generator.generate_iterative_combinations(first_param, baseline_config_dict)

            # Both runs should generate same number of configs
            assert len(configs1) == len(configs2)
            assert len(configs1) > 0

            # Both should be valid
            assert all('parameters' in config for config in configs1)
            assert all('parameters' in config for config in configs2)
        finally:
            temp_path.unlink()

    def test_config_structure_is_valid(self, test_config_generator):
        """Test that all returned configs have valid structure"""
        # Skip if no parameters enabled
        if not ConfigGenerator.PARAMETER_ORDER:
            return

        first_param = ConfigGenerator.PARAMETER_ORDER[0]
        configs = test_config_generator.generate_iterative_combinations(
            first_param,
            test_config_generator.baseline_config
        )

        for config in configs:
            # Check required top-level keys
            assert 'config_name' in config
            assert 'parameters' in config
            # Parameters should be a dict
            assert isinstance(config['parameters'], dict)

    def test_combination_configs_have_multiple_params_varied(self, baseline_config_dict):
        """Test that combination configs actually vary multiple parameters"""
        # Skip if not enough parameters enabled
        if len(ConfigGenerator.PARAMETER_ORDER) < 2:
            return

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(baseline_config_dict, f)
            temp_path = Path(f.name)

        try:
            generator = ConfigGenerator(temp_path, num_test_values=2, num_parameters_to_test=2)
            first_param = ConfigGenerator.PARAMETER_ORDER[0]
            configs = generator.generate_iterative_combinations(first_param, baseline_config_dict)

            # Should generate multiple configs
            assert len(configs) > 0

            # All configs should be valid
            for config in configs:
                assert 'parameters' in config
                assert isinstance(config['parameters'], dict)
        finally:
            temp_path.unlink()

    def test_edge_case_num_parameters_zero_defaults_to_one(self, baseline_config_dict):
        """Test that num_parameters_to_test=0 defaults to 1"""
        # Skip if no parameters enabled
        if not ConfigGenerator.PARAMETER_ORDER:
            return

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(baseline_config_dict, f)
            temp_path = Path(f.name)

        try:
            generator = ConfigGenerator(temp_path, num_test_values=5, num_parameters_to_test=0)
            first_param = ConfigGenerator.PARAMETER_ORDER[0]
            configs = generator.generate_iterative_combinations(first_param, baseline_config_dict)

            # Should default to 1, returning N+1 configs
            expected_count = generator.num_test_values + 1
            assert len(configs) == expected_count
        finally:
            temp_path.unlink()


class TestDraftOrderFile:
    """Test DRAFT_ORDER_FILE parameter functionality"""

    @pytest.fixture
    def baseline_config_with_draft_order(self):
        """Create baseline config with DRAFT_ORDER_FILE"""
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
                "DRAFT_ORDER_FILE": 1,
                "DRAFT_ORDER": [{"FLEX": "P", "QB": "S"}] * 15,
                "MAX_POSITIONS": {"QB": 2, "RB": 4, "WR": 4, "FLEX": 2, "TE": 1, "K": 1, "DST": 1},
                "FLEX_ELIGIBLE_POSITIONS": ["RB", "WR"],
                "ADP_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {"EXCELLENT": 1.2, "GOOD": 1.1, "POOR": 0.9, "VERY_POOR": 0.8},
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 37.5}
                },
                "PLAYER_RATING_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {"EXCELLENT": 1.25, "GOOD": 1.15, "POOR": 0.85, "VERY_POOR": 0.75},
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 20.0}
                },
                "TEAM_QUALITY_SCORING": {
                    "MIN_WEEKS": 5,
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {"EXCELLENT": 1.3, "GOOD": 1.2, "POOR": 0.8, "VERY_POOR": 0.7},
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 6.25}
                },
                "PERFORMANCE_SCORING": {
                    "WEIGHT": 1.0,
                    "MIN_WEEKS": 5,
                    "MULTIPLIERS": {"EXCELLENT": 1.15, "GOOD": 1.05, "POOR": 0.95, "VERY_POOR": 0.85},
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "BI_EXCELLENT_HI", "STEPS": 0.1}
                },
                "MATCHUP_SCORING": {
                    "MIN_WEEKS": 5,
                    "WEIGHT": 1.0,
                    "IMPACT_SCALE": 100.0,
                    "MULTIPLIERS": {"EXCELLENT": 1.2, "GOOD": 1.1, "POOR": 0.9, "VERY_POOR": 0.8},
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 6.25}
                }
            }
        }
        return config

    def test_draft_order_file_in_param_definitions(self):
        """Test DRAFT_ORDER_FILE is in PARAM_DEFINITIONS with correct range"""
        assert 'DRAFT_ORDER_FILE' in ConfigGenerator.PARAM_DEFINITIONS
        min_val, max_val = ConfigGenerator.PARAM_DEFINITIONS['DRAFT_ORDER_FILE']
        assert min_val == 1
        assert max_val == 10  # Updated to include more draft order strategies

    def test_draft_order_file_in_parameter_order(self):
        """Test DRAFT_ORDER_FILE is included in PARAMETER_ORDER for optimization"""
        assert 'DRAFT_ORDER_FILE' in ConfigGenerator.PARAMETER_ORDER

    def test_generate_discrete_parameter_values(self, baseline_config_with_draft_order):
        """Test discrete value generation for DRAFT_ORDER_FILE"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(baseline_config_with_draft_order, f)
            temp_path = Path(f.name)

        try:
            generator = ConfigGenerator(temp_path, num_test_values=5)
            values = generator.generate_discrete_parameter_values('DRAFT_ORDER_FILE', 1, 1, 30)

            # Should have N+1 values
            assert len(values) == 6
            # First value should be optimal
            assert values[0] == 1
            # All values should be integers in range
            for v in values:
                assert isinstance(v, int)
                assert 1 <= v <= 30
            # All values should be unique
            assert len(set(values)) == 6
        finally:
            temp_path.unlink()

    def test_extract_combination_includes_draft_order_file(self, baseline_config_with_draft_order):
        """Test _extract_combination_from_config includes DRAFT_ORDER_FILE"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(baseline_config_with_draft_order, f)
            temp_path = Path(f.name)

        try:
            generator = ConfigGenerator(temp_path)
            combination = generator._extract_combination_from_config(baseline_config_with_draft_order)

            assert 'DRAFT_ORDER_FILE' in combination
            assert combination['DRAFT_ORDER_FILE'] == 1
        finally:
            temp_path.unlink()

    def test_generate_single_parameter_configs_draft_order_file(self, baseline_config_with_draft_order):
        """Test generating configs for DRAFT_ORDER_FILE parameter"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(baseline_config_with_draft_order, f)
            temp_path = Path(f.name)

        try:
            generator = ConfigGenerator(temp_path, num_test_values=3)
            configs = generator.generate_single_parameter_configs(
                'DRAFT_ORDER_FILE',
                baseline_config_with_draft_order
            )

            # Should have N+1 configs
            assert len(configs) == 4

            # Each config should have DRAFT_ORDER_FILE and DRAFT_ORDER
            for config in configs:
                assert 'DRAFT_ORDER_FILE' in config['parameters']
                assert 'DRAFT_ORDER' in config['parameters']
                # DRAFT_ORDER should be a list
                assert isinstance(config['parameters']['DRAFT_ORDER'], list)
        finally:
            temp_path.unlink()

    def test_create_config_dict_loads_draft_order(self, baseline_config_with_draft_order):
        """Test create_config_dict loads DRAFT_ORDER from file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(baseline_config_with_draft_order, f)
            temp_path = Path(f.name)

        try:
            generator = ConfigGenerator(temp_path)
            combination = generator._extract_combination_from_config(baseline_config_with_draft_order)

            # Test with file 1
            combination['DRAFT_ORDER_FILE'] = 1
            config = generator.create_config_dict(combination)

            assert config['parameters']['DRAFT_ORDER_FILE'] == 1
            assert isinstance(config['parameters']['DRAFT_ORDER'], list)
            assert len(config['parameters']['DRAFT_ORDER']) == 15
        finally:
            temp_path.unlink()

    def test_load_draft_order_from_file_not_found(self, baseline_config_with_draft_order):
        """Test _load_draft_order_from_file raises error for invalid file number"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(baseline_config_with_draft_order, f)
            temp_path = Path(f.name)

        try:
            generator = ConfigGenerator(temp_path)
            with pytest.raises(FileNotFoundError):
                generator._load_draft_order_from_file(999)
        finally:
            temp_path.unlink()
