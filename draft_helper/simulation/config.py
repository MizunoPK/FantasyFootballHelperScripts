"""
Simulation-specific configuration settings.
"""

import os
from typing import Dict, List, Tuple

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

# Set logging level for simulation runs
# Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
# Set to WARNING to suppress INFO logs from positional_ranking_calculator and other modules
SIMULATION_LOG_LEVEL = "WARNING"

# =============================================================================
# SIMULATION PARAMETERS
# =============================================================================

# PARAMETER RANGE STRATEGY:
# -------------------------
# All parameters use 2-value testing for computational efficiency:
#   - First value: Current default or baseline setting
#   - Second value: More aggressive or higher impact setting
#
# This strategy allows meaningful comparison between conservative and aggressive
# configurations while keeping total simulation combinations manageable.
#
# PARAMETER USAGE BY MODE:
# -------------------------
# Draft Mode (Initial Roster Construction):
#   - DRAFT_ORDER bonuses (PRIMARY/SECONDARY)
#   - NORMALIZATION_MAX_SCALE
#   - BASE_BYE_PENALTY
#   - INJURY_PENALTIES (MEDIUM/HIGH)
#   - Enhanced scoring multipliers (ADP, PLAYER_RATING, TEAM)
#
# Starter Helper Mode (Weekly Lineup Optimization):
#   - MATCHUP_MULTIPLIERS (EXCELLENT/GOOD/NEUTRAL/POOR/VERY_POOR)
#   - Binary injury system (not point-based penalties)
#   - NO bye week penalties (already 0.0 in data)
#
# INTERDEPENDENCIES:
# ------------------
# - DRAFT_ORDER bonuses interact with NORMALIZATION_MAX_SCALE
# - Higher NORMALIZATION_MAX_SCALE increases point separation
# - MATCHUP_MULTIPLIERS only affect Starter Helper weekly scoring
# - BASE_BYE_PENALTY affects draft decisions, not weekly matchups
# - Enhanced scoring multipliers compound (ADP * PLAYER_RATING * TEAM)

# NOTE: Parameter configurations are now loaded from JSON files in the parameters/ directory.
# See parameters/README.md for documentation on creating parameter configuration files.
# Use the parameter_loader module to load and validate configurations.

# Simulation settings
SIMULATIONS_PER_CONFIG = 1           # Number of drafts to run per configuration
PRELIMINARY_SIMULATIONS_PER_CONFIG = 1  # Reduced for preliminary testing
TOP_CONFIGS_PERCENTAGE = 0.2          # Top configs advance to full testing

# Parallel processing settings
MAX_PARALLEL_THREADS = 7             # Max concurrent threads for simulation
                                       # None = auto-detect: min(6, CPU_COUNT)
                                       # Integer = explicit thread count
                                       # Examples: 1, 4, 8, 12, None

# League settings
LEAGUE_SIZE = 10                      # Number of teams in the draft
NFL_SEASON_WEEKS = 17                 # Full season simulation
HUMAN_ERROR_RATE = 0.3              # 30% chance of suboptimal pick
SUBOPTIMAL_CHOICE_POOL = 5          # Pick from top 5 instead of #1

# Team strategy distribution
TEAM_STRATEGIES = {
    'conservative': 2,    # 2 teams use conservative strategy
    'aggressive': 2,      # 2 teams use aggressive strategy
    'positional': 2,      # 2 teams use positional strategy
    'value': 3,           # 3 teams use value strategy
    'draft_helper': 1     # 1 team uses draft_helper logic
}

# =============================================================================
# FILE PATHS
# =============================================================================

# Simulation data paths
SIMULATION_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
RESULTS_DIR = os.path.join(os.path.dirname(__file__), 'results')
RESULTS_FILE = os.path.join(os.path.dirname(__file__), 'results.md')  # Legacy path for compatibility

def get_timestamped_results_file():
    """Generate timestamped results file path."""
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return os.path.join(RESULTS_DIR, f'result_{timestamp}.md')

# =============================================================================
# VALIDATION
# =============================================================================

def validate_simulation_config():
    """Validate simulation configuration settings"""
    errors = []

    if LEAGUE_SIZE != sum(TEAM_STRATEGIES.values()):
        errors.append(f"LEAGUE_SIZE ({LEAGUE_SIZE}) must equal sum of TEAM_STRATEGIES ({sum(TEAM_STRATEGIES.values())})")

    if not (0 <= HUMAN_ERROR_RATE <= 1):
        errors.append("HUMAN_ERROR_RATE must be between 0 and 1")

    if SUBOPTIMAL_CHOICE_POOL < 2:
        errors.append("SUBOPTIMAL_CHOICE_POOL must be at least 2")

    if not (0 < TOP_CONFIGS_PERCENTAGE <= 1):
        errors.append("TOP_CONFIGS_PERCENTAGE must be between 0 and 1")

    if MAX_PARALLEL_THREADS is not None and MAX_PARALLEL_THREADS < 1:
        errors.append("MAX_PARALLEL_THREADS must be at least 1 or None for auto-detection")

    if errors:
        raise ValueError(f"Simulation configuration validation failed: {'; '.join(errors)}")

# Run validation on import
if __name__ != "__main__":
    validate_simulation_config()