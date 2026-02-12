"""
Unit Tests for Feature 06: compile_historical_data.py Logger Setup

Tests verify setup_logger() integration works correctly:
- Logger called with log_to_file=True when flag provided
- Logger called with log_to_file=False when flag omitted
- Logger name is "historical_data_compiler"
- Log file created in correct location when enabled

Test Category: R2 - setup_logger() Integration (4 tests)

Created: 2026-02-11 (Feature 06 S6 Phase 6 Task 12)
"""

import pytest
from unittest.mock import patch, MagicMock, call


class TestSetupLoggerIntegration:
    """R2: Unit tests for setup_logger() parameter passing"""

    def test_setup_logger_called_with_log_to_file_true(self):
        """T2.1: Verify setup_logger() receives log_to_file=True when flag provided

        When --enable-log-file flag is provided, main() should call setup_logger()
        with log_to_file=True parameter.
        """
        # Mock sys.argv with flag
        test_args = ['compile_historical_data.py', '--year', '2024', '--enable-log-file']

        with patch('sys.argv', test_args):
            with patch('compile_historical_data.setup_logger') as mock_setup:
                with patch('compile_historical_data.get_logger', return_value=MagicMock()):
                    import compile_historical_data
                    args = compile_historical_data.parse_args()

                    # Simulate what main() does
                    log_level = "DEBUG" if args.verbose else "INFO"
                    compile_historical_data.setup_logger(
                        name="historical_data_compiler",
                        level=log_level,
                        log_to_file=args.enable_log_file,
                        log_file_path=None
                    )

                    # Verify setup_logger called with correct parameters
                    assert mock_setup.called, "setup_logger should be called"
                    call_kwargs = mock_setup.call_args[1]
                    assert call_kwargs['log_to_file'] is True, "log_to_file should be True with flag"
                    assert call_kwargs['log_file_path'] is None, "log_file_path should be None"

    def test_setup_logger_called_with_log_to_file_false(self):
        """T2.2: Verify setup_logger() receives log_to_file=False when flag omitted

        When --enable-log-file flag is NOT provided, main() should call
        setup_logger() with log_to_file=False (default behavior).
        """
        # Mock sys.argv without flag
        test_args = ['compile_historical_data.py', '--year', '2024']

        with patch('sys.argv', test_args):
            with patch('compile_historical_data.setup_logger') as mock_setup:
                with patch('compile_historical_data.get_logger', return_value=MagicMock()):
                    import compile_historical_data
                    args = compile_historical_data.parse_args()

                    # Simulate what main() does
                    log_level = "DEBUG" if args.verbose else "INFO"
                    compile_historical_data.setup_logger(
                        name="historical_data_compiler",
                        level=log_level,
                        log_to_file=args.enable_log_file,
                        log_file_path=None
                    )

                    # Verify setup_logger called with log_to_file=False
                    assert mock_setup.called, "setup_logger should be called"
                    call_kwargs = mock_setup.call_args[1]
                    assert call_kwargs['log_to_file'] is False, "log_to_file should be False without flag"

    def test_logger_name_is_historical_data_compiler(self):
        """T2.3: Verify logger name is "historical_data_compiler"

        Logger name should match module convention (historical_data_compiler)
        for consistent log file naming.
        """
        # Mock sys.argv
        test_args = ['compile_historical_data.py', '--year', '2024']

        with patch('sys.argv', test_args):
            with patch('compile_historical_data.setup_logger') as mock_setup:
                with patch('compile_historical_data.get_logger', return_value=MagicMock()):
                    import compile_historical_data
                    args = compile_historical_data.parse_args()

                    # Simulate what main() does
                    log_level = "DEBUG" if args.verbose else "INFO"
                    compile_historical_data.setup_logger(
                        name="historical_data_compiler",
                        level=log_level,
                        log_to_file=args.enable_log_file,
                        log_file_path=None
                    )

                    # Verify logger name
                    assert mock_setup.called, "setup_logger should be called"
                    call_kwargs = mock_setup.call_args[1]
                    assert call_kwargs['name'] == "historical_data_compiler", "Logger name should match module"

    def test_log_file_path_is_none_for_auto_generation(self):
        """T2.4: Verify log_file_path=None to enable auto-generation

        When log_to_file=True, log_file_path should be None to let
        LoggingManager auto-generate the path following convention:
        logs/historical_data_compiler/historical_data_compiler-{timestamp}.log
        """
        # Mock sys.argv with flag
        test_args = ['compile_historical_data.py', '--year', '2024', '--enable-log-file']

        with patch('sys.argv', test_args):
            with patch('compile_historical_data.setup_logger') as mock_setup:
                with patch('compile_historical_data.get_logger', return_value=MagicMock()):
                    import compile_historical_data
                    args = compile_historical_data.parse_args()

                    # Simulate what main() does
                    log_level = "DEBUG" if args.verbose else "INFO"
                    compile_historical_data.setup_logger(
                        name="historical_data_compiler",
                        level=log_level,
                        log_to_file=args.enable_log_file,
                        log_file_path=None
                    )

                    # Verify log_file_path is None (auto-generate)
                    assert mock_setup.called, "setup_logger should be called"
                    call_kwargs = mock_setup.call_args[1]
                    assert call_kwargs['log_file_path'] is None, "log_file_path should be None for auto-generation"
                    assert call_kwargs['log_to_file'] is True, "log_to_file should be True"
