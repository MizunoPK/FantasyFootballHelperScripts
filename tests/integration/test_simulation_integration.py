"""
Integration Tests for Simulation Workflow

Tests end-to-end simulation workflows:
- Config generation → Simulation → Results
- Multi-config simulation runs
- Parallel execution
- Error scenarios

Author: Kai Mizuno
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import json

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

# Simulation imports
sys.path.append(str(project_root / "simulation"))
from ConfigGenerator import ConfigGenerator
from SimulationManager import SimulationManager
from ParallelLeagueRunner import ParallelLeagueRunner
from ResultsManager import ResultsManager
from ConfigPerformance import ConfigPerformance


@pytest.fixture
def temp_simulation_data(tmp_path):
    """Create temporary simulation data folder"""
    data_folder = tmp_path / "sim_data"
    data_folder.mkdir()

    # Create minimal players_projected.csv
    players_csv = data_folder / "players_projected.csv"
    players_csv.write_text("""Name,Position,Team,Projected Points,ADP,Injury Status
Patrick Mahomes,QB,KC,350.5,1.2,Healthy
Justin Jefferson,WR,MIN,310.8,2.1,Healthy
Christian McCaffrey,RB,SF,320.1,1.1,Healthy
Travis Kelce,TE,KC,220.4,4.5,Healthy
""")

    # Create minimal players_actual.csv
    players_actual_csv = data_folder / "players_actual.csv"
    players_actual_csv.write_text("""Name,Position,Team,Week 1,Week 2,Week 3
Patrick Mahomes,QB,KC,25.5,22.3,28.1
Justin Jefferson,WR,MIN,18.2,15.4,22.3
Christian McCaffrey,RB,SF,22.1,19.5,25.2
Travis Kelce,TE,KC,12.3,10.2,15.1
""")

    return data_folder


@pytest.fixture
def baseline_config(tmp_path):
    """Create a baseline configuration file"""
    config_path = tmp_path / "baseline_config.json"
    config_data = {
        "config_name": "Test Baseline",
        "description": "Test configuration",
        "projected_points_multiplier": 1.0,
        "adp_multiplier_at_0": 1.5,
        "adp_multiplier_at_50": 1.2,
        "adp_multiplier_at_100": 1.0,
        "adp_multiplier_at_150": 0.8,
        "adp_multiplier_at_200": 0.6,
        "healthy_penalty": 0.0,
        "questionable_penalty": -5.0,
        "doubtful_penalty": -15.0,
        "out_penalty": -100.0,
        "ir_penalty": -100.0
    }
    config_path.write_text(json.dumps(config_data, indent=2))
    return config_path


class TestConfigGeneratorIntegration:
    """Integration tests for config generator"""

    def test_config_generator_loads_baseline(self, baseline_config):
        """Test config generator loads baseline config"""
        generator = ConfigGenerator(baseline_config, num_test_values=3)

        assert generator is not None
        assert generator.baseline_config is not None

    def test_config_generator_creates_combinations(self, baseline_config):
        """Test config generator creates parameter combinations"""
        generator = ConfigGenerator(baseline_config, num_test_values=2)

        combinations = generator.generate_all_combinations()

        # With 2 test values, should generate (2+1)^6 = 729 combinations
        assert len(combinations) > 0

    def test_config_dict_has_required_fields(self, baseline_config):
        """Test generated config dicts have all required fields"""
        generator = ConfigGenerator(baseline_config, num_test_values=1)

        combinations = generator.generate_all_combinations()
        config_dict = generator.create_config_dict(combinations[0])

        # Verify all required fields present
        assert "projected_points_multiplier" in config_dict
        assert "adp_multiplier_at_0" in config_dict


class TestSimulationManagerIntegration:
    """Integration tests for simulation manager"""

    def test_simulation_manager_initializes(self, baseline_config, temp_simulation_data, tmp_path):
        """Test simulation manager initializes successfully"""
        output_dir = tmp_path / "results"

        manager = SimulationManager(
            baseline_config_path=baseline_config,
            output_dir=output_dir,
            num_simulations_per_config=2,
            max_workers=2,
            data_folder=temp_simulation_data,
            num_test_values=2
        )

        assert manager is not None
        assert manager.output_dir == output_dir

    def test_simulation_manager_single_config_test(self, baseline_config, temp_simulation_data, tmp_path):
        """Test simulation manager can run single config test"""
        output_dir = tmp_path / "results"

        manager = SimulationManager(
            baseline_config_path=baseline_config,
            output_dir=output_dir,
            num_simulations_per_config=1,
            max_workers=1,
            data_folder=temp_simulation_data,
            num_test_values=1
        )

        # Run single config test (should not raise exception)
        manager.run_single_config_test()

        # Verify results manager was used
        assert manager.results_manager is not None


class TestParallelLeagueRunnerIntegration:
    """Integration tests for parallel league runner"""

    def test_parallel_runner_initializes(self, temp_simulation_data):
        """Test parallel runner initializes successfully"""
        runner = ParallelLeagueRunner(
            max_workers=2,
            data_folder=temp_simulation_data
        )

        assert runner is not None
        assert runner.max_workers == 2

    def test_parallel_runner_can_run_simulations(self, baseline_config, temp_simulation_data):
        """Test parallel runner can execute simulations"""
        runner = ParallelLeagueRunner(
            max_workers=1,
            data_folder=temp_simulation_data
        )

        # Load baseline config
        with open(baseline_config) as f:
            config_dict = json.load(f)

        # Run a single simulation (should complete without error)
        results = runner.run_simulations_for_config(config_dict, num_simulations=1)

        assert results is not None
        assert len(results) == 1


class TestResultsManagerIntegration:
    """Integration tests for results manager"""

    def test_results_manager_initializes(self):
        """Test results manager initializes"""
        manager = ResultsManager()

        assert manager is not None

    def test_results_manager_registers_config(self, baseline_config):
        """Test results manager can register configs"""
        manager = ResultsManager()

        # Load config
        with open(baseline_config) as f:
            config_dict = json.load(f)

        manager.register_config("test_config_1", config_dict)

        # Should be registered (no exception)
        assert manager is not None

    def test_results_manager_records_results(self, baseline_config):
        """Test results manager can record simulation results"""
        manager = ResultsManager()

        # Load and register config
        with open(baseline_config) as f:
            config_dict = json.load(f)

        manager.register_config("test_config_1", config_dict)

        # Record some results
        manager.record_result("test_config_1", wins=10, losses=4, points=1500.5)
        manager.record_result("test_config_1", wins=9, losses=5, points=1480.2)

        # Get best config
        best = manager.get_best_config()

        assert best is not None
        assert best.config_id == "test_config_1"
        assert best.num_simulations == 2


class TestConfigPerformanceIntegration:
    """Integration tests for config performance tracking"""

    def test_config_performance_initialization(self, baseline_config):
        """Test ConfigPerformance initializes correctly"""
        # Load config
        with open(baseline_config) as f:
            config_dict = json.load(f)

        perf = ConfigPerformance("test_config", config_dict)

        assert perf.config_id == "test_config"
        assert perf.config_dict == config_dict

    def test_config_performance_adds_results(self, baseline_config):
        """Test ConfigPerformance can add simulation results"""
        # Load config
        with open(baseline_config) as f:
            config_dict = json.load(f)

        perf = ConfigPerformance("test_config", config_dict)

        perf.add_result(wins=10, losses=4, points=1500.0)
        perf.add_result(wins=9, losses=5, points=1480.0)

        assert perf.num_simulations == 2
        assert perf.total_wins == 19
        assert perf.total_losses == 9

    def test_config_performance_calculates_win_rate(self, baseline_config):
        """Test ConfigPerformance calculates win rate correctly"""
        # Load config
        with open(baseline_config) as f:
            config_dict = json.load(f)

        perf = ConfigPerformance("test_config", config_dict)

        perf.add_result(wins=10, losses=4, points=1500.0)

        win_rate = perf.get_win_rate()

        # Win rate should be wins / (wins + losses)
        expected_rate = 10 / (10 + 4)
        assert abs(win_rate - expected_rate) < 0.001


class TestEndToEndSimulationWorkflow:
    """End-to-end integration tests for complete simulation workflows"""

    def test_complete_single_simulation_workflow(self, baseline_config, temp_simulation_data, tmp_path):
        """Test complete workflow: init → run single → get results"""
        output_dir = tmp_path / "results"

        # Initialize manager
        manager = SimulationManager(
            baseline_config_path=baseline_config,
            output_dir=output_dir,
            num_simulations_per_config=2,
            max_workers=1,
            data_folder=temp_simulation_data,
            num_test_values=1
        )

        # Run single config test
        manager.run_single_config_test()

        # Verify results were recorded
        best = manager.results_manager.get_best_config()
        assert best is not None
        assert best.num_simulations == 2


class TestErrorHandling:
    """Integration tests for error handling"""

    def test_simulation_handles_missing_data_folder(self, baseline_config):
        """Test simulation handles missing data folder gracefully"""
        nonexistent_path = Path("/nonexistent/sim_data")

        with pytest.raises(Exception):
            SimulationManager(
                baseline_config_path=baseline_config,
                output_dir=Path("/tmp/results"),
                num_simulations_per_config=1,
                max_workers=1,
                data_folder=nonexistent_path
            )

    def test_simulation_handles_invalid_baseline_config(self, tmp_path, temp_simulation_data):
        """Test simulation handles invalid baseline config"""
        # Create invalid config
        invalid_config = tmp_path / "invalid.json"
        invalid_config.write_text("{invalid json")

        with pytest.raises(Exception):
            ConfigGenerator(invalid_config)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
