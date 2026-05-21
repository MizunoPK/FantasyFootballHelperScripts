#!/usr/bin/env python3
"""
ESPN Fantasy API Client

This module handles all ESPN API interactions for fantasy football data collection.
Separated from the main script for better organization and maintainability.

Author: Kai Mizuno
"""

import asyncio
from contextlib import asynccontextmanager
import datetime
import json
import math
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from urllib.parse import urlparse

import httpx
from tenacity import retry, stop_after_attempt, wait_random_exponential

from player_data_fetcher.player_data_models import ESPNPlayerData, ScoringFormat
from player_data_fetcher.fantasy_points_calculator import FantasyPointsExtractor, FantasyPointsConfig
from player_data_fetcher.player_data_constants import (
    ESPN_TEAM_MAPPINGS, ESPN_POSITION_MAPPINGS, MIN_WEEKS_FOR_RANKINGS
)
from player_data_fetcher.config import ESPN_USER_AGENT
from utils.LoggingManager import get_logger
from utils.csv_utils import read_dict_csv


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
        self._client = None
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
        async with self._session_lock:
            if self._client is None:
                timeout = httpx.Timeout(self.settings.request_timeout)
                self._client = httpx.AsyncClient(timeout=timeout)
                self.logger.debug("Created new HTTP client session")

        try:
            yield self._client
        finally:
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

    @staticmethod
    def _get_fixture_filename(url: str, params: dict) -> str:
        """Map an ESPN API URL + params to a deterministic fixture filename.

        Args:
            url: ESPN API endpoint URL
            params: Query parameters dict (may be empty)

        Returns:
            Fixture filename (without directory prefix)

        Raises:
            ValueError: If url does not match any known ESPN API endpoint
        """
        path = urlparse(url).path

        if "nfl/scoreboard" in path:
            week = params.get("week", "unknown")
            dates = params.get("dates", "unknown")
            return f"scoreboard_week_{week}_{dates}.json"
        elif path.rstrip("/").endswith("/nfl/teams"):
            return "teams_list.json"
        elif "/nfl/teams/" in path and "/statistics" in path:
            parts = path.split("/")
            team_id = parts[parts.index("teams") + 1]
            return f"team_stats_{team_id}.json"
        elif "leaguedefaults" in path:
            parts = path.split("/")
            season_idx = parts.index("seasons") + 1
            season = parts[season_idx]
            return f"season_projections_{season}.json"
        else:
            raise ValueError(
                f"No fixture filename defined for URL: {url}. "
                f"Add a mapping to BaseAPIClient._get_fixture_filename()."
            )

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

        fixture_dir = os.environ.get("ESPN_FIXTURE_DIR")
        if fixture_dir:
            params = kwargs.get("params", {}) or {}
            filename = self._get_fixture_filename(url, params)
            fixture_path = Path(fixture_dir) / "espn_api" / filename
            if not fixture_path.exists():
                raise FileNotFoundError(
                    f"Fixture file not found: {fixture_path}. "
                    f"Run the fixture recording mechanism to populate the fixture directory."
                )
            return json.loads(fixture_path.read_text())

        await asyncio.sleep(self.settings.rate_limit_delay)

        try:
            response = await self._client.request(method, url, **kwargs)

            if response.status_code == 429:
                raise ESPNRateLimitError(f"Rate limit exceeded: {response.status_code}")
            elif response.status_code >= 500:
                raise ESPNServerError(f"ESPN server error: {response.status_code}")
            elif response.status_code >= 400:
                raise ESPNAPIError(f"ESPN API error: {response.status_code}")

            response.raise_for_status()
            self.logger.debug("Request successful")

            data = response.json()

            record_dir = os.environ.get("ESPN_RECORD_FIXTURES_DIR")
            if record_dir:
                params = kwargs.get("params", {}) or {}
                filename = self._get_fixture_filename(url, params)
                record_path = Path(record_dir) / "espn_api" / filename
                record_path.parent.mkdir(parents=True, exist_ok=True)
                record_path.write_text(json.dumps(data, indent=2))

            return data

        except httpx.RequestError as e:
            self.logger.error(f"Request failed: {e}")
            raise ESPNAPIError(f"Network error: {e}")
        except Exception as e:
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
    - Uses bulk API fetch with scoringPeriodId=0 for all weekly stats in one call
    """


    def __init__(self, settings):
        """
        Initialize ESPN API client for player data collection.

        Sets up:
        - HTTP client session (inherited from BaseAPIClient)
        - Bye week mappings for NFL teams
        - Team rankings cache (offensive/defensive quality)
        - Current week schedule cache (team matchups)
        - Shared fantasy points extractor for consistent scoring calculations

        Args:
            settings: Settings object with season, scoring_format, timeouts, etc.
        """
        super().__init__(settings)

        self.bye_weeks: Dict[str, int] = {}

        self.team_rankings: Dict[str, Dict[str, int]] = {}

        self.current_week_schedule: Dict[str, str] = {}

        fp_config = FantasyPointsConfig(
            prefer_actual_over_projected=True,
            include_negative_dst_points=True
        )
        self.fantasy_points_extractor = FantasyPointsExtractor(fp_config, settings.season)
    
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
        if self.team_rankings:
            return self.team_rankings

        try:
            self.logger.info("Fetching team quality rankings from ESPN")

            team_stats_url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams"

            async with self.session() as client:
                team_data = await self._make_request("GET", team_stats_url)

            teams = team_data.get('teams', [])
            team_rankings = {}

            team_rankings = await self._calculate_team_rankings_from_stats()

            self.team_rankings = team_rankings
            self.logger.info(f"Calculated data-driven rankings for {len(team_rankings)} teams")

            return self.team_rankings

        except Exception as e:
            self.logger.error(f"Failed to fetch team rankings: {e}")
            return {}

    def _get_cache_path(self, cache_dir: Optional[Path] = None) -> Path:
        """
        Compute the date-stamped cache file path.

        Args:
            cache_dir: Optional override of the cache base directory; defaults
                to `<project_root>/data` when None. Used for test isolation.

        Returns:
            Path to today's cache file.
        """
        date = datetime.date.today().isoformat()
        base_dir = cache_dir if cache_dir is not None else Path(__file__).parent.parent / 'data'
        return base_dir / f'team_rankings_cache_{date}.json'

    def _load_rankings_from_cache(self, cache_dir: Optional[Path] = None) -> Optional[Dict[str, Dict[str, int]]]:
        """
        Attempt to load today's team rankings from the date-stamped cache file.

        Args:
            cache_dir: Optional override of the cache base directory; defaults
                to `<project_root>/data` when None. Used for test isolation.

        Returns:
            Dict mapping team abbreviations to {'offensive_rank': int, 'defensive_rank': int}
            if today's cache file exists and is valid; None if cache miss or read error.
        """
        cache_path = self._get_cache_path(cache_dir)
        if not cache_path.exists():
            return None
        try:
            with open(cache_path, 'r') as f:
                data = json.load(f)
            if not isinstance(data, dict) or not data:
                return None
            sample = next(iter(data.values()))
            if not isinstance(sample, dict) or not isinstance(sample.get('offensive_rank'), int) or not isinstance(sample.get('defensive_rank'), int):
                self.logger.warning(f"Rankings cache {cache_path} has invalid schema, re-fetching from API")
                return None
            self.logger.info(f"Loaded team rankings from cache: {cache_path}")
            return data
        except Exception as e:
            self.logger.warning(f"Failed to read rankings cache {cache_path}: {e}")
            return None

    def _save_rankings_to_cache(self, rankings: Dict[str, Dict[str, int]], cache_dir: Optional[Path] = None) -> None:
        """
        Save team rankings to the date-stamped cache file.

        Does not raise on write errors — logs a warning and returns silently.

        Args:
            rankings: Dict mapping team abbreviations to rank dicts.
            cache_dir: Optional override of the cache base directory; defaults
                to `<project_root>/data` when None. Used for test isolation.
        """
        cache_path = self._get_cache_path(cache_dir)
        try:
            with open(cache_path, 'w') as f:
                json.dump(rankings, f, indent=2)
            self.logger.info(f"Saved team rankings to cache: {cache_path}")
        except Exception as e:
            self.logger.warning(f"Failed to write rankings cache {cache_path}: {e}")

    def _calculate_week_by_week_projection(self, player_info: dict, name: str, position: str) -> float:
        """
        Calculate remaining season projection by summing current + future week projections.

        Uses stats array from bulk API response (no additional API calls needed).

        Args:
            player_info: Player data dict containing 'stats' array from bulk fetch
            name: Player name for logging
            position: Player position (QB, RB, WR, TE, K, DST)

        Returns:
            Total projected fantasy points for remaining season
        """
        try:
            if not player_info.get('stats'):
                return 0.0

            end_week = 17
            start_week = self.settings.current_nfl_week

            total_projection = 0.0
            weeks_processed = 0

            for week in range(start_week, end_week + 1):
                week_points = None

                week_points = self._extract_week_points(player_info, week, position=position, player_name=name)

                if week == self.settings.current_nfl_week:
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

    def _extract_week_points(self, player_data: dict, week: int, position: str, player_name: str = "Unknown") -> float:
        """
        Extract points for a specific week from player data using shared logic

        NOTE: This uses the shared FantasyPointsExtractor for consistent logic.
        ESPN API uses appliedTotal field with statSourceId to distinguish:
        - statSourceId=0 + appliedTotal = Actual game scores
        - statSourceId=1 + appliedTotal = ESPN projections
        """
        try:
            points = self.fantasy_points_extractor.extract_week_points(
                player_data={'player': player_data},
                week=week,
                position=position,
                player_name=player_name,
                current_nfl_week=self.settings.current_nfl_week
            )

            return points if points is not None else 0.0

        except Exception as e:
            self.logger.error(f"Error extracting week points for {player_name} week {week}: {str(e)}")
            return 0.0

    def _populate_weekly_projections(self, player_data: ESPNPlayerData, player_info: dict, name: str, position: str):
        """
        Populate weekly projections for a player.

        Uses stats array from bulk API response (no additional API calls needed).

        This method populates two sets of data:
        1. week_N_points: Smart values (actual for past weeks, projection for future)
        2. projected_weeks: Projection-only values (statSourceId=1 for ALL weeks)

        Args:
            player_data: The ESPNPlayerData object to populate
            player_info: Player data dict containing 'stats' array from bulk fetch
            name: Player name for logging
            position: Player position
        """
        try:
            if not player_info.get('stats'):
                return

            end_week = 17

            for week in range(1, end_week + 1):
                smart_points = self._extract_raw_espn_week_points(player_info, week, position, 'smart')

                if smart_points is not None and (smart_points > 0 or position == 'DST'):
                    player_data.set_week_points(week, smart_points)
                    self.logger.debug(f"{name} Week {week}: {smart_points:.1f} points (smart)")
                else:
                    player_data.set_week_points(week, 0.0)
                    if position == 'DST':
                        self.logger.debug(f"{name} Week {week}: 0.0 points (likely bye week)")
                    else:
                        self.logger.debug(f"{name} Week {week}: 0.0 points (no data)")

                projected_points = self._extract_raw_espn_week_points(player_info, week, position, 'projection')

                if projected_points is not None and (projected_points > 0 or position == 'DST'):
                    player_data.set_week_projected(week, projected_points)
                    self.logger.debug(f"{name} Week {week}: {projected_points:.1f} projected")
                else:
                    player_data.set_week_projected(week, 0.0)

        except Exception as e:
            self.logger.warning(f"Failed to populate weekly projections for {name}: {str(e)}")

    def _extract_raw_espn_week_points(
        self,
        player_data: dict,
        week: int,
        position: str,
        source_type: str = 'smart'
    ) -> Optional[float]:
        """
        Extract fantasy points for a specific week from ESPN's complex data structure.

        This method handles ESPN's multi-layered stat system where the same week can have:
        - Multiple stat entries (actual vs projected)
        - Multiple data sources (statSourceId=0 for actuals, statSourceId=1 for projections)

        ESPN Data Structure (for one week):
        [
          {"seasonId": 2024, "scoringPeriodId": 7, "statSourceId": 0, "appliedTotal": 18.2, ...},  # Actual results
          {"seasonId": 2024, "scoringPeriodId": 7, "statSourceId": 1, "appliedTotal": 15.8, ...}   # Projections
        ]

        ESPN API Structure:
        - statSourceId=0 + appliedTotal = Actual game scores (for completed weeks)
        - statSourceId=1 + appliedTotal = ESPN projections (for all weeks)
        - NOTE: The 'projectedTotal' field does NOT exist in ESPN's current API

        Special handling:
        - DST positions: Allow negative fantasy points (e.g., -2.0 for bad defense performance)
        - Other positions: Filter out negative/zero values (invalid data)
        - NaN values: Treated as invalid and skipped

        Args:
            player_data: Dict containing 'stats' array (from bulk fetch)
            week: Week number (1-18)
            position: Player position (QB, RB, WR, TE, K, DST)
            source_type: Data extraction mode:
                - 'smart' (default): Actual if available, fallback to projection
                - 'actual': Only return statSourceId=0 data (actual game scores)
                - 'projection': Only return statSourceId=1 data (ESPN projections)

        Returns:
            Float: Fantasy points for the week, or None if no ESPN data available
        """
        try:
            stats = player_data.get('stats', [])
            if not stats:
                return None

            actual_entries = []
            projected_entries = []

            for stat in stats:
                if not isinstance(stat, dict):
                    continue

                season_id = stat.get('seasonId')
                scoring_period = stat.get('scoringPeriodId')

                if season_id == self.settings.season and scoring_period == week:
                    stat_source_id = stat.get('statSourceId')

                    points = None
                    if 'appliedTotal' in stat and stat['appliedTotal'] is not None:
                        try:
                            points = float(stat['appliedTotal'])
                            if math.isnan(points):
                                continue
                        except (ValueError, TypeError):
                            continue

                    if points is not None:
                        if stat_source_id == 0:
                            actual_entries.append(points)
                        elif stat_source_id == 1:
                            projected_entries.append(points)

            if source_type == 'actual':
                if actual_entries:
                    valid_actuals = [p for p in actual_entries if position == 'DST' or p > 0]
                    if valid_actuals:
                        return valid_actuals[0]
                return None

            elif source_type == 'projection':
                if projected_entries:
                    valid_projected = [p for p in projected_entries if position == 'DST' or p > 0]
                    if valid_projected:
                        return valid_projected[0]
                return None

            else:
                if actual_entries:
                    valid_actuals = [p for p in actual_entries if position == 'DST' or p > 0]
                    if valid_actuals:
                        return valid_actuals[0]

                if projected_entries:
                    valid_projected = [p for p in projected_entries if position == 'DST' or p > 0]
                    if valid_projected:
                        return valid_projected[0]

                return None

        except Exception as e:
            self.logger.debug(f"Error extracting raw ESPN week points: {str(e)}")
            return None


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

        url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{use_season}/segments/0/leaguedefaults/{ppr_id}"
        
        params = {
            "view": "kona_player_info",
            "scoringPeriodId": 0
        }
        
        headers = {
            'User-Agent': ESPN_USER_AGENT,
            'X-Fantasy-Filter': f'{{"players":{{"limit":{self.settings.espn_player_limit},"sortPercOwned":{{"sortPriority":4,"sortAsc":false}}}}}}'
        }
        
        data = await self._make_request("GET", url, params=params, headers=headers)
        return await self._parse_espn_data(data)
    
    async def _make_request(self, method: str, url: str, **kwargs):
        """Override to add ESPN-specific headers"""
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        
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
            cached = await asyncio.to_thread(self._load_rankings_from_cache)
            if cached is not None:
                return cached

            min_weeks_for_rankings = MIN_WEEKS_FOR_RANKINGS

            use_current_season = self.settings.current_nfl_week > min_weeks_for_rankings

            self.logger.info(f"Team rankings: Using {'current season' if use_current_season else 'neutral'} data. "
                           f"Current week: {self.settings.current_nfl_week}, Min weeks needed: {min_weeks_for_rankings}")

            if not use_current_season:
                self.logger.info(f"Not enough weeks for current season rankings - using neutral data (all ranks = 16)")
                return self._get_fallback_team_rankings()

            team_ids = {
                1: 'ATL', 2: 'BUF', 3: 'CHI', 4: 'CIN', 5: 'CLE', 6: 'DAL', 7: 'DEN', 8: 'DET',
                9: 'GB', 10: 'TEN', 11: 'IND', 12: 'KC', 13: 'LV', 14: 'LAR', 15: 'MIA', 16: 'MIN',
                17: 'NE', 18: 'NO', 19: 'NYG', 20: 'NYJ', 21: 'PHI', 22: 'ARI', 23: 'PIT', 24: 'LAC',
                25: 'SF', 26: 'SEA', 27: 'TB', 28: 'WSH', 29: 'CAR', 30: 'JAX', 33: 'BAL', 34: 'HOU'
            }

            team_rankings = await self._calculate_rolling_window_rankings(self.settings.current_nfl_week, min_weeks_for_rankings)
            await asyncio.to_thread(self._save_rankings_to_cache, team_rankings)
            return team_rankings

        except Exception as e:
            min_weeks_for_rankings = MIN_WEEKS_FOR_RANKINGS
            use_current_season = self.settings.current_nfl_week > min_weeks_for_rankings
            season_info = f"{self.settings.season} season" if use_current_season else "neutral data"

            self.logger.error(f"Error calculating team rankings for {season_info}: {e}")

            self.logger.info(f"Falling back to neutral team rankings (all ranks = 16)")
            return self._get_fallback_team_rankings()

    async def _calculate_team_rankings_for_season(self, season: int, team_ids: Dict[int, str]) -> Dict[str, Dict[str, int]]:
        """
        Helper method to calculate team rankings for a specific season.

        DEPRECATED: This method uses cumulative season statistics from ESPN's team stats API.
        It has been replaced by _calculate_rolling_window_rankings() which uses a rolling
        window of recent game scores for more current team performance assessment.

        Kept for potential historical analysis use cases.
        """
        team_stats = {}
        all_teams = list(team_ids.items())

        for team_id, team_abbr in all_teams:
            try:
                team_stats_url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/statistics"

                self.logger.debug(f"Fetching team {team_abbr} stats (intended season: {season}, actual: current season)")

                async with self.session() as client:
                    stats_data = await self._make_request("GET", team_stats_url)

                if stats_data and 'results' in stats_data and 'stats' in stats_data['results']:
                    stats = stats_data['results']['stats']

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

        if len(team_stats) >= 3:
            sorted_offensive = sorted(team_stats.items(), key=lambda x: x[1]['offensive_points'], reverse=True)
            sorted_defensive = sorted(team_stats.items(), key=lambda x: x[1]['takeaways'], reverse=True)

            team_rankings = {}

            for rank, (team, stats) in enumerate(sorted_offensive, 1):
                team_rankings[team] = {'offensive_rank': rank}

            for rank, (team, stats) in enumerate(sorted_defensive, 1):
                if team in team_rankings:
                    team_rankings[team]['defensive_rank'] = rank

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

    async def _calculate_rolling_window_rankings(
        self,
        current_week: int,
        min_weeks: int
    ) -> Dict[str, Dict[str, int]]:
        """
        Calculate team rankings from rolling window of recent weeks.

        Uses game scores from the most recent MIN_WEEKS previous weeks to calculate
        offensive and defensive rankings. This provides more current team performance
        compared to cumulative season statistics.

        Rolling Window Example (MIN_WEEKS=4, current_week=10):
        - Analyzes weeks 6, 7, 8, 9 (previous 4 weeks)
        - Excludes current week (10) and earlier weeks (1-5)

        Args:
            current_week: Current NFL week (1-18)
            min_weeks: Number of weeks to include in rolling window

        Returns:
            Dict[team, {'offensive_rank': int, 'defensive_rank': int}]
            Rankings are 1-32 where 1 = best, 16 = neutral
        """
        from collections import defaultdict

        window_start = max(1, current_week - min_weeks)
        window_weeks = list(range(window_start, current_week))

        self.logger.info(
            f"Calculating rolling {len(window_weeks)}-week rankings "
            f"from weeks {window_start} to {current_week - 1}"
        )

        all_games = []
        for week in window_weeks:
            try:
                week_games = await self._fetch_week_scores(week)
                completed_games = [g for g in week_games if g['is_completed']]
                all_games.extend(completed_games)
                self.logger.debug(
                    f"Week {week}: {len(completed_games)} completed games fetched"
                )
            except Exception as e:
                self.logger.warning(f"Failed to fetch week {week} scores: {e}")
                continue

        if not all_games:
            self.logger.error("No games fetched for rolling window, using neutral rankings")
            return self._get_fallback_team_rankings()

        team_offensive = defaultdict(lambda: {'points_scored': 0, 'games': 0})
        team_defensive = defaultdict(lambda: {'points_allowed': 0, 'games': 0})

        for game in all_games:
            home_team = game['home_team']
            away_team = game['away_team']
            home_score = game['home_score']
            away_score = game['away_score']

            team_offensive[home_team]['points_scored'] += home_score
            team_offensive[home_team]['games'] += 1
            team_offensive[away_team]['points_scored'] += away_score
            team_offensive[away_team]['games'] += 1

            team_defensive[home_team]['points_allowed'] += away_score
            team_defensive[home_team]['games'] += 1
            team_defensive[away_team]['points_allowed'] += home_score
            team_defensive[away_team]['games'] += 1

        team_offensive_avg = {}
        team_defensive_avg = {}

        for team, stats in team_offensive.items():
            if stats['games'] > 0:
                avg = stats['points_scored'] / stats['games']
                team_offensive_avg[team] = avg
                self.logger.debug(
                    f"{team} offense: {stats['points_scored']} pts in "
                    f"{stats['games']} games = {avg:.1f} ppg"
                )

        for team, stats in team_defensive.items():
            if stats['games'] > 0:
                avg = stats['points_allowed'] / stats['games']
                team_defensive_avg[team] = avg
                self.logger.debug(
                    f"{team} defense: {stats['points_allowed']} pts allowed in "
                    f"{stats['games']} games = {avg:.1f} ppg allowed"
                )

        sorted_offensive = sorted(
            team_offensive_avg.items(),
            key=lambda x: x[1],
            reverse=True
        )
        sorted_defensive = sorted(
            team_defensive_avg.items(),
            key=lambda x: x[1],
            reverse=False
        )

        team_rankings = {}

        for rank, (team, avg) in enumerate(sorted_offensive, 1):
            team_rankings[team] = {'offensive_rank': rank}
            self.logger.debug(f"{team}: offensive_rank={rank} ({avg:.1f} ppg)")

        for rank, (team, avg) in enumerate(sorted_defensive, 1):
            if team in team_rankings:
                team_rankings[team]['defensive_rank'] = rank
            else:
                team_rankings[team] = {'defensive_rank': rank}
            self.logger.debug(f"{team}: defensive_rank={rank} ({avg:.1f} ppg allowed)")

        all_nfl_teams = [
            'KC', 'NE', 'LAC', 'LAR', 'SF', 'DAL', 'PHI', 'NYG', 'WSH', 'CHI',
            'GB', 'MIN', 'DET', 'ATL', 'CAR', 'NO', 'TB', 'SEA', 'ARI', 'BAL',
            'PIT', 'CLE', 'CIN', 'BUF', 'MIA', 'NYJ', 'TEN', 'IND', 'HOU', 'JAX',
            'LV', 'DEN'
        ]

        for team in all_nfl_teams:
            if team not in team_rankings:
                team_rankings[team] = {'offensive_rank': 16, 'defensive_rank': 16}
            elif 'offensive_rank' not in team_rankings[team]:
                team_rankings[team]['offensive_rank'] = 16
            elif 'defensive_rank' not in team_rankings[team]:
                team_rankings[team]['defensive_rank'] = 16

        self.logger.info(
            f"Rolling window rankings complete: {len(all_games)} games analyzed, "
            f"{len(team_rankings)} teams ranked"
        )

        return team_rankings

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
            self.logger.info(f"Fetching week {self.settings.current_nfl_week} schedule from ESPN")

            url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
            params = {
                "seasontype": 2,
                "week": self.settings.current_nfl_week,
                "dates": self.settings.season
            }

            data = await self._make_request("GET", url, params=params)

            schedule_map = {}
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

                    team1_data = competitors[0].get('team', {})
                    team2_data = competitors[1].get('team', {})

                    team1_abbrev = team1_data.get('abbreviation', '')
                    team2_abbrev = team2_data.get('abbreviation', '')

                    team1_abbrev = 'WSH' if team1_abbrev == 'WAS' else team1_abbrev
                    team2_abbrev = 'WSH' if team2_abbrev == 'WAS' else team2_abbrev

                    if team1_abbrev and team2_abbrev:
                        schedule_map[team1_abbrev] = team2_abbrev
                        schedule_map[team2_abbrev] = team1_abbrev

                except Exception as e:
                    self.logger.warning(f"Error parsing schedule event: {e}")
                    continue

            self.logger.info(f"Retrieved schedule for {len(schedule_map)} teams in week {self.settings.current_nfl_week}")
            return schedule_map

        except Exception as e:
            self.logger.error(f"Failed to fetch current week schedule: {e}")
            return {}

    def _load_season_schedule_from_csv(self, csv_path: Optional[Path] = None) -> Dict[int, Dict[str, str]]:
        """
        Load the full season schedule from data/season_schedule.csv.

        Args:
            csv_path: Optional override path; defaults to
                ``<project_root>/data/season_schedule.csv``. Used for test isolation.

        Returns:
            Dict mapping week number to team-opponent mapping
            (e.g. ``{1: {'KC': 'DEN', 'DEN': 'KC', ...}, ...}``).
            Returns ``{}`` on any read or parse error.
        """
        try:
            csv_path = csv_path or Path(__file__).parent.parent / "data" / "season_schedule.csv"
            rows = read_dict_csv(csv_path, required_columns=['week', 'team', 'opponent'])
        except FileNotFoundError as e:
            self.logger.error(f"Failed to load season schedule from CSV: {e}")
            return {}
        except Exception as e:
            self.logger.error(f"Failed to load season schedule from CSV: {e}")
            return {}
        try:
            schedule: Dict[int, Dict[str, str]] = {}
            for row in rows:
                week_num = int(row['week'])
                if week_num not in schedule:
                    schedule[week_num] = {}
                schedule[week_num][row['team']] = row['opponent']
            return schedule
        except Exception as e:
            self.logger.error(f"Failed to load season schedule from CSV: {e}")
            return {}

    async def _fetch_week_scores(self, week: int) -> List[Dict]:
        """
        Fetch game scores for a specific week from ESPN scoreboard API.

        Args:
            week: NFL week number (1-18)

        Returns:
            List of game dictionaries with structure:
            [
                {
                    'home_team': 'KC',
                    'away_team': 'DEN',
                    'home_score': 27,
                    'away_score': 14,
                    'is_completed': True
                },
                ...
            ]
        """
        url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
        params = {
            "seasontype": 2,
            "week": week,
            "dates": self.settings.season
        }

        data = await self._make_request("GET", url, params=params)
        games = []

        for event in data.get('events', []):
            competitions = event.get('competitions', [])
            if not competitions:
                continue

            competition = competitions[0]
            status = competition.get('status', {}).get('type', {})
            is_completed = status.get('completed', False)

            competitors = competition.get('competitors', [])
            if len(competitors) != 2:
                continue

            home_data = None
            away_data = None

            for competitor in competitors:
                if competitor.get('homeAway') == 'home':
                    home_data = competitor
                else:
                    away_data = competitor

            if not home_data or not away_data:
                continue

            home_abbrev = home_data.get('team', {}).get('abbreviation', '')
            away_abbrev = away_data.get('team', {}).get('abbreviation', '')
            home_score = int(home_data.get('score', 0))
            away_score = int(away_data.get('score', 0))

            home_abbrev = 'WSH' if home_abbrev == 'WAS' else home_abbrev
            away_abbrev = 'WSH' if away_abbrev == 'WAS' else away_abbrev

            games.append({
                'home_team': home_abbrev,
                'away_team': away_abbrev,
                'home_score': home_score,
                'away_score': away_score,
                'is_completed': is_completed
            })

        return games

    def _calculate_position_defense_rankings(
        self,
        players: List[ESPNPlayerData],
        schedule: Dict[int, Dict[str, str]],
        current_week: int
    ) -> Dict[str, Dict[str, int]]:
        """
        Calculate position-specific defense rankings for all teams using a rolling window.

        Uses the most recent 5 weeks of data (default rolling window)
        to calculate how many points each defense has allowed to each position.

        Rolling Window Example (MIN_WEEKS=4, current_week=10):
        - Analyzes weeks 6, 7, 8, 9 (previous 4 weeks)
        - Excludes current week (10) and earlier weeks (1-5)
        - Ranks defenses based on points allowed to QB, RB, WR, TE, K

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

        defense_stats = defaultdict(lambda: defaultdict(float))

        all_teams = [
            'ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE',
            'DAL', 'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAX', 'KC',
            'LAC', 'LAR', 'LV', 'MIA', 'MIN', 'NE', 'NO', 'NYG',
            'NYJ', 'PHI', 'PIT', 'SEA', 'SF', 'TB', 'TEN', 'WSH'
        ]

        min_weeks_for_rankings = MIN_WEEKS_FOR_RANKINGS
        window_start = max(1, current_week - min_weeks_for_rankings)

        for player in players:
            if player.position not in ['QB', 'RB', 'WR', 'TE', 'K']:
                continue

            for week in range(window_start, current_week):
                week_schedule = schedule.get(week, {})
                opponent_defense = week_schedule.get(player.team)

                if not opponent_defense:
                    continue

                week_points = player.get_week_points(week)

                if week_points is None:
                    continue

                if week_points <= 0 and player.position != 'DST':
                    continue

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

        rankings = {}
        for position in ['vs_qb', 'vs_rb', 'vs_wr', 'vs_te', 'vs_k']:
            teams_with_data = [
                (team, stats[position])
                for team, stats in defense_stats.items()
                if position in stats and stats[position] > 0
            ]

            sorted_teams = sorted(teams_with_data, key=lambda x: x[1])

            for rank, (team, points_allowed) in enumerate(sorted_teams, 1):
                if team not in rankings:
                    rankings[team] = {}
                rankings[team][f'def_{position}_rank'] = rank
                self.logger.debug(
                    f"{team} {position}: Rank {rank} ({points_allowed:.1f} points allowed)"
                )

        for team in all_teams:
            if team not in rankings:
                rankings[team] = {}

            for position in ['vs_qb', 'vs_rb', 'vs_wr', 'vs_te', 'vs_k']:
                rank_key = f'def_{position}_rank'
                if rank_key not in rankings[team]:
                    rankings[team][rank_key] = 16

        self.logger.info(f"Calculated position-specific rankings for {len(rankings)} teams across 5 positions")

        return rankings

    def _collect_team_weekly_data(
        self,
        players: List[ESPNPlayerData],
        schedule: Dict[int, Dict[str, str]],
        current_week: int
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Collect per-team, per-week data for the new team_data format.

        For each team and each completed week, collects:
        - Fantasy points allowed by position (QB, RB, WR, TE, K)
        - Total points scored by team
        - Total points allowed by team

        Args:
            players: List of all players with weekly stats
            schedule: Dict mapping {week: {team: opponent}}
            current_week: Current NFL week (1-17)

        Returns:
            Dict[team, List[{week, QB, RB, WR, TE, K, points_scored, points_allowed}]]
        """
        from collections import defaultdict

        self.logger.info(f"Collecting team weekly data through week {current_week - 1}")

        all_teams = [
            'ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE',
            'DAL', 'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAX', 'KC',
            'LAC', 'LAR', 'LV', 'MIA', 'MIN', 'NE', 'NO', 'NYG',
            'NYJ', 'PHI', 'PIT', 'SEA', 'SF', 'TB', 'TEN', 'WSH'
        ]

        team_week_data = {team: {} for team in all_teams}
        for team in all_teams:
            for week in range(1, current_week):
                team_week_data[team][week] = {
                    'QB': 0.0, 'RB': 0.0, 'WR': 0.0, 'TE': 0.0, 'K': 0.0,
                    'points_scored': 0.0, 'points_allowed': 0.0
                }

        for player in players:
            if player.position not in ['QB', 'RB', 'WR', 'TE', 'K']:
                continue

            player_team = player.team
            if not player_team or player_team not in all_teams:
                continue

            for week in range(1, current_week):
                week_points = player.get_week_points(week)
                if week_points is None or week_points <= 0:
                    continue

                if player_team in team_week_data and week in team_week_data[player_team]:
                    team_week_data[player_team][week]['points_scored'] += week_points

                week_schedule = schedule.get(week, {})
                opponent = week_schedule.get(player_team)
                if opponent and opponent in team_week_data:
                    team_week_data[opponent][week][player.position] += week_points
                    team_week_data[opponent][week]['points_allowed'] += week_points

        result = {}
        for team in all_teams:
            result[team] = []
            for week in range(1, current_week):
                week_data = team_week_data[team].get(week, {})
                result[team].append({
                    'week': week,
                    'pts_allowed_to_QB': round(week_data.get('QB', 0.0), 1),
                    'pts_allowed_to_RB': round(week_data.get('RB', 0.0), 1),
                    'pts_allowed_to_WR': round(week_data.get('WR', 0.0), 1),
                    'pts_allowed_to_TE': round(week_data.get('TE', 0.0), 1),
                    'pts_allowed_to_K': round(week_data.get('K', 0.0), 1),
                    'points_scored': round(week_data.get('points_scored', 0.0), 1),
                    'points_allowed': round(week_data.get('points_allowed', 0.0), 1)
                })

        self.logger.info(f"Collected weekly data for {len(result)} teams through week {current_week - 1}")
        return result


    def _has_consensus_ranking(self, rankings_list: List[Dict], position: str) -> bool:
        """
        Check if a rankings list has a valid consensus ranking entry.

        Consensus rankings have:
        - rankSourceId == 0 (ESPN's aggregated consensus)
        - rankType == 'PPR'
        - slotId matching the player's position
        - averageRank field present

        Args:
            rankings_list: List of ranking entries from ESPN API
            position: Player position (QB, RB, WR, TE, K, DST)

        Returns:
            True if valid consensus ranking exists, False otherwise
        """
        if not rankings_list:
            return False

        expected_slot_id = self._position_to_slot_id(position)
        if expected_slot_id == -1:
            return False

        for ranking in rankings_list:
            if (ranking.get('rankSourceId') == 0 and
                ranking.get('rankType') == 'PPR' and
                ranking.get('slotId') == expected_slot_id and
                'averageRank' in ranking):
                return True

        return False

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
        if position == 'D/ST':
            position = 'DST'

        position_id = self._position_to_position_id(position)
        if position_id == -1:
            return None

        same_position_players = [
            p for p in all_players_data
            if p.get('position_id') == position_id and p.get('draft_rank') is not None
        ]

        if not same_position_players:
            return None

        same_position_players.sort(key=lambda p: p['draft_rank'])

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
        from player_data_fetcher.player_data_constants import ESPN_POSITION_MAPPINGS

        if position == 'D/ST':
            position = 'DST'

        reverse_mapping = {v: k for k, v in ESPN_POSITION_MAPPINGS.items()}
        return reverse_mapping.get(position, -1)

    async def _parse_espn_data(self, data: Dict[str, Any]) -> List[ESPNPlayerData]:
        """Parse ESPN API response into ESPNPlayerData objects"""
        from player_data_fetcher.config import PROGRESS_ETA_WINDOW_SIZE

        projections = []
        unknown_position_count = 0

        team_rankings = await self._fetch_team_rankings()
        current_week_schedule = await self._fetch_current_week_schedule()

        full_season_schedule = self._load_season_schedule_from_csv()

        self.current_week_schedule = current_week_schedule
        self.full_season_schedule = full_season_schedule

        players = data.get('players', [])
        self.logger.info(f"Processing {len(players)} players from ESPN API")

        from player_data_fetcher.progress_tracker import ProgressTracker
        progress_tracker = ProgressTracker(
            total_players=len(players),
            logger=self.logger,
            update_frequency=self.settings.progress_frequency,
            eta_window_size=PROGRESS_ETA_WINDOW_SIZE
        )

        all_players_with_ranks = []
        if self.settings.current_nfl_week <= 1:
            self.logger.info(f"Calculating position-specific ranks for Week {self.settings.current_nfl_week} (processing {len(players)} players)")
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

        self.logger.info(f"Collecting positional rank ranges for normalization (processing {len(players)} players)")
        position_rank_ranges = {}
        player_positional_ranks = {}

        for player in players:
            try:
                player_info = player.get('player', {})
                player_id = str(player_info.get('id', ''))

                if not player_id:
                    continue

                position_id = player_info.get('defaultPositionId')
                position = ESPN_POSITION_MAPPINGS.get(position_id, 'UNKNOWN')

                if position == 'UNKNOWN':
                    continue

                positional_rank = None

                if self.settings.current_nfl_week <= 1:
                    draft_ranks = player_info.get('draftRanksByRankType', {})
                    ppr_rank_data = draft_ranks.get('PPR', {})

                    if ppr_rank_data and 'rank' in ppr_rank_data:
                        draft_rank = ppr_rank_data['rank']
                        positional_rank = self._get_positional_rank_from_overall(
                            draft_rank, position, all_players_with_ranks
                        )
                else:
                    ranking_key = '0' if self.settings.current_nfl_week == 1 else str(self.settings.current_nfl_week)
                    rankings_ros = player_info.get('rankings', {}).get(ranking_key, [])
                    all_rankings = player_info.get('rankings', {})

                    has_consensus = self._has_consensus_ranking(rankings_ros, position)

                    if not rankings_ros or not has_consensus:
                        for fallback_week in range(self.settings.current_nfl_week - 1, 0, -1):
                            fallback_key = str(fallback_week)
                            if fallback_key in all_rankings and all_rankings[fallback_key]:
                                fallback_rankings = all_rankings[fallback_key]
                                if self._has_consensus_ranking(fallback_rankings, position):
                                    rankings_ros = fallback_rankings
                                    break

                        if (not rankings_ros or not self._has_consensus_ranking(rankings_ros, position)) and '0' in all_rankings:
                            rankings_ros = all_rankings['0']

                    if rankings_ros:
                        expected_slot_id = self._position_to_slot_id(position)

                        for ranking_entry in rankings_ros:
                            if (ranking_entry.get('rankType') == 'PPR' and
                                ranking_entry.get('rankSourceId') == 0):
                                actual_slot_id = ranking_entry.get('slotId')
                                if actual_slot_id == expected_slot_id:
                                    if 'averageRank' in ranking_entry:
                                        positional_rank = ranking_entry['averageRank']
                                        break

                        if positional_rank is None:
                            for ranking_entry in rankings_ros:
                                if ranking_entry.get('rankType') == 'PPR':
                                    actual_slot_id = ranking_entry.get('slotId')
                                    if actual_slot_id == expected_slot_id:
                                        if 'averageRank' in ranking_entry:
                                            positional_rank = ranking_entry['averageRank']
                                            break

                if positional_rank is not None:
                    player_positional_ranks[player_id] = positional_rank

                    if position not in position_rank_ranges:
                        position_rank_ranges[position] = {
                            'min': positional_rank,
                            'max': positional_rank,
                            'count': 1
                        }
                    else:
                        position_rank_ranges[position]['min'] = min(
                            position_rank_ranges[position]['min'], positional_rank
                        )
                        position_rank_ranges[position]['max'] = max(
                            position_rank_ranges[position]['max'], positional_rank
                        )
                        position_rank_ranges[position]['count'] += 1

            except Exception as e:
                self.logger.debug(f"Error collecting rank for player {player_id}: {e}")
                continue

        self.logger.info(f"Position rank ranges collected for {len(position_rank_ranges)} positions:")
        for position, ranges in sorted(position_rank_ranges.items()):
            self.logger.info(
                f"  {position}: {ranges['min']:.1f}-{ranges['max']:.1f} "
                f"({ranges['count']} players with ranks)"
            )

        parsed_count = 0
        for player in players:
            try:
                player_info = player.get('player', {})
                id = str(player_info.get('id', ''))
                
                if not id:
                    if progress_tracker:
                        progress_tracker.update()
                    continue
                
                name_parts = []
                if player_info.get('firstName'):
                    name_parts.append(player_info['firstName'])
                if player_info.get('lastName'):  
                    name_parts.append(player_info['lastName'])
                name = ' '.join(name_parts) if name_parts else 'Unknown Player'
                
                pro_team_id = player_info.get('proTeamId')
                team = ESPN_TEAM_MAPPINGS.get(pro_team_id, 'UNK')

                if team == 'UNK':
                    if progress_tracker:
                        progress_tracker.update()
                    continue
                
                position_id = player_info.get('defaultPositionId')
                position = ESPN_POSITION_MAPPINGS.get(position_id, 'UNKNOWN')

                if position == 'UNKNOWN':
                    self.logger.debug(f"Skipping player {name} (ID: {id}) with unknown position ID: {position_id}")
                    unknown_position_count += 1
                    if progress_tracker:
                        progress_tracker.update()
                    continue

                bye_week = self.bye_weeks.get(team)
                
                fantasy_points = self._calculate_week_by_week_projection(player_info, name, position)
                
                
                injury_status = "ACTIVE"
                injury_info = player_info.get('injuryStatus')
                if injury_info:
                    injury_status = injury_info.upper()
                
                average_draft_position = None
                ownership_data = player_info.get('ownership', {})
                if ownership_data and 'averageDraftPosition' in ownership_data:
                    average_draft_position = float(ownership_data['averageDraftPosition'])

                player_rating = None
                positional_rank = None

                if self.settings.current_nfl_week <= 1:
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

                    ranking_key = '0' if self.settings.current_nfl_week == 1 else str(self.settings.current_nfl_week)
                    rankings_ros = player_info.get('rankings', {}).get(ranking_key, [])
                    all_rankings = player_info.get('rankings', {})

                    has_consensus = self._has_consensus_ranking(rankings_ros, position)

                    if not rankings_ros or not has_consensus:

                        for fallback_week in range(self.settings.current_nfl_week - 1, 0, -1):
                            fallback_key = str(fallback_week)
                            if fallback_key in all_rankings and all_rankings[fallback_key]:
                                fallback_rankings = all_rankings[fallback_key]
                                if self._has_consensus_ranking(fallback_rankings, position):
                                    rankings_ros = fallback_rankings
                                    self.logger.debug(
                                        f"No valid consensus rankings['{ranking_key}'] for {name}, using rankings['{fallback_key}'] (most recent with consensus)"
                                    )
                                    break

                        if (not rankings_ros or not self._has_consensus_ranking(rankings_ros, position)) and '0' in all_rankings:
                            rankings_ros = all_rankings['0']
                            self.logger.debug(
                                f"No weekly consensus rankings for {name}, using rankings['0'] (pre-season)"
                            )

                    if rankings_ros:
                        expected_slot_id = self._position_to_slot_id(position)

                        for ranking_entry in rankings_ros:
                            if (ranking_entry.get('rankType') == 'PPR' and
                                ranking_entry.get('rankSourceId') == 0):
                                actual_slot_id = ranking_entry.get('slotId')

                                if actual_slot_id == expected_slot_id:
                                    if 'averageRank' in ranking_entry:
                                        positional_rank = ranking_entry['averageRank']
                                        self.logger.debug(
                                            f"Found consensus ranking for {name}: {positional_rank}"
                                        )
                                        break

                        if positional_rank is None:
                            for ranking_entry in rankings_ros:
                                if ranking_entry.get('rankType') == 'PPR':
                                    actual_slot_id = ranking_entry.get('slotId')

                                    if actual_slot_id == expected_slot_id:
                                        if 'averageRank' in ranking_entry:
                                            positional_rank = ranking_entry['averageRank']
                                            self.logger.debug(
                                                f"Found non-consensus ranking for {name}: {positional_rank}"
                                            )
                                            break
                                    elif actual_slot_id is not None and expected_slot_id != -1:
                                        self.logger.debug(
                                            f"slotId mismatch for {name}: expected {expected_slot_id}, got {actual_slot_id}, skipping"
                                        )

                if positional_rank is not None:
                    player_positional_ranks[id] = positional_rank
                    player_rating = None
                else:
                    player_rating = None
                    draft_ranks = player_info.get('draftRanksByRankType', {})
                    ppr_rank_data = draft_ranks.get('PPR', {})

                    if ppr_rank_data and 'rank' in ppr_rank_data:
                        draft_rank = ppr_rank_data['rank']
                        if draft_rank <= 50:
                            player_rating = 100.0 - (draft_rank - 1) * 0.4
                        elif draft_rank <= 150:
                            player_rating = 80.0 - (draft_rank - 50) * 0.25
                        elif draft_rank <= 300:
                            player_rating = 55.0 - (draft_rank - 150) * 0.2
                        else:
                            player_rating = max(15.0, 25.0 - (draft_rank - 300) * 0.01)

                        self.logger.warning(
                            f"Rankings object missing for {name} (ID: {id}), using draft rank fallback"
                        )


                projection = ESPNPlayerData(
                    id=id,
                    name=name,
                    team=team,
                    position=position,
                    bye_week=bye_week,
                    drafted_by="",
                    fantasy_points=fantasy_points,
                    average_draft_position=average_draft_position,
                    player_rating=player_rating,
                    injury_status=injury_status,
                    api_source="ESPN",
                    raw_stats=player_info.get('stats', [])
                )

                self._populate_weekly_projections(projection, player_info, name, position)
                
                projections.append(projection)
                parsed_count += 1

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
        
        self.logger.info(f"Successfully parsed {parsed_count} players with projections")

        if progress_tracker:
            progress_tracker.complete()

        if unknown_position_count > 0:
            self.logger.info(f"Filtered out {unknown_position_count} players with unknown positions")

        position_defense_rankings = self._calculate_position_defense_rankings(
            projections,
            full_season_schedule,
            self.settings.current_nfl_week
        )

        self.position_defense_rankings = position_defense_rankings

        self.logger.info(f"Normalizing player ratings for {len(player_positional_ranks)} players with positional ranks")

        normalized_count = 0
        fallback_count = 0

        for projection in projections:
            if projection.id in player_positional_ranks:
                positional_rank = player_positional_ranks[projection.id]
                position = projection.position

                if position in position_rank_ranges:
                    min_rank = position_rank_ranges[position]['min']
                    max_rank = position_rank_ranges[position]['max']

                    if min_rank == max_rank:
                        projection.player_rating = 50.0
                        self.logger.debug(
                            f"Single rank for position {position} (rank={min_rank}), "
                            f"using neutral rating 50.0 for {projection.name}"
                        )
                    else:
                        normalized = 1 + ((positional_rank - max_rank) / (min_rank - max_rank)) * 99
                        projection.player_rating = normalized

                        if not (1.0 <= normalized <= 100.0):
                            self.logger.warning(
                                f"Normalized rating out of range for {projection.name}: {normalized:.2f} "
                                f"(rank={positional_rank}, min={min_rank}, max={max_rank})"
                            )

                        if normalized >= 99.5 or normalized <= 1.5:
                            self.logger.debug(
                                f"Extreme rating for {projection.name} ({position}): {normalized:.1f} "
                                f"(rank={positional_rank:.1f})"
                            )

                    normalized_count += 1

                    if normalized_count % 100 == 0:
                        self.logger.debug(f"Normalized {normalized_count} player ratings...")

                else:
                    self.logger.warning(
                        f"Position {position} not in rank ranges for {projection.name}, "
                        f"player_rating will remain None"
                    )
                    fallback_count += 1
            elif projection.player_rating is None:
                fallback_count += 1

        self.logger.info(
            f"Player rating normalization complete: {normalized_count} normalized, "
            f"{fallback_count} using fallback or None"
        )

        total_players = len(projections)
        if total_players > 0:
            fallback_percentage = (fallback_count / total_players) * 100
            if fallback_percentage > 10:
                self.logger.warning(
                    f"High fallback usage: {fallback_percentage:.1f}% of players "
                    f"({fallback_count}/{total_players}) using fallback or have no rating"
                )

        return projections


