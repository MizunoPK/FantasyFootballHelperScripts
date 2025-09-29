#!/usr/bin/env python3
"""
Unit tests for error_handler.py

Tests all functionality of the standardized error handling and recovery system.
"""

import asyncio
import logging
import pytest
import tempfile
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from shared_files.error_handler import (
    ErrorContext, ErrorHandler, RetryHandler, FantasyFootballError,
    DataProcessingError, APIError, FileOperationError, ConfigurationError,
    handle_errors, handle_async_errors, retry_with_backoff, error_context,
    safe_execute, safe_execute_async, validate_file_operation,
    create_component_error_handler, log_and_return_none,
    log_and_return_empty_list, log_and_return_empty_dict
)


class TestErrorContext:
    """Test ErrorContext class functionality"""

    def test_error_context_creation(self):
        """Test basic ErrorContext creation"""
        context = ErrorContext(
            operation="test_operation",
            component="test_component",
            file_path="/test/path",
            player_id="player123"
        )

        assert context.operation == "test_operation"
        assert context.component == "test_component"
        assert context.file_path == "/test/path"
        assert context.player_id == "player123"
        assert isinstance(context.additional_context, dict)

    def test_error_context_to_dict(self):
        """Test ErrorContext conversion to dictionary"""
        context = ErrorContext(
            operation="test_op",
            component="test_comp",
            additional_context={"key": "value"}
        )

        result = context.to_dict()

        assert result["operation"] == "test_op"
        assert result["component"] == "test_comp"
        assert result["additional_context"] == {"key": "value"}
        assert "timestamp" in result

    def test_error_context_defaults(self):
        """Test ErrorContext with minimal parameters"""
        context = ErrorContext(operation="test", component="test")

        assert context.operation == "test"
        assert context.component == "test"
        assert context.file_path is None
        assert context.player_id is None
        assert context.additional_context == {}


class TestFantasyFootballExceptions:
    """Test custom exception classes"""

    def test_fantasy_football_error_basic(self):
        """Test basic FantasyFootballError"""
        error = FantasyFootballError("Test error message")

        assert str(error) == "Test error message"
        assert error.message == "Test error message"
        assert error.context is None
        assert error.original_exception is None

    def test_fantasy_football_error_with_context(self):
        """Test FantasyFootballError with context"""
        context = ErrorContext(operation="test_op", component="test_comp")
        error = FantasyFootballError("Test error", context=context)

        error_str = str(error)
        assert "Test error" in error_str
        assert "[Component: test_comp, Operation: test_op]" in error_str

    def test_fantasy_football_error_with_original_exception(self):
        """Test FantasyFootballError with original exception"""
        original = ValueError("Original error")
        error = FantasyFootballError("Wrapper error", original_exception=original)

        error_str = str(error)
        assert "Wrapper error" in error_str
        assert "[Original: ValueError: Original error]" in error_str

    def test_custom_exception_types(self):
        """Test all custom exception types inherit correctly"""
        assert issubclass(DataProcessingError, FantasyFootballError)
        assert issubclass(APIError, FantasyFootballError)
        assert issubclass(FileOperationError, FantasyFootballError)
        assert issubclass(ConfigurationError, FantasyFootballError)

        # Test they can be instantiated
        data_error = DataProcessingError("Data error")
        api_error = APIError("API error")
        file_error = FileOperationError("File error")
        config_error = ConfigurationError("Config error")

        assert isinstance(data_error, FantasyFootballError)
        assert isinstance(api_error, FantasyFootballError)
        assert isinstance(file_error, FantasyFootballError)
        assert isinstance(config_error, FantasyFootballError)


class TestErrorHandler:
    """Test ErrorHandler class functionality"""

    def test_error_handler_creation(self):
        """Test ErrorHandler initialization"""
        handler = ErrorHandler("test_component", enable_detailed_logging=False)

        assert handler.component_name == "test_component"
        assert handler.enable_detailed_logging is False
        assert handler.error_counts == {}

    @patch('shared_files.error_handler.setup_module_logging')
    def test_log_error_basic(self, mock_setup_logging):
        """Test basic error logging"""
        mock_logger = Mock()
        mock_setup_logging.return_value = mock_logger

        handler = ErrorHandler("test_component")
        test_error = ValueError("Test error")

        handler.log_error(test_error)

        # Check error was logged
        mock_logger.error.assert_called_once()

        # Check error count tracking
        assert handler.error_counts["ValueError"] == 1

    @patch('shared_files.error_handler.setup_module_logging')
    def test_log_error_with_context(self, mock_setup_logging):
        """Test error logging with context"""
        mock_logger = Mock()
        mock_setup_logging.return_value = mock_logger

        handler = ErrorHandler("test_component", enable_detailed_logging=True)
        test_error = ValueError("Test error")
        context = ErrorContext(operation="test_op", component="test_comp")

        handler.log_error(test_error, context)

        # Verify logger was called
        mock_logger.error.assert_called_once()

        # Check the logged message includes context
        call_args = mock_logger.error.call_args[0][0]
        assert "test_op" in call_args
        assert "test_comp" in call_args

    def test_handle_error_with_reraise(self):
        """Test error handling with reraise=True"""
        handler = ErrorHandler("test_component")
        test_error = ValueError("Test error")

        with pytest.raises(ValueError):
            handler.handle_error(test_error, reraise=True)

    def test_handle_error_with_default_return(self):
        """Test error handling with default return value"""
        handler = ErrorHandler("test_component")
        test_error = ValueError("Test error")

        result = handler.handle_error(test_error, default_return="fallback")

        assert result == "fallback"

    def test_create_context(self):
        """Test context creation"""
        handler = ErrorHandler("test_component")

        context = handler.create_context(
            "test_operation",
            file_path="/test/path",
            player_id="player123",
            custom_field="custom_value"
        )

        assert context.operation == "test_operation"
        assert context.component == "test_component"
        assert context.file_path == "/test/path"
        assert context.player_id == "player123"
        assert context.additional_context["custom_field"] == "custom_value"

    def test_error_summary_and_reset(self):
        """Test error count tracking and reset"""
        handler = ErrorHandler("test_component")

        # Generate some errors
        handler.log_error(ValueError("Error 1"))
        handler.log_error(ValueError("Error 2"))
        handler.log_error(TypeError("Error 3"))

        summary = handler.get_error_summary()
        assert summary["ValueError"] == 2
        assert summary["TypeError"] == 1

        # Test reset
        handler.reset_error_counts()
        assert handler.get_error_summary() == {}


class TestRetryHandler:
    """Test RetryHandler class functionality"""

    def test_retry_handler_initialization(self):
        """Test RetryHandler initialization"""
        handler = RetryHandler(
            max_attempts=5,
            base_delay=2.0,
            max_delay=30.0,
            backoff_factor=3.0
        )

        assert handler.max_attempts == 5
        assert handler.base_delay == 2.0
        assert handler.max_delay == 30.0
        assert handler.backoff_factor == 3.0

    def test_calculate_delay(self):
        """Test delay calculation for exponential backoff"""
        handler = RetryHandler(base_delay=1.0, max_delay=10.0, backoff_factor=2.0)

        assert handler.calculate_delay(0) == 1.0  # 1.0 * 2^0
        assert handler.calculate_delay(1) == 2.0  # 1.0 * 2^1
        assert handler.calculate_delay(2) == 4.0  # 1.0 * 2^2
        assert handler.calculate_delay(10) == 10.0  # Capped at max_delay

    def test_retry_sync_success(self):
        """Test successful sync retry"""
        handler = RetryHandler(max_attempts=3, base_delay=0.01)

        def successful_function(x, y):
            return x + y

        result = handler.retry_sync(successful_function, 5, 3)
        assert result == 8

    def test_retry_sync_failure_then_success(self):
        """Test sync retry with initial failures"""
        handler = RetryHandler(max_attempts=3, base_delay=0.01)
        call_count = 0

        def flaky_function():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise RuntimeError(f"Failure {call_count}")
            return "success"

        result = handler.retry_sync(flaky_function)
        assert result == "success"
        assert call_count == 3

    def test_retry_sync_all_failures(self):
        """Test sync retry when all attempts fail"""
        handler = RetryHandler(max_attempts=2, base_delay=0.01)

        def always_fails():
            raise RuntimeError("Always fails")

        with pytest.raises(RuntimeError, match="Always fails"):
            handler.retry_sync(always_fails)

    @pytest.mark.asyncio
    async def test_retry_async_success(self):
        """Test successful async retry"""
        handler = RetryHandler(max_attempts=3, base_delay=0.01)

        async def successful_async_function(x, y):
            return x * y

        result = await handler.retry_async(successful_async_function, 4, 5)
        assert result == 20

    @pytest.mark.asyncio
    async def test_retry_async_failure_then_success(self):
        """Test async retry with initial failures"""
        handler = RetryHandler(max_attempts=3, base_delay=0.01)
        call_count = 0

        async def flaky_async_function():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise RuntimeError(f"Async failure {call_count}")
            return "async_success"

        result = await handler.retry_async(flaky_async_function)
        assert result == "async_success"
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_retry_async_all_failures(self):
        """Test async retry when all attempts fail"""
        handler = RetryHandler(max_attempts=2, base_delay=0.01)

        async def always_fails_async():
            raise RuntimeError("Always fails async")

        with pytest.raises(RuntimeError, match="Always fails async"):
            await handler.retry_async(always_fails_async)


class TestDecorators:
    """Test error handling decorators"""

    def test_handle_errors_decorator_success(self):
        """Test handle_errors decorator with successful function"""
        @handle_errors(default_return="fallback", component="test")
        def successful_function(x):
            return x * 2

        result = successful_function(5)
        assert result == 10

    def test_handle_errors_decorator_with_exception(self):
        """Test handle_errors decorator with exception"""
        @handle_errors(default_return="fallback", reraise=False, component="test")
        def failing_function():
            raise ValueError("Test error")

        result = failing_function()
        assert result == "fallback"

    def test_handle_errors_decorator_with_reraise(self):
        """Test handle_errors decorator with reraise=True"""
        @handle_errors(reraise=True, component="test")
        def failing_function():
            raise ValueError("Test error")

        with pytest.raises(ValueError):
            failing_function()

    @pytest.mark.asyncio
    async def test_handle_async_errors_decorator_success(self):
        """Test handle_async_errors decorator with successful function"""
        @handle_async_errors(default_return="async_fallback", component="test")
        async def successful_async_function(x):
            return x * 3

        result = await successful_async_function(4)
        assert result == 12

    @pytest.mark.asyncio
    async def test_handle_async_errors_decorator_with_exception(self):
        """Test handle_async_errors decorator with exception"""
        @handle_async_errors(default_return="async_fallback", reraise=False, component="test")
        async def failing_async_function():
            raise ValueError("Async test error")

        result = await failing_async_function()
        assert result == "async_fallback"

    def test_retry_with_backoff_decorator_success(self):
        """Test retry_with_backoff decorator with successful function"""
        @retry_with_backoff(max_attempts=3, base_delay=0.01)
        def successful_function(x):
            return x + 10

        result = successful_function(5)
        assert result == 15

    def test_retry_with_backoff_decorator_with_retries(self):
        """Test retry_with_backoff decorator with eventual success"""
        call_count = 0

        @retry_with_backoff(max_attempts=3, base_delay=0.01)
        def flaky_function():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise RuntimeError(f"Failure {call_count}")
            return "success"

        result = flaky_function()
        assert result == "success"
        assert call_count == 3

    @pytest.mark.asyncio
    async def test_retry_with_backoff_decorator_async(self):
        """Test retry_with_backoff decorator with async function"""
        call_count = 0

        @retry_with_backoff(max_attempts=2, base_delay=0.01)
        async def flaky_async_function():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise RuntimeError(f"Async failure {call_count}")
            return "async_success"

        result = await flaky_async_function()
        assert result == "async_success"
        assert call_count == 2


class TestContextManager:
    """Test error_context context manager"""

    def test_error_context_success(self):
        """Test error_context with successful operation"""
        with error_context("test_operation", component="test_comp") as context:
            result = "success"

        assert context.operation == "test_operation"
        assert context.component == "test_comp"
        assert result == "success"

    def test_error_context_with_exception(self):
        """Test error_context with exception (should re-raise)"""
        with pytest.raises(ValueError, match="Test error"):
            with error_context("test_operation", component="test_comp"):
                raise ValueError("Test error")

    def test_error_context_with_additional_kwargs(self):
        """Test error_context with additional context"""
        with error_context("test_op", component="test_comp",
                          file_path="/test", custom="value") as context:
            pass

        assert context.additional_context["file_path"] == "/test"
        assert context.additional_context["custom"] == "value"


class TestSafeExecution:
    """Test safe execution functions"""

    def test_safe_execute_success(self):
        """Test safe_execute with successful function"""
        def successful_function(x, y):
            return x + y

        result = safe_execute(successful_function, 3, 4, default="fallback")
        assert result == 7

    def test_safe_execute_with_exception(self):
        """Test safe_execute with exception"""
        def failing_function():
            raise ValueError("Test error")

        result = safe_execute(failing_function, default="fallback")
        assert result == "fallback"

    def test_safe_execute_no_logging(self):
        """Test safe_execute with log_errors=False"""
        def failing_function():
            raise ValueError("Test error")

        result = safe_execute(failing_function, default="fallback", log_errors=False)
        assert result == "fallback"

    @pytest.mark.asyncio
    async def test_safe_execute_async_success(self):
        """Test safe_execute_async with successful function"""
        async def successful_async_function(x, y):
            return x * y

        result = await safe_execute_async(successful_async_function, 3, 4, default="fallback")
        assert result == 12

    @pytest.mark.asyncio
    async def test_safe_execute_async_with_exception(self):
        """Test safe_execute_async with exception"""
        async def failing_async_function():
            raise ValueError("Async test error")

        result = await safe_execute_async(failing_async_function, default="async_fallback")
        assert result == "async_fallback"


class TestFileValidation:
    """Test file operation validation"""

    def test_validate_file_operation_existing_file_read(self):
        """Test validation for reading existing file"""
        with tempfile.NamedTemporaryFile() as temp_file:
            # Should not raise exception
            validate_file_operation(temp_file.name, "read")

    def test_validate_file_operation_missing_file_read(self):
        """Test validation for reading missing file"""
        with pytest.raises(FileOperationError, match="File not found"):
            validate_file_operation("/nonexistent/file.txt", "read")

    def test_validate_file_operation_write_new_file(self):
        """Test validation for writing new file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "new_file.txt"

            # Should not raise exception
            validate_file_operation(file_path, "write")

    def test_validate_file_operation_write_create_directory(self):
        """Test validation for writing to new directory"""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "new_subdir" / "new_file.txt"

            # Should create directory and not raise exception
            validate_file_operation(file_path, "write")

            # Verify directory was created
            assert file_path.parent.exists()
            assert file_path.parent.is_dir()


class TestConvenienceFunctions:
    """Test convenience functions"""

    def test_create_component_error_handler(self):
        """Test error handler factory function"""
        handler = create_component_error_handler("test_comp", enable_detailed_logging=False)

        assert isinstance(handler, ErrorHandler)
        assert handler.component_name == "test_comp"
        assert handler.enable_detailed_logging is False

    def test_log_and_return_none(self):
        """Test log_and_return_none convenience function"""
        error = ValueError("Test error")
        result = log_and_return_none(error)

        assert result is None

    def test_log_and_return_empty_list(self):
        """Test log_and_return_empty_list convenience function"""
        error = ValueError("Test error")
        result = log_and_return_empty_list(error)

        assert result == []
        assert isinstance(result, list)

    def test_log_and_return_empty_dict(self):
        """Test log_and_return_empty_dict convenience function"""
        error = ValueError("Test error")
        result = log_and_return_empty_dict(error)

        assert result == {}
        assert isinstance(result, dict)


class TestIntegration:
    """Test integration scenarios combining multiple features"""

    def test_error_handler_with_retry_decorator(self):
        """Test combining error handler with retry decorator"""
        handler = ErrorHandler("integration_test")
        call_count = 0

        @retry_with_backoff(max_attempts=3, base_delay=0.01)
        def flaky_function_with_logging():
            nonlocal call_count
            call_count += 1

            try:
                if call_count < 3:
                    raise RuntimeError(f"Failure {call_count}")
                return "success"
            except Exception as e:
                context = handler.create_context("flaky_operation")
                handler.log_error(e, context, severity="DEBUG")
                raise

        result = flaky_function_with_logging()
        assert result == "success"
        assert call_count == 3
        assert handler.get_error_summary()["RuntimeError"] == 2

    @pytest.mark.asyncio
    async def test_comprehensive_async_error_handling(self):
        """Test comprehensive async error handling scenario"""
        handler = ErrorHandler("async_integration")

        @handle_async_errors(default_return="fallback", component="async_test")
        @retry_with_backoff(max_attempts=2, base_delay=0.01)
        async def complex_async_operation(data):
            if data == "fail":
                raise APIError("API connection failed")
            elif data == "retry":
                # This will be retried but still fail
                raise RuntimeError("Temporary failure")
            return f"processed_{data}"

        # Test success case
        result1 = await complex_async_operation("success")
        assert result1 == "processed_success"

        # Test failure case (should return fallback due to handle_async_errors)
        result2 = await complex_async_operation("fail")
        assert result2 == "fallback"

    def test_error_context_with_file_operations(self):
        """Test error context with file operation validation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "test_file.txt"

            with error_context("file_processing", component="file_handler",
                              file_path=str(file_path)) as context:

                # This should work
                validate_file_operation(file_path, "write")

                # Create the file
                file_path.write_text("test content")

                # This should also work
                validate_file_operation(file_path, "read")

            assert context.additional_context["file_path"] == str(file_path)


if __name__ == "__main__":
    # Run tests if script is executed directly
    pytest.main([__file__, "-v"])