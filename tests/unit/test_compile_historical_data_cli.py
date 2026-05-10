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
from unittest.mock import patch, MagicMock


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
    """Tests for --format, --keep-partial, --all-years, --weeks CLI flags."""

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

    def test_weeks_zero_raises_error(self):
        with patch('sys.argv', ['compile_historical_data.py', '--year', '2024', '--weeks', '0']):
            import compile_historical_data
            with pytest.raises(SystemExit):
                compile_historical_data.parse_args()

    def test_weeks_negative_raises_error(self):
        with patch('sys.argv', ['compile_historical_data.py', '--year', '2024', '--weeks', '-3']):
            import compile_historical_data
            with pytest.raises(SystemExit):
                compile_historical_data.parse_args()


class TestWeeksPropagation:
    """Tests verifying max_weeks flows through compile_season_data to all downstream callers."""

    def test_weeks_propagated_to_all_phases(self):
        import compile_historical_data
        from unittest.mock import AsyncMock

        mock_http = MagicMock()
        mock_http.close = AsyncMock()

        with patch('sys.argv', ['compile_historical_data.py', '--year', '2024', '--weeks', '3']), \
             patch('compile_historical_data.setup_logger'), \
             patch('compile_historical_data.get_logger', return_value=MagicMock()), \
             patch('compile_historical_data.create_output_directories'), \
             patch('pathlib.Path.exists', return_value=False), \
             patch('compile_historical_data.BaseHTTPClient', return_value=mock_http), \
             patch('compile_historical_data.fetch_and_write_schedule', new_callable=AsyncMock, return_value={}) as mock_sched, \
             patch('compile_historical_data.fetch_and_write_game_data', new_callable=AsyncMock, return_value=[]) as mock_game, \
             patch('compile_historical_data.fetch_player_data', new_callable=AsyncMock, return_value=[]) as mock_player, \
             patch('compile_historical_data.calculate_and_write_team_data', return_value={}) as mock_team, \
             patch('compile_historical_data.generate_weekly_snapshots') as mock_snap:
            compile_historical_data.main()

        assert mock_sched.call_args.kwargs.get('max_weeks') == 3
        assert mock_game.call_args.kwargs.get('max_weeks') == 3
        assert mock_snap.call_args.kwargs.get('max_weeks') == 3


class TestKeepPartialBehavior:
    """Tests verifying --keep-partial suppresses cleanup and preserves exit code 1."""

    def test_keep_partial_prevents_cleanup_on_failure(self):
        import compile_historical_data

        mock_logger = MagicMock()

        with patch('sys.argv', ['compile_historical_data.py', '--year', '2024', '--keep-partial']), \
             patch('compile_historical_data.setup_logger'), \
             patch('compile_historical_data.get_logger', return_value=mock_logger), \
             patch('compile_historical_data.create_output_directories'), \
             patch('pathlib.Path.exists', return_value=False), \
             patch('compile_historical_data.asyncio.run', side_effect=Exception("network error")), \
             patch('compile_historical_data.cleanup_on_error') as mock_cleanup:
            result = compile_historical_data.main()

        assert result == 1
        mock_cleanup.assert_not_called()
        assert any(
            "Partial output preserved" in str(call)
            for call in mock_logger.warning.call_args_list
        )


class TestWeeksCapBehavior:
    """Tests verifying --weeks N > season_length is silently capped."""

    def test_weeks_exceeding_season_capped_to_regular_season_weeks(self):
        import asyncio
        from unittest.mock import AsyncMock as AM
        from historical_data_compiler.schedule_fetcher import ScheduleFetcher
        from historical_data_compiler.constants import REGULAR_SEASON_WEEKS

        mock_http = MagicMock()
        mock_http.get = AM(return_value={'events': []})

        with patch('historical_data_compiler.schedule_fetcher.get_logger', return_value=MagicMock()):
            fetcher = ScheduleFetcher(mock_http)
            schedule = asyncio.run(fetcher.fetch_schedule(year=2024, max_weeks=20))

        assert len(schedule) == REGULAR_SEASON_WEEKS
        assert mock_http.get.call_count == REGULAR_SEASON_WEEKS
