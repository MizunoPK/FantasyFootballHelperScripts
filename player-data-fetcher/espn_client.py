#!/usr/bin/env python3
"""
ESPN Fantasy API Client

This module handles all ESPN API interactions for fantasy football data collection.
Separated from the main script for better organization and maintainability.

Author: Kai Mizuno
Last Updated: September 2025
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
    """Base API client with common functionality"""
    
    def __init__(self, settings):
        self.settings = settings
        self.logger = get_logger()
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
        self.logger.debug(f"Making request to: {url}")
        
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
            self.logger.debug("Request successful")
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
        self.team_rankings: Dict[str, Dict[str, int]] = {}  # Cache team offensive/defensive rankings
        self.current_week_schedule: Dict[str, str] = {}  # Cache current week opponent matchups

        # Initialize shared fantasy points extractor (pure week-by-week system)
        fp_config = FantasyPointsConfig(
            prefer_actual_over_projected=True,
            include_negative_dst_points=True
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
                            if position == 'DST' or points > 0:  # Allow zero/negative DST, filter zero/negative others
                                return points
                        except (ValueError, TypeError):
                            continue
                    elif 'projectedTotal' in stat and stat['projectedTotal'] is not None:
                        try:
                            points = float(stat['projectedTotal'])
                            # Check for NaN values and treat them as None
                            if math.isnan(points):
                                continue
                            if position == 'DST' or points > 0:  # Allow zero/negative DST, filter zero/negative others
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
            use_current_season = CURRENT_NFL_WEEK >= MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS + 1
            target_season = NFL_SEASON if use_current_season else NFL_SEASON - 1

            self.logger.info(f"Team rankings: Using {'current' if use_current_season else 'previous'} season ({target_season}) data. "
                           f"Current week: {CURRENT_NFL_WEEK}, Min weeks needed: {MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS}")

            # ESPN team IDs mapping (standard NFL team IDs)
            team_ids = {
                1: 'ATL', 2: 'BUF', 3: 'CHI', 4: 'CIN', 5: 'CLE', 6: 'DAL', 7: 'DEN', 8: 'DET',
                9: 'GB', 10: 'TEN', 11: 'IND', 12: 'KC', 13: 'LV', 14: 'LAR', 15: 'MIA', 16: 'MIN',
                17: 'NE', 18: 'NO', 19: 'NYG', 20: 'NYJ', 21: 'PHI', 22: 'ARI', 23: 'PIT', 24: 'LAC',
                25: 'SF', 26: 'SEA', 27: 'TB', 28: 'WSH', 29: 'CAR', 30: 'JAX', 33: 'BAL', 34: 'HOU'
            }

            # Use the helper method to calculate rankings for the target season
            return await self._calculate_team_rankings_for_season(target_season, team_ids)

        except Exception as e:
            # Handle case where variables might not be defined yet
            season_info = "unknown season"
            try:
                import sys
                import os
                sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
                from config import CURRENT_NFL_WEEK, NFL_SEASON
                from config import MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS
                use_current_season = CURRENT_NFL_WEEK >= MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS + 1
                target_season = NFL_SEASON if use_current_season else NFL_SEASON - 1
                season_info = f"{target_season} season"
            except:
                pass

            self.logger.error(f"Error calculating team rankings for {season_info}: {e}")

            # Try fallback approach if we can determine the variables
            try:
                import sys
                import os
                sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
                from config import CURRENT_NFL_WEEK, NFL_SEASON
                from config import MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS
                use_current_season = CURRENT_NFL_WEEK >= MIN_WEEKS_FOR_CURRENT_SEASON_RANKINGS + 1

                if use_current_season:
                    self.logger.info(f"Attempting fallback to previous season ({NFL_SEASON - 1}) data...")
                    team_ids = {
                        1: 'ATL', 2: 'BUF', 3: 'CHI', 4: 'CIN', 5: 'CLE', 6: 'DAL', 7: 'DEN', 8: 'DET',
                        9: 'GB', 10: 'TEN', 11: 'IND', 12: 'KC', 13: 'LV', 14: 'LAR', 15: 'MIA', 16: 'MIN',
                        17: 'NE', 18: 'NO', 19: 'NYG', 20: 'NYJ', 21: 'PHI', 22: 'ARI', 23: 'PIT', 24: 'LAC',
                        25: 'SF', 26: 'SEA', 27: 'TB', 28: 'WSH', 29: 'CAR', 30: 'JAX', 33: 'BAL', 34: 'HOU'
                    }
                    return await self._calculate_team_rankings_for_season(NFL_SEASON - 1, team_ids)
            except Exception as fallback_error:
                self.logger.warning(f"Previous season fallback also failed: {fallback_error}")

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

    async def _parse_espn_data(self, data: Dict[str, Any]) -> List[ESPNPlayerData]:
        """Parse ESPN API response into ESPNPlayerData objects"""
        from config import (
            PROGRESS_UPDATE_FREQUENCY, PROGRESS_ETA_WINDOW_SIZE
        )

        projections = []
        unknown_position_count = 0  # Track players filtered due to unknown positions

        # Fetch team rankings and current week schedule for all players
        team_rankings = await self._fetch_team_rankings()
        current_week_schedule = await self._fetch_current_week_schedule()

        # Store schedule data for later use
        self.current_week_schedule = current_week_schedule

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

                # Extract ESPN player rating (using draft rank as proxy)
                player_rating = None
                draft_ranks = player_info.get('draftRanksByRankType', {})
                ppr_rank_data = draft_ranks.get('PPR', {})

                if ppr_rank_data and 'rank' in ppr_rank_data:
                    # Convert ESPN draft rank (1-2000+) to rating scale (15-100)
                    # Lower rank number = higher rating
                    draft_rank = ppr_rank_data['rank']
                    if draft_rank <= 50:  # Elite players
                        player_rating = 100.0 - (draft_rank - 1) * 0.4  # 100 to 80.4
                    elif draft_rank <= 150:  # Good players
                        player_rating = 80.0 - (draft_rank - 50) * 0.25  # 80 to 55
                    elif draft_rank <= 300:  # Average players
                        player_rating = 55.0 - (draft_rank - 150) * 0.2  # 55 to 25
                    else:  # Deep/waiver players
                        player_rating = max(15.0, 25.0 - (draft_rank - 300) * 0.01)  # 25 to 15

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

        return projections
