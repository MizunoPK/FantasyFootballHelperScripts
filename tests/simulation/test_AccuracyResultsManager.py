"""
Tests for AccuracyResultsManager

Tests results tracking and storage for accuracy simulation.

Author: Kai Mizuno
"""

import json
import pytest
from pathlib import Path
from unittest.mock import Mock, patch
import sys
import tempfile
import shutil

# Add simulation/accuracy to path
sys.path.append(str(Path(__file__).parent.parent.parent / "simulation" / "accuracy"))
from AccuracyResultsManager import (
    AccuracyResultsManager,
    AccuracyConfigPerformance,
    RankingMetrics,
    WEEK_RANGES
)
from AccuracyCalculator import AccuracyResult


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
        assert perf.config_value is None  # No param_name provided
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
        # Test WIND_SCORING_WEIGHT extraction
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

        # Test LOCATION_AWAY extraction
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

        # Test top-level param extraction
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
        # Create league_config.json
        league_config = {
            'config_name': 'Test Baseline',
            'description': 'Test baseline config',
            'parameters': {'PARAM1': 'value1'}
        }
        with open(baseline / "league_config.json", 'w') as f:
            json.dump(league_config, f)
        # Create week files
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

        # Create ranking metrics for both results
        metrics1 = RankingMetrics(
            pairwise_accuracy=0.65,
            top_5_accuracy=0.80,
            top_10_accuracy=0.75,
            top_20_accuracy=0.70,
            spearman_correlation=0.82
        )
        metrics2 = RankingMetrics(
            pairwise_accuracy=0.70,  # Better pairwise accuracy
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
            pairwise_accuracy=0.70,  # Better
            top_5_accuracy=0.80,
            top_10_accuracy=0.75,
            top_20_accuracy=0.70,
            spearman_correlation=0.82
        )
        metrics2 = RankingMetrics(
            pairwise_accuracy=0.65,  # Worse
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

    def test_save_optimal_configs(self, results_manager):
        """Test saving optimal configs to folder."""
        # Add results for two week ranges
        # Use real WEEK_SPECIFIC_PARAMS parameters with nested structure
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

        # Save
        optimal_path = results_manager.save_optimal_configs()

        # Verify folder created
        assert optimal_path.exists()
        assert optimal_path.name.startswith("accuracy_optimal_")

        # Verify all files created (league_config.json + 4 weekly configs)
        # No separate performance_metrics.json - metrics are embedded in each config
        assert (optimal_path / "league_config.json").exists()  # Copied from baseline
        assert (optimal_path / "week1-5.json").exists()
        assert (optimal_path / "week6-9.json").exists()
        assert (optimal_path / "week10-13.json").exists()
        assert (optimal_path / "week14-17.json").exists()

        # Verify week1-5.json has proper nested structure
        with open(optimal_path / "week1-5.json") as f:
            saved_config = json.load(f)
        assert 'config_name' in saved_config
        assert 'description' in saved_config
        assert 'parameters' in saved_config
        assert 'TEAM_QUALITY_SCORING' in saved_config['parameters']
        assert saved_config['parameters']['TEAM_QUALITY_SCORING']['WEIGHT'] == 1.5
        assert 'performance_metrics' in saved_config
        assert saved_config['performance_metrics']['mae'] == 5.0

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
        # Standard config files (can be used as baseline and for resume)
        assert (intermediate_path / "league_config.json").exists()
        # Week files copied from baseline since no results for them
        assert (intermediate_path / "week1-5.json").exists()
        assert (intermediate_path / "week6-9.json").exists()
        assert (intermediate_path / "week10-13.json").exists()
        assert (intermediate_path / "week14-17.json").exists()
        # Metadata file for tournament mode tracking (new in Phase 2)
        assert (intermediate_path / "metadata.json").exists()
        # Config files + metadata.json = 6 files
        all_files = list(intermediate_path.glob("*.json"))
        assert len(all_files) == 6  # league_config + 4 week files + metadata.json

    def test_load_intermediate_results(self, results_manager, temp_dir):
        """Test loading intermediate results from standard config files."""
        # Create intermediate folder with saved config in standard format
        intermediate_path = temp_dir / "accuracy_intermediate_00_TEST"
        intermediate_path.mkdir()

        # Standard config format with nested structure
        config_data = {
            'config_name': 'Test Config',
            'description': 'Test description',
            'parameters': {'test': 'config'},
            'performance_metrics': {
                'mae': 5.0,
                'player_count': 100,
                'config_value': 2.5
            }
        }
        with open(intermediate_path / "week1-5.json", 'w') as f:
            json.dump(config_data, f)

        # Load
        success = results_manager.load_intermediate_results(intermediate_path)

        # Should return True indicating files were found
        assert success
        # best_configs should NOT be populated (metrics are for user visibility only)
        # Each run evaluates configs fresh with current ranking metrics
        assert results_manager.best_configs['week_1_5'] is None

    def test_load_intermediate_results_not_found(self, results_manager, temp_dir):
        """Test loading from non-existent folder."""
        success = results_manager.load_intermediate_results(temp_dir / "nonexistent")
        assert not success

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

        # Record different configs for ros and week_1_5
        results_manager.add_result('ros', config1, result1)
        results_manager.add_result('week_1_5', config2, result2)

        # Verify they're stored independently
        ros_config = results_manager.best_configs['ros'].config_dict
        week_config = results_manager.best_configs['week_1_5'].config_dict

        assert ros_config['parameters']['NORMALIZATION_MAX_SCALE'] == 100
        assert week_config['parameters']['NORMALIZATION_MAX_SCALE'] == 150

        # Modify ros config and verify week_1_5 is unaffected
        ros_config['parameters']['NORMALIZATION_MAX_SCALE'] = 200
        assert week_config['parameters']['NORMALIZATION_MAX_SCALE'] == 150  # Should still be 150


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
        # Create required config files
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
        assert synced['OTHER_PARAM'] == 'value'  # Other params preserved

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
                'IMPACT_SCALE': 0.5  # Different value
            }
        }

        synced = results_manager._sync_schedule_params(config)

        # Original unchanged
        assert config['SCHEDULE_SCORING']['IMPACT_SCALE'] == 0.5
        # Synced has MATCHUP value
        assert synced['SCHEDULE_SCORING']['IMPACT_SCALE'] == 0.8

    def test_save_optimal_configs_syncs_schedule(self, results_manager):
        """Test that save_optimal_configs applies SCHEDULE sync."""
        # Use nested structure matching actual config format
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

        # SCHEDULE params should mirror MATCHUP in parameters section (nested structure)
        params = saved_config['parameters']
        assert 'SCHEDULE_SCORING' in params
        assert params['SCHEDULE_SCORING']['IMPACT_SCALE'] == 0.8
        assert params['SCHEDULE_SCORING']['WEIGHT'] == 0.15
        assert params['SCHEDULE_SCORING']['MIN_WEEKS'] == 3

    def test_save_intermediate_results_syncs_schedule(self, results_manager):
        """Test that save_intermediate_results applies SCHEDULE sync."""
        # Use nested structure matching actual config format
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

        # Check the standard config file (week1-5.json for 'week_1_5')
        with open(intermediate_path / "week1-5.json") as f:
            saved_data = json.load(f)

        # SCHEDULE params should mirror MATCHUP in parameters section (nested structure)
        assert 'SCHEDULE_SCORING' in saved_data['parameters']
        assert saved_data['parameters']['SCHEDULE_SCORING']['IMPACT_SCALE'] == 0.7


    def test_is_better_than_rejects_zero_players(self):
        """Test that is_better_than() rejects configs with player_count=0."""
        # Valid config
        config_a = AccuracyConfigPerformance(
            config_dict={},
            mae=2.5,
            player_count=100,
            total_error=250.0
        )

        # Invalid config (better MAE but no players)
        config_b = AccuracyConfigPerformance(
            config_dict={},
            mae=2.0,
            player_count=0,
            total_error=0.0
        )

        # Valid config should not beat invalid config
        assert config_a.is_better_than(config_b) == False

        # Invalid config should not beat valid config
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

        # Neither invalid config beats the other
        assert config_a.is_better_than(config_b) == False
        assert config_b.is_better_than(config_a) == False

    def test_is_better_than_zero_vs_none(self):
        """Test that invalid config (player_count=0) does not beat None (no previous best)."""
        # Invalid config
        config_invalid = AccuracyConfigPerformance(
            config_dict={},
            mae=1.0,
            player_count=0,
            total_error=0.0
        )

        # Invalid config should not become "best" even when no previous best exists
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
            top_5_accuracy=0.85,  # Better top_5, but pairwise_accuracy is what matters
            top_10_accuracy=0.80,
            top_20_accuracy=0.75,
            spearman_correlation=0.85
        )

        perf1 = AccuracyConfigPerformance(
            config_dict={'test': 'config1'},
            mae=10.0,  # Worse MAE, but better pairwise_accuracy
            player_count=100,
            total_error=1000.0,
            overall_metrics=metrics1
        )

        perf2 = AccuracyConfigPerformance(
            config_dict={'test': 'config2'},
            mae=5.0,  # Better MAE, but worse pairwise_accuracy
            player_count=100,
            total_error=500.0,
            overall_metrics=metrics2
        )

        # perf1 should be better because pairwise_accuracy (0.70) > (0.65)
        assert perf1.is_better_than(perf2)
        assert not perf2.is_better_than(perf1)

    def test_is_better_than_rejects_configs_without_metrics(self):
        """Test that configs without ranking metrics are rejected (invalid)."""
        perf1 = AccuracyConfigPerformance(
            config_dict={'test': 'config1'},
            mae=5.0,
            player_count=100,
            total_error=500.0
            # No overall_metrics - invalid config
        )

        perf2 = AccuracyConfigPerformance(
            config_dict={'test': 'config2'},
            mae=10.0,
            player_count=100,
            total_error=1000.0
            # No overall_metrics - invalid config
        )

        # Both configs invalid, neither should be "better"
        assert not perf1.is_better_than(perf2)
        assert not perf2.is_better_than(perf1)

        # Invalid config should not beat None (cannot become "best")
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

        # Should not have ranking metrics keys
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

        # Test to_dict includes by_position
        result = perf.to_dict()
        assert 'by_position' in result
        assert result['by_position']['QB']['pairwise_accuracy'] == 0.71
        assert result['by_position']['RB']['pairwise_accuracy'] == 0.66

        # Test from_dict loads by_position
        perf2 = AccuracyConfigPerformance.from_dict(result)
        assert perf2.by_position['QB'].pairwise_accuracy == 0.71
        assert perf2.by_position['RB'].pairwise_accuracy == 0.66


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
