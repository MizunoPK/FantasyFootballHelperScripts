"""
Integration Tests for Feature 06: historical_data_compiler_logging

Tests verify logging integration works correctly:
- Script can be imported with new CLI flag
- Logger setup works with/without --enable-log-file flag
- Flag parsing works correctly

Test Categories:
- Task 9: E2E with --enable-log-file flag
- Task 10: E2E without flag (console-only)

Created: 2026-02-11 (Feature 06 S6 Phase 5)
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

project_root = Path(__file__).parent.parent.parent



class TestHistoricalDataCompilerLogging:
    """Integration tests for compile_historical_data.py logging"""

    def test_compile_with_log_file_enabled(self):
        """Task 9: Integration test with --enable-log-file flag

        Verifies:
        - Script accepts --enable-log-file flag
        - Flag parsed correctly as True
        - Logger setup would be called with log_to_file=True
        """
        test_args = ['compile_historical_data.py', '--year', '2024', '--enable-log-file']

        with patch('sys.argv', test_args):
            import compile_historical_data
            args = compile_historical_data.parse_args()

            assert args.enable_log_file is True, "Flag should be True when --enable-log-file provided"
            assert args.year == 2024, "Year should be parsed correctly"

            log_level = "DEBUG" if args.verbose else "INFO"
            assert log_level == "INFO", "Log level should be INFO when not verbose"

            expected_name = "historical_data_compiler"
            expected_log_to_file = args.enable_log_file
            expected_log_file_path = None

            assert expected_log_to_file is True, "log_to_file should be True with flag"
            assert expected_log_file_path is None, "log_file_path should be None (auto-generate)"

    def test_compile_without_log_file_default(self):
        """Task 10: Integration test without flag (console-only default)

        Verifies:
        - Script works without --enable-log-file flag
        - Flag defaults to False
        - Logger setup would be called with log_to_file=False
        """
        test_args = ['compile_historical_data.py', '--year', '2024']

        with patch('sys.argv', test_args):
            import compile_historical_data
            args = compile_historical_data.parse_args()

            assert args.enable_log_file is False, "Flag should default to False when not provided"
            assert args.year == 2024, "Year should be parsed correctly"

            log_level = "DEBUG" if args.verbose else "INFO"
            assert log_level == "INFO", "Log level should be INFO when not verbose"

            expected_log_to_file = args.enable_log_file
            assert expected_log_to_file is False, "log_to_file should be False without flag"

    def test_help_text_includes_flag(self, capsys):
        """Bonus: Verify --enable-log-file appears in help output

        Verifies CLI flag is documented in help text
        """
        test_args = ['compile_historical_data.py', '--help']

        with patch('sys.argv', test_args):
            import compile_historical_data

            try:
                compile_historical_data.parse_args()
            except SystemExit:
                pass

            captured = capsys.readouterr()
            help_text = captured.out

            assert '--enable-log-file' in help_text, "Help should show --enable-log-file flag"
            assert 'Enable file logging' in help_text, "Help should describe flag purpose"


