"""
Unit tests for ConfigPerformance module

Tests performance tracking, aggregation, and comparison logic.

Author: Kai Mizuno
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))
from simulation.ConfigPerformance import ConfigPerformance


class TestConfigPerformanceInitialization:
    """Test ConfigPerformance initialization"""

    def test_init_with_empty_config(self):
        """Test initialization with empty config dict"""
        perf = ConfigPerformance("config_001", {})

        assert perf.config_id == "config_001"
        assert perf.config_dict == {}
        assert perf.total_wins == 0
        assert perf.total_losses == 0
        assert perf.total_points == 0.0
        assert perf.num_simulations == 0

    def test_init_with_config_data(self):
        """Test initialization with config data"""
        config_dict = {'param1': 1.0, 'param2': 2.0}
        perf = ConfigPerformance("test_config", config_dict)

        assert perf.config_id == "test_config"
        assert perf.config_dict == config_dict
        assert perf.total_wins == 0

    def test_init_multiple_instances_independent(self):
        """Test multiple instances are independent"""
        perf1 = ConfigPerformance("config_001", {})
        perf2 = ConfigPerformance("config_002", {})

        perf1.add_league_result(10, 7, 1234.56)

        assert perf1.total_wins == 10
        assert perf2.total_wins == 0


class TestAddLeagueResult:
    """Test add_league_result functionality"""

    def test_add_single_result(self):
        """Test adding a single league result"""
        perf = ConfigPerformance("config_001", {})

        perf.add_league_result(10, 7, 1234.56)

        assert perf.total_wins == 10
        assert perf.total_losses == 7
        assert perf.total_points == 1234.56
        assert perf.num_simulations == 1

    def test_add_multiple_results(self):
        """Test adding multiple league results"""
        perf = ConfigPerformance("config_001", {})

        perf.add_league_result(10, 7, 1234.56)
        perf.add_league_result(11, 6, 1345.67)
        perf.add_league_result(9, 8, 1123.45)

        assert perf.total_wins == 30
        assert perf.total_losses == 21
        assert perf.total_points == pytest.approx(3703.68)
        assert perf.num_simulations == 3

    def test_add_result_zero_wins(self):
        """Test adding result with zero wins"""
        perf = ConfigPerformance("config_001", {})

        perf.add_league_result(0, 17, 800.00)

        assert perf.total_wins == 0
        assert perf.total_losses == 17
        assert perf.num_simulations == 1

    def test_add_result_perfect_season(self):
        """Test adding result with perfect season (17-0)"""
        perf = ConfigPerformance("config_001", {})

        perf.add_league_result(17, 0, 2000.00)

        assert perf.total_wins == 17
        assert perf.total_losses == 0
        assert perf.num_simulations == 1

    def test_add_result_fractional_points(self):
        """Test adding result with fractional points"""
        perf = ConfigPerformance("config_001", {})

        perf.add_league_result(10, 7, 1234.567)

        assert perf.total_points == pytest.approx(1234.567)


class TestTotalGamesProperty:
    """Test total_games property"""

    def test_total_games_zero_initially(self):
        """Test total_games is zero initially"""
        perf = ConfigPerformance("config_001", {})

        assert perf.total_games == 0

    def test_total_games_after_single_result(self):
        """Test total_games after adding one result"""
        perf = ConfigPerformance("config_001", {})
        perf.add_league_result(10, 7, 1234.56)

        assert perf.total_games == 17

    def test_total_games_after_multiple_results(self):
        """Test total_games accumulates correctly"""
        perf = ConfigPerformance("config_001", {})
        perf.add_league_result(10, 7, 1234.56)
        perf.add_league_result(11, 6, 1345.67)
        perf.add_league_result(9, 8, 1123.45)

        assert perf.total_games == 51  # 17 + 17 + 17


class TestGetWinRate:
    """Test get_win_rate functionality"""

    def test_get_win_rate_no_games(self):
        """Test win rate with no games returns 0.0"""
        perf = ConfigPerformance("config_001", {})

        assert perf.get_win_rate() == 0.0

    def test_get_win_rate_single_result(self):
        """Test win rate with single result"""
        perf = ConfigPerformance("config_001", {})
        perf.add_league_result(10, 7, 1234.56)

        assert perf.get_win_rate() == pytest.approx(10/17)

    def test_get_win_rate_multiple_results(self):
        """Test win rate with multiple results"""
        perf = ConfigPerformance("config_001", {})
        perf.add_league_result(10, 7, 1234.56)  # 10/17
        perf.add_league_result(12, 5, 1345.67)  # 12/17

        # Total: 22 wins, 12 losses = 22/34
        assert perf.get_win_rate() == pytest.approx(22/34)

    def test_get_win_rate_perfect_record(self):
        """Test win rate with perfect record (100%)"""
        perf = ConfigPerformance("config_001", {})
        perf.add_league_result(17, 0, 2000.00)

        assert perf.get_win_rate() == 1.0

    def test_get_win_rate_winless_record(self):
        """Test win rate with winless record (0%)"""
        perf = ConfigPerformance("config_001", {})
        perf.add_league_result(0, 17, 800.00)

        assert perf.get_win_rate() == 0.0

    def test_get_win_rate_exactly_50_percent(self):
        """Test win rate exactly 50%"""
        perf = ConfigPerformance("config_001", {})
        perf.add_league_result(10, 10, 1200.00)

        assert perf.get_win_rate() == 0.5


class TestGetAvgPointsPerLeague:
    """Test get_avg_points_per_league functionality"""

    def test_get_avg_points_no_simulations(self):
        """Test avg points with no simulations returns 0.0"""
        perf = ConfigPerformance("config_001", {})

        assert perf.get_avg_points_per_league() == 0.0

    def test_get_avg_points_single_simulation(self):
        """Test avg points with single simulation"""
        perf = ConfigPerformance("config_001", {})
        perf.add_league_result(10, 7, 1234.56)

        assert perf.get_avg_points_per_league() == pytest.approx(1234.56)

    def test_get_avg_points_multiple_simulations(self):
        """Test avg points with multiple simulations"""
        perf = ConfigPerformance("config_001", {})
        perf.add_league_result(10, 7, 1200.00)
        perf.add_league_result(11, 6, 1400.00)
        perf.add_league_result(9, 8, 1000.00)

        # Avg: (1200 + 1400 + 1000) / 3 = 1200
        assert perf.get_avg_points_per_league() == pytest.approx(1200.00)

    def test_get_avg_points_high_variance(self):
        """Test avg points with high variance"""
        perf = ConfigPerformance("config_001", {})
        perf.add_league_result(17, 0, 2000.00)
        perf.add_league_result(0, 17, 500.00)

        # Avg: (2000 + 500) / 2 = 1250
        assert perf.get_avg_points_per_league() == pytest.approx(1250.00)


class TestCompareTo:
    """Test compare_to functionality"""

    def test_compare_to_self_is_better_win_rate(self):
        """Test comparison when self has higher win rate"""
        config1 = ConfigPerformance("config_001", {})
        config1.add_league_result(12, 5, 1300.00)  # 70.6% win rate

        config2 = ConfigPerformance("config_002", {})
        config2.add_league_result(10, 7, 1200.00)  # 58.8% win rate

        assert config1.compare_to(config2) == 1

    def test_compare_to_other_is_better_win_rate(self):
        """Test comparison when other has higher win rate"""
        config1 = ConfigPerformance("config_001", {})
        config1.add_league_result(10, 7, 1200.00)  # 58.8% win rate

        config2 = ConfigPerformance("config_002", {})
        config2.add_league_result(12, 5, 1300.00)  # 70.6% win rate

        assert config1.compare_to(config2) == -1

    def test_compare_to_tied_win_rate_self_better_points(self):
        """Test comparison when win rates equal, self has higher points"""
        config1 = ConfigPerformance("config_001", {})
        config1.add_league_result(10, 7, 1400.00)

        config2 = ConfigPerformance("config_002", {})
        config2.add_league_result(10, 7, 1200.00)

        assert config1.compare_to(config2) == 1

    def test_compare_to_tied_win_rate_other_better_points(self):
        """Test comparison when win rates equal, other has higher points"""
        config1 = ConfigPerformance("config_001", {})
        config1.add_league_result(10, 7, 1200.00)

        config2 = ConfigPerformance("config_002", {})
        config2.add_league_result(10, 7, 1400.00)

        assert config1.compare_to(config2) == -1

    def test_compare_to_completely_tied(self):
        """Test comparison when both metrics are essentially equal"""
        config1 = ConfigPerformance("config_001", {})
        config1.add_league_result(10, 7, 1234.56)

        config2 = ConfigPerformance("config_002", {})
        config2.add_league_result(10, 7, 1234.56)

        assert config1.compare_to(config2) == 0

    def test_compare_to_win_rate_within_threshold(self):
        """Test comparison when win rates within threshold (0.0001)"""
        config1 = ConfigPerformance("config_001", {})
        # Create result where win rate difference < 0.0001
        config1.add_league_result(1000, 1000, 10000.00)  # 50.00% exactly

        config2 = ConfigPerformance("config_002", {})
        config2.add_league_result(1000, 1001, 10100.00)  # 49.975% (diff = 0.00025)

        # Should use points as tiebreaker since win rates essentially equal
        result = config1.compare_to(config2)
        # config2 has slightly higher points, but win rate diff might matter
        # Let's check: 1000/2000 = 0.5, 1000/2001 = 0.4997...
        # Diff = 0.0002... which is > 0.0001, so win rate determines result
        assert result == 1  # config1 has higher win rate

    def test_compare_to_points_within_threshold(self):
        """Test comparison when points within threshold (0.01)"""
        config1 = ConfigPerformance("config_001", {})
        config1.add_league_result(10, 7, 1234.560)

        config2 = ConfigPerformance("config_002", {})
        config2.add_league_result(10, 7, 1234.565)  # Diff = 0.005

        # Points diff < 0.01, should be tied
        assert config1.compare_to(config2) == 0

    def test_compare_to_both_empty(self):
        """Test comparison when both configs have no results"""
        config1 = ConfigPerformance("config_001", {})
        config2 = ConfigPerformance("config_002", {})

        # Both have 0.0 win rate and 0.0 avg points
        assert config1.compare_to(config2) == 0


class TestToDict:
    """Test to_dict functionality"""

    def test_to_dict_no_results(self):
        """Test to_dict with no results"""
        perf = ConfigPerformance("config_001", {'param': 1.0})

        result = perf.to_dict()

        assert result['config_id'] == 'config_001'
        assert result['total_wins'] == 0
        assert result['total_losses'] == 0
        assert result['total_points'] == 0.0
        assert result['num_simulations'] == 0
        assert result['total_games'] == 0
        assert result['win_rate'] == 0.0
        assert result['avg_points_per_league'] == 0.0

    def test_to_dict_with_results(self):
        """Test to_dict with results"""
        perf = ConfigPerformance("config_001", {})
        perf.add_league_result(10, 7, 1234.56)

        result = perf.to_dict()

        assert result['config_id'] == 'config_001'
        assert result['total_wins'] == 10
        assert result['total_losses'] == 7
        assert result['total_points'] == pytest.approx(1234.56)
        assert result['num_simulations'] == 1
        assert result['total_games'] == 17
        assert result['win_rate'] == pytest.approx(10/17)
        assert result['avg_points_per_league'] == pytest.approx(1234.56)

    def test_to_dict_multiple_results(self):
        """Test to_dict with multiple results"""
        perf = ConfigPerformance("config_001", {})
        perf.add_league_result(10, 7, 1200.00)
        perf.add_league_result(12, 5, 1400.00)

        result = perf.to_dict()

        assert result['total_wins'] == 22
        assert result['total_losses'] == 12
        assert result['num_simulations'] == 2
        assert result['win_rate'] == pytest.approx(22/34)
        assert result['avg_points_per_league'] == pytest.approx(1300.00)

    def test_to_dict_structure(self):
        """Test to_dict returns all expected keys"""
        perf = ConfigPerformance("config_001", {})

        result = perf.to_dict()

        expected_keys = {
            'config_id', 'total_wins', 'total_losses', 'total_points',
            'num_simulations', 'total_games', 'win_rate', 'avg_points_per_league'
        }
        assert set(result.keys()) == expected_keys


class TestStringRepresentations:
    """Test __repr__ and __str__ functionality"""

    def test_repr_no_results(self):
        """Test __repr__ with no results"""
        perf = ConfigPerformance("config_001", {})

        repr_str = repr(perf)

        assert "config_001" in repr_str
        assert "0.0000" in repr_str  # win rate
        assert "0.00" in repr_str    # avg pts
        assert "sims=0" in repr_str

    def test_repr_with_results(self):
        """Test __repr__ with results"""
        perf = ConfigPerformance("test_config", {})
        perf.add_league_result(10, 7, 1234.56)

        repr_str = repr(perf)

        assert "test_config" in repr_str
        assert "ConfigPerformance" in repr_str

    def test_str_no_results(self):
        """Test __str__ with no results"""
        perf = ConfigPerformance("config_001", {})

        str_rep = str(perf)

        assert "config_001" in str_rep
        assert "0W-0L" in str_rep

    def test_str_with_results(self):
        """Test __str__ with results"""
        perf = ConfigPerformance("config_001", {})
        perf.add_league_result(10, 7, 1234.56)

        str_rep = str(perf)

        assert "config_001" in str_rep
        assert "10W-7L" in str_rep
        assert "1234.6" in str_rep  # points rounded to 1 decimal
        assert "1 sims" in str_rep

    def test_str_multiple_results(self):
        """Test __str__ with multiple results"""
        perf = ConfigPerformance("config_001", {})
        perf.add_league_result(10, 7, 1234.56)
        perf.add_league_result(11, 6, 1345.67)

        str_rep = str(perf)

        assert "21W-13L" in str_rep
        assert "2 sims" in str_rep


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_very_large_numbers(self):
        """Test with very large numbers"""
        perf = ConfigPerformance("config_001", {})

        # Add 1000 simulations
        for _ in range(1000):
            perf.add_league_result(10, 7, 1234.56)

        assert perf.num_simulations == 1000
        assert perf.total_wins == 10000
        assert perf.get_win_rate() == pytest.approx(10/17)

    def test_floating_point_precision(self):
        """Test floating point precision handling"""
        perf = ConfigPerformance("config_001", {})
        perf.add_league_result(10, 7, 1234.567890123456)

        assert perf.total_points == pytest.approx(1234.567890123456)

    def test_zero_zero_record(self):
        """Test with 0-0 record (edge case)"""
        perf = ConfigPerformance("config_001", {})
        perf.add_league_result(0, 0, 0.0)

        assert perf.total_games == 0
        assert perf.get_win_rate() == 0.0  # Should handle division by zero

    def test_compare_to_after_many_simulations(self):
        """Test comparison with many simulations"""
        config1 = ConfigPerformance("config_001", {})
        config2 = ConfigPerformance("config_002", {})

        # Add 100 simulations to each
        for _ in range(100):
            config1.add_league_result(10, 7, 1200.00)
            config2.add_league_result(10, 7, 1300.00)

        # Same win rate, but config2 has higher points
        assert config1.compare_to(config2) == -1


class TestIntegrationScenarios:
    """Test realistic integration scenarios"""

    def test_realistic_optimization_scenario(self):
        """Test realistic optimization scenario"""
        perf = ConfigPerformance("baseline", {'param1': 1.0, 'param2': 2.0})

        # Run 10 simulations with varying results
        results = [
            (10, 7, 1234.56),
            (11, 6, 1345.67),
            (9, 8, 1123.45),
            (12, 5, 1456.78),
            (10, 7, 1298.34),
            (11, 6, 1376.12),
            (10, 7, 1255.89),
            (12, 5, 1421.33),
            (9, 8, 1178.90),
            (11, 6, 1389.45)
        ]

        for wins, losses, points in results:
            perf.add_league_result(wins, losses, points)

        # Verify aggregation
        assert perf.num_simulations == 10
        assert perf.total_wins == 105
        assert perf.total_losses == 65
        assert perf.total_games == 170

        # Verify metrics
        win_rate = perf.get_win_rate()
        assert 0.6 < win_rate < 0.65  # Around 61.8%

        avg_points = perf.get_avg_points_per_league()
        assert 1200 < avg_points < 1400

        # Verify serialization
        data = perf.to_dict()
        assert data['num_simulations'] == 10
