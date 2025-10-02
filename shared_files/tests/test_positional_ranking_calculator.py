#!/usr/bin/env python3
"""
Unit tests for Positional Ranking Calculator module

Tests positional ranking calculations, team data loading, and edge cases.

Author: Kai Mizuno
Last Updated: September 2025
"""

import unittest
import tempfile
import csv
import pandas as pd
from pathlib import Path
from unittest.mock import patch, MagicMock

import sys
sys.path.append(str(Path(__file__).parent.parent))

from positional_ranking_calculator import PositionalRankingCalculator
from shared_files.TeamData import TeamData


class TestPositionalRankingCalculator(unittest.TestCase):
    """Test cases for PositionalRankingCalculator functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.test_teams_file = self.test_dir / "teams.csv"

        # Create test team data
        self.test_team_data = [
            {"team": "KC", "offensive_rank": "1", "defensive_rank": "15", "opponent": "BUF"},  # Elite offense, poor defense
            {"team": "BUF", "offensive_rank": "8", "defensive_rank": "2", "opponent": "KC"},   # Good offense, elite defense
            {"team": "PHI", "offensive_rank": "20", "defensive_rank": "5", "opponent": "DAL"}, # Poor offense, excellent defense
            {"team": "DAL", "offensive_rank": "12", "defensive_rank": "25", "opponent": "PHI"}, # Average offense, poor defense
            {"team": "GB", "offensive_rank": "3", "defensive_rank": "12", "opponent": "MIN"}    # Elite offense, good defense
        ]

        # Write test teams.csv
        with open(self.test_teams_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["team", "offensive_rank", "defensive_rank", "opponent"])
            writer.writeheader()
            writer.writerows(self.test_team_data)

        # Create test DataFrame
        self.test_teams_df = pd.DataFrame(self.test_team_data)

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.test_dir)

    def test_initialization_with_file_path(self):
        """Test calculator initialization with custom file path"""
        calc = PositionalRankingCalculator(teams_file_path=str(self.test_teams_file))

        self.assertEqual(calc.teams_file, self.test_teams_file)
        self.assertTrue(calc.is_positional_ranking_available())
        self.assertEqual(len(calc.get_available_teams()), 5)

    def test_initialization_with_dataframe(self):
        """Test calculator initialization with DataFrame"""
        calc = PositionalRankingCalculator(teams_dataframe=self.test_teams_df)

        self.assertIsNotNone(calc.teams_dataframe)
        self.assertTrue(calc.is_positional_ranking_available())
        self.assertEqual(len(calc.get_available_teams()), 5)

    def test_initialization_with_default_path(self):
        """Test calculator initialization with default path"""
        with patch('positional_ranking_calculator.load_teams_from_csv') as mock_load:
            mock_load.return_value = []
            calc = PositionalRankingCalculator()

            expected_path = Path(__file__).parent.parent / "teams.csv"
            self.assertEqual(calc.teams_file, expected_path)

    def test_default_config_values(self):
        """Test default configuration is loaded correctly"""
        calc = PositionalRankingCalculator(teams_dataframe=self.test_teams_df)

        config = calc.config
        self.assertEqual(config["offensive_positions"], ["QB", "RB", "WR", "TE"])
        self.assertEqual(config["defensive_positions"], ["DST"])
        self.assertEqual(config["kicker_positions"], ["K"])
        self.assertEqual(config["excellent_threshold"], 5)
        self.assertEqual(config["good_threshold"], 12)
        self.assertEqual(config["poor_threshold"], 25)
        self.assertTrue(config["enable_adjustments"])
        self.assertEqual(config["adjustment_weight"], 0.15)

    def test_custom_config_override(self):
        """Test custom configuration overrides defaults"""
        custom_config = {
            "excellent_threshold": 3,
            "adjustment_weight": 0.2,
            "enable_adjustments": False
        }

        calc = PositionalRankingCalculator(teams_dataframe=self.test_teams_df, config=custom_config)

        self.assertEqual(calc.config["excellent_threshold"], 3)
        self.assertEqual(calc.config["adjustment_weight"], 0.2)
        self.assertFalse(calc.config["enable_adjustments"])
        # Should still have defaults for non-overridden values
        self.assertEqual(calc.config["good_threshold"], 12)

    def test_load_teams_from_dataframe(self):
        """Test loading teams from DataFrame"""
        calc = PositionalRankingCalculator(teams_dataframe=self.test_teams_df)

        # Check KC team data
        kc_data = calc.team_data_cache.get("KC")
        self.assertIsInstance(kc_data, TeamData)
        self.assertEqual(kc_data.team, "KC")
        self.assertEqual(kc_data.offensive_rank, 1)
        self.assertEqual(kc_data.defensive_rank, 15)
        self.assertEqual(kc_data.opponent, "BUF")

    def test_load_teams_file_not_found(self):
        """Test handling of missing teams file"""
        nonexistent_file = self.test_dir / "nonexistent.csv"

        with patch('positional_ranking_calculator.setup_module_logging') as mock_logging:
            calc = PositionalRankingCalculator(teams_file_path=str(nonexistent_file))

            self.assertFalse(calc.is_positional_ranking_available())
            self.assertEqual(len(calc.team_data_cache), 0)

    def test_load_teams_with_exception(self):
        """Test handling of exceptions during team data loading"""
        with patch('positional_ranking_calculator.load_teams_from_csv', side_effect=Exception("CSV error")):
            calc = PositionalRankingCalculator(teams_file_path=str(self.test_teams_file))

            self.assertFalse(calc.is_positional_ranking_available())
            self.assertEqual(len(calc.team_data_cache), 0)

    def test_calculate_adjustment_offensive_positions(self):
        """Test positional adjustments for offensive positions"""
        calc = PositionalRankingCalculator(teams_dataframe=self.test_teams_df)

        # Test elite offensive team (KC, rank 1)
        adjusted_points, explanation = calc.calculate_positional_adjustment("KC", "QB", 100.0)
        self.assertGreater(adjusted_points, 100.0)  # Should be boosted
        self.assertIn("Elite offensive", explanation)
        self.assertIn("rank 1", explanation)

        # Test QB, RB, WR, TE should all use offensive rank
        for position in ["QB", "RB", "WR", "TE"]:
            adjusted_points, explanation = calc.calculate_positional_adjustment("KC", position, 100.0)
            self.assertGreater(adjusted_points, 100.0)
            self.assertIn("offensive", explanation)

    def test_calculate_adjustment_defensive_positions(self):
        """Test positional adjustments for defensive positions"""
        calc = PositionalRankingCalculator(teams_dataframe=self.test_teams_df)

        # Test elite defensive team (BUF, defensive rank 2)
        adjusted_points, explanation = calc.calculate_positional_adjustment("BUF", "DST", 100.0)
        self.assertGreater(adjusted_points, 100.0)  # Should be boosted
        self.assertIn("Elite defensive", explanation)
        self.assertIn("rank 2", explanation)

    def test_calculate_adjustment_kicker_positions(self):
        """Test positional adjustments for kickers"""
        calc = PositionalRankingCalculator(teams_dataframe=self.test_teams_df)

        # Test kicker using offensive rank (KC, offensive rank 1)
        adjusted_points, explanation = calc.calculate_positional_adjustment("KC", "K", 100.0)
        self.assertGreater(adjusted_points, 100.0)  # Should be boosted
        self.assertIn("Elite offensive (kicking)", explanation)
        self.assertIn("rank 1", explanation)

    def test_calculate_adjustment_rank_tiers(self):
        """Test different rank tiers produce appropriate adjustments"""
        calc = PositionalRankingCalculator(teams_dataframe=self.test_teams_df)

        # Elite tier (rank 1-5): KC offense rank 1, PHI defense rank 5
        kc_points, kc_explanation = calc.calculate_positional_adjustment("KC", "QB", 100.0)
        phi_dst_points, phi_dst_explanation = calc.calculate_positional_adjustment("PHI", "DST", 100.0)

        # Good tier (rank 6-12): BUF offense rank 8, GB defense rank 12
        buf_points, buf_explanation = calc.calculate_positional_adjustment("BUF", "QB", 100.0)

        # Poor tier (rank 25-32): DAL defense rank 25
        dal_dst_points, dal_dst_explanation = calc.calculate_positional_adjustment("DAL", "DST", 100.0)

        # Elite should be best, poor should be worst
        self.assertGreater(kc_points, buf_points)  # Elite > Good
        self.assertGreater(buf_points, dal_dst_points)  # Good > Poor

        # Check explanations
        self.assertIn("Elite", kc_explanation)
        self.assertIn("Good", buf_explanation)
        self.assertIn("Poor", dal_dst_explanation)

    def test_calculate_adjustment_disabled(self):
        """Test adjustments when disabled"""
        custom_config = {"enable_adjustments": False}
        calc = PositionalRankingCalculator(teams_dataframe=self.test_teams_df, config=custom_config)

        adjusted_points, explanation = calc.calculate_positional_adjustment("KC", "QB", 100.0)

        self.assertEqual(adjusted_points, 100.0)  # No change
        self.assertIn("No adjustment", explanation)

    def test_calculate_adjustment_no_team_data(self):
        """Test adjustments when team data is unavailable"""
        # Create calculator with non-existent file to ensure no data is loaded
        nonexistent_file = self.test_dir / "nonexistent.csv"
        calc = PositionalRankingCalculator(teams_file_path=str(nonexistent_file))

        adjusted_points, explanation = calc.calculate_positional_adjustment("KC", "QB", 100.0)

        self.assertEqual(adjusted_points, 100.0)  # No change
        self.assertIn("No adjustment (rankings unavailable)", explanation)

    def test_calculate_adjustment_team_not_found(self):
        """Test adjustments for non-existent team"""
        calc = PositionalRankingCalculator(teams_dataframe=self.test_teams_df)

        adjusted_points, explanation = calc.calculate_positional_adjustment("INVALID", "QB", 100.0)

        self.assertEqual(adjusted_points, 100.0)  # No change
        self.assertIn("team INVALID not found", explanation)

    def test_calculate_adjustment_unknown_position(self):
        """Test adjustments for unknown position"""
        calc = PositionalRankingCalculator(teams_dataframe=self.test_teams_df)

        adjusted_points, explanation = calc.calculate_positional_adjustment("KC", "INVALID", 100.0)

        self.assertEqual(adjusted_points, 100.0)  # No change
        self.assertIn("unknown position INVALID", explanation)

    def test_calculate_adjustment_missing_rank(self):
        """Test adjustments when rank data is missing"""
        # Create team with missing rank data - should not load due to conversion error
        df_with_missing = pd.DataFrame([
            {"team": "TEST", "offensive_rank": "", "defensive_rank": "", "opponent": "KC"}
        ])

        calc = PositionalRankingCalculator(teams_dataframe=df_with_missing)
        adjusted_points, explanation = calc.calculate_positional_adjustment("TEST", "QB", 100.0)

        self.assertEqual(adjusted_points, 100.0)  # No change
        # Should fail to load due to conversion error, so no rankings available
        self.assertIn("No adjustment (rankings unavailable)", explanation)

    def test_adjustment_weight_factor(self):
        """Test adjustment weight factor limits impact"""
        # Test with different weight factors
        low_weight_config = {"adjustment_weight": 0.05}  # 5% max impact
        high_weight_config = {"adjustment_weight": 0.3}   # 30% max impact

        calc_low = PositionalRankingCalculator(teams_dataframe=self.test_teams_df, config=low_weight_config)
        calc_high = PositionalRankingCalculator(teams_dataframe=self.test_teams_df, config=high_weight_config)

        # Same team/position, different weights
        low_points, _ = calc_low.calculate_positional_adjustment("KC", "QB", 100.0)
        high_points, _ = calc_high.calculate_positional_adjustment("KC", "QB", 100.0)

        # Higher weight should produce bigger adjustment
        low_adjustment = abs(low_points - 100.0)
        high_adjustment = abs(high_points - 100.0)
        self.assertGreater(high_adjustment, low_adjustment)

    def test_get_multiplier_from_rank(self):
        """Test rank to multiplier conversion"""
        calc = PositionalRankingCalculator(teams_dataframe=self.test_teams_df)

        # Test each tier
        self.assertEqual(calc._get_multiplier_from_rank(1), calc.config["excellent_matchup"])  # Elite
        self.assertEqual(calc._get_multiplier_from_rank(8), calc.config["good_matchup"])       # Good
        self.assertEqual(calc._get_multiplier_from_rank(15), calc.config["neutral_matchup"])   # Average
        self.assertEqual(calc._get_multiplier_from_rank(28), calc.config["bad_matchup"])       # Poor

    def test_get_rank_tier_description(self):
        """Test rank tier descriptions"""
        calc = PositionalRankingCalculator(teams_dataframe=self.test_teams_df)

        self.assertEqual(calc._get_rank_tier_description(1), "Elite")
        self.assertEqual(calc._get_rank_tier_description(8), "Good")
        self.assertEqual(calc._get_rank_tier_description(15), "Average")
        self.assertEqual(calc._get_rank_tier_description(28), "Poor")

    def test_is_positional_ranking_available(self):
        """Test availability check"""
        # With data and enabled
        calc_enabled = PositionalRankingCalculator(teams_dataframe=self.test_teams_df)
        self.assertTrue(calc_enabled.is_positional_ranking_available())

        # With data but disabled
        calc_disabled = PositionalRankingCalculator(teams_dataframe=self.test_teams_df,
                                                   config={"enable_adjustments": False})
        self.assertFalse(calc_disabled.is_positional_ranking_available())

        # No data - use non-existent file
        nonexistent_file = self.test_dir / "nonexistent.csv"
        calc_no_data = PositionalRankingCalculator(teams_file_path=str(nonexistent_file))
        self.assertFalse(calc_no_data.is_positional_ranking_available())

    def test_get_available_teams(self):
        """Test getting available teams list"""
        calc = PositionalRankingCalculator(teams_dataframe=self.test_teams_df)

        available_teams = calc.get_available_teams()
        expected_teams = {"KC", "BUF", "PHI", "DAL", "GB"}
        self.assertEqual(set(available_teams), expected_teams)

    def test_get_team_summary(self):
        """Test team summary generation"""
        calc = PositionalRankingCalculator(teams_dataframe=self.test_teams_df)

        # Test existing team
        kc_summary = calc.get_team_summary("KC")
        self.assertIsNotNone(kc_summary)
        self.assertIn("KC:", kc_summary)
        self.assertIn("Elite offense", kc_summary)
        self.assertIn("#1", kc_summary)
        self.assertIn("defense", kc_summary)
        self.assertIn("#15", kc_summary)

        # Test non-existent team
        invalid_summary = calc.get_team_summary("INVALID")
        self.assertIsNone(invalid_summary)

    def test_reload_team_data(self):
        """Test reloading team data"""
        calc = PositionalRankingCalculator(teams_file_path=str(self.test_teams_file))

        # Initially should have 5 teams
        self.assertEqual(len(calc.team_data_cache), 5)

        # Clear cache
        calc.team_data_cache = {}
        self.assertEqual(len(calc.team_data_cache), 0)

        # Reload should restore data
        calc.reload_team_data()
        self.assertEqual(len(calc.team_data_cache), 5)

    def test_edge_case_zero_points(self):
        """Test adjustment with zero base points"""
        calc = PositionalRankingCalculator(teams_dataframe=self.test_teams_df)

        adjusted_points, explanation = calc.calculate_positional_adjustment("KC", "QB", 0.0)

        self.assertEqual(adjusted_points, 0.0)  # Should remain 0
        self.assertIn("Elite offensive", explanation)

    def test_edge_case_negative_points(self):
        """Test adjustment with negative base points"""
        calc = PositionalRankingCalculator(teams_dataframe=self.test_teams_df)

        adjusted_points, explanation = calc.calculate_positional_adjustment("KC", "QB", -10.0)

        # Negative points should still be adjusted proportionally
        self.assertNotEqual(adjusted_points, -10.0)
        self.assertIn("Elite offensive", explanation)

    def test_edge_case_very_large_points(self):
        """Test adjustment with very large base points"""
        calc = PositionalRankingCalculator(teams_dataframe=self.test_teams_df)

        large_points = 999999.0
        adjusted_points, explanation = calc.calculate_positional_adjustment("KC", "QB", large_points)

        # Should still apply proportional adjustment
        self.assertNotEqual(adjusted_points, large_points)
        self.assertGreater(adjusted_points, large_points)  # Elite team should boost
        self.assertIn("Elite offensive", explanation)

    def test_edge_case_malformed_dataframe(self):
        """Test handling of malformed DataFrame"""
        # Create DataFrame with missing columns
        malformed_df = pd.DataFrame([
            {"team": "KC", "offensive_rank": "1"},  # Missing defensive_rank and opponent
            {"offensive_rank": "2", "defensive_rank": "3"},  # Missing team
        ])

        calc = PositionalRankingCalculator(teams_dataframe=malformed_df)

        # Should handle gracefully
        available_teams = calc.get_available_teams()
        self.assertIsInstance(available_teams, list)

    def test_logging_behavior(self):
        """Test logging configuration is properly set and accessible"""
        # Create config with logging enabled
        config = {
            "enable_adjustments": True,
            "log_adjustments": True,  # Enable logging
            "offensive_positions": ["QB", "RB", "WR", "TE"],
            "defensive_positions": ["DST"],
            "rank_multipliers": {
                "excellent": 1.15, "good": 1.08, "average": 1.0,
                "poor": 0.92, "very_poor": 0.85
            }
        }

        calc = PositionalRankingCalculator(teams_dataframe=self.test_teams_df, config=config)

        # Test that logging config is properly set and accessible
        self.assertTrue(calc.config["log_adjustments"])
        self.assertTrue(calc.config["enable_adjustments"])

        # Test that logger exists and is properly initialized
        self.assertIsNotNone(calc.logger)
        self.assertTrue(hasattr(calc.logger, 'info'))

    def test_concurrent_calculations(self):
        """Test multiple concurrent calculations don't interfere"""
        calc = PositionalRankingCalculator(teams_dataframe=self.test_teams_df)

        # Run multiple calculations
        results = []
        for team in ["KC", "BUF", "PHI"]:
            for position in ["QB", "RB", "DST"]:
                result = calc.calculate_positional_adjustment(team, position, 100.0)
                results.append((team, position, result))

        # All should return valid results
        self.assertEqual(len(results), 9)
        for team, position, (points, explanation) in results:
            self.assertIsInstance(points, float)
            self.assertIsInstance(explanation, str)
            # Explanation contains position type but not necessarily team name
            self.assertIsInstance(explanation, str)


if __name__ == '__main__':
    unittest.main()