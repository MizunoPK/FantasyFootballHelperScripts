#!/usr/bin/env python3
"""
Runner Script for Game Data Fetcher

This script runs the game data fetcher to collect NFL game information
including venue, weather, and scores from ESPN and Open-Meteo APIs.

Usage:
    # Fetch current season data (default)
    python run_game_data_fetcher.py

    # Fetch 2024 season data for simulation
    python run_game_data_fetcher.py --season 2024 --output simulation/sim_data/game_data.csv

    # Fetch specific weeks
    python run_game_data_fetcher.py --weeks 1-5
    python run_game_data_fetcher.py --weeks 1,3,5,7

Author: Kai Mizuno
"""

import argparse
import sys
from pathlib import Path

# Module-level sys.path setup
_script_dir = Path(__file__).parent
_fetcher_dir = _script_dir / "player-data-fetcher"
sys.path.insert(0, str(_fetcher_dir))
sys.path.insert(0, str(_script_dir))

from game_data_fetcher import fetch_game_data, GameDataFetcher  # noqa: E402
from utils.LoggingManager import setup_logger  # noqa: E402


def parse_weeks(weeks_str: str) -> list:
    """
    Parse weeks string into list of week numbers.

    Args:
        weeks_str: Weeks specification like "1-18" or "1,3,5,7"

    Returns:
        List of week numbers
    """
    weeks = []

    if '-' in weeks_str and ',' not in weeks_str:
        # Range format: "1-18"
        start, end = weeks_str.split('-')
        weeks = list(range(int(start), int(end) + 1))
    elif ',' in weeks_str:
        # List format: "1,3,5,7"
        weeks = [int(w.strip()) for w in weeks_str.split(',')]
    else:
        # Single week: "5"
        weeks = [int(weeks_str)]

    return weeks


def parse_args(argv=None):
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Fetch NFL game data (venue, weather, scores) from ESPN and Open-Meteo APIs"
    )
    parser.add_argument(
        '--season',
        type=int,
        default=2025,
        help='NFL season year (default: 2025)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Output file path (default: data/game_data.csv)'
    )
    parser.add_argument(
        '--weeks',
        type=str,
        default=None,
        help='Weeks to fetch: "1-18" for range, "1,3,5" for specific weeks'
    )
    parser.add_argument(
        '--current-week',
        type=int,
        default=17,
        help='Override current NFL week (default: 17)'
    )
    parser.add_argument(
        '--e2e-test',
        action='store_true',
        default=False,
        help='E2E test mode: limits to week 1, outputs to /tmp/game_data_e2e_test.csv'
    )
    parser.add_argument(
        '--log-level',
        type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Logging level (default: INFO)'
    )
    parser.add_argument(
        '--request-timeout',
        type=int,
        default=30,
        help='HTTP request timeout in seconds (default: 30)'
    )
    parser.add_argument(
        '--historical-season',
        action='store_true',
        default=False,
        help='Fetch a past season: overrides current_week to 18 (all weeks)'
    )
    return parser.parse_args(argv)


def main():
    """Main entry point for game data fetcher."""
    args = parse_args()

    try:
        # Setup logging
        logger = setup_logger("game_data_fetcher", args.log_level, False, None, "standard")

        # Determine parameters
        season = args.season
        current_week = args.current_week

        # Historical season mode: fetch all 18 weeks
        if args.historical_season:
            current_week = 18
            logger.info(f"Historical season mode: fetching all 18 weeks for {args.season}")

        # Determine output path
        if args.output:
            output_path = _script_dir / args.output
        else:
            output_path = _script_dir / "data" / "game_data.csv"

        # E2E test mode: limit to week 1, override output path
        if args.e2e_test:
            weeks = [1]
            logger.info("E2E test mode: limiting to week 1")
            output_path = Path("/tmp/game_data_e2e_test.csv")
        elif args.weeks:
            weeks = parse_weeks(args.weeks)
            logger.info(f"Fetching specific weeks: {weeks}")
        else:
            weeks = None

        # Log configuration
        logger.info(f"Game Data Fetcher Configuration:")
        logger.info(f"  Season: {season}")
        logger.info(f"  Current Week: {current_week}")
        logger.info(f"  Output: {output_path}")
        if weeks:
            logger.info(f"  Weeks: {weeks}")

        # Fetch game data
        print(f"\n[INFO] Fetching game data for {season} season...")

        result_path = fetch_game_data(
            output_path=output_path,
            season=season,
            current_week=current_week,
            weeks=weeks,
            request_timeout=args.request_timeout
        )

        print(f"\n[SUCCESS] Game data saved to: {result_path}")

        # Print summary
        import pandas as pd
        df = pd.read_csv(result_path)
        print(f"\nSummary:")
        print(f"  Total games: {len(df)}")
        print(f"  Weeks covered: {df['week'].min()} - {df['week'].max()}")
        print(f"  Games with scores: {df['home_team_score'].notna().sum()}")
        print(f"  Indoor games: {(df['indoor'] == True).sum()}")
        print(f"  Outdoor games with weather: {df['temperature'].notna().sum()}")

    except Exception as e:
        print(f"\n[ERROR] Failed to fetch game data: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
