"""
Parameter Loader Module

Handles loading and validation of JSON parameter configuration files for simulations.
"""

import json
import os
from typing import Dict, List, Any
from pathlib import Path

# Required parameter names (all 23 parameters must be present)
REQUIRED_PARAMETERS = [
    # Core Scoring
    'NORMALIZATION_MAX_SCALE',
    'DRAFT_ORDER_PRIMARY_BONUS',
    'DRAFT_ORDER_SECONDARY_BONUS',

    # Matchup Multipliers
    'MATCHUP_EXCELLENT_MULTIPLIER',
    'MATCHUP_GOOD_MULTIPLIER',
    'MATCHUP_NEUTRAL_MULTIPLIER',
    'MATCHUP_POOR_MULTIPLIER',
    'MATCHUP_VERY_POOR_MULTIPLIER',

    # Injury & Bye Penalties
    'INJURY_PENALTIES_MEDIUM',
    'INJURY_PENALTIES_HIGH',
    'BASE_BYE_PENALTY',

    # ADP Adjustments
    'ADP_EXCELLENT_MULTIPLIER',
    'ADP_GOOD_MULTIPLIER',
    'ADP_POOR_MULTIPLIER',

    # Player Rating Adjustments
    'PLAYER_RATING_EXCELLENT_MULTIPLIER',
    'PLAYER_RATING_GOOD_MULTIPLIER',
    'PLAYER_RATING_POOR_MULTIPLIER',

    # Team Quality Adjustments
    'TEAM_EXCELLENT_MULTIPLIER',
    'TEAM_GOOD_MULTIPLIER',
    'TEAM_POOR_MULTIPLIER',

    # Consistency/Volatility Multipliers
    'CONSISTENCY_LOW_MULTIPLIER',
    'CONSISTENCY_MEDIUM_MULTIPLIER',
    'CONSISTENCY_HIGH_MULTIPLIER',
]


class ParameterConfigError(Exception):
    """Exception raised for parameter configuration errors"""
    pass


def load_parameter_config(json_path: str) -> Dict[str, Any]:
    """
    Load and validate a parameter configuration from a JSON file.

    Args:
        json_path: Path to the JSON configuration file

    Returns:
        Dictionary containing validated configuration data with keys:
        - config_name: Name of the configuration
        - description: Description of the configuration
        - parameters: Dictionary of parameter names to value lists

    Raises:
        ParameterConfigError: If file not found, invalid JSON, or missing required fields
    """
    # Resolve path
    path = Path(json_path)

    if not path.exists():
        raise ParameterConfigError(f"Configuration file not found: {json_path}")

    # Load JSON
    try:
        with open(path, 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        raise ParameterConfigError(f"Invalid JSON in {json_path}: {e}")
    except Exception as e:
        raise ParameterConfigError(f"Error reading {json_path}: {e}")

    # Validate structure
    _validate_config_structure(config, json_path)

    # Validate parameters
    _validate_parameters(config['parameters'], json_path)

    return config


def _validate_config_structure(config: Dict[str, Any], file_path: str) -> None:
    """
    Validate the top-level structure of the configuration.

    Args:
        config: Configuration dictionary to validate
        file_path: Path to config file (for error messages)

    Raises:
        ParameterConfigError: If required fields are missing or invalid
    """
    # Check required top-level fields
    required_fields = ['config_name', 'description', 'parameters']

    for field in required_fields:
        if field not in config:
            raise ParameterConfigError(
                f"Missing required field '{field}' in {file_path}"
            )

    # Validate field types
    if not isinstance(config['config_name'], str):
        raise ParameterConfigError(
            f"'config_name' must be a string in {file_path}"
        )

    if not isinstance(config['description'], str):
        raise ParameterConfigError(
            f"'description' must be a string in {file_path}"
        )

    if not isinstance(config['parameters'], dict):
        raise ParameterConfigError(
            f"'parameters' must be a dictionary in {file_path}"
        )


def _validate_parameters(parameters: Dict[str, List], file_path: str) -> None:
    """
    Validate that all required parameters are present and have valid values.

    Args:
        parameters: Parameters dictionary to validate
        file_path: Path to config file (for error messages)

    Raises:
        ParameterConfigError: If parameters are missing or invalid
    """
    # Check all required parameters are present
    missing_params = set(REQUIRED_PARAMETERS) - set(parameters.keys())
    if missing_params:
        raise ParameterConfigError(
            f"Missing required parameters in {file_path}: {sorted(missing_params)}"
        )

    # Check for unexpected parameters
    extra_params = set(parameters.keys()) - set(REQUIRED_PARAMETERS)
    if extra_params:
        raise ParameterConfigError(
            f"Unexpected parameters in {file_path}: {sorted(extra_params)}"
        )

    # Validate each parameter has valid value list
    for param_name, value_list in parameters.items():
        if not isinstance(value_list, list):
            raise ParameterConfigError(
                f"Parameter '{param_name}' must have a list of values in {file_path}"
            )

        if len(value_list) == 0:
            raise ParameterConfigError(
                f"Parameter '{param_name}' must have at least one value in {file_path}"
            )

        # Validate all values are numbers
        for i, value in enumerate(value_list):
            if not isinstance(value, (int, float)):
                raise ParameterConfigError(
                    f"Parameter '{param_name}' value at index {i} must be a number in {file_path}, got {type(value).__name__}"
                )


def expand_parameter_combinations(parameters: Dict[str, List]) -> List[Dict[str, float]]:
    """
    Expand parameter ranges into all possible combinations.

    For example, if parameters are:
        {"A": [1, 2], "B": [10, 20]}

    This returns:
        [
            {"A": 1, "B": 10},
            {"A": 1, "B": 20},
            {"A": 2, "B": 10},
            {"A": 2, "B": 20}
        ]

    Args:
        parameters: Dictionary of parameter names to lists of values to test

    Returns:
        List of dictionaries, each representing one combination of parameter values
    """
    import itertools

    # Get parameter names and their value lists
    param_names = sorted(parameters.keys())  # Sort for consistent ordering
    value_lists = [parameters[name] for name in param_names]

    # Generate all combinations
    combinations = []
    for value_combo in itertools.product(*value_lists):
        combo_dict = dict(zip(param_names, value_combo))
        combinations.append(combo_dict)

    return combinations


def get_num_combinations(parameters: Dict[str, List]) -> int:
    """
    Calculate the total number of parameter combinations without generating them.

    Args:
        parameters: Dictionary of parameter names to lists of values

    Returns:
        Total number of combinations
    """
    total = 1
    for value_list in parameters.values():
        total *= len(value_list)
    return total


def load_and_expand_config(json_path: str) -> tuple:
    """
    Load a configuration file and expand it into all parameter combinations.

    This is a convenience function that combines load_parameter_config and
    expand_parameter_combinations.

    Args:
        json_path: Path to JSON configuration file

    Returns:
        Tuple of (config_dict, combinations_list) where:
        - config_dict: The full configuration (including name and description)
        - combinations_list: List of all parameter combinations to test
    """
    config = load_parameter_config(json_path)
    combinations = expand_parameter_combinations(config['parameters'])

    return config, combinations


# Convenience function for quick validation without loading
def validate_config_file(json_path: str) -> bool:
    """
    Validate a configuration file without loading combinations.

    Args:
        json_path: Path to JSON configuration file

    Returns:
        True if valid, raises ParameterConfigError if invalid
    """
    load_parameter_config(json_path)
    return True
