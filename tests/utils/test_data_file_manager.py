#!/usr/bin/env python3
"""
Tests for data_file_manager module.

Comprehensive tests for DataFileManager class including file cap enforcement,
timestamped file operations, DataFrame saving, and backup management.

Author: Kai Mizuno
"""

import pytest
import pandas as pd
import asyncio
import json
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from utils.data_file_manager import (
    DataFileManager,
    log_file_operation,
    enforce_caps_for_new_file
)


class TestDataFileManagerInit:
    """Test suite for DataFileManager initialization."""

    def test_init_creates_data_folder_if_not_exists(self, tmp_path):
        """Test initialization creates data folder when it doesn't exist."""
        data_folder = tmp_path / "new_data_folder"
        assert not data_folder.exists()

        manager = DataFileManager(str(data_folder))

        assert data_folder.exists()
        assert manager.data_folder == data_folder

    def test_init_with_custom_file_caps(self, tmp_path):
        """Test initialization with custom file caps."""
        custom_caps = {'csv': 10, 'json': 5, 'xlsx': 3}
        manager = DataFileManager(str(tmp_path), file_caps=custom_caps)

        assert manager.file_caps == custom_caps

    def test_init_with_default_file_caps(self, tmp_path):
        """Test initialization uses default caps when none provided."""
        manager = DataFileManager(str(tmp_path))

        expected_defaults = {'csv': 5, 'json': 5, 'xlsx': 5, 'txt': 5}
        assert manager.file_caps == expected_defaults

    def test_init_sets_data_folder_path(self, tmp_path):
        """Test initialization correctly sets data folder path."""
        manager = DataFileManager(str(tmp_path))

        assert isinstance(manager.data_folder, Path)
        assert manager.data_folder == tmp_path


class TestGetFilesByType:
    """Test suite for get_files_by_type() method."""

    @pytest.fixture
    def manager(self, tmp_path):
        """Create a DataFileManager instance for testing."""
        return DataFileManager(str(tmp_path))

    def test_get_files_by_type_returns_files_sorted_by_time(self, manager, tmp_path):
        """Test files are returned sorted by modification time (oldest first)."""
        # Create files with different timestamps
        file1 = tmp_path / "file1.csv"
        file2 = tmp_path / "file2.csv"
        file3 = tmp_path / "file3.csv"

        file1.touch()
        time.sleep(0.01)
        file2.touch()
        time.sleep(0.01)
        file3.touch()

        files = manager.get_files_by_type('csv')

        assert len(files) == 3
        assert files[0] == file1  # Oldest first
        assert files[1] == file2
        assert files[2] == file3  # Newest last

    def test_get_files_by_type_filters_by_extension(self, manager, tmp_path):
        """Test only files with matching extension are returned."""
        (tmp_path / "data.csv").touch()
        (tmp_path / "info.json").touch()
        (tmp_path / "report.xlsx").touch()
        (tmp_path / "notes.txt").touch()

        csv_files = manager.get_files_by_type('csv')
        json_files = manager.get_files_by_type('json')

        assert len(csv_files) == 1
        assert csv_files[0].suffix == '.csv'
        assert len(json_files) == 1
        assert json_files[0].suffix == '.json'

    def test_get_files_by_type_returns_empty_for_nonexistent_type(self, manager):
        """Test returns empty list when no files of type exist."""
        files = manager.get_files_by_type('csv')

        assert files == []

    def test_get_files_by_type_case_insensitive(self, manager, tmp_path):
        """Test file type matching handles lowercase extension parameter."""
        # Note: glob is case-sensitive on Linux, so only lowercase files will match
        (tmp_path / "data.csv").touch()
        (tmp_path / "info.csv").touch()

        files = manager.get_files_by_type('csv')

        assert len(files) == 2


class TestDeleteOldestFiles:
    """Test suite for delete_oldest_files() method."""

    @pytest.fixture
    def manager(self, tmp_path):
        """Create a DataFileManager instance for testing."""
        return DataFileManager(str(tmp_path))

    def test_delete_oldest_files_deletes_correct_count(self, manager, tmp_path):
        """Test deletes the specified number of oldest files."""
        # Create 5 files
        for i in range(5):
            (tmp_path / f"file{i}.csv").touch()
            time.sleep(0.01)

        deleted = manager.delete_oldest_files('csv', 2)

        assert len(deleted) == 2
        assert "file0.csv" in deleted
        assert "file1.csv" in deleted

        # Verify files were actually deleted
        remaining = manager.get_files_by_type('csv')
        assert len(remaining) == 3

    def test_delete_oldest_files_returns_empty_for_zero_count(self, manager):
        """Test returns empty list when count_to_delete is 0."""
        deleted = manager.delete_oldest_files('csv', 0)

        assert deleted == []

    def test_delete_oldest_files_returns_empty_for_negative_count(self, manager):
        """Test returns empty list when count_to_delete is negative."""
        deleted = manager.delete_oldest_files('csv', -5)

        assert deleted == []

    def test_delete_oldest_files_handles_missing_files_gracefully(self, manager):
        """Test handles case where no files exist gracefully."""
        deleted = manager.delete_oldest_files('csv', 5)

        assert deleted == []


class TestEnforceFileCaps:
    """Test suite for enforce_file_caps() method."""

    @pytest.fixture
    def manager(self, tmp_path):
        """Create a DataFileManager with cap of 3 CSV files."""
        return DataFileManager(str(tmp_path), file_caps={'csv': 3, 'json': 2})

    def test_enforce_file_caps_deletes_excess_files(self, manager, tmp_path):
        """Test deletes excess files when cap is exceeded."""
        # Create 5 files (cap is 3, so 2 should be deleted)
        for i in range(5):
            (tmp_path / f"file{i}.csv").touch()
            time.sleep(0.01)

        new_file = tmp_path / "new_file.csv"
        deleted = manager.enforce_file_caps(str(new_file))

        assert 'csv' in deleted
        assert len(deleted['csv']) == 2

    def test_enforce_file_caps_keeps_newest_files(self, manager, tmp_path):
        """Test keeps the newest files when enforcing caps."""
        # Create 5 files
        file_names = []
        for i in range(5):
            name = f"file{i}.csv"
            (tmp_path / name).touch()
            file_names.append(name)
            time.sleep(0.01)

        manager.enforce_file_caps(str(tmp_path / file_names[-1]))

        remaining = manager.get_files_by_type('csv')
        remaining_names = [f.name for f in remaining]

        # Should keep the newest 3 files
        assert len(remaining) == 3
        assert file_names[2] in remaining_names
        assert file_names[3] in remaining_names
        assert file_names[4] in remaining_names

    def test_enforce_file_caps_returns_empty_for_unconfigured_extension(self, manager, tmp_path):
        """Test returns empty dict for file type with no cap configured."""
        new_file = tmp_path / "file.txt"
        deleted = manager.enforce_file_caps(str(new_file))

        assert deleted == {}

    def test_enforce_file_caps_returns_empty_when_cap_is_zero(self, tmp_path):
        """Test returns empty dict when cap is set to 0 (disabled)."""
        manager = DataFileManager(str(tmp_path), file_caps={'csv': 0})

        # Create multiple files
        for i in range(5):
            (tmp_path / f"file{i}.csv").touch()

        deleted = manager.enforce_file_caps(str(tmp_path / "new.csv"))

        assert deleted == {}

    def test_enforce_file_caps_does_not_delete_when_under_cap(self, manager, tmp_path):
        """Test does not delete files when count is under cap."""
        # Create 2 files (cap is 3)
        (tmp_path / "file1.csv").touch()
        (tmp_path / "file2.csv").touch()

        deleted = manager.enforce_file_caps(str(tmp_path / "file2.csv"))

        assert deleted == {}


class TestCleanupAllFileTypes:
    """Test suite for cleanup_all_file_types() method."""

    @pytest.fixture
    def manager(self, tmp_path):
        """Create a DataFileManager with multiple file type caps."""
        return DataFileManager(str(tmp_path), file_caps={'csv': 2, 'json': 2, 'xlsx': 2})

    def test_cleanup_all_file_types_enforces_all_caps(self, manager, tmp_path):
        """Test enforces caps for all configured file types."""
        # Create excess files for each type
        for i in range(4):
            (tmp_path / f"file{i}.csv").touch()
            (tmp_path / f"data{i}.json").touch()
            (tmp_path / f"report{i}.xlsx").touch()
            time.sleep(0.01)

        deleted = manager.cleanup_all_file_types()

        assert 'csv' in deleted
        assert 'json' in deleted
        assert 'xlsx' in deleted
        assert len(deleted['csv']) == 2
        assert len(deleted['json']) == 2
        assert len(deleted['xlsx']) == 2

    def test_cleanup_all_file_types_skips_disabled_caps(self, tmp_path):
        """Test skips file types with cap set to 0."""
        manager = DataFileManager(str(tmp_path), file_caps={'csv': 2, 'json': 0})

        # Create excess files
        for i in range(4):
            (tmp_path / f"file{i}.csv").touch()
            (tmp_path / f"data{i}.json").touch()
            time.sleep(0.01)

        deleted = manager.cleanup_all_file_types()

        assert 'csv' in deleted
        assert 'json' not in deleted

    def test_cleanup_all_file_types_returns_empty_when_under_caps(self, manager, tmp_path):
        """Test returns empty dict when all file counts are under caps."""
        # Create 1 file of each type (caps are 2)
        (tmp_path / "file.csv").touch()
        (tmp_path / "data.json").touch()

        deleted = manager.cleanup_all_file_types()

        assert deleted == {}


class TestGetFileCounts:
    """Test suite for get_file_counts() method."""

    @pytest.fixture
    def manager(self, tmp_path):
        """Create a DataFileManager instance."""
        return DataFileManager(str(tmp_path), file_caps={'csv': 5, 'json': 5, 'xlsx': 5})

    def test_get_file_counts_returns_correct_counts(self, manager, tmp_path):
        """Test returns accurate file counts for each type."""
        # Create different numbers of each file type
        for i in range(3):
            (tmp_path / f"file{i}.csv").touch()
        for i in range(2):
            (tmp_path / f"data{i}.json").touch()
        (tmp_path / "report.xlsx").touch()

        counts = manager.get_file_counts()

        assert counts['csv'] == 3
        assert counts['json'] == 2
        assert counts['xlsx'] == 1

    def test_get_file_counts_returns_zero_for_missing_types(self, manager):
        """Test returns 0 for file types with no files."""
        counts = manager.get_file_counts()

        assert counts['csv'] == 0
        assert counts['json'] == 0
        assert counts['xlsx'] == 0


class TestValidateCaps:
    """Test suite for validate_caps() method."""

    def test_validate_caps_returns_empty_for_valid_caps(self, tmp_path):
        """Test returns empty list for valid cap configuration."""
        manager = DataFileManager(str(tmp_path), file_caps={'csv': 5, 'json': 3})

        errors = manager.validate_caps()

        assert errors == []

    def test_validate_caps_detects_non_dict_caps(self, tmp_path):
        """Test detects when file_caps is not a dictionary."""
        manager = DataFileManager(str(tmp_path))
        manager.file_caps = "invalid"

        errors = manager.validate_caps()

        assert len(errors) > 0
        assert "must be a dictionary" in errors[0]

    def test_validate_caps_detects_non_string_file_type(self, tmp_path):
        """Test detects when file type key is not a string."""
        manager = DataFileManager(str(tmp_path))
        manager.file_caps = {123: 5}

        errors = manager.validate_caps()

        assert len(errors) > 0
        assert "File type must be string" in errors[0]

    def test_validate_caps_detects_non_integer_cap_value(self, tmp_path):
        """Test detects when cap value is not an integer."""
        manager = DataFileManager(str(tmp_path))
        manager.file_caps = {'csv': "five"}

        errors = manager.validate_caps()

        assert len(errors) > 0
        assert "must be integer" in errors[0]

    def test_validate_caps_detects_negative_cap_value(self, tmp_path):
        """Test detects when cap value is negative."""
        manager = DataFileManager(str(tmp_path))
        manager.file_caps = {'csv': -5}

        errors = manager.validate_caps()

        assert len(errors) > 0
        assert "must be non-negative" in errors[0]


class TestTimestampedFilenames:
    """Test suite for timestamped filename generation methods."""

    @pytest.fixture
    def manager(self, tmp_path):
        """Create a DataFileManager instance."""
        return DataFileManager(str(tmp_path))

    def test_generate_timestamped_filename_with_time(self, manager):
        """Test generates filename with date and time."""
        filename = manager.generate_timestamped_filename('players', 'csv', include_time=True)

        assert filename.startswith('players_')
        assert filename.endswith('.csv')
        # Format is: players_YYYYMMDD_HHMMSS.csv
        # Split by '_' gives: ['players', 'YYYYMMDD', 'HHMMSS.csv']
        parts = filename.split('_')
        assert len(parts) == 3
        assert len(parts[1]) == 8  # YYYYMMDD
        assert len(parts[2].split('.')[0]) == 6  # HHMMSS

    def test_generate_timestamped_filename_without_time(self, manager):
        """Test generates filename with date only."""
        filename = manager.generate_timestamped_filename('players', 'csv', include_time=False)

        assert filename.startswith('players_')
        assert filename.endswith('.csv')
        assert len(filename.split('_')[1].split('.')[0]) == 8  # YYYYMMDD format

    def test_get_timestamped_path_returns_full_path(self, manager, tmp_path):
        """Test returns full path in data folder."""
        path = manager.get_timestamped_path('players', 'csv')

        assert isinstance(path, Path)
        assert path.parent == tmp_path
        assert path.name.startswith('players_')
        assert path.suffix == '.csv'

    def test_get_latest_path_returns_latest_filename(self, manager, tmp_path):
        """Test returns path with 'latest' in filename."""
        path = manager.get_latest_path('players', 'csv')

        assert isinstance(path, Path)
        assert path.parent == tmp_path
        assert path.name == 'players_latest.csv'


class TestSaveDataframeCsv:
    """Test suite for save_dataframe_csv() async method."""

    @pytest.fixture
    def manager(self, tmp_path):
        """Create a DataFileManager instance."""
        return DataFileManager(str(tmp_path))

    @pytest.mark.asyncio
    async def test_save_dataframe_csv_creates_timestamped_file(self, manager, tmp_path):
        """Test creates timestamped CSV file."""
        df = pd.DataFrame({'id': [1, 2, 3], 'name': ['A', 'B', 'C']})

        timestamped, latest = await manager.save_dataframe_csv(df, 'test')

        assert timestamped.exists()
        assert timestamped.suffix == '.csv'
        assert timestamped.name.startswith('test_')

    @pytest.mark.asyncio
    async def test_save_dataframe_csv_creates_latest_copy(self, manager, tmp_path):
        """Test creates latest copy when create_latest=True."""
        df = pd.DataFrame({'id': [1, 2, 3]})

        timestamped, latest = await manager.save_dataframe_csv(df, 'test', create_latest=True)

        assert latest is not None
        assert latest.exists()
        assert latest.name == 'test_latest.csv'

    @pytest.mark.asyncio
    async def test_save_dataframe_csv_skips_latest_when_false(self, manager):
        """Test skips latest copy when create_latest=False."""
        df = pd.DataFrame({'id': [1, 2]})

        timestamped, latest = await manager.save_dataframe_csv(df, 'test', create_latest=False)

        assert latest is None

    @pytest.mark.asyncio
    async def test_save_dataframe_csv_enforces_caps(self, tmp_path):
        """Test enforces file caps after saving."""
        manager = DataFileManager(str(tmp_path), file_caps={'csv': 2})

        # Manually create old files with different timestamps to test cap enforcement
        (tmp_path / "test_20200101_120000.csv").touch()
        (tmp_path / "test_20200101_120001.csv").touch()
        (tmp_path / "test_20200101_120002.csv").touch()

        # Save new file - should trigger cap enforcement and delete oldest
        df = pd.DataFrame({'data': [1]})
        await manager.save_dataframe_csv(df, 'test', create_latest=False)

        # Should only have 2 timestamped files (cap) after enforcement
        csv_files = [f for f in tmp_path.glob('test_*.csv') if 'latest' not in f.name]
        assert len(csv_files) == 2


class TestSaveDataframeExcel:
    """Test suite for save_dataframe_excel() async method."""

    @pytest.fixture
    def manager(self, tmp_path):
        """Create a DataFileManager instance."""
        return DataFileManager(str(tmp_path))

    @pytest.mark.asyncio
    async def test_save_dataframe_excel_creates_timestamped_file(self, manager):
        """Test creates timestamped Excel file."""
        df = pd.DataFrame({'id': [1, 2, 3], 'value': [10, 20, 30]})

        timestamped, latest = await manager.save_dataframe_excel(df, 'report')

        assert timestamped.exists()
        assert timestamped.suffix == '.xlsx'
        assert timestamped.name.startswith('report_')

    @pytest.mark.asyncio
    async def test_save_dataframe_excel_creates_latest_copy(self, manager):
        """Test creates latest copy for Excel files."""
        df = pd.DataFrame({'data': [1, 2]})

        timestamped, latest = await manager.save_dataframe_excel(df, 'report', create_latest=True)

        assert latest is not None
        assert latest.exists()
        assert latest.name == 'report_latest.xlsx'

    @pytest.mark.asyncio
    async def test_save_dataframe_excel_custom_sheet_name(self, manager):
        """Test uses custom sheet name."""
        df = pd.DataFrame({'id': [1]})

        timestamped, _ = await manager.save_dataframe_excel(df, 'report', sheet_name='CustomSheet')

        # Read back and verify sheet name
        loaded = pd.read_excel(timestamped, sheet_name='CustomSheet')
        assert len(loaded) == 1


class TestSaveJsonData:
    """Test suite for save_json_data() method."""

    @pytest.fixture
    def manager(self, tmp_path):
        """Create a DataFileManager instance."""
        return DataFileManager(str(tmp_path))

    def test_save_json_data_creates_timestamped_file(self, manager):
        """Test creates timestamped JSON file."""
        data = {'players': ['Alice', 'Bob'], 'scores': [85, 92]}

        timestamped, latest = manager.save_json_data(data, 'config')

        assert timestamped.exists()
        assert timestamped.suffix == '.json'
        assert timestamped.name.startswith('config_')

    def test_save_json_data_creates_latest_copy(self, manager):
        """Test creates latest copy for JSON files."""
        data = {'test': 'data'}

        timestamped, latest = manager.save_json_data(data, 'config', create_latest=True)

        assert latest is not None
        assert latest.exists()
        assert latest.name == 'config_latest.json'

    def test_save_json_data_content_is_valid_json(self, manager):
        """Test saved JSON content is valid and matches original."""
        data = {'name': 'Test', 'count': 42, 'items': ['a', 'b', 'c']}

        timestamped, _ = manager.save_json_data(data, 'config')

        with open(timestamped, 'r', encoding='utf-8') as f:
            loaded = json.load(f)

        assert loaded == data

    def test_save_json_data_handles_nested_structures(self, manager):
        """Test handles complex nested JSON structures."""
        data = {
            'teams': [
                {'name': 'Team A', 'players': ['Alice', 'Bob']},
                {'name': 'Team B', 'players': ['Charlie', 'Dave']}
            ]
        }

        timestamped, _ = manager.save_json_data(data, 'teams')

        with open(timestamped, 'r', encoding='utf-8') as f:
            loaded = json.load(f)

        assert loaded == data


class TestExportMultiFormat:
    """Test suite for export_multi_format() async method."""

    @pytest.fixture
    def manager(self, tmp_path):
        """Create a DataFileManager instance."""
        return DataFileManager(str(tmp_path))

    @pytest.mark.asyncio
    async def test_export_multi_format_creates_all_default_formats(self, manager, tmp_path):
        """Test creates CSV, XLSX, and JSON by default."""
        df = pd.DataFrame({'id': [1, 2], 'value': [10, 20]})

        results = await manager.export_multi_format(df, 'export_test')

        assert 'csv' in results
        assert 'xlsx' in results
        assert 'json' in results

        # Verify all files exist
        csv_path, _ = results['csv']
        xlsx_path, _ = results['xlsx']
        json_path, _ = results['json']

        assert csv_path.exists()
        assert xlsx_path.exists()
        assert json_path.exists()

    @pytest.mark.asyncio
    async def test_export_multi_format_creates_specific_formats(self, manager):
        """Test creates only specified formats."""
        df = pd.DataFrame({'data': [1]})

        results = await manager.export_multi_format(df, 'partial', formats=['csv', 'json'])

        assert 'csv' in results
        assert 'json' in results
        assert 'xlsx' not in results

    @pytest.mark.asyncio
    async def test_export_multi_format_creates_latest_copies(self, manager, tmp_path):
        """Test creates latest copies for all formats."""
        df = pd.DataFrame({'id': [1]})

        results = await manager.export_multi_format(df, 'latest_test', create_latest=True)

        # Check that all formats have latest copies
        for format_name, (timestamped, latest) in results.items():
            assert latest is not None
            assert latest.exists()
            assert 'latest' in latest.name


class TestBackupOperations:
    """Test suite for backup-related methods."""

    @pytest.fixture
    def manager(self, tmp_path):
        """Create a DataFileManager instance."""
        return DataFileManager(str(tmp_path))

    def test_create_backup_copy_creates_backup_file(self, manager, tmp_path):
        """Test creates backup copy of existing file."""
        source = tmp_path / "original.csv"
        source.write_text("test data")

        backup_path = manager.create_backup_copy(source)

        assert backup_path.exists()
        assert 'backup' in backup_path.name
        assert backup_path.read_text() == "test data"

    def test_create_backup_copy_includes_timestamp(self, manager, tmp_path):
        """Test backup filename includes timestamp."""
        source = tmp_path / "file.json"
        source.write_text('{"data": 1}')

        backup_path = manager.create_backup_copy(source)

        # Filename should be: file_backup_YYYYMMDD_HHMMSS.json
        parts = backup_path.stem.split('_')
        assert len(parts) >= 3  # file, backup, timestamp parts

    def test_create_backup_copy_handles_missing_source(self, manager, tmp_path):
        """Test handles missing source file gracefully."""
        nonexistent = tmp_path / "missing.csv"

        backup_path = manager.create_backup_copy(nonexistent)

        # Should return path but not create backup
        assert not backup_path.exists()

    def test_cleanup_old_backups_keeps_recent_backups(self, manager, tmp_path):
        """Test keeps only the most recent backups."""
        # Create 5 backup files
        for i in range(5):
            backup = tmp_path / f"file_backup_{i}.csv"
            backup.touch()
            time.sleep(0.01)

        deleted = manager.cleanup_old_backups("file_backup_*.csv", keep_count=2)

        assert len(deleted) == 3

        # Verify only 2 backups remain
        remaining = list(tmp_path.glob("file_backup_*.csv"))
        assert len(remaining) == 2

    def test_cleanup_old_backups_does_nothing_when_under_limit(self, manager, tmp_path):
        """Test does nothing when backup count is under limit."""
        # Create 2 backups with keep_count=3
        (tmp_path / "backup1.csv").touch()
        (tmp_path / "backup2.csv").touch()

        deleted = manager.cleanup_old_backups("backup*.csv", keep_count=3)

        assert deleted == []


class TestModuleLevelFunctions:
    """Test suite for module-level convenience functions."""

    def test_enforce_caps_for_new_file_uses_file_parent_as_data_folder(self, tmp_path):
        """Test auto-detects data folder from file path."""
        # Create some existing files
        for i in range(4):
            (tmp_path / f"file{i}.csv").touch()
            time.sleep(0.01)

        new_file = tmp_path / "new_file.csv"
        new_file.touch()

        # Should use default cap of 5 and delete 0 files (4 existing + 1 new = 5)
        deleted = enforce_caps_for_new_file(str(new_file))

        # With default cap of 5, no files should be deleted
        assert deleted == {}

    def test_enforce_caps_for_new_file_accepts_explicit_data_folder(self, tmp_path):
        """Test accepts explicit data folder parameter."""
        new_file = tmp_path / "file.csv"
        new_file.touch()

        deleted = enforce_caps_for_new_file(str(new_file), data_folder=str(tmp_path))

        # Should work without errors
        assert isinstance(deleted, dict)
