"""
Tests for AccuracySimulationManager

Tests the orchestration of accuracy simulation.

Author: Kai Mizuno
"""

import json
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys
import tempfile
import shutil

# Add simulation/accuracy to path
sys.path.append(str(Path(__file__).parent.parent.parent / "simulation" / "accuracy"))
from AccuracySimulationManager import AccuracySimulationManager


# Test parameter order - mirrors the PARAMETER_ORDER in run_accuracy_simulation.py
# These affect how projected points are calculated (prediction params)
# NOTE: PLAYER_RATING_SCORING_WEIGHT is excluded because the consuming mode
# (StarterHelperModeManager) has player_rating=False, so it has no effect.
TEST_PARAMETER_ORDER = [
    'NORMALIZATION_MAX_SCALE',
    'TEAM_QUALITY_SCORING_WEIGHT',
    'TEAM_QUALITY_MIN_WEEKS',
    'PERFORMANCE_SCORING_WEIGHT',
    'PERFORMANCE_SCORING_STEPS',
    'PERFORMANCE_MIN_WEEKS',
    'MATCHUP_IMPACT_SCALE',
    'MATCHUP_SCORING_WEIGHT',
    'MATCHUP_MIN_WEEKS',
    'TEMPERATURE_IMPACT_SCALE',
    'TEMPERATURE_SCORING_WEIGHT',
    'WIND_IMPACT_SCALE',
    'WIND_SCORING_WEIGHT',
    'LOCATION_HOME',
    'LOCATION_AWAY',
    'LOCATION_INTERNATIONAL',
]


class TestAccuracyParameterOrder:
    """Tests for accuracy parameter definitions."""

    def test_parameter_order_contains_expected_params(self):
        """Test that test parameter order contains expected prediction params."""
        expected = [
            'NORMALIZATION_MAX_SCALE',
            'TEAM_QUALITY_SCORING_WEIGHT',
            'MATCHUP_IMPACT_SCALE',
            'MATCHUP_SCORING_WEIGHT',
        ]
        for param in expected:
            assert param in TEST_PARAMETER_ORDER

    def test_parameter_order_excludes_strategy_params(self):
        """Test that test parameter order excludes win-rate strategy params."""
        # These are strategy params optimized by win-rate sim, not accuracy
        strategy_params = [
            'SAME_POS_BYE_WEIGHT',
            'DIFF_POS_BYE_WEIGHT',
            'PRIMARY_BONUS',
            'SECONDARY_BONUS',
            'ADP_SCORING_WEIGHT',
            'DRAFT_ORDER_FILE',
        ]
        for param in strategy_params:
            assert param not in TEST_PARAMETER_ORDER

    def test_parameter_order_excludes_unused_params(self):
        """Test that params disabled in consuming mode are excluded."""
        # PLAYER_RATING_SCORING_WEIGHT is excluded because StarterHelperModeManager
        # has player_rating=False, so optimizing it has no effect
        unused_params = [
            'PLAYER_RATING_SCORING_WEIGHT',
        ]
        for param in unused_params:
            assert param not in TEST_PARAMETER_ORDER

    def test_parameter_order_count(self):
        """Test that we have 16 accuracy parameters."""
        assert len(TEST_PARAMETER_ORDER) == 16


class TestAccuracySimulationManagerInit:
    """Tests for AccuracySimulationManager initialization."""

    @pytest.fixture
    def mock_baseline_config(self, tmp_path):
        """Create a mock baseline config file."""
        config = {
            'config_name': 'test_config',
            'description': 'Test config',
            'parameters': {
                'NORMALIZATION_MAX_SCALE': 150,
                'DRAFT_NORMALIZATION_MAX_SCALE': 163,
                'PLAYER_RATING_SCORING': {'WEIGHT': 1.0},
            }
        }
        config_path = tmp_path / "baseline.json"
        with open(config_path, 'w') as f:
            json.dump(config, f)
        return config_path

    @pytest.fixture
    def mock_data_folder(self, tmp_path):
        """Create a mock data folder with season structure."""
        data_folder = tmp_path / "sim_data"
        data_folder.mkdir()

        # Create a season folder
        season_folder = data_folder / "2024"
        season_folder.mkdir()

        weeks_folder = season_folder / "weeks"
        weeks_folder.mkdir()

        # Create week folders with minimal files
        for week in range(1, 18):
            week_folder = weeks_folder / f"week_{week:02d}"
            week_folder.mkdir()

            # Create minimal CSV files
            (week_folder / "players.csv").write_text("id,name\n1,Player1\n")
            (week_folder / "players_projected.csv").write_text("id,name\n1,Player1\n")

        return data_folder

    @patch('AccuracySimulationManager.ConfigGenerator')
    @patch('AccuracySimulationManager.AccuracyCalculator')
    @patch('AccuracySimulationManager.AccuracyResultsManager')
    def test_initialization(
        self,
        mock_results_mgr,
        mock_calculator,
        mock_config_gen,
        mock_baseline_config,
        mock_data_folder,
        tmp_path
    ):
        """Test manager initialization."""
        output_dir = tmp_path / "output"

        manager = AccuracySimulationManager(
            baseline_config_path=mock_baseline_config,
            output_dir=output_dir,
            data_folder=mock_data_folder,
            parameter_order=TEST_PARAMETER_ORDER,
            num_test_values=5
        )

        assert manager.baseline_config_path == mock_baseline_config
        assert manager.output_dir == output_dir
        assert manager.data_folder == mock_data_folder
        assert manager.parameter_order == TEST_PARAMETER_ORDER
        assert manager.num_test_values == 5

    @patch('AccuracySimulationManager.ConfigGenerator')
    @patch('AccuracySimulationManager.AccuracyCalculator')
    @patch('AccuracySimulationManager.AccuracyResultsManager')
    def test_discover_seasons(
        self,
        mock_results_mgr,
        mock_calculator,
        mock_config_gen,
        mock_baseline_config,
        mock_data_folder,
        tmp_path
    ):
        """Test season discovery."""
        output_dir = tmp_path / "output"

        manager = AccuracySimulationManager(
            baseline_config_path=mock_baseline_config,
            output_dir=output_dir,
            data_folder=mock_data_folder,
            parameter_order=TEST_PARAMETER_ORDER
        )

        assert len(manager.available_seasons) == 1
        assert manager.available_seasons[0].name == "2024"

    @patch('AccuracySimulationManager.ConfigGenerator')
    @patch('AccuracySimulationManager.AccuracyCalculator')
    @patch('AccuracySimulationManager.AccuracyResultsManager')
    def test_discover_seasons_multiple(
        self,
        mock_results_mgr,
        mock_calculator,
        mock_config_gen,
        mock_baseline_config,
        mock_data_folder,
        tmp_path
    ):
        """Test discovery of multiple seasons."""
        # Add another season
        season_2023 = mock_data_folder / "2023"
        season_2023.mkdir()
        (season_2023 / "weeks").mkdir()

        output_dir = tmp_path / "output"
        manager = AccuracySimulationManager(
            baseline_config_path=mock_baseline_config,
            output_dir=output_dir,
            data_folder=mock_data_folder,
            parameter_order=TEST_PARAMETER_ORDER
        )

        assert len(manager.available_seasons) == 2
        assert manager.available_seasons[0].name == "2023"
        assert manager.available_seasons[1].name == "2024"

    @patch('AccuracySimulationManager.ConfigGenerator')
    @patch('AccuracySimulationManager.AccuracyCalculator')
    @patch('AccuracySimulationManager.AccuracyResultsManager')
    def test_discover_seasons_no_valid_seasons_raises(
        self,
        mock_results_mgr,
        mock_calculator,
        mock_config_gen,
        mock_baseline_config,
        tmp_path
    ):
        """Test that missing seasons raises error."""
        empty_data_folder = tmp_path / "empty_data"
        empty_data_folder.mkdir()

        output_dir = tmp_path / "output"

        with pytest.raises(ValueError) as exc_info:
            AccuracySimulationManager(
                baseline_config_path=mock_baseline_config,
                output_dir=output_dir,
                data_folder=empty_data_folder,
                parameter_order=TEST_PARAMETER_ORDER
            )

        assert "No valid season folders found" in str(exc_info.value)


class TestAccuracySimulationManagerSignalHandlers:
    """Tests for signal handling."""

    @pytest.fixture
    def mock_baseline_config(self, tmp_path):
        """Create a mock baseline config file."""
        config = {'config_name': 'test'}
        config_path = tmp_path / "baseline.json"
        with open(config_path, 'w') as f:
            json.dump(config, f)
        return config_path

    @pytest.fixture
    def mock_data_folder(self, tmp_path):
        """Create minimal data folder."""
        data_folder = tmp_path / "sim_data" / "2024" / "weeks"
        data_folder.mkdir(parents=True)
        return tmp_path / "sim_data"

    @patch('AccuracySimulationManager.ConfigGenerator')
    @patch('AccuracySimulationManager.AccuracyCalculator')
    @patch('AccuracySimulationManager.AccuracyResultsManager')
    @patch('signal.signal')
    def test_setup_signal_handlers(
        self,
        mock_signal,
        mock_results_mgr,
        mock_calculator,
        mock_config_gen,
        mock_baseline_config,
        mock_data_folder,
        tmp_path
    ):
        """Test signal handler setup."""
        output_dir = tmp_path / "output"

        manager = AccuracySimulationManager(
            baseline_config_path=mock_baseline_config,
            output_dir=output_dir,
            data_folder=mock_data_folder,
            parameter_order=TEST_PARAMETER_ORDER
        )

        manager._setup_signal_handlers()

        # Verify signal.signal was called for SIGINT and SIGTERM
        assert mock_signal.call_count >= 2


class TestAccuracySimulationManagerDataLoading:
    """Tests for data loading helpers."""

    @pytest.fixture
    def manager_with_data(self, tmp_path):
        """Create manager with mock data folder."""
        # Create config
        config = {'config_name': 'test'}
        config_path = tmp_path / "baseline.json"
        with open(config_path, 'w') as f:
            json.dump(config, f)

        # Create data folder
        data_folder = tmp_path / "sim_data"
        data_folder.mkdir()

        season = data_folder / "2024"
        season.mkdir()
        weeks = season / "weeks"
        weeks.mkdir()

        for week in [1, 2, 5]:  # Only some weeks
            week_folder = weeks / f"week_{week:02d}"
            week_folder.mkdir()
            (week_folder / "players.csv").write_text("id,name\n1,Test\n")
            (week_folder / "players_projected.csv").write_text("id,name\n1,Test\n")

        output_dir = tmp_path / "output"

        with patch('AccuracySimulationManager.ConfigGenerator'), \
             patch('AccuracySimulationManager.AccuracyCalculator'), \
             patch('AccuracySimulationManager.AccuracyResultsManager'):
            return AccuracySimulationManager(
                baseline_config_path=config_path,
                output_dir=output_dir,
                data_folder=data_folder,
                parameter_order=TEST_PARAMETER_ORDER
            )

    def test_load_season_data_existing_week(self, manager_with_data):
        """Test loading data for an existing week."""
        season_path = manager_with_data.available_seasons[0]
        projected, actual = manager_with_data._load_season_data(season_path, 1)

        assert projected is not None
        assert actual is not None
        assert projected.exists()
        assert actual.exists()

    def test_load_season_data_missing_week(self, manager_with_data):
        """Test loading data for a missing week returns None."""
        season_path = manager_with_data.available_seasons[0]
        projected, actual = manager_with_data._load_season_data(season_path, 10)

        assert projected is None
        assert actual is None

    def test_load_season_data_returns_two_folders(self, tmp_path):
        """Test that _load_season_data returns two different folders (week_N and week_N+1)."""
        # Create config
        config = {'config_name': 'test'}
        config_path = tmp_path / "baseline.json"
        with open(config_path, 'w') as f:
            json.dump(config, f)

        # Create data folder with week_01, week_02, week_17, week_18
        data_folder = tmp_path / "sim_data"
        data_folder.mkdir()
        season = data_folder / "2024"
        season.mkdir()
        weeks = season / "weeks"
        weeks.mkdir()

        for week_num in [1, 2, 17, 18]:
            week_folder = weeks / f"week_{week_num:02d}"
            week_folder.mkdir()

        output_dir = tmp_path / "output"

        with patch('AccuracySimulationManager.ConfigGenerator'), \
             patch('AccuracySimulationManager.AccuracyCalculator'), \
             patch('AccuracySimulationManager.AccuracyResultsManager'):
            manager = AccuracySimulationManager(
                baseline_config_path=config_path,
                output_dir=output_dir,
                data_folder=data_folder,
                parameter_order=TEST_PARAMETER_ORDER
            )

        season_path = manager.available_seasons[0]

        # Test week 1: should return (week_01, week_02)
        projected, actual = manager._load_season_data(season_path, 1)
        assert projected is not None
        assert actual is not None
        assert projected.name == "week_01"
        assert actual.name == "week_02"
        assert projected != actual  # Different folders

        # Test week 17: should return (week_17, week_18)
        projected, actual = manager._load_season_data(season_path, 17)
        assert projected is not None
        assert actual is not None
        assert projected.name == "week_17"
        assert actual.name == "week_18"
        assert projected != actual  # Different folders

    def test_load_season_data_handles_missing_actual_folder(self, tmp_path):
        """Test that _load_season_data handles missing week_N+1 folder gracefully."""
        # Create config
        config = {'config_name': 'test'}
        config_path = tmp_path / "baseline.json"
        with open(config_path, 'w') as f:
            json.dump(config, f)

        # Create data folder with week_18 but NO week_19
        data_folder = tmp_path / "sim_data"
        data_folder.mkdir()
        season = data_folder / "2024"
        season.mkdir()
        weeks = season / "weeks"
        weeks.mkdir()

        week_18 = weeks / "week_18"
        week_18.mkdir()
        # week_19 intentionally NOT created

        output_dir = tmp_path / "output"

        with patch('AccuracySimulationManager.ConfigGenerator'), \
             patch('AccuracySimulationManager.AccuracyCalculator'), \
             patch('AccuracySimulationManager.AccuracyResultsManager'):
            manager = AccuracySimulationManager(
                baseline_config_path=config_path,
                output_dir=output_dir,
                data_folder=data_folder,
                parameter_order=TEST_PARAMETER_ORDER
            )

        season_path = manager.available_seasons[0]

        # Test missing actual folder (week_19) - should return (None, None) gracefully
        projected, actual = manager._load_season_data(season_path, 18)

        # Should return (None, None)
        assert projected is None
        assert actual is None

        # No exception should be raised (test passes if we get here)
        # Note: Warning IS logged (visible in test output), but logger not captured by caplog

    def test_load_season_data_handles_missing_projected_folder(self, tmp_path):
        """Test that _load_season_data handles missing week_N folder gracefully."""
        # Create config
        config = {'config_name': 'test'}
        config_path = tmp_path / "baseline.json"
        with open(config_path, 'w') as f:
            json.dump(config, f)

        # Create data folder with NO week_01
        data_folder = tmp_path / "sim_data"
        data_folder.mkdir()
        season = data_folder / "2024"
        season.mkdir()
        weeks = season / "weeks"
        weeks.mkdir()
        # week_01 intentionally NOT created

        output_dir = tmp_path / "output"

        with patch('AccuracySimulationManager.ConfigGenerator'), \
             patch('AccuracySimulationManager.AccuracyCalculator'), \
             patch('AccuracySimulationManager.AccuracyResultsManager'):
            manager = AccuracySimulationManager(
                baseline_config_path=config_path,
                output_dir=output_dir,
                data_folder=data_folder,
                parameter_order=TEST_PARAMETER_ORDER
            )

        season_path = manager.available_seasons[0]

        # Test missing projected folder (week_01) - should return (None, None) gracefully
        projected, actual = manager._load_season_data(season_path, 1)

        # Should return (None, None)
        assert projected is None
        assert actual is None

        # No exception should be raised (test passes if we get here)
        # Note: Warning IS logged (visible in test output), but logger not captured by caplog


    def test_evaluate_config_weekly_uses_two_player_managers(self, tmp_path):
        """Test that _evaluate_config_weekly creates TWO PlayerManager instances (projected and actual)."""
        # Create config
        config = {'config_name': 'test', 'parameters': {}}
        config_path = tmp_path / "baseline.json"
        with open(config_path, 'w') as f:
            json.dump(config, f)

        # Create data folder with week_01 and week_02
        data_folder = tmp_path / "sim_data"
        data_folder.mkdir()
        season = data_folder / "2024"
        season.mkdir()
        weeks = season / "weeks"
        weeks.mkdir()

        for week_num in [1, 2]:
            week_folder = weeks / f"week_{week_num:02d}"
            week_folder.mkdir()

        output_dir = tmp_path / "output"

        # Mock the accuracy calculator methods
        mock_calc = MagicMock()
        mock_calc.calculate_weekly_mae.return_value = MagicMock(mae=5.0)
        mock_calc.calculate_ranking_metrics_for_season.return_value = ({}, {})

        with patch('AccuracySimulationManager.ConfigGenerator'), \
             patch('AccuracySimulationManager.AccuracyCalculator', return_value=mock_calc), \
             patch('AccuracySimulationManager.AccuracyResultsManager'):
            manager = AccuracySimulationManager(
                baseline_config_path=config_path,
                output_dir=output_dir,
                data_folder=data_folder,
                parameter_order=TEST_PARAMETER_ORDER
            )

        season_path = manager.available_seasons[0]

        # Mock _create_player_manager to track calls
        mock_projected_mgr = MagicMock()
        mock_actual_mgr = MagicMock()
        mock_projected_mgr.players = []
        mock_actual_mgr.players = []
        mock_projected_mgr.calculate_max_weekly_projection.return_value = 100.0

        call_count = [0]
        def create_manager_side_effect(config_dict, week_folder, season_path):
            call_count[0] += 1
            if call_count[0] == 1:
                return mock_projected_mgr
            else:
                return mock_actual_mgr

        with patch.object(manager, '_create_player_manager', side_effect=create_manager_side_effect) as mock_create:
            with patch.object(manager, '_cleanup_player_manager') as mock_cleanup:
                # Call _evaluate_config_weekly for week 1
                result = manager._evaluate_config_weekly(config, (1, 1))

        # Verify _create_player_manager called TWICE (once for projected, once for actual)
        assert mock_create.call_count == 2, f"Expected 2 calls to _create_player_manager, got {mock_create.call_count}"

        # Verify first call used week_01 (projected_path)
        first_call_folder = mock_create.call_args_list[0][0][1]
        assert first_call_folder.name == "week_01", f"First call should use week_01, got {first_call_folder.name}"

        # Verify second call used week_02 (actual_path)
        second_call_folder = mock_create.call_args_list[1][0][1]
        assert second_call_folder.name == "week_02", f"Second call should use week_02, got {second_call_folder.name}"

        # Verify both managers cleaned up
        assert mock_cleanup.call_count == 2, f"Expected 2 cleanup calls, got {mock_cleanup.call_count}"


class TestAccuracySimulationManagerResumeState:
    """Tests for resume state detection."""

    @pytest.fixture
    def manager_with_output(self, tmp_path):
        """Create manager with output directory for resume testing."""
        # Create config
        config = {'config_name': 'test'}
        config_path = tmp_path / "baseline.json"
        with open(config_path, 'w') as f:
            json.dump(config, f)

        # Create data folder
        data_folder = tmp_path / "sim_data"
        data_folder.mkdir()
        season = data_folder / "2024"
        season.mkdir()
        weeks = season / "weeks"
        weeks.mkdir()

        output_dir = tmp_path / "output"
        output_dir.mkdir()

        with patch('AccuracySimulationManager.ConfigGenerator'), \
             patch('AccuracySimulationManager.AccuracyCalculator'), \
             patch('AccuracySimulationManager.AccuracyResultsManager'):
            manager = AccuracySimulationManager(
                baseline_config_path=config_path,
                output_dir=output_dir,
                data_folder=data_folder,
                parameter_order=TEST_PARAMETER_ORDER
            )
            return manager

    def test_detect_resume_no_folders(self, manager_with_output):
        """Test resume detection with no intermediate folders."""
        should_resume, start_idx, path = manager_with_output._detect_resume_state('weekly')

        assert should_resume is False
        assert start_idx == 0
        assert path is None

    def test_detect_resume_with_valid_folder(self, manager_with_output):
        """Test resume detection with valid intermediate folder."""
        # Create an intermediate folder with a valid config file
        intermediate = manager_with_output.output_dir / "accuracy_intermediate_02_TEAM_QUALITY_SCORING_WEIGHT"
        intermediate.mkdir()
        (intermediate / "week1-5.json").write_text('{"config_name": "test", "parameters": {}, "performance_metrics": {"mae": 10.5}}')

        should_resume, start_idx, path = manager_with_output._detect_resume_state('weekly')

        assert should_resume is True
        assert start_idx == 3  # Next parameter after index 2
        assert path == intermediate

    def test_detect_resume_with_weekly_prefix(self, manager_with_output):
        """Test resume detection with weekly prefix in folder name."""
        # Create folder with week range prefix
        intermediate = manager_with_output.output_dir / "accuracy_intermediate_01_week1-5_TEAM_QUALITY_SCORING_WEIGHT"
        intermediate.mkdir()
        (intermediate / "week1-5.json").write_text('{"config_name": "test", "parameters": {}, "performance_metrics": {"mae": 10.5}}')

        should_resume, start_idx, path = manager_with_output._detect_resume_state('weekly')

        assert should_resume is True
        assert start_idx == 2  # Next parameter after index 1

    def test_detect_resume_incomplete_folder(self, manager_with_output):
        """Test resume detection skips folders without best.json files."""
        # Create folder without best.json
        intermediate = manager_with_output.output_dir / "accuracy_intermediate_01_TEAM_QUALITY_SCORING_WEIGHT"
        intermediate.mkdir()
        # No *_best.json file

        should_resume, start_idx, path = manager_with_output._detect_resume_state('weekly')

        assert should_resume is False
        assert start_idx == 0
        assert path is None

    def test_detect_resume_all_params_complete(self, manager_with_output):
        """Test resume detection when all parameters are complete."""
        # Create folder for last parameter
        last_param = TEST_PARAMETER_ORDER[-1]
        last_idx = len(TEST_PARAMETER_ORDER) - 1
        intermediate = manager_with_output.output_dir / f"accuracy_intermediate_{last_idx:02d}_{last_param}"
        intermediate.mkdir()
        (intermediate / "week1-5_best.json").write_text('{"mae": 10.5}')

        should_resume, start_idx, path = manager_with_output._detect_resume_state('weekly')

        # All params complete, should start fresh
        assert should_resume is False
        assert start_idx == 0

    def test_detect_resume_ros_mode(self, manager_with_output):
        """Test resume detection in ROS mode."""
        # Create ROS-style intermediate folder (no week prefix)
        intermediate = manager_with_output.output_dir / "accuracy_intermediate_03_TEAM_QUALITY_MIN_WEEKS"
        intermediate.mkdir()
        # Use standard config file (week1-5.json for week_1_5 mode)
        (intermediate / "week1-5.json").write_text('{"config_name": "test", "parameters": {}, "performance_metrics": {"mae": 10.5}}')

        should_resume, start_idx, path = manager_with_output._detect_resume_state('ros')

        assert should_resume is True
        assert start_idx == 4  # Next parameter after index 3

    def test_detect_resume_invalid_folder_name(self, manager_with_output):
        """Test resume detection ignores folders with invalid names."""
        # Create folder with invalid name format
        invalid = manager_with_output.output_dir / "accuracy_intermediate_invalid"
        invalid.mkdir()
        (invalid / "week1-5.json").write_text('{"config_name": "test", "parameters": {}, "performance_metrics": {"mae": 10.5}}')

        should_resume, start_idx, path = manager_with_output._detect_resume_state('weekly')

        assert should_resume is False
        assert start_idx == 0

    def test_detect_resume_unknown_param(self, manager_with_output):
        """Test resume detection ignores folders with unknown parameter names."""
        # Create folder with unknown parameter
        unknown = manager_with_output.output_dir / "accuracy_intermediate_01_UNKNOWN_PARAM"
        unknown.mkdir()
        (unknown / "week1-5_best.json").write_text('{"mae": 10.5}')

        should_resume, start_idx, path = manager_with_output._detect_resume_state('weekly')

        assert should_resume is False
        assert start_idx == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
