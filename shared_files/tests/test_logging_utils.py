#!/usr/bin/env python3
"""
Unit tests for logging utilities module

Tests standardized logging configuration and management patterns.

Author: Kai Mizuno
Last Updated: September 2025
"""

import unittest
import tempfile
import shutil
import logging
import sys
import os
import time
from pathlib import Path
from unittest.mock import patch, MagicMock
from io import StringIO

from shared_files.logging_utils import (
    LoggingManager,
    setup_logger,
    setup_module_logging,
    setup_draft_helper_logging,
    setup_data_fetcher_logging,
    get_progress_logger,
    setup_basic_logging,
    disable_all_logging,
    enable_all_logging,
    get_logger_info,
    configure_async_logging,
    setup_logging_config
)


class TestLoggingManager(unittest.TestCase):
    """Test cases for LoggingManager class"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.manager = LoggingManager()

        # Store original logging state
        self.original_loggers = logging.getLogger().manager.loggerDict.copy()

    def _safe_cleanup_temp_dir(self):
        """Safely clean up temporary directory on Windows"""
        try:
            shutil.rmtree(self.temp_dir)
        except (OSError, PermissionError):
            # Windows file lock issues - try again after brief delay
            time.sleep(0.1)
            try:
                shutil.rmtree(self.temp_dir)
            except (OSError, PermissionError):
                pass  # Skip cleanup if still locked

    def _close_all_handlers(self):
        """Close all handlers to release file locks"""
        for logger_name in list(logging.getLogger().manager.loggerDict.keys()):
            logger = logging.getLogger(logger_name)
            for handler in logger.handlers[:]:
                try:
                    handler.close()
                    logger.removeHandler(handler)
                except:
                    pass

    def tearDown(self):
        """Clean up test fixtures"""
        # Close all handlers to release file locks
        self._close_all_handlers()

        # Clean up temporary directory
        self._safe_cleanup_temp_dir()

        # Reset logging state
        logging.getLogger().manager.loggerDict.clear()
        logging.getLogger().manager.loggerDict.update(self.original_loggers)

        # Re-enable logging if disabled
        logging.disable(logging.NOTSET)

    def test_setup_logger_basic(self):
        """Test basic logger setup"""
        logger = self.manager.setup_logger('test_logger')

        self.assertEqual(logger.name, 'test_logger')
        self.assertEqual(logger.level, logging.INFO)
        self.assertGreater(len(logger.handlers), 0)

    def test_setup_logger_with_file_logging(self):
        """Test logger setup with file logging"""
        log_file = self.temp_dir / "test.log"

        logger = self.manager.setup_logger(
            'test_file_logger',
            log_to_file=True,
            log_file_path=log_file
        )

        # Test that file handler is added
        file_handlers = [h for h in logger.handlers if isinstance(h, logging.handlers.RotatingFileHandler)]
        self.assertEqual(len(file_handlers), 1)

        # Test logging to file
        logger.info("Test message")
        self.assertTrue(log_file.exists())

    def test_setup_logger_different_levels(self):
        """Test logger setup with different logging levels"""
        for level_name, level_value in LoggingManager.LEVEL_MAP.items():
            with self.subTest(level=level_name):
                logger = self.manager.setup_logger(f'test_{level_name.lower()}', level=level_name)
                self.assertEqual(logger.level, level_value)

    def test_setup_logger_different_formats(self):
        """Test logger setup with different formats"""
        formats = ['detailed', 'standard', 'simple']

        for fmt in formats:
            with self.subTest(format=fmt):
                logger = self.manager.setup_logger(f'test_{fmt}', log_format=fmt)
                self.assertGreater(len(logger.handlers), 0)

    def test_setup_logger_no_console(self):
        """Test logger setup without console handler"""
        logger = self.manager.setup_logger(
            'test_no_console',
            enable_console=False,
            log_to_file=True,
            log_file_path=self.temp_dir / "no_console.log"
        )

        # Should have only file handler, no console handler
        console_handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)
                          and not isinstance(h, logging.handlers.RotatingFileHandler)]
        self.assertEqual(len(console_handlers), 0)

    def test_logger_already_configured(self):
        """Test that already configured loggers are not reconfigured"""
        logger1 = self.manager.setup_logger('duplicate_test')
        original_handlers = len(logger1.handlers)

        logger2 = self.manager.setup_logger('duplicate_test')

        self.assertEqual(logger1, logger2)
        self.assertEqual(len(logger2.handlers), original_handlers)

    def test_generate_log_file_path(self):
        """Test automatic log file path generation"""
        path = self.manager._generate_log_file_path('test.module')

        self.assertIsInstance(path, Path)
        self.assertTrue(str(path).endswith('.log'))
        self.assertIn('module', str(path))

    def test_disable_and_enable_logging(self):
        """Test disabling and enabling logging"""
        logger = self.manager.setup_logger('disable_test')

        # Test disable
        self.manager.disable_logging('disable_test')
        self.assertTrue(logger.disabled)

        # Test enable
        self.manager.enable_logging('disable_test')
        self.assertFalse(logger.disabled)

    def test_get_logger_status(self):
        """Test getting logger status information"""
        logger = self.manager.setup_logger('status_test', level='DEBUG')
        status = self.manager.get_logger_status('status_test')

        self.assertEqual(status['name'], 'status_test')
        self.assertEqual(status['level'], 'DEBUG')
        self.assertIsInstance(status['handlers'], list)
        self.assertGreater(len(status['handlers']), 0)


class TestConvenienceFunctions(unittest.TestCase):
    """Test cases for convenience functions"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = Path(tempfile.mkdtemp())

        # Store original logging state
        self.original_loggers = logging.getLogger().manager.loggerDict.copy()

    def _safe_cleanup_temp_dir(self):
        """Safely clean up temporary directory on Windows"""
        try:
            shutil.rmtree(self.temp_dir)
        except (OSError, PermissionError):
            time.sleep(0.1)
            try:
                shutil.rmtree(self.temp_dir)
            except (OSError, PermissionError):
                pass

    def _close_all_handlers(self):
        """Close all handlers to release file locks"""
        for logger_name in list(logging.getLogger().manager.loggerDict.keys()):
            logger = logging.getLogger(logger_name)
            for handler in logger.handlers[:]:
                try:
                    handler.close()
                    logger.removeHandler(handler)
                except:
                    pass

    def tearDown(self):
        """Clean up test fixtures"""
        # Close all handlers to release file locks
        self._close_all_handlers()

        # Clean up temporary directory
        self._safe_cleanup_temp_dir()

        # Reset logging state
        logging.getLogger().manager.loggerDict.clear()
        logging.getLogger().manager.loggerDict.update(self.original_loggers)

        # Re-enable logging if disabled
        logging.disable(logging.NOTSET)

    def test_setup_logger_convenience(self):
        """Test convenience setup_logger function"""
        logger = setup_logger('convenience_test', level='WARNING')

        self.assertEqual(logger.name, 'convenience_test')
        self.assertEqual(logger.level, logging.WARNING)

    def test_setup_module_logging(self):
        """Test module logging setup"""
        logger = setup_module_logging('test_module')

        self.assertEqual(logger.name, 'test_module')
        self.assertEqual(logger.level, logging.INFO)

    def test_setup_module_logging_with_config(self):
        """Test module logging setup with custom config"""
        config = {
            'level': 'DEBUG',
            'log_to_file': True,
            'log_file_path': self.temp_dir / 'module_test.log'
        }

        logger = setup_module_logging('test_module_config', config)

        self.assertEqual(logger.level, logging.DEBUG)

        # Check for file handler
        file_handlers = [h for h in logger.handlers if isinstance(h, logging.handlers.RotatingFileHandler)]
        self.assertEqual(len(file_handlers), 1)

    def test_setup_draft_helper_logging_enabled(self):
        """Test draft helper logging when enabled"""
        logger = setup_draft_helper_logging(enabled=True, log_level='DEBUG')

        self.assertEqual(logger.name, 'draft_helper')
        self.assertEqual(logger.level, logging.DEBUG)

    def test_setup_draft_helper_logging_disabled(self):
        """Test draft helper logging when disabled"""
        logger = setup_draft_helper_logging(enabled=False)

        self.assertEqual(logger.name, 'draft_helper')
        self.assertTrue(logger.disabled)

    def test_setup_data_fetcher_logging(self):
        """Test data fetcher logging setup"""
        log_file = self.temp_dir / 'data_fetcher.log'
        logger = setup_data_fetcher_logging(
            enabled=True,
            log_level='INFO',
            log_file=str(log_file)
        )

        self.assertEqual(logger.name, 'data_fetcher')
        self.assertEqual(logger.level, logging.INFO)

    def test_get_progress_logger(self):
        """Test progress logger setup"""
        logger = get_progress_logger('progress_test', show_progress=True)

        self.assertEqual(logger.name, 'progress_test.progress')
        self.assertEqual(logger.level, logging.INFO)

    def test_get_progress_logger_no_progress(self):
        """Test progress logger with progress disabled"""
        logger = get_progress_logger('no_progress_test', show_progress=False)

        self.assertEqual(logger.level, logging.WARNING)

    def test_disable_enable_all_logging(self):
        """Test disabling and enabling all logging"""
        logger = setup_logger('global_test')

        # Test disable all
        disable_all_logging()
        # Note: This affects the root logger, so we check the global state

        # Test enable all
        enable_all_logging()

    def test_get_logger_info(self):
        """Test getting logger information"""
        logger = setup_logger('info_test', level='ERROR')
        info = get_logger_info('info_test')

        self.assertEqual(info['name'], 'info_test')
        self.assertEqual(info['level'], 'ERROR')

    def test_configure_async_logging(self):
        """Test async logging configuration"""
        logger = setup_logger('async_test')
        async_logger = configure_async_logging(logger)

        self.assertEqual(logger, async_logger)

        # Check that handlers have async context
        for handler in async_logger.handlers:
            if handler.formatter:
                self.assertIn('[async]', handler.formatter._fmt)

    def test_setup_logging_config_legacy(self):
        """Test legacy configuration compatibility"""
        config = {
            'name': 'legacy_test',
            'level': 'WARNING',
            'filename': str(self.temp_dir / 'legacy.log')
        }

        logger = setup_logging_config(config)

        self.assertEqual(logger.name, 'legacy_test')
        self.assertEqual(logger.level, logging.WARNING)


class TestLoggingIntegration(unittest.TestCase):
    """Integration tests for logging functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = Path(tempfile.mkdtemp())

        # Store original logging state
        self.original_loggers = logging.getLogger().manager.loggerDict.copy()

    def _safe_cleanup_temp_dir(self):
        """Safely clean up temporary directory on Windows"""
        try:
            shutil.rmtree(self.temp_dir)
        except (OSError, PermissionError):
            time.sleep(0.1)
            try:
                shutil.rmtree(self.temp_dir)
            except (OSError, PermissionError):
                pass

    def _close_all_handlers(self):
        """Close all handlers to release file locks"""
        for logger_name in list(logging.getLogger().manager.loggerDict.keys()):
            logger = logging.getLogger(logger_name)
            for handler in logger.handlers[:]:
                try:
                    handler.close()
                    logger.removeHandler(handler)
                except:
                    pass

    def tearDown(self):
        """Clean up test fixtures"""
        # Close all handlers to release file locks
        self._close_all_handlers()

        # Clean up temporary directory
        self._safe_cleanup_temp_dir()

        # Reset logging state
        logging.getLogger().manager.loggerDict.clear()
        logging.getLogger().manager.loggerDict.update(self.original_loggers)

        # Re-enable logging if disabled
        logging.disable(logging.NOTSET)

    def test_actual_logging_output(self):
        """Test that loggers actually produce output"""
        log_file = self.temp_dir / 'output_test.log'
        logger = setup_logger(
            'output_test',
            level='INFO',
            log_to_file=True,
            log_file_path=log_file
        )

        test_message = "Test logging output"
        logger.info(test_message)

        # Check file output
        self.assertTrue(log_file.exists())
        with open(log_file, 'r') as f:
            content = f.read()
        self.assertIn(test_message, content)

    def test_multiple_loggers_isolation(self):
        """Test that multiple loggers work independently"""
        logger1 = setup_logger('isolation_test_1', level='DEBUG')
        logger2 = setup_logger('isolation_test_2', level='ERROR')

        self.assertEqual(logger1.level, logging.DEBUG)
        self.assertEqual(logger2.level, logging.ERROR)
        self.assertNotEqual(logger1, logger2)

    def test_log_rotation(self):
        """Test log file rotation functionality"""
        log_file = self.temp_dir / 'rotation_test.log'
        logger = setup_logger(
            'rotation_test',
            log_to_file=True,
            log_file_path=log_file,
            max_file_size=100,  # Very small size to trigger rotation
            backup_count=2
        )

        # Write enough data to trigger rotation
        for i in range(50):
            logger.info(f"Test message {i} with enough content to trigger rotation")

        # Check that rotation occurred (backup files exist)
        backup_files = list(self.temp_dir.glob('rotation_test.log.*'))
        self.assertGreater(len(backup_files), 0)

    def test_format_consistency(self):
        """Test that different format styles work consistently"""
        formats = ['detailed', 'standard', 'simple']

        for fmt in formats:
            with self.subTest(format=fmt):
                log_file = self.temp_dir / f'format_{fmt}.log'
                logger = setup_logger(
                    f'format_{fmt}',
                    log_to_file=True,
                    log_file_path=log_file,
                    log_format=fmt
                )

                logger.info("Test format message")

                with open(log_file, 'r') as f:
                    content = f.read()

                self.assertIn("Test format message", content)
                if fmt == 'detailed':
                    self.assertIn('test_format_consistency', content)


if __name__ == '__main__':
    unittest.main()