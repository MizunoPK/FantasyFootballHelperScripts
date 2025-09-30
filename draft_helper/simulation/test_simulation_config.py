"""
Unit tests for simulation configuration.

Tests parameter range validation, coverage, and consistency with actual config constants.
"""

import unittest
import sys
import os

# Add parent directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from draft_helper.simulation import config as sim_config
from draft_helper import draft_helper_config as base_config


class TestSimulationConfig(unittest.TestCase):
    """Test simulation configuration parameters"""

    def test_all_parameters_have_two_values(self):
        """Verify all parameters in PARAMETER_RANGES have exactly 2 values"""
        for param_name, values in sim_config.PARAMETER_RANGES.items():
            with self.subTest(parameter=param_name):
                self.assertEqual(
                    len(values), 2,
                    f"{param_name} should have exactly 2 values, got {len(values)}"
                )

    def test_required_parameters_present(self):
        """Verify all required parameters from scoring overhaul are present"""
        required_params = [
            'DRAFT_ORDER_PRIMARY_BONUS',
            'DRAFT_ORDER_SECONDARY_BONUS',
            'NORMALIZATION_MAX_SCALE',
            'BASE_BYE_PENALTY',
            'INJURY_PENALTIES_MEDIUM',
            'INJURY_PENALTIES_HIGH',
            'MATCHUP_EXCELLENT_MULTIPLIER',
            'MATCHUP_GOOD_MULTIPLIER',
            'MATCHUP_NEUTRAL_MULTIPLIER',
            'MATCHUP_POOR_MULTIPLIER',
            'MATCHUP_VERY_POOR_MULTIPLIER',
            'ADP_EXCELLENT_MULTIPLIER',
            'ADP_GOOD_MULTIPLIER',
            'ADP_POOR_MULTIPLIER',
            'PLAYER_RATING_EXCELLENT_MULTIPLIER',
            'PLAYER_RATING_GOOD_MULTIPLIER',
            'PLAYER_RATING_POOR_MULTIPLIER',
            'TEAM_EXCELLENT_MULTIPLIER',
            'TEAM_GOOD_MULTIPLIER',
            'TEAM_POOR_MULTIPLIER',
        ]

        for param in required_params:
            with self.subTest(parameter=param):
                self.assertIn(
                    param, sim_config.PARAMETER_RANGES,
                    f"Required parameter {param} missing from PARAMETER_RANGES"
                )

    def test_parameter_value_ranges_reasonable(self):
        """Verify all parameter values are in reasonable ranges"""
        ranges_validation = {
            'NORMALIZATION_MAX_SCALE': (50, 200),
            'DRAFT_ORDER_PRIMARY_BONUS': (30, 80),
            'DRAFT_ORDER_SECONDARY_BONUS': (15, 40),
            'MATCHUP_EXCELLENT_MULTIPLIER': (1.0, 1.5),
            'MATCHUP_GOOD_MULTIPLIER': (1.0, 1.3),
            'MATCHUP_NEUTRAL_MULTIPLIER': (0.8, 1.2),
            'MATCHUP_POOR_MULTIPLIER': (0.7, 1.0),
            'MATCHUP_VERY_POOR_MULTIPLIER': (0.5, 1.0),
            'INJURY_PENALTIES_MEDIUM': (0, 50),
            'INJURY_PENALTIES_HIGH': (0, 100),
            'BASE_BYE_PENALTY': (0, 50),
            'ADP_EXCELLENT_MULTIPLIER': (1.0, 1.5),
            'ADP_GOOD_MULTIPLIER': (1.0, 1.3),
            'ADP_POOR_MULTIPLIER': (0.5, 1.0),
            'PLAYER_RATING_EXCELLENT_MULTIPLIER': (1.0, 1.5),
            'PLAYER_RATING_GOOD_MULTIPLIER': (1.0, 1.3),
            'PLAYER_RATING_POOR_MULTIPLIER': (0.5, 1.0),
            'TEAM_EXCELLENT_MULTIPLIER': (1.0, 1.3),
            'TEAM_GOOD_MULTIPLIER': (1.0, 1.2),
            'TEAM_POOR_MULTIPLIER': (0.8, 1.0),
        }

        for param_name, (min_val, max_val) in ranges_validation.items():
            if param_name in sim_config.PARAMETER_RANGES:
                values = sim_config.PARAMETER_RANGES[param_name]
                for value in values:
                    with self.subTest(parameter=param_name, value=value):
                        self.assertGreaterEqual(
                            value, min_val,
                            f"{param_name} value {value} below minimum {min_val}"
                        )
                        self.assertLessEqual(
                            value, max_val,
                            f"{param_name} value {value} above maximum {max_val}"
                        )

    def test_first_value_is_baseline(self):
        """Verify first value in each range is baseline/current default"""
        baseline_expectations = {
            'NORMALIZATION_MAX_SCALE': 100,
            'DRAFT_ORDER_PRIMARY_BONUS': 50,
            'DRAFT_ORDER_SECONDARY_BONUS': 25,
            'MATCHUP_EXCELLENT_MULTIPLIER': 1.2,
            'MATCHUP_GOOD_MULTIPLIER': 1.1,
            'MATCHUP_NEUTRAL_MULTIPLIER': 1.0,
            'MATCHUP_POOR_MULTIPLIER': 0.9,
            'MATCHUP_VERY_POOR_MULTIPLIER': 0.8,
        }

        for param_name, expected_baseline in baseline_expectations.items():
            if param_name in sim_config.PARAMETER_RANGES:
                values = sim_config.PARAMETER_RANGES[param_name]
                with self.subTest(parameter=param_name):
                    self.assertEqual(
                        values[0], expected_baseline,
                        f"{param_name} first value should be baseline {expected_baseline}"
                    )

    def test_second_value_more_aggressive(self):
        """Verify second value represents more aggressive/higher impact setting"""
        for param_name, values in sim_config.PARAMETER_RANGES.items():
            with self.subTest(parameter=param_name):
                # For multipliers > 1.0, second should be higher
                # For multipliers < 1.0, second should be higher (closer to 1.0)
                # For penalties, second should be higher
                if 'MULTIPLIER' in param_name:
                    if values[0] >= 1.0:
                        self.assertGreater(
                            values[1], values[0],
                            f"{param_name} second value should be more aggressive"
                        )
                    else:  # penalty multipliers < 1.0
                        self.assertGreater(
                            values[1], values[0],
                            f"{param_name} second value should be less penalizing"
                        )
                elif 'BONUS' in param_name or 'SCALE' in param_name:
                    self.assertGreater(
                        values[1], values[0],
                        f"{param_name} second value should be higher"
                    )

    def test_simulation_config_validation_passes(self):
        """Verify simulation config validation passes with no errors"""
        try:
            sim_config.validate_simulation_config()
        except ValueError as e:
            self.fail(f"Simulation config validation failed: {e}")

    def test_parameter_naming_matches_constants(self):
        """Verify parameter names use uppercase convention matching actual configs"""
        for param_name in sim_config.PARAMETER_RANGES.keys():
            with self.subTest(parameter=param_name):
                self.assertEqual(
                    param_name, param_name.upper(),
                    f"Parameter {param_name} should use uppercase naming"
                )

    def test_draft_order_defaults_align(self):
        """Verify DRAFT_ORDER bonus defaults align with base_config"""
        draft_primary_values = sim_config.PARAMETER_RANGES['DRAFT_ORDER_PRIMARY_BONUS']
        draft_secondary_values = sim_config.PARAMETER_RANGES['DRAFT_ORDER_SECONDARY_BONUS']

        # First values should match base config defaults
        self.assertEqual(
            draft_primary_values[0], base_config.DRAFT_ORDER_PRIMARY_BONUS,
            "DRAFT_ORDER_PRIMARY_BONUS baseline should match base_config"
        )
        self.assertEqual(
            draft_secondary_values[0], base_config.DRAFT_ORDER_SECONDARY_BONUS,
            "DRAFT_ORDER_SECONDARY_BONUS baseline should match base_config"
        )

    def test_no_deprecated_parameters(self):
        """Verify deprecated parameters are not in config"""
        deprecated_params = [
            'PLAYER_RATING_MAX_BOOST',  # Confirmed as mistake in requirements
            'POS_NEEDED_SCORE',         # Deprecated in scoring overhaul
            'PROJECTION_BASE_SCORE',    # Deprecated in scoring overhaul
        ]

        for param in deprecated_params:
            with self.subTest(parameter=param):
                self.assertNotIn(
                    param, sim_config.PARAMETER_RANGES,
                    f"Deprecated parameter {param} should not be in config"
                )

    def test_matchup_multipliers_cover_all_ranges(self):
        """Verify all matchup multiplier ranges are covered"""
        matchup_params = [
            'MATCHUP_EXCELLENT_MULTIPLIER',
            'MATCHUP_GOOD_MULTIPLIER',
            'MATCHUP_NEUTRAL_MULTIPLIER',
            'MATCHUP_POOR_MULTIPLIER',
            'MATCHUP_VERY_POOR_MULTIPLIER',
        ]

        for param in matchup_params:
            with self.subTest(parameter=param):
                self.assertIn(
                    param, sim_config.PARAMETER_RANGES,
                    f"Matchup parameter {param} missing from config"
                )


class TestParameterCombinations(unittest.TestCase):
    """Test parameter combination generation"""

    def test_can_generate_parameter_combinations(self):
        """Verify we can generate valid parameter combinations"""
        from itertools import product

        # Get all parameter names and values
        param_names = list(sim_config.PARAMETER_RANGES.keys())
        param_values = [sim_config.PARAMETER_RANGES[name] for name in param_names]

        # Generate first few combinations
        combinations = list(product(*param_values))

        # Should have 2^20 = 1,048,576 combinations with 20 parameters
        expected_combinations = 2 ** len(param_names)
        self.assertEqual(
            len(combinations), expected_combinations,
            f"Should have {expected_combinations} parameter combinations"
        )

    def test_sample_combination_has_all_parameters(self):
        """Verify a sample parameter combination contains all required keys"""
        from itertools import product

        param_names = list(sim_config.PARAMETER_RANGES.keys())
        param_values = [sim_config.PARAMETER_RANGES[name] for name in param_names]

        # Get first combination
        first_combo = next(product(*param_values))

        # Create config dict
        config_dict = dict(zip(param_names, first_combo))

        # Verify all required parameters present
        required_params = [
            'DRAFT_ORDER_PRIMARY_BONUS',
            'DRAFT_ORDER_SECONDARY_BONUS',
            'NORMALIZATION_MAX_SCALE',
            'BASE_BYE_PENALTY',
        ]

        for param in required_params:
            with self.subTest(parameter=param):
                self.assertIn(param, config_dict, f"Parameter {param} missing from combination")


if __name__ == '__main__':
    unittest.main()
