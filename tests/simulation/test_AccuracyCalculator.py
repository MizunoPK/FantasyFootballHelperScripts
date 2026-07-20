"""
Tests for AccuracyCalculator

Tests ranking-accuracy and MAE calculation logic with various scenarios.

Author: Kai Mizuno
"""

import numpy as np
import pytest

from simulation.accuracy.AccuracyCalculator import AccuracyCalculator, AccuracyResult
from simulation.accuracy.accuracy_types import RankingMetrics
from simulation.accuracy.AccuracyResultsManager import AccuracyConfigPerformance


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

    def test_accuracy_result_coverage_defaults(self):
        """weeks_evaluated / weeks_requested default to 0 (backward-compatible, D3)."""
        result = AccuracyResult(mae=5.5, player_count=100, total_error=550.0)
        assert result.weeks_evaluated == 0
        assert result.weeks_requested == 0

    def test_accuracy_result_coverage_set(self):
        """weeks_evaluated / weeks_requested are settable via constructor (D3)."""
        result = AccuracyResult(
            mae=5.5, player_count=100, total_error=550.0,
            weeks_evaluated=3, weeks_requested=4
        )
        assert result.weeks_evaluated == 3
        assert result.weeks_requested == 4


class TestAccuracyCalculator:
    """Tests for AccuracyCalculator class."""

    @pytest.fixture
    def calculator(self):
        """Create AccuracyCalculator instance."""
        return AccuracyCalculator()

    def test_calculate_mae_basic(self, calculator):
        """Test basic MAE calculation."""
        player_data = [
            {'projected': 10.0, 'actual': 12.0},
            {'projected': 15.0, 'actual': 13.0},
            {'projected': 20.0, 'actual': 25.0},
        ]
        result = calculator.calculate_mae(player_data)

        assert result.player_count == 3
        assert result.total_error == 9.0
        assert result.mae == 3.0

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
            {'projected': 10.0, 'actual': 12.0},
            {'projected': 15.0, 'actual': 0.0},
            {'projected': 20.0, 'actual': 0.0},
        ]
        result = calculator.calculate_mae(player_data)

        assert result.player_count == 1
        assert result.mae == 2.0

    def test_calculate_mae_excludes_negative_actual(self, calculator):
        """Test that players with negative actual points are excluded."""
        player_data = [
            {'projected': 10.0, 'actual': 12.0},
            {'projected': 15.0, 'actual': -1.0},
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
            {'projected': 10.0},
            {'actual': 12.0},
            {'projected': 15.0, 'actual': 15.0},
        ]
        result = calculator.calculate_mae(player_data)

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
            1: {1: 12.0, 2: 22.0},
            2: {1: 14.0, 2: 19.0},
        }

        result = calculator.calculate_weekly_mae(
            week_projections, week_actuals, (1, 2)
        )

        assert result.player_count == 4
        assert result.mae == 2.25

    def test_calculate_weekly_mae_missing_week(self, calculator):
        """Test weekly MAE skips missing weeks."""
        week_projections = {
            1: {1: 15.0},
        }
        week_actuals = {
            1: {1: 12.0},
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
        assert result.mae == 5.0

    def test_calculate_weekly_mae_full_coverage(self, calculator):
        """Coverage: every requested week present -> evaluated == requested (D1, AC3)."""
        week_projections = {1: {1: 15.0}, 2: {1: 16.0}}
        week_actuals = {1: {1: 12.0}, 2: {1: 14.0}}

        result = calculator.calculate_weekly_mae(
            week_projections, week_actuals, (1, 2)
        )

        assert result.weeks_requested == 2
        assert result.weeks_evaluated == 2

    def test_calculate_weekly_mae_partial_coverage(self, calculator):
        """Coverage: a missing week is requested-but-not-evaluated (D1, AC3)."""
        week_projections = {1: {1: 15.0}}
        week_actuals = {1: {1: 12.0}}

        result = calculator.calculate_weekly_mae(
            week_projections, week_actuals, (1, 2)
        )

        assert result.weeks_requested == 2
        assert result.weeks_evaluated == 1


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
        assert result.mae == 4.5

    def test_aggregate_season_results_weighted(self, calculator):
        """Test aggregation properly weights by player count."""
        season_results = [
            ('2023', AccuracyResult(mae=5.0, player_count=50, total_error=250.0)),
            ('2024', AccuracyResult(mae=3.0, player_count=150, total_error=450.0)),
        ]

        result = calculator.aggregate_season_results(season_results)

        assert result.player_count == 200
        assert result.total_error == 700.0
        assert result.mae == 3.5

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

    def test_aggregate_sums_coverage(self, calculator):
        """Coverage: aggregate sums weeks_evaluated/weeks_requested across seasons,
        and leaves mae / player_count untouched (D2, AC4)."""
        r1 = AccuracyResult(mae=5.0, player_count=100, total_error=500.0,
                            weeks_evaluated=4, weeks_requested=4)
        r2 = AccuracyResult(mae=4.0, player_count=100, total_error=400.0,
                            weeks_evaluated=3, weeks_requested=4)
        season_results = [('2023', r1), ('2024', r2)]

        result = calculator.aggregate_season_results(season_results)

        assert result.weeks_evaluated == 7
        assert result.weeks_requested == 8
        assert result.mae == 4.5
        assert result.player_count == 200


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
        assert accuracy == 1.0

    def test_pairwise_inverse_ranking(self, calculator):
        """Test pairwise accuracy with completely wrong predictions."""
        player_data = [
            {'position': 'QB', 'projected': 30.0, 'actual': 10.0},
            {'position': 'QB', 'projected': 25.0, 'actual': 20.0},
            {'position': 'QB', 'projected': 20.0, 'actual': 30.0},
        ]
        accuracy = calculator.calculate_pairwise_accuracy(player_data, 'QB')
        assert accuracy == 0.0

    def test_pairwise_filters_low_actual(self, calculator):
        """Test that players with actual < 3 are excluded."""
        player_data = [
            {'position': 'QB', 'projected': 30.0, 'actual': 28.0},
            {'position': 'QB', 'projected': 25.0, 'actual': 2.0},
            {'position': 'QB', 'projected': 20.0, 'actual': 18.0},
        ]
        accuracy = calculator.calculate_pairwise_accuracy(player_data, 'QB')
        assert accuracy == 1.0

    def test_pairwise_skips_ties(self, calculator):
        """Test that an all-ties slate returns the np.nan insufficient-data sentinel (no valid comparison) (D5)."""
        player_data = [
            {'position': 'QB', 'projected': 30.0, 'actual': 20.0},
            {'position': 'QB', 'projected': 25.0, 'actual': 20.0},
        ]
        accuracy = calculator.calculate_pairwise_accuracy(player_data, 'QB')
        assert np.isnan(accuracy)

    def test_pairwise_insufficient_players(self, calculator):
        """Test with fewer than 2 players returns the np.nan insufficient-data sentinel (D5)."""
        player_data = [
            {'position': 'QB', 'projected': 30.0, 'actual': 28.0},
        ]
        accuracy = calculator.calculate_pairwise_accuracy(player_data, 'QB')
        assert np.isnan(accuracy)

    def test_pairwise_per_position(self, calculator):
        """Test that positions are separated correctly."""
        player_data = [
            {'position': 'QB', 'projected': 30.0, 'actual': 28.0},
            {'position': 'QB', 'projected': 20.0, 'actual': 18.0},
            {'position': 'RB', 'projected': 25.0, 'actual': 22.0},
        ]
        accuracy = calculator.calculate_pairwise_accuracy(player_data, 'QB')
        assert accuracy == 1.0

    def test_pairwise_accuracy_k_position(self, calculator):
        """Test pairwise accuracy with K position (discrete scoring: 0, 3, 6, 9)."""
        player_data = [
            {'position': 'K', 'projected': 9.0, 'actual': 9.0},
            {'position': 'K', 'projected': 6.0, 'actual': 6.0},
            {'position': 'K', 'projected': 3.0, 'actual': 3.0},
        ]
        accuracy = calculator.calculate_pairwise_accuracy(player_data, 'K')
        assert accuracy == 1.0
        assert accuracy is not None
        assert not (accuracy != accuracy)

    def test_pairwise_accuracy_dst_position_with_negatives(self, calculator):
        """Test pairwise accuracy with DST position including negative scores."""
        player_data = [
            {'position': 'DST', 'projected': 12.0, 'actual': 15.0},
            {'position': 'DST', 'projected': 8.0, 'actual': 5.0},
            {'position': 'DST', 'projected': 5.0, 'actual': 3.0},
        ]
        accuracy = calculator.calculate_pairwise_accuracy(player_data, 'DST')
        assert accuracy == 1.0
        assert accuracy is not None
        assert not (accuracy != accuracy)


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
        assert accuracy == 1.0

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
        assert accuracy == 0.8

    def test_top_n_filters_low_actual(self, calculator):
        """Test that players with actual < 3 are excluded."""
        player_data = [
            {'position': 'RB', 'name': 'Player A', 'projected': 30.0, 'actual': 28.0},
            {'position': 'RB', 'name': 'Player B', 'projected': 25.0, 'actual': 2.0},
            {'position': 'RB', 'name': 'Player C', 'projected': 20.0, 'actual': 18.0},
        ]
        accuracy = calculator.calculate_top_n_accuracy(player_data, 2, 'RB')
        assert accuracy == 1.0

    def test_top_n_insufficient_players(self, calculator):
        """Test with fewer players than N returns the np.nan insufficient-data sentinel (D5)."""
        player_data = [
            {'position': 'TE', 'name': 'Player A', 'projected': 30.0, 'actual': 28.0},
            {'position': 'TE', 'name': 'Player B', 'projected': 25.0, 'actual': 22.0},
        ]
        accuracy = calculator.calculate_top_n_accuracy(player_data, 5, 'TE')
        assert np.isnan(accuracy)

    def test_top_n_accuracy_k_dst_small_sample(self, calculator):
        """Test top-N accuracy with K/DST small sample sizes."""
        k_player_data = [
            {'position': 'K', 'name': f'K{i}', 'projected': 10.0 - i, 'actual': 10.0 - i}
            for i in range(10)
        ]
        accuracy_top5 = calculator.calculate_top_n_accuracy(k_player_data, 5, 'K')
        assert accuracy_top5 == 1.0
        assert accuracy_top5 is not None
        assert not (accuracy_top5 != accuracy_top5)

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
        assert abs(corr - 1.0) < 0.01

    def test_spearman_inverse_correlation(self, calculator):
        """Test Spearman with perfect negative correlation."""
        player_data = [
            {'position': 'QB', 'projected': 30.0, 'actual': 12.0},
            {'position': 'QB', 'projected': 25.0, 'actual': 18.0},
            {'position': 'QB', 'projected': 20.0, 'actual': 22.0},
            {'position': 'QB', 'projected': 15.0, 'actual': 28.0},
        ]
        corr = calculator.calculate_spearman_correlation(player_data, 'QB')
        assert abs(corr - (-1.0)) < 0.01

    def test_spearman_zero_variance(self, calculator):
        """Test Spearman returns the np.nan sentinel on zero variance (D5)."""
        player_data = [
            {'position': 'QB', 'projected': 20.0, 'actual': 20.0},
            {'position': 'QB', 'projected': 20.0, 'actual': 20.0},
            {'position': 'QB', 'projected': 20.0, 'actual': 20.0},
        ]
        corr = calculator.calculate_spearman_correlation(player_data, 'QB')
        assert np.isnan(corr)

    def test_spearman_filters_low_actual(self, calculator):
        """Test that players with actual < 3 are excluded."""
        player_data = [
            {'position': 'WR', 'projected': 30.0, 'actual': 28.0},
            {'position': 'WR', 'projected': 25.0, 'actual': 2.0},
            {'position': 'WR', 'projected': 20.0, 'actual': 18.0},
        ]
        corr = calculator.calculate_spearman_correlation(player_data, 'WR')
        assert abs(corr - 1.0) < 0.01

    def test_spearman_insufficient_players(self, calculator):
        """Test with fewer than 2 players returns the np.nan insufficient-data sentinel (D5)."""
        player_data = [
            {'position': 'TE', 'projected': 30.0, 'actual': 28.0},
        ]
        corr = calculator.calculate_spearman_correlation(player_data, 'TE')
        assert np.isnan(corr)

    def test_spearman_correlation_k_dst(self, calculator):
        """Test Spearman correlation with K and DST positions."""
        k_player_data = [
            {'position': 'K', 'projected': 9.0, 'actual': 12.0},
            {'position': 'K', 'projected': 8.0, 'actual': 6.0},
            {'position': 'K', 'projected': 7.0, 'actual': 9.0},
            {'position': 'K', 'projected': 6.0, 'actual': 3.0},
        ]
        corr_k = calculator.calculate_spearman_correlation(k_player_data, 'K')
        assert -1.0 <= corr_k <= 1.0
        assert corr_k is not None
        assert not (corr_k != corr_k)

        dst_player_data = [
            {'position': 'DST', 'projected': 10.0, 'actual': 15.0},
            {'position': 'DST', 'projected': 8.0, 'actual': 5.0},
            {'position': 'DST', 'projected': 6.0, 'actual': 10.0},
            {'position': 'DST', 'projected': 4.0, 'actual': 3.0},
        ]
        corr_dst = calculator.calculate_spearman_correlation(dst_player_data, 'DST')
        assert -1.0 <= corr_dst <= 1.0
        assert corr_dst is not None


class TestRankingMetricsForSeason:
    """Tests for per-metric denominators, genuine-0.0 inclusion, the perfect-week clamp, and no NaN/inf leakage."""

    @pytest.fixture
    def calculator(self):
        """Create AccuracyCalculator instance."""
        return AccuracyCalculator()

    def test_sparse_position_per_metric_denominator_and_zero_valid_week_none(self, calculator):
        """Sparse position: pairwise averages only valid weeks (per-metric denominator, D1);
        a metric with zero valid weeks reports None, not 0.0 (D6, AC1)."""
        # K always has 2 players (valid pairwise/spearman, top-N always <5 -> sentinel).
        # Week 3 has 1 K player -> every metric is the np.nan sentinel and must be excluded.
        player_data_by_week = {
            1: [  # perfect order -> pairwise 1.0 (valid)
                {'position': 'K', 'name': 'K1', 'projected': 9.0, 'actual': 9.0},
                {'position': 'K', 'name': 'K2', 'projected': 6.0, 'actual': 6.0},
            ],
            2: [  # inverse order -> pairwise 0.0 (genuine, valid)
                {'position': 'K', 'name': 'K1', 'projected': 9.0, 'actual': 3.0},
                {'position': 'K', 'name': 'K2', 'projected': 6.0, 'actual': 12.0},
            ],
            3: [  # 1 player -> all metrics np.nan sentinel (must be excluded from denominators)
                {'position': 'K', 'name': 'K1', 'projected': 9.0, 'actual': 9.0},
            ],
        }
        overall, by_position = calculator.calculate_ranking_metrics_for_season(player_data_by_week)

        assert 'K' in by_position
        # (1.0 + 0.0) / 2 valid weeks = 0.5; the 1-player week is excluded.
        # Old shared-week_count dilution would give (1.0 + 0.0 + 0.0) / 3 = 0.333.
        assert by_position['K'].pairwise_accuracy == 0.5
        # top-N never had >=5 K players -> zero valid weeks -> None (not 0.0).
        assert by_position['K'].top_5_accuracy is None
        assert by_position['K'].top_10_accuracy is None
        assert by_position['K'].top_20_accuracy is None

    def test_genuine_zero_spearman_included_sentinel_excluded(self, calculator):
        """A genuine 0.0-correlation week is included in the averaged Spearman (D3);
        a zero-variance sentinel week is excluded (D2, AC2)."""
        week1 = [  # orthogonal ranks -> Spearman exactly 0.0 (genuine)
            {'position': 'QB', 'projected': 10.0, 'actual': 30.0},
            {'position': 'QB', 'projected': 20.0, 'actual': 10.0},
            {'position': 'QB', 'projected': 30.0, 'actual': 40.0},
            {'position': 'QB', 'projected': 40.0, 'actual': 20.0},
        ]
        week2 = [  # Spearman 0.5
            {'position': 'QB', 'projected': 10.0, 'actual': 10.0},
            {'position': 'QB', 'projected': 20.0, 'actual': 40.0},
            {'position': 'QB', 'projected': 30.0, 'actual': 30.0},
        ]
        week3 = [  # zero variance -> np.nan sentinel, must be EXCLUDED
            {'position': 'QB', 'projected': 20.0, 'actual': 20.0},
            {'position': 'QB', 'projected': 20.0, 'actual': 20.0},
            {'position': 'QB', 'projected': 20.0, 'actual': 20.0},
        ]
        overall, by_position = calculator.calculate_ranking_metrics_for_season(
            {1: week1, 2: week2, 3: week3}
        )
        # Fisher-z mean of [arctanh(0.0), arctanh(0.5)] -> tanh(0.27465) ~= 0.2679.
        # If the genuine 0.0 were dropped (old != 0.0 bug) the result would be 0.5;
        # if the zero-variance week were wrongly included as 0.0 it would be ~0.181.
        assert by_position['QB'].spearman_correlation is not None
        assert abs(by_position['QB'].spearman_correlation - 0.2679) < 0.01

    def test_perfect_correlation_week_not_pinned(self, calculator, recwarn):
        """A single perfect-correlation week does not pin the averaged Spearman to exactly 1.0
        and emits no arctanh divide-by-zero RuntimeWarning (D4, AC3, AC6)."""
        player_data_by_week = {
            1: [
                {'position': 'QB', 'projected': 30.0, 'actual': 30.0},
                {'position': 'QB', 'projected': 20.0, 'actual': 20.0},
                {'position': 'QB', 'projected': 10.0, 'actual': 10.0},
            ],
        }
        overall, by_position = calculator.calculate_ranking_metrics_for_season(player_data_by_week)

        spearman = by_position['QB'].spearman_correlation
        assert spearman is not None
        assert np.isfinite(spearman)
        assert 0.99 < spearman < 1.0  # strong but clamped, not pinned to exactly 1.0
        offending = [
            w for w in recwarn
            if 'arctanh' in str(w.message).lower() or 'divide by zero' in str(w.message).lower()
        ]
        assert offending == []

    def test_no_nan_or_inf_leak(self, calculator):
        """No reported metric is NaN or inf under mixed sparse + perfect inputs (AC6)."""
        player_data_by_week = {
            1: [  # perfect QB week
                {'position': 'QB', 'projected': 30.0, 'actual': 30.0},
                {'position': 'QB', 'projected': 20.0, 'actual': 20.0},
                {'position': 'QB', 'projected': 10.0, 'actual': 10.0},
            ],
            2: [  # sparse K week (2 players -> pairwise/spearman valid, top-N sentinel)
                {'position': 'K', 'name': 'K1', 'projected': 9.0, 'actual': 9.0},
                {'position': 'K', 'name': 'K2', 'projected': 6.0, 'actual': 6.0},
            ],
        }
        overall, by_position = calculator.calculate_ranking_metrics_for_season(player_data_by_week)

        all_metrics = [overall] + list(by_position.values())
        for metrics in all_metrics:
            for value in (
                metrics.pairwise_accuracy,
                metrics.top_5_accuracy,
                metrics.top_10_accuracy,
                metrics.top_20_accuracy,
                metrics.spearman_correlation,
            ):
                assert value is None or np.isfinite(value)


class TestAggregateSeasonResultsClamp:
    """Tests that the season-level arctanh sites also clamp perfect correlations (D4)."""

    @pytest.fixture
    def calculator(self):
        """Create AccuracyCalculator instance."""
        return AccuracyCalculator()

    def test_aggregate_season_results_clamps_perfect_spearman(self, calculator):
        """A perfect per-season Spearman does not pin the aggregated Spearman to 1.0
        (clamp applies at aggregate_season_results too) (D4, AC3)."""
        perfect = RankingMetrics(
            pairwise_accuracy=0.70,
            top_5_accuracy=0.80,
            top_10_accuracy=0.75,
            top_20_accuracy=0.70,
            spearman_correlation=1.0,
        )
        season_results = [
            ('2023', AccuracyResult(
                mae=5.0, player_count=100, total_error=500.0,
                overall_metrics=perfect, by_position={'QB': perfect},
            )),
            ('2024', AccuracyResult(
                mae=4.0, player_count=100, total_error=400.0,
                overall_metrics=perfect, by_position={'QB': perfect},
            )),
        ]
        aggregated = calculator.aggregate_season_results(season_results)

        assert aggregated.overall_metrics is not None
        assert aggregated.overall_metrics.spearman_correlation is not None
        assert np.isfinite(aggregated.overall_metrics.spearman_correlation)
        assert 0.99 < aggregated.overall_metrics.spearman_correlation < 1.0
        assert aggregated.by_position['QB'].spearman_correlation < 1.0


# --- AC4 selection-invariance model -----------------------------------------
#
# AC4 asserts the adopted/promoted config is (empirically) unchanged by this
# reporting-correctness fix. The single corrected pairwise feeds BOTH reporting
# and selection: AccuracyConfigPerformance.is_better_than compares the OVERALL
# pairwise (pairwise-only, no MAE), and the overall pairwise is the mean over
# positions of each position's per-position pairwise
# (AccuracyCalculator.calculate_ranking_metrics_for_season: overall
# pairwise = np.mean([m.pairwise_accuracy for ... if not None])).
#
# The D1 fix changes ONLY the per-position pairwise DENOMINATOR:
#   old (buggy): pairwise = sum_over_valid_weeks / W        (shared week_count; sentinel weeks diluted it)
#   new (D1):    pairwise = sum_over_valid_weeks / V_pos    (per-metric valid-week count)
# so new = old * k_pos, where k_pos = W / V_pos >= 1 is config-INDEPENDENT
# (V_pos depends only on the actual>=3.0 qualifying set) but varies BY POSITION.
# Because the overall is a UNIFORM mean across positions, a position-varying
# k_pos is a non-uniform reweighting of the terms the argmax ranks over — which
# is exactly why AC4 is empirically-accepted, not proven. The grounding that the
# real calculator's per-position pairwise IS sum/V_pos is proven by
# TestRankingMetricsForSeason::test_sparse_position_per_metric_denominator_...
# (K: (1.0 + 0.0) / 2 valid weeks = 0.5); these tests model the selection-LEVEL
# effect of that reweighting on the argmax over a set of synthetic configs,
# using the real is_better_than comparator to pick the winner.

W_SEASON = 17  # total weeks in a season = the old shared week_count denominator


def _overall_pairwise(per_position, use_valid_denominator):
    """Overall pairwise = mean over positions of per-position pairwise.

    Mirrors the real selection math: per-position pairwise = pairwise_sum / denom,
    then overall = np.mean over positions (AccuracyCalculator overall build).

    Args:
        per_position: {pos: (pairwise_sum_over_valid_weeks, valid_week_count)}.
        use_valid_denominator: False = old shared W_SEASON denominator (the bug);
            True = new per-position valid_week_count denominator (D1 fix).
    """
    per_pos_pairwise = []
    for pairwise_sum, valid_weeks in per_position.values():
        denom = valid_weeks if use_valid_denominator else W_SEASON
        per_pos_pairwise.append(pairwise_sum / denom)
    return float(np.mean(per_pos_pairwise))


def _select_argmax(config_overall_pairwise):
    """Pick the winning config via the REAL selection comparator.

    Reduces over the configs with AccuracyConfigPerformance.is_better_than
    (pairwise-only), exactly as the tournament selects its adopted config.

    Args:
        config_overall_pairwise: {config_name: overall_pairwise_float}.

    Returns:
        The name of the config is_better_than ranks highest.
    """
    best_name, best_perf = None, None
    for name, pairwise in config_overall_pairwise.items():
        perf = AccuracyConfigPerformance(
            config_dict={}, mae=0.0, player_count=100, total_error=0.0,
            overall_metrics=RankingMetrics(
                pairwise_accuracy=pairwise,
                top_5_accuracy=None,
                top_10_accuracy=None,
                top_20_accuracy=None,
                spearman_correlation=None,
            ),
        )
        if perf.is_better_than(best_perf):
            best_name, best_perf = name, perf
    return best_name


class TestAC4SelectionInvarianceUnderReweighting:
    """AC4: model the D1 per-metric-denominator reweighting's effect on the
    overall-pairwise argmax that drives config selection.

    Selection is empirically-accepted (can flip in theory), so these tests show
    it is PRESERVED in the uniform/near-uniform regime AC4 relies on and identify
    the sparse regime where it CAN flip (making the suite non-vacuous)."""

    def test_uniform_coverage_reweighting_is_identity_selection_preserved(self):
        """(a) Uniform coverage: every position valid in all 17 weeks
        (V_pos == W_SEASON, no pairwise sentinel weeks), so k_pos == 1 and the new
        overall pairwise EQUALS the old for every config. The argmax is therefore
        trivially unchanged. This is the common regime. (AC4)"""
        configs = {
            'A': {'QB': (11.90, 17), 'RB': (10.20, 17), 'WR': (11.05, 17), 'K': (9.35, 17)},
            'B': {'QB': (11.56, 17), 'RB': (10.54, 17), 'WR': (11.22, 17), 'K': (8.50, 17)},
            'C': {'QB': (10.20, 17), 'RB': (10.54, 17), 'WR': (10.37, 17), 'K': (9.86, 17)},
        }
        old = {n: _overall_pairwise(pp, use_valid_denominator=False) for n, pp in configs.items()}
        new = {n: _overall_pairwise(pp, use_valid_denominator=True) for n, pp in configs.items()}

        # Identity: with V_pos == W the reweighting is a no-op for every config.
        for name in configs:
            assert new[name] == pytest.approx(old[name])
        # Selection (via the real is_better_than) is trivially preserved.
        assert _select_argmax(old) == _select_argmax(new)

    def test_near_uniform_sparse_coverage_selection_preserved(self):
        """(b) Realistic near-uniform sparse regime: ONE position (K) misses a few
        weeks to the <2-qualifier pairwise sentinel (V_K = 14 of 17 -> k_K ~= 1.21),
        every other position fully covered. This is the REAL pairwise regime — its
        sentinel needs <2 qualifying players, which is rare — so the reweighting is
        near-identity and the argmax is preserved before vs after the fix. AC4's
        positive evidence. (AC4)"""
        # V_pos is config-INDEPENDENT (the actual>=3.0 qualifying set is shared),
        # so the denominators are the same across configs; only the sums differ.
        valid_weeks = {'QB': 17, 'RB': 17, 'WR': 17, 'K': 14}
        old_per_position_pairwise = {
            'A': {'QB': 0.72, 'RB': 0.70, 'WR': 0.71, 'K': 0.60},
            'B': {'QB': 0.66, 'RB': 0.64, 'WR': 0.65, 'K': 0.62},
            'C': {'QB': 0.60, 'RB': 0.62, 'WR': 0.61, 'K': 0.58},
        }
        # sum = old_pairwise * W_SEASON; new pairwise = sum / V_pos (<= 1.0 here).
        configs = {
            name: {pos: (pp * W_SEASON, valid_weeks[pos]) for pos, pp in per_pos.items()}
            for name, per_pos in old_per_position_pairwise.items()
        }
        old = {n: _overall_pairwise(pp, use_valid_denominator=False) for n, pp in configs.items()}
        new = {n: _overall_pairwise(pp, use_valid_denominator=True) for n, pp in configs.items()}

        # A leads on the dense positions; the modest K up-weight (k ~= 1.21) does
        # not overcome that lead, so selection is preserved.
        assert _select_argmax(old) == 'A'
        assert _select_argmax(new) == 'A'
        assert _select_argmax(old) == _select_argmax(new)

    def test_pathological_sparse_coverage_can_flip_selection(self):
        """(c) Adversarial / documented: a selection-relevant position (K) with HEAVY
        sentinel coverage (valid only 5 of 17 weeks -> k_K = 3.4) is up-weighted so
        much by D1 that the adopted config FLIPS. This proves the suite is
        non-vacuous and documents exactly why AC4 is empirically-accepted, not
        proven: the D1 reweighting is position-non-uniform and CAN move the argmax
        when a selection-relevant position is heavily sparse. Mirrors the
        context.md AC4 reweighting analysis (QB-vs-sparse-K counterexample). (AC4)"""
        # k_QB = 17/17 = 1 (dense); k_K = 17/5 = 3.4 (heavily sparse).
        # A leads on the dense QB by sum +3; B leads on the sparse K by sum +2.
        configs = {
            'A': {'QB': (12.0, 17), 'K': (1.0, 5)},
            'B': {'QB': (9.0, 17), 'K': (3.0, 5)},
        }
        old = {n: _overall_pairwise(pp, use_valid_denominator=False) for n, pp in configs.items()}
        new = {n: _overall_pairwise(pp, use_valid_denominator=True) for n, pp in configs.items()}

        # Old (diluted) selects A; the D1 fix up-weights the sparse K enough that B
        # now wins -> a genuine selection flip (the empirical-accept risk realized).
        assert _select_argmax(old) == 'A'
        assert _select_argmax(new) == 'B'
        assert _select_argmax(old) != _select_argmax(new)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


