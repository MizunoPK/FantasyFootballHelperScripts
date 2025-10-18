#!/usr/bin/env python3
"""
Tests for LoggingManager module.

Comprehensive tests for logging configuration, formatters, handlers,
and log file management.

Author: Kai Mizuno
"""

import pytest
import logging
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from utils.LoggingManager import (
    LoggingManager,
    setup_logger,
    get_logger
)


class TestLoggingManager:
    """Test suite for LoggingManager class."""

    def test_logging_manager_initialization(self):
        """Test LoggingManager initializes with default logger."""
        manager = LoggingManager()

        assert manager._logger is not None
        assert isinstance(manager._logger, logging.Logger)

    def test_setup_logger_creates_logger(self):
        """Test setup_logger creates a logger instance."""
        manager = LoggingManager()

        logger = manager.setup_logger("test_logger")

        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_logger"

    def test_setup_logger_sets_level_from_string(self):
        """Test setup_logger sets logging level from string."""
        manager = LoggingManager()

        logger = manager.setup_logger("test", level="DEBUG")

        assert logger.level == logging.DEBUG

    def test_setup_logger_sets_level_from_int(self):
        """Test setup_logger sets logging level from integer."""
        manager = LoggingManager()

        logger = manager.setup_logger("test", level=logging.WARNING)

        assert logger.level == logging.WARNING

    def test_setup_logger_clears_existing_handlers(self):
        """Test setup_logger clears previous handlers."""
        manager = LoggingManager()

        # Setup logger twice
        logger1 = manager.setup_logger("test")
        initial_handler_count = len(logger1.handlers)

        logger2 = manager.setup_logger("test")

        # Should have same number of handlers, not double
        assert len(logger2.handlers) == initial_handler_count

    def test_setup_logger_with_console_enabled(self):
        """Test setup_logger creates console handler when enabled."""
        manager = LoggingManager()

        logger = manager.setup_logger("test", enable_console=True)

        # Should have at least one StreamHandler
        stream_handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
        assert len(stream_handlers) > 0

    def test_setup_logger_with_console_disabled(self):
        """Test setup_logger skips console handler when disabled."""
        manager = LoggingManager()

        logger = manager.setup_logger("test", enable_console=False, log_to_file=False)

        # Should have no StreamHandler
        stream_handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
        assert len(stream_handlers) == 0

    def test_setup_logger_with_file_logging(self, tmp_path):
        """Test setup_logger creates file handler when requested."""
        manager = LoggingManager()
        log_file = tmp_path / "test.log"

        logger = manager.setup_logger("test", log_to_file=True, log_file_path=log_file, enable_console=False)

        # Should have RotatingFileHandler
        file_handlers = [h for h in logger.handlers if isinstance(h, logging.handlers.RotatingFileHandler)]
        assert len(file_handlers) > 0
        assert log_file.exists()

    def test_setup_logger_creates_log_directory(self, tmp_path):
        """Test setup_logger creates parent directories for log file."""
        manager = LoggingManager()
        log_file = tmp_path / "logs" / "subdir" / "test.log"

        manager.setup_logger("test", log_to_file=True, log_file_path=log_file, enable_console=False)

        assert log_file.parent.exists()

    def test_get_logger_returns_current_logger(self):
        """Test get_logger returns the configured logger."""
        manager = LoggingManager()

        logger = manager.setup_logger("test")
        retrieved = manager.get_logger()

        assert retrieved == logger


class TestLogFormats:
    """Test suite for log format configuration."""

    def test_get_formatter_detailed(self):
        """Test _get_formatter returns detailed format."""
        manager = LoggingManager()

        formatter = manager._get_formatter('detailed')

        assert 'funcName' in formatter._fmt
        assert 'lineno' in formatter._fmt

    def test_get_formatter_standard(self):
        """Test _get_formatter returns standard format."""
        manager = LoggingManager()

        formatter = manager._get_formatter('standard')

        assert 'levelname' in formatter._fmt
        assert 'funcName' not in formatter._fmt

    def test_get_formatter_simple(self):
        """Test _get_formatter returns simple format."""
        manager = LoggingManager()

        formatter = manager._get_formatter('simple')

        assert 'levelname' in formatter._fmt
        assert 'asctime' not in formatter._fmt

    def test_get_formatter_unknown_defaults_to_standard(self):
        """Test _get_formatter defaults to standard for unknown format."""
        manager = LoggingManager()

        formatter = manager._get_formatter('unknown_format')

        # Should default to standard format
        assert formatter._fmt == manager.STANDARD_FORMAT

    def test_setup_logger_applies_format(self):
        """Test setup_logger applies specified format to handlers."""
        manager = LoggingManager()

        logger = manager.setup_logger("test", log_format='simple')

        # Check that handlers have the correct formatter
        for handler in logger.handlers:
            assert handler.formatter is not None


class TestLogLevels:
    """Test suite for log level configuration."""

    def test_level_map_contains_all_levels(self):
        """Test LEVEL_MAP contains all standard logging levels."""
        assert 'DEBUG' in LoggingManager.LEVEL_MAP
        assert 'INFO' in LoggingManager.LEVEL_MAP
        assert 'WARNING' in LoggingManager.LEVEL_MAP
        assert 'ERROR' in LoggingManager.LEVEL_MAP
        assert 'CRITICAL' in LoggingManager.LEVEL_MAP

    def test_level_map_values_are_correct(self):
        """Test LEVEL_MAP values match logging module constants."""
        assert LoggingManager.LEVEL_MAP['DEBUG'] == logging.DEBUG
        assert LoggingManager.LEVEL_MAP['INFO'] == logging.INFO
        assert LoggingManager.LEVEL_MAP['WARNING'] == logging.WARNING
        assert LoggingManager.LEVEL_MAP['ERROR'] == logging.ERROR
        assert LoggingManager.LEVEL_MAP['CRITICAL'] == logging.CRITICAL

    def test_setup_logger_case_insensitive_level(self):
        """Test setup_logger handles case-insensitive level strings."""
        manager = LoggingManager()

        logger1 = manager.setup_logger("test1", level="debug")
        logger2 = manager.setup_logger("test2", level="DEBUG")

        assert logger1.level == logger2.level == logging.DEBUG


class TestFileHandlerConfiguration:
    """Test suite for file handler specific configuration."""

    def test_rotating_file_handler_max_size(self, tmp_path):
        """Test file handler uses specified max file size."""
        manager = LoggingManager()
        log_file = tmp_path / "test.log"
        max_size = 5 * 1024 * 1024  # 5MB

        logger = manager.setup_logger(
            "test",
            log_to_file=True,
            log_file_path=log_file,
            max_file_size=max_size,
            enable_console=False
        )

        file_handler = [h for h in logger.handlers if isinstance(h, logging.handlers.RotatingFileHandler)][0]
        assert file_handler.maxBytes == max_size

    def test_rotating_file_handler_backup_count(self, tmp_path):
        """Test file handler uses specified backup count."""
        manager = LoggingManager()
        log_file = tmp_path / "test.log"
        backup_count = 3

        logger = manager.setup_logger(
            "test",
            log_to_file=True,
            log_file_path=log_file,
            backup_count=backup_count,
            enable_console=False
        )

        file_handler = [h for h in logger.handlers if isinstance(h, logging.handlers.RotatingFileHandler)][0]
        assert file_handler.backupCount == backup_count

    def test_file_handler_encoding(self, tmp_path):
        """Test file handler uses UTF-8 encoding."""
        manager = LoggingManager()
        log_file = tmp_path / "test.log"

        logger = manager.setup_logger(
            "test",
            log_to_file=True,
            log_file_path=log_file,
            enable_console=False
        )

        file_handler = [h for h in logger.handlers if isinstance(h, logging.handlers.RotatingFileHandler)][0]
        # RotatingFileHandler stores encoding in stream.encoding
        assert file_handler.stream.encoding == 'utf-8'


class TestGenerateLogFilePath:
    """Test suite for _generate_log_file_path method."""

    def test_generate_log_file_path_includes_logger_name(self, tmp_path):
        """Test generated path includes logger name."""
        manager = LoggingManager()

        path = manager._generate_log_file_path(tmp_path, "my_logger")

        assert "my_logger" in path.name

    def test_generate_log_file_path_includes_timestamp(self, tmp_path):
        """Test generated path includes date timestamp."""
        manager = LoggingManager()

        path = manager._generate_log_file_path(tmp_path, "test")

        # Should contain YYYYMMDD format
        assert len(path.stem.split('_')[-1]) == 8  # Date in YYYYMMDD format

    def test_generate_log_file_path_has_log_extension(self, tmp_path):
        """Test generated path has .log extension."""
        manager = LoggingManager()

        path = manager._generate_log_file_path(tmp_path, "test")

        assert path.suffix == ".log"


class TestModuleLevelFunctions:
    """Test suite for module-level convenience functions."""

    def test_setup_logger_function_creates_logger(self):
        """Test module-level setup_logger creates logger."""
        logger = setup_logger("module_test", enable_console=False)

        assert isinstance(logger, logging.Logger)
        assert logger.name == "module_test"

    def test_setup_logger_function_passes_arguments(self, tmp_path):
        """Test module-level setup_logger passes arguments correctly."""
        log_file = tmp_path / "module.log"

        logger = setup_logger(
            "module_test",
            level="WARNING",
            log_to_file=True,
            log_file_path=log_file,
            enable_console=False
        )

        assert logger.level == logging.WARNING
        assert log_file.exists()

    def test_get_logger_function_returns_logger(self):
        """Test module-level get_logger returns current logger."""
        logger = get_logger()

        assert isinstance(logger, logging.Logger)


class TestLoggerPropagation:
    """Test suite for logger propagation settings."""

    def test_setup_logger_disables_propagation(self):
        """Test setup_logger sets propagate to False."""
        manager = LoggingManager()

        logger = manager.setup_logger("test")

        assert logger.propagate is False


class TestMultipleHandlers:
    """Test suite for multiple handler scenarios."""

    def test_setup_logger_with_both_console_and_file(self, tmp_path):
        """Test setup_logger can create both console and file handlers."""
        manager = LoggingManager()
        log_file = tmp_path / "test.log"

        logger = manager.setup_logger(
            "test",
            enable_console=True,
            log_to_file=True,
            log_file_path=log_file
        )

        # Should have both types of handlers
        stream_handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler) and not isinstance(h, logging.handlers.RotatingFileHandler)]
        file_handlers = [h for h in logger.handlers if isinstance(h, logging.handlers.RotatingFileHandler)]

        assert len(stream_handlers) > 0
        assert len(file_handlers) > 0

    def test_handlers_have_same_level_as_logger(self):
        """Test all handlers inherit logger's level."""
        manager = LoggingManager()

        logger = manager.setup_logger("test", level=logging.ERROR)

        for handler in logger.handlers:
            assert handler.level == logging.ERROR
