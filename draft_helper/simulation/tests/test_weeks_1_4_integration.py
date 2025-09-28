"""
Unit tests for weeks 1-4 team data integration
"""

import unittest
import sys
import os
import pandas as pd

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from data_manager import SimulationDataManager

class TestWeeks1to4Integration(unittest.TestCase):
    """Test that weeks 1-4 team data is properly integrated"""

    def setUp(self):
        """Set up test data manager"""
        self.data_manager = SimulationDataManager()

    def test_weeks_1_4_files_exist(self):
        """Test that all weeks 1-4 files exist and are readable"""
        for week in range(1, 5):
            with self.subTest(week=week):
                teams_data = self.data_manager.get_teams_weekly_data(week)
                self.assertIsInstance(teams_data, pd.DataFrame)
                self.assertGreater(len(teams_data), 0)
                self.assertIn('team', teams_data.columns)
                self.assertIn('offensive_rank', teams_data.columns)
                self.assertIn('defensive_rank', teams_data.columns)

    def test_regression_applied_vs_week_0(self):
        """Test that regression is applied to weeks 1-4 vs week 0 baseline"""
        week_0_data = self.data_manager.get_teams_weekly_data(0)

        for week in range(1, 5):
            with self.subTest(week=week):
                week_data = self.data_manager.get_teams_weekly_data(week)

                # At least some teams should have different rankings
                changes_found = 0
                for _, row in week_data.head(10).iterrows():  # Check first 10 teams
                    team = row['team']
                    week_0_row = week_0_data[week_0_data['team'] == team]

                    if not week_0_row.empty:
                        week_0_off = week_0_row.iloc[0]['offensive_rank']
                        week_0_def = week_0_row.iloc[0]['defensive_rank']
                        week_off = row['offensive_rank']
                        week_def = row['defensive_rank']

                        if week_0_off != week_off or week_0_def != week_def:
                            changes_found += 1

                # At least some teams should have changed rankings (regression applied)
                self.assertGreater(changes_found, 0,
                    f"Week {week} should have some teams with different rankings vs week 0")

    def test_progressive_regression_by_week(self):
        """Test that regression becomes stronger by week (more changes from baseline)"""
        week_0_data = self.data_manager.get_teams_weekly_data(0)
        week_changes = {}

        for week in range(1, 5):
            week_data = self.data_manager.get_teams_weekly_data(week)
            changes = 0

            for _, row in week_data.iterrows():
                team = row['team']
                week_0_row = week_0_data[week_0_data['team'] == team]

                if not week_0_row.empty:
                    week_0_off = week_0_row.iloc[0]['offensive_rank']
                    week_0_def = week_0_row.iloc[0]['defensive_rank']
                    week_off = row['offensive_rank']
                    week_def = row['defensive_rank']

                    if week_0_off != week_off or week_0_def != week_def:
                        changes += 1

            week_changes[week] = changes

        # Later weeks should generally have more changes (stronger regression)
        # Week 4 should have at least as many changes as week 1
        self.assertGreaterEqual(week_changes[4], week_changes[1],
            "Week 4 should have at least as many ranking changes as week 1 (progressive regression)")

    def test_all_weeks_have_same_teams(self):
        """Test that all weeks have the same set of teams"""
        week_0_teams = set(self.data_manager.get_teams_weekly_data(0)['team'])

        for week in range(1, 5):
            with self.subTest(week=week):
                week_teams = set(self.data_manager.get_teams_weekly_data(week)['team'])
                self.assertEqual(week_0_teams, week_teams,
                    f"Week {week} should have the same teams as week 0")

    def test_ranking_values_in_valid_range(self):
        """Test that all ranking values are in valid range (1-32)"""
        for week in range(0, 5):
            with self.subTest(week=week):
                week_data = self.data_manager.get_teams_weekly_data(week)

                # Test offensive rankings
                self.assertTrue(all(1 <= rank <= 32 for rank in week_data['offensive_rank']),
                    f"Week {week} offensive rankings should be between 1-32")

                # Test defensive rankings
                self.assertTrue(all(1 <= rank <= 32 for rank in week_data['defensive_rank']),
                    f"Week {week} defensive rankings should be between 1-32")

    def test_data_manager_week_range_validation(self):
        """Test that data manager properly validates week ranges"""
        # Valid weeks should work
        for week in range(0, 19):
            try:
                data = self.data_manager.get_teams_weekly_data(week)
                self.assertIsInstance(data, pd.DataFrame)
            except FileNotFoundError:
                # Some weeks might not have files, that's okay for this test
                pass

        # Invalid weeks should raise ValueError
        with self.assertRaises(ValueError):
            self.data_manager.get_teams_weekly_data(-1)

        with self.assertRaises(ValueError):
            self.data_manager.get_teams_weekly_data(19)

if __name__ == '__main__':
    unittest.main()