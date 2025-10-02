#!/usr/bin/env python3
"""
Unit tests for the DraftedDataLoader module.

Tests functionality for loading drafted player data from CSV files and fuzzy matching.

Author: Generated for NFL Fantasy Data Collection
Created: September 2025
"""

import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

import sys
# Ensure the parent directory is in the path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from drafted_data_loader import DraftedDataLoader


class TestDraftedDataLoader(unittest.TestCase):
    """Test cases for DraftedDataLoader functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.loader = DraftedDataLoader()

    def create_test_csv(self, data: list) -> str:
        """Create a temporary CSV file with test data"""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        writer = csv.writer(temp_file)
        for row in data:
            writer.writerow(row)
        temp_file.close()
        return temp_file.name

    @patch('drafted_data_loader.LOAD_DRAFTED_DATA_FROM_FILE', True)
    @patch('drafted_data_loader.MY_TEAM_NAME', 'Sea Sharp')
    def test_load_drafted_data_success(self):
        """Test successful loading of drafted data"""
        test_data = [
            ['Patrick Mahomes QB - KC', 'Sea Sharp'],
            ['Christian McCaffrey RB - SF', 'Other Team'],
            ['Travis Kelce TE - KC', 'Sea Sharp'],
            ['', 'Empty Player'],  # Should be skipped
            ['Incomplete Data'],    # Should be skipped
        ]

        csv_file = self.create_test_csv(test_data)

        try:
            with patch('drafted_data_loader.DRAFTED_DATA', csv_file):
                success = self.loader.load_drafted_data()

                self.assertTrue(success)
                self.assertEqual(len(self.loader.drafted_players), 3)  # Only valid entries

                stats = self.loader.get_stats()
                self.assertEqual(stats['total_players'], 3)
                self.assertEqual(stats['user_team_players'], 2)  # Mahomes and Kelce
                self.assertEqual(stats['other_team_players'], 1)  # McCaffrey
        finally:
            Path(csv_file).unlink()

    @patch('drafted_data_loader.LOAD_DRAFTED_DATA_FROM_FILE', False)
    def test_load_drafted_data_disabled(self):
        """Test that loading is skipped when toggle is disabled"""
        success = self.loader.load_drafted_data()
        self.assertFalse(success)
        self.assertEqual(len(self.loader.drafted_players), 0)

    @patch('drafted_data_loader.LOAD_DRAFTED_DATA_FROM_FILE', True)
    def test_load_drafted_data_missing_file(self):
        """Test handling of missing CSV file"""
        with patch('drafted_data_loader.DRAFTED_DATA', 'nonexistent_file.csv'):
            success = self.loader.load_drafted_data()
            self.assertFalse(success)
            self.assertEqual(len(self.loader.drafted_players), 0)

    def test_normalize_player_info(self):
        """Test player info normalization"""
        test_cases = [
            ('Amon-Ra St. Brown WR - DET', 'amon ra st brown wr det'),
            ('Patrick Mahomes Jr. QB - KC', 'patrick mahomes qb kc'),
            ('D.K. Metcalf WR - SEA', 'dk metcalf wr sea'),
            ('  Extra   Spaces  QB - NYG  ', 'extra spaces qb nyg'),
            ('Tucker Kraft TE - GB Q View News', 'tucker kraft te gb'),  # Test noise removal
        ]

        for input_str, expected in test_cases:
            with self.subTest(input=input_str):
                result = self.loader._normalize_player_info(input_str)
                self.assertEqual(result, expected)

    def test_extract_player_components(self):
        """Test extraction of name, position, and team from player info"""
        test_cases = [
            ('Amon-Ra St. Brown WR - DET', ('Amon-Ra St. Brown', 'WR', 'DET')),
            ('Patrick Mahomes QB - KC', ('Patrick Mahomes', 'QB', 'KC')),
            ('Tucker Kraft TE - GB Q View News', ('Tucker Kraft', 'TE', 'GB')),
            ('Invalid Format', ('', '', '')),
        ]

        for input_str, expected in test_cases:
            with self.subTest(input=input_str):
                result = self.loader._extract_player_components(input_str)
                self.assertEqual(result, expected)

    def test_similarity_score(self):
        """Test similarity scoring function"""
        test_cases = [
            ('Patrick Mahomes', 'Patrick Mahomes', 1.0),
            ('Patrick Mahomes', 'patrick mahomes', 1.0),
            ('Patrick Mahomes', 'Pat Mahomes', 0.85),  # Approximate
            ('Patrick Mahomes', 'Completely Different', 0.0),  # Approximate
        ]

        for str1, str2, min_expected in test_cases:
            with self.subTest(str1=str1, str2=str2):
                result = self.loader._similarity_score(str1, str2)
                if min_expected == 1.0:
                    self.assertEqual(result, 1.0)
                elif min_expected == 0.0:
                    self.assertLess(result, 0.3)  # Should be very low
                else:
                    self.assertGreater(result, 0.7)  # Should be reasonably high

    @patch('drafted_data_loader.LOAD_DRAFTED_DATA_FROM_FILE', True)
    @patch('drafted_data_loader.MY_TEAM_NAME', 'Sea Sharp')
    def test_find_drafted_state_exact_match(self):
        """Test finding drafted state with exact matches"""
        test_data = [
            ['Patrick Mahomes QB - KC', 'Sea Sharp'],
            ['Christian McCaffrey RB - SF', 'Other Team'],
        ]

        csv_file = self.create_test_csv(test_data)

        try:
            with patch('drafted_data_loader.DRAFTED_DATA', csv_file):
                self.loader.load_drafted_data()

                # Test user team player
                result = self.loader.find_drafted_state('Patrick Mahomes', 'QB', 'KC')
                self.assertEqual(result, 2)

                # Test other team player
                result = self.loader.find_drafted_state('Christian McCaffrey', 'RB', 'SF')
                self.assertEqual(result, 1)

                # Test non-drafted player
                result = self.loader.find_drafted_state('Unknown Player', 'WR', 'NYG')
                self.assertEqual(result, 0)
        finally:
            Path(csv_file).unlink()

    @patch('drafted_data_loader.LOAD_DRAFTED_DATA_FROM_FILE', True)
    @patch('drafted_data_loader.MY_TEAM_NAME', 'Sea Sharp')
    def test_find_drafted_state_fuzzy_match(self):
        """Test finding drafted state with fuzzy matching"""
        test_data = [
            ['Amon-Ra St. Brown WR - DET', 'Sea Sharp'],
        ]

        csv_file = self.create_test_csv(test_data)

        try:
            with patch('drafted_data_loader.DRAFTED_DATA', csv_file):
                self.loader.load_drafted_data()

                # Test slight name variations
                result = self.loader.find_drafted_state('Amon Ra St Brown', 'WR', 'DET')
                self.assertEqual(result, 2)

                # Test with wrong position (should not match)
                result = self.loader.find_drafted_state('Amon-Ra St. Brown', 'RB', 'DET')
                self.assertEqual(result, 0)

                # Test with wrong team (should not match)
                result = self.loader.find_drafted_state('Amon-Ra St. Brown', 'WR', 'GB')
                self.assertEqual(result, 0)
        finally:
            Path(csv_file).unlink()

    @patch('drafted_data_loader.LOAD_DRAFTED_DATA_FROM_FILE', False)
    def test_find_drafted_state_disabled(self):
        """Test that find_drafted_state returns 0 when disabled"""
        result = self.loader.find_drafted_state('Any Player', 'QB', 'KC')
        self.assertEqual(result, 0)

    def test_get_stats_empty(self):
        """Test statistics with no loaded data"""
        stats = self.loader.get_stats()
        expected = {
            "total_players": 0,
            "user_team_players": 0,
            "other_team_players": 0
        }
        self.assertEqual(stats, expected)

    @patch('drafted_data_loader.LOAD_DRAFTED_DATA_FROM_FILE', True)
    @patch('drafted_data_loader.MY_TEAM_NAME', 'Test Team')
    def test_duplicate_handling(self):
        """Test that duplicate entries are handled correctly"""
        test_data = [
            ['Patrick Mahomes QB - KC', 'Test Team'],
            ['Patrick Mahomes QB - KC', 'Other Team'],  # Duplicate - should be skipped
            ['Different Player WR - NYG', 'Test Team'],
        ]

        csv_file = self.create_test_csv(test_data)

        try:
            with patch('drafted_data_loader.DRAFTED_DATA', csv_file):
                success = self.loader.load_drafted_data()

                self.assertTrue(success)
                self.assertEqual(len(self.loader.drafted_players), 2)  # Only first occurrence counted

                # Verify the first occurrence is kept
                result = self.loader.find_drafted_state('Patrick Mahomes', 'QB', 'KC')
                self.assertEqual(result, 2)  # Should be user team (first entry)
        finally:
            Path(csv_file).unlink()

    def test_config_validation_integration(self):
        """Test that configuration validation works with new settings"""
        # This is an integration test to ensure the config validation catches conflicts
        from shared_files.configs.player_data_fetcher_config import validate_config
        import shared_files.configs.player_data_fetcher_config as player_data_fetcher_config as config

        # Store original values
        original_preserve = config.PRESERVE_DRAFTED_VALUES
        original_load_file = config.LOAD_DRAFTED_DATA_FROM_FILE

        try:
            # Test valid configurations
            config.PRESERVE_DRAFTED_VALUES = True
            config.LOAD_DRAFTED_DATA_FROM_FILE = False
            validate_config()  # Should not raise

            config.PRESERVE_DRAFTED_VALUES = False
            config.LOAD_DRAFTED_DATA_FROM_FILE = True
            validate_config()  # Should not raise

            config.PRESERVE_DRAFTED_VALUES = False
            config.LOAD_DRAFTED_DATA_FROM_FILE = False
            validate_config()  # Should not raise

            # Test invalid configuration
            config.PRESERVE_DRAFTED_VALUES = True
            config.LOAD_DRAFTED_DATA_FROM_FILE = True
            with self.assertRaises(ValueError) as context:
                validate_config()
            self.assertIn("cannot both be enabled", str(context.exception))

        finally:
            # Restore original values
            config.PRESERVE_DRAFTED_VALUES = original_preserve
            config.LOAD_DRAFTED_DATA_FROM_FILE = original_load_file

    @patch('drafted_data_loader.LOAD_DRAFTED_DATA_FROM_FILE', True)
    @patch('drafted_data_loader.MY_TEAM_NAME', 'Test Team')
    def test_apply_drafted_data_to_players(self):
        """Test the new reverse search approach: apply_drafted_data_to_players"""
        # Create test CSV data
        test_data = [
            ['Patrick Mahomes QB - KC', 'Test Team'],          # Should get drafted=2
            ['Christian McCaffrey RB - SF', 'Other Team'],     # Should get drafted=1
            ['Tyreek Hill WR - MIA', 'Test Team'],            # Should get drafted=2
            ['Unknown Player WR - NYG', 'Other Team'],        # Won't match anyone
        ]

        csv_file = self.create_test_csv(test_data)

        try:
            with patch('drafted_data_loader.DRAFTED_DATA', csv_file):
                # Load drafted data from CSV
                success = self.loader.load_drafted_data()
                self.assertTrue(success)

                # Create mock FantasyPlayer objects
                from FantasyPlayer import FantasyPlayer
                mock_players = [
                    FantasyPlayer(
                        id='1234',
                        name='Patrick Mahomes',
                        team='KC',
                        position='QB',
                        fantasy_points=315.5,
                        bye_week=10,
                        drafted=0,  # Initially not drafted
                        locked=0
                    ),
                    FantasyPlayer(
                        id='5678',
                        name='Christian McCaffrey',
                        team='SF',
                        position='RB',
                        fantasy_points=295.2,
                        bye_week=9,
                        drafted=0,  # Initially not drafted
                        locked=0
                    ),
                    FantasyPlayer(
                        id='9012',
                        name='Tyreek Hill',
                        team='MIA',
                        position='WR',
                        fantasy_points=280.7,
                        bye_week=6,
                        drafted=0,  # Initially not drafted
                        locked=0
                    ),
                    FantasyPlayer(
                        id='3456',
                        name='Unrelated Player',
                        team='NYJ',
                        position='TE',
                        fantasy_points=150.0,
                        bye_week=8,
                        drafted=0,  # Should remain 0
                        locked=0
                    ),
                ]

                # Apply drafted data to players (NEW REVERSE SEARCH APPROACH)
                updated_players = self.loader.apply_drafted_data_to_players(mock_players)

                # Verify the results
                player_by_name = {p.name: p for p in updated_players}

                # Patrick Mahomes should be drafted=2 (my team)
                self.assertEqual(player_by_name['Patrick Mahomes'].drafted, 2)

                # Christian McCaffrey should be drafted=1 (other team)
                self.assertEqual(player_by_name['Christian McCaffrey'].drafted, 1)

                # Tyreek Hill should be drafted=2 (my team)
                self.assertEqual(player_by_name['Tyreek Hill'].drafted, 2)

                # Unrelated Player should remain drafted=0
                self.assertEqual(player_by_name['Unrelated Player'].drafted, 0)

                # Verify that all other attributes remain unchanged
                self.assertEqual(player_by_name['Patrick Mahomes'].fantasy_points, 315.5)
                self.assertEqual(player_by_name['Christian McCaffrey'].team, 'SF')
                self.assertEqual(player_by_name['Tyreek Hill'].position, 'WR')

        finally:
            Path(csv_file).unlink()

    @patch('drafted_data_loader.LOAD_DRAFTED_DATA_FROM_FILE', False)
    def test_apply_drafted_data_to_players_disabled(self):
        """Test that apply_drafted_data_to_players does nothing when disabled"""
        from FantasyPlayer import FantasyPlayer

        mock_players = [
            FantasyPlayer(
                id='1234',
                name='Patrick Mahomes',
                team='KC',
                position='QB',
                fantasy_points=315.5,
                bye_week=10,
                drafted=0,
                locked=0
            )
        ]

        # Apply drafted data (should do nothing when disabled)
        updated_players = self.loader.apply_drafted_data_to_players(mock_players)

        # Verify no changes
        self.assertEqual(len(updated_players), 1)
        self.assertEqual(updated_players[0].drafted, 0)
        self.assertEqual(updated_players[0].name, 'Patrick Mahomes')

    @patch('drafted_data_loader.LOAD_DRAFTED_DATA_FROM_FILE', True)
    @patch('drafted_data_loader.MY_TEAM_NAME', 'Sea Sharp')
    def test_apply_drafted_data_defense_name_variations(self):
        """Test defense matching with different name formats (ESPN vs CSV)"""
        # Create test CSV data with full defense names (like real CSV)
        test_data = [
            ['Seattle Seahawks DEF', 'Sea Sharp'],              # Full name in CSV
            ['Baltimore Ravens DEF', 'Other Team'],             # Full name in CSV
        ]

        csv_file = self.create_test_csv(test_data)

        try:
            with patch('drafted_data_loader.DRAFTED_DATA', csv_file):
                # Load drafted data from CSV
                success = self.loader.load_drafted_data()
                self.assertTrue(success)

                # Create mock players as they appear from ESPN (short names)
                from FantasyPlayer import FantasyPlayer
                espn_players = [
                    FantasyPlayer(
                        id='-16026',
                        name='Seahawks D/ST',  # ESPN format - short name
                        team='SEA',
                        position='DST',
                        fantasy_points=100.8,
                        bye_week=8,
                        drafted=0,
                        locked=0
                    ),
                    FantasyPlayer(
                        id='-16033',
                        name='Ravens D/ST',  # ESPN format - short name
                        team='BAL',
                        position='DST',
                        fantasy_points=95.2,
                        bye_week=14,
                        drafted=0,
                        locked=0
                    ),
                ]

                # Apply drafted data (should match despite name format differences)
                updated_players = self.loader.apply_drafted_data_to_players(espn_players)

                # Verify results
                player_by_team = {p.team: p for p in updated_players}

                # Seahawks should be drafted=2 (Sea Sharp team)
                self.assertEqual(player_by_team['SEA'].drafted, 2)
                self.assertEqual(player_by_team['SEA'].name, 'Seahawks D/ST')

                # Ravens should be drafted=1 (Other Team)
                self.assertEqual(player_by_team['BAL'].drafted, 1)
                self.assertEqual(player_by_team['BAL'].name, 'Ravens D/ST')

        finally:
            Path(csv_file).unlink()

    def test_extract_player_components_view_news_suffix(self):
        """Test parsing of entries with 'View News' and other suffixes"""
        test_cases = [
            # Defense entries with "View News" suffix (new format)
            ('Seattle Seahawks DEF View News', ('Seattle Seahawks', 'DEF', 'SEA')),
            ('Denver Broncos DEF View News', ('Denver Broncos', 'DEF', 'DEN')),
            ('Atlanta Falcons DEF View News', ('Atlanta Falcons', 'DEF', 'ATL')),
            ('Pittsburgh Steelers DEF', ('Pittsburgh Steelers', 'DEF', 'PIT')),
            ('Baltimore Ravens DEF View News', ('Baltimore Ravens', 'DEF', 'BAL')),

            # Regular player entries with various suffixes (should still work)
            ('Mike Evans WR - TB D View News', ('Mike Evans', 'WR', 'TB')),
            ('Terry McLaurin WR - WAS Q View News', ('Terry McLaurin', 'WR', 'WAS')),
            ('CeeDee Lamb WR - DAL D', ('CeeDee Lamb', 'WR', 'DAL')),
            ('Justice Hill RB - BAL View News', ('Justice Hill', 'RB', 'BAL')),
        ]

        for input_str, expected in test_cases:
            with self.subTest(input_str=input_str):
                result = self.loader._extract_player_components(input_str)
                self.assertEqual(result, expected,
                    f"Failed to parse '{input_str}' correctly. Got {result}, expected {expected}")

    @patch('drafted_data_loader.LOAD_DRAFTED_DATA_FROM_FILE', True)
    @patch('drafted_data_loader.MY_TEAM_NAME', 'Test Team')
    def test_team_abbreviation_normalization(self):
        """Test team abbreviation normalization (ESPN WSH vs CSV WAS)"""
        # Create test CSV data with WAS abbreviation
        test_data = [
            ['Jacory Croskey-Merritt RB - WAS', 'The Eskimo Brothers'],  # CSV uses WAS
        ]

        csv_file = self.create_test_csv(test_data)

        try:
            with patch('drafted_data_loader.DRAFTED_DATA', csv_file):
                # Load drafted data from CSV
                success = self.loader.load_drafted_data()
                self.assertTrue(success)

                # Create mock player as it appears from ESPN (using WSH)
                from FantasyPlayer import FantasyPlayer
                espn_player = FantasyPlayer(
                    id='4575131',
                    name='Jacory Croskey-Merritt',
                    team='WSH',  # ESPN uses WSH for Washington
                    position='RB',
                    fantasy_points=142.49,
                    bye_week=12,
                    drafted=0,
                    locked=0
                )

                # Apply drafted data (should match despite team abbreviation difference)
                updated_players = self.loader.apply_drafted_data_to_players([espn_player])

                # Verify the result
                self.assertEqual(len(updated_players), 1)
                self.assertEqual(updated_players[0].drafted, 1)  # Should match as other team
                self.assertEqual(updated_players[0].name, 'Jacory Croskey-Merritt')
                self.assertEqual(updated_players[0].team, 'WSH')  # ESPN team preserved

        finally:
            Path(csv_file).unlink()

    def test_team_normalization_methods(self):
        """Test the team normalization helper methods directly"""
        # Test _normalize_team_abbr
        self.assertEqual(self.loader._normalize_team_abbr('WSH'), 'WAS')
        self.assertEqual(self.loader._normalize_team_abbr('WAS'), 'WAS')
        self.assertEqual(self.loader._normalize_team_abbr('KC'), 'KC')  # No mapping needed

        # Test _teams_equivalent
        self.assertTrue(self.loader._teams_equivalent('WSH', 'WAS'))  # Should be equivalent
        self.assertTrue(self.loader._teams_equivalent('WAS', 'WSH'))  # Bidirectional
        self.assertTrue(self.loader._teams_equivalent('KC', 'KC'))    # Same team
        self.assertFalse(self.loader._teams_equivalent('WSH', 'KC'))  # Different teams


if __name__ == '__main__':
    unittest.main()