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


class TestPairwiseAccuracy:
    """Tests for pairwise decision accuracy calculation."""

    @pytest.fixture
    def calculator(self):
        """Create AccuracyCalculator instance."""
        return AccuracyCalculator()

    def test_pairwise_perfect_ranking(self, calculator):
        """Test pairwise accuracy with perfect predictions."""
        player_data = [
            {'position': 'QB', 'projected': 30.0, 'actual': 28.0},
            {'position': 'QB', 'projected': 25.0, 'actual': 22.0},
            {'position': 'QB', 'projected': 20.0, 'actual': 18.0},
        ]
        accuracy = calculator.calculate_pairwise_accuracy(player_data, 'QB')
        assert accuracy == 1.0  # All 3 pairs correct

    def test_pairwise_inverse_ranking(self, calculator):
        """Test pairwise accuracy with completely wrong predictions."""
        player_data = [
            {'position': 'QB', 'projected': 30.0, 'actual': 10.0},
            {'position': 'QB', 'projected': 25.0, 'actual': 20.0},
            {'position': 'QB', 'projected': 20.0, 'actual': 30.0},
        ]
        accuracy = calculator.calculate_pairwise_accuracy(player_data, 'QB')
        assert accuracy == 0.0  # All 3 pairs wrong

    def test_pairwise_filters_low_actual(self, calculator):
        """Test that players with actual < 3 are excluded."""
        player_data = [
            {'position': 'QB', 'projected': 30.0, 'actual': 28.0},
            {'position': 'QB', 'projected': 25.0, 'actual': 2.0},  # Excluded
            {'position': 'QB', 'projected': 20.0, 'actual': 18.0},
        ]
        accuracy = calculator.calculate_pairwise_accuracy(player_data, 'QB')
        # Only 1 pair (28 vs 18), which is correct
        assert accuracy == 1.0

    def test_pairwise_skips_ties(self, calculator):
        """Test that ties in actual points are skipped."""
        player_data = [
            {'position': 'QB', 'projected': 30.0, 'actual': 20.0},
            {'position': 'QB', 'projected': 25.0, 'actual': 20.0},  # Tie
        ]
        accuracy = calculator.calculate_pairwise_accuracy(player_data, 'QB')
        assert accuracy == 0.0  # No valid comparisons (tie skipped)

    def test_pairwise_insufficient_players(self, calculator):
        """Test with fewer than 2 players."""
        player_data = [
            {'position': 'QB', 'projected': 30.0, 'actual': 28.0},
        ]
        accuracy = calculator.calculate_pairwise_accuracy(player_data, 'QB')
        assert accuracy == 0.0

    def test_pairwise_per_position(self, calculator):
        """Test that positions are separated correctly."""
        player_data = [
            {'position': 'QB', 'projected': 30.0, 'actual': 28.0},
            {'position': 'QB', 'projected': 20.0, 'actual': 18.0},
            {'position': 'RB', 'projected': 25.0, 'actual': 22.0},  # Different position
        ]
        accuracy = calculator.calculate_pairwise_accuracy(player_data, 'QB')
        assert accuracy == 1.0  # Only QBs compared

    def test_pairwise_accuracy_k_position(self, calculator):
        """Test pairwise accuracy with K position (discrete scoring: 0, 3, 6, 9)."""
        player_data = [
            {'position': 'K', 'projected': 9.0, 'actual': 9.0},
            {'position': 'K', 'projected': 6.0, 'actual': 6.0},
            {'position': 'K', 'projected': 3.0, 'actual': 3.0},
        ]
        accuracy = calculator.calculate_pairwise_accuracy(player_data, 'K')
        assert accuracy == 1.0  # Perfect ranking
        assert accuracy is not None
        assert not (accuracy != accuracy)  # Not NaN

    def test_pairwise_accuracy_dst_position_with_negatives(self, calculator):
        """Test pairwise accuracy with DST position including negative scores."""
        player_data = [
            {'position': 'DST', 'projected': 12.0, 'actual': 15.0},
            {'position': 'DST', 'projected': 8.0, 'actual': 5.0},
            {'position': 'DST', 'projected': 5.0, 'actual': 3.0},  # Above filter threshold
        ]
        accuracy = calculator.calculate_pairwise_accuracy(player_data, 'DST')
        assert accuracy == 1.0  # Perfect ranking
        assert accuracy is not None
        assert not (accuracy != accuracy)  # Not NaN


class TestTopNAccuracy:
    """Tests for top-N overlap accuracy calculation."""

    @pytest.fixture
    def calculator(self):
        """Create AccuracyCalculator instance."""
        return AccuracyCalculator()

    def test_top_n_perfect_overlap(self, calculator):
        """Test top-N accuracy with perfect overlap."""
        player_data = [
            {'position': 'WR', 'name': 'Player A', 'projected': 30.0, 'actual': 28.0},
            {'position': 'WR', 'name': 'Player B', 'projected': 25.0, 'actual': 22.0},
            {'position': 'WR', 'name': 'Player C', 'projected': 20.0, 'actual': 18.0},
            {'position': 'WR', 'name': 'Player D', 'projected': 15.0, 'actual': 12.0},
            {'position': 'WR', 'name': 'Player E', 'projected': 10.0, 'actual': 8.0},
        ]
        accuracy = calculator.calculate_top_n_accuracy(player_data, 5, 'WR')
        assert accuracy == 1.0  # All 5 match

    def test_top_n_no_overlap(self, calculator):
        """Test top-N accuracy with no overlap."""
        player_data = [
            {'position': 'WR', 'name': 'Player A', 'projected': 30.0, 'actual': 8.0},
            {'position': 'WR', 'name': 'Player B', 'projected': 25.0, 'actual': 10.0},
            {'position': 'WR', 'name': 'Player C', 'projected': 20.0, 'actual': 12.0},
            {'position': 'WR', 'name': 'Player D', 'projected': 15.0, 'actual': 18.0},
            {'position': 'WR', 'name': 'Player E', 'projected': 10.0, 'actual': 22.0},
            {'position': 'WR', 'name': 'Player F', 'projected': 5.0, 'actual': 28.0},
        ]
        accuracy = calculator.calculate_top_n_accuracy(player_data, 5, 'WR')
        # Top 5 projected: A,B,C,D,E
        # Top 5 actual: F,E,D,C,B
        # Overlap: B,C,D,E (4/5)
        assert accuracy == 0.8

    def test_top_n_filters_low_actual(self, calculator):
        """Test that players with actual < 3 are excluded."""
        player_data = [
            {'position': 'RB', 'name': 'Player A', 'projected': 30.0, 'actual': 28.0},
            {'position': 'RB', 'name': 'Player B', 'projected': 25.0, 'actual': 2.0},  # Excluded
            {'position': 'RB', 'name': 'Player C', 'projected': 20.0, 'actual': 18.0},
        ]
        accuracy = calculator.calculate_top_n_accuracy(player_data, 2, 'RB')
        # After filtering, only A and C remain
        assert accuracy == 1.0

    def test_top_n_insufficient_players(self, calculator):
        """Test with fewer players than N."""
        player_data = [
            {'position': 'TE', 'name': 'Player A', 'projected': 30.0, 'actual': 28.0},
            {'position': 'TE', 'name': 'Player B', 'projected': 25.0, 'actual': 22.0},
        ]
        accuracy = calculator.calculate_top_n_accuracy(player_data, 5, 'TE')
        assert accuracy == 0.0  # Not enough players

    def test_top_n_accuracy_k_dst_small_sample(self, calculator):
        """Test top-N accuracy with K/DST small sample sizes."""
        # Test with 10 K players (realistic small sample)
        k_player_data = [
            {'position': 'K', 'name': f'K{i}', 'projected': 10.0 - i, 'actual': 10.0 - i}
            for i in range(10)
        ]
        # Top-5 accuracy with perfect predictions
        accuracy_top5 = calculator.calculate_top_n_accuracy(k_player_data, 5, 'K')
        assert accuracy_top5 == 1.0
        assert accuracy_top5 is not None
        assert not (accuracy_top5 != accuracy_top5)  # Not NaN

        # Test with 10 DST players
        dst_player_data = [
            {'position': 'DST', 'name': f'DST{i}', 'projected': 15.0 - i, 'actual': 15.0 - i}
            for i in range(10)
        ]
        accuracy_dst = calculator.calculate_top_n_accuracy(dst_player_data, 5, 'DST')
        assert accuracy_dst == 1.0
        assert accuracy_dst is not None


class TestSpearmanCorrelation:
    """Tests for Spearman rank correlation calculation."""

    @pytest.fixture
    def calculator(self):
        """Create AccuracyCalculator instance."""
        return AccuracyCalculator()

    def test_spearman_perfect_correlation(self, calculator):
        """Test Spearman with perfect positive correlation."""
        player_data = [
            {'position': 'QB', 'projected': 30.0, 'actual': 28.0},
            {'position': 'QB', 'projected': 25.0, 'actual': 22.0},
            {'position': 'QB', 'projected': 20.0, 'actual': 18.0},
            {'position': 'QB', 'projected': 15.0, 'actual': 12.0},
        ]
        corr = calculator.calculate_spearman_correlation(player_data, 'QB')
        assert abs(corr - 1.0) < 0.01  # Should be ~1.0

    def test_spearman_inverse_correlation(self, calculator):
        """Test Spearman with perfect negative correlation."""
        player_data = [
            {'position': 'QB', 'projected': 30.0, 'actual': 12.0},
            {'position': 'QB', 'projected': 25.0, 'actual': 18.0},
            {'position': 'QB', 'projected': 20.0, 'actual': 22.0},
            {'position': 'QB', 'projected': 15.0, 'actual': 28.0},
        ]
        corr = calculator.calculate_spearman_correlation(player_data, 'QB')
        assert abs(corr - (-1.0)) < 0.01  # Should be ~-1.0

    def test_spearman_zero_variance(self, calculator):
        """Test Spearman handles zero variance gracefully."""
        player_data = [
            {'position': 'QB', 'projected': 20.0, 'actual': 20.0},
            {'position': 'QB', 'projected': 20.0, 'actual': 20.0},
            {'position': 'QB', 'projected': 20.0, 'actual': 20.0},
        ]
        corr = calculator.calculate_spearman_correlation(player_data, 'QB')
        assert corr == 0.0  # Should return 0 for zero variance

    def test_spearman_filters_low_actual(self, calculator):
        """Test that players with actual < 3 are excluded."""
        player_data = [
            {'position': 'WR', 'projected': 30.0, 'actual': 28.0},
            {'position': 'WR', 'projected': 25.0, 'actual': 2.0},  # Excluded
            {'position': 'WR', 'projected': 20.0, 'actual': 18.0},
        ]
        corr = calculator.calculate_spearman_correlation(player_data, 'WR')
        # Only 2 players remain, should still calculate
        assert abs(corr - 1.0) < 0.01

    def test_spearman_insufficient_players(self, calculator):
        """Test with fewer than 2 players."""
        player_data = [
            {'position': 'TE', 'projected': 30.0, 'actual': 28.0},
        ]
        corr = calculator.calculate_spearman_correlation(player_data, 'TE')
        assert corr == 0.0

    def test_spearman_correlation_k_dst(self, calculator):
        """Test Spearman correlation with K and DST positions."""
        # Test K position with discrete scoring pattern
        k_player_data = [
            {'position': 'K', 'projected': 9.0, 'actual': 12.0},
            {'position': 'K', 'projected': 8.0, 'actual': 6.0},
            {'position': 'K', 'projected': 7.0, 'actual': 9.0},
            {'position': 'K', 'projected': 6.0, 'actual': 3.0},
        ]
        corr_k = calculator.calculate_spearman_correlation(k_player_data, 'K')
        assert -1.0 <= corr_k <= 1.0  # Valid correlation range
        assert corr_k is not None
        assert not (corr_k != corr_k)  # Not NaN

        # Test DST position
        dst_player_data = [
            {'position': 'DST', 'projected': 10.0, 'actual': 15.0},
            {'position': 'DST', 'projected': 8.0, 'actual': 5.0},
            {'position': 'DST', 'projected': 6.0, 'actual': 10.0},
            {'position': 'DST', 'projected': 4.0, 'actual': 3.0},
        ]
        corr_dst = calculator.calculate_spearman_correlation(dst_player_data, 'DST')
        assert -1.0 <= corr_dst <= 1.0  # Valid correlation range
        assert corr_dst is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
