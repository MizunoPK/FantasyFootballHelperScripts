"""
Unit tests for data manager.
"""

import unittest
import tempfile
import os
import pandas as pd
import sys

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from draft_helper.simulation.data_manager import SimulationDataManager


class TestSimulationDataManager(unittest.TestCase):
    """Test cases for SimulationDataManager"""

    def setUp(self):
        """Set up test environment"""
        # Create temporary directories for testing
        self.temp_dir = tempfile.mkdtemp()
        self.test_source_players_file = os.path.join(self.temp_dir, 'source_players.csv')
        self.test_source_teams_file = os.path.join(self.temp_dir, 'source_teams.csv')
        self.test_projected_file = os.path.join(self.temp_dir, 'players_projected.csv')
        self.test_actual_file = os.path.join(self.temp_dir, 'players_actual.csv')

        # Create sample source data
        sample_players_data = pd.DataFrame({
            'name': ['Player 1', 'Player 2', 'Player 3'],
            'position': ['QB', 'RB', 'WR'],
            'team': ['Team1', 'Team2', 'Team3'],
            'drafted': [0, 1, 0],
            'week_1_points': [25.0, 15.0, 12.0]
        })
        sample_players_data.to_csv(self.test_source_players_file, index=False)

        # Create sample teams data
        sample_teams_data = pd.DataFrame({
            'team': ['Team1', 'Team2', 'Team3'],
            'qb_allowed': [20.0, 25.0, 15.0],
            'rb_allowed': [15.0, 20.0, 10.0],
            'wr_allowed': [18.0, 22.0, 12.0]
        })
        sample_teams_data.to_csv(self.test_source_teams_file, index=False)

        # Create data manager with test paths
        self.data_manager = SimulationDataManager()
        self.data_manager.source_players_csv = self.test_source_players_file
        self.data_manager.source_teams_csv = self.test_source_teams_file
        self.data_manager.players_projected_csv = self.test_projected_file
        self.data_manager.players_actual_csv = self.test_actual_file
        self.data_manager.data_dir = self.temp_dir

        # Update weekly teams CSV paths to use temp directory
        self.data_manager.teams_weekly_csvs = {
            week: os.path.join(self.temp_dir, f'teams_week_{week}.csv')
            for week in range(0, 19)  # Week 0 through Week 18
        }

    def tearDown(self):
        """Clean up test environment"""
        # Remove temporary files
        for file_path in [self.test_source_players_file, self.test_source_teams_file,
                         self.test_projected_file, self.test_actual_file]:
            if os.path.exists(file_path):
                os.remove(file_path)

        # Remove weekly teams files
        for week in range(0, 19):
            weekly_file = os.path.join(self.temp_dir, f'teams_week_{week}.csv')
            if os.path.exists(weekly_file):
                os.remove(weekly_file)

        # Remove temp directory if empty
        try:
            os.rmdir(self.temp_dir)
        except OSError:
            pass

    def test_setup_simulation_data(self):
        """Test setting up simulation data"""
        self.data_manager.setup_simulation_data()

        # Check that projected and actual files were created
        self.assertTrue(os.path.exists(self.test_projected_file))
        self.assertTrue(os.path.exists(self.test_actual_file))

        # Check that weekly teams files were created
        for week in range(0, 19):
            weekly_file = os.path.join(self.temp_dir, f'teams_week_{week}.csv')
            self.assertTrue(os.path.exists(weekly_file))

        # Check that data is identical to source
        source_df = pd.read_csv(self.test_source_players_file)
        projected_df = pd.read_csv(self.test_projected_file)
        actual_df = pd.read_csv(self.test_actual_file)

        pd.testing.assert_frame_equal(source_df, projected_df)
        pd.testing.assert_frame_equal(source_df, actual_df)

    def test_setup_simulation_data_missing_source(self):
        """Test setup with missing source file"""
        # Remove source players file
        os.remove(self.test_source_players_file)

        with self.assertRaises(FileNotFoundError):
            self.data_manager.setup_simulation_data()

    def test_get_players_projected_data(self):
        """Test getting projected players data"""
        # Setup data first
        self.data_manager.setup_simulation_data()

        # Get data
        players_df = self.data_manager.get_players_projected_data()

        self.assertIsInstance(players_df, pd.DataFrame)
        self.assertEqual(len(players_df), 3)
        self.assertIn('name', players_df.columns)
        self.assertIn('position', players_df.columns)

    def test_get_players_actual_data(self):
        """Test getting actual players data"""
        # Setup data first
        self.data_manager.setup_simulation_data()

        # Get data
        players_df = self.data_manager.get_players_actual_data()

        self.assertIsInstance(players_df, pd.DataFrame)
        self.assertEqual(len(players_df), 3)
        self.assertIn('name', players_df.columns)
        self.assertIn('position', players_df.columns)

    def test_get_teams_weekly_data(self):
        """Test getting weekly teams data"""
        # Setup data first
        self.data_manager.setup_simulation_data()

        # Test week 0 (draft phase)
        week_0_df = self.data_manager.get_teams_weekly_data(0)
        self.assertIsInstance(week_0_df, pd.DataFrame)
        self.assertEqual(len(week_0_df), 3)
        self.assertIn('team', week_0_df.columns)

        # Test week 1 (season phase)
        week_1_df = self.data_manager.get_teams_weekly_data(1)
        self.assertIsInstance(week_1_df, pd.DataFrame)
        self.assertEqual(len(week_1_df), 3)

        # Test invalid week
        with self.assertRaises(ValueError):
            self.data_manager.get_teams_weekly_data(19)

    def test_get_players_data_auto_setup(self):
        """Test that get_players_data automatically sets up if needed"""
        # Don't setup manually
        players_df = self.data_manager.get_players_data()

        # Should still work and create the files
        self.assertTrue(os.path.exists(self.test_projected_file))
        self.assertIsInstance(players_df, pd.DataFrame)

    def test_reset_players_data(self):
        """Test resetting players data"""
        # Setup data first
        self.data_manager.setup_simulation_data()

        # Modify drafted status in both files
        projected_df = pd.read_csv(self.test_projected_file)
        projected_df.loc[0, 'drafted'] = 2
        projected_df.to_csv(self.test_projected_file, index=False)

        actual_df = pd.read_csv(self.test_actual_file)
        actual_df.loc[0, 'drafted'] = 2
        actual_df.to_csv(self.test_actual_file, index=False)

        # Reset data
        self.data_manager.reset_players_data()

        # Check that drafted status is reset in both files
        reset_projected_df = pd.read_csv(self.test_projected_file)
        reset_actual_df = pd.read_csv(self.test_actual_file)
        self.assertTrue(all(reset_projected_df['drafted'] == 0))
        self.assertTrue(all(reset_actual_df['drafted'] == 0))

    def test_cleanup_simulation_data(self):
        """Test cleaning up simulation data"""
        # Setup data first
        self.data_manager.setup_simulation_data()
        self.assertTrue(os.path.exists(self.test_projected_file))
        self.assertTrue(os.path.exists(self.test_actual_file))

        # Cleanup
        self.data_manager.cleanup_simulation_data()

        # Check that files are removed
        self.assertFalse(os.path.exists(self.test_projected_file))
        self.assertFalse(os.path.exists(self.test_actual_file))

        # Check that weekly teams files are removed
        for week in range(0, 19):
            weekly_file = os.path.join(self.temp_dir, f'teams_week_{week}.csv')
            self.assertFalse(os.path.exists(weekly_file))

    def test_verify_data_integrity_valid(self):
        """Test data integrity verification with valid data"""
        # Setup data
        self.data_manager.setup_simulation_data()

        # Verify integrity
        is_valid = self.data_manager.verify_data_integrity()
        self.assertTrue(is_valid)

    def test_verify_data_integrity_missing_source(self):
        """Test data integrity with missing source file"""
        # Remove source players file
        os.remove(self.test_source_players_file)

        is_valid = self.data_manager.verify_data_integrity()
        self.assertFalse(is_valid)

    def test_verify_data_integrity_missing_copy(self):
        """Test data integrity with missing simulation copy"""
        # Source exists but projected/actual copies don't
        is_valid = self.data_manager.verify_data_integrity()
        self.assertFalse(is_valid)

    def test_verify_data_integrity_column_mismatch(self):
        """Test data integrity with column mismatch"""
        # Setup data
        self.data_manager.setup_simulation_data()

        # Modify projected file to have different columns
        sim_df = pd.read_csv(self.test_projected_file)
        sim_df = sim_df.drop('position', axis=1)
        sim_df.to_csv(self.test_projected_file, index=False)

        is_valid = self.data_manager.verify_data_integrity()
        self.assertFalse(is_valid)

    def test_verify_data_integrity_row_mismatch(self):
        """Test data integrity with row count mismatch"""
        # Setup data
        self.data_manager.setup_simulation_data()

        # Remove a row from actual file
        sim_df = pd.read_csv(self.test_actual_file)
        sim_df = sim_df.iloc[:-1]  # Remove last row
        sim_df.to_csv(self.test_actual_file, index=False)

        is_valid = self.data_manager.verify_data_integrity()
        self.assertFalse(is_valid)


if __name__ == '__main__':
    unittest.main()