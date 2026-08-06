"""
Sim Data Projection Coverage

Cross-simulation primitive: measure how much of a compiled
simulation/sim_data/{YEAR}/ season tree actually carries weekly projections.

Structural validation (files present, week folders present, one JSON parses)
cannot see a season-week whose files are all present but whose projections are
zeroed at the source, which is exactly the 2023 week-1 condition delivery ticket
D8 exists to expose. This module is the single owner of that measurement (D8
TD4): validate_sim_data.py consumes it through check_coverage, and the accuracy
harness consumes the same per-week figures through excluded_weeks_by_season, so
the two cannot disagree about the set this module computes. Note the exact
scope of that guarantee: both consumers measure the weeks/week_18/ snapshot,
whereas the harness evaluates each week's own weeks/week_NN/ folder, so
"the measured set matches the corpus actually evaluated" is an EMPIRICAL
result, not a structural one. It was verified at D8 /dt7: the week_18-derived
and week_NN-derived projection counts are identical across all 85 committed
season-weeks (zero disagreements), and the ~34-point margin between the floor
and the worst healthy observation means a disagreement would have to be large
to flip any verdict.

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
from typing import Dict, FrozenSet, Iterable, List, Optional, Tuple

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

# Both floors below are BYE-EXCLUDED percentages (BYE_CONVENTION), and every log
# line that quotes one says so. Read against the bye-INCLUDED band (81.9-85.6%)
# instead, each floor looks ~5.9 points stricter than it is (D8 TD3 part 1).

# Sited inside the measured separation: across the 85 committed season-weeks the
# defect (2023 week 01) is 16.0% and the next-lowest observation (2021 week 16)
# is 81.0%, so any floor in the open interval (16.0%, 81.0%) separates the defect
# from every healthy week. 50.0% sits 34.0 points above the defect and 31.0
# points below the worst healthy week — an inequality with margin on both sides.
PER_WEEK_COVERAGE_FLOOR_PCT = 50.0

# A diffuse-degradation BACKSTOP, deliberately not this defect's detector: 2023's
# season figure is 87.1% against a healthy band of 90.7-91.0%, a 3.6-point
# corridor too narrow to site a floor inside (2021 is a healthy season at 90.9%
# whose eight lowest weeks average 86.9%, below 2023's figure). 75.0% is derived
# from a bound instead — a season every week of which sat at the worst healthy
# week ever observed (81.0%) scores exactly 81.0%, so no such season reaches
# 75.0%. 2023 passes this floor and fails on the per-week floor above.
PER_SEASON_COVERAGE_FLOOR_PCT = 75.0


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
            with json_path.open('r', encoding='utf-8') as f:
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


def weeks_below_floor(coverage: SeasonCoverage) -> List[int]:
    """Return the weeks whose coverage is below the per-week floor.

    The comparison is on raw counts (covered * 100.0 < floor * eligible) rather
    than on the rounded percentage _format_coverage prints, so the verdict and
    the logged figure can never disagree and no division is performed. Strictly
    below fails; exactly at the floor passes.

    A week whose eligible count is zero is skipped: a zero denominator is not a
    measurement, and comparing it against a floor would read a missing
    population as a total coverage failure.

    Args:
        coverage: One season's measured coverage, byes excluded.

    Returns:
        The offending week numbers in ascending week order; empty when every
        measured week is at or above PER_WEEK_COVERAGE_FLOOR_PCT.
    """
    offending: List[int] = []
    for week in sorted(coverage.per_week):
        covered, eligible = coverage.per_week[week]
        if eligible == 0:
            continue
        if covered * 100.0 < PER_WEEK_COVERAGE_FLOOR_PCT * eligible:
            offending.append(week)
    return offending


def season_below_floor(coverage: SeasonCoverage) -> bool:
    """Report whether the season aggregate is below the per-season floor.

    Same raw-count comparison and same strictly-below convention as
    weeks_below_floor. A zero season denominator returns False for the same
    reason that function skips a zero-denominator week.

    Args:
        coverage: One season's measured coverage, byes excluded.

    Returns:
        True when the season aggregate is strictly below
        PER_SEASON_COVERAGE_FLOOR_PCT, else False.
    """
    covered, eligible = coverage.season
    if eligible == 0:
        return False
    return covered * 100.0 < PER_SEASON_COVERAGE_FLOOR_PCT * eligible


def check_coverage(output_dir: Path) -> bool:
    """Report projection coverage for a compiled season, and enforce its floors.

    Conforms to the (output_dir: Path) -> bool check-function shape the other
    validate_sim_data.py checks use. The full per-week and per-season report is
    logged at INFO on every call exactly as before; the check then returns False
    when — and only when — a successfully computed measurement carrying a
    non-zero denominator falls below PER_WEEK_COVERAGE_FLOOR_PCT (per week) or
    PER_SEASON_COVERAGE_FLOOR_PCT (per season). Both floors are bye-EXCLUDED,
    and every violation is logged at ERROR naming the offending season-week, its
    figure, the floor it failed and the population size.

    Two input states deliberately never fail. Missing, unreadable, or malformed
    coverage inputs are logged at WARNING and return True — an unreadable tree is
    the structural checks' verdict to give, not this one's. A season whose
    denominator is zero is logged at WARNING and returns True for the same
    reason: a zero denominator is not a measurement, and reading it as 0.0%
    coverage would report a missing corpus as a catastrophic coverage failure.

    Args:
        output_dir: Path to the sim_data/{year}/ output directory.

    Returns:
        True when coverage is at or above both floors, or could not be measured.
        False when a measured season falls below either floor.
    """
    logger = get_logger()
    snapshot_dir = _season_snapshot_dir(output_dir)

    try:
        coverage = compute_season_coverage(output_dir)
    except OSError as e:
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

    season_covered, season_eligible = coverage.season
    if season_eligible == 0:
        logger.warning(
            f"check_coverage: coverage not measured under {snapshot_dir}: no "
            f"eligible player-weeks (population {coverage.population_size})"
        )
        return True

    offending_weeks = weeks_below_floor(coverage)
    for week in offending_weeks:
        covered, eligible = coverage.per_week[week]
        logger.error(
            f"check_coverage: week {week:02d} {covered}/{eligible} "
            f"({100.0 * covered / eligible:.1f}%) [{BYE_CONVENTION}] is below "
            f"the {PER_WEEK_COVERAGE_FLOOR_PCT:.1f}% per-week floor "
            f"[{BYE_CONVENTION}]; population {coverage.population_size}"
        )

    season_low = season_below_floor(coverage)
    if season_low:
        logger.error(
            f"check_coverage: season {season_covered}/{season_eligible} "
            f"({100.0 * season_covered / season_eligible:.1f}%) "
            f"[{BYE_CONVENTION}] is below the "
            f"{PER_SEASON_COVERAGE_FLOOR_PCT:.1f}% per-season floor "
            f"[{BYE_CONVENTION}]; population {coverage.population_size}"
        )

    return not offending_weeks and not season_low


def excluded_weeks_by_season(
    season_dirs: Iterable[Path]
) -> Dict[str, FrozenSet[int]]:
    """Decide which season-weeks the accuracy harness must not evaluate.

    The harness-facing half of this module's single ownership (D8 TD4): the
    exclusion set is weeks_below_floor(compute_season_coverage(...)) verbatim,
    so the validator and the harness cannot disagree about the computed set.
    That both measure the week_18 snapshot while the harness evaluates the
    per-week week_NN folders is verified empirically, not guaranteed
    structurally — see the module docstring (identical across all 85 committed
    season-weeks, D8 /dt7). The floor itself is never named outside this module.

    Every exclusion is announced once, here, in the parent process before any
    worker starts (D8.4 HD1/HD4) — the worker emits no per-skip line, which for
    a bounded run would fire thousands of times across eight processes and bury
    the signal. The closing count is logged even when it is zero, because "the
    flag was on and nothing qualified" is a distinct outcome silence cannot
    express. When one or more seasons failed to measure, that count is named on
    the same line: a bare "0 season-week(s) excluded" would otherwise read as a
    clean corpus when a season was in fact never measured at all.

    A season whose coverage cannot be computed is logged once at WARNING and
    excludes NOTHING (D8.4 HD5, fail-open): an unreadable tree is not evidence
    that a week is under-covered, and for a change whose direction is a corpus
    narrowing the conservative failure is to narrow less. The exception arms
    match check_coverage's.

    Args:
        season_dirs: The sim_data/{year}/ directories to measure.

    Returns:
        season directory name -> the frozenset of that season's week numbers
        below PER_WEEK_COVERAGE_FLOOR_PCT. A season with nothing to exclude is
        omitted entirely. Keyed by directory name, and valued by a frozenset of
        ints, so the mapping is picklable across the worker process boundary.
    """
    logger = get_logger()
    excluded: Dict[str, FrozenSet[int]] = {}
    excluded_count = 0
    unmeasured_count = 0

    for season_dir in season_dirs:
        snapshot_dir = _season_snapshot_dir(season_dir)

        try:
            coverage = compute_season_coverage(season_dir)
        except OSError as e:
            logger.warning(
                f"excluded_weeks_by_season: coverage not computed for "
                f"{snapshot_dir}: {e}; excluding nothing for {season_dir.name}"
            )
            unmeasured_count += 1
            continue
        except ValueError as e:
            # ValueError, not json.JSONDecodeError: the latter is one ValueError
            # subclass among several json.load can raise. UnicodeDecodeError is
            # the reachable sibling.
            logger.warning(
                f"excluded_weeks_by_season: coverage not computed, unreadable or "
                f"invalid JSON under {snapshot_dir}: {e}; excluding nothing for "
                f"{season_dir.name}"
            )
            unmeasured_count += 1
            continue
        except (KeyError, IndexError, TypeError) as e:
            # KeyError.__str__ repr()s its single argument, so unwrap it to
            # format the same way as the arms it shares this handler with.
            detail = e.args[0] if isinstance(e, KeyError) and e.args else e
            logger.warning(
                f"excluded_weeks_by_season: coverage not computed, malformed "
                f"record or file under {snapshot_dir}: {detail}; excluding "
                f"nothing for {season_dir.name}"
            )
            unmeasured_count += 1
            continue

        offending_weeks = weeks_below_floor(coverage)
        if not offending_weeks:
            continue

        for week in offending_weeks:
            covered, eligible = coverage.per_week[week]
            logger.warning(
                f"excluded_weeks_by_season: excluding {season_dir.name} week "
                f"{week:02d} from accuracy evaluation: {covered}/{eligible} "
                f"({100.0 * covered / eligible:.1f}%) [{BYE_CONVENTION}] is "
                f"below the {PER_WEEK_COVERAGE_FLOOR_PCT:.1f}% per-week floor "
                f"[{BYE_CONVENTION}]; population {coverage.population_size}"
            )

        excluded[season_dir.name] = frozenset(offending_weeks)
        excluded_count += len(offending_weeks)

    # The count alone cannot express the third outcome: a season that failed to
    # measure excluded nothing, so "0 season-week(s) excluded" read alone would
    # claim a clean corpus. Name the unmeasurable seasons when there are any.
    summary = f"Accuracy evaluation corpus: {excluded_count} season-week(s) excluded"
    if unmeasured_count:
        summary += f"; {unmeasured_count} season(s) not measured"
    logger.info(summary)

    return excluded
