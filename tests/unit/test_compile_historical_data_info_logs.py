"""
Unit tests for compile_historical_data.py INFO log quality.

Tests verify the output-format INFO log is emitted at startup.
"""

import pytest
from unittest.mock import patch, MagicMock


class TestINFOLogQuality:
    """R4: Unit tests for INFO log quality improvements"""

    def test_config_info_log_added(self):
        """T4.1: Verify config INFO log added at startup"""
        import compile_historical_data

        mock_logger = MagicMock()
        test_args = ['compile_historical_data.py', '--year', '2024', '--format', 'both']

        with patch('sys.argv', test_args), \
             patch('compile_historical_data.setup_logger'), \
             patch('compile_historical_data.get_logger', return_value=mock_logger), \
             patch('compile_historical_data.asyncio.run', return_value=None), \
             patch('compile_historical_data.create_output_directories'), \
             patch('pathlib.Path.exists', return_value=False):
            compile_historical_data.main()

        mock_logger.info.assert_any_call("Output format: both")


