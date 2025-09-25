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
# Week-by-week projections are always enabled - this is the only method used
INCLUDE_PLAYOFF_WEEKS = False  # Include playoff weeks (19-22) in calculations
RECENT_WEEKS_FOR_AVERAGE = 4  # Number of recent weeks to average for projections

# Team Rankings Configuration (FREQUENTLY MODIFIED)
MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS = 3  # Minimum games played to use current season data
# When CURRENT_NFL_WEEK >= MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS + 1, use current season stats
# Otherwise, fall back to previous season data or neutral rankings
# Example: If set to 5 and CURRENT_NFL_WEEK is 6+, uses 2025 data. If week 4 or less, uses 2024 data.
# This ensures rankings are based on meaningful sample sizes rather than small early-season samples.

# Data Preservation Settings (FREQUENTLY MODIFIED)
PRESERVE_DRAFTED_VALUES = False   # Keep draft status between data updates
PRESERVE_LOCKED_VALUES = False    # Keep locked players between data updates

# Drafted Data Loading Settings (FREQUENTLY MODIFIED)
LOAD_DRAFTED_DATA_FROM_FILE = True  # Load drafted state from external CSV file (alternative to PRESERVE_DRAFTED_VALUES)
DRAFTED_DATA = "./drafted_data.csv"  # Path to CSV file containing drafted player data
MY_TEAM_NAME = "Sea Sharp"           # Name of your fantasy team for identifying roster players (drafted=2)

# Optimization Settings (FREQUENTLY MODIFIED)
SKIP_DRAFTED_PLAYER_UPDATES = False  # Skip API calls for drafted=1 players (major optimization)
USE_SCORE_THRESHOLD = False  # Only update players above score threshold (preserves low-scoring player data)
PLAYER_SCORE_THRESHOLD = 50.0  # Minimum fantasy points to trigger API update

# Output Settings (FREQUENTLY MODIFIED)
OUTPUT_DIRECTORY = "./data"
CREATE_CSV = True
CREATE_JSON = False
CREATE_EXCEL = False
CREATE_CONDENSED_EXCEL = True

# File Paths (FREQUENTLY MODIFIED)
PLAYERS_CSV = '../shared_files/players.csv'

# =============================================================================
# FALLBACK FANTASY POINTS - REMOVED (Week-by-week only system)
# =============================================================================

# ADP fallback system removed - using week-by-week projections only

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
    'injury_status', 'drafted', 'locked', 'average_draft_position',
    'player_rating',
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

LOGGING_ENABLED = True          # ← Enable/disable logging
LOGGING_LEVEL = 'WARNING'      # ← DEBUG, INFO, WARNING, ERROR, CRITICAL (WARNING+ to reduce spam)
LOGGING_TO_FILE = False        # ← Console vs file logging
LOGGING_FILE = './data/log.txt'

# Progress Tracking Configuration (FREQUENTLY MODIFIED)
PROGRESS_TRACKING_ENABLED = True       # ← Enable progress tracking with ETA
PROGRESS_UPDATE_FREQUENCY = 10         # ← Show progress every N players processed
PROGRESS_ETA_WINDOW_SIZE = 50          # ← Number of recent players to use for ETA calculation (higher = more stable, lower = more responsive)

# =============================================================================
# CONFIGURATION VALIDATION
# =============================================================================

def validate_config():
    """Validate configuration settings"""
    errors = []

    if NFL_SCORING_FORMAT not in ["ppr", "std", "half"]:
        errors.append(f"Invalid NFL_SCORING_FORMAT: {NFL_SCORING_FORMAT}")

    # POSITION_FALLBACK_CONFIG removed - week-by-week only system

    # Validate mutual exclusivity of drafted data loading options
    if PRESERVE_DRAFTED_VALUES and LOAD_DRAFTED_DATA_FROM_FILE:
        errors.append("PRESERVE_DRAFTED_VALUES and LOAD_DRAFTED_DATA_FROM_FILE cannot both be enabled. Choose one method for loading drafted data.")
        
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
1. ESPN_PLAYER_LIMIT - Increase for larger leagues

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