#!/usr/bin/env python3
"""
Validation Utilities Module

Provides standardized validation patterns used across the fantasy football system.
Consolidates common validation logic for configuration, data integrity, file operations,
and business rules to ensure consistency and reliability.

Author: Kai Mizuno
Last Updated: September 2025
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Callable, Type
from enum import Enum
import pandas as pd
from shared_files.logging_utils import setup_module_logging

# Set up logging
logger = setup_module_logging(__name__)


class ValidationError(Exception):
    """Custom exception for validation errors"""
    def __init__(self, message: str, field: str = None, value: Any = None):
        self.message = message
        self.field = field
        self.value = value
        super().__init__(self.message)


class ValidationResult:
    """Container for validation results with detailed error information"""

    def __init__(self):
        self.errors: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []

    def add_error(self, message: str, field: str = None, value: Any = None, code: str = None):
        """Add a validation error"""
        self.errors.append({
            'message': message,
            'field': field,
            'value': value,
            'code': code
        })

    def add_warning(self, message: str, field: str = None, value: Any = None, code: str = None):
        """Add a validation warning"""
        self.warnings.append({
            'message': message,
            'field': field,
            'value': value,
            'code': code
        })

    @property
    def is_valid(self) -> bool:
        """Check if validation passed (no errors)"""
        return len(self.errors) == 0

    @property
    def has_warnings(self) -> bool:
        """Check if validation has warnings"""
        return len(self.warnings) > 0

    def get_error_messages(self) -> List[str]:
        """Get list of error messages"""
        return [error['message'] for error in self.errors]

    def get_warning_messages(self) -> List[str]:
        """Get list of warning messages"""
        return [warning['message'] for warning in self.warnings]

    def raise_if_invalid(self):
        """Raise ValidationError if validation failed"""
        if not self.is_valid:
            messages = self.get_error_messages()
            raise ValidationError(f"Validation failed: {'; '.join(messages)}")


class ConfigValidator:
    """Validator for configuration settings and options"""

    @staticmethod
    def validate_enum_value(value: Any, enum_class: Type[Enum], field_name: str) -> ValidationResult:
        """Validate that value is a valid enum option"""
        result = ValidationResult()

        if value is None:
            result.add_error(f"{field_name} cannot be None", field_name, value)
            return result

        # Get valid values
        valid_values = [item.value for item in enum_class]

        if value not in valid_values:
            result.add_error(
                f"Invalid {field_name}: '{value}'. Valid options: {valid_values}",
                field_name, value, "INVALID_ENUM"
            )

        return result

    @staticmethod
    def validate_mutually_exclusive(config: Dict[str, Any],
                                  exclusive_groups: List[List[str]]) -> ValidationResult:
        """Validate that mutually exclusive options are not both enabled"""
        result = ValidationResult()

        for group in exclusive_groups:
            enabled_options = [option for option in group if config.get(option, False)]

            if len(enabled_options) > 1:
                result.add_error(
                    f"Mutually exclusive options cannot both be enabled: {enabled_options}",
                    code="MUTUALLY_EXCLUSIVE"
                )

        return result

    @staticmethod
    def validate_required_fields(config: Dict[str, Any],
                                required_fields: List[str]) -> ValidationResult:
        """Validate that all required configuration fields are present"""
        result = ValidationResult()

        for field in required_fields:
            if field not in config:
                result.add_error(f"Required configuration field missing: {field}", field)
            elif config[field] is None:
                result.add_error(f"Required configuration field cannot be None: {field}", field)

        return result

    @staticmethod
    def validate_range(value: Union[int, float], min_val: Union[int, float] = None,
                      max_val: Union[int, float] = None, field_name: str = "value") -> ValidationResult:
        """Validate that a numeric value is within specified range"""
        result = ValidationResult()

        if not isinstance(value, (int, float)):
            result.add_error(f"{field_name} must be numeric, got {type(value).__name__}", field_name, value)
            return result

        if min_val is not None and value < min_val:
            result.add_error(f"{field_name} must be >= {min_val}, got {value}", field_name, value)

        if max_val is not None and value > max_val:
            result.add_error(f"{field_name} must be <= {max_val}, got {value}", field_name, value)

        return result


class FileValidator:
    """Validator for file operations and data integrity"""

    @staticmethod
    def validate_file_exists(filepath: Union[str, Path],
                           required: bool = True) -> ValidationResult:
        """Validate that a file exists"""
        result = ValidationResult()
        filepath = Path(filepath)

        if not filepath.exists():
            if required:
                result.add_error(f"Required file not found: {filepath}", "filepath", str(filepath))
            else:
                result.add_warning(f"Optional file not found: {filepath}", "filepath", str(filepath))

        return result

    @staticmethod
    def validate_directory_exists(dirpath: Union[str, Path],
                                create_if_missing: bool = False) -> ValidationResult:
        """Validate that a directory exists, optionally create it"""
        result = ValidationResult()
        dirpath = Path(dirpath)

        if not dirpath.exists():
            if create_if_missing:
                try:
                    dirpath.mkdir(parents=True, exist_ok=True)
                    result.add_warning(f"Created missing directory: {dirpath}", "dirpath", str(dirpath))
                except Exception as e:
                    result.add_error(f"Failed to create directory {dirpath}: {e}", "dirpath", str(dirpath))
            else:
                result.add_error(f"Directory not found: {dirpath}", "dirpath", str(dirpath))

        return result

    @staticmethod
    def validate_file_extension(filepath: Union[str, Path],
                              allowed_extensions: List[str]) -> ValidationResult:
        """Validate that file has an allowed extension"""
        result = ValidationResult()
        filepath = Path(filepath)

        file_ext = filepath.suffix.lower()
        allowed_extensions = [ext.lower() if ext.startswith('.') else f'.{ext.lower()}'
                            for ext in allowed_extensions]

        if file_ext not in allowed_extensions:
            result.add_error(
                f"Invalid file extension '{file_ext}'. Allowed: {allowed_extensions}",
                "filepath", str(filepath)
            )

        return result

    @staticmethod
    def validate_csv_columns(filepath: Union[str, Path],
                           required_columns: List[str],
                           optional_columns: List[str] = None) -> ValidationResult:
        """Validate that CSV file contains required columns"""
        result = ValidationResult()
        filepath = Path(filepath)

        # First validate file exists
        file_result = FileValidator.validate_file_exists(filepath)
        if not file_result.is_valid:
            result.errors.extend(file_result.errors)
            return result

        try:
            df = pd.read_csv(filepath, nrows=0)  # Read just headers
            existing_columns = set(df.columns)
            required_set = set(required_columns)

            missing_required = required_set - existing_columns
            if missing_required:
                result.add_error(
                    f"Missing required columns in {filepath}: {list(missing_required)}",
                    "columns", list(missing_required)
                )

            # Check for optional columns
            if optional_columns:
                optional_set = set(optional_columns)
                missing_optional = optional_set - existing_columns
                if missing_optional:
                    result.add_warning(
                        f"Missing optional columns in {filepath}: {list(missing_optional)}",
                        "columns", list(missing_optional)
                    )

        except Exception as e:
            result.add_error(f"Failed to read CSV file {filepath}: {e}", "filepath", str(filepath))

        return result


class DataValidator:
    """Validator for data integrity and business rules"""

    @staticmethod
    def validate_player_data(player_data: Dict[str, Any]) -> ValidationResult:
        """Validate fantasy player data"""
        result = ValidationResult()

        # Required fields
        required_fields = ['id', 'name', 'team', 'position']
        for field in required_fields:
            if not player_data.get(field):
                result.add_error(f"Player missing required field: {field}", field)

        # Position validation
        valid_positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']
        position = player_data.get('position', '').upper()
        if position and position not in valid_positions:
            result.add_error(f"Invalid position: {position}. Valid: {valid_positions}", "position", position)

        # Fantasy points validation
        fantasy_points = player_data.get('fantasy_points', 0)
        if isinstance(fantasy_points, (int, float)) and fantasy_points < 0:
            result.add_warning(f"Negative fantasy points: {fantasy_points}", "fantasy_points", fantasy_points)

        # ADP validation
        adp = player_data.get('average_draft_position')
        if adp is not None:
            adp_result = ConfigValidator.validate_range(adp, 1, 1000, "average_draft_position")
            result.errors.extend(adp_result.errors)

        return result

    @staticmethod
    def validate_team_data(team_data: Dict[str, Any]) -> ValidationResult:
        """Validate NFL team data"""
        result = ValidationResult()

        # Required fields
        if not team_data.get('team'):
            result.add_error("Team missing required field: team", "team")

        # Ranking validation
        for rank_field in ['offensive_rank', 'defensive_rank']:
            rank = team_data.get(rank_field)
            if rank is not None:
                rank_result = ConfigValidator.validate_range(rank, 1, 32, rank_field)
                result.errors.extend(rank_result.errors)

        return result

    @staticmethod
    def validate_week_number(week: int, allow_playoffs: bool = False) -> ValidationResult:
        """Validate NFL week number"""
        result = ValidationResult()

        min_week = 1
        max_week = 18 if allow_playoffs else 17

        week_result = ConfigValidator.validate_range(week, min_week, max_week, "week")
        result.errors.extend(week_result.errors)

        return result


class StringValidator:
    """Validator for string patterns and formats"""

    @staticmethod
    def validate_pattern(value: str, pattern: str, field_name: str = "value") -> ValidationResult:
        """Validate that string matches regex pattern"""
        result = ValidationResult()

        if not isinstance(value, str):
            result.add_error(f"{field_name} must be string, got {type(value).__name__}", field_name, value)
            return result

        if not re.match(pattern, value):
            result.add_error(f"{field_name} does not match required pattern: {pattern}", field_name, value)

        return result

    @staticmethod
    def validate_not_empty(value: str, field_name: str = "value",
                          strip_whitespace: bool = True) -> ValidationResult:
        """Validate that string is not empty"""
        result = ValidationResult()

        if not isinstance(value, str):
            result.add_error(f"{field_name} must be string, got {type(value).__name__}", field_name, value)
            return result

        check_value = value.strip() if strip_whitespace else value
        if not check_value:
            result.add_error(f"{field_name} cannot be empty", field_name, value)

        return result

    @staticmethod
    def validate_team_abbreviation(team: str) -> ValidationResult:
        """Validate NFL team abbreviation format"""
        result = ValidationResult()

        # Team should be 2-4 uppercase letters
        pattern = r'^[A-Z]{2,4}$'
        pattern_result = StringValidator.validate_pattern(team, pattern, "team")
        result.errors.extend(pattern_result.errors)

        return result


def validate_multiple(validators: List[Callable[[], ValidationResult]]) -> ValidationResult:
    """Run multiple validators and combine results"""
    combined_result = ValidationResult()

    for validator in validators:
        try:
            result = validator()
            combined_result.errors.extend(result.errors)
            combined_result.warnings.extend(result.warnings)
        except Exception as e:
            combined_result.add_error(f"Validator error: {e}")

    return combined_result


def validate_fantasy_league_config(config: Dict[str, Any]) -> ValidationResult:
    """Validate fantasy league configuration"""
    result = ValidationResult()

    # Validate scoring format
    if 'scoring_format' in config:
        # Would use ScoringFormat enum if imported from player_data_models
        valid_formats = ['ppr', 'std', 'half']
        if config['scoring_format'] not in valid_formats:
            result.add_error(f"Invalid scoring format: {config['scoring_format']}")

    # Validate current week
    if 'current_nfl_week' in config:
        week_result = DataValidator.validate_week_number(config['current_nfl_week'], allow_playoffs=True)
        result.errors.extend(week_result.errors)

    # Validate roster limits
    if 'max_players' in config:
        max_result = ConfigValidator.validate_range(config['max_players'], 1, 50, "max_players")
        result.errors.extend(max_result.errors)

    return result


# Convenience functions for common validation patterns
def validate_player_csv(filepath: Union[str, Path]) -> ValidationResult:
    """Validate player CSV file has required columns"""
    required_columns = ['id', 'name', 'team', 'position', 'fantasy_points']
    optional_columns = ['bye_week', 'drafted', 'injury_status', 'average_draft_position']

    return FileValidator.validate_csv_columns(filepath, required_columns, optional_columns)


def validate_teams_csv(filepath: Union[str, Path]) -> ValidationResult:
    """Validate teams CSV file has required columns"""
    required_columns = ['team']
    optional_columns = ['offensive_rank', 'defensive_rank', 'opponent']

    return FileValidator.validate_csv_columns(filepath, required_columns, optional_columns)


def validate_module_config(config: Dict[str, Any], module_name: str) -> ValidationResult:
    """Validate module-specific configuration"""
    result = ValidationResult()

    logger.info(f"Validating configuration for module: {module_name}")

    # Common validation for all modules
    if 'enabled' in config and not isinstance(config['enabled'], bool):
        result.add_error("'enabled' must be boolean", "enabled", config['enabled'])

    if 'log_level' in config:
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if config['log_level'] not in valid_levels:
            result.add_error(f"Invalid log_level: {config['log_level']}")

    # Module-specific validation
    if module_name == 'player_data_fetcher':
        if 'skip_drafted_player_updates' in config and not isinstance(config['skip_drafted_player_updates'], bool):
            result.add_error("'skip_drafted_player_updates' must be boolean")

    elif module_name == 'draft_helper':
        if 'trade_helper_mode' in config and not isinstance(config['trade_helper_mode'], bool):
            result.add_error("'trade_helper_mode' must be boolean")

    logger.info(f"Configuration validation completed for {module_name}: {len(result.errors)} errors, {len(result.warnings)} warnings")
    return result