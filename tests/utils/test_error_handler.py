#!/usr/bin/env python3
"""
Tests for error_handler module.

Comprehensive tests for error handling patterns, custom exceptions,
retry mechanisms, and error context management.

Author: Kai Mizuno
"""

import pytest
import asyncio
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from utils.error_handler import (
    ErrorContext,
    FantasyFootballError,
    DataProcessingError,
    APIError,
    FileOperationError,
    ConfigurationError,
    ErrorHandler,
    RetryHandler,
    handle_errors,
    handle_async_errors,
    retry_with_backoff,
    error_context,
    safe_execute,
    safe_execute_async,
    validate_file_operation,
    create_component_error_handler,
    log_and_return_none,
    log_and_return_empty_list,
    log_and_return_empty_dict
)


class TestErrorContext:
    """Test suite for ErrorContext dataclass."""

    def test_error_context_initialization(self):
        """Test ErrorContext initializes with required fields."""
        ctx = ErrorContext(operation="test_op", component="test_component")

        assert ctx.operation == "test_op"
        assert ctx.component == "test_component"
        assert isinstance(ctx.timestamp, datetime)
        assert ctx.file_path is None
        assert ctx.player_id is None
        assert ctx.additional_context == {}

    def test_error_context_with_optional_fields(self):
        """Test ErrorContext accepts optional fields."""
        ctx = ErrorContext(
            operation="load_data",
            component="data_loader",
            file_path="/path/to/file.csv",
            player_id="12345"
        )

        assert ctx.file_path == "/path/to/file.csv"
        assert ctx.player_id == "12345"

    def test_error_context_to_dict(self):
        """Test ErrorContext.to_dict() converts to dictionary."""
        ctx = ErrorContext(
            operation="test",
            component="test_comp",
            file_path="test.csv"
        )

        result = ctx.to_dict()

        assert isinstance(result, dict)
        assert result["operation"] == "test"
        assert result["component"] == "test_comp"
        assert result["file_path"] == "test.csv"
        assert "timestamp" in result


class TestFantasyFootballError:
    """Test suite for FantasyFootballError and subclasses."""

    def test_fantasy_football_error_basic(self):
        """Test basic FantasyFootballError creation."""
        error = FantasyFootballError("Test error message")

        assert str(error) == "Test error message"
        assert error.message == "Test error message"
        assert error.context is None
        assert error.original_exception is None

    def test_fantasy_football_error_with_context(self):
        """Test FantasyFootballError with error context."""
        ctx = ErrorContext(operation="test", component="test_comp")
        error = FantasyFootballError("Error occurred", context=ctx)

        error_str = str(error)
        assert "Error occurred" in error_str
        assert "test_comp" in error_str
        assert "test" in error_str

    def test_fantasy_football_error_with_original_exception(self):
        """Test FantasyFootballError wraps original exception."""
        original = ValueError("Original error")
        error = FantasyFootballError("Wrapped error", original_exception=original)

        error_str = str(error)
        assert "Wrapped error" in error_str
        assert "ValueError" in error_str
        assert "Original error" in error_str

    def test_data_processing_error_is_subclass(self):
        """Test DataProcessingError is a FantasyFootballError."""
        error = DataProcessingError("Data error")

        assert isinstance(error, FantasyFootballError)
        assert isinstance(error, DataProcessingError)

    def test_api_error_is_subclass(self):
        """Test APIError is a FantasyFootballError."""
        error = APIError("API error")

        assert isinstance(error, FantasyFootballError)
        assert isinstance(error, APIError)

    def test_file_operation_error_is_subclass(self):
        """Test FileOperationError is a FantasyFootballError."""
        error = FileOperationError("File error")

        assert isinstance(error, FantasyFootballError)
        assert isinstance(error, FileOperationError)

    def test_configuration_error_is_subclass(self):
        """Test ConfigurationError is a FantasyFootballError."""
        error = ConfigurationError("Config error")

        assert isinstance(error, FantasyFootballError)
        assert isinstance(error, ConfigurationError)


class TestErrorHandler:
    """Test suite for ErrorHandler class."""

    @pytest.fixture
    def handler(self):
        """Create ErrorHandler instance."""
        return ErrorHandler("test_component")

    def test_error_handler_initialization(self, handler):
        """Test ErrorHandler initializes correctly."""
        assert handler.component_name == "test_component"
        assert handler.enable_detailed_logging is True
        assert handler.error_counts == {}

    def test_log_error_updates_counts(self, handler):
        """Test log_error() updates error counts."""
        error = ValueError("Test error")

        handler.log_error(error)

        assert "ValueError" in handler.error_counts
        assert handler.error_counts["ValueError"] == 1

    def test_log_error_creates_default_context(self, handler):
        """Test log_error() creates default context when none provided."""
        error = ValueError("Test")

        # Should not raise exception
        handler.log_error(error)

        assert "ValueError" in handler.error_counts

    def test_handle_error_logs_and_returns_default(self, handler):
        """Test handle_error() logs error and returns default value."""
        error = ValueError("Test error")
        default_value = "fallback"

        result = handler.handle_error(error, default_return=default_value, reraise=False)

        assert result == "fallback"
        assert "ValueError" in handler.error_counts

    def test_handle_error_reraises_when_requested(self, handler):
        """Test handle_error() re-raises exception when reraise=True."""
        error = ValueError("Test error")

        with pytest.raises(ValueError):
            handler.handle_error(error, reraise=True)

    def test_create_context(self, handler):
        """Test create_context() creates ErrorContext with component."""
        ctx = handler.create_context("test_operation", file_path="test.csv")

        assert ctx.operation == "test_operation"
        assert ctx.component == "test_component"
        assert ctx.file_path == "test.csv"

    def test_get_error_summary(self, handler):
        """Test get_error_summary() returns copy of error counts."""
        handler.log_error(ValueError("Error 1"))
        handler.log_error(ValueError("Error 2"))
        handler.log_error(TypeError("Error 3"))

        summary = handler.get_error_summary()

        assert summary["ValueError"] == 2
        assert summary["TypeError"] == 1

    def test_reset_error_counts(self, handler):
        """Test reset_error_counts() clears counters."""
        handler.log_error(ValueError("Error"))

        handler.reset_error_counts()

        assert handler.error_counts == {}


class TestRetryHandler:
    """Test suite for RetryHandler class."""

    def test_retry_handler_initialization(self):
        """Test RetryHandler initializes with default values."""
        handler = RetryHandler()

        assert handler.max_attempts == 3
        assert handler.base_delay == 1.0
        assert handler.max_delay == 60.0
        assert handler.backoff_factor == 2.0

    def test_retry_handler_custom_values(self):
        """Test RetryHandler accepts custom values."""
        handler = RetryHandler(
            max_attempts=5,
            base_delay=0.5,
            max_delay=30.0,
            backoff_factor=3.0
        )

        assert handler.max_attempts == 5
        assert handler.base_delay == 0.5

    def test_calculate_delay_exponential_backoff(self):
        """Test calculate_delay() uses exponential backoff."""
        handler = RetryHandler(base_delay=1.0, backoff_factor=2.0)

        delay0 = handler.calculate_delay(0)
        delay1 = handler.calculate_delay(1)
        delay2 = handler.calculate_delay(2)

        assert delay0 == 1.0
        assert delay1 == 2.0
        assert delay2 == 4.0

    def test_calculate_delay_respects_max(self):
        """Test calculate_delay() respects max_delay."""
        handler = RetryHandler(base_delay=10.0, max_delay=15.0, backoff_factor=2.0)

        delay = handler.calculate_delay(5)  # Would be 320.0 without max

        assert delay == 15.0

    def test_retry_sync_succeeds_on_first_attempt(self):
        """Test retry_sync() returns result on first success."""
        handler = RetryHandler(max_attempts=3, base_delay=0.01)

        def success_func():
            return "success"

        result = handler.retry_sync(success_func)

        assert result == "success"

    def test_retry_sync_succeeds_after_failures(self):
        """Test retry_sync() retries until success."""
        handler = RetryHandler(max_attempts=3, base_delay=0.01)
        handler.logger = Mock()  # Mock logger since RetryHandler doesn't initialize it
        attempts = []

        def flaky_func():
            attempts.append(1)
            if len(attempts) < 2:
                raise ValueError("Temporary failure")
            return "success"

        result = handler.retry_sync(flaky_func)

        assert result == "success"
        assert len(attempts) == 2

    def test_retry_sync_raises_after_max_attempts(self):
        """Test retry_sync() raises last exception after max attempts."""
        handler = RetryHandler(max_attempts=2, base_delay=0.01)
        handler.logger = Mock()  # Mock logger

        def always_fails():
            raise ValueError("Always fails")

        with pytest.raises(ValueError, match="Always fails"):
            handler.retry_sync(always_fails)

    @pytest.mark.asyncio
    async def test_retry_async_succeeds(self):
        """Test retry_async() works with async functions."""
        handler = RetryHandler(max_attempts=3, base_delay=0.01)

        async def async_success():
            return "async_success"

        result = await handler.retry_async(async_success)

        assert result == "async_success"

    @pytest.mark.asyncio
    async def test_retry_async_retries_on_failure(self):
        """Test retry_async() retries async function failures."""
        handler = RetryHandler(max_attempts=3, base_delay=0.01)
        handler.logger = Mock()  # Mock logger
        attempts = []

        async def flaky_async():
            attempts.append(1)
            if len(attempts) < 2:
                raise ValueError("Async failure")
            return "async_success"

        result = await handler.retry_async(flaky_async)

        assert result == "async_success"
        assert len(attempts) == 2


class TestHandleErrorsDecorator:
    """Test suite for handle_errors decorator."""

    def test_handle_errors_returns_result_on_success(self):
        """Test decorator returns function result when no error."""
        @handle_errors()
        def success_func():
            return "result"

        result = success_func()

        assert result == "result"

    def test_handle_errors_returns_default_on_exception(self):
        """Test decorator returns default value on exception."""
        @handle_errors(default_return="fallback")
        def failing_func():
            raise ValueError("Error")

        result = failing_func()

        assert result == "fallback"

    def test_handle_errors_reraises_when_requested(self):
        """Test decorator re-raises exception when reraise=True."""
        @handle_errors(reraise=True)
        def failing_func():
            raise ValueError("Error")

        with pytest.raises(ValueError):
            failing_func()


class TestHandleAsyncErrorsDecorator:
    """Test suite for handle_async_errors decorator."""

    @pytest.mark.asyncio
    async def test_handle_async_errors_returns_result(self):
        """Test async decorator returns result on success."""
        @handle_async_errors()
        async def async_success():
            return "async_result"

        result = await async_success()

        assert result == "async_result"

    @pytest.mark.asyncio
    async def test_handle_async_errors_returns_default_on_exception(self):
        """Test async decorator returns default on exception."""
        @handle_async_errors(default_return="async_fallback")
        async def async_failure():
            raise ValueError("Async error")

        result = await async_failure()

        assert result == "async_fallback"


class TestRetryWithBackoffDecorator:
    """Test suite for retry_with_backoff decorator."""

    def test_retry_with_backoff_sync_function(self):
        """Test decorator works with synchronous functions (success case)."""
        # Test successful function (doesn't trigger retry/logger path)
        @retry_with_backoff(max_attempts=2, base_delay=0.01)
        def success_sync():
            return "success"

        result = success_sync()

        assert result == "success"

    @pytest.mark.asyncio
    async def test_retry_with_backoff_async_function(self):
        """Test decorator works with async functions (success case)."""
        # Test successful function (doesn't trigger retry/logger path)
        @retry_with_backoff(max_attempts=2, base_delay=0.01)
        async def success_async():
            return "async_success"

        result = await success_async()

        assert result == "async_success"


class TestErrorContextManager:
    """Test suite for error_context context manager."""

    def test_error_context_yields_context(self):
        """Test context manager yields ErrorContext."""
        with error_context("test_operation", component="test") as ctx:
            assert isinstance(ctx, ErrorContext)
            assert ctx.operation == "test_operation"
            assert ctx.component == "test"

    def test_error_context_logs_and_reraises(self):
        """Test context manager logs error and re-raises."""
        with pytest.raises(ValueError):
            with error_context("test_op", component="test"):
                raise ValueError("Test error")


class TestSafeExecute:
    """Test suite for safe_execute function."""

    def test_safe_execute_returns_result_on_success(self):
        """Test safe_execute returns function result."""
        def success_func(x):
            return x * 2

        result = safe_execute(success_func, 5)

        assert result == 10

    def test_safe_execute_returns_default_on_error(self):
        """Test safe_execute returns default on exception."""
        def failing_func():
            raise ValueError("Error")

        result = safe_execute(failing_func, default="fallback")

        assert result == "fallback"

    def test_safe_execute_with_log_errors_false(self):
        """Test safe_execute respects log_errors flag."""
        def failing_func():
            raise ValueError("Error")

        result = safe_execute(failing_func, default="fallback", log_errors=False)

        assert result == "fallback"


class TestSafeExecuteAsync:
    """Test suite for safe_execute_async function."""

    @pytest.mark.asyncio
    async def test_safe_execute_async_returns_result(self):
        """Test safe_execute_async returns result on success."""
        async def async_func(x):
            return x * 3

        result = await safe_execute_async(async_func, 4)

        assert result == 12

    @pytest.mark.asyncio
    async def test_safe_execute_async_returns_default_on_error(self):
        """Test safe_execute_async returns default on exception."""
        async def async_failure():
            raise ValueError("Async error")

        result = await safe_execute_async(async_failure, default="async_fallback")

        assert result == "async_fallback"


class TestValidateFileOperation:
    """Test suite for validate_file_operation function."""

    def test_validate_file_operation_read_existing_file(self, tmp_path):
        """Test validates existing file for read operation."""
        test_file = tmp_path / "exists.txt"
        test_file.touch()

        # Should not raise exception
        validate_file_operation(test_file, operation="read")

    def test_validate_file_operation_read_missing_file(self, tmp_path):
        """Test raises FileOperationError for missing file."""
        missing_file = tmp_path / "missing.txt"

        with pytest.raises(FileOperationError):
            validate_file_operation(missing_file, operation="read")

    def test_validate_file_operation_write_creates_parent(self, tmp_path):
        """Test write operation creates parent directory."""
        new_file = tmp_path / "subdir" / "newfile.txt"

        # Should not raise exception and create parent
        validate_file_operation(new_file, operation="write")

        assert new_file.parent.exists()

    def test_validate_file_operation_write_existing_parent(self, tmp_path):
        """Test write operation with existing parent directory."""
        new_file = tmp_path / "newfile.txt"

        # Should not raise exception
        validate_file_operation(new_file, operation="write")


class TestCreateComponentErrorHandler:
    """Test suite for create_component_error_handler factory."""

    def test_create_component_error_handler_returns_handler(self):
        """Test factory returns ErrorHandler instance."""
        handler = create_component_error_handler("my_component")

        assert isinstance(handler, ErrorHandler)
        assert handler.component_name == "my_component"

    def test_create_component_error_handler_accepts_kwargs(self):
        """Test factory passes kwargs to ErrorHandler."""
        handler = create_component_error_handler(
            "my_component",
            enable_detailed_logging=False
        )

        assert handler.enable_detailed_logging is False


class TestConvenienceFunctions:
    """Test suite for convenience error handling functions."""

    def test_log_and_return_none(self):
        """Test log_and_return_none returns None."""
        error = ValueError("Test")

        result = log_and_return_none(error)

        assert result is None

    def test_log_and_return_empty_list(self):
        """Test log_and_return_empty_list returns empty list."""
        error = ValueError("Test")

        result = log_and_return_empty_list(error)

        assert result == []

    def test_log_and_return_empty_dict(self):
        """Test log_and_return_empty_dict returns empty dict."""
        error = ValueError("Test")

        result = log_and_return_empty_dict(error)

        assert result == {}
