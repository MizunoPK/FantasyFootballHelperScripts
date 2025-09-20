#!/usr/bin/env python3
"""
ESPN Fantasy API Client

This module handles all ESPN API interactions for fantasy football data collection.
Separated from the main script for better organization and maintainability.

Author: Generated for NFL Fantasy Data Collection
Last Updated: September 2025
"""

import asyncio
import csv
import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
import math

import httpx
from tenacity import retry, stop_after_attempt, wait_random_exponential

from player_data_models import ESPNPlayerData, ScoringFormat
# Import shared fantasy points calculator
import sys
from pathlib import Path
# Add shared_files to path using robust path resolution
shared_files_path = Path(__file__).parent.parent / "shared_files"
sys.path.insert(0, str(shared_files_path))
from fantasy_points_calculator import FantasyPointsExtractor, FantasyPointsConfig
from player_data_constants import (
    ESPN_TEAM_MAPPINGS, ESPN_POSITION_MAPPINGS, ESPN_USER_AGENT, ESPN_PLAYER_LIMIT,
    MIN_PLAYERS_FOR_EMPIRICAL_MAPPING, MIN_PLAYERS_PER_POSITION_MAPPING,
    POSITION_FALLBACK_CONFIG, DEFAULT_FALLBACK_CONFIG, MIN_ADP_RANGE_THRESHOLD,
    MIN_FANTASY_POINTS_BOUND_FACTOR, MAX_FANTASY_POINTS_BOUND_FACTOR,
    UNCERTAINTY_ADJUSTMENT_FACTOR, PositionDataDict, PositionMappingDict,
    CURRENT_NFL_WEEK, USE_WEEK_BY_WEEK_PROJECTIONS, USE_REMAINING_SEASON_PROJECTIONS,
    INCLUDE_PLAYOFF_WEEKS, RECENT_WEEKS_FOR_AVERAGE, SKIP_DRAFTED_PLAYER_UPDATES,
    USE_SCORE_THRESHOLD, PLAYER_SCORE_THRESHOLD, PLAYERS_CSV
)


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
    """Base API client with common functionality"""
    
    def __init__(self, settings):
        self.settings = settings
        self.logger = logging.getLogger(__name__)
        self._client = None
        self._session_lock = asyncio.Lock()
    
    @asynccontextmanager
    async def session(self):
        """Async context manager for HTTP client session with race condition protection"""
        async with self._session_lock:
            if self._client is None:
                timeout = httpx.Timeout(self.settings.request_timeout)
                self._client = httpx.AsyncClient(timeout=timeout)
                self.logger.debug("Created new HTTP client session")

        try:
            yield self._client
        finally:
            # Note: We don't close the client here to allow reuse
            # The client will be closed when the class instance is destroyed
            pass

    async def close(self):
        """Close the HTTP client session"""
        async with self._session_lock:
            if self._client:
                await self._client.aclose()
                self._client = None
                self.logger.debug("Closed HTTP client session")
    
    @retry(stop=stop_after_attempt(3), wait=wait_random_exponential(multiplier=1, max=10))
    async def _make_request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request with retry logic"""
        self.logger.info(f"Making request to: {url}")
        
        # Add rate limiting delay
        await asyncio.sleep(self.settings.rate_limit_delay)
        
        try:
            response = await self._client.request(method, url, **kwargs)
            
            # Handle specific HTTP errors
            if response.status_code == 429:
                raise ESPNRateLimitError(f"Rate limit exceeded: {response.status_code}")
            elif response.status_code >= 500:
                raise ESPNServerError(f"ESPN server error: {response.status_code}")
            elif response.status_code >= 400:
                raise ESPNAPIError(f"ESPN API error: {response.status_code}")
                
            response.raise_for_status()
            self.logger.info("Request successful")
            return response.json()
            
        except httpx.RequestError as e:
            self.logger.error(f"Request failed: {e}")
            raise ESPNAPIError(f"Network error: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            raise


class ESPNClient(BaseAPIClient):
    """ESPN Fantasy API client for player projections"""
    
    def __init__(self, settings):
        super().__init__(settings)
        self.bye_weeks: Dict[str, int] = {}
        self.drafted_player_ids: Set[str] = set()
        self.low_score_player_data: Dict[str, Dict] = {}

        # Initialize shared fantasy points extractor
        fp_config = FantasyPointsConfig(
            prefer_actual_over_projected=True,
            include_negative_dst_points=True,
            use_historical_fallback=True,
            use_adp_estimation=True
        )
        self.fantasy_points_extractor = FantasyPointsExtractor(fp_config, settings.season)

        # Load optimization data (drafted player IDs and low-score player data)
        if SKIP_DRAFTED_PLAYER_UPDATES or USE_SCORE_THRESHOLD:
            self._load_optimization_data()
    
    def _get_ppr_id(self) -> int:
        """Get ESPN scoring format ID"""
        scoring_map = {
            ScoringFormat.STANDARD: 1,
            ScoringFormat.PPR: 3,
            ScoringFormat.HALF_PPR: 2
        }
        return scoring_map.get(self.settings.scoring_format, 3)

    def _load_optimization_data(self):
        """Load player data for optimization (drafted players to skip and low-score players to preserve)"""
        try:
            players_file_path = Path(__file__).parent / PLAYERS_CSV

            with open(players_file_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    player_id = row.get('id')
                    if not player_id:
                        continue

                    drafted_value = int(row.get('drafted', 0))
                    fantasy_points = float(row.get('fantasy_points', 0.0))

                    # Track drafted=1 players to skip API calls (if optimization enabled)
                    if SKIP_DRAFTED_PLAYER_UPDATES and drafted_value == 1:
                        self.drafted_player_ids.add(player_id)

                    # Track low-score players to preserve data (if threshold optimization enabled)
                    if USE_SCORE_THRESHOLD:
                        # Always update players on our roster (drafted=2) regardless of score
                        if drafted_value == 2:
                            pass  # Don't add to low_score_player_data, always update
                        # Preserve data for players below threshold
                        elif fantasy_points < PLAYER_SCORE_THRESHOLD:
                            self.low_score_player_data[player_id] = dict(row)

            optimization_messages = []
            if SKIP_DRAFTED_PLAYER_UPDATES:
                optimization_messages.append(f"{len(self.drafted_player_ids)} drafted player IDs to skip")
            if USE_SCORE_THRESHOLD:
                optimization_messages.append(f"{len(self.low_score_player_data)} low-score players to preserve (threshold: {PLAYER_SCORE_THRESHOLD})")

            if optimization_messages:
                self.logger.info(f"Loaded optimization data: {', '.join(optimization_messages)}")

        except FileNotFoundError:
            self.logger.warning(f"Players file not found at {players_file_path}. No optimizations will be applied.")
        except Exception as e:
            self.logger.error(f"Error loading optimization data: {e}. No optimizations will be applied.")

    def _calculate_remaining_season_projection(self, stats: List[Dict], position: str) -> float:
        """Calculate remaining season projection based on recent performance"""
        if not USE_REMAINING_SEASON_PROJECTIONS:
            return 0.0

        # Get recent weeks data for current season
        recent_weeks = []
        current_week = CURRENT_NFL_WEEK
        start_week = max(1, current_week - RECENT_WEEKS_FOR_AVERAGE)

        for stat_entry in stats:
            if (stat_entry.get('seasonId') == self.settings.season and
                stat_entry.get('scoringPeriodId', 0) >= start_week and
                stat_entry.get('scoringPeriodId', 0) < current_week):

                week_points = 0.0
                if 'appliedTotal' in stat_entry:
                    week_points = float(stat_entry['appliedTotal'])
                elif 'projectedTotal' in stat_entry:
                    week_points = float(stat_entry['projectedTotal'])

                # Include valid scores (positive for most positions, any for DST)
                if week_points != 0 and (position == 'DST' or week_points > 0):
                    recent_weeks.append(week_points)

        if len(recent_weeks) == 0:
            return 0.0

        # Calculate average of recent weeks
        recent_average = sum(recent_weeks) / len(recent_weeks)

        # Calculate remaining games in season (fantasy regular season is 17 weeks)
        remaining_weeks = max(0, 17 - current_week)

        # Project remaining season total
        remaining_projection = recent_average * remaining_weeks

        self.logger.debug(f"Remaining season calc: {len(recent_weeks)} recent weeks, "
                         f"avg={recent_average:.1f}, remaining={remaining_weeks} weeks, "
                         f"projection={remaining_projection:.1f}")

        return remaining_projection

    async def _calculate_week_by_week_projection(self, player_id: str, name: str, position: str) -> float:
        """Calculate season projection by summing week-by-week data (actual + projected)"""
        if not USE_WEEK_BY_WEEK_PROJECTIONS:
            return 0.0

        try:
            # Get all weekly data for this player in a single optimized call
            all_weeks_data = await self._get_all_weeks_data(player_id, position)
            if not all_weeks_data:
                return 0.0

            # Determine week range (limit to 17 for fantasy regular season)
            end_week = 17
            start_week = CURRENT_NFL_WEEK + 1 if USE_REMAINING_SEASON_PROJECTIONS else 1

            total_projection = 0.0
            weeks_processed = 0

            for week in range(start_week, end_week + 1):
                week_points = None

                # Extract week points using standardized logic (always prefers actual over projected)
                week_points = self._extract_week_points(all_weeks_data, week, position=position, player_name=name)

                # Determine data type for logging
                if not USE_REMAINING_SEASON_PROJECTIONS and week <= CURRENT_NFL_WEEK:
                    data_type = 'actual'
                else:
                    data_type = 'projected'

                if week_points > 0:
                    total_projection += week_points
                    weeks_processed += 1
                    self.logger.debug(f"{name} Week {week}: {week_points:.1f} points ({data_type})")

            if weeks_processed > 0:
                self.logger.info(f"Week-by-week total for {name}: {total_projection:.1f} points ({weeks_processed} weeks)")
                return total_projection

        except Exception as e:
            self.logger.warning(f"Week-by-week calculation failed for {name}: {e}")

        return 0.0

    async def _get_all_weeks_data(self, player_id: str, position: str) -> Optional[dict]:
        """Get all weekly data for a player in a single optimized API call"""
        try:
            url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{self.settings.season}/segments/0/leaguedefaults/3"

            # Get all available data for the player (not filtered by week)
            params = {
                'view': 'kona_player_info',
                'scoringPeriodId': 0  # 0 gets all available data
            }

            headers = {
                'User-Agent': ESPN_USER_AGENT,
                'X-Fantasy-Filter': f'{{"players":{{"filterIds":{{"value":[{player_id}]}}}}}}'
            }

            data = await self._make_request('GET', url, params=params, headers=headers)
            players = data.get('players', [])

            if not players:
                return None

            # Return the first player's data which contains all available stats
            return players[0].get('player', {})

        except Exception as e:
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
                fallback_data=None,  # Will add ADP fallback in future if needed
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
        if not USE_WEEK_BY_WEEK_PROJECTIONS:
            return

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

                if espn_points is not None and espn_points > 0:
                    player_data.set_week_points(week, espn_points)
                    self.logger.debug(f"{name} Week {week}: {espn_points:.1f} points (ESPN data)")
                else:
                    # Check if seasonal fallback should be distributed
                    if player_data.data_method == "seasonal":
                        # Distribute seasonal projection evenly across weeks 1-17
                        weekly_points = player_data.fantasy_points / 17
                        player_data.set_week_points(week, weekly_points)
                        self.logger.debug(f"{name} Week {week}: {weekly_points:.1f} points (seasonal distribution)")
                    else:
                        # Set to 0.0 when no ESPN data available and no seasonal fallback
                        player_data.set_week_points(week, 0.0)
                        self.logger.debug(f"{name} Week {week}: 0.0 points (no data)")

        except Exception as e:
            self.logger.warning(f"Failed to populate weekly projections for {name}: {str(e)}")

    def _extract_raw_espn_week_points(self, player_data: dict, week: int, position: str) -> Optional[float]:
        """
        Extract points for a specific week from ESPN data only (no fallbacks)

        Returns None if no ESPN data is available for this week, rather than falling back to position defaults.
        This ensures we only populate weekly columns with actual ESPN projection data.
        """
        try:
            stats = player_data.get('stats', [])
            if not stats:
                return None

            # Look for exact week match in current season
            for stat in stats:
                if not isinstance(stat, dict):
                    continue

                season_id = stat.get('seasonId')
                scoring_period = stat.get('scoringPeriodId')

                if season_id == self.settings.season and scoring_period == week:
                    # Check for actual ESPN data (prefer appliedTotal over projectedTotal)
                    if 'appliedTotal' in stat and stat['appliedTotal'] is not None:
                        try:
                            points = float(stat['appliedTotal'])
                            # Check for NaN values and treat them as None
                            if math.isnan(points):
                                continue
                            if position == 'DST' or points >= 0:  # Allow negative DST, filter negative others
                                return points
                        except (ValueError, TypeError):
                            continue
                    elif 'projectedTotal' in stat and stat['projectedTotal'] is not None:
                        try:
                            points = float(stat['projectedTotal'])
                            # Check for NaN values and treat them as None
                            if math.isnan(points):
                                continue
                            if position == 'DST' or points >= 0:  # Allow negative DST, filter negative others
                                return points
                        except (ValueError, TypeError):
                            continue

            # No ESPN data found for this week
            return None

        except Exception as e:
            self.logger.debug(f"Error extracting raw ESPN week points: {str(e)}")
            return None

    async def _get_week_actual_performance(self, player_id: str, week: int, position: str) -> Optional[float]:
        """Get actual performance data for a specific past week"""
        try:
            url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{self.settings.season}/segments/0/leaguedefaults/3"

            params = {
                'view': 'kona_player_info',
                'scoringPeriodId': week
            }

            headers = {
                'User-Agent': ESPN_USER_AGENT,
                'X-Fantasy-Filter': f'{{"players":{{"filterIds":{{"value":[{player_id}]}}}}}}'
            }

            data = await self._make_request('GET', url, params=params, headers=headers)
            players = data.get('players', [])

            if not players:
                return None

            # Find matching week entries in player stats
            player_info = players[0].get('player', {})
            stats = player_info.get('stats', [])

            # Collect all viable entries for this week
            week_entries = []
            for stat_entry in stats:
                if (stat_entry.get('seasonId') == self.settings.season and
                    stat_entry.get('scoringPeriodId') == week):

                    # Priority: appliedTotal > projectedTotal > 0
                    points = None
                    if 'appliedTotal' in stat_entry and stat_entry['appliedTotal'] is not None:
                        points = float(stat_entry['appliedTotal'])
                    elif 'projectedTotal' in stat_entry and stat_entry['projectedTotal'] is not None:
                        points = float(stat_entry['projectedTotal'])

                    if points is not None and (position == 'DST' or points >= 0):
                        week_entries.append(points)

            # Average multiple sources if available
            if week_entries:
                return sum(week_entries) / len(week_entries)

            return None

        except Exception as e:
            self.logger.warning(f"Failed to get week {week} actual for player {player_id}: {e}")
            return None

    async def _get_week_projection(self, player_id: str, week: int, position: str) -> Optional[float]:
        """Get projection data for a specific future week"""
        try:
            url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{self.settings.season}/segments/0/leaguedefaults/3"

            params = {
                'view': 'kona_player_info',
                'scoringPeriodId': week
            }

            headers = {
                'User-Agent': ESPN_USER_AGENT,
                'X-Fantasy-Filter': f'{{"players":{{"filterIds":{{"value":[{player_id}]}}}}}}'
            }

            data = await self._make_request('GET', url, params=params, headers=headers)
            players = data.get('players', [])

            if not players:
                return None

            # Find matching week entries in player stats
            player_info = players[0].get('player', {})
            stats = player_info.get('stats', [])

            # First try 2025 projections
            current_season_entries = []
            for stat_entry in stats:
                if (stat_entry.get('seasonId') == self.settings.season and
                    stat_entry.get('scoringPeriodId') == week):

                    points = None
                    if 'appliedTotal' in stat_entry and stat_entry['appliedTotal'] is not None:
                        points = float(stat_entry['appliedTotal'])
                    elif 'projectedTotal' in stat_entry and stat_entry['projectedTotal'] is not None:
                        points = float(stat_entry['projectedTotal'])

                    if points is not None and points > 0:
                        current_season_entries.append(points)

            if current_season_entries:
                return sum(current_season_entries) / len(current_season_entries)

            # No historical fallback - return None if no current season data available
            return None

        except Exception as e:
            self.logger.warning(f"Failed to get week {week} projection for player {player_id}: {e}")
            return None

    async def get_season_projections(self) -> List[ESPNPlayerData]:
        """Get season projections from ESPN"""
        ppr_id = self._get_ppr_id()
        
        # ESPN's main fantasy API endpoint for player projections
        url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{self.settings.season}/segments/0/leaguedefaults/{ppr_id}"
        
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
    
    async def _parse_espn_data(self, data: Dict[str, Any]) -> List[ESPNPlayerData]:
        """Parse ESPN API response into ESPNPlayerData objects"""
        projections = []
        
        players = data.get('players', [])
        self.logger.info(f"Processing {len(players)} players from ESPN API")
        
        parsed_count = 0
        skipped_drafted_count = 0
        skipped_low_score_count = 0
        for player in players:
            try:
                # Extract basic info
                player_info = player.get('player', {})
                id = str(player_info.get('id', ''))
                
                if not id:
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
                        average_draft_position=float(preserved_data.get('average_draft_position', 0.0)) if preserved_data.get('average_draft_position') else None,
                        data_method=preserved_data.get('data_method', 'weekly')  # Preserve existing data method
                    )
                    projections.append(preserved_projection)
                    skipped_low_score_count += 1
                    continue

                # Skip players not on active NFL rosters (free agents, practice squad, etc.)
                if team == 'UNK':
                    continue
                
                # Extract position
                position_id = player_info.get('defaultPositionId')
                position = ESPN_POSITION_MAPPINGS.get(position_id, 'UNKNOWN')
                
                # Get bye week
                bye_week = self.bye_weeks.get(team)
                
                # Extract fantasy points using week-by-week calculation (primary) with fallbacks
                fantasy_points = 0.0
                stats = player.get('player', {}).get('stats', [])
                fallback_used = False
                fallback_type = ""

                # PRIMARY: Week-by-week calculation (actual + projected)
                if USE_WEEK_BY_WEEK_PROJECTIONS:
                    week_by_week_points = await self._calculate_week_by_week_projection(id, name, position)
                    if week_by_week_points > 0:
                        fantasy_points = week_by_week_points
                        self.logger.debug(f"Using week-by-week projection for {name}: {fantasy_points:.1f}")

                # FALLBACK 1: Remaining season projection
                if fantasy_points == 0.0 and USE_REMAINING_SEASON_PROJECTIONS:
                    remaining_projection = self._calculate_remaining_season_projection(stats, position)
                    if remaining_projection > 0:
                        fantasy_points = remaining_projection
                        fallback_used = True
                        fallback_type = "remaining_season"
                        self.logger.debug(f"Using remaining season projection for {name}: {fantasy_points:.1f}")

                # FALLBACK 2: Current season (2025) total projections
                if fantasy_points == 0.0:
                    # Debug DST data availability
                    if position == 'DST':
                        self.logger.info(f"DST DEBUG: {name} has {len(stats)} stat entries")
                        season_entries = [stat for stat in stats if stat.get('scoringPeriodId') == 0]
                        self.logger.info(f"  Season projection entries (scoringPeriodId=0): {len(season_entries)}")
                        for i, stat in enumerate(season_entries):
                            self.logger.info(f"    Season entry {i}: seasonId={stat.get('seasonId')}, appliedTotal={stat.get('appliedTotal')}, projectedTotal={stat.get('projectedTotal')}")

                    season_projections = []
                    for stat_entry in stats:
                        if stat_entry.get('scoringPeriodId') == 0 and stat_entry.get('seasonId') == self.settings.season:
                            points = 0.0
                            if 'appliedTotal' in stat_entry:
                                points = float(stat_entry['appliedTotal'])
                            elif 'projectedTotal' in stat_entry:
                                points = float(stat_entry['projectedTotal'])
                            if points > 0:  # Only consider positive projections
                                season_projections.append(points)

                    if season_projections:
                        fantasy_points = max(season_projections)  # Use the highest positive projection
                        fallback_used = True
                        fallback_type = "2025_season"

                # FALLBACK 3: ADP estimation (if enabled and will be applied later in empirical mapping)
                # Note: Individual ADP estimation is handled in _apply_empirical_adp_mapping

                # FALLBACK 4: Zero score (as specified in requirements)
                if fantasy_points == 0.0:
                    self.logger.warning(f"No usable data for {name} ({position}). Setting to 0.0 points.")
                    fallback_type = "zero"

                # Log when fallback is used for transparency
                if fallback_used:
                    self.logger.info(f"Using {fallback_type} fallback for {name} ({position}): {fantasy_points:.1f} points")
                
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
                
                # Create player projection
                # Map fallback types to standard data methods
                if fallback_used:
                    if fallback_type in ["remaining_season", "2025_season"]:
                        data_method = "seasonal"
                    elif fallback_type == "adp":
                        data_method = "adp"
                    elif fallback_type == "zero":
                        data_method = "zero"
                    else:
                        data_method = fallback_type
                else:
                    data_method = "weekly"

                projection = ESPNPlayerData(
                    id=id,
                    name=name,
                    team=team,
                    position=position,
                    bye_week=bye_week,
                    drafted=0,  # Initialize all players as not drafted
                    fantasy_points=fantasy_points,
                    average_draft_position=average_draft_position,
                    injury_status=injury_status,
                    api_source="ESPN",
                    data_method=data_method
                )

                # Collect weekly projections for this player
                await self._populate_weekly_projections(projection, id, name, position)
                
                projections.append(projection)
                parsed_count += 1
                
            except (KeyError, TypeError, ValueError) as e:
                player_id = player.get('player', {}).get('id', 'unknown')
                self.logger.warning(f"Failed to parse player {player_id}: {e}")
                continue
            except Exception as e:
                player_id = player.get('player', {}).get('id', 'unknown')
                self.logger.error(f"Unexpected error parsing player {player_id}: {e}")
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
        
        # Apply empirical ADP mapping for 0-point players
        projections = self._apply_empirical_adp_mapping(projections)
        
        return projections
    
    def _apply_empirical_adp_mapping(self, players: List[ESPNPlayerData]) -> List[ESPNPlayerData]:
        """Apply empirical ADP-to-fantasy-points mapping for players with 0 points"""
        
        # Step 1: Analyze existing players with both ADP and fantasy points
        players_with_both = []
        zero_point_players = []
        
        for player in players:
            if player.fantasy_points > 0 and player.average_draft_position:
                players_with_both.append(player)
            elif player.fantasy_points == 0 and player.average_draft_position:
                zero_point_players.append(player)
        
        self.logger.info(f"Found {len(players_with_both)} players with both fantasy points and ADP")
        self.logger.info(f"Found {len(zero_point_players)} zero-point players with ADP to update")
        
        if len(players_with_both) < MIN_PLAYERS_FOR_EMPIRICAL_MAPPING:
            self.logger.warning("Insufficient data for empirical ADP mapping - skipping")
            return players
        
        # Step 2: Build position-specific ADP->fantasy points mappings
        position_mappings = self._build_position_adp_mappings(players_with_both)
        
        # Step 3: Apply mappings to zero-point players
        updated_count = 0
        for player in zero_point_players:
            if player.position in position_mappings:
                estimated_points = self._estimate_fantasy_points_from_adp(
                    player.average_draft_position,
                    player.position,
                    position_mappings
                )
                player.fantasy_points = estimated_points
                player.data_method = "adp"  # Track that this player used ADP estimation

                # Distribute ADP estimation evenly across weeks 1-17
                weekly_points = estimated_points / 17
                for week in range(1, 18):
                    player.set_week_points(week, weekly_points)

                updated_count += 1
                self.logger.debug(f"Updated {player.name} ({player.position}) ADP {player.average_draft_position:.1f} -> {estimated_points:.1f} points (distributed across weeks 1-17)")
        
        self.logger.info(f"Updated fantasy points for {updated_count} players using empirical ADP mapping")
        return players
    
    def _build_position_adp_mappings(self, players_with_both: List[ESPNPlayerData]) -> Dict[str, PositionMappingDict]:
        """Build position-specific mappings from ADP to fantasy points using position-adjusted scaling"""
        # Group players by position
        position_data = self._group_players_by_position(players_with_both)
        
        # Create position-adjusted scaling models
        position_mappings = {}
        for position, data in position_data.items():
            if len(data['adp_values']) >= MIN_PLAYERS_PER_POSITION_MAPPING:
                mapping = self._create_position_mapping(position, data['adp_values'], data['fantasy_values'])
                if mapping:
                    position_mappings[position] = mapping
        
        return position_mappings
    
    def _group_players_by_position(self, players: List[ESPNPlayerData]) -> Dict[str, PositionDataDict]:
        """Group players by position for ADP analysis"""
        position_data = {}
        
        for player in players:
            position = player.position
            adp = player.average_draft_position
            fantasy_points = player.fantasy_points
            
            if position not in position_data:
                position_data[position] = {'adp_values': [], 'fantasy_values': []}
            
            position_data[position]['adp_values'].append(adp)
            position_data[position]['fantasy_values'].append(fantasy_points)
        
        return position_data
    
    def _create_position_mapping(self, position: str, adp_values: List[float], fantasy_values: List[float]) -> Optional[PositionMappingDict]:
        """Create position-specific ADP-to-fantasy-points mapping"""
        try:
            # Calculate position-specific ADP and fantasy point ranges
            min_adp = min(adp_values)
            max_adp = max(adp_values)
            min_points = min(fantasy_values)
            max_points = max(fantasy_values)
            
            # Avoid division by zero if all ADPs are the same
            if max_adp - min_adp < MIN_ADP_RANGE_THRESHOLD:
                self.logger.warning(f"Insufficient ADP range for {position}: {min_adp:.1f} to {max_adp:.1f}")
                return None
            
            # Calculate correlation to validate relationship strength
            correlation = self._calculate_correlation(adp_values, fantasy_values)
            if correlation is None:
                return None
            
            mapping = {
                'min_adp': min_adp,
                'max_adp': max_adp,
                'min_points': min_points,
                'max_points': max_points,
                'adp_range': max_adp - min_adp,
                'points_range': max_points - min_points,
                'sample_size': len(adp_values),
                'correlation': correlation
            }
            
            self.logger.debug(f"{position}: ADP {min_adp:.1f}-{max_adp:.1f}, "
                            f"Points {min_points:.1f}-{max_points:.1f}, "
                            f"correlation={correlation:.3f}, n={len(adp_values)}")
            
            return mapping
            
        except (ZeroDivisionError, ValueError) as e:
            self.logger.warning(f"Failed to create mapping for {position}: {e}")
            return None
    
    def _calculate_correlation(self, x_values: List[float], y_values: List[float]) -> Optional[float]:
        """Calculate Pearson correlation coefficient between two lists"""
        n = len(x_values)
        if n == 0:
            return None
            
        mean_x = sum(x_values) / n
        mean_y = sum(y_values) / n
        
        numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_values, y_values))
        denominator_x = sum((x - mean_x) ** 2 for x in x_values)
        denominator_y = sum((y - mean_y) ** 2 for y in y_values)
        
        if denominator_x == 0 or denominator_y == 0:
            return None
            
        correlation = numerator / (math.sqrt(denominator_x) * math.sqrt(denominator_y))
        return correlation
    
    def _estimate_fantasy_points_from_adp(self, adp: float, position: str, position_mappings: Dict[str, PositionMappingDict]) -> float:
        """Estimate fantasy points from ADP using position-adjusted scaling"""
        
        if position not in position_mappings:
            # Position-aware fallback based on configurable constants
            config = POSITION_FALLBACK_CONFIG.get(position, DEFAULT_FALLBACK_CONFIG)
            return max(1.0, config.base_points - (adp * config.multiplier))
        
        mapping = position_mappings[position]
        
        # Position-adjusted scaling: normalize ADP within position range, then scale to fantasy points
        normalized_adp = (adp - mapping['min_adp']) / mapping['adp_range']
        
        # Clamp normalized ADP to [0, 1] range to handle players outside observed range
        normalized_adp = max(0.0, min(1.0, normalized_adp))
        
        # Convert to fantasy points: lower ADP (normalized closer to 0) = higher fantasy points
        estimated_points = mapping['max_points'] - (normalized_adp * mapping['points_range'])
        
        # Apply reasonable bounds with some flexibility
        min_bound = max(1.0, mapping['min_points'] * MIN_FANTASY_POINTS_BOUND_FACTOR)
        max_bound = mapping['max_points'] * MAX_FANTASY_POINTS_BOUND_FACTOR
        
        estimated_points = max(min_bound, min(max_bound, estimated_points))
        
        # Add small random component based on correlation strength to account for uncertainty
        # Lower correlation = more uncertainty = more conservative estimate
        uncertainty_factor = 1.0 - abs(mapping.get('correlation', 0.0))
        adjustment = estimated_points * uncertainty_factor * UNCERTAINTY_ADJUSTMENT_FACTOR
        estimated_points = max(min_bound, estimated_points - adjustment)
        
        return float(estimated_points)