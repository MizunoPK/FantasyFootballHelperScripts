"""
Unit Tests for Draft Order Simulation Script

Tests all functionality of the draft order simulation script including:
- Draft order file discovery
- DRAFT_ORDER loading from files
- Results aggregation and win percentage calculation
- JSON output format
- Error handling

Author: Kai Mizuno
Date: 2025
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import functions to test
from run_draft_order_simulation import (
    discover_draft_order_files,
    load_draft_order_from_file,
    run_simulation_for_draft_order,
    save_results_json
)


class TestDraftOrderFileDiscovery:
    """Test draft order file discovery logic"""

    def test_discovers_all_files(self, tmp_path):
        """Test that all JSON files are discovered and numbered correctly"""
        # Create mock draft order directory
        draft_order_dir = tmp_path / "draft_order_possibilities"
        draft_order_dir.mkdir()

        # Create test files with various naming patterns
        (draft_order_dir / "1.json").write_text('{"DRAFT_ORDER": []}')
        (draft_order_dir / "2_zero_rb.json").write_text('{"DRAFT_ORDER": []}')
        (draft_order_dir / "10_strategy.json").write_text('{"DRAFT_ORDER": []}')
        (draft_order_dir / "25_test.json").write_text('{"DRAFT_ORDER": []}')

        # Discover files
        file_numbers = discover_draft_order_files(draft_order_dir)

        # Verify
        assert len(file_numbers) == 4
        assert file_numbers == [1, 2, 10, 25]  # Should be sorted
        assert isinstance(file_numbers[0], int)

    def test_handles_missing_directory(self):
        """Test error handling when directory doesn't exist"""
        nonexistent_dir = Path("/nonexistent/directory")

        with pytest.raises(FileNotFoundError, match="Draft order directory not found"):
            discover_draft_order_files(nonexistent_dir)

    def test_extracts_file_numbers_correctly(self, tmp_path):
        """Test number extraction from both file patterns"""
        draft_order_dir = tmp_path / "draft_order_possibilities"
        draft_order_dir.mkdir()

        # Pattern 1: Just number
        (draft_order_dir / "5.json").write_text('{"DRAFT_ORDER": []}')
        # Pattern 2: Number with suffix
        (draft_order_dir / "42_hero_rb.json").write_text('{"DRAFT_ORDER": []}')

        file_numbers = discover_draft_order_files(draft_order_dir)

        assert 5 in file_numbers
        assert 42 in file_numbers

    def test_skips_files_without_numbers(self, tmp_path):
        """Test that files without leading numbers are skipped"""
        draft_order_dir = tmp_path / "draft_order_possibilities"
        draft_order_dir.mkdir()

        (draft_order_dir / "1.json").write_text('{"DRAFT_ORDER": []}')
        (draft_order_dir / "invalid_name.json").write_text('{"DRAFT_ORDER": []}')
        (draft_order_dir / "README.json").write_text('{"DRAFT_ORDER": []}')

        file_numbers = discover_draft_order_files(draft_order_dir)

        # Only file with leading number should be included
        assert len(file_numbers) == 1
        assert file_numbers == [1]

    def test_returns_sorted_list(self, tmp_path):
        """Test that file numbers are returned in sorted order"""
        draft_order_dir = tmp_path / "draft_order_possibilities"
        draft_order_dir.mkdir()

        # Create files in random order
        for num in [50, 1, 25, 10, 75]:
            (draft_order_dir / f"{num}.json").write_text('{"DRAFT_ORDER": []}')

        file_numbers = discover_draft_order_files(draft_order_dir)

        assert file_numbers == [1, 10, 25, 50, 75]


class TestDraftOrderLoading:
    """Test DRAFT_ORDER loading from files"""

    def test_loads_draft_order_from_numbered_file(self, tmp_path):
        """Test loading DRAFT_ORDER from file with just number"""
        draft_order_dir = tmp_path / "draft_order_possibilities"
        draft_order_dir.mkdir()

        draft_order = [{"FLEX": "P"}, {"QB": "P"}]
        (draft_order_dir / "1.json").write_text(json.dumps({"DRAFT_ORDER": draft_order}))

        result = load_draft_order_from_file(1, tmp_path)

        assert result == draft_order

    def test_loads_draft_order_from_named_file(self, tmp_path):
        """Test loading DRAFT_ORDER from file with suffix"""
        draft_order_dir = tmp_path / "draft_order_possibilities"
        draft_order_dir.mkdir()

        draft_order = [{"FLEX": "P"}, {"QB": "P"}]
        (draft_order_dir / "2_zero_rb.json").write_text(json.dumps({"DRAFT_ORDER": draft_order}))

        result = load_draft_order_from_file(2, tmp_path)

        assert result == draft_order

    def test_prefers_suffix_file_over_numbered(self, tmp_path):
        """Test that suffixed file is preferred when both patterns exist"""
        draft_order_dir = tmp_path / "draft_order_possibilities"
        draft_order_dir.mkdir()

        draft_order_numbered = [{"FLEX": "P"}]
        draft_order_suffixed = [{"QB": "P"}, {"FLEX": "P"}]

        (draft_order_dir / "3.json").write_text(json.dumps({"DRAFT_ORDER": draft_order_numbered}))
        (draft_order_dir / "3_strategy.json").write_text(json.dumps({"DRAFT_ORDER": draft_order_suffixed}))

        result = load_draft_order_from_file(3, tmp_path)

        # Should load from suffixed file first
        assert result == draft_order_suffixed

    def test_raises_error_for_missing_file(self, tmp_path):
        """Test error handling when file doesn't exist"""
        draft_order_dir = tmp_path / "draft_order_possibilities"
        draft_order_dir.mkdir()

        with pytest.raises(FileNotFoundError, match="No draft order file found for number 99"):
            load_draft_order_from_file(99, tmp_path)


class TestResultsAggregation:
    """Test results calculation and aggregation"""

    def test_calculates_win_percentage_correctly(self, tmp_path):
        """Test win percentage calculation"""
        # Setup mock baseline config
        baseline_config = {
            "config_name": "test",
            "parameters": {
                "DRAFT_ORDER": [],
                "DRAFT_ORDER_FILE": 1
            }
        }

        # Create mock draft order directory
        draft_order_dir = tmp_path / "draft_order_possibilities"
        draft_order_dir.mkdir()
        (draft_order_dir / "1.json").write_text(json.dumps({"DRAFT_ORDER": [{"FLEX": "P"}]}))

        # Create mock season folder
        season_folder = tmp_path / "2024"
        season_folder.mkdir()
        (season_folder / "weeks").mkdir()
        (season_folder / "weeks" / "week_01").mkdir()
        season_folders = [season_folder]

        # Mock ParallelLeagueRunner
        mock_runner = Mock()
        # Simulate week-by-week results: List[List[Tuple[week, won, points]]]
        # 10 wins, 7 losses across simulations
        mock_runner.run_simulations_for_config_with_weeks.return_value = [
            [(1, True, 100), (2, True, 110), (3, True, 105), (4, False, 95), (5, True, 120),
             (6, False, 90), (7, True, 115), (8, True, 108)],  # 6W-2L
            [(1, True, 102), (2, False, 88), (3, True, 107), (4, False, 91), (5, True, 118),
             (6, False, 85), (7, True, 112), (8, False, 80), (9, False, 78)]  # 4W-5L
        ]
        # Total: 10W-7L = 58.8% win rate

        file_num, win_pct, success = run_simulation_for_draft_order(
            1, baseline_config, 2, mock_runner, tmp_path, season_folders
        )

        assert success is True
        assert file_num == 1
        assert win_pct == 58.8  # (10/17) * 100 = 58.8%

    def test_handles_zero_games(self, tmp_path):
        """Test edge case where no games were played"""
        baseline_config = {
            "config_name": "test",
            "parameters": {
                "DRAFT_ORDER": [],
                "DRAFT_ORDER_FILE": 1
            }
        }

        draft_order_dir = tmp_path / "draft_order_possibilities"
        draft_order_dir.mkdir()
        (draft_order_dir / "1.json").write_text(json.dumps({"DRAFT_ORDER": [{"FLEX": "P"}]}))

        # Create mock season folder
        season_folder = tmp_path / "2024"
        season_folder.mkdir()
        (season_folder / "weeks").mkdir()
        (season_folder / "weeks" / "week_01").mkdir()
        season_folders = [season_folder]

        mock_runner = Mock()
        # No games played (shouldn't happen in practice, but handle gracefully)
        mock_runner.run_simulations_for_config_with_weeks.return_value = []

        file_num, win_pct, success = run_simulation_for_draft_order(
            1, baseline_config, 0, mock_runner, tmp_path, season_folders
        )

        assert success is True
        assert win_pct == 0.0  # Should handle division by zero

    def test_handles_simulation_failure(self, tmp_path):
        """Test error handling when simulation fails"""
        baseline_config = {
            "config_name": "test",
            "parameters": {
                "DRAFT_ORDER": [],
                "DRAFT_ORDER_FILE": 1
            }
        }

        draft_order_dir = tmp_path / "draft_order_possibilities"
        draft_order_dir.mkdir()
        (draft_order_dir / "1.json").write_text(json.dumps({"DRAFT_ORDER": [{"FLEX": "P"}]}))

        # Create mock season folder
        season_folder = tmp_path / "2024"
        season_folder.mkdir()
        (season_folder / "weeks").mkdir()
        (season_folder / "weeks" / "week_01").mkdir()
        season_folders = [season_folder]

        mock_runner = Mock()
        # Simulate failure
        mock_runner.run_simulations_for_config_with_weeks.side_effect = Exception("Simulation error")

        file_num, win_pct, success = run_simulation_for_draft_order(
            1, baseline_config, 2, mock_runner, tmp_path, season_folders
        )

        assert success is False
        assert win_pct == 0.0
        assert file_num == 1

    def test_rounds_to_one_decimal_place(self, tmp_path):
        """Test that win percentage is rounded to 1 decimal place"""
        baseline_config = {
            "config_name": "test",
            "parameters": {
                "DRAFT_ORDER": [],
                "DRAFT_ORDER_FILE": 1
            }
        }

        draft_order_dir = tmp_path / "draft_order_possibilities"
        draft_order_dir.mkdir()
        (draft_order_dir / "1.json").write_text(json.dumps({"DRAFT_ORDER": [{"FLEX": "P"}]}))

        # Create mock season folder
        season_folder = tmp_path / "2024"
        season_folder.mkdir()
        (season_folder / "weeks").mkdir()
        (season_folder / "weeks" / "week_01").mkdir()
        season_folders = [season_folder]

        mock_runner = Mock()
        # 2 wins, 1 loss = 66.666...%
        mock_runner.run_simulations_for_config_with_weeks.return_value = [
            [(1, True, 100), (2, True, 110), (3, False, 95)]  # 2W-1L
        ]

        file_num, win_pct, success = run_simulation_for_draft_order(
            1, baseline_config, 1, mock_runner, tmp_path, season_folders
        )

        assert win_pct == 66.7  # Should be rounded to 1 decimal


class TestJSONOutput:
    """Test JSON output format"""

    def test_saves_correct_format(self, tmp_path):
        """Test that JSON is saved in the correct format"""
        results = {"1": 70.2, "2": 80.1, "3": 65.5}
        metadata = {
            "timestamp": "2025-11-24 12:34:56",
            "num_simulations_per_file": 15,
            "total_files_tested": 3,
            "baseline_config": "test_config.json"
        }

        output_file = save_results_json(results, metadata, tmp_path)

        # Verify file was created
        assert output_file.exists()
        assert output_file.suffix == ".json"

        # Load and verify contents
        with open(output_file, 'r') as f:
            data = json.load(f)

        assert "metadata" in data
        assert "results" in data
        assert data["metadata"]["timestamp"] == "2025-11-24 12:34:56"
        assert data["results"] == results

    def test_creates_output_directory(self, tmp_path):
        """Test that output directory is created if it doesn't exist"""
        output_dir = tmp_path / "new" / "nested" / "directory"
        results = {"1": 70.2}
        metadata = {"timestamp": "2025-11-24 12:34:56"}

        # Directory shouldn't exist yet
        assert not output_dir.exists()

        output_file = save_results_json(results, metadata, output_dir)

        # Directory should now exist
        assert output_dir.exists()
        assert output_file.exists()

    def test_filename_includes_timestamp(self, tmp_path):
        """Test that filename includes timestamp"""
        results = {"1": 70.2}
        metadata = {"timestamp": "2025-11-24 12:34:56"}

        output_file = save_results_json(results, metadata, tmp_path)

        # Filename should match pattern: draft_order_win_rates_YYYYMMDD_HHMMSS.json
        assert output_file.name.startswith("draft_order_win_rates_")
        assert output_file.name.endswith(".json")
        # draft_order_win_rates_20251124_111013.json = 42 characters
        assert len(output_file.name) == 42  # Fixed length with timestamp

    def test_json_is_formatted_with_indent(self, tmp_path):
        """Test that JSON is formatted with indentation for readability"""
        results = {"1": 70.2, "2": 80.1}
        metadata = {"timestamp": "2025-11-24 12:34:56"}

        output_file = save_results_json(results, metadata, tmp_path)

        # Read raw contents
        with open(output_file, 'r') as f:
            contents = f.read()

        # Should have newlines and indentation (not single line)
        assert "\n" in contents
        assert "  " in contents  # 2-space indent


class TestIntegration:
    """Integration tests for complete workflows"""

    def test_complete_workflow_with_mock_runner(self, tmp_path):
        """Test complete workflow from discovery to JSON output"""
        # Setup
        draft_order_dir = tmp_path / "draft_order_possibilities"
        draft_order_dir.mkdir()

        # Create mock files
        for i in [1, 2, 3]:
            draft_order = [{"FLEX": "P"}] * 15
            (draft_order_dir / f"{i}.json").write_text(json.dumps({"DRAFT_ORDER": draft_order}))

        # Create mock season folder
        season_folder = tmp_path / "2024"
        season_folder.mkdir()
        (season_folder / "weeks").mkdir()
        (season_folder / "weeks" / "week_01").mkdir()
        season_folders = [season_folder]

        # Discover files
        file_numbers = discover_draft_order_files(draft_order_dir)
        assert len(file_numbers) == 3

        # Mock simulation - week-by-week results
        mock_runner = Mock()
        mock_runner.run_simulations_for_config_with_weeks.return_value = [
            [(1, True, 100), (2, True, 110), (3, False, 95), (4, True, 105),
             (5, False, 90), (6, True, 115), (7, True, 108), (8, False, 85),
             (9, True, 120), (10, True, 112)]  # 7W-3L = 70%
        ]

        baseline_config = {
            "config_name": "test",
            "parameters": {"DRAFT_ORDER": [], "DRAFT_ORDER_FILE": 1}
        }

        # Run simulations
        results = {}
        for file_num in file_numbers:
            file_num, win_pct, success = run_simulation_for_draft_order(
                file_num, baseline_config, 1, mock_runner, tmp_path, season_folders
            )
            if success:
                results[str(file_num)] = win_pct

        # Save results
        metadata = {
            "timestamp": "2025-11-24 12:34:56",
            "num_simulations_per_file": 1,
            "total_files_tested": 3
        }
        output_file = save_results_json(results, metadata, tmp_path)

        # Verify complete workflow
        assert len(results) == 3
        assert output_file.exists()

        with open(output_file, 'r') as f:
            data = json.load(f)

        assert data["metadata"]["total_files_tested"] == 3
        assert len(data["results"]) == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
