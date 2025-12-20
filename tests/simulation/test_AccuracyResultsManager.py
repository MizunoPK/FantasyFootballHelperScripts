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
        assert perf.config_id is not None
        assert perf.timestamp is not None

    def test_config_performance_with_id(self):
        """Test creating with explicit config_id."""
        perf = AccuracyConfigPerformance(
            config_dict={},
            mae=5.0,
            player_count=100,
            total_error=500.0,
            config_id="test123"
        )

        assert perf.config_id == "test123"

    def test_is_better_than_lower_mae(self):
        """Test that lower MAE is better."""
        perf1 = AccuracyConfigPerformance(
            config_dict={}, mae=4.0, player_count=100, total_error=400.0
        )
        perf2 = AccuracyConfigPerformance(
            config_dict={}, mae=5.0, player_count=100, total_error=500.0
        )

        assert perf1.is_better_than(perf2)
        assert not perf2.is_better_than(perf1)

    def test_is_better_than_none(self):
        """Test comparison with None."""
        perf = AccuracyConfigPerformance(
            config_dict={}, mae=5.0, player_count=100, total_error=500.0
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
            config_id="abc123"
        )

        data = original.to_dict()
        restored = AccuracyConfigPerformance.from_dict(data)

        assert restored.config_dict == original.config_dict
        assert restored.mae == original.mae
        assert restored.player_count == original.player_count
        assert restored.config_id == original.config_id

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
        for filename in ['draft_config.json', 'week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']:
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
        assert 'ros' in manager.best_configs
        assert 'week_1_5' in manager.best_configs
        assert manager.best_configs['ros'] is None

    def test_add_result_first_is_best(self, results_manager):
        """Test that first result is automatically best."""
        config = {'test': 'config'}
        accuracy_result = AccuracyResult(mae=5.0, player_count=100, total_error=500.0)

        is_best = results_manager.add_result('ros', config, accuracy_result)

        assert is_best
        assert results_manager.best_configs['ros'] is not None
        assert results_manager.best_configs['ros'].mae == 5.0

    def test_add_result_better_replaces(self, results_manager):
        """Test that better result replaces current best."""
        config1 = {'version': 1}
        config2 = {'version': 2}
        result1 = AccuracyResult(mae=5.0, player_count=100, total_error=500.0)
        result2 = AccuracyResult(mae=3.0, player_count=100, total_error=300.0)

        results_manager.add_result('ros', config1, result1)
        is_best = results_manager.add_result('ros', config2, result2)

        assert is_best
        assert results_manager.best_configs['ros'].mae == 3.0
        assert results_manager.best_configs['ros'].config_dict == config2

    def test_add_result_worse_does_not_replace(self, results_manager):
        """Test that worse result does not replace best."""
        config1 = {'version': 1}
        config2 = {'version': 2}
        result1 = AccuracyResult(mae=3.0, player_count=100, total_error=300.0)
        result2 = AccuracyResult(mae=5.0, player_count=100, total_error=500.0)

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
        result = AccuracyResult(mae=5.0, player_count=100, total_error=500.0)
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
        # Add results for ROS and one week range
        # Use real WEEK_SPECIFIC_PARAMS parameters with nested structure
        config_ros = {'TEAM_QUALITY_SCORING': {'WEIGHT': 1.5}}
        config_week = {'MATCHUP_SCORING': {'WEIGHT': 1.2}}
        result = AccuracyResult(mae=5.0, player_count=100, total_error=500.0)

        results_manager.add_result('ros', config_ros, result)
        results_manager.add_result('week_1_5', config_week, result)

        # Save
        optimal_path = results_manager.save_optimal_configs()

        # Verify folder created
        assert optimal_path.exists()
        assert optimal_path.name.startswith("accuracy_optimal_")

        # Verify all files created (league_config.json + 5 prediction configs)
        # No separate performance_metrics.json - metrics are embedded in each config
        assert (optimal_path / "league_config.json").exists()  # Copied from baseline
        assert (optimal_path / "draft_config.json").exists()
        assert (optimal_path / "week1-5.json").exists()

        # Verify draft_config.json has proper nested structure
        with open(optimal_path / "draft_config.json") as f:
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
        result = AccuracyResult(mae=5.0, player_count=100, total_error=500.0)
        results_manager.add_result('ros', config, result)

        intermediate_path = results_manager.save_intermediate_results(0, 'NORMALIZATION')

        assert intermediate_path.exists()
        assert "accuracy_intermediate_00_NORMALIZATION" in intermediate_path.name
        # Standard config files (can be used as baseline and for resume)
        assert (intermediate_path / "league_config.json").exists()
        assert (intermediate_path / "draft_config.json").exists()
        # Week files copied from baseline since no results for them
        assert (intermediate_path / "week1-5.json").exists()
        # Metadata file for tournament mode tracking (new in Phase 2)
        assert (intermediate_path / "metadata.json").exists()
        # Config files + metadata.json = 7 files
        all_files = list(intermediate_path.glob("*.json"))
        assert len(all_files) == 7  # league_config + draft_config + 4 week files + metadata.json

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
                'config_id': 'test123'
            }
        }
        with open(intermediate_path / "draft_config.json", 'w') as f:
            json.dump(config_data, f)

        # Load
        success = results_manager.load_intermediate_results(intermediate_path)

        assert success
        assert results_manager.best_configs['ros'] is not None
        assert results_manager.best_configs['ros'].mae == 5.0

    def test_load_intermediate_results_not_found(self, results_manager, temp_dir):
        """Test loading from non-existent folder."""
        success = results_manager.load_intermediate_results(temp_dir / "nonexistent")
        assert not success

    def test_get_summary(self, results_manager):
        """Test getting results summary."""
        config = {'test': 'config'}
        result = AccuracyResult(mae=5.0, player_count=100, total_error=500.0)
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
        result1 = AccuracyResult(mae=68.0, player_count=100, total_error=6800.0)
        result2 = AccuracyResult(mae=3.8, player_count=100, total_error=380.0)

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
        for filename in ['league_config.json', 'draft_config.json', 'week1-5.json',
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
        result = AccuracyResult(mae=5.0, player_count=100, total_error=500.0)
        results_manager.add_result('ros', config, result)

        optimal_path = results_manager.save_optimal_configs()

        with open(optimal_path / "draft_config.json") as f:
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
        result = AccuracyResult(mae=5.0, player_count=100, total_error=500.0)
        results_manager.add_result('ros', config, result)

        intermediate_path = results_manager.save_intermediate_results(0, 'TEST')

        # Check the standard config file (draft_config.json for 'ros')
        with open(intermediate_path / "draft_config.json") as f:
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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
