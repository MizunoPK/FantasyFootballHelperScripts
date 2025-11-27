"""
League Helper Constants

Centralized constants for the Fantasy Football League Helper application.
Defines logging configuration, roster structure, position limits, and
other application-wide settings.

This module provides:
- Logging configuration (level, format, output)
- Position constants (QB, RB, WR, TE, K, DST, FLEX)
- Mode-specific constants (waiver optimizer, recommendations)

Note: Roster construction limits (MAX_POSITIONS, MAX_PLAYERS) and FLEX-eligible
positions (FLEX_ELIGIBLE_POSITIONS) moved to league_config.json

Author: Kai Mizuno
"""

FANTASY_TEAM_NAME = "Sea Sharp"

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================
LOGGING_LEVEL = 'INFO'      # DEBUG, INFO, WARNING, ERROR, CRITICAL (WARNING+ to reduce spam)
LOGGING_TO_FILE = False        # Console vs file logging
LOG_NAME = "league_helper"     # Logger name
LOGGING_FILE = './data/log.txt'  # Log file path (if LOGGING_TO_FILE=True)
LOGGING_FORMAT = 'detailed'    # detailed / standard / simple

# =============================================================================
# GENERAL SETTINGS
# =============================================================================
RECOMMENDATION_COUNT = 10  # Number of player recommendations to display

# =============================================================================
# WAIVER OPTIMIZER CONSTANTS
# =============================================================================
MIN_WAIVER_IMPROVEMENT = 0  # Minimum score improvement to suggest a trade
NUM_TRADE_RUNNERS_UP = 9   # Number of alternative trade suggestions to show

# Minimum position requirements for trade validation
# Applies to Waiver Optimizer and Trade Suggestor modes
# Ensures trades don't leave user's team below minimum thresholds
# Note: Counts total players by position (including FLEX assignments)
# Note: No FLEX entry - FLEX-eligible players counted toward natural position
MIN_POSITIONS = {
    "QB": 1,
    "RB": 3,
    "WR": 3,
    "TE": 1,
    "K": 1,
    "DST": 1
}

# TRADE SUGGESTOR
MIN_TRADE_IMPROVEMENT = 0
VALID_TEAMS = ["Fishoutawater", "Chase-ing points", "Annihilators", "The Injury Report", "Striking Shibas", "Bo Him-ian Rhapsody", "Saquon Deez", "The Eskimo Brothers", "Pidgin"]
# VALID_TEAMS = ["Fishoutawater"]

# =============================================================================
# POSITION CONSTANTS
# =============================================================================
RB, WR, QB, TE, K, DST, FLEX = 'RB', 'WR', 'QB', 'TE', 'K', 'DST', 'FLEX'

# Position groupings for scoring calculations
ALL_POSITIONS = [RB, WR, QB, TE, K, DST]
OFFENSE_POSITIONS = ["QB", "RB", "WR", "TE", "K"]  # Offensive positions
DEFENSE_POSITIONS = ["DEF", "DST", "D/ST"]         # Defensive position variations

# Wind-affected positions (passing game and kicking affected by wind)
# Wind scoring only applies to these positions
WIND_AFFECTED_POSITIONS = ["QB", "WR", "K"]

# =============================================================================
# ROSTER CONSTRUCTION
# =============================================================================
# NOTE: MAX_POSITIONS, MAX_PLAYERS, and FLEX_ELIGIBLE_POSITIONS have been moved
# to league_config.json for runtime configuration. Access via:
# - ConfigManager.max_positions
# - ConfigManager.max_players
# - ConfigManager.flex_eligible_positions
# - ConfigManager.get_position_with_flex(position)

# =============================================================================
# BYE WEEKS
# =============================================================================
# Weeks in which NFL teams have bye weeks (no game)
POSSIBLE_BYE_WEEKS = [5, 6, 7, 8, 9, 10, 11, 12, 14]