#!/usr/bin/env python3
"""
ESPN Fantasy API Client

This module handles all ESPN API interactions for fantasy football data collection.
Separated from the main script for better organization and maintainability.

Author: Kai Mizuno
"""

import asyncio
import csv
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
import math

import httpx
from tenacity import retry, stop_after_attempt, wait_random_exponential

from player_data_models import ESPNPlayerData, ScoringFormat
from pathlib import Path
from fantasy_points_calculator import FantasyPointsExtractor, FantasyPointsConfig
from player_data_constants import (
    ESPN_TEAM_MAPPINGS, ESPN_POSITION_MAPPINGS
)
from config import (ESPN_USER_AGENT, ESPN_PLAYER_LIMIT,
    CURRENT_NFL_WEEK,
    SKIP_DRAFTED_PLAYER_UPDATES, USE_SCORE_THRESHOLD, PLAYER_SCORE_THRESHOLD, PLAYERS_CSV
)

import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.LoggingManager import get_logger


class ESPNAPIError(Exception):
    """Custom exception for ESPN API errors"""
    pass


class ESPNRateLimitError(ESPNAPIError):
    """Rate limit exceeded exception"""
    pass


class ESPNServerError(ESPNAPIError):
    """ESPN server error exception"""  
    pass


class BaseAPIClient:
    """
    Base API client with common HTTP functionality for ESPN API requests.

    Provides:
    - Shared HTTP client session management with race condition protection
    - Automatic retry logic with exponential backoff
    - Rate limiting to avoid ESPN API throttling
    - HTTP error handling (429 rate limits, 500 server errors, 400 client errors)
    """

    def __init__(self, settings):
        """
        Initialize base API client.

        Args:
            settings: Settings object containing request_timeout and rate_limit_delay
        """
        self.settings = settings
        self.logger = get_logger()
        # HTTP client instance (created lazily on first use)
        self._client = None
        # Lock to prevent race conditions when creating HTTP client from multiple async tasks
        self._session_lock = asyncio.Lock()

    @asynccontextmanager
    async def session(self):
        """
        Async context manager for HTTP client session with race condition protection.

        Creates HTTP client on first use and reuses it for subsequent requests.
        Thread-safe: Uses asyncio.Lock to prevent multiple tasks from creating
        duplicate HTTP clients simultaneously.

        Yields:
            httpx.AsyncClient: Shared HTTP client for making requests
        """
        # Acquire lock before checking/creating client (prevents race conditions)
        async with self._session_lock:
            if self._client is None:
                # Create HTTP client with configured timeout
                timeout = httpx.Timeout(self.settings.request_timeout)
                self._client = httpx.AsyncClient(timeout=timeout)
                self.logger.debug("Created new HTTP client session")

        try:
            # Yield client for use (lock is released, allowing concurrent requests)
            yield self._client
        finally:
            # Note: We don't close the client here to allow reuse across requests
            # The client will be closed when close() is called explicitly
            pass

    async def close(self):
        """
        Close the HTTP client session and release resources.

        Should be called when done with all API requests to clean up connections.
        """
        async with self._session_lock:
            if self._client:
                await self._client.aclose()
                self._client = None
                self.logger.debug("Closed HTTP client session")
    
    @retry(stop=stop_after_attempt(3), wait=wait_random_exponential(multiplier=1, max=10))
    async def _make_request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """
        Make HTTP request with automatic retry logic and rate limiting.

        Uses tenacity retry decorator to automatically retry failed requests up to 3 times
        with exponential backoff (1s, 2s, 4s, up to 10s max between retries).

        Rate limiting: Adds configurable delay before each request to avoid ESPN throttling.

        Args:
            method: HTTP method ('GET', 'POST', etc.)
            url: Full URL to request
            **kwargs: Additional arguments passed to httpx (headers, params, etc.)

        Returns:
            Dict containing JSON response data from ESPN API

        Raises:
            ESPNRateLimitError: If ESPN returns 429 (Too Many Requests)
            ESPNServerError: If ESPN returns 500+ (server error)
            ESPNAPIError: For other HTTP errors (400-499) or network failures
        """
        self.logger.debug(f"Making request to: {url}")

        # Rate limiting: Sleep before each request to avoid ESPN API throttling
        # Configured via settings.rate_limit_delay (typically 0.1-0.5 seconds)
        await asyncio.sleep(self.settings.rate_limit_delay)

        try:
            # Make the actual HTTP request using shared client
            response = await self._client.request(method, url, **kwargs)

            # Handle specific HTTP error codes with custom exceptions
            if response.status_code == 429:
                # 429 = Too Many Requests (rate limit exceeded)
                # Retry decorator will automatically retry after backoff
                raise ESPNRateLimitError(f"Rate limit exceeded: {response.status_code}")
            elif response.status_code >= 500:
                # 500-599 = Server errors (ESPN's fault, should retry)
                raise ESPNServerError(f"ESPN server error: {response.status_code}")
            elif response.status_code >= 400:
                # 400-499 = Client errors (our fault, probably won't fix on retry)
                raise ESPNAPIError(f"ESPN API error: {response.status_code}")

            # Verify response is successful (2xx status code)
            response.raise_for_status()
            self.logger.debug("Request successful")

            # Parse and return JSON response data
            return response.json()

        except httpx.RequestError as e:
            # Network-level errors (DNS, connection timeout, etc.)
            self.logger.error(f"Request failed: {e}")
            raise ESPNAPIError(f"Network error: {e}")
        except Exception as e:
            # Unexpected errors (JSON parsing, etc.)
            self.logger.error(f"Unexpected error: {e}")
            raise


class ESPNClient(BaseAPIClient):
    """
    ESPN Fantasy API client for fetching player projections and team data.

    Features:
    - Fetches season projections for all players from ESPN Fantasy API
    - Calculates week-by-week projections (weeks 1-17) for each player
    - Fetches team quality rankings (offensive/defensive) from ESPN stats
    - Fetches current week schedule/matchups
    - Optimization: Can skip API calls for drafted players (SKIP_DRAFTED_PLAYER_UPDATES)
    - Optimization: Can preserve data for low-scoring players (USE_SCORE_THRESHOLD)
    """

    # ============================================================================
    # INITIALIZATION & CONFIGURATION
    # ============================================================================

    def __init__(self, settings):
        """
        Initialize ESPN API client for player data collection.

        Sets up:
        - HTTP client session (inherited from BaseAPIClient)
        - Bye week mappings for NFL teams
        - Optimization tracking (drafted players, low-score players)
        - Team rankings cache (offensive/defensive quality)
        - Current week schedule cache (team matchups)
        - Shared fantasy points extractor for consistent scoring calculations

        Args:
            settings: Settings object with season, scoring_format, timeouts, etc.
        """
        super().__init__(settings)

        # Bye week data: team abbreviation → bye week number (1-18)
        # Loaded from external CSV file, populated by main script
        self.bye_weeks: Dict[str, int] = {}

        # OPTIMIZATION: Track drafted player IDs to skip expensive API calls
        # Players with drafted=1 in players.csv (already on other teams)
        # Skipping these saves ~50% of API calls in mid-season
        self.drafted_player_ids: Set[str] = set()

        # OPTIMIZATION: Preserve data for low-scoring players to avoid API calls
        # Players below PLAYER_SCORE_THRESHOLD get their data preserved from players.csv
        # Key = player ID, Value = dict of all player data from CSV
        self.low_score_player_data: Dict[str, Dict] = {}

        # Team quality rankings cache: team abbrev → {'offensive_rank': N, 'defensive_rank': N}
        # Fetched once per session from ESPN team stats API
        # Used to evaluate matchup difficulty for player projections
        self.team_rankings: Dict[str, Dict[str, int]] = {}

        # Current week schedule cache: team abbrev → opponent abbrev
        # Example: {'KC': 'DEN', 'DEN': 'KC', ...}
        # Fetched once per session from ESPN scoreboard API
        self.current_week_schedule: Dict[str, str] = {}

        # Initialize shared fantasy points extractor for consistent week-by-week calculations
        # Configuration:
        # - prefer_actual_over_projected=True: Use actual game results when available
        # - include_negative_dst_points=True: Allow DST to have negative fantasy points
        fp_config = FantasyPointsConfig(
            prefer_actual_over_projected=True,
            include_negative_dst_points=True
        )
        self.fantasy_points_extractor = FantasyPointsExtractor(fp_config, settings.season)

        # Load optimization data if any optimization features are enabled
        # This reads players.csv to identify which players to skip/preserve
        if SKIP_DRAFTED_PLAYER_UPDATES or USE_SCORE_THRESHOLD:
            self._load_optimization_data()
    
    def _get_ppr_id(self) -> int:
        """
        Get ESPN scoring format ID for API requests.

        ESPN uses numeric IDs to identify scoring formats:
        - 1 = Standard scoring (no points per reception)
        - 2 = Half-PPR (0.5 points per reception)
        - 3 = Full PPR (1 point per reception)

        Returns:
            int: ESPN scoring format ID (defaults to 3/PPR if unrecognized)
        """
        scoring_map = {
            ScoringFormat.STANDARD: 1,
            ScoringFormat.PPR: 3,
            ScoringFormat.HALF_PPR: 2
        }
        return scoring_map.get(self.settings.scoring_format, 3)

    def _load_optimization_data(self):
        """
        Load player data from players.csv to enable performance optimizations.

        This method implements two major performance optimizations:

        1. SKIP_DRAFTED_PLAYER_UPDATES (config flag):
           - Identifies players with drafted=1 (already drafted by other teams)
           - These players don't need weekly API calls since we won't draft them
           - Saves ~50% of API calls in mid-season (hundreds of players)
           - Players with drafted=2 (our roster) are NEVER skipped

        2. USE_SCORE_THRESHOLD (config flag):
           - Identifies players below PLAYER_SCORE_THRESHOLD fantasy points
           - Preserves their existing data from players.csv instead of API calls
           - Focuses API calls on high-value players who might be drafted
           - Players with drafted=2 (our roster) are ALWAYS updated regardless of score

        Data structure loaded:
        - drafted_player_ids: Set of player IDs with drafted=1 to skip
        - low_score_player_data: Dict of player IDs → full CSV row data for players below threshold

        Note: These optimizations dramatically reduce API call volume (70-80% reduction)
        while maintaining accuracy for players we actually care about drafting.
        """
        try:
            # Path to players.csv (shared data file with draft helper)
            players_file_path = Path(__file__).parent / PLAYERS_CSV

            with open(players_file_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Get player ID (required for all optimizations)
                    player_id = row.get('id')
                    if not player_id:
                        continue

                    # Get player metadata for optimization decisions
                    drafted_value = int(row.get('drafted', 0))  # 0=available, 1=drafted by others, 2=our roster
                    fantasy_points = float(row.get('fantasy_points', 0.0))  # Season projection

                    # OPTIMIZATION 1: Track drafted=1 players to skip API calls
                    # Players already drafted by other teams don't need updates
                    if SKIP_DRAFTED_PLAYER_UPDATES and drafted_value == 1:
                        self.drafted_player_ids.add(player_id)

                    # OPTIMIZATION 2: Track low-scoring players to preserve data
                    if USE_SCORE_THRESHOLD:
                        # Always update players on our roster (drafted=2) regardless of score
                        # This ensures we have fresh data for our team evaluation
                        if drafted_value == 2:
                            pass  # Don't add to low_score_player_data, always update our players

                        # Preserve data for low-scoring players (below threshold)
                        # Save entire CSV row so we can use it without API calls
                        elif fantasy_points < PLAYER_SCORE_THRESHOLD:
                            self.low_score_player_data[player_id] = dict(row)

            # Log optimization statistics
            optimization_messages = []
            if SKIP_DRAFTED_PLAYER_UPDATES:
                optimization_messages.append(f"{len(self.drafted_player_ids)} drafted player IDs to skip")
            if USE_SCORE_THRESHOLD:
                optimization_messages.append(f"{len(self.low_score_player_data)} low-score players to preserve (threshold: {PLAYER_SCORE_THRESHOLD})")

            if optimization_messages:
                self.logger.info(f"Loaded optimization data: {', '.join(optimization_messages)}")

        except FileNotFoundError:
            # File missing = first run or file deleted, proceed without optimizations
            self.logger.warning(f"Players file not found at {players_file_path}. No optimizations will be applied.")
        except Exception as e:
            # Unexpected error reading file, log and proceed without optimizations
            self.logger.error(f"Error loading optimization data: {e}. No optimizations will be applied.")

    # ============================================================================
    # TEAM DATA (Rankings, Schedule, Matchups)
    # ============================================================================

    async def _fetch_team_rankings(self) -> Dict[str, Dict[str, int]]:
        """
        Fetch team offensive and defensive rankings from ESPN.

        Returns:
            Dictionary with team abbreviations as keys and rankings as values:
            {
                'KC': {'offensive_rank': 5, 'defensive_rank': 15},
                'NE': {'offensive_rank': 20, 'defensive_rank': 8},
                ...
            }
        """
        if self.team_rankings:  # Return cached data if available
            return self.team_rankings

        try:
            self.logger.info("Fetching team quality rankings from ESPN")

            # ESPN team stats endpoint
            team_stats_url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams"

            async with self.session() as client:
                team_data = await self._make_request("GET", team_stats_url)

            teams = team_data.get('teams', [])
            team_rankings = {}

            # Calculate actual team rankings from ESPN team statistics
            team_rankings = await self._calculate_team_rankings_from_stats()

            self.team_rankings = team_rankings
            self.logger.info(f"Calculated data-driven rankings for {len(team_rankings)} teams")

            return self.team_rankings

        except Exception as e:
            self.logger.error(f"Failed to fetch team rankings: {e}")
            # Return empty rankings - players will get None values
            return {}

    # ============================================================================
    # PLAYER WEEKLY PROJECTIONS (Week-by-week point calculations)
    # ============================================================================

    async def _calculate_week_by_week_projection(self, player_id: str, name: str, position: str) -> float:
        """Calculate remaining season projection by summing current + future week projections"""

        try:
            # Get all weekly data for this player in a single optimized call
            all_weeks_data = await self._get_all_weeks_data(player_id, position)
            if not all_weeks_data:
                return 0.0

            # Only calculate for remaining season (current week + future weeks)
            end_week = 17
            start_week = CURRENT_NFL_WEEK

            total_projection = 0.0
            weeks_processed = 0

            for week in range(start_week, end_week + 1):
                week_points = None

                # Extract week points using standardized logic (always prefers actual over projected)
                week_points = self._extract_week_points(all_weeks_data, week, position=position, player_name=name)

                # Determine data type for logging (current week = current, future weeks = projected)
                if week == CURRENT_NFL_WEEK:
                    data_type = 'current'
                else:
                    data_type = 'projected'

                if week_points > 0:
                    total_projection += week_points
                    weeks_processed += 1
                    self.logger.debug(f"{name} Week {week}: {week_points:.1f} points ({data_type})")

            if weeks_processed > 0:
                self.logger.debug(f"Remaining season projection for {name}: {total_projection:.1f} points ({weeks_processed} weeks)")
                return total_projection

        except Exception as e:
            self.logger.warning(f"Week-by-week calculation failed for {name}: {e}")

        return 0.0

    async def _get_all_weeks_data(self, player_id: str, position: str) -> Optional[dict]:
        """
        Get all weekly stat data for a player in a single optimized API call.

        This method fetches ALL available weekly data for a player (weeks 1-18) in one API request
        instead of making 18 separate requests (one per week). This is a major performance optimization.

        ESPN API Endpoint:
        - URL: https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{season}/segments/0/leaguedefaults/3
        - Query params:
          - view=kona_player_info: Get detailed player information
          - scoringPeriodId=0: Special value meaning "all weeks" (not a specific week number)
        - Headers:
          - X-Fantasy-Filter: JSON filter to select specific player by ID

        Response structure:
        {
          "players": [{
            "player": {
              "id": 12345,
              "stats": [
                {"seasonId": 2024, "scoringPeriodId": 1, "appliedTotal": 15.2, "statSourceId": 0, ...},
                {"seasonId": 2024, "scoringPeriodId": 1, "projectedTotal": 14.8, "statSourceId": 1, ...},
                {"seasonId": 2024, "scoringPeriodId": 2, "appliedTotal": 18.5, "statSourceId": 0, ...},
                ...
              ]
            }
          }]
        }

        Args:
            player_id: ESPN player ID (numeric string)
            position: Player position (QB, RB, WR, TE, K, DST)

        Returns:
            Dict containing player data with 'stats' array, or None if player not found
        """
        try:
            # ESPN Fantasy League API endpoint for player projections
            url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{self.settings.season}/segments/0/leaguedefaults/3"

            # Query parameters
            params = {
                'view': 'kona_player_info',  # ESPN view name for detailed player data
                'scoringPeriodId': 0  # 0 = get ALL weeks (optimization to avoid 18 separate API calls)
            }

            # Request headers with player filter
            headers = {
                'User-Agent': ESPN_USER_AGENT,  # Required by ESPN to identify client
                # X-Fantasy-Filter is ESPN's proprietary JSON filter syntax to select specific players
                # filterIds.value=[{player_id}] = only return this specific player
                'X-Fantasy-Filter': f'{{"players":{{"filterIds":{{"value":[{player_id}]}}}}}}'
            }

            # Make API request with automatic retry and rate limiting
            data = await self._make_request('GET', url, params=params, headers=headers)
            players = data.get('players', [])

            if not players:
                # Player not found in ESPN database (rookie, practice squad, etc.)
                return None

            # Return player data containing 'stats' array with all weekly data
            # Each stat entry has: seasonId, scoringPeriodId, appliedTotal, projectedTotal, statSourceId
            return players[0].get('player', {})

        except Exception as e:
            # Log warning but don't crash - caller will handle None return
            self.logger.warning(f"Failed to get all weeks data for player {player_id}: {e}")
            return None

    def _extract_week_points(self, player_data: dict, week: int, position: str, player_name: str = "Unknown") -> float:
        """
        Extract points for a specific week from player data using shared logic

        NOTE: This now uses the shared FantasyPointsExtractor for consistent logic
        across all modules. The prefer_actual parameter has been removed as we
        now standardize on always preferring appliedTotal over projectedTotal.
        """
        try:
            # Use shared fantasy points extractor
            # Note: player_data already has the correct structure with 'stats' array
            points = self.fantasy_points_extractor.extract_week_points(
                player_data={'player': player_data},  # Wrap to match expected structure
                week=week,
                position=position,
                player_name=player_name,
                current_nfl_week=CURRENT_NFL_WEEK
            )

            return points if points is not None else 0.0

        except Exception as e:
            self.logger.error(f"Error extracting week points for {player_name} week {week}: {str(e)}")
            return 0.0

    async def _populate_weekly_projections(self, player_data: ESPNPlayerData, player_id: str, name: str, position: str):
        """
        Populate weekly projections for a player if week-by-week projections are enabled

        Args:
            player_data: The ESPNPlayerData object to populate
            player_id: ESPN player ID
            name: Player name for logging
            position: Player position
        """
        # Week-by-week projections are always enabled

        try:
            # Get all weekly data for this player
            all_weeks_data = await self._get_all_weeks_data(player_id, position)
            if not all_weeks_data:
                return

            # Determine week range (limit to 17 for fantasy regular season)
            end_week = 17

            # Collect weekly projections for all weeks
            for week in range(1, end_week + 1):
                # Get raw points from ESPN data without fallbacks
                espn_points = self._extract_raw_espn_week_points(all_weeks_data, week, position)

                if espn_points is not None and (espn_points > 0 or position == 'DST'):
                    player_data.set_week_points(week, espn_points)
                    self.logger.debug(f"{name} Week {week}: {espn_points:.1f} points (ESPN data)")
                else:
                    # Set to 0.0 when no ESPN data available (likely bye week for DST teams)
                    player_data.set_week_points(week, 0.0)
                    if position == 'DST':
                        self.logger.debug(f"{name} Week {week}: 0.0 points (likely bye week)")
                    else:
                        self.logger.debug(f"{name} Week {week}: 0.0 points (no data)")

        except Exception as e:
            self.logger.warning(f"Failed to populate weekly projections for {name}: {str(e)}")

    def _extract_raw_espn_week_points(self, player_data: dict, week: int, position: str) -> Optional[float]:
        """
        Extract fantasy points for a specific week from ESPN's complex data structure.

        This method handles ESPN's multi-layered stat system where the same week can have:
        - Multiple stat entries (actual vs projected)
        - Multiple point values (appliedTotal vs projectedTotal)
        - Multiple data sources (statSourceId=0 for actuals, statSourceId=1 for projections)

        ESPN Data Structure (for one week):
        [
          {"seasonId": 2024, "scoringPeriodId": 7, "statSourceId": 0, "appliedTotal": 18.2, ...},  # Actual results
          {"seasonId": 2024, "scoringPeriodId": 7, "statSourceId": 1, "projectedTotal": 15.8, ...}  # Projections
        ]

        Priority Logic:
        1. statSourceId=0 + appliedTotal: Actual game results (HIGHEST PRIORITY for completed weeks)
        2. statSourceId=0 + projectedTotal: Official projection from ESPN (for completed weeks without actuals)
        3. statSourceId=1 + appliedTotal: Projected actuals (for future weeks)
        4. statSourceId=1 + projectedTotal: Projected estimate (LOWEST PRIORITY for future weeks)
        5. None: No ESPN data available (likely bye week or player inactive)

        Special handling:
        - DST positions: Allow negative fantasy points (e.g., -2.0 for bad defense performance)
        - Other positions: Filter out negative/zero values (invalid data)
        - NaN values: Treated as invalid and skipped

        Args:
            player_data: Dict from _get_all_weeks_data containing 'stats' array
            week: Week number (1-18)
            position: Player position (QB, RB, WR, TE, K, DST)

        Returns:
            Float: Fantasy points for the week, or None if no ESPN data available
        """
        try:
            # Get stats array from player data
            stats = player_data.get('stats', [])
            if not stats:
                return None

            # Separate stat entries by data source quality
            # statSourceId=0: Actual game results (high quality, use for completed weeks)
            # statSourceId=1: Projected/estimated values (lower quality, use for future weeks)
            actual_entries = []  # statSourceId=0 (actual game results)
            projected_entries = []  # statSourceId=1 (projections/estimates)

            # Scan all stat entries to find matching week
            for stat in stats:
                if not isinstance(stat, dict):
                    continue

                # Check if this stat entry matches our target week and season
                season_id = stat.get('seasonId')
                scoring_period = stat.get('scoringPeriodId')

                if season_id == self.settings.season and scoring_period == week:
                    # This stat entry is for the week we're looking for
                    stat_source_id = stat.get('statSourceId')

                    # Try to extract fantasy points from this stat entry
                    # Priority: appliedTotal (actual/realized) > projectedTotal (forecast)
                    points = None
                    if 'appliedTotal' in stat and stat['appliedTotal'] is not None:
                        try:
                            points = float(stat['appliedTotal'])
                            # Validate: ESPN sometimes returns NaN, which we must skip
                            if math.isnan(points):
                                continue
                        except (ValueError, TypeError):
                            # Invalid data type, skip this entry
                            continue
                    elif 'projectedTotal' in stat and stat['projectedTotal'] is not None:
                        try:
                            points = float(stat['projectedTotal'])
                            # Validate: ESPN sometimes returns NaN, which we must skip
                            if math.isnan(points):
                                continue
                        except (ValueError, TypeError):
                            # Invalid data type, skip this entry
                            continue

                    # Categorize valid points by data source quality
                    if points is not None:
                        if stat_source_id == 0:
                            # statSourceId=0 = actual game results (HIGHEST QUALITY)
                            # Use this for weeks that have already been played
                            actual_entries.append(points)
                        elif stat_source_id == 1:
                            # statSourceId=1 = projections/estimates (LOWER QUALITY)
                            # Use this for future weeks or as fallback
                            projected_entries.append(points)

            # PRIORITY 1: Use actual game results if available (statSourceId=0)
            # These are the most reliable data points for completed weeks
            if actual_entries:
                # Filter out zero/negative values for non-DST positions
                # (DST can have negative points, other positions cannot)
                valid_actuals = [p for p in actual_entries if position == 'DST' or p > 0]
                if valid_actuals:
                    return valid_actuals[0]  # Return first valid actual result

            # PRIORITY 2: Fall back to projections if no actual results (statSourceId=1)
            # Used for future weeks or when actual data isn't available yet
            if projected_entries:
                # Filter out zero/negative values for non-DST positions
                valid_projected = [p for p in projected_entries if position == 'DST' or p > 0]
                if valid_projected:
                    return valid_projected[0]  # Return first valid projection

            # No valid ESPN data found for this week
            # This is normal for bye weeks or inactive players
            return None

        except Exception as e:
            # Log debug message but don't crash - return None to indicate no data
            self.logger.debug(f"Error extracting raw ESPN week points: {str(e)}")
            return None

    # ============================================================================
    # MAIN API METHODS & DATA PARSING
    # ============================================================================

    async def get_season_projections(self, season: Optional[int] = None) -> List[ESPNPlayerData]:
        """
        Get season projections from ESPN.

        Args:
            season: Optional season year (defaults to settings.season if not provided).
                   Use season=2024 to fetch historical data for simulation validation.

        Returns:
            List of player data with projections
        """
        ppr_id = self._get_ppr_id()
        use_season = season if season is not None else self.settings.season

        self.logger.info(f"Fetching season projections for {use_season}")

        # ESPN's main fantasy API endpoint for player projections
        url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{use_season}/segments/0/leaguedefaults/{ppr_id}"
        
        params = {
            "view": "kona_player_info",
            "scoringPeriodId": 0  # 0 = season projections
        }
        
        headers = {
            'User-Agent': ESPN_USER_AGENT,
            'X-Fantasy-Filter': f'{{"players":{{"limit":{ESPN_PLAYER_LIMIT},"sortPercOwned":{{"sortPriority":4,"sortAsc":false}}}}}}'
        }
        
        data = await self._make_request("GET", url, params=params, headers=headers)
        return await self._parse_espn_data(data)
    
    async def _make_request(self, method: str, url: str, **kwargs):
        """Override to add ESPN-specific headers"""
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        
        # Ensure User-Agent is always set for ESPN
        if 'User-Agent' not in kwargs['headers']:
            kwargs['headers']['User-Agent'] = ESPN_USER_AGENT
        
        return await super()._make_request(method, url, **kwargs)

    async def _calculate_team_rankings_from_stats(self) -> Dict[str, Dict[str, int]]:
        """
        Calculate team offensive and defensive rankings from actual ESPN statistics.
        Uses current season data if sufficient weeks have been played, otherwise falls back
        to previous season or neutral rankings.

        Returns:
            Dictionary mapping team abbreviations to offensive/defensive ranks
        """
        try:
            from config import MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
            from config import CURRENT_NFL_WEEK, NFL_SEASON

            # Determine which season to use for statistics
            use_current_season = CURRENT_NFL_WEEK > MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS

            self.logger.info(f"Team rankings: Using {'current season' if use_current_season else 'neutral'} data. "
                           f"Current week: {CURRENT_NFL_WEEK}, Min weeks needed: {MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS}")

            # Use neutral rankings if not enough weeks have passed
            if not use_current_season:
                self.logger.info(f"Not enough weeks for current season rankings - using neutral data (all ranks = 16)")
                return self._get_fallback_team_rankings()

            # ESPN team IDs mapping (standard NFL team IDs)
            team_ids = {
                1: 'ATL', 2: 'BUF', 3: 'CHI', 4: 'CIN', 5: 'CLE', 6: 'DAL', 7: 'DEN', 8: 'DET',
                9: 'GB', 10: 'TEN', 11: 'IND', 12: 'KC', 13: 'LV', 14: 'LAR', 15: 'MIA', 16: 'MIN',
                17: 'NE', 18: 'NO', 19: 'NYG', 20: 'NYJ', 21: 'PHI', 22: 'ARI', 23: 'PIT', 24: 'LAC',
                25: 'SF', 26: 'SEA', 27: 'TB', 28: 'WSH', 29: 'CAR', 30: 'JAX', 33: 'BAL', 34: 'HOU'
            }

            # Use the helper method to calculate rankings for the current season
            return await self._calculate_team_rankings_for_season(NFL_SEASON, team_ids)

        except Exception as e:
            # Handle case where variables might not be defined yet
            season_info = "unknown season"
            try:
                import sys
                import os
                sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
                from config import CURRENT_NFL_WEEK, NFL_SEASON
                from config import MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS
                use_current_season = CURRENT_NFL_WEEK > MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS
                season_info = f"{NFL_SEASON} season" if use_current_season else "neutral data"
            except:
                pass

            self.logger.error(f"Error calculating team rankings for {season_info}: {e}")

            # Always fall back to neutral rankings on error
            self.logger.info(f"Falling back to neutral team rankings (all ranks = 16)")
            return self._get_fallback_team_rankings()

    async def _calculate_team_rankings_for_season(self, season: int, team_ids: Dict[int, str]) -> Dict[str, Dict[str, int]]:
        """
        Helper method to calculate team rankings for a specific season.
        Used for both current season and fallback scenarios.
        """
        team_stats = {}
        # Get all teams now that we have a working endpoint
        all_teams = list(team_ids.items())

        for team_id, team_abbr in all_teams:
            try:
                # Use the working endpoint (doesn't support season filtering, but works)
                team_stats_url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/statistics"

                # Log which season we intended to fetch vs what we're getting
                self.logger.debug(f"Fetching team {team_abbr} stats (intended season: {season}, actual: current season)")

                async with self.session() as client:
                    stats_data = await self._make_request("GET", team_stats_url)

                if stats_data and 'results' in stats_data and 'stats' in stats_data['results']:
                    stats = stats_data['results']['stats']

                    # Extract key offensive metrics
                    offensive_points = self._extract_stat_value(stats, 'totalPointsPerGame')
                    total_yards = self._extract_stat_value(stats, 'totalYards')
                    takeaways = self._extract_stat_value(stats, 'totalTakeaways')

                    team_stats[team_abbr] = {
                        'offensive_points': offensive_points or 0,
                        'total_yards': total_yards or 0,
                        'takeaways': takeaways or 0
                    }

                    self.logger.debug(f"Stats for {team_abbr} ({season}): PPG={offensive_points}, Yards={total_yards}")

            except Exception as e:
                self.logger.warning(f"Failed to get {season} stats for team {team_abbr}: {e}")
                continue

        # If we got enough data, calculate rankings
        if len(team_stats) >= 3:
            # Sort by offensive points per game
            sorted_offensive = sorted(team_stats.items(), key=lambda x: x[1]['offensive_points'], reverse=True)
            sorted_defensive = sorted(team_stats.items(), key=lambda x: x[1]['takeaways'], reverse=True)

            team_rankings = {}

            # Assign rankings to collected teams
            for rank, (team, stats) in enumerate(sorted_offensive, 1):
                team_rankings[team] = {'offensive_rank': rank}

            for rank, (team, stats) in enumerate(sorted_defensive, 1):
                if team in team_rankings:
                    team_rankings[team]['defensive_rank'] = rank

            # Fill in remaining teams with neutral rankings
            all_teams = ['KC', 'NE', 'LAC', 'LAR', 'SF', 'DAL', 'PHI', 'NYG', 'WSH', 'CHI',
                        'GB', 'MIN', 'DET', 'ATL', 'CAR', 'NO', 'TB', 'SEA', 'ARI', 'BAL',
                        'PIT', 'CLE', 'CIN', 'BUF', 'MIA', 'NYJ', 'TEN', 'IND', 'HOU', 'JAX', 'LV', 'DEN']

            for team in all_teams:
                if team not in team_rankings:
                    team_rankings[team] = {'offensive_rank': 16, 'defensive_rank': 16}

            self.logger.info(f"ESPN {season} data rankings - Offensive leaders: {[team for team, _ in sorted_offensive[:3]]}")
            return team_rankings
        else:
            raise Exception(f"Insufficient team data for {season} season: only {len(team_stats)} teams")

    def _extract_stat_value(self, stats, stat_name: str) -> float:
        """Extract a specific stat value from ESPN stats structure"""
        try:
            for category in stats.get('categories', []):
                for stat in category.get('stats', []):
                    if stat.get('name') == stat_name:
                        return float(stat.get('value', 0))
            return None
        except:
            return None

    def _get_fallback_team_rankings(self) -> Dict[str, Dict[str, int]]:
        """Fallback team rankings when ESPN data unavailable"""
        all_teams = ['KC', 'NE', 'LAC', 'LAR', 'SF', 'DAL', 'PHI', 'NYG', 'WSH', 'CHI',
                     'GB', 'MIN', 'DET', 'ATL', 'CAR', 'NO', 'TB', 'SEA', 'ARI', 'BAL',
                     'PIT', 'CLE', 'CIN', 'BUF', 'MIA', 'NYJ', 'TEN', 'IND', 'HOU', 'JAX', 'LV', 'DEN']

        return {team: {'offensive_rank': 16, 'defensive_rank': 16} for team in all_teams}

    async def _fetch_current_week_schedule(self) -> Dict[str, str]:
        """
        Fetch current week schedule to determine opponent matchups.

        Returns:
            Dictionary with team abbreviations as keys and opponent abbreviations as values:
            {'KC': 'DEN', 'DEN': 'KC', 'NE': 'BUF', 'BUF': 'NE', ...}
        """
        try:
            from config import CURRENT_NFL_WEEK, NFL_SEASON

            self.logger.info(f"Fetching week {CURRENT_NFL_WEEK} schedule from ESPN")

            # ESPN scoreboard API endpoint for current week
            url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
            params = {
                "seasontype": 2,  # Regular season
                "week": CURRENT_NFL_WEEK,
                "dates": NFL_SEASON
            }

            data = await self._make_request("GET", url, params=params)

            # Parse schedule data to create opponent mapping
            schedule_map = {}
            events = data.get('events', [])

            for event in events:
                try:
                    # Extract teams from the competition
                    competitions = event.get('competitions', [])
                    if not competitions:
                        continue

                    competition = competitions[0]
                    competitors = competition.get('competitors', [])

                    if len(competitors) != 2:
                        continue

                    # Get team abbreviations for both teams
                    team1_data = competitors[0].get('team', {})
                    team2_data = competitors[1].get('team', {})

                    team1_abbrev = team1_data.get('abbreviation', '')
                    team2_abbrev = team2_data.get('abbreviation', '')

                    # Handle team abbreviation mapping (ESPN might use WAS instead of WSH)
                    team1_abbrev = 'WSH' if team1_abbrev == 'WAS' else team1_abbrev
                    team2_abbrev = 'WSH' if team2_abbrev == 'WAS' else team2_abbrev

                    if team1_abbrev and team2_abbrev:
                        # Each team's opponent is the other team
                        schedule_map[team1_abbrev] = team2_abbrev
                        schedule_map[team2_abbrev] = team1_abbrev

                except Exception as e:
                    self.logger.warning(f"Error parsing schedule event: {e}")
                    continue

            self.logger.info(f"Retrieved schedule for {len(schedule_map)} teams in week {CURRENT_NFL_WEEK}")
            return schedule_map

        except Exception as e:
            self.logger.error(f"Failed to fetch current week schedule: {e}")
            return {}

    async def _fetch_full_season_schedule(self) -> Dict[int, Dict[str, str]]:
        """
        Fetch complete season schedule for all weeks.

        Returns:
            Dict[week_number, Dict[team, opponent]]
            Example: {1: {'KC': 'BAL', 'BAL': 'KC', ...}, 2: {...}, ...}
        """
        try:
            from config import NFL_SEASON
            import asyncio

            full_schedule = {}

            self.logger.info("Fetching full season schedule (weeks 1-18)")

            for week in range(1, 19):  # Weeks 1-18
                self.logger.debug(f"Fetching schedule for week {week}/18")

                # ESPN scoreboard API endpoint
                url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
                params = {
                    "seasontype": 2,  # Regular season
                    "week": week,
                    "dates": NFL_SEASON
                }

                data = await self._make_request("GET", url, params=params)

                # Parse schedule for this week
                week_schedule = {}
                events = data.get('events', [])

                for event in events:
                    try:
                        competitions = event.get('competitions', [])
                        if not competitions:
                            continue

                        competition = competitions[0]
                        competitors = competition.get('competitors', [])

                        if len(competitors) != 2:
                            continue

                        # Get team abbreviations
                        team1_data = competitors[0].get('team', {})
                        team2_data = competitors[1].get('team', {})

                        team1 = team1_data.get('abbreviation', '')
                        team2 = team2_data.get('abbreviation', '')

                        # Normalize team names (ESPN uses WAS, we use WSH)
                        team1 = 'WSH' if team1 == 'WAS' else team1
                        team2 = 'WSH' if team2 == 'WAS' else team2

                        if team1 and team2:
                            week_schedule[team1] = team2
                            week_schedule[team2] = team1

                    except Exception as e:
                        self.logger.debug(f"Error parsing event in week {week}: {e}")
                        continue

                full_schedule[week] = week_schedule

                # Rate limiting between requests
                await asyncio.sleep(0.2)

            self.logger.info(f"Successfully fetched schedule for {len(full_schedule)} weeks")
            return full_schedule

        except Exception as e:
            self.logger.error(f"Failed to fetch full season schedule: {e}")
            return {}

    def _calculate_position_defense_rankings(
        self,
        players: List[ESPNPlayerData],
        schedule: Dict[int, Dict[str, str]],
        current_week: int
    ) -> Dict[str, Dict[str, int]]:
        """
        Calculate position-specific defense rankings for all teams.

        Args:
            players: List of all players with weekly stats (from ESPN API)
            schedule: Dict mapping {week: {team: opponent}} for all weeks
            current_week: Current NFL week (1-17)

        Returns:
            Dict[team, {'def_vs_qb_rank': int, 'def_vs_rb_rank': int, ...}]
            Rankings are 1-32 where 1 = best defense (fewest points allowed)
        """
        from collections import defaultdict

        self.logger.info(f"Calculating position-specific defense rankings for week {current_week}")

        # Track points allowed by each defense to each position
        defense_stats = defaultdict(lambda: defaultdict(float))

        # All 32 NFL teams
        all_teams = [
            'ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE',
            'DAL', 'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAX', 'KC',
            'LAC', 'LAR', 'LV', 'MIA', 'MIN', 'NE', 'NO', 'NYG',
            'NYJ', 'PHI', 'PIT', 'SEA', 'SF', 'TB', 'TEN', 'WSH'
        ]

        # For each player, accumulate points scored against their opponents
        for player in players:
            # Only process offensive positions (QB, RB, WR, TE, K)
            if player.position not in ['QB', 'RB', 'WR', 'TE', 'K']:
                continue

            # Get all opponents this team has faced (weeks 1 to current_week-1)
            for week in range(1, current_week):
                # Get week's opponent for player's team
                week_schedule = schedule.get(week, {})
                opponent_defense = week_schedule.get(player.team)

                if not opponent_defense:
                    continue

                # Get player's actual points for this week (from ESPN data)
                week_points = player.get_week_points(week)

                # Only use actual stats (week_points will be None for future weeks)
                if week_points is None:
                    continue

                # Skip negative/zero points for non-DST positions
                if week_points <= 0 and player.position != 'DST':
                    continue

                # Accumulate points allowed by opponent's defense
                if player.position == 'QB':
                    defense_stats[opponent_defense]['vs_qb'] += week_points
                elif player.position == 'RB':
                    defense_stats[opponent_defense]['vs_rb'] += week_points
                elif player.position == 'WR':
                    defense_stats[opponent_defense]['vs_wr'] += week_points
                elif player.position == 'TE':
                    defense_stats[opponent_defense]['vs_te'] += week_points
                elif player.position == 'K':
                    defense_stats[opponent_defense]['vs_k'] += week_points

        # Rank defenses for each position (lower points allowed = better rank)
        rankings = {}
        for position in ['vs_qb', 'vs_rb', 'vs_wr', 'vs_te', 'vs_k']:
            # Get teams that have data for this position
            teams_with_data = [
                (team, stats[position])
                for team, stats in defense_stats.items()
                if position in stats and stats[position] > 0
            ]

            # Sort teams by total points allowed (ascending = better defense)
            sorted_teams = sorted(teams_with_data, key=lambda x: x[1])

            # Assign ranks (1 = fewest points = best defense)
            for rank, (team, points_allowed) in enumerate(sorted_teams, 1):
                if team not in rankings:
                    rankings[team] = {}
                rankings[team][f'def_{position}_rank'] = rank
                self.logger.debug(
                    f"{team} {position}: Rank {rank} ({points_allowed:.1f} points allowed)"
                )

        # Fill in neutral ranks (16) for teams with no data or missing positions
        for team in all_teams:
            if team not in rankings:
                rankings[team] = {}

            for position in ['vs_qb', 'vs_rb', 'vs_wr', 'vs_te', 'vs_k']:
                rank_key = f'def_{position}_rank'
                if rank_key not in rankings[team]:
                    rankings[team][rank_key] = 16  # Neutral rank (middle of 32 teams)

        self.logger.info(f"Calculated position-specific rankings for {len(rankings)} teams across 5 positions")

        return rankings

    # ============================================================================
    # PLAYER RATING HELPER FUNCTIONS
    # ============================================================================

    def _position_to_slot_id(self, position: str) -> int:
        """
        Map position string to ESPN slotId for rankings validation.

        ESPN uses different IDs for positions vs ranking slots:
        - Position IDs (defaultPositionId): QB=1, RB=2, WR=3, TE=4, K=5, DST=16
        - Slot IDs (slotId in rankings): QB=0, RB=2, WR=4, TE=6, K=17, DST=16

        Args:
            position: Position string (QB, RB, WR, TE, K, DST, D/ST)

        Returns:
            ESPN slotId for ranking validation, or -1 if unknown
        """
        # Handle D/ST alias
        if position == 'D/ST':
            position = 'DST'

        slot_mapping = {
            'QB': 0,
            'RB': 2,
            'WR': 4,
            'TE': 6,
            'K': 17,
            'DST': 16
        }
        return slot_mapping.get(position, -1)

    def _convert_positional_rank_to_rating(self, positional_rank: float) -> float:
        """
        Convert ESPN position-specific rank to 0-100 rating scale.

        Uses a tiered formula that values elite positional players highest:
        - Top 2 (Tier 1): 95-100 rating
        - Ranks 3-5 (Tier 2): 80-94 rating
        - Ranks 6-12 (Tier 3): 66-79 rating
        - Ranks 13-24 (Tier 4): 50-65 rating
        - Ranks 25-50 (Tier 5): 30-49 rating
        - Ranks 50+ (Tier 6): 10-29 rating

        Args:
            positional_rank: ESPN consensus positional rank (e.g., 1.0 for QB1, 5.5 for RB6)

        Returns:
            Rating on 0-100 scale (actually 10-100 with floor)
        """
        if positional_rank <= 2:  # Elite tier (QB1-2, RB1-2, etc.)
            return 100.0 - (positional_rank - 1.0) * 2.5  # 100 to 97.5
        elif positional_rank <= 5:  # Top 5 starters
            return 94.0 - (positional_rank - 2.0) * 4.67  # 94 to 80
        elif positional_rank <= 12:  # Quality starters
            return 79.0 - (positional_rank - 5.0) * 1.86  # 79 to 66
        elif positional_rank <= 24:  # Flex/Bye week starters
            return 65.0 - (positional_rank - 12.0) * 1.25  # 65 to 50
        elif positional_rank <= 50:  # Deep bench
            return 49.0 - (positional_rank - 24.0) * 0.73  # 49 to 30
        else:  # Waiver wire
            return max(10.0, 29.0 - (positional_rank - 50.0) * 0.38)  # 29 to 10 (floor at 10)

    def _get_positional_rank_from_overall(
        self,
        overall_draft_rank: int,
        position: str,
        all_players_data: List[Dict[str, Any]]
    ) -> Optional[float]:
        """
        Calculate position-specific rank from overall draft rank.

        Used for Week 1 when ROS rankings aren't available yet. Groups all players
        by position and calculates where this player ranks within their position.

        Args:
            overall_draft_rank: ESPN overall draft rank (1-300+)
            position: Player position (QB, RB, WR, TE, K, DST)
            all_players_data: List of all player dicts with draft ranks and position IDs

        Returns:
            Positional rank (e.g., 5.0 for 5th QB), or None if can't calculate
        """
        # Handle D/ST alias
        if position == 'D/ST':
            position = 'DST'

        # Get ESPN position ID for grouping
        position_id = self._position_to_position_id(position)
        if position_id == -1:
            return None

        # Group players by position and sort by draft rank
        same_position_players = [
            p for p in all_players_data
            if p.get('position_id') == position_id and p.get('draft_rank') is not None
        ]

        if not same_position_players:
            return None

        # Sort by draft rank (lower is better)
        same_position_players.sort(key=lambda p: p['draft_rank'])

        # Find this player's position-specific rank
        for idx, player in enumerate(same_position_players, start=1):
            if player['draft_rank'] == overall_draft_rank:
                return float(idx)

        return None

    def _position_to_position_id(self, position: str) -> int:
        """
        Map position string to ESPN defaultPositionId for player grouping.

        Args:
            position: Position string (QB, RB, WR, TE, K, DST, D/ST)

        Returns:
            ESPN defaultPositionId, or -1 if unknown
        """
        from player_data_constants import ESPN_POSITION_MAPPINGS

        # Handle D/ST alias
        if position == 'D/ST':
            position = 'DST'

        # ESPN_POSITION_MAPPINGS: {1: 'QB', 2: 'RB', ...}
        # Need reverse mapping: {'QB': 1, 'RB': 2, ...}
        reverse_mapping = {v: k for k, v in ESPN_POSITION_MAPPINGS.items()}
        return reverse_mapping.get(position, -1)

    async def _parse_espn_data(self, data: Dict[str, Any]) -> List[ESPNPlayerData]:
        """Parse ESPN API response into ESPNPlayerData objects"""
        from config import (
            PROGRESS_UPDATE_FREQUENCY, PROGRESS_ETA_WINDOW_SIZE, CURRENT_NFL_WEEK
        )

        projections = []
        unknown_position_count = 0  # Track players filtered due to unknown positions

        # Fetch team rankings and current week schedule for all players
        team_rankings = await self._fetch_team_rankings()
        current_week_schedule = await self._fetch_current_week_schedule()

        # Fetch full season schedule for position-specific defense calculation
        full_season_schedule = await self._fetch_full_season_schedule()

        # Store schedule data for later use
        self.current_week_schedule = current_week_schedule
        self.full_season_schedule = full_season_schedule

        players = data.get('players', [])
        self.logger.info(f"Processing {len(players)} players from ESPN API")

        # Initialize progress tracker if enabled
        from progress_tracker import ProgressTracker
        progress_tracker = ProgressTracker(
            total_players=len(players),
            logger=self.logger,
            update_frequency=PROGRESS_UPDATE_FREQUENCY,
            eta_window_size=PROGRESS_ETA_WINDOW_SIZE
        )

        # Week 1 preprocessing: Collect all player draft ranks for position-specific calculation
        all_players_with_ranks = []
        if CURRENT_NFL_WEEK <= 1:
            self.logger.info(f"Calculating position-specific ranks for Week {CURRENT_NFL_WEEK} (processing {len(players)} players)")
            for player in players:
                player_info = player.get('player', {})
                draft_ranks = player_info.get('draftRanksByRankType', {})
                ppr_rank_data = draft_ranks.get('PPR', {})

                if ppr_rank_data and 'rank' in ppr_rank_data:
                    draft_rank = ppr_rank_data['rank']
                    position_id = player_info.get('defaultPositionId')

                    if position_id:
                        all_players_with_ranks.append({
                            'draft_rank': draft_rank,
                            'position_id': position_id
                        })

            self.logger.info(f"Grouped {len(all_players_with_ranks)} players for position-specific ranking")

        parsed_count = 0
        skipped_drafted_count = 0
        skipped_low_score_count = 0
        for player in players:
            try:
                # Extract basic info
                player_info = player.get('player', {})
                id = str(player_info.get('id', ''))
                
                if not id:
                    if progress_tracker:
                        progress_tracker.update()
                    continue
                
                # Extract name parts
                name_parts = []
                if player_info.get('firstName'):
                    name_parts.append(player_info['firstName'])
                if player_info.get('lastName'):  
                    name_parts.append(player_info['lastName'])
                name = ' '.join(name_parts) if name_parts else 'Unknown Player'
                
                # Extract team
                pro_team_id = player_info.get('proTeamId')
                team = ESPN_TEAM_MAPPINGS.get(pro_team_id, 'UNK')

                # OPTIMIZATION: Skip expensive API calls for drafted=1 players if enabled
                if SKIP_DRAFTED_PLAYER_UPDATES and id in self.drafted_player_ids:
                    self.logger.debug(f"Skipping API calls for drafted player: {name} (ID: {id})")
                    skipped_drafted_count += 1
                    if progress_tracker:
                        progress_tracker.update()
                    continue

                # OPTIMIZATION: Skip API calls for low-scoring players and preserve their data
                if USE_SCORE_THRESHOLD and id in self.low_score_player_data:
                    self.logger.debug(f"Preserving data for low-scoring player: {name} (ID: {id})")
                    # Add preserved player data to projections without API calls
                    preserved_data = self.low_score_player_data[id]
                    preserved_projection = ESPNPlayerData(
                        id=id,
                        name=preserved_data.get('name', name),
                        team=preserved_data.get('team', ''),
                        position=preserved_data.get('position', ''),
                        bye_week=int(preserved_data.get('bye_week', 0)) if preserved_data.get('bye_week') else None,
                        fantasy_points=float(preserved_data.get('fantasy_points', 0.0)),
                        injury_status=preserved_data.get('injury_status', 'UNKNOWN'),
                        average_draft_position=float(preserved_data.get('average_draft_position', 0.0)) if preserved_data.get('average_draft_position') else None
                    )
                    projections.append(preserved_projection)
                    skipped_low_score_count += 1
                    if progress_tracker:
                        progress_tracker.update()
                    continue

                # Skip players not on active NFL rosters (free agents, practice squad, etc.)
                if team == 'UNK':
                    if progress_tracker:
                        progress_tracker.update()
                    continue
                
                # Extract position
                position_id = player_info.get('defaultPositionId')
                position = ESPN_POSITION_MAPPINGS.get(position_id, 'UNKNOWN')

                # Skip players with unknown positions to avoid downstream errors
                if position == 'UNKNOWN':
                    self.logger.debug(f"Skipping player {name} (ID: {id}) with unknown position ID: {position_id}")
                    unknown_position_count += 1
                    if progress_tracker:
                        progress_tracker.update()
                    continue

                # Get bye week
                bye_week = self.bye_weeks.get(team)
                
                # Extract fantasy points using ONLY week-by-week calculation
                fantasy_points = await self._calculate_week_by_week_projection(id, name, position)
                
                # Fantasy points are already positive from our selection logic above
                
                # Extract injury status
                injury_status = "ACTIVE"  # Default
                injury_info = player_info.get('injuryStatus')
                if injury_info:
                    injury_status = injury_info.upper()
                
                # Extract ADP data
                average_draft_position = None
                ownership_data = player_info.get('ownership', {})
                if ownership_data and 'averageDraftPosition' in ownership_data:
                    average_draft_position = float(ownership_data['averageDraftPosition'])

                # Extract ESPN player rating (position-specific consensus rankings)
                player_rating = None
                positional_rank = None

                # Determine which ranking source to use based on current week
                if CURRENT_NFL_WEEK <= 1:
                    # Pre-season/Week 1: Use draft rankings (ROS not updated yet)
                    # Convert overall draft rank to position-specific
                    draft_ranks = player_info.get('draftRanksByRankType', {})
                    ppr_rank_data = draft_ranks.get('PPR', {})

                    if ppr_rank_data and 'rank' in ppr_rank_data:
                        draft_rank = ppr_rank_data['rank']
                        positional_rank = self._get_positional_rank_from_overall(
                            draft_rank, position, all_players_with_ranks
                        )

                        if positional_rank is None:
                            self.logger.warning(
                                f"No draft rank found for {name} (ID: {id}), using default rating"
                            )
                else:
                    # During season (Week 2+): Use current week's ROS consensus rankings
                    # rankings[N] = "ROS consensus snapshot taken during Week N"
                    # Use current week's snapshot for most up-to-date expert consensus
                    # Exception: Week 1 uses rankings['0'] (pre-season) since Week 1 rankings may be sparse

                    ranking_key = '0' if CURRENT_NFL_WEEK == 1 else str(CURRENT_NFL_WEEK)
                    rankings_ros = player_info.get('rankings', {}).get(ranking_key, [])

                    if not rankings_ros:
                        # Fallback: Find the most recent available week (working backwards from current week)
                        all_rankings = player_info.get('rankings', {})

                        # Try weeks in descending order from current week down to week 1
                        for fallback_week in range(CURRENT_NFL_WEEK - 1, 0, -1):
                            fallback_key = str(fallback_week)
                            if fallback_key in all_rankings and all_rankings[fallback_key]:
                                rankings_ros = all_rankings[fallback_key]
                                self.logger.debug(
                                    f"No rankings['{ranking_key}'] for {name}, using rankings['{fallback_key}'] (most recent available)"
                                )
                                break

                        # Final fallback to rankings['0'] if no weekly data exists
                        if not rankings_ros and '0' in all_rankings:
                            rankings_ros = all_rankings['0']
                            self.logger.debug(
                                f"No weekly rankings for {name}, using rankings['0'] (pre-season)"
                            )

                    if rankings_ros:
                        # Look for PPR rankType with averageRank field
                        expected_slot_id = self._position_to_slot_id(position)

                        for ranking_entry in rankings_ros:
                            if ranking_entry.get('rankType') == 'PPR':
                                actual_slot_id = ranking_entry.get('slotId')

                                # Validate slotId matches position
                                if actual_slot_id == expected_slot_id:
                                    if 'averageRank' in ranking_entry:
                                        positional_rank = ranking_entry['averageRank']
                                        break
                                elif actual_slot_id is not None and expected_slot_id != -1:
                                    self.logger.warning(
                                        f"slotId mismatch for {name}: expected {expected_slot_id}, got {actual_slot_id}, skipping"
                                    )

                # Convert positional rank to 0-100 rating scale
                if positional_rank is not None:
                    player_rating = self._convert_positional_rank_to_rating(positional_rank)
                else:
                    # Fallback: Use original overall draft rank formula
                    draft_ranks = player_info.get('draftRanksByRankType', {})
                    ppr_rank_data = draft_ranks.get('PPR', {})

                    if ppr_rank_data and 'rank' in ppr_rank_data:
                        draft_rank = ppr_rank_data['rank']
                        # Original formula preserved as fallback
                        if draft_rank <= 50:  # Elite players
                            player_rating = 100.0 - (draft_rank - 1) * 0.4  # 100 to 80.4
                        elif draft_rank <= 150:  # Good players
                            player_rating = 80.0 - (draft_rank - 50) * 0.25  # 80 to 55
                        elif draft_rank <= 300:  # Average players
                            player_rating = 55.0 - (draft_rank - 150) * 0.2  # 55 to 25
                        else:  # Deep/waiver players
                            player_rating = max(15.0, 25.0 - (draft_rank - 300) * 0.01)  # 25 to 15

                        self.logger.warning(
                            f"Rankings object missing for {name} (ID: {id}), using draft rank fallback"
                        )

                # Create player projection

                projection = ESPNPlayerData(
                    id=id,
                    name=name,
                    team=team,
                    position=position,
                    bye_week=bye_week,
                    drafted=0,  # Initialize all players as not drafted
                    fantasy_points=fantasy_points,
                    average_draft_position=average_draft_position,
                    player_rating=player_rating,
                    injury_status=injury_status,
                    api_source="ESPN"
                )

                # Collect weekly projections for this player
                await self._populate_weekly_projections(projection, id, name, position)
                
                projections.append(projection)
                parsed_count += 1

                # Update progress tracker
                if progress_tracker:
                    progress_tracker.update()

            except (KeyError, TypeError, ValueError) as e:
                player_id = player.get('player', {}).get('id', 'unknown')
                self.logger.warning(f"Failed to parse player {player_id}: {e}")
                if progress_tracker:
                    progress_tracker.update()
                continue
            except Exception as e:
                player_id = player.get('player', {}).get('id', 'unknown')
                self.logger.error(f"Unexpected error parsing player {player_id}: {e}")
                if progress_tracker:
                    progress_tracker.update()
                continue
        
        # Log parsing results with optimization info
        optimization_messages = []
        if SKIP_DRAFTED_PLAYER_UPDATES and skipped_drafted_count > 0:
            optimization_messages.append(f"skipped {skipped_drafted_count} drafted players")
        if USE_SCORE_THRESHOLD and skipped_low_score_count > 0:
            optimization_messages.append(f"preserved {skipped_low_score_count} low-scoring players")

        if optimization_messages:
            self.logger.info(f"Successfully parsed {parsed_count} players with projections "
                           f"({', '.join(optimization_messages)} for optimization)")
        else:
            self.logger.info(f"Successfully parsed {parsed_count} players with projections")

        # Complete progress tracking
        if progress_tracker:
            progress_tracker.complete()

        # Log filtering statistics
        if unknown_position_count > 0:
            self.logger.info(f"Filtered out {unknown_position_count} players with unknown positions")

        # Calculate position-specific defense rankings
        from config import CURRENT_NFL_WEEK
        position_defense_rankings = self._calculate_position_defense_rankings(
            projections,
            full_season_schedule,
            CURRENT_NFL_WEEK
        )

        # Store position defense rankings for later use
        self.position_defense_rankings = position_defense_rankings

        return projections
