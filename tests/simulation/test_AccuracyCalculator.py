"""
Tests for AccuracyCalculator

Tests MAE calculation logic with various scenarios.

Author: Kai Mizuno
"""

import pytest
from pathlib import Path
import sys

# Add simulation/accuracy to path
sys.path.append(str(Path(__file__).parent.parent.parent / "simulation" / "accuracy"))
from AccuracyCalculator import AccuracyCalculator, AccuracyResult


class TestAccuracyResult:
    """Tests for AccuracyResult dataclass."""

    def test_accuracy_result_creation(self):
        """Test creating an AccuracyResult."""
        result = AccuracyResult(
            mae=5.5,
            player_count=100,
            total_error=550.0
        )
        assert result.mae == 5.5
        assert result.player_count == 100
        assert result.total_error == 550.0
        assert result.errors == []

    def test_accuracy_result_with_errors(self):
        """Test AccuracyResult with individual errors."""
        errors = [1.0, 2.0, 3.0]
        result = AccuracyResult(
            mae=2.0,
            player_count=3,
            total_error=6.0,
            errors=errors
        )
        assert result.errors == errors

    def test_accuracy_result_repr(self):
        """Test AccuracyResult string representation."""
        result = AccuracyResult(mae=5.5, player_count=100, total_error=550.0)
        assert "mae=5.5000" in repr(result)
        assert "players=100" in repr(result)


class TestAccuracyCalculator:
    """Tests for AccuracyCalculator class."""

    @pytest.fixture
    def calculator(self):
        """Create AccuracyCalculator instance."""
        return AccuracyCalculator()

    def test_calculate_mae_basic(self, calculator):
        """Test basic MAE calculation."""
        player_data = [
            {'projected': 10.0, 'actual': 12.0},  # error = 2
            {'projected': 15.0, 'actual': 13.0},  # error = 2
            {'projected': 20.0, 'actual': 25.0},  # error = 5
        ]
        result = calculator.calculate_mae(player_data)

        assert result.player_count == 3
        assert result.total_error == 9.0
        assert result.mae == 3.0  # 9/3

    def test_calculate_mae_perfect_prediction(self, calculator):
        """Test MAE with perfect predictions."""
        player_data = [
            {'projected': 10.0, 'actual': 10.0},
            {'projected': 15.0, 'actual': 15.0},
        ]
        result = calculator.calculate_mae(player_data)

        assert result.mae == 0.0
        assert result.player_count == 2

    def test_calculate_mae_excludes_zero_actual(self, calculator):
        """Test that players with 0 actual points are excluded."""
        player_data = [
            {'projected': 10.0, 'actual': 12.0},  # included
            {'projected': 15.0, 'actual': 0.0},   # excluded
            {'projected': 20.0, 'actual': 0.0},   # excluded
        ]
        result = calculator.calculate_mae(player_data)

        assert result.player_count == 1
        assert result.mae == 2.0

    def test_calculate_mae_excludes_negative_actual(self, calculator):
        """Test that players with negative actual points are excluded."""
        player_data = [
            {'projected': 10.0, 'actual': 12.0},   # included
            {'projected': 15.0, 'actual': -1.0},   # excluded
        ]
        result = calculator.calculate_mae(player_data)

        assert result.player_count == 1

    def test_calculate_mae_empty_data(self, calculator):
        """Test MAE with no valid data."""
        result = calculator.calculate_mae([])
        assert result.mae == 0.0
        assert result.player_count == 0

    def test_calculate_mae_all_excluded(self, calculator):
        """Test MAE when all players are excluded."""
        player_data = [
            {'projected': 10.0, 'actual': 0.0},
            {'projected': 15.0, 'actual': 0.0},
        ]
        result = calculator.calculate_mae(player_data)

        assert result.mae == 0.0
        assert result.player_count == 0

    def test_calculate_mae_with_individual_errors(self, calculator):
        """Test MAE calculation includes individual errors when requested."""
        player_data = [
            {'projected': 10.0, 'actual': 12.0},
            {'projected': 15.0, 'actual': 13.0},
        ]
        result = calculator.calculate_mae(player_data, include_individual_errors=True)

        assert len(result.errors) == 2
        assert 2.0 in result.errors

    def test_calculate_mae_handles_missing_keys(self, calculator):
        """Test MAE handles missing projected/actual keys."""
        player_data = [
            {'projected': 10.0},  # missing actual - defaults to 0, excluded
            {'actual': 12.0},     # missing projected - defaults to 0, included (actual > 0)
            {'projected': 15.0, 'actual': 15.0},  # valid
        ]
        result = calculator.calculate_mae(player_data)

        # Two valid: the second (actual > 0, projected defaults to 0) and the third
        # The second has error |12.0 - 0| = 12.0
        # The third has error |15.0 - 15.0| = 0.0
        # Total = 12.0, count = 2, MAE = 6.0
        assert result.player_count == 2
        assert result.mae == 6.0


class TestAccuracyCalculatorWeekly:
    """Tests for weekly MAE calculation."""

    @pytest.fixture
    def calculator(self):
        """Create AccuracyCalculator instance."""
        return AccuracyCalculator()

    def test_calculate_weekly_mae(self, calculator):
        """Test weekly MAE calculation."""
        week_projections = {
            1: {1: 15.0, 2: 20.0},
            2: {1: 16.0, 2: 21.0},
        }
        week_actuals = {
            1: {1: 12.0, 2: 22.0},  # errors: 3, 2
            2: {1: 14.0, 2: 19.0},  # errors: 2, 2
        }

        result = calculator.calculate_weekly_mae(
            week_projections, week_actuals, (1, 2)
        )

        assert result.player_count == 4
        # total error = 3 + 2 + 2 + 2 = 9, mae = 9/4 = 2.25
        assert result.mae == 2.25

    def test_calculate_weekly_mae_missing_week(self, calculator):
        """Test weekly MAE skips missing weeks."""
        week_projections = {
            1: {1: 15.0},
            # week 2 missing
        }
        week_actuals = {
            1: {1: 12.0},
            # week 2 missing
        }

        result = calculator.calculate_weekly_mae(
            week_projections, week_actuals, (1, 2)
        )

        assert result.player_count == 1

    def test_calculate_weekly_mae_single_week(self, calculator):
        """Test weekly MAE for a single week."""
        week_projections = {5: {1: 15.0, 2: 20.0}}
        week_actuals = {5: {1: 10.0, 2: 25.0}}

        result = calculator.calculate_weekly_mae(
            week_projections, week_actuals, (5, 5)
        )

        assert result.player_count == 2
        assert result.mae == 5.0  # errors: 5, 5


class TestAccuracyCalculatorAggregation:
    """Tests for season result aggregation."""

    @pytest.fixture
    def calculator(self):
        """Create AccuracyCalculator instance."""
        return AccuracyCalculator()

    def test_aggregate_season_results(self, calculator):
        """Test aggregating results across seasons."""
        season_results = [
            ('2023', AccuracyResult(mae=5.0, player_count=100, total_error=500.0)),
            ('2024', AccuracyResult(mae=4.0, player_count=100, total_error=400.0)),
        ]

        result = calculator.aggregate_season_results(season_results)

        assert result.player_count == 200
        assert result.total_error == 900.0
        assert result.mae == 4.5  # 900/200

    def test_aggregate_season_results_weighted(self, calculator):
        """Test aggregation properly weights by player count."""
        season_results = [
            ('2023', AccuracyResult(mae=5.0, player_count=50, total_error=250.0)),
            ('2024', AccuracyResult(mae=3.0, player_count=150, total_error=450.0)),
        ]

        result = calculator.aggregate_season_results(season_results)

        assert result.player_count == 200
        assert result.total_error == 700.0
        assert result.mae == 3.5  # 700/200 (not 4.0 which would be unweighted avg)

    def test_aggregate_season_results_empty(self, calculator):
        """Test aggregation with no results."""
        result = calculator.aggregate_season_results([])

        assert result.mae == 0.0
        assert result.player_count == 0

    def test_aggregate_season_results_single(self, calculator):
        """Test aggregation with single season."""
        season_results = [
            ('2024', AccuracyResult(mae=5.0, player_count=100, total_error=500.0)),
        ]

        result = calculator.aggregate_season_results(season_results)

        assert result.mae == 5.0
        assert result.player_count == 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
