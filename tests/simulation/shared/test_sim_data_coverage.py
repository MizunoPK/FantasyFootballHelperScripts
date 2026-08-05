"""
Unit Tests for the Shared Sim Data Projection Coverage Computation

Covers simulation/shared/sim_data_coverage - the single owner (D8 TD4) of the
scale-free, production-ranked, bye-excluded projection coverage measurement that
validate_sim_data.py reports and a later unit enforces.

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
    check_coverage,
    compute_season_coverage,
    select_coverage_population,
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
        from pathlib import Path
        sim_data = Path(__file__).resolve().parents[3] / "simulation" / "sim_data"
        seasons = sorted(p for p in sim_data.iterdir() if p.name.isdigit())

        # Act
        rates = {}
        for season in seasons:
            coverage = compute_season_coverage(season)
            for week, (covered, eligible) in coverage.per_week.items():
                rates[(season.name, week)] = covered / eligible

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
