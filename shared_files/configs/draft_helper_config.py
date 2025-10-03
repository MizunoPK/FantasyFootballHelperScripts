#!/usr/bin/env python3
"""
Draft Helper Configuration

This file contains all the frequently modified constants for the draft helper.
Most important and frequently modified settings are at the top.

Author: Kai Mizuno
Last Updated: September 2025
"""

from typing import Dict, List
import sys
from pathlib import Path

# Add parent directory to path for shared_files imports
sys.path.append(str(Path(__file__).parent.parent))
from shared_files.validation_utils import ValidationResult, ConfigValidator, validate_multiple

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

# DRAFT_ORDER bonus configuration (FREQUENTLY MODIFIED)
DRAFT_ORDER_PRIMARY_BONUS = 50    # Points for #1 priority position
DRAFT_ORDER_SECONDARY_BONUS = 25  # Points for #2 priority position

# Draft Strategy - Round-based position bonuses (FREQUENTLY MODIFIED)
# Uses DRAFT_ORDER_PRIMARY_BONUS and DRAFT_ORDER_SECONDARY_BONUS variables
# To adjust bonuses, modify the two variables above - changes apply to all rounds
P = DRAFT_ORDER_PRIMARY_BONUS    # Alias for readability
S = DRAFT_ORDER_SECONDARY_BONUS  # Alias for readability

DRAFT_ORDER = [
    {FLEX: P, QB: S},        # Round 1: FLEX priority, QB secondary
    {FLEX: P, QB: S},        # Round 2: FLEX priority, QB secondary
    {FLEX: P, QB: S+5},      # Round 3: FLEX priority, QB increasing (+5)
    {FLEX: P, QB: S+5},      # Round 4: FLEX priority, QB increasing (+5)
    {QB: P, FLEX: S},        # Round 5: QB priority, FLEX secondary
    {TE: P, FLEX: S},        # Round 6: TE priority, FLEX secondary
    {FLEX: P},               # Round 7: FLEX only
    {QB: P, FLEX: S},        # Round 8: QB priority, FLEX secondary
    {TE: P, FLEX: S},        # Round 9: TE priority, FLEX secondary
    {FLEX: P},               # Round 10: FLEX only
    {FLEX: P},               # Round 11: FLEX only
    {K: P},                  # Round 12: Kicker
    {DST: P},                # Round 13: Defense
    {FLEX: P},               # Round 14: FLEX
    {FLEX: P}                # Round 15: FLEX
]

# =============================================================================
# SCORING WEIGHTS (FREQUENTLY MODIFIED)
# =============================================================================

# Normalization configuration
NORMALIZATION_MAX_SCALE = 100.0  # ← Maximum value for normalized fantasy points (0-N scale)

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

LOGGING_ENABLED = True         # ← Enable/disable logging
LOGGING_LEVEL = 'WARNING'         # ← DEBUG, INFO, WARNING, ERROR, CRITICAL
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
    """Validate configuration settings using shared validation utilities"""
    def validate_basic_settings():
        """
        Validate basic settings like MAX_PLAYERS and bye weeks.

        Returns:
            ValidationResult: Result object containing any validation errors
        """
        result = ValidationResult()

        # Validate MAX_PLAYERS
        max_players_result = ConfigValidator.validate_range(MAX_PLAYERS, 1, 50, "MAX_PLAYERS")
        result.errors.extend(max_players_result.errors)

        # Validate that POSSIBLE_BYE_WEEKS is not empty
        if not POSSIBLE_BYE_WEEKS:
            result.add_error("POSSIBLE_BYE_WEEKS cannot be empty", "POSSIBLE_BYE_WEEKS")

        # Validate bye weeks are in valid range
        for week in POSSIBLE_BYE_WEEKS:
            week_result = ConfigValidator.validate_range(week, 1, 18, f"bye_week_{week}")
            result.errors.extend(week_result.errors)

        return result

    def validate_position_settings():
        """
        Validate position settings including MAX_POSITIONS totals and limits.

        Returns:
            ValidationResult: Result object containing any validation errors
        """
        result = ValidationResult()

        # Validate MAX_POSITIONS totals
        total_positions = sum(MAX_POSITIONS.values())
        if total_positions < MAX_PLAYERS:
            result.add_error(f"MAX_POSITIONS total ({total_positions}) should be >= MAX_PLAYERS ({MAX_PLAYERS})", "MAX_POSITIONS")

        # Validate each position limit
        for position, limit in MAX_POSITIONS.items():
            pos_result = ConfigValidator.validate_range(limit, 0, 10, f"MAX_POSITIONS[{position}]")
            result.errors.extend(pos_result.errors)

        return result

    def validate_draft_order():
        """
        Validate draft order configuration including round count and position weights.

        Returns:
            ValidationResult: Result object containing any validation errors
        """
        result = ValidationResult()

        total_rounds = len(DRAFT_ORDER)
        if total_rounds != MAX_PLAYERS:
            result.add_error(f"DRAFT_ORDER has {total_rounds} rounds but MAX_PLAYERS is {MAX_PLAYERS}", "DRAFT_ORDER")

        # Validate each round has valid positions
        for round_idx, round_prefs in enumerate(DRAFT_ORDER):
            if not round_prefs:
                result.add_error(f"Round {round_idx + 1} cannot have empty preferences", f"DRAFT_ORDER[{round_idx}]")

            for position, bonus_value in round_prefs.items():
                if position not in list(MAX_POSITIONS.keys()):
                    result.add_error(f"Invalid position '{position}' in round {round_idx + 1}", f"DRAFT_ORDER[{round_idx}]")

                # Validate bonus values (should be 0-100 for static point bonuses)
                bonus_result = ConfigValidator.validate_range(bonus_value, 0.0, 100.0, f"DRAFT_ORDER[{round_idx}][{position}]")
                result.errors.extend(bonus_result.errors)

        return result

    def validate_penalties():
        """
        Validate penalty settings including injury penalties, bye week penalties, and trade thresholds.

        Returns:
            ValidationResult: Result object containing any validation errors
        """
        result = ValidationResult()

        # Validate injury penalties
        for injury_level, penalty in INJURY_PENALTIES.items():
            penalty_result = ConfigValidator.validate_range(penalty, 0, 200, f"INJURY_PENALTIES[{injury_level}]")
            result.errors.extend(penalty_result.errors)

        # Validate other penalty settings
        bye_penalty_result = ConfigValidator.validate_range(BASE_BYE_PENALTY, 0, 100, "BASE_BYE_PENALTY")
        result.errors.extend(bye_penalty_result.errors)

        trade_improvement_result = ConfigValidator.validate_range(MIN_TRADE_IMPROVEMENT, 0, 100, "MIN_TRADE_IMPROVEMENT")
        result.errors.extend(trade_improvement_result.errors)

        return result

    # Run all validations
    combined_result = validate_multiple([
        validate_basic_settings,
        validate_position_settings,
        validate_draft_order,
        validate_penalties
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