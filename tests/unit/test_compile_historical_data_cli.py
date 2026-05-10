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
        test_args = ['compile_historical_data.py', '--year', '2024', '--enable-log-file']

        with patch('sys.argv', test_args):
            import compile_historical_data
            args = compile_historical_data.parse_args()

            assert args.enable_log_file is True, "Flag should be True when --enable-log-file provided"
            assert args.year == 2024, "Year should be parsed correctly"

    def test_flag_parsing_without_flag_default(self):
        """T1.2: Verify args.enable_log_file defaults to False when flag omitted

        When user does NOT provide --enable-log-file flag, argument parser
        should default enable_log_file to False (file logging disabled).
        """
        test_args = ['compile_historical_data.py', '--year', '2024']

        with patch('sys.argv', test_args):
            import compile_historical_data
            args = compile_historical_data.parse_args()

            assert args.enable_log_file is False, "Flag should default to False when not provided"
            assert args.year == 2024, "Year should be parsed correctly"

    def test_help_text_includes_flag(self, capsys):
        """T1.3: Verify help text contains flag description

        Help output should document the --enable-log-file flag with clear
        description of its purpose.
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


class TestNewCLIFlags:
    """Tests for --format, --keep-partial, --all-years, --weeks CLI flags (R7)."""

    def test_format_csv(self):
        with patch('sys.argv', ['compile_historical_data.py', '--year', '2024', '--format', 'csv']):
            import compile_historical_data
            args = compile_historical_data.parse_args()
            assert args.format == 'csv'

    def test_format_json(self):
        with patch('sys.argv', ['compile_historical_data.py', '--year', '2024', '--format', 'json']):
            import compile_historical_data
            args = compile_historical_data.parse_args()
            assert args.format == 'json'

    def test_format_both(self):
        with patch('sys.argv', ['compile_historical_data.py', '--year', '2024', '--format', 'both']):
            import compile_historical_data
            args = compile_historical_data.parse_args()
            assert args.format == 'both'

    def test_format_default_is_json(self):
        with patch('sys.argv', ['compile_historical_data.py', '--year', '2024']):
            import compile_historical_data
            args = compile_historical_data.parse_args()
            assert args.format == 'json'

    def test_keep_partial_true(self):
        with patch('sys.argv', ['compile_historical_data.py', '--year', '2024', '--keep-partial']):
            import compile_historical_data
            args = compile_historical_data.parse_args()
            assert args.keep_partial is True

    def test_keep_partial_default_false(self):
        with patch('sys.argv', ['compile_historical_data.py', '--year', '2024']):
            import compile_historical_data
            args = compile_historical_data.parse_args()
            assert args.keep_partial is False

    def test_all_years_flag(self):
        with patch('sys.argv', ['compile_historical_data.py', '--all-years']):
            import compile_historical_data
            args = compile_historical_data.parse_args()
            assert args.all_years is True

    def test_all_years_and_year_mutually_exclusive(self):
        with patch('sys.argv', ['compile_historical_data.py', '--all-years', '--year', '2024']):
            import compile_historical_data
            with pytest.raises(SystemExit):
                compile_historical_data.parse_args()

    def test_weeks_flag(self):
        with patch('sys.argv', ['compile_historical_data.py', '--year', '2024', '--weeks', '3']):
            import compile_historical_data
            args = compile_historical_data.parse_args()
            assert args.weeks == 3

    def test_neither_year_nor_all_years_raises_error(self):
        with patch('sys.argv', ['compile_historical_data.py']):
            import compile_historical_data
            with pytest.raises(SystemExit):
                compile_historical_data.parse_args()
