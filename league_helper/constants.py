"""
League Helper Constants

Centralized constants for the Fantasy Football League Helper application.
Defines logging configuration, roster structure, position limits, and
other application-wide settings.

This module provides:
- Logging configuration (level, format, output)
- Position constants (QB, RB, WR, TE, K, DST, FLEX)
- Roster construction limits (MAX_POSITIONS, MAX_PLAYERS)
- Starting lineup requirements (Start 7 format)
- Bye week definitions
- Mode-specific constants (waiver optimizer, recommendations)

Author: Kai Mizuno
"""

FANTASY_TEAM_NAME = "Sea Sharp"

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================
LOGGING_LEVEL = 'WARNING'      # DEBUG, INFO, WARNING, ERROR, CRITICAL (WARNING+ to reduce spam)
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
MIN_TRADE_IMPROVEMENT = 0  # Minimum score improvement to suggest a trade
NUM_TRADE_RUNNERS_UP = 3   # Number of alternative trade suggestions to show
MIN_PLAYER_SCORE_TO_CONSIDER_TRADE = 40

# =============================================================================
# POSITION CONSTANTS
# =============================================================================
RB, WR, QB, TE, K, DST, FLEX = 'RB', 'WR', 'QB', 'TE', 'K', 'DST', 'FLEX'

# Position groupings for scoring calculations
OFFENSE_POSITIONS = ["QB", "RB", "WR", "TE", "K"]  # Offensive positions
DEFENSE_POSITIONS = ["DEF", "DST", "D/ST"]         # Defensive position variations

# =============================================================================
# ROSTER CONSTRUCTION
# =============================================================================
# Maximum players allowed per position on the roster
MAX_POSITIONS = {
    QB: 2,      # 2 Quarterbacks
    RB: 4,      # 4 Running Backs
    WR: 4,      # 4 Wide Receivers
    FLEX: 1,    # 1 FLEX (RB or WR only)
    TE: 2,      # 2 Tight Ends
    K: 1,       # 1 Kicker
    DST: 1,     # 1 Defense/Special Teams
}

# Total roster size (sum of MAX_POSITIONS values)
MAX_PLAYERS = 15

# Positions eligible for FLEX spot (RB or WR only)
FLEX_ELIGIBLE_POSITIONS = [RB, WR, DST]

def get_position_with_flex(position):
    """
    Determine if a position should be considered for FLEX assignment.

    Args:
        position (str): Player position (RB, WR, QB, TE, K, DST)

    Returns:
        str: FLEX if position is RB or WR, otherwise the original position

    Example:
        >>> get_position_with_flex('RB')
        'FLEX'
        >>> get_position_with_flex('QB')
        'QB'
    """
    if position in FLEX_ELIGIBLE_POSITIONS:
        return FLEX
    else:
        return position

# =============================================================================
# BYE WEEKS
# =============================================================================
# Weeks in which NFL teams have bye weeks (no game)
POSSIBLE_BYE_WEEKS = [5, 6, 7, 8, 9, 10, 11, 12, 14]

# =============================================================================
# SCORING CONFIGURATION
# =============================================================================
# Positions that receive matchup multiplier adjustments in scoring
# (Kickers and Defense excluded as they don't use matchup scoring)
MATCHUP_ENABLED_POSITIONS = [QB, RB, WR, TE]