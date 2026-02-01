#!/usr/bin/env python3
"""
Runner Script for Player Data Fetcher

This script provides a CLI wrapper with argparse support for the player data fetcher.
Supports 23 CLI arguments to override config.py constants, plus debug and E2E test modes.

Usage:
    python run_player_fetcher.py [OPTIONS]
    python run_player_fetcher.py --debug
    python run_player_fetcher.py --e2e-test
    python run_player_fetcher.py --week 12 --season 2025 --debug

Author: Kai Mizuno
"""

import argparse
import asyncio
import importlib
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> None:
    """
    Main entry point for player data fetcher CLI wrapper.

    Parses CLI arguments, overrides config.py constants, and runs the fetcher.
    Supports debug mode (--debug) and E2E test mode (--e2e-test).

    Args:
        argv: Optional list of command-line arguments (default: sys.argv). Used for testing.

    Returns:
        None (calls sys.exit() on errors or asyncio.run() for main execution)

    Raises:
        SystemExit: On argument parsing errors, config import failures, or validation errors

    Example:
        # Run with default settings
        $ python run_player_fetcher.py

        # Run with week override
        $ python run_player_fetcher.py --week 12

        # Run in debug mode (DEBUG logging + minimal data fetch)
        $ python run_player_fetcher.py --debug

        # Run E2E test mode (limited data fetch, <=3 min)
        $ python run_player_fetcher.py --e2e-test

        # Combine modes (E2E limits + debug logging)
        $ python run_player_fetcher.py --debug --e2e-test

    Notes:
        - Mode precedence: E2E takes precedence for data limits, debug for logging
        - All arguments default=None to distinguish "not provided" vs explicit value
        - Config overrides applied before importing player_data_fetcher_main
    """
    # Create argument parser
    parser = argparse.ArgumentParser(
        description='Player Data Fetcher - Fetch NFL player projections from ESPN API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python run_player_fetcher.py                    # Run with default settings
  python run_player_fetcher.py --week 12         # Override current NFL week
  python run_player_fetcher.py --debug            # Debug mode (minimal data + DEBUG logs)
  python run_player_fetcher.py --e2e-test         # E2E test mode (fast fetch, <=3 min)
  python run_player_fetcher.py --debug --e2e-test # Combined modes
        '''
    )

    # Week/Season Arguments
    parser.add_argument(
        '--week',
        type=int,
        default=None,
        help='Current NFL week (1-18). Default: 17 from config'
    )

    parser.add_argument(
        '--season',
        type=int,
        default=None,
        help='Current NFL season year (e.g., 2025). Default: 2025 from config'
    )

    # Data Preservation Arguments
    parser.add_argument(
        '--preserve-locked',
        action='store_true',
        default=None,
        help='Keep locked players between data updates. Default: False from config'
    )

    parser.add_argument(
        '--load-drafted-data',
        action='store_true',
        dest='load_drafted_data',
        default=None,
        help='Load drafted state from external CSV file. Default: True from config'
    )

    parser.add_argument(
        '--no-load-drafted-data',
        action='store_false',
        dest='load_drafted_data',
        help='Disable loading drafted data from file'
    )

    parser.add_argument(
        '--drafted-data-file',
        type=str,
        default=None,
        help='Path to CSV file containing drafted player data. Default: "../data/drafted_data.csv" from config'
    )

    parser.add_argument(
        '--my-team-name',
        type=str,
        default=None,
        help='Name of your fantasy team for identifying roster players. Default: "Sea Sharp" from config'
    )

    # Output Format Arguments
    parser.add_argument(
        '--output-dir',
        type=str,
        default=None,
        help='Output directory for generated files. Default: "./data" from config'
    )

    parser.add_argument(
        '--create-csv',
        action='store_true',
        dest='create_csv',
        default=None,
        help='Create CSV output file. Default: True from config'
    )

    parser.add_argument(
        '--no-csv',
        action='store_false',
        dest='create_csv',
        help='Disable CSV output'
    )

    parser.add_argument(
        '--create-json',
        action='store_true',
        dest='create_json',
        default=None,
        help='Create JSON output file. Default: False from config'
    )

    parser.add_argument(
        '--no-json',
        action='store_false',
        dest='create_json',
        help='Disable JSON output'
    )

    parser.add_argument(
        '--create-excel',
        action='store_true',
        dest='create_excel',
        default=None,
        help='Create Excel output file. Default: False from config'
    )

    parser.add_argument(
        '--no-excel',
        action='store_false',
        dest='create_excel',
        help='Disable Excel output'
    )

    parser.add_argument(
        '--create-condensed-excel',
        action='store_true',
        dest='create_condensed_excel',
        default=None,
        help='Create condensed Excel output file. Default: False from config'
    )

    parser.add_argument(
        '--no-condensed-excel',
        action='store_false',
        dest='create_condensed_excel',
        help='Disable condensed Excel output'
    )

    parser.add_argument(
        '--create-position-json',
        action='store_true',
        dest='create_position_json',
        default=None,
        help='Generate position-based JSON files (QB, RB, WR, TE, K, DST). Default: True from config'
    )

    parser.add_argument(
        '--no-position-json',
        action='store_false',
        dest='create_position_json',
        help='Disable position JSON output'
    )

    parser.add_argument(
        '--position-json-output',
        type=str,
        default=None,
        help='Output folder for position-based JSON files. Default: "../data/player_data" from config'
    )

    # File Path Arguments
    parser.add_argument(
        '--team-data-folder',
        type=str,
        default=None,
        help='Output folder for per-team historical data files. Default: "../data/team_data" from config'
    )

    parser.add_argument(
        '--game-data-csv',
        type=str,
        default=None,
        help='Output file for game-level data (venue, weather, scores). Default: "../data/game_data.csv" from config'
    )

    # Feature Toggle Arguments
    parser.add_argument(
        '--enable-historical-save',
        action='store_true',
        dest='enable_historical_save',
        default=None,
        help='Automatically save weekly data snapshots to historical folder. Default: False from config'
    )

    parser.add_argument(
        '--no-historical-save',
        action='store_false',
        dest='enable_historical_save',
        help='Disable historical data saving'
    )

    parser.add_argument(
        '--enable-game-data',
        action='store_true',
        dest='enable_game_data',
        default=None,
        help='Enable game data fetching during player data collection. Default: True from config'
    )

    parser.add_argument(
        '--no-game-data',
        action='store_false',
        dest='enable_game_data',
        help='Disable game data fetching'
    )

    # Logging Arguments
    parser.add_argument(
        '--log-level',
        type=str,
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default=None,
        help='Logging level. Default: INFO from config'
    )

    parser.add_argument(
        '--log-to-file',
        action='store_true',
        dest='log_to_file',
        default=None,
        help='Enable logging to file. Default: False from config'
    )

    parser.add_argument(
        '--no-log-file',
        action='store_false',
        dest='log_to_file',
        help='Disable logging to file'
    )

    parser.add_argument(
        '--log-file',
        type=str,
        default=None,
        help='Path to log file. Default: "./data/log.txt" from config'
    )

    parser.add_argument(
        '--progress-frequency',
        type=int,
        default=None,
        help='Show progress every N players processed. Default: 10 from config'
    )

    # Special Mode Arguments
    parser.add_argument(
        '--debug',
        action='store_true',
        default=False,
        help='Enable debug mode (DEBUG logging + minimal data fetch for fast execution)'
    )

    parser.add_argument(
        '--e2e-test',
        action='store_true',
        default=False,
        help='Enable E2E test mode (limited player fetch with real API, <=3 min)'
    )

    # Parse arguments
    args = parser.parse_args(argv)

    # Get fetcher directory
    script_dir = Path(__file__).parent
    fetcher_dir = script_dir / "player-data-fetcher"

    # Add fetcher directory to Python path
    sys.path.insert(0, str(fetcher_dir))

    # Import config module (must import before applying overrides)
    try:
        config = importlib.import_module('config')
    except ImportError as e:
        print(f"[ERROR] Failed to import config module: {e}")
        print(f"[ERROR] Expected location: {fetcher_dir / 'config.py'}")
        sys.exit(1)

    # Apply debug mode config overrides FIRST (User Answer Q4 - debug mode includes behavioral changes + DEBUG logs)
    if args.debug:
        config.LOGGING_LEVEL = 'DEBUG'
        config.ESPN_PLAYER_LIMIT = 100
        config.PROGRESS_UPDATE_FREQUENCY = 5
        config.ENABLE_GAME_DATA_FETCH = False
        config.ENABLE_HISTORICAL_DATA_SAVE = False
        # Force minimal output formats (User Answer Q4 - keep only fast formats)
        config.CREATE_CSV = True
        config.CREATE_JSON = False
        config.CREATE_EXCEL = False
        config.CREATE_CONDENSED_EXCEL = False
        config.CREATE_POSITION_JSON = True

    # Apply E2E test mode config overrides SECOND (User Answer Q3 - E2E precedence for data limits)
    if args.e2e_test:
        config.ESPN_PLAYER_LIMIT = 100  # E2E precedence (overrides debug if both specified)
        config.ENABLE_GAME_DATA_FETCH = False
        config.ENABLE_HISTORICAL_DATA_SAVE = False
        config.CREATE_EXCEL = False
        config.CREATE_JSON = False
        # Note: If debug was set, LOGGING_LEVEL stays 'DEBUG' (not overridden by E2E mode)

    # Apply individual CLI argument overrides (after mode overrides)
    # Week argument with validation
    if args.week is not None:
        if args.week < 1 or args.week > 18:
            print(f"[ERROR] Invalid week: {args.week}. Must be between 1 and 18.")
            sys.exit(1)
        config.CURRENT_NFL_WEEK = args.week

    # Season argument with unusual value warning
    if args.season is not None:
        if args.season < 2020 or args.season > 2030:
            print(f"[WARNING] Unusual season value: {args.season}. Are you sure?")
        config.NFL_SEASON = args.season

    # Data preservation arguments
    if args.preserve_locked is not None:
        config.PRESERVE_LOCKED_VALUES = args.preserve_locked

    if args.load_drafted_data is not None:
        config.LOAD_DRAFTED_DATA_FROM_FILE = args.load_drafted_data

    if args.drafted_data_file is not None:
        config.DRAFTED_DATA = args.drafted_data_file

    if args.my_team_name is not None:
        config.MY_TEAM_NAME = args.my_team_name

    # Output format arguments
    if args.output_dir is not None:
        config.OUTPUT_DIRECTORY = args.output_dir

    if args.create_csv is not None:
        config.CREATE_CSV = args.create_csv

    if args.create_json is not None:
        config.CREATE_JSON = args.create_json

    if args.create_excel is not None:
        config.CREATE_EXCEL = args.create_excel

    if args.create_condensed_excel is not None:
        config.CREATE_CONDENSED_EXCEL = args.create_condensed_excel

    if args.create_position_json is not None:
        config.CREATE_POSITION_JSON = args.create_position_json

    if args.position_json_output is not None:
        config.POSITION_JSON_OUTPUT = args.position_json_output

    # File path arguments
    if args.team_data_folder is not None:
        config.TEAM_DATA_FOLDER = args.team_data_folder

    if args.game_data_csv is not None:
        config.GAME_DATA_CSV = args.game_data_csv

    # Feature toggle arguments
    if args.enable_historical_save is not None:
        config.ENABLE_HISTORICAL_DATA_SAVE = args.enable_historical_save

    if args.enable_game_data is not None:
        config.ENABLE_GAME_DATA_FETCH = args.enable_game_data

    # Logging arguments
    if args.log_level is not None:
        config.LOGGING_LEVEL = args.log_level

    if args.log_to_file is not None:
        config.LOGGING_TO_FILE = args.log_to_file

    if args.log_file is not None:
        config.LOGGING_FILE = args.log_file

    if args.progress_frequency is not None:
        config.PROGRESS_UPDATE_FREQUENCY = args.progress_frequency

    # Import and run player_data_fetcher_main (after all config overrides applied)
    try:
        player_data_fetcher_main = importlib.import_module('player_data_fetcher_main')
    except ImportError as e:
        print(f"[ERROR] Failed to import player_data_fetcher_main: {e}")
        print(f"[ERROR] Expected location: {fetcher_dir / 'player_data_fetcher_main.py'}")
        sys.exit(1)

    # Run async main
    asyncio.run(player_data_fetcher_main.main())


if __name__ == "__main__":
    main()
