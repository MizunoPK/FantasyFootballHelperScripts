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
    # Core existing parameters (3 values each for thorough testing)
    'INJURY_PENALTIES_MEDIUM': [20, 25, 30],         # Test injury tolerance range
    'INJURY_PENALTIES_HIGH': [40, 45, 50],           # Test high injury penalty range
    'POS_NEEDED_SCORE': [40, 45, 50],                # Test positional need scoring
    'PROJECTION_BASE_SCORE': [90, 95, 100],          # Test projection weighting
    'BASE_BYE_PENALTY': [20, 25, 30],                # Test bye week penalty range
    'DRAFT_ORDER_WEIGHTS': [0.9, 1.0, 1.1],         # Test draft order influence

    # Enhanced scoring parameters - Key multipliers for comprehensive testing
    'ADP_EXCELLENT_MULTIPLIER': [1.10, 1.15, 1.20],        # ADP boost range
    'ADP_POOR_MULTIPLIER': [0.90, 0.95],                    # ADP penalty range
    'PLAYER_RATING_EXCELLENT_MULTIPLIER': [1.15, 1.20, 1.25],  # Player rating boost
    'PLAYER_RATING_POOR_MULTIPLIER': [0.90, 0.95],             # Player rating penalty

    # Total: 3^6 * 3 * 2 * 3 * 2 = 729 * 3 * 2 * 3 * 2 = 26,244 configurations
    # This provides meaningful analysis while remaining computationally feasible
}

# Simulation settings
SIMULATIONS_PER_CONFIG = 10           # Number of drafts to run per configuration
PRELIMINARY_SIMULATIONS_PER_CONFIG = 3  # Reduced for preliminary testing
TOP_CONFIGS_PERCENTAGE = 0.025          # Top 5% of configs advance to full testing

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
PLAYERS_CSV_COPY = os.path.join(SIMULATION_DATA_DIR, 'players_simulation.csv')
RESULTS_DIR = os.path.join(os.path.dirname(__file__), 'results')
RESULTS_FILE = os.path.join(os.path.dirname(__file__), 'results.md')  # Legacy path for compatibility

def get_timestamped_results_file():
    """Generate timestamped results file path."""
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return os.path.join(RESULTS_DIR, f'result_{timestamp}.md')

# Source data paths (to copy from)
SOURCE_PLAYERS_CSV = os.path.join(os.path.dirname(__file__), '..', '..', 'shared_files', 'players.csv')

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