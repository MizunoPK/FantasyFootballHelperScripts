#!/usr/bin/env python3
"""
Error Handler - Standardized Error Handling and Recovery

This module provides standardized error handling patterns, logging, and recovery
mechanisms for the Fantasy Football Helper Scripts project.

Features:
- Consistent error logging with context information
- Configurable retry mechanisms with exponential backoff
- Standard exception handling decorators
- Error context management for better debugging
- Graceful degradation patterns

Author: Kai Mizuno
Last Updated: September 2025
"""

import asyncio
import functools
import time
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union
from dataclasses import dataclass, field

from utils.LoggingManager import get_logger

# Type variables for generic decorators
T = TypeVar('T')
F = TypeVar('F', bound=Callable[..., Any])


@dataclass
class ErrorContext:
    """
    Contextual information about an error for better debugging and recovery.
    """
    operation: str
    component: str
    timestamp: datetime = field(default_factory=datetime.now)
    file_path: Optional[str] = None
    player_id: Optional[str] = None
    additional_context: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert error context to dictionary for logging"""
        return {
            'operation': self.operation,
            'component': self.component,
            'timestamp': self.timestamp.isoformat(),
            'file_path': self.file_path,
            'player_id': self.player_id,
            'additional_context': self.additional_context
        }


class FantasyFootballError(Exception):
    """Base exception class for Fantasy Football Helper Scripts"""

    def __init__(self, message: str, context: Optional[ErrorContext] = None, original_exception: Optional[Exception] = None):
        super().__init__(message)
        self.message = message
        self.context = context
        self.original_exception = original_exception
        self.timestamp = datetime.now()

    def __str__(self) -> str:
        base_message = self.message
        if self.context:
            base_message += f" [Component: {self.context.component}, Operation: {self.context.operation}]"
        if self.original_exception:
            base_message += f" [Original: {type(self.original_exception).__name__}: {self.original_exception}]"
        return base_message


class DataProcessingError(FantasyFootballError):
    """Exception for data processing and validation errors"""
    pass


class APIError(FantasyFootballError):
    """Exception for API communication errors"""
    pass


class FileOperationError(FantasyFootballError):
    """Exception for file I/O and data export errors"""
    pass


class ConfigurationError(FantasyFootballError):
    """Exception for configuration and setup errors"""
    pass


class ErrorHandler:
    """
    Centralized error handling and logging with context awareness.
    """

    def __init__(self, component_name: str, enable_detailed_logging: bool = True):
        """
        Initialize error handler for a specific component.

        Args:
            component_name: Name of the component using this error handler
            enable_detailed_logging: Whether to include detailed context in logs
        """
        self.component_name = component_name
        self.enable_detailed_logging = enable_detailed_logging
        self.error_counts: Dict[str, int] = {}
        self.logger = get_logger()

    def log_error(self, error: Exception, context: Optional[ErrorContext] = None,
                  severity: str = "ERROR", include_traceback: bool = True) -> None:
        """
        Log an error with optional context information.

        Args:
            error: The exception that occurred
            context: Additional context about the error
            severity: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            include_traceback: Whether to include full traceback in logs
        """
        # Create default context if none provided
        if context is None:
            context = ErrorContext(
                operation="unknown",
                component=self.component_name
            )

        # Track error frequency
        error_type = type(error).__name__
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1

        # Prepare log message
        base_message = f"{error_type}: {str(error)}"

        if self.enable_detailed_logging and context:
            context_info = context.to_dict()
            context_str = ", ".join([f"{k}={v}" for k, v in context_info.items() if v is not None])
            base_message += f" | Context: {context_str}"

        # Log with appropriate severity
        log_method = getattr(self.logger, severity.lower(), self.logger.error)

        if include_traceback and severity in ("ERROR", "CRITICAL"):
            log_method(base_message, exc_info=True)
        else:
            log_method(base_message)

    def handle_error(self, error: Exception, context: Optional[ErrorContext] = None,
                    default_return: Any = None, reraise: bool = False) -> Any:
        """
        Handle an error with logging and optional recovery.

        Args:
            error: The exception that occurred
            context: Additional context about the error
            default_return: Value to return if not re-raising
            reraise: Whether to re-raise the exception after logging

        Returns:
            default_return if not re-raising, otherwise raises the exception
        """
        self.log_error(error, context)

        if reraise:
            raise error

        return default_return

    def create_context(self, operation: str, file_path: Optional[str] = None,
                      player_id: Optional[str] = None, **kwargs) -> ErrorContext:
        """
        Create an error context for the current operation.

        Args:
            operation: Description of the current operation
            file_path: File being processed (if applicable)
            player_id: Player ID being processed (if applicable)
            **kwargs: Additional context information

        Returns:
            ErrorContext object with provided information
        """
        return ErrorContext(
            operation=operation,
            component=self.component_name,
            file_path=file_path,
            player_id=player_id,
            additional_context=kwargs
        )

    def get_error_summary(self) -> Dict[str, int]:
        """Get summary of error counts by type"""
        return self.error_counts.copy()

    def reset_error_counts(self) -> None:
        """Reset error tracking counters"""
        self.error_counts.clear()


class RetryHandler:
    """
    Configurable retry mechanism with exponential backoff.
    """

    def __init__(self, max_attempts: int = 3, base_delay: float = 1.0,
                 max_delay: float = 60.0, backoff_factor: float = 2.0):
        """
        Initialize retry handler with exponential backoff settings.

        Args:
            max_attempts: Maximum number of retry attempts
            base_delay: Initial delay between retries (seconds)
            max_delay: Maximum delay between retries (seconds)
            backoff_factor: Multiplier for exponential backoff
        """
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor

    def calculate_delay(self, attempt: int) -> float:
        """Calculate delay for a given attempt number"""
        delay = self.base_delay * (self.backoff_factor ** attempt)
        return min(delay, self.max_delay)

    def retry_sync(self, func: Callable[..., T], *args, **kwargs) -> T:
        """
        Execute a function with retry logic (synchronous).

        Args:
            func: Function to execute with retries
            *args: Arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function

        Returns:
            Result of successful function execution

        Raises:
            Last exception if all retries fail
        """
        last_exception = None

        for attempt in range(self.max_attempts):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                if attempt < self.max_attempts - 1:  # Don't delay after last attempt
                    delay = self.calculate_delay(attempt)
                    self.logger.debug(f"Retry attempt {attempt + 1} failed, waiting {delay:.2f}s: {e}")
                    time.sleep(delay)
                else:
                    self.logger.error(f"All {self.max_attempts} retry attempts failed: {e}")

        if last_exception:
            raise last_exception

    async def retry_async(self, func: Callable[..., T], *args, **kwargs) -> T:
        """
        Execute an async function with retry logic.

        Args:
            func: Async function to execute with retries
            *args: Arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function

        Returns:
            Result of successful function execution

        Raises:
            Last exception if all retries fail
        """
        last_exception = None

        for attempt in range(self.max_attempts):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e

                if attempt < self.max_attempts - 1:  # Don't delay after last attempt
                    delay = self.calculate_delay(attempt)
                    self.logger.debug(f"Async retry attempt {attempt + 1} failed, waiting {delay:.2f}s: {e}")
                    await asyncio.sleep(delay)
                else:
                    self.logger.error(f"All {self.max_attempts} async retry attempts failed: {e}")

        if last_exception:
            raise last_exception


# Global error handler instance for convenience
_global_error_handler = ErrorHandler("global")


def handle_errors(default_return: Any = None, reraise: bool = False,
                 component: Optional[str] = None, operation: Optional[str] = None):
    """
    Decorator for automatic error handling with logging.

    Args:
        default_return: Value to return if an exception occurs and reraise=False
        reraise: Whether to re-raise exceptions after logging
        component: Component name for error context
        operation: Operation name for error context

    Returns:
        Decorated function with error handling
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                context = ErrorContext(
                    operation=operation or func.__name__,
                    component=component or "unknown"
                )
                return _global_error_handler.handle_error(e, context, default_return, reraise)
        return wrapper
    return decorator


def handle_async_errors(default_return: Any = None, reraise: bool = False,
                       component: Optional[str] = None, operation: Optional[str] = None):
    """
    Decorator for automatic error handling with logging (async version).

    Args:
        default_return: Value to return if an exception occurs and reraise=False
        reraise: Whether to re-raise exceptions after logging
        component: Component name for error context
        operation: Operation name for error context

    Returns:
        Decorated async function with error handling
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                context = ErrorContext(
                    operation=operation or func.__name__,
                    component=component or "unknown"
                )
                return _global_error_handler.handle_error(e, context, default_return, reraise)
        return wrapper
    return decorator


def retry_with_backoff(max_attempts: int = 3, base_delay: float = 1.0,
                      max_delay: float = 60.0, backoff_factor: float = 2.0):
    """
    Decorator for adding retry logic with exponential backoff.

    Args:
        max_attempts: Maximum number of retry attempts
        base_delay: Initial delay between retries (seconds)
        max_delay: Maximum delay between retries (seconds)
        backoff_factor: Multiplier for exponential backoff

    Returns:
        Decorated function with retry logic
    """
    retry_handler = RetryHandler(max_attempts, base_delay, max_delay, backoff_factor)

    def decorator(func: F) -> F:
        if asyncio.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                return await retry_handler.retry_async(func, *args, **kwargs)
            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                return retry_handler.retry_sync(func, *args, **kwargs)
            return sync_wrapper
    return decorator


@contextmanager
def error_context(operation: str, component: str = "unknown", **context_kwargs):
    """
    Context manager for capturing and logging errors with context.

    Args:
        operation: Description of the operation being performed
        component: Component name performing the operation
        **context_kwargs: Additional context information

    Example:
        with error_context("loading player data", component="data_loader", file_path="players.csv"):
            # Code that might raise exceptions
            data = load_player_data()
    """
    context = ErrorContext(
        operation=operation,
        component=component,
        additional_context=context_kwargs
    )

    try:
        yield context
    except Exception as e:
        _global_error_handler.log_error(e, context)
        raise


def safe_execute(func: Callable[..., T], *args, default: T = None,
                log_errors: bool = True, **kwargs) -> T:
    """
    Safely execute a function with error handling and optional default return.

    Args:
        func: Function to execute
        *args: Arguments to pass to the function
        default: Default value to return on error
        log_errors: Whether to log errors that occur
        **kwargs: Keyword arguments to pass to the function

    Returns:
        Function result or default value on error
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        if log_errors:
            context = ErrorContext(
                operation=func.__name__,
                component="safe_execute"
            )
            _global_error_handler.log_error(e, context, severity="WARNING", include_traceback=False)
        return default


async def safe_execute_async(func: Callable[..., T], *args, default: T = None,
                            log_errors: bool = True, **kwargs) -> T:
    """
    Safely execute an async function with error handling and optional default return.

    Args:
        func: Async function to execute
        *args: Arguments to pass to the function
        default: Default value to return on error
        log_errors: Whether to log errors that occur
        **kwargs: Keyword arguments to pass to the function

    Returns:
        Function result or default value on error
    """
    try:
        return await func(*args, **kwargs)
    except Exception as e:
        if log_errors:
            context = ErrorContext(
                operation=func.__name__,
                component="safe_execute_async"
            )
            _global_error_handler.log_error(e, context, severity="WARNING", include_traceback=False)
        return default


def validate_file_operation(file_path: Union[str, Path], operation: str = "access") -> None:
    """
    Validate file operations and raise appropriate exceptions.

    Args:
        file_path: Path to the file
        operation: Type of operation (read, write, access)

    Raises:
        FileOperationError: If file operation cannot be completed
    """
    path = Path(file_path)

    if operation in ("read", "access") and not path.exists():
        raise FileOperationError(
            f"File not found: {file_path}",
            context=ErrorContext(operation=f"validate_{operation}", component="file_validator")
        )

    if operation == "write":
        # Check if parent directory exists and is writable
        parent = path.parent
        if not parent.exists():
            try:
                parent.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                raise FileOperationError(
                    f"Cannot create directory for file: {file_path}",
                    context=ErrorContext(operation="validate_write", component="file_validator"),
                    original_exception=e
                )
        elif not parent.is_dir():
            raise FileOperationError(
                f"Parent path is not a directory: {parent}",
                context=ErrorContext(operation="validate_write", component="file_validator")
            )


def create_component_error_handler(component_name: str, **kwargs) -> ErrorHandler:
    """
    Factory function to create error handlers for specific components.

    Args:
        component_name: Name of the component
        **kwargs: Additional arguments for ErrorHandler initialization

    Returns:
        ErrorHandler instance configured for the component
    """
    return ErrorHandler(component_name, **kwargs)


# Convenience functions for common error handling patterns
def log_and_return_none(error: Exception, context: Optional[ErrorContext] = None) -> None:
    """Log an error and return None (common pattern for optional data)"""
    _global_error_handler.log_error(error, context, severity="WARNING", include_traceback=False)
    return None


def log_and_return_empty_list(error: Exception, context: Optional[ErrorContext] = None) -> List:
    """Log an error and return empty list (common pattern for collection operations)"""
    _global_error_handler.log_error(error, context, severity="WARNING", include_traceback=False)
    return []


def log_and_return_empty_dict(error: Exception, context: Optional[ErrorContext] = None) -> Dict:
    """Log an error and return empty dict (common pattern for mapping operations)"""
    _global_error_handler.log_error(error, context, severity="WARNING", include_traceback=False)
    return {}


if __name__ == "__main__":
    # Example usage and testing
    from shared_files.logging_utils import setup_basic_logging
    setup_basic_logging(level='INFO', format_style='simple')

    # Test error handler
    handler = ErrorHandler("test_component")

    try:
        raise ValueError("Test error")
    except Exception as e:
        context = handler.create_context("testing error handler", file_path="test.csv")
        handler.handle_error(e, context, default_return="fallback_value")

    print("Error handler test completed")
    print(f"Error summary: {handler.get_error_summary()}")

    # Test retry mechanism
    retry_handler = RetryHandler(max_attempts=3, base_delay=0.1)

    @retry_with_backoff(max_attempts=2, base_delay=0.1)
    def flaky_function():
        import random
        if random.random() < 0.7:  # 70% chance of failure
            raise RuntimeError("Random failure")
        return "Success!"

    try:
        result = flaky_function()
        print(f"Retry test result: {result}")
    except Exception as e:
        print(f"Retry test failed: {e}")

    # Test context manager
    try:
        with error_context("testing context manager", component="test"):
            raise ValueError("Context manager test error")
    except ValueError:
        print("Context manager test completed")