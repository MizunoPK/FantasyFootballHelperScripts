#!/usr/bin/env python3
"""
NFL API Client for Game Scores Collection

This module handles all communication with ESPN's NFL API for game scores
and statistics. Provides async operations with proper error handling and
rate limiting.

Author: Kai Mizuno
Last Updated: September 2025
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any, Optional

import httpx
from tenacity import retry, stop_after_attempt, wait_random_exponential

from nfl_scores_models import GameScore, Team, NFLAPIError
from scores_constants import ESPN_NFL_BASE_URL, ESPN_USER_AGENT, STATUS_IN_PROGRESS, STATUS_FINAL


class NFLAPIClient:
    """Async client for ESPN's NFL scoreboard API.
    
    ESPN provides a free, public API that doesn't require authentication.
    This client implements best practices:
    - Async HTTP requests for better performance
    - Automatic retry with exponential backoff
    - Rate limiting to be respectful to ESPN's servers
    - Comprehensive error handling
    """
    
    def __init__(self, settings):
        self.settings = settings
        # ESPN's base URL for NFL data - this is their public API endpoint
        self.base_url = ESPN_NFL_BASE_URL
        self.client: Optional[httpx.AsyncClient] = None  # HTTP client (created in context manager)
        
        # Setup logging for debugging and monitoring
        self.logger = logging.getLogger(__name__)
    
    @asynccontextmanager
    async def session(self):
        """Async context manager for HTTP client lifecycle.
        
        Creates and manages the HTTP client connection pool.
        This ensures proper resource cleanup and connection reuse.
        """
        # Create HTTP client with optimized settings
        self.client = httpx.AsyncClient(
            # Set timeout to prevent hanging requests
            timeout=httpx.Timeout(self.settings.request_timeout),
            # Connection pooling for better performance
            limits=httpx.Limits(max_keepalive_connections=20, max_connections=100),
            # Identify our client to ESPN's servers
            headers={'User-Agent': ESPN_USER_AGENT}
        )
        try:
            yield self  # Provide the client to the calling code
        finally:
            # Always close the client to free resources
            await self.client.aclose()
    
    @retry(
        wait=wait_random_exponential(min=1, max=30),  # Exponential backoff: 1s, 2s, 4s, etc. up to 30s
        stop=stop_after_attempt(3)  # Try 3 times total before giving up
    )
    async def _make_request(self, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Core HTTP request method with robust error handling.
        
        Implements:
        - Rate limiting to respect ESPN's servers
        - Automatic retries with exponential backoff
        - Proper HTTP status code handling
        - JSON parsing with error handling
        
        Args:
            url: The ESPN API endpoint to request
            params: Optional query parameters
            
        Returns:
            Parsed JSON response as dictionary
            
        Raises:
            NFLAPIError: For API-specific errors after retries exhausted
        """
        self.logger.info(f"Making request to: {url}")
        
        # Rate limiting - be respectful to ESPN's servers
        # This prevents us from overwhelming their API
        await asyncio.sleep(self.settings.rate_limit_delay)
        
        try:
            # Make the actual HTTP request
            response = await self.client.get(url, params=params)
            
            # Handle rate limiting explicitly
            if response.status_code == 429:
                # ESPN is telling us to slow down
                retry_after = int(response.headers.get('Retry-After', 30))
                self.logger.warning(f"Rate limited, waiting {retry_after} seconds")
                await asyncio.sleep(retry_after)
                # Raise exception to trigger tenacity retry
                raise NFLAPIError(f"Rate limited, retry after {retry_after} seconds")
            
            # Handle server errors
            if response.status_code >= 500:
                raise NFLAPIError(f"ESPN server error: {response.status_code}")
            
            # Handle client errors
            if response.status_code >= 400:
                raise NFLAPIError(f"ESPN API error: {response.status_code}")
            
            # Raise exception for any other HTTP errors
            response.raise_for_status()
            
            # Parse JSON response
            data = response.json()
            self.logger.info("Request successful")
            
            return data
            
        except httpx.RequestError as e:
            self.logger.error(f"Network error for {url}: {e}")
            raise NFLAPIError(f"Network error: {e}")
        except httpx.HTTPStatusError as e:
            self.logger.error(f"HTTP error {e.response.status_code} for {url}: {e}")
            raise NFLAPIError(f"HTTP {e.response.status_code}: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error for {url}: {e}")
            raise NFLAPIError(f"Unexpected error: {e}")
    
    async def get_current_week_scores(self) -> List[GameScore]:
        """Fetch scores for the current NFL week.
        
        This method gets whatever ESPN considers the "current" week,
        which might be the most recently completed week or the upcoming week.
        """
        url = f"{self.base_url}/scoreboard"
        data = await self._make_request(url)
        return self._parse_scoreboard_data(data)
    
    async def get_week_scores(self, week: int) -> List[GameScore]:
        """Fetch scores for a specific NFL week.
        
        Args:
            week: NFL week number (1-18 for regular season)
            
        Returns:
            List of GameScore objects for that week
        """
        url = f"{self.base_url}/scoreboard"
        # ESPN API parameters for specific week requests
        params = {
            "seasontype": self.settings.season_type,  # Regular season, preseason, or postseason
            "week": week,  # Specific week number
            "dates": self.settings.season  # Season year
        }
        data = await self._make_request(url, params=params)
        return self._parse_scoreboard_data(data)
    
    async def get_completed_games_recent(self, days_back: int = 7) -> List[GameScore]:
        """Fetch completed games from the last N days.

        This is useful when you don't know the specific week but want
        recent final scores. Automatically filters to only completed games.

        Args:
            days_back: Number of days to look back from today

        Returns:
            List of completed GameScore objects from the date range
        """
        try:
            # Calculate date range for the search
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)

            url = f"{self.base_url}/scoreboard"
            # ESPN accepts date ranges in YYYYMMDD-YYYYMMDD format
            params = {
                "dates": f"{start_date.strftime('%Y%m%d')}-{end_date.strftime('%Y%m%d')}",
                "limit": 1000  # High limit to ensure we get all games in the range
            }

            data = await self._make_request(url, params=params)
            games = self._parse_scoreboard_data(data)

            # Filter to only games that have finished
            # This is important because the API might return ongoing games
            return [game for game in games if game.is_completed]
        except Exception as e:
            self.logger.error(f"Error fetching recent completed games: {e}")
            return []
    
    def _parse_scoreboard_data(self, data: Dict[str, Any]) -> List[GameScore]:
        """Parse ESPN's scoreboard API response into our GameScore objects.
        
        ESPN's API returns a complex nested structure. This method extracts
        all the relevant game information and converts it to our clean data model.
        
        Args:
            data: Raw JSON response from ESPN API
            
        Returns:
            List of parsed GameScore objects
        """
        games = []
        
        # ESPN wraps games in an 'events' array
        events = data.get('events', [])
        self.logger.info(f"Processing {len(events)} games")
        
        # Process each game individually
        for event in events:
            try:
                # Skip if event is not a dictionary
                if not isinstance(event, dict):
                    self.logger.warning(f"Event is not a dictionary: {type(event)}")
                    continue
                
                # Parse individual game data
                game_score = self._parse_game_event(event)
                if game_score:
                    # Apply filtering based on settings
                    if not self.settings.only_completed_games or game_score.is_completed:
                        games.append(game_score)
            except Exception as e:
                # Log parsing errors but continue with other games
                # This prevents one bad game from breaking the entire collection
                event_id = event.get('id', 'unknown') if isinstance(event, dict) else 'non-dict'
                self.logger.warning(f"Failed to parse game {event_id}: {e}")
        
        self.logger.info(f"Successfully parsed {len(games)} games")
        return games
    
    def _parse_game_event(self, event: Dict[str, Any]) -> Optional[GameScore]:
        """Parse a single game from ESPN's complex nested JSON structure.
        
        ESPN's API returns games as 'events' with deeply nested data structures.
        This method extracts all available information and maps it to our clean model.
        
        Args:
            event: Single game event from ESPN API
            
        Returns:
            GameScore object or None if parsing fails
        """
        try:
            # Extract basic game information
            game_id = event.get('id', '')
            date_str = event.get('date', '')
            
            if not game_id or not date_str:
                self.logger.warning("Game missing required id or date")
                return None
            
            # Parse game date
            game_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            
            # Extract season information
            season_info = event.get('season', {})
            week = season_info.get('week', 0)
            season_year = season_info.get('year', self.settings.season)
            season_type = season_info.get('type', self.settings.season_type)
            
            # Extract competitions (there's usually only one)
            competitions = event.get('competitions', [])
            if not competitions:
                self.logger.warning(f"Game {game_id} has no competitions")
                return None
            
            competition = competitions[0]  # Take the first (and usually only) competition
            
            # Extract game status
            status = competition.get('status', {})
            if not isinstance(status, dict):
                self.logger.error(f"Status is not a dict: {status}")
                return None
            status_type = status.get('type', {})
            if not isinstance(status_type, dict):
                self.logger.error(f"Status type is not a dict: {status_type}")
                return None
            game_status = status_type.get('name', 'UNKNOWN')
            status_detail = status_type.get('detail', 'Unknown Status')
            is_completed = status_type.get('completed', False)
            is_in_progress = status_type.get('name', '').upper() in [STATUS_IN_PROGRESS, 'STATUS_HALFTIME', 'STATUS_END_PERIOD']
            
            # Extract teams and scores
            competitors = competition.get('competitors', [])
            if len(competitors) != 2:
                self.logger.warning(f"Game {game_id} doesn't have exactly 2 teams")
                return None
            
            # Determine home and away teams
            home_team_data = None
            away_team_data = None
            
            for competitor in competitors:
                if not isinstance(competitor, dict):
                    self.logger.error(f"Competitor is not a dict: {type(competitor)}")
                    return None
                home_away = competitor.get('homeAway')
                if home_away == 'home':
                    home_team_data = competitor
                else:
                    away_team_data = competitor
            
            if not home_team_data or not away_team_data:
                self.logger.warning(f"Game {game_id} missing home or away team designation")
                return None
            
            # Parse team information
            home_team_dict = home_team_data.get('team', {})
            home_team = self._parse_team_data(home_team_dict)
            
            away_team_dict = away_team_data.get('team', {})
            away_team = self._parse_team_data(away_team_dict)
            
            # Extract scores
            home_score = int(home_team_data.get('score', 0))
            away_score = int(away_team_data.get('score', 0))
            
            # Extract venue information
            venue = competition.get('venue', {})
            venue_name = venue.get('fullName')
            venue_address = venue.get('address', {})
            venue_city = venue_address.get('city')
            venue_state = venue_address.get('state')
            venue_capacity = venue.get('capacity')
            
            # Extract attendance
            attendance = competition.get('attendance')
            
            # Extract weather (if available)
            weather = competition.get('weather', {})
            temperature = weather.get('temperature')
            weather_desc = weather.get('conditionId')  # This might need mapping
            wind_speed = weather.get('highTemperature')  # ESPN's field names are inconsistent
            
            # Extract broadcast info
            broadcasts = competition.get('broadcasts', [])
            tv_network = None
            if broadcasts and isinstance(broadcasts[0], dict):
                market = broadcasts[0].get('market', {})
                if isinstance(market, dict):
                    tv_network = market.get('name')
                else:
                    tv_network = str(market) if market else None
            elif broadcasts and isinstance(broadcasts[0], str):
                tv_network = broadcasts[0]
            
            # Extract odds (if available)
            odds = competition.get('odds', [])
            home_odds = None
            away_odds = None
            over_under = None
            
            if odds:
                odd = odds[0]  # Take first odds entry
                home_odds = odd.get('homeTeamOdds', {}).get('moneyLine')
                away_odds = odd.get('awayTeamOdds', {}).get('moneyLine')
                over_under = odd.get('overUnder')
            
            # Extract detailed statistics (if available)
            home_stats = home_team_data.get('statistics', [])
            away_stats = away_team_data.get('statistics', [])
            
            home_total_yards = self._extract_stat(home_stats, 'totalYards')
            away_total_yards = self._extract_stat(away_stats, 'totalYards')
            home_turnovers = self._extract_stat(home_stats, 'turnovers')
            away_turnovers = self._extract_stat(away_stats, 'turnovers')
            
            # Extract quarter scores (if available)
            home_line_scores = home_team_data.get('linescores', [])
            away_line_scores = away_team_data.get('linescores', [])
            
            home_q1 = self._get_quarter_score(home_line_scores, 0)
            home_q2 = self._get_quarter_score(home_line_scores, 1)
            home_q3 = self._get_quarter_score(home_line_scores, 2)
            home_q4 = self._get_quarter_score(home_line_scores, 3)
            home_ot = self._get_quarter_score(home_line_scores, 4)
            
            away_q1 = self._get_quarter_score(away_line_scores, 0)
            away_q2 = self._get_quarter_score(away_line_scores, 1)
            away_q3 = self._get_quarter_score(away_line_scores, 2)
            away_q4 = self._get_quarter_score(away_line_scores, 3)
            away_ot = self._get_quarter_score(away_line_scores, 4)
            
            # Create the GameScore object
            game_score = GameScore(
                game_id=game_id,
                date=game_date,
                week=week,
                season=season_year,
                season_type=season_type,
                home_team=home_team,
                away_team=away_team,
                home_score=home_score,
                away_score=away_score,
                status=game_status,
                status_detail=status_detail,
                is_completed=is_completed,
                is_in_progress=is_in_progress,
                venue_name=venue_name,
                venue_city=venue_city,
                venue_state=venue_state,
                venue_capacity=venue_capacity,
                attendance=attendance,
                temperature=temperature,
                weather_description=weather_desc,
                wind_speed=wind_speed,
                tv_network=tv_network,
                home_team_odds=home_odds,
                away_team_odds=away_odds,
                over_under=over_under,
                home_total_yards=home_total_yards,
                away_total_yards=away_total_yards,
                home_turnovers=home_turnovers,
                away_turnovers=away_turnovers,
                home_score_q1=home_q1,
                home_score_q2=home_q2,
                home_score_q3=home_q3,
                home_score_q4=home_q4,
                home_score_ot=home_ot,
                away_score_q1=away_q1,
                away_score_q2=away_q2,
                away_score_q3=away_q3,
                away_score_q4=away_q4,
                away_score_ot=away_ot
            )
            
            return game_score
            
        except Exception as e:
            self.logger.error(f"Error parsing game event: {e}")
            return None
    
    def _parse_team_data(self, team_data: Dict[str, Any]) -> Team:
        """Parse team information from ESPN API format.
        
        Args:
            team_data: Team data from ESPN API
            
        Returns:
            Team object
        """
        if not isinstance(team_data, dict):
            self.logger.error(f"Team data is not a dict: {team_data}")
            # Return a basic Team object for now
            return Team(
                id='', 
                name='Unknown', 
                display_name='Unknown', 
                abbreviation='???', 
                location='Unknown'
            )
        
        record_data = team_data.get('record', {})
        record_value = None
        if isinstance(record_data, dict):
            record_value = record_data.get('displayValue')
            
        return Team(
            id=team_data.get('id', ''),
            name=team_data.get('name', ''),
            display_name=team_data.get('displayName', ''),
            abbreviation=team_data.get('abbreviation', ''),
            location=team_data.get('location', ''),
            color=team_data.get('color'),
            alternate_color=team_data.get('alternateColor'),
            logo_url=team_data.get('logo'),
            record=record_value
        )
    
    def _extract_stat(self, stats_list: List[Dict], stat_name: str) -> Optional[int]:
        """Extract a specific statistic from ESPN's stats format.
        
        Args:
            stats_list: List of statistics dictionaries
            stat_name: Name of the statistic to extract
            
        Returns:
            Statistic value as integer or None if not found
        """
        for stat in stats_list:
            if stat.get('name') == stat_name:
                try:
                    return int(stat.get('displayValue', 0))
                except (ValueError, TypeError):
                    return None
        return None
    
    def _get_quarter_score(self, line_scores: List[Dict], quarter_index: int) -> Optional[int]:
        """Extract score for a specific quarter from ESPN's linescore format.
        
        Args:
            line_scores: List of quarter scores
            quarter_index: Index of the quarter (0-3 for Q1-Q4, 4+ for OT)
            
        Returns:
            Quarter score as integer or None if not available
        """
        if quarter_index < len(line_scores):
            try:
                return int(line_scores[quarter_index].get('value', 0))
            except (ValueError, TypeError):
                return None
        return None