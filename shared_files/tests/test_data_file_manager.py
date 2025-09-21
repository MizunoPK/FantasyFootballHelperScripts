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
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch, MagicMock
import logging

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


if __name__ == '__main__':
    unittest.main()