#!/usr/bin/env python3
"""
HTTP Client for Historical Data Compiler

Provides async HTTP client with retry logic and rate limiting for ESPN API requests.
Adapted from player-data-fetcher/espn_client.py BaseAPIClient pattern.

Author: Kai Mizuno
"""

import asyncio
import json
import os
from contextlib import asynccontextmanager
from typing import Any, Dict, Optional

import httpx
from tenacity import retry, stop_after_attempt, wait_random_exponential

from .constants import (
    REQUEST_TIMEOUT,
    RATE_LIMIT_DELAY,
    MAX_RETRY_ATTEMPTS,
    ESPN_USER_AGENT,
)

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.LoggingManager import get_logger


class HTTPClientError(Exception):
    """Base exception for HTTP client errors"""
    pass


class RateLimitError(HTTPClientError):
    """Rate limit exceeded (429)"""
    pass


class ServerError(HTTPClientError):
    """Server error (500+)"""
    pass


class ClientError(HTTPClientError):
    """Client error (400-499, excluding 429)"""
    pass


def _derive_fixture_filename(url: str, params: Optional[Dict[str, Any]]) -> Optional[str]:
    if "site.api.espn.com" in url:
        p = params or {}
        return f"scoreboard_week_{p['week']}_{p['dates']}.json"
    if "fantasy.espn.com" in url:
        parts = url.split("/")
        year = parts[parts.index("seasons") + 1]
        return f"season_projections_{year}.json"
    return None


class BaseHTTPClient:
    """
    Async HTTP client with retry logic and rate limiting.

    Provides:
    - Shared HTTP client session management
    - Automatic retry with exponential backoff
    - Rate limiting to avoid API throttling
    - Error handling for common HTTP status codes
    """

    def __init__(
        self,
        timeout: float = REQUEST_TIMEOUT,
        rate_limit_delay: float = RATE_LIMIT_DELAY,
        user_agent: str = ESPN_USER_AGENT
    ):
        """
        Initialize HTTP client.

        Args:
            timeout: Request timeout in seconds
            rate_limit_delay: Delay between requests in seconds
            user_agent: User agent string for requests
        """
        self.timeout = timeout
        self.rate_limit_delay = rate_limit_delay
        self.user_agent = user_agent
        self.logger = get_logger()
        self._client: Optional[httpx.AsyncClient] = None
        self._session_lock = asyncio.Lock()

    @asynccontextmanager
    async def session(self):
        """
        Async context manager for HTTP client session.

        Creates HTTP client on first use and reuses for subsequent requests.
        Thread-safe via asyncio.Lock.

        Yields:
            httpx.AsyncClient: Shared HTTP client
        """
        async with self._session_lock:
            if self._client is None:
                timeout = httpx.Timeout(self.timeout)
                self._client = httpx.AsyncClient(timeout=timeout)
                self.logger.debug("Created new HTTP client session")

        try:
            yield self._client
        finally:
            pass

    async def close(self):
        """Close the HTTP client session."""
        async with self._session_lock:
            if self._client is not None:
                await self._client.aclose()
                self._client = None
                self.logger.debug("Closed HTTP client session")

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_random_exponential(multiplier=1, max=10)
    )
    async def request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make HTTP request with retry logic and rate limiting.

        Uses tenacity to retry failed requests up to MAX_RETRY_ATTEMPTS times
        with exponential backoff.

        Args:
            method: HTTP method ('GET', 'POST', etc.)
            url: Full URL to request
            headers: Optional request headers
            params: Optional query parameters
            **kwargs: Additional arguments passed to httpx

        Returns:
            Dict containing JSON response data

        Raises:
            RateLimitError: If API returns 429 (triggers retry)
            ServerError: If API returns 500+ (triggers retry)
            ClientError: For other HTTP errors (no retry)
        """
        self.logger.debug(f"Making {method} request to: {url}")

        await asyncio.sleep(self.rate_limit_delay)

        if headers is None:
            headers = {}
        if 'User-Agent' not in headers:
            headers['User-Agent'] = self.user_agent

        async with self.session() as client:
            try:
                response = await client.request(
                    method,
                    url,
                    headers=headers,
                    params=params,
                    **kwargs
                )

                if response.status_code == 429:
                    raise RateLimitError(f"Rate limit exceeded: {response.status_code}")
                elif response.status_code >= 500:
                    raise ServerError(f"Server error: {response.status_code}")
                elif response.status_code >= 400:
                    raise ClientError(f"Client error: {response.status_code}")

                response.raise_for_status()
                self.logger.debug("Request successful")

                return response.json()

            except httpx.RequestError as e:
                self.logger.error(f"HTTP request failed: {e}")
                raise HTTPClientError(f"Request failed: {e}") from e

    async def get(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make GET request.

        When ESPN_FIXTURE_DIR is set, returns fixture JSON for recognized ESPN API URLs
        instead of making live HTTP requests. URL matching rules:
        - site.api.espn.com: returns scoreboard_week_{week}_{dates}.json
        - fantasy.espn.com: returns season_projections_{year}.json
        - open-meteo.com: returns {} immediately
        - Other URLs: falls through to live HTTP

        When ESPN_RECORD_FIXTURES_DIR is set and ESPN_FIXTURE_DIR is not set, writes
        the live response JSON to a fixture file after each successful live request
        (not recorded for open-meteo.com or unrecognized URLs).

        Args:
            url: URL to request
            headers: Optional headers
            params: Optional query parameters
            **kwargs: Additional arguments

        Returns:
            JSON response as dict

        Raises:
            FileNotFoundError: When ESPN_FIXTURE_DIR is set but the fixture file
                for the requested URL does not exist.
            KeyError: When ESPN_FIXTURE_DIR is set, the URL contains
                "site.api.espn.com", and params does not include both "week"
                and "dates".
        """
        fixture_dir = os.environ.get("ESPN_FIXTURE_DIR")
        if fixture_dir:
            if "open-meteo.com" in url:
                return {}
            filename = _derive_fixture_filename(url, params)
            if filename is not None:
                fixture_path = Path(fixture_dir) / "espn_api" / filename
                if not fixture_path.exists():
                    raise FileNotFoundError(
                        f"Fixture file not found: {fixture_path}. "
                        f"Set ESPN_RECORD_FIXTURES_DIR to record fixtures from a live run."
                    )
                return json.loads(fixture_path.read_text())
        response = await self.request('GET', url, headers=headers, params=params, **kwargs)
        record_dir = os.environ.get("ESPN_RECORD_FIXTURES_DIR")
        if record_dir and "open-meteo.com" not in url:
            filename = _derive_fixture_filename(url, params)
            if filename is not None:
                record_path = Path(record_dir) / "espn_api" / filename
                record_path.parent.mkdir(parents=True, exist_ok=True)
                record_path.write_text(json.dumps(response, indent=2))
        return response


