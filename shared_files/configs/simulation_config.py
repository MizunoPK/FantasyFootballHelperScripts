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
SIMULATIONS_PER_CONFIG = 10           # Number of drafts to run per configuration
PRELIMINARY_SIMULATIONS_PER_CONFIG = 3  # Reduced for preliminary testing
TOP_CONFIGS_PERCENTAGE = 0.1          # Top configs advance to full testing

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

# =============================================================================
# FINE-GRAIN VARIATION OFFSETS
# =============================================================================
# These offsets are used in the second phase of optimization to generate
# fine-grained variations around top-performing configurations.
#
# For each top configuration, the system creates variations by adding these
# offset values to each parameter. For example, if a top config has
# INJURY_PENALTIES_MEDIUM = 25, and offsets are [-10, -5, 0, 5, 10],
# it will test: 15, 20, 25, 30, 35
#
# Offset Design Guidelines:
# - Include 0 to test the original top config value
# - Use symmetric ranges around 0 for balanced exploration
# - Scale offsets based on parameter magnitude and typical range
# - More offsets = more thorough testing but more computation time

FINE_GRAIN_OFFSETS = {
    # Core Scoring Parameters
    'NORMALIZATION_MAX_SCALE': [-20, -10, 0, 10, 20],  # Scale: 80-120 typical
    'DRAFT_ORDER_PRIMARY_BONUS': [-10, -5, 0, 5, 10],  # Scale: 40-60 typical
    'DRAFT_ORDER_SECONDARY_BONUS': [-5, -2, 0, 2, 5],  # Scale: 20-30 typical

    # Matchup Multipliers (decimal offsets for 0.8-1.2 range)
    'MATCHUP_EXCELLENT_MULTIPLIER': [-0.05, -0.02, 0, 0.02, 0.05],
    'MATCHUP_GOOD_MULTIPLIER': [-0.05, -0.02, 0, 0.02, 0.05],
    'MATCHUP_NEUTRAL_MULTIPLIER': [-0.02, -0.01, 0, 0.01, 0.02],
    'MATCHUP_POOR_MULTIPLIER': [-0.05, -0.02, 0, 0.02, 0.05],
    'MATCHUP_VERY_POOR_MULTIPLIER': [-0.05, -0.02, 0, 0.02, 0.05],

    # Injury & Bye Penalties
    'INJURY_PENALTIES_MEDIUM': [-10, -5, 0, 5, 10],     # Scale: 15-35 typical
    'INJURY_PENALTIES_HIGH': [-15, -10, -5, 0, 5, 10, 15],  # Scale: 35-65 typical
    'BASE_BYE_PENALTY': [-10, -5, 0, 5, 10],            # Scale: 0-20 typical

    # ADP Adjustments (decimal offsets for 0.9-1.2 range)
    'ADP_EXCELLENT_MULTIPLIER': [-0.05, -0.02, 0, 0.02, 0.05],
    'ADP_GOOD_MULTIPLIER': [-0.03, -0.01, 0, 0.01, 0.03],
    'ADP_POOR_MULTIPLIER': [-0.05, -0.02, 0, 0.02, 0.05],

    # Player Rating Adjustments (decimal offsets for 0.9-1.2 range)
    'PLAYER_RATING_EXCELLENT_MULTIPLIER': [-0.05, -0.02, 0, 0.02, 0.05],
    'PLAYER_RATING_GOOD_MULTIPLIER': [-0.03, -0.01, 0, 0.01, 0.03],
    'PLAYER_RATING_POOR_MULTIPLIER': [-0.05, -0.02, 0, 0.02, 0.05],

    # Team Quality Adjustments (decimal offsets for 0.9-1.2 range)
    'TEAM_EXCELLENT_MULTIPLIER': [-0.05, -0.02, 0, 0.02, 0.05],
    'TEAM_GOOD_MULTIPLIER': [-0.03, -0.01, 0, 0.01, 0.03],
    'TEAM_POOR_MULTIPLIER': [-0.05, -0.02, 0, 0.02, 0.05],
}

# Parameter bounds for fine-grain variations
# Format: {parameter_name: (min_value, max_value)}
FINE_GRAIN_BOUNDS = {
    # Core Scoring Parameters
    'NORMALIZATION_MAX_SCALE': (50, 200),
    'DRAFT_ORDER_PRIMARY_BONUS': (0, 100),
    'DRAFT_ORDER_SECONDARY_BONUS': (0, 50),

    # Matchup Multipliers
    'MATCHUP_EXCELLENT_MULTIPLIER': (1.0, 1.5),
    'MATCHUP_GOOD_MULTIPLIER': (1.0, 1.3),
    'MATCHUP_NEUTRAL_MULTIPLIER': (0.95, 1.05),
    'MATCHUP_POOR_MULTIPLIER': (0.7, 1.0),
    'MATCHUP_VERY_POOR_MULTIPLIER': (0.5, 1.0),

    # Injury & Bye Penalties
    'INJURY_PENALTIES_MEDIUM': (0, 100),
    'INJURY_PENALTIES_HIGH': (0, 100),
    'BASE_BYE_PENALTY': (0, 100),

    # ADP Adjustments
    'ADP_EXCELLENT_MULTIPLIER': (1.0, 1.5),
    'ADP_GOOD_MULTIPLIER': (1.0, 1.3),
    'ADP_POOR_MULTIPLIER': (0.7, 1.0),

    # Player Rating Adjustments
    'PLAYER_RATING_EXCELLENT_MULTIPLIER': (1.0, 1.5),
    'PLAYER_RATING_GOOD_MULTIPLIER': (1.0, 1.3),
    'PLAYER_RATING_POOR_MULTIPLIER': (0.7, 1.0),

    # Team Quality Adjustments
    'TEAM_EXCELLENT_MULTIPLIER': (1.0, 1.5),
    'TEAM_GOOD_MULTIPLIER': (1.0, 1.3),
    'TEAM_POOR_MULTIPLIER': (0.7, 1.0),
}

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

# Get the simulation directory path (draft_helper/simulation/)
_config_dir = os.path.dirname(__file__)  # shared_files/configs/
_shared_files_dir = os.path.dirname(_config_dir)  # shared_files/
_root_dir = os.path.dirname(_shared_files_dir)  # root
_simulation_dir = os.path.join(_root_dir, 'draft_helper', 'simulation')

# Simulation data paths
SIMULATION_DATA_DIR = os.path.join(_simulation_dir, 'data')
RESULTS_DIR = os.path.join(_simulation_dir, 'results')
RESULTS_FILE = os.path.join(_simulation_dir, 'results.md')  # Legacy path for compatibility

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

    # Validate fine-grain offsets - each parameter should have a list
    for param_name, offsets in FINE_GRAIN_OFFSETS.items():
        if not isinstance(offsets, list):
            errors.append(f"FINE_GRAIN_OFFSETS['{param_name}'] must be a list, got {type(offsets).__name__}")
        elif not offsets:
            errors.append(f"FINE_GRAIN_OFFSETS['{param_name}'] cannot be empty")
        elif 0 not in offsets:
            errors.append(f"FINE_GRAIN_OFFSETS['{param_name}'] should include 0 to test the original value")

    # Validate fine-grain bounds - each parameter should have (min, max) tuple
    for param_name, bounds in FINE_GRAIN_BOUNDS.items():
        if not isinstance(bounds, tuple) or len(bounds) != 2:
            errors.append(f"FINE_GRAIN_BOUNDS['{param_name}'] must be a (min, max) tuple")
        else:
            min_val, max_val = bounds
            if min_val >= max_val:
                errors.append(f"FINE_GRAIN_BOUNDS['{param_name}'] min ({min_val}) must be < max ({max_val})")

    # Check that offset parameters have corresponding bounds
    missing_bounds = set(FINE_GRAIN_OFFSETS.keys()) - set(FINE_GRAIN_BOUNDS.keys())
    if missing_bounds:
        errors.append(f"Parameters in FINE_GRAIN_OFFSETS missing from FINE_GRAIN_BOUNDS: {missing_bounds}")

    if errors:
        raise ValueError(f"Simulation configuration validation failed: {'; '.join(errors)}")

# Run validation on import
if __name__ != "__main__":
    validate_simulation_config()
