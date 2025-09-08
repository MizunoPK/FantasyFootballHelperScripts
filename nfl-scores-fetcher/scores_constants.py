#!/usr/bin/env python3
"""
NFL Scores Constants and Mappings

This module contains all constant values and mappings used for NFL game scores
collection from ESPN API. Separated for better maintainability.

Author: Generated for NFL Fantasy Data Collection
Last Updated: September 2025
"""

from typing import Dict

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