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
        """Test that all parameter definitions are present"""
        gen = ConfigGenerator(temp_baseline_config)

        assert 'NORMALIZATION_MAX_SCALE' in gen.param_definitions
        assert 'SAME_POS_BYE_WEIGHT' in gen.param_definitions
        assert 'DIFF_POS_BYE_WEIGHT' in gen.param_definitions
        assert 'PRIMARY_BONUS' in gen.param_definitions
        assert 'SECONDARY_BONUS' in gen.param_definitions
        assert 'ADP_SCORING_WEIGHT' in gen.param_definitions
        assert 'PLAYER_RATING_SCORING_WEIGHT' in gen.param_definitions
        assert 'MATCHUP_SCORING_WEIGHT' in gen.param_definitions
        assert 'PERFORMANCE_SCORING_WEIGHT' in gen.param_definitions
        assert 'MATCHUP_IMPACT_SCALE' in gen.param_definitions
        # SCHEDULE_IMPACT_SCALE disabled
        # assert 'SCHEDULE_IMPACT_SCALE' in gen.param_definitions

    def test_parameter_order_exists(self, temp_baseline_config):
        """Test that PARAMETER_ORDER list exists and has expected length"""
        gen = ConfigGenerator(temp_baseline_config)

        assert hasattr(gen, 'PARAMETER_ORDER')
        assert len(gen.PARAMETER_ORDER) == 16  # 5 scalars + 5 weights + 3 MIN_WEEKS + 2 threshold STEPS + 1 IMPACT_SCALE (SCHEDULE disabled, some STEPS disabled)


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
        """Test that value sets are generated for all parameters"""
        value_sets = generator.generate_all_parameter_value_sets()

        # Should have 5 scalar + 5 weight + 2 MIN_WEEKS + 2 threshold STEPS + 1 IMPACT_SCALE
        assert len(value_sets) == 16  # Only ADP and PERFORMANCE have STEPS; only MATCHUP has IMPACT_SCALE; 3 MIN_WEEKS (others disabled)
        assert 'NORMALIZATION_MAX_SCALE' in value_sets
        assert 'SAME_POS_BYE_WEIGHT' in value_sets
        assert 'DIFF_POS_BYE_WEIGHT' in value_sets
        assert 'PRIMARY_BONUS' in value_sets
        assert 'SECONDARY_BONUS' in value_sets
        assert 'ADP_SCORING_WEIGHT' in value_sets
        assert 'PLAYER_RATING_SCORING_WEIGHT' in value_sets
        assert 'MATCHUP_SCORING_WEIGHT' in value_sets
        assert 'PERFORMANCE_SCORING_WEIGHT' in value_sets
        # SCHEDULE disabled
        # assert 'SCHEDULE_SCORING_WEIGHT' in value_sets
        assert 'MATCHUP_IMPACT_SCALE' in value_sets
        # assert 'SCHEDULE_IMPACT_SCALE' in value_sets

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

        # Verify value sets exist for all expected parameters
        assert len(value_sets) == 16  # 5 scalars + 5 weights + 3 MIN_WEEKS + 2 threshold STEPS + 1 IMPACT_SCALE (only ADP, PERFORMANCE, MATCHUP optimized)
        assert 'NORMALIZATION_MAX_SCALE' in value_sets
        assert 'ADP_SCORING_WEIGHT' in value_sets
        # SCHEDULE disabled
        # assert 'SCHEDULE_SCORING_WEIGHT' in value_sets

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
        assert 'SAME_POS_BYE_WEIGHT' in test_combo
        assert 'DIFF_POS_BYE_WEIGHT' in test_combo
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

        # Should have all parameters (5 scalar + 5 weights + 5 threshold STEPS + 1 IMPACT_SCALE)
        assert 'NORMALIZATION_MAX_SCALE' in combination
        assert 'SAME_POS_BYE_WEIGHT' in combination
        assert 'DIFF_POS_BYE_WEIGHT' in combination
        assert 'PRIMARY_BONUS' in combination
        assert 'SECONDARY_BONUS' in combination
        assert 'ADP_SCORING_WEIGHT' in combination
        assert 'PLAYER_RATING_SCORING_WEIGHT' in combination
        assert 'TEAM_QUALITY_SCORING_WEIGHT' in combination
        assert 'MATCHUP_SCORING_WEIGHT' in combination
        assert 'PERFORMANCE_SCORING_WEIGHT' in combination
        # SCHEDULE disabled
        # assert 'SCHEDULE_SCORING_WEIGHT' in combination
        assert 'ADP_SCORING_STEPS' in combination
        assert 'PLAYER_RATING_SCORING_STEPS' in combination
        assert 'TEAM_QUALITY_SCORING_STEPS' in combination
        assert 'PERFORMANCE_SCORING_STEPS' in combination
        assert 'MATCHUP_SCORING_STEPS' in combination
        assert 'MATCHUP_IMPACT_SCALE' in combination
        # assert 'SCHEDULE_IMPACT_SCALE' in combination
        assert len(combination) == 19  # 5 scalars + 5 weights + 3 MIN_WEEKS + 5 STEPS + 1 IMPACT_SCALE

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
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(baseline_config_dict, f)
            temp_path = Path(f.name)

        try:
            generator = ConfigGenerator(temp_path, num_test_values=5, num_parameters_to_test=1)
            configs = generator.generate_iterative_combinations('NORMALIZATION_MAX_SCALE', baseline_config_dict)

            # Should return N+1 configs (5+1 = 6)
            assert len(configs) == 6

            # All configs should be complete dictionaries
            for config in configs:
                assert 'parameters' in config
                assert 'config_name' in config
        finally:
            temp_path.unlink()

    def test_with_num_parameters_2_base_plus_one_random(self, baseline_config_dict):
        """Test with NUM_PARAMETERS_TO_TEST=2 (base + 1 random)"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(baseline_config_dict, f)
            temp_path = Path(f.name)

        try:
            generator = ConfigGenerator(temp_path, num_test_values=5, num_parameters_to_test=2)
            configs = generator.generate_iterative_combinations('NORMALIZATION_MAX_SCALE', baseline_config_dict)

            # Should return 2*(N+1) + (N+1)^2 configs
            # With N=5: 2*6 + 36 = 48 total
            assert len(configs) == 48

            # Verify all configs are valid
            for config in configs:
                assert 'parameters' in config
                assert 'NORMALIZATION_MAX_SCALE' in config['parameters']
        finally:
            temp_path.unlink()

    def test_with_num_parameters_3_base_plus_two_random(self, baseline_config_dict):
        """Test with NUM_PARAMETERS_TO_TEST=3 (base + 2 random)"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(baseline_config_dict, f)
            temp_path = Path(f.name)

        try:
            generator = ConfigGenerator(temp_path, num_test_values=5, num_parameters_to_test=3)
            configs = generator.generate_iterative_combinations('NORMALIZATION_MAX_SCALE', baseline_config_dict)

            # Should return 3*(N+1) + (N+1)^3 configs
            # With N=5: 3*6 + 216 = 234 total
            assert len(configs) == 234

            # Verify all configs are valid
            for config in configs:
                assert 'parameters' in config
        finally:
            temp_path.unlink()

    def test_edge_case_num_parameters_exceeds_available(self, baseline_config_dict):
        """Test with NUM_PARAMETERS_TO_TEST > 13 (should cap at 13)"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(baseline_config_dict, f)
            temp_path = Path(f.name)

        try:
            # Use num_test_values=1 to keep cartesian product small (2^16 = 65,536 configs)
            generator = ConfigGenerator(temp_path, num_test_values=1, num_parameters_to_test=20)

            # Should cap at 16 parameters (PARAMETER_ORDER length)
            configs = generator.generate_iterative_combinations('NORMALIZATION_MAX_SCALE', baseline_config_dict)

            # Should generate configs (capped at 16 params)
            # Base parameter: 2 configs
            # Random parameters (15): 30 configs (15 * 2)
            # Combinations: 2^16 = 65,536
            # Total: 65,568 configs
            assert len(configs) == 65568
            assert all('parameters' in config for config in configs)
        finally:
            temp_path.unlink()

    def test_edge_case_invalid_param_name(self, test_config_generator):
        """Test with invalid parameter name (should raise ValueError)"""
        with pytest.raises(ValueError, match="Unknown parameter: INVALID_PARAM"):
            test_config_generator.generate_iterative_combinations('INVALID_PARAM', test_config_generator.baseline_config)

    def test_randomness_varies_parameter_selection(self, baseline_config_dict):
        """Test that random parameter selection varies between runs"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(baseline_config_dict, f)
            temp_path = Path(f.name)

        try:
            generator = ConfigGenerator(temp_path, num_test_values=5, num_parameters_to_test=2)

            # Run twice and check that configs might differ due to random selection
            # Note: We can't guarantee difference, but both runs should succeed
            configs1 = generator.generate_iterative_combinations('NORMALIZATION_MAX_SCALE', baseline_config_dict)
            configs2 = generator.generate_iterative_combinations('NORMALIZATION_MAX_SCALE', baseline_config_dict)

            # Both runs should generate same number of configs
            assert len(configs1) == len(configs2) == 48

            # Both should be valid
            assert all('parameters' in config for config in configs1)
            assert all('parameters' in config for config in configs2)
        finally:
            temp_path.unlink()

    def test_config_structure_is_valid(self, test_config_generator):
        """Test that all returned configs have valid structure"""
        configs = test_config_generator.generate_iterative_combinations(
            'SAME_POS_BYE_WEIGHT',
            test_config_generator.baseline_config
        )

        for config in configs:
            # Check required top-level keys
            assert 'config_name' in config
            assert 'parameters' in config

            # Check parameters section has expected keys
            params = config['parameters']
            assert 'NORMALIZATION_MAX_SCALE' in params
            assert 'SAME_POS_BYE_WEIGHT' in params
            assert 'DIFF_POS_BYE_WEIGHT' in params
            assert 'DRAFT_ORDER_BONUSES' in params
            assert 'ADP_SCORING' in params
            assert 'PLAYER_RATING_SCORING' in params
            assert 'PERFORMANCE_SCORING' in params
            assert 'MATCHUP_SCORING' in params

    def test_combination_configs_have_multiple_params_varied(self, baseline_config_dict):
        """Test that combination configs actually vary multiple parameters"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(baseline_config_dict, f)
            temp_path = Path(f.name)

        try:
            generator = ConfigGenerator(temp_path, num_test_values=2, num_parameters_to_test=2)
            configs = generator.generate_iterative_combinations('NORMALIZATION_MAX_SCALE', baseline_config_dict)

            # With N=2: 2*3 + 9 = 15 total configs
            assert len(configs) == 15

            # Last 9 configs should be combinations (cartesian product of 3x3)
            combination_configs = configs[-9:]

            # Extract NORMALIZATION_MAX_SCALE values from combination configs
            norm_values = set()
            for config in combination_configs:
                norm_values.add(config['parameters']['NORMALIZATION_MAX_SCALE'])

            # Should have 3 unique values (N+1 = 3)
            assert len(norm_values) == 3
        finally:
            temp_path.unlink()

    def test_edge_case_num_parameters_zero_defaults_to_one(self, baseline_config_dict):
        """Test that num_parameters_to_test=0 defaults to 1"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(baseline_config_dict, f)
            temp_path = Path(f.name)

        try:
            generator = ConfigGenerator(temp_path, num_test_values=5, num_parameters_to_test=0)
            configs = generator.generate_iterative_combinations('NORMALIZATION_MAX_SCALE', baseline_config_dict)

            # Should default to 1, returning N+1 configs
            assert len(configs) == 6
        finally:
            temp_path.unlink()
