#!/usr/bin/env python3
"""
Run Schedule Data Fetcher

Fetches complete NFL season schedule from ESPN API and exports to season_schedule.csv.

Usage:
    python run_schedule_fetcher.py

Output:
    data/season_schedule.csv - Complete season schedule with bye weeks

Author: Kai Mizuno
"""

import asyncio
import sys
from pathlib import Path

# Add schedule-data-fetcher to path
sys.path.append(str(Path(__file__).parent / "schedule-data-fetcher"))
sys.path.append(str(Path(__file__).parent / "player-data-fetcher"))

from ScheduleFetcher import ScheduleFetcher
from config import NFL_SEASON


async def main():
    """Main entry point for schedule fetcher."""
    try:
        # Define output path
        output_path = Path(__file__).parent / "data" / "season_schedule.csv"

        # Create fetcher
        fetcher = ScheduleFetcher(output_path)

        print(f"Fetching NFL season schedule for {NFL_SEASON}...")

        # Fetch schedule from ESPN API
        schedule = await fetcher.fetch_full_schedule(NFL_SEASON)

        if not schedule:
            print("ERROR: Failed to fetch schedule data")
            return 1

        # Export to CSV
        fetcher.export_to_csv(schedule)

        print(f"✓ Schedule successfully exported to {output_path}")
        print(f"  - Weeks: {len(schedule)}")
        print(f"  - Season: {NFL_SEASON}")

        return 0

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
