#!/usr/bin/env python3
"""
Unit tests for ConsistencyCalculator

Tests the consistency/volatility calculation logic including:
- CV calculation accuracy
- Volatility categorization
- Edge cases (missing data, zero values, etc.)
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from shared_files.consistency_calculator import ConsistencyCalculator, calculate_player_consistency


class MockPlayer:
    """Mock FantasyPlayer for testing"""
    def __init__(self, name="Test Player"):
        self.name = name
        self.bye_week = None  # Default: no bye week
        # Initialize all week attributes to None
        for week in range(1, 18):
            setattr(self, f'week_{week}_points', None)


class TestConsistencyCalculator:
    """Test suite for ConsistencyCalculator"""

    @pytest.fixture
    def calculator(self):
        """Create ConsistencyCalculator instance"""
        return ConsistencyCalculator()

    def test_consistent_player_low_volatility(self, calculator):
        """Test player with same points every week (CV = 0, should be LOW)"""
        player = MockPlayer("Consistent Player")

        # Set same points for weeks 1-4 (assuming CURRENT_NFL_WEEK = 5)
        for week in range(1, 5):
            setattr(player, f'week_{week}_points', 12.0)

        result = calculator.calculate_consistency_score(player)

        assert result['mean_points'] == 12.0
        assert result['std_dev'] == 0.0
        assert result['coefficient_of_variation'] == 0.0
        assert result['volatility_category'] == 'LOW'
        assert result['weeks_analyzed'] == 4

    def test_volatile_player_high_volatility(self, calculator):
        """Test player with alternating high/low points (should be HIGH)"""
        player = MockPlayer("Volatile Player")

        # Alternating 24 and 2 points (mean=13, high CV)
        for week in range(1, 5):
            setattr(player, f'week_{week}_points', 24.0 if week % 2 == 0 else 2.0)

        result = calculator.calculate_consistency_score(player)

        assert result['mean_points'] == 13.0  # (24+2+24+2)/4
        assert result['std_dev'] > 10  # Should be high
        assert result['coefficient_of_variation'] > 0.6  # CV > 0.6 = HIGH
        assert result['volatility_category'] == 'HIGH'

    def test_medium_volatility_player(self, calculator):
        """Test player with moderate variance (should be MEDIUM)"""
        player = MockPlayer("Medium Player")

        # Moderate variance: 8, 12, 14, 18 (mean=13, moderate CV)
        setattr(player, 'week_1_points', 8.0)
        setattr(player, 'week_2_points', 12.0)
        setattr(player, 'week_3_points', 14.0)
        setattr(player, 'week_4_points', 18.0)

        result = calculator.calculate_consistency_score(player)

        assert result['mean_points'] == 13.0
        cv = result['coefficient_of_variation']
        assert 0.3 <= cv <= 0.6  # MEDIUM range
        assert result['volatility_category'] == 'MEDIUM'

    def test_insufficient_data_defaults_to_medium(self, calculator):
        """Test player with < 3 weeks (insufficient data) defaults to MEDIUM"""
        player = MockPlayer("New Player")

        # Only 2 weeks of data (less than MINIMUM_WEEKS_FOR_CONSISTENCY = 3)
        setattr(player, 'week_1_points', 10.0)
        setattr(player, 'week_2_points', 12.0)

        result = calculator.calculate_consistency_score(player)

        assert result['volatility_category'] == 'MEDIUM'
        assert result['weeks_analyzed'] == 2

    def test_single_week_defaults_to_medium(self, calculator):
        """Test player with only 1 week of data"""
        player = MockPlayer("One Week Player")

        setattr(player, 'week_1_points', 15.0)

        result = calculator.calculate_consistency_score(player)

        assert result['volatility_category'] == 'MEDIUM'
        assert result['weeks_analyzed'] == 1

    def test_zero_mean_points_defaults_to_medium(self, calculator):
        """Test player with zero mean points (avoid division by zero)"""
        player = MockPlayer("Zero Points Player")

        # All weeks have 0 points
        for week in range(1, 5):
            setattr(player, f'week_{week}_points', 0.0)

        result = calculator.calculate_consistency_score(player)

        assert result['mean_points'] == 0.0
        assert result['volatility_category'] == 'MEDIUM'

    def test_missing_weeks_are_filtered(self, calculator):
        """Test that None values (missing weeks) are filtered out"""
        player = MockPlayer("Missing Weeks Player")

        # Set some weeks to None, some to values
        setattr(player, 'week_1_points', 10.0)
        setattr(player, 'week_2_points', None)  # Missing
        setattr(player, 'week_3_points', 12.0)
        setattr(player, 'week_4_points', 14.0)

        result = calculator.calculate_consistency_score(player)

        # Should only use weeks 1, 3, 4 (3 weeks)
        assert result['weeks_analyzed'] == 3
        assert result['mean_points'] == 12.0  # (10+12+14)/3

    def test_zero_points_excluded_from_calculation(self, calculator):
        """Test that 0 point weeks are excluded (could be bye, benched, or data issues)"""
        player = MockPlayer("Zero Point Week Player")
        player.bye_week = None  # No bye week

        # Week 2 has 0 points - should be excluded regardless of bye status
        setattr(player, 'week_1_points', 10.0)
        setattr(player, 'week_2_points', 0.0)  # Should be excluded (zero points)
        setattr(player, 'week_3_points', 12.0)
        setattr(player, 'week_4_points', 14.0)

        result = calculator.calculate_consistency_score(player)

        # Should use 3 weeks (excluding the zero)
        assert result['weeks_analyzed'] == 3
        assert result['mean_points'] == 12.0  # (10+12+14)/3, excluding zero

    def test_multiple_zeros_excluded(self, calculator):
        """Test that multiple zero weeks are all excluded"""
        player = MockPlayer("Multiple Zeros Player")
        player.bye_week = None

        # Multiple zero weeks
        setattr(player, 'week_1_points', 10.0)
        setattr(player, 'week_2_points', 0.0)  # Excluded
        setattr(player, 'week_3_points', 0.0)  # Excluded
        setattr(player, 'week_4_points', 14.0)

        result = calculator.calculate_consistency_score(player)

        # Should only use weeks 1 and 4
        assert result['weeks_analyzed'] == 2
        # With only 2 weeks, defaults to MEDIUM (< minimum 3 weeks)
        assert result['volatility_category'] == 'MEDIUM'

    def test_very_high_variance(self, calculator):
        """Test player with CV > 1.0 (very high variance)"""
        player = MockPlayer("Extreme Variance Player")

        # Extreme variance: 2, 1, 50, 1 (boom/bust player)
        setattr(player, 'week_1_points', 2.0)
        setattr(player, 'week_2_points', 1.0)
        setattr(player, 'week_3_points', 50.0)
        setattr(player, 'week_4_points', 1.0)

        result = calculator.calculate_consistency_score(player)

        # CV should be very high (> 1.0)
        assert result['coefficient_of_variation'] > 1.0
        assert result['volatility_category'] == 'HIGH'

    def test_cv_threshold_boundaries(self, calculator):
        """Test CV values at threshold boundaries"""
        # This is a validation test - we trust the categorization logic
        # Just verify the thresholds are applied correctly

        # Create players with known CV values by constructing data
        # LOW: CV < 0.3
        player_low = MockPlayer("Boundary Low")
        setattr(player_low, 'week_1_points', 10.0)
        setattr(player_low, 'week_2_points', 10.0)
        setattr(player_low, 'week_3_points', 10.0)

        result_low = calculator.calculate_consistency_score(player_low)
        assert result_low['coefficient_of_variation'] < 0.3
        assert result_low['volatility_category'] == 'LOW'

    def test_only_past_weeks_analyzed(self, calculator):
        """Test that only weeks < CURRENT_NFL_WEEK are analyzed"""
        from shared_files.configs.shared_config import CURRENT_NFL_WEEK

        player = MockPlayer("Future Weeks Player")

        # Set all weeks 1-17 to have data
        for week in range(1, 18):
            setattr(player, f'week_{week}_points', 10.0)

        result = calculator.calculate_consistency_score(player)

        # Should only analyze weeks < CURRENT_NFL_WEEK
        assert result['weeks_analyzed'] == CURRENT_NFL_WEEK - 1

    def test_convenience_function(self):
        """Test the convenience function calculate_player_consistency()"""
        player = MockPlayer("Convenience Test")

        for week in range(1, 5):
            setattr(player, f'week_{week}_points', 12.0)

        result = calculate_player_consistency(player)

        assert result['volatility_category'] == 'LOW'
        assert 'mean_points' in result
        assert 'coefficient_of_variation' in result

    def test_with_logger(self):
        """Test that logger integration works without errors"""
        mock_logger = Mock()
        calculator = ConsistencyCalculator(logger=mock_logger)

        player = MockPlayer("Logged Player")
        for week in range(1, 5):
            setattr(player, f'week_{week}_points', 12.0)

        result = calculator.calculate_consistency_score(player)

        # Should have logged debug messages
        assert mock_logger.debug.called
        assert result['volatility_category'] == 'LOW'

    def test_return_dict_structure(self, calculator):
        """Test that return dictionary has all required keys"""
        player = MockPlayer("Structure Test")

        for week in range(1, 5):
            setattr(player, f'week_{week}_points', 12.0)

        result = calculator.calculate_consistency_score(player)

        # Verify all expected keys are present
        required_keys = [
            'mean_points',
            'std_dev',
            'coefficient_of_variation',
            'volatility_category',
            'weeks_analyzed'
        ]

        for key in required_keys:
            assert key in result, f"Missing key: {key}"

    def test_numerical_precision(self, calculator):
        """Test that numerical values are rounded appropriately"""
        player = MockPlayer("Precision Test")

        # Use values that create non-round numbers
        setattr(player, 'week_1_points', 10.333)
        setattr(player, 'week_2_points', 12.666)
        setattr(player, 'week_3_points', 14.999)

        result = calculator.calculate_consistency_score(player)

        # Check rounding
        assert isinstance(result['mean_points'], float)
        assert isinstance(result['std_dev'], float)
        assert isinstance(result['coefficient_of_variation'], float)

        # CV should be rounded to 3 decimal places
        cv_str = str(result['coefficient_of_variation'])
        decimal_places = len(cv_str.split('.')[-1]) if '.' in cv_str else 0
        assert decimal_places <= 3


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
