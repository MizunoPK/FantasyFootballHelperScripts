#!/usr/bin/env python3
"""
Unit tests for FantasyPlayer class.

Tests the enhanced FantasyPlayer functionality including:
- Robust data type conversion fixes
- CSV/Excel file loading with error handling
- Player creation and validation
- Data export and import integrity
"""

import pytest
import sys
import tempfile
import csv
from pathlib import Path
from unittest.mock import patch, MagicMock
import pandas as pd

# Add the parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from FantasyPlayer import FantasyPlayer


class TestFantasyPlayer:
    """Test suite for FantasyPlayer class with enhanced type conversion"""

    @pytest.fixture
    def sample_player_data(self):
        """Create sample player data for testing"""
        return {
            'id': '12345',
            'name': 'Test Player',
            'team': 'TEST',
            'position': 'RB',
            'bye_week': 7,
            'drafted': 0,
            'locked': 0,
            'fantasy_points': 150.5,
            'injury_status': 'ACTIVE',
            'average_draft_position': 25.3
        }

    def test_player_creation_basic(self, sample_player_data):
        """Test basic player creation with valid data"""
        player = FantasyPlayer(**sample_player_data)

        assert player.id == '12345'
        assert player.name == 'Test Player'
        assert player.team == 'TEST'
        assert player.position == 'RB'
        assert player.bye_week == 7
        assert player.drafted == 0
        assert player.locked == 0
        assert player.fantasy_points == 150.5
        assert player.injury_status == 'ACTIVE'
        assert player.adp == 25.3

    def test_player_creation_minimal(self):
        """Test player creation with minimal required data"""
        player = FantasyPlayer(
            id='123',
            name='Minimal Player',
            team='TEST',
            position='QB'
        )

        assert player.id == '123'
        assert player.name == 'Minimal Player'
        assert player.position == 'QB'
        assert player.team == 'TEST'  # Set value
        assert player.bye_week is None  # Default value
        assert player.fantasy_points == 0.0  # Default value

    def test_safe_int_conversion_function(self):
        """Test the safe_int_conversion helper function"""
        from FantasyPlayer import safe_int_conversion

        # Valid integer strings
        assert safe_int_conversion('123') == 123
        assert safe_int_conversion('0') == 0
        assert safe_int_conversion('-5') == -5

        # Invalid strings should return default (0 when specified)
        assert safe_int_conversion('nan', 0) == 0
        assert safe_int_conversion('none', 0) == 0
        assert safe_int_conversion('null', 0) == 0
        assert safe_int_conversion('invalid', 0) == 0
        assert safe_int_conversion('', 0) == 0

        # None and empty values with explicit default
        assert safe_int_conversion(None, 0) == 0
        assert safe_int_conversion('', 0) == 0

        # None should return None when no default specified
        assert safe_int_conversion(None) is None
        assert safe_int_conversion('nan') is None

        # Custom default
        assert safe_int_conversion('invalid', default=99) == 99

        # Already integers
        assert safe_int_conversion(123) == 123

    def test_safe_float_conversion_function(self):
        """Test the safe_float_conversion helper function"""
        from FantasyPlayer import safe_float_conversion

        # Valid float strings
        assert safe_float_conversion('123.45') == 123.45
        assert safe_float_conversion('0.0') == 0.0
        assert safe_float_conversion('-5.5') == -5.5

        # Invalid strings should return default
        assert safe_float_conversion('nan') == 0.0
        assert safe_float_conversion('none') == 0.0
        assert safe_float_conversion('null') == 0.0
        assert safe_float_conversion('invalid') == 0.0
        assert safe_float_conversion('') == 0.0

        # None and empty values
        assert safe_float_conversion(None) == 0.0
        assert safe_float_conversion('') == 0.0

        # Custom default
        assert safe_float_conversion('invalid', default=99.9) == 99.9

        # Already floats
        assert safe_float_conversion(123.45) == 123.45

    def test_from_dict_method_valid_data(self, sample_player_data):
        """Test from_dict method with valid data"""
        player = FantasyPlayer.from_dict(sample_player_data)

        assert player.id == '12345'
        assert player.name == 'Test Player'
        assert player.fantasy_points == 150.5
        assert player.bye_week == 7

    def test_from_dict_method_problematic_data(self):
        """Test from_dict method with problematic data that was causing bugs"""
        problematic_data = {
            'id': '123',
            'name': 'Problematic Player',
            'team': 'TEST',
            'position': 'RB',
            'bye_week': 'nan',  # This was problematic before the fix
            'fantasy_points': 'invalid',  # This was problematic
            'drafted': '',  # Empty string
            'locked': 'none',  # String 'none'
            'average_draft_position': None  # None value
        }

        player = FantasyPlayer.from_dict(problematic_data)

        # Should handle all problematic values gracefully
        assert player.id == '123'
        assert player.name == 'Problematic Player'
        assert player.bye_week == 0  # Converted from 'nan'
        assert player.fantasy_points == 0.0  # Converted from 'invalid'
        assert player.drafted == 0  # Converted from empty string
        assert player.locked == 0  # Converted from 'none'
        assert player.average_draft_position is None  # None remains None for optional fields

    def test_to_dict_method(self, sample_player_data):
        """Test to_dict method exports data correctly"""
        player = FantasyPlayer(**sample_player_data)
        exported_dict = player.to_dict()

        # Should contain all the same data
        assert exported_dict['id'] == '12345'
        assert exported_dict['name'] == 'Test Player'
        assert exported_dict['fantasy_points'] == 150.5
        assert exported_dict['bye_week'] == 7

        # Should be a complete dictionary
        assert isinstance(exported_dict, dict)
        assert len(exported_dict) > 5  # Should have multiple fields

    def test_load_from_csv_file_success(self):
        """Test loading players from CSV file"""
        # Create temporary CSV file
        csv_data = """id,name,team,position,bye_week,fantasy_points,drafted,locked
1,Player One,TEAM1,RB,7,150.5,0,0
2,Player Two,TEAM2,WR,9,125.3,1,0
3,Player Three,TEAM3,QB,5,280.7,0,1"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_data)
            csv_file_path = f.name

        try:
            players = FantasyPlayer.load_from_csv(csv_file_path)

            assert len(players) == 3
            assert players[0].id == '1'
            assert players[0].name == 'Player One'
            assert players[0].fantasy_points == 150.5
            assert players[1].drafted == 1
            assert players[2].locked == 1

        finally:
            Path(csv_file_path).unlink()

    def test_load_from_csv_file_with_problematic_data(self):
        """Test loading CSV with problematic data that caused original bugs"""
        # CSV with problematic values that were causing crashes
        problematic_csv = """id,name,team,position,bye_week,fantasy_points,drafted,locked
1,Player One,TEAM1,RB,nan,150.5,0,0
2,Player Two,TEAM2,WR,,invalid,none,
3,Player Three,TEAM3,QB,null,280.7,,1"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(problematic_csv)
            csv_file_path = f.name

        try:
            players = FantasyPlayer.load_from_csv(csv_file_path)

            # Should successfully load and convert problematic values
            assert len(players) == 3

            # Player 1: 'nan' bye_week should become 0
            assert players[0].bye_week == 0

            # Player 2: empty bye_week, 'invalid' fantasy_points, 'none' drafted
            assert players[1].bye_week == 0
            assert players[1].fantasy_points == 0.0
            assert players[1].drafted == 0

            # Player 3: 'null' bye_week, empty drafted
            assert players[2].bye_week == 0
            assert players[2].drafted == 0

        finally:
            Path(csv_file_path).unlink()

    def test_load_from_csv_file_missing(self):
        """Test loading from non-existent CSV file"""
        with pytest.raises(FileNotFoundError):
            FantasyPlayer.load_from_csv('nonexistent_file.csv')

    def test_load_from_excel_file_success(self):
        """Test loading players from Excel file"""
        # Create temporary Excel file using pandas
        data = {
            'id': ['1', '2', '3'],
            'name': ['Player One', 'Player Two', 'Player Three'],
            'team': ['TEAM1', 'TEAM2', 'TEAM3'],
            'position': ['RB', 'WR', 'QB'],
            'bye_week': [7, 9, 5],
            'fantasy_points': [150.5, 125.3, 280.7],
            'drafted': [0, 1, 0],
            'locked': [0, 0, 1]
        }

        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            excel_file_path = f.name

        try:
            df = pd.DataFrame(data)
            df.to_excel(excel_file_path, index=False)

            players = FantasyPlayer.load_from_excel(excel_file_path, 'Sheet1')

            assert len(players) == 3
            assert players[0].name == 'Player One'
            assert players[1].drafted == 1
            assert players[2].locked == 1

        finally:
            Path(excel_file_path).unlink()

    def test_load_from_excel_file_with_problematic_data(self):
        """Test loading Excel with problematic data"""
        # Excel with NaN and other problematic values
        data = {
            'id': ['1', '2', '3'],
            'name': ['Player One', 'Player Two', 'Player Three'],
            'team': ['TEAM1', 'TEAM2', 'TEAM3'],
            'position': ['RB', 'WR', 'QB'],
            'bye_week': [float('nan'), None, 'invalid'],  # Problematic values
            'fantasy_points': ['invalid', 150.5, None],  # Mixed types
            'drafted': [0, 'none', ''],  # Various empty/invalid values
        }

        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            excel_file_path = f.name

        try:
            df = pd.DataFrame(data)
            df.to_excel(excel_file_path, index=False)

            players = FantasyPlayer.load_from_excel(excel_file_path, 'Sheet1')

            # Should handle all problematic values
            assert len(players) == 3
            assert players[0].bye_week == 0  # NaN converted
            assert players[0].fantasy_points == 0.0  # 'invalid' converted
            assert players[1].drafted == 0  # 'none' converted
            assert players[2].fantasy_points == 0.0  # None converted

        finally:
            Path(excel_file_path).unlink()

    def test_load_from_excel_file_missing(self):
        """Test loading from non-existent Excel file"""
        with pytest.raises(FileNotFoundError):
            FantasyPlayer.load_from_excel('nonexistent_file.xlsx')

    def test_save_to_csv_file(self):
        """Test saving players to CSV file"""
        players = [
            FantasyPlayer(id='1', name='Player One', team='TEAM1', position='RB', fantasy_points=150.5),
            FantasyPlayer(id='2', name='Player Two', team='TEAM2', position='WR', fantasy_points=125.3)
        ]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            csv_file_path = f.name

        try:
            # Save to CSV
            FantasyPlayer.save_to_csv(players, csv_file_path)

            # Verify file was created and has correct content
            assert Path(csv_file_path).exists()

            with open(csv_file_path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)

            assert len(rows) == 2
            assert rows[0]['name'] == 'Player One'
            assert rows[1]['name'] == 'Player Two'

        finally:
            Path(csv_file_path).unlink()

    def test_player_equality_and_comparison(self):
        """Test player equality and comparison methods"""
        player1 = FantasyPlayer(id='123', name='Player', team='TEAM1', position='RB')
        player2 = FantasyPlayer(id='123', name='Player', team='TEAM1', position='RB')
        player3 = FantasyPlayer(id='456', name='Different', team='TEAM2', position='WR')

        # Test equality (should be based on ID)
        assert player1.id == player2.id
        assert player1.id != player3.id

        # Test string representation
        player_str = str(player1)
        assert 'Player' in player_str
        assert 'RB' in player_str

    def test_data_type_edge_cases(self):
        """Test edge cases in data type conversion"""
        edge_case_data = {
            'id': '123',
            'name': 'Edge Case Player',
            'position': 'RB',
            'bye_week': float('inf'),  # Infinity
            'fantasy_points': float('-inf'),  # Negative infinity
            'drafted': 'TRUE',  # String boolean
            'locked': 'false',  # String boolean lowercase
        }

        player = FantasyPlayer.from_dict(edge_case_data)

        # Should handle extreme values gracefully
        assert player.id == '123'
        assert player.name == 'Edge Case Player'
        # Infinity values should be converted to safe defaults
        assert isinstance(player.bye_week, int)
        assert isinstance(player.fantasy_points, float)

    def test_unicode_and_special_characters(self):
        """Test handling of unicode and special characters"""
        unicode_data = {
            'id': '123',
            'name': 'Jäger ÖÄÜ',  # Unicode characters
            'team': 'TËÄM',
            'position': 'RB',
            'fantasy_points': 100.5
        }

        player = FantasyPlayer.from_dict(unicode_data)

        assert player.name == 'Jäger ÖÄÜ'
        assert player.team == 'TËÄM'

        # Test export and import cycle with unicode
        exported = player.to_dict()
        reimported = FantasyPlayer.from_dict(exported)

        assert reimported.name == 'Jäger ÖÄÜ'
        assert reimported.team == 'TËÄM'

    def test_performance_with_large_dataset(self):
        """Test performance with large number of players"""
        # Create large dataset
        large_dataset = []
        for i in range(1000):
            data = {
                'id': str(i),
                'name': f'Player {i}',
                'position': 'RB' if i % 2 == 0 else 'WR',
                'fantasy_points': float(i * 1.5),
                'bye_week': (i % 17) + 1
            }
            large_dataset.append(data)

        # Test batch conversion
        players = [FantasyPlayer.from_dict(data) for data in large_dataset]

        assert len(players) == 1000
        assert all(isinstance(p, FantasyPlayer) for p in players)

        # Test that all conversions worked
        assert players[0].fantasy_points == 0.0
        assert players[999].fantasy_points == 1498.5

    def test_backwards_compatibility(self):
        """Test backwards compatibility with old data formats"""
        # Old format might be missing some fields
        old_format_data = {
            'id': '123',
            'name': 'Old Format Player',
            'position': 'RB',
            # Missing newer fields like injury_status, adp, etc.
        }

        player = FantasyPlayer.from_dict(old_format_data)

        # Should create player with defaults for missing fields
        assert player.id == '123'
        assert player.name == 'Old Format Player'
        assert player.position == 'RB'
        assert hasattr(player, 'injury_status')  # Should have default
        assert hasattr(player, 'adp')  # Should have default


if __name__ == "__main__":
    # Run tests with pytest if available, otherwise basic test
    try:
        import pytest
        pytest.main([__file__, "-v"])
    except ImportError:
        print("pytest not available, running basic tests...")

        # Basic test runner
        print("Testing FantasyPlayer creation...")
        player = FantasyPlayer(
            id='test1',
            name='Test Player',
            position='RB',
            fantasy_points=100.5
        )
        assert player.name == 'Test Player'
        assert player.fantasy_points == 100.5
        print("✅ Player creation test passed")

        # Test safe conversion functions
        from FantasyPlayer import safe_int_conversion, safe_float_conversion

        assert safe_int_conversion('123') == 123
        assert safe_int_conversion('nan') == 0
        assert safe_float_conversion('123.45') == 123.45
        assert safe_float_conversion('invalid') == 0.0
        print("✅ Safe conversion functions test passed")

        # Test from_dict with problematic data
        problematic_data = {
            'id': '123',
            'name': 'Test',
            'position': 'RB',
            'bye_week': 'nan',
            'fantasy_points': 'invalid'
        }
        player2 = FantasyPlayer.from_dict(problematic_data)
        assert player2.bye_week == 0
        assert player2.fantasy_points == 0.0
        print("✅ Problematic data handling test passed")

        # Test CSV loading with missing file
        players = FantasyPlayer.load_from_csv('nonexistent.csv')
        assert players == []
        print("✅ Missing file handling test passed")

        print("Basic tests completed successfully!")