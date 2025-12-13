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


# ============================================================================
# Test: Per-Week-Range Methods
# ============================================================================

class TestPerWeekRangeMethods:
    """Tests for week-by-week config optimization methods."""

    def create_sample_week_results(self, wins_early=3, wins_mid_early=2, wins_mid_late=2, wins_late=3):
        """
        Create sample week results for testing.

        Returns a list of (week, won, points) tuples simulating a 16-week season.
        Allows customizing wins per range for testing different scenarios.
        Week ranges: 1-5, 6-9, 10-13, 14-17
        """
        week_results = []
        # Weeks 1-5 (early season)
        for week in range(1, 6):
            won = (week <= wins_early)
            week_results.append((week, won, 100.0 + week))
        # Weeks 6-9 (mid-early season)
        for week in range(6, 10):
            won = (week - 5 <= wins_mid_early)
            week_results.append((week, won, 110.0 + week))
        # Weeks 10-13 (mid-late season)
        for week in range(10, 14):
            won = (week - 9 <= wins_mid_late)
            week_results.append((week, won, 120.0 + week))
        # Weeks 14-17 (late season)
        for week in range(14, 18):
            won = (week - 13 <= wins_late)
            week_results.append((week, won, 130.0 + week))
        return week_results

    def test_record_week_results_success(self):
        """record_week_results should update config with per-week data."""
        mgr = ResultsManager()
        config_dict = {"config_name": "test", "parameters": {}}
        mgr.register_config("config_0001", config_dict)

        week_results = self.create_sample_week_results(wins_early=3, wins_mid_early=2, wins_mid_late=2, wins_late=3)
        mgr.record_week_results("config_0001", week_results)

        config = mgr.results["config_0001"]
        assert config.num_simulations == 1
        assert config.total_wins == 10  # 3 + 2 + 2 + 3
        assert config.total_losses == 7  # (5-3) + (4-2) + (4-2) + (4-3) = 2 + 2 + 2 + 1 = 7

    def test_record_week_results_unregistered_config_raises_error(self):
        """record_week_results should raise KeyError for unregistered config."""
        mgr = ResultsManager()
        week_results = self.create_sample_week_results()

        with pytest.raises(KeyError, match="Config .* not registered"):
            mgr.record_week_results("unregistered", week_results)

    def test_record_week_results_multiple_simulations(self):
        """record_week_results should accumulate across multiple simulations."""
        mgr = ResultsManager()
        config_dict = {"config_name": "test", "parameters": {}}
        mgr.register_config("config_0001", config_dict)

        # Run two simulations
        week_results_1 = self.create_sample_week_results(wins_early=3, wins_mid_early=2, wins_mid_late=2, wins_late=3)
        week_results_2 = self.create_sample_week_results(wins_early=2, wins_mid_early=1, wins_mid_late=1, wins_late=2)

        mgr.record_week_results("config_0001", week_results_1)
        mgr.record_week_results("config_0001", week_results_2)

        config = mgr.results["config_0001"]
        assert config.num_simulations == 2
        assert config.total_wins == 10 + 6  # (3+2+2+3) + (2+1+1+2) = 16
        assert config.total_losses == 7 + 11  # (2+2+2+1) + (3+3+3+2) = 18

    def test_get_best_config_for_range_returns_best_for_early_season(self):
        """get_best_config_for_range should return config with best win rate for range."""
        mgr = ResultsManager()

        # Config A: Good early season (4/5 wins), bad late (1/4 wins)
        mgr.register_config("config_A", {"config_name": "A", "parameters": {}})
        mgr.record_week_results("config_A", self.create_sample_week_results(wins_early=4, wins_mid_early=2, wins_mid_late=2, wins_late=1))

        # Config B: Bad early season (2/5 wins), good late (4/4 wins)
        mgr.register_config("config_B", {"config_name": "B", "parameters": {}})
        mgr.record_week_results("config_B", self.create_sample_week_results(wins_early=2, wins_mid_early=2, wins_mid_late=2, wins_late=4))

        best_early = mgr.get_best_config_for_range("1-5")
        assert best_early.config_id == "config_A"

    def test_get_best_config_for_range_returns_best_for_late_season(self):
        """get_best_config_for_range should correctly identify best late season config."""
        mgr = ResultsManager()

        # Config A: Good early season (4/5 wins), bad late (1/4 wins)
        mgr.register_config("config_A", {"config_name": "A", "parameters": {}})
        mgr.record_week_results("config_A", self.create_sample_week_results(wins_early=4, wins_mid_early=2, wins_mid_late=2, wins_late=1))

        # Config B: Bad early season (2/5 wins), good late (4/4 wins)
        mgr.register_config("config_B", {"config_name": "B", "parameters": {}})
        mgr.record_week_results("config_B", self.create_sample_week_results(wins_early=2, wins_mid_early=2, wins_mid_late=2, wins_late=4))

        best_late = mgr.get_best_config_for_range("14-17")
        assert best_late.config_id == "config_B"

    def test_get_best_config_for_range_no_results(self):
        """get_best_config_for_range should return None when no results."""
        mgr = ResultsManager()
        result = mgr.get_best_config_for_range("1-5")
        assert result is None

    def test_get_best_config_for_range_invalid_range_raises_error(self):
        """get_best_config_for_range should raise ValueError for invalid range."""
        mgr = ResultsManager()
        mgr.register_config("config_0001", {"config_name": "test", "parameters": {}})
        mgr.record_week_results("config_0001", self.create_sample_week_results())

        with pytest.raises(ValueError, match="Invalid week range"):
            mgr.get_best_config_for_range("1-6")  # Invalid range

    def test_get_best_configs_per_range_returns_all_ranges(self):
        """get_best_configs_per_range should return dict with all four ranges."""
        mgr = ResultsManager()

        # Register configs with different strengths
        mgr.register_config("config_early", {"config_name": "early", "parameters": {}})
        mgr.record_week_results("config_early", self.create_sample_week_results(wins_early=5, wins_mid_early=1, wins_mid_late=1, wins_late=1))

        mgr.register_config("config_mid_early", {"config_name": "mid_early", "parameters": {}})
        mgr.record_week_results("config_mid_early", self.create_sample_week_results(wins_early=1, wins_mid_early=4, wins_mid_late=1, wins_late=1))

        mgr.register_config("config_mid_late", {"config_name": "mid_late", "parameters": {}})
        mgr.record_week_results("config_mid_late", self.create_sample_week_results(wins_early=1, wins_mid_early=1, wins_mid_late=4, wins_late=1))

        mgr.register_config("config_late", {"config_name": "late", "parameters": {}})
        mgr.record_week_results("config_late", self.create_sample_week_results(wins_early=1, wins_mid_early=1, wins_mid_late=1, wins_late=4))

        best_per_range = mgr.get_best_configs_per_range()

        assert "1-5" in best_per_range
        assert "6-9" in best_per_range
        assert "10-13" in best_per_range
        assert "14-17" in best_per_range

        assert best_per_range["1-5"].config_id == "config_early"
        assert best_per_range["6-9"].config_id == "config_mid_early"
        assert best_per_range["10-13"].config_id == "config_mid_late"
        assert best_per_range["14-17"].config_id == "config_late"

    @patch('simulation.ResultsManager.datetime')
    def test_save_optimal_configs_folder_creates_correct_structure(self, mock_datetime, tmp_path):
        """save_optimal_configs_folder should create folder with 4 config files."""
        mock_datetime.now.return_value.strftime.return_value = "2025-01-01_12-00-00"

        mgr = ResultsManager()

        # Create config with week-specific parameters
        config_dict = {
            "config_name": "Test Config",
            "parameters": {
                "CURRENT_NFL_WEEK": 6,
                "NFL_SEASON": 2025,
                "NFL_SCORING_FORMAT": "ppr",
                "PLAYER_RATING_SCORING": {"WEIGHT": 2.0},
                "TEAM_QUALITY_SCORING": {"WEIGHT": 1.5}
            }
        }

        mgr.register_config("config_0001", config_dict)
        mgr.record_week_results("config_0001", self.create_sample_week_results())

        folder_path = mgr.save_optimal_configs_folder(tmp_path)

        # Verify folder created
        assert folder_path.exists()
        assert folder_path.name == "optimal_2025-01-01_12-00-00"

        # Verify all 5 files created
        assert (folder_path / "league_config.json").exists()
        assert (folder_path / "week1-5.json").exists()
        assert (folder_path / "week6-9.json").exists()
        assert (folder_path / "week10-13.json").exists()
        assert (folder_path / "week14-17.json").exists()

    @patch('simulation.ResultsManager.datetime')
    def test_save_optimal_configs_folder_base_config_has_base_params(self, mock_datetime, tmp_path):
        """Base config should only contain base (non-week-specific) parameters."""
        mock_datetime.now.return_value.strftime.return_value = "2025-01-01_12-00-00"

        mgr = ResultsManager()

        config_dict = {
            "config_name": "Test Config",
            "parameters": {
                "CURRENT_NFL_WEEK": 6,
                "NFL_SEASON": 2025,
                "PLAYER_RATING_SCORING": {"WEIGHT": 2.0}
            }
        }

        mgr.register_config("config_0001", config_dict)
        mgr.record_week_results("config_0001", self.create_sample_week_results())

        folder_path = mgr.save_optimal_configs_folder(tmp_path)

        # Read base config
        with open(folder_path / "league_config.json", 'r') as f:
            base_config = json.load(f)

        # Base config should have base params
        assert "CURRENT_NFL_WEEK" in base_config["parameters"]
        assert "NFL_SEASON" in base_config["parameters"]

        # Base config should NOT have week-specific params
        assert "PLAYER_RATING_SCORING" not in base_config["parameters"]

    @patch('simulation.ResultsManager.datetime')
    def test_save_optimal_configs_folder_week_configs_have_week_params(self, mock_datetime, tmp_path):
        """Week configs should only contain week-specific parameters."""
        mock_datetime.now.return_value.strftime.return_value = "2025-01-01_12-00-00"

        mgr = ResultsManager()

        config_dict = {
            "config_name": "Test Config",
            "parameters": {
                "CURRENT_NFL_WEEK": 6,
                "NFL_SEASON": 2025,
                "PLAYER_RATING_SCORING": {"WEIGHT": 2.0},
                "MATCHUP_SCORING": {"WEIGHT": 1.5}
            }
        }

        mgr.register_config("config_0001", config_dict)
        mgr.record_week_results("config_0001", self.create_sample_week_results())

        folder_path = mgr.save_optimal_configs_folder(tmp_path)

        # Read week config
        with open(folder_path / "week1-5.json", 'r') as f:
            week_config = json.load(f)

        # Week config should have week-specific params
        assert "PLAYER_RATING_SCORING" in week_config["parameters"]
        assert "MATCHUP_SCORING" in week_config["parameters"]

        # Week config should NOT have base params
        assert "CURRENT_NFL_WEEK" not in week_config["parameters"]
        assert "NFL_SEASON" not in week_config["parameters"]

    def test_save_optimal_configs_folder_no_results_raises_error(self):
        """save_optimal_configs_folder should raise ValueError when no results."""
        mgr = ResultsManager()
        with pytest.raises(ValueError, match="No results available"):
            mgr.save_optimal_configs_folder(Path("/tmp"))


# ============================================================================
# Test: update_configs_folder() Method
# ============================================================================

class TestUpdateConfigsFolder:
    """Tests for update_configs_folder functionality."""

    def create_optimal_configs(self, folder: Path) -> None:
        """Create sample optimal config files in a folder."""
        folder.mkdir(parents=True, exist_ok=True)

        # league_config.json
        league_config = {
            "config_name": "optimal_test",
            "description": "Win Rate: 0.85",
            "parameters": {
                "CURRENT_NFL_WEEK": 13,
                "NFL_SEASON": 2024,
                "MAX_POSITIONS": {"QB": 3, "RB": 5},
                "FLEX_ELIGIBLE_POSITIONS": ["RB"],
                "INJURY_PENALTIES": {"OUT": -100},
                "NORMALIZATION_MAX_SCALE": 150.0
            },
            "performance_metrics": {
                "config_id": "optimal",
                "win_rate": 0.85,
                "total_wins": 850
            }
        }
        with open(folder / "league_config.json", 'w') as f:
            json.dump(league_config, f)

        # Week files with MATCHUP_SCORING and SCHEDULE_SCORING
        for week_file in ["week1-5.json", "week6-9.json", "week10-13.json", "week14-17.json"]:
            week_config = {
                "config_name": f"optimal_test_{week_file}",
                "parameters": {
                    "MATCHUP_SCORING": {
                        "MIN_WEEKS": 3,
                        "IMPACT_SCALE": 107.45,
                        "WEIGHT": 0.409,
                        "THRESHOLDS": {"BASE_POSITION": 0}
                    },
                    "SCHEDULE_SCORING": {
                        "MIN_WEEKS": 5,
                        "IMPACT_SCALE": 108.44,
                        "WEIGHT": 0.80,
                        "THRESHOLDS": {"BASE_POSITION": 16}
                    },
                    "PLAYER_RATING_SCORING": {"WEIGHT": 2.0}
                },
                "performance_metrics": {
                    "config_id": "optimal",
                    "win_rate": 0.85
                }
            }
            with open(folder / week_file, 'w') as f:
                json.dump(week_config, f)

    def create_original_configs(self, folder: Path) -> None:
        """Create sample original config files in target folder."""
        folder.mkdir(parents=True, exist_ok=True)

        # league_config.json with user-maintained values
        league_config = {
            "config_name": "original",
            "description": "Original config",
            "parameters": {
                "CURRENT_NFL_WEEK": 1,
                "NFL_SEASON": 2025,
                "MAX_POSITIONS": {"QB": 2, "RB": 4},
                "FLEX_ELIGIBLE_POSITIONS": ["RB", "WR", "DST"],
                "INJURY_PENALTIES": {"OUT": -50, "DOUBTFUL": -25},
                "NORMALIZATION_MAX_SCALE": 100.0
            }
        }
        with open(folder / "league_config.json", 'w') as f:
            json.dump(league_config, f)

        # Week files
        for week_file in ["week1-5.json", "week6-9.json", "week10-13.json", "week14-17.json"]:
            week_config = {
                "config_name": f"original_{week_file}",
                "parameters": {
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
            with open(folder / week_file, 'w') as f:
                json.dump(week_config, f)

    def test_update_configs_folder_preserves_league_config_parameters(self, tmp_path):
        """Test that preserved parameters are kept from original league_config.json."""
        optimal_folder = tmp_path / "optimal"
        target_folder = tmp_path / "data" / "configs"

        self.create_optimal_configs(optimal_folder)
        self.create_original_configs(target_folder)

        mgr = ResultsManager()
        mgr.update_configs_folder(optimal_folder, target_folder)

        # Read updated league_config
        with open(target_folder / "league_config.json", 'r') as f:
            updated = json.load(f)

        # Verify preserved parameters are from original
        assert updated["parameters"]["CURRENT_NFL_WEEK"] == 1
        assert updated["parameters"]["NFL_SEASON"] == 2025
        assert updated["parameters"]["MAX_POSITIONS"] == {"QB": 2, "RB": 4}
        assert updated["parameters"]["FLEX_ELIGIBLE_POSITIONS"] == ["RB", "WR", "DST"]
        assert updated["parameters"]["INJURY_PENALTIES"] == {"OUT": -50, "DOUBTFUL": -25}

        # Verify non-preserved parameters are from optimal
        assert updated["parameters"]["NORMALIZATION_MAX_SCALE"] == 150.0

    def test_update_configs_folder_applies_matchup_to_schedule_mapping(self, tmp_path):
        """Test that MATCHUP_SCORING values are copied to SCHEDULE_SCORING in week files."""
        optimal_folder = tmp_path / "optimal"
        target_folder = tmp_path / "data" / "configs"

        self.create_optimal_configs(optimal_folder)
        self.create_original_configs(target_folder)

        mgr = ResultsManager()
        mgr.update_configs_folder(optimal_folder, target_folder)

        # Check each week file
        for week_file in ["week1-5.json", "week6-9.json", "week10-13.json", "week14-17.json"]:
            with open(target_folder / week_file, 'r') as f:
                updated = json.load(f)

            matchup = updated["parameters"]["MATCHUP_SCORING"]
            schedule = updated["parameters"]["SCHEDULE_SCORING"]

            # Verify MATCHUP values copied to SCHEDULE
            assert schedule["MIN_WEEKS"] == matchup["MIN_WEEKS"] == 3
            assert schedule["IMPACT_SCALE"] == matchup["IMPACT_SCALE"] == 107.45
            assert schedule["WEIGHT"] == matchup["WEIGHT"] == 0.409

            # Verify other SCHEDULE values preserved (THRESHOLDS not mapped)
            assert schedule["THRESHOLDS"]["BASE_POSITION"] == 16

    def test_update_configs_folder_handles_missing_target_files(self, tmp_path):
        """Test that configs are created from optimal when target doesn't exist."""
        optimal_folder = tmp_path / "optimal"
        target_folder = tmp_path / "data" / "configs"

        self.create_optimal_configs(optimal_folder)
        # Do NOT create original configs - target folder is empty

        mgr = ResultsManager()
        mgr.update_configs_folder(optimal_folder, target_folder)

        # Verify all files were created
        assert (target_folder / "league_config.json").exists()
        assert (target_folder / "week1-5.json").exists()
        assert (target_folder / "week6-9.json").exists()
        assert (target_folder / "week10-13.json").exists()
        assert (target_folder / "week14-17.json").exists()

        # Verify league_config has optimal values (no preservation possible)
        with open(target_folder / "league_config.json", 'r') as f:
            league_config = json.load(f)

        assert league_config["parameters"]["CURRENT_NFL_WEEK"] == 13
        assert league_config["parameters"]["NFL_SEASON"] == 2024

    def test_update_configs_folder_logs_warning_for_missing_matchup_scoring(self, tmp_path):
        """Test that warning is logged when MATCHUP_SCORING is missing."""
        optimal_folder = tmp_path / "optimal"
        target_folder = tmp_path / "data" / "configs"

        # Create optimal folder
        optimal_folder.mkdir(parents=True, exist_ok=True)

        # Create league_config.json
        league_config = {
            "config_name": "optimal",
            "parameters": {
                "CURRENT_NFL_WEEK": 13,
                "NFL_SEASON": 2024
            }
        }
        with open(optimal_folder / "league_config.json", 'w') as f:
            json.dump(league_config, f)

        # Create week file WITHOUT MATCHUP_SCORING
        week_config = {
            "config_name": "optimal_week",
            "parameters": {
                "SCHEDULE_SCORING": {
                    "MIN_WEEKS": 5,
                    "IMPACT_SCALE": 108.0,
                    "WEIGHT": 0.8
                }
            }
        }
        with open(optimal_folder / "week1-5.json", 'w') as f:
            json.dump(week_config, f)

        # Should complete without error (warning logged internally)
        mgr = ResultsManager()
        mgr.update_configs_folder(optimal_folder, target_folder)

        # Verify file was still created
        assert (target_folder / "week1-5.json").exists()

        # Verify SCHEDULE_SCORING unchanged (MATCHUP mapping couldn't apply)
        with open(target_folder / "week1-5.json", 'r') as f:
            updated = json.load(f)
        assert updated["parameters"]["SCHEDULE_SCORING"]["MIN_WEEKS"] == 5

    def test_update_configs_folder_keeps_performance_metrics(self, tmp_path):
        """Test that performance_metrics are kept in updated files."""
        optimal_folder = tmp_path / "optimal"
        target_folder = tmp_path / "data" / "configs"

        self.create_optimal_configs(optimal_folder)
        self.create_original_configs(target_folder)

        mgr = ResultsManager()
        mgr.update_configs_folder(optimal_folder, target_folder)

        # Verify performance_metrics are preserved
        with open(target_folder / "league_config.json", 'r') as f:
            league_config = json.load(f)
        assert "performance_metrics" in league_config
        assert league_config["performance_metrics"]["win_rate"] == 0.85

        with open(target_folder / "week1-5.json", 'r') as f:
            week_config = json.load(f)
        assert "performance_metrics" in week_config

    def test_update_configs_folder_missing_optimal_file_logs_warning(self, tmp_path):
        """Test that warning is logged when optimal file is missing."""
        optimal_folder = tmp_path / "optimal"
        target_folder = tmp_path / "data" / "configs"

        # Create only league_config.json in optimal folder
        optimal_folder.mkdir(parents=True, exist_ok=True)
        league_config = {
            "config_name": "optimal",
            "parameters": {"CURRENT_NFL_WEEK": 13}
        }
        with open(optimal_folder / "league_config.json", 'w') as f:
            json.dump(league_config, f)

        # Do NOT create week files

        mgr = ResultsManager()
        mgr.update_configs_folder(optimal_folder, target_folder)

        # Only league_config.json should exist in target
        assert (target_folder / "league_config.json").exists()
        assert not (target_folder / "week1-5.json").exists()

    def test_update_configs_folder_creates_target_folder_if_missing(self, tmp_path):
        """Test that target folder is created if it doesn't exist."""
        optimal_folder = tmp_path / "optimal"
        target_folder = tmp_path / "nonexistent" / "path" / "configs"

        self.create_optimal_configs(optimal_folder)

        # Target folder doesn't exist
        assert not target_folder.exists()

        mgr = ResultsManager()
        mgr.update_configs_folder(optimal_folder, target_folder)

        # Target folder should now exist with files
        assert target_folder.exists()
        assert (target_folder / "league_config.json").exists()


class TestApplyMatchupToScheduleMapping:
    """Tests for _apply_matchup_to_schedule_mapping helper method."""

    def test_applies_all_mapped_values(self):
        """Test all three values are mapped from MATCHUP to SCHEDULE."""
        config = {
            "parameters": {
                "MATCHUP_SCORING": {
                    "MIN_WEEKS": 3,
                    "IMPACT_SCALE": 107.0,
                    "WEIGHT": 0.4,
                    "THRESHOLDS": {"BASE_POSITION": 0}
                },
                "SCHEDULE_SCORING": {
                    "MIN_WEEKS": 5,
                    "IMPACT_SCALE": 108.0,
                    "WEIGHT": 0.8,
                    "THRESHOLDS": {"BASE_POSITION": 16}
                }
            }
        }

        mgr = ResultsManager()
        mgr._apply_matchup_to_schedule_mapping(config)

        schedule = config["parameters"]["SCHEDULE_SCORING"]
        assert schedule["MIN_WEEKS"] == 3
        assert schedule["IMPACT_SCALE"] == 107.0
        assert schedule["WEIGHT"] == 0.4
        # THRESHOLDS should NOT be mapped
        assert schedule["THRESHOLDS"]["BASE_POSITION"] == 16

    def test_handles_missing_parameters_key(self):
        """Test graceful handling when config has no parameters key."""
        config = {"config_name": "test"}

        mgr = ResultsManager()
        # Should not raise error
        mgr._apply_matchup_to_schedule_mapping(config)

    def test_creates_schedule_scoring_if_missing(self):
        """Test SCHEDULE_SCORING is created if it doesn't exist."""
        config = {
            "parameters": {
                "MATCHUP_SCORING": {
                    "MIN_WEEKS": 3,
                    "IMPACT_SCALE": 107.0,
                    "WEIGHT": 0.4
                }
            }
        }

        mgr = ResultsManager()
        mgr._apply_matchup_to_schedule_mapping(config)

        assert "SCHEDULE_SCORING" in config["parameters"]
        schedule = config["parameters"]["SCHEDULE_SCORING"]
        assert schedule["MIN_WEEKS"] == 3
        assert schedule["IMPACT_SCALE"] == 107.0
        assert schedule["WEIGHT"] == 0.4
