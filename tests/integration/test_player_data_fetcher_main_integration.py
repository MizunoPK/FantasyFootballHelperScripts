"""
Integration tests for the empty response guard in player_data_fetcher_main.py.

Verifies that the player count guard (AC3-AC6) correctly aborts before file writes
when ESPN returns insufficient player data, and proceeds normally with sufficient data.
"""
import asyncio
import pytest
from unittest.mock import patch, AsyncMock, Mock

from player_data_fetcher.player_data_fetcher_main import main
from player_data_fetcher.player_data_models import ProjectionData


class TestPlayerDataFetcherMainIntegration:
    """Integration tests for the empty response guard in player_data_fetcher_main.main()."""

    _SETTINGS_DICT = {
        'season': 2025,
        'current_nfl_week': 1,
        'request_timeout': 30,
        'rate_limit_delay': 0.2,
        'espn_player_limit': 2000,
        'position_json_output': '../data/player_data',
        'team_data_folder': '../data/team_data',
        'game_data_csv': '../data/game_data.csv',
        'enable_historical_save': False,
        'enable_game_data': False,
        'load_drafted_data': False,
        'drafted_data_path': '../data/drafted_data.csv',
        'my_team_name': 'Test Team',
        'progress_frequency': 10,
        'log_level': 'INFO',
        'logging_to_file': False,
        'e2e_test': True,
    }

    @patch('player_data_fetcher.player_data_fetcher_main.NFLProjectionsCollector')
    @patch('player_data_fetcher.player_data_fetcher_main.setup_logger')
    def test_guard_fires_on_zero_total_players(self, mock_setup, mock_collector_class):
        """AC3/AC5: Guard fires when all positions return zero players; export_data not called."""
        mock_collector = mock_collector_class.return_value
        mock_collector.collect_all_projections = AsyncMock(return_value={
            'qb': ProjectionData(season=2025, scoring_format='PPR', total_players=0, players=[])
        })
        mock_collector.export_data = AsyncMock(return_value=[])
        mock_collector.fetch_game_data = Mock(return_value=False)
        mock_collector.save_to_historical_data = Mock(return_value=False)

        with pytest.raises(SystemExit) as exc_info:
            asyncio.run(main(self._SETTINGS_DICT))

        assert exc_info.value.code == 1
        mock_collector.export_data.assert_not_called()

    @patch('player_data_fetcher.player_data_fetcher_main.NFLProjectionsCollector')
    @patch('player_data_fetcher.player_data_fetcher_main.setup_logger')
    def test_guard_fires_on_insufficient_total_players(self, mock_setup, mock_collector_class):
        """AC4: Guard fires when total player count is below MIN_EXPECTED_PLAYER_COUNT (100)."""
        mock_collector = mock_collector_class.return_value
        mock_collector.collect_all_projections = AsyncMock(return_value={
            'qb': ProjectionData(season=2025, scoring_format='PPR', total_players=30, players=[]),
            'rb': ProjectionData(season=2025, scoring_format='PPR', total_players=20, players=[]),
        })
        mock_collector.export_data = AsyncMock(return_value=[])
        mock_collector.fetch_game_data = Mock(return_value=False)
        mock_collector.save_to_historical_data = Mock(return_value=False)

        with pytest.raises(SystemExit) as exc_info:
            asyncio.run(main(self._SETTINGS_DICT))

        assert exc_info.value.code == 1
        mock_collector.export_data.assert_not_called()

    @patch('player_data_fetcher.player_data_fetcher_main.NFLProjectionsCollector')
    @patch('player_data_fetcher.player_data_fetcher_main.setup_logger')
    def test_guard_passes_on_sufficient_players(self, mock_setup, mock_collector_class):
        """AC5: Guard does not fire when total player count is at or above 100; export_data called."""
        mock_collector = mock_collector_class.return_value
        mock_collector.collect_all_projections = AsyncMock(return_value={
            'qb': ProjectionData(season=2025, scoring_format='PPR', total_players=200, players=[])
        })
        mock_collector.export_data = AsyncMock(return_value=[])
        mock_collector.fetch_game_data = Mock(return_value=False)
        mock_collector.save_to_historical_data = Mock(return_value=False)

        asyncio.run(main(self._SETTINGS_DICT))

        mock_collector.export_data.assert_called_once()

    @patch('player_data_fetcher.player_data_fetcher_main.NFLProjectionsCollector')
    @patch('player_data_fetcher.player_data_fetcher_main.setup_logger')
    def test_error_logged_on_guard_trigger(self, mock_setup, mock_collector_class):
        """AC6: logger.error called with message containing player count and threshold when guard triggers."""
        mock_collector = mock_collector_class.return_value
        mock_collector.collect_all_projections = AsyncMock(return_value={
            'qb': ProjectionData(season=2025, scoring_format='PPR', total_players=0, players=[])
        })
        mock_collector.export_data = AsyncMock(return_value=[])
        mock_collector.fetch_game_data = Mock(return_value=False)
        mock_collector.save_to_historical_data = Mock(return_value=False)

        with pytest.raises(SystemExit):
            asyncio.run(main(self._SETTINGS_DICT))

        mock_setup.return_value.error.assert_called_once()
        error_call_str = str(mock_setup.return_value.error.call_args)
        assert '0' in error_call_str
        assert '100' in error_call_str

    @patch('player_data_fetcher.player_data_fetcher_main.NFLProjectionsCollector')
    @patch('player_data_fetcher.player_data_fetcher_main.setup_logger')
    def test_game_data_exception_logs_warning_and_continues(self, mock_setup, mock_collector_class):
        """R3: Exception from fetch_game_data logs warning and execution continues."""
        mock_collector = mock_collector_class.return_value
        mock_collector.collect_all_projections = AsyncMock(return_value={
            'qb': ProjectionData(season=2025, scoring_format='PPR', total_players=200, players=[])
        })
        mock_collector.export_data = AsyncMock(return_value=[])
        mock_collector.fetch_game_data = Mock(side_effect=RuntimeError("network failure"))
        mock_collector.save_to_historical_data = Mock(return_value=False)

        asyncio.run(main(self._SETTINGS_DICT))

        mock_setup.return_value.warning.assert_called_once()
        warning_call_str = str(mock_setup.return_value.warning.call_args)
        assert 'network failure' in warning_call_str
        mock_collector.save_to_historical_data.assert_called_once()


