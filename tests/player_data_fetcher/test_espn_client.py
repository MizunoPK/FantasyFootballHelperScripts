#!/usr/bin/env python3
"""
Tests for ESPN Client Module

Basic smoke tests for ESPN client initialization and exception handling.
Focuses on testable functionality without deep HTTP mocking.

Author: Kai Mizuno
"""

import asyncio
import datetime
import json
import logging
import pytest
import httpx
from unittest.mock import AsyncMock, Mock

from player_data_fetcher.espn_client import (
    ESPNAPIError, ESPNRateLimitError, ESPNServerError,
    BaseAPIClient, ESPNClient, CorpusRoute, is_corpus_route
)
from player_data_fetcher.player_data_fetcher_main import Settings


class TestCustomExceptions:
    """Test custom ESPN exception classes"""

    def test_espn_api_error_is_exception(self):
        """Test ESPNAPIError is an Exception"""
        assert issubclass(ESPNAPIError, Exception)

    def test_espn_api_error_can_be_raised(self):
        """Test ESPNAPIError can be raised and caught"""
        with pytest.raises(ESPNAPIError):
            raise ESPNAPIError("Test error")

    def test_espn_api_error_with_message(self):
        """Test ESPNAPIError preserves error message"""
        try:
            raise ESPNAPIError("Custom error message")
        except ESPNAPIError as e:
            assert "Custom error message" in str(e)

    def test_espn_rate_limit_error_is_api_error(self):
        """Test ESPNRateLimitError inherits from ESPNAPIError"""
        assert issubclass(ESPNRateLimitError, ESPNAPIError)

    def test_espn_rate_limit_error_can_be_raised(self):
        """Test ESPNRateLimitError can be raised"""
        with pytest.raises(ESPNRateLimitError):
            raise ESPNRateLimitError("Rate limit exceeded")

    def test_espn_rate_limit_error_caught_as_api_error(self):
        """Test ESPNRateLimitError can be caught as ESPNAPIError"""
        with pytest.raises(ESPNAPIError):
            raise ESPNRateLimitError("Rate limit")

    def test_espn_server_error_is_api_error(self):
        """Test ESPNServerError inherits from ESPNAPIError"""
        assert issubclass(ESPNServerError, ESPNAPIError)

    def test_espn_server_error_can_be_raised(self):
        """Test ESPNServerError can be raised"""
        with pytest.raises(ESPNServerError):
            raise ESPNServerError("Server error")

    def test_espn_server_error_caught_as_api_error(self):
        """Test ESPNServerError can be caught as ESPNAPIError"""
        with pytest.raises(ESPNAPIError):
            raise ESPNServerError("Server error")


class TestBaseAPIClientInit:
    """Test BaseAPIClient initialization"""

    def test_base_client_initialization(self):
        """Test BaseAPIClient can be initialized"""
        settings = Settings()
        client = BaseAPIClient(settings)

        assert client.settings == settings
        assert client._client is None
        assert hasattr(client, '_session_lock')

    def test_base_client_stores_settings(self):
        """Test BaseAPIClient stores settings correctly"""
        settings = Settings(request_timeout=30, rate_limit_delay=0.5)
        client = BaseAPIClient(settings)

        assert client.settings.request_timeout == 30
        assert client.settings.rate_limit_delay == 0.5

    def test_base_client_has_logger(self):
        """Test BaseAPIClient initializes logger"""
        settings = Settings()
        client = BaseAPIClient(settings)

        assert hasattr(client, 'logger')
        assert client.logger is not None


class TestBaseAPIClientSession:
    """Test BaseAPIClient session management"""

    @pytest.mark.asyncio
    async def test_session_context_manager(self):
        """Test session can be used as async context manager"""
        settings = Settings()
        client = BaseAPIClient(settings)

        async with client.session() as http_client:
            assert http_client is not None

    @pytest.mark.asyncio
    async def test_close_without_session(self):
        """Test close() doesn't crash when no session exists"""
        settings = Settings()
        client = BaseAPIClient(settings)

        await client.close()


class TestSettings:
    """Test Settings configuration used by ESPNClient"""

    def test_settings_default_values(self):
        """Test Settings has sensible defaults"""
        settings = Settings()

        assert settings.season > 0
        assert settings.request_timeout > 0
        assert settings.rate_limit_delay >= 0

    def test_settings_custom_timeout(self):
        """Test Settings accepts custom timeout"""
        settings = Settings(request_timeout=60)

        assert settings.request_timeout == 60

    def test_settings_custom_rate_limit(self):
        """Test Settings accepts custom rate limit"""
        settings = Settings(rate_limit_delay=1.0)

        assert settings.rate_limit_delay == 1.0


class TestModuleImports:
    """Test that all expected classes can be imported"""

    def test_import_exceptions(self):
        """Test custom exception classes can be imported"""
        from player_data_fetcher.espn_client import ESPNAPIError, ESPNRateLimitError, ESPNServerError

        assert ESPNAPIError is not None
        assert ESPNRateLimitError is not None
        assert ESPNServerError is not None

    def test_import_base_client(self):
        """Test BaseAPIClient can be imported"""
        from player_data_fetcher.espn_client import BaseAPIClient

        assert BaseAPIClient is not None

    def test_import_espn_client(self):
        """Test ESPNClient can be imported"""
        from player_data_fetcher.espn_client import ESPNClient

        assert ESPNClient is not None


class TestPositionToSlotId:
    """Test _position_to_slot_id helper function"""

    @pytest.fixture
    def client(self):
        """Create ESPNClient instance for testing"""
        settings = Settings()
        return ESPNClient(settings)

    def test_qb_slot_id(self, client):
        """Test QB maps to slot 0"""
        assert client._position_to_slot_id('QB') == 0

    def test_rb_slot_id(self, client):
        """Test RB maps to slot 2"""
        assert client._position_to_slot_id('RB') == 2

    def test_wr_slot_id(self, client):
        """Test WR maps to slot 4"""
        assert client._position_to_slot_id('WR') == 4

    def test_te_slot_id(self, client):
        """Test TE maps to slot 6"""
        assert client._position_to_slot_id('TE') == 6

    def test_k_slot_id(self, client):
        """Test K maps to slot 17"""
        assert client._position_to_slot_id('K') == 17

    def test_dst_slot_id(self, client):
        """Test DST maps to slot 16"""
        assert client._position_to_slot_id('DST') == 16

    def test_d_st_alias(self, client):
        """Test D/ST alias maps to slot 16 (same as DST)"""
        assert client._position_to_slot_id('D/ST') == 16

    def test_invalid_position(self, client):
        """Test invalid position returns -1"""
        assert client._position_to_slot_id('INVALID') == -1

    def test_empty_string(self, client):
        """Test empty string returns -1"""
        assert client._position_to_slot_id('') == -1

    def test_lowercase_position(self, client):
        """Test lowercase position (not handled, returns -1)"""
        assert client._position_to_slot_id('qb') == -1


class TestGetPositionalRankFromOverall:
    """Test _get_positional_rank_from_overall helper function"""

    @pytest.fixture
    def client(self):
        """Create ESPNClient instance for testing"""
        settings = Settings()
        return ESPNClient(settings)

    @pytest.fixture
    def mock_players_simple(self):
        """Create simple mock player data for testing"""
        return [
            {'draft_rank': 12, 'position_id': 1},
            {'draft_rank': 25, 'position_id': 1},
            {'draft_rank': 50, 'position_id': 1},
            {'draft_rank': 5, 'position_id': 2},
            {'draft_rank': 10, 'position_id': 2},
            {'draft_rank': 15, 'position_id': 2},
        ]

    def test_qb1_from_overall_rank_12(self, client, mock_players_simple):
        """Test QB with overall rank 12 becomes QB1"""
        result = client._get_positional_rank_from_overall(12, 'QB', mock_players_simple)
        assert result == 1.0

    def test_qb2_from_overall_rank_25(self, client, mock_players_simple):
        """Test QB with overall rank 25 becomes QB2"""
        result = client._get_positional_rank_from_overall(25, 'QB', mock_players_simple)
        assert result == 2.0

    def test_qb3_from_overall_rank_50(self, client, mock_players_simple):
        """Test QB with overall rank 50 becomes QB3"""
        result = client._get_positional_rank_from_overall(50, 'QB', mock_players_simple)
        assert result == 3.0

    def test_rb1_from_overall_rank_5(self, client, mock_players_simple):
        """Test RB with overall rank 5 becomes RB1"""
        result = client._get_positional_rank_from_overall(5, 'RB', mock_players_simple)
        assert result == 1.0

    def test_rb2_from_overall_rank_10(self, client, mock_players_simple):
        """Test RB with overall rank 10 becomes RB2"""
        result = client._get_positional_rank_from_overall(10, 'RB', mock_players_simple)
        assert result == 2.0

    def test_rb3_from_overall_rank_15(self, client, mock_players_simple):
        """Test RB with overall rank 15 becomes RB3"""
        result = client._get_positional_rank_from_overall(15, 'RB', mock_players_simple)
        assert result == 3.0

    def test_d_st_alias(self, client, mock_players_simple):
        """Test D/ST position alias works"""
        mock_with_dst = mock_players_simple + [{'draft_rank': 100, 'position_id': 16}]
        result = client._get_positional_rank_from_overall(100, 'D/ST', mock_with_dst)
        assert result == 1.0

    def test_invalid_position(self, client, mock_players_simple):
        """Test invalid position returns None"""
        result = client._get_positional_rank_from_overall(12, 'INVALID', mock_players_simple)
        assert result is None

    def test_player_not_found(self, client, mock_players_simple):
        """Test player with non-existent draft rank returns None"""
        result = client._get_positional_rank_from_overall(999, 'QB', mock_players_simple)
        assert result is None

    def test_empty_player_list(self, client):
        """Test empty player list returns None"""
        result = client._get_positional_rank_from_overall(12, 'QB', [])
        assert result is None

    def test_no_players_at_position(self, client, mock_players_simple):
        """Test position with no players returns None"""
        result = client._get_positional_rank_from_overall(12, 'TE', mock_players_simple)
        assert result is None

    def test_players_missing_draft_rank(self, client):
        """Test players with missing draft_rank are ignored"""
        mock_players = [
            {'draft_rank': 10, 'position_id': 1},
            {'draft_rank': None, 'position_id': 1},
            {'draft_rank': 20, 'position_id': 1},
        ]
        result = client._get_positional_rank_from_overall(20, 'QB', mock_players)
        assert result == 2.0

    def test_players_missing_position_id(self, client):
        """Test players with missing position_id are ignored"""
        mock_players = [
            {'draft_rank': 10, 'position_id': 1},
            {'draft_rank': 15, 'position_id': None},
            {'draft_rank': 20, 'position_id': 1},
        ]
        result = client._get_positional_rank_from_overall(20, 'QB', mock_players)
        assert result == 2.0


class TestPositionToPositionId:
    """Test _position_to_position_id helper function"""

    @pytest.fixture
    def client(self):
        """Create ESPNClient instance for testing"""
        settings = Settings()
        return ESPNClient(settings)

    def test_qb_position_id(self, client):
        """Test QB maps to position ID 1"""
        assert client._position_to_position_id('QB') == 1

    def test_rb_position_id(self, client):
        """Test RB maps to position ID 2"""
        assert client._position_to_position_id('RB') == 2

    def test_wr_position_id(self, client):
        """Test WR maps to position ID 3"""
        assert client._position_to_position_id('WR') == 3

    def test_te_position_id(self, client):
        """Test TE maps to position ID 4"""
        assert client._position_to_position_id('TE') == 4

    def test_k_position_id(self, client):
        """Test K maps to position ID 5"""
        assert client._position_to_position_id('K') == 5

    def test_dst_position_id(self, client):
        """Test DST maps to position ID 16"""
        assert client._position_to_position_id('DST') == 16

    def test_d_st_alias(self, client):
        """Test D/ST alias maps to position ID 16 (same as DST)"""
        assert client._position_to_position_id('D/ST') == 16

    def test_invalid_position(self, client):
        """Test invalid position returns -1"""
        assert client._position_to_position_id('INVALID') == -1

    def test_empty_string(self, client):
        """Test empty string returns -1"""
        assert client._position_to_position_id('') == -1

    def test_lowercase_position(self, client):
        """Test lowercase position (not handled, returns -1)"""
        assert client._position_to_position_id('qb') == -1



class TestESPNClientSettingsKAI10:
    """
    Tests verifying KAI-10 refactoring: ESPNClient no longer imports
    CLI-configurable constants from config; uses self.settings instead.
    (REQ-06 — 5 tests)
    """

    def test_espn_player_limit_not_imported_from_config(self):
        """6.1: espn_client module does not have ESPN_PLAYER_LIMIT from config"""
        import player_data_fetcher.espn_client as espn_client
        assert not hasattr(espn_client, 'ESPN_PLAYER_LIMIT')

    def test_current_nfl_week_not_imported_at_module_level(self):
        """6.2: espn_client module does not have CURRENT_NFL_WEEK from config at module level"""
        import player_data_fetcher.espn_client as espn_client
        assert not hasattr(espn_client, 'CURRENT_NFL_WEEK')

    def test_espn_user_agent_still_imported(self):
        """6.3: ESPN_USER_AGENT is still imported in espn_client (non-CLI constant)"""
        import player_data_fetcher.espn_client as espn_client
        assert hasattr(espn_client, 'ESPN_USER_AGENT')
        assert isinstance(espn_client.ESPN_USER_AGENT, str)
        assert len(espn_client.ESPN_USER_AGENT) > 0

    def test_espn_client_accepts_settings_with_espn_player_limit(self):
        """I-7: ESPNClient is initialized with Settings that includes espn_player_limit"""
        settings = Settings(espn_player_limit=500)
        client = ESPNClient(settings)
        assert client.settings.espn_player_limit == 500

    def test_progress_frequency_accessible_via_settings(self):
        """E-17: ESPNClient.settings.progress_frequency is accessible (not from config)"""
        settings = Settings(progress_frequency=25)
        client = ESPNClient(settings)
        assert client.settings.progress_frequency == 25


class TestLoadSeasonScheduleFromCSV:

    def test_happy_path_returns_correct_structure(self, tmp_path):
        csv_file = tmp_path / "schedule.csv"
        csv_file.write_text("week,team,opponent\n1,ARI,NO\n1,NO,ARI\n")
        client = ESPNClient(Settings())
        result = client._load_season_schedule_from_csv(csv_path=csv_file)
        assert result == {1: {'ARI': 'NO', 'NO': 'ARI'}}

    def test_all_18_weeks_present(self):
        client = ESPNClient(Settings())
        result = client._load_season_schedule_from_csv()
        assert len(result) == 18
        assert all(isinstance(k, int) for k in result.keys())

    def test_missing_csv_returns_empty_dict(self, tmp_path):
        client = ESPNClient(Settings())
        result = client._load_season_schedule_from_csv(csv_path=tmp_path / "nonexistent.csv")
        assert result == {}

    def test_csv_with_missing_required_column_returns_empty_dict(self, tmp_path):
        csv_file = tmp_path / "schedule.csv"
        csv_file.write_text("week,team\n1,ARI\n")
        client = ESPNClient(Settings())
        result = client._load_season_schedule_from_csv(csv_path=csv_file)
        assert result == {}

    def test_week_values_are_int_keys(self, tmp_path):
        csv_file = tmp_path / "schedule.csv"
        csv_file.write_text("week,team,opponent\n3,KC,BUF\n")
        client = ESPNClient(Settings())
        result = client._load_season_schedule_from_csv(csv_path=csv_file)
        assert 3 in result
        assert '3' not in result

    def test_uses_default_path_when_none_provided(self):
        client = ESPNClient(Settings())
        result = client._load_season_schedule_from_csv(csv_path=None)
        assert isinstance(result, dict)
        assert len(result) == 18
        assert all(isinstance(k, int) for k in result.keys())
        assert all(len(v) > 0 for v in result.values())


class TestRankingsCacheConstant:

    def test_min_weeks_for_rankings_constant_importable(self):
        from player_data_fetcher.player_data_constants import MIN_WEEKS_FOR_RANKINGS
        assert MIN_WEEKS_FOR_RANKINGS is not None

    def test_min_weeks_for_rankings_constant_value(self):
        from player_data_fetcher.player_data_constants import MIN_WEEKS_FOR_RANKINGS
        assert MIN_WEEKS_FOR_RANKINGS == 5


class TestLoadRankingsFromCache:

    @pytest.fixture
    def client(self):
        return ESPNClient(Settings())

    def test_cache_miss_returns_none(self, client, tmp_path):
        data_dir = tmp_path / 'data'
        data_dir.mkdir()
        result = client._load_rankings_from_cache(cache_dir=data_dir)
        assert result is None

    def test_cache_hit_returns_dict(self, client, tmp_path):
        data_dir = tmp_path / 'data'
        data_dir.mkdir()
        today = datetime.date.today().isoformat()
        cache_file = data_dir / f'team_rankings_cache_{today}.json'
        cache_file.write_text('{"KC": {"offensive_rank": 5, "defensive_rank": 15}}')
        result = client._load_rankings_from_cache(cache_dir=data_dir)
        assert result == {"KC": {"offensive_rank": 5, "defensive_rank": 15}}

    def test_cache_invalid_json_returns_none(self, client, tmp_path):
        data_dir = tmp_path / 'data'
        data_dir.mkdir()
        today = datetime.date.today().isoformat()
        cache_file = data_dir / f'team_rankings_cache_{today}.json'
        cache_file.write_text('not valid json {{{{')
        result = client._load_rankings_from_cache(cache_dir=data_dir)
        assert result is None

    def test_cache_empty_dict_returns_none(self, client, tmp_path):
        data_dir = tmp_path / 'data'
        data_dir.mkdir()
        today = datetime.date.today().isoformat()
        cache_file = data_dir / f'team_rankings_cache_{today}.json'
        cache_file.write_text('{}')
        result = client._load_rankings_from_cache(cache_dir=data_dir)
        assert result is None

    def test_cache_invalid_schema_returns_none(self, client, tmp_path):
        data_dir = tmp_path / 'data'
        data_dir.mkdir()
        today = datetime.date.today().isoformat()
        cache_file = data_dir / f'team_rankings_cache_{today}.json'
        cache_file.write_text('{"KC": "not_a_dict"}')
        result = client._load_rankings_from_cache(cache_dir=data_dir)
        assert result is None

    def test_cache_path_uses_todays_date(self, client, tmp_path):
        data_dir = tmp_path / 'data'
        data_dir.mkdir()
        (data_dir / 'team_rankings_cache_1999-12-31.json').write_text('{"KC": {"offensive_rank": 5, "defensive_rank": 15}}')
        result = client._load_rankings_from_cache(cache_dir=data_dir)
        assert result is None


class TestSaveRankingsToCache:

    @pytest.fixture
    def client(self):
        return ESPNClient(Settings())

    def test_save_creates_json_file(self, client, tmp_path):
        data_dir = tmp_path / 'data'
        data_dir.mkdir()
        rankings = {'KC': {'offensive_rank': 5, 'defensive_rank': 15}}
        client._save_rankings_to_cache(rankings, cache_dir=data_dir)
        today = datetime.date.today().isoformat()
        cache_file = data_dir / f'team_rankings_cache_{today}.json'
        assert cache_file.exists()
        assert json.loads(cache_file.read_text()) == rankings

    def test_save_content_matches_input(self, client, tmp_path):
        data_dir = tmp_path / 'data'
        data_dir.mkdir()
        rankings = {'KC': {'offensive_rank': 5, 'defensive_rank': 15}, 'BUF': {'offensive_rank': 3, 'defensive_rank': 2}}
        client._save_rankings_to_cache(rankings, cache_dir=data_dir)
        today = datetime.date.today().isoformat()
        cache_file = data_dir / f'team_rankings_cache_{today}.json'
        loaded = json.loads(cache_file.read_text())
        assert loaded == rankings

    def test_save_ioerror_logs_warning(self, client, tmp_path):
        from unittest.mock import patch, MagicMock
        data_dir = tmp_path / 'data'
        data_dir.mkdir()
        mock_logger = MagicMock()
        client.logger = mock_logger
        rankings = {'KC': {'offensive_rank': 5, 'defensive_rank': 15}}
        with patch('builtins.open', side_effect=IOError('permission denied')):
            client._save_rankings_to_cache(rankings, cache_dir=data_dir)
        mock_logger.warning.assert_called_once()
        assert 'permission denied' in str(mock_logger.warning.call_args)


class TestRankingsCacheIntegration:

    @pytest.fixture
    def client(self):
        return ESPNClient(Settings())

    @pytest.mark.asyncio
    async def test_cache_hit_skips_api_call(self, client):
        from unittest.mock import patch, AsyncMock
        cached_rankings = {'KC': {'offensive_rank': 5, 'defensive_rank': 15}}
        with patch.object(client, '_load_rankings_from_cache', return_value=cached_rankings) as mock_load, \
             patch.object(client, '_calculate_rolling_window_rankings', new_callable=AsyncMock) as mock_api:
            result = await client._calculate_team_rankings_from_stats()
        assert result == cached_rankings
        mock_load.assert_called_once()
        mock_api.assert_not_called()

    @pytest.mark.asyncio
    async def test_cache_miss_calls_api_and_saves(self, client):
        from unittest.mock import patch, AsyncMock
        api_rankings = {'KC': {'offensive_rank': 5, 'defensive_rank': 15}}
        with patch.object(client, '_load_rankings_from_cache', return_value=None), \
             patch.object(client, '_calculate_rolling_window_rankings', new_callable=AsyncMock, return_value=api_rankings) as mock_api, \
             patch.object(client, '_save_rankings_to_cache') as mock_save:
            result = await client._calculate_team_rankings_from_stats()
        assert result == api_rankings
        mock_api.assert_called_once()
        mock_save.assert_called_once_with(api_rankings)


class TestParseEspnDataPositionRankRanges:
    """D9.1: position_rank_ranges is derived from the export set, not the ranked input set."""

    @pytest.fixture
    def client(self):
        settings = Settings(current_nfl_week=1)
        client = ESPNClient(settings)
        client._fetch_team_rankings = AsyncMock(return_value={})
        client._fetch_current_week_schedule = AsyncMock(return_value={})
        client._load_season_schedule_from_csv = Mock(return_value={})
        client._calculate_week_by_week_projection = Mock(return_value=0.0)
        client._calculate_position_defense_rankings = Mock(return_value={})

        def _populate_side_effect(projection, player_info, name, position):
            if projection.id == '1004':
                raise ValueError('synthetic parse failure')
            return None

        client._populate_weekly_projections = Mock(side_effect=_populate_side_effect)
        return client

    @pytest.mark.asyncio
    async def test_survivor_only_population_reaches_both_endpoints(self, client):
        """Neither the guard-rejected row (1003) nor the parse-failed row (1004) may widen
        RB's range, so the two exported survivors normalize to exactly 100.0 and the 1.0 floor.

        Row roles: 1001 is the exported best rank (PPR rank 1), 1002 the exported worst
        survivor (rank 2), 1003 is rejected by the unknown-team guard (proTeamId 999), and
        1004 raises after rank discovery but before append. Asserting exactly [100.0, 1.0]
        is what pins the invariant: had the ranges been collected over the ranked *input*
        set, 1003/1004 would stretch RB's max to rank 4 and no survivor would reach 1.0.
        """
        # Arrange
        players = [
            {'player': {
                'id': 1001, 'firstName': 'Alpha', 'lastName': 'One',
                'defaultPositionId': 2, 'proTeamId': 1,
                'draftRanksByRankType': {'PPR': {'rank': 1}},
            }},
            {'player': {
                'id': 1002, 'firstName': 'Bravo', 'lastName': 'Two',
                'defaultPositionId': 2, 'proTeamId': 1,
                'draftRanksByRankType': {'PPR': {'rank': 2}},
            }},
            {'player': {
                'id': 1003, 'firstName': 'Charlie', 'lastName': 'Three',
                'defaultPositionId': 2, 'proTeamId': 999,
                'draftRanksByRankType': {'PPR': {'rank': 3}},
            }},
            {'player': {
                'id': 1004, 'firstName': 'Delta', 'lastName': 'Four',
                'defaultPositionId': 2, 'proTeamId': 1,
                'draftRanksByRankType': {'PPR': {'rank': 4}},
            }},
        ]

        # Act
        projections = await client._parse_espn_data({'players': players})

        # Assert
        ids = [projection.id for projection in projections]
        ratings = [projection.player_rating for projection in projections]

        assert ids == ['1001', '1002']
        assert ratings == [100.0, 1.0]


class TestLeagueDraftFixtureCorpus:
    """Test league_draft fixture corpus resolution (R4, R6)"""

    def test_get_fixture_filename_maps_league_route(self):
        """Test _get_fixture_filename returns a CorpusRoute('league_draft') for the
        authenticated league URL -- a directory key, not a plain filename
        (D17.3 review BLOCKING-4: the two return kinds must be structurally
        distinguishable)."""
        url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2026/segments/0/leagues/123"
        result = BaseAPIClient._get_fixture_filename(url, {})
        assert is_corpus_route(result)
        assert result.key == "league_draft"

    def test_resolve_league_draft_fixture_missing_manifest_raises_filenotfounderror(self, tmp_path):
        """Test missing manifest.json raises FileNotFoundError (R6)"""
        # No manifest.json present
        with pytest.raises(FileNotFoundError):
            BaseAPIClient._resolve_league_draft_fixture(str(tmp_path))

    def test_resolve_league_draft_fixture_missing_selector_raises_valueerror(self, tmp_path, monkeypatch):
        """Test missing ESPN_DRAFT_FIXTURE_STEP raises ValueError (R6)"""
        # Create minimal manifest
        manifest_dir = tmp_path / "espn_api" / "league_draft"
        manifest_dir.mkdir(parents=True)
        manifest_path = manifest_dir / "manifest.json"
        manifest_path.write_text(json.dumps({"entries": [{"step": 0, "file": "step_000.json"}]}))

        # No ESPN_DRAFT_FIXTURE_STEP set
        monkeypatch.delenv("ESPN_DRAFT_FIXTURE_STEP", raising=False)

        with pytest.raises(ValueError, match="ESPN_DRAFT_FIXTURE_STEP is required"):
            BaseAPIClient._resolve_league_draft_fixture(str(tmp_path))

    def test_resolve_league_draft_fixture_non_integer_selector_raises_valueerror(self, tmp_path, monkeypatch):
        """Test non-integer ESPN_DRAFT_FIXTURE_STEP raises ValueError (R6)"""
        manifest_dir = tmp_path / "espn_api" / "league_draft"
        manifest_dir.mkdir(parents=True)
        manifest_path = manifest_dir / "manifest.json"
        manifest_path.write_text(json.dumps({"entries": []}))

        monkeypatch.setenv("ESPN_DRAFT_FIXTURE_STEP", "not-an-int")

        with pytest.raises(ValueError, match="must be an integer"):
            BaseAPIClient._resolve_league_draft_fixture(str(tmp_path))

    def test_resolve_league_draft_fixture_out_of_range_selector_raises_valueerror(self, tmp_path, monkeypatch):
        """Test out-of-range ESPN_DRAFT_FIXTURE_STEP raises ValueError (R6)"""
        manifest_dir = tmp_path / "espn_api" / "league_draft"
        manifest_dir.mkdir(parents=True)
        manifest_path = manifest_dir / "manifest.json"
        manifest_path.write_text(json.dumps({"entries": [{"step": 0}, {"step": 1}]}))

        monkeypatch.setenv("ESPN_DRAFT_FIXTURE_STEP", "99")

        with pytest.raises(ValueError, match="does not match exactly one manifest entry"):
            BaseAPIClient._resolve_league_draft_fixture(str(tmp_path))

    def test_resolve_league_draft_fixture_malformed_entry_raises_valueerror_not_keyerror(self, tmp_path, monkeypatch):
        """PR review (Copilot, espn_client.py:231): a manifest entry with a missing/malformed
        'file' field must raise ValueError -- the docstring's and error taxonomy's guaranteed
        type -- not an opaque KeyError."""
        manifest_dir = tmp_path / "espn_api" / "league_draft"
        manifest_dir.mkdir(parents=True)
        manifest_path = manifest_dir / "manifest.json"
        # Entry matches the selector but has no 'file' field at all.
        manifest_path.write_text(json.dumps({"entries": [{"step": 0}]}))

        monkeypatch.setenv("ESPN_DRAFT_FIXTURE_STEP", "0")

        with pytest.raises(ValueError, match="missing a valid 'file' field"):
            BaseAPIClient._resolve_league_draft_fixture(str(tmp_path))

    def test_resolve_league_draft_fixture_non_contiguous_steps_raises_valueerror(self, tmp_path, monkeypatch):
        """SUGGESTION (D17.3 review): a manifest whose step numbers are not contiguous
        from 0 is structurally corrupt and must be rejected before any selector matching."""
        manifest_dir = tmp_path / "espn_api" / "league_draft"
        manifest_dir.mkdir(parents=True)
        manifest_path = manifest_dir / "manifest.json"
        manifest_path.write_text(json.dumps({
            "entries": [
                {"step": 0, "file": "step_000.json"},
                {"step": 2, "file": "step_002.json"},
            ]
        }))

        monkeypatch.setenv("ESPN_DRAFT_FIXTURE_STEP", "0")

        with pytest.raises(ValueError, match="not contiguous"):
            BaseAPIClient._resolve_league_draft_fixture(str(tmp_path))

    def test_resolve_league_draft_fixture_duplicate_filenames_raises_valueerror(self, tmp_path, monkeypatch):
        """SUGGESTION (D17.3 review): a manifest whose entries reuse the same filename for
        two different steps is structurally corrupt and must be rejected before any
        selector matching."""
        manifest_dir = tmp_path / "espn_api" / "league_draft"
        manifest_dir.mkdir(parents=True)
        manifest_path = manifest_dir / "manifest.json"
        manifest_path.write_text(json.dumps({
            "entries": [
                {"step": 0, "file": "step_000.json"},
                {"step": 1, "file": "step_000.json"},
            ]
        }))

        monkeypatch.setenv("ESPN_DRAFT_FIXTURE_STEP", "0")

        with pytest.raises(ValueError, match="duplicate 'file' entries"):
            BaseAPIClient._resolve_league_draft_fixture(str(tmp_path))

    def test_resolve_league_draft_fixture_hash_mismatch_raises_valueerror(self, tmp_path, monkeypatch):
        """Test hash mismatch raises ValueError (R6)"""
        manifest_dir = tmp_path / "espn_api" / "league_draft"
        manifest_dir.mkdir(parents=True)

        step_file = manifest_dir / "step_000.json"
        step_file.write_text(json.dumps({"test": "data"}))

        manifest_path = manifest_dir / "manifest.json"
        manifest_path.write_text(json.dumps({
            "entries": [{"step": 0, "file": "step_000.json", "sha256": "wronghash"}]
        }))

        monkeypatch.setenv("ESPN_DRAFT_FIXTURE_STEP", "0")

        with pytest.raises(ValueError, match="sha256 mismatch"):
            BaseAPIClient._resolve_league_draft_fixture(str(tmp_path))

    def test_resolve_league_draft_fixture_happy_path_returns_selected_step(self, tmp_path, monkeypatch):
        """Test happy path returns selected step content (R6)"""
        import hashlib

        manifest_dir = tmp_path / "espn_api" / "league_draft"
        manifest_dir.mkdir(parents=True)

        # Create step files
        step0_content = json.dumps({"step": 0, "picks": []})
        step0_file = manifest_dir / "step_000.json"
        step0_file.write_text(step0_content)
        step0_hash = hashlib.sha256(step0_content.encode("utf-8")).hexdigest()

        step1_content = json.dumps({"step": 1, "picks": [{"playerId": 123}]})
        step1_file = manifest_dir / "step_001.json"
        step1_file.write_text(step1_content)
        step1_hash = hashlib.sha256(step1_content.encode("utf-8")).hexdigest()

        manifest_path = manifest_dir / "manifest.json"
        manifest_path.write_text(json.dumps({
            "entries": [
                {"step": 0, "file": "step_000.json", "sha256": step0_hash},
                {"step": 1, "file": "step_001.json", "sha256": step1_hash},
            ]
        }))

        monkeypatch.setenv("ESPN_DRAFT_FIXTURE_STEP", "1")
        result = BaseAPIClient._resolve_league_draft_fixture(str(tmp_path))

        assert result == {"step": 1, "picks": [{"playerId": 123}]}

    @pytest.mark.asyncio
    async def test_make_request_offline_league_draft_dispatches_to_resolver(self, tmp_path, monkeypatch):
        """Test _make_request dispatches league_draft to resolver (R4, R6)"""
        import hashlib

        manifest_dir = tmp_path / "espn_api" / "league_draft"
        manifest_dir.mkdir(parents=True)

        # Create one step file
        step_content = json.dumps({"draftDetail": {"picks": []}, "teams": []})
        step_file = manifest_dir / "step_000.json"
        step_file.write_text(step_content)
        step_hash = hashlib.sha256(step_content.encode("utf-8")).hexdigest()

        manifest_path = manifest_dir / "manifest.json"
        manifest_path.write_text(json.dumps({
            "entries": [{"step": 0, "file": "step_000.json", "sha256": step_hash}]
        }))

        monkeypatch.setenv("ESPN_FIXTURE_DIR", str(tmp_path))
        monkeypatch.setenv("ESPN_DRAFT_FIXTURE_STEP", "0")

        settings = Settings()
        client = BaseAPIClient(settings)

        result = await client._make_request(
            "GET",
            "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2026/segments/0/leagues/123",
            params={"view": ["mDraftDetail", "mTeam"]}
        )

        assert result == {"draftDetail": {"picks": []}, "teams": []}


class TestAuthenticatedLeagueSnapshot:
    """Test authenticated league snapshot reading (R1, R1a, R2, R3)"""

    @pytest.mark.asyncio
    async def test_get_raw_league_snapshot_calls_make_request_with_expected_shape(self, monkeypatch):
        """Test _get_raw_league_snapshot constructs request with correct shape (R1)"""
        monkeypatch.setenv("espn_s2", "sentinel_s2")
        monkeypatch.setenv("SWID", "sentinel_swid")

        settings = Settings()
        client = ESPNClient(settings)

        # _make_request is mocked wholesale, so the real live-session guard (now
        # inside BaseAPIClient._make_request, D17.3 review CONCERN-2) never runs --
        # client._client's state is irrelevant here.
        mock_response = {"draftDetail": {"picks": []}, "teams": []}
        client._make_request = AsyncMock(return_value=mock_response)

        result = await client._get_raw_league_snapshot(league_id=123, season=2026)

        # Verify the mock was called with expected arguments
        client._make_request.assert_called_once()
        call_args = client._make_request.call_args
        assert call_args.args[0] == "GET"
        assert "seasons/2026" in call_args.args[1]
        assert "leagues/123" in call_args.args[1]
        assert call_args.kwargs.get("params") == {"view": ["mDraftDetail", "mTeam"]}
        assert call_args.kwargs.get("cookies") == {"espn_s2": "sentinel_s2", "SWID": "sentinel_swid"}

        assert result == mock_response

    @pytest.mark.asyncio
    async def test_get_league_snapshot_returns_validated_only(self, monkeypatch):
        """Test get_league_snapshot returns only validated LeagueSnapshot (R2)"""
        from player_data_fetcher.espn_league_snapshot_models import LeagueSnapshot

        monkeypatch.setenv("espn_s2", "sentinel_s2")
        monkeypatch.setenv("SWID", "sentinel_swid")

        settings = Settings()
        client = ESPNClient(settings)

        # Valid minimal payload matching LeagueSnapshot contract
        valid_payload = {
            "draftDetail": {"picks": [], "drafted": False, "inProgress": False},
            "teams": [],
            "settings": {"draftSettings": {"pickOrder": []}},
        }

        # Mock _get_raw_league_snapshot to return the valid payload
        client._get_raw_league_snapshot = AsyncMock(return_value=valid_payload)

        result = await client.get_league_snapshot(league_id=123)

        # Assert result is a validated LeagueSnapshot instance
        assert isinstance(result, LeagueSnapshot)

    @pytest.mark.asyncio
    async def test_get_league_snapshot_raises_on_invalid_payload(self, monkeypatch):
        """Test get_league_snapshot raises ESPNAPIError on validation failure (R2)"""
        monkeypatch.setenv("espn_s2", "sentinel_s2")
        monkeypatch.setenv("SWID", "sentinel_swid")

        settings = Settings()
        client = ESPNClient(settings)

        # Invalid payload: draftDetail missing or wrong type
        invalid_payload = {"draftDetail": None, "teams": []}

        # Mock _get_raw_league_snapshot to return invalid payload
        client._get_raw_league_snapshot = AsyncMock(return_value=invalid_payload)

        # Should raise ESPNAPIError on validation failure
        with pytest.raises(ESPNAPIError, match="validation failed"):
            await client.get_league_snapshot(league_id=123)

    @pytest.mark.asyncio
    async def test_get_raw_league_snapshot_redacts_credential_on_http_error(self, monkeypatch):
        """Test _get_raw_league_snapshot redacts credentials from error messages (R3)"""
        sentinel_s2 = "sentinel_s2_secret"
        sentinel_swid = "sentinel_swid_secret"
        monkeypatch.setenv("espn_s2", sentinel_s2)
        monkeypatch.setenv("SWID", sentinel_swid)

        settings = Settings()
        client = ESPNClient(settings)

        # _make_request is mocked wholesale (see note above); client._client's
        # state is irrelevant since the real guard never runs.
        error_msg = f"HTTP 401 Unauthorized: {sentinel_s2} is invalid"
        client._make_request = AsyncMock(side_effect=ESPNAPIError(error_msg))

        with pytest.raises(ESPNAPIError) as exc_info:
            await client._get_raw_league_snapshot(league_id=123)

        # Verify the sentinel is NOT in the raised error message
        raised_msg = str(exc_info.value)
        assert sentinel_s2 not in raised_msg
        assert sentinel_swid not in raised_msg

    @pytest.mark.asyncio
    async def test_get_raw_league_snapshot_missing_credentials_fails_loudly(self, monkeypatch):
        """Test _get_raw_league_snapshot fails before calling _make_request if credentials missing (R1, R3)

        D17.3 review CONCERN-1: previously this test passed vacuously -- the
        polish-pass-2 RuntimeError session guard sat at the top of
        _get_raw_league_snapshot (before get_espn_credentials() was even called),
        and pytest.raises(Exception) is satisfied by any exception, so the test
        no longer proved the "missing credential" failure mode it names; deleting
        get_espn_credentials()'s whole validation block would have left it green.
        The guard has since moved into BaseAPIClient._make_request (CONCERN-2), so
        credential validation is reached first again regardless; the assertion is
        also tightened to pin the exact failure this test is named for.
        """
        from utils.error_handler import ConfigurationError

        monkeypatch.delenv("espn_s2", raising=False)
        monkeypatch.delenv("SWID", raising=False)

        settings = Settings()
        client = ESPNClient(settings)

        # Mock _make_request so we can verify it's not called
        client._make_request = Mock()

        with pytest.raises(ConfigurationError, match="Missing required ESPN credential"):
            await client._get_raw_league_snapshot(league_id=123)

        client._make_request.assert_not_called()

    @pytest.mark.asyncio
    async def test_end_to_end_sentinel_absent_from_message_and_logs(self, monkeypatch, caplog):
        """D17.3 review obligation (d) -- the mandatory end-to-end sentinel test.

        Drives the REAL decorated _make_request (through tenacity's @retry with
        reraise=True, through the moved live-session guard, through the single
        redacting wrapper in _get_raw_league_snapshot) by patching only
        client._client.request -- the lowest possible level -- rather than mocking
        _make_request itself, so BLOCKING-1/2/3's seams are all actually
        traversed, which is precisely the check the review says per-path unit
        tests (mocking _make_request wholesale) cannot provide.

        Deliberately does NOT call install_credential_redaction() itself
        (D17.3 review BLOCKING-5): the filter is now installed unconditionally
        inside get_espn_credentials() (called below, via
        _get_raw_league_snapshot), so this test proves the *production*
        wiring rather than supplying its own setup -- the inverted assertion
        the review named as the fix for the exact blind spot that let
        BLOCKING-5 ship undetected three passes in a row.

        Attaches caplog's handler directly to the project's actual logger
        object (utils.LoggingManager.get_logger()): that logger sets
        propagate=False (LoggingManager.setup_logger), so caplog's default
        root-logger handler would capture nothing from it and the log
        assertion would pass vacuously -- attaching directly to the logger's
        own handler list is unaffected by propagate (Logger.callHandlers
        always runs a logger's own handlers before considering propagation).
        """
        from utils.LoggingManager import get_logger

        sentinel_s2 = "SENTINEL_S2_e2e_9f8e7d6c"
        sentinel_swid = "SENTINEL_SWID_e2e_1a2b3c4d"
        monkeypatch.setenv("espn_s2", sentinel_s2)
        monkeypatch.setenv("SWID", sentinel_swid)
        monkeypatch.delenv("ESPN_FIXTURE_DIR", raising=False)
        monkeypatch.delenv("ESPN_RECORD_FIXTURES_DIR", raising=False)

        # Tenacity's wait_random_exponential backoff sleeps real wall-clock time
        # between the 3 attempts; patch asyncio.sleep (used both by tenacity's
        # async retrying and by _make_request's own rate-limit delay) to keep
        # this test fast without changing retry *counts* or *predicates*.
        async def _no_sleep(*_args, **_kwargs):
            return None

        monkeypatch.setattr(asyncio, "sleep", _no_sleep)

        settings = Settings()
        client = ESPNClient(settings)

        call_count = {"n": 0}

        async def fake_request(method, url, **kwargs):
            call_count["n"] += 1
            # Simulates a network-layer failure whose message happens to embed
            # credential-shaped text -- the class of leak BLOCKING-1/2 exist to
            # close, regardless of which layer originates it.
            raise httpx.ConnectError(
                f"connection failed; cookie=espn_s2={sentinel_s2}; SWID={sentinel_swid}"
            )

        project_logger = get_logger()
        project_logger.addHandler(caplog.handler)
        caplog.set_level("DEBUG")
        try:
            async with client.session():
                client._client.request = fake_request
                with pytest.raises(ESPNAPIError) as exc_info:
                    await client._get_raw_league_snapshot(league_id=123, season=2026)
        finally:
            project_logger.removeHandler(caplog.handler)

        assert call_count["n"] == 3, "expected all 3 tenacity attempts to run (reraise=True, not swallowed)"

        raised_msg = str(exc_info.value)
        assert sentinel_s2 not in raised_msg
        assert sentinel_swid not in raised_msg
        assert sentinel_s2 not in caplog.text
        assert sentinel_swid not in caplog.text

    @pytest.mark.asyncio
    async def test_end_to_end_sentinel_absent_from_file_sink_clean_slate(
        self, monkeypatch, tmp_path
    ):
        """D17.3 review SUGGESTION-14 (both reach gaps, addressed together).

        Gap 1 -- the predecessor e2e test asserts only on `caplog.text` via a
        handler attached to the project logger; it never exercises the
        **file** sink (`LineBasedRotatingHandler`, the handler CONCERN-8's
        narrowing was specifically extended to cover). This test attaches a
        real file-backed logger via `setup_logger(..., log_to_file=True)` and
        asserts the sentinel is absent from the file's bytes on disk.

        Gap 2 -- `_credential_redaction_installed` is a module global that
        latches `True` for the whole pytest process, so under an unlucky
        ordering the predecessor e2e test could pass because an *earlier*
        test already installed the filter, not because `get_espn_credentials()`
        did -- the exact "test supplies its own setup" blind spot BLOCKING-5's
        remediation exists to eliminate, displaced one level. This test resets
        that flag (and detaches the filter from every logger/handler it may
        already be on) before driving the real production path, so the proof
        is from a genuinely clean slate.
        """
        from player_data_fetcher import espn_credentials
        from utils.credential_redaction import credential_redaction_filter
        from utils.LoggingManager import setup_logger, get_logger

        # Clean-slate reset (gap 2): undo any earlier test's install so this
        # test proves get_espn_credentials()'s own unconditional install,
        # not a residual from process-wide latching.
        monkeypatch.setattr(espn_credentials, "_credential_redaction_installed", False)
        for lg in (logging.getLogger(), get_logger()):
            if credential_redaction_filter in lg.filters:
                lg.removeFilter(credential_redaction_filter)
            for handler in lg.handlers:
                if credential_redaction_filter in handler.filters:
                    handler.removeFilter(credential_redaction_filter)

        sentinel_s2 = "SENTINEL_S2_filesink_5c4d3e2f"
        sentinel_swid = "SENTINEL_SWID_filesink_6a7b8c9d"
        monkeypatch.setenv("espn_s2", sentinel_s2)
        monkeypatch.setenv("SWID", sentinel_swid)
        monkeypatch.delenv("ESPN_FIXTURE_DIR", raising=False)
        monkeypatch.delenv("ESPN_RECORD_FIXTURES_DIR", raising=False)

        async def _no_sleep(*_args, **_kwargs):
            return None

        monkeypatch.setattr(asyncio, "sleep", _no_sleep)

        # Re-point the project logger at a file-backed handler for the
        # duration of this test, then restore it -- this logger is a
        # process-wide singleton (utils.LoggingManager's module-level
        # instance) shared with every other test.
        log_file = tmp_path / "espn_filesink_test.log"
        original_logger = get_logger()
        setup_logger("default", log_to_file=True, log_file_path=log_file, enable_console=False)
        try:
            settings = Settings()
            client = ESPNClient(settings)

            async def fake_request(method, url, **kwargs):
                raise httpx.ConnectError(
                    f"connection failed; cookie=espn_s2={sentinel_s2}; SWID={sentinel_swid}"
                )

            async with client.session():
                client._client.request = fake_request
                with pytest.raises(ESPNAPIError):
                    await client._get_raw_league_snapshot(league_id=123, season=2026)
        finally:
            setup_logger("default", log_to_file=False, enable_console=True)

        file_bytes = log_file.read_bytes()
        assert sentinel_s2.encode() not in file_bytes
        assert sentinel_swid.encode() not in file_bytes
        assert b"***REDACTED***" in file_bytes


class TestFixtureRecordingRefusesCorpusRoute:
    """Test BLOCKING-4: ESPN_RECORD_FIXTURES_DIR must never silently write the
    raw, unsanitized league_draft payload -- that route is a manifest-backed
    directory produced only by generate_espn_draft_corpus.py, never a single
    recordable fixture file."""

    @pytest.mark.asyncio
    async def test_authenticated_route_refuses_to_record_fixtures(self, monkeypatch, tmp_path):
        """D17.3 review obligation (d)'s second required check: set
        ESPN_RECORD_FIXTURES_DIR, drive the authenticated route, assert nothing
        is written and the call raises rather than silently succeeding."""
        monkeypatch.delenv("ESPN_FIXTURE_DIR", raising=False)
        monkeypatch.setenv("ESPN_RECORD_FIXTURES_DIR", str(tmp_path))

        async def _no_sleep(*_args, **_kwargs):
            return None

        monkeypatch.setattr(asyncio, "sleep", _no_sleep)

        settings = Settings()
        client = BaseAPIClient(settings)

        class FakeResponse:
            status_code = 200

            def raise_for_status(self):
                pass

            def json(self):
                return {"draftDetail": {"picks": []}, "teams": [], "members": []}

        call_count = {"n": 0}

        async def fake_request(method, url, **kwargs):
            call_count["n"] += 1
            return FakeResponse()

        async with client.session():
            client._client.request = fake_request
            with pytest.raises(ESPNAPIError, match="league_draft"):
                await client._make_request(
                    "GET",
                    "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2026/segments/0/leagues/123",
                    params={"view": ["mDraftDetail", "mTeam"]},
                )

        # D17.3 review CONCERN-10/11: the refusal must be classified
        # non-retryable (FixtureRecordingRefused, excluded structurally in
        # _should_retry_espn_request), not just eventually raised -- a
        # deterministic configuration error that retries 3x still costs 3
        # live authenticated requests against ESPN on the real path. This
        # assertion is the regression pin on that classification.
        assert call_count["n"] == 1, (
            "a deterministic FixtureRecordingRefused must not be retried -- "
            "expected exactly 1 request attempt"
        )

        record_dir = tmp_path / "espn_api"
        assert not record_dir.exists() or not any(record_dir.rglob("*")), (
            "ESPN_RECORD_FIXTURES_DIR must write nothing for the league_draft corpus route"
        )
