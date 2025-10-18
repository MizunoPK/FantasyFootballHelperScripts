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
    BaseAPIClient
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
