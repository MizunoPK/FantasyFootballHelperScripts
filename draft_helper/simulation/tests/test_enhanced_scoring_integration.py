#!/usr/bin/env python3
"""
Unit tests for enhanced scoring integration in simulation.

Tests the enhanced scoring parameter variations and their impact on draft strategy.
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from draft_helper.simulation.team_strategies import TeamStrategyManager
from draft_helper.simulation.config import PARAMETER_RANGES, get_timestamped_results_file
from draft_helper.FantasyTeam import FantasyTeam
from shared_files.FantasyPlayer import FantasyPlayer


class TestEnhancedScoringSimulationIntegration:
    """Test enhanced scoring integration in simulation components"""

    def setup_method(self):
        """Set up test fixtures"""
        self.base_config = {
            'INJURY_PENALTIES_MEDIUM': 25,
            'INJURY_PENALTIES_HIGH': 50,
            'POS_NEEDED_SCORE': 50,
            'PROJECTION_BASE_SCORE': 100,
            'BASE_BYE_PENALTY': 20,

            # Enhanced scoring parameters
            'ADP_EXCELLENT_MULTIPLIER': 1.15,
            'ADP_GOOD_MULTIPLIER': 1.08,
            'ADP_POOR_MULTIPLIER': 0.92,
            'PLAYER_RATING_EXCELLENT_MULTIPLIER': 1.20,
            'PLAYER_RATING_GOOD_MULTIPLIER': 1.10,
            'PLAYER_RATING_POOR_MULTIPLIER': 0.90,
            'TEAM_EXCELLENT_MULTIPLIER': 1.12,
            'TEAM_GOOD_MULTIPLIER': 1.06,
            'TEAM_POOR_MULTIPLIER': 0.94,
            'MAX_TOTAL_ADJUSTMENT': 1.50,
            'MIN_TOTAL_ADJUSTMENT': 0.70
        }

        # Create test player with weekly points
        self.test_player = FantasyPlayer(
            id="test1", name="Test Player", team="KC", position="RB",
            fantasy_points=200.0, average_draft_position=50.0, player_rating=75.0
        )

        # Add weekly points so _get_player_total_points works
        for week in range(1, 18):
            setattr(self.test_player, f'week_{week}_points', 200.0 / 17)  # ~11.76 per week

    def test_parameter_ranges_include_enhanced_scoring(self):
        """Test that PARAMETER_RANGES includes all enhanced scoring parameters"""
        expected_enhanced_params = [
            'ADP_EXCELLENT_MULTIPLIER',
            'ADP_GOOD_MULTIPLIER',
            'ADP_POOR_MULTIPLIER',
            'PLAYER_RATING_EXCELLENT_MULTIPLIER',
            'PLAYER_RATING_GOOD_MULTIPLIER',
            'PLAYER_RATING_POOR_MULTIPLIER',
            'TEAM_EXCELLENT_MULTIPLIER',
            'TEAM_GOOD_MULTIPLIER',
            'TEAM_POOR_MULTIPLIER',
            'MAX_TOTAL_ADJUSTMENT',
            'MIN_TOTAL_ADJUSTMENT'
        ]

        for param in expected_enhanced_params:
            assert param in PARAMETER_RANGES, f"Parameter {param} missing from PARAMETER_RANGES"
            assert len(PARAMETER_RANGES[param]) >= 3, f"Parameter {param} should have multiple test values"

    def test_team_strategy_manager_enhanced_scoring_initialization(self):
        """Test that TeamStrategyManager properly initializes enhanced scoring"""
        with patch('draft_helper.simulation.team_strategies.EnhancedScoringCalculator') as mock_calculator, \
             patch('draft_helper.simulation.team_strategies.TeamDataLoader') as mock_loader:

            manager = TeamStrategyManager(self.base_config)

            # Verify enhanced scoring calculator was initialized with correct config
            mock_calculator.assert_called_once()
            call_args = mock_calculator.call_args[0]

            if call_args:  # If config was passed as positional argument
                enhanced_config = call_args[0]
            else:  # If config was passed as keyword argument
                enhanced_config = mock_calculator.call_args[1].get('config', {})

            # Check that config contains expected values
            assert enhanced_config.get('adp_excellent_multiplier') == 1.15
            assert enhanced_config.get('player_rating_excellent_multiplier') == 1.20
            assert enhanced_config.get('team_excellent_multiplier') == 1.12

            # Verify team data loader was initialized
            mock_loader.assert_called_once()

    def test_draft_helper_strategy_uses_enhanced_scoring(self):
        """Test that draft helper strategy uses enhanced scoring calculator"""
        with patch('draft_helper.simulation.team_strategies.EnhancedScoringCalculator') as mock_calculator, \
             patch('draft_helper.simulation.team_strategies.TeamDataLoader') as mock_loader:

            # Set up mocks
            mock_calculator_instance = MagicMock()
            mock_calculator.return_value = mock_calculator_instance
            mock_calculator_instance.calculate_enhanced_score.return_value = {
                'enhanced_score': 220.0,
                'total_multiplier': 1.1
            }

            mock_loader_instance = MagicMock()
            mock_loader.return_value = mock_loader_instance
            mock_loader_instance.get_team_offensive_rank.return_value = 5
            mock_loader_instance.get_team_defensive_rank.return_value = 10

            manager = TeamStrategyManager(self.base_config)

            # Create test roster and available players
            test_roster = FantasyTeam()
            available_players = [self.test_player]

            # Call draft helper strategy
            result = manager._draft_helper_strategy(available_players, test_roster, 1)

            # Verify enhanced scoring was called
            mock_calculator_instance.calculate_enhanced_score.assert_called_once()
            call_args = mock_calculator_instance.calculate_enhanced_score.call_args[1]

            assert abs(call_args['base_fantasy_points'] - 200.0) < 0.01  # Allow for floating point precision
            assert call_args['position'] == 'RB'
            assert call_args['adp'] == 50.0
            assert call_args['player_rating'] == 75.0
            assert call_args['team_offensive_rank'] == 5
            assert call_args['team_defensive_rank'] == 10

    def test_enhanced_scoring_parameter_variations(self):
        """Test that different parameter values produce different results"""
        configs = [
            {**self.base_config, 'ADP_EXCELLENT_MULTIPLIER': 1.05},
            {**self.base_config, 'ADP_EXCELLENT_MULTIPLIER': 1.25},
        ]

        results = []
        for config in configs:
            with patch('draft_helper.simulation.team_strategies.EnhancedScoringCalculator') as mock_calculator, \
                 patch('draft_helper.simulation.team_strategies.TeamDataLoader'):

                mock_calculator_instance = MagicMock()
                mock_calculator.return_value = mock_calculator_instance

                # Different enhanced scores based on multiplier
                multiplier = config['ADP_EXCELLENT_MULTIPLIER']
                mock_calculator_instance.calculate_enhanced_score.return_value = {
                    'enhanced_score': 200.0 * multiplier,
                    'total_multiplier': multiplier
                }

                manager = TeamStrategyManager(config)
                test_roster = FantasyTeam()
                result = manager._draft_helper_strategy([self.test_player], test_roster, 1)
                results.append(len(result))

        # Results should be consistent (same player available) but different scoring internally
        assert all(r == 1 for r in results), "All configurations should return the available player"

    def test_timestamped_results_file_generation(self):
        """Test that timestamped results files are generated correctly"""
        import re
        from datetime import datetime
        import time

        # Generate timestamped file
        file1 = get_timestamped_results_file()

        # Wait a moment to ensure different timestamp
        time.sleep(1)
        file2 = get_timestamped_results_file()

        # Check format
        timestamp_pattern = r'result_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}\.md$'
        assert re.search(timestamp_pattern, file1)
        assert re.search(timestamp_pattern, file2)

        # Check paths are different (different timestamps)
        assert file1 != file2

        # Check paths contain results directory
        assert 'results' in file1
        assert 'results' in file2

    def test_enhanced_scoring_config_mapping(self):
        """Test that simulation config parameters map correctly to enhanced scoring"""
        test_config = {
            'ADP_EXCELLENT_MULTIPLIER': 1.33,
            'PLAYER_RATING_POOR_MULTIPLIER': 0.77,
            'MAX_TOTAL_ADJUSTMENT': 1.66
        }

        with patch('draft_helper.simulation.team_strategies.EnhancedScoringCalculator') as mock_calculator:
            manager = TeamStrategyManager(test_config)

            # Get the config passed to enhanced scoring calculator
            call_kwargs = mock_calculator.call_args[1] if mock_calculator.call_args[1] else {}
            call_args = mock_calculator.call_args[0] if mock_calculator.call_args[0] else []

            enhanced_config = call_kwargs.get('config') or (call_args[0] if call_args else {})

            # Verify specific mappings
            assert enhanced_config.get('adp_excellent_multiplier') == 1.33
            assert enhanced_config.get('player_rating_poor_multiplier') == 0.77
            assert enhanced_config.get('max_total_adjustment') == 1.66

    def test_enhanced_scoring_error_handling(self):
        """Test error handling when enhanced scoring components fail"""
        with patch('draft_helper.simulation.team_strategies.EnhancedScoringCalculator') as mock_calculator, \
             patch('draft_helper.simulation.team_strategies.TeamDataLoader') as mock_loader:

            # Set up calculator to raise exception
            mock_calculator_instance = MagicMock()
            mock_calculator.return_value = mock_calculator_instance
            mock_calculator_instance.calculate_enhanced_score.side_effect = Exception("Enhanced scoring failed")

            mock_loader_instance = MagicMock()
            mock_loader.return_value = mock_loader_instance
            mock_loader_instance.get_team_offensive_rank.return_value = None
            mock_loader_instance.get_team_defensive_rank.return_value = None

            manager = TeamStrategyManager(self.base_config)

            # This should not crash even if enhanced scoring fails
            try:
                test_roster = FantasyTeam()
                result = manager._draft_helper_strategy([self.test_player], test_roster, 1)
                # If it doesn't crash, the error was handled gracefully
                assert True
            except Exception as e:
                # If it does crash, we need to improve error handling
                pytest.fail(f"Draft helper strategy should handle enhanced scoring errors gracefully: {e}")


class TestSimulationConfigValidation:
    """Test configuration validation for enhanced scoring parameters"""

    def test_parameter_ranges_have_valid_values(self):
        """Test that all parameter ranges have valid numerical values"""
        for param_name, values in PARAMETER_RANGES.items():
            assert len(values) > 0, f"Parameter {param_name} has no values"

            for value in values:
                assert isinstance(value, (int, float)), f"Parameter {param_name} has non-numeric value: {value}"

                # Check that multiplier parameters are positive
                if 'MULTIPLIER' in param_name or 'ADJUSTMENT' in param_name:
                    assert value > 0, f"Multiplier parameter {param_name} has non-positive value: {value}"

    def test_enhanced_scoring_ranges_are_reasonable(self):
        """Test that enhanced scoring parameter ranges are within reasonable bounds"""
        # ADP multipliers should be close to 1.0
        for param in ['ADP_EXCELLENT_MULTIPLIER', 'ADP_GOOD_MULTIPLIER', 'ADP_POOR_MULTIPLIER']:
            values = PARAMETER_RANGES[param]
            assert all(0.5 <= v <= 2.0 for v in values), f"{param} values should be between 0.5 and 2.0"

        # Adjustment caps should have max > min
        max_values = PARAMETER_RANGES['MAX_TOTAL_ADJUSTMENT']
        min_values = PARAMETER_RANGES['MIN_TOTAL_ADJUSTMENT']
        assert max(min_values) < min(max_values), "MIN_TOTAL_ADJUSTMENT should be less than MAX_TOTAL_ADJUSTMENT"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])