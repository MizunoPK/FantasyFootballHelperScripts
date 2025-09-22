#!/usr/bin/env python3
"""
ESPN Matchup Analysis Client

This module handles ESPN API interactions specifically for matchup analysis data.
Fetches team defense statistics, weekly schedules, and defensive performance trends.

Author: Generated for Fantasy Football Helper Scripts
Last Updated: September 2025
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from contextlib import asynccontextmanager

import httpx
from tenacity import retry, stop_after_attempt, wait_random_exponential

from matchup_models import (
    TeamDefenseStats, WeeklyMatchup, PlayerMatchupContext, FantasyPosition,
    HomeAwayStatus, GameStatus, InjuryStatus
)
from starter_helper_config import (
    ESPN_USER_AGENT, MATCHUP_REQUEST_TIMEOUT, MATCHUP_RATE_LIMIT_DELAY,
    MAX_CONCURRENT_MATCHUP_REQUESTS, CURRENT_NFL_WEEK, NFL_SEASON, NFL_SCORING_FORMAT,
    RECENT_WEEKS_FOR_DEFENSE
)

# Import shared fantasy points calculator
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / 'shared_files'))
from fantasy_points_calculator import FantasyPointsExtractor, extract_stat_entry_fantasy_points


class ESPNMatchupAPIError(Exception):
    """Custom exception for ESPN Matchup API errors"""
    pass


class ESPNMatchupRateLimitError(ESPNMatchupAPIError):
    """Rate limit exceeded exception"""
    pass


class ESPNMatchupServerError(ESPNMatchupAPIError):
    """ESPN server error exception"""
    pass


class ESPNMatchupClient:
    """ESPN API client for matchup analysis data"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._client = None
        self._session_lock = asyncio.Lock()

        # ESPN API endpoints based on ESPN_data_report.md
        self.fantasy_api_base = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{NFL_SEASON}/segments/0/leaguedefaults"
        self.nfl_api_base = "https://site.api.espn.com/apis/site/v2/sports/football/nfl"

        # Scoring format mapping
        self.scoring_format_id = {
            "std": 1,    # Standard (Non-PPR)
            "half": 2,   # Half-PPR
            "ppr": 3     # PPR (Points Per Reception)
        }.get(NFL_SCORING_FORMAT, 3)

        # ESPN team ID to defense player ID mapping (negative IDs)
        self.team_to_defense_id = {
            1: -16001,   # ATL -> Falcons D/ST
            2: -16002,   # BUF -> Bills D/ST
            3: -16003,   # CHI -> Bears D/ST
            4: -16004,   # CIN -> Bengals D/ST
            5: -16005,   # CLE -> Browns D/ST
            6: -16006,   # DAL -> Cowboys D/ST
            7: -16007,   # DEN -> Broncos D/ST
            8: -16008,   # DET -> Lions D/ST
            9: -16009,   # GB -> Packers D/ST
            10: -16010,  # TEN -> Titans D/ST
            11: -16011,  # IND -> Colts D/ST
            12: -16012,  # KC -> Chiefs D/ST
            13: -16013,  # LV -> Raiders D/ST
            14: -16014,  # LAR -> Rams D/ST
            15: -16015,  # MIA -> Dolphins D/ST
            16: -16016,  # MIN -> Vikings D/ST
            17: -16017,  # NE -> Patriots D/ST
            18: -16018,  # NO -> Saints D/ST
            19: -16019,  # NYG -> Giants D/ST
            20: -16020,  # NYJ -> Jets D/ST
            21: -16021,  # PHI -> Eagles D/ST
            22: -16022,  # ARI -> Cardinals D/ST
            23: -16023,  # PIT -> Steelers D/ST
            24: -16024,  # LAC -> Chargers D/ST
            25: -16025,  # SF -> 49ers D/ST
            26: -16026,  # SEA -> Seahawks D/ST
            27: -16027,  # TB -> Buccaneers D/ST
            28: -16028,  # WSH -> Commanders D/ST
            29: -16029,  # CAR -> Panthers D/ST
            30: -16030,  # JAX -> Jaguars D/ST
            33: -16033,  # BAL -> Ravens D/ST
            34: -16034   # HOU -> Texans D/ST
        }

        # ESPN team ID to abbreviation mapping
        self.team_abbreviations = {
            1: 'ATL', 2: 'BUF', 3: 'CHI', 4: 'CIN', 5: 'CLE', 6: 'DAL',
            7: 'DEN', 8: 'DET', 9: 'GB', 10: 'TEN', 11: 'IND', 12: 'KC',
            13: 'LV', 14: 'LAR', 15: 'MIA', 16: 'MIN', 17: 'NE', 18: 'NO',
            19: 'NYG', 20: 'NYJ', 21: 'PHI', 22: 'ARI', 23: 'PIT', 24: 'LAC',
            25: 'SF', 26: 'SEA', 27: 'TB', 28: 'WSH', 29: 'CAR', 30: 'JAX',
            33: 'BAL', 34: 'HOU'
        }

    @asynccontextmanager
    async def session(self):
        """Async context manager for HTTP client session"""
        async with self._session_lock:
            if self._client is None:
                timeout = httpx.Timeout(MATCHUP_REQUEST_TIMEOUT)
                self._client = httpx.AsyncClient(timeout=timeout)
                self.logger.debug("Created new ESPN matchup HTTP client session")

        try:
            yield self._client
        finally:
            pass  # Keep session open for reuse

    async def close(self):
        """Close the HTTP client session"""
        async with self._session_lock:
            if self._client:
                await self._client.aclose()
                self._client = None
                self.logger.debug("Closed ESPN matchup HTTP client session")

    @retry(stop=stop_after_attempt(3), wait=wait_random_exponential(multiplier=1, max=10))
    async def _make_request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request with retry logic and rate limiting"""
        self.logger.debug(f"Making matchup request to: {url}")

        # Add rate limiting delay
        await asyncio.sleep(MATCHUP_RATE_LIMIT_DELAY)

        try:
            async with self.session() as client:
                response = await client.request(method, url, **kwargs)

                if response.status_code == 429:
                    self.logger.warning("Rate limited by ESPN API, retrying...")
                    raise ESPNMatchupRateLimitError("Rate limit exceeded")

                if response.status_code >= 500:
                    self.logger.error(f"ESPN server error: {response.status_code}")
                    raise ESPNMatchupServerError(f"Server error: {response.status_code}")

                response.raise_for_status()
                return response.json()

        except httpx.TimeoutException:
            self.logger.error("Timeout making ESPN matchup request")
            raise ESPNMatchupAPIError("Request timeout")
        except httpx.HTTPStatusError as e:
            self.logger.error(f"HTTP error in matchup request: {e}")
            raise ESPNMatchupAPIError(f"HTTP error: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error in matchup request: {e}")
            raise ESPNMatchupAPIError(f"Unexpected error: {e}")

    async def fetch_current_week_schedule(self, week: Optional[int] = None) -> List[WeeklyMatchup]:
        """
        Fetch current week NFL schedule and matchups.
        Returns list of WeeklyMatchup objects for the specified week.
        """
        target_week = week or CURRENT_NFL_WEEK
        self.logger.info(f"Fetching NFL schedule for week {target_week}")

        try:
            # Use NFL Scores API for schedule data
            url = f"{self.nfl_api_base}/scoreboard"
            params = {
                "seasontype": 2,  # Regular season
                "week": target_week,
                "dates": NFL_SEASON
            }

            headers = {"User-Agent": ESPN_USER_AGENT}

            data = await self._make_request("GET", url, params=params, headers=headers)

            matchups = []
            for event in data.get("events", []):
                try:
                    matchup = self._parse_nfl_event_to_matchup(event, target_week)
                    if matchup:
                        matchups.append(matchup)
                except Exception as e:
                    self.logger.warning(f"Failed to parse NFL event {event.get('id', 'unknown')}: {e}")
                    continue

            self.logger.info(f"Successfully fetched {len(matchups)} matchups for week {target_week}")
            return matchups

        except Exception as e:
            self.logger.error(f"Failed to fetch week {target_week} schedule: {e}")
            raise ESPNMatchupAPIError(f"Failed to fetch schedule: {e}")

    def _parse_nfl_event_to_matchup(self, event: Dict[str, Any], week: int) -> Optional[WeeklyMatchup]:
        """Parse NFL event data into WeeklyMatchup object"""
        try:
            competition = event["competitions"][0]
            competitors = competition["competitors"]

            # Find home and away teams
            home_team = next(c for c in competitors if c["homeAway"] == "home")
            away_team = next(c for c in competitors if c["homeAway"] == "away")

            # Parse game status
            status_data = competition["status"]["type"]
            game_status = GameStatus.SCHEDULED
            if status_data["name"] == "STATUS_FINAL":
                game_status = GameStatus.FINAL
            elif status_data["name"] == "STATUS_IN_PROGRESS":
                game_status = GameStatus.IN_PROGRESS
            elif "POSTPONED" in status_data["name"]:
                game_status = GameStatus.POSTPONED
            elif "CANCELED" in status_data["name"]:
                game_status = GameStatus.CANCELED

            # Parse venue and weather
            venue_data = competition.get("venue", {})
            weather_data = competition.get("weather", {})

            matchup = WeeklyMatchup(
                week=week,
                season=NFL_SEASON,
                home_team_id=int(home_team["team"]["id"]),
                home_team_name=home_team["team"]["name"],
                home_team_abbreviation=home_team["team"]["abbreviation"],
                away_team_id=int(away_team["team"]["id"]),
                away_team_name=away_team["team"]["name"],
                away_team_abbreviation=away_team["team"]["abbreviation"],
                game_date=datetime.fromisoformat(event["date"].replace("Z", "+00:00")),
                game_status=game_status,
                venue_name=venue_data.get("fullName"),
                venue_city=venue_data.get("address", {}).get("city"),
                is_indoor=venue_data.get("indoor"),
                temperature=weather_data.get("temperature"),
                weather_condition=weather_data.get("description")
            )

            return matchup

        except Exception as e:
            self.logger.error(f"Error parsing NFL event: {e}")
            return None

    async def fetch_team_defense_stats(self, team_ids: Optional[List[int]] = None) -> Dict[int, TeamDefenseStats]:
        """
        Fetch team defense statistics for fantasy points allowed by position.
        If team_ids not provided, fetches for all teams.
        """
        target_teams = team_ids or list(self.team_abbreviations.keys())
        self.logger.info(f"Fetching defense stats for {len(target_teams)} teams")

        defense_stats = {}

        # Create semaphore for concurrent request limiting
        semaphore = asyncio.Semaphore(MAX_CONCURRENT_MATCHUP_REQUESTS)

        async def fetch_team_defense(team_id: int) -> Optional[TeamDefenseStats]:
            async with semaphore:
                try:
                    return await self._fetch_single_team_defense_stats(team_id)
                except Exception as e:
                    self.logger.error(f"Failed to fetch defense stats for team {team_id}: {e}")
                    return None

        # Fetch all team defense stats concurrently
        tasks = [fetch_team_defense(team_id) for team_id in target_teams]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        for team_id, result in zip(target_teams, results):
            if isinstance(result, TeamDefenseStats):
                defense_stats[team_id] = result
            elif isinstance(result, Exception):
                self.logger.error(f"Exception fetching team {team_id} defense: {result}")

        self.logger.info(f"Successfully fetched defense stats for {len(defense_stats)} teams")
        return defense_stats

    async def _fetch_single_team_defense_stats(self, team_id: int) -> TeamDefenseStats:
        """Fetch defense statistics for a single team"""
        defense_id = self.team_to_defense_id.get(team_id)
        if not defense_id:
            raise ESPNMatchupAPIError(f"No defense ID found for team {team_id}")

        team_abbr = self.team_abbreviations.get(team_id, f"TEAM{team_id}")
        team_name = team_abbr  # Simplified for now

        # Fetch seasonal defense stats
        seasonal_stats = await self._fetch_defense_seasonal_stats(defense_id)

        # Fetch recent weeks trends
        recent_stats = await self._fetch_defense_recent_trends(defense_id)

        # Calculate points allowed by position from defense stats
        defense_stats = TeamDefenseStats(
            team_id=team_id,
            team_name=team_name,
            team_abbreviation=team_abbr,
            qb_points_allowed=seasonal_stats.get("qb_allowed", 0.0),
            rb_points_allowed=seasonal_stats.get("rb_allowed", 0.0),
            wr_points_allowed=seasonal_stats.get("wr_allowed", 0.0),
            te_points_allowed=seasonal_stats.get("te_allowed", 0.0),
            k_points_allowed=seasonal_stats.get("k_allowed", 0.0),
            dst_points_allowed=seasonal_stats.get("dst_allowed", 0.0),
            recent_qb_trend=recent_stats.get("qb_trend", 0.0),
            recent_rb_trend=recent_stats.get("rb_trend", 0.0),
            recent_wr_trend=recent_stats.get("wr_trend", 0.0),
            recent_te_trend=recent_stats.get("te_trend", 0.0),
            recent_k_trend=recent_stats.get("k_trend", 0.0),
            recent_dst_trend=recent_stats.get("dst_trend", 0.0),
            games_played=seasonal_stats.get("games_played", 0),
            recent_games_analyzed=recent_stats.get("games_analyzed", 0)
        )

        return defense_stats

    async def _fetch_defense_seasonal_stats(self, defense_id: int) -> Dict[str, float]:
        """Fetch seasonal defense statistics"""
        url = f"{self.fantasy_api_base}/{self.scoring_format_id}"

        params = {
            "view": "kona_player_info",
            "scoringPeriodId": 0  # 0 = full season data
        }

        headers = {
            "User-Agent": ESPN_USER_AGENT,
            "X-Fantasy-Filter": f'{{"players":{{"filterIds":{{"value":[{defense_id}]}}}}}}'
        }

        try:
            data = await self._make_request("GET", url, params=params, headers=headers)

            if not data.get("players"):
                self.logger.warning(f"No defense data found for ID {defense_id}")
                return self._get_default_defense_stats()

            player_data = data["players"][0]["player"]
            stats_array = player_data.get("stats", [])

            # Extract defensive stats from season data
            return self._parse_defense_stats(stats_array, is_seasonal=True)

        except Exception as e:
            self.logger.error(f"Failed to fetch seasonal defense stats for {defense_id}: {e}")
            return self._get_default_defense_stats()

    async def _fetch_defense_recent_trends(self, defense_id: int) -> Dict[str, float]:
        """Fetch recent weeks defense trends"""
        recent_weeks_data = []

        # Fetch last RECENT_WEEKS_FOR_DEFENSE weeks
        start_week = max(1, CURRENT_NFL_WEEK - RECENT_WEEKS_FOR_DEFENSE)
        end_week = min(CURRENT_NFL_WEEK - 1, 18)  # Don't include current week

        for week in range(start_week, end_week + 1):
            try:
                week_data = await self._fetch_defense_week_stats(defense_id, week)
                if week_data:
                    recent_weeks_data.append(week_data)
            except Exception as e:
                self.logger.warning(f"Failed to fetch week {week} defense stats: {e}")
                continue

        # Calculate trends from recent weeks
        return self._calculate_defense_trends(recent_weeks_data)

    async def _fetch_defense_week_stats(self, defense_id: int, week: int) -> Optional[Dict[str, float]]:
        """Fetch defense statistics for a specific week"""
        url = f"{self.fantasy_api_base}/{self.scoring_format_id}"

        params = {
            "view": "kona_player_info",
            "scoringPeriodId": week
        }

        headers = {
            "User-Agent": ESPN_USER_AGENT,
            "X-Fantasy-Filter": f'{{"players":{{"filterIds":{{"value":[{defense_id}]}}}}}}'
        }

        try:
            data = await self._make_request("GET", url, params=params, headers=headers)

            if not data.get("players"):
                return None

            player_data = data["players"][0]["player"]
            stats_array = player_data.get("stats", [])

            return self._parse_defense_stats(stats_array, is_seasonal=False)

        except Exception as e:
            self.logger.debug(f"Failed to fetch week {week} defense stats: {e}")
            return None

    def _parse_defense_stats(self, stats_array: List[Dict], is_seasonal: bool = True) -> Dict[str, float]:
        """Parse defense stats array into points allowed by position"""
        # This is a simplified implementation
        # In reality, defense stats would need to be calculated differently
        # For now, return placeholder values that represent defensive strength

        total_fantasy_points = 0.0
        games_played = 1

        for stat_entry in stats_array:
            if stat_entry.get("scoringPeriodId") == (0 if is_seasonal else stat_entry.get("scoringPeriodId")):
                total_fantasy_points = stat_entry.get("appliedTotal", 0.0)
                break

        # Estimate points allowed by position based on defense performance
        # Better defenses (higher fantasy points) allow fewer points to opponents
        base_points = max(5.0, 25.0 - (total_fantasy_points / 10.0))

        return {
            "qb_allowed": base_points + 2.0,  # QBs typically score more
            "rb_allowed": base_points,
            "wr_allowed": base_points,
            "te_allowed": base_points - 2.0,  # TEs typically score less
            "k_allowed": base_points - 5.0,   # Kickers score least
            "dst_allowed": base_points,
            "games_played": games_played
        }

    def _calculate_defense_trends(self, recent_weeks_data: List[Dict[str, float]]) -> Dict[str, float]:
        """Calculate defensive trends from recent weeks data"""
        if not recent_weeks_data:
            return {
                "qb_trend": 0.0, "rb_trend": 0.0, "wr_trend": 0.0,
                "te_trend": 0.0, "k_trend": 0.0, "dst_trend": 0.0,
                "games_analyzed": 0
            }

        # Calculate average points allowed for recent weeks
        positions = ["qb_allowed", "rb_allowed", "wr_allowed", "te_allowed", "k_allowed", "dst_allowed"]
        trends = {}

        for pos in positions:
            values = [week_data.get(pos, 0.0) for week_data in recent_weeks_data]
            avg_value = sum(values) / len(values) if values else 0.0
            trend_key = pos.replace("_allowed", "_trend")
            trends[trend_key] = avg_value

        trends["games_analyzed"] = len(recent_weeks_data)
        return trends

    def _get_default_defense_stats(self) -> Dict[str, float]:
        """Return default defense stats when data is unavailable"""
        return {
            "qb_allowed": 20.0, "rb_allowed": 15.0, "wr_allowed": 15.0,
            "te_allowed": 10.0, "k_allowed": 8.0, "dst_allowed": 12.0,
            "games_played": 1
        }

    async def create_player_matchup_context(self, player_id: str, player_name: str,
                                          player_position: FantasyPosition, player_team_id: int,
                                          week: Optional[int] = None) -> Optional[PlayerMatchupContext]:
        """
        Create matchup context for a specific player by finding their opponent.
        """
        target_week = week or CURRENT_NFL_WEEK

        try:
            # Get weekly matchups to find opponent
            matchups = await self.fetch_current_week_schedule(target_week)

            # Find the matchup for this player's team
            player_matchup = None
            for matchup in matchups:
                if matchup.home_team_id == player_team_id or matchup.away_team_id == player_team_id:
                    player_matchup = matchup
                    break

            if not player_matchup:
                self.logger.warning(f"No matchup found for team {player_team_id} in week {target_week}")
                return None

            # Get opponent information
            opponent_info = player_matchup.get_opponent_for_team(player_team_id)
            if not opponent_info:
                return None

            # Create player matchup context
            context = PlayerMatchupContext(
                player_id=player_id,
                player_name=player_name,
                player_position=player_position,
                player_team_id=player_team_id,
                player_team_abbreviation=self.team_abbreviations.get(player_team_id, f"TEAM{player_team_id}"),
                opponent_team_id=opponent_info["team_id"],
                opponent_team_name=opponent_info["team_name"],
                opponent_team_abbreviation=opponent_info["team_abbreviation"],
                is_home_game=player_matchup.is_home_team(player_team_id),
                week=target_week,
                game_date=player_matchup.game_date,
                injury_status=InjuryStatus.ACTIVE,  # Will be updated by caller if needed
                is_available=True
            )

            return context

        except Exception as e:
            self.logger.error(f"Failed to create matchup context for player {player_id}: {e}")
            return None

    async def get_league_average_points_allowed(self, position: FantasyPosition) -> float:
        """Get league average points allowed to a specific position"""
        try:
            # Fetch all team defense stats
            all_defense_stats = await self.fetch_team_defense_stats()

            if not all_defense_stats:
                # Return default league averages if no data available
                defaults = {
                    FantasyPosition.QB: 18.0,
                    FantasyPosition.RB: 14.0,
                    FantasyPosition.WR: 13.5,
                    FantasyPosition.TE: 9.0,
                    FantasyPosition.K: 7.5,
                    FantasyPosition.DST: 10.0,
                    FantasyPosition.FLEX: 13.5
                }
                return defaults.get(position, 12.0)

            # Calculate league average for this position
            position_values = []
            for defense in all_defense_stats.values():
                points_allowed = defense.get_points_allowed_by_position(position)
                position_values.append(points_allowed)

            if position_values:
                return sum(position_values) / len(position_values)
            else:
                return 12.0  # Default fallback

        except Exception as e:
            self.logger.error(f"Failed to get league average for {position}: {e}")
            return 12.0  # Default fallback