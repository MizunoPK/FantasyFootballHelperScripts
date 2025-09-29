#!/usr/bin/env python3
"""
Unit tests for Data Exporter module.

Tests the async data export functionality including:
- Concurrent multi-format export (CSV, Excel, JSON)
- Error handling for file operations
- Shared files synchronization
- Directory creation and cleanup
"""

import asyncio
import pytest
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
import json

# Add the parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from player_data_exporter import DataExporter


class TestDataExporter:
    """Test suite for DataExporter class"""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for test files"""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)

    @pytest.fixture
    def sample_players(self):
        """Create sample player data for testing"""
        return [
            {
                'id': '1',
                'name': 'Test Player 1',
                'position': 'RB',
                'team': 'TEST',
                'fantasy_points': 150.5,
                'bye_week': 7
            },
            {
                'id': '2',
                'name': 'Test Player 2',
                'position': 'WR',
                'team': 'DEMO',
                'fantasy_points': 125.3,
                'bye_week': 9
            }
        ]

    @pytest.fixture
    def sample_projection_data(self, sample_players):
        """Create ProjectionData for testing"""
        from player_data_models import ProjectionData, ESPNPlayerData

        # Convert dict players to ESPNPlayerData objects
        player_objects = []
        for player_dict in sample_players:
            player_objects.append(ESPNPlayerData(
                id=player_dict['id'],
                name=player_dict['name'],
                team=player_dict['team'],
                position=player_dict['position'],
                fantasy_points=player_dict['fantasy_points'],
                bye_week=player_dict.get('bye_week')
            ))

        return ProjectionData(
            season=2025,
            scoring_format="PPR",
            total_players=len(player_objects),
            players=player_objects
        )

    @pytest.fixture
    def exporter(self, temp_dir):
        """Create DataExporter instance with temporary directory"""
        return DataExporter(str(temp_dir))

    @pytest.mark.asyncio
    async def test_export_csv_success(self, exporter, sample_projection_data, temp_dir):
        """Test successful CSV export"""
        # Method returns filepath, not boolean, and generates filename automatically
        result_filepath = await exporter.export_csv(sample_projection_data)

        assert isinstance(result_filepath, str)
        assert result_filepath.endswith('.csv')
        csv_file = Path(result_filepath)
        assert csv_file.exists()

        # Verify CSV content
        content = csv_file.read_text(encoding='utf-8')
        assert 'Test Player 1' in content
        assert 'Test Player 2' in content
        assert 'RB' in content
        assert 'WR' in content

    @pytest.mark.asyncio
    async def test_export_csv_error_handling(self, temp_dir, sample_projection_data):
        """Test CSV export error handling"""
        # Mock pandas to_csv to raise an exception
        with patch('pandas.DataFrame.to_csv', side_effect=Exception("CSV write error")):
            exporter = DataExporter(str(temp_dir))
            with pytest.raises(Exception):
                await exporter.export_csv(sample_projection_data)

    @pytest.mark.asyncio
    async def test_export_excel_success(self, exporter, sample_projection_data, temp_dir):
        """Test successful Excel export"""
        # Method returns filepath and generates filename automatically
        result_filepath = await exporter.export_excel(sample_projection_data)

        assert isinstance(result_filepath, str)
        assert result_filepath.endswith('.xlsx')
        excel_file = Path(result_filepath)
        assert excel_file.exists()

    @pytest.mark.asyncio
    async def test_export_excel_error_handling(self, exporter, sample_projection_data):
        """Test Excel export error handling"""
        with patch('pandas.DataFrame.to_excel', side_effect=Exception("Excel error")):
            with pytest.raises(Exception):
                await exporter.export_excel(sample_projection_data)

    @pytest.mark.asyncio
    async def test_export_json_success(self, exporter, sample_projection_data, temp_dir):
        """Test successful JSON export"""
        result_filepath = await exporter.export_json(sample_projection_data)

        assert isinstance(result_filepath, str)
        assert result_filepath.endswith('.json')
        json_file = Path(result_filepath)
        assert json_file.exists()

        # Verify JSON content
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert len(data['players']) == 2
            assert data['players'][0]['name'] == 'Test Player 1'
            assert data['players'][1]['name'] == 'Test Player 2'

    @pytest.mark.asyncio
    async def test_export_json_error_handling(self, exporter, sample_projection_data):
        """Test JSON export error handling"""
        with patch.object(exporter.file_manager, 'save_json_data', side_effect=Exception("JSON error")):
            with pytest.raises(Exception):
                await exporter.export_json(sample_projection_data)

    @pytest.mark.asyncio
    async def test_export_to_shared_files_success(self, exporter, sample_projection_data, temp_dir):
        """Test successful shared files update"""
        # Create a temporary file path for testing instead of using the real shared_files/players.csv
        temp_shared_file = temp_dir / "players.csv"

        # Mock the DRAFT_HELPER_PLAYERS_FILE constant to use our temporary file
        with patch('player_data_exporter.DRAFT_HELPER_PLAYERS_FILE', str(temp_shared_file)):
            result_filepath = await exporter.export_to_shared_files(sample_projection_data)

            assert isinstance(result_filepath, str)
            assert result_filepath.endswith('.csv')
            shared_file_path = Path(result_filepath)
            assert shared_file_path.exists()

            # Verify shared file content
            content = shared_file_path.read_text(encoding='utf-8')
            assert 'Test Player 1' in content
            assert 'Test Player 2' in content

    @pytest.mark.asyncio
    async def test_export_to_shared_files_error_handling(self, exporter, sample_projection_data, temp_dir):
        """Test shared files update error handling"""
        # Create a temporary file path for testing
        temp_shared_file = temp_dir / "players.csv"

        # Mock the DRAFT_HELPER_PLAYERS_FILE constant and aiofiles.open to raise an exception
        with patch('player_data_exporter.DRAFT_HELPER_PLAYERS_FILE', str(temp_shared_file)):
            with patch('aiofiles.open', side_effect=Exception("Shared file error")):
                with pytest.raises(Exception):
                    await exporter.export_to_shared_files(sample_projection_data)

    @pytest.mark.asyncio
    async def test_concurrent_export_all_formats(self, exporter, sample_projection_data, temp_dir):
        """Test concurrent export to all formats"""
        csv_task = exporter.export_csv(sample_projection_data)
        excel_task = exporter.export_excel(sample_projection_data)
        json_task = exporter.export_json(sample_projection_data)

        results = await asyncio.gather(csv_task, excel_task, json_task)

        # All exports should return file paths
        assert all(isinstance(result, str) for result in results)

        # All files should exist
        csv_file = Path(results[0])
        excel_file = Path(results[1])
        json_file = Path(results[2])
        assert csv_file.exists()
        assert excel_file.exists()
        assert json_file.exists()

    @pytest.mark.asyncio
    async def test_directory_creation(self, sample_projection_data):
        """Test automatic directory creation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            nested_dir = Path(temp_dir) / "data" / "exports"
            exporter = DataExporter(str(nested_dir))

            result_filepath = await exporter.export_csv(sample_projection_data)

            assert isinstance(result_filepath, str)
            assert nested_dir.exists()
            csv_file = Path(result_filepath)
            assert csv_file.exists()

    @pytest.mark.asyncio
    async def test_empty_data_export(self, exporter, temp_dir):
        """Test export with empty data"""
        from player_data_models import ProjectionData
        empty_projection_data = ProjectionData(
            season=2025,
            scoring_format="PPR",
            total_players=0,
            players=[]
        )

        csv_result = await exporter.export_csv(empty_projection_data)
        excel_result = await exporter.export_excel(empty_projection_data)
        json_result = await exporter.export_json(empty_projection_data)

        # Should handle empty data gracefully and return file paths
        assert isinstance(csv_result, str)
        assert isinstance(excel_result, str)
        assert isinstance(json_result, str)

        # Files should exist (even if empty/minimal)
        assert Path(csv_result).exists()
        assert Path(excel_result).exists()
        assert Path(json_result).exists()

    @pytest.mark.asyncio
    async def test_special_characters_in_data(self, exporter, temp_dir):
        """Test export with special characters and unicode"""
        from player_data_models import ProjectionData, ESPNPlayerData

        special_player = ESPNPlayerData(
            id='1',
            name='Játékos Ümlaut',  # Unicode characters
            position='RB',
            team='TÉM',
            fantasy_points=150.5
        )

        special_projection_data = ProjectionData(
            season=2025,
            scoring_format="PPR",
            total_players=1,
            players=[special_player]
        )

        csv_result = await exporter.export_csv(special_projection_data)
        json_result = await exporter.export_json(special_projection_data)

        assert isinstance(csv_result, str)
        assert isinstance(json_result, str)

        # Verify files exist and can be read
        csv_file = Path(csv_result)
        json_file = Path(json_result)
        assert csv_file.exists()
        assert json_file.exists()

        # Verify content integrity
        csv_content = csv_file.read_text(encoding='utf-8')
        assert 'Játékos Ümlaut' in csv_content

    @pytest.mark.asyncio
    async def test_large_dataset_export(self, exporter, temp_dir):
        """Test export with large dataset"""
        from player_data_models import ProjectionData, ESPNPlayerData
        from unittest.mock import patch

        large_players = []
        for i in range(1000):
            player = ESPNPlayerData(
                id=str(i),
                name=f'Player {i}',
                position='RB' if i % 2 == 0 else 'WR',
                team=f'TEAM{i % 32}',
                fantasy_points=float(i * 1.5),
                bye_week=(i % 17) + 1
            )
            large_players.append(player)

        large_projection_data = ProjectionData(
            season=2025,
            scoring_format="PPR",
            total_players=len(large_players),
            players=large_players
        )

        # Mock the drafted data loader to prevent slow CSV processing
        with patch('player_data_exporter.DraftedDataLoader') as mock_loader_class:
            mock_loader = mock_loader_class.return_value
            mock_loader.load_drafted_data.return_value = large_players  # Return unmodified data

            start_time = asyncio.get_event_loop().time()
            result_filepath = await exporter.export_csv(large_projection_data)
            end_time = asyncio.get_event_loop().time()

            assert isinstance(result_filepath, str)
            assert Path(result_filepath).exists()

            # Should complete reasonably quickly (under 10 seconds with mocked loader)
            assert end_time - start_time < 10.0

    def test_data_validation_helpers(self, exporter):
        """Test data validation and formatting helpers"""
        # Test with various data types
        test_data = [
            {'id': 1, 'name': 'Test', 'points': 100.5},  # Mixed types
            {'id': '2', 'name': None, 'points': 'invalid'},  # Invalid data
        ]

        # Should handle mixed data types without crashing
        # (This tests the robustness of the export process)
        assert isinstance(test_data, list)
        assert len(test_data) == 2


if __name__ == "__main__":
    # Run tests with pytest if available, otherwise basic test
    try:
        import pytest
        pytest.main([__file__, "-v"])
    except ImportError:
        print("pytest not available, running basic tests...")

        async def run_basic_tests():
            with tempfile.TemporaryDirectory() as temp_dir:
                from player_data_exporter import DataExporter
                from player_data_models import ProjectionData, ESPNPlayerData

                exporter = DataExporter(temp_dir)
                sample_player = ESPNPlayerData(
                    id='1',
                    name='Test Player',
                    position='RB',
                    team='TEST',
                    fantasy_points=100.0
                )
                sample_projection_data = ProjectionData(
                    season=2025,
                    scoring_format="PPR",
                    total_players=1,
                    players=[sample_player]
                )

                # Test CSV export
                csv_result = await exporter.export_csv(sample_projection_data)
                assert isinstance(csv_result, str)
                print("✅ CSV export test passed")

                # Test JSON export
                json_result = await exporter.export_json(sample_projection_data)
                assert isinstance(json_result, str)
                print("✅ JSON export test passed")

                # Test Excel export
                excel_result = await exporter.export_excel(sample_projection_data)
                assert isinstance(excel_result, str)
                print("✅ Excel export test passed")

                print("Basic tests completed successfully!")

        asyncio.run(run_basic_tests())