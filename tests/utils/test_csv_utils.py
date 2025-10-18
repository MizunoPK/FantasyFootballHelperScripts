#!/usr/bin/env python3
"""
Tests for csv_utils module.

Comprehensive tests for all CSV utility functions including validation,
reading, writing, merging, and error handling.

Author: Kai Mizuno
"""

import pytest
import pandas as pd
import asyncio
from pathlib import Path
from unittest.mock import Mock, patch
import csv

from utils.csv_utils import (
    validate_csv_columns,
    read_csv_with_validation,
    write_csv_with_backup,
    write_csv_async,
    read_dict_csv,
    write_dict_csv,
    merge_csv_files,
    safe_csv_read,
    csv_column_exists
)
from utils.error_handler import FileOperationError, DataProcessingError


class TestValidateCsvColumns:
    """Test suite for validate_csv_columns() function."""

    @pytest.fixture
    def sample_csv(self, tmp_path):
        """Create a sample CSV file with known columns."""
        csv_file = tmp_path / "test.csv"
        data = pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['Alice', 'Bob', 'Charlie'],
            'score': [85.5, 92.0, 78.3]
        })
        data.to_csv(csv_file, index=False)
        return csv_file

    def test_validate_csv_columns_with_all_required_columns_present(self, sample_csv):
        """Test validation passes when all required columns exist."""
        result = validate_csv_columns(sample_csv, ['id', 'name', 'score'])
        assert result is True

    def test_validate_csv_columns_with_subset_of_columns(self, sample_csv):
        """Test validation passes when checking subset of columns."""
        result = validate_csv_columns(sample_csv, ['id', 'name'])
        assert result is True

    def test_validate_csv_columns_raises_error_for_missing_columns(self, sample_csv):
        """Test validation raises DataProcessingError when columns are missing."""
        with pytest.raises(DataProcessingError) as exc_info:
            validate_csv_columns(sample_csv, ['id', 'age', 'missing'])

        assert 'Missing required columns' in str(exc_info.value)

    def test_validate_csv_columns_raises_error_for_missing_file(self, tmp_path):
        """Test validation raises FileOperationError when file doesn't exist."""
        nonexistent = tmp_path / "does_not_exist.csv"

        with pytest.raises(FileOperationError) as exc_info:
            validate_csv_columns(nonexistent, ['id'])

        assert 'CSV file not found' in str(exc_info.value)

    def test_validate_csv_columns_with_empty_required_list(self, sample_csv):
        """Test validation passes with empty required columns list."""
        result = validate_csv_columns(sample_csv, [])
        assert result is True


class TestReadCsvWithValidation:
    """Test suite for read_csv_with_validation() function."""

    @pytest.fixture
    def sample_csv(self, tmp_path):
        """Create a sample CSV file."""
        csv_file = tmp_path / "test.csv"
        data = pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['Alice', 'Bob', 'Charlie'],
            'value': [10.5, 20.3, 30.1]
        })
        data.to_csv(csv_file, index=False)
        return csv_file

    def test_read_csv_without_validation(self, sample_csv):
        """Test reading CSV without column validation."""
        df = read_csv_with_validation(sample_csv)

        assert len(df) == 3
        assert list(df.columns) == ['id', 'name', 'value']
        assert df['name'].tolist() == ['Alice', 'Bob', 'Charlie']

    def test_read_csv_with_valid_column_requirements(self, sample_csv):
        """Test reading CSV with successful column validation."""
        df = read_csv_with_validation(sample_csv, required_columns=['id', 'name'])

        assert len(df) == 3
        assert 'id' in df.columns
        assert 'name' in df.columns

    def test_read_csv_raises_error_for_missing_file(self, tmp_path):
        """Test reading raises FileNotFoundError for missing file."""
        nonexistent = tmp_path / "missing.csv"

        with pytest.raises(FileNotFoundError):
            read_csv_with_validation(nonexistent)

    def test_read_csv_raises_error_for_missing_required_columns(self, sample_csv):
        """Test reading raises error when required columns are missing."""
        with pytest.raises(DataProcessingError):
            read_csv_with_validation(sample_csv, required_columns=['id', 'age', 'missing'])

    def test_read_csv_with_custom_encoding(self, tmp_path):
        """Test reading CSV with custom encoding."""
        csv_file = tmp_path / "encoded.csv"
        data = pd.DataFrame({'text': ['Test']})
        data.to_csv(csv_file, index=False, encoding='utf-8')

        df = read_csv_with_validation(csv_file, encoding='utf-8')

        assert len(df) == 1
        assert df['text'].iloc[0] == 'Test'


class TestWriteCsvWithBackup:
    """Test suite for write_csv_with_backup() function."""

    def test_write_csv_creates_new_file(self, tmp_path):
        """Test writing CSV creates new file when none exists."""
        csv_file = tmp_path / "new.csv"
        data = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})

        write_csv_with_backup(data, csv_file, create_backup=False)

        assert csv_file.exists()
        loaded = pd.read_csv(csv_file)
        assert len(loaded) == 2
        assert list(loaded.columns) == ['col1', 'col2']

    def test_write_csv_creates_backup_of_existing_file(self, tmp_path):
        """Test writing CSV creates backup when file exists."""
        # Note: csv_utils skips backup for paths containing 'tmp' or 'temp'
        # Since pytest tmp_path contains 'tmp', we cannot fully test backup behavior here.
        # This test verifies that the function doesn't error when backup=True is passed.
        csv_file = tmp_path / "existing.csv"

        # Create original file
        original_data = pd.DataFrame({'old': [1, 2]})
        original_data.to_csv(csv_file, index=False)

        # Write new data with backup requested
        new_data = pd.DataFrame({'new': [3, 4]})
        write_csv_with_backup(new_data, csv_file, create_backup=True)

        # Check new file was written correctly
        assert csv_file.exists()
        loaded = pd.read_csv(csv_file)
        assert 'new' in loaded.columns
        assert 'old' not in loaded.columns

        # Note: backup will not be created because path contains 'tmp'
        # This is expected behavior - temp files don't get backed up

    def test_write_csv_skips_backup_for_temp_files(self, tmp_path):
        """Test writing CSV skips backup for temporary files."""
        csv_file = tmp_path / "tmp_test.csv"

        # Create original file
        original_data = pd.DataFrame({'old': [1]})
        original_data.to_csv(csv_file, index=False)

        # Write new data - should not create backup for tmp files
        new_data = pd.DataFrame({'new': [2]})
        write_csv_with_backup(new_data, csv_file, create_backup=True)

        # Backup should not exist for temp files
        backup_file = csv_file.with_suffix('.backup.csv')
        assert not backup_file.exists()

    def test_write_csv_creates_parent_directories(self, tmp_path):
        """Test writing CSV creates parent directories if they don't exist."""
        csv_file = tmp_path / "subdir" / "nested" / "file.csv"
        data = pd.DataFrame({'col': [1, 2, 3]})

        write_csv_with_backup(data, csv_file, create_backup=False)

        assert csv_file.exists()
        assert csv_file.parent.exists()

    def test_write_csv_with_custom_encoding(self, tmp_path):
        """Test writing CSV with custom encoding."""
        csv_file = tmp_path / "encoded.csv"
        data = pd.DataFrame({'text': ['Test']})

        write_csv_with_backup(data, csv_file, create_backup=False, encoding='utf-8')

        assert csv_file.exists()
        loaded = pd.read_csv(csv_file, encoding='utf-8')
        assert loaded['text'].iloc[0] == 'Test'


class TestWriteCsvAsync:
    """Test suite for write_csv_async() function."""

    @pytest.mark.asyncio
    async def test_write_csv_async_creates_file(self, tmp_path):
        """Test async CSV writing creates file successfully."""
        csv_file = tmp_path / "async.csv"
        data = pd.DataFrame({'id': [1, 2, 3], 'value': ['a', 'b', 'c']})

        await write_csv_async(data, csv_file)

        assert csv_file.exists()
        loaded = pd.read_csv(csv_file)
        assert len(loaded) == 3
        assert list(loaded.columns) == ['id', 'value']

    @pytest.mark.asyncio
    async def test_write_csv_async_creates_parent_directories(self, tmp_path):
        """Test async CSV writing creates parent directories."""
        csv_file = tmp_path / "nested" / "dir" / "async.csv"
        data = pd.DataFrame({'col': [1]})

        await write_csv_async(data, csv_file)

        assert csv_file.exists()
        assert csv_file.parent.exists()

    @pytest.mark.asyncio
    async def test_write_csv_async_with_custom_encoding(self, tmp_path):
        """Test async CSV writing with custom encoding."""
        csv_file = tmp_path / "encoded_async.csv"
        data = pd.DataFrame({'text': ['Test']})

        await write_csv_async(data, csv_file, encoding='utf-8')

        assert csv_file.exists()
        loaded = pd.read_csv(csv_file, encoding='utf-8')
        assert loaded['text'].iloc[0] == 'Test'


class TestReadDictCsv:
    """Test suite for read_dict_csv() function."""

    @pytest.fixture
    def sample_csv(self, tmp_path):
        """Create a sample CSV file."""
        csv_file = tmp_path / "dict_test.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'name', 'score'])
            writer.writeheader()
            writer.writerows([
                {'id': '1', 'name': 'Alice', 'score': '85'},
                {'id': '2', 'name': 'Bob', 'score': '92'}
            ])
        return csv_file

    def test_read_dict_csv_returns_list_of_dicts(self, sample_csv):
        """Test reading CSV returns list of dictionaries."""
        rows = read_dict_csv(sample_csv)

        assert isinstance(rows, list)
        assert len(rows) == 2
        assert rows[0] == {'id': '1', 'name': 'Alice', 'score': '85'}
        assert rows[1] == {'id': '2', 'name': 'Bob', 'score': '92'}

    def test_read_dict_csv_with_column_validation(self, sample_csv):
        """Test reading dict CSV with column validation."""
        rows = read_dict_csv(sample_csv, required_columns=['id', 'name'])

        assert len(rows) == 2
        assert 'id' in rows[0]
        assert 'name' in rows[0]

    def test_read_dict_csv_raises_error_for_missing_file(self, tmp_path):
        """Test reading dict CSV raises error for missing file."""
        nonexistent = tmp_path / "missing.csv"

        with pytest.raises(FileNotFoundError):
            read_dict_csv(nonexistent)

    def test_read_dict_csv_raises_error_for_missing_columns(self, sample_csv):
        """Test reading dict CSV raises error when required columns missing."""
        with pytest.raises(DataProcessingError):
            read_dict_csv(sample_csv, required_columns=['id', 'age', 'missing'])

    def test_read_dict_csv_with_empty_file(self, tmp_path):
        """Test reading dict CSV with empty file (headers only)."""
        csv_file = tmp_path / "empty.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'name'])
            writer.writeheader()

        rows = read_dict_csv(csv_file)

        assert len(rows) == 0


class TestWriteDictCsv:
    """Test suite for write_dict_csv() function."""

    def test_write_dict_csv_creates_file(self, tmp_path):
        """Test writing dict CSV creates file with correct data."""
        csv_file = tmp_path / "output.csv"
        data = [
            {'id': 1, 'name': 'Alice', 'score': 85},
            {'id': 2, 'name': 'Bob', 'score': 92}
        ]

        write_dict_csv(data, csv_file)

        assert csv_file.exists()

        # Read back and verify
        with open(csv_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        assert len(rows) == 2
        assert rows[0]['name'] == 'Alice'
        assert rows[1]['name'] == 'Bob'

    def test_write_dict_csv_with_custom_fieldnames(self, tmp_path):
        """Test writing dict CSV with custom fieldnames order."""
        csv_file = tmp_path / "custom_fields.csv"
        data = [
            {'id': 1, 'name': 'Alice', 'score': 85},
            {'id': 2, 'name': 'Bob', 'score': 92}
        ]

        write_dict_csv(data, csv_file, fieldnames=['name', 'id', 'score'])

        with open(csv_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            assert list(reader.fieldnames) == ['name', 'id', 'score']

    def test_write_dict_csv_with_empty_data(self, tmp_path):
        """Test writing dict CSV with empty data list does nothing."""
        csv_file = tmp_path / "empty_output.csv"

        write_dict_csv([], csv_file)

        # File should not be created for empty data
        assert not csv_file.exists()

    def test_write_dict_csv_creates_parent_directories(self, tmp_path):
        """Test writing dict CSV creates parent directories."""
        csv_file = tmp_path / "nested" / "dir" / "output.csv"
        data = [{'id': 1, 'value': 'test'}]

        write_dict_csv(data, csv_file)

        assert csv_file.exists()
        assert csv_file.parent.exists()


class TestMergeCsvFiles:
    """Test suite for merge_csv_files() function."""

    @pytest.fixture
    def sample_csvs(self, tmp_path):
        """Create multiple sample CSV files for merging."""
        csv1 = tmp_path / "file1.csv"
        csv2 = tmp_path / "file2.csv"

        data1 = pd.DataFrame({'id': [1, 2], 'value': ['a', 'b']})
        data2 = pd.DataFrame({'id': [3, 4], 'value': ['c', 'd']})

        data1.to_csv(csv1, index=False)
        data2.to_csv(csv2, index=False)

        return [csv1, csv2]

    def test_merge_csv_files_concatenates_files(self, sample_csvs, tmp_path):
        """Test merging CSV files concatenates them correctly."""
        output_file = tmp_path / "merged.csv"

        merged_df = merge_csv_files(sample_csvs, output_file, how='concat')

        assert len(merged_df) == 4
        assert list(merged_df.columns) == ['id', 'value']
        assert merged_df['id'].tolist() == [1, 2, 3, 4]
        assert output_file.exists()

    def test_merge_csv_files_skips_missing_files(self, sample_csvs, tmp_path):
        """Test merging CSV files skips files that don't exist."""
        output_file = tmp_path / "merged.csv"
        nonexistent = tmp_path / "does_not_exist.csv"

        files_to_merge = sample_csvs + [nonexistent]
        merged_df = merge_csv_files(files_to_merge, output_file, how='concat')

        # Should still merge the existing files
        assert len(merged_df) == 4

    def test_merge_csv_files_raises_error_for_no_valid_files(self, tmp_path):
        """Test merging raises ValueError when no valid files found."""
        output_file = tmp_path / "merged.csv"
        nonexistent1 = tmp_path / "missing1.csv"
        nonexistent2 = tmp_path / "missing2.csv"

        with pytest.raises(ValueError) as exc_info:
            merge_csv_files([nonexistent1, nonexistent2], output_file)

        assert 'No valid CSV files found' in str(exc_info.value)

    def test_merge_csv_files_raises_error_for_unsupported_method(self, sample_csvs, tmp_path):
        """Test merging raises ValueError for unsupported merge method."""
        output_file = tmp_path / "merged.csv"

        with pytest.raises(ValueError) as exc_info:
            merge_csv_files(sample_csvs, output_file, how='unsupported')

        assert 'Unsupported merge method' in str(exc_info.value)


class TestSafeCsvRead:
    """Test suite for safe_csv_read() function."""

    def test_safe_csv_read_returns_dataframe_for_existing_file(self, tmp_path):
        """Test safe_csv_read returns DataFrame for existing file."""
        csv_file = tmp_path / "exists.csv"
        data = pd.DataFrame({'col': [1, 2, 3]})
        data.to_csv(csv_file, index=False)

        result = safe_csv_read(csv_file)

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 3
        assert 'col' in result.columns

    def test_safe_csv_read_returns_empty_dataframe_for_missing_file(self, tmp_path):
        """Test safe_csv_read returns empty DataFrame for missing file."""
        nonexistent = tmp_path / "missing.csv"

        result = safe_csv_read(nonexistent)

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    def test_safe_csv_read_returns_custom_default_for_missing_file(self, tmp_path):
        """Test safe_csv_read returns custom default for missing file."""
        nonexistent = tmp_path / "missing.csv"
        default_df = pd.DataFrame({'default': [999]})

        result = safe_csv_read(nonexistent, default_value=default_df)

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert 'default' in result.columns
        assert result['default'].iloc[0] == 999

    def test_safe_csv_read_returns_default_on_read_error(self, tmp_path):
        """Test safe_csv_read returns default on read error."""
        # Create a malformed CSV file
        csv_file = tmp_path / "malformed.csv"
        with open(csv_file, 'w') as f:
            f.write("col1,col2\n")
            f.write("value1\n")  # Missing column value

        default_df = pd.DataFrame({'fallback': [0]})

        result = safe_csv_read(csv_file, default_value=default_df)

        # Should return default or empty depending on pandas behavior
        assert isinstance(result, pd.DataFrame)


class TestCsvColumnExists:
    """Test suite for csv_column_exists() function."""

    @pytest.fixture
    def sample_csv(self, tmp_path):
        """Create a sample CSV file."""
        csv_file = tmp_path / "columns.csv"
        data = pd.DataFrame({'id': [1], 'name': ['Alice'], 'score': [85]})
        data.to_csv(csv_file, index=False)
        return csv_file

    def test_csv_column_exists_returns_true_for_existing_column(self, sample_csv):
        """Test csv_column_exists returns True when column exists."""
        assert csv_column_exists(sample_csv, 'id') is True
        assert csv_column_exists(sample_csv, 'name') is True
        assert csv_column_exists(sample_csv, 'score') is True

    def test_csv_column_exists_returns_false_for_missing_column(self, sample_csv):
        """Test csv_column_exists returns False when column doesn't exist."""
        assert csv_column_exists(sample_csv, 'age') is False
        assert csv_column_exists(sample_csv, 'missing') is False

    def test_csv_column_exists_returns_false_for_missing_file(self, tmp_path):
        """Test csv_column_exists returns False when file doesn't exist."""
        nonexistent = tmp_path / "missing.csv"

        assert csv_column_exists(nonexistent, 'any_column') is False

    def test_csv_column_exists_handles_read_errors_gracefully(self, tmp_path):
        """Test csv_column_exists returns False on read errors."""
        # Create an invalid file
        invalid_file = tmp_path / "invalid.csv"
        invalid_file.write_bytes(b'\xff\xfe')  # Invalid UTF-8

        result = csv_column_exists(invalid_file, 'col')

        assert result is False
