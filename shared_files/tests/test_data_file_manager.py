#!/usr/bin/env python3
"""
Unit Tests for DataFileManager

Tests file cap enforcement, file deletion logic, and configuration validation.

Author: Generated for Fantasy Football Helper Scripts
Last Updated: September 2025
"""

import os
import tempfile
import unittest
import asyncio
import json
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch, MagicMock, AsyncMock, mock_open
import logging
import pandas as pd

# Set up the path for imports
import sys
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent))

from data_file_manager import DataFileManager, log_file_operation, enforce_caps_for_new_file


class TestDataFileManager(unittest.TestCase):
    """Test suite for DataFileManager functionality"""

    def setUp(self):
        """Set up test environment with temporary directory"""
        self.test_dir = tempfile.mkdtemp()
        self.test_caps = {'csv': 3, 'json': 2, 'xlsx': 1, 'txt': 2}
        self.manager = DataFileManager(self.test_dir, self.test_caps)

        # Disable logging for tests to reduce noise
        logging.getLogger().setLevel(logging.CRITICAL)

    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_manager_initialization(self):
        """Test DataFileManager initialization"""
        self.assertEqual(str(self.manager.data_folder), self.test_dir)
        self.assertEqual(self.manager.file_caps, self.test_caps)
        self.assertTrue(Path(self.test_dir).exists())

    def test_manager_initialization_with_defaults(self):
        """Test DataFileManager initialization with default caps"""
        with patch('shared_config.DEFAULT_FILE_CAPS', {'csv': 5, 'json': 5}):
            manager = DataFileManager(self.test_dir, None)
            self.assertEqual(manager.file_caps['csv'], 5)
            self.assertEqual(manager.file_caps['json'], 5)

    def test_validate_caps_valid_config(self):
        """Test configuration validation with valid caps"""
        errors = self.manager.validate_caps()
        self.assertEqual(len(errors), 0)

    def test_validate_caps_invalid_config(self):
        """Test configuration validation with invalid caps"""
        invalid_manager = DataFileManager(self.test_dir, {'csv': 'invalid', 123: 5, 'json': -1})
        errors = invalid_manager.validate_caps()
        self.assertGreater(len(errors), 0)
        self.assertTrue(any('must be integer' in error for error in errors))
        self.assertTrue(any('must be string' in error for error in errors))
        self.assertTrue(any('must be non-negative' in error for error in errors))

    def test_get_files_by_type_empty_directory(self):
        """Test getting files from empty directory"""
        files = self.manager.get_files_by_type('csv')
        self.assertEqual(len(files), 0)

    def test_get_files_by_type_with_files(self):
        """Test getting files when files exist"""
        # Create test files with different timestamps
        test_files = ['test1.csv', 'test2.csv', 'test3.csv']
        created_paths = []
        base_time = datetime.now()

        for i, filename in enumerate(test_files):
            filepath = Path(self.test_dir) / filename
            filepath.write_text(f"test content {i}")
            created_paths.append(filepath)

            # Modify file times to ensure predictable sorting (older files have earlier timestamps)
            timestamp = base_time - timedelta(hours=len(test_files) - i)
            mod_time = timestamp.timestamp()
            os.utime(filepath, (mod_time, mod_time))

        files = self.manager.get_files_by_type('csv')
        self.assertEqual(len(files), 3)

        # Should be sorted by modification time (oldest first)
        # test1.csv should be oldest (base_time - 3 hours)
        # test2.csv should be middle (base_time - 2 hours)
        # test3.csv should be newest (base_time - 1 hour)
        file_names = [f.name for f in files]
        self.assertEqual(file_names, ['test1.csv', 'test2.csv', 'test3.csv'])

    def test_get_file_counts(self):
        """Test getting file counts for all types"""
        # Create test files
        (Path(self.test_dir) / 'test1.csv').write_text("test")
        (Path(self.test_dir) / 'test2.csv').write_text("test")
        (Path(self.test_dir) / 'test1.json').write_text("test")
        (Path(self.test_dir) / 'test1.xlsx').write_text("test")

        counts = self.manager.get_file_counts()
        expected = {'csv': 2, 'json': 1, 'xlsx': 1, 'txt': 0}
        self.assertEqual(counts, expected)

    def test_delete_oldest_files(self):
        """Test deleting oldest files"""
        # Create test files
        test_files = ['old1.csv', 'old2.csv', 'new.csv']
        for i, filename in enumerate(test_files):
            filepath = Path(self.test_dir) / filename
            filepath.write_text(f"test content {i}")

            # Set different modification times
            timestamp = datetime.now() - timedelta(minutes=len(test_files) - i)
            mod_time = timestamp.timestamp()
            os.utime(filepath, (mod_time, mod_time))

        # Delete 2 oldest files
        deleted = self.manager.delete_oldest_files('csv', 2)
        self.assertEqual(len(deleted), 2)
        self.assertIn('old1.csv', deleted)
        self.assertIn('old2.csv', deleted)

        # Check remaining files
        remaining_files = self.manager.get_files_by_type('csv')
        self.assertEqual(len(remaining_files), 1)
        self.assertEqual(remaining_files[0].name, 'new.csv')

    @patch('shared_config.ENABLE_FILE_CAPS', False)
    def test_delete_oldest_files_caps_disabled(self):
        """Test that file deletion is skipped when caps are disabled"""
        # Create test files
        (Path(self.test_dir) / 'test1.csv').write_text("test")
        (Path(self.test_dir) / 'test2.csv').write_text("test")

        deleted = self.manager.delete_oldest_files('csv', 1)
        self.assertEqual(len(deleted), 0)

        # Files should still exist
        files = self.manager.get_files_by_type('csv')
        self.assertEqual(len(files), 2)

    @patch('shared_config.DRY_RUN_MODE', True)
    def test_delete_oldest_files_dry_run(self):
        """Test dry run mode doesn't actually delete files"""
        # Create test files
        (Path(self.test_dir) / 'test1.csv').write_text("test")
        (Path(self.test_dir) / 'test2.csv').write_text("test")

        deleted = self.manager.delete_oldest_files('csv', 1)
        self.assertEqual(len(deleted), 1)
        self.assertTrue(deleted[0].startswith('[DRY RUN]'))

        # Files should still exist
        files = self.manager.get_files_by_type('csv')
        self.assertEqual(len(files), 2)

    def test_enforce_file_caps_under_limit(self):
        """Test file cap enforcement when under limit"""
        # Create fewer files than the cap
        (Path(self.test_dir) / 'test1.csv').write_text("test")
        new_file = Path(self.test_dir) / 'test2.csv'
        new_file.write_text("test")

        deleted = self.manager.enforce_file_caps(str(new_file))
        self.assertEqual(len(deleted), 0)

        # All files should still exist
        files = self.manager.get_files_by_type('csv')
        self.assertEqual(len(files), 2)

    def test_enforce_file_caps_over_limit(self):
        """Test file cap enforcement when over limit"""
        # Create more files than the cap (cap is 3 for csv)
        for i in range(5):
            filepath = Path(self.test_dir) / f'test{i}.csv'
            filepath.write_text(f"test {i}")

            # Set different modification times
            timestamp = datetime.now() - timedelta(minutes=5 - i)
            mod_time = timestamp.timestamp()
            os.utime(filepath, (mod_time, mod_time))

        # Enforce caps on the newest file
        newest_file = Path(self.test_dir) / 'test4.csv'
        deleted = self.manager.enforce_file_caps(str(newest_file))

        # Should delete 2 files (5 - 3 = 2)
        self.assertIn('csv', deleted)
        self.assertEqual(len(deleted['csv']), 2)

        # Should have exactly 3 files remaining
        remaining_files = self.manager.get_files_by_type('csv')
        self.assertEqual(len(remaining_files), 3)

    def test_enforce_file_caps_unknown_extension(self):
        """Test file cap enforcement with unknown file extension"""
        new_file = Path(self.test_dir) / 'test.unknown'
        new_file.write_text("test")

        deleted = self.manager.enforce_file_caps(str(new_file))
        self.assertEqual(len(deleted), 0)

    def test_enforce_file_caps_disabled_extension(self):
        """Test file cap enforcement with disabled extension (cap = 0)"""
        disabled_manager = DataFileManager(self.test_dir, {'csv': 0})
        new_file = Path(self.test_dir) / 'test.csv'
        new_file.write_text("test")

        deleted = disabled_manager.enforce_file_caps(str(new_file))
        self.assertEqual(len(deleted), 0)

    @patch('shared_config.ENABLE_FILE_CAPS', False)
    def test_enforce_file_caps_globally_disabled(self):
        """Test file cap enforcement when globally disabled"""
        # Create files over the limit
        for i in range(5):
            (Path(self.test_dir) / f'test{i}.csv').write_text(f"test {i}")

        newest_file = Path(self.test_dir) / 'test4.csv'
        deleted = self.manager.enforce_file_caps(str(newest_file))
        self.assertEqual(len(deleted), 0)

    def test_cleanup_all_file_types(self):
        """Test cleanup across all configured file types"""
        # Create files exceeding caps for multiple types
        # CSV cap = 3, create 5 files
        for i in range(5):
            (Path(self.test_dir) / f'test{i}.csv').write_text(f"csv {i}")

        # JSON cap = 2, create 4 files
        for i in range(4):
            (Path(self.test_dir) / f'test{i}.json').write_text(f"json {i}")

        # XLSX cap = 1, create 3 files
        for i in range(3):
            (Path(self.test_dir) / f'test{i}.xlsx').write_text(f"xlsx {i}")

        deleted = self.manager.cleanup_all_file_types()

        # Check deletions
        self.assertIn('csv', deleted)
        self.assertIn('json', deleted)
        self.assertIn('xlsx', deleted)
        self.assertEqual(len(deleted['csv']), 2)  # 5 - 3 = 2
        self.assertEqual(len(deleted['json']), 2)  # 4 - 2 = 2
        self.assertEqual(len(deleted['xlsx']), 2)  # 3 - 1 = 2

        # Verify remaining counts
        counts = self.manager.get_file_counts()
        self.assertEqual(counts['csv'], 3)
        self.assertEqual(counts['json'], 2)
        self.assertEqual(counts['xlsx'], 1)

    def test_log_file_operation(self):
        """Test file operation logging"""
        with patch('data_file_manager.logger') as mock_logger:
            log_file_operation("TEST", "/path/to/file.csv", "additional info")
            mock_logger.info.assert_called_once()
            call_args = mock_logger.info.call_args[0][0]
            self.assertIn("TEST", call_args)
            self.assertIn("file.csv", call_args)
            self.assertIn("additional info", call_args)

    def test_enforce_caps_for_new_file_convenience_function(self):
        """Test the convenience function for enforcing caps"""
        # Create files over the limit
        for i in range(4):
            (Path(self.test_dir) / f'test{i}.csv').write_text(f"test {i}")

        new_file = Path(self.test_dir) / 'test3.csv'

        with patch('data_file_manager.DataFileManager') as mock_manager_class:
            mock_manager = MagicMock()
            mock_manager.enforce_file_caps.return_value = {'csv': ['test0.csv']}
            mock_manager_class.return_value = mock_manager

            deleted = enforce_caps_for_new_file(str(new_file), self.test_dir)

            mock_manager_class.assert_called_once_with(self.test_dir)
            mock_manager.enforce_file_caps.assert_called_once_with(str(new_file))
            self.assertEqual(deleted, {'csv': ['test0.csv']})

    def test_enforce_caps_for_new_file_auto_detect_folder(self):
        """Test convenience function with auto-detected folder"""
        new_file = Path(self.test_dir) / 'test.csv'
        new_file.write_text("test")

        with patch('data_file_manager.DataFileManager') as mock_manager_class:
            mock_manager = MagicMock()
            mock_manager.enforce_file_caps.return_value = {}
            mock_manager_class.return_value = mock_manager

            deleted = enforce_caps_for_new_file(str(new_file))

            # Should auto-detect parent directory
            expected_folder = new_file.parent
            mock_manager_class.assert_called_once_with(expected_folder)

    def test_file_manager_handles_permission_errors(self):
        """Test that file manager handles permission errors gracefully"""
        # Create test files
        for i in range(3):
            (Path(self.test_dir) / f'test{i}.csv').write_text(f"test {i}")

        # Mock file deletion to raise permission error
        with patch('pathlib.Path.unlink') as mock_unlink:
            mock_unlink.side_effect = PermissionError("Access denied")

            deleted = self.manager.delete_oldest_files('csv', 1)

            # Should handle error gracefully and return empty list
            self.assertEqual(len(deleted), 0)

    def test_file_manager_handles_missing_directory(self):
        """Test file manager with non-existent directory"""
        non_existent_dir = str(Path(self.test_dir) / "non_existent")
        manager = DataFileManager(non_existent_dir, self.test_caps)

        # Directory should be created
        self.assertTrue(Path(non_existent_dir).exists())

        # Should handle empty directory gracefully
        files = manager.get_files_by_type('csv')
        self.assertEqual(len(files), 0)

    def test_edge_case_zero_files_to_delete(self):
        """Test edge case where zero files need to be deleted"""
        (Path(self.test_dir) / 'test.csv').write_text("test")

        deleted = self.manager.delete_oldest_files('csv', 0)
        self.assertEqual(len(deleted), 0)

        # File should still exist
        files = self.manager.get_files_by_type('csv')
        self.assertEqual(len(files), 1)

    def test_edge_case_negative_files_to_delete(self):
        """Test edge case where negative files to delete is passed"""
        (Path(self.test_dir) / 'test.csv').write_text("test")

        deleted = self.manager.delete_oldest_files('csv', -1)
        self.assertEqual(len(deleted), 0)

        # File should still exist
        files = self.manager.get_files_by_type('csv')
        self.assertEqual(len(files), 1)


class TestEnhancedFilePatterns(unittest.TestCase):
    """Test cases for enhanced file pattern methods in DataFileManager"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.manager = DataFileManager(self.test_dir, {'csv': 3, 'json': 3, 'xlsx': 3, 'txt': 3})

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        try:
            shutil.rmtree(self.test_dir)
        except PermissionError:
            # Windows file locks - try again after brief delay
            import time
            time.sleep(0.1)
            try:
                shutil.rmtree(self.test_dir)
            except:
                pass  # Skip cleanup if still locked

    def test_generate_timestamped_filename(self):
        """Test timestamped filename generation"""
        filename = self.manager.generate_timestamped_filename('test', 'csv', include_time=True)

        # Should match pattern: test_YYYYMMDD_HHMMSS.csv
        self.assertTrue(filename.startswith('test_'))
        self.assertTrue(filename.endswith('.csv'))
        self.assertEqual(len(filename), len('test_YYYYMMDD_HHMMSS.csv'))

        # Test without time
        filename_no_time = self.manager.generate_timestamped_filename('test', 'json', include_time=False)
        self.assertTrue(filename_no_time.startswith('test_'))
        self.assertTrue(filename_no_time.endswith('.json'))
        self.assertEqual(len(filename_no_time), len('test_YYYYMMDD.json'))

    def test_get_timestamped_path(self):
        """Test timestamped path generation"""
        path = self.manager.get_timestamped_path('data', 'csv')

        self.assertIsInstance(path, Path)
        self.assertEqual(path.parent, Path(self.test_dir))
        self.assertTrue(path.name.startswith('data_'))
        self.assertTrue(path.name.endswith('.csv'))

    def test_get_latest_path(self):
        """Test latest file path generation"""
        path = self.manager.get_latest_path('players', 'json')

        self.assertIsInstance(path, Path)
        self.assertEqual(path.parent, Path(self.test_dir))
        self.assertEqual(path.name, 'players_latest.json')

    def test_save_dataframe_csv(self):
        """Test async CSV saving with DataFrame"""
        async def run_csv_test():
            with patch('pandas.DataFrame.to_csv') as mock_to_csv:
                df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

                timestamped_path, latest_path = await self.manager.save_dataframe_csv(df, 'test_data')

                # Check paths
                self.assertIsInstance(timestamped_path, Path)
                self.assertTrue(timestamped_path.name.startswith('test_data_'))
                self.assertTrue(timestamped_path.name.endswith('.csv'))

                self.assertIsInstance(latest_path, Path)
                self.assertEqual(latest_path.name, 'test_data_latest.csv')

                # Check that DataFrame.to_csv was called
                self.assertEqual(mock_to_csv.call_count, 2)  # Once for timestamped, once for latest

        asyncio.run(run_csv_test())

    def test_save_dataframe_excel(self):
        """Test async Excel saving with DataFrame"""
        async def run_excel_test():
            with patch('pandas.DataFrame.to_excel') as mock_to_excel:
                df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

                timestamped_path, latest_path = await self.manager.save_dataframe_excel(
                    df, 'test_data', sheet_name='TestSheet'
                )

                # Check paths
                self.assertTrue(timestamped_path.name.startswith('test_data_'))
                self.assertTrue(timestamped_path.name.endswith('.xlsx'))
                self.assertEqual(latest_path.name, 'test_data_latest.xlsx')

                # Check that DataFrame.to_excel was called
                self.assertEqual(mock_to_excel.call_count, 2)

        asyncio.run(run_excel_test())

    def test_save_json_data(self):
        """Test JSON saving"""
        with patch('builtins.open', mock_open()) as mock_file:
            test_data = {'key1': 'value1', 'key2': [1, 2, 3]}

            timestamped_path, latest_path = self.manager.save_json_data(test_data, 'test_json')

            # Check paths
            self.assertTrue(timestamped_path.name.startswith('test_json_'))
            self.assertTrue(timestamped_path.name.endswith('.json'))
            self.assertEqual(latest_path.name, 'test_json_latest.json')

            # Check that file open was called (once for timestamped, once for latest)
            self.assertEqual(mock_file.call_count, 2)

    def test_export_multi_format(self):
        """Test multi-format export functionality"""
        async def run_multi_format_test():
            with patch('pandas.DataFrame.to_csv') as mock_to_csv, \
                 patch('pandas.DataFrame.to_excel') as mock_to_excel, \
                 patch('builtins.open', mock_open()) as mock_file:

                df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

                results = await self.manager.export_multi_format(df, 'multi_test', formats=['csv', 'xlsx', 'json'])

                # Check that all formats were exported
                self.assertIn('csv', results)
                self.assertIn('xlsx', results)
                self.assertIn('json', results)

                # Check paths for each format
                for format_name, (timestamped_path, latest_path) in results.items():
                    self.assertTrue(timestamped_path.name.startswith('multi_test_'))
                    self.assertTrue(timestamped_path.name.endswith(f'.{format_name}'))
                    self.assertEqual(latest_path.name, f'multi_test_latest.{format_name}')

        asyncio.run(run_multi_format_test())

    def test_create_backup_copy(self):
        """Test backup file creation"""
        # Create a test file
        test_file = Path(self.test_dir) / 'test_original.csv'
        test_file.write_text("test,data\n1,2\n")

        backup_path = self.manager.create_backup_copy(test_file)

        # Check backup exists
        self.assertTrue(backup_path.exists())
        self.assertTrue(backup_path.name.startswith('test_original_backup_'))
        self.assertTrue(backup_path.name.endswith('.csv'))

        # Check content is the same
        self.assertEqual(backup_path.read_text(), test_file.read_text())

    def test_create_backup_copy_nonexistent_file(self):
        """Test backup creation for non-existent file"""
        nonexistent_file = Path(self.test_dir) / 'does_not_exist.csv'

        backup_path = self.manager.create_backup_copy(nonexistent_file)

        # Should return a backup path but file shouldn't exist
        self.assertFalse(backup_path.exists())
        self.assertTrue(backup_path.name.startswith('does_not_exist_backup_'))

    def test_cleanup_old_backups(self):
        """Test cleanup of old backup files"""
        # Create multiple backup files with different timestamps
        for i in range(5):
            backup_file = Path(self.test_dir) / f'test_backup_{i:02d}_20241001_120000.csv'
            backup_file.write_text(f"backup {i}")
            # Modify the timestamp to simulate different creation times
            timestamp = datetime.now().timestamp() - (i * 3600)  # 1 hour apart
            os.utime(backup_file, (timestamp, timestamp))

        # Keep only 3 most recent
        deleted_files = self.manager.cleanup_old_backups('test_backup_*.csv', keep_count=3)

        # Should delete 2 oldest files
        self.assertEqual(len(deleted_files), 2)

        # Check remaining files
        remaining_files = list(Path(self.test_dir).glob('test_backup_*.csv'))
        self.assertEqual(len(remaining_files), 3)

    def test_async_method_execution(self):
        """Test that async methods can be properly executed"""
        async def run_async_test():
            df = pd.DataFrame({'test': [1, 2, 3]})

            # This should not raise any exceptions
            with patch('pandas.DataFrame.to_csv'):
                timestamped_path, latest_path = await self.manager.save_dataframe_csv(df, 'async_test')
                self.assertIsNotNone(timestamped_path)
                self.assertIsNotNone(latest_path)

        # Run the async test
        asyncio.run(run_async_test())


if __name__ == '__main__':
    unittest.main()