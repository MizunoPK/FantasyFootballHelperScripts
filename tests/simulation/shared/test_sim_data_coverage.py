"""
Unit Tests for the Shared Sim Data Projection Coverage Computation

Covers simulation/shared/sim_data_coverage - the single owner (D8 TD4) of the
scale-free, production-ranked, bye-excluded projection coverage measurement that
validate_sim_data.py reports and enforces against the floors in the same module
(D8.3).

Author: Kai Mizuno
"""

# Standard library
import json
from unittest.mock import MagicMock, patch

# Third-party
import pytest

# Local
from historical_data_compiler.constants import (
    POSITION_JSON_FILES,
    REGULAR_SEASON_WEEKS,
    VALIDATION_WEEKS,
    WEEKS_FOLDER,
)
from simulation.shared.sim_data_coverage import (
    BYE_CONVENTION,
    PER_SEASON_COVERAGE_FLOOR_PCT,
    PER_WEEK_COVERAGE_FLOOR_PCT,
    check_coverage,
    compute_season_coverage,
    excluded_weeks_by_season,
    season_below_floor,
    SeasonCoverage,
    select_coverage_population,
    weeks_below_floor,
)


# FIXTURES

def _record(name, position, projected, actual, bye_week=None, adp=170.0):
    """Build one synthetic compiled player record."""
    return {
        'id': name,
        'name': name,
        'position': position,
        'bye_week': bye_week,
        'average_draft_position': adp,
        'projected_points': list(projected),
        'actual_points': list(actual),
    }


def _flat(value):
    """A REGULAR_SEASON_WEEKS-long array of one repeated value."""
    return [value] * REGULAR_SEASON_WEEKS


def _write_season(season_dir, records_by_position):
    """Write a synthetic season tree carrying only the season-final snapshot."""
    snapshot = season_dir / WEEKS_FOLDER / f"week_{VALIDATION_WEEKS:02d}"
    snapshot.mkdir(parents=True, exist_ok=True)
    for position, filename in POSITION_JSON_FILES.items():
        key = filename.rsplit('.', 1)[0]
        payload = {key: records_by_position.get(position, [])}
        (snapshot / filename).write_text(json.dumps(payload))
    return snapshot


def _coverage(per_week, population_size=200):
    """Build a synthetic SeasonCoverage from a {week: (covered, eligible)} map."""
    return SeasonCoverage(
        per_week=dict(per_week),
        season=(
            sum(covered for covered, _ in per_week.values()),
            sum(eligible for _, eligible in per_week.values()),
        ),
        population_size=population_size,
    )


def _committed_seasons():
    """Resolve the committed sim_data corpus, skipping if it is not present.

    The corpus-backed tests below assert facts about the real committed
    seasons, so they are meaningful only in a checkout that carries them. A
    missing corpus is an environment without the data, not a failure of the
    code under test, so it SKIPS rather than raising FileNotFoundError out of
    iterdir().

    Returns:
        The sorted list of numeric season directories under simulation/sim_data.
    """
    from pathlib import Path
    sim_data = Path(__file__).resolve().parents[3] / "simulation" / "sim_data"
    if not sim_data.is_dir():
        pytest.skip(f"committed sim_data corpus not present at {sim_data}")

    seasons = sorted(p for p in sim_data.iterdir() if p.name.isdigit())
    if not seasons:
        pytest.skip(f"committed sim_data corpus carries no seasons at {sim_data}")
    return seasons


@pytest.fixture
def season_dir(tmp_path):
    """An empty season directory a test fills via _write_season."""
    return tmp_path / "2023"


class TestSelectCoveragePopulation:
    """The scale-free, production-ranked population rule (D8 TD2)."""

    def test_ranks_by_season_actual_production_not_adp(self, season_dir):
        # Arrange - the best ADP belongs to the worst producer
        _write_season(season_dir, {'QB': [
            _record('low_prod_best_adp', 'QB', _flat(1.0), _flat(1.0), adp=1.0),
            _record('high_prod_worst_adp', 'QB', _flat(1.0), _flat(20.0), adp=880.0),
        ]})

        # Act
        population = select_coverage_population(season_dir)

        # Assert
        assert [r['name'] for r in population] == [
            'high_prod_worst_adp', 'low_prod_best_adp'
        ]

    def test_truncates_to_the_population_size(self, season_dir):
        # Arrange
        with patch(
            'simulation.shared.sim_data_coverage.COVERAGE_POPULATION_SIZE', 2
        ):
            _write_season(season_dir, {'RB': [
                _record(f"rb{i}", 'RB', _flat(1.0), _flat(float(i)))
                for i in range(5)
            ]})

            # Act
            population = select_coverage_population(season_dir)

        # Assert
        assert [r['name'] for r in population] == ['rb4', 'rb3']

    def test_reads_every_position_file(self, season_dir):
        # Arrange
        _write_season(season_dir, {
            position: [_record(position, position, _flat(1.0), _flat(1.0))]
            for position in POSITION_JSON_FILES
        })

        # Act
        population = select_coverage_population(season_dir)

        # Assert
        assert sorted(r['position'] for r in population) == sorted(POSITION_JSON_FILES)


class TestByeExclusion:
    """A player's own bye week leaves that player's denominator (D8 TD3)."""

    def test_bye_week_is_removed_from_the_denominator(self, season_dir):
        # Arrange - one player, projected in every week except its own bye
        projected = _flat(10.0)
        projected[5] = 0.0
        _write_season(season_dir, {'QB': [
            _record('bye6', 'QB', projected, _flat(10.0), bye_week=6),
        ]})

        # Act
        coverage = compute_season_coverage(season_dir)

        # Assert - bye-excluded is a perfect season; bye-included would be 16/17
        assert coverage.per_week[6] == (0, 0)
        assert coverage.season == (REGULAR_SEASON_WEEKS - 1, REGULAR_SEASON_WEEKS - 1)

    def test_missing_bye_week_excludes_no_week(self, season_dir):
        # Arrange
        _write_season(season_dir, {'QB': [
            _record('nobye', 'QB', _flat(10.0), _flat(10.0), bye_week=None),
        ]})

        # Act
        coverage = compute_season_coverage(season_dir)

        # Assert
        assert coverage.season == (REGULAR_SEASON_WEEKS, REGULAR_SEASON_WEEKS)

    def test_out_of_range_bye_week_excludes_no_week(self, season_dir):
        # Arrange
        _write_season(season_dir, {'QB': [
            _record('bye18', 'QB', _flat(10.0), _flat(10.0),
                    bye_week=REGULAR_SEASON_WEEKS + 1),
        ]})

        # Act
        coverage = compute_season_coverage(season_dir)

        # Assert
        assert coverage.season == (REGULAR_SEASON_WEEKS, REGULAR_SEASON_WEEKS)


class TestCoveragePredicate:
    """Covered is projected_points[week - 1] > 0, applied to every position."""

    def test_zero_projection_is_not_covered(self, season_dir):
        # Arrange
        projected = _flat(10.0)
        projected[0] = 0.0
        _write_season(season_dir, {'WR': [
            _record('wk1_zero', 'WR', projected, _flat(10.0)),
        ]})

        # Act
        coverage = compute_season_coverage(season_dir)

        # Assert
        assert coverage.per_week[1] == (0, 1)
        assert coverage.per_week[2] == (1, 1)

    def test_dst_zero_projection_is_not_special_cased(self, season_dir):
        # Arrange
        _write_season(season_dir, {'DST': [
            _record('dst_zero', 'DST', _flat(0.0), _flat(5.0)),
        ]})

        # Act
        coverage = compute_season_coverage(season_dir)

        # Assert
        assert coverage.season == (0, REGULAR_SEASON_WEEKS)

    def test_negative_projection_is_not_covered(self, season_dir):
        # Arrange
        _write_season(season_dir, {'DST': [
            _record('dst_neg', 'DST', _flat(-2.0), _flat(5.0)),
        ]})

        # Act
        coverage = compute_season_coverage(season_dir)

        # Assert
        assert coverage.season == (0, REGULAR_SEASON_WEEKS)

    def test_per_week_and_season_are_both_reported(self, season_dir):
        # Arrange
        _write_season(season_dir, {'TE': [
            _record('te', 'TE', _flat(4.0), _flat(4.0)),
        ]})

        # Act
        coverage = compute_season_coverage(season_dir)

        # Assert
        assert sorted(coverage.per_week) == list(range(1, REGULAR_SEASON_WEEKS + 1))
        assert coverage.season == (REGULAR_SEASON_WEEKS, REGULAR_SEASON_WEEKS)
        assert coverage.population_size == 1


class TestCheckCoverageDegradation:
    """Every malformed input degrades to a logged WARNING and a True return."""

    def _run(self, season_dir):
        logger = MagicMock()
        with patch('simulation.shared.sim_data_coverage.get_logger',
                   return_value=logger):
            result = check_coverage(season_dir)
        return result, logger

    def test_healthy_season_logs_info_and_returns_true(self, season_dir):
        # Arrange
        _write_season(season_dir, {'QB': [
            _record('qb', 'QB', _flat(10.0), _flat(10.0)),
        ]})

        # Act
        result, logger = self._run(season_dir)

        # Assert
        assert result is True
        assert logger.warning.call_count == 0
        info_messages = [c.args[0] for c in logger.info.call_args_list]
        assert len(info_messages) == REGULAR_SEASON_WEEKS + 2
        assert all(BYE_CONVENTION in msg for msg in info_messages)

    def test_missing_snapshot_folder_warns_and_returns_true(self, season_dir):
        # Arrange - nothing is written at all
        season_dir.mkdir(parents=True)

        # Act
        result, logger = self._run(season_dir)

        # Assert
        assert result is True
        assert logger.warning.call_count == 1
        assert f"week_{VALIDATION_WEEKS:02d}" in logger.warning.call_args.args[0]

    def test_invalid_json_warns_and_returns_true(self, season_dir):
        # Arrange
        snapshot = _write_season(season_dir, {})
        (snapshot / POSITION_JSON_FILES['QB']).write_text("{not valid json")

        # Act
        result, logger = self._run(season_dir)

        # Assert
        assert result is True
        assert logger.warning.call_count == 1
        assert POSITION_JSON_FILES['QB'] in logger.warning.call_args.args[0]

    def test_non_utf8_file_warns_and_returns_true(self, season_dir):
        # Arrange - a single non-UTF-8 byte raises UnicodeDecodeError, a
        # ValueError sibling of json.JSONDecodeError rather than a subclass.
        snapshot = _write_season(season_dir, {})
        path = snapshot / POSITION_JSON_FILES['QB']
        path.write_bytes(b'\xff' + json.dumps({'qb_data': []}).encode())

        # Act
        result, logger = self._run(season_dir)

        # Assert
        assert result is True
        assert logger.warning.call_count == 1
        assert POSITION_JSON_FILES['QB'] in logger.warning.call_args.args[0]

    def test_missing_wrapper_key_warns_and_returns_true(self, season_dir):
        # Arrange
        snapshot = _write_season(season_dir, {})
        (snapshot / POSITION_JSON_FILES['QB']).write_text(json.dumps([{"id": 1}]))

        # Act
        result, logger = self._run(season_dir)

        # Assert
        assert result is True
        assert logger.warning.call_count == 1
        assert POSITION_JSON_FILES['QB'] in logger.warning.call_args.args[0]

    def test_record_missing_actual_points_warns_and_returns_true(self, season_dir):
        # Arrange
        snapshot = _write_season(season_dir, {})
        (snapshot / POSITION_JSON_FILES['QB']).write_text(
            json.dumps({'qb_data': [{'name': 'broken'}]})
        )

        # Act
        result, logger = self._run(season_dir)

        # Assert
        assert result is True
        assert logger.warning.call_count == 1

    def test_short_projected_points_array_warns_and_returns_true(self, season_dir):
        # Arrange
        _write_season(season_dir, {'QB': [
            _record('short', 'QB', [1.0], _flat(10.0)),
        ]})

        # Act
        result, logger = self._run(season_dir)

        # Assert
        assert result is True
        assert logger.warning.call_count == 1

    def test_partial_population_reports_its_actual_size(self, season_dir):
        # Arrange
        _write_season(season_dir, {'QB': [
            _record(f"qb{i}", 'QB', _flat(10.0), _flat(10.0)) for i in range(3)
        ]})

        # Act
        result, logger = self._run(season_dir)

        # Assert
        assert result is True
        assert "top 3 by season actual production" in logger.info.call_args_list[0].args[0]


class TestRealCorpusSeparation:
    """The one fact D8 exists to protect, asserted as an inequality."""

    def test_2023_week_1_is_below_every_other_season_week(self):
        # Arrange
        seasons = _committed_seasons()

        # Act - a week with no eligible player-weeks has no coverage RATE at
        # all (0/0 is undefined, not 0%), so it is excluded from the corridor
        # rather than divided by. compute_season_coverage already reports such
        # a week separately; asserting a rate for it would be inventing one.
        rates = {}
        for season in seasons:
            coverage = compute_season_coverage(season)
            for week, (covered, eligible) in coverage.per_week.items():
                if eligible == 0:
                    continue
                rates[(season.name, week)] = covered / eligible

        assert rates, "no measurable season-week in the committed corpus"

        # Assert
        # Assert against the CORRIDOR, not the observed extremes. The defect
        # (2023 wk1, 16.0%) and the next-lowest healthy week (2021 wk16, 81.0%)
        # are separated by ~5.06x, so 0.50 sits well inside the gap: every
        # implementation regression this test exists to catch (an ADP-ranked
        # population, a bye-convention flip, a wrong week span) moves one side
        # across it, while ordinary corpus drift cannot. The exact 16.0% / 81.0%
        # figures are recorded in coverage_baseline.md, D8.3's calibration input.
        defective = rates.pop(('2023', 1))
        assert defective < 0.50
        assert min(rates.values()) > 0.50


class TestWeeksBelowFloor:
    """The per-week floor predicate: raw counts, strictly below, byes excluded."""

    def test_a_week_below_the_floor_is_returned(self):
        # Arrange - 40% against a 50.0% floor
        coverage = _coverage({1: (40, 100)})

        # Act / Assert
        assert weeks_below_floor(coverage) == [1]

    def test_a_week_exactly_at_the_floor_passes(self):
        # Arrange - exactly 50.0%; the raw-count comparison must not round it down
        coverage = _coverage({1: (50, 100)})

        # Act / Assert
        assert weeks_below_floor(coverage) == []

    def test_a_week_above_the_floor_passes(self):
        # Arrange
        coverage = _coverage({1: (51, 100)})

        # Act / Assert
        assert weeks_below_floor(coverage) == []

    def test_offending_weeks_are_returned_in_week_order(self):
        # Arrange - inserted out of order on purpose
        coverage = _coverage({3: (1, 100), 1: (2, 100), 2: (99, 100)})

        # Act / Assert
        assert weeks_below_floor(coverage) == [1, 3]

    def test_a_zero_denominator_week_is_not_reported_as_a_breach(self):
        # Arrange - 0/0 is not a measurement and must never read as 0.0%.
        #
        # This asserts the OUTCOME, not the `if eligible == 0: continue` guard,
        # and the distinction is deliberate. The raw-count comparison already
        # yields this outcome without the guard: `covered <= eligible` holds by
        # construction (compute_season_coverage increments covered only after
        # eligible), so eligible == 0 implies covered == 0 and the comparison
        # reads 0 * 100.0 < 50.0 * 0, i.e. 0.0 < 0.0, which is False. No
        # in-domain input can therefore distinguish the guard's presence - the
        # only input that does is a NEGATIVE covered count, which no producer
        # can emit and which is outside a count's domain. The guard is kept
        # because it states the intent explicitly and is the correct shape for a
        # future divided implementation (covered / eligible), under which
        # eligible == 0 becomes a ZeroDivisionError rather than a benign False.
        coverage = _coverage({1: (0, 0), 2: (99, 100)})

        # Act / Assert
        assert weeks_below_floor(coverage) == []


class TestSeasonBelowFloor:
    """The per-season backstop predicate, on the same comparison rules."""

    def test_a_season_below_the_floor_is_reported(self):
        # Arrange - 74% against a 75.0% floor
        coverage = _coverage({1: (74, 100)})

        # Act / Assert
        assert season_below_floor(coverage) is True

    def test_a_season_exactly_at_the_floor_passes(self):
        # Arrange - exactly 75.0%
        coverage = _coverage({1: (75, 100)})

        # Act / Assert
        assert season_below_floor(coverage) is False

    def test_a_season_above_the_floor_passes(self):
        # Arrange
        coverage = _coverage({1: (76, 100)})

        # Act / Assert
        assert season_below_floor(coverage) is False

    def test_a_zero_denominator_season_is_not_below_the_floor(self):
        # Arrange - an empty population, not a 0% covered one.
        #
        # Same shape as the per-week twin above: this asserts the OUTCOME, not
        # the `if eligible == 0: return False` guard, which the raw-count
        # comparison already produces on its own for every in-domain input. See
        # test_a_zero_denominator_week_is_not_reported_as_a_breach for the full
        # derivation and for why the guard is nonetheless kept.
        coverage = _coverage({1: (0, 0)}, population_size=0)

        # Act / Assert
        assert season_below_floor(coverage) is False


class TestCheckCoverageEnforcement:
    """check_coverage now returns False on a measured floor violation."""

    def _run(self, season_dir):
        logger = MagicMock()
        with patch('simulation.shared.sim_data_coverage.get_logger',
                   return_value=logger):
            result = check_coverage(season_dir)
        return result, logger

    def test_a_week_below_the_per_week_floor_fails_and_names_the_week(self, season_dir):
        # Arrange - three players, two of them zeroed in week 1 (1/3 = 33.3%).
        # The population is 3, well under COVERAGE_POPULATION_SIZE, so this also
        # pins that a partial-but-non-zero population is enforced normally.
        zeroed = _flat(10.0)
        zeroed[0] = 0.0
        _write_season(season_dir, {'QB': [
            _record('ok', 'QB', _flat(10.0), _flat(10.0)),
            _record('zero_a', 'QB', zeroed, _flat(10.0)),
            _record('zero_b', 'QB', zeroed, _flat(10.0)),
        ]})

        # Act
        result, logger = self._run(season_dir)

        # Assert
        assert result is False
        errors = [c.args[0] for c in logger.error.call_args_list]
        assert len(errors) == 1
        assert "week 01" in errors[0]
        assert "1/3" in errors[0]
        assert f"{PER_WEEK_COVERAGE_FLOOR_PCT:.1f}% per-week floor" in errors[0]
        assert errors[0].count(BYE_CONVENTION) == 2
        assert "population 3" in errors[0]

    def test_a_diffuse_season_fails_the_backstop_with_no_week_below(self, season_dir):
        # Arrange - every week sits at 60% (above the per-week floor) while the
        # season aggregate is 60% (below the per-season floor): the diffuse
        # degradation the per-week floor structurally cannot see.
        _write_season(season_dir, {'RB': (
            [_record(f"ok{i}", 'RB', _flat(10.0), _flat(10.0)) for i in range(3)]
            + [_record(f"zero{i}", 'RB', _flat(0.0), _flat(9.0)) for i in range(2)]
        )})

        # Act
        result, logger = self._run(season_dir)

        # Assert
        assert result is False
        errors = [c.args[0] for c in logger.error.call_args_list]
        assert len(errors) == 1
        assert f"{PER_SEASON_COVERAGE_FLOOR_PCT:.1f}% per-season floor" in errors[0]
        assert "per-week floor" not in errors[0]

    def test_a_healthy_season_logs_no_error_and_returns_true(self, season_dir):
        # Arrange
        _write_season(season_dir, {'TE': [
            _record('te', 'TE', _flat(4.0), _flat(4.0)),
        ]})

        # Act
        result, logger = self._run(season_dir)

        # Assert
        assert result is True
        assert logger.error.call_count == 0

    def test_an_empty_population_warns_and_returns_true(self, season_dir):
        # Arrange - every position file parses and holds an empty list, so the
        # season denominator is 0. That is a missing corpus, not 0% coverage.
        _write_season(season_dir, {})

        # Act
        result, logger = self._run(season_dir)

        # Assert
        assert result is True
        assert logger.error.call_count == 0
        assert logger.warning.call_count == 1
        assert "no eligible player-weeks" in logger.warning.call_args.args[0]


class TestRealCorpusEnforcement:
    """The committed corpus, asserted against the floors rather than a figure."""

    def _seasons(self):
        return _committed_seasons()

    def test_only_2023_week_1_is_below_the_per_week_floor(self):
        # Arrange
        seasons = self._seasons()

        # Act
        offending = {
            season.name: weeks_below_floor(compute_season_coverage(season))
            for season in seasons
        }

        # Assert - the defect fires, and nothing else does. A floor that failed a
        # second committed season would be mis-calibrated, not stricter.
        assert offending.pop('2023') == [1]
        assert all(weeks == [] for weeks in offending.values())

    def test_no_committed_season_is_below_the_per_season_floor(self):
        # Arrange
        seasons = self._seasons()

        # Act / Assert - the backstop deliberately does not fire on 2023 either;
        # 2023 exits 1 solely by the per-week floor above.
        assert all(
            season_below_floor(compute_season_coverage(season)) is False
            for season in seasons
        )


class TestExcludedWeeksBySeason:
    """The harness-facing exclusion mapping (D8.4): floor-driven, loud, fail-open."""

    def _run(self, season_dirs):
        logger = MagicMock()
        with patch('simulation.shared.sim_data_coverage.get_logger',
                   return_value=logger):
            mapping = excluded_weeks_by_season(season_dirs)
        return mapping, logger

    def _defective(self, season_dir):
        """Write a season whose week 1 alone is below the floor."""
        projected = _flat(10.0)
        projected[0] = 0.0
        _write_season(season_dir, {'QB': [
            _record('qb', 'QB', projected, _flat(10.0)),
        ]})

    def _healthy(self, season_dir):
        """Write a season every week of which is fully covered."""
        _write_season(season_dir, {'QB': [
            _record('qb', 'QB', _flat(10.0), _flat(10.0)),
        ]})

    def test_a_sub_floor_week_is_returned_keyed_by_directory_name(self, season_dir):
        # Arrange
        self._defective(season_dir)

        # Act
        mapping, _logger = self._run([season_dir])

        # Assert - the key is the season DIRECTORY name, which is what the
        # worker holds (season_path.name), and the value is picklable.
        assert mapping == {'2023': frozenset({1})}

    def test_a_healthy_season_is_omitted_from_the_mapping(self, season_dir):
        # Arrange
        self._healthy(season_dir)

        # Act
        mapping, logger = self._run([season_dir])

        # Assert
        assert mapping == {}
        assert logger.warning.call_count == 0

    def test_each_exclusion_is_logged_once_naming_both_bye_conventions(self, season_dir):
        # Arrange
        self._defective(season_dir)

        # Act
        _mapping, logger = self._run([season_dir])

        # Assert - season, week, raw figure, percentage, the floor, and the bye
        # convention on BOTH figures.
        assert logger.warning.call_count == 1
        message = logger.warning.call_args.args[0]
        assert '2023' in message
        assert 'week 01' in message
        assert '0/1' in message
        assert '(0.0%)' in message
        assert f"{PER_WEEK_COVERAGE_FLOOR_PCT:.1f}%" in message
        assert message.count(BYE_CONVENTION) == 2

    def test_the_summary_count_is_logged_even_when_it_is_zero(self, season_dir):
        # Arrange - "the flag was on and nothing qualified" is a distinct
        # outcome silence cannot express.
        self._healthy(season_dir)

        # Act
        _mapping, logger = self._run([season_dir])

        # Assert
        info_messages = [c.args[0] for c in logger.info.call_args_list]
        assert info_messages == [
            'Accuracy evaluation corpus: 0 season-week(s) excluded'
        ]

    def test_an_unmeasurable_season_warns_and_excludes_nothing(self, season_dir):
        # Arrange - fail-open: an unreadable tree is not evidence that a week is
        # under-covered, and the conservative direction for a narrowing is to
        # narrow less.
        snapshot = _write_season(season_dir, {})
        (snapshot / POSITION_JSON_FILES['QB']).write_text("{not valid json")

        # Act
        mapping, logger = self._run([season_dir])

        # Assert
        assert mapping == {}
        assert logger.warning.call_count == 1
        assert POSITION_JSON_FILES['QB'] in logger.warning.call_args.args[0]

    def test_seasons_are_measured_independently(self, tmp_path):
        # Arrange
        defective = tmp_path / "2023"
        healthy = tmp_path / "2024"
        self._defective(defective)
        self._healthy(healthy)

        # Act
        mapping, logger = self._run([defective, healthy])

        # Assert
        assert mapping == {'2023': frozenset({1})}
        info_messages = [c.args[0] for c in logger.info.call_args_list]
        assert info_messages == [
            'Accuracy evaluation corpus: 1 season-week(s) excluded'
        ]
