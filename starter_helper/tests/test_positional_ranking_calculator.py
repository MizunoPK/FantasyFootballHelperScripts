#!/usr/bin/env python3
"""
Unit tests for PositionalRankingCalculator class in starter_helper.

Tests the positional ranking calculations used for enhanced
lineup recommendations based on team offensive/defensive rankings.

Author: Generated for NFL Fantasy Data Collection
Last Updated: September 2025
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
import logging

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from shared_files.positional_ranking_calculator import PositionalRankingCalculator
from shared_files.TeamData import save_teams_to_csv, TeamData


class TestPositionalRankingCalculator:
    """Test the PositionalRankingCalculator class functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        # Create sample team data with various ranks
        self.sample_teams = [
            TeamData(team='KC', offensive_rank=1, defensive_rank=5),      # Elite offense, good defense
            TeamData(team='BUF', offensive_rank=4, defensive_rank=13),    # Good offense, average defense
            TeamData(team='PHI', offensive_rank=8, defensive_rank=17),    # Good offense, average defense
            TeamData(team='DAL', offensive_rank=12, defensive_rank=22),   # Average offense, poor defense
            TeamData(team='NYG', offensive_rank=28, defensive_rank=2),    # Poor offense, elite defense
            TeamData(team='CHI', offensive_rank=30, defensive_rank=30)    # Poor offense, poor defense
        ]

    def create_temp_teams_file(self):
        """Create a temporary teams.csv file with sample data."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        save_teams_to_csv(self.sample_teams, temp_file.name)
        temp_file.close()
        return temp_file.name

    def test_calculator_initialization_with_file(self):
        """Test PositionalRankingCalculator initialization with valid file."""
        temp_path = self.create_temp_teams_file()

        try:
            calc = PositionalRankingCalculator(temp_path)

            assert calc.is_positional_ranking_available()
            assert len(calc.get_available_teams()) == 6
            assert 'KC' in calc.get_available_teams()
            assert 'PHI' in calc.get_available_teams()

        finally:
            os.unlink(temp_path)

    def test_calculator_initialization_nonexistent_file(self):
        """Test calculator initialization with nonexistent file."""
        with patch('logging.getLogger') as mock_logger:
            mock_logger_instance = MagicMock()
            mock_logger.return_value = mock_logger_instance

            calc = PositionalRankingCalculator('/nonexistent/teams.csv')

            assert not calc.is_positional_ranking_available()
            assert len(calc.get_available_teams()) == 0

    def test_calculator_default_config(self):
        """Test calculator with default configuration."""
        temp_path = self.create_temp_teams_file()

        try:
            calc = PositionalRankingCalculator(temp_path)

            config = calc.config

            # Check key config values
            assert config['enable_adjustments'] is True
            assert config['adjustment_weight'] == 0.15
            assert config['excellent_threshold'] == 5
            assert config['good_threshold'] == 12
            assert config['poor_threshold'] == 25

            # Check multipliers (conservative values)
            assert config['excellent_matchup'] == 1.1
            assert config['good_matchup'] == 1.05
            assert config['neutral_matchup'] == 1.0
            assert config['bad_matchup'] == 0.95
            assert config['terrible_matchup'] == 0.9

        finally:
            os.unlink(temp_path)

    def test_calculator_custom_config(self):
        """Test calculator with custom configuration."""
        temp_path = self.create_temp_teams_file()

        custom_config = {
            'enable_adjustments': True,
            'adjustment_weight': 0.10,  # Custom weight
            'excellent_threshold': 3,
            'excellent_matchup': 1.20,
            'log_adjustments': False
        }

        try:
            calc = PositionalRankingCalculator(temp_path, custom_config)

            # Should merge with defaults
            assert calc.config['adjustment_weight'] == 0.10
            assert calc.config['excellent_threshold'] == 3
            assert calc.config['excellent_matchup'] == 1.20
            assert calc.config['log_adjustments'] is False

            # Should keep other defaults
            assert calc.config['good_threshold'] == 12  # Default value

        finally:
            os.unlink(temp_path)

    def test_offensive_positions_adjustment(self):
        """Test positional adjustments for offensive positions."""
        temp_path = self.create_temp_teams_file()

        try:
            calc = PositionalRankingCalculator(temp_path)

            # Test QB with elite offense (KC, rank 1)
            adjusted_points, explanation = calc.calculate_positional_adjustment(
                player_team='KC',
                position='QB',
                base_points=30.0
            )

            # Should get excellent multiplier: 1.1 * 0.15 weight = 1 + (0.1 * 0.15) = 1.015
            expected_multiplier = 1.0 + (1.1 - 1.0) * 0.15  # 1.015
            expected_points = 30.0 * expected_multiplier

            assert abs(adjusted_points - expected_points) < 0.01
            assert 'Elite offensive' in explanation
            assert 'rank 1' in explanation

            # Test RB with good offense (BUF, rank 4)
            adjusted_points, explanation = calc.calculate_positional_adjustment(
                player_team='BUF',
                position='RB',
                base_points=20.0
            )

            # Should get excellent multiplier (rank 4 <= 5)
            expected_points = 20.0 * (1.0 + (1.1 - 1.0) * 0.15)
            assert abs(adjusted_points - expected_points) < 0.01
            assert 'Elite offensive' in explanation

            # Test WR with average offense (DAL, rank 12)
            adjusted_points, explanation = calc.calculate_positional_adjustment(
                player_team='DAL',
                position='WR',
                base_points=15.0
            )

            # Should get good multiplier (rank 12 <= 12)
            expected_points = 15.0 * (1.0 + (1.05 - 1.0) * 0.15)
            assert abs(adjusted_points - expected_points) < 0.01
            assert 'Good offensive' in explanation

        finally:
            os.unlink(temp_path)

    def test_defensive_positions_adjustment(self):
        """Test positional adjustments for defensive positions."""
        temp_path = self.create_temp_teams_file()

        try:
            calc = PositionalRankingCalculator(temp_path)

            # Test DST with elite defense (NYG, rank 2)
            adjusted_points, explanation = calc.calculate_positional_adjustment(
                player_team='NYG',
                position='DST',
                base_points=12.0
            )

            # Should get excellent multiplier using defensive rank
            expected_multiplier = 1.0 + (1.1 - 1.0) * 0.15
            expected_points = 12.0 * expected_multiplier

            assert abs(adjusted_points - expected_points) < 0.01
            assert 'Elite defensive' in explanation
            assert 'rank 2' in explanation

            # Test DST with poor defense (CHI, rank 30)
            adjusted_points, explanation = calc.calculate_positional_adjustment(
                player_team='CHI',
                position='DST',
                base_points=8.0
            )

            # Should get bad multiplier (rank 30 >= 25)
            expected_points = 8.0 * (1.0 + (0.95 - 1.0) * 0.15)
            assert abs(adjusted_points - expected_points) < 0.01
            assert 'Poor defensive' in explanation

        finally:
            os.unlink(temp_path)

    def test_kicker_positions_adjustment(self):
        """Test positional adjustments for kickers."""
        temp_path = self.create_temp_teams_file()

        try:
            calc = PositionalRankingCalculator(temp_path)

            # Test kicker with good offense (should use offensive rank)
            adjusted_points, explanation = calc.calculate_positional_adjustment(
                player_team='KC',  # Elite offense
                position='K',
                base_points=10.0
            )

            # Should use offensive rank for kickers
            expected_multiplier = 1.0 + (1.1 - 1.0) * 0.15
            expected_points = 10.0 * expected_multiplier

            assert abs(adjusted_points - expected_points) < 0.01
            assert 'Elite offensive (kicking)' in explanation

        finally:
            os.unlink(temp_path)

    def test_unknown_position_no_adjustment(self):
        """Test that unknown positions get no adjustment."""
        temp_path = self.create_temp_teams_file()

        try:
            calc = PositionalRankingCalculator(temp_path)

            adjusted_points, explanation = calc.calculate_positional_adjustment(
                player_team='KC',
                position='UNKNOWN',
                base_points=20.0
            )

            assert adjusted_points == 20.0  # No change
            assert 'unknown position' in explanation

        finally:
            os.unlink(temp_path)

    def test_unknown_team_no_adjustment(self):
        """Test that unknown teams get no adjustment."""
        temp_path = self.create_temp_teams_file()

        try:
            calc = PositionalRankingCalculator(temp_path)

            adjusted_points, explanation = calc.calculate_positional_adjustment(
                player_team='UNKNOWN',
                position='QB',
                base_points=25.0
            )

            assert adjusted_points == 25.0  # No change
            assert 'team UNKNOWN not found' in explanation

        finally:
            os.unlink(temp_path)

    def test_adjustments_disabled(self):
        """Test calculator with adjustments disabled."""
        temp_path = self.create_temp_teams_file()

        config = {'enable_adjustments': False}

        try:
            calc = PositionalRankingCalculator(temp_path, config)

            adjusted_points, explanation = calc.calculate_positional_adjustment(
                player_team='KC',
                position='QB',
                base_points=30.0
            )

            assert adjusted_points == 30.0  # No change
            assert 'rankings unavailable' in explanation

        finally:
            os.unlink(temp_path)

    def test_missing_rank_data(self):
        """Test calculation when rank data is missing."""
        # Create team data with missing ranks
        teams_with_missing_ranks = [
            TeamData(team='TEST', offensive_rank=None, defensive_rank=None)
        ]

        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        save_teams_to_csv(teams_with_missing_ranks, temp_file.name)
        temp_file.close()

        try:
            calc = PositionalRankingCalculator(temp_file.name)

            # Test offensive position with missing offensive rank
            adjusted_points, explanation = calc.calculate_positional_adjustment(
                player_team='TEST',
                position='QB',
                base_points=25.0
            )

            assert adjusted_points == 25.0  # No change
            assert 'rank unavailable' in explanation

            # Test defensive position with missing defensive rank
            adjusted_points, explanation = calc.calculate_positional_adjustment(
                player_team='TEST',
                position='DST',
                base_points=10.0
            )

            assert adjusted_points == 10.0  # No change
            assert 'rank unavailable' in explanation

        finally:
            os.unlink(temp_file.name)

    def test_rank_tier_descriptions(self):
        """Test rank tier description logic."""
        temp_path = self.create_temp_teams_file()

        try:
            calc = PositionalRankingCalculator(temp_path)

            # Test different rank tiers
            assert calc._get_rank_tier_description(1) == "Elite"
            assert calc._get_rank_tier_description(5) == "Elite"
            assert calc._get_rank_tier_description(6) == "Good"
            assert calc._get_rank_tier_description(12) == "Good"
            assert calc._get_rank_tier_description(13) == "Average"
            assert calc._get_rank_tier_description(24) == "Average"
            assert calc._get_rank_tier_description(25) == "Poor"
            assert calc._get_rank_tier_description(32) == "Poor"

        finally:
            os.unlink(temp_path)

    def test_team_summary(self):
        """Test team summary generation."""
        temp_path = self.create_temp_teams_file()

        try:
            calc = PositionalRankingCalculator(temp_path)

            # Test known team
            summary = calc.get_team_summary('KC')
            assert 'KC:' in summary
            assert 'Elite offense' in summary
            assert '#1' in summary
            assert 'Elite defense' in summary
            assert '#5' in summary

            # Test unknown team
            summary = calc.get_team_summary('UNKNOWN')
            assert summary is None

        finally:
            os.unlink(temp_path)

    def test_reload_functionality(self):
        """Test reloading team data."""
        temp_path = self.create_temp_teams_file()

        try:
            calc = PositionalRankingCalculator(temp_path)

            # Initial calculation
            initial_points, _ = calc.calculate_positional_adjustment(
                player_team='KC',
                position='QB',
                base_points=30.0
            )

            # Modify file with different ranks
            modified_teams = [
                TeamData(team='KC', offensive_rank=20, defensive_rank=25)  # Much worse ranks
            ]
            save_teams_to_csv(modified_teams, temp_path)

            # Reload and recalculate
            calc.reload_team_data()
            new_points, explanation = calc.calculate_positional_adjustment(
                player_team='KC',
                position='QB',
                base_points=30.0
            )

            # Should now be neutral (no adjustment for rank 20)
            assert new_points == 30.0  # Neutral adjustment
            assert new_points != initial_points  # Should be different from initial

        finally:
            os.unlink(temp_path)


if __name__ == '__main__':
    pytest.main([__file__])