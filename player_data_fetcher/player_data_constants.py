#!/usr/bin/env python3
"""
Player Data Constants and Mappings

This module contains all constant values and mappings used for NFL player data collection
from ESPN API. Separated from the main script for better maintainability.

Author: Kai Mizuno
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