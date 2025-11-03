#!/usr/bin/env python3
"""
Tests for ESPN Client Module

Basic smoke tests for ESPN client initialization and exception handling.
Focuses on testable functionality without deep HTTP mocking.

Author: Kai Mizuno
"""

import pytest
from pathlib import Path
import sys

# Add project root and player-data-fetcher to path
sys.path.append(str(Path(__file__).parent.parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent / "player-data-fetcher"))

from espn_client import (
    ESPNAPIError, ESPNRateLimitError, ESPNServerError,
    BaseAPIClient, ESPNClient
)
from player_data_fetcher_main import Settings


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

        # Should not raise any exceptions
        async with client.session() as http_client:
            assert http_client is not None

    @pytest.mark.asyncio
    async def test_close_without_session(self):
        """Test close() doesn't crash when no session exists"""
        settings = Settings()
        client = BaseAPIClient(settings)

        # Should not raise any exception
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
        from espn_client import ESPNAPIError, ESPNRateLimitError, ESPNServerError

        assert ESPNAPIError is not None
        assert ESPNRateLimitError is not None
        assert ESPNServerError is not None

    def test_import_base_client(self):
        """Test BaseAPIClient can be imported"""
        from espn_client import BaseAPIClient

        assert BaseAPIClient is not None

    def test_import_espn_client(self):
        """Test ESPNClient can be imported"""
        from espn_client import ESPNClient

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
        # Our implementation is case-sensitive
        assert client._position_to_slot_id('qb') == -1


class TestConvertPositionalRankToRating:
    """Test _convert_positional_rank_to_rating helper function"""

    @pytest.fixture
    def client(self):
        """Create ESPNClient instance for testing"""
        settings = Settings()
        return ESPNClient(settings)

    def test_rank_1_elite(self, client):
        """Test rank 1 (QB1/RB1) returns 100"""
        assert client._convert_positional_rank_to_rating(1.0) == 100.0

    def test_rank_2_elite(self, client):
        """Test rank 2 returns 97.5 (top tier)"""
        assert client._convert_positional_rank_to_rating(2.0) == 97.5

    def test_rank_1_5_elite(self, client):
        """Test fractional rank 1.5 in elite tier"""
        result = client._convert_positional_rank_to_rating(1.5)
        assert 97.5 < result < 100.0

    def test_rank_3_tier2(self, client):
        """Test rank 3 in tier 2 (top 5)"""
        result = client._convert_positional_rank_to_rating(3.0)
        assert 80.0 < result < 94.0

    def test_rank_5_tier2(self, client):
        """Test rank 5 at tier 2 boundary"""
        result = client._convert_positional_rank_to_rating(5.0)
        assert result >= 79.9  # Allow for floating-point precision

    def test_rank_6_tier3(self, client):
        """Test rank 6 in tier 3 (quality starters)"""
        result = client._convert_positional_rank_to_rating(6.0)
        assert 66.0 < result < 80.0

    def test_rank_12_tier3(self, client):
        """Test rank 12 at tier 3 boundary"""
        result = client._convert_positional_rank_to_rating(12.0)
        assert result >= 65.9  # Allow for floating-point precision

    def test_rank_13_tier4(self, client):
        """Test rank 13 in tier 4 (flex/bye week)"""
        result = client._convert_positional_rank_to_rating(13.0)
        assert 50.0 < result < 66.0

    def test_rank_24_tier4(self, client):
        """Test rank 24 at tier 4 boundary"""
        result = client._convert_positional_rank_to_rating(24.0)
        assert result >= 50.0

    def test_rank_25_tier5(self, client):
        """Test rank 25 in tier 5 (deep bench)"""
        result = client._convert_positional_rank_to_rating(25.0)
        assert 30.0 < result < 50.0

    def test_rank_50_tier5(self, client):
        """Test rank 50 at tier 5 boundary"""
        result = client._convert_positional_rank_to_rating(50.0)
        assert result >= 30.0

    def test_rank_51_tier6(self, client):
        """Test rank 51 in tier 6 (waiver wire)"""
        result = client._convert_positional_rank_to_rating(51.0)
        assert 10.0 < result < 30.0

    def test_rank_100_deep_waiver(self, client):
        """Test very deep rank (100) hits floor at 10.0"""
        result = client._convert_positional_rank_to_rating(100.0)
        assert result == 10.0

    def test_rank_200_floor(self, client):
        """Test extremely deep rank maintains floor at 10.0"""
        result = client._convert_positional_rank_to_rating(200.0)
        assert result == 10.0

    def test_fractional_rank_2_5(self, client):
        """Test fractional rank 2.5 (between elite tiers)"""
        result = client._convert_positional_rank_to_rating(2.5)
        assert 80.0 < result < 97.5

    def test_fractional_rank_12_7(self, client):
        """Test fractional rank 12.7"""
        result = client._convert_positional_rank_to_rating(12.7)
        # Should be in tier 4 (between 50 and 66)
        assert 50.0 < result < 66.0


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
        # 3 QBs, 3 RBs
        return [
            {'draft_rank': 12, 'position_id': 1},  # QB1
            {'draft_rank': 25, 'position_id': 1},  # QB2
            {'draft_rank': 50, 'position_id': 1},  # QB3
            {'draft_rank': 5, 'position_id': 2},   # RB1
            {'draft_rank': 10, 'position_id': 2},  # RB2
            {'draft_rank': 15, 'position_id': 2},  # RB3
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
            {'draft_rank': 10, 'position_id': 1},   # QB1
            {'draft_rank': None, 'position_id': 1},  # Ignored
            {'draft_rank': 20, 'position_id': 1},   # QB2
        ]
        result = client._get_positional_rank_from_overall(20, 'QB', mock_players)
        assert result == 2.0  # QB2, not QB3

    def test_players_missing_position_id(self, client):
        """Test players with missing position_id are ignored"""
        mock_players = [
            {'draft_rank': 10, 'position_id': 1},    # QB1
            {'draft_rank': 15, 'position_id': None},  # Ignored
            {'draft_rank': 20, 'position_id': 1},    # QB2
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
        # Our implementation is case-sensitive
        assert client._position_to_position_id('qb') == -1
