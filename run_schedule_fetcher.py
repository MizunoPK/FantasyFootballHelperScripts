#!/usr/bin/env python3
"""
Run Schedule Data Fetcher

Fetches complete NFL season schedule from ESPN API and exports to season_schedule.csv.

Usage:
    python run_schedule_fetcher.py [--season YEAR] [--output PATH] [--force-refresh]
                                   [--timeout SECONDS] [--rate-limit-delay SECONDS]
                                   [--enable-log-file]

Output:
    data/season_schedule.csv - Complete season schedule with bye weeks (default)

Author: Kai Mizuno
"""

import argparse
import asyncio
import sys
from datetime import datetime
from pathlib import Path

from schedule_data_fetcher.ScheduleFetcher import ScheduleFetcher
from utils.LoggingManager import setup_logger


def _non_negative_float(value: str) -> float:
    f = float(value)
    if f < 0:
        raise argparse.ArgumentTypeError(f"must be non-negative, got {f}")
    return f


async def main():
    """Main entry point for schedule fetcher."""
    parser = argparse.ArgumentParser(description="Fetch NFL season schedule from ESPN API")
    parser.add_argument(
        '--enable-log-file',
        action='store_true',
        help='Enable logging to file (default: console only)'
    )
    parser.add_argument(
        '--season',
        type=int,
        default=datetime.now().year,
        help='NFL season year to fetch (default: current calendar year)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default=str(Path(__file__).parent / 'data' / 'season_schedule.csv'),
        help='Output CSV file path (default: data/season_schedule.csv)'
    )
    parser.add_argument(
        '--force-refresh',
        action='store_true',
        help='Force re-fetch even if output file already exists'
    )
    parser.add_argument(
        '--timeout',
        type=_non_negative_float,
        default=30.0,
        help='HTTP client timeout in seconds (default: 30.0)'
    )
    parser.add_argument(
        '--rate-limit-delay',
        type=_non_negative_float,
        default=0.2,
        help='Delay between week requests in seconds (default: 0.2)'
    )
    args = parser.parse_args()

    logger = setup_logger(
        name="schedule_fetcher",
        level="INFO",
        log_to_file=args.enable_log_file,
        log_file_path=None,
        log_format="standard"
    )

    try:
        output_path = Path(args.output)
        try:
            if not args.force_refresh and output_path.stat().st_size > 0:
                logger.info("Schedule file exists, skipping fetch (use --force-refresh to override)")
                return 0
        except FileNotFoundError:
            pass

        fetcher = ScheduleFetcher(output_path, timeout=args.timeout, rate_limit_delay=args.rate_limit_delay)

        logger.info(f"Fetching NFL season schedule for {args.season}...")

        schedule = await fetcher.fetch_full_schedule(args.season)

        if not schedule:
            logger.error("Failed to fetch schedule data")
            return 1

        fetcher.export_to_csv(schedule)

        logger.info(f"Schedule successfully exported to {output_path}")
        logger.info(f"  Weeks: {len(schedule)}, Season: {args.season}")

        return 0

    except Exception as e:
        logger.error(f"Unhandled error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
