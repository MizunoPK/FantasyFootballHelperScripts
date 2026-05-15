#!/usr/bin/env python3
"""
Validate Sim Data

Validates a compiled sim_data/{YEAR}/ output tree before simulation engines attempt to use it.

Usage:
    python validate_sim_data.py --year 2025
    python validate_sim_data.py --year 2025 --output-dir /path/to/output
    python validate_sim_data.py --year 2025 --verbose
    python validate_sim_data.py --year 2025 --enable-log-file

Exit codes:
    0: All checks passed
    1: One or more checks failed
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from utils.LoggingManager import setup_logger, get_logger
from historical_data_compiler.constants import (
    SEASON_SCHEDULE_FILE,
    GAME_DATA_FILE,
    TEAM_DATA_FOLDER,
    WEEKS_FOLDER,
    VALIDATION_WEEKS,
    EXPECTED_NFL_TEAMS,
    POSITION_JSON_FILES,
)


def check_csv_files(output_dir: Path) -> bool:
    """
    Check that root CSV files and team_data CSVs exist and are non-empty.

    Args:
        output_dir: Path to the sim_data/{year}/ output directory.

    Returns:
        True if all CSV checks pass, False if any fail.
    """
    logger = get_logger()
    passed = True

    for csv_file in [SEASON_SCHEDULE_FILE, GAME_DATA_FILE]:
        csv_path = output_dir / csv_file
        if not csv_path.exists():
            logger.error(f"Missing required CSV: {csv_path}")
            passed = False
        elif csv_path.stat().st_size == 0:
            logger.error(f"Empty CSV file: {csv_path}")
            passed = False

    team_data_dir = output_dir / TEAM_DATA_FOLDER
    if not team_data_dir.exists():
        logger.error(f"Missing team_data directory: {team_data_dir}")
        passed = False
    else:
        csv_count = len(list(team_data_dir.glob("*.csv")))
        if csv_count != EXPECTED_NFL_TEAMS:
            logger.error(
                f"Expected {EXPECTED_NFL_TEAMS} team CSV files in {team_data_dir}, found {csv_count}"
            )
            passed = False

    return passed


def _iter_week_folders(output_dir: Path):
    weeks_dir = output_dir / WEEKS_FOLDER
    for week_num in range(1, VALIDATION_WEEKS + 1):
        yield weeks_dir / f"week_{week_num:02d}"


def check_week_folders(output_dir: Path) -> bool:
    """
    Check that all 18 week folders exist and contain the 6 position JSON files.

    Args:
        output_dir: Path to the sim_data/{year}/ output directory.

    Returns:
        True if all week folder and JSON file checks pass, False if any fail.
    """
    logger = get_logger()
    passed = True

    for week_folder in _iter_week_folders(output_dir):
        if not week_folder.exists():
            logger.error(f"Missing week folder: {week_folder}")
            passed = False
            continue

        for json_filename in POSITION_JSON_FILES.values():
            json_path = week_folder / json_filename
            if not json_path.exists():
                logger.error(f"Missing JSON file: {json_path}")
                passed = False

    return passed


def check_json_spot(week_dir: Path) -> bool:
    """
    Spot-check qb_data.json in a week folder for valid dict-wrapper format.

    Skips the check (returns True) if qb_data.json does not exist — that absence
    is already reported by check_week_folders.

    Args:
        week_dir: Path to the week folder (e.g., weeks/week_01/).

    Returns:
        True if qb_data.json is structurally valid OR is absent (the absence is already
        flagged by check_week_folders). False if the file exists but has invalid structure
        (unreadable, invalid JSON, missing 'qb_data' key, value not a non-empty list).
    """
    logger = get_logger()
    qb_json_path = week_dir / POSITION_JSON_FILES['QB']

    if not qb_json_path.exists():
        return True

    try:
        with qb_json_path.open('r') as f:
            data = json.load(f)
    except (IOError, OSError) as e:
        logger.error(f"Failed to read {qb_json_path}: {e}")
        return False
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {qb_json_path}: {e}")
        return False

    expected_key = qb_json_path.stem
    if not isinstance(data, dict) or expected_key not in data:
        logger.error(
            f"Unexpected structure in {qb_json_path}: expected dict with key '{expected_key}'"
        )
        return False

    if not isinstance(data[expected_key], list) or len(data[expected_key]) == 0:
        logger.error(
            f"Expected non-empty list at {qb_json_path}['{expected_key}']"
        )
        return False

    return True


def check_all_json_spots(output_dir: Path) -> bool:
    """
    Run JSON spot-check on qb_data.json for all existing week folders.

    Args:
        output_dir: Path to the sim_data/{year}/ output directory.

    Returns:
        True if all spot-checks pass, False if any fail.
    """
    passed = True

    for week_folder in _iter_week_folders(output_dir):
        if week_folder.exists():
            if not check_json_spot(week_folder):
                passed = False

    return passed


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="Validate a compiled sim_data/{YEAR}/ output tree",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python validate_sim_data.py --year 2025
    python validate_sim_data.py --year 2025 --output-dir /path/to/output
    python validate_sim_data.py --year 2025 --verbose
    python validate_sim_data.py --year 2025 --enable-log-file
        """
    )
    parser.add_argument(
        "--year",
        type=int,
        required=True,
        help="NFL season year to validate"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Override directory to validate (default: simulation/sim_data/{YEAR})"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--enable-log-file",
        action="store_true",
        help="Enable file logging to logs/validate_sim_data/"
    )
    return parser.parse_args()


def main() -> int:
    """
    Main entry point for validate_sim_data.

    Returns:
        Exit code: 0 if all checks pass, 1 if any fail.
    """
    args = parse_args()

    log_level = "DEBUG" if args.verbose else "INFO"
    setup_logger(
        name="validate_sim_data",
        level=log_level,
        log_to_file=args.enable_log_file,
        log_file_path=None,
    )
    logger = get_logger()

    if args.output_dir is not None:
        output_dir = args.output_dir
        if not output_dir.exists():
            logger.error(f"Output directory does not exist: {output_dir}")
            return 1
        if not output_dir.is_dir():
            logger.error(f"Output directory is not a directory: {output_dir}")
            return 1
    else:
        output_dir = Path(__file__).parent / "simulation" / "sim_data" / str(args.year)

    logger.info(f"Validating sim data for year {args.year} at {output_dir}")

    csv_passed = check_csv_files(output_dir)
    weeks_passed = check_week_folders(output_dir)
    spot_passed = check_all_json_spots(output_dir)
    all_passed = csv_passed and weeks_passed and spot_passed

    if all_passed:
        logger.info("All validation checks passed.")
    else:
        logger.error("Validation failed. See errors above.")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
