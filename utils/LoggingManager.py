#!/usr/bin/env python3
"""
Logging Utilities Module

Provides standardized logging configuration and setup patterns used across multiple modules
in the fantasy football system. Consolidates logging configuration and provides consistent
formatting, handlers, and logging levels.

Author: Kai Mizuno
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional, Union
from datetime import datetime

from utils.LineBasedRotatingHandler import LineBasedRotatingHandler


class LoggingManager:
    """
    Centralized logging configuration manager that provides standardized logging
    setup for all modules in the fantasy football system.
    """

    # Standard log formats
    DETAILED_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    STANDARD_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    SIMPLE_FORMAT = '%(levelname)s: %(message)s'
    TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'
    TIME_ONLY_FORMAT = '%H:%M:%S'

    # Standard log levels mapping
    LEVEL_MAP = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    def __init__(self):
        self._logger = self.setup_logger("default")

    def setup_logger(self,
                    name: str,
                    level: Union[str, int] = 'INFO',
                    log_to_file: bool = False,
                    log_file_path: Optional[Union[str, Path]] = None,
                    log_format: str = 'standard',
                    enable_console: bool = True,
                    max_file_size: int = 10 * 1024 * 1024,  # 10MB
                    backup_count: int = 5) -> logging.Logger:
        """
        Set up a standardized logger with consistent configuration.

        Args:
            name: Logger name (typically __name__)
            level: Logging level ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL' or int)
            log_to_file: Whether to enable file logging
            log_file_path: Path to log file (auto-generated if None)
            log_format: Format style ('detailed', 'standard', 'simple')
            enable_console: Whether to enable console logging
            max_file_size: Maximum log file size before rotation
            backup_count: Number of backup files to keep

        Returns:
            Configured logger instance
        """
        logger = logging.getLogger(name)

        # Clear existing handlers to avoid duplicate log messages
        # Multiple calls to setup_logger for the same name would otherwise accumulate handlers
        logger.handlers.clear()
        # Disable propagation to prevent logs from bubbling up to root logger
        # This prevents duplicate log messages when using hierarchical logger names (e.g., "app.module.submodule")
        logger.propagate = False

        # Set logging level (convert string to logging constant if needed)
        # Allows both "INFO" and logging.INFO to be passed
        if isinstance(level, str):
            level = self.LEVEL_MAP.get(level.upper(), logging.INFO)
        logger.setLevel(level)

        # Get formatter
        formatter = self._get_formatter(log_format)

        # Console handler
        if enable_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            console_handler.setLevel(level)
            logger.addHandler(console_handler)

        # File handler with rotation to prevent unbounded log file growth
        if log_to_file:
            # Auto-generate timestamped log file path if none provided
            if log_file_path is None:
                # Use default logs/ directory at project root
                log_file_path = self._generate_log_file_path(Path('logs'), name)

            log_file_path = Path(log_file_path)
            # Create parent directory if it doesn't exist (e.g., logs/)
            log_file_path.parent.mkdir(parents=True, exist_ok=True)

            # LineBasedRotatingHandler rotates logs based on line count (not file size)
            # Creates timestamped files: {name}-{YYYYMMDD_HHMMSS}.log
            # Automatically cleans up old files when folder exceeds max_files limit
            # Note: max_file_size and backup_count parameters are kept for backward
            # compatibility but are not used by LineBasedRotatingHandler
            file_handler = LineBasedRotatingHandler(
                filename=str(log_file_path),
                mode='a',
                max_lines=500,  # Rotate after 500 lines (hardcoded per spec)
                max_files=50,   # Keep max 50 files per folder (hardcoded per spec)
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            file_handler.setLevel(level)
            logger.addHandler(file_handler)

        self._logger = logger
        return logger
    
    def get_logger(self) -> logging.Logger:
        return self._logger
    
    def _get_formatter(self, format_style: str) -> logging.Formatter:
        """Get appropriate formatter based on style."""
        format_map = {
            'detailed': self.DETAILED_FORMAT,
            'standard': self.STANDARD_FORMAT,
            'simple': self.SIMPLE_FORMAT
        }

        format_string = format_map.get(format_style, self.STANDARD_FORMAT)
        return logging.Formatter(format_string, datefmt=self.TIMESTAMP_FORMAT)

    def _generate_log_file_path(self, log_path: Path, logger_name: str) -> Path:
        """
        Generate a log file path with timestamp in script-specific subfolder.

        Creates logs/{logger_name}/ subfolder structure and generates
        timestamped filename: {logger_name}-{YYYYMMDD_HHMMSS}.log

        Args:
            log_path (Path): Base logs directory (e.g., Path('logs'))
            logger_name (str): Logger name (used for subfolder and filename)

        Returns:
            Path: Full path to log file

        Example:
            >>> _generate_log_file_path(Path('logs'), 'accuracy_simulation')
            Path('logs/accuracy_simulation/accuracy_simulation-20260207_160000.log')

        Raises:
            OSError: If folder creation fails due to permissions
        """
        # Create script-specific subfolder: logs/{logger_name}/
        log_dir = log_path / logger_name

        # Auto-create subfolder if it doesn't exist
        try:
            log_dir.mkdir(parents=True, exist_ok=True)
        except (PermissionError, OSError) as e:
            # Log error to console (can't write to file yet)
            print(f"ERROR: Failed to create log directory {log_dir}: {e}", file=sys.stderr)
            raise

        # Generate full timestamp: YYYYMMDD_HHMMSS (not just date)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Generate filename with hyphen separator: {logger_name}-{timestamp}.log
        filename = f"{logger_name}-{timestamp}.log"

        # Return full path: logs/{logger_name}/{logger_name}-{YYYYMMDD_HHMMSS}.log
        return log_dir / filename



# Global logging manager instance (singleton-like pattern)
# This ensures consistent logging configuration across all modules
# Modules call setup_logger() or get_logger() convenience functions instead of creating their own manager
_logging_manager = LoggingManager()


def setup_logger(name: str,
                level: Union[str, int] = 'INFO',
                log_to_file: bool = False,
                log_file_path: Optional[Union[str, Path]] = None,
                log_format: str = 'standard',
                enable_console: bool = True,
                max_file_size: int = 10 * 1024 * 1024,  # 10MB
                backup_count: int = 5) -> logging.Logger:
    """
    Convenience function to set up a logger using the global logging manager.

    Args:
        name: Logger name (typically __name__)
        **kwargs: Additional arguments passed to LoggingManager.setup_logger()

    Returns:
        Configured logger instance
    """
    return _logging_manager.setup_logger(name, level, log_to_file, log_file_path, log_format, enable_console, max_file_size, backup_count)

def get_logger() -> logging.Logger:
    return _logging_manager.get_logger()
