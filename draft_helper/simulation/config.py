"""
Simulation-specific configuration settings.
"""

import os
from typing import Dict, List, Tuple

# =============================================================================
# SIMULATION PARAMETERS
# =============================================================================

# Test parameters and their ranges
PARAMETER_RANGES = {
    'INJURY_PENALTIES_MEDIUM': [5, 15, 25, 35, 45],  # Every 3rd value from original range
    'INJURY_PENALTIES_HIGH': [25, 35, 45, 55, 65],   # Every 3rd value from original range
    'POS_NEEDED_SCORE': [25, 35, 45, 55, 65],        # Every 3rd value from original range
    'PROJECTION_BASE_SCORE': [75, 85, 95, 105, 115], # Every 3rd value from original range
    'BASE_BYE_PENALTY': [5, 15, 25, 35, 45],         # Every 3rd value from original range
    'DRAFT_ORDER_WEIGHTS': [0.5, 0.8, 1.0, 1.2]     # Subset of weight values to test
}

# Simulation settings
SIMULATIONS_PER_CONFIG = 50           # Number of drafts to run per configuration
PRELIMINARY_SIMULATIONS_PER_CONFIG = 10  # Reduced for preliminary testing
TOP_CONFIGS_PERCENTAGE = 0.1          # Top 10% of configs advance to full testing

# League settings
LEAGUE_SIZE = 10                      # Number of teams in the draft
NFL_SEASON_WEEKS = 17                 # Full season simulation
HUMAN_ERROR_RATE = 0.15              # 15% chance of suboptimal pick
SUBOPTIMAL_CHOICE_POOL = 10          # Pick from top 10 instead of #1

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
RESULTS_FILE = os.path.join(os.path.dirname(__file__), 'results.md')

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

    if errors:
        raise ValueError(f"Simulation configuration validation failed: {'; '.join(errors)}")

# Run validation on import
if __name__ != "__main__":
    validate_simulation_config()