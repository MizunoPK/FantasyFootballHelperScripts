#!/usr/bin/env python3
"""
Player Data Constants and Mappings

This module contains all constant values and mappings used for NFL player data collection
from ESPN API. Separated from the main script for better maintainability.

Author: Kai Mizuno
Last Updated: September 2025
"""

from typing import Dict, List
from dataclasses import dataclass
from typing_extensions import TypedDict

# ESPN Team ID to Abbreviation Mapping
ESPN_TEAM_MAPPINGS: Dict[int, str] = {
    1: 'ATL', 2: 'BUF', 3: 'CHI', 4: 'CIN', 5: 'CLE', 6: 'DAL',
    7: 'DEN', 8: 'DET', 9: 'GB', 10: 'TEN', 11: 'IND', 12: 'KC',
    13: 'LV', 14: 'LAR', 15: 'MIA', 16: 'MIN', 17: 'NE', 18: 'NO',
    19: 'NYG', 20: 'NYJ', 21: 'PHI', 22: 'ARI', 23: 'PIT', 24: 'LAC',
    25: 'SF', 26: 'SEA', 27: 'TB', 28: 'WSH', 29: 'CAR', 30: 'JAX',
    33: 'BAL', 34: 'HOU'
}

# ESPN Position ID to Position Name Mapping
ESPN_POSITION_MAPPINGS: Dict[int, str] = {
    1: 'QB', 
    2: 'RB', 
    3: 'WR', 
    4: 'TE', 
    5: 'K', 
    16: 'DST'
}

# Removed unused ESPN_STAT_MAPPINGS - detailed stats not currently extracted

# Removed unused INJURY_RISK_LEVELS - risk assessment not implemented

# Removed unused VALID_POSITIONS and VALID_INJURY_STATUSES - validation not implemented

# API Configuration (moved to config.py)

# =============================================================================
# PLAYER DATA CONSTANTS - PARTIALLY MIGRATED TO CONFIG.PY
# =============================================================================
"""
Frequently modified constants have been moved to config.py.
ESPN-specific mappings and technical constants remain here.
"""

import sys
from pathlib import Path

# Import frequently modified constants from script-specific config
from shared_files.configs.player_data_fetcher_config import (
    EXCEL_POSITION_SHEETS, PRESERVE_DRAFTED_VALUES, PRESERVE_LOCKED_VALUES,
    EXPORT_COLUMNS, PLAYERS_CSV, ESPN_USER_AGENT, ESPN_PLAYER_LIMIT,
    REQUEST_TIMEOUT, RATE_LIMIT_DELAY, NFL_SEASON, NFL_SCORING_FORMAT,
    OUTPUT_DIRECTORY, CREATE_CSV, CREATE_JSON, CREATE_EXCEL, CREATE_CONDENSED_EXCEL,
    LOGGING_ENABLED, LOGGING_LEVEL, LOGGING_TO_FILE, LOGGING_FILE,
    CURRENT_NFL_WEEK, INCLUDE_PLAYOFF_WEEKS, RECENT_WEEKS_FOR_AVERAGE,
    SKIP_DRAFTED_PLAYER_UPDATES, LOAD_DRAFTED_DATA_FROM_FILE, DRAFTED_DATA, MY_TEAM_NAME,
    USE_SCORE_THRESHOLD, PLAYER_SCORE_THRESHOLD
)

# Adjust file paths for player-data-fetcher subdirectory context
# PLAYERS_CSV already has '../' prefix, so we use it directly
DRAFT_HELPER_PLAYERS_FILE = PLAYERS_CSV

# ADP-related constants removed - week-by-week only system

# Removed unused constants: ESPN_BASE_URL, ESPN_FANTASY_FILTER, EXPORT_COLUMNS, TOP_PLAYERS_SUMMARY_COUNT