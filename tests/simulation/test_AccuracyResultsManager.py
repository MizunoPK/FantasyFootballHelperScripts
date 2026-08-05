"""
Tests for AccuracyResultsManager

Tests results tracking and storage for accuracy simulation.

Author: Kai Mizuno
"""

import json
import pytest
from pathlib import Path
from unittest.mock import Mock, patch
import tempfile
import shutil

from simulation.accuracy.AccuracyResultsManager import (
    AccuracyResultsManager,
    AccuracyConfigPerformance,
    RankingMetrics,
    WEEK_RANGES,
    propagate_to_configs,
    _min_season_wins,
)
from simulation.accuracy.AccuracyCalculator import AccuracyResult
from simulation.shared.config_constants import BASE_CONFIG_PARAMS, WEEK_SPECIFIC_PARAMS
from utils.error_handler import FileOperationError


class TestAccuracyConfigPerformance:
    """Tests for AccuracyConfigPerformance class."""

    def test_config_performance_creation(self):
        """Test creating a config performance record."""
        config = {'test': 'config'}
        perf = AccuracyConfigPerformance(
            config_dict=config,
            mae=5.5,
            player_count=100,
            total_error=550.0
        )

        assert perf.config_dict == config
        assert perf.mae == 5.5
        assert perf.player_count == 100
        assert perf.total_error == 550.0
        assert perf.config_value is None
        assert perf.timestamp is not None

    def test_config_performance_with_value(self):
        """Test creating with explicit config_value."""
        perf = AccuracyConfigPerformance(
            config_dict={},
            mae=5.0,
            player_count=100,
            total_error=500.0,
            config_value=2.5
        )

        assert perf.config_value == 2.5

    def test_config_value_extraction_nested_params(self):
        """Test that config_value is extracted from nested parameters."""
        config = {
            'parameters': {
                'WIND_SCORING': {
                    'WEIGHT': 0.25,
                    'IMPACT_SCALE': 100
                }
            }
        }
        perf = AccuracyConfigPerformance(
            config_dict=config,
            mae=5.0,
            player_count=100,
            total_error=500.0,
            param_name='WIND_SCORING_WEIGHT'
        )
        assert perf.config_value == 0.25

        config2 = {
            'parameters': {
                'LOCATION_MODIFIERS': {
                    'HOME': 4.3,
                    'AWAY': 3.9,
                    'INTERNATIONAL': -2.0
                }
            }
        }
        perf2 = AccuracyConfigPerformance(
            config_dict=config2,
            mae=5.0,
            player_count=100,
            total_error=500.0,
            param_name='LOCATION_AWAY'
        )
        assert perf2.config_value == 3.9

        config3 = {
            'parameters': {
                'NORMALIZATION_MAX_SCALE': 150
            }
        }
        perf3 = AccuracyConfigPerformance(
            config_dict=config3,
            mae=5.0,
            player_count=100,
            total_error=500.0,
            param_name='NORMALIZATION_MAX_SCALE'
        )
        assert perf3.config_value == 150

    def test_is_better_than_higher_pairwise_accuracy(self):
        """Test that higher pairwise accuracy is better."""
        metrics1 = RankingMetrics(
            pairwise_accuracy=0.70,
            top_5_accuracy=0.80,
            top_10_accuracy=0.75,
            top_20_accuracy=0.70,
            spearman_correlation=0.82
        )
        metrics2 = RankingMetrics(
            pairwise_accuracy=0.65,
            top_5_accuracy=0.80,
            top_10_accuracy=0.75,
            top_20_accuracy=0.70,
            spearman_correlation=0.82
        )

        perf1 = AccuracyConfigPerformance(
            config_dict={}, mae=4.0, player_count=100, total_error=400.0,
            overall_metrics=metrics1
        )
        perf2 = AccuracyConfigPerformance(
            config_dict={}, mae=5.0, player_count=100, total_error=500.0,
            overall_metrics=metrics2
        )

        assert perf1.is_better_than(perf2)
        assert not perf2.is_better_than(perf1)

    def test_is_better_than_none(self):
        """Test comparison with None."""
        metrics = RankingMetrics(
            pairwise_accuracy=0.68,
            top_5_accuracy=0.80,
            top_10_accuracy=0.75,
            top_20_accuracy=0.70,
            spearman_correlation=0.82
        )

        perf = AccuracyConfigPerformance(
            config_dict={}, mae=5.0, player_count=100, total_error=500.0,
            overall_metrics=metrics
        )

        assert perf.is_better_than(None)

    def test_is_better_than_equal_mae(self):
        """Test that equal MAE is not better (first wins ties)."""
        perf1 = AccuracyConfigPerformance(
            config_dict={}, mae=5.0, player_count=100, total_error=500.0
        )
        perf2 = AccuracyConfigPerformance(
            config_dict={}, mae=5.0, player_count=100, total_error=500.0
        )

        assert not perf1.is_better_than(perf2)
        assert not perf2.is_better_than(perf1)

    def test_is_better_than_self_pairwise_none_not_better(self):
        """AC1: self has non-None overall_metrics but pairwise_accuracy is None
        (no usable primary metric) -> not better, and no TypeError raised."""
        self_metrics = RankingMetrics(
            pairwise_accuracy=None,
            top_5_accuracy=0.80,
            top_10_accuracy=0.75,
            top_20_accuracy=0.70,
            spearman_correlation=0.82
        )
        other_metrics = RankingMetrics(
            pairwise_accuracy=0.65,
            top_5_accuracy=0.80,
            top_10_accuracy=0.75,
            top_20_accuracy=0.70,
            spearman_correlation=0.82
        )
        perf_self = AccuracyConfigPerformance(
            config_dict={}, mae=4.0, player_count=100, total_error=400.0,
            overall_metrics=self_metrics
        )
        perf_other = AccuracyConfigPerformance(
            config_dict={}, mae=5.0, player_count=100, total_error=500.0,
            overall_metrics=other_metrics
        )

        assert perf_self.is_better_than(perf_other) is False

    def test_is_better_than_other_pairwise_none_self_wins(self):
        """AC1: other has non-None overall_metrics but pairwise_accuracy is None
        while self has a usable pairwise value -> this config wins, no TypeError."""
        self_metrics = RankingMetrics(
            pairwise_accuracy=0.65,
            top_5_accuracy=0.80,
            top_10_accuracy=0.75,
            top_20_accuracy=0.70,
            spearman_correlation=0.82
        )
        other_metrics = RankingMetrics(
            pairwise_accuracy=None,
            top_5_accuracy=0.80,
            top_10_accuracy=0.75,
            top_20_accuracy=0.70,
            spearman_correlation=0.82
        )
        perf_self = AccuracyConfigPerformance(
            config_dict={}, mae=4.0, player_count=100, total_error=400.0,
            overall_metrics=self_metrics
        )
        perf_other = AccuracyConfigPerformance(
            config_dict={}, mae=5.0, player_count=100, total_error=500.0,
            overall_metrics=other_metrics
        )

        assert perf_self.is_better_than(perf_other) is True

    def test_is_better_than_both_pairwise_none_not_better(self):
        """AC1: both operands have non-None overall_metrics with pairwise_accuracy
        is None -> False via the self-first check, no TypeError."""
        both_metrics_self = RankingMetrics(
            pairwise_accuracy=None,
            top_5_accuracy=0.80,
            top_10_accuracy=0.75,
            top_20_accuracy=0.70,
            spearman_correlation=0.82
        )
        both_metrics_other = RankingMetrics(
            pairwise_accuracy=None,
            top_5_accuracy=0.85,
            top_10_accuracy=0.80,
            top_20_accuracy=0.75,
            spearman_correlation=0.85
        )
        perf_self = AccuracyConfigPerformance(
            config_dict={}, mae=4.0, player_count=100, total_error=400.0,
            overall_metrics=both_metrics_self
        )
        perf_other = AccuracyConfigPerformance(
            config_dict={}, mae=5.0, player_count=100, total_error=500.0,
            overall_metrics=both_metrics_other
        )

        assert perf_self.is_better_than(perf_other) is False

    def test_to_dict_from_dict_roundtrip(self):
        """Test serialization roundtrip."""
        config = {'param1': 'value1'}
        original = AccuracyConfigPerformance(
            config_dict=config,
            mae=5.5,
            player_count=100,
            total_error=550.0,
            config_value=1.25
        )

        data = original.to_dict()
        restored = AccuracyConfigPerformance.from_dict(data)

        assert restored.config_dict == original.config_dict
        assert restored.mae == original.mae
        assert restored.player_count == original.player_count
        assert restored.config_value == original.config_value

    def test_repr(self):
        """Test string representation."""
        perf = AccuracyConfigPerformance(
            config_dict={}, mae=5.5, player_count=100, total_error=550.0
        )
        repr_str = repr(perf)

        assert "mae=5.5000" in repr_str
        assert "players=100" in repr_str


class TestAccuracyResultsManager:
    """Tests for AccuracyResultsManager class."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests."""
        temp = tempfile.mkdtemp(prefix="accuracy_test_")
        yield Path(temp)
        shutil.rmtree(temp, ignore_errors=True)

    @pytest.fixture
    def mock_baseline(self, temp_dir):
        """Create mock baseline config folder with required files."""
        baseline = temp_dir / "baseline"
        baseline.mkdir()
        league_config = {
            'config_name': 'Test Baseline',
            'description': 'Test baseline config',
            'parameters': {'PARAM1': 'value1'}
        }
        with open(baseline / "league_config.json", 'w') as f:
            json.dump(league_config, f)
        for filename in ['week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']:
            week_config = {
                'config_name': f'Test {filename}',
                'description': 'Test config',
                'parameters': {'WEEK_PARAM': 1}
            }
            with open(baseline / filename, 'w') as f:
                json.dump(week_config, f)
        return baseline

    @pytest.fixture
    def results_manager(self, temp_dir, mock_baseline):
        """Create AccuracyResultsManager instance."""
        output_dir = temp_dir / "output"
        return AccuracyResultsManager(output_dir, mock_baseline)

    def test_initialization(self, temp_dir, mock_baseline):
        """Test AccuracyResultsManager initialization."""
        output_dir = temp_dir / "output"
        manager = AccuracyResultsManager(output_dir, mock_baseline)

        assert manager.output_dir == output_dir
        assert manager.baseline_config_path == mock_baseline
        assert 'week_1_5' in manager.best_configs
        assert 'week_6_9' in manager.best_configs
        assert manager.best_configs['week_1_5'] is None

    def test_add_result_first_is_best(self, results_manager):
        """Test that first result is automatically best."""
        config = {'test': 'config'}
        metrics = RankingMetrics(
            pairwise_accuracy=0.68,
            top_5_accuracy=0.80,
            top_10_accuracy=0.75,
            top_20_accuracy=0.70,
            spearman_correlation=0.82
        )
        accuracy_result = AccuracyResult(
            mae=5.0, player_count=100, total_error=500.0,
            overall_metrics=metrics
        )

        is_best = results_manager.add_result('ros', config, accuracy_result)

        assert is_best
        assert results_manager.best_configs['ros'] is not None
        assert results_manager.best_configs['ros'].mae == 5.0

    def test_add_result_better_replaces(self, results_manager):
        """Test that better result replaces current best."""
        config1 = {'version': 1}
        config2 = {'version': 2}

        metrics1 = RankingMetrics(
            pairwise_accuracy=0.65,
            top_5_accuracy=0.80,
            top_10_accuracy=0.75,
            top_20_accuracy=0.70,
            spearman_correlation=0.82
        )
        metrics2 = RankingMetrics(
            pairwise_accuracy=0.70,
            top_5_accuracy=0.80,
            top_10_accuracy=0.75,
            top_20_accuracy=0.70,
            spearman_correlation=0.82
        )

        result1 = AccuracyResult(
            mae=5.0, player_count=100, total_error=500.0,
            overall_metrics=metrics1
        )
        result2 = AccuracyResult(
            mae=3.0, player_count=100, total_error=300.0,
            overall_metrics=metrics2
        )

        results_manager.add_result('ros', config1, result1)
        is_best = results_manager.add_result('ros', config2, result2)

        assert is_best
        assert results_manager.best_configs['ros'].overall_metrics.pairwise_accuracy == 0.70
        assert results_manager.best_configs['ros'].config_dict == config2

    def test_add_result_worse_does_not_replace(self, results_manager):
        """Test that worse result does not replace best."""
        config1 = {'version': 1}
        config2 = {'version': 2}
        metrics1 = RankingMetrics(
            pairwise_accuracy=0.70,
            top_5_accuracy=0.80,
            top_10_accuracy=0.75,
            top_20_accuracy=0.70,
            spearman_correlation=0.82
        )
        metrics2 = RankingMetrics(
            pairwise_accuracy=0.65,
            top_5_accuracy=0.80,
            top_10_accuracy=0.75,
            top_20_accuracy=0.70,
            spearman_correlation=0.82
        )
        result1 = AccuracyResult(
            mae=3.0, player_count=100, total_error=300.0,
            overall_metrics=metrics1
        )
        result2 = AccuracyResult(
            mae=5.0, player_count=100, total_error=500.0,
            overall_metrics=metrics2
        )

        results_manager.add_result('ros', config1, result1)
        is_best = results_manager.add_result('ros', config2, result2)

        assert not is_best
        assert results_manager.best_configs['ros'].config_dict == config1

    def test_add_result_tracks_all(self, results_manager):
        """Test that all results are tracked."""
        for i in range(3):
            config = {'version': i}
            result = AccuracyResult(mae=5.0 - i, player_count=100, total_error=500.0)
            results_manager.add_result('ros', config, result)

        assert len(results_manager.all_results) == 3

    def test_get_best_config(self, results_manager):
        """Test getting best config for a week range."""
        config = {'test': 'config'}
        metrics = RankingMetrics(
            pairwise_accuracy=0.68,
            top_5_accuracy=0.80,
            top_10_accuracy=0.75,
            top_20_accuracy=0.70,
            spearman_correlation=0.82
        )
        result = AccuracyResult(
            mae=5.0, player_count=100, total_error=500.0,
            overall_metrics=metrics
        )
        results_manager.add_result('week_1_5', config, result)

        best = results_manager.get_best_config('week_1_5')

        assert best is not None
        assert best.mae == 5.0

    def test_get_best_config_not_found(self, results_manager):
        """Test getting best config when none exists."""
        best = results_manager.get_best_config('week_1_5')
        assert best is None

    def test_save_optimal_configs_filters_week_owned_keys_from_league_config(self, temp_dir):
        """T90 AC2: a new optimal folder is born clean even from an INFLATED baseline."""
        # Arrange - a --baseline folder whose league_config carries week-owned keys.
        baseline = temp_dir / "inflated_baseline"
        baseline.mkdir()
        inflated = {
            'config_name': 'Inflated Baseline',
            'description': 'Reproduces the pre-T90 20-key shape',
            'parameters': {
                'CURRENT_NFL_WEEK': 15,
                'ADP_SCORING': {'WEIGHT': 1.5},
                'PLAYER_RATING_SCORING': {'WEIGHT': 1.8},
                'TEAM_QUALITY_SCORING': {'WEIGHT': 2.77},
                'PERFORMANCE_SCORING': {'WEIGHT': 3.55},
                'MATCHUP_SCORING': {'WEIGHT': 1.62},
                'SCHEDULE_SCORING': {'WEIGHT': 0.9},
                'TEMPERATURE_SCORING': {'WEIGHT': 0.81},
                'WIND_SCORING': {'WEIGHT': 1.23},
                'NOT_A_REAL_PARAM': 1,
            }
        }
        with open(baseline / "league_config.json", 'w') as f:
            json.dump(inflated, f)
        manager = AccuracyResultsManager(temp_dir / "inflated_output", baseline)

        # Act
        optimal_path = manager.save_optimal_configs()

        # Assert
        with open(optimal_path / "league_config.json") as f:
            written = set(json.load(f)['parameters'].keys())
        assert written & set(WEEK_SPECIFIC_PARAMS) == set(), \
            f"week-owned keys leaked into the optimal base config: {sorted(written & set(WEEK_SPECIFIC_PARAMS))}"
        assert written <= set(BASE_CONFIG_PARAMS), \
            f"non-base keys leaked into the optimal base config: {sorted(written - set(BASE_CONFIG_PARAMS))}"

    def test_save_optimal_configs_missing_baseline_league_config_warns_and_skips(self, temp_dir):
        """T90 AC2 second arm: a missing baseline league_config still warns and writes nothing."""
        # Arrange
        baseline = temp_dir / "no_league_baseline"
        baseline.mkdir()
        manager = AccuracyResultsManager(temp_dir / "no_league_output", baseline)
        manager.logger = Mock()

        # Act
        optimal_path = manager.save_optimal_configs()

        # Assert
        assert not (optimal_path / "league_config.json").exists()
        assert any('No league_config.json found in baseline' in str(c)
                   for c in manager.logger.warning.call_args_list), \
            "the existing missing-baseline warning must still be logged"

    def test_save_optimal_configs(self, results_manager):
        """Test saving optimal configs to folder."""
        config_week_1_5 = {'TEAM_QUALITY_SCORING': {'WEIGHT': 1.5}}
        config_week_6_9 = {'MATCHUP_SCORING': {'WEIGHT': 1.2}}
        metrics = RankingMetrics(
            pairwise_accuracy=0.68,
            top_5_accuracy=0.80,
            top_10_accuracy=0.75,
            top_20_accuracy=0.70,
            spearman_correlation=0.82
        )
        result = AccuracyResult(
            mae=5.0, player_count=100, total_error=500.0,
            overall_metrics=metrics
        )

        results_manager.add_result('week_1_5', config_week_1_5, result)
        results_manager.add_result('week_6_9', config_week_6_9, result)

        optimal_path = results_manager.save_optimal_configs()

        assert optimal_path.exists()
        assert optimal_path.name.startswith("accuracy_optimal_")

        assert (optimal_path / "league_config.json").exists()
        assert (optimal_path / "week1-5.json").exists()
        assert (optimal_path / "week6-9.json").exists()
        assert (optimal_path / "week10-13.json").exists()
        assert (optimal_path / "week14-17.json").exists()

        with open(optimal_path / "week1-5.json") as f:
            saved_config = json.load(f)
        assert 'config_name' in saved_config
        assert 'description' in saved_config
        assert 'parameters' in saved_config
        assert 'TEAM_QUALITY_SCORING' in saved_config['parameters']
        assert saved_config['parameters']['TEAM_QUALITY_SCORING']['WEIGHT'] == 1.5
        assert 'performance_metrics' in saved_config
        assert saved_config['performance_metrics']['mae'] == 5.0

    def test_add_result_threads_coverage(self, results_manager):
        """add_result copies weeks_evaluated/weeks_requested from the
        AccuracyResult into the stored AccuracyConfigPerformance (D4)."""
        metrics = RankingMetrics(pairwise_accuracy=0.70, top_5_accuracy=0.80,
                                 top_10_accuracy=0.75, top_20_accuracy=0.70,
                                 spearman_correlation=0.82)
        result = AccuracyResult(mae=5.0, player_count=100, total_error=500.0,
                                weeks_evaluated=18, weeks_requested=20,
                                overall_metrics=metrics)
        results_manager.add_result('week_1_5', {'test': 'config'}, result)
        best = results_manager.best_configs['week_1_5']
        assert best.weeks_evaluated == 18
        assert best.weeks_requested == 20

    def test_save_optimal_configs_includes_coverage(self, results_manager):
        """save_optimal_configs writes the coverage pair into
        performance_metrics (D5)."""
        metrics = RankingMetrics(pairwise_accuracy=0.70, top_5_accuracy=0.80,
                                 top_10_accuracy=0.75, top_20_accuracy=0.70,
                                 spearman_correlation=0.82)
        result = AccuracyResult(mae=5.0, player_count=100, total_error=500.0,
                                weeks_evaluated=19, weeks_requested=20,
                                overall_metrics=metrics)
        results_manager.add_result('week_1_5', {'X': 1}, result)
        optimal_path = results_manager.save_optimal_configs()
        with open(optimal_path / "week1-5.json") as f:
            saved = json.load(f)
        assert saved['performance_metrics']['weeks_evaluated'] == 19
        assert saved['performance_metrics']['weeks_requested'] == 20

    def test_intermediate_resume_roundtrips_coverage(self, results_manager, mock_baseline, temp_dir):
        """save_intermediate_results writes the pair and load_intermediate_results
        reconstructs it — a resumed run reports real coverage, not 0/0 (D4)."""
        metrics = RankingMetrics(pairwise_accuracy=0.70, top_5_accuracy=0.80,
                                 top_10_accuracy=0.75, top_20_accuracy=0.70,
                                 spearman_correlation=0.82)
        result = AccuracyResult(mae=5.0, player_count=100, total_error=500.0,
                                weeks_evaluated=19, weeks_requested=20,
                                overall_metrics=metrics)
        results_manager.add_result('week_1_5', {'test': 'config'}, result)

        intermediate_path = results_manager.save_intermediate_results(0, 'NORMALIZATION')

        with open(intermediate_path / "week1-5.json") as f:
            saved = json.load(f)
        assert saved['performance_metrics']['weeks_evaluated'] == 19
        assert saved['performance_metrics']['weeks_requested'] == 20

        fresh = AccuracyResultsManager(temp_dir / "resumed_output", mock_baseline)
        fresh.load_intermediate_results(intermediate_path)
        reconstructed = fresh.best_configs['week_1_5']
        assert reconstructed is not None
        assert reconstructed.weeks_evaluated == 19
        assert reconstructed.weeks_requested == 20

    def test_is_better_than_ignores_coverage(self):
        """AC4: coverage is never read by selection. Equal pairwise compares
        symmetrically despite very different coverage, and a higher-pairwise
        config wins even with worse coverage."""
        metrics = RankingMetrics(pairwise_accuracy=0.70, top_5_accuracy=0.80,
                                 top_10_accuracy=0.75, top_20_accuracy=0.70,
                                 spearman_correlation=0.82)
        full = AccuracyConfigPerformance(config_dict={'v': 1}, mae=5.0,
                                         player_count=100, total_error=500.0,
                                         overall_metrics=metrics,
                                         weeks_evaluated=20, weeks_requested=20)
        partial = AccuracyConfigPerformance(config_dict={'v': 2}, mae=5.0,
                                            player_count=100, total_error=500.0,
                                            overall_metrics=metrics,
                                            weeks_evaluated=15, weeks_requested=20)
        assert full.is_better_than(partial) == partial.is_better_than(full)

        better_partial = AccuracyConfigPerformance(
            config_dict={'v': 3}, mae=5.0, player_count=100, total_error=500.0,
            overall_metrics=RankingMetrics(pairwise_accuracy=0.90,
                top_5_accuracy=0.80, top_10_accuracy=0.75, top_20_accuracy=0.70,
                spearman_correlation=0.82),
            weeks_evaluated=10, weeks_requested=20)
        assert better_partial.is_better_than(full)

    def test_save_intermediate_results(self, results_manager):
        """Test saving intermediate results."""
        config = {'test': 'config'}
        metrics = RankingMetrics(
            pairwise_accuracy=0.68,
            top_5_accuracy=0.80,
            top_10_accuracy=0.75,
            top_20_accuracy=0.70,
            spearman_correlation=0.82
        )
        result = AccuracyResult(
            mae=5.0, player_count=100, total_error=500.0,
            overall_metrics=metrics
        )
        results_manager.add_result('ros', config, result)

        intermediate_path = results_manager.save_intermediate_results(0, 'NORMALIZATION')

        assert intermediate_path.exists()
        assert "accuracy_intermediate_00_NORMALIZATION" in intermediate_path.name
        assert (intermediate_path / "league_config.json").exists()
        assert (intermediate_path / "week1-5.json").exists()
        assert (intermediate_path / "week6-9.json").exists()
        assert (intermediate_path / "week10-13.json").exists()
        assert (intermediate_path / "week14-17.json").exists()
        assert (intermediate_path / "metadata.json").exists()
        # T69/D5: the folder now also carries _ascent_state.json (pass index + frozen
        # horizons), so the resume record is a single self-describing artifact rather than
        # state kept somewhere else. Asserted by NAME as well as count, so a future stray
        # file cannot satisfy the count while the real one is missing.
        assert (intermediate_path / "_ascent_state.json").exists()
        all_files = list(intermediate_path.glob("*.json"))
        assert len(all_files) == 7, sorted(f.name for f in all_files)

    def test_load_intermediate_results(self, results_manager, temp_dir):
        """Test that loading fully reconstructs best_configs for optimized horizons
        and leaves baseline-only horizons as None (D2)."""
        intermediate_path = temp_dir / "accuracy_intermediate_00_TEST"
        intermediate_path.mkdir()

        league_config = {
            'config_name': 'League',
            'description': 'league base',
            'parameters': {'BASE_PARAM': 1}
        }
        with open(intermediate_path / "league_config.json", 'w') as f:
            json.dump(league_config, f)

        optimized = {
            'config_name': 'Optimized week1-5',
            'description': 'optimized',
            'parameters': {'WEEK_PARAM': 2},
            'performance_metrics': {
                'mae': 5.0,
                'player_count': 100,
                'config_value': 2.5,
                'ranking_metrics': {
                    'pairwise_accuracy': 0.68,
                    'top_5_accuracy': 0.80,
                    'top_10_accuracy': 0.75,
                    'top_20_accuracy': 0.70,
                    'spearman_correlation': 0.82,
                    'by_position': {
                        'QB': {
                            'pairwise_accuracy': 0.70,
                            'top_5_accuracy': 0.60,
                            'top_10_accuracy': 0.65,
                            'top_20_accuracy': 0.55,
                            'spearman_correlation': 0.50
                        }
                    }
                }
            }
        }
        with open(intermediate_path / "week1-5.json", 'w') as f:
            json.dump(optimized, f)

        baseline_only = {
            'config_name': 'Baseline horizon',
            'description': 'from baseline (no optimization yet)',
            'parameters': {'WEEK_PARAM': 1},
            'performance_metrics': {
                'mae': None,
                'player_count': None,
                'total_error': None,
                'config_value': None
            }
        }
        for filename in ['week6-9.json', 'week10-13.json', 'week14-17.json']:
            with open(intermediate_path / filename, 'w') as f:
                json.dump(baseline_only, f)

        metadata = {
            'best_mae_per_horizon': {
                'week_1_5': {'mae': 5.0, 'test_idx': 3},
                'week_6_9': {'mae': None, 'test_idx': -1},
                'week_10_13': {'mae': None, 'test_idx': -1},
                'week_14_17': {'mae': None, 'test_idx': -1}
            }
        }
        with open(intermediate_path / "metadata.json", 'w') as f:
            json.dump(metadata, f)

        success = results_manager.load_intermediate_results(intermediate_path)

        assert success
        reconstructed = results_manager.best_configs['week_1_5']
        assert reconstructed is not None
        assert reconstructed.mae == 5.0
        assert reconstructed.player_count == 100
        assert reconstructed.config_value == 2.5
        assert reconstructed.total_error == 500.0
        assert reconstructed.overall_metrics is not None
        assert reconstructed.overall_metrics.pairwise_accuracy == 0.68
        assert reconstructed.by_position['QB'].pairwise_accuracy == 0.70
        assert reconstructed.test_idx == 3
        assert 'parameters' in reconstructed.config_dict
        assert results_manager.best_configs['week_6_9'] is None

    def test_resume_null_pairwise_then_add_result_selects(self, results_manager, temp_dir):
        """AC3: a resume reading a week file whose ranking_metrics.pairwise_accuracy
        is null reconstructs a None-pairwise incumbent; a subsequent add_result with a
        usable pairwise value completes and selects it instead of raising TypeError."""
        intermediate_path = temp_dir / "accuracy_intermediate_00_TEST"
        intermediate_path.mkdir()

        league_config = {
            'config_name': 'League',
            'description': 'league base',
            'parameters': {'BASE_PARAM': 1}
        }
        with open(intermediate_path / "league_config.json", 'w') as f:
            json.dump(league_config, f)

        null_pairwise = {
            'config_name': 'Optimized week1-5',
            'description': 'usable spearman/top-N but no pairwise samples',
            'parameters': {'WEEK_PARAM': 2},
            'performance_metrics': {
                'mae': 5.0,
                'player_count': 100,
                'config_value': 2.5,
                'ranking_metrics': {
                    'pairwise_accuracy': None,
                    'top_5_accuracy': 0.80,
                    'top_10_accuracy': 0.75,
                    'top_20_accuracy': 0.70,
                    'spearman_correlation': 0.82
                }
            }
        }
        with open(intermediate_path / "week1-5.json", 'w') as f:
            json.dump(null_pairwise, f)

        baseline_only = {
            'config_name': 'Baseline horizon',
            'description': 'from baseline (no optimization yet)',
            'parameters': {'WEEK_PARAM': 1},
            'performance_metrics': {
                'mae': None,
                'player_count': None,
                'total_error': None,
                'config_value': None
            }
        }
        for filename in ['week6-9.json', 'week10-13.json', 'week14-17.json']:
            with open(intermediate_path / filename, 'w') as f:
                json.dump(baseline_only, f)

        metadata = {
            'best_mae_per_horizon': {
                'week_1_5': {'mae': 5.0, 'test_idx': 3},
                'week_6_9': {'mae': None, 'test_idx': -1},
                'week_10_13': {'mae': None, 'test_idx': -1},
                'week_14_17': {'mae': None, 'test_idx': -1}
            }
        }
        with open(intermediate_path / "metadata.json", 'w') as f:
            json.dump(metadata, f)

        assert results_manager.load_intermediate_results(intermediate_path)
        incumbent = results_manager.best_configs['week_1_5']
        assert incumbent is not None
        assert incumbent.overall_metrics is not None
        assert incumbent.overall_metrics.pairwise_accuracy is None

        new_metrics = RankingMetrics(
            pairwise_accuracy=0.68,
            top_5_accuracy=0.80,
            top_10_accuracy=0.75,
            top_20_accuracy=0.70,
            spearman_correlation=0.82
        )
        new_result = AccuracyResult(
            mae=4.0, player_count=100, total_error=400.0,
            overall_metrics=new_metrics
        )

        is_best = results_manager.add_result('week_1_5', {'test': 'config'}, new_result)

        assert is_best is True
        assert results_manager.best_configs['week_1_5'].overall_metrics.pairwise_accuracy == 0.68

    def test_load_intermediate_results_not_found(self, results_manager, temp_dir):
        """Test loading from non-existent folder."""
        success = results_manager.load_intermediate_results(temp_dir / "nonexistent")
        assert not success

    def test_load_intermediate_results_incomplete_folder(self, results_manager, temp_dir):
        """S2: an incomplete intermediate folder (missing required files) is handled
        gracefully — load returns False (not a raised ValueError) and best_configs
        is left untouched."""
        incomplete = temp_dir / "accuracy_intermediate_00_TEST"
        incomplete.mkdir()
        # Only league_config.json present; the 4 week files are missing, so
        # ConfigGenerator.load_baseline_from_folder would raise — S2 catches it.
        with open(incomplete / "league_config.json", 'w') as f:
            json.dump({'config_name': 'partial'}, f)

        success = results_manager.load_intermediate_results(incomplete)

        assert success is False
        assert all(v is None for v in results_manager.best_configs.values())

    def test_get_summary(self, results_manager):
        """Test getting results summary."""
        config = {'test': 'config'}
        metrics = RankingMetrics(
            pairwise_accuracy=0.68,
            top_5_accuracy=0.80,
            top_10_accuracy=0.75,
            top_20_accuracy=0.70,
            spearman_correlation=0.82
        )
        result = AccuracyResult(
            mae=5.0, player_count=100, total_error=500.0,
            overall_metrics=metrics
        )
        results_manager.add_result('ros', config, result)
        results_manager.add_result('week_1_5', config, result)

        summary = results_manager.get_summary()

        assert "Accuracy Simulation Results" in summary
        assert "ros:" in summary
        assert "MAE=5.0000" in summary
        assert "100 players" in summary

    def test_horizons_have_independent_configs(self, results_manager):
        """Test that different horizons store independent config objects (regression test for bug)."""
        config1 = {'parameters': {'NORMALIZATION_MAX_SCALE': 100}}
        config2 = {'parameters': {'NORMALIZATION_MAX_SCALE': 150}}
        metrics1 = RankingMetrics(
            pairwise_accuracy=0.65,
            top_5_accuracy=0.80,
            top_10_accuracy=0.75,
            top_20_accuracy=0.70,
            spearman_correlation=0.82
        )
        metrics2 = RankingMetrics(
            pairwise_accuracy=0.72,
            top_5_accuracy=0.80,
            top_10_accuracy=0.75,
            top_20_accuracy=0.70,
            spearman_correlation=0.82
        )
        result1 = AccuracyResult(
            mae=68.0, player_count=100, total_error=6800.0,
            overall_metrics=metrics1
        )
        result2 = AccuracyResult(
            mae=3.8, player_count=100, total_error=380.0,
            overall_metrics=metrics2
        )

        results_manager.add_result('ros', config1, result1)
        results_manager.add_result('week_1_5', config2, result2)

        ros_config = results_manager.best_configs['ros'].config_dict
        week_config = results_manager.best_configs['week_1_5'].config_dict

        assert ros_config['parameters']['NORMALIZATION_MAX_SCALE'] == 100
        assert week_config['parameters']['NORMALIZATION_MAX_SCALE'] == 150

        ros_config['parameters']['NORMALIZATION_MAX_SCALE'] = 200
        assert week_config['parameters']['NORMALIZATION_MAX_SCALE'] == 150


class TestScheduleSync:
    """Tests for SCHEDULE parameter sync with MATCHUP."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests."""
        temp = tempfile.mkdtemp(prefix="accuracy_test_")
        yield Path(temp)
        shutil.rmtree(temp, ignore_errors=True)

    @pytest.fixture
    def mock_baseline(self, temp_dir):
        """Create mock baseline config folder."""
        baseline = temp_dir / "baseline"
        baseline.mkdir()
        for filename in ['league_config.json', 'week1-5.json',
                        'week6-9.json', 'week10-13.json', 'week14-17.json']:
            config = {'config_name': f'Test {filename}', 'parameters': {}}
            with open(baseline / filename, 'w') as f:
                json.dump(config, f)
        return baseline

    @pytest.fixture
    def results_manager(self, temp_dir, mock_baseline):
        """Create AccuracyResultsManager instance."""
        output_dir = temp_dir / "output"
        return AccuracyResultsManager(output_dir, mock_baseline)

    def test_sync_schedule_params_all_matchup_params(self, results_manager):
        """Test syncing all MATCHUP params to SCHEDULE (nested structure)."""
        config = {
            'MATCHUP_SCORING': {
                'IMPACT_SCALE': 0.8,
                'WEIGHT': 0.15,
                'MIN_WEEKS': 3
            },
            'OTHER_PARAM': 'value'
        }

        synced = results_manager._sync_schedule_params(config)

        assert 'SCHEDULE_SCORING' in synced
        assert synced['SCHEDULE_SCORING']['IMPACT_SCALE'] == 0.8
        assert synced['SCHEDULE_SCORING']['WEIGHT'] == 0.15
        assert synced['SCHEDULE_SCORING']['MIN_WEEKS'] == 3
        assert synced['OTHER_PARAM'] == 'value'

    def test_sync_schedule_params_partial(self, results_manager):
        """Test syncing when only some MATCHUP params exist (nested structure)."""
        config = {
            'MATCHUP_SCORING': {
                'IMPACT_SCALE': 0.5
            },
            'OTHER_PARAM': 'value'
        }

        synced = results_manager._sync_schedule_params(config)

        assert 'SCHEDULE_SCORING' in synced
        assert synced['SCHEDULE_SCORING']['IMPACT_SCALE'] == 0.5
        assert 'WEIGHT' not in synced['SCHEDULE_SCORING']
        assert 'MIN_WEEKS' not in synced['SCHEDULE_SCORING']

    def test_sync_schedule_params_no_matchup(self, results_manager):
        """Test syncing when no MATCHUP params exist."""
        config = {'OTHER_PARAM': 'value'}

        synced = results_manager._sync_schedule_params(config)

        assert 'SCHEDULE_SCORING' not in synced
        assert synced == config

    def test_sync_schedule_params_preserves_original(self, results_manager):
        """Test that original config is not modified (nested structure)."""
        config = {
            'MATCHUP_SCORING': {
                'IMPACT_SCALE': 0.8
            },
            'SCHEDULE_SCORING': {
                'IMPACT_SCALE': 0.5
            }
        }

        synced = results_manager._sync_schedule_params(config)

        assert config['SCHEDULE_SCORING']['IMPACT_SCALE'] == 0.5
        assert synced['SCHEDULE_SCORING']['IMPACT_SCALE'] == 0.8

    def test_save_optimal_configs_syncs_schedule(self, results_manager):
        """Test that save_optimal_configs applies SCHEDULE sync."""
        config = {
            'MATCHUP_SCORING': {
                'IMPACT_SCALE': 0.8,
                'WEIGHT': 0.15,
                'MIN_WEEKS': 3
            }
        }
        metrics = RankingMetrics(
            pairwise_accuracy=0.68,
            top_5_accuracy=0.80,
            top_10_accuracy=0.75,
            top_20_accuracy=0.70,
            spearman_correlation=0.82
        )
        result = AccuracyResult(
            mae=5.0, player_count=100, total_error=500.0,
            overall_metrics=metrics
        )
        results_manager.add_result('week_1_5', config, result)

        optimal_path = results_manager.save_optimal_configs()

        with open(optimal_path / "week1-5.json") as f:
            saved_config = json.load(f)

        params = saved_config['parameters']
        assert 'SCHEDULE_SCORING' in params
        assert params['SCHEDULE_SCORING']['IMPACT_SCALE'] == 0.8
        assert params['SCHEDULE_SCORING']['WEIGHT'] == 0.15
        assert params['SCHEDULE_SCORING']['MIN_WEEKS'] == 3

    def test_save_intermediate_results_syncs_schedule(self, results_manager):
        """Test that save_intermediate_results applies SCHEDULE sync."""
        config = {
            'MATCHUP_SCORING': {
                'IMPACT_SCALE': 0.7
            }
        }
        metrics = RankingMetrics(
            pairwise_accuracy=0.68,
            top_5_accuracy=0.80,
            top_10_accuracy=0.75,
            top_20_accuracy=0.70,
            spearman_correlation=0.82
        )
        result = AccuracyResult(
            mae=5.0, player_count=100, total_error=500.0,
            overall_metrics=metrics
        )
        results_manager.add_result('week_1_5', config, result)

        intermediate_path = results_manager.save_intermediate_results(0, 'TEST')

        with open(intermediate_path / "week1-5.json") as f:
            saved_data = json.load(f)

        assert 'SCHEDULE_SCORING' in saved_data['parameters']
        assert saved_data['parameters']['SCHEDULE_SCORING']['IMPACT_SCALE'] == 0.7


    def test_is_better_than_rejects_zero_players(self):
        """Test that is_better_than() rejects configs with player_count=0."""
        config_a = AccuracyConfigPerformance(
            config_dict={},
            mae=2.5,
            player_count=100,
            total_error=250.0
        )

        config_b = AccuracyConfigPerformance(
            config_dict={},
            mae=2.0,
            player_count=0,
            total_error=0.0
        )

        assert config_a.is_better_than(config_b) == False

        assert config_b.is_better_than(config_a) == False

    def test_is_better_than_both_zero_players(self):
        """Test that neither config is better when both have player_count=0."""
        config_a = AccuracyConfigPerformance(
            config_dict={},
            mae=2.5,
            player_count=0,
            total_error=0.0
        )

        config_b = AccuracyConfigPerformance(
            config_dict={},
            mae=2.0,
            player_count=0,
            total_error=0.0
        )

        assert config_a.is_better_than(config_b) == False
        assert config_b.is_better_than(config_a) == False

    def test_is_better_than_zero_vs_none(self):
        """Test that invalid config (player_count=0) does not beat None (no previous best)."""
        config_invalid = AccuracyConfigPerformance(
            config_dict={},
            mae=1.0,
            player_count=0,
            total_error=0.0
        )

        assert config_invalid.is_better_than(None) == False


class TestWeekRanges:
    """Tests for week range constants."""

    def test_week_ranges_defined(self):
        """Test that all week ranges are defined."""
        assert 'week_1_5' in WEEK_RANGES
        assert 'week_6_9' in WEEK_RANGES
        assert 'week_10_13' in WEEK_RANGES
        assert 'week_14_17' in WEEK_RANGES

    def test_week_ranges_values(self):
        """Test week range tuple values."""
        assert WEEK_RANGES['week_1_5'] == (1, 5)
        assert WEEK_RANGES['week_6_9'] == (6, 9)
        assert WEEK_RANGES['week_10_13'] == (10, 13)
        assert WEEK_RANGES['week_14_17'] == (14, 17)


class TestRankingMetrics:
    """Tests for RankingMetrics dataclass."""

    def test_ranking_metrics_creation(self):
        """Test creating RankingMetrics instance."""
        metrics = RankingMetrics(
            pairwise_accuracy=0.68,
            top_5_accuracy=0.80,
            top_10_accuracy=0.75,
            top_20_accuracy=0.70,
            spearman_correlation=0.82
        )

        assert metrics.pairwise_accuracy == 0.68
        assert metrics.top_5_accuracy == 0.80
        assert metrics.top_10_accuracy == 0.75
        assert metrics.top_20_accuracy == 0.70
        assert metrics.spearman_correlation == 0.82


class TestAccuracyConfigPerformanceRanking:
    """Tests for ranking metrics in AccuracyConfigPerformance."""

    def test_config_with_ranking_metrics(self):
        """Test creating config with ranking metrics."""
        metrics = RankingMetrics(
            pairwise_accuracy=0.68,
            top_5_accuracy=0.80,
            top_10_accuracy=0.75,
            top_20_accuracy=0.70,
            spearman_correlation=0.82
        )

        perf = AccuracyConfigPerformance(
            config_dict={'test': 'config'},
            mae=5.5,
            player_count=100,
            total_error=550.0,
            overall_metrics=metrics
        )

        assert perf.overall_metrics == metrics
        assert perf.overall_metrics.pairwise_accuracy == 0.68

    def test_is_better_than_uses_pairwise_accuracy(self):
        """Test that is_better_than() uses pairwise_accuracy when available."""
        metrics1 = RankingMetrics(
            pairwise_accuracy=0.70,
            top_5_accuracy=0.80,
            top_10_accuracy=0.75,
            top_20_accuracy=0.70,
            spearman_correlation=0.82
        )

        metrics2 = RankingMetrics(
            pairwise_accuracy=0.65,
            top_5_accuracy=0.85,
            top_10_accuracy=0.80,
            top_20_accuracy=0.75,
            spearman_correlation=0.85
        )

        perf1 = AccuracyConfigPerformance(
            config_dict={'test': 'config1'},
            mae=10.0,
            player_count=100,
            total_error=1000.0,
            overall_metrics=metrics1
        )

        perf2 = AccuracyConfigPerformance(
            config_dict={'test': 'config2'},
            mae=5.0,
            player_count=100,
            total_error=500.0,
            overall_metrics=metrics2
        )

        assert perf1.is_better_than(perf2)
        assert not perf2.is_better_than(perf1)

    def test_is_better_than_rejects_configs_without_metrics(self):
        """Test that configs without ranking metrics are rejected (invalid)."""
        perf1 = AccuracyConfigPerformance(
            config_dict={'test': 'config1'},
            mae=5.0,
            player_count=100,
            total_error=500.0
        )

        perf2 = AccuracyConfigPerformance(
            config_dict={'test': 'config2'},
            mae=10.0,
            player_count=100,
            total_error=1000.0
        )

        assert not perf1.is_better_than(perf2)
        assert not perf2.is_better_than(perf1)

        assert not perf1.is_better_than(None)

    def test_to_dict_includes_ranking_metrics(self):
        """Test that to_dict() includes ranking metrics."""
        metrics = RankingMetrics(
            pairwise_accuracy=0.68,
            top_5_accuracy=0.80,
            top_10_accuracy=0.75,
            top_20_accuracy=0.70,
            spearman_correlation=0.82
        )

        perf = AccuracyConfigPerformance(
            config_dict={'test': 'config'},
            mae=5.5,
            player_count=100,
            total_error=550.0,
            overall_metrics=metrics
        )

        result = perf.to_dict()

        assert result['pairwise_accuracy'] == 0.68
        assert result['top_5_accuracy'] == 0.80
        assert result['top_10_accuracy'] == 0.75
        assert result['top_20_accuracy'] == 0.70
        assert result['spearman_correlation'] == 0.82

    def test_to_dict_without_ranking_metrics(self):
        """Test that to_dict() works without ranking metrics (backward compat)."""
        perf = AccuracyConfigPerformance(
            config_dict={'test': 'config'},
            mae=5.5,
            player_count=100,
            total_error=550.0
        )

        result = perf.to_dict()

        assert 'pairwise_accuracy' not in result
        assert 'top_5_accuracy' not in result
        assert result['mae'] == 5.5

    def test_from_dict_with_ranking_metrics(self):
        """Test that from_dict() loads ranking metrics."""
        data = {
            'config': {'test': 'config'},
            'mae': 5.5,
            'player_count': 100,
            'total_error': 550.0,
            'pairwise_accuracy': 0.68,
            'top_5_accuracy': 0.80,
            'top_10_accuracy': 0.75,
            'top_20_accuracy': 0.70,
            'spearman_correlation': 0.82
        }

        perf = AccuracyConfigPerformance.from_dict(data)

        assert perf.overall_metrics is not None
        assert perf.overall_metrics.pairwise_accuracy == 0.68
        assert perf.overall_metrics.top_5_accuracy == 0.80
        assert perf.overall_metrics.spearman_correlation == 0.82

    def test_from_dict_without_ranking_metrics(self):
        """Test that from_dict() handles old format (backward compat)."""
        data = {
            'config': {'test': 'config'},
            'mae': 5.5,
            'player_count': 100,
            'total_error': 550.0
        }

        perf = AccuracyConfigPerformance.from_dict(data)

        assert perf.overall_metrics is None
        assert perf.mae == 5.5
        assert perf.player_count == 100

    def test_roundtrip_with_ranking_metrics(self):
        """Test to_dict() and from_dict() roundtrip with ranking metrics."""
        metrics = RankingMetrics(
            pairwise_accuracy=0.68,
            top_5_accuracy=0.80,
            top_10_accuracy=0.75,
            top_20_accuracy=0.70,
            spearman_correlation=0.82
        )

        perf1 = AccuracyConfigPerformance(
            config_dict={'test': 'config'},
            mae=5.5,
            player_count=100,
            total_error=550.0,
            overall_metrics=metrics
        )

        data = perf1.to_dict()
        perf2 = AccuracyConfigPerformance.from_dict(data)

        assert perf2.overall_metrics.pairwise_accuracy == perf1.overall_metrics.pairwise_accuracy
        assert perf2.overall_metrics.top_5_accuracy == perf1.overall_metrics.top_5_accuracy
        assert perf2.overall_metrics.spearman_correlation == perf1.overall_metrics.spearman_correlation

    def test_by_position_metrics(self):
        """Test per-position ranking metrics."""
        qb_metrics = RankingMetrics(
            pairwise_accuracy=0.71,
            top_5_accuracy=0.85,
            top_10_accuracy=0.80,
            top_20_accuracy=0.75,
            spearman_correlation=0.88
        )

        rb_metrics = RankingMetrics(
            pairwise_accuracy=0.66,
            top_5_accuracy=0.75,
            top_10_accuracy=0.70,
            top_20_accuracy=0.65,
            spearman_correlation=0.78
        )

        by_position = {'QB': qb_metrics, 'RB': rb_metrics}

        perf = AccuracyConfigPerformance(
            config_dict={'test': 'config'},
            mae=5.5,
            player_count=100,
            total_error=550.0,
            by_position=by_position
        )

        assert perf.by_position['QB'].pairwise_accuracy == 0.71
        assert perf.by_position['RB'].pairwise_accuracy == 0.66

        result = perf.to_dict()
        assert 'by_position' in result
        assert result['by_position']['QB']['pairwise_accuracy'] == 0.71
        assert result['by_position']['RB']['pairwise_accuracy'] == 0.66

        perf2 = AccuracyConfigPerformance.from_dict(result)
        assert perf2.by_position['QB'].pairwise_accuracy == 0.71
        assert perf2.by_position['RB'].pairwise_accuracy == 0.66

    def test_roundtrip_with_none_metric_json_null(self):
        """A None metric field serializes to JSON null and round-trips back to None (D6)."""
        metrics = RankingMetrics(
            pairwise_accuracy=0.68,
            top_5_accuracy=0.80,
            top_10_accuracy=None,
            top_20_accuracy=None,
            spearman_correlation=None
        )

        perf1 = AccuracyConfigPerformance(
            config_dict={'test': 'config'},
            mae=5.5,
            player_count=100,
            total_error=550.0,
            overall_metrics=metrics
        )

        serialized = json.dumps(perf1.to_dict())
        assert '"top_10_accuracy": null' in serialized
        assert '"spearman_correlation": null' in serialized

        perf2 = AccuracyConfigPerformance.from_dict(json.loads(serialized))
        assert perf2.overall_metrics.pairwise_accuracy == 0.68
        assert perf2.overall_metrics.top_10_accuracy is None
        assert perf2.overall_metrics.top_20_accuracy is None
        assert perf2.overall_metrics.spearman_correlation is None


class TestPropagateToConfigs:
    """Tests for propagate_to_configs module-level function (F02 spec TS1)."""

    def test_copies_all_five_files(self, tmp_path):
        """All 5 standard config files are copied from optimal_folder to target_folder."""
        import logging
        config_files = ['league_config.json', 'week1-5.json', 'week6-9.json',
                        'week10-13.json', 'week14-17.json']
        optimal = tmp_path / "optimal"
        optimal.mkdir()
        target = tmp_path / "target"
        for cf in config_files:
            (optimal / cf).write_text(json.dumps({'parameters': {'TEST': 1}}))
        logger = logging.getLogger('test')
        propagate_to_configs(optimal, target, logger)
        for cf in config_files:
            assert (target / cf).exists(), f"Expected {cf} to be copied to target"

    def test_target_created_if_missing(self, tmp_path):
        """target_folder is auto-created via mkdir(parents=True, exist_ok=True)."""
        import logging
        optimal = tmp_path / "optimal"
        optimal.mkdir()
        target = tmp_path / "nonexistent" / "nested" / "target"
        (optimal / 'league_config.json').write_text(json.dumps({'parameters': {}}))
        logger = logging.getLogger('test')
        propagate_to_configs(optimal, target, logger)
        assert target.exists()
        assert (target / 'league_config.json').exists()

    def test_league_config_preserves_user_maintained_keys(self, tmp_path):
        """league_config.json: 6 PRESERVE_KEYS retained from existing target file."""
        import logging
        optimal = tmp_path / "optimal"
        optimal.mkdir()
        target = tmp_path / "target"
        target.mkdir()
        preserve_keys = ['CURRENT_NFL_WEEK', 'NFL_SEASON', 'MAX_POSITIONS',
                         'FLEX_ELIGIBLE_POSITIONS', 'INJURY_PENALTIES',
                         'OPPONENT_TEAMS']
        optimal_params = {k: 'OPTIMAL_VALUE' for k in preserve_keys}
        # ADP_SCORING is a BASE_CONFIG_PARAMS member that is NOT preserved, so it
        # survives the T90 filter and must come from the source (was: SCORING_WEIGHT,
        # a synthetic non-base key the filter now correctly drops).
        optimal_params['ADP_SCORING'] = 0.9
        (optimal / 'league_config.json').write_text(json.dumps({'parameters': optimal_params}))
        original_params = {k: f'ORIGINAL_{k}' for k in preserve_keys}
        original_params['ADP_SCORING'] = 0.5
        (target / 'league_config.json').write_text(json.dumps({'parameters': original_params}))
        logger = logging.getLogger('test')
        propagate_to_configs(optimal, target, logger)
        with open(target / 'league_config.json') as f:
            result = json.load(f)
        for key in preserve_keys:
            assert result['parameters'][key] == f'ORIGINAL_{key}', \
                f"Expected {key} preserved from original config"
        assert result['parameters']['ADP_SCORING'] == 0.9, \
            "Non-preserved base-owned key should come from optimal config"

    def test_league_config_copied_as_is_if_no_target(self, tmp_path):
        """league_config.json lands unchanged when no existing target file (no preservation)."""
        import logging
        optimal = tmp_path / "optimal"
        optimal.mkdir()
        target = tmp_path / "target"
        target.mkdir()
        # Both keys are BASE_CONFIG_PARAMS members, so the T90 filter is a no-op
        # here and the no-target arm's "no preserve-overlay" property still reads
        # as an exact-equality assertion (was: SCORING_WEIGHT, a synthetic non-base key).
        optimal_config = {'parameters': {'CURRENT_NFL_WEEK': 5, 'ADP_SCORING': 0.9}}
        (optimal / 'league_config.json').write_text(json.dumps(optimal_config))
        logger = logging.getLogger('test')
        propagate_to_configs(optimal, target, logger)
        with open(target / 'league_config.json') as f:
            result = json.load(f)
        assert result == optimal_config

    def test_weekly_files_copied_as_is(self, tmp_path):
        """Weekly config files copied byte-for-byte (no MATCHUP->SCHEDULE mapping applied)."""
        import logging
        optimal = tmp_path / "optimal"
        optimal.mkdir()
        target = tmp_path / "target"
        weekly_config = {'parameters': {'MATCHUP_SCORING': {'WEIGHT': 0.5}, 'OTHER': 1}}
        (optimal / 'week1-5.json').write_text(json.dumps(weekly_config))
        logger = logging.getLogger('test')
        propagate_to_configs(optimal, target, logger)
        with open(target / 'week1-5.json') as f:
            result = json.load(f)
        assert result == weekly_config

    def test_missing_source_file_logs_warning_and_skips(self, tmp_path):
        """Missing source file: WARNING logged, file skipped, other files copied."""
        optimal = tmp_path / "optimal"
        optimal.mkdir()
        target = tmp_path / "target"
        (optimal / 'league_config.json').write_text(json.dumps({'parameters': {}}))
        (optimal / 'week1-5.json').write_text(json.dumps({'parameters': {}}))
        mock_logger = Mock()
        propagate_to_configs(optimal, target, mock_logger)
        assert (target / 'league_config.json').exists()
        assert (target / 'week1-5.json').exists()
        assert not (target / 'week6-9.json').exists()
        warning_messages = [str(c) for c in mock_logger.warning.call_args_list]
        assert len(warning_messages) >= 3, "Expected warnings for 3 missing files"

    def test_performance_metrics_block_stripped(self, tmp_path):
        """propagate_to_configs strips performance_metrics so live data/configs stays sim-free."""
        import logging
        optimal = tmp_path / "optimal"
        optimal.mkdir()
        target = tmp_path / "target"
        src_with_metrics = {
            'parameters': {'ADP_SCORING': 1},
            'performance_metrics': {'mae': 1.23, 'ranking_metrics': {'pairwise_accuracy': 0.7}}
        }
        (optimal / 'league_config.json').write_text(json.dumps(src_with_metrics))
        (optimal / 'week1-5.json').write_text(json.dumps(src_with_metrics))
        logger = logging.getLogger('test')
        propagate_to_configs(optimal, target, logger)
        for fname in ('league_config.json', 'week1-5.json'):
            with open(target / fname) as f:
                written = json.load(f)
            assert 'performance_metrics' not in written, \
                f"{fname} must have performance_metrics stripped"
            assert written['parameters'] == {'ADP_SCORING': 1}, \
                f"{fname} parameters must be preserved"

    def test_malformed_source_leaves_configs_byte_identical(self, tmp_path):
        """Malformed mid-list source (week6-9.json): Phase 1 raises, target dir untouched (D1)."""
        import logging
        optimal = tmp_path / "optimal"
        optimal.mkdir()
        target = tmp_path / "target"
        target.mkdir()
        # Pre-existing target files whose bytes must be unchanged after a failed promote.
        sentinel = json.dumps({'parameters': {'SENTINEL': True}}, indent=2)
        for cf in ('league_config.json', 'week1-5.json'):
            (target / cf).write_text(sentinel)
        before = {p.name: p.read_bytes() for p in target.iterdir()}
        # Valid sources for files 1-2, malformed source for file 3 (week6-9.json).
        (optimal / 'league_config.json').write_text(json.dumps({'parameters': {'X': 1}}))
        (optimal / 'week1-5.json').write_text(json.dumps({'parameters': {'X': 1}}))
        (optimal / 'week6-9.json').write_text('{ this is not valid json ')
        logger = logging.getLogger('test')
        with pytest.raises(json.JSONDecodeError):
            propagate_to_configs(optimal, target, logger)
        after = {p.name: p.read_bytes() for p in target.iterdir()}
        assert after == before, "target dir must be byte-identical after a Phase-1 failure"
        assert not list(target.glob('*.tmp')), "no .tmp residue after a failed promote"

    def test_unwritable_non_first_target_no_tmp_and_failing_target_unchanged(self, tmp_path):
        """Write failure on a non-first file: failing target unchanged, no .tmp residue (D1).

        Files written before the failing one in Phase 2 are the accepted set-level
        residual (spec Out of Scope: five-file transactionality is OOS). The in-scope
        guarantees asserted here are per-file atomicity of the failing write (no .tmp,
        failing target byte-identical) and that Phase 1 built every payload before any
        write (the injected failure is reached only in Phase 2).
        """
        import logging
        config_files = ['league_config.json', 'week1-5.json', 'week6-9.json',
                        'week10-13.json', 'week14-17.json']
        optimal = tmp_path / "optimal"
        optimal.mkdir()
        target = tmp_path / "target"
        target.mkdir()
        for cf in config_files:
            (optimal / cf).write_text(json.dumps({'parameters': {'X': 1}}))
        # A pre-existing failing target whose bytes must be unchanged.
        sentinel = json.dumps({'parameters': {'SENTINEL': True}}, indent=2)
        (target / 'week6-9.json').write_text(sentinel)
        failing_before = (target / 'week6-9.json').read_bytes()

        real_replace = Path.replace

        def flaky_replace(self, target_arg):
            if Path(target_arg).name == 'week6-9.json':
                raise OSError("injected rename failure")
            return real_replace(self, target_arg)

        logger = logging.getLogger('test')
        with patch.object(Path, 'replace', flaky_replace):
            with pytest.raises(FileOperationError):
                propagate_to_configs(optimal, target, logger)
        # Failing target unchanged and no .tmp residue anywhere in the target dir.
        assert (target / 'week6-9.json').read_bytes() == failing_before
        assert not list(target.glob('*.tmp')), "no .tmp residue after a failed write"

    def test_malformed_existing_league_target_leaves_configs_byte_identical(self, tmp_path):
        """Malformed existing target league_config.json: Phase 1 preserve-merge read raises (D1)."""
        import logging
        config_files = ['league_config.json', 'week1-5.json', 'week6-9.json',
                        'week10-13.json', 'week14-17.json']
        optimal = tmp_path / "optimal"
        optimal.mkdir()
        target = tmp_path / "target"
        target.mkdir()
        for cf in config_files:
            (optimal / cf).write_text(json.dumps({'parameters': {'X': 1}}))
        # Existing league_config target is malformed -> preserve-merge read raises on file 1.
        (target / 'league_config.json').write_text('{ not valid json ')
        before = {p.name: p.read_bytes() for p in target.iterdir()}
        logger = logging.getLogger('test')
        with pytest.raises(json.JSONDecodeError):
            propagate_to_configs(optimal, target, logger)
        after = {p.name: p.read_bytes() for p in target.iterdir()}
        assert after == before, "target dir must be byte-identical after a Phase-1 failure"
        assert not list(target.glob('*.tmp')), "no .tmp residue after a failed promote"

    def test_happy_path_all_five_land_stripped_bytes_identical_no_tmp(self, tmp_path):
        """Happy path: all five land, performance_metrics stripped, indent=2 bytes, no .tmp (D4)."""
        import logging
        config_files = ['league_config.json', 'week1-5.json', 'week6-9.json',
                        'week10-13.json', 'week14-17.json']
        optimal = tmp_path / "optimal"
        optimal.mkdir()
        target = tmp_path / "target"
        # ADP_SCORING is a BASE_CONFIG_PARAMS member, so the T90 filter is a no-op
        # and the byte-identity property holds for league_config.json too (was: 'X',
        # a synthetic non-base key the filter now correctly drops).
        src = {'parameters': {'ADP_SCORING': 1}, 'performance_metrics': {'mae': 1.23}}
        expected = {'parameters': {'ADP_SCORING': 1}}
        for cf in config_files:
            (optimal / cf).write_text(json.dumps(src))
        logger = logging.getLogger('test')
        propagate_to_configs(optimal, target, logger)
        for cf in config_files:
            written = (target / cf).read_text()
            assert written == json.dumps(expected, indent=2), \
                f"{cf} must be byte-identical to json.dump(indent=2) with metrics stripped"
        assert not list(target.glob('*.tmp')), "no .tmp residue after a successful promote"

    def test_inflated_source_cannot_reinflate_league_config(self, tmp_path):
        """T90 AC3: week-owned keys in the promote SOURCE never reach the base config.

        Drives an actual promote from a source shaped like the real on-disk inflated
        accuracy_optimal_* folder, in BOTH arms (existing target / no target). This is
        the promote-PATH guard T86's committed-data guard cannot provide.
        Targets are under tmp_path only - never data/configs/.
        """
        import logging
        # Arrange - the 20-key inflated shape, in miniature.
        inflated_params = {
            'CURRENT_NFL_WEEK': 15,
            'NFL_SEASON': 2023,
            'ADP_SCORING': {'WEIGHT': 1.5},
            'PLAYER_RATING_SCORING': {'WEIGHT': 1.8},
            'TEAM_QUALITY_SCORING': {'WEIGHT': 2.77},
            'PERFORMANCE_SCORING': {'WEIGHT': 3.55},
            'MATCHUP_SCORING': {'WEIGHT': 1.62},
            'SCHEDULE_SCORING': {'WEIGHT': 0.9},
            'TEMPERATURE_SCORING': {'WEIGHT': 0.81},
            'WIND_SCORING': {'WEIGHT': 1.23},
        }
        optimal = tmp_path / "optimal"
        optimal.mkdir()
        (optimal / 'league_config.json').write_text(
            json.dumps({'config_name': 'Inflated', 'parameters': inflated_params}))
        logger = logging.getLogger('test')

        existing_target = tmp_path / "target_existing"
        existing_target.mkdir()
        (existing_target / 'league_config.json').write_text(
            json.dumps({'parameters': {'CURRENT_NFL_WEEK': 1, 'OPPONENT_TEAMS': ['KC']}}))
        absent_target = tmp_path / "target_absent"

        for arm, target in (('existing-target', existing_target), ('no-target', absent_target)):
            # Act
            propagate_to_configs(optimal, target, logger)

            # Assert
            with open(target / 'league_config.json') as f:
                written = set(json.load(f)['parameters'].keys())
            assert written & set(WEEK_SPECIFIC_PARAMS) == set(), \
                f"{arm}: week-owned keys reached the base config: {sorted(written & set(WEEK_SPECIFIC_PARAMS))}"
            assert written <= set(BASE_CONFIG_PARAMS), \
                f"{arm}: non-base keys reached the base config: {sorted(written - set(BASE_CONFIG_PARAMS))}"

    def test_opponent_teams_survives_a_promote_from_a_source_lacking_it(self, tmp_path):
        """T90 AC4 (D2): OPPONENT_TEAMS is preserved from the target when the source omits it.

        The drop direction no subtractive filter can fix - propagate_to_configs
        atomically REPLACES the target, so a live-only base key is deleted unless
        it is in PRESERVE_KEYS. Target is under tmp_path only - never data/configs/.
        """
        import logging
        # Arrange
        optimal = tmp_path / "optimal"
        optimal.mkdir()
        target = tmp_path / "target"
        target.mkdir()
        (optimal / 'league_config.json').write_text(
            json.dumps({'parameters': {'CURRENT_NFL_WEEK': 9, 'ADP_SCORING': {'WEIGHT': 1.5}}}))
        original_teams = ['KC', 'SF', 'BUF']
        (target / 'league_config.json').write_text(
            json.dumps({'parameters': {'CURRENT_NFL_WEEK': 1, 'OPPONENT_TEAMS': original_teams}}))
        logger = logging.getLogger('test')

        # Act
        propagate_to_configs(optimal, target, logger)

        # Assert
        with open(target / 'league_config.json') as f:
            written = json.load(f)['parameters']
        assert written['OPPONENT_TEAMS'] == original_teams, \
            "OPPONENT_TEAMS must be preserved from the promote target, not dropped"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])




SEASONS = ['2021', '2022', '2023', '2024', '2025']


def _gate_perf(mean_pairwise, per_season=None):
    """Build a performance carrying only what the T69 consistency gate reads.

    mean_pairwise is what overall_metrics reports (the pre-T69 comparison); per_season is
    the T69 vector. Everything else is filler -- the gate touches neither MAE nor players.
    """
    return AccuracyConfigPerformance(
        config_dict={},
        mae=1.0,
        player_count=10,
        total_error=10.0,
        overall_metrics=RankingMetrics(
            pairwise_accuracy=mean_pairwise,
            top_5_accuracy=None,
            top_10_accuracy=None,
            top_20_accuracy=None,
            spearman_correlation=None,
        ),
        per_season_pairwise=per_season,
    )


class TestT69ConsistencyAdoptionGate:
    """T69/D2: adoption requires a supermajority of per-season wins AND a better mean.

    The gate guards against a difference driven by one or two idiosyncratic seasons. It is
    NOT a noise gate -- accuracy evaluation is deterministic, so re-evaluating a config
    yields an identical number.
    """

    def test_consistency_gate_adopts_genuine_improvement(self):
        """T69/AC4b: a candidate better on EVERY season is adopted.

        NOT OPTIONAL. Without this, every other test here is satisfied by a gate that
        always returns False -- an inert optimizer that terminates reporting convergence
        having optimized nothing, which is this story's primary silent-failure mode.
        """
        cand = _gate_perf(0.60, dict(zip(SEASONS, [.61, .62, .60, .63, .59])))
        inc = _gate_perf(0.55, dict(zip(SEASONS, [.55, .56, .54, .57, .53])))
        assert cand.is_better_than(inc) is True

    def test_consistency_gate_rejects_single_season_fluke(self):
        """T69/AC4a: a better MEAN carried by one season is not enough (wins 1 of 5)."""
        fluke = _gate_perf(0.60, dict(zip(SEASONS, [.50, .50, .50, .50, 1.00])))
        base = _gate_perf(0.55, dict(zip(SEASONS, [.55, .55, .55, .55, .55])))
        assert fluke.is_better_than(base) is False

    def test_consistency_gate_adopts_at_exactly_the_threshold(self):
        """T69/AC4a boundary: 4 of 5 wins is exactly ceil(0.8 * 5) -- adoptable."""
        base = _gate_perf(0.55, dict(zip(SEASONS, [.55, .55, .55, .55, .55])))
        edge = _gate_perf(0.60, dict(zip(SEASONS, [.61, .62, .63, .64, .40])))
        assert edge.is_better_than(base) is True

    def test_consistency_gate_rejects_one_win_below_threshold(self):
        """T69/AC4a boundary: 3 of 5 wins is below ceil(0.8 * 5) = 4 -- rejected."""
        base = _gate_perf(0.55, dict(zip(SEASONS, [.55, .55, .55, .55, .55])))
        below = _gate_perf(0.60, dict(zip(SEASONS, [.61, .62, .63, .40, .40])))
        assert below.is_better_than(base) is False

    def test_consistency_gate_rejects_when_mean_regresses(self):
        """T69/AC4a: winning every season does not override a worse mean."""
        base = _gate_perf(0.55, dict(zip(SEASONS, [.55, .55, .55, .55, .55])))
        lower_mean = _gate_perf(0.50, dict(zip(SEASONS, [.56, .56, .56, .56, .56])))
        assert lower_mean.is_better_than(base) is False

    def test_threshold_derives_from_actual_season_count(self):
        """T69/AC4c: the threshold is computed, never a literal tuned for 5 seasons.

        A hardcoded value would be UNSATISFIABLE on a smaller corpus -- nothing would ever
        adopt and the optimizer would go silently inert. Seasons are discovered at runtime
        from --data, so the count is not fixed.
        """
        assert [_min_season_wins(n) for n in range(1, 11)] == [1, 2, 3, 4, 4, 5, 6, 7, 8, 8]

    def test_threshold_is_always_satisfiable(self):
        """T69/AC4c: ceil(0.8 * n) <= n for every n, so no corpus size blocks adoption."""
        for n in range(1, 51):
            assert _min_season_wins(n) <= n

    def test_gate_degrades_without_per_season_map(self):
        """T69/AC6: no per-season data -> the pre-T69 mean comparison, both directions."""
        assert _gate_perf(0.60, {}).is_better_than(_gate_perf(0.55, {})) is True
        assert _gate_perf(0.50, {}).is_better_than(_gate_perf(0.55, {})) is False

    def test_gate_degrades_with_one_shared_season(self):
        """T69/AC6: one shared season cannot evidence consistency -> mean comparison.

        The maps are non-empty but overlap in only '2021', so the gate must not engage.
        """
        a = _gate_perf(0.60, {'2021': 0.40, '2022': 0.90})
        b = _gate_perf(0.55, {'2021': 0.99, '2023': 0.10})
        assert a.is_better_than(b) is True

    def test_t63_none_guards_still_fire_first(self):
        """T69/AC5: T63's None handling precedes the gate and is unchanged."""
        assert _gate_perf(None, dict(zip(SEASONS, [.9] * 5))).is_better_than(
            _gate_perf(0.5, dict(zip(SEASONS, [.1] * 5)))) is False
        assert _gate_perf(0.5, dict(zip(SEASONS, [.1] * 5))).is_better_than(
            _gate_perf(None, dict(zip(SEASONS, [.9] * 5)))) is True

    def test_per_season_map_survives_dict_roundtrip(self):
        """T69/AC6: to_dict -> from_dict preserves the vector."""
        original = dict(zip(SEASONS, [.61, .62, .60, .63, .59]))
        perf = _gate_perf(0.61, original)
        restored = AccuracyConfigPerformance.from_dict(perf.to_dict())
        assert restored.per_season_pairwise == original

    def test_reconstruction_without_the_key_does_not_raise(self):
        """T69/AC6: a pre-T69 artifact has no such key -- reconstruct to {} , not KeyError."""
        d = _gate_perf(0.61, dict(zip(SEASONS, [.6] * 5))).to_dict()
        d.pop('per_season_pairwise', None)
        restored = AccuracyConfigPerformance.from_dict(d)
        assert restored.per_season_pairwise == {}

    def test_empty_map_is_not_serialized(self):
        """T69/A4: an empty vector adds no key, so pre-T69 golden files are unchanged."""
        assert 'per_season_pairwise' not in _gate_perf(0.61, {}).to_dict()
