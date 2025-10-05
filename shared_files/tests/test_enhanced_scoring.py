#!/usr/bin/env python3
"""
Comprehensive unit tests for enhanced scoring functionality.

This module tests all aspects of the enhanced scoring system including:
- Basic scoring calculations
- ADP adjustments
- Player rating adjustments
- Team quality adjustments
- Configuration options
- Edge cases and error handling
- Integration with FantasyPlayer
"""

import pytest
from unittest.mock import patch
import logging
from typing import Dict, Any

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from enhanced_scoring import (
    EnhancedScoringCalculator,
    calculate_enhanced_player_score,
    DEFAULT_SCORING_CONFIG
)
from FantasyPlayer import FantasyPlayer


class TestEnhancedScoringCalculator:
    """Test the main EnhancedScoringCalculator class"""

    def test_init_default_config(self):
        """Test calculator initialization with default configuration"""
        calc = EnhancedScoringCalculator()

        # Verify all configuration keys are present
        expected_keys = {
            'enable_adp_adjustment', 'enable_player_rating_adjustment', 'enable_team_quality_adjustment',
            'adp_excellent_threshold', 'adp_good_threshold', 'adp_poor_threshold',
            'adp_excellent_multiplier', 'adp_good_multiplier', 'adp_poor_multiplier',
            'player_rating_excellent_threshold', 'player_rating_good_threshold', 'player_rating_poor_threshold',
            'player_rating_excellent_multiplier', 'player_rating_good_multiplier', 'player_rating_poor_multiplier',
            'player_rating_max_boost', 'team_excellent_threshold', 'team_good_threshold', 'team_poor_threshold',
            'team_excellent_multiplier', 'team_good_multiplier', 'team_poor_multiplier',
            'max_total_adjustment', 'min_total_adjustment', 'skill_positions', 'defense_positions'
        }

        assert set(calc.config.keys()) == expected_keys
        assert calc.config == DEFAULT_SCORING_CONFIG

    def test_init_custom_config(self):
        """Test calculator initialization with custom configuration"""
        custom_config = {
            'enable_adp_adjustment': False,
            'adp_excellent_multiplier': 1.2
        }

        calc = EnhancedScoringCalculator(custom_config)

        # Should merge with defaults
        assert calc.config['enable_adp_adjustment'] is False
        assert calc.config['adp_excellent_multiplier'] == 1.2
        # Other values should remain default
        assert calc.config['enable_player_rating_adjustment'] is True


class TestBasicScoringCalculations:
    """Test basic scoring calculations without adjustments"""

    def test_zero_base_score(self):
        """Test handling of zero base score"""
        calc = EnhancedScoringCalculator()

        result = calc.calculate_enhanced_score(
            base_fantasy_points=0.0,
            position="RB",
            adp=100.0,
            player_rating=50.0
        )

        assert result['enhanced_score'] == 0.0
        assert result['base_score'] == 0.0
        assert result['total_multiplier'] == 1.0
        assert result['adjustments'] == {}

    def test_negative_base_score(self):
        """Test handling of negative base score"""
        calc = EnhancedScoringCalculator()

        result = calc.calculate_enhanced_score(
            base_fantasy_points=-5.0,
            position="DST"  # DST can have negative scores
        )

        assert result['enhanced_score'] == 0.0
        assert result['base_score'] == -5.0

    def test_no_adjustments_all_disabled(self):
        """Test calculation with all adjustments disabled"""
        config = {
            'enable_adp_adjustment': False,
            'enable_player_rating_adjustment': False,
            'enable_team_quality_adjustment': False
        }
        calc = EnhancedScoringCalculator(config)

        result = calc.calculate_enhanced_score(
            base_fantasy_points=100.0,
            position="RB",
            adp=50.0,
            player_rating=80.0,
        )

        assert result['enhanced_score'] == 100.0
        assert result['total_multiplier'] == 1.0
        assert result['adjustments'] == {}

    def test_no_adjustments_no_data(self):
        """Test calculation with no enhancement data provided"""
        calc = EnhancedScoringCalculator()

        result = calc.calculate_enhanced_score(
            base_fantasy_points=150.0,
            position="QB"
        )

        assert result['enhanced_score'] == 150.0
        assert result['total_multiplier'] == 1.0
        assert result['adjustments'] == {}


class TestADPAdjustments:
    """Test ADP (Average Draft Position) adjustment calculations"""

    def test_adp_excellent_boost(self):
        """Test ADP adjustment for excellent draft position (< 50)"""
        calc = EnhancedScoringCalculator()

        result = calc.calculate_enhanced_score(
            base_fantasy_points=100.0,
            position="RB",
            adp=25.0  # Excellent ADP
        )

        assert result['enhanced_score'] == 118.0  # 100 * 1.18 (optimized multiplier)
        assert result['adjustments']['adp'] == 1.18  # Optimized from 1.15
        assert 'adp' not in result['missing_data']

    def test_adp_good_boost(self):
        """Test ADP adjustment for good draft position (50-100)"""
        calc = EnhancedScoringCalculator()

        result = calc.calculate_enhanced_score(
            base_fantasy_points=100.0,
            position="RB",
            adp=75.0  # Good ADP
        )

        assert result['enhanced_score'] == 108.0  # 100 * 1.08
        assert result['adjustments']['adp'] == 1.08

    def test_adp_poor_penalty(self):
        """Test ADP adjustment for poor draft position (> 200)"""
        calc = EnhancedScoringCalculator()

        result = calc.calculate_enhanced_score(
            base_fantasy_points=100.0,
            position="RB",
            adp=250.0  # Poor ADP
        )

        assert result['enhanced_score'] == 70.0  # 100 * 0.52 capped at 0.70 min = 70.0
        assert result['adjustments']['adp'] == 0.52  # Optimized from 0.92 (but capped at 0.70 in final)

    def test_adp_neutral_range(self):
        """Test ADP adjustment for neutral range (100-200)"""
        calc = EnhancedScoringCalculator()

        result = calc.calculate_enhanced_score(
            base_fantasy_points=100.0,
            position="RB",
            adp=150.0  # Neutral ADP
        )

        # Should be no adjustment in neutral range (multiplier = 1.0)
        assert result['enhanced_score'] == 100.0
        assert result['adjustments']['adp'] == 1.0

    def test_adp_boundary_values(self):
        """Test ADP adjustment at exact boundary values"""
        calc = EnhancedScoringCalculator()

        # Test at exact excellent threshold (50)
        result1 = calc.calculate_enhanced_score(100.0, "RB", adp=50.0)
        assert result1['adjustments']['adp'] == 1.18  # Optimized from 1.15

        # Test at exact good threshold (100)
        result2 = calc.calculate_enhanced_score(100.0, "RB", adp=100.0)
        assert result2['adjustments']['adp'] == 1.08

        # Test at exact poor threshold (200)
        result3 = calc.calculate_enhanced_score(100.0, "RB", adp=200.0)
        assert result3['adjustments']['adp'] == 0.52  # Poor ADP (optimized from 0.92)

    def test_adp_disabled(self):
        """Test that ADP adjustments are ignored when disabled"""
        config = {'enable_adp_adjustment': False}
        calc = EnhancedScoringCalculator(config)

        result = calc.calculate_enhanced_score(
            base_fantasy_points=100.0,
            position="RB",
            adp=25.0  # Would normally give excellent boost
        )

        assert result['enhanced_score'] == 100.0
        assert 'adp' not in result['adjustments']
        assert 'adp' not in result['missing_data']


class TestPlayerRatingAdjustments:
    """Test ESPN player rating adjustment calculations"""

    def test_player_rating_excellent_boost(self):
        """Test player rating adjustment for excellent rating (>= 80)"""
        calc = EnhancedScoringCalculator()

        result = calc.calculate_enhanced_score(
            base_fantasy_points=100.0,
            position="RB",
            player_rating=85.0  # Excellent rating
        )

        assert result['enhanced_score'] == 121.0  # 100 * 1.21 (optimized from 1.20)
        assert result['adjustments']['player_rating'] == 1.21  # Optimized

    def test_player_rating_good_boost(self):
        """Test player rating adjustment for good rating (60-80)"""
        calc = EnhancedScoringCalculator()

        result = calc.calculate_enhanced_score(
            base_fantasy_points=100.0,
            position="RB",
            player_rating=70.0  # Good rating
        )

        assert result['enhanced_score'] == 115.0  # 100 * 1.15 (optimized from 1.10)
        assert result['adjustments']['player_rating'] == 1.15  # Optimized

    def test_player_rating_poor_penalty(self):
        """Test player rating adjustment for poor rating (<= 30)"""
        calc = EnhancedScoringCalculator()

        result = calc.calculate_enhanced_score(
            base_fantasy_points=100.0,
            position="RB",
            player_rating=25.0  # Poor rating
        )

        assert result['enhanced_score'] == 94.0  # 100 * 0.94 (optimized from 0.90)
        assert result['adjustments']['player_rating'] == 0.94  # Optimized

    def test_player_rating_neutral_range(self):
        """Test player rating adjustment for neutral range (30-60)"""
        calc = EnhancedScoringCalculator()

        # Test middle of neutral range
        result = calc.calculate_enhanced_score(
            base_fantasy_points=100.0,
            position="RB",
            player_rating=45.0  # Neutral rating
        )

        # Should get neutral adjustment (multiplier = 1.0) at middle of range
        assert result['enhanced_score'] == 100.0
        assert result['adjustments']['player_rating'] == 1.0

    def test_player_rating_max_boost_cap(self):
        """Test that player rating boost is capped at max_boost"""
        # Set a lower max boost to test the cap
        config = {'player_rating_max_boost': 1.15}  # Cap at 15%
        calc = EnhancedScoringCalculator(config)

        result = calc.calculate_enhanced_score(
            base_fantasy_points=100.0,
            position="RB",
            player_rating=90.0  # Would normally give 20% boost
        )

        assert result['enhanced_score'] == 115.0  # Capped at 15%
        assert result['adjustments']['player_rating'] == 1.15

    def test_player_rating_disabled(self):
        """Test that player rating adjustments are ignored when disabled"""
        config = {'enable_player_rating_adjustment': False}
        calc = EnhancedScoringCalculator(config)

        result = calc.calculate_enhanced_score(
            base_fantasy_points=100.0,
            position="RB",
            player_rating=85.0  # Would normally give excellent boost
        )

        assert result['enhanced_score'] == 100.0
        assert 'player_rating' not in result['adjustments']


class TestCombinedAdjustments:
    """Test combinations of multiple adjustments"""

    def test_all_positive_adjustments(self):
        """Test combination of all positive adjustments"""
        calc = EnhancedScoringCalculator()

        result = calc.calculate_enhanced_score(
            base_fantasy_points=100.0,
            position="RB",
            adp=40.0,  # Excellent ADP (+15%)
            player_rating=85.0,  # Excellent rating (+20%)
        )

        # Combined ADP (+18%) and Rating (+21%) = 100 * 1.18 * 1.21 = 142.78 (optimized)
        assert result['enhanced_score'] == 142.78
        assert result['total_multiplier'] == 1.428
        assert len(result['adjustments']) == 2

    def test_mixed_adjustments(self):
        """Test combination of positive and negative adjustments"""
        calc = EnhancedScoringCalculator()

        result = calc.calculate_enhanced_score(
            base_fantasy_points=100.0,
            position="RB",
            adp=25.0,  # Excellent ADP (+18%)
            player_rating=20.0,  # Poor rating (-6%)
        )

        # 100 * 1.18 * 0.94 = 110.92 (optimized values)
        expected_score = 100.0 * 1.18 * 0.94
        assert abs(result['enhanced_score'] - expected_score) < 0.01

    def test_max_total_adjustment_cap(self):
        """Test that total adjustment is capped at maximum"""
        # Set a low max cap to test
        config = {'max_total_adjustment': 1.25}  # Cap at 25%
        calc = EnhancedScoringCalculator(config)

        result = calc.calculate_enhanced_score(
            base_fantasy_points=100.0,
            position="RB",
            adp=10.0,  # Excellent ADP
            player_rating=95.0,  # Excellent rating
        )

        assert result['enhanced_score'] == 125.0  # Capped at 25%
        assert result['total_multiplier'] == 1.25

    def test_min_total_adjustment_cap(self):
        """Test that total adjustment is capped at minimum"""
        # Set a high min cap to test
        config = {'min_total_adjustment': 0.85}  # Cap penalty at 15%
        calc = EnhancedScoringCalculator(config)

        result = calc.calculate_enhanced_score(
            base_fantasy_points=100.0,
            position="RB",
            adp=300.0,  # Poor ADP
            player_rating=10.0,  # Poor rating
        )

        assert result['enhanced_score'] == 85.0  # Capped at 15% penalty
        assert result['total_multiplier'] == 0.85

    def test_hunt_vs_henderson_scenario(self):
        """Test the specific Hunt vs Henderson scenario"""
        calc = EnhancedScoringCalculator()

        # Kareem Hunt data
        hunt_result = calc.calculate_enhanced_score(
            base_fantasy_points=135.54,
            position="RB",
            adp=120.0,
            player_rating=45.0,
        )

        # TreVeyon Henderson data
        henderson_result = calc.calculate_enhanced_score(
            base_fantasy_points=121.97,
            position="RB",
            adp=85.0,
            player_rating=65.0,
        )

        # Henderson should score higher due to better ADP and rating adjustments
        assert henderson_result['enhanced_score'] > hunt_result['enhanced_score']

        # Verify the specific expected scores
        assert abs(hunt_result['enhanced_score'] - 135.54) < 0.01  # No adjustments
        # Henderson: 121.97 * 1.08 * 1.15 = 151.49 (rounded)
        assert abs(henderson_result['enhanced_score'] - 151.49) < 0.01


class TestAdjustmentSummary:
    """Test the adjustment summary functionality"""

    def test_no_adjustments_summary(self):
        """Test adjustment summary when no adjustments are made"""
        calc = EnhancedScoringCalculator()

        result = calc.calculate_enhanced_score(100.0, "RB")
        summary = calc.get_adjustment_summary(result)

        assert summary == "No adjustments applied"

    def test_single_positive_adjustment_summary(self):
        """Test adjustment summary for single positive adjustment"""
        calc = EnhancedScoringCalculator()

        result = calc.calculate_enhanced_score(
            base_fantasy_points=100.0,
            position="RB",
            adp=40.0
        )

        summary = calc.get_adjustment_summary(result)
        assert "ADP boost (+18.0%)" in summary  # Optimized from +15.0%
        assert "Total: +18.0%" in summary

    def test_single_negative_adjustment_summary(self):
        """Test adjustment summary for single negative adjustment"""
        calc = EnhancedScoringCalculator()

        result = calc.calculate_enhanced_score(
            base_fantasy_points=100.0,
            position="RB",
            adp=250.0
        )

        summary = calc.get_adjustment_summary(result)
        # The summary shows the raw penalty (48%), but the total is capped at 30%
        assert "ADP penalty (48.0%)" in summary  # 0.52 multiplier = 48% penalty
        assert "Total: -30.0%" in summary  # Capped at 30% (0.70 min)

    def test_multiple_adjustments_summary(self):
        """Test adjustment summary for multiple adjustments"""
        calc = EnhancedScoringCalculator()

        result = calc.calculate_enhanced_score(
            base_fantasy_points=100.0,
            position="RB",
            adp=40.0,  # +18%
            player_rating=70.0,  # +15%
        )

        summary = calc.get_adjustment_summary(result)
        assert "ADP boost (+18.0%)" in summary  # Optimized from +15.0%
        assert "Rating boost (+15.0%)" in summary  # Optimized from +10.0%
        assert "Total:" in summary
        # No team boost expected without team ranking data


class TestConvenienceFunction:
    """Test the convenience function for single player calculations"""

    def test_calculate_enhanced_player_score_basic(self):
        """Test basic usage of convenience function"""
        score = calculate_enhanced_player_score(
            base_fantasy_points=100.0,
            position="RB",
            adp=50.0
        )

        assert score == 118.0  # 100 * 1.18 (ADP 50 is excellent, optimized from 1.15)

    def test_calculate_enhanced_player_score_with_config(self):
        """Test convenience function with custom config"""
        custom_config = {'adp_good_multiplier': 1.15}

        score = calculate_enhanced_player_score(
            base_fantasy_points=100.0,
            position="RB",
            adp=75.0,
            config=custom_config
        )

        assert score == 115.0  # 100 * 1.15


class TestFantasyPlayerIntegration:
    """Test integration with FantasyPlayer objects"""

    def test_fantasy_player_with_enhanced_data(self):
        """Test enhanced scoring with FantasyPlayer that has enhanced data"""
        player = FantasyPlayer(
            id="12345",
            name="Test Player",
            team="KC",
            position="RB",
            fantasy_points=100.0,
            average_draft_position=50.0,
            player_rating=70.0,
        )

        calc = EnhancedScoringCalculator()
        result = calc.calculate_enhanced_score(
            base_fantasy_points=player.fantasy_points,
            position=player.position,
            adp=player.average_draft_position,
            player_rating=player.player_rating,
        )

        # Should get multiple adjustments
        assert result['enhanced_score'] > player.fantasy_points
        assert len(result['adjustments']) > 1

    def test_fantasy_player_without_enhanced_data(self):
        """Test enhanced scoring with FantasyPlayer that lacks enhanced data"""
        player = FantasyPlayer(
            id="12345",
            name="Test Player",
            team="KC",
            position="RB",
            fantasy_points=100.0
        )

        calc = EnhancedScoringCalculator()
        result = calc.calculate_enhanced_score(
            base_fantasy_points=player.fantasy_points,
            position=player.position,
            adp=getattr(player, 'average_draft_position', None),
            player_rating=getattr(player, 'player_rating', None),
        )

        # Should have no adjustments
        assert result['enhanced_score'] == player.fantasy_points
        assert result['adjustments'] == {}


class TestEdgeCases:
    """Test edge cases and error conditions"""

    def test_none_values_handling(self):
        """Test handling of None values for optional parameters"""
        calc = EnhancedScoringCalculator()

        result = calc.calculate_enhanced_score(
            base_fantasy_points=100.0,
            position="RB",
            adp=None,
            player_rating=None,
        )

        assert result['enhanced_score'] == 100.0
        assert result['adjustments'] == {}

    def test_extreme_values(self):
        """Test handling of extreme input values"""
        calc = EnhancedScoringCalculator()

        # Very high values
        result1 = calc.calculate_enhanced_score(
            base_fantasy_points=999999.0,
            position="RB",
            adp=1.0,  # Best possible ADP
            player_rating=100.0,  # Max rating
        )

        assert result1['enhanced_score'] > 999999.0
        assert result1['enhanced_score'] <= 999999.0 * calc.config['max_total_adjustment']

        # Very low values
        result2 = calc.calculate_enhanced_score(
            base_fantasy_points=0.1,
            position="RB",
            adp=500.0,  # Terrible ADP
            player_rating=0.0,  # Min rating
        )

        assert result2['enhanced_score'] >= 0.1 * calc.config['min_total_adjustment']

    def test_invalid_position_types(self):
        """Test handling of invalid or unusual position types"""
        calc = EnhancedScoringCalculator()

        for position in ["", "INVALID", "123", None]:
            # Convert None to string to avoid TypeError
            pos_str = str(position) if position is not None else "None"

            result = calc.calculate_enhanced_score(
                base_fantasy_points=100.0,
                position=pos_str,
            )

            # Unknown positions should get no team adjustment
            assert result['enhanced_score'] == 100.0
            assert 'team_quality' not in result['adjustments']

    def test_boundary_rank_values(self):
        """Test calculations without team ranking data"""
        calc = EnhancedScoringCalculator()

        # Without team ranking data, should have no team adjustments
        result1 = calc.calculate_enhanced_score(
            base_fantasy_points=100.0,
            position="RB",
        )
        # No team adjustment expected
        assert result1['enhanced_score'] == 100.0

        # Test with different position
        result2 = calc.calculate_enhanced_score(
            base_fantasy_points=100.0,
            position="QB",
        )
        # Still no team adjustment expected
        assert result2['enhanced_score'] == 100.0

    def test_rounding_precision(self):
        """Test that results are properly rounded"""
        calc = EnhancedScoringCalculator()

        result = calc.calculate_enhanced_score(
            base_fantasy_points=100.0,
            position="RB",
            adp=25.0  # Creates 1.18 multiplier (optimized)
        )

        # Result should be rounded to 2 decimal places
        assert result['enhanced_score'] == 118.0
        # Multiplier should be rounded to 3 decimal places
        assert result['total_multiplier'] == 1.18

    def test_configuration_validation(self):
        """Test that invalid configurations are handled properly"""
        # This would ideally validate config in a real implementation
        # For now, just test that bad configs don't crash
        bad_config = {
            'max_total_adjustment': 0.5,  # Less than min (would be problematic)
            'min_total_adjustment': 2.0   # Greater than max
        }

        calc = EnhancedScoringCalculator(bad_config)

        # Should still work, just with potentially odd results
        result = calc.calculate_enhanced_score(
            base_fantasy_points=100.0,
            position="RB"
        )

        assert isinstance(result['enhanced_score'], float)


class TestLogging:
    """Test logging functionality"""

    def test_logging_setup(self):
        """Test that logger is properly set up"""
        calc = EnhancedScoringCalculator()

        assert hasattr(calc, 'logger')
        assert isinstance(calc.logger, logging.Logger)

    def test_debug_logging_content(self, caplog):
        """Test that appropriate debug messages are logged"""
        with caplog.at_level(logging.DEBUG):
            calc = EnhancedScoringCalculator()

            # This would require setting up debug logging properly
            # For now just verify no crashes occur
            result = calc.calculate_enhanced_score(
                base_fantasy_points=100.0,
                position="RB",
                adp=50.0
            )

            assert result is not None


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])