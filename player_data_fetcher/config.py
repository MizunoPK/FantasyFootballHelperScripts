#!/usr/bin/env python3
"""
Player Data Fetcher Configuration

This file contains only non-CLI-configurable constants.
All CLI-configurable values (week, season, paths, flags, limits) are managed
via argparse defaults in run_player_fetcher.py.

Author: Kai Mizuno
"""

COORDINATES_JSON = 'coordinates.json'


LOG_NAME = "player_data_fetcher"
LOGGING_FORMAT = 'standard'

PROGRESS_ETA_WINDOW_SIZE = 50


ESPN_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"


