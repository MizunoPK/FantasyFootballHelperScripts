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
# MOST FREQUENTLY MODIFIED SETTINGS
# =============================================================================

# Week Configuration (FREQUENTLY MODIFIED)
CURRENT_NFL_WEEK = 3  # Current NFL week for projections (1-18, update weekly)
NFL_SEASON = 2025
NFL_SCORING_FORMAT = "ppr"  # "ppr", "std", or "half"

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
    "QUESTIONABLE": 5,     # Questionable to play
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
3. RECOMMENDATION_COUNT - Number of players to display

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