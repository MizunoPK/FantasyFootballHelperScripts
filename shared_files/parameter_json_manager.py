#!/usr/bin/env python3
"""
Parameter JSON Manager

Manages loading and validation of parameter JSON files for draft helper and starter helper.
Provides centralized parameter management with validation and easy access patterns.

Author: Kai Mizuno
Last Updated: October 2025
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from shared_files.validation_utils import ValidationResult, ConfigValidator
from shared_files.logging_utils import setup_module_logging

# Set up logging
logger = setup_module_logging(__name__)


class ParameterJsonManager:
    """
    Manages parameter loading and validation from JSON files.

    Supports both dict-style and attribute-style access to parameters.
    Validates all parameters on load to ensure data integrity.
    """

    # All 22 required parameters (INJURY_PENALTIES counts as 1 nested dict with 3 sub-keys)
    REQUIRED_PARAMETERS = [
        'ADP_EXCELLENT_MULTIPLIER',
        'ADP_GOOD_MULTIPLIER',
        'ADP_POOR_MULTIPLIER',
        'BASE_BYE_PENALTY',
        'DRAFT_ORDER_PRIMARY_BONUS',
        'DRAFT_ORDER_SECONDARY_BONUS',
        'INJURY_PENALTIES',  # Nested dict with LOW, MEDIUM, HIGH
        'MATCHUP_EXCELLENT_MULTIPLIER',
        'MATCHUP_GOOD_MULTIPLIER',
        'MATCHUP_NEUTRAL_MULTIPLIER',
        'MATCHUP_POOR_MULTIPLIER',
        'MATCHUP_VERY_POOR_MULTIPLIER',
        'NORMALIZATION_MAX_SCALE',
        'PLAYER_RATING_EXCELLENT_MULTIPLIER',
        'PLAYER_RATING_GOOD_MULTIPLIER',
        'PLAYER_RATING_POOR_MULTIPLIER',
        'TEAM_EXCELLENT_MULTIPLIER',
        'TEAM_GOOD_MULTIPLIER',
        'TEAM_POOR_MULTIPLIER',
        'CONSISTENCY_LOW_MULTIPLIER',
        'CONSISTENCY_MEDIUM_MULTIPLIER',
        'CONSISTENCY_HIGH_MULTIPLIER',
    ]

    # Required INJURY_PENALTIES sub-keys
    REQUIRED_INJURY_KEYS = ['LOW', 'MEDIUM', 'HIGH']

    def __init__(self, json_file_path: str):
        """
        Initialize ParameterJsonManager with a JSON file path.

        Args:
            json_file_path: Path to parameter JSON file

        Raises:
            FileNotFoundError: If JSON file doesn't exist
            ValueError: If JSON is malformed or validation fails
            SystemExit: On critical errors (for CLI usage)
        """
        self.json_file_path = Path(json_file_path)
        self.config_name: Optional[str] = None
        self.description: Optional[str] = None
        self.parameters: Dict[str, Any] = {}

        logger.info(f"Initializing ParameterJsonManager with file: {self.json_file_path}")

        try:
            self._load_json()
            self._validate_parameters()
            logger.info(f"Successfully loaded parameters from {self.json_file_path}")
        except Exception as e:
            error_msg = f"Failed to load parameter file '{self.json_file_path}': {e}"
            logger.error(error_msg)
            print(f"\n❌ ERROR: {error_msg}\n", file=sys.stderr)
            sys.exit(1)

    def _load_json(self):
        """Load and parse JSON file."""
        if not self.json_file_path.exists():
            raise FileNotFoundError(f"Parameter JSON file not found: {self.json_file_path}")

        try:
            with open(self.json_file_path, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")

        # Extract metadata
        self.config_name = data.get('config_name', 'unknown')
        self.description = data.get('description', '')

        # Extract parameters
        if 'parameters' not in data:
            raise ValueError("JSON file must contain 'parameters' section")

        self.parameters = data['parameters']

        logger.debug(f"Loaded config: {self.config_name}")
        logger.debug(f"Description: {self.description}")

    def _validate_parameters(self):
        """
        Validate all parameters using validation utilities.

        Raises:
            ValueError: If any validation fails
        """
        result = ValidationResult()

        # Check for required parameters
        missing_params = []
        for param in self.REQUIRED_PARAMETERS:
            if param not in self.parameters:
                missing_params.append(param)

        if missing_params:
            raise ValueError(f"Missing required parameters: {', '.join(missing_params)}")

        # Validate INJURY_PENALTIES structure
        if 'INJURY_PENALTIES' in self.parameters:
            injury_penalties = self.parameters['INJURY_PENALTIES']

            if not isinstance(injury_penalties, dict):
                result.add_error(
                    "INJURY_PENALTIES must be a nested dict with LOW, MEDIUM, HIGH keys",
                    "INJURY_PENALTIES",
                    injury_penalties
                )
            else:
                # Check for required injury keys
                missing_injury_keys = []
                for key in self.REQUIRED_INJURY_KEYS:
                    if key not in injury_penalties:
                        missing_injury_keys.append(key)

                if missing_injury_keys:
                    result.add_error(
                        f"INJURY_PENALTIES missing required keys: {', '.join(missing_injury_keys)}",
                        "INJURY_PENALTIES"
                    )

                # Validate each injury penalty value
                for key in self.REQUIRED_INJURY_KEYS:
                    if key in injury_penalties:
                        penalty_result = ConfigValidator.validate_range(
                            injury_penalties[key], 0, 200,
                            f"INJURY_PENALTIES.{key}"
                        )
                        result.errors.extend(penalty_result.errors)

        # Validate multiplier ranges (0.0 to 2.0 for reasonable adjustments)
        multiplier_params = [
            'ADP_EXCELLENT_MULTIPLIER', 'ADP_GOOD_MULTIPLIER', 'ADP_POOR_MULTIPLIER',
            'PLAYER_RATING_EXCELLENT_MULTIPLIER', 'PLAYER_RATING_GOOD_MULTIPLIER', 'PLAYER_RATING_POOR_MULTIPLIER',
            'TEAM_EXCELLENT_MULTIPLIER', 'TEAM_GOOD_MULTIPLIER', 'TEAM_POOR_MULTIPLIER',
            'MATCHUP_EXCELLENT_MULTIPLIER', 'MATCHUP_GOOD_MULTIPLIER', 'MATCHUP_NEUTRAL_MULTIPLIER',
            'MATCHUP_POOR_MULTIPLIER', 'MATCHUP_VERY_POOR_MULTIPLIER',
            'CONSISTENCY_LOW_MULTIPLIER', 'CONSISTENCY_MEDIUM_MULTIPLIER', 'CONSISTENCY_HIGH_MULTIPLIER',
        ]

        for param in multiplier_params:
            if param in self.parameters:
                mult_result = ConfigValidator.validate_range(
                    self.parameters[param], 0.0, 2.0, param
                )
                result.errors.extend(mult_result.errors)

        # Validate penalty ranges (0 to 200)
        penalty_params = ['BASE_BYE_PENALTY']
        for param in penalty_params:
            if param in self.parameters:
                penalty_result = ConfigValidator.validate_range(
                    self.parameters[param], 0, 200, param
                )
                result.errors.extend(penalty_result.errors)

        # Validate bonus ranges (0 to 100)
        bonus_params = ['DRAFT_ORDER_PRIMARY_BONUS', 'DRAFT_ORDER_SECONDARY_BONUS']
        for param in bonus_params:
            if param in self.parameters:
                bonus_result = ConfigValidator.validate_range(
                    self.parameters[param], 0, 100, param
                )
                result.errors.extend(bonus_result.errors)

        # Validate normalization scale (50 to 200 for reasonable range)
        if 'NORMALIZATION_MAX_SCALE' in self.parameters:
            norm_result = ConfigValidator.validate_range(
                self.parameters['NORMALIZATION_MAX_SCALE'], 50, 200,
                'NORMALIZATION_MAX_SCALE'
            )
            result.errors.extend(norm_result.errors)

        # Raise if validation failed
        if not result.is_valid:
            error_messages = result.get_error_messages()
            raise ValueError(f"Parameter validation failed: {'; '.join(error_messages)}")

        logger.debug("All parameters validated successfully")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get parameter value (dict-style access).

        Args:
            key: Parameter name
            default: Default value if parameter not found

        Returns:
            Parameter value or default
        """
        return self.parameters.get(key, default)

    def __getitem__(self, key: str) -> Any:
        """
        Get parameter value using bracket notation.

        Args:
            key: Parameter name

        Returns:
            Parameter value

        Raises:
            KeyError: If parameter doesn't exist
        """
        return self.parameters[key]

    def __getattr__(self, name: str) -> Any:
        """
        Get parameter value using attribute notation.

        Args:
            name: Parameter name

        Returns:
            Parameter value

        Raises:
            AttributeError: If parameter doesn't exist
        """
        # Avoid infinite recursion for internal attributes
        if name in ('parameters', 'json_file_path', 'config_name', 'description'):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

        if name in self.parameters:
            return self.parameters[name]

        raise AttributeError(f"Parameter '{name}' not found")

    def __contains__(self, key: str) -> bool:
        """Check if parameter exists."""
        return key in self.parameters

    def get_all_parameters(self) -> Dict[str, Any]:
        """Get all parameters as a dictionary."""
        return self.parameters.copy()

    def get_metadata(self) -> Dict[str, str]:
        """Get configuration metadata."""
        return {
            'config_name': self.config_name,
            'description': self.description,
            'file_path': str(self.json_file_path)
        }

    def __repr__(self) -> str:
        """String representation."""
        return f"ParameterJsonManager(config_name='{self.config_name}', file='{self.json_file_path.name}')"

    def __str__(self) -> str:
        """Human-readable string."""
        return f"Parameters: {self.config_name} ({len(self.parameters)} parameters loaded)"
