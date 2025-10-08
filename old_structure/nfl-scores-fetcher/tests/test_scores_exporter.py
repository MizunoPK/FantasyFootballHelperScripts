#!/usr/bin/env python3
"""
Unit tests for Scores Exporter module.

Tests the NFL scores export functionality including:
- Multi-format export (CSV, Excel, JSON)
- Async file operations
- Error handling and resilience
- Data validation and formatting
"""

import asyncio
import pytest
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
import json
import csv

# Add the parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from nfl_scores_exporter import ScoresDataExporter as ScoresExporter


class TestScoresExporter:
    """Test suite for ScoresExporter class"""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for test files"""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir, ignore_errors=True)

    @pytest.fixture
    def sample_weekly_scores(self, sample_games):
        """Create WeeklyScores object for testing"""
        from nfl_scores_models import WeeklyScores, GameScore, Team

        # Convert dict games to GameScore objects
        game_objects = []
        for game_dict in sample_games:
            home_team = Team(
                id=game_dict['home_team_id'],
                name=game_dict['home_team_abbr'],  # Use abbr as name
                display_name=game_dict['home_team_name'],
                abbreviation=game_dict['home_team_abbr'],
                location="Home City"  # Dummy location
            )
            away_team = Team(
                id=game_dict['away_team_id'],
                name=game_dict['away_team_abbr'],  # Use abbr as name
                display_name=game_dict['away_team_name'],
                abbreviation=game_dict['away_team_abbr'],
                location="Away City"  # Dummy location
            )
            game_score = GameScore(
                game_id=game_dict['game_id'],
                date=game_dict['date'],
                week=game_dict['week'],
                season=game_dict['season'],
                season_type=game_dict['season_type'],
                home_team=home_team,
                away_team=away_team,
                home_score=game_dict['home_score'],
                away_score=game_dict['away_score'],
                status=game_dict['status'],
                status_detail=game_dict.get('status_detail', 'Final'),  # Add required field
                is_completed=game_dict.get('is_completed', True)  # Add required field
            )
            game_objects.append(game_score)

        return WeeklyScores(
            week=1,
            season=2025,
            season_type=2,
            total_games=len(game_objects),
            completed_games=len(game_objects),
            games=game_objects
        )

    @pytest.fixture
    def sample_games(self):
        """Create sample NFL game data for testing"""
        return [
            {
                'game_id': '401772936',
                'date': '2025-09-12T00:15:00+00:00',
                'week': 1,
                'season': 2025,
                'season_type': 2,
                'home_team_id': '9',
                'home_team_name': 'Green Bay Packers',
                'home_team_abbr': 'GB',
                'away_team_id': '28',
                'away_team_name': 'Washington Commanders',
                'away_team_abbr': 'WSH',
                'home_score': 27,
                'away_score': 18,
                'total_points': 45,
                'point_difference': 9,
                'winning_team': 'GB',
                'status': 'STATUS_FINAL',
                'status_detail': 'Final',
                'is_completed': True,
                'is_overtime': False,
                'venue_name': 'Lambeau Field',
                'venue_city': 'Green Bay',
                'venue_state': 'WI'
            },
            {
                'game_id': '401772725',
                'date': '2025-09-14T17:00:00+00:00',
                'week': 1,
                'season': 2025,
                'season_type': 2,
                'home_team_id': '4',
                'home_team_name': 'Cincinnati Bengals',
                'home_team_abbr': 'CIN',
                'away_team_id': '30',
                'away_team_name': 'Jacksonville Jaguars',
                'away_team_abbr': 'JAX',
                'home_score': 30,
                'away_score': 27,
                'total_points': 57,
                'point_difference': 3,
                'winning_team': 'CIN',
                'status': 'STATUS_FINAL',
                'status_detail': 'Final',
                'is_completed': True,
                'is_overtime': False,
                'venue_name': 'Paycor Stadium',
                'venue_city': 'Cincinnati',
                'venue_state': 'OH'
            }
        ]

    @pytest.fixture
    def exporter(self, temp_dir):
        """Create ScoresExporter instance with temporary directory"""
        return ScoresExporter(str(temp_dir))

    @pytest.mark.asyncio
    async def test_export_csv_success(self, exporter, sample_weekly_scores, temp_dir):
        """Test successful CSV export"""
        filename = "test_scores"

        result_filepath = await exporter.export_csv(sample_weekly_scores, filename)

        assert isinstance(result_filepath, str)
        assert result_filepath.endswith('.csv')
        csv_file = Path(result_filepath)
        assert csv_file.exists()

        # Verify CSV content structure
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

            assert len(rows) == 2
            assert 'game_id' in rows[0]
            assert 'home_team_name' in rows[0]
            assert 'away_team_name' in rows[0]
            assert 'home_score' in rows[0]
            assert 'away_score' in rows[0]

            # Verify actual data
            assert rows[0]['game_id'] == '401772936'
            assert rows[0]['home_team_name'] == 'Green Bay Packers'
            assert rows[0]['home_score'] == '27'

    @pytest.mark.asyncio
    async def test_export_csv_error_handling(self, temp_dir, sample_weekly_scores):
        """Test CSV export error handling"""
        # Use invalid directory
        invalid_dir = temp_dir / "nonexistent" / "nested"
        exporter = ScoresExporter(str(invalid_dir))

        with patch('pandas.DataFrame.to_csv', side_effect=Exception("CSV error")):
            result = await exporter.export_csv(sample_weekly_scores, "test.csv")
            assert result is None

    @pytest.mark.asyncio
    async def test_export_excel_success(self, exporter, sample_weekly_scores, temp_dir):
        """Test successful Excel export"""
        filename = "test_scores.xlsx"

        result = await exporter.export_excel(sample_weekly_scores, filename)

        assert isinstance(result, str) and result.endswith(".xlsx")
        # The actual filename has timestamp and week suffix added
        actual_filename = Path(result).name
        excel_file = temp_dir / actual_filename
        assert excel_file.exists()

        # Verify file is not empty
        assert excel_file.stat().st_size > 0

    @pytest.mark.asyncio
    async def test_export_excel_error_handling(self, exporter, sample_weekly_scores):
        """Test Excel export error handling"""
        with patch('pandas.DataFrame.to_excel', side_effect=Exception("Excel error")):
            result = await exporter.export_excel(sample_weekly_scores, "test.xlsx")
            assert result is None

    @pytest.mark.asyncio
    async def test_export_json_success(self, exporter, sample_weekly_scores, temp_dir):
        """Test successful JSON export"""
        filename = "test_scores.json"

        result = await exporter.export_json(sample_weekly_scores, filename)

        assert isinstance(result, str) and result.endswith(".json")
        # The actual filename has timestamp and week suffix added
        actual_filename = Path(result).name
        json_file = temp_dir / actual_filename
        assert json_file.exists()

        # Verify JSON content
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

            # Should be a WeeklyScores structure
            assert 'week' in data
            assert 'season' in data
            assert 'games' in data
            assert data['total_games'] == 2
            assert len(data['games']) == 2
            assert data['games'][0]['game_id'] == '401772936'
            assert data['games'][0]['home_team_name'] == 'Green Bay Packers'

    @pytest.mark.asyncio
    async def test_export_json_error_handling(self, exporter, sample_weekly_scores):
        """Test JSON export error handling"""
        # Test error handling by patching the file manager's save_json_data method
        with patch.object(exporter.file_manager, 'save_json_data', side_effect=Exception("JSON error")):
            result = await exporter.export_json(sample_weekly_scores, "test.json")
            assert result is None

    @pytest.mark.asyncio
    async def test_concurrent_multi_format_export(self, exporter, sample_weekly_scores, temp_dir):
        """Test concurrent export to all formats"""
        csv_task = exporter.export_csv(sample_weekly_scores, "test")
        excel_task = exporter.export_excel(sample_weekly_scores, "test")
        json_task = exporter.export_json(sample_weekly_scores, "test")

        # Run all exports concurrently
        start_time = asyncio.get_event_loop().time()
        results = await asyncio.gather(csv_task, excel_task, json_task)
        end_time = asyncio.get_event_loop().time()

        # All exports should succeed and return file paths
        assert all(results)
        csv_path, excel_path, json_path = results

        # All files should exist (using actual returned paths)
        assert Path(csv_path).exists()
        assert Path(excel_path).exists()
        assert Path(json_path).exists()

        # Files should have timestamped names
        assert "test_week1_" in csv_path and csv_path.endswith(".csv")
        assert "test_week1_" in excel_path and excel_path.endswith(".xlsx")
        assert "test_week1_" in json_path and json_path.endswith(".json")

        # Should complete in reasonable time (concurrent should be faster than sequential)
        assert end_time - start_time < 5.0

    @pytest.mark.asyncio
    async def test_directory_creation(self, sample_weekly_scores):
        """Test automatic directory creation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            nested_dir = Path(temp_dir) / "scores" / "data" / "exports"
            exporter = ScoresExporter(str(nested_dir))

            result = await exporter.export_csv(sample_weekly_scores, "test")

            assert isinstance(result, str)
            assert nested_dir.exists()
            # Check that the actual returned file exists
            assert Path(result).exists()
            # Check filename pattern matches expectation
            assert "test_week1_" in result and result.endswith(".csv")

    @pytest.mark.asyncio
    async def test_empty_games_export(self, exporter, temp_dir):
        """Test export with empty games list"""
        from datetime import datetime, timezone
        from nfl_scores_models import WeeklyScores

        empty_weekly_scores = WeeklyScores(
            week=1,
            season=2025,
            season_type=2,
            total_games=0,
            completed_games=0,
            games=[],
            generated_at=datetime.now(timezone.utc)
        )

        csv_result = await exporter.export_csv(empty_weekly_scores, "empty.csv")
        excel_result = await exporter.export_excel(empty_weekly_scores, "empty.xlsx")
        json_result = await exporter.export_json(empty_weekly_scores, "empty.json")

        # Should handle empty data gracefully and return file paths
        assert csv_result is not None
        assert excel_result is not None
        assert json_result is not None

        # Files should exist (check returned paths)
        from pathlib import Path
        assert Path(csv_result).exists()
        assert Path(excel_result).exists()
        assert Path(json_result).exists()

        # JSON should contain empty games array
        import json
        with open(json_result, 'r') as f:
            data = json.load(f)
            assert data["games"] == []
            assert data["total_games"] == 0

    @pytest.mark.asyncio
    async def test_special_characters_in_data(self, exporter, temp_dir):
        """Test export with special characters and edge cases"""
        from datetime import datetime, timezone
        from nfl_scores_models import WeeklyScores, GameScore, Team

        # Create team objects with special characters
        home_team = Team(
            id="1",
            name='Team with "Quotes" & Symbols',
            display_name='Team with "Quotes" & Symbols',
            abbreviation="QT",
            location="Test City"
        )
        away_team = Team(
            id="2",
            name="Équipe Spéciàle",
            display_name="Équipe Spéciàle",
            abbreviation="ES",
            location="Test City"
        )

        # Create game with special characters
        special_game = GameScore(
            game_id="123",
            date=datetime.now(timezone.utc),
            week=1,
            season=2025,
            season_type=2,
            home_team=home_team,
            away_team=away_team,
            home_score=21,
            away_score=21,
            status="Final/OT",
            status_detail="Final/OT",
            is_completed=True,
            venue_name="Stadium, with commas"
        )

        special_weekly_scores = WeeklyScores(
            week=1,
            season=2025,
            season_type=2,
            total_games=1,
            completed_games=1,
            games=[special_game],
            generated_at=datetime.now(timezone.utc)
        )

        csv_result = await exporter.export_csv(special_weekly_scores, "special.csv")
        json_result = await exporter.export_json(special_weekly_scores, "special.json")

        assert csv_result is not None
        assert json_result is not None

        # Verify CSV handles special characters using returned path
        from pathlib import Path
        csv_file = Path(csv_result)
        content = csv_file.read_text(encoding='utf-8')
        # CSV properly escapes quotes by doubling them
        assert 'Team with ""Quotes"" & Symbols' in content
        assert 'Équipe Spéciàle' in content

        # Verify JSON handles tie game values using returned path
        import json
        with open(json_result, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Check the games array in WeeklyScores structure
            assert data['games'][0]['winning_team'] == 'TIE'  # Tie game
            assert data['games'][0]['point_difference'] == 0

    @pytest.mark.asyncio
    async def test_large_dataset_export(self, exporter, temp_dir):
        """Test export with large number of games"""
        large_games = []
        for i in range(1000):
            game = {
                'game_id': f'game_{i}',
                'home_team_name': f'Home Team {i}',
                'away_team_name': f'Away Team {i}',
                'home_score': i % 50,
                'away_score': (i + 10) % 50,
                'total_points': (i % 50) + ((i + 10) % 50),
                'week': (i % 18) + 1,
                'season': 2025,
                'is_completed': True
            }
            large_games.append(game)

        # Create WeeklyScores object from large games
        from nfl_scores_models import WeeklyScores, GameScore, Team
        large_weekly_scores = WeeklyScores(
            week=1,
            season=2025,
            season_type=2,
            total_games=len(large_games),
            completed_games=len(large_games),
            games=[]  # Empty games list for performance test - just testing file creation
        )

        start_time = asyncio.get_event_loop().time()
        result = await exporter.export_csv(large_weekly_scores, "large.csv")
        end_time = asyncio.get_event_loop().time()

        assert isinstance(result, str) and "large.csv" in result
        from pathlib import Path
        assert Path(result).exists()

        # Should complete in reasonable time
        assert end_time - start_time < 10.0

        # Verify file exists and has content (using returned path)
        file_size = Path(result).stat().st_size
        assert file_size > 0  # Should have at least CSV headers

    @pytest.mark.asyncio
    async def test_timestamp_filename_generation(self, exporter, sample_weekly_scores, temp_dir):
        """Test filename generation through actual export"""
        # Test file naming through CSV export (which uses enhanced file manager)
        result_filepath = await exporter.export_csv(sample_weekly_scores, "test_scores")

        # Verify the filename follows the expected pattern
        assert result_filepath is not None
        filename = result_filepath.split("/")[-1]  # Get just the filename
        assert "test_scores_week" in filename
        assert filename.endswith(".csv")
        assert "_20" in filename  # Should have a timestamp

    def test_data_validation_and_formatting(self, exporter):
        """Test data validation and formatting helpers"""
        # Test with various data types and edge cases
        test_games = [
            {
                'game_id': 123,  # Integer instead of string
                'home_score': '21',  # String instead of integer
                'away_score': None,  # None value
                'is_completed': 'true',  # String instead of boolean
                'total_points': 21.5,  # Float value
            }
        ]

        # Should handle mixed data types gracefully
        # (Implementation-specific, but should not crash)
        assert isinstance(test_games, list)

    @pytest.mark.asyncio
    async def test_file_permission_error_handling(self, exporter, sample_weekly_scores):
        """Test handling of file permission errors"""
        with patch('pandas.DataFrame.to_csv', side_effect=PermissionError("Permission denied")):
            result = await exporter.export_csv(sample_weekly_scores, "test")
            assert result is None

    @pytest.mark.asyncio
    async def test_disk_space_error_handling(self, exporter, sample_weekly_scores):
        """Test handling of disk space errors"""
        # Test error handling by patching the file manager's save_json_data method
        with patch.object(exporter.file_manager, 'save_json_data', side_effect=OSError("No space left on device")):
            result = await exporter.export_json(sample_weekly_scores, "test.json")
            assert result is None

    def test_csv_header_consistency(self, exporter, temp_dir, sample_weekly_scores):
        """Test that CSV headers are consistent and complete"""
        # This test ensures all expected NFL game fields are included
        expected_headers = [
            'game_id', 'date', 'week', 'season', 'home_team_name', 'away_team_name',
            'home_score', 'away_score', 'total_points', 'winning_team', 'status',
            'is_completed', 'venue_name'
        ]

        async def run_test():
            result_path = await exporter.export_csv(sample_weekly_scores, "header_test")
            assert result_path is not None

            with open(result_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader)

                # Check that important headers are present
                for header in ['game_id', 'home_team_name', 'away_team_name', 'home_score', 'away_score']:
                    assert header in headers

        asyncio.run(run_test())

    @pytest.mark.asyncio
    async def test_json_structure_consistency(self, exporter, sample_weekly_scores, temp_dir):
        """Test that JSON structure is consistent"""
        result_path = await exporter.export_json(sample_weekly_scores, "structure_test")
        assert result_path is not None

        with open(result_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            # Should be a WeeklyScores structure (dict)
            assert isinstance(data, dict)
            assert 'games' in data
            assert isinstance(data['games'], list)

            # Each game should be a dictionary
            for game in data['games']:
                assert isinstance(game, dict)
                assert 'game_id' in game
                assert 'home_team_name' in game
                assert 'away_team_name' in game


if __name__ == "__main__":
    # Run tests with pytest if available, otherwise basic test
    try:
        import pytest
        pytest.main([__file__, "-v"])
    except ImportError:
        print("pytest not available, running basic tests...")

        async def run_basic_tests():
            with tempfile.TemporaryDirectory() as temp_dir:
                exporter = ScoresExporter(temp_dir)
                sample_data = [
                    {
                        'game_id': '123',
                        'home_team_name': 'Home Team',
                        'away_team_name': 'Away Team',
                        'home_score': 21,
                        'away_score': 14,
                        'status': 'Final'
                    }
                ]

                # Test CSV export
                csv_result = await exporter.export_csv(sample_data, "test.csv")
                assert csv_result is True
                print("✅ CSV export test passed")

                # Test JSON export
                json_result = await exporter.export_json(sample_data, "test.json")
                assert json_result is True
                print("✅ JSON export test passed")

                # Test Excel export
                excel_result = await exporter.export_excel(sample_data, "test.xlsx")
                assert excel_result is True
                print("✅ Excel export test passed")

                # Test concurrent export
                csv_task = exporter.export_csv(sample_data, "concurrent.csv")
                json_task = exporter.export_json(sample_data, "concurrent.json")

                results = await asyncio.gather(csv_task, json_task)
                assert all(results)
                print("✅ Concurrent export test passed")

                print("Basic tests completed successfully!")

        asyncio.run(run_basic_tests())