#!/usr/bin/env python3
"""
Unit Tests for Validation Utilities Module

Tests standardized validation patterns including configuration validation,
data integrity checks, file operations, and business rule validation.

Author: Kai Mizuno
Last Updated: September 2025
"""

import unittest
import tempfile
import os
from pathlib import Path
from enum import Enum
import pandas as pd

# Set up the path for imports
import sys
sys.path.append(str(Path(__file__).parent.parent))

from shared_files.validation_utils import (
    ValidationError,
    ValidationResult,
    ConfigValidator,
    FileValidator,
    DataValidator,
    StringValidator,
    validate_multiple,
    validate_fantasy_league_config,
    validate_player_csv,
    validate_teams_csv,
    validate_module_config
)


class SampleTestEnum(Enum):
    OPTION_A = "option_a"
    OPTION_B = "option_b"
    OPTION_C = "option_c"


class TestValidationResult(unittest.TestCase):
    """Test cases for ValidationResult class"""

    def test_validation_result_initialization(self):
        """Test ValidationResult initialization"""
        result = ValidationResult()

        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.warnings), 0)
        self.assertTrue(result.is_valid)
        self.assertFalse(result.has_warnings)

    def test_add_error(self):
        """Test adding validation errors"""
        result = ValidationResult()

        result.add_error("Test error", "test_field", "test_value", "TEST_CODE")

        self.assertEqual(len(result.errors), 1)
        self.assertFalse(result.is_valid)

        error = result.errors[0]
        self.assertEqual(error['message'], "Test error")
        self.assertEqual(error['field'], "test_field")
        self.assertEqual(error['value'], "test_value")
        self.assertEqual(error['code'], "TEST_CODE")

    def test_add_warning(self):
        """Test adding validation warnings"""
        result = ValidationResult()

        result.add_warning("Test warning", "test_field")

        self.assertEqual(len(result.warnings), 1)
        self.assertTrue(result.is_valid)  # Warnings don't affect validity
        self.assertTrue(result.has_warnings)

    def test_get_messages(self):
        """Test getting error and warning messages"""
        result = ValidationResult()

        result.add_error("Error 1")
        result.add_error("Error 2")
        result.add_warning("Warning 1")

        error_messages = result.get_error_messages()
        warning_messages = result.get_warning_messages()

        self.assertEqual(error_messages, ["Error 1", "Error 2"])
        self.assertEqual(warning_messages, ["Warning 1"])

    def test_raise_if_invalid(self):
        """Test raising exception for invalid results"""
        result = ValidationResult()

        # Valid result should not raise
        result.raise_if_invalid()

        # Invalid result should raise
        result.add_error("Test error")

        with self.assertRaises(ValidationError) as context:
            result.raise_if_invalid()

        self.assertIn("Test error", str(context.exception))


class TestConfigValidator(unittest.TestCase):
    """Test cases for ConfigValidator class"""

    def test_validate_enum_value_success(self):
        """Test successful enum validation"""
        result = ConfigValidator.validate_enum_value("option_a", SampleTestEnum, "test_field")

        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)

    def test_validate_enum_value_invalid(self):
        """Test enum validation with invalid value"""
        result = ConfigValidator.validate_enum_value("invalid_option", SampleTestEnum, "test_field")

        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 1)
        self.assertIn("Invalid test_field", result.errors[0]['message'])

    def test_validate_enum_value_none(self):
        """Test enum validation with None value"""
        result = ConfigValidator.validate_enum_value(None, SampleTestEnum, "test_field")

        self.assertFalse(result.is_valid)
        self.assertIn("cannot be None", result.errors[0]['message'])

    def test_validate_mutually_exclusive_valid(self):
        """Test mutually exclusive validation with valid config"""
        config = {"option_a": True, "option_b": False, "option_c": False}
        groups = [["option_a", "option_b"], ["option_b", "option_c"]]

        result = ConfigValidator.validate_mutually_exclusive(config, groups)

        self.assertTrue(result.is_valid)

    def test_validate_mutually_exclusive_invalid(self):
        """Test mutually exclusive validation with conflicting options"""
        config = {"option_a": True, "option_b": True}
        groups = [["option_a", "option_b"]]

        result = ConfigValidator.validate_mutually_exclusive(config, groups)

        self.assertFalse(result.is_valid)
        self.assertIn("Mutually exclusive", result.errors[0]['message'])

    def test_validate_required_fields_success(self):
        """Test required fields validation with complete config"""
        config = {"field1": "value1", "field2": "value2"}
        required = ["field1", "field2"]

        result = ConfigValidator.validate_required_fields(config, required)

        self.assertTrue(result.is_valid)

    def test_validate_required_fields_missing(self):
        """Test required fields validation with missing fields"""
        config = {"field1": "value1"}
        required = ["field1", "field2"]

        result = ConfigValidator.validate_required_fields(config, required)

        self.assertFalse(result.is_valid)
        self.assertIn("field2", result.errors[0]['message'])

    def test_validate_required_fields_none(self):
        """Test required fields validation with None values"""
        config = {"field1": "value1", "field2": None}
        required = ["field1", "field2"]

        result = ConfigValidator.validate_required_fields(config, required)

        self.assertFalse(result.is_valid)
        self.assertIn("cannot be None", result.errors[0]['message'])

    def test_validate_range_success(self):
        """Test range validation with valid values"""
        result = ConfigValidator.validate_range(5, 1, 10, "test_value")

        self.assertTrue(result.is_valid)

    def test_validate_range_below_minimum(self):
        """Test range validation below minimum"""
        result = ConfigValidator.validate_range(0, 1, 10, "test_value")

        self.assertFalse(result.is_valid)
        self.assertIn("must be >= 1", result.errors[0]['message'])

    def test_validate_range_above_maximum(self):
        """Test range validation above maximum"""
        result = ConfigValidator.validate_range(15, 1, 10, "test_value")

        self.assertFalse(result.is_valid)
        self.assertIn("must be <= 10", result.errors[0]['message'])

    def test_validate_range_non_numeric(self):
        """Test range validation with non-numeric value"""
        result = ConfigValidator.validate_range("not_a_number", 1, 10, "test_value")

        self.assertFalse(result.is_valid)
        self.assertIn("must be numeric", result.errors[0]['message'])


class TestFileValidator(unittest.TestCase):
    """Test cases for FileValidator class"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_file = Path(self.temp_dir) / "test_file.txt"
        self.temp_file.write_text("test content")

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        try:
            shutil.rmtree(self.temp_dir)
        except:
            pass

    def test_validate_file_exists_success(self):
        """Test file existence validation with existing file"""
        result = FileValidator.validate_file_exists(self.temp_file)

        self.assertTrue(result.is_valid)

    def test_validate_file_exists_missing_required(self):
        """Test file existence validation with missing required file"""
        missing_file = Path(self.temp_dir) / "missing.txt"
        result = FileValidator.validate_file_exists(missing_file, required=True)

        self.assertFalse(result.is_valid)
        self.assertIn("Required file not found", result.errors[0]['message'])

    def test_validate_file_exists_missing_optional(self):
        """Test file existence validation with missing optional file"""
        missing_file = Path(self.temp_dir) / "missing.txt"
        result = FileValidator.validate_file_exists(missing_file, required=False)

        self.assertTrue(result.is_valid)
        self.assertTrue(result.has_warnings)
        self.assertIn("Optional file not found", result.warnings[0]['message'])

    def test_validate_directory_exists_success(self):
        """Test directory existence validation with existing directory"""
        result = FileValidator.validate_directory_exists(self.temp_dir)

        self.assertTrue(result.is_valid)

    def test_validate_directory_exists_create(self):
        """Test directory existence validation with creation"""
        new_dir = Path(self.temp_dir) / "new_subdir"
        result = FileValidator.validate_directory_exists(new_dir, create_if_missing=True)

        self.assertTrue(result.is_valid)
        self.assertTrue(result.has_warnings)
        self.assertTrue(new_dir.exists())

    def test_validate_file_extension_success(self):
        """Test file extension validation with valid extension"""
        result = FileValidator.validate_file_extension(self.temp_file, ['.txt', '.csv'])

        self.assertTrue(result.is_valid)

    def test_validate_file_extension_invalid(self):
        """Test file extension validation with invalid extension"""
        result = FileValidator.validate_file_extension(self.temp_file, ['.csv', '.json'])

        self.assertFalse(result.is_valid)
        self.assertIn("Invalid file extension", result.errors[0]['message'])

    def test_validate_csv_columns_success(self):
        """Test CSV column validation with valid file"""
        csv_file = Path(self.temp_dir) / "test.csv"
        df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4], 'col3': [5, 6]})
        df.to_csv(csv_file, index=False)

        result = FileValidator.validate_csv_columns(csv_file, ['col1', 'col2'], ['col3', 'col4'])

        self.assertTrue(result.is_valid)
        self.assertTrue(result.has_warnings)  # col4 is missing but optional

    def test_validate_csv_columns_missing_required(self):
        """Test CSV column validation with missing required columns"""
        csv_file = Path(self.temp_dir) / "test.csv"
        df = pd.DataFrame({'col1': [1, 2]})
        df.to_csv(csv_file, index=False)

        result = FileValidator.validate_csv_columns(csv_file, ['col1', 'col2'])

        self.assertFalse(result.is_valid)
        self.assertIn("Missing required columns", result.errors[0]['message'])


class TestDataValidator(unittest.TestCase):
    """Test cases for DataValidator class"""

    def test_validate_player_data_success(self):
        """Test player data validation with valid data"""
        player_data = {
            'id': 'player_123',
            'name': 'Test Player',
            'team': 'KC',
            'position': 'QB',
            'fantasy_points': 250.5,
            'average_draft_position': 12
        }

        result = DataValidator.validate_player_data(player_data)

        self.assertTrue(result.is_valid)

    def test_validate_player_data_missing_required(self):
        """Test player data validation with missing required fields"""
        player_data = {
            'id': 'player_123',
            'name': 'Test Player'
            # Missing team and position
        }

        result = DataValidator.validate_player_data(player_data)

        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 2)  # team and position missing

    def test_validate_player_data_invalid_position(self):
        """Test player data validation with invalid position"""
        player_data = {
            'id': 'player_123',
            'name': 'Test Player',
            'team': 'KC',
            'position': 'INVALID',
            'fantasy_points': 250.5
        }

        result = DataValidator.validate_player_data(player_data)

        self.assertFalse(result.is_valid)
        self.assertIn("Invalid position", result.errors[0]['message'])

    def test_validate_player_data_negative_points(self):
        """Test player data validation with negative fantasy points"""
        player_data = {
            'id': 'player_123',
            'name': 'Test Player',
            'team': 'KC',
            'position': 'QB',
            'fantasy_points': -10.5
        }

        result = DataValidator.validate_player_data(player_data)

        self.assertTrue(result.is_valid)  # Negative points are warning, not error
        self.assertTrue(result.has_warnings)
        self.assertIn("Negative fantasy points", result.warnings[0]['message'])

    def test_validate_team_data_success(self):
        """Test team data validation with valid data"""
        team_data = {
            'team': 'KC',
            'offensive_rank': 5,
            'defensive_rank': 12
        }

        result = DataValidator.validate_team_data(team_data)

        self.assertTrue(result.is_valid)

    def test_validate_team_data_invalid_rank(self):
        """Test team data validation with invalid ranking"""
        team_data = {
            'team': 'KC',
            'offensive_rank': 50  # Out of range
        }

        result = DataValidator.validate_team_data(team_data)

        self.assertFalse(result.is_valid)
        self.assertIn("must be <= 32", result.errors[0]['message'])

    def test_validate_week_number_regular_season(self):
        """Test week number validation for regular season"""
        result = DataValidator.validate_week_number(10, allow_playoffs=False)

        self.assertTrue(result.is_valid)

    def test_validate_week_number_playoffs(self):
        """Test week number validation for playoffs"""
        result = DataValidator.validate_week_number(18, allow_playoffs=True)

        self.assertTrue(result.is_valid)

    def test_validate_week_number_invalid(self):
        """Test week number validation with invalid week"""
        result = DataValidator.validate_week_number(25, allow_playoffs=True)

        self.assertFalse(result.is_valid)
        self.assertIn("must be <= 18", result.errors[0]['message'])


class TestStringValidator(unittest.TestCase):
    """Test cases for StringValidator class"""

    def test_validate_pattern_success(self):
        """Test pattern validation with matching string"""
        result = StringValidator.validate_pattern("ABC123", r'^[A-Z]{3}\d{3}$', "test_field")

        self.assertTrue(result.is_valid)

    def test_validate_pattern_failure(self):
        """Test pattern validation with non-matching string"""
        result = StringValidator.validate_pattern("abc123", r'^[A-Z]{3}\d{3}$', "test_field")

        self.assertFalse(result.is_valid)
        self.assertIn("does not match required pattern", result.errors[0]['message'])

    def test_validate_pattern_non_string(self):
        """Test pattern validation with non-string value"""
        result = StringValidator.validate_pattern(123, r'^\d+$', "test_field")

        self.assertFalse(result.is_valid)
        self.assertIn("must be string", result.errors[0]['message'])

    def test_validate_not_empty_success(self):
        """Test non-empty validation with valid string"""
        result = StringValidator.validate_not_empty("test value", "test_field")

        self.assertTrue(result.is_valid)

    def test_validate_not_empty_failure(self):
        """Test non-empty validation with empty string"""
        result = StringValidator.validate_not_empty("", "test_field")

        self.assertFalse(result.is_valid)
        self.assertIn("cannot be empty", result.errors[0]['message'])

    def test_validate_not_empty_whitespace(self):
        """Test non-empty validation with whitespace string"""
        result = StringValidator.validate_not_empty("   ", "test_field", strip_whitespace=True)

        self.assertFalse(result.is_valid)
        self.assertIn("cannot be empty", result.errors[0]['message'])

    def test_validate_team_abbreviation_success(self):
        """Test team abbreviation validation with valid team"""
        result = StringValidator.validate_team_abbreviation("KC")

        self.assertTrue(result.is_valid)

    def test_validate_team_abbreviation_invalid(self):
        """Test team abbreviation validation with invalid team"""
        result = StringValidator.validate_team_abbreviation("invalid")

        self.assertFalse(result.is_valid)
        self.assertIn("does not match required pattern", result.errors[0]['message'])


class TestConvenienceFunctions(unittest.TestCase):
    """Test cases for convenience validation functions"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        try:
            shutil.rmtree(self.temp_dir)
        except:
            pass

    def test_validate_player_csv_success(self):
        """Test player CSV validation with valid file"""
        csv_file = Path(self.temp_dir) / "players.csv"
        df = pd.DataFrame({
            'id': ['1', '2'],
            'name': ['Player 1', 'Player 2'],
            'team': ['KC', 'BUF'],
            'position': ['QB', 'RB'],
            'fantasy_points': [250, 180],
            'bye_week': [10, 11]
        })
        df.to_csv(csv_file, index=False)

        result = validate_player_csv(csv_file)

        self.assertTrue(result.is_valid)

    def test_validate_teams_csv_success(self):
        """Test teams CSV validation with valid file"""
        csv_file = Path(self.temp_dir) / "teams.csv"
        df = pd.DataFrame({
            'team': ['KC', 'BUF'],
            'offensive_rank': [5, 8],
            'defensive_rank': [12, 3]
        })
        df.to_csv(csv_file, index=False)

        result = validate_teams_csv(csv_file)

        self.assertTrue(result.is_valid)

    def test_validate_fantasy_league_config_success(self):
        """Test fantasy league config validation with valid config"""
        config = {
            'scoring_format': 'ppr',
            'current_nfl_week': 10,
            'max_players': 15
        }

        result = validate_fantasy_league_config(config)

        self.assertTrue(result.is_valid)

    def test_validate_fantasy_league_config_invalid(self):
        """Test fantasy league config validation with invalid config"""
        config = {
            'scoring_format': 'invalid',
            'current_nfl_week': 25,
            'max_players': -5
        }

        result = validate_fantasy_league_config(config)

        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 3)

    def test_validate_module_config_success(self):
        """Test module config validation with valid config"""
        config = {
            'enabled': True,
            'log_level': 'INFO',
            'trade_helper_mode': False
        }

        result = validate_module_config(config, 'draft_helper')

        self.assertTrue(result.is_valid)

    def test_validate_multiple_success(self):
        """Test multiple validator execution with all passing"""
        validators = [
            lambda: ConfigValidator.validate_range(5, 1, 10, "value1"),
            lambda: ConfigValidator.validate_range(8, 1, 10, "value2")
        ]

        result = validate_multiple(validators)

        self.assertTrue(result.is_valid)

    def test_validate_multiple_with_errors(self):
        """Test multiple validator execution with some failures"""
        validators = [
            lambda: ConfigValidator.validate_range(5, 1, 10, "value1"),
            lambda: ConfigValidator.validate_range(15, 1, 10, "value2")
        ]

        result = validate_multiple(validators)

        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.errors), 1)


if __name__ == '__main__':
    unittest.main()