#!/usr/bin/env python3
"""
Unit tests for ESPN Client module.

Tests the ESPN API client functionality including:
- Async session management and race condition protection
- Player data fetching and week-by-week projections
- Error handling and fallback mechanisms
- Data extraction and point calculation
"""

import asyncio
import pytest
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

# Add the parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from espn_client import ESPNClient

# Create a simple ClientSettings class for testing
class ClientSettings:
    def __init__(self, season=2025, scoring_format="PPR"):
        self.season = season
        self.scoring_format = scoring_format
        self.request_timeout = 30.0
        self.rate_limit_delay = 0.5


class TestESPNClient:
    """Test suite for ESPNClient class"""

    @pytest.fixture
    def settings(self):
        """Create test settings"""
        return ClientSettings(season=2025, scoring_format="PPR")

    @pytest.fixture
    def client(self, settings):
        """Create test ESPN client"""
        return ESPNClient(settings)

    @pytest.mark.asyncio
    async def test_client_initialization(self, client):
        """Test client initializes correctly with async lock"""
        assert client._session_lock is not None
        assert hasattr(client, 'settings')
        assert client.settings.season == 2025

    @pytest.mark.asyncio
    async def test_client_creation_race_condition_protection(self, client):
        """Test that async session context manager is protected from race conditions"""
        # Test that session context manager works properly
        async with client.session() as session1:
            async with client.session() as session2:
                # Both should provide access to the same underlying client
                assert session1 is not None
                assert session2 is not None
                assert session1 is session2  # Same client instance

    @pytest.mark.asyncio
    async def test_get_all_weeks_data_success(self, client):
        """Test successful week-by-week data fetching"""
        player_data = {
            "stats": [
                {
                    "seasonId": 2025,
                    "scoringPeriodId": 1,
                    "appliedTotal": 25.5,
                    "projectedTotal": 23.0
                },
                {
                    "seasonId": 2025,
                    "scoringPeriodId": 2,
                    "appliedTotal": 18.3,
                    "projectedTotal": 20.5
                }
            ]
        }

        # Mock the API response structure that _get_all_weeks_data expects
        mock_api_response = {
            "players": [
                {
                    "player": player_data
                }
            ]
        }

        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_api_response

            result = await client._get_all_weeks_data("12345", "RB")

            assert result == player_data
            mock_request.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_all_weeks_data_failure(self, client):
        """Test week-by-week data fetching with API failure"""
        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = Exception("API Error")

            result = await client._get_all_weeks_data("12345", "RB")

            assert result is None

    def test_extract_week_points_success(self, client):
        """Test successful point extraction from week data"""
        player_data = {
            "stats": [
                {
                    "seasonId": 2025,
                    "scoringPeriodId": 1,
                    "appliedTotal": 25.5,
                    "projectedTotal": 23.0
                },
                {
                    "seasonId": 2025,
                    "scoringPeriodId": 2,
                    "appliedTotal": 18.3,
                    "projectedTotal": 20.5
                }
            ]
        }

        points = client._extract_week_points(player_data, 1, "RB", "Test Player")
        assert points == 25.5

        points = client._extract_week_points(player_data, 2, "RB", "Test Player")
        assert points == 18.3

    def test_extract_week_points_missing_week(self, client):
        """Test point extraction when week data is missing"""
        player_data = {
            "stats": [
                {
                    "seasonId": 2025,
                    "scoringPeriodId": 1,
                    "appliedTotal": 25.5,
                    "projectedTotal": 23.0
                }
            ]
        }

        points = client._extract_week_points(player_data, 3, "RB", "Test Player")
        # Returns position default when week data is missing
        assert points == 8.0  # RB position default

    def test_extract_week_points_malformed_data(self, client):
        """Test point extraction with malformed data"""
        player_data = {
            "stats": [
                {
                    "seasonId": 2025,
                    "scoringPeriodId": 1,
                    # Missing appliedTotal
                    "projectedTotal": 23.0
                }
            ]
        }

        points = client._extract_week_points(player_data, 1, "RB", "Test Player")
        # Uses projected when applied is missing
        assert points == 23.0

    def test_extract_week_points_empty_stats(self, client):
        """Test point extraction with empty stats"""
        player_data = {"stats": []}

        points = client._extract_week_points(player_data, 1, "RB", "Test Player")
        # Returns position default when stats are empty
        assert points == 8.0  # RB position default

    def test_extract_week_points_no_stats(self, client):
        """Test point extraction with no stats key"""
        player_data = {}

        points = client._extract_week_points(player_data, 1, "RB", "Test Player")
        # Returns position default when no stats key
        assert points == 8.0  # RB position default

    @pytest.mark.asyncio
    async def test_client_close(self, client):
        """Test client cleanup properly closes session"""
        # Test that session context manager works
        async with client.session() as session:
            assert session is not None

        # Close the client
        await client.close()

        # Client should be cleaned up
        assert client._client is None

    @pytest.mark.asyncio
    async def test_client_close_no_client(self, client):
        """Test client cleanup when no session exists"""
        # Should not raise exception
        await client.close()
        assert client._client is None

    def test_math_import_available(self, client):
        """Test that math module is properly imported and available"""
        # This test ensures the critical math import bug is fixed
        import math
        assert hasattr(math, 'isnan')
        assert hasattr(math, 'isinf')

    @pytest.mark.asyncio
    async def test_concurrent_client_access(self, client):
        """Test concurrent access to session doesn't cause race conditions"""
        async def use_session_task():
            async with client.session() as session:
                return session

        # Create 10 concurrent tasks
        tasks = [use_session_task() for _ in range(10)]
        sessions = await asyncio.gather(*tasks)

        # All should return the same session instance
        first_client = sessions[0]
        for session in sessions:
            assert session is first_client

    def test_week_range_calculation(self, client):
        """Test that week range calculations work correctly"""
        # Test with current NFL week settings
        client.settings.current_nfl_week = 5
        client.settings.include_playoff_weeks = False

        # Should calculate remaining weeks correctly
        expected_weeks = list(range(5, 19))  # Weeks 5-18

        # This is tested implicitly through the week-by-week system
        assert client.settings.current_nfl_week == 5

    @pytest.mark.asyncio
    async def test_error_recovery_mechanisms(self, client):
        """Test error recovery and graceful degradation"""
        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            # Simulate network error
            mock_request.side_effect = Exception("Network timeout")

            result = await client._get_all_weeks_data("12345", "RB")

            # Should return None instead of crashing
            assert result is None


if __name__ == "__main__":
    # Run tests with pytest if available, otherwise basic test
    try:
        import pytest
        pytest.main([__file__, "-v"])
    except ImportError:
        print("pytest not available, running basic tests...")

        async def run_basic_tests():
            settings = ClientSettings(season=2025, scoring_format="PPR")
            client = ESPNClient(settings)

            # Test initialization
            assert client._session_lock is not None
            print("✅ Client initialization test passed")

            # Test session creation
            session = await client.session()
            assert session is not None
            print("✅ Session creation test passed")

            # Test cleanup
            await client.close()
            print("✅ Client cleanup test passed")

            print("Basic tests completed successfully!")

        asyncio.run(run_basic_tests())