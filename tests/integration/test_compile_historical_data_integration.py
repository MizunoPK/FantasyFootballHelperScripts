import pytest
from unittest.mock import patch, MagicMock


class TestCompileHistoricalDataMultiYear:

    def test_single_year_compiles_once(self):
        mock_logger = MagicMock()
        with patch('sys.argv', ['compile_historical_data.py', '--year', '2024']), \
             patch('compile_historical_data.setup_logger'), \
             patch('compile_historical_data.get_logger', return_value=mock_logger), \
             patch('compile_historical_data.asyncio.run', return_value=None) as mock_run, \
             patch('compile_historical_data.create_output_directories'), \
             patch('pathlib.Path.exists', return_value=False):
            import compile_historical_data
            result = compile_historical_data.main()
        assert mock_run.call_count == 1
        assert result == 0

    def test_multi_year_compiles_all_years(self):
        mock_logger = MagicMock()
        with patch('sys.argv', ['compile_historical_data.py']), \
             patch('compile_historical_data.setup_logger'), \
             patch('compile_historical_data.get_logger', return_value=mock_logger), \
             patch('compile_historical_data.asyncio.run', return_value=None) as mock_run, \
             patch('compile_historical_data.create_output_directories'), \
             patch('pathlib.Path.exists', return_value=False), \
             patch('compile_historical_data.YEARS', [2024, 2023]):
            import compile_historical_data
            result = compile_historical_data.main()
        assert mock_run.call_count == 2
        assert result == 0

    def test_multi_year_fail_fast_on_first_year_error(self):
        mock_logger = MagicMock()
        with patch('sys.argv', ['compile_historical_data.py']), \
             patch('compile_historical_data.setup_logger'), \
             patch('compile_historical_data.get_logger', return_value=mock_logger), \
             patch('compile_historical_data.asyncio.run', side_effect=Exception("ESPN API error")) as mock_run, \
             patch('compile_historical_data.create_output_directories'), \
             patch('pathlib.Path.exists', return_value=False), \
             patch('compile_historical_data.YEARS', [2024, 2023]):
            import compile_historical_data
            result = compile_historical_data.main()
        assert mock_run.call_count == 1
        assert result == 1
