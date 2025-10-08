#!/usr/bin/env python3
"""
NFL Scores Fetcher Configuration

This file contains all the frequently modified constants for the NFL scores fetcher.
Most important and frequently modified settings are at the top.

Author: Kai Mizuno
"""


# Map shared variables to local names for backwards compatibility
NFL_SCORES_SEASON = 2025
NFL_SCORES_CURRENT_WEEK = 5

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
DEFAULT_FILE_CAPS = {'csv': 5, 'json': 5, 'xlsx': 5, 'txt': 5}

# =============================================================================
# API CONFIGURATION
# =============================================================================

# API settings
REQUEST_TIMEOUT = 30
RATE_LIMIT_DELAY = 0.2

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

LOGGING_LEVEL = 'INFO'      # ← DEBUG, INFO, WARNING, ERROR, CRITICAL (WARNING+ to reduce spam)
LOGGING_TO_FILE = False        # ← Console vs file logging
LOG_NAME = "nfl_scores_fetcher"
LOGGING_FILE = './data/log.txt'
LOGGING_FORMAT = 'standard'     # detailed / standard / simple