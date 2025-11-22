"""
Unit tests for ParallelLeagueRunner module

Tests multi-threaded simulation execution, progress tracking, and result collection.

Author: Kai Mizuno
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call
import sys
from pathlib import Path
import threading

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))
from simulation.ParallelLeagueRunner import ParallelLeagueRunner


class TestParallelLeagueRunnerInitialization:
    """Test ParallelLeagueRunner initialization"""

    def test_init_default_parameters(self):
        """Test initialization with default parameters"""
        runner = ParallelLeagueRunner()

        assert runner.max_workers == 4
        assert runner.data_folder == Path("simulation/sim_data")
        assert runner.progress_callback is None
        assert isinstance(runner.lock, type(threading.Lock()))

    def test_init_custom_max_workers(self):
        """Test initialization with custom max_workers"""
        runner = ParallelLeagueRunner(max_workers=8)

        assert runner.max_workers == 8

    def test_init_custom_data_folder(self):
        """Test initialization with custom data folder"""
        custom_path = Path("/custom/path/to/data")
        runner = ParallelLeagueRunner(data_folder=custom_path)

        assert runner.data_folder == custom_path

    def test_init_with_progress_callback(self):
        """Test initialization with progress callback"""
        callback = Mock()
        runner = ParallelLeagueRunner(progress_callback=callback)

        assert runner.progress_callback == callback

    def test_init_all_custom_parameters(self):
        """Test initialization with all custom parameters"""
        callback = Mock()
        custom_path = Path("/test/data")

        runner = ParallelLeagueRunner(
            max_workers=12,
            data_folder=custom_path,
            progress_callback=callback
        )

        assert runner.max_workers == 12
        assert runner.data_folder == custom_path
        assert runner.progress_callback == callback

    def test_init_single_worker(self):
        """Test initialization with single worker (edge case)"""
        runner = ParallelLeagueRunner(max_workers=1)

        assert runner.max_workers == 1


class TestRunSingleSimulation:
    """Test run_single_simulation functionality"""

    @patch('simulation.ParallelLeagueRunner.SimulatedLeague')
    def test_run_single_simulation_success(self, mock_league_class):
        """Test successful single simulation run"""
        # Setup mock league
        mock_league = Mock()
        mock_league.get_draft_helper_results.return_value = (10, 7, 1234.56)
        mock_league_class.return_value = mock_league

        runner = ParallelLeagueRunner()
        config = {'test': 'config'}

        result = runner.run_single_simulation(config, simulation_id=1)

        # Verify league was created with correct parameters
        mock_league_class.assert_called_once_with(config, runner.data_folder)

        # Verify draft and season were run
        mock_league.run_draft.assert_called_once()
        mock_league.run_season.assert_called_once()

        # Verify results
        assert result == (10, 7, 1234.56)

    @patch('simulation.ParallelLeagueRunner.SimulatedLeague')
    def test_run_single_simulation_different_results(self, mock_league_class):
        """Test single simulation with different results"""
        mock_league = Mock()
        mock_league.get_draft_helper_results.return_value = (12, 5, 1500.00)
        mock_league_class.return_value = mock_league

        runner = ParallelLeagueRunner()
        config = {}

        result = runner.run_single_simulation(config, simulation_id=5)

        assert result == (12, 5, 1500.00)

    @patch('simulation.ParallelLeagueRunner.SimulatedLeague')
    def test_run_single_simulation_exception_during_draft(self, mock_league_class):
        """Test exception handling during draft"""
        mock_league = Mock()
        mock_league.run_draft.side_effect = Exception("Draft failed")
        mock_league_class.return_value = mock_league

        runner = ParallelLeagueRunner()
        config = {}

        with pytest.raises(Exception, match="Draft failed"):
            runner.run_single_simulation(config, simulation_id=2)

    @patch('simulation.ParallelLeagueRunner.SimulatedLeague')
    def test_run_single_simulation_exception_during_season(self, mock_league_class):
        """Test exception handling during season"""
        mock_league = Mock()
        mock_league.run_season.side_effect = Exception("Season failed")
        mock_league_class.return_value = mock_league

        runner = ParallelLeagueRunner()
        config = {}

        with pytest.raises(Exception, match="Season failed"):
            runner.run_single_simulation(config, simulation_id=3)

    @patch('simulation.ParallelLeagueRunner.SimulatedLeague')
    def test_run_single_simulation_zero_points(self, mock_league_class):
        """Test simulation with zero points (edge case)"""
        mock_league = Mock()
        mock_league.get_draft_helper_results.return_value = (0, 17, 0.0)
        mock_league_class.return_value = mock_league

        runner = ParallelLeagueRunner()
        config = {}

        result = runner.run_single_simulation(config, simulation_id=10)

        assert result == (0, 17, 0.0)


class TestRunSimulationsForConfig:
    """Test run_simulations_for_config functionality"""

    @patch('simulation.ParallelLeagueRunner.SimulatedLeague')
    def test_run_simulations_single_sim(self, mock_league_class):
        """Test running single simulation for config"""
        mock_league = Mock()
        mock_league.get_draft_helper_results.return_value = (10, 7, 1234.56)
        mock_league_class.return_value = mock_league

        runner = ParallelLeagueRunner(max_workers=1)
        config = {}

        results = runner.run_simulations_for_config(config, num_simulations=1)

        assert len(results) == 1
        assert results[0] == (10, 7, 1234.56)

    @patch('simulation.ParallelLeagueRunner.SimulatedLeague')
    def test_run_simulations_multiple_sims(self, mock_league_class):
        """Test running multiple simulations for config"""
        # Return different results for each simulation
        mock_league = Mock()
        mock_league.get_draft_helper_results.side_effect = [
            (10, 7, 1234.56),
            (11, 6, 1345.67),
            (9, 8, 1123.45)
        ]
        mock_league_class.return_value = mock_league

        runner = ParallelLeagueRunner(max_workers=2)
        config = {}

        results = runner.run_simulations_for_config(config, num_simulations=3)

        assert len(results) == 3
        # Results can be in any order due to parallel execution
        assert (10, 7, 1234.56) in results
        assert (11, 6, 1345.67) in results
        assert (9, 8, 1123.45) in results

    @patch('simulation.ParallelLeagueRunner.SimulatedLeague')
    def test_run_simulations_with_progress_callback(self, mock_league_class):
        """Test progress callback is called correctly"""
        mock_league = Mock()
        mock_league.get_draft_helper_results.return_value = (10, 7, 1234.56)
        mock_league_class.return_value = mock_league

        callback = Mock()
        runner = ParallelLeagueRunner(max_workers=1, progress_callback=callback)
        config = {}

        results = runner.run_simulations_for_config(config, num_simulations=3)

        # Progress callback should be called 3 times (once per completed sim)
        assert callback.call_count == 3

        # Check that it was called with correct arguments
        expected_calls = [
            call(1, 3),
            call(2, 3),
            call(3, 3)
        ]
        # Order might vary due to threading, so check all calls are present
        assert len(callback.call_args_list) == 3
        for call_args in callback.call_args_list:
            assert call_args[0][1] == 3  # total is always 3
            assert 1 <= call_args[0][0] <= 3  # completed is between 1 and 3

    @patch('simulation.ParallelLeagueRunner.SimulatedLeague')
    def test_run_simulations_handles_one_failure(self, mock_league_class):
        """Test that one failed simulation doesn't stop others"""
        # Create a list to track which simulation we're on
        call_count = [0]

        def create_league_with_failure(config, data_folder):
            mock_league = Mock()
            sim_num = call_count[0]
            call_count[0] += 1

            # First sim succeeds, second fails, third succeeds
            if sim_num == 0:
                mock_league.get_draft_helper_results.return_value = (10, 7, 1234.56)
            elif sim_num == 1:
                mock_league.get_draft_helper_results.side_effect = Exception("Simulation failed")
            else:
                mock_league.get_draft_helper_results.return_value = (11, 6, 1345.67)

            return mock_league

        mock_league_class.side_effect = create_league_with_failure

        runner = ParallelLeagueRunner(max_workers=1)
        config = {}

        results = runner.run_simulations_for_config(config, num_simulations=3)

        # Should have 2 successful results (1 failed)
        assert len(results) == 2
        # Verify the successful results are present
        assert (10, 7, 1234.56) in results
        assert (11, 6, 1345.67) in results

    @patch('simulation.ParallelLeagueRunner.SimulatedLeague')
    def test_run_simulations_zero_simulations(self, mock_league_class):
        """Test running zero simulations (edge case)"""
        runner = ParallelLeagueRunner()
        config = {}

        results = runner.run_simulations_for_config(config, num_simulations=0)

        assert len(results) == 0
        # SimulatedLeague should never be instantiated
        mock_league_class.assert_not_called()


class TestRunMultipleConfigs:
    """Test run_multiple_configs functionality"""

    @patch('simulation.ParallelLeagueRunner.SimulatedLeague')
    def test_run_multiple_configs_single_config(self, mock_league_class):
        """Test running simulations for single config"""
        mock_league = Mock()
        mock_league.get_draft_helper_results.return_value = (10, 7, 1234.56)
        mock_league_class.return_value = mock_league

        runner = ParallelLeagueRunner(max_workers=1)
        configs = [{'config_name': 'test_config'}]

        results = runner.run_multiple_configs(configs, simulations_per_config=2)

        assert len(results) == 1
        assert 'test_config' in results
        assert len(results['test_config']) == 2

    @patch('simulation.ParallelLeagueRunner.SimulatedLeague')
    def test_run_multiple_configs_multiple_configs(self, mock_league_class):
        """Test running simulations for multiple configs"""
        mock_league = Mock()
        mock_league.get_draft_helper_results.return_value = (10, 7, 1234.56)
        mock_league_class.return_value = mock_league

        runner = ParallelLeagueRunner(max_workers=1)
        configs = [
            {'config_name': 'config1'},
            {'config_name': 'config2'},
            {'config_name': 'config3'}
        ]

        results = runner.run_multiple_configs(configs, simulations_per_config=2)

        assert len(results) == 3
        assert 'config1' in results
        assert 'config2' in results
        assert 'config3' in results
        assert len(results['config1']) == 2
        assert len(results['config2']) == 2
        assert len(results['config3']) == 2

    @patch('simulation.ParallelLeagueRunner.SimulatedLeague')
    def test_run_multiple_configs_default_names(self, mock_league_class):
        """Test configs without explicit names get default names"""
        mock_league = Mock()
        mock_league.get_draft_helper_results.return_value = (10, 7, 1234.56)
        mock_league_class.return_value = mock_league

        runner = ParallelLeagueRunner(max_workers=1)
        configs = [
            {},  # No config_name
            {},  # No config_name
        ]

        results = runner.run_multiple_configs(configs, simulations_per_config=1)

        assert len(results) == 2
        assert 'config_0001' in results
        assert 'config_0002' in results

    @patch('simulation.ParallelLeagueRunner.SimulatedLeague')
    def test_run_multiple_configs_empty_list(self, mock_league_class):
        """Test running with empty config list"""
        runner = ParallelLeagueRunner()
        configs = []

        results = runner.run_multiple_configs(configs, simulations_per_config=5)

        assert len(results) == 0
        mock_league_class.assert_not_called()

    @patch('simulation.ParallelLeagueRunner.SimulatedLeague')
    def test_run_multiple_configs_zero_simulations_per_config(self, mock_league_class):
        """Test running multiple configs with zero simulations each"""
        runner = ParallelLeagueRunner()
        configs = [
            {'config_name': 'config1'},
            {'config_name': 'config2'}
        ]

        results = runner.run_multiple_configs(configs, simulations_per_config=0)

        assert len(results) == 2
        assert len(results['config1']) == 0
        assert len(results['config2']) == 0


class TestTestSingleRun:
    """Test test_single_run functionality"""

    @patch('simulation.ParallelLeagueRunner.SimulatedLeague')
    def test_test_single_run_success(self, mock_league_class):
        """Test single run for debugging/testing"""
        mock_league = Mock()
        mock_league.get_draft_helper_results.return_value = (10, 7, 1234.56)
        mock_league_class.return_value = mock_league

        runner = ParallelLeagueRunner()
        config = {'test': 'config'}

        result = runner.test_single_run(config)

        # Should call run_single_simulation with simulation_id=0
        assert result == (10, 7, 1234.56)
        mock_league_class.assert_called_once_with(config, runner.data_folder)

    @patch('simulation.ParallelLeagueRunner.SimulatedLeague')
    def test_test_single_run_with_exception(self, mock_league_class):
        """Test single run with exception"""
        mock_league = Mock()
        mock_league.run_draft.side_effect = Exception("Test exception")
        mock_league_class.return_value = mock_league

        runner = ParallelLeagueRunner()
        config = {}

        with pytest.raises(Exception, match="Test exception"):
            runner.test_single_run(config)


class TestThreadSafety:
    """Test thread-safety of parallel operations"""

    @patch('simulation.ParallelLeagueRunner.SimulatedLeague')
    def test_progress_callback_thread_safety(self, mock_league_class):
        """Test that progress callback is thread-safe"""
        mock_league = Mock()
        mock_league.get_draft_helper_results.return_value = (10, 7, 1234.56)
        mock_league_class.return_value = mock_league

        # Track callback calls in a thread-safe way
        callback_calls = []
        lock = threading.Lock()

        def thread_safe_callback(completed, total):
            with lock:
                callback_calls.append((completed, total))

        runner = ParallelLeagueRunner(
            max_workers=4,
            progress_callback=thread_safe_callback
        )
        config = {}

        results = runner.run_simulations_for_config(config, num_simulations=10)

        # All simulations should complete
        assert len(results) == 10

        # Callback should be called 10 times
        assert len(callback_calls) == 10

        # All callbacks should have total=10
        for completed, total in callback_calls:
            assert total == 10

        # Completed counts should be 1 through 10 (in some order)
        completed_counts = sorted([completed for completed, _ in callback_calls])
        assert completed_counts == list(range(1, 11))


class TestIntegrationScenarios:
    """Test integration scenarios combining multiple features"""

    @patch('simulation.ParallelLeagueRunner.SimulatedLeague')
    def test_realistic_scenario_small_batch(self, mock_league_class):
        """Test realistic scenario with small batch of simulations"""
        mock_league = Mock()

        # Simulate varying results
        results_sequence = [
            (10, 7, 1234.56),
            (11, 6, 1345.67),
            (9, 8, 1123.45),
            (12, 5, 1456.78),
            (10, 7, 1298.34)
        ]
        mock_league.get_draft_helper_results.side_effect = results_sequence
        mock_league_class.return_value = mock_league

        callback = Mock()
        runner = ParallelLeagueRunner(
            max_workers=2,
            progress_callback=callback
        )
        config = {'num_recommendations': 5}

        results = runner.run_simulations_for_config(config, num_simulations=5)

        # All simulations should complete
        assert len(results) == 5

        # All expected results should be present
        for expected_result in results_sequence:
            assert expected_result in results

        # Progress callback called 5 times
        assert callback.call_count == 5

    @patch('simulation.ParallelLeagueRunner.SimulatedLeague')
    def test_realistic_scenario_multiple_configs(self, mock_league_class):
        """Test realistic scenario with multiple configs"""
        mock_league = Mock()
        mock_league.get_draft_helper_results.return_value = (10, 7, 1234.56)
        mock_league_class.return_value = mock_league

        runner = ParallelLeagueRunner(max_workers=4)
        configs = [
            {'config_name': 'baseline', 'param': 1.0},
            {'config_name': 'variant_a', 'param': 1.5},
            {'config_name': 'variant_b', 'param': 2.0}
        ]

        results = runner.run_multiple_configs(configs, simulations_per_config=3)

        # Each config should have 3 simulations
        assert len(results) == 3
        for config_name in ['baseline', 'variant_a', 'variant_b']:
            assert len(results[config_name]) == 3

    @patch('simulation.ParallelLeagueRunner.SimulatedLeague')
    def test_custom_data_folder_propagation(self, mock_league_class):
        """Test that custom data folder is propagated to SimulatedLeague"""
        mock_league = Mock()
        mock_league.get_draft_helper_results.return_value = (10, 7, 1234.56)
        mock_league_class.return_value = mock_league

        custom_folder = Path("/custom/sim/data")
        runner = ParallelLeagueRunner(
            max_workers=1,
            data_folder=custom_folder
        )
        config = {}

        runner.test_single_run(config)

        # Verify SimulatedLeague was created with custom data folder
        mock_league_class.assert_called_once_with(config, custom_folder)


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    @patch('simulation.ParallelLeagueRunner.SimulatedLeague')
    def test_very_high_worker_count(self, mock_league_class):
        """Test with very high worker count"""
        mock_league = Mock()
        mock_league.get_draft_helper_results.return_value = (10, 7, 1234.56)
        mock_league_class.return_value = mock_league

        # More workers than simulations
        runner = ParallelLeagueRunner(max_workers=100)
        config = {}

        results = runner.run_simulations_for_config(config, num_simulations=5)

        assert len(results) == 5

    @patch('simulation.ParallelLeagueRunner.SimulatedLeague')
    def test_perfect_season_results(self, mock_league_class):
        """Test with perfect season (17-0)"""
        mock_league = Mock()
        mock_league.get_draft_helper_results.return_value = (17, 0, 2000.00)
        mock_league_class.return_value = mock_league

        runner = ParallelLeagueRunner()
        config = {}

        result = runner.run_single_simulation(config, simulation_id=1)

        assert result == (17, 0, 2000.00)

    @patch('simulation.ParallelLeagueRunner.SimulatedLeague')
    def test_winless_season_results(self, mock_league_class):
        """Test with winless season (0-17)"""
        mock_league = Mock()
        mock_league.get_draft_helper_results.return_value = (0, 17, 500.00)
        mock_league_class.return_value = mock_league

        runner = ParallelLeagueRunner()
        config = {}

        result = runner.run_single_simulation(config, simulation_id=1)

        assert result == (0, 17, 500.00)


class TestParallelLeagueRunnerCleanup:
    """Test cleanup behavior for memory management (OOM fix)"""

    @patch('simulation.ParallelLeagueRunner.SimulatedLeague')
    def test_cleanup_called_on_success(self, mock_league_class):
        """Test that cleanup is called on successful simulation"""
        # Arrange: Mock SimulatedLeague with cleanup method
        mock_league = Mock()
        mock_league.get_draft_helper_results.return_value = (10, 7, 1234.56)
        mock_league_class.return_value = mock_league

        runner = ParallelLeagueRunner()

        # Act: Run single simulation
        result = runner.run_single_simulation({}, simulation_id=1)

        # Assert: cleanup() was called exactly once
        mock_league.cleanup.assert_called_once()
        assert result == (10, 7, 1234.56)

    @patch('simulation.ParallelLeagueRunner.SimulatedLeague')
    def test_cleanup_called_on_draft_exception(self, mock_league_class):
        """Test that cleanup is called even when draft raises exception"""
        # Arrange: Mock league that raises exception during draft
        mock_league = Mock()
        mock_league.run_draft.side_effect = Exception("Draft failed")
        mock_league_class.return_value = mock_league

        runner = ParallelLeagueRunner()

        # Act: Run simulation (expect exception)
        with pytest.raises(Exception, match="Draft failed"):
            runner.run_single_simulation({}, simulation_id=1)

        # Assert: cleanup() was STILL called (finally block)
        mock_league.cleanup.assert_called_once()

    @patch('simulation.ParallelLeagueRunner.SimulatedLeague')
    def test_cleanup_called_on_season_exception(self, mock_league_class):
        """Test that cleanup is called even when season raises exception"""
        # Arrange: Mock league that raises exception during season
        mock_league = Mock()
        mock_league.run_season.side_effect = Exception("Season failed")
        mock_league_class.return_value = mock_league

        runner = ParallelLeagueRunner()

        # Act: Run simulation (expect exception)
        with pytest.raises(Exception, match="Season failed"):
            runner.run_single_simulation({}, simulation_id=1)

        # Assert: cleanup() was STILL called (finally block)
        mock_league.cleanup.assert_called_once()

    @patch('simulation.ParallelLeagueRunner.gc')
    @patch('simulation.ParallelLeagueRunner.SimulatedLeague')
    def test_gc_forced_every_10_simulations(self, mock_league_class, mock_gc):
        """Test that GC is forced every GC_FREQUENCY simulations"""
        # Arrange: Mock successful simulations
        mock_league = Mock()
        mock_league.get_draft_helper_results.return_value = (10, 7, 1234.56)
        mock_league_class.return_value = mock_league

        runner = ParallelLeagueRunner(max_workers=1)

        # Act: Run 25 simulations
        results = runner.run_simulations_for_config({}, num_simulations=25)

        # Assert: gc.collect() called at 5, 10, 15, 20, 25 (5 times total with GC_FREQUENCY=5)
        assert mock_gc.collect.call_count == 5
        assert len(results) == 25

    @patch('simulation.ParallelLeagueRunner.gc')
    @patch('simulation.ParallelLeagueRunner.SimulatedLeague')
    def test_gc_not_called_for_less_than_gc_frequency(self, mock_league_class, mock_gc):
        """Test that GC is not called when simulations < GC_FREQUENCY"""
        # Arrange
        mock_league = Mock()
        mock_league.get_draft_helper_results.return_value = (10, 7, 1234.56)
        mock_league_class.return_value = mock_league

        runner = ParallelLeagueRunner(max_workers=1)

        # Act: Run only 4 simulations (less than GC_FREQUENCY=5)
        results = runner.run_simulations_for_config({}, num_simulations=4)

        # Assert: gc.collect() never called (no 5th simulation)
        mock_gc.collect.assert_not_called()
        assert len(results) == 4
