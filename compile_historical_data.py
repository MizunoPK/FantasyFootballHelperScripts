#!/usr/bin/env python3
"""
Historical Data Compiler

A standalone script to compile historical NFL season data from ESPN APIs.
Creates point-in-time snapshots for simulation system testing.

Usage:
    python compile_historical_data.py --year 2024

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

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from utils.LoggingManager import setup_logger, get_logger
from historical_data_compiler.constants import (
    MIN_SUPPORTED_YEAR,
    REGULAR_SEASON_WEEKS,
    TEAM_DATA_FOLDER,
    WEEKS_FOLDER,
)
from historical_data_compiler.http_client import BaseHTTPClient
from historical_data_compiler.schedule_fetcher import fetch_and_write_schedule
from historical_data_compiler.game_data_fetcher import fetch_and_write_game_data
from historical_data_compiler.player_data_fetcher import fetch_player_data
from historical_data_compiler.team_data_calculator import calculate_and_write_team_data
from historical_data_compiler.weekly_snapshot_generator import generate_weekly_snapshots


# =============================================================================
# OUTPUT FORMAT TOGGLES
# =============================================================================

# Control which output formats are generated
GENERATE_CSV = True   # Generate legacy CSV files (players.csv, players_projected.csv)
GENERATE_JSON = True  # Generate new JSON files (qb_data.json, rb_data.json, etc.)


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
    python compile_historical_data.py --year 2023 --verbose

Output will be written to:
    simulation/sim_data/{YEAR}/
        """
    )
    parser.add_argument(
        "--year",
        type=int,
        required=True,
        help=f"NFL season year to compile (>= {MIN_SUPPORTED_YEAR})"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Override output directory (default: simulation/sim_data/{YEAR})"
    )

    return parser.parse_args()


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

    # Create base directory
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Created output directory: {output_dir}")

    # Create team_data subdirectory
    team_data_dir = output_dir / TEAM_DATA_FOLDER
    team_data_dir.mkdir(exist_ok=True)

    # Create weeks subdirectories
    weeks_dir = output_dir / WEEKS_FOLDER
    weeks_dir.mkdir(exist_ok=True)

    for week in range(1, REGULAR_SEASON_WEEKS + 1):
        week_dir = weeks_dir / f"week_{week:02d}"
        week_dir.mkdir(exist_ok=True)

    logger.info(f"Created {REGULAR_SEASON_WEEKS} week folders")


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


async def compile_season_data(year: int, output_dir: Path) -> None:
    """
    Main compilation workflow.

    Fetches all data from ESPN APIs and generates simulation data files.
    Uses fail-completely approach - any error aborts the entire compilation.

    Args:
        year: NFL season year
        output_dir: Output directory path

    Raises:
        Exception: Any error during compilation
    """
    logger = get_logger()
    logger.info(f"Starting compilation for {year} season")

    # Create shared HTTP client
    http_client = BaseHTTPClient()

    try:
        # Phase 1: Fetch schedule data
        logger.info("[1/5] Fetching schedule data...")
        schedule = await fetch_and_write_schedule(year, output_dir, http_client)
        logger.info(f"  - Schedule fetched for {len(schedule)} weeks")

        # Derive bye weeks from schedule
        bye_weeks = _derive_bye_weeks(schedule)
        logger.info(f"  - Derived bye weeks for {len(bye_weeks)} teams")

        # Phase 2: Fetch game data with weather
        logger.info("[2/5] Fetching game data...")
        game_data = await fetch_and_write_game_data(year, output_dir, http_client)
        logger.info(f"  - Game data fetched for {len(game_data)} games")

        # Phase 3: Fetch player data
        logger.info("[3/5] Fetching player data...")
        players = await fetch_player_data(year, http_client, bye_weeks)
        logger.info(f"  - Player data fetched for {len(players)} players")

        # Phase 4: Calculate team data
        logger.info("[4/5] Calculating team data...")
        team_data = calculate_and_write_team_data(players, schedule, game_data, output_dir)
        logger.info(f"  - Team data calculated for {len(team_data)} teams")

        # Phase 5: Generate weekly snapshots
        logger.info("[5/5] Generating weekly snapshots...")
        generate_weekly_snapshots(players, output_dir, GENERATE_CSV, GENERATE_JSON)
        logger.info(f"  - Generated {REGULAR_SEASON_WEEKS} weekly snapshots")

        logger.info(f"Compilation complete for {year} season")
        logger.info(f"Output written to: {output_dir}")

    finally:
        # Always close HTTP client
        await http_client.close()


def _derive_bye_weeks(schedule: dict) -> dict:
    """
    Derive bye week for each team from schedule.

    A team's bye week is the week where they have no opponent scheduled.

    Args:
        schedule: Dict[week, Dict[team, opponent]]

    Returns:
        Dict mapping team abbreviation to bye week number
    """
    from historical_data_compiler.constants import ALL_NFL_TEAMS

    bye_weeks = {}

    for team in ALL_NFL_TEAMS:
        for week in range(1, REGULAR_SEASON_WEEKS + 1):
            week_schedule = schedule.get(week, {})
            if team not in week_schedule:
                bye_weeks[team] = week
                break

    return bye_weeks


def main() -> int:
    """
    Main entry point.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    args = parse_args()

    # Set up logging
    log_level = "DEBUG" if args.verbose else "INFO"
    setup_logger(name="historical_data_compiler", level=log_level)
    logger = get_logger()

    try:
        # Validate year
        validate_year(args.year)

        # Determine output directory
        if args.output_dir:
            output_dir = args.output_dir
        else:
            output_dir = Path(__file__).parent / "simulation" / "sim_data" / str(args.year)

        # Check if output already exists
        if output_dir.exists():
            logger.warning(f"Output directory already exists: {output_dir}")
            logger.warning("Existing data will be overwritten")
            shutil.rmtree(output_dir)

        # Create directory structure
        create_output_directories(output_dir)

        # Run compilation
        asyncio.run(compile_season_data(args.year, output_dir))

        logger.info("Historical data compilation completed successfully!")
        return 0

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return 1
    except KeyboardInterrupt:
        logger.warning("Compilation interrupted by user")
        if 'output_dir' in locals():
            cleanup_on_error(output_dir)
        return 1
    except Exception as e:
        logger.error(f"Compilation failed: {e}", exc_info=True)
        if 'output_dir' in locals():
            cleanup_on_error(output_dir)
        return 1


if __name__ == "__main__":
    sys.exit(main())
