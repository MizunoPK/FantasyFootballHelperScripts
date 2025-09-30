"""
Unit tests for parameter_loader module
"""

import unittest
import json
import tempfile
import os
from pathlib import Path

from draft_helper.simulation.parameter_loader import (
    load_parameter_config,
    expand_parameter_combinations,
    get_num_combinations,
    load_and_expand_config,
    validate_config_file,
    ParameterConfigError,
    REQUIRED_PARAMETERS
)


class TestParameterLoader(unittest.TestCase):
    """Test parameter loading and validation"""

    def setUp(self):
        """Create temporary directory for test files"""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary files"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def _create_valid_config(self) -> dict:
        """Create a valid configuration dictionary"""
        return {
            "config_name": "test_config",
            "description": "Test configuration",
            "parameters": {param: [1.0, 2.0] for param in REQUIRED_PARAMETERS}
        }

    def _write_config_file(self, config: dict, filename: str = "test_config.json") -> str:
        """Write configuration to a temporary JSON file"""
        filepath = os.path.join(self.test_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(config, f)
        return filepath

    # =========================================================================
    # Test load_parameter_config
    # =========================================================================

    def test_load_valid_config(self):
        """Test loading a valid configuration file"""
        config = self._create_valid_config()
        filepath = self._write_config_file(config)

        loaded = load_parameter_config(filepath)

        self.assertEqual(loaded['config_name'], 'test_config')
        self.assertEqual(loaded['description'], 'Test configuration')
        self.assertEqual(len(loaded['parameters']), len(REQUIRED_PARAMETERS))

    def test_load_nonexistent_file(self):
        """Test loading a file that doesn't exist"""
        with self.assertRaises(ParameterConfigError) as cm:
            load_parameter_config("/nonexistent/file.json")

        self.assertIn("not found", str(cm.exception))

    def test_load_invalid_json(self):
        """Test loading a file with invalid JSON"""
        filepath = os.path.join(self.test_dir, "invalid.json")
        with open(filepath, 'w') as f:
            f.write("{invalid json content")

        with self.assertRaises(ParameterConfigError) as cm:
            load_parameter_config(filepath)

        self.assertIn("Invalid JSON", str(cm.exception))

    def test_missing_config_name(self):
        """Test configuration missing config_name field"""
        config = self._create_valid_config()
        del config['config_name']
        filepath = self._write_config_file(config)

        with self.assertRaises(ParameterConfigError) as cm:
            load_parameter_config(filepath)

        self.assertIn("config_name", str(cm.exception))

    def test_missing_description(self):
        """Test configuration missing description field"""
        config = self._create_valid_config()
        del config['description']
        filepath = self._write_config_file(config)

        with self.assertRaises(ParameterConfigError) as cm:
            load_parameter_config(filepath)

        self.assertIn("description", str(cm.exception))

    def test_missing_parameters(self):
        """Test configuration missing parameters field"""
        config = self._create_valid_config()
        del config['parameters']
        filepath = self._write_config_file(config)

        with self.assertRaises(ParameterConfigError) as cm:
            load_parameter_config(filepath)

        self.assertIn("parameters", str(cm.exception))

    def test_invalid_config_name_type(self):
        """Test config_name with wrong type"""
        config = self._create_valid_config()
        config['config_name'] = 123  # Should be string
        filepath = self._write_config_file(config)

        with self.assertRaises(ParameterConfigError) as cm:
            load_parameter_config(filepath)

        self.assertIn("config_name", str(cm.exception))
        self.assertIn("string", str(cm.exception))

    def test_missing_required_parameter(self):
        """Test configuration missing a required parameter"""
        config = self._create_valid_config()
        del config['parameters']['NORMALIZATION_MAX_SCALE']
        filepath = self._write_config_file(config)

        with self.assertRaises(ParameterConfigError) as cm:
            load_parameter_config(filepath)

        self.assertIn("Missing required parameters", str(cm.exception))
        self.assertIn("NORMALIZATION_MAX_SCALE", str(cm.exception))

    def test_extra_parameter(self):
        """Test configuration with unexpected extra parameter"""
        config = self._create_valid_config()
        config['parameters']['UNKNOWN_PARAMETER'] = [1.0]
        filepath = self._write_config_file(config)

        with self.assertRaises(ParameterConfigError) as cm:
            load_parameter_config(filepath)

        self.assertIn("Unexpected parameters", str(cm.exception))
        self.assertIn("UNKNOWN_PARAMETER", str(cm.exception))

    def test_parameter_not_list(self):
        """Test parameter with value that's not a list"""
        config = self._create_valid_config()
        config['parameters']['NORMALIZATION_MAX_SCALE'] = 100  # Should be [100]
        filepath = self._write_config_file(config)

        with self.assertRaises(ParameterConfigError) as cm:
            load_parameter_config(filepath)

        self.assertIn("must have a list", str(cm.exception))

    def test_parameter_empty_list(self):
        """Test parameter with empty value list"""
        config = self._create_valid_config()
        config['parameters']['NORMALIZATION_MAX_SCALE'] = []
        filepath = self._write_config_file(config)

        with self.assertRaises(ParameterConfigError) as cm:
            load_parameter_config(filepath)

        self.assertIn("at least one value", str(cm.exception))

    def test_parameter_non_numeric_value(self):
        """Test parameter with non-numeric value"""
        config = self._create_valid_config()
        config['parameters']['NORMALIZATION_MAX_SCALE'] = [100, "not a number"]
        filepath = self._write_config_file(config)

        with self.assertRaises(ParameterConfigError) as cm:
            load_parameter_config(filepath)

        self.assertIn("must be a number", str(cm.exception))

    # =========================================================================
    # Test expand_parameter_combinations
    # =========================================================================

    def test_expand_single_values(self):
        """Test expansion with single values per parameter"""
        parameters = {
            'PARAM_A': [100],
            'PARAM_B': [200]
        }

        combinations = expand_parameter_combinations(parameters)

        self.assertEqual(len(combinations), 1)
        self.assertEqual(combinations[0], {'PARAM_A': 100, 'PARAM_B': 200})

    def test_expand_two_values_each(self):
        """Test expansion with two values per parameter"""
        parameters = {
            'PARAM_A': [1, 2],
            'PARAM_B': [10, 20]
        }

        combinations = expand_parameter_combinations(parameters)

        self.assertEqual(len(combinations), 4)  # 2 * 2 = 4 combinations

        # Check all combinations are present
        expected = [
            {'PARAM_A': 1, 'PARAM_B': 10},
            {'PARAM_A': 1, 'PARAM_B': 20},
            {'PARAM_A': 2, 'PARAM_B': 10},
            {'PARAM_A': 2, 'PARAM_B': 20}
        ]

        for expected_combo in expected:
            self.assertIn(expected_combo, combinations)

    def test_expand_mixed_value_counts(self):
        """Test expansion with different numbers of values per parameter"""
        parameters = {
            'PARAM_A': [1],
            'PARAM_B': [10, 20],
            'PARAM_C': [100, 200, 300]
        }

        combinations = expand_parameter_combinations(parameters)

        # 1 * 2 * 3 = 6 combinations
        self.assertEqual(len(combinations), 6)

        # Check that PARAM_A is always 1
        for combo in combinations:
            self.assertEqual(combo['PARAM_A'], 1)

    def test_expand_maintains_parameter_names(self):
        """Test that all combinations have all parameter names"""
        parameters = {param: [1.0] for param in REQUIRED_PARAMETERS[:5]}

        combinations = expand_parameter_combinations(parameters)

        for combo in combinations:
            self.assertEqual(set(combo.keys()), set(parameters.keys()))

    # =========================================================================
    # Test get_num_combinations
    # =========================================================================

    def test_get_num_combinations_single(self):
        """Test combination count with single values"""
        parameters = {
            'PARAM_A': [100],
            'PARAM_B': [200]
        }

        count = get_num_combinations(parameters)
        self.assertEqual(count, 1)

    def test_get_num_combinations_multiple(self):
        """Test combination count with multiple values"""
        parameters = {
            'PARAM_A': [1, 2],
            'PARAM_B': [10, 20, 30],
            'PARAM_C': [100, 200]
        }

        count = get_num_combinations(parameters)
        self.assertEqual(count, 2 * 3 * 2)  # 12

    def test_get_num_combinations_matches_expand(self):
        """Test that count matches actual expansion"""
        parameters = {param: [1.0, 2.0] for param in REQUIRED_PARAMETERS[:10]}

        count = get_num_combinations(parameters)
        combinations = expand_parameter_combinations(parameters)

        self.assertEqual(count, len(combinations))

    # =========================================================================
    # Test load_and_expand_config
    # =========================================================================

    def test_load_and_expand_valid_config(self):
        """Test combined load and expand operation"""
        config = self._create_valid_config()
        filepath = self._write_config_file(config)

        loaded_config, combinations = load_and_expand_config(filepath)

        self.assertEqual(loaded_config['config_name'], 'test_config')
        self.assertGreater(len(combinations), 0)
        self.assertEqual(len(combinations), 2 ** len(REQUIRED_PARAMETERS))  # 2 values each

    # =========================================================================
    # Test validate_config_file
    # =========================================================================

    def test_validate_valid_file(self):
        """Test validation of valid configuration file"""
        config = self._create_valid_config()
        filepath = self._write_config_file(config)

        result = validate_config_file(filepath)
        self.assertTrue(result)

    def test_validate_invalid_file(self):
        """Test validation of invalid configuration file"""
        config = self._create_valid_config()
        del config['config_name']
        filepath = self._write_config_file(config)

        with self.assertRaises(ParameterConfigError):
            validate_config_file(filepath)

    # =========================================================================
    # Integration Tests
    # =========================================================================

    def test_load_baseline_parameters(self):
        """Test loading the actual baseline_parameters.json file"""
        # Get path to baseline parameters
        sim_dir = Path(__file__).parent.parent / "simulation"
        baseline_path = sim_dir / "parameters" / "baseline_parameters.json"

        if baseline_path.exists():
            config = load_parameter_config(str(baseline_path))

            self.assertEqual(config['config_name'], 'baseline')
            self.assertEqual(len(config['parameters']), len(REQUIRED_PARAMETERS))

            # All baseline parameters should have single values
            for param_name, values in config['parameters'].items():
                self.assertEqual(len(values), 1,
                               f"{param_name} should have exactly 1 value in baseline")

    def test_load_template_parameters(self):
        """Test loading the actual parameter_template.json file"""
        # Get path to template
        sim_dir = Path(__file__).parent.parent / "simulation"
        template_path = sim_dir / "parameters" / "parameter_template.json"

        if template_path.exists():
            config = load_parameter_config(str(template_path))

            self.assertEqual(config['config_name'], 'template')
            self.assertEqual(len(config['parameters']), len(REQUIRED_PARAMETERS))

            # Template should have 2 values for each parameter
            for param_name, values in config['parameters'].items():
                self.assertEqual(len(values), 2,
                               f"{param_name} should have exactly 2 values in template")


if __name__ == '__main__':
    unittest.main()
