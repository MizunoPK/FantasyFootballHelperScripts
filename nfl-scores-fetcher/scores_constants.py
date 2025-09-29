#!/usr/bin/env python3
"""
NFL Scores Constants and Mappings

This module contains all constant values and mappings used for NFL game scores
collection from ESPN API. Separated for better maintainability.

Author: Kai Mizuno
Last Updated: September 2025
"""

from typing import Dict

# Import frequently modified constants from script-specific config
from nfl_scores_fetcher_config import (
    NFL_SCORES_SEASON, NFL_SCORES_SEASON_TYPE, NFL_SCORES_CURRENT_WEEK,
    NFL_SCORES_ONLY_COMPLETED_GAMES, OUTPUT_DIRECTORY, CREATE_CSV,
    CREATE_JSON, CREATE_EXCEL, REQUEST_TIMEOUT, RATE_LIMIT_DELAY,
    LOGGING_ENABLED, LOGGING_LEVEL, LOGGING_TO_FILE, LOGGING_FILE
)

# ESPN API Configuration
ESPN_NFL_BASE_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl"
ESPN_USER_AGENT = "NFL-Scores-Collector/2.0"

# Game Status Constants
STATUS_IN_PROGRESS = "STATUS_IN_PROGRESS"
STATUS_FINAL = "STATUS_FINAL"

# NFL Team Abbreviation to Name Mapping
NFL_TEAM_NAMES: Dict[str, str] = {
    'ARI': 'Cardinals', 'ATL': 'Falcons', 'BAL': 'Ravens', 'BUF': 'Bills',
    'CAR': 'Panthers', 'CHI': 'Bears', 'CIN': 'Bengals', 'CLE': 'Browns',
    'DAL': 'Cowboys', 'DEN': 'Broncos', 'DET': 'Lions', 'GB': 'Packers',
    'HOU': 'Texans', 'IND': 'Colts', 'JAX': 'Jaguars', 'KC': 'Chiefs',
    'LAC': 'Chargers', 'LAR': 'Rams', 'LV': 'Raiders', 'MIA': 'Dolphins',
    'MIN': 'Vikings', 'NE': 'Patriots', 'NO': 'Saints', 'NYG': 'Giants',
    'NYJ': 'Jets', 'PHI': 'Eagles', 'PIT': 'Steelers', 'SF': '49ers',
    'SEA': 'Seahawks', 'TB': 'Buccaneers', 'TEN': 'Titans', 'WSH': 'Commanders'
}