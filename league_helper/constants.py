"""
League Helper Constants

Centralized constants for the Fantasy Football League Helper application.
Defines logging configuration, roster structure, position limits, and
other application-wide settings.

This module provides:
- Logging configuration (level, format, output)
- Position constants (QB, RB, WR, TE, K, DST, FLEX)
- Mode-specific constants (waiver optimizer, recommendations)

Note: Roster construction limits (MAX_POSITIONS, MAX_PLAYERS) and FLEX-eligible
positions (FLEX_ELIGIBLE_POSITIONS) moved to league_config.json

Author: Kai Mizuno
"""

FANTASY_TEAM_NAME = "Sea Sharp"

LOGGING_LEVEL = 'INFO'
LOG_NAME = "league_helper"
LOGGING_FORMAT = 'detailed'


RECOMMENDATION_COUNT = 5

MIN_WAIVER_IMPROVEMENT = 0
NUM_TRADE_RUNNERS_UP = 9

MIN_POSITIONS = {
    "QB": 1,
    "RB": 3,
    "WR": 3,
    "TE": 1,
    "K": 1,
    "DST": 1
}

MIN_TRADE_IMPROVEMENT = 0
VALID_TEAMS = ["Fishoutawater", "Chase-ing points", "Annihilators", "The Injury Report", "Striking Shibas", "Bo Him-ian Rhapsody", "Saquon Deez", "The Eskimo Brothers", "Pidgin"]

RB, WR, QB, TE, K, DST, FLEX = 'RB', 'WR', 'QB', 'TE', 'K', 'DST', 'FLEX'

ALL_POSITIONS = [RB, WR, QB, TE, K, DST]
OFFENSE_POSITIONS = ["QB", "RB", "WR", "TE", "K"]
DEFENSE_POSITIONS = ["DEF", "DST", "D/ST"]

WIND_AFFECTED_POSITIONS = ["QB", "WR", "K"]


POSSIBLE_BYE_WEEKS = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]