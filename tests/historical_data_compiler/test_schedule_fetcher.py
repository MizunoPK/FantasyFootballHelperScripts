#!/usr/bin/env python3
"""
Tests for historical_data_compiler/schedule_fetcher.py

Pins the outbound ESPN scoreboard request's User-Agent header contract.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, AsyncMock

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from historical_data_compiler.constants import (
    ESPN_SCOREBOARD_API_URL,
    ESPN_SCOREBOARD_USER_AGENT,
)
from historical_data_compiler.schedule_fetcher import ScheduleFetcher


class TestScheduleFetcherScoreboardHeaders:
    """Tests that the scoreboard request sends a User-Agent the endpoint accepts"""

    @pytest.mark.asyncio
    async def test_scoreboard_request_sends_the_accepted_user_agent(self):
        """Should pass an explicit programmatic User-Agent, not the injected browser one"""
        http_client = Mock()
        http_client.get = AsyncMock(return_value={"events": []})
        fetcher = ScheduleFetcher(http_client)

        await fetcher.fetch_schedule(2024, max_weeks=1)

        http_client.get.assert_called_once()
        call_args = http_client.get.call_args
        assert call_args.args[0] == ESPN_SCOREBOARD_API_URL
        assert call_args.kwargs["headers"] == {"User-Agent": ESPN_SCOREBOARD_USER_AGENT}
        assert call_args.kwargs["params"] == {
            "seasontype": 2,
            "week": 1,
            "dates": 2024,
        }
