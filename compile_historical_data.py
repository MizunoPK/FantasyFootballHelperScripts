#!/usr/bin/env python3
"""
Historical Data Compiler

A standalone script to compile historical NFL season data from ESPN APIs.
Creates point-in-time snapshots for simulation system testing.

Usage:
    python compile_historical_data.py --year 2024
    python compile_historical_data.py --all-years
    python compile_historical_data.py --year 2025 --format both --weeks 3
    python compile_historical_data.py --year 2025 --keep-partial

Output:
    simulation/sim_data/{YEAR}/
    ├── season_schedule.csv
    ├── game_data.csv
    ├── team_data/{32 team CSVs}
    └── weeks/week_01...week_17/
        ├── players.csv
        └── players_projected.csv

Author: Kai Mizuno
"""

import argparse
import asyncio
import shutil
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))

from utils.LoggingManager import setup_logger, get_logger
from historical_data_compiler.constants import (
    MIN_SUPPORTED_YEAR,
    REGULAR_SEASON_WEEKS,
    VALIDATION_WEEKS,
    TEAM_DATA_FOLDER,
    WEEKS_FOLDER,
)
from historical_data_compiler.http_client import BaseHTTPClient
from historical_data_compiler.schedule_fetcher import fetch_and_write_schedule
from historical_data_compiler.game_data_fetcher import fetch_and_write_game_data
from historical_data_compiler.player_data_fetcher import fetch_player_data
from historical_data_compiler.team_data_calculator import calculate_and_write_team_data
from historical_data_compiler.weekly_snapshot_generator import generate_weekly_snapshots


YEARS = [2021, 2022, 2023, 2024, 2025]


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Compile historical NFL season data from ESPN APIs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python compile_historical_data.py --year 2024
    python compile_historical_data.py --all-years
    python compile_historical_data.py --year 2025 --format both
    python compile_historical_data.py --year 2025 --weeks 3
    python compile_historical_data.py --year 2025 --keep-partial

Output will be written to:
    simulation/sim_data/{YEAR}/
        """
    )

    year_group = parser.add_mutually_exclusive_group()
    year_group.add_argument(
        "--year",
        type=int,
        help=f"NFL season year to compile (>= {MIN_SUPPORTED_YEAR})"
    )
    year_group.add_argument(
        "--all-years",
        action="store_true",
        help="Compile all supported years"
    )

    parser.add_argument(
        "--format",
        choices=['csv', 'json', 'both'],
        default='json',
        help="Output format (default: json)"
    )
    parser.add_argument(
        "--keep-partial",
        action="store_true",
        help="Preserve partial output on failure instead of cleaning up"
    )
    parser.add_argument(
        "--weeks",
        type=int,
        help="Limit compilation to first N weeks"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--enable-log-file",
        action="store_true",
        help="Enable file logging to logs/historical_data_compiler/"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Override output directory (default: simulation/sim_data/{YEAR})"
    )

    args = parser.parse_args()
    if args.year is None and not args.all_years:
        parser.error("Must provide --year YEAR or --all-years")
    if args.weeks is not None and args.weeks < 1:
        parser.error("--weeks must be a positive integer")
    return args


def validate_year(year: int) -> None:
    """
    Validate the year is supported.

    Args:
        year: NFL season year

    Raises:
        ValueError: If year is not supported
    """
    if year < MIN_SUPPORTED_YEAR:
        raise ValueError(
            f"Year {year} is not supported. "
            f"Weekly data is only available for {MIN_SUPPORTED_YEAR}+."
        )


def create_output_directories(output_dir: Path) -> None:
    """
    Create the output directory structure.

    Args:
        output_dir: Base output directory

    Creates:
        {output_dir}/
        ├── team_data/
        └── weeks/
            ├── week_01/
            ├── week_02/
            └── ... week_17/
    """
    logger = get_logger()

    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Created output directory: {output_dir}")

    team_data_dir = output_dir / TEAM_DATA_FOLDER
    team_data_dir.mkdir(exist_ok=True)

    weeks_dir = output_dir / WEEKS_FOLDER
    weeks_dir.mkdir(exist_ok=True)

    for week in range(1, VALIDATION_WEEKS + 1):
        week_dir = weeks_dir / f"week_{week:02d}"
        week_dir.mkdir(exist_ok=True)

    logger.info(f"Created {VALIDATION_WEEKS} week folders")


def cleanup_on_error(output_dir: Path) -> None:
    """
    Clean up partial output on error.

    Args:
        output_dir: Directory to remove
    """
    logger = get_logger()
    if output_dir.exists():
        logger.warning(f"Cleaning up partial output: {output_dir}")
        shutil.rmtree(output_dir)


async def compile_season_data(
    year: int,
    output_dir: Path,
    generate_csv: bool,
    generate_json: bool,
    max_weeks: Optional[int] = None,
) -> None:
    """
    Main compilation workflow.

    Fetches all data from ESPN APIs and generates simulation data files.
    Uses fail-completely approach - any error aborts the entire compilation.

    Args:
        year: NFL season year
        output_dir: Output directory path
        generate_csv: Whether to generate CSV snapshot files
        generate_json: Whether to generate JSON snapshot files
        max_weeks: Limit compilation to first N weeks; None compiles all weeks

    Raises:
        Exception: Any error during compilation
    """
    logger = get_logger()
    logger.info(f"Starting compilation for {year} season")

    http_client = BaseHTTPClient()

    try:
        logger.info("[1/5] Fetching schedule data...")
        schedule, bye_weeks = await fetch_and_write_schedule(year, output_dir, http_client, max_weeks=max_weeks)
        logger.info(f"  - Schedule fetched for {len(schedule)} weeks")
        logger.info(f"  - Derived bye weeks for {len(bye_weeks)} teams")

        logger.info("[2/5] Fetching game data...")
        game_data = await fetch_and_write_game_data(year, output_dir, http_client, max_weeks=max_weeks)
        logger.info(f"  - Game data fetched for {len(game_data)} games")

        logger.info("[3/5] Fetching player data...")
        players = await fetch_player_data(year, http_client, bye_weeks)
        logger.info(f"  - Player data fetched for {len(players)} players")

        logger.info("[4/5] Calculating team data...")
        team_data = calculate_and_write_team_data(players, schedule, game_data, output_dir)
        logger.info(f"  - Team data calculated for {len(team_data)} teams")

        logger.info("[5/5] Generating weekly snapshots...")
        snapshot_week_limit = min(max_weeks, VALIDATION_WEEKS) if max_weeks is not None else VALIDATION_WEEKS
        generate_weekly_snapshots(players, output_dir, generate_csv, generate_json, max_weeks=max_weeks)
        logger.info(f"  - Generated {snapshot_week_limit} weekly snapshots")

        logger.info(f"Compilation complete for {year} season")
        logger.info(f"Output written to: {output_dir}")

    finally:
        await http_client.close()


def main() -> int:
    """
    Main entry point.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    args = parse_args()

    log_level = "DEBUG" if args.verbose else "INFO"
    setup_logger(
        name="historical_data_compiler",
        level=log_level,
        log_to_file=args.enable_log_file,
        log_file_path=None
    )
    logger = get_logger()

    generate_csv = args.format in ('csv', 'both')
    generate_json = args.format in ('json', 'both')
    logger.info(f"Output format: {args.format}")

    if args.year is not None:
        year_array = [int(args.year)]
    else:
        year_array = YEARS

    for current_year in year_array:
        output_dir = None
        try:
            validate_year(current_year)

            if args.output_dir:
                output_dir = args.output_dir
            else:
                output_dir = Path(__file__).parent / "simulation" / "sim_data" / str(current_year)

            if output_dir.exists():
                logger.warning(f"Output directory already exists: {output_dir}")
                logger.warning("Existing data will be overwritten")
                shutil.rmtree(output_dir)

            create_output_directories(output_dir)

            asyncio.run(compile_season_data(current_year, output_dir, generate_csv, generate_json, max_weeks=args.weeks))

            logger.info("Historical data compilation completed successfully!")

        except ValueError as e:
            logger.error(f"Validation error: {e}")
            return 1
        except KeyboardInterrupt:
            logger.warning("Compilation interrupted by user")
            if output_dir and output_dir.exists():
                if args.keep_partial:
                    logger.warning(f"Partial output preserved at: {output_dir}")
                else:
                    cleanup_on_error(output_dir)
            return 1
        except Exception as e:
            logger.error(f"Compilation failed: {e}", exc_info=True)
            if output_dir and output_dir.exists():
                if args.keep_partial:
                    logger.warning(f"Partial output preserved at: {output_dir}")
                else:
                    cleanup_on_error(output_dir)
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())


