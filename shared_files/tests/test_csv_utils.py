#!/usr/bin/env python3
"""
Unit tests for CSV utilities module

Tests common CSV operations and error handling patterns.

Author: Kai Mizuno
Last Updated: September 2025
"""

import unittest
import tempfile
import shutil
import pandas as pd
import csv
from pathlib import Path
from unittest.mock import patch, mock_open
import asyncio

from shared_files.csv_utils import (
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


class TestCSVUtils(unittest.TestCase):
    """Test cases for CSV utility functions"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.test_csv = self.test_dir / "test.csv"

        # Create test CSV data
        self.test_data = [
            {"name": "Player1", "position": "QB", "team": "KC", "points": "100.5"},
            {"name": "Player2", "position": "RB", "team": "BUF", "points": "85.2"},
            {"name": "Player3", "position": "WR", "team": "SEA", "points": "92.8"}
        ]

        # Write test CSV
        with open(self.test_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["name", "position", "team", "points"])
            writer.writeheader()
            writer.writerows(self.test_data)

    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.test_dir)

    def test_validate_csv_columns_success(self):
        """Test successful column validation"""
        required_cols = ["name", "position", "team"]
        result = validate_csv_columns(self.test_csv, required_cols)
        self.assertTrue(result)

    def test_validate_csv_columns_missing(self):
        """Test validation with missing columns"""
        required_cols = ["name", "position", "missing_column"]
        with self.assertRaises(ValueError) as context:
            validate_csv_columns(self.test_csv, required_cols)
        self.assertIn("missing_column", str(context.exception))

    def test_validate_csv_columns_file_not_found(self):
        """Test validation with non-existent file"""
        with self.assertRaises(FileNotFoundError):
            validate_csv_columns(self.test_dir / "nonexistent.csv", ["name"])

    def test_read_csv_with_validation_success(self):
        """Test successful CSV reading with validation"""
        required_cols = ["name", "position"]
        df = read_csv_with_validation(self.test_csv, required_cols)

        self.assertEqual(len(df), 3)
        self.assertIn("name", df.columns)
        self.assertIn("position", df.columns)
        self.assertEqual(df.iloc[0]["name"], "Player1")

    def test_read_csv_with_validation_no_requirements(self):
        """Test CSV reading without column requirements"""
        df = read_csv_with_validation(self.test_csv)
        self.assertEqual(len(df), 3)
        self.assertEqual(len(df.columns), 4)

    def test_read_csv_with_validation_file_not_found(self):
        """Test CSV reading with non-existent file"""
        with self.assertRaises(FileNotFoundError):
            read_csv_with_validation(self.test_dir / "nonexistent.csv")

    def test_write_csv_with_backup_new_file(self):
        """Test writing CSV to new file"""
        df = pd.DataFrame(self.test_data)
        output_file = self.test_dir / "output.csv"

        write_csv_with_backup(df, output_file)

        self.assertTrue(output_file.exists())
        written_df = pd.read_csv(output_file)
        self.assertEqual(len(written_df), 3)

    def test_write_csv_with_backup_existing_file(self):
        """Test writing CSV with backup of existing file"""
        # Create initial file (use regular directory to avoid temp file detection)
        import os
        regular_dir = Path(os.getcwd()) / "test_backup_dir"
        regular_dir.mkdir(exist_ok=True)

        df1 = pd.DataFrame([{"col1": "value1"}])
        output_file = regular_dir / "backup_test.csv"
        df1.to_csv(output_file, index=False)

        # Write new data with backup
        df2 = pd.DataFrame(self.test_data)
        write_csv_with_backup(df2, output_file, create_backup=True)

        # Check backup was created
        backup_file = regular_dir / "backup_test.backup.csv"
        self.assertTrue(backup_file.exists())

        # Check new data was written
        written_df = pd.read_csv(output_file)
        self.assertEqual(len(written_df), 3)

        # Cleanup
        backup_file.unlink(missing_ok=True)
        output_file.unlink(missing_ok=True)
        regular_dir.rmdir()

    def test_write_csv_async(self):
        """Test async CSV writing"""
        async def test_async_write():
            df = pd.DataFrame(self.test_data)
            output_file = self.test_dir / "async_output.csv"

            await write_csv_async(df, output_file)

            self.assertTrue(output_file.exists())
            written_df = pd.read_csv(output_file)
            self.assertEqual(len(written_df), 3)

        # Run async test
        asyncio.run(test_async_write())

    def test_read_dict_csv_success(self):
        """Test reading CSV as list of dictionaries"""
        result = read_dict_csv(self.test_csv)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["name"], "Player1")
        self.assertEqual(result[1]["position"], "RB")

    def test_read_dict_csv_with_validation(self):
        """Test reading CSV as dictionaries with validation"""
        required_cols = ["name", "team"]
        result = read_dict_csv(self.test_csv, required_cols)

        self.assertEqual(len(result), 3)
        self.assertIn("name", result[0])
        self.assertIn("team", result[0])

    def test_write_dict_csv(self):
        """Test writing list of dictionaries to CSV"""
        output_file = self.test_dir / "dict_output.csv"

        write_dict_csv(self.test_data, output_file)

        self.assertTrue(output_file.exists())

        # Read back and verify
        with open(output_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["name"], "Player1")

    def test_write_dict_csv_empty_data(self):
        """Test writing empty data to CSV"""
        output_file = self.test_dir / "empty_output.csv"

        write_dict_csv([], output_file)

        # Should not create file for empty data
        self.assertFalse(output_file.exists())

    def test_merge_csv_files(self):
        """Test merging multiple CSV files"""
        # Create second CSV file
        csv2_data = [
            {"name": "Player4", "position": "TE", "team": "DAL", "points": "75.3"},
            {"name": "Player5", "position": "K", "team": "NE", "points": "55.1"}
        ]
        csv2_file = self.test_dir / "test2.csv"

        with open(csv2_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["name", "position", "team", "points"])
            writer.writeheader()
            writer.writerows(csv2_data)

        # Merge files
        output_file = self.test_dir / "merged.csv"
        result_df = merge_csv_files([self.test_csv, csv2_file], output_file)

        self.assertEqual(len(result_df), 5)  # 3 + 2 rows
        self.assertTrue(output_file.exists())

    def test_merge_csv_files_missing_file(self):
        """Test merging with some missing files"""
        nonexistent_file = self.test_dir / "nonexistent.csv"
        output_file = self.test_dir / "merged_partial.csv"

        result_df = merge_csv_files([self.test_csv, nonexistent_file], output_file)

        self.assertEqual(len(result_df), 3)  # Only from existing file
        self.assertTrue(output_file.exists())

    def test_safe_csv_read_existing_file(self):
        """Test safe reading of existing file"""
        df = safe_csv_read(self.test_csv)

        self.assertEqual(len(df), 3)
        self.assertIn("name", df.columns)

    def test_safe_csv_read_nonexistent_file(self):
        """Test safe reading of non-existent file"""
        df = safe_csv_read(self.test_dir / "nonexistent.csv")

        self.assertTrue(df.empty)
        self.assertEqual(len(df), 0)

    def test_safe_csv_read_with_default(self):
        """Test safe reading with custom default value"""
        default_df = pd.DataFrame({"default": ["value"]})
        df = safe_csv_read(self.test_dir / "nonexistent.csv", default_df)

        self.assertEqual(len(df), 1)
        self.assertIn("default", df.columns)

    def test_csv_column_exists_true(self):
        """Test column existence check for existing column"""
        result = csv_column_exists(self.test_csv, "name")
        self.assertTrue(result)

    def test_csv_column_exists_false(self):
        """Test column existence check for non-existing column"""
        result = csv_column_exists(self.test_csv, "nonexistent_column")
        self.assertFalse(result)

    def test_csv_column_exists_nonexistent_file(self):
        """Test column existence check for non-existent file"""
        result = csv_column_exists(self.test_dir / "nonexistent.csv", "name")
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()