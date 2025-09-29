#!/usr/bin/env python3
"""
Starter Helper Configuration

This file contains all the frequently modified constants for the starter helper.
Most important and frequently modified settings are at the top.

Author: Generated for NFL Fantasy Data Collection
Last Updated: September 2025
"""

from typing import Dict, List

# =============================================================================
# SHARED VARIABLES (imported from shared_config.py)
# =============================================================================

# Import shared NFL season/week variables from central location
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from shared_config import CURRENT_NFL_WEEK, NFL_SEASON, NFL_SCORING_FORMAT
from shared_files.validation_utils import ValidationResult, ConfigValidator, validate_multiple

# =============================================================================
# STARTER HELPER SPECIFIC SETTINGS
# =============================================================================

# Position Constants
RB, WR, QB, TE, K, DST, FLEX = 'RB', 'WR', 'QB', 'TE', 'K', 'DST', 'FLEX'

# Starting Lineup Requirements (Start 7 Fantasy League)
STARTING_LINEUP_REQUIREMENTS = {
    QB: 1,      # 1 Quarterback
    RB: 2,      # 2 Running Backs
    WR: 2,      # 2 Wide Receivers
    TE: 1,      # 1 Tight End
    FLEX: 1,    # 1 FLEX (Wide Receiver OR Running Back)
    K: 1,       # 1 Kicker
    DST: 1,     # 1 Defense/Special Teams
}

FLEX_ELIGIBLE_POSITIONS = [RB, WR]  # Positions eligible for FLEX spot

# Display Configuration (FREQUENTLY MODIFIED)
SHOW_PROJECTION_DETAILS = True      # Show detailed projection info
SHOW_INJURY_STATUS = True           # Show injury status in recommendations
RECOMMENDATION_COUNT = 15           # Number of total players to show

# =============================================================================
# POSITIONAL RANKING CONFIGURATION
# =============================================================================

# Positional ranking adjustments are handled automatically via positional_ranking_calculator.py
# which uses team offensive/defensive rankings from teams.csv to apply score adjustments

# =============================================================================
# ESPN API CONFIGURATION
# =============================================================================

# ESPN API settings for current week projections
ESPN_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
REQUEST_TIMEOUT = 30
RATE_LIMIT_DELAY = 0.2

# Current week projection settings
USE_CURRENT_WEEK_PROJECTIONS = True  # Fetch fresh current week projections
FALLBACK_TO_SEASON_PROJECTIONS = True  # Use season projections if current week unavailable


# =============================================================================
# FILE PATHS
# =============================================================================

# Data paths
PLAYERS_CSV = '../shared_files/players.csv'
DATA_DIR = './data'

# =============================================================================
# FILE OUTPUT CONFIGURATION
# =============================================================================

# Output file settings (FREQUENTLY MODIFIED)
SAVE_OUTPUT_TO_FILE = True          # Enable/disable file output
OUTPUT_FILE_PREFIX = 'starter_results'  # Prefix for output files
LATEST_FILE_NAME = 'starter_results_latest.txt'  # Latest results file name

# File paths (auto-generated based on above settings)
def get_timestamped_filename():
    """Generate timestamped filename for current run"""
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return f"{OUTPUT_FILE_PREFIX}_{timestamp}.txt"

def get_latest_filepath():
    """Get path to latest results file"""
    return f"{DATA_DIR}/{LATEST_FILE_NAME}"

def get_timestamped_filepath():
    """Get path to timestamped results file"""
    return f"{DATA_DIR}/{get_timestamped_filename()}"

# =============================================================================
# SCORING AND PENALTIES
# =============================================================================

# Injury status penalties for starter recommendations (FREQUENTLY MODIFIED)
INJURY_PENALTIES = {
    "ACTIVE": 0,           # Healthy/Active players
    "LOW": 0,              # Healthy players
    "MEDIUM": 0,           # ← Often adjusted (Questionable, Day-to-Day)
    "HIGH": 50,            # ← Often adjusted (Doubtful)
    "OUT": 100,            # Out for the week (should not start)
    "INJURY_RESERVE": 100, # On IR (should not start)
    "SUSPENSION": 100,     # Suspended (should not start)
    "DOUBTFUL": 50,        # Doubtful to play
    "QUESTIONABLE": 0,     # Questionable to play
}

# Bye week penalty (should not start players on bye)
BYE_WEEK_PENALTY = 1000

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

LOGGING_ENABLED = True          # ← Enable/disable logging
LOGGING_LEVEL = 'INFO'         # ← DEBUG, INFO, WARNING, ERROR, CRITICAL
LOGGING_TO_FILE = False        # ← Console vs file logging
LOGGING_FILE = './data/log.txt'

# =============================================================================
# CONFIGURATION VALIDATION
# =============================================================================

def validate_config():
    """Validate configuration settings using shared validation utilities"""
    def validate_basic_settings():
        result = ValidationResult()

        # Validate scoring format
        valid_formats = ["ppr", "std", "half"]
        if NFL_SCORING_FORMAT not in valid_formats:
            result.add_error(f"Invalid NFL_SCORING_FORMAT: {NFL_SCORING_FORMAT}. Valid options: {valid_formats}", "NFL_SCORING_FORMAT", NFL_SCORING_FORMAT)

        # Validate current NFL week
        week_result = ConfigValidator.validate_range(CURRENT_NFL_WEEK, 1, 18, "CURRENT_NFL_WEEK")
        result.errors.extend(week_result.errors)

        # Validate NFL season
        season_result = ConfigValidator.validate_range(NFL_SEASON, 2020, 2030, "NFL_SEASON")
        result.errors.extend(season_result.errors)

        return result

    def validate_lineup_requirements():
        result = ValidationResult()

        # Validate required positions are present
        required_positions = [QB, RB, WR, TE, FLEX, K, DST]
        for pos in required_positions:
            if pos not in STARTING_LINEUP_REQUIREMENTS:
                result.add_error(f"Missing position in STARTING_LINEUP_REQUIREMENTS: {pos}", "STARTING_LINEUP_REQUIREMENTS")

        # Validate position requirements are positive
        for position, count in STARTING_LINEUP_REQUIREMENTS.items():
            pos_result = ConfigValidator.validate_range(count, 0, 5, f"STARTING_LINEUP_REQUIREMENTS[{position}]")
            result.errors.extend(pos_result.errors)

        # Validate FLEX eligible positions
        if not FLEX_ELIGIBLE_POSITIONS:
            result.add_error("FLEX_ELIGIBLE_POSITIONS cannot be empty", "FLEX_ELIGIBLE_POSITIONS")

        return result

    def validate_penalty_settings():
        result = ValidationResult()

        # Validate injury penalties
        for injury_status, penalty in INJURY_PENALTIES.items():
            penalty_result = ConfigValidator.validate_range(penalty, 0, 1000, f"INJURY_PENALTIES[{injury_status}]")
            result.errors.extend(penalty_result.errors)

        # Validate bye week penalty
        bye_result = ConfigValidator.validate_range(BYE_WEEK_PENALTY, 0, 10000, "BYE_WEEK_PENALTY")
        result.errors.extend(bye_result.errors)

        return result

    def validate_display_settings():
        result = ValidationResult()

        # Validate recommendation count
        rec_result = ConfigValidator.validate_range(RECOMMENDATION_COUNT, 1, 100, "RECOMMENDATION_COUNT")
        result.errors.extend(rec_result.errors)

        # Validate API timeout settings
        timeout_result = ConfigValidator.validate_range(REQUEST_TIMEOUT, 1, 300, "REQUEST_TIMEOUT")
        result.errors.extend(timeout_result.errors)

        delay_result = ConfigValidator.validate_range(RATE_LIMIT_DELAY, 0.0, 10.0, "RATE_LIMIT_DELAY")
        result.errors.extend(delay_result.errors)

        return result

    # Run all validations
    combined_result = validate_multiple([
        validate_basic_settings,
        validate_lineup_requirements,
        validate_penalty_settings,
        validate_display_settings
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
1. CURRENT_NFL_WEEK - Update every Tuesday for the upcoming week (1-18)

STRATEGY CHANGES:
1. INJURY_PENALTIES - Adjust risk tolerance for questionable players
2. SHOW_PROJECTION_DETAILS - Show/hide detailed projection information

POSITIONAL RANKING:
1. Team rankings are automatically loaded from teams.csv
2. Adjustments are applied based on offensive/defensive rankings
3. Configuration is handled in positional_ranking_calculator.py
4. RECOMMENDATION_COUNT - Number of players to display

FILE OUTPUT:
1. SAVE_OUTPUT_TO_FILE - Enable/disable saving results to files
2. OUTPUT_FILE_PREFIX - Change the prefix for output file names

LEAGUE SETTINGS:
1. STARTING_LINEUP_REQUIREMENTS - Adjust for different league formats
2. NFL_SCORING_FORMAT - PPR vs Standard vs Half-PPR

DEBUGGING:
1. LOGGING_LEVEL = 'DEBUG' (detailed) vs 'INFO' (minimal)

🔧 HOW TO MODIFY:

To be more conservative with injuries:
    INJURY_PENALTIES["QUESTIONABLE"] = 10  # Higher penalty for questionable players

To show more/fewer recommendations:
    RECOMMENDATION_COUNT = 20  # Show more players

To adjust for standard scoring:
    NFL_SCORING_FORMAT = "std"

To configure positional ranking adjustments:
    Edit positional_ranking_calculator.py configuration

⚠️ VALIDATION:
Configuration is automatically validated on import. Invalid settings will
raise ValueError with details about what needs to be fixed.
"""