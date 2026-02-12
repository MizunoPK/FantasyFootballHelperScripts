#!/usr/bin/env python3
"""
Run Schedule Data Fetcher

Fetches complete NFL season schedule from ESPN API and exports to season_schedule.csv.

Usage:
    python run_schedule_fetcher.py [--enable-log-file]

Options:
    --enable-log-file    Enable logging to file (default: console only)

Output:
    data/season_schedule.csv - Complete season schedule with bye weeks

Author: Kai Mizuno
"""

import argparse
import asyncio
import sys
from pathlib import Path

from utils.LoggingManager import setup_logger

# Add schedule-data-fetcher to path
sys.path.append(str(Path(__file__).parent / "schedule-data-fetcher"))
sys.path.append(str(Path(__file__).parent / "player-data-fetcher"))

from ScheduleFetcher import ScheduleFetcher
NFL_SEASON = 2025


async def main():
    """Main entry point for schedule fetcher."""
    # Parse arguments (synchronous, runs before async operations)
    parser = argparse.ArgumentParser(description="Fetch NFL season schedule from ESPN API")
    parser.add_argument(
        '--enable-log-file',
        action='store_true',
        help='Enable logging to file (default: console only)'
    )
    args = parser.parse_args()

    # Setup logger (ONCE in entry script)
    logger = setup_logger(
        name="schedule_fetcher",
        level="INFO",
        log_to_file=args.enable_log_file,
        log_file_path=None,
        log_format="standard"
    )

    try:
        # Define output path
        output_path = Path(__file__).parent / "data" / "season_schedule.csv"

        # Create fetcher
        fetcher = ScheduleFetcher(output_path)

        logger.info(f"Fetching NFL season schedule for {NFL_SEASON}...")

        # Fetch schedule from ESPN API
        schedule = await fetcher.fetch_full_schedule(NFL_SEASON)

        if not schedule:
            logger.error("Failed to fetch schedule data")
            return 1

        # Export to CSV
        fetcher.export_to_csv(schedule)

        logger.info(f"Schedule successfully exported to {output_path}")
        logger.info(f"  Weeks: {len(schedule)}, Season: {NFL_SEASON}")

        return 0

    except Exception as e:
        logger.error(f"Unhandled error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
