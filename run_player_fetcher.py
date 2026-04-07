#!/usr/bin/env python3
"""
Runner Script for Player Data Fetcher

This script runs the player data fetcher directly (no subprocess).

Usage:
    python run_player_fetcher.py
    python run_player_fetcher.py --help
    python run_player_fetcher.py --week 1 --e2e-test

Author: Kai Mizuno
"""

import argparse
import asyncio
import tempfile
from pathlib import Path

from player_data_fetcher.player_data_fetcher_main import main


def parse_args(argv=None):
    """Parse command-line arguments for the player data fetcher runner."""
    parser = argparse.ArgumentParser(
        description='Fetch NFL player projection data from ESPN'
    )

    parser.add_argument(
        '--e2e-test',
        action='store_true',
        default=False,
        help='Run in end-to-end test mode (limits ESPN player fetch to 100)'
    )
    parser.add_argument(
        '--log-level',
        type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Logging level (default: INFO)'
    )
    parser.add_argument(
        '--enable-log-file',
        action='store_true',
        default=False,
        help='Enable file logging to logs/player_data_fetcher/'
    )

    parser.add_argument(
        '--week',
        type=int,
        default=17,
        help='Current NFL week number (default: 17)'
    )
    parser.add_argument(
        '--season',
        type=int,
        default=2025,
        help='NFL season year (default: 2025)'
    )

    parser.add_argument(
        '--my-team-name',
        type=str,
        default='Sea Sharp',
        help='Your fantasy team name (default: Sea Sharp)'
    )
    parser.add_argument(
        '--load-drafted-data',
        action=argparse.BooleanOptionalAction,
        default=True,
        help='Load drafted roster data (default: enabled)'
    )
    parser.add_argument(
        '--drafted-data-path',
        type=str,
        default='../data/drafted_data.csv',
        help='Path to drafted data CSV (default: ../data/drafted_data.csv)'
    )

    parser.add_argument(
        '--position-json-output',
        type=str,
        default='../data/player_data',
        help='Output directory for position JSON files (default: ../data/player_data)'
    )
    parser.add_argument(
        '--team-data-folder',
        type=str,
        default='../data/team_data',
        help='Output directory for team data files (default: ../data/team_data)'
    )
    parser.add_argument(
        '--game-data-csv',
        type=str,
        default='../data/game_data.csv',
        help='Output path for game data CSV (default: ../data/game_data.csv)'
    )

    parser.add_argument(
        '--enable-historical-save',
        action='store_true',
        default=False,
        help='Save historical snapshot of player data'
    )
    parser.add_argument(
        '--enable-game-data',
        action=argparse.BooleanOptionalAction,
        default=True,
        help='Fetch NFL game data (default: enabled)'
    )

    parser.add_argument(
        '--espn-player-limit',
        type=int,
        default=2000,
        help='Maximum number of ESPN players to fetch (default: 2000)'
    )
    parser.add_argument(
        '--request-timeout',
        type=int,
        default=30,
        help='HTTP request timeout in seconds (default: 30)'
    )
    parser.add_argument(
        '--rate-limit-delay',
        type=float,
        default=0.2,
        help='Delay between API requests in seconds (default: 0.2)'
    )
    parser.add_argument(
        '--progress-frequency',
        type=int,
        default=10,
        help='How often to log progress updates (every N players, default: 10)'
    )

    return parser.parse_args(argv)


def create_settings_dict(args) -> dict:
    """Convert parsed args to a settings dict for player_data_fetcher_main.main()."""
    espn_player_limit = 100 if args.e2e_test else args.espn_player_limit

    if args.e2e_test:
        tmp_dir = tempfile.mkdtemp(prefix='player_fetcher_e2e_')
        position_json_output = str(Path(tmp_dir) / 'player_data')
        team_data_folder = str(Path(tmp_dir) / 'team_data')
        game_data_csv = str(Path(tmp_dir) / 'game_data.csv')
    else:
        position_json_output = args.position_json_output
        team_data_folder = args.team_data_folder
        game_data_csv = args.game_data_csv

    return {
        'e2e_test': args.e2e_test,
        'log_level': args.log_level,
        'logging_to_file': args.enable_log_file,
        'current_nfl_week': args.week,
        'season': args.season,
        'my_team_name': args.my_team_name,
        'load_drafted_data': args.load_drafted_data,
        'drafted_data_path': args.drafted_data_path,
        'position_json_output': position_json_output,
        'team_data_folder': team_data_folder,
        'game_data_csv': game_data_csv,
        'enable_historical_save': args.enable_historical_save,
        'enable_game_data': args.enable_game_data,
        'espn_player_limit': espn_player_limit,
        'request_timeout': args.request_timeout,
        'rate_limit_delay': args.rate_limit_delay,
        'progress_frequency': args.progress_frequency,
    }


if __name__ == "__main__":
    args = parse_args()
    settings_dict = create_settings_dict(args)
    asyncio.run(main(settings_dict))


