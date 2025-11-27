"""
Unit tests for ResultsManager module

Tests results aggregation, best config identification, and file saving.

Author: Kai Mizuno
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, mock_open
import json
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))
from simulation.ResultsManager import ResultsManager
from simulation.ConfigPerformance import ConfigPerformance


class TestResultsManagerInitialization:
    """Test ResultsManager initialization"""

    def test_init_empty_results(self):
        """Test initialization creates empty results dict"""
        mgr = ResultsManager()

        assert mgr.results == {}
        assert isinstance(mgr.results, dict)

    def test_init_multiple_instances_independent(self):
        """Test multiple instances are independent"""
        mgr1 = ResultsManager()
        mgr2 = ResultsManager()

        mgr1.register_config("config1", {})

        assert len(mgr1.results) == 1
        assert len(mgr2.results) == 0


class TestRegisterConfig:
    """Test register_config functionality"""

    def test_register_single_config(self):
        """Test registering a single configuration"""
        mgr = ResultsManager()
        config_dict = {'param1': 1.0, 'param2': 2.0}

        mgr.register_config("config_001", config_dict)

        assert "config_001" in mgr.results
        # Verify it's a ConfigPerformance-like object by checking attributes
        assert hasattr(mgr.results["config_001"], 'config_id')
        assert hasattr(mgr.results["config_001"], 'add_league_result')
        assert mgr.results["config_001"].config_id == "config_001"

    def test_register_multiple_configs(self):
        """Test registering multiple configurations"""
        mgr = ResultsManager()

        mgr.register_config("config_001", {'param': 1.0})
        mgr.register_config("config_002", {'param': 2.0})
        mgr.register_config("config_003", {'param': 3.0})

        assert len(mgr.results) == 3
        assert "config_001" in mgr.results
        assert "config_002" in mgr.results
        assert "config_003" in mgr.results

    def test_register_config_overwrites_existing(self):
        """Test registering same config ID overwrites"""
        mgr = ResultsManager()

        mgr.register_config("config_001", {'param': 1.0})
        mgr.record_result("config_001", 10, 7, 1234.56)

        # Register again with different config
        mgr.register_config("config_001", {'param': 2.0})

        # Should have new ConfigPerformance with no results
        assert mgr.results["config_001"].num_simulations == 0


class TestRecordResult:
    """Test record_result functionality"""

    def test_record_single_result(self):
        """Test recording a single simulation result"""
        mgr = ResultsManager()
        mgr.register_config("config_001", {})

        mgr.record_result("config_001", 10, 7, 1234.56)

        config_perf = mgr.results["config_001"]
        assert config_perf.total_wins == 10
        assert config_perf.total_losses == 7
        assert config_perf.total_points == 1234.56
        assert config_perf.num_simulations == 1

    def test_record_multiple_results_same_config(self):
        """Test recording multiple results for same config"""
        mgr = ResultsManager()
        mgr.register_config("config_001", {})

        mgr.record_result("config_001", 10, 7, 1234.56)
        mgr.record_result("config_001", 11, 6, 1345.67)
        mgr.record_result("config_001", 9, 8, 1123.45)

        config_perf = mgr.results["config_001"]
        assert config_perf.total_wins == 30
        assert config_perf.total_losses == 21
        assert config_perf.total_points == pytest.approx(3703.68)
        assert config_perf.num_simulations == 3

    def test_record_result_unregistered_config_raises_error(self):
        """Test recording result for unregistered config raises KeyError"""
        mgr = ResultsManager()

        with pytest.raises(KeyError, match="not registered"):
            mgr.record_result("config_999", 10, 7, 1234.56)

    def test_record_result_zero_wins(self):
        """Test recording result with zero wins"""
        mgr = ResultsManager()
        mgr.register_config("config_001", {})

        mgr.record_result("config_001", 0, 17, 800.00)

        config_perf = mgr.results["config_001"]
        assert config_perf.total_wins == 0
        assert config_perf.get_win_rate() == 0.0

    def test_record_result_perfect_season(self):
        """Test recording result with perfect season (17-0)"""
        mgr = ResultsManager()
        mgr.register_config("config_001", {})

        mgr.record_result("config_001", 17, 0, 2000.00)

        config_perf = mgr.results["config_001"]
        assert config_perf.total_wins == 17
        assert config_perf.get_win_rate() == 1.0


class TestGetBestConfig:
    """Test get_best_config functionality"""

    def test_get_best_config_no_results(self):
        """Test getting best config with no results returns None"""
        mgr = ResultsManager()

        best = mgr.get_best_config()

        assert best is None

    def test_get_best_config_single_config(self):
        """Test getting best config with single config"""
        mgr = ResultsManager()
        mgr.register_config("config_001", {})
        mgr.record_result("config_001", 10, 7, 1234.56)

        best = mgr.get_best_config()

        assert best is not None
        assert best.config_id == "config_001"

    def test_get_best_config_by_win_rate(self):
        """Test best config selected by highest win rate"""
        mgr = ResultsManager()

        # Config 1: 10-7 (58.8% win rate)
        mgr.register_config("config_001", {})
        mgr.record_result("config_001", 10, 7, 1200.00)

        # Config 2: 12-5 (70.6% win rate) - BEST
        mgr.register_config("config_002", {})
        mgr.record_result("config_002", 12, 5, 1300.00)

        # Config 3: 9-8 (52.9% win rate)
        mgr.register_config("config_003", {})
        mgr.record_result("config_003", 9, 8, 1100.00)

        best = mgr.get_best_config()

        assert best.config_id == "config_002"

    def test_get_best_config_tiebreaker_by_points(self):
        """Test best config uses points as tiebreaker when win rates equal"""
        mgr = ResultsManager()

        # Config 1: 10-7, 1200 pts
        mgr.register_config("config_001", {})
        mgr.record_result("config_001", 10, 7, 1200.00)

        # Config 2: 10-7, 1400 pts - BEST (same win rate, higher points)
        mgr.register_config("config_002", {})
        mgr.record_result("config_002", 10, 7, 1400.00)

        best = mgr.get_best_config()

        assert best.config_id == "config_002"

    def test_get_best_config_many_configs(self):
        """Test best config selection with many configs"""
        mgr = ResultsManager()

        # Create 10 configs with varying performance
        for i in range(10):
            mgr.register_config(f"config_{i:03d}", {})
            # Varying win rates from 50% to 95%
            wins = 10 + i
            losses = 17 - wins
            points = 1000.0 + (i * 50)
            mgr.record_result(f"config_{i:03d}", wins, losses, points)

        best = mgr.get_best_config()

        # Config 009 should have highest win rate
        assert best.config_id == "config_009"


class TestGetTopNConfigs:
    """Test get_top_n_configs functionality"""

    def test_get_top_n_configs_empty_results(self):
        """Test get_top_n with no results returns empty list"""
        mgr = ResultsManager()

        top_5 = mgr.get_top_n_configs(5)

        assert top_5 == []

    def test_get_top_n_configs_fewer_than_n(self):
        """Test get_top_n when fewer configs than n"""
        mgr = ResultsManager()

        mgr.register_config("config_001", {})
        mgr.record_result("config_001", 10, 7, 1200.00)

        mgr.register_config("config_002", {})
        mgr.record_result("config_002", 11, 6, 1300.00)

        top_5 = mgr.get_top_n_configs(5)

        assert len(top_5) == 2

    def test_get_top_n_configs_correct_order(self):
        """Test get_top_n returns configs in correct order"""
        mgr = ResultsManager()

        # Create configs with different win rates
        mgr.register_config("worst", {})
        mgr.record_result("worst", 8, 9, 1000.00)

        mgr.register_config("best", {})
        mgr.record_result("best", 13, 4, 1500.00)

        mgr.register_config("middle", {})
        mgr.record_result("middle", 10, 7, 1200.00)

        top_3 = mgr.get_top_n_configs(3)

        assert len(top_3) == 3
        assert top_3[0].config_id == "best"
        assert top_3[1].config_id == "middle"
        assert top_3[2].config_id == "worst"

    def test_get_top_n_configs_default_n(self):
        """Test get_top_n uses default n=10"""
        mgr = ResultsManager()

        # Create 15 configs
        for i in range(15):
            mgr.register_config(f"config_{i:03d}", {})
            mgr.record_result(f"config_{i:03d}", 10, 7, 1200.00)

        top = mgr.get_top_n_configs()  # Default n=10

        assert len(top) == 10


class TestSaveOptimalConfig:
    """Test save_optimal_config functionality"""

    @patch('simulation.ResultsManager.datetime')
    @patch('builtins.open', new_callable=mock_open)
    @patch('pathlib.Path.mkdir')
    def test_save_optimal_config_success(self, mock_mkdir, mock_file, mock_datetime):
        """Test saving optimal config to file"""
        # Mock datetime for consistent filename
        mock_datetime.now.return_value.strftime.return_value = "2024-01-15_10-30-45"

        mgr = ResultsManager()
        mgr.register_config("config_001", {'param1': 1.0, 'param2': 2.0})
        mgr.record_result("config_001", 12, 5, 1400.00)

        output_dir = Path("/test/output")
        result_path = mgr.save_optimal_config(output_dir)

        # Verify directory creation
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

        # Verify file write
        mock_file.assert_called_once()

        # Verify returned path
        assert result_path == output_dir / "optimal_2024-01-15_10-30-45.json"

    def test_save_optimal_config_no_results_raises_error(self):
        """Test saving with no results raises ValueError"""
        mgr = ResultsManager()

        with pytest.raises(ValueError, match="No results available"):
            mgr.save_optimal_config(Path("/test/output"))

    @patch('simulation.ResultsManager.datetime')
    @patch('builtins.open', new_callable=mock_open)
    @patch('pathlib.Path.mkdir')
    def test_save_optimal_config_includes_performance_metrics(self, mock_mkdir, mock_file, mock_datetime):
        """Test saved config includes performance metrics"""
        mock_datetime.now.return_value.strftime.return_value = "2024-01-15_10-30-45"

        mgr = ResultsManager()
        mgr.register_config("config_001", {'param': 1.0})
        mgr.record_result("config_001", 10, 7, 1234.56)

        mgr.save_optimal_config(Path("/test"))

        # Get the data that was written
        written_data = ''.join(call.args[0] for call in mock_file().write.call_args_list)
        saved_config = json.loads(written_data)

        # Verify performance metrics are included
        assert 'performance_metrics' in saved_config
        assert saved_config['performance_metrics']['config_id'] == 'config_001'
        assert saved_config['performance_metrics']['total_wins'] == 10
        assert saved_config['performance_metrics']['total_losses'] == 7


class TestSaveAllResults:
    """Test save_all_results functionality"""

    @patch('builtins.open', new_callable=mock_open)
    @patch('pathlib.Path.mkdir')
    def test_save_all_results_success(self, mock_mkdir, mock_file):
        """Test saving all results to file"""
        mgr = ResultsManager()

        mgr.register_config("config_001", {})
        mgr.record_result("config_001", 10, 7, 1234.56)

        mgr.register_config("config_002", {})
        mgr.record_result("config_002", 11, 6, 1345.67)

        output_path = Path("/test/all_results.json")
        mgr.save_all_results(output_path)

        # Verify parent directory creation
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

        # Verify file write
        mock_file.assert_called_once_with(output_path, 'w')

        # Get written data
        written_data = ''.join(call.args[0] for call in mock_file().write.call_args_list)
        saved_data = json.loads(written_data)

        # Verify structure
        assert 'total_configs' in saved_data
        assert saved_data['total_configs'] == 2
        assert 'configs' in saved_data
        assert 'config_001' in saved_data['configs']
        assert 'config_002' in saved_data['configs']

    @patch('builtins.open', new_callable=mock_open)
    @patch('pathlib.Path.mkdir')
    def test_save_all_results_empty(self, mock_mkdir, mock_file):
        """Test saving all results with no configs"""
        mgr = ResultsManager()

        output_path = Path("/test/empty_results.json")
        mgr.save_all_results(output_path)

        # Verify file was written
        mock_file.assert_called_once()

        # Get written data
        written_data = ''.join(call.args[0] for call in mock_file().write.call_args_list)
        saved_data = json.loads(written_data)

        assert saved_data['total_configs'] == 0
        assert saved_data['configs'] == {}


class TestGetStats:
    """Test get_stats functionality"""

    def test_get_stats_empty_results(self):
        """Test get_stats with no results returns empty dict"""
        mgr = ResultsManager()

        stats = mgr.get_stats()

        assert stats == {}

    def test_get_stats_single_config(self):
        """Test get_stats with single config"""
        mgr = ResultsManager()
        mgr.register_config("config_001", {})
        mgr.record_result("config_001", 10, 7, 1234.56)

        stats = mgr.get_stats()

        assert stats['total_configs'] == 1
        assert stats['min_win_rate'] == stats['max_win_rate']
        assert stats['min_win_rate'] == pytest.approx(10/17)

    def test_get_stats_multiple_configs(self):
        """Test get_stats calculates correct aggregate statistics"""
        mgr = ResultsManager()

        # Config 1: 10-7 (58.8%)
        mgr.register_config("config_001", {})
        mgr.record_result("config_001", 10, 7, 1000.00)

        # Config 2: 12-5 (70.6%)
        mgr.register_config("config_002", {})
        mgr.record_result("config_002", 12, 5, 1500.00)

        # Config 3: 8-9 (47.1%)
        mgr.register_config("config_003", {})
        mgr.record_result("config_003", 8, 9, 900.00)

        stats = mgr.get_stats()

        assert stats['total_configs'] == 3
        assert stats['min_win_rate'] == pytest.approx(8/17)
        assert stats['max_win_rate'] == pytest.approx(12/17)
        assert stats['min_avg_points'] == pytest.approx(900.00)
        assert stats['max_avg_points'] == pytest.approx(1500.00)


class TestPrintSummary:
    """Test print_summary functionality"""

    @patch('builtins.print')
    def test_print_summary_no_results(self, mock_print):
        """Test print summary with no results"""
        mgr = ResultsManager()

        mgr.print_summary()

        # Should print "No results available"
        mock_print.assert_called_with("No results available")

    @patch('builtins.print')
    def test_print_summary_with_results(self, mock_print):
        """Test print summary with results"""
        mgr = ResultsManager()

        mgr.register_config("config_001", {})
        mgr.record_result("config_001", 10, 7, 1234.56)

        mgr.register_config("config_002", {})
        mgr.record_result("config_002", 12, 5, 1400.00)

        mgr.print_summary(top_n=2)

        # Verify print was called multiple times (for the summary)
        assert mock_print.call_count > 5  # Multiple lines printed

    @patch('builtins.print')
    def test_print_summary_custom_top_n(self, mock_print):
        """Test print summary with custom top_n"""
        mgr = ResultsManager()

        for i in range(10):
            mgr.register_config(f"config_{i:03d}", {})
            mgr.record_result(f"config_{i:03d}", 10 + i, 7 - i, 1200.00)

        mgr.print_summary(top_n=5)

        # Should print, but we just verify it doesn't crash
        assert mock_print.called


class TestIntegrationScenarios:
    """Test realistic integration scenarios"""

    def test_realistic_workflow(self):
        """Test realistic workflow with multiple configs and results"""
        mgr = ResultsManager()

        # Register 5 configs
        configs = ["baseline", "variant_a", "variant_b", "variant_c", "variant_d"]
        for config_id in configs:
            mgr.register_config(config_id, {'name': config_id})

        # Run 10 simulations per config with varying results
        import random
        random.seed(42)  # For reproducibility

        for config_id in configs:
            for _ in range(10):
                wins = random.randint(8, 13)
                losses = 17 - wins
                points = random.uniform(1000, 1600)
                mgr.record_result(config_id, wins, losses, points)

        # Get best config
        best = mgr.get_best_config()
        assert best is not None

        # Get top 3
        top_3 = mgr.get_top_n_configs(3)
        assert len(top_3) == 3

        # Get stats
        stats = mgr.get_stats()
        assert stats['total_configs'] == 5

    @patch('builtins.open', new_callable=mock_open)
    @patch('pathlib.Path.mkdir')
    def test_complete_optimization_workflow(self, mock_mkdir, mock_file):
        """Test complete optimization workflow"""
        mgr = ResultsManager()

        # Register configs
        mgr.register_config("config_001", {'param': 1.0})
        mgr.register_config("config_002", {'param': 2.0})

        # Record results
        mgr.record_result("config_001", 10, 7, 1234.56)
        mgr.record_result("config_002", 12, 5, 1345.67)

        # Get best
        best = mgr.get_best_config()
        assert best.config_id == "config_002"

        # Save results
        mgr.save_all_results(Path("/test/results.json"))

        # Verify save was attempted
        assert mock_file.called


class TestUpdateLeagueConfig:
    """Test update_league_config functionality"""

    def test_update_league_config_preserves_required_keys(self, tmp_path):
        """Test that preserved keys are kept from original config"""
        # Create original league config
        original_config = {
            "config_name": "original",
            "description": "Original config",
            "parameters": {
                "CURRENT_NFL_WEEK": 1,
                "NFL_SEASON": 2025,
                "MAX_POSITIONS": {"QB": 2, "RB": 4, "WR": 4},
                "FLEX_ELIGIBLE_POSITIONS": ["RB", "WR", "DST"],
                "NORMALIZATION_MAX_SCALE": 100.0,
                "MATCHUP_SCORING": {
                    "MIN_WEEKS": 5,
                    "IMPACT_SCALE": 50.0,
                    "WEIGHT": 1.0
                },
                "SCHEDULE_SCORING": {
                    "MIN_WEEKS": 3,
                    "IMPACT_SCALE": 75.0,
                    "WEIGHT": 0.5
                }
            }
        }
        league_config_path = tmp_path / "league_config.json"
        with open(league_config_path, 'w') as f:
            json.dump(original_config, f)

        # Create optimal config with different values
        optimal_config = {
            "config_name": "optimal",
            "description": "Win Rate: 0.85",
            "parameters": {
                "CURRENT_NFL_WEEK": 13,
                "NFL_SEASON": 2024,
                "MAX_POSITIONS": {"QB": 3, "RB": 5, "WR": 5},
                "FLEX_ELIGIBLE_POSITIONS": ["RB", "WR"],
                "NORMALIZATION_MAX_SCALE": 150.0,
                "MATCHUP_SCORING": {
                    "MIN_WEEKS": 3,
                    "IMPACT_SCALE": 107.0,
                    "WEIGHT": 0.4
                },
                "SCHEDULE_SCORING": {
                    "MIN_WEEKS": 5,
                    "IMPACT_SCALE": 108.0,
                    "WEIGHT": 0.8
                }
            }
        }
        optimal_config_path = tmp_path / "optimal.json"
        with open(optimal_config_path, 'w') as f:
            json.dump(optimal_config, f)

        # Update league config
        mgr = ResultsManager()
        mgr.update_league_config(optimal_config_path, league_config_path)

        # Read updated config
        with open(league_config_path, 'r') as f:
            updated_config = json.load(f)

        # Verify preserved keys are from original
        assert updated_config["parameters"]["CURRENT_NFL_WEEK"] == 1
        assert updated_config["parameters"]["NFL_SEASON"] == 2025
        assert updated_config["parameters"]["MAX_POSITIONS"] == {"QB": 2, "RB": 4, "WR": 4}
        assert updated_config["parameters"]["FLEX_ELIGIBLE_POSITIONS"] == ["RB", "WR", "DST"]

    def test_update_league_config_copies_other_parameters(self, tmp_path):
        """Test that non-preserved parameters are copied from optimal"""
        # Create original league config
        original_config = {
            "config_name": "original",
            "description": "Original config",
            "parameters": {
                "CURRENT_NFL_WEEK": 1,
                "NFL_SEASON": 2025,
                "MAX_POSITIONS": {"QB": 2},
                "FLEX_ELIGIBLE_POSITIONS": ["RB", "WR"],
                "NORMALIZATION_MAX_SCALE": 100.0,
                "MATCHUP_SCORING": {"MIN_WEEKS": 5, "IMPACT_SCALE": 50.0, "WEIGHT": 1.0},
                "SCHEDULE_SCORING": {"MIN_WEEKS": 3, "IMPACT_SCALE": 75.0, "WEIGHT": 0.5}
            }
        }
        league_config_path = tmp_path / "league_config.json"
        with open(league_config_path, 'w') as f:
            json.dump(original_config, f)

        # Create optimal config
        optimal_config = {
            "config_name": "optimal",
            "description": "Win Rate: 0.80",
            "parameters": {
                "CURRENT_NFL_WEEK": 13,
                "NFL_SEASON": 2024,
                "MAX_POSITIONS": {"QB": 3},
                "FLEX_ELIGIBLE_POSITIONS": ["RB"],
                "NORMALIZATION_MAX_SCALE": 150.0,
                "MATCHUP_SCORING": {"MIN_WEEKS": 3, "IMPACT_SCALE": 107.0, "WEIGHT": 0.4},
                "SCHEDULE_SCORING": {"MIN_WEEKS": 5, "IMPACT_SCALE": 108.0, "WEIGHT": 0.8}
            }
        }
        optimal_config_path = tmp_path / "optimal.json"
        with open(optimal_config_path, 'w') as f:
            json.dump(optimal_config, f)

        # Update league config
        mgr = ResultsManager()
        mgr.update_league_config(optimal_config_path, league_config_path)

        # Read updated config
        with open(league_config_path, 'r') as f:
            updated_config = json.load(f)

        # Verify non-preserved parameter is from optimal
        assert updated_config["parameters"]["NORMALIZATION_MAX_SCALE"] == 150.0

    def test_update_league_config_matchup_to_schedule_mapping(self, tmp_path):
        """Test that MATCHUP_SCORING values are copied to SCHEDULE_SCORING"""
        # Create original league config
        original_config = {
            "config_name": "original",
            "description": "Original",
            "parameters": {
                "CURRENT_NFL_WEEK": 1,
                "NFL_SEASON": 2025,
                "MAX_POSITIONS": {"QB": 2},
                "FLEX_ELIGIBLE_POSITIONS": ["RB", "WR"],
                "MATCHUP_SCORING": {
                    "MIN_WEEKS": 5,
                    "IMPACT_SCALE": 50.0,
                    "THRESHOLDS": {"BASE_POSITION": 0},
                    "MULTIPLIERS": {"GOOD": 1.025},
                    "WEIGHT": 1.0
                },
                "SCHEDULE_SCORING": {
                    "MIN_WEEKS": 3,
                    "IMPACT_SCALE": 75.0,
                    "THRESHOLDS": {"BASE_POSITION": 16},
                    "MULTIPLIERS": {"GOOD": 1.05},
                    "WEIGHT": 0.5
                }
            }
        }
        league_config_path = tmp_path / "league_config.json"
        with open(league_config_path, 'w') as f:
            json.dump(original_config, f)

        # Create optimal config with specific MATCHUP values
        optimal_config = {
            "config_name": "optimal",
            "description": "Win Rate: 0.80",
            "parameters": {
                "CURRENT_NFL_WEEK": 13,
                "NFL_SEASON": 2024,
                "MAX_POSITIONS": {"QB": 2},
                "FLEX_ELIGIBLE_POSITIONS": ["RB"],
                "MATCHUP_SCORING": {
                    "MIN_WEEKS": 3,
                    "IMPACT_SCALE": 107.45,
                    "THRESHOLDS": {"BASE_POSITION": 0},
                    "MULTIPLIERS": {"GOOD": 1.025},
                    "WEIGHT": 0.409
                },
                "SCHEDULE_SCORING": {
                    "MIN_WEEKS": 5,
                    "IMPACT_SCALE": 108.44,
                    "THRESHOLDS": {"BASE_POSITION": 16},
                    "MULTIPLIERS": {"GOOD": 1.05},
                    "WEIGHT": 0.80
                }
            }
        }
        optimal_config_path = tmp_path / "optimal.json"
        with open(optimal_config_path, 'w') as f:
            json.dump(optimal_config, f)

        # Update league config
        mgr = ResultsManager()
        mgr.update_league_config(optimal_config_path, league_config_path)

        # Read updated config
        with open(league_config_path, 'r') as f:
            updated_config = json.load(f)

        # Verify MATCHUP values are copied to SCHEDULE
        schedule = updated_config["parameters"]["SCHEDULE_SCORING"]
        matchup = updated_config["parameters"]["MATCHUP_SCORING"]

        assert schedule["MIN_WEEKS"] == matchup["MIN_WEEKS"] == 3
        assert schedule["IMPACT_SCALE"] == matchup["IMPACT_SCALE"] == 107.45
        assert schedule["WEIGHT"] == matchup["WEIGHT"] == 0.409

        # Verify THRESHOLDS and MULTIPLIERS are NOT copied from MATCHUP
        # (They should remain from optimal's SCHEDULE_SCORING)
        assert schedule["THRESHOLDS"]["BASE_POSITION"] == 16
        assert schedule["MULTIPLIERS"]["GOOD"] == 1.05

    def test_update_league_config_copies_config_name_and_description(self, tmp_path):
        """Test that config_name and description are copied from optimal"""
        # Create original league config
        original_config = {
            "config_name": "original_name",
            "description": "Original description",
            "parameters": {
                "CURRENT_NFL_WEEK": 1,
                "NFL_SEASON": 2025,
                "MAX_POSITIONS": {"QB": 2},
                "FLEX_ELIGIBLE_POSITIONS": ["RB", "WR"],
                "MATCHUP_SCORING": {"MIN_WEEKS": 5, "IMPACT_SCALE": 50.0, "WEIGHT": 1.0},
                "SCHEDULE_SCORING": {"MIN_WEEKS": 3, "IMPACT_SCALE": 75.0, "WEIGHT": 0.5}
            }
        }
        league_config_path = tmp_path / "league_config.json"
        with open(league_config_path, 'w') as f:
            json.dump(original_config, f)

        # Create optimal config
        optimal_config = {
            "config_name": "simulation/optimal_iterative_20251126.json",
            "description": "Win Rate: 0.85",
            "parameters": {
                "CURRENT_NFL_WEEK": 13,
                "NFL_SEASON": 2024,
                "MAX_POSITIONS": {"QB": 2},
                "FLEX_ELIGIBLE_POSITIONS": ["RB"],
                "MATCHUP_SCORING": {"MIN_WEEKS": 3, "IMPACT_SCALE": 107.0, "WEIGHT": 0.4},
                "SCHEDULE_SCORING": {"MIN_WEEKS": 5, "IMPACT_SCALE": 108.0, "WEIGHT": 0.8}
            }
        }
        optimal_config_path = tmp_path / "optimal.json"
        with open(optimal_config_path, 'w') as f:
            json.dump(optimal_config, f)

        # Update league config
        mgr = ResultsManager()
        mgr.update_league_config(optimal_config_path, league_config_path)

        # Read updated config
        with open(league_config_path, 'r') as f:
            updated_config = json.load(f)

        # Verify config_name and description are from optimal
        assert updated_config["config_name"] == "simulation/optimal_iterative_20251126.json"
        assert updated_config["description"] == "Win Rate: 0.85"

    def test_update_league_config_removes_performance_metrics(self, tmp_path):
        """Test that performance_metrics are removed from saved config"""
        # Create original league config
        original_config = {
            "config_name": "original",
            "description": "Original",
            "parameters": {
                "CURRENT_NFL_WEEK": 1,
                "NFL_SEASON": 2025,
                "MAX_POSITIONS": {"QB": 2},
                "FLEX_ELIGIBLE_POSITIONS": ["RB", "WR"],
                "MATCHUP_SCORING": {"MIN_WEEKS": 5, "IMPACT_SCALE": 50.0, "WEIGHT": 1.0},
                "SCHEDULE_SCORING": {"MIN_WEEKS": 3, "IMPACT_SCALE": 75.0, "WEIGHT": 0.5}
            }
        }
        league_config_path = tmp_path / "league_config.json"
        with open(league_config_path, 'w') as f:
            json.dump(original_config, f)

        # Create optimal config with performance_metrics
        optimal_config = {
            "config_name": "optimal",
            "description": "Win Rate: 0.80",
            "parameters": {
                "CURRENT_NFL_WEEK": 13,
                "NFL_SEASON": 2024,
                "MAX_POSITIONS": {"QB": 2},
                "FLEX_ELIGIBLE_POSITIONS": ["RB"],
                "MATCHUP_SCORING": {"MIN_WEEKS": 3, "IMPACT_SCALE": 107.0, "WEIGHT": 0.4},
                "SCHEDULE_SCORING": {"MIN_WEEKS": 5, "IMPACT_SCALE": 108.0, "WEIGHT": 0.8}
            },
            "performance_metrics": {
                "config_id": "config_001",
                "win_rate": 0.8,
                "total_wins": 800,
                "total_losses": 200
            }
        }
        optimal_config_path = tmp_path / "optimal.json"
        with open(optimal_config_path, 'w') as f:
            json.dump(optimal_config, f)

        # Update league config
        mgr = ResultsManager()
        mgr.update_league_config(optimal_config_path, league_config_path)

        # Read updated config
        with open(league_config_path, 'r') as f:
            updated_config = json.load(f)

        # Verify performance_metrics is not present
        assert "performance_metrics" not in updated_config

    def test_update_league_config_handles_missing_preserved_keys(self, tmp_path):
        """Test graceful handling when original config missing preserved keys"""
        # Create original league config WITHOUT all preserved keys
        original_config = {
            "config_name": "original",
            "description": "Original",
            "parameters": {
                "CURRENT_NFL_WEEK": 1,
                # Missing NFL_SEASON, MAX_POSITIONS, FLEX_ELIGIBLE_POSITIONS
                "MATCHUP_SCORING": {"MIN_WEEKS": 5, "IMPACT_SCALE": 50.0, "WEIGHT": 1.0},
                "SCHEDULE_SCORING": {"MIN_WEEKS": 3, "IMPACT_SCALE": 75.0, "WEIGHT": 0.5}
            }
        }
        league_config_path = tmp_path / "league_config.json"
        with open(league_config_path, 'w') as f:
            json.dump(original_config, f)

        # Create optimal config
        optimal_config = {
            "config_name": "optimal",
            "description": "Win Rate: 0.80",
            "parameters": {
                "CURRENT_NFL_WEEK": 13,
                "NFL_SEASON": 2024,
                "MAX_POSITIONS": {"QB": 2},
                "FLEX_ELIGIBLE_POSITIONS": ["RB"],
                "MATCHUP_SCORING": {"MIN_WEEKS": 3, "IMPACT_SCALE": 107.0, "WEIGHT": 0.4},
                "SCHEDULE_SCORING": {"MIN_WEEKS": 5, "IMPACT_SCALE": 108.0, "WEIGHT": 0.8}
            }
        }
        optimal_config_path = tmp_path / "optimal.json"
        with open(optimal_config_path, 'w') as f:
            json.dump(optimal_config, f)

        # Update league config - should not raise error
        mgr = ResultsManager()
        mgr.update_league_config(optimal_config_path, league_config_path)

        # Read updated config
        with open(league_config_path, 'r') as f:
            updated_config = json.load(f)

        # Verify CURRENT_NFL_WEEK was preserved (it existed)
        assert updated_config["parameters"]["CURRENT_NFL_WEEK"] == 1

        # Other preserved keys should be from optimal (since they didn't exist in original)
        assert updated_config["parameters"]["NFL_SEASON"] == 2024
        assert updated_config["parameters"]["MAX_POSITIONS"] == {"QB": 2}
        assert updated_config["parameters"]["FLEX_ELIGIBLE_POSITIONS"] == ["RB"]
