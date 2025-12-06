#!/usr/bin/env python3
"""
Historical Data Compiler Module

A standalone module for compiling historical NFL season data from ESPN APIs.
Creates point-in-time snapshots for simulation system testing.

Usage:
    python compile_historical_data.py --year 2024

Author: Kai Mizuno
"""

from .constants import (
    ESPN_TEAM_MAPPINGS,
    ESPN_POSITION_MAPPINGS,
    ALL_NFL_TEAMS,
    FANTASY_POSITIONS,
    ESPN_FANTASY_API_URL,
    ESPN_SCOREBOARD_API_URL,
    REGULAR_SEASON_WEEKS,
    MIN_SUPPORTED_YEAR,
)

from .http_client import BaseHTTPClient

from .schedule_fetcher import (
    ScheduleFetcher,
    fetch_and_write_schedule,
)

from .game_data_fetcher import (
    GameDataFetcher,
    GameData,
    fetch_and_write_game_data,
)

from .player_data_fetcher import (
    PlayerDataFetcher,
    PlayerData,
    fetch_and_write_player_data,
)

from .team_data_calculator import (
    TeamDataCalculator,
    calculate_and_write_team_data,
)

from .weekly_snapshot_generator import (
    WeeklySnapshotGenerator,
    generate_weekly_snapshots,
)

__all__ = [
    # Constants
    'ESPN_TEAM_MAPPINGS',
    'ESPN_POSITION_MAPPINGS',
    'ALL_NFL_TEAMS',
    'FANTASY_POSITIONS',
    'ESPN_FANTASY_API_URL',
    'ESPN_SCOREBOARD_API_URL',
    'REGULAR_SEASON_WEEKS',
    'MIN_SUPPORTED_YEAR',
    # HTTP Client
    'BaseHTTPClient',
    # Schedule
    'ScheduleFetcher',
    'fetch_and_write_schedule',
    # Game Data
    'GameDataFetcher',
    'GameData',
    'fetch_and_write_game_data',
    # Player Data
    'PlayerDataFetcher',
    'PlayerData',
    'fetch_and_write_player_data',
    # Team Data
    'TeamDataCalculator',
    'calculate_and_write_team_data',
    # Weekly Snapshots
    'WeeklySnapshotGenerator',
    'generate_weekly_snapshots',
]
