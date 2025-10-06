# =============================================================================
# DRAFT HELPER CONSTANTS - MIGRATED TO CONFIG.PY
# =============================================================================
"""
This file now imports constants from the centralized config.py file.
All frequently modified constants have been moved to config.py for easier management.

To modify constants, edit config.py instead of this file.
"""

import os
import sys

# Add current directory to path to ensure we import the local config.py
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import all constants from script-specific config  
from shared_files.configs.draft_helper_config import (
    # Logging
    LOGGING_ENABLED, LOGGING_LEVEL, LOGGING_TO_FILE, LOGGING_FILE,
    
    # File paths  
    PLAYERS_CSV,
    
    # Mode configuration
    TRADE_HELPER_MODE, RECOMMENDATION_COUNT, APPLY_INJURY_PENALTY_TO_ROSTER,
    
    # Position constants
    RB, WR, QB, TE, K, DST, FLEX,
    
    # Roster construction
    MAX_POSITIONS, MAX_PLAYERS, FLEX_ELIGIBLE_POSITIONS,
    
    # Draft strategy
    DRAFT_ORDER, get_ideal_draft_position,

    # Non-parameter settings (parameters now loaded via ParameterJsonManager)
    POSSIBLE_BYE_WEEKS, MIN_TRADE_IMPROVEMENT,
    NUM_TRADE_RUNNERS_UP
)

# Note: The following parameters are now loaded from JSON via ParameterJsonManager:
# - NORMALIZATION_MAX_SCALE
# - INJURY_PENALTIES (nested dict)
# - BASE_BYE_PENALTY
# - DRAFT_ORDER_PRIMARY_BONUS
# - DRAFT_ORDER_SECONDARY_BONUS
# - ADP multipliers
# - Player rating multipliers
# - Team quality multipliers
# - Matchup multipliers
# - Consistency multipliers

# Path is already correct in the script-specific config, no adjustment needed