"""
Unit tests for simulation configuration.

Tests simulation config settings and validates baseline/template parameter files.
"""

import unittest
import sys
import os
from pathlib import Path

# Add parent directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from shared_files.configs import simulation_config as sim_config
from draft_helper.simulation.parameter_loader import load_parameter_config, REQUIRED_PARAMETERS


class TestSimulationConfig(unittest.TestCase):
    """Test simulation configuration"""

    def test_simulation_settings_valid(self):
        """Verify simulation settings are properly configured"""
        self.assertGreater(sim_config.SIMULATIONS_PER_CONFIG, 0)
        self.assertGreater(sim_config.PRELIMINARY_SIMULATIONS_PER_CONFIG, 0)
        self.assertGreater(sim_config.TOP_CONFIGS_PERCENTAGE, 0)
        self.assertLessEqual(sim_config.TOP_CONFIGS_PERCENTAGE, 1.0)

    def test_league_settings_valid(self):
        """Verify league settings are properly configured"""
        self.assertGreater(sim_config.LEAGUE_SIZE, 0)
        self.assertGreater(sim_config.NFL_SEASON_WEEKS, 0)
        self.assertGreaterEqual(sim_config.HUMAN_ERROR_RATE, 0)
        self.assertLessEqual(sim_config.HUMAN_ERROR_RATE, 1.0)

    def test_team_strategies_match_league_size(self):
        """Verify team strategies sum to league size"""
        total_teams = sum(sim_config.TEAM_STRATEGIES.values())
        self.assertEqual(
            total_teams, sim_config.LEAGUE_SIZE,
            f"Team strategies sum ({total_teams}) must equal LEAGUE_SIZE ({sim_config.LEAGUE_SIZE})"
        )

    def test_simulation_config_validation(self):
        """Test that config validation function works"""
        # Should not raise exception
        sim_config.validate_simulation_config()

    def test_baseline_parameters_exist(self):
        """Verify baseline_parameters.json exists and is valid"""
        params_dir = Path(__file__).parent / "parameters"
        baseline_path = params_dir / "baseline_parameters.json"

        self.assertTrue(
            baseline_path.exists(),
            f"baseline_parameters.json not found at {baseline_path}"
        )

        # Should load without errors
        config = load_parameter_config(str(baseline_path))
        self.assertEqual(config['config_name'], 'baseline')

    def test_template_parameters_exist(self):
        """Verify parameter_template.json exists and is valid"""
        params_dir = Path(__file__).parent / "parameters"
        template_path = params_dir / "parameter_template.json"

        self.assertTrue(
            template_path.exists(),
            f"parameter_template.json not found at {template_path}"
        )

        # Should load without errors
        config = load_parameter_config(str(template_path))
        self.assertEqual(config['config_name'], 'template')

    def test_baseline_has_all_required_parameters(self):
        """Verify baseline_parameters.json has all 20 required parameters"""
        params_dir = Path(__file__).parent / "parameters"
        baseline_path = params_dir / "baseline_parameters.json"

        if baseline_path.exists():
            config = load_parameter_config(str(baseline_path))

            self.assertEqual(
                len(config['parameters']), len(REQUIRED_PARAMETERS),
                f"Baseline should have {len(REQUIRED_PARAMETERS)} parameters"
            )

            for param in REQUIRED_PARAMETERS:
                self.assertIn(
                    param, config['parameters'],
                    f"Required parameter {param} missing from baseline"
                )

    def test_baseline_parameters_single_values(self):
        """Verify baseline parameters have single values (not ranges)"""
        params_dir = Path(__file__).parent / "parameters"
        baseline_path = params_dir / "parameters" / "baseline_parameters.json"

        if baseline_path.exists():
            config = load_parameter_config(str(baseline_path))

            for param_name, values in config['parameters'].items():
                self.assertEqual(
                    len(values), 1,
                    f"Baseline parameter {param_name} should have exactly 1 value"
                )

    def test_template_parameters_two_values(self):
        """Verify template parameters have two values for testing"""
        params_dir = Path(__file__).parent / "parameters"
        template_path = params_dir / "parameter_template.json"

        if template_path.exists():
            config = load_parameter_config(str(template_path))

            for param_name, values in config['parameters'].items():
                self.assertEqual(
                    len(values), 2,
                    f"Template parameter {param_name} should have exactly 2 values"
                )

    def test_parameter_values_reasonable(self):
        """Verify parameter values in baseline are in reasonable ranges"""
        params_dir = Path(__file__).parent / "parameters"
        baseline_path = params_dir / "baseline_parameters.json"

        if not baseline_path.exists():
            self.skipTest("baseline_parameters.json not found")

        config = load_parameter_config(str(baseline_path))

        # Define reasonable ranges for validation
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
            if param_name in config['parameters']:
                values = config['parameters'][param_name]
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


if __name__ == '__main__':
    unittest.main()
