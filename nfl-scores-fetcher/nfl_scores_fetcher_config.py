#!/usr/bin/env python3
"""
NFL Scores Fetcher Configuration

This file contains all the frequently modified constants for the NFL scores fetcher.
Most important and frequently modified settings are at the top.

Author: Kai Mizuno
Last Updated: September 2025
"""

# =============================================================================
# SHARED VARIABLES (imported from shared_config.py)
# =============================================================================

# Import shared NFL season/week variables from central location
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from shared_config import CURRENT_NFL_WEEK, NFL_SEASON
from shared_files.validation_utils import ValidationResult, ConfigValidator, validate_multiple

# Map shared variables to local names for backwards compatibility
NFL_SCORES_SEASON = NFL_SEASON
NFL_SCORES_CURRENT_WEEK = CURRENT_NFL_WEEK

# =============================================================================
# NFL SCORES FETCHER SPECIFIC SETTINGS
# =============================================================================

# NFL Scores Settings (FREQUENTLY MODIFIED)
NFL_SCORES_SEASON_TYPE = 2
NFL_SCORES_ONLY_COMPLETED_GAMES = False

# Output Settings (FREQUENTLY MODIFIED)
OUTPUT_DIRECTORY = "./data"
CREATE_CSV = True
CREATE_JSON = False
CREATE_EXCEL = True

# =============================================================================
# API CONFIGURATION
# =============================================================================

# API settings
REQUEST_TIMEOUT = 30
RATE_LIMIT_DELAY = 0.2

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

LOGGING_ENABLED = False         # ← Enable/disable logging
LOGGING_LEVEL = 'INFO'         # ← DEBUG, INFO, WARNING, ERROR, CRITICAL
LOGGING_TO_FILE = False        # ← Console vs file logging
LOGGING_FILE = './data/log.txt'

# =============================================================================
# CONFIGURATION VALIDATION
# =============================================================================

def validate_config():
    """Validate configuration settings using shared validation utilities"""
    def validate_basic_settings():
        """
        Validate basic NFL settings like season, week, and season type.

        Returns:
            ValidationResult: Result object containing any validation errors
        """
        result = ValidationResult()

        # Validate NFL season
        season_result = ConfigValidator.validate_range(NFL_SCORES_SEASON, 2020, 2030, "NFL_SCORES_SEASON")
        result.errors.extend(season_result.errors)

        # Validate current NFL week
        week_result = ConfigValidator.validate_range(NFL_SCORES_CURRENT_WEEK, 1, 22, "NFL_SCORES_CURRENT_WEEK")
        result.errors.extend(week_result.errors)

        # Validate season type
        valid_season_types = [1, 2, 3, 4]
        if NFL_SCORES_SEASON_TYPE not in valid_season_types:
            result.add_error(
                f"NFL_SCORES_SEASON_TYPE must be 1 (preseason), 2 (regular), 3 (postseason), or 4 (off-season). Got: {NFL_SCORES_SEASON_TYPE}",
                "NFL_SCORES_SEASON_TYPE", NFL_SCORES_SEASON_TYPE
            )

        return result

    def validate_api_settings():
        """
        Validate API-related settings like timeouts and rate limits.

        Returns:
            ValidationResult: Result object containing any validation errors
        """
        result = ValidationResult()

        # Validate timeout settings
        timeout_result = ConfigValidator.validate_range(REQUEST_TIMEOUT, 1, 300, "REQUEST_TIMEOUT")
        result.errors.extend(timeout_result.errors)

        delay_result = ConfigValidator.validate_range(RATE_LIMIT_DELAY, 0.0, 10.0, "RATE_LIMIT_DELAY")
        result.errors.extend(delay_result.errors)

        return result

    # Run all validations
    combined_result = validate_multiple([
        validate_basic_settings,
        validate_api_settings
    ])

    if not combined_result.is_valid:
        error_messages = combined_result.get_error_messages()
        raise ValueError(f"Configuration validation failed: {'; '.join(error_messages)}")

# Run validation on import
if __name__ != "__main__":
    validate_config()

# =============================================================================
# QUICK CONFIGURATION GUIDE
# =============================================================================
"""
🎯 MOST FREQUENTLY MODIFIED SETTINGS:

WEEKLY CHANGES:
1. NFL_SCORES_CURRENT_WEEK - Update for current NFL week
2. NFL_SCORES_ONLY_COMPLETED_GAMES - True for final scores, False for live updates

SEASON CHANGES:
1. NFL_SCORES_SEASON - Update for current year
2. NFL_SCORES_SEASON_TYPE - 1 (preseason), 2 (regular), 3 (postseason), 4 (off-season)

OUTPUT CHANGES:
1. CREATE_EXCEL/CREATE_CSV/CREATE_JSON - Control output formats
2. OUTPUT_DIRECTORY - Change where files are saved

DEBUGGING:
1. LOGGING_LEVEL = 'DEBUG' (detailed) vs 'INFO' (minimal)
2. LOGGING_TO_FILE = True (save logs to file)

⚠️ VALIDATION:
Configuration is automatically validated on import. Invalid settings will
raise ValueError with details about what needs to be fixed.
"""