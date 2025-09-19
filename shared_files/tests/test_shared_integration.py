#!/usr/bin/env python3
"""
Integration tests for shared_files module.

Tests the integration and cross-module compatibility including:
- Data flow between different modules
- File format consistency
- Cross-platform compatibility
- Performance with realistic datasets
"""

import pytest
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
import csv
import json

# Add the parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from FantasyPlayer import FantasyPlayer


class TestSharedFilesIntegration:
    """Integration test suite for shared_files module"""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for test files"""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir, ignore_errors=True)

    @pytest.fixture
    def realistic_player_dataset(self):
        """Create realistic player dataset for integration testing"""
        return [
            {
                'id': '4890973',
                'name': 'Ashton Jeanty',
                'team': 'BOISE',
                'position': 'RB',
                'bye_week': 10,
                'drafted': 0,
                'locked': 0,
                'fantasy_points': 285.3,
                'injury_status': 'ACTIVE',
                'adp': 12.5
            },
            {
                'id': '2555234',
                'name': 'Ja\'Marr Chase',
                'team': 'CIN',
                'position': 'WR',
                'bye_week': 7,
                'drafted': 1,
                'locked': 0,
                'fantasy_points': 234.7,
                'injury_status': 'ACTIVE',
                'adp': 8.2
            },
            {
                'id': '4362887',
                'name': 'Josh Allen',
                'team': 'BUF',
                'position': 'QB',
                'bye_week': 12,
                'drafted': 0,
                'locked': 1,
                'fantasy_points': 387.9,
                'injury_status': 'QUESTIONABLE',
                'adp': 15.3
            },
            {
                'id': '3155899',
                'name': 'Travis Kelce',
                'team': 'KC',
                'position': 'TE',
                'bye_week': 6,
                'drafted': 1,
                'locked': 0,
                'fantasy_points': 178.4,
                'injury_status': 'ACTIVE',
                'adp': 28.7
            },
            {
                'id': '99999',
                'name': 'Injured Player',
                'team': 'INJ',
                'position': 'RB',
                'bye_week': 'nan',  # Problematic data
                'drafted': '',
                'locked': 'none',
                'fantasy_points': 'invalid',
                'injury_status': 'OUT',
                'adp': None
            }
        ]

    def test_full_data_cycle_csv(self, temp_dir, realistic_player_dataset):
        """Test complete data cycle: create -> save to CSV -> load -> verify"""
        csv_file = temp_dir / "test_players.csv"

        # Create players from dataset
        players = [FantasyPlayer.from_dict(data) for data in realistic_player_dataset]

        # Save to CSV
        FantasyPlayer.save_to_csv(players, str(csv_file))
        assert csv_file.exists()

        # Load back from CSV
        loaded_players = FantasyPlayer.load_from_csv(str(csv_file))

        # Verify data integrity
        assert len(loaded_players) == len(players)

        for original, loaded in zip(players, loaded_players):
            assert original.id == loaded.id
            assert original.name == loaded.name
            assert original.position == loaded.position
            assert original.fantasy_points == loaded.fantasy_points
            assert original.drafted == loaded.drafted

        # Verify problematic data was handled correctly
        injured_player = next(p for p in loaded_players if p.name == 'Injured Player')
        assert injured_player.bye_week == 0  # 'nan' converted
        assert injured_player.fantasy_points == 0.0  # 'invalid' converted
        assert injured_player.drafted == 0  # empty string converted
        assert injured_player.locked == 0  # 'none' converted

    def test_cross_format_compatibility(self, temp_dir, realistic_player_dataset):
        """Test compatibility between CSV and Excel formats"""
        csv_file = temp_dir / "players.csv"
        excel_file = temp_dir / "players.xlsx"

        # Create players
        players = [FantasyPlayer.from_dict(data) for data in realistic_player_dataset]

        # Save to both formats
        FantasyPlayer.save_to_csv(players, str(csv_file))

        # Load from CSV
        csv_players = FantasyPlayer.load_from_csv(str(csv_file))

        # Export to Excel using pandas (simulate Excel save)
        import pandas as pd
        player_dicts = [p.to_dict() for p in csv_players]
        df = pd.DataFrame(player_dicts)
        df.to_excel(excel_file, index=False)

        # Load from Excel
        excel_players = FantasyPlayer.load_from_excel(str(excel_file), 'Sheet1')

        # Verify both formats produce identical results
        assert len(csv_players) == len(excel_players)

        for csv_player, excel_player in zip(csv_players, excel_players):
            assert csv_player.id == excel_player.id
            assert csv_player.name == excel_player.name
            assert csv_player.fantasy_points == excel_player.fantasy_points

    def test_data_preservation_with_mixed_types(self, temp_dir):
        """Test data preservation with various data types and edge cases"""
        mixed_data = [
            {
                'id': '1',
                'name': 'Normal Player',
                'position': 'RB',
                'bye_week': 7,
                'fantasy_points': 150.5,
                'drafted': 0
            },
            {
                'id': '2',
                'name': 'Edge Case Player',
                'position': 'WR',
                'bye_week': 'nan',
                'fantasy_points': '',
                'drafted': 'none'
            },
            {
                'id': '3',
                'name': 'Unicode Player ÄÖÜ',
                'position': 'QB',
                'bye_week': None,
                'fantasy_points': 'invalid',
                'drafted': 'TRUE'
            }
        ]

        csv_file = temp_dir / "mixed_data.csv"

        # Process through full cycle
        players = [FantasyPlayer.from_dict(data) for data in mixed_data]
        FantasyPlayer.save_to_csv(players, str(csv_file))
        loaded_players = FantasyPlayer.load_from_csv(str(csv_file))

        # Verify all edge cases handled
        assert len(loaded_players) == 3

        # Normal player should be unchanged
        normal = loaded_players[0]
        assert normal.bye_week == 7
        assert normal.fantasy_points == 150.5

        # Edge case player should have safe defaults
        edge = loaded_players[1]
        assert edge.bye_week == 0
        assert edge.fantasy_points == 0.0
        assert edge.drafted == 0

        # Unicode player should preserve unicode
        unicode_player = loaded_players[2]
        assert 'ÄÖÜ' in unicode_player.name
        assert unicode_player.bye_week == 0

    def test_performance_with_large_realistic_dataset(self, temp_dir):
        """Test performance with large, realistic dataset"""
        # Generate large dataset with realistic NFL player data
        large_dataset = []
        positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']
        teams = ['BUF', 'NE', 'MIA', 'NYJ', 'CIN', 'CLE', 'BAL', 'PIT']
        injury_statuses = ['ACTIVE', 'QUESTIONABLE', 'DOUBTFUL', 'OUT']

        for i in range(2000):  # Realistic NFL player pool size
            player_data = {
                'id': str(i + 1),
                'name': f'Player {i + 1}',
                'team': teams[i % len(teams)],
                'position': positions[i % len(positions)],
                'bye_week': (i % 17) + 1,
                'drafted': 1 if i < 150 else 0,  # ~150 drafted players realistic
                'locked': 1 if i < 20 else 0,  # ~20 locked players
                'fantasy_points': round(abs(300 - i * 0.15), 1),  # Declining points
                'injury_status': injury_statuses[i % len(injury_statuses)],
                'adp': round(i * 0.1 + 1, 1)
            }
            large_dataset.append(player_data)

        csv_file = temp_dir / "large_dataset.csv"

        import time

        # Test creation performance
        start_time = time.time()
        players = [FantasyPlayer.from_dict(data) for data in large_dataset]
        creation_time = time.time() - start_time

        # Test save performance
        start_time = time.time()
        FantasyPlayer.save_to_csv(players, str(csv_file))
        save_time = time.time() - start_time

        # Test load performance
        start_time = time.time()
        loaded_players = FantasyPlayer.load_from_csv(str(csv_file))
        load_time = time.time() - start_time

        # Performance assertions (should be reasonable for 2000 players)
        assert creation_time < 2.0  # Should create 2000 players in under 2 seconds
        assert save_time < 3.0  # Should save in under 3 seconds
        assert load_time < 3.0  # Should load in under 3 seconds

        # Verify data integrity
        assert len(loaded_players) == 2000
        assert loaded_players[0].name == 'Player 1'
        assert loaded_players[-1].name == 'Player 2000'

    def test_file_encoding_and_special_characters(self, temp_dir):
        """Test file encoding with special characters and international names"""
        international_players = [
            {
                'id': '1',
                'name': 'José Rodríguez',
                'team': 'MIA',
                'position': 'RB',
                'fantasy_points': 150.5
            },
            {
                'id': '2',
                'name': 'François Müller',
                'team': 'GB',
                'position': 'WR',
                'fantasy_points': 125.3
            },
            {
                'id': '3',
                'name': 'Олексій Петренко',  # Cyrillic
                'team': 'NYJ',
                'position': 'QB',
                'fantasy_points': 280.7
            },
            {
                'id': '4',
                'name': '山田太郎',  # Japanese
                'team': 'SF',
                'position': 'TE',
                'fantasy_points': 90.2
            }
        ]

        csv_file = temp_dir / "international.csv"

        # Process international names
        players = [FantasyPlayer.from_dict(data) for data in international_players]
        FantasyPlayer.save_to_csv(players, str(csv_file))

        # Verify file was created with UTF-8 encoding
        assert csv_file.exists()

        # Load and verify encoding preserved
        loaded_players = FantasyPlayer.load_from_csv(str(csv_file))

        assert len(loaded_players) == 4
        assert loaded_players[0].name == 'José Rodríguez'
        assert loaded_players[1].name == 'François Müller'
        assert loaded_players[2].name == 'Олексій Петренко'
        assert loaded_players[3].name == '山田太郎'

    def test_data_validation_and_consistency(self, realistic_player_dataset):
        """Test data validation and consistency across operations"""
        # Create players with validation
        players = []
        for data in realistic_player_dataset:
            player = FantasyPlayer.from_dict(data)

            # Basic validation
            assert isinstance(player.id, str)
            assert len(player.id) > 0
            assert isinstance(player.name, str)
            assert len(player.name) > 0
            assert player.position in ['QB', 'RB', 'WR', 'TE', 'K', 'DST']
            assert isinstance(player.fantasy_points, float)
            assert isinstance(player.bye_week, int)
            assert player.bye_week >= 0
            assert player.drafted in [0, 1]
            assert player.locked in [0, 1]

            players.append(player)

        # Verify all validations passed
        assert len(players) == len(realistic_player_dataset)

        # Test export/import consistency
        exported_dicts = [p.to_dict() for p in players]
        reimported_players = [FantasyPlayer.from_dict(d) for d in exported_dicts]

        # Should be identical after round trip
        for original, reimported in zip(players, reimported_players):
            assert original.id == reimported.id
            assert original.name == reimported.name
            assert original.fantasy_points == reimported.fantasy_points

    def test_error_resilience_and_recovery(self, temp_dir):
        """Test error resilience and recovery mechanisms"""
        # Test with corrupted CSV data
        corrupted_csv = temp_dir / "corrupted.csv"
        corrupted_content = """id,name,position,fantasy_points
1,Player One,RB,150.5
2,Player Two,WR,invalid_number
CORRUPTED LINE WITHOUT PROPER COLUMNS
3,Player Three,QB,280.7"""

        corrupted_csv.write_text(corrupted_content, encoding='utf-8')

        # Should handle corrupted data gracefully
        players = FantasyPlayer.load_from_csv(str(corrupted_csv))

        # Should load valid rows and skip/handle invalid ones
        assert len(players) >= 2  # At least the valid rows
        valid_players = [p for p in players if p.name in ['Player One', 'Player Three']]
        assert len(valid_players) >= 2

    def test_cross_platform_path_handling(self, temp_dir):
        """Test cross-platform file path handling"""
        # Test with various path formats
        csv_file = temp_dir / "cross_platform.csv"

        players = [
            FantasyPlayer(id='1', name='Test Player', team='TEST', position='RB', fantasy_points=100.0)
        ]

        # Test with Path object
        FantasyPlayer.save_to_csv(players, csv_file)
        loaded1 = FantasyPlayer.load_from_csv(csv_file)

        # Test with string path
        FantasyPlayer.save_to_csv(players, str(csv_file))
        loaded2 = FantasyPlayer.load_from_csv(str(csv_file))

        # Should work with both path types
        assert len(loaded1) == 1
        assert len(loaded2) == 1
        assert loaded1[0].name == loaded2[0].name

    def test_memory_efficiency_and_cleanup(self, temp_dir):
        """Test memory efficiency and proper cleanup"""
        # Create moderately large dataset
        medium_dataset = []
        for i in range(500):
            data = {
                'id': str(i),
                'name': f'Player {i}',
                'position': 'RB',
                'fantasy_points': float(i),
                'extra_data': 'x' * 100  # Some extra data to increase memory usage
            }
            medium_dataset.append(data)

        csv_file = temp_dir / "memory_test.csv"

        # Process data multiple times to test memory cleanup
        for iteration in range(3):
            players = [FantasyPlayer.from_dict(data) for data in medium_dataset]
            FantasyPlayer.save_to_csv(players, str(csv_file))
            loaded_players = FantasyPlayer.load_from_csv(str(csv_file))

            # Verify data integrity each iteration
            assert len(loaded_players) == 500
            assert loaded_players[0].name == 'Player 0'
            assert loaded_players[-1].name == 'Player 499'

            # Clear references to allow garbage collection
            del players
            del loaded_players

        # Should complete all iterations without memory issues


if __name__ == "__main__":
    # Run tests with pytest if available, otherwise basic test
    try:
        import pytest
        pytest.main([__file__, "-v"])
    except ImportError:
        print("pytest not available, running basic integration tests...")

        import tempfile
        import time

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Test basic data cycle
            test_data = [
                {'id': '1', 'name': 'Test Player', 'position': 'RB', 'fantasy_points': 100.5},
                {'id': '2', 'name': 'Test Player 2', 'position': 'WR', 'fantasy_points': 'invalid'}
            ]

            players = [FantasyPlayer.from_dict(data) for data in test_data]
            csv_file = temp_path / "test.csv"

            FantasyPlayer.save_to_csv(players, str(csv_file))
            loaded_players = FantasyPlayer.load_from_csv(str(csv_file))

            assert len(loaded_players) == 2
            assert loaded_players[0].name == 'Test Player'
            assert loaded_players[1].fantasy_points == 0.0  # 'invalid' converted
            print("✅ Basic data cycle test passed")

            # Test performance with larger dataset
            large_data = []
            for i in range(1000):
                large_data.append({
                    'id': str(i),
                    'name': f'Player {i}',
                    'position': 'RB',
                    'fantasy_points': float(i)
                })

            start_time = time.time()
            large_players = [FantasyPlayer.from_dict(data) for data in large_data]
            creation_time = time.time() - start_time

            assert len(large_players) == 1000
            assert creation_time < 2.0  # Should be fast
            print("✅ Performance test passed")

            # Test special characters
            unicode_data = {
                'id': '999',
                'name': 'José Müller',
                'position': 'QB',
                'fantasy_points': 200.0
            }

            unicode_player = FantasyPlayer.from_dict(unicode_data)
            assert unicode_player.name == 'José Müller'
            print("✅ Unicode handling test passed")

            print("Basic integration tests completed successfully!")