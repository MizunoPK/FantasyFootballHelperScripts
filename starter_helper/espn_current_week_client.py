#!/usr/bin/env python3
"""
ESPN Current Week Projections Client

This module handles ESPN API interactions specifically for current week projections.
Optimized for roster players only to minimize API calls.

Author: Generated for NFL Fantasy Data Collection
Last Updated: September 2025
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from contextlib import asynccontextmanager

import httpx
from tenacity import retry, stop_after_attempt, wait_random_exponential

from starter_helper_config import (
    ESPN_USER_AGENT, REQUEST_TIMEOUT, RATE_LIMIT_DELAY,
    CURRENT_NFL_WEEK, NFL_SEASON, NFL_SCORING_FORMAT,
    USE_CURRENT_WEEK_PROJECTIONS, FALLBACK_TO_SEASON_PROJECTIONS
)

# Import shared fantasy points calculator
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / 'shared_files'))
from fantasy_points_calculator import FantasyPointsExtractor, FantasyPointsConfig, extract_stat_entry_fantasy_points


class ESPNAPIError(Exception):
    """Custom exception for ESPN API errors"""
    pass


class ESPNRateLimitError(ESPNAPIError):
    """Rate limit exceeded exception"""
    pass


class ESPNServerError(ESPNAPIError):
    """ESPN server error exception"""
    pass


class ESPNCurrentWeekClient:
    """ESPN API client for current week projections"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._client = None

        # Initialize shared fantasy points extractor
        fp_config = FantasyPointsConfig(
            prefer_actual_over_projected=True,
            include_negative_dst_points=True,
            use_historical_fallback=False,  # Current week focus - no historical fallback needed
            use_adp_estimation=False        # Current week focus - no ADP estimation needed
        )
        self.fantasy_points_extractor = FantasyPointsExtractor(fp_config, NFL_SEASON)

        # ESPN Fantasy API endpoints (using working endpoint from player-data-fetcher)
        self.base_url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons"

        # Position and team mappings
        self.espn_position_mappings = {
            1: 'QB', 2: 'RB', 3: 'WR', 4: 'TE', 5: 'K', 16: 'DST'
        }

        self.espn_team_mappings = {
            1: 'ATL', 2: 'BUF', 3: 'CHI', 4: 'CIN', 5: 'CLE', 6: 'DAL',
            7: 'DEN', 8: 'DET', 9: 'GB', 10: 'TEN', 11: 'IND', 12: 'KC',
            13: 'LV', 14: 'LAR', 15: 'MIA', 16: 'MIN', 17: 'NE', 18: 'NO',
            19: 'NYG', 20: 'NYJ', 21: 'PHI', 22: 'ARI', 23: 'PIT', 24: 'LAC',
            25: 'SF', 26: 'SEA', 27: 'TB', 28: 'WSH', 29: 'CAR', 30: 'JAX',
            33: 'BAL', 34: 'HOU'
        }

    @asynccontextmanager
    async def session(self):
        """Async context manager for HTTP client"""
        if self._client is None:
            headers = {'User-Agent': ESPN_USER_AGENT}
            timeout = httpx.Timeout(REQUEST_TIMEOUT)
            self._client = httpx.AsyncClient(headers=headers, timeout=timeout)

        try:
            yield self._client
        finally:
            if self._client is not None:
                await self._client.aclose()
                self._client = None

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_random_exponential(multiplier=1, max=10),
        retry_error_callback=lambda retry_state: None
    )
    async def _make_api_request(self, url: str, params: Dict[str, Any], headers: Dict[str, str] = None) -> Dict[str, Any]:
        """Make a single API request with retry logic"""
        async with self.session() as client:
            try:
                response = await client.get(url, params=params, headers=headers)

                if response.status_code == 429:
                    await asyncio.sleep(RATE_LIMIT_DELAY * 5)  # Extra delay for rate limits
                    raise ESPNRateLimitError(f"Rate limit exceeded: {response.status_code}")
                elif response.status_code >= 500:
                    raise ESPNServerError(f"ESPN server error: {response.status_code}")
                elif response.status_code != 200:
                    raise ESPNAPIError(f"API request failed: {response.status_code}")

                return response.json()

            except httpx.TimeoutException:
                raise ESPNAPIError("Request timeout")
            except httpx.RequestError as e:
                raise ESPNAPIError(f"Request error: {str(e)}")

    @retry(
        stop=stop_after_attempt(2),
        wait=wait_random_exponential(multiplier=1, max=3),
        retry_error_callback=lambda retry_state: logging.getLogger(__name__).debug(
            f"Retry attempt {retry_state.attempt_number} failed for player data retrieval"
        )
    )
    async def get_current_week_projection(self, player_id: str) -> Optional[float]:
        """
        Get current week projection for a specific player

        Args:
            player_id: ESPN player ID

        Returns:
            Current week fantasy points projection or None if unavailable
        """
        if not USE_CURRENT_WEEK_PROJECTIONS:
            return None

        try:
            # ESPN fantasy API endpoint (using working endpoint structure)
            url = f"{self.base_url}/{NFL_SEASON}/segments/0/leaguedefaults/3"

            # Use the same parameters as the working player-data-fetcher
            params = {
                'view': 'kona_player_info',
                'scoringPeriodId': CURRENT_NFL_WEEK
            }

            headers = {
                'User-Agent': ESPN_USER_AGENT,
                'X-Fantasy-Filter': f'{{"players":{{"filterIds":{{"value":[{player_id}]}}}}}}'
            }

            self.logger.debug(f"Fetching current week projection for player {player_id}")

            # Special handling for defensive teams (negative IDs)
            if int(player_id) < 0:
                self.logger.debug(f"Processing defensive team with negative ID: {player_id}")

            data = await self._make_api_request(url, params, headers=headers)

            # Navigate the ESPN Fantasy API response structure
            players = data.get('players', [])
            if not players:
                self.logger.debug(f"No players array in response for player {player_id}")
                raise ESPNAPIError(f"No players data returned for player {player_id}")

            self.logger.debug(f"Player {player_id}: Found {len(players)} players in response")

            player_data = players[0].get('player', {})
            # Handle case where player_data is None (happens with some player IDs)
            if player_data is None:
                self.logger.debug(f"Player {player_id}: players[0].get('player') returned None")
                # Check what keys are actually available in players[0]
                available_keys = list(players[0].keys()) if players[0] else []
                self.logger.debug(f"Player {player_id}: Available keys in players[0]: {available_keys}")
                raise ESPNAPIError(f"No player data in response for player {player_id}")

            stats = player_data.get('stats', [])

            # Look for current week stats/projections
            for stat_entry in stats:
                # Skip None stat entries
                if stat_entry is None:
                    continue

                season_id = stat_entry.get('seasonId')
                scoring_period = stat_entry.get('scoringPeriodId')

                # Match current season and week
                if season_id == NFL_SEASON and scoring_period == CURRENT_NFL_WEEK:
                    # Try projected stats first, then actual stats
                    stat_source_id = stat_entry.get('statSourceId')
                    if stat_source_id == 1:  # Projected stats
                        return self._extract_fantasy_points_from_stats(stat_entry)

            # Fallback: look for season projections and estimate current week
            if FALLBACK_TO_SEASON_PROJECTIONS:
                for stat_entry in stats:
                    # Skip None stat entries
                    if stat_entry is None:
                        continue

                    if stat_entry.get('statSourceId') == 1 and stat_entry.get('scoringPeriodId') == 0:  # Season projections
                        season_points = self._extract_fantasy_points_from_stats(stat_entry)
                        if season_points > 0:
                            # Estimate current week as season average
                            remaining_weeks = 18 - CURRENT_NFL_WEEK + 1
                            return season_points / remaining_weeks

            await asyncio.sleep(RATE_LIMIT_DELAY)  # Rate limiting

            # If we reach here, we couldn't find any usable projection data
            # Raise an exception to trigger retry
            raise ESPNAPIError(f"No usable projection data found for player {player_id}")

        except ESPNAPIError:
            # Re-raise API errors to trigger retry mechanism
            raise
        except Exception as e:
            self.logger.warning(f"Failed to get current week projection for player {player_id}: {str(e)}")
            # Convert other exceptions to ESPNAPIError to trigger retry
            raise ESPNAPIError(f"Data parsing error for player {player_id}: {str(e)}")

    def _extract_fantasy_points_from_stats(self, stat_entry: Dict[str, Any]) -> float:
        """
        Extract fantasy points directly from ESPN stat entry using shared logic

        Args:
            stat_entry: ESPN stat entry dictionary

        Returns:
            Fantasy points from ESPN's calculations
        """
        # Use shared fantasy points extraction logic for consistency
        return extract_stat_entry_fantasy_points(stat_entry)

    def _calculate_fantasy_points(self, stats: Dict[str, Any]) -> float:
        """
        Calculate fantasy points from ESPN stats (fallback method)
        This is used only when ESPN doesn't provide pre-calculated totals

        Args:
            stats: ESPN player stats dictionary

        Returns:
            Calculated fantasy points
        """
        # This method is kept as a fallback but ESPN usually provides appliedTotal/projectedTotal
        # which are more accurate than manual calculation. The shared utility handles this.
        self.logger.debug("Using manual fantasy points calculation (fallback)")
        return 0.0  # Simplified - rely on ESPN's calculations via shared utility

    async def get_roster_current_week_projections(self, roster_player_ids: List[str]) -> Dict[str, float]:
        """
        Get current week projections for all roster players

        Args:
            roster_player_ids: List of ESPN player IDs for roster players

        Returns:
            Dictionary mapping player_id to current week fantasy points projection
        """
        self.logger.info(f"Fetching current week projections for {len(roster_player_ids)} roster players")

        projections = {}

        # Process players in batches to avoid overwhelming the API
        batch_size = 5
        for i in range(0, len(roster_player_ids), batch_size):
            batch = roster_player_ids[i:i + batch_size]

            # Create tasks for concurrent requests
            tasks = [self.get_current_week_projection(player_id) for player_id in batch]

            try:
                batch_results = await asyncio.gather(*tasks, return_exceptions=True)

                for player_id, result in zip(batch, batch_results):
                    if isinstance(result, Exception):
                        self.logger.warning(f"Error getting projection for {player_id}: {result}")
                        projections[player_id] = 0.0
                    elif result is not None:
                        projections[player_id] = result
                    else:
                        projections[player_id] = 0.0

                # Rate limiting between batches
                if i + batch_size < len(roster_player_ids):
                    await asyncio.sleep(RATE_LIMIT_DELAY * len(batch))

            except Exception as e:
                self.logger.error(f"Error processing batch {i}-{i+batch_size}: {str(e)}")
                # Set default values for failed batch
                for player_id in batch:
                    projections[player_id] = 0.0

        successful_projections = sum(1 for p in projections.values() if p > 0)
        self.logger.info(f"Successfully retrieved {successful_projections}/{len(roster_player_ids)} current week projections")

        return projections

    async def close(self):
        """Clean up HTTP client"""
        if self._client is not None:
            await self._client.aclose()
            self._client = None