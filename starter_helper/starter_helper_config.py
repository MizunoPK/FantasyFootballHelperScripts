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
# MATCHUP ANALYSIS CONFIGURATION (NEW)
# =============================================================================

# Matchup Analysis Toggle (FREQUENTLY MODIFIED)
ENABLE_MATCHUP_ANALYSIS = True       # Enable/disable matchup analysis
SHOW_MATCHUP_SIMPLE = True           # Show simple matchup ratings (★/⚠️ indicators)
SHOW_MATCHUP_DETAILED = True        # Show detailed matchup analysis breakdown

# Matchup Calculation Settings (FREQUENTLY MODIFIED)
MATCHUP_WEIGHT_FACTOR = 1.0         # Impact of matchup on recommendations (0.0-1.0)
RECENT_WEEKS_FOR_DEFENSE = 4         # Weeks for defensive trend analysis
FAVORABLE_MATCHUP_THRESHOLD = 65.0   # Threshold for "favorable" matchup (1-100)
HOME_FIELD_ADVANTAGE_BONUS = 5.0     # Rating bonus for home games

# Rating Component Weights (must sum to 1.0)
DEFENSE_STRENGTH_WEIGHT = 0.40       # Opponent defense strength vs position
RECENT_TREND_WEIGHT = 0.30           # Recent defensive performance trend
HOME_FIELD_WEIGHT = 0.15             # Home/away advantage factor
SCHEDULE_STRENGTH_WEIGHT = 0.15      # Strength of schedule adjustment

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

# Matchup Analysis ESPN API Settings
MATCHUP_REQUEST_TIMEOUT = 30         # Timeout for matchup analysis API requests
MATCHUP_RATE_LIMIT_DELAY = 0.3       # Delay between matchup API requests (seconds)
MAX_CONCURRENT_MATCHUP_REQUESTS = 5  # Maximum concurrent ESPN API requests

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
    "MEDIUM": 5,           # ← Often adjusted (Questionable, Day-to-Day)
    "HIGH": 15,            # ← Often adjusted (Doubtful)
    "OUT": 100,            # Out for the week (should not start)
    "INJURY_RESERVE": 100, # On IR (should not start)
    "SUSPENSION": 100,     # Suspended (should not start)
    "DOUBTFUL": 15,        # Doubtful to play
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
    """Validate configuration settings"""
    errors = []

    if NFL_SCORING_FORMAT not in ["ppr", "std", "half"]:
        errors.append(f"Invalid NFL_SCORING_FORMAT: {NFL_SCORING_FORMAT}")

    if CURRENT_NFL_WEEK < 1 or CURRENT_NFL_WEEK > 18:
        errors.append(f"Invalid CURRENT_NFL_WEEK: {CURRENT_NFL_WEEK}")

    required_positions = [QB, RB, WR, TE, FLEX, K, DST]
    for pos in required_positions:
        if pos not in STARTING_LINEUP_REQUIREMENTS:
            errors.append(f"Missing position in STARTING_LINEUP_REQUIREMENTS: {pos}")

    if not FLEX_ELIGIBLE_POSITIONS:
        errors.append("FLEX_ELIGIBLE_POSITIONS cannot be empty")

    # Validate matchup analysis settings
    if ENABLE_MATCHUP_ANALYSIS:
        if MATCHUP_WEIGHT_FACTOR < 0 or MATCHUP_WEIGHT_FACTOR > 1:
            errors.append(f"MATCHUP_WEIGHT_FACTOR must be between 0 and 1: {MATCHUP_WEIGHT_FACTOR}")

        if FAVORABLE_MATCHUP_THRESHOLD < 1 or FAVORABLE_MATCHUP_THRESHOLD > 100:
            errors.append(f"FAVORABLE_MATCHUP_THRESHOLD must be between 1 and 100: {FAVORABLE_MATCHUP_THRESHOLD}")

        if RECENT_WEEKS_FOR_DEFENSE < 1 or RECENT_WEEKS_FOR_DEFENSE > 10:
            errors.append(f"RECENT_WEEKS_FOR_DEFENSE must be between 1 and 10: {RECENT_WEEKS_FOR_DEFENSE}")

        # Validate that rating weights sum to approximately 1.0
        total_weight = (DEFENSE_STRENGTH_WEIGHT + RECENT_TREND_WEIGHT +
                       HOME_FIELD_WEIGHT + SCHEDULE_STRENGTH_WEIGHT)
        if abs(total_weight - 1.0) > 0.01:
            errors.append(f"Matchup rating weights must sum to 1.0, got {total_weight}")

    if errors:
        raise ValueError(f"Configuration validation failed: {'; '.join(errors)}")

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

MATCHUP ANALYSIS (NEW):
1. ENABLE_MATCHUP_ANALYSIS - Turn matchup analysis on/off
2. MATCHUP_WEIGHT_FACTOR - How much matchups impact recommendations (0.0-1.0)
3. SHOW_MATCHUP_SIMPLE - Show basic matchup indicators (★/⚠️)
4. SHOW_MATCHUP_DETAILED - Show detailed matchup breakdown
5. FAVORABLE_MATCHUP_THRESHOLD - What rating counts as "favorable" (1-100)
3. RECOMMENDATION_COUNT - Number of players to display

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

⚠️ VALIDATION:
Configuration is automatically validated on import. Invalid settings will
raise ValueError with details about what needs to be fixed.
"""