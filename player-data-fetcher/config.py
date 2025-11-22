#!/usr/bin/env python3
"""
Player Data Fetcher Configuration

This file contains all the frequently modified constants for the player data fetcher.
Most important and frequently modified settings are at the top.

Author: Kai Mizuno
"""

from dataclasses import dataclass

CURRENT_NFL_WEEK = 12     # Current NFL week (1-18, update weekly)
NFL_SEASON = 2025        # Current NFL season year

# Data Preservation Settings (FREQUENTLY MODIFIED)
PRESERVE_DRAFTED_VALUES = False   # Keep draft status between data updates
PRESERVE_LOCKED_VALUES = False    # Keep locked players between data updates

# Drafted Data Loading Settings (FREQUENTLY MODIFIED)
LOAD_DRAFTED_DATA_FROM_FILE = True  # Load drafted state from external CSV file (alternative to PRESERVE_DRAFTED_VALUES)
DRAFTED_DATA = "../data/drafted_data.csv"  # Path to CSV file containing drafted player data (now in root data/ directory)
MY_TEAM_NAME = "Sea Sharp"           # Name of your fantasy team for identifying roster players (drafted=2)

# Optimization Settings (FREQUENTLY MODIFIED)
SKIP_DRAFTED_PLAYER_UPDATES = False  # Skip API calls for drafted=1 players (major optimization)
USE_SCORE_THRESHOLD = False  # Only update players above score threshold (preserves low-scoring player data)
PLAYER_SCORE_THRESHOLD = 40.0  # Minimum fantasy points to trigger API update

# Output Settings (FREQUENTLY MODIFIED)
OUTPUT_DIRECTORY = "./data"
CREATE_CSV = True
CREATE_JSON = False
CREATE_EXCEL = False
CREATE_CONDENSED_EXCEL = False
DEFAULT_FILE_CAPS = {'csv': 5, 'json': 5, 'xlsx': 5, 'txt': 5}

# File Paths (FREQUENTLY MODIFIED)
PLAYERS_CSV = '../data/players.csv'
TEAM_DATA_FOLDER = '../data/team_data'  # Output folder for per-team historical data files

# Historical Data Auto-Save Configuration (FREQUENTLY MODIFIED)
ENABLE_HISTORICAL_DATA_SAVE = True  # Automatically save weekly data snapshots to historical folder

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

LOGGING_LEVEL = 'INFO'      # ← DEBUG, INFO, WARNING, ERROR, CRITICAL (WARNING+ to reduce spam)
LOGGING_TO_FILE = False        # ← Console vs file logging
LOG_NAME = "player_data_fetcher"
LOGGING_FILE = './data/log.txt'
LOGGING_FORMAT = 'standard'     # detailed / standard / simple

# Progress Tracking Configuration (FREQUENTLY MODIFIED)
PROGRESS_UPDATE_FREQUENCY = 10         # ← Show progress every N players processed
PROGRESS_ETA_WINDOW_SIZE = 50          # ← Number of recent players to use for ETA calculation (higher = more stable, lower = more responsive)


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