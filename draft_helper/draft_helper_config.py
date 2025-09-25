#!/usr/bin/env python3
"""
Draft Helper Configuration

This file contains all the frequently modified constants for the draft helper.
Most important and frequently modified settings are at the top.

Author: Generated for NFL Fantasy Data Collection
Last Updated: September 2025
"""

from typing import Dict, List

# =============================================================================
# MOST FREQUENTLY MODIFIED SETTINGS
# =============================================================================
# Mode Configuration (FREQUENTLY MODIFIED)
TRADE_HELPER_MODE = False       # True for trade helper, False for draft helper
RECOMMENDATION_COUNT = 10        # Number of players to recommend

# Trade Mode Injury Settings (FREQUENTLY MODIFIED)
APPLY_INJURY_PENALTY_TO_ROSTER = False  # True to apply injury penalties to roster players (drafted=2), False to ignore injury penalties for roster players only

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
POS_NEEDED_SCORE = 65           # ← Weight for positional need (optimized from simulation)
PROJECTION_BASE_SCORE = 95      # ← Base score for projections (optimized from simulation)

# Penalty system (FREQUENTLY MODIFIED)
BASE_BYE_PENALTY = 5           # ← Base penalty for bye week conflicts (optimized from simulation)

INJURY_PENALTIES = {           # ← Risk tolerance settings (optimized from simulation)
    "LOW": 0,                  # Healthy/Active players
    "MEDIUM": 15,              # ← Optimized from simulation (was 25)
    "HIGH": 35                 # ← Optimized from simulation (was 50)
}

# Trade optimization settings (FREQUENTLY MODIFIED)
MIN_TRADE_IMPROVEMENT = 15     # ← Minimum point improvement required for a trade to be considered
NUM_TRADE_RUNNERS_UP = 3      # ← Number of runner-up trades to show for each player

# Bye weeks for NFL season
POSSIBLE_BYE_WEEKS = [5, 6, 7, 8, 9, 10, 11, 12, 14]

# =============================================================================
# FILE PATHS
# =============================================================================

# Data paths
PLAYERS_CSV = '../shared_files/players.csv'  # Production player data

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

LOGGING_ENABLED = False         # ← Enable/disable logging
LOGGING_LEVEL = 'INFO'         # ← DEBUG, INFO, WARNING, ERROR, CRITICAL
LOGGING_TO_FILE = False        # ← Console vs file logging
LOGGING_FILE = './data/log.txt'

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

STRATEGY CHANGES:
1. TRADE_HELPER_MODE - Switch between draft and trade modes
2. RECOMMENDATION_COUNT - How many players to suggest
3. MIN_TRADE_IMPROVEMENT - Minimum point improvement to suggest a trade
4. APPLY_INJURY_PENALTY_TO_ROSTER - Apply injury penalties to roster players in trade mode

SCORING FORMAT CHANGES:
1. BASE_BYE_PENALTY - Higher in smaller leagues, lower in larger leagues
2. POS_NEEDED_SCORE - Weight for positional need in scoring

DEBUGGING/TUNING:
1. LOGGING_LEVEL = 'DEBUG' (detailed) vs 'INFO' (minimal)

🔧 HOW TO MODIFY:

To change draft strategy for RB-heavy approach:
    DRAFT_ORDER[0] = {RB: 1.2, FLEX: 0.8}  # Prioritize RB in round 1
    
To increase injury risk tolerance:
    INJURY_PENALTIES["HIGH"] = 25  # Reduce penalty for injured players
    
To adjust for 12-team league (more scarcity):
    BASE_BYE_PENALTY = 30  # Increase penalty for bye conflicts
    
To only consider significant trades:
    MIN_TRADE_IMPROVEMENT = 15  # Only suggest trades with 15+ point improvement

To ignore injury penalties for roster players in trade analysis:
    APPLY_INJURY_PENALTY_TO_ROSTER = False  # Score roster players as if healthy

⚠️ VALIDATION:
Configuration is automatically validated on import. Invalid settings will
raise ValueError with details about what needs to be fixed.
"""