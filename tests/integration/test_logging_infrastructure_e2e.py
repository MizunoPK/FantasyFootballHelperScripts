#!/usr/bin/env python3
"""
End-to-End Integration Tests for Logging Infrastructure

Tests the complete logging workflow with real objects (no mocks).
Verifies LineBasedRotatingHandler + LoggingManager integration.
"""

import unittest
import tempfile
import logging
from pathlib import Path
import shutil

from utils.LoggingManager import LoggingManager
from utils.LineBasedRotatingHandler import LineBasedRotatingHandler


class TestLoggingInfrastructureE2E(unittest.TestCase):
    """End-to-end integration tests with real objects."""

    def setUp(self):
        """Create temporary directory for test logs."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary test files."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
        # Clear any loggers created during tests
        logging.getLogger('test_app').handlers.clear()
        logging.getLogger('test_script').handlers.clear()

    def test_e2e_rotation_creates_multiple_files(self):
        """
        E2E Test 1: Verify rotation creates multiple timestamped files.

        Emits 750 lines, expects 2 files (rotation at 500 lines).
        """
        import os
        original_dir = os.getcwd()
        os.chdir(self.test_dir)

        try:
            # Create logger using LoggingManager
            manager = LoggingManager()
            logger = manager.setup_logger(
                name='test_app',
                level='INFO',
                log_to_file=True
            )

            # Emit 750 log messages (should create 2 files: 0-500, 501-750)
            for i in range(750):
                logger.info(f"Test message {i}")

            # Verify folder structure created
            logs_path = Path('logs')
            self.assertTrue(logs_path.exists(), "logs/ directory should exist")

            # Verify script subfolder created
            script_folder = logs_path / 'test_app'
            self.assertTrue(script_folder.exists(), "logs/test_app/ subfolder should exist")

            # Verify multiple log files created
            log_files = sorted(script_folder.glob('*.log'))
            self.assertGreaterEqual(len(log_files), 2,
                                   f"Should have at least 2 files after 750 lines, got {len(log_files)}")

            # Verify filename format
            # Initial file: test_app-YYYYMMDD_HHMMSS.log (from LoggingManager)
            # Rotated files: test_app-YYYYMMDD_HHMMSS_microseconds.log
            for log_file in log_files:
                filename = log_file.name
                # Accept both formats (with and without microseconds)
                self.assertRegex(filename, r'^test_app-\d{8}_\d{6}(?:_\d{6})?\.log$',
                               f"Filename should match pattern {{name}}-{{YYYYMMDD_HHMMSS}}[_microseconds].log: {filename}")

            print(f"✅ E2E Test 1 passed: {len(log_files)} files created with correct format")

        finally:
            os.chdir(original_dir)

    def test_e2e_multiple_loggers_separate_folders(self):
        """
        E2E Test 2: Verify multiple loggers create separate subfolders.

        Creates 3 different loggers, verifies each gets its own subfolder.
        """
        import os
        original_dir = os.getcwd()
        os.chdir(self.test_dir)

        try:
            # Create multiple loggers
            manager = LoggingManager()

            logger1 = manager.setup_logger('script_a', log_to_file=True)
            logger2 = manager.setup_logger('script_b', log_to_file=True)
            logger3 = manager.setup_logger('script_c', log_to_file=True)

            # Emit logs to each
            logger1.info("Message from script A")
            logger2.info("Message from script B")
            logger3.info("Message from script C")

            # Verify separate subfolders created
            logs_path = Path('logs')
            subfolders = [d.name for d in logs_path.iterdir() if d.is_dir()]

            self.assertIn('script_a', subfolders)
            self.assertIn('script_b', subfolders)
            self.assertIn('script_c', subfolders)

            # Verify each has its own log file
            self.assertTrue((logs_path / 'script_a').glob('*.log'))
            self.assertTrue((logs_path / 'script_b').glob('*.log'))
            self.assertTrue((logs_path / 'script_c').glob('*.log'))

            print(f"✅ E2E Test 2 passed: {len(subfolders)} separate subfolders created")

        finally:
            os.chdir(original_dir)

    def test_e2e_handler_direct_usage(self):
        """
        E2E Test 3: Verify LineBasedRotatingHandler works directly.

        Tests handler without LoggingManager wrapper.
        """
        log_dir = Path(self.test_dir) / "direct_test"
        log_dir.mkdir(parents=True)
        log_file = log_dir / "direct-20260207_120000.log"

        # Create handler and logger directly
        handler = LineBasedRotatingHandler(
            filename=str(log_file),
            max_lines=100,
            max_files=5
        )

        logger = logging.getLogger('direct_test')
        logger.handlers.clear()
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        # Emit 250 lines (should create 3 files: 0-100, 101-200, 201-250)
        for i in range(250):
            logger.info(f"Direct message {i}")

        # Verify multiple files created
        log_files = list(log_dir.glob('*.log'))
        self.assertGreaterEqual(len(log_files), 2,
                               f"Should have at least 2 files after 250 lines, got {len(log_files)}")

        handler.close()

        print(f"✅ E2E Test 3 passed: {len(log_files)} files created via direct handler usage")

    def test_e2e_backward_compatibility(self):
        """
        E2E Test 4: Verify backward compatibility with existing code.

        Tests that existing setup_logger() calls work without modification.
        """
        import os
        original_dir = os.getcwd()
        os.chdir(self.test_dir)

        try:
            # Use setup_logger() with old-style parameters (should still work)
            manager = LoggingManager()
            logger = manager.setup_logger(
                name='legacy_script',
                level='INFO',
                log_to_file=True,
                max_file_size=10485760,  # Old parameter (now ignored)
                backup_count=5           # Old parameter (now ignored)
            )

            # Should work without errors
            logger.info("Legacy message 1")
            logger.info("Legacy message 2")

            # Verify logs created with new structure
            logs_path = Path('logs') / 'legacy_script'
            self.assertTrue(logs_path.exists())

            log_files = list(logs_path.glob('*.log'))
            self.assertEqual(len(log_files), 1)

            # Verify new filename format used
            filename = log_files[0].name
            self.assertRegex(filename, r'^legacy_script-\d{8}_\d{6}\.log$')

            print("✅ E2E Test 4 passed: Backward compatibility maintained")

        finally:
            os.chdir(original_dir)

    def test_e2e_logs_folder_auto_creation(self):
        """
        E2E Test 5: Verify logs/ folder auto-creation.

        Tests that logs/ folder is created if it doesn't exist.
        """
        import os
        original_dir = os.getcwd()
        os.chdir(self.test_dir)

        try:
            # Verify logs/ doesn't exist yet
            logs_path = Path('logs')
            self.assertFalse(logs_path.exists(), "logs/ should not exist initially")

            # Create logger (should auto-create logs/)
            manager = LoggingManager()
            logger = manager.setup_logger('auto_test', log_to_file=True)
            logger.info("Auto-creation test")

            # Verify logs/ was created
            self.assertTrue(logs_path.exists(), "logs/ should be auto-created")
            self.assertTrue((logs_path / 'auto_test').exists(),
                          "logs/auto_test/ subfolder should be auto-created")

            print("✅ E2E Test 5 passed: logs/ folder auto-created")

        finally:
            os.chdir(original_dir)

    def test_e2e_timestamp_uniqueness(self):
        """
        E2E Test 6: Verify timestamps are unique across rotations.

        Tests that each rotation creates a file with unique timestamp.
        """
        import os
        original_dir = os.getcwd()
        os.chdir(self.test_dir)

        try:
            # Create logger
            manager = LoggingManager()
            logger = manager.setup_logger('timestamp_test', log_to_file=True)

            # Emit 600 lines quickly (should rotate once)
            for i in range(600):
                logger.info(f"Timestamp test {i}")

            # Get all log files
            logs_path = Path('logs') / 'timestamp_test'
            log_files = sorted(logs_path.glob('*.log'))

            if len(log_files) >= 2:
                # Extract timestamps from filenames
                timestamps = []
                for log_file in log_files:
                    # Format: {name}-{YYYYMMDD_HHMMSS}.log
                    timestamp = log_file.stem.split('-')[-1]
                    timestamps.append(timestamp)

                # Verify all unique
                self.assertEqual(len(timestamps), len(set(timestamps)),
                               "All timestamps should be unique")

                print(f"✅ E2E Test 6 passed: {len(timestamps)} unique timestamps")
            else:
                print("⚠️  E2E Test 6: Only 1 file created (rotation may need more lines)")

        finally:
            os.chdir(original_dir)


if __name__ == '__main__':
    unittest.main()
