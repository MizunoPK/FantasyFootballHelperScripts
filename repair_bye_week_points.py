#!/usr/bin/env python3
"""
Repair Bye Week Points

One-time, offline repair of the tracked player pool under data/player_data/:
each record's projected and actual weekly arrays are zeroed at that record's
own bye week through the single owner of the invariant,
player_data_fetcher.player_data_exporter.zero_bye_week_points.

No network call and no re-fetch -- the correction is a pure function of data
already on disk (Spec: D3 context.md TD2). Idempotent and re-runnable: a second
run reports 0 records changed.

Usage:
    python repair_bye_week_points.py
    python repair_bye_week_points.py --dry-run
    python repair_bye_week_points.py --data-root /path/to/data
    python repair_bye_week_points.py --verbose

Exit codes:
    0: All position files processed successfully
    1: A missing or malformed file, or a malformed record, aborted the run

Author: Kai Mizuno
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Optional

sys.path.insert(0, str(Path(__file__).parent))

from utils.LoggingManager import setup_logger, get_logger
from player_data_fetcher.config import data_root
from player_data_fetcher.player_data_exporter import zero_bye_week_points
from player_data_fetcher.player_data_fetcher_main import POSITION_CODES

WEEKS_PER_SEASON = 17
POINT_ARRAY_KEYS = ('projected_points', 'actual_points')


def validate_record(record: Any, position: str, index: int) -> bool:
    """Check that one record carries the keys and array shape the repair assumes.

    A violation is an error rather than a skipped record: it breaks an
    assumption the repair depends on, so it must not be swallowed.

    Args:
        record: The candidate record read from the position file.
        position: Lowercase position code, used in the error message.
        index: Zero-based position of the record within its file.

    Returns:
        True if the record is repairable, False if it is malformed.
    """
    logger = get_logger()

    if not isinstance(record, dict):
        logger.error(f"validate_record: {position}_data.json record {index} is not an object")
        return False

    if 'bye_week' not in record:
        logger.error(f"validate_record: {position}_data.json record {index} has no 'bye_week' key")
        return False

    for key in POINT_ARRAY_KEYS:
        array = record.get(key)
        if not isinstance(array, list):
            logger.error(f"validate_record: {position}_data.json record {index} has no list '{key}'")
            return False
        if len(array) != WEEKS_PER_SEASON:
            logger.error(
                f"validate_record: {position}_data.json record {index} has {len(array)} "
                f"'{key}' slots, expected {WEEKS_PER_SEASON}"
            )
            return False

    return True


def repair_document(document: Any, position: str) -> Optional[int]:
    """Zero the bye slot of every record in one already-parsed position document.

    Args:
        document: The parsed JSON document for one position file.
        position: Lowercase position code, which also names the root key.

    Returns:
        The number of records whose arrays changed, or None if the document or
        any record is malformed.
    """
    logger = get_logger()
    root_key = f"{position}_data"

    records = document.get(root_key) if isinstance(document, dict) else None
    if not isinstance(records, list):
        logger.error(
            f"repair_document: {position}_data.json has no list under the root key '{root_key}'"
        )
        return None

    changed = 0
    for index, record in enumerate(records):
        if not validate_record(record, position, index):
            return None

        projected_points = record['projected_points']
        actual_points = record['actual_points']
        before = (list(projected_points), list(actual_points))

        zero_bye_week_points(projected_points, actual_points, record['bye_week'])

        if (projected_points, actual_points) != before:
            changed += 1

    return changed


def repair_file(path: Path, position: str, dry_run: bool) -> Optional[int]:
    """Read, repair and atomically rewrite one position file.

    The rewrite is a temporary file plus an os-level replace, so the live file
    is never observed half-written. Serialization matches the exporter that
    wrote these bytes (indent=2, ensure_ascii=False, no trailing newline),
    which is what keeps the diff value-only.

    Args:
        path: Path to the position JSON file.
        position: Lowercase position code.
        dry_run: When True, report the count and write nothing.

    Returns:
        The number of records changed, or None if the file could not be repaired.
    """
    logger = get_logger()

    if not path.exists():
        logger.error(f"repair_file: missing player data file {path}")
        return None

    try:
        document = json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        logger.error(f"repair_file: malformed JSON in {path}: {e}")
        return None

    changed = repair_document(document, position)
    if changed is None:
        return None

    if dry_run:
        logger.info(f"repair_file: [dry-run] {path.name} would change {changed} records")
        return changed

    payload = json.dumps(document, indent=2, ensure_ascii=False)
    tmp_path = path.with_suffix('.tmp')
    tmp_path.write_text(payload, encoding='utf-8')
    tmp_path.replace(path)

    logger.info(f"repair_file: {path.name} changed {changed} records")
    return changed


def repair_pool(player_data_dir: Path, dry_run: bool) -> Optional[int]:
    """Repair every position file in one player_data directory.

    Args:
        player_data_dir: Directory holding the six position JSON files.
        dry_run: When True, report counts and write nothing.

    Returns:
        The total number of records changed, or None if any file aborted the run.
    """
    logger = get_logger()
    total = 0

    for position in POSITION_CODES:
        changed = repair_file(player_data_dir / f"{position}_data.json", position, dry_run)
        if changed is None:
            logger.error(f"repair_pool: aborting -- {position}_data.json could not be repaired")
            return None
        total += changed

    return total


def parse_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="Zero the bye-week slot of every record in data/player_data/",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python repair_bye_week_points.py
    python repair_bye_week_points.py --dry-run
    python repair_bye_week_points.py --data-root /path/to/data
    python repair_bye_week_points.py --verbose
        """
    )
    parser.add_argument(
        "--data-root",
        type=Path,
        default=None,
        help="Override the data ROOT containing player_data/ (default: the fetcher's data root)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report the records that would change and write nothing"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    return parser.parse_args()


def main() -> int:
    """Main entry point for repair_bye_week_points.

    Returns:
        Exit code: 0 if every file was processed, 1 on any failure.
    """
    args = parse_args()

    setup_logger(
        name="repair_bye_week_points",
        level="DEBUG" if args.verbose else "INFO",
        log_to_file=False,
        log_file_path=None,
    )
    logger = get_logger()

    root = args.data_root if args.data_root is not None else data_root()
    player_data_dir = Path(root) / 'player_data'
    if not player_data_dir.is_dir():
        logger.error(f"main: player data directory does not exist: {player_data_dir}")
        return 1

    mode = "dry run" if args.dry_run else "repair"
    logger.info(f"main: starting bye-week {mode} over {player_data_dir}")

    total = repair_pool(player_data_dir, args.dry_run)
    if total is None:
        logger.error("main: bye-week repair failed. See errors above.")
        return 1

    verb = "would change" if args.dry_run else "changed"
    logger.info(
        f"main: bye-week {mode} complete -- {verb} {total} records "
        f"across {len(POSITION_CODES)} files"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
