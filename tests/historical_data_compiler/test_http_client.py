#!/usr/bin/env python3
"""
Tests for historical_data_compiler/http_client.py

Pins the outbound User-Agent merge seam in BaseHTTPClient._request:

    if headers is None: headers = {}
    if 'User-Agent' not in headers: headers['User-Agent'] = self.user_agent

Both arms are load-bearing for D9.2's scoreboard fix. The scoreboard call
sites pass an explicit ESPN_SCOREBOARD_USER_AGENT, and their own tests mock
the HTTP client entirely, so they assert only what the CALL SITE passes and
would still pass if this merge overwrote the caller's header unconditionally
— silently restoring the site.api.espn.com 403. These tests therefore drive
the REAL merge logic and assert on the headers the client actually emits.
"""

import sys
from contextlib import asynccontextmanager
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from unittest.mock import AsyncMock, MagicMock, patch

from historical_data_compiler.constants import ESPN_USER_AGENT
from historical_data_compiler.http_client import BaseHTTPClient


class TestRequestUserAgentMerge:
    """D9.2: the caller-supplied vs injected-default arms of the header merge."""

    @pytest.fixture
    def client(self):
        return BaseHTTPClient(rate_limit_delay=0)

    @staticmethod
    def _capturing_session(captured):
        """Patch-in for BaseHTTPClient.session that records outbound kwargs."""
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {"ok": True}
        response.raise_for_status.return_value = None

        async def _request(method, url, **kwargs):
            captured.append(kwargs)
            return response

        transport = MagicMock()
        transport.request = AsyncMock(side_effect=_request)

        @asynccontextmanager
        async def _session():
            yield transport

        return _session

    @pytest.mark.asyncio
    async def test_caller_supplied_user_agent_survives_the_merge(self, client):
        """A caller-supplied User-Agent reaches the request unchanged."""
        captured = []
        with patch.object(client, 'session', self._capturing_session(captured)):
            await client.request(
                'GET',
                'https://site.api.espn.com/test',
                headers={'User-Agent': 'sentinel-agent'},
            )
        assert len(captured) == 1
        assert captured[0]['headers']['User-Agent'] == 'sentinel-agent'
        assert captured[0]['headers']['User-Agent'] != ESPN_USER_AGENT

    @pytest.mark.asyncio
    async def test_absent_user_agent_gets_the_default_injected(self, client):
        """With no caller header, the client's default User-Agent is injected."""
        captured = []
        with patch.object(client, 'session', self._capturing_session(captured)):
            await client.request('GET', 'https://site.api.espn.com/test')
        assert len(captured) == 1
        assert captured[0]['headers']['User-Agent'] == ESPN_USER_AGENT

    @pytest.mark.asyncio
    async def test_other_caller_headers_are_preserved_alongside_the_default(self, client):
        """Injecting the default must not drop the caller's other headers."""
        captured = []
        with patch.object(client, 'session', self._capturing_session(captured)):
            await client.request(
                'GET',
                'https://lm-api-reads.fantasy.espn.com/test',
                headers={'X-Fantasy-Filter': '{}'},
            )
        assert len(captured) == 1
        assert captured[0]['headers']['X-Fantasy-Filter'] == '{}'
        assert captured[0]['headers']['User-Agent'] == ESPN_USER_AGENT
