#!/usr/bin/env python3
"""
NFL Scores Fetcher Configuration

This file contains all the frequently modified constants for the NFL scores fetcher.
Most important and frequently modified settings are at the top.

Author: Generated for NFL Fantasy Data Collection
Last Updated: September 2025
"""

# =============================================================================
# SHARED VARIABLES (imported from shared_config.py)
# =============================================================================

# Import shared NFL season/week variables from central location
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from shared_config import CURRENT_NFL_WEEK, NFL_SEASON

# Map shared variables to local names for backwards compatibility
NFL_SCORES_SEASON = NFL_SEASON
NFL_SCORES_CURRENT_WEEK = CURRENT_NFL_WEEK

# =============================================================================
# NFL SCORES FETCHER SPECIFIC SETTINGS
# =============================================================================

# NFL Scores Settings (FREQUENTLY MODIFIED)
NFL_SCORES_SEASON_TYPE = 2
NFL_SCORES_ONLY_COMPLETED_GAMES = False

# Output Settings (FREQUENTLY MODIFIED)
OUTPUT_DIRECTORY = "./data"
CREATE_CSV = True
CREATE_JSON = False
CREATE_EXCEL = True

# =============================================================================
# API CONFIGURATION
# =============================================================================

# API settings
REQUEST_TIMEOUT = 30
RATE_LIMIT_DELAY = 0.2

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

LOGGING_ENABLED = False         # ← Enable/disable logging
LOGGING_LEVEL = 'INFO'         # ← DEBUG, INFO, WARNING, ERROR, CRITICAL
LOGGING_TO_FILE = False        # ← Console vs file logging
LOGGING_FILE = './data/log.txt'

# =============================================================================
# CONFIGURATION VALIDATION
# =============================================================================

def validate_config():
    """Validate configuration settings"""
    errors = []
    
    if NFL_SCORES_SEASON <= 0:
        errors.append("NFL_SCORES_SEASON must be positive")
        
    if NFL_SCORES_SEASON_TYPE not in [1, 2, 3, 4]:
        errors.append("NFL_SCORES_SEASON_TYPE must be 1 (preseason), 2 (regular), 3 (postseason), or 4 (off-season)")
        
    if NFL_SCORES_CURRENT_WEEK <= 0:
        errors.append("NFL_SCORES_CURRENT_WEEK must be positive")
        
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

WEEKLY CHANGES:
1. NFL_SCORES_CURRENT_WEEK - Update for current NFL week
2. NFL_SCORES_ONLY_COMPLETED_GAMES - True for final scores, False for live updates

SEASON CHANGES:
1. NFL_SCORES_SEASON - Update for current year
2. NFL_SCORES_SEASON_TYPE - 1 (preseason), 2 (regular), 3 (postseason), 4 (off-season)

OUTPUT CHANGES:
1. CREATE_EXCEL/CREATE_CSV/CREATE_JSON - Control output formats
2. OUTPUT_DIRECTORY - Change where files are saved

DEBUGGING:
1. LOGGING_LEVEL = 'DEBUG' (detailed) vs 'INFO' (minimal)
2. LOGGING_TO_FILE = True (save logs to file)

⚠️ VALIDATION:
Configuration is automatically validated on import. Invalid settings will
raise ValueError with details about what needs to be fixed.
"""