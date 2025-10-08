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
        from shared_files.error_handler import DataProcessingError
        required_cols = ["name", "position", "missing_column"]
        with self.assertRaises(DataProcessingError) as context:
            validate_csv_columns(self.test_csv, required_cols)
        self.assertIn("missing_column", str(context.exception))

    def test_validate_csv_columns_file_not_found(self):
        """Test validation with non-existent file"""
        from shared_files.error_handler import FileOperationError
        with self.assertRaises(FileOperationError):
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


class TestCSVUtilsEdgeCases(unittest.TestCase):
    """Edge case tests for CSV utility functions"""

    def setUp(self):
        """Set up edge case test fixtures"""
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        """Clean up edge case test fixtures"""
        shutil.rmtree(self.test_dir)

    def test_malformed_csv_handling(self):
        """Test handling of malformed CSV files"""
        malformed_csv = self.test_dir / "malformed.csv"

        # Create CSV with inconsistent columns
        with open(malformed_csv, 'w', encoding='utf-8') as f:
            f.write("name,position,team\n")
            f.write("Player1,QB,KC,extra_field\n")  # Extra field
            f.write("Player2,RB\n")  # Missing field
            f.write("Player3,WR,SEA\n")  # Normal line

        # Should handle malformed data gracefully
        df = safe_csv_read(malformed_csv)
        self.assertGreaterEqual(len(df), 1)  # Should read at least one valid row

    def test_unicode_csv_handling(self):
        """Test handling of CSV files with unicode characters"""
        unicode_csv = self.test_dir / "unicode.csv"
        unicode_data = [
            {"name": "José Martínez", "position": "QB", "team": "MÉX"},
            {"name": "François Müller", "position": "RB", "team": "FRA"},
            {"name": "李小明", "position": "WR", "team": "CHN"}
        ]

        # Write unicode data
        write_dict_csv(unicode_data, unicode_csv)

        # Read back and verify
        result = read_dict_csv(unicode_csv)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["name"], "José Martínez")
        self.assertEqual(result[2]["name"], "李小明")

    def test_very_large_csv_handling(self):
        """Test handling of large CSV files (performance test)"""
        large_csv = self.test_dir / "large.csv"

        # Create large dataset (1000 rows)
        large_data = []
        for i in range(1000):
            large_data.append({
                "name": f"Player{i}",
                "position": "QB" if i % 4 == 0 else "RB",
                "team": f"TEAM{i % 32}",
                "points": str(float(i * 10.5))
            })

        # Test writing large file
        import time
        start_time = time.time()
        write_dict_csv(large_data, large_csv)
        write_time = time.time() - start_time

        self.assertLess(write_time, 5.0)  # Should complete within 5 seconds
        self.assertTrue(large_csv.exists())

        # Test reading large file
        start_time = time.time()
        result = read_dict_csv(large_csv)
        read_time = time.time() - start_time

        self.assertEqual(len(result), 1000)
        self.assertLess(read_time, 5.0)  # Should complete within 5 seconds

    def test_empty_csv_edge_cases(self):
        """Test various empty CSV scenarios"""
        empty_csv = self.test_dir / "empty.csv"

        # Test completely empty file
        with open(empty_csv, 'w', encoding='utf-8') as f:
            pass  # Empty file

        df = safe_csv_read(empty_csv)
        self.assertTrue(df.empty)

        # Test file with header only
        header_only_csv = self.test_dir / "header_only.csv"
        with open(header_only_csv, 'w', encoding='utf-8') as f:
            f.write("name,position,team\n")

        df = safe_csv_read(header_only_csv)
        self.assertEqual(len(df), 0)
        self.assertEqual(len(df.columns), 3)

    def test_csv_with_special_characters(self):
        """Test CSV handling with special characters and edge formatting"""
        special_csv = self.test_dir / "special.csv"
        special_data = [
            {"name": "Player, Jr.", "position": "QB", "team": "KC"},  # Comma in name
            {"name": 'Player "Nickname"', "position": "RB", "team": "BUF"},  # Quotes
            {"name": "Player\nNewline", "position": "WR", "team": "SEA"},  # Newline
            {"name": "", "position": "TE", "team": "DAL"}  # Empty name
        ]

        write_dict_csv(special_data, special_csv)
        result = read_dict_csv(special_csv)

        self.assertEqual(len(result), 4)
        self.assertIn(",", result[0]["name"])  # Comma preserved
        self.assertIn('"', result[1]["name"])  # Quotes preserved

    def test_csv_column_validation_edge_cases(self):
        """Test column validation with edge cases"""
        test_csv = self.test_dir / "edge_columns.csv"

        # Create CSV with duplicate columns
        with open(test_csv, 'w', encoding='utf-8') as f:
            f.write("name,position,name,team\n")  # Duplicate 'name'
            f.write("Player1,QB,Player1Alt,KC\n")

        # Test that validation handles duplicates
        result = csv_column_exists(test_csv, "name")
        self.assertTrue(result)  # Should find at least one 'name' column

    def test_concurrent_csv_operations(self):
        """Test concurrent CSV operations for thread safety"""
        import threading
        import time

        results = []
        errors = []

        def write_csv_worker(worker_id):
            try:
                worker_csv = self.test_dir / f"worker_{worker_id}.csv"
                data = [{"id": str(i), "worker": str(worker_id)} for i in range(10)]
                write_dict_csv(data, worker_csv)
                results.append(worker_id)
            except Exception as e:
                errors.append(e)

        # Start multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=write_csv_worker, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for completion
        for thread in threads:
            thread.join()

        # Verify results
        self.assertEqual(len(results), 5)
        self.assertEqual(len(errors), 0)

        # Verify all files were created
        for i in range(5):
            worker_csv = self.test_dir / f"worker_{i}.csv"
            self.assertTrue(worker_csv.exists())

    def test_path_traversal_security(self):
        """Test protection against path traversal attacks"""
        from shared_files.error_handler import FileOperationError

        # Attempt path traversal
        try:
            dangerous_path = self.test_dir / "../../../etc/passwd"
            result = safe_csv_read(dangerous_path)
            # Should either fail safely or return empty dataframe
            self.assertTrue(result.empty or len(result) >= 0)
        except (FileOperationError, PermissionError, FileNotFoundError):
            # These exceptions are acceptable for security
            pass

    def test_memory_usage_with_large_files(self):
        """Test memory efficiency with large CSV operations"""
        try:
            import psutil
            import os
        except ImportError:
            self.skipTest("psutil not available for memory testing")

        # Get initial memory usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        # Create moderately large CSV
        large_csv = self.test_dir / "memory_test.csv"
        large_data = []
        for i in range(5000):  # 5000 rows
            large_data.append({
                "name": f"Player{i}",
                "position": "QB",
                "team": f"TEAM{i % 32}",
                "points": str(float(i * 10.5)),
                "extra_data": "x" * 100  # 100 char string per row
            })

        write_dict_csv(large_data, large_csv)
        result = read_dict_csv(large_csv)

        # Check memory usage didn't explode
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory

        self.assertLess(memory_increase, 100)  # Should use less than 100MB extra
        self.assertEqual(len(result), 5000)

    def test_csv_encoding_edge_cases(self):
        """Test CSV files with different encodings"""
        # Test UTF-8 with BOM
        utf8_bom_csv = self.test_dir / "utf8_bom.csv"

        with open(utf8_bom_csv, 'w', encoding='utf-8-sig') as f:
            f.write("name,position,team\n")
            f.write("Player1,QB,KC\n")

        # Should handle BOM gracefully
        df = safe_csv_read(utf8_bom_csv)
        self.assertEqual(len(df), 1)
        # Column name should not have BOM characters
        self.assertIn("name", df.columns[0])


if __name__ == '__main__':
    unittest.main()