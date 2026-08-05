"""
Sim Data Projection Coverage

Cross-simulation primitive: measure how much of a compiled
simulation/sim_data/{YEAR}/ season tree actually carries weekly projections.

Structural validation (files present, week folders present, one JSON parses)
cannot see a season-week whose files are all present but whose projections are
zeroed at the source, which is exactly the 2023 week-1 condition delivery ticket
D8 exists to expose. This module is the single owner of that measurement (D8
TD4): validate_sim_data.py consumes it today, and the accuracy harness consumes
the same per-week figures later, so the two can never disagree about which
season-weeks are under-covered.

Coverage is computed over a scale-free, production-ranked population — the top
COVERAGE_POPULATION_SIZE players by season actual production, the identical rule
for every season (D8 TD2; an ADP-ranked population is forbidden, it would couple
this detector to the separate 2025 ADP scale defect). A player's own bye week is
removed from that player's denominator (D8 TD3), so every figure this module
produces is bye-EXCLUDED and every log line says so — the bye-included and
bye-excluded bands differ by ~5.9 points, so an unqualified figure is not merely
imprecise.

Numerator/denominator pairs are returned raw rather than pre-rounded so a later
threshold comparison can be exact.

Author: Kai Mizuno
"""

# Standard library
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Local
from historical_data_compiler.constants import (
    POSITION_JSON_FILES,
    REGULAR_SEASON_WEEKS,
    VALIDATION_WEEKS,
    WEEKS_FOLDER,
)
from utils.LoggingManager import get_logger


COVERAGE_POPULATION_SIZE = 200

BYE_CONVENTION = "byes excluded"


@dataclass
class SeasonCoverage:
    """Projection coverage for one compiled season.

    Attributes:
        per_week: Week number (1..REGULAR_SEASON_WEEKS) -> (covered, eligible)
            raw counts, byes excluded from `eligible`.
        season: (covered, eligible) summed over every week, byes excluded.
        population_size: Actual number of players measured. Normally
            COVERAGE_POPULATION_SIZE; smaller when the season compiled fewer
            players, reported so a small-corpus figure is never mistaken for a
            full-population one.
    """

    per_week: Dict[int, Tuple[int, int]]
    season: Tuple[int, int]
    population_size: int


def _season_snapshot_dir(season_dir: Path) -> Path:
    """Resolve the season-final week folder used as the coverage snapshot.

    Args:
        season_dir: Path to the sim_data/{year}/ directory.

    Returns:
        Path to weeks/week_{VALIDATION_WEEKS:02d}/ — the only folder carrying
        complete season actuals, and therefore the only folder a
        production-ranked population is computable from.
    """
    return season_dir / WEEKS_FOLDER / f"week_{VALIDATION_WEEKS:02d}"


def _load_snapshot_records(snapshot_dir: Path) -> List[dict]:
    """Load every position record from one week folder.

    Args:
        snapshot_dir: Path to a weeks/week_NN/ folder.

    Returns:
        The concatenated player records across all POSITION_JSON_FILES.

    Raises:
        OSError: If a position JSON file is missing or unreadable.
        ValueError: If a position JSON file does not parse or does not decode
            as UTF-8. json.JSONDecodeError (itself a ValueError) is preserved
            for a parse failure; any other decode ValueError — notably
            UnicodeDecodeError — is re-raised as a plain ValueError. The
            offending path is prefixed onto the message in both cases.
        KeyError: If a position JSON file is not a dict carrying its own
            "<stem>" key. The offending path is named in the message.
        TypeError: If a position JSON file's "<stem>" value is not a list.
    """
    records: List[dict] = []

    for json_filename in POSITION_JSON_FILES.values():
        json_path = snapshot_dir / json_filename
        try:
            with json_path.open('r') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"{json_path}: {e.msg}", e.doc, e.pos) from e
        except ValueError as e:
            # Strictly wider than the arm above: a file that is not valid UTF-8
            # raises UnicodeDecodeError, a sibling ValueError subclass that
            # json.JSONDecodeError does not cover.
            raise ValueError(f"{json_path}: {e}") from e

        expected_key = json_path.stem
        if not isinstance(data, dict) or expected_key not in data:
            raise KeyError(
                f"{json_path}: expected dict with key '{expected_key}'"
            )
        if not isinstance(data[expected_key], list):
            raise TypeError(
                f"{json_path}: expected list at ['{expected_key}']"
            )

        records.extend(data[expected_key])

    return records


def _bye_week_of(record: dict) -> Optional[int]:
    """Return the record's own bye week, or None when it excludes no week.

    A missing, null, or out-of-range bye_week excludes no week for that player
    (its denominator is REGULAR_SEASON_WEEKS rather than one less) instead of
    dropping the player, so a malformed record degrades a single denominator
    rather than the population.

    Args:
        record: One compiled player record.

    Returns:
        The bye week when it is an int in 1..REGULAR_SEASON_WEEKS, else None.
    """
    bye_week = record.get('bye_week')
    if isinstance(bye_week, int) and 1 <= bye_week <= REGULAR_SEASON_WEEKS:
        return bye_week
    return None


def select_coverage_population(season_dir: Path) -> List[dict]:
    """Select the scale-free, production-ranked coverage population.

    The top COVERAGE_POPULATION_SIZE players by summed season actual points,
    read from the season-final week folder — the identical rule for every season
    (D8 TD2). average_draft_position is deliberately never consulted.

    Args:
        season_dir: Path to the sim_data/{year}/ directory.

    Returns:
        The selected player records, highest season actual production first.
        Shorter than COVERAGE_POPULATION_SIZE when the season compiled fewer
        players.

    Raises:
        OSError: If the season-final snapshot is missing or unreadable.
        json.JSONDecodeError: If a snapshot JSON file does not parse.
        KeyError: If a snapshot file or a record lacks a required key.
        TypeError: If a snapshot file or a record has an unexpected shape.
    """
    records = _load_snapshot_records(_season_snapshot_dir(season_dir))
    records.sort(key=lambda record: sum(record['actual_points']), reverse=True)
    return records[:COVERAGE_POPULATION_SIZE]


def compute_season_coverage(season_dir: Path) -> SeasonCoverage:
    """Compute per-week and per-season projection coverage for one season.

    A player-week counts toward the denominator unless it is that player's own
    bye week (D8 TD3), and toward the numerator when the player's
    projected_points entry for that week is greater than zero.

    Args:
        season_dir: Path to the sim_data/{year}/ directory.

    Returns:
        The season's raw coverage counts, byes excluded.

    Raises:
        OSError: If the season-final snapshot is missing or unreadable.
        json.JSONDecodeError: If a snapshot JSON file does not parse.
        KeyError: If a snapshot file or a record lacks a required key.
        IndexError: If a record's projected_points array is shorter than
            REGULAR_SEASON_WEEKS.
        TypeError: If a snapshot file or a record has an unexpected shape.
    """
    population = select_coverage_population(season_dir)

    per_week: Dict[int, Tuple[int, int]] = {}
    for week in range(1, REGULAR_SEASON_WEEKS + 1):
        covered = 0
        eligible = 0
        for record in population:
            if _bye_week_of(record) == week:
                continue
            eligible += 1
            if record['projected_points'][week - 1] > 0:
                covered += 1
        per_week[week] = (covered, eligible)

    season = (
        sum(covered for covered, _ in per_week.values()),
        sum(eligible for _, eligible in per_week.values()),
    )

    return SeasonCoverage(
        per_week=per_week,
        season=season,
        population_size=len(population),
    )


def _format_coverage(label: str, covered: int, eligible: int) -> str:
    """Format one coverage figure, always stating its bye convention.

    Args:
        label: Row label (e.g. "week 01" or "season").
        covered: Player-weeks carrying a positive projection.
        eligible: Player-weeks in the denominator.

    Returns:
        The formatted log line body.
    """
    percentage = (100.0 * covered / eligible) if eligible else 0.0
    return (
        f"  {label}: {covered}/{eligible} ({percentage:.1f}%) projected "
        f"[{BYE_CONVENTION}]"
    )


def check_coverage(output_dir: Path) -> bool:
    """Report projection coverage for a compiled season. Never fails.

    Conforms to the (output_dir: Path) -> bool check-function shape the other
    validate_sim_data.py checks use, but returns True unconditionally: this is
    the reporting-only stage of D8's staged rollout, so the validator's exit
    code and pass/fail verdict are identical with and without this call. The
    enforcing comparison and its threshold constants are added to this same
    module by a later unit.

    Missing, unreadable, or malformed coverage inputs are logged at WARNING and
    the check still returns True, so no input state can change the caller's exit
    code.

    Args:
        output_dir: Path to the sim_data/{year}/ output directory.

    Returns:
        True, always.
    """
    logger = get_logger()
    snapshot_dir = _season_snapshot_dir(output_dir)

    try:
        coverage = compute_season_coverage(output_dir)
    except (IOError, OSError) as e:
        logger.warning(
            f"check_coverage: coverage not computed for {snapshot_dir}: {e}"
        )
        return True
    except ValueError as e:
        # ValueError, not json.JSONDecodeError: the latter is one ValueError
        # subclass among several json.load can raise. UnicodeDecodeError is the
        # reachable sibling — a position file that is not valid UTF-8 — and it
        # must not escape, or the caller's exit code changes.
        logger.warning(
            f"check_coverage: coverage not computed, unreadable or invalid JSON "
            f"under {snapshot_dir}: {e}"
        )
        return True
    except (KeyError, IndexError, TypeError) as e:
        # KeyError.__str__ repr()s its single argument, so unwrap it to format
        # the same way as the IndexError/TypeError arms it shares this handler with.
        detail = e.args[0] if isinstance(e, KeyError) and e.args else e
        logger.warning(
            f"check_coverage: coverage not computed, malformed record or file "
            f"under {snapshot_dir}: {detail}"
        )
        return True

    logger.info(
        f"Projection coverage (population: top {coverage.population_size} by "
        f"season actual production; snapshot: {snapshot_dir.name}; "
        f"{BYE_CONVENTION} from every denominator):"
    )
    for week in range(1, REGULAR_SEASON_WEEKS + 1):
        covered, eligible = coverage.per_week[week]
        logger.info(_format_coverage(f"week {week:02d}", covered, eligible))
    logger.info(_format_coverage("season", *coverage.season))

    return True
