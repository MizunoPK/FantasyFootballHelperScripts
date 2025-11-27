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
import os
import sys
from pathlib import Path


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


def main():
    """Main entry point for game data fetcher."""
    parser = argparse.ArgumentParser(
        description="Fetch NFL game data (venue, weather, scores) from ESPN and Open-Meteo APIs"
    )
    parser.add_argument(
        '--season',
        type=int,
        default=None,
        help='NFL season year (default: current season from config)'
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
        default=None,
        help='Override current NFL week (default: from config)'
    )

    args = parser.parse_args()

    # Get the directory where this script is located (project root)
    script_dir = Path(__file__).parent

    # Construct path to the player-data-fetcher module directory
    fetcher_dir = script_dir / "player-data-fetcher"

    # Save current working directory to restore later
    original_cwd = os.getcwd()

    try:
        # Change to fetcher directory so imports work correctly
        os.chdir(fetcher_dir)

        # Add fetcher directory to path
        sys.path.insert(0, str(fetcher_dir))
        sys.path.insert(0, str(script_dir))

        # Import after changing directory
        from game_data_fetcher import fetch_game_data, GameDataFetcher
        from config import NFL_SEASON, CURRENT_NFL_WEEK
        from utils.LoggingManager import setup_logger

        # Setup logging
        logger = setup_logger("game_data_fetcher", "INFO", False, None, "standard")

        # Determine parameters
        season = args.season if args.season else NFL_SEASON
        current_week = args.current_week if args.current_week else CURRENT_NFL_WEEK

        # For historical seasons (like 2024), use week 18 as current week
        if args.season and args.season < NFL_SEASON:
            current_week = 18
            logger.info(f"Historical season {season}: setting current_week to 18")

        # Determine output path
        if args.output:
            output_path = script_dir / args.output
        else:
            output_path = script_dir / "data" / "game_data.csv"

        # Parse weeks if specified
        weeks = None
        if args.weeks:
            weeks = parse_weeks(args.weeks)
            logger.info(f"Fetching specific weeks: {weeks}")

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
            weeks=weeks
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
    finally:
        # Always restore original working directory
        os.chdir(original_cwd)


if __name__ == "__main__":
    main()
