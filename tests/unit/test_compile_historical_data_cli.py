"""
Unit Tests for Feature 06: compile_historical_data.py CLI Flag

Tests verify --enable-log-file flag works correctly:
- Flag parsing with flag provided
- Flag parsing without flag (default False)
- Help text includes flag documentation

Test Category: R1 - CLI Flag Integration (3 tests)

Created: 2026-02-11 (Feature 06 S6 Phase 6 Task 11)
"""

import pytest
from unittest.mock import patch


class TestCLIFlagParsing:
    """R1: Unit tests for --enable-log-file CLI flag"""

    def test_flag_parsing_with_enable_log_file(self):
        """T1.1: Verify --enable-log-file sets args.enable_log_file=True

        When user provides --enable-log-file flag, argument parser should
        set enable_log_file attribute to True.
        """
        # Mock sys.argv with flag
        test_args = ['compile_historical_data.py', '--year', '2024', '--enable-log-file']

        with patch('sys.argv', test_args):
            import compile_historical_data
            args = compile_historical_data.parse_args()

            # Verify flag parsed correctly
            assert args.enable_log_file is True, "Flag should be True when --enable-log-file provided"
            assert args.year == 2024, "Year should be parsed correctly"

    def test_flag_parsing_without_flag_default(self):
        """T1.2: Verify args.enable_log_file defaults to False when flag omitted

        When user does NOT provide --enable-log-file flag, argument parser
        should default enable_log_file to False (file logging disabled).
        """
        # Mock sys.argv without flag
        test_args = ['compile_historical_data.py', '--year', '2024']

        with patch('sys.argv', test_args):
            import compile_historical_data
            args = compile_historical_data.parse_args()

            # Verify flag defaults to False
            assert args.enable_log_file is False, "Flag should default to False when not provided"
            assert args.year == 2024, "Year should be parsed correctly"

    def test_help_text_includes_flag(self, capsys):
        """T1.3: Verify help text contains flag description

        Help output should document the --enable-log-file flag with clear
        description of its purpose.
        """
        # Mock sys.argv for help
        test_args = ['compile_historical_data.py', '--help']

        with patch('sys.argv', test_args):
            import compile_historical_data

            # Capture help output (argparse raises SystemExit)
            try:
                compile_historical_data.parse_args()
            except SystemExit:
                pass  # Expected - argparse exits after showing help

            # Get captured output
            captured = capsys.readouterr()
            help_text = captured.out

            # Verify flag in help
            assert '--enable-log-file' in help_text, "Help should show --enable-log-file flag"
            assert 'Enable file logging' in help_text, "Help should describe flag purpose"
