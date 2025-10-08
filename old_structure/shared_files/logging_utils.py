#!/usr/bin/env python3
"""
Logging Utilities Module

Provides standardized logging configuration and setup patterns used across multiple modules
in the fantasy football system. Consolidates logging configuration and provides consistent
formatting, handlers, and logging levels.

Author: Kai Mizuno
Last Updated: September 2025
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
        self._configured_loggers = set()

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

        # Skip if already configured
        if name in self._configured_loggers:
            return logger

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
                log_file_path = self._generate_log_file_path(name)

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

        self._configured_loggers.add(name)
        return logger

    def _get_formatter(self, format_style: str) -> logging.Formatter:
        """Get appropriate formatter based on style."""
        format_map = {
            'detailed': self.DETAILED_FORMAT,
            'standard': self.STANDARD_FORMAT,
            'simple': self.SIMPLE_FORMAT
        }

        format_string = format_map.get(format_style, self.STANDARD_FORMAT)
        return logging.Formatter(format_string, datefmt=self.TIMESTAMP_FORMAT)

    def _generate_log_file_path(self, logger_name: str) -> Path:
        """Generate a log file path based on logger name."""
        # Extract module name from logger name
        module_name = logger_name.split('.')[-1] if '.' in logger_name else logger_name
        timestamp = datetime.now().strftime('%Y%m%d')
        filename = f"{module_name}_{timestamp}.log"

        # Create logs directory in project root
        logs_dir = Path.cwd() / 'logs'
        return logs_dir / filename

    def setup_basic_logging(self,
                           level: Union[str, int] = 'INFO',
                           format_style: str = 'standard') -> None:
        """
        Set up basic logging configuration for simple use cases.

        Args:
            level: Logging level
            format_style: Format style ('detailed', 'standard', 'simple')
        """
        if isinstance(level, str):
            level = self.LEVEL_MAP.get(level.upper(), logging.INFO)

        formatter = self._get_formatter(format_style)

        # Clear any existing configuration
        logging.getLogger().handlers.clear()

        # Set up basic configuration
        logging.basicConfig(
            level=level,
            format=formatter._fmt,
            datefmt=formatter.datefmt,
            stream=sys.stdout
        )

    def disable_logging(self, logger_name: Optional[str] = None) -> None:
        """
        Disable logging for a specific logger or all logging.

        Args:
            logger_name: Specific logger to disable, or None for all logging
        """
        if logger_name:
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.CRITICAL + 1)
            logger.disabled = True
        else:
            logging.disable(logging.CRITICAL)

    def enable_logging(self, logger_name: Optional[str] = None) -> None:
        """
        Re-enable logging for a specific logger or all logging.

        Args:
            logger_name: Specific logger to enable, or None for all logging
        """
        if logger_name:
            logger = logging.getLogger(logger_name)
            logger.disabled = False
        else:
            logging.disable(logging.NOTSET)

    def get_logger_status(self, logger_name: str) -> Dict[str, Any]:
        """
        Get status information about a logger.

        Args:
            logger_name: Name of the logger to inspect

        Returns:
            Dictionary with logger status information
        """
        logger = logging.getLogger(logger_name)

        return {
            'name': logger.name,
            'level': logging.getLevelName(logger.level),
            'disabled': logger.disabled,
            'handlers': [
                {
                    'type': type(handler).__name__,
                    'level': logging.getLevelName(handler.level),
                    'formatter': type(handler.formatter).__name__ if handler.formatter else None
                }
                for handler in logger.handlers
            ],
            'propagate': logger.propagate
        }


# Global logging manager instance
_logging_manager = LoggingManager()


def setup_logger(name: str, **kwargs) -> logging.Logger:
    """
    Convenience function to set up a logger using the global logging manager.

    Args:
        name: Logger name (typically __name__)
        **kwargs: Additional arguments passed to LoggingManager.setup_logger()

    Returns:
        Configured logger instance
    """
    return _logging_manager.setup_logger(name, **kwargs)


def setup_module_logging(module_name: str,
                        config: Optional[Dict[str, Any]] = None) -> logging.Logger:
    """
    Set up logging for a specific module with common patterns.

    Args:
        module_name: Name of the module (typically __name__)
        config: Optional configuration dictionary

    Returns:
        Configured logger instance
    """
    if config is None:
        config = {}

    # Check for simulation mode environment variable
    simulation_log_level = os.environ.get('SIMULATION_LOG_LEVEL', None)

    # Default configuration for modules
    default_config = {
        'level': simulation_log_level if simulation_log_level else 'INFO',
        'log_to_file': False,
        'log_format': 'standard',
        'enable_console': True
    }

    # Merge with provided config
    final_config = {**default_config, **config}

    return setup_logger(module_name, **final_config)


def setup_draft_helper_logging(enabled: bool = True,
                              log_to_file: bool = False,
                              log_level: str = 'INFO') -> logging.Logger:
    """
    Set up logging specifically for draft helper module.

    Args:
        enabled: Whether logging is enabled
        log_to_file: Whether to log to file
        log_level: Logging level

    Returns:
        Configured logger for draft helper
    """
    if not enabled:
        _logging_manager.disable_logging('draft_helper')
        return logging.getLogger('draft_helper')

    config = {
        'level': log_level,
        'log_to_file': log_to_file,
        'log_format': 'standard',
        'enable_console': True
    }

    if log_to_file:
        config['log_file_path'] = Path('logs') / 'draft_helper.log'

    return setup_logger('draft_helper', **config)


def setup_data_fetcher_logging(enabled: bool = True,
                              log_level: str = 'INFO',
                              log_file: Optional[str] = None) -> logging.Logger:
    """
    Set up logging specifically for data fetcher modules.

    Args:
        enabled: Whether logging is enabled
        log_level: Logging level
        log_file: Optional log file path

    Returns:
        Configured logger for data fetcher
    """
    if not enabled:
        _logging_manager.disable_logging('data_fetcher')
        return logging.getLogger('data_fetcher')

    config = {
        'level': log_level,
        'log_to_file': bool(log_file),
        'log_format': 'detailed',
        'enable_console': True
    }

    if log_file:
        config['log_file_path'] = log_file

    return setup_logger('data_fetcher', **config)


def get_progress_logger(name: str, show_progress: bool = True) -> logging.Logger:
    """
    Get a logger configured for progress tracking.

    Args:
        name: Logger name
        show_progress: Whether to show progress messages

    Returns:
        Logger configured for progress tracking
    """
    config = {
        'level': 'INFO' if show_progress else 'WARNING',
        'log_format': 'simple',
        'enable_console': True,
        'log_to_file': False
    }

    return setup_logger(f"{name}.progress", **config)


def setup_basic_logging(level: str = 'INFO', format_style: str = 'standard') -> None:
    """
    Convenience function for basic logging setup.

    Args:
        level: Logging level
        format_style: Format style
    """
    _logging_manager.setup_basic_logging(level, format_style)


def disable_all_logging() -> None:
    """Disable all logging across the application."""
    _logging_manager.disable_logging()


def enable_all_logging() -> None:
    """Re-enable all logging across the application."""
    _logging_manager.enable_logging()


def get_logger_info(logger_name: str) -> Dict[str, Any]:
    """
    Get information about a specific logger.

    Args:
        logger_name: Name of the logger

    Returns:
        Dictionary with logger information
    """
    return _logging_manager.get_logger_status(logger_name)


def configure_async_logging(logger: logging.Logger) -> logging.Logger:
    """
    Configure a logger for async operations with appropriate formatting.

    Args:
        logger: Logger to configure

    Returns:
        Configured logger
    """
    # Add async context to formatter if not already present
    for handler in logger.handlers:
        if handler.formatter and 'asyncio' not in handler.formatter._fmt:
            # Create new formatter with async context
            new_format = handler.formatter._fmt.replace(
                '%(message)s',
                '%(message)s [async]'
            )
            handler.setFormatter(logging.Formatter(
                new_format,
                datefmt=handler.formatter.datefmt
            ))

    return logger


# Legacy compatibility functions for existing code
def setup_logging_config(config_dict: Dict[str, Any]) -> logging.Logger:
    """
    Legacy function for backward compatibility with existing configuration dictionaries.

    Args:
        config_dict: Configuration dictionary with logging settings

    Returns:
        Configured logger
    """
    name = config_dict.get('name', 'main')
    level = config_dict.get('level', 'INFO')
    log_to_file = config_dict.get('filename') is not None
    log_file_path = config_dict.get('filename')

    config = {
        'level': level,
        'log_to_file': log_to_file,
        'log_file_path': log_file_path,
        'log_format': 'standard'
    }

    return setup_logger(name, **config)