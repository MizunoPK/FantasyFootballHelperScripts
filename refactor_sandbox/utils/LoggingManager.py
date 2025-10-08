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
import os
from pathlib import Path
from typing import Optional, Dict, Any, Union
from datetime import datetime


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

        # Clear existing handlers
        logger.handlers.clear()
        logger.propagate = False

        # Set logging level
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

        # File handler with rotation
        if log_to_file:
            if log_file_path is None:
                log_file_path = self._generate_log_file_path(log_file_path, name)

            log_file_path = Path(log_file_path)
            log_file_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.handlers.RotatingFileHandler(
                log_file_path,
                maxBytes=max_file_size,
                backupCount=backup_count,
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

    def _generate_log_file_path(self, log_path: str, logger_name: str) -> Path:
        """Generate a log file path based on logger name."""
        timestamp = datetime.now().strftime('%Y%m%d')
        filename = f"{logger_name}_{timestamp}.log"

        # Create logs directory in project root
        return log_path / filename



# Global logging manager instance
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
