"""
Comprehensive Unit Tests for SimulationManager

Tests all functionality of the SimulationManager class including:
- Initialization with different configurations
- Full optimization (grid search)
- Iterative optimization (coordinate descent)
- Single config testing
- Result saving and file generation
- Error handling

Author: Kai Mizuno
Date: 2025
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, call
import sys

# Add simulation directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "simulation"))
from SimulationManager import SimulationManager


# Module-level fixtures (shared across all test classes)
@pytest.fixture
def temp_baseline_config():
    """Create a temporary baseline config file"""
    config = {
        "config_name": "test_baseline",
        "parameters": {
            "NORMALIZATION_MAX_SCALE": 100.0,
            "SAME_POS_BYE_WEIGHT": 1.0,
            "DIFF_POS_BYE_WEIGHT": 1.0,
            "DRAFT_ORDER_BONUSES": {"PRIMARY": 50.0, "SECONDARY": 40.0}
        }
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config, f)
        temp_path = Path(f.name)

    yield temp_path
    temp_path.unlink()


@pytest.fixture
def temp_output_dir():
    """Create a temporary output directory"""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    # Cleanup
    for file in temp_dir.glob('*'):
        file.unlink()
    temp_dir.rmdir()


@pytest.fixture
def temp_data_folder():
    """Create a temporary data folder"""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    temp_dir.rmdir()


class TestSimulationManagerInitialization:
    """Test SimulationManager initialization"""

    def test_initialization_success(self, temp_baseline_config, temp_output_dir, temp_data_folder):
        """Test successful initialization"""
        manager = SimulationManager(
            baseline_config_path=temp_baseline_config,
            output_dir=temp_output_dir,
            num_simulations_per_config=5,
            max_workers=4,
            data_folder=temp_data_folder,
            num_test_values=2
        )

        assert manager.baseline_config_path == temp_baseline_config
        assert manager.output_dir == temp_output_dir
        assert manager.num_simulations_per_config == 5
        assert manager.max_workers == 4
        assert manager.num_test_values == 2

    def test_initialization_creates_output_dir(self, temp_baseline_config, temp_data_folder):
        """Test that output directory is created if it doesn't exist"""
        output_dir = Path(tempfile.mkdtemp()) / "nonexistent_dir"

        try:
            manager = SimulationManager(
                baseline_config_path=temp_baseline_config,
                output_dir=output_dir,
                num_simulations_per_config=5,
                max_workers=4,
                data_folder=temp_data_folder
            )

            assert output_dir.exists()
        finally:
            if output_dir.exists():
                output_dir.rmdir()
                output_dir.parent.rmdir()

    def test_initialization_components_created(self, temp_baseline_config, temp_output_dir, temp_data_folder):
        """Test that all components are initialized"""
        manager = SimulationManager(
            baseline_config_path=temp_baseline_config,
            output_dir=temp_output_dir,
            num_simulations_per_config=5,
            max_workers=4,
            data_folder=temp_data_folder
        )

        assert hasattr(manager, 'config_generator')
        assert hasattr(manager, 'parallel_runner')
        assert hasattr(manager, 'results_manager')


class TestSingleConfigTest:
    """Test run_single_config_test method"""

    @pytest.fixture
    def mock_manager(self, temp_baseline_config, temp_output_dir, temp_data_folder):
        """Create a SimulationManager with mocked dependencies"""
        with patch('SimulationManager.ConfigGenerator') as MockConfigGenerator, \
             patch('SimulationManager.ParallelLeagueRunner') as MockParallelRunner, \
             patch('SimulationManager.ResultsManager') as MockResultsManager:

            # Setup mocks
            mock_config_gen = MockConfigGenerator.return_value
            mock_config_gen.baseline_config = {"config_name": "test", "parameters": {}}

            mock_parallel = MockParallelRunner.return_value
            mock_parallel.run_simulations_for_config.return_value = [
                (10, 7, 1404.62),
                (12, 5, 1523.45),
                (9, 8, 1380.22)
            ]

            # Create mock config performance with proper return values
            mock_best_config = Mock()
            mock_best_config.config_id = "test_config"
            mock_best_config.num_simulations = 3
            mock_best_config.total_wins = 31
            mock_best_config.total_losses = 20
            mock_best_config.total_games = 51
            mock_best_config.get_win_rate.return_value = 0.608
            mock_best_config.get_avg_points_per_league.return_value = 1436.10

            mock_results = MockResultsManager.return_value
            mock_results.get_best_config.return_value = mock_best_config

            manager = SimulationManager(
                baseline_config_path=temp_baseline_config,
                output_dir=temp_output_dir,
                num_simulations_per_config=3,
                max_workers=4,
                data_folder=temp_data_folder
            )

            return manager, mock_results, mock_parallel

    def test_run_single_config_test_registers_config(self, mock_manager):
        """Test that config is registered with ResultsManager"""
        manager, mock_results, mock_parallel = mock_manager

        manager.run_single_config_test()

        # Verify config was registered
        assert mock_results.register_config.called

    def test_run_single_config_test_runs_simulations(self, mock_manager):
        """Test that simulations are run"""
        manager, mock_results, mock_parallel = mock_manager

        manager.run_single_config_test()

        # Verify simulations were run
        assert mock_parallel.run_simulations_for_config.called
        assert mock_parallel.run_simulations_for_config.call_count == 1

    def test_run_single_config_test_records_results(self, mock_manager):
        """Test that results are recorded"""
        manager, mock_results, mock_parallel = mock_manager

        manager.run_single_config_test()

        # Verify results were recorded (3 results)
        assert mock_results.record_result.call_count == 3


class TestFullOptimization:
    """Test run_full_optimization method"""

    @pytest.fixture
    def mock_manager_for_full(self, temp_baseline_config, temp_output_dir, temp_data_folder):
        """Create a SimulationManager with mocked dependencies for full optimization"""
        with patch('SimulationManager.ConfigGenerator') as MockConfigGenerator, \
             patch('SimulationManager.ParallelLeagueRunner') as MockParallelRunner, \
             patch('SimulationManager.ResultsManager') as MockResultsManager:

            # Setup mocks
            mock_config_gen = MockConfigGenerator.return_value
            mock_config_gen.baseline_config = {"config_name": "test", "parameters": {}}

            # Mock combinations (use small number for testing)
            mock_config_gen.generate_all_combinations.return_value = [
                {"NORMALIZATION_MAX_SCALE": 100.0, "SAME_POS_BYE_WEIGHT": 1.0,
            "DIFF_POS_BYE_WEIGHT": 1.0},
                {"NORMALIZATION_MAX_SCALE": 110.0, "SAME_POS_BYE_WEIGHT": 1.0,
            "DIFF_POS_BYE_WEIGHT": 1.0}
            ]

            mock_config_gen.create_config_dict.side_effect = lambda combo: {
                "config_name": "test",
                "parameters": combo
            }

            mock_parallel = MockParallelRunner.return_value
            mock_parallel.run_simulations_for_config.return_value = [
                (10, 7, 1404.62)
            ]

            mock_results = MockResultsManager.return_value
            mock_results.save_optimal_config.return_value = temp_output_dir / "optimal_test.json"
            mock_results.save_all_results.return_value = None

            manager = SimulationManager(
                baseline_config_path=temp_baseline_config,
                output_dir=temp_output_dir,
                num_simulations_per_config=1,
                max_workers=2,
                data_folder=temp_data_folder,
                num_test_values=1  # Will create 2^6 = 64 configs (but we mock to 2)
            )

            return manager, mock_results, mock_parallel, mock_config_gen

    def test_full_optimization_generates_combinations(self, mock_manager_for_full):
        """Test that combinations are generated"""
        manager, mock_results, mock_parallel, mock_config_gen = mock_manager_for_full

        manager.run_full_optimization()

        # Verify combinations were generated
        assert mock_config_gen.generate_all_combinations.called

    def test_full_optimization_registers_all_configs(self, mock_manager_for_full):
        """Test that all configs are registered"""
        manager, mock_results, mock_parallel, mock_config_gen = mock_manager_for_full

        manager.run_full_optimization()

        # Should register 2 configs (mocked)
        assert mock_results.register_config.call_count == 2

    def test_full_optimization_runs_all_simulations(self, mock_manager_for_full):
        """Test that simulations are run for all configs"""
        manager, mock_results, mock_parallel, mock_config_gen = mock_manager_for_full

        manager.run_full_optimization()

        # Should run simulations for 2 configs
        assert mock_parallel.run_simulations_for_config.call_count == 2

    def test_full_optimization_saves_results(self, mock_manager_for_full):
        """Test that optimal config and all results are saved"""
        manager, mock_results, mock_parallel, mock_config_gen = mock_manager_for_full

        optimal_path = manager.run_full_optimization()

        # Verify results were saved
        assert mock_results.save_optimal_config.called
        assert mock_results.save_all_results.called
        assert optimal_path is not None


class TestIterativeOptimization:
    """Test run_iterative_optimization method"""

    @pytest.fixture
    def mock_manager_for_iterative(self, temp_baseline_config, temp_output_dir, temp_data_folder):
        """Create a SimulationManager with mocked dependencies for iterative optimization"""
        with patch('SimulationManager.ConfigGenerator') as MockConfigGenerator, \
             patch('SimulationManager.ParallelLeagueRunner') as MockParallelRunner, \
             patch('SimulationManager.ResultsManager') as MockResultsManager:

            # Setup mocks
            mock_config_gen = MockConfigGenerator.return_value
            mock_config_gen.baseline_config = {"config_name": "test", "parameters": {"NORMALIZATION_MAX_SCALE": 100.0}}
            mock_config_gen.PARAMETER_ORDER = ['NORMALIZATION_MAX_SCALE', 'BASE_BYE_PENALTY']  # Only 2 for testing

            # Mock iterative combinations
            mock_config_gen.generate_iterative_combinations.return_value = [
                {"config_name": "test1", "parameters": {"NORMALIZATION_MAX_SCALE": 100.0}},
                {"config_name": "test2", "parameters": {"NORMALIZATION_MAX_SCALE": 110.0}}
            ]

            mock_parallel = MockParallelRunner.return_value
            mock_parallel.run_simulations_for_config.return_value = [
                (10, 7, 1404.62)
            ]

            # Mock ResultsManager
            mock_results_class = MockResultsManager
            mock_results_instance = Mock()

            # Create mock config performance
            mock_best_config = Mock()
            mock_best_config.get_win_rate.return_value = 0.60
            mock_best_config.get_avg_points_per_league.return_value = 1400.0
            mock_best_config.total_wins = 10
            mock_best_config.total_losses = 7
            mock_best_config.config_dict = {"config_name": "best", "parameters": {"NORMALIZATION_MAX_SCALE": 110.0}}

            mock_results_instance.get_best_config.return_value = mock_best_config
            mock_results_class.return_value = mock_results_instance

            manager = SimulationManager(
                baseline_config_path=temp_baseline_config,
                output_dir=temp_output_dir,
                num_simulations_per_config=1,
                max_workers=2,
                data_folder=temp_data_folder,
                num_test_values=1
            )

            # Replace the results_manager with our properly mocked one
            manager.results_manager = mock_results_instance

            return manager, mock_results_instance, mock_parallel, mock_config_gen

    def test_iterative_optimization_iterates_through_parameters(self, mock_manager_for_iterative):
        """Test that optimization iterates through all parameters"""
        manager, mock_results, mock_parallel, mock_config_gen = mock_manager_for_iterative

        manager.run_iterative_optimization()

        # Should generate configs for each parameter (2 parameters in PARAMETER_ORDER)
        assert mock_config_gen.generate_iterative_combinations.call_count == 2

    def test_iterative_optimization_runs_simulations_for_each_param(self, mock_manager_for_iterative):
        """Test that simulations are run for each parameter's configs"""
        manager, mock_results, mock_parallel, mock_config_gen = mock_manager_for_iterative

        manager.run_iterative_optimization()

        # Should run simulations for 2 configs per parameter × 2 parameters = 4 times
        assert mock_parallel.run_simulations_for_config.call_count == 4

    def test_iterative_optimization_updates_optimal_config(self, mock_manager_for_iterative, temp_output_dir):
        """Test that optimal config is saved and intermediate configs exist"""
        manager, mock_results, mock_parallel, mock_config_gen = mock_manager_for_iterative

        optimal_path = manager.run_iterative_optimization()

        # Verify optimization completed and saved final optimal config
        assert optimal_path.exists()
        assert 'optimal_iterative' in optimal_path.name

        # Verify intermediate configs were created
        intermediate_files = list(temp_output_dir.glob("intermediate_*.json"))
        assert len(intermediate_files) >= 2  # One per parameter

    def test_iterative_optimization_saves_intermediate_configs(self, mock_manager_for_iterative, temp_output_dir):
        """Test that intermediate configs are saved"""
        manager, mock_results, mock_parallel, mock_config_gen = mock_manager_for_iterative

        manager.run_iterative_optimization()

        # Check that intermediate files were created
        intermediate_files = list(temp_output_dir.glob("intermediate_*.json"))
        assert len(intermediate_files) == 2  # One per parameter

    def test_iterative_optimization_saves_final_optimal(self, mock_manager_for_iterative, temp_output_dir):
        """Test that final optimal config is saved"""
        manager, mock_results, mock_parallel, mock_config_gen = mock_manager_for_iterative

        optimal_path = manager.run_iterative_optimization()

        # Verify final optimal config exists
        assert optimal_path.exists()
        assert 'optimal_iterative' in optimal_path.name

    def test_iterative_optimization_cleans_up_old_intermediate_files(self, mock_manager_for_iterative, temp_output_dir):
        """Test that intermediate files are cleaned up when starting fresh (not resuming)"""
        manager, mock_results, mock_parallel, mock_config_gen = mock_manager_for_iterative

        # Create intermediate files that will be detected as completed run
        # (param_idx > PARAMETER_ORDER length causes cleanup)
        old_intermediate_1 = temp_output_dir / "intermediate_01_OLD_PARAM.json"
        old_intermediate_2 = temp_output_dir / "intermediate_99_ANOTHER_OLD.json"
        old_intermediate_1.write_text('{"old": "config1"}')
        old_intermediate_2.write_text('{"old": "config2"}')

        # Verify old files exist
        assert old_intermediate_1.exists()
        assert old_intermediate_2.exists()

        # Run optimization - should cleanup because files are from completed/invalid run
        manager.run_iterative_optimization()

        # Verify old intermediate files were deleted
        assert not old_intermediate_1.exists()
        assert not old_intermediate_2.exists()

        # Verify new intermediate files were created
        new_intermediate_files = list(temp_output_dir.glob("intermediate_*.json"))
        assert len(new_intermediate_files) == 2  # One per parameter in mock

        # Verify new files don't have the old names
        new_file_names = [f.name for f in new_intermediate_files]
        assert "intermediate_01_OLD_PARAM.json" not in new_file_names
        assert "intermediate_99_ANOTHER_OLD.json" not in new_file_names


class TestResumeDetection:
    """Test resume detection functionality"""

    @pytest.fixture
    def manager(self, temp_baseline_config, temp_output_dir, temp_data_folder):
        """Create a SimulationManager for testing resume detection"""
        with patch('SimulationManager.ConfigGenerator') as MockConfigGenerator, \
             patch('SimulationManager.ParallelLeagueRunner') as MockParallelRunner, \
             patch('SimulationManager.ResultsManager') as MockResultsManager:

            # Setup mocks
            mock_config_gen = MockConfigGenerator.return_value
            mock_config_gen.baseline_config = {
                "config_name": "test",
                "parameters": {"NORMALIZATION_MAX_SCALE": 100.0}
            }
            mock_config_gen.PARAMETER_ORDER = [
                'NORMALIZATION_MAX_SCALE',
                'SAME_POS_BYE_WEIGHT',
                'DIFF_POS_BYE_WEIGHT',
                'PRIMARY_BONUS'
            ]

            manager = SimulationManager(
                baseline_config_path=temp_baseline_config,
                output_dir=temp_output_dir,
                num_simulations_per_config=1,
                max_workers=2,
                data_folder=temp_data_folder,
                num_test_values=1
            )

            return manager

    def test_detect_resume_state_no_files(self, manager):
        """Test resume detection with no intermediate files"""
        should_resume, start_idx, last_path = manager._detect_resume_state()

        assert should_resume is False
        assert start_idx == 0
        assert last_path is None

    def test_detect_resume_state_partial_run(self, manager, temp_output_dir):
        """Test resume detection with partial run (2 of 4 parameters complete)"""
        # Create valid intermediate files
        config = {"config_name": "test", "parameters": {"NORMALIZATION_MAX_SCALE": 100.0}}
        file1 = temp_output_dir / "intermediate_01_NORMALIZATION_MAX_SCALE.json"
        file2 = temp_output_dir / "intermediate_02_SAME_POS_BYE_WEIGHT.json"
        file1.write_text(json.dumps(config))
        file2.write_text(json.dumps(config))

        should_resume, start_idx, last_path = manager._detect_resume_state()

        assert should_resume is True
        assert start_idx == 2  # Resume from index 2 (3rd parameter)
        assert last_path == file2

    def test_detect_resume_state_completed_run(self, manager, temp_output_dir):
        """Test resume detection with all parameters complete"""
        # Create intermediate files for all 4 parameters
        config = {"config_name": "test", "parameters": {"NORMALIZATION_MAX_SCALE": 100.0}}
        for i in range(1, 5):
            param_name = manager.config_generator.PARAMETER_ORDER[i-1]
            file = temp_output_dir / f"intermediate_{i:02d}_{param_name}.json"
            file.write_text(json.dumps(config))

        should_resume, start_idx, last_path = manager._detect_resume_state()

        # All parameters complete - should NOT resume
        assert should_resume is False
        assert start_idx == 0
        assert last_path is None

    def test_detect_resume_state_corrupted_json(self, manager, temp_output_dir):
        """Test resume detection skips corrupted JSON files"""
        # Create one valid file and one corrupted file
        valid_config = {"config_name": "test", "parameters": {"NORMALIZATION_MAX_SCALE": 100.0}}
        file1 = temp_output_dir / "intermediate_01_NORMALIZATION_MAX_SCALE.json"
        file2 = temp_output_dir / "intermediate_02_SAME_POS_BYE_WEIGHT.json"
        file1.write_text(json.dumps(valid_config))
        file2.write_text("{ invalid json }")  # Corrupted

        should_resume, start_idx, last_path = manager._detect_resume_state()

        # Should skip corrupted file and use highest valid (file1)
        assert should_resume is True
        assert start_idx == 1  # Resume from index 1 (2nd parameter)
        assert last_path == file1

    def test_detect_resume_state_missing_fields(self, manager, temp_output_dir):
        """Test resume detection skips files with missing required fields"""
        # Create file with missing 'parameters' field
        invalid_config = {"config_name": "test"}  # Missing 'parameters'
        file1 = temp_output_dir / "intermediate_01_NORMALIZATION_MAX_SCALE.json"
        file1.write_text(json.dumps(invalid_config))

        should_resume, start_idx, last_path = manager._detect_resume_state()

        # Should skip invalid file
        assert should_resume is False
        assert start_idx == 0
        assert last_path is None

    def test_detect_resume_state_parameter_order_mismatch(self, manager, temp_output_dir):
        """Test resume detection with parameter order mismatch"""
        # Create file with wrong parameter name at index 1
        config = {"config_name": "test", "parameters": {"NORMALIZATION_MAX_SCALE": 100.0}}
        file1 = temp_output_dir / "intermediate_01_WRONG_PARAM.json"
        file1.write_text(json.dumps(config))

        should_resume, start_idx, last_path = manager._detect_resume_state()

        # Should detect mismatch and NOT resume
        assert should_resume is False
        assert start_idx == 0
        assert last_path is None

    def test_detect_resume_state_invalid_filename_format(self, manager, temp_output_dir):
        """Test resume detection skips files with invalid filename format"""
        # Create file with invalid name format
        config = {"config_name": "test", "parameters": {"NORMALIZATION_MAX_SCALE": 100.0}}
        file1 = temp_output_dir / "invalid_filename.json"
        file1.write_text(json.dumps(config))

        should_resume, start_idx, last_path = manager._detect_resume_state()

        # Should skip invalid filename
        assert should_resume is False
        assert start_idx == 0
        assert last_path is None

    def test_detect_resume_state_param_idx_exceeds_order(self, manager, temp_output_dir):
        """Test resume detection when param_idx exceeds PARAMETER_ORDER length"""
        # Create file with idx beyond parameter count (idx=99 > 4 parameters)
        config = {"config_name": "test", "parameters": {"NORMALIZATION_MAX_SCALE": 100.0}}
        file1 = temp_output_dir / "intermediate_99_EXTRA_PARAM.json"
        file1.write_text(json.dumps(config))

        should_resume, start_idx, last_path = manager._detect_resume_state()

        # Should treat as completed run
        assert should_resume is False
        assert start_idx == 0
        assert last_path is None


class TestTimeFormatting:
    """Test time formatting helper method"""

    @pytest.fixture
    def manager(self, temp_baseline_config, temp_output_dir, temp_data_folder):
        """Create a basic SimulationManager"""
        return SimulationManager(
            baseline_config_path=temp_baseline_config,
            output_dir=temp_output_dir,
            num_simulations_per_config=1,
            max_workers=1,
            data_folder=temp_data_folder
        )

    def test_format_time_seconds(self, manager):
        """Test formatting for < 60 seconds"""
        formatted = manager._format_time(45.7)
        assert formatted == "45s"

    def test_format_time_minutes(self, manager):
        """Test formatting for minutes"""
        formatted = manager._format_time(125.3)  # 2 min 5 sec
        assert formatted == "2m 5s"

    def test_format_time_hours(self, manager):
        """Test formatting for hours"""
        formatted = manager._format_time(3725.0)  # 1 hour 2 minutes
        assert formatted == "1h 2m"
