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

from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.utils.LoggingManager import setup_logger, get_logger
from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.player_data_fetcher.config import POSITION_CODES, data_root
from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.player_data_fetcher.player_data_exporter import zero_bye_week_points

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

    # A non-integer bye_week reaches arithmetic in zero_bye_week_points and raises,
    # which would break the module's documented 0/1 exit-code contract. None stays
    # permitted -- it is TD1's documented skip arm.
    bye_week = record['bye_week']
    if bye_week is not None and not isinstance(bye_week, int):
        logger.error(
            f"validate_record: {position}_data.json record {index} has non-integer "
            f"'bye_week' {bye_week!r}"
        )
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


def load_and_repair_file(path: Path, position: str) -> Optional[tuple[Any, int]]:
    """Read one position file and repair it IN MEMORY, writing nothing.

    Reading and repairing are separated from writing so the pool-level operation
    can validate every file before it mutates any of them (see repair_pool).

    Args:
        path: Path to the position JSON file.
        position: Lowercase position code.

    Returns:
        A (repaired document, records changed) pair, or None if the file is
        missing or malformed.
    """
    logger = get_logger()

    if not path.exists():
        logger.error(f"load_and_repair_file: missing player data file {path}")
        return None

    try:
        document = json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        logger.error(f"load_and_repair_file: malformed JSON in {path}: {e}")
        return None

    changed = repair_document(document, position)
    if changed is None:
        return None

    return document, changed


def write_repaired_file(path: Path, document: Any) -> bool:
    """Atomically rewrite one position file from an already-repaired document.

    The rewrite is a temporary file plus an os-level replace, so the live file
    is never observed half-written. Serialization matches the exporter that
    wrote these bytes (indent=2, ensure_ascii=False, no trailing newline),
    which is what keeps the diff value-only.

    Args:
        path: Path to the position JSON file.
        document: The repaired document to serialize.

    Returns:
        True on success, False if the write failed (the temporary file is
        removed before returning, so no stray .tmp is left behind).
    """
    logger = get_logger()

    # Deliberately NOT simulation.shared.atomic_io.atomic_write_json: it forces
    # ensure_ascii=True, which would escape non-ASCII player names and break
    # byte-fidelity with the exporter's writer (player_data_exporter.py).
    payload = json.dumps(document, indent=2, ensure_ascii=False)
    tmp_path = path.with_suffix('.tmp')
    try:
        tmp_path.write_text(payload, encoding='utf-8')
        tmp_path.replace(path)
    except (OSError, PermissionError) as e:
        # An orphaned .tmp under data/ turns every later suite run red through
        # tests/run_all_tests.py's data-cleanliness backstop, so clean it up.
        tmp_path.unlink(missing_ok=True)
        logger.error(f"write_repaired_file: could not write {path}: {e}")
        return False

    return True


def repair_pool(player_data_dir: Path, dry_run: bool) -> Optional[int]:
    """Repair every position file in one player_data directory.

    Two-phase, so the pool-level operation is atomic with respect to malformed
    input: every file is read and repaired in memory and only then, once all
    six have passed, is anything written. A missing or malformed file therefore
    aborts with the pool untouched rather than leaving earlier positions
    already rewritten.

    Args:
        player_data_dir: Directory holding the six position JSON files.
        dry_run: When True, report counts and write nothing.

    Returns:
        The total number of records changed, or None if any file aborted the run.
    """
    logger = get_logger()

    # Phase 1 -- read and repair every file in memory. Nothing is written yet.
    repaired: list[tuple[Path, Any, int]] = []
    total = 0
    for position in POSITION_CODES:
        path = player_data_dir / f"{position}_data.json"
        result = load_and_repair_file(path, position)
        if result is None:
            logger.error(
                f"repair_pool: aborting -- {position}_data.json could not be repaired. "
                f"No file was written."
            )
            return None
        document, changed = result
        repaired.append((path, document, changed))
        total += changed

    if dry_run:
        for path, _document, changed in repaired:
            logger.info(f"repair_pool: [dry-run] {path.name} would change {changed} records")
        return total

    # Phase 2 -- every file validated, so commit the writes.
    for path, document, changed in repaired:
        if not write_repaired_file(path, document):
            logger.error(f"repair_pool: aborting -- {path.name} could not be written")
            return None
        logger.info(f"repair_pool: {path.name} changed {changed} records")

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
