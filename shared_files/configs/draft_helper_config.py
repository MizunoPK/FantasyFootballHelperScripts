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

# DRAFT_ORDER bonus configuration
# NOTE: Actual bonus values are now loaded from parameters.json
# These are placeholder values for the DRAFT_ORDER structure below
# To modify bonus values, edit parameters.json instead
DRAFT_ORDER_PRIMARY_BONUS = 75.0    # Placeholder - actual value from JSON
DRAFT_ORDER_SECONDARY_BONUS = 40.0  # Placeholder - actual value from JSON

# Draft Strategy - Round-based position bonuses
# The structure below defines which positions get bonuses in each round
# Actual bonus values (P and S) come from parameters.json via ParameterJsonManager
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
# SCORING WEIGHTS
# =============================================================================
# NOTE: All scoring parameters are now loaded from parameters.json
# Parameters moved to JSON:
# - NORMALIZATION_MAX_SCALE
# - BASE_BYE_PENALTY
# - INJURY_PENALTIES (nested dict with LOW, MEDIUM, HIGH)
# - ADP multipliers (EXCELLENT, GOOD, POOR)
# - Player rating multipliers (EXCELLENT, GOOD, POOR)
# - Team quality multipliers (EXCELLENT, GOOD, POOR)
# - Consistency multipliers (LOW, MEDIUM, HIGH)
# - Matchup multipliers (5 levels)
#
# To modify these values, edit shared_files/parameters.json instead

# Trade optimization settings (FREQUENTLY MODIFIED)
MIN_TRADE_IMPROVEMENT = 0     # ← Minimum point improvement required for a trade to be considered
NUM_TRADE_RUNNERS_UP = 3      # ← Number of runner-up trades to show for each player

# Bye weeks for NFL season
POSSIBLE_BYE_WEEKS = [5, 6, 7, 8, 9, 10, 11, 12, 14]

# =============================================================================
# CONSISTENCY SCORING CONFIGURATION
# =============================================================================

# Enable/disable consistency scoring (based on week-to-week variance)
ENABLE_CONSISTENCY_SCORING = True

# NOTE: Consistency multipliers are now loaded from parameters.json
# CONSISTENCY_LOW_MULTIPLIER, CONSISTENCY_MEDIUM_MULTIPLIER, CONSISTENCY_HIGH_MULTIPLIER

# Coefficient of Variation (CV) thresholds
# CV = standard_deviation / mean (measures relative variability)
CONSISTENCY_CV_LOW_THRESHOLD = 0.3    # Below this = LOW volatility
CONSISTENCY_CV_HIGH_THRESHOLD = 0.6   # Above this = HIGH volatility

# Minimum weeks required for CV calculation
# If fewer weeks available, defaults to MEDIUM category
MINIMUM_WEEKS_FOR_CONSISTENCY = 3

# Consistency weight tuning (optional, for future use)
# Scales the impact of consistency multipliers
CONSISTENCY_WEIGHT = 1.0  # 1.0 = full impact, 0.5 = half impact

# Note: Only weeks < CURRENT_NFL_WEEK are used for ALL players
# This ensures we only analyze actual performance, not future projections

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

    def validate_trade_settings():
        """
        Validate trade optimization settings.

        Note: Penalty parameters (INJURY_PENALTIES, BASE_BYE_PENALTY) are now
        validated by ParameterJsonManager when loading parameters.json

        Returns:
            ValidationResult: Result object containing any validation errors
        """
        result = ValidationResult()

        # Validate trade improvement threshold
        trade_improvement_result = ConfigValidator.validate_range(MIN_TRADE_IMPROVEMENT, 0, 100, "MIN_TRADE_IMPROVEMENT")
        result.errors.extend(trade_improvement_result.errors)

        return result

    # Run all validations
    combined_result = validate_multiple([
        validate_basic_settings,
        validate_position_settings,
        validate_draft_order,
        validate_trade_settings
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

📊 SCORING PARAMETERS (edit shared_files/parameters.json):
- All scoring multipliers (ADP, player rating, team quality, consistency, matchup)
- Penalty values (BASE_BYE_PENALTY, INJURY_PENALTIES)
- Normalization scale (NORMALIZATION_MAX_SCALE)
- Draft order bonuses (DRAFT_ORDER_PRIMARY_BONUS, DRAFT_ORDER_SECONDARY_BONUS)
- Full parameter documentation: shared_files/README_parameters.md

⚙️ CONFIG SETTINGS (edit this file):
1. DRAFT_ORDER - Update round-based position priorities
2. MAX_POSITIONS - Adjust for different league roster requirements
3. TRADE_HELPER_MODE - Switch between draft and trade modes
4. RECOMMENDATION_COUNT - How many players to suggest
5. MIN_TRADE_IMPROVEMENT - Minimum point improvement to suggest a trade
6. APPLY_INJURY_PENALTY_TO_ROSTER - Apply injury penalties to roster players in trade mode
7. LOGGING_LEVEL - 'DEBUG' (detailed) vs 'INFO' (minimal)

🔧 HOW TO MODIFY:

To change scoring parameters (penalties, multipliers, bonuses):
    Edit shared_files/parameters.json
    Example: Change "BASE_BYE_PENALTY": 28.85 to a different value

To change draft strategy for RB-heavy approach:
    DRAFT_ORDER[0] = {RB: P, FLEX: S}  # Prioritize RB in round 1
    (P and S values come from parameters.json)

To only consider significant trades:
    MIN_TRADE_IMPROVEMENT = 15  # Only suggest trades with 15+ point improvement

To ignore injury penalties for roster players in trade analysis:
    APPLY_INJURY_PENALTY_TO_ROSTER = False  # Score roster players as if healthy

⚠️ VALIDATION:
- Config validation happens on import (this file)
- Parameter validation happens when loading parameters.json
- Invalid settings will raise ValueError with details
"""