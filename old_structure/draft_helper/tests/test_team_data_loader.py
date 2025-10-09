#!/usr/bin/env python3
"""
Unit tests for Team Data Loader module

Tests team data loading, caching, and retrieval functionality.

Author: Kai Mizuno
Last Updated: September 2025
"""

import unittest
import tempfile
import csv
from pathlib import Path
from unittest.mock import patch, MagicMock

import sys
sys.path.append(str(Path(__file__).parent.parent))

from league_helper.util.TeamDataManager import TeamDataLoader

sys.path.append(str(Path(__file__).parent.parent.parent))
from shared_files.TeamData import TeamData


class TestTeamDataLoader(unittest.TestCase):
    """Test cases for TeamDataLoader functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.test_teams_file = self.test_dir / "teams.csv"

        # Create test team data
        self.test_team_data = [
            {"team": "KC", "offensive_rank": "1", "defensive_rank": "15", "opponent": "BUF"},
            {"team": "BUF", "offensive_rank": "3", "defensive_rank": "2", "opponent": "KC"},
            {"team": "PHI", "offensive_rank": "5", "defensive_rank": "8", "opponent": "DAL"},
            {"team": "DAL", "offensive_rank": "12", "defensive_rank": "25", "opponent": "PHI"}
        ]

        # Write test teams.csv
        with open(self.test_teams_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["team", "offensive_rank", "defensive_rank", "opponent"])
            writer.writeheader()
            writer.writerows(self.test_team_data)

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.test_dir)

    def test_initialization_with_custom_file_path(self):
        """Test TeamDataLoader initialization with custom file path"""
        loader = TeamDataLoader(str(self.test_teams_file))

        self.assertEqual(loader.teams_file, self.test_teams_file)
        self.assertTrue(loader.is_team_data_available())
        self.assertEqual(len(loader.get_available_teams()), 4)

    def test_initialization_with_default_path(self):
        """Test TeamDataLoader initialization with default path"""
        with patch('team_data_loader.load_teams_from_csv') as mock_load:
            mock_load.return_value = []
            loader = TeamDataLoader()

            # Should use default shared_files/teams.csv path
            expected_path = Path(__file__).parent.parent.parent / "shared_files" / "teams.csv"
            self.assertEqual(loader.teams_file, expected_path)

    def test_load_team_data_success(self):
        """Test successful team data loading"""
        loader = TeamDataLoader(str(self.test_teams_file))

        # Check that teams were loaded correctly
        self.assertEqual(len(loader.team_data_cache), 4)
        self.assertIn("KC", loader.team_data_cache)
        self.assertIn("BUF", loader.team_data_cache)
        self.assertIn("PHI", loader.team_data_cache)
        self.assertIn("DAL", loader.team_data_cache)

    def test_load_team_data_file_not_found(self):
        """Test handling of missing teams.csv file"""
        nonexistent_file = self.test_dir / "nonexistent.csv"

        with patch('team_data_loader.logging.getLogger') as mock_logger:
            loader = TeamDataLoader(str(nonexistent_file))

            self.assertFalse(loader.is_team_data_available())
            self.assertEqual(len(loader.team_data_cache), 0)
            # Should log warning about missing file
            mock_logger.return_value.warning.assert_called()

    def test_load_team_data_with_exception(self):
        """Test handling of exceptions during data loading"""
        with patch('team_data_loader.load_teams_from_csv', side_effect=Exception("CSV error")):
            with patch('team_data_loader.logging.getLogger') as mock_logger:
                loader = TeamDataLoader(str(self.test_teams_file))

                self.assertFalse(loader.is_team_data_available())
                self.assertEqual(len(loader.team_data_cache), 0)
                # Should log warning about error
                mock_logger.return_value.warning.assert_called()

    def test_get_team_offensive_rank_success(self):
        """Test successful retrieval of team offensive rank"""
        loader = TeamDataLoader(str(self.test_teams_file))

        self.assertEqual(loader.get_team_offensive_rank("KC"), 1)
        self.assertEqual(loader.get_team_offensive_rank("BUF"), 3)
        self.assertEqual(loader.get_team_offensive_rank("PHI"), 5)
        self.assertEqual(loader.get_team_offensive_rank("DAL"), 12)

    def test_get_team_offensive_rank_not_found(self):
        """Test retrieval of offensive rank for non-existent team"""
        loader = TeamDataLoader(str(self.test_teams_file))

        self.assertIsNone(loader.get_team_offensive_rank("NONEXISTENT"))

    def test_get_team_defensive_rank_success(self):
        """Test successful retrieval of team defensive rank"""
        loader = TeamDataLoader(str(self.test_teams_file))

        self.assertEqual(loader.get_team_defensive_rank("KC"), 15)
        self.assertEqual(loader.get_team_defensive_rank("BUF"), 2)
        self.assertEqual(loader.get_team_defensive_rank("PHI"), 8)
        self.assertEqual(loader.get_team_defensive_rank("DAL"), 25)

    def test_get_team_defensive_rank_not_found(self):
        """Test retrieval of defensive rank for non-existent team"""
        loader = TeamDataLoader(str(self.test_teams_file))

        self.assertIsNone(loader.get_team_defensive_rank("NONEXISTENT"))

    def test_get_team_opponent_success(self):
        """Test successful retrieval of team opponent"""
        loader = TeamDataLoader(str(self.test_teams_file))

        self.assertEqual(loader.get_team_opponent("KC"), "BUF")
        self.assertEqual(loader.get_team_opponent("BUF"), "KC")
        self.assertEqual(loader.get_team_opponent("PHI"), "DAL")
        self.assertEqual(loader.get_team_opponent("DAL"), "PHI")

    def test_get_team_opponent_not_found(self):
        """Test retrieval of opponent for non-existent team"""
        loader = TeamDataLoader(str(self.test_teams_file))

        self.assertIsNone(loader.get_team_opponent("NONEXISTENT"))

    def test_get_team_data_success(self):
        """Test successful retrieval of complete team data"""
        loader = TeamDataLoader(str(self.test_teams_file))

        kc_data = loader.get_team_data("KC")
        self.assertIsInstance(kc_data, TeamData)
        self.assertEqual(kc_data.team, "KC")
        self.assertEqual(kc_data.offensive_rank, 1)
        self.assertEqual(kc_data.defensive_rank, 15)
        self.assertEqual(kc_data.opponent, "BUF")

    def test_get_team_data_not_found(self):
        """Test retrieval of team data for non-existent team"""
        loader = TeamDataLoader(str(self.test_teams_file))

        self.assertIsNone(loader.get_team_data("NONEXISTENT"))

    def test_is_team_data_available_true(self):
        """Test is_team_data_available when data is loaded"""
        loader = TeamDataLoader(str(self.test_teams_file))

        self.assertTrue(loader.is_team_data_available())

    def test_is_team_data_available_false(self):
        """Test is_team_data_available when no data is loaded"""
        nonexistent_file = self.test_dir / "nonexistent.csv"
        loader = TeamDataLoader(str(nonexistent_file))

        self.assertFalse(loader.is_team_data_available())

    def test_get_available_teams(self):
        """Test retrieval of all available teams"""
        loader = TeamDataLoader(str(self.test_teams_file))

        available_teams = loader.get_available_teams()
        self.assertEqual(set(available_teams), {"KC", "BUF", "PHI", "DAL"})
        self.assertEqual(len(available_teams), 4)

    def test_get_available_teams_empty(self):
        """Test get_available_teams when no data is loaded"""
        nonexistent_file = self.test_dir / "nonexistent.csv"
        loader = TeamDataLoader(str(nonexistent_file))

        available_teams = loader.get_available_teams()
        self.assertEqual(available_teams, [])

    def test_reload_team_data(self):
        """Test reloading team data functionality"""
        loader = TeamDataLoader(str(self.test_teams_file))

        # Initially should have 4 teams
        self.assertEqual(len(loader.team_data_cache), 4)

        # Clear cache manually to simulate data being lost
        loader.team_data_cache = {}
        self.assertEqual(len(loader.team_data_cache), 0)

        # Reload should restore the data
        loader.reload_team_data()
        self.assertEqual(len(loader.team_data_cache), 4)
        self.assertTrue(loader.is_team_data_available())

    def test_reload_team_data_with_updated_file(self):
        """Test reloading after file is updated"""
        loader = TeamDataLoader(str(self.test_teams_file))

        # Initially should have 4 teams
        self.assertEqual(len(loader.team_data_cache), 4)

        # Update the file with additional team
        updated_data = self.test_team_data + [
            {"team": "GB", "offensive_rank": "8", "defensive_rank": "12", "opponent": "MIN"}
        ]

        with open(self.test_teams_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["team", "offensive_rank", "defensive_rank", "opponent"])
            writer.writeheader()
            writer.writerows(updated_data)

        # Reload should pick up the new team
        loader.reload_team_data()
        self.assertEqual(len(loader.team_data_cache), 5)
        self.assertIn("GB", loader.team_data_cache)
        self.assertEqual(loader.get_team_offensive_rank("GB"), 8)

    def test_edge_case_empty_teams_file(self):
        """Test handling of empty teams.csv file"""
        empty_file = self.test_dir / "empty.csv"

        # Create empty CSV with just headers
        with open(empty_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["team", "offensive_rank", "defensive_rank", "opponent"])
            writer.writeheader()

        loader = TeamDataLoader(str(empty_file))

        self.assertFalse(loader.is_team_data_available())
        self.assertEqual(len(loader.get_available_teams()), 0)
        self.assertIsNone(loader.get_team_offensive_rank("KC"))

    def test_edge_case_malformed_csv_data(self):
        """Test handling of malformed CSV data"""
        malformed_file = self.test_dir / "malformed.csv"

        # Create CSV with missing/invalid data
        malformed_data = [
            {"team": "KC", "offensive_rank": "", "defensive_rank": "15", "opponent": "BUF"},
            {"team": "", "offensive_rank": "3", "defensive_rank": "invalid", "opponent": "KC"},
            {"team": "PHI", "offensive_rank": "5", "defensive_rank": "8", "opponent": ""}
        ]

        with open(malformed_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["team", "offensive_rank", "defensive_rank", "opponent"])
            writer.writeheader()
            writer.writerows(malformed_data)

        # Should handle malformed data gracefully
        loader = TeamDataLoader(str(malformed_file))

        # Should still be able to load teams, even with some malformed data
        # (The actual behavior depends on TeamData validation)
        available_teams = loader.get_available_teams()
        self.assertIsInstance(available_teams, list)

    def test_logging_behavior(self):
        """Test that appropriate logging occurs"""
        with patch('team_data_loader.logging.getLogger') as mock_logger:
            mock_logger_instance = MagicMock()
            mock_logger.return_value = mock_logger_instance

            # Test successful loading
            loader = TeamDataLoader(str(self.test_teams_file))
            mock_logger_instance.info.assert_called()

            # Reset mock
            mock_logger_instance.reset_mock()

            # Test file not found
            nonexistent_file = self.test_dir / "nonexistent.csv"
            loader = TeamDataLoader(str(nonexistent_file))
            mock_logger_instance.warning.assert_called()


if __name__ == '__main__':
    unittest.main()