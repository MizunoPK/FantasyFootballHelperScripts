"""
Simulation-specific configuration settings.
"""

import os
from typing import Dict, List, Tuple

# =============================================================================
# SIMULATION PARAMETERS
# =============================================================================

# Test parameters and their ranges (balanced for meaningful analysis)
PARAMETER_RANGES = {
    # === NEW SCORING SYSTEM PARAMETERS ===
    # Normalization parameters
    'NORMALIZATION_MAX_SCALE': [80, 100, 120],           # Test different scale values for normalization

    # DRAFT_ORDER bonus parameters
    'DRAFT_ORDER_PRIMARY_BONUS': [40, 50, 60],           # Test primary position bonus range
    'DRAFT_ORDER_SECONDARY_BONUS': [20, 25, 30],         # Test secondary position bonus range

    # Matchup multiplier parameters (for Starter Helper)
    'MATCHUP_EXCELLENT_MULTIPLIER': [1.15, 1.2, 1.25],   # Very favorable matchup (rank diff >15)
    'MATCHUP_GOOD_MULTIPLIER': [1.05, 1.1, 1.15],        # Favorable matchup (rank diff 6-15)
    'MATCHUP_NEUTRAL_MULTIPLIER': [0.95, 1.0, 1.05],     # Neutral matchup (rank diff -5 to 5)
    'MATCHUP_POOR_MULTIPLIER': [0.85, 0.9, 0.95],        # Unfavorable matchup (rank diff -15 to -6)
    'MATCHUP_VERY_POOR_MULTIPLIER': [0.75, 0.8, 0.85],   # Very unfavorable matchup (rank diff <-15)

    # === EXISTING PARAMETERS (KEPT FOR COMPATIBILITY) ===
    # Core existing parameters
    'INJURY_PENALTIES_MEDIUM': [15, 20],                 # Test injury tolerance range
    'INJURY_PENALTIES_HIGH': [30, 40],                   # Test high injury penalty range
    'BASE_BYE_PENALTY': [10, 20],                        # Test bye week penalty range

    # DEPRECATED PARAMETERS (will be removed after scoring overhaul)
    # 'POS_NEEDED_SCORE': [65, 75],                      # DEPRECATED: Positional need being removed
    # 'PROJECTION_BASE_SCORE': [90, 100],                # DEPRECATED: Using normalization instead
    # 'DRAFT_ORDER_WEIGHTS': [1.0, 1.2],                 # DEPRECATED: Using static bonuses instead

    # Enhanced scoring parameters - Key multipliers for comprehensive testing
    'ADP_EXCELLENT_MULTIPLIER': [1.10, 1.15, 1.20],        # ADP boost range
    'ADP_GOOD_MULTIPLIER': [1.05, 1.08, 1.10],             # ADP good range
    'ADP_POOR_MULTIPLIER': [0.85, 0.90, 0.95],              # ADP penalty range
    'PLAYER_RATING_EXCELLENT_MULTIPLIER': [1.15, 1.20, 1.25],  # Player rating boost
    'PLAYER_RATING_GOOD_MULTIPLIER': [1.08, 1.10, 1.12],      # Player rating good
    'PLAYER_RATING_POOR_MULTIPLIER': [0.85, 0.90, 0.95],      # Player rating penalty

    # Team performance multipliers
    'TEAM_EXCELLENT_MULTIPLIER': [1.10, 1.12, 1.15],          # Team excellent performance
    'TEAM_GOOD_MULTIPLIER': [1.04, 1.06, 1.08],               # Team good performance
    'TEAM_POOR_MULTIPLIER': [0.92, 0.94, 0.96],               # Team poor performance

    # Adjustment caps (DEPRECATED - will be removed after scoring overhaul)
    # 'MAX_TOTAL_ADJUSTMENT': [1.45, 1.50, 1.55],            # DEPRECATED: Removing multiplier caps
    # 'MIN_TOTAL_ADJUSTMENT': [0.65, 0.70, 0.75],            # DEPRECATED: Removing multiplier caps
}

# Simulation settings
SIMULATIONS_PER_CONFIG = 20           # Number of drafts to run per configuration
PRELIMINARY_SIMULATIONS_PER_CONFIG = 5  # Reduced for preliminary testing
TOP_CONFIGS_PERCENTAGE = 0.01          # Top 1% of configs advance to full testing

# Parallel processing settings
MAX_PARALLEL_THREADS = None             # Max concurrent threads for simulation
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