#!/usr/bin/env python3
"""
Centralized Configuration for Fantasy Football Helper Scripts

This file contains all the frequently modified constants across different modules.
Consolidates settings from draft_helper_constants.py, player_data_constants.py, and .env
"""

from dataclasses import dataclass
from typing import Dict, List

# =============================================================================
# SEASON & DATA CONFIGURATION
# =============================================================================

# Season settings (from .env)
NFL_SEASON = 2025
NFL_SCORING_FORMAT = "ppr"  # "ppr", "std", or "half"

# Data paths and preservation
PLAYERS_CSV = 'shared_files/players.csv'
PRESERVE_DRAFTED_VALUES = True   # Keep draft status between data updates
PRESERVE_LOCKED_VALUES = True    # Keep locked players between data updates

# Output settings (from .env)
OUTPUT_DIRECTORY = "./data"
CREATE_CSV = True
CREATE_JSON = False
CREATE_EXCEL = True
CREATE_CONDENSED_EXCEL = True

# API settings (from .env)
REQUEST_TIMEOUT = 30
RATE_LIMIT_DELAY = 0.2

# =============================================================================
# DRAFT/TRADE STRATEGY CONFIGURATION
# =============================================================================

# Mode Configuration
TRADE_HELPER_MODE = True         # True for trade helper, False for draft helper
RECOMMENDATION_COUNT = 10        # Number of players to recommend

# Position Constants
RB, WR, QB, TE, K, DST, FLEX = 'RB', 'WR', 'QB', 'TE', 'K', 'DST', 'FLEX'

# Roster Construction (FREQUENTLY MODIFIED)
MAX_POSITIONS = {
    QB: 2,      # ← Adjust for league settings
    RB: 4,      # ← Adjust based on strategy
    WR: 4,      # ← Adjust based on strategy  
    FLEX: 1,    # FLEX can be RB or WR
    TE: 2,      # ← Sometimes adjusted
    K: 1,       # ← Rarely changes
    DST: 1,     # ← Rarely changes
}
MAX_PLAYERS = 15  # Total roster size

FLEX_ELIGIBLE_POSITIONS = [RB, WR]  # Positions eligible for FLEX spot

# Draft Strategy - Ideal position priorities by round (FREQUENTLY MODIFIED)
DRAFT_ORDER = [
    {FLEX: 1.0, QB: 0.7},    # Round 1
    {FLEX: 1.0, QB: 0.7},    # Round 2  
    {FLEX: 1.0, QB: 0.8},    # Round 3
    {FLEX: 1.0, QB: 0.8},    # Round 4
    {QB: 1.0, FLEX: 0.7},    # Round 5
    {TE: 1.0, FLEX: 0.7},    # Round 6
    {FLEX: 1.0},             # Round 7
    {QB: 1.0, FLEX: 0.7},    # Round 8
    {TE: 1.0, FLEX: 0.7},    # Round 9
    {FLEX: 1.0},             # Round 10
    {FLEX: 1.0},             # Round 11
    {K: 1.0},                # Round 12
    {DST: 1.0},              # Round 13
    {FLEX: 1.0},             # Round 14
    {FLEX: 1.0}              # Round 15
]

# =============================================================================
# SCORING WEIGHTS (FREQUENTLY MODIFIED)
# =============================================================================

# Primary scoring components
POS_NEEDED_SCORE = 50           # ← Weight for positional need
PROJECTION_BASE_SCORE = 100     # ← Base score for projections

# Penalty system (FREQUENTLY MODIFIED)
BASE_BYE_PENALTY = 20          # ← Base penalty for bye week conflicts

INJURY_PENALTIES = {           # ← Risk tolerance settings
    "LOW": 0,                  # Healthy/Active players
    "MEDIUM": 25,              # ← Often adjusted (Questionable, etc.)
    "HIGH": 50                 # ← Often adjusted (Out, IR, etc.)
}

# Trade optimization settings (FREQUENTLY MODIFIED)
MIN_TRADE_IMPROVEMENT = 5     # ← Minimum point improvement required for a trade to be considered

# Bye weeks for NFL season
POSSIBLE_BYE_WEEKS = [5, 6, 7, 8, 9, 10, 11, 12, 14]

# =============================================================================
# PLAYER DATA FETCHER CONFIGURATION
# =============================================================================

# ESPN API Configuration
ESPN_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
ESPN_PLAYER_LIMIT = 2000

# Export configuration
EXCEL_POSITION_SHEETS = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']
EXPORT_COLUMNS = [
    'id', 'name', 'team', 'position', 'bye_week', 'fantasy_points',
    'injury_status', 'drafted', 'locked'
]

# =============================================================================
# FALLBACK FANTASY POINTS (FREQUENTLY MODIFIED)
# =============================================================================

@dataclass
class PositionFallbackConfig:
    """Configuration for position-specific ADP fallback calculations"""
    base_points: float
    multiplier: float

# Position-specific fallback when ADP data is missing (FREQUENTLY MODIFIED)
# Format: max(1.0, base_points - (adp * multiplier))
POSITION_FALLBACK_CONFIG: Dict[str, PositionFallbackConfig] = {
    'QB': PositionFallbackConfig(base_points=300, multiplier=1.5),   # ← Adjust for scoring format
    'RB': PositionFallbackConfig(base_points=250, multiplier=1.2),   # ← Adjust based on league trends
    'WR': PositionFallbackConfig(base_points=240, multiplier=1.1),   # ← Adjust based on league trends
    'TE': PositionFallbackConfig(base_points=180, multiplier=0.8),   # ← PPR vs Standard
    'K': PositionFallbackConfig(base_points=140, multiplier=0.3),    # ← Rarely changes
    'DST': PositionFallbackConfig(base_points=130, multiplier=0.3)   # ← Rarely changes
}

# Default fallback for unknown positions
DEFAULT_FALLBACK_CONFIG = PositionFallbackConfig(base_points=150, multiplier=0.8)

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

LOGGING_ENABLED = False         # ← Enable/disable logging
LOGGING_LEVEL = 'INFO'         # ← DEBUG, INFO, WARNING, ERROR, CRITICAL
LOGGING_TO_FILE = False        # ← Console vs file logging
LOGGING_FILE = './data/log.txt'

# =============================================================================
# NFL SCORES CONFIGURATION (from .env)
# =============================================================================

# NFL Scores settings
NFL_SCORES_SEASON = 2025
NFL_SCORES_SEASON_TYPE = 2
NFL_SCORES_CURRENT_WEEK = 1
NFL_SCORES_ONLY_COMPLETED_GAMES = False

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_ideal_draft_position(round_num: int) -> str:
    """Get the ideal position to draft in a given round"""
    if round_num < len(DRAFT_ORDER):
        best_position = max(DRAFT_ORDER[round_num], key=DRAFT_ORDER[round_num].get)
        return best_position
    return FLEX

# =============================================================================
# CONFIGURATION VALIDATION
# =============================================================================

def validate_config():
    """Validate configuration settings"""
    errors = []
    
    if not POSSIBLE_BYE_WEEKS:
        errors.append("POSSIBLE_BYE_WEEKS cannot be empty")
    
    if MAX_PLAYERS <= 0:
        errors.append("MAX_PLAYERS must be positive")
        
    if sum(MAX_POSITIONS.values()) < MAX_PLAYERS:
        errors.append("MAX_POSITIONS total should be >= MAX_PLAYERS")
        
    total_rounds = len(DRAFT_ORDER)
    if total_rounds != MAX_PLAYERS:
        errors.append(f"DRAFT_ORDER has {total_rounds} rounds but MAX_PLAYERS is {MAX_PLAYERS}")
    
    if NFL_SCORING_FORMAT not in ["ppr", "std", "half"]:
        errors.append(f"Invalid NFL_SCORING_FORMAT: {NFL_SCORING_FORMAT}")
        
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

WEEKLY/DRAFT SEASON CHANGES:
1. DRAFT_ORDER - Update strategy based on ADP trends and position scarcity
2. INJURY_PENALTIES["MEDIUM"]/["HIGH"] - Adjust risk tolerance for your league
3. MAX_POSITIONS - Adjust for different league roster requirements

SCORING FORMAT CHANGES (PPR vs Standard):
1. POSITION_FALLBACK_CONFIG - Adjust point values for different scoring
2. BASE_BYE_PENALTY - Higher in smaller leagues, lower in larger leagues

DEBUGGING/TUNING:
1. LOGGING_LEVEL = 'DEBUG' (detailed) vs 'INFO' (minimal)
2. TRADE_HELPER_MODE - Switch between draft and trade modes
3. RECOMMENDATION_COUNT - How many players to suggest
4. MIN_TRADE_IMPROVEMENT - Minimum point improvement to suggest a trade

SEASON SETUP:
1. NFL_SEASON - Update for current year
2. PRESERVE_DRAFTED_VALUES = False (reset), then True (maintain)

🔧 HOW TO MODIFY:

To change draft strategy for RB-heavy approach:
    DRAFT_ORDER[0] = {RB: 1.2, FLEX: 0.8}  # Prioritize RB in round 1
    
To increase injury risk tolerance:
    INJURY_PENALTIES["HIGH"] = 25  # Reduce penalty for injured players
    
To adjust for 12-team league (more scarcity):
    BASE_BYE_PENALTY = 30  # Increase penalty for bye conflicts
    
To only consider significant trades:
    MIN_TRADE_IMPROVEMENT = 15  # Only suggest trades with 15+ point improvement
    
📁 FILE ORGANIZATION:
- config.py: All frequently modified settings (THIS FILE)
- draft_helper_constants.py: Imports from config.py
- player_data_constants.py: Imports from config.py + ESPN mappings
- .env: Can be deleted (values moved here)

⚠️ VALIDATION:
Configuration is automatically validated on import. Invalid settings will
raise ValueError with details about what needs to be fixed.
"""
