#!/usr/bin/env python3
"""
Player Data Fetcher Configuration

This file contains all the frequently modified constants for the player data fetcher.
Most important and frequently modified settings are at the top.

Author: Kai Mizuno
"""

CURRENT_NFL_WEEK = 17     # Current NFL week (1-18, update weekly)
NFL_SEASON = 2025        # Current NFL season year

# Drafted Data Loading Settings (FREQUENTLY MODIFIED)
LOAD_DRAFTED_DATA_FROM_FILE = True  # Load drafted state from external CSV file (alternative to PRESERVE_DRAFTED_VALUES)
DRAFTED_DATA = "../data/drafted_data.csv"  # Path to CSV file containing drafted player data (now in root data/ directory)
MY_TEAM_NAME = "Sea Sharp"           # Name of your fantasy team for identifying roster players (drafted=2)

# Position JSON Output Settings
POSITION_JSON_OUTPUT = "../data/player_data"  # Output folder for position-based JSON files

# File Paths (FREQUENTLY MODIFIED)
TEAM_DATA_FOLDER = '../data/team_data'  # Output folder for per-team historical data files
GAME_DATA_CSV = '../data/game_data.csv'  # Output file for game-level data (venue, weather, scores)
COORDINATES_JSON = 'coordinates.json'  # Stadium coordinates for weather lookups

# Historical Data Auto-Save Configuration (FREQUENTLY MODIFIED)
ENABLE_HISTORICAL_DATA_SAVE = False  # Automatically save weekly data snapshots to historical folder

# Game Data Fetcher Configuration (FREQUENTLY MODIFIED)
ENABLE_GAME_DATA_FETCH = True  # Enable game data fetching during player data collection

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

LOGGING_LEVEL = 'INFO'      # ← DEBUG, INFO, WARNING, ERROR, CRITICAL (WARNING+ to reduce spam)
LOG_NAME = "player_data_fetcher"
LOGGING_FORMAT = 'standard'     # detailed / standard / simple
# Note: File logging is now controlled via --enable-log-file CLI flag (not config constants)

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