#!/usr/bin/env python3
"""
Historical Data Compiler Constants

Contains all constant values and mappings used for historical NFL data compilation
from ESPN API. Adapted from player-data-fetcher/player_data_constants.py.

Author: Kai Mizuno
"""

from typing import Dict, List

# =============================================================================
# ESPN API ENDPOINTS
# =============================================================================

ESPN_FANTASY_API_URL = (
    "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{year}/segments/0/leaguedefaults/3"
)

ESPN_SCOREBOARD_API_URL = (
    "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
)

OPEN_METEO_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# =============================================================================
# ESPN TEAM MAPPINGS
# =============================================================================

# ESPN Team ID (proTeamId) to Abbreviation Mapping
ESPN_TEAM_MAPPINGS: Dict[int, str] = {
    1: 'ATL', 2: 'BUF', 3: 'CHI', 4: 'CIN', 5: 'CLE', 6: 'DAL',
    7: 'DEN', 8: 'DET', 9: 'GB', 10: 'TEN', 11: 'IND', 12: 'KC',
    13: 'LV', 14: 'LAR', 15: 'MIA', 16: 'MIN', 17: 'NE', 18: 'NO',
    19: 'NYG', 20: 'NYJ', 21: 'PHI', 22: 'ARI', 23: 'PIT', 24: 'LAC',
    25: 'SF', 26: 'SEA', 27: 'TB', 28: 'WSH', 29: 'CAR', 30: 'JAX',
    33: 'BAL', 34: 'HOU'
}

# All 32 NFL team abbreviations (canonical list)
ALL_NFL_TEAMS: List[str] = [
    'ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE',
    'DAL', 'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAX', 'KC',
    'LAC', 'LAR', 'LV', 'MIA', 'MIN', 'NE', 'NO', 'NYG',
    'NYJ', 'PHI', 'PIT', 'SEA', 'SF', 'TB', 'TEN', 'WSH'
]

# =============================================================================
# ESPN POSITION MAPPINGS
# =============================================================================

# ESPN Position ID (defaultPositionId) to Position Name Mapping
ESPN_POSITION_MAPPINGS: Dict[int, str] = {
    1: 'QB',
    2: 'RB',
    3: 'WR',
    4: 'TE',
    5: 'K',
    16: 'DST'
}

# Position name to ID reverse mapping
POSITION_TO_ID: Dict[str, int] = {v: k for k, v in ESPN_POSITION_MAPPINGS.items()}

# Fantasy-relevant positions (6 positions)
FANTASY_POSITIONS: List[str] = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']

# ESPN Slot IDs for ranking (different from position IDs)
SLOT_ID_MAPPINGS: Dict[str, int] = {
    'QB': 0,
    'RB': 2,
    'WR': 4,
    'TE': 6,
    'K': 17,
    'DST': 16
}

# =============================================================================
# SEASON CONFIGURATION
# =============================================================================

# Supported years (weekly data available from 2021+)
MIN_SUPPORTED_YEAR = 2021

# Regular season weeks
REGULAR_SEASON_WEEKS = 17

# =============================================================================
# HTTP CLIENT CONFIGURATION
# =============================================================================

# Default request timeout in seconds
REQUEST_TIMEOUT = 30.0

# Rate limit delay between requests (seconds)
RATE_LIMIT_DELAY = 0.3

# Maximum retry attempts
MAX_RETRY_ATTEMPTS = 3

# User agent for ESPN API requests
ESPN_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# =============================================================================
# OUTPUT FILE CONFIGURATION
# =============================================================================

# CSV file names
SEASON_SCHEDULE_FILE = "season_schedule.csv"
GAME_DATA_FILE = "game_data.csv"
PLAYERS_FILE = "players.csv"
PLAYERS_PROJECTED_FILE = "players_projected.csv"

# JSON file names
QB_DATA_FILE = "qb_data.json"
RB_DATA_FILE = "rb_data.json"
WR_DATA_FILE = "wr_data.json"
TE_DATA_FILE = "te_data.json"
K_DATA_FILE = "k_data.json"
DST_DATA_FILE = "dst_data.json"
POSITION_JSON_FILES = {
    'QB': QB_DATA_FILE,
    'RB': RB_DATA_FILE,
    'WR': WR_DATA_FILE,
    'TE': TE_DATA_FILE,
    'K': K_DATA_FILE,
    'DST': DST_DATA_FILE
}

# Folder names
TEAM_DATA_FOLDER = "team_data"
WEEKS_FOLDER = "weeks"


def normalize_team_abbrev(abbrev: str) -> str:
    """
    Normalize team abbreviation to canonical form.

    Args:
        abbrev: Team abbreviation (e.g., 'WAS', 'WSH')

    Returns:
        Normalized abbreviation (e.g., 'WSH')
    """
    # Handle Washington name change (WAS -> WSH)
    if abbrev == 'WAS':
        return 'WSH'
    return abbrev
