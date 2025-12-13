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
            'num_simulations', 'total_games', 'win_rate', 'avg_points_per_league',
            'week_range_performance'
        }
        assert set(result.keys()) == expected_keys

        # Verify week_range_performance structure
        assert set(result['week_range_performance'].keys()) == {'1-5', '6-9', '10-13', '14-17'}
        for week_range in result['week_range_performance'].values():
            assert set(week_range.keys()) == {'wins', 'losses', 'points', 'win_rate'}


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


# ============================================================================
# NEW: Per-Week Range Tracking Tests
# ============================================================================

class TestGetWeekRange:
    """Test get_week_range() function."""

    def test_weeks_1_to_5_return_1_5(self):
        """Weeks 1-5 should return '1-5' range."""
        from simulation.ConfigPerformance import get_week_range
        for week in range(1, 6):
            assert get_week_range(week) == "1-5"

    def test_weeks_6_to_9_return_6_9(self):
        """Weeks 6-9 should return '6-9' range."""
        from simulation.ConfigPerformance import get_week_range
        for week in range(6, 10):
            assert get_week_range(week) == "6-9"

    def test_weeks_10_to_13_return_10_13(self):
        """Weeks 10-13 should return '10-13' range."""
        from simulation.ConfigPerformance import get_week_range
        for week in range(10, 14):
            assert get_week_range(week) == "10-13"

    def test_weeks_14_to_17_return_14_17(self):
        """Weeks 14-17 should return '14-17' range."""
        from simulation.ConfigPerformance import get_week_range
        for week in range(14, 18):
            assert get_week_range(week) == "14-17"

    def test_week_0_raises_error(self):
        """Week 0 should raise ValueError."""
        from simulation.ConfigPerformance import get_week_range
        with pytest.raises(ValueError, match="Invalid week number: 0"):
            get_week_range(0)

    def test_week_18_raises_error(self):
        """Week 18 should raise ValueError."""
        from simulation.ConfigPerformance import get_week_range
        with pytest.raises(ValueError, match="Invalid week number: 18"):
            get_week_range(18)


class TestAddWeekResults:
    """Test add_week_results() method."""

    def test_add_week_results_updates_totals(self):
        """add_week_results should update overall totals."""
        perf = ConfigPerformance("config_001", {})

        # 5 wins, 3 losses across weeks 1-8
        week_results = [
            (1, True, 120.0),
            (2, True, 110.0),
            (3, False, 90.0),
            (4, True, 130.0),
            (5, False, 85.0),
            (6, True, 125.0),
            (7, False, 95.0),
            (8, True, 115.0),
        ]

        perf.add_week_results(week_results)

        assert perf.total_wins == 5
        assert perf.total_losses == 3
        assert perf.total_points == pytest.approx(870.0)
        assert perf.num_simulations == 1

    def test_add_week_results_updates_per_range(self):
        """add_week_results should update per-week-range tracking."""
        perf = ConfigPerformance("config_001", {})

        week_results = [
            # Week 1-5 range: 3 wins, 2 losses
            (1, True, 120.0),
            (2, True, 110.0),
            (3, False, 90.0),
            (4, True, 130.0),
            (5, False, 85.0),
            # Week 6-11 range: 2 wins, 2 losses
            (6, True, 125.0),
            (7, False, 95.0),
            (8, True, 115.0),
            (9, False, 100.0),
            # Week 12-17 range: 1 win, 1 loss
            (12, True, 140.0),
            (13, False, 80.0),
        ]

        perf.add_week_results(week_results)

        # Check per-range wins
        assert perf.week_range_wins["1-5"] == 3
        assert perf.week_range_wins["6-9"] == 2
        assert perf.week_range_wins["10-13"] == 1

        # Check per-range losses
        assert perf.week_range_losses["1-5"] == 2
        assert perf.week_range_losses["6-9"] == 2
        assert perf.week_range_losses["10-13"] == 1

    def test_add_multiple_leagues(self):
        """Adding multiple leagues should accumulate results."""
        perf = ConfigPerformance("config_001", {})

        # League 1
        perf.add_week_results([
            (1, True, 100.0),
            (2, False, 90.0),
            (6, True, 110.0),
        ])

        # League 2
        perf.add_week_results([
            (1, False, 80.0),
            (2, True, 120.0),
            (6, False, 95.0),
        ])

        assert perf.num_simulations == 2
        assert perf.total_wins == 3
        assert perf.total_losses == 3
        assert perf.week_range_wins["1-5"] == 2
        assert perf.week_range_losses["1-5"] == 2


class TestGetWinRateForRange:
    """Test get_win_rate_for_range() method."""

    def test_win_rate_for_range_no_games(self):
        """Should return 0.0 when no games in range."""
        perf = ConfigPerformance("config_001", {})
        assert perf.get_win_rate_for_range("1-5") == 0.0

    def test_win_rate_for_range_perfect_record(self):
        """Should return 1.0 for perfect record in range."""
        perf = ConfigPerformance("config_001", {})
        perf.add_week_results([
            (1, True, 100.0),
            (2, True, 110.0),
            (3, True, 120.0),
        ])
        assert perf.get_win_rate_for_range("1-5") == 1.0

    def test_win_rate_for_range_winless_record(self):
        """Should return 0.0 for winless record in range."""
        perf = ConfigPerformance("config_001", {})
        perf.add_week_results([
            (6, False, 80.0),
            (7, False, 85.0),
        ])
        assert perf.get_win_rate_for_range("6-9") == 0.0

    def test_win_rate_for_range_mixed(self):
        """Should calculate correct win rate for mixed results."""
        perf = ConfigPerformance("config_001", {})
        perf.add_week_results([
            (1, True, 100.0),
            (2, True, 110.0),
            (3, False, 90.0),
            (4, True, 120.0),
            (5, False, 85.0),
        ])
        # 3 wins, 2 losses = 60%
        assert perf.get_win_rate_for_range("1-5") == pytest.approx(0.6)


class TestWeekRangePerformanceIntegration:
    """Integration tests for per-week-range tracking."""

    def test_full_16_week_season(self):
        """Test tracking a full 16-week season."""
        perf = ConfigPerformance("config_001", {})

        # Simulate a 10-6 season with varying performance by range
        week_results = [
            # Weeks 1-5: 4-1 (strong start)
            (1, True, 120.0), (2, True, 115.0), (3, True, 125.0),
            (4, False, 90.0), (5, True, 130.0),
            # Weeks 6-11: 3-3 (mid-season slump)
            (6, True, 110.0), (7, False, 95.0), (8, True, 105.0),
            (9, False, 88.0), (10, True, 118.0), (11, False, 92.0),
            # Weeks 12-16: split between 10-13 and 14-17 ranges
            (12, True, 140.0), (13, False, 85.0), (14, True, 135.0),
            (15, False, 82.0), (16, True, 142.0),
        ]

        perf.add_week_results(week_results)

        # Overall: 10-6
        assert perf.total_wins == 10
        assert perf.total_losses == 6
        assert perf.get_win_rate() == pytest.approx(10/16)

        # Per-range performance with new 4-range split
        assert perf.get_win_rate_for_range("1-5") == pytest.approx(4/5)  # 80%
        assert perf.get_win_rate_for_range("6-9") == pytest.approx(2/4)  # 50% (weeks 6-9: 2 wins, 2 losses)
        assert perf.get_win_rate_for_range("10-13") == pytest.approx(2/4)  # 50% (weeks 10-13: 2 wins, 2 losses)
        assert perf.get_win_rate_for_range("14-17") == pytest.approx(2/3)  # 66.7% (weeks 14-16: 2 wins, 1 loss)

    def test_different_configs_best_in_different_ranges(self):
        """Different configs can be best in different week ranges."""
        config_a = ConfigPerformance("config_a", {})
        config_b = ConfigPerformance("config_b", {})

        # Config A: Strong early, weak late
        config_a.add_week_results([
            (1, True, 120.0), (2, True, 115.0), (3, True, 125.0),
            (4, True, 110.0), (5, True, 130.0),  # 5-0 in weeks 1-5
            (12, False, 85.0), (13, False, 80.0), (14, False, 75.0),
            (15, False, 70.0), (16, False, 65.0),  # 0-5 in weeks 12-16
        ])

        # Config B: Weak early, strong late
        config_b.add_week_results([
            (1, False, 85.0), (2, False, 80.0), (3, False, 75.0),
            (4, False, 70.0), (5, False, 65.0),  # 0-5 in weeks 1-5
            (12, True, 140.0), (13, True, 135.0), (14, True, 145.0),
            (15, True, 150.0), (16, True, 155.0),  # 5-0 in weeks 12-16
        ])

        # Same overall record (5-5 each)
        assert config_a.get_win_rate() == config_b.get_win_rate()

        # But different range performance
        assert config_a.get_win_rate_for_range("1-5") == 1.0
        assert config_b.get_win_rate_for_range("1-5") == 0.0
        assert config_a.get_win_rate_for_range("14-17") == 0.0
        assert config_b.get_win_rate_for_range("14-17") == 1.0
