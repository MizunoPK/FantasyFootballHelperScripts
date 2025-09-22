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
        self.test_source_file = os.path.join(self.temp_dir, 'source_players.csv')
        self.test_sim_file = os.path.join(self.temp_dir, 'sim_players.csv')

        # Create sample source data
        sample_data = pd.DataFrame({
            'name': ['Player 1', 'Player 2', 'Player 3'],
            'position': ['QB', 'RB', 'WR'],
            'team': ['Team1', 'Team2', 'Team3'],
            'drafted': [0, 1, 0],
            'week_1_points': [25.0, 15.0, 12.0]
        })
        sample_data.to_csv(self.test_source_file, index=False)

        # Create data manager with test paths
        self.data_manager = SimulationDataManager()
        self.data_manager.source_players_csv = self.test_source_file
        self.data_manager.players_csv_copy = self.test_sim_file
        self.data_manager.data_dir = self.temp_dir

    def tearDown(self):
        """Clean up test environment"""
        # Remove temporary files
        for file_path in [self.test_source_file, self.test_sim_file]:
            if os.path.exists(file_path):
                os.remove(file_path)

        # Remove temp directory if empty
        try:
            os.rmdir(self.temp_dir)
        except OSError:
            pass

    def test_setup_simulation_data(self):
        """Test setting up simulation data"""
        self.data_manager.setup_simulation_data()

        # Check that copy was created
        self.assertTrue(os.path.exists(self.test_sim_file))

        # Check that data is identical
        source_df = pd.read_csv(self.test_source_file)
        sim_df = pd.read_csv(self.test_sim_file)

        pd.testing.assert_frame_equal(source_df, sim_df)

    def test_setup_simulation_data_missing_source(self):
        """Test setup with missing source file"""
        # Remove source file
        os.remove(self.test_source_file)

        with self.assertRaises(FileNotFoundError):
            self.data_manager.setup_simulation_data()

    def test_get_players_data(self):
        """Test getting players data"""
        # Setup data first
        self.data_manager.setup_simulation_data()

        # Get data
        players_df = self.data_manager.get_players_data()

        self.assertIsInstance(players_df, pd.DataFrame)
        self.assertEqual(len(players_df), 3)
        self.assertIn('name', players_df.columns)
        self.assertIn('position', players_df.columns)

    def test_get_players_data_auto_setup(self):
        """Test that get_players_data automatically sets up if needed"""
        # Don't setup manually
        players_df = self.data_manager.get_players_data()

        # Should still work and create the copy
        self.assertTrue(os.path.exists(self.test_sim_file))
        self.assertIsInstance(players_df, pd.DataFrame)

    def test_reset_players_data(self):
        """Test resetting players data"""
        # Setup data first
        self.data_manager.setup_simulation_data()

        # Modify drafted status
        sim_df = pd.read_csv(self.test_sim_file)
        sim_df.loc[0, 'drafted'] = 2
        sim_df.to_csv(self.test_sim_file, index=False)

        # Reset data
        self.data_manager.reset_players_data()

        # Check that drafted status is reset
        reset_df = pd.read_csv(self.test_sim_file)
        self.assertTrue(all(reset_df['drafted'] == 0))

    def test_cleanup_simulation_data(self):
        """Test cleaning up simulation data"""
        # Setup data first
        self.data_manager.setup_simulation_data()
        self.assertTrue(os.path.exists(self.test_sim_file))

        # Cleanup
        self.data_manager.cleanup_simulation_data()

        # Check that file is removed
        self.assertFalse(os.path.exists(self.test_sim_file))

    def test_verify_data_integrity_valid(self):
        """Test data integrity verification with valid data"""
        # Setup data
        self.data_manager.setup_simulation_data()

        # Verify integrity
        is_valid = self.data_manager.verify_data_integrity()
        self.assertTrue(is_valid)

    def test_verify_data_integrity_missing_source(self):
        """Test data integrity with missing source file"""
        # Remove source file
        os.remove(self.test_source_file)

        is_valid = self.data_manager.verify_data_integrity()
        self.assertFalse(is_valid)

    def test_verify_data_integrity_missing_copy(self):
        """Test data integrity with missing simulation copy"""
        # Source exists but copy doesn't
        is_valid = self.data_manager.verify_data_integrity()
        self.assertFalse(is_valid)

    def test_verify_data_integrity_column_mismatch(self):
        """Test data integrity with column mismatch"""
        # Setup data
        self.data_manager.setup_simulation_data()

        # Modify copy to have different columns
        sim_df = pd.read_csv(self.test_sim_file)
        sim_df = sim_df.drop('position', axis=1)
        sim_df.to_csv(self.test_sim_file, index=False)

        is_valid = self.data_manager.verify_data_integrity()
        self.assertFalse(is_valid)

    def test_verify_data_integrity_row_mismatch(self):
        """Test data integrity with row count mismatch"""
        # Setup data
        self.data_manager.setup_simulation_data()

        # Remove a row from copy
        sim_df = pd.read_csv(self.test_sim_file)
        sim_df = sim_df.iloc[:-1]  # Remove last row
        sim_df.to_csv(self.test_sim_file, index=False)

        is_valid = self.data_manager.verify_data_integrity()
        self.assertFalse(is_valid)


if __name__ == '__main__':
    unittest.main()