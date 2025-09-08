# =============================================================================
# DRAFT HELPER CONSTANTS - MIGRATED TO CONFIG.PY
# =============================================================================
"""
This file now imports constants from the centralized config.py file.
All frequently modified constants have been moved to config.py for easier management.

To modify constants, edit config.py instead of this file.
"""

import sys
from pathlib import Path

# Add parent directory to path to import config
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Import all constants from centralized config
from config import (
    # Logging
    LOGGING_ENABLED, LOGGING_LEVEL, LOGGING_TO_FILE, LOGGING_FILE,
    
    # File paths  
    PLAYERS_CSV,
    
    # Mode configuration
    TRADE_HELPER_MODE, RECOMMENDATION_COUNT,
    
    # Position constants
    RB, WR, QB, TE, K, DST, FLEX,
    
    # Roster construction
    MAX_POSITIONS, MAX_PLAYERS, FLEX_ELIGIBLE_POSITIONS,
    
    # Draft strategy
    DRAFT_ORDER, get_ideal_draft_position,
    
    # Scoring weights
    POS_NEEDED_SCORE, PROJECTION_BASE_SCORE, INJURY_PENALTIES,
    BASE_BYE_PENALTY, POSSIBLE_BYE_WEEKS, MIN_TRADE_IMPROVEMENT
)

# Adjust file path for draft_helper subdirectory context
PLAYERS_CSV = '../' + PLAYERS_CSV