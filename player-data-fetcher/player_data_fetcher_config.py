#!/usr/bin/env python3
"""
Player Data Fetcher Configuration

This file contains all the frequently modified constants for the player data fetcher.
Most important and frequently modified settings are at the top.

Author: Generated for NFL Fantasy Data Collection
Last Updated: September 2025
"""

from dataclasses import dataclass
from typing import Dict, List

# =============================================================================
# SHARED VARIABLES (imported from shared_config.py)
# =============================================================================

# Import shared NFL season/week variables from central location
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from shared_config import CURRENT_NFL_WEEK, NFL_SEASON, NFL_SCORING_FORMAT

# =============================================================================
# PLAYER DATA FETCHER SPECIFIC SETTINGS
# =============================================================================

# Week-by-Week Projection Settings (FREQUENTLY MODIFIED)
USE_WEEK_BY_WEEK_PROJECTIONS = True  # Use week-by-week calculation (primary method)
USE_REMAINING_SEASON_PROJECTIONS = False  # Use remaining games instead of full season
INCLUDE_PLAYOFF_WEEKS = False  # Include playoff weeks (19-22) in calculations
RECENT_WEEKS_FOR_AVERAGE = 4  # Number of recent weeks to average for projections

# Data Preservation Settings (FREQUENTLY MODIFIED)
PRESERVE_DRAFTED_VALUES = True   # Keep draft status between data updates
PRESERVE_LOCKED_VALUES = False    # Keep locked players between data updates

# Optimization Settings (FREQUENTLY MODIFIED)
SKIP_DRAFTED_PLAYER_UPDATES = False  # Skip API calls for drafted=1 players (major optimization)
USE_SCORE_THRESHOLD = False  # Only update players above score threshold (preserves low-scoring player data)
PLAYER_SCORE_THRESHOLD = 50.0  # Minimum fantasy points to trigger API update

# Output Settings (FREQUENTLY MODIFIED)
OUTPUT_DIRECTORY = "./data"
CREATE_CSV = True
CREATE_JSON = False
CREATE_EXCEL = True
CREATE_CONDENSED_EXCEL = True

# File Paths (FREQUENTLY MODIFIED)
PLAYERS_CSV = '../shared_files/players.csv'

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
# ESPN API CONFIGURATION
# =============================================================================

# ESPN API settings
ESPN_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
ESPN_PLAYER_LIMIT = 2000

# API settings
REQUEST_TIMEOUT = 30
RATE_LIMIT_DELAY = 0.2

# =============================================================================
# EXPORT CONFIGURATION
# =============================================================================

# Export settings
EXCEL_POSITION_SHEETS = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']
EXPORT_COLUMNS = [
    'id', 'name', 'team', 'position', 'bye_week', 'fantasy_points',
    'injury_status', 'drafted', 'locked', 'data_method',
    # Weekly projections (weeks 1-17 fantasy regular season only)
    'week_1_points', 'week_2_points', 'week_3_points', 'week_4_points',
    'week_5_points', 'week_6_points', 'week_7_points', 'week_8_points',
    'week_9_points', 'week_10_points', 'week_11_points', 'week_12_points',
    'week_13_points', 'week_14_points', 'week_15_points', 'week_16_points',
    'week_17_points'
]

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
    
    if NFL_SCORING_FORMAT not in ["ppr", "std", "half"]:
        errors.append(f"Invalid NFL_SCORING_FORMAT: {NFL_SCORING_FORMAT}")
        
    if not POSITION_FALLBACK_CONFIG:
        errors.append("POSITION_FALLBACK_CONFIG cannot be empty")
        
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

SEASON CHANGES:
1. NFL_SEASON - Update for current year
2. NFL_SCORING_FORMAT - PPR vs Standard scoring
3. PRESERVE_DRAFTED_VALUES - False (reset), then True (maintain)

SCORING FORMAT CHANGES:
1. POSITION_FALLBACK_CONFIG - Adjust point values for different scoring formats
2. ESPN_PLAYER_LIMIT - Increase for larger leagues

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