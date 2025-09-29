#!/usr/bin/env python3
"""
NFL Team Scores Data Collection Script - ESPN API
=================================================

Retrieves the latest completed NFL game scores using ESPN's free API.
Focuses on final game results with comprehensive team and game details.

Example Usage:
    # Collect current week scores
    python data_fetcher-scores.py
    
    # Collect specific week (set NFL_SCORES_CURRENT_WEEK environment variable)
    NFL_SCORES_CURRENT_WEEK=15 python data_fetcher-scores.py
    
    # Collect only completed games from last 10 days  
    NFL_SCORES_ONLY_COMPLETED_GAMES=true python data_fetcher-scores.py
    
    # Change output directory
    NFL_SCORES_OUTPUT_DIRECTORY=./my_scores python data_fetcher-scores.py
    
    # Using .env file (create .env in project root):
    # NFL_SCORES_SEASON=2025
    # NFL_SCORES_CURRENT_WEEK=15
    # NFL_SCORES_OUTPUT_DIRECTORY=./data/nfl_scores

Author: Kai Mizuno
Last Updated: September 2025

Dependencies:
    pip install httpx pydantic python-dotenv pandas openpyxl
"""

# Standard library imports for async operations, JSON handling, logging, and datetime
import asyncio
import json
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from contextlib import asynccontextmanager

# Third-party imports
import httpx  # Modern async HTTP client (replacement for requests)
import pandas as pd  # Data manipulation and CSV/Excel export
from pydantic import BaseModel, Field  # Data validation and serialization
from pydantic_settings import BaseSettings, SettingsConfigDict  # Environment variable management
from tenacity import retry, stop_after_attempt, wait_random_exponential  # Retry logic with backoff


# Configuration Management
# ========================
# Uses Pydantic Settings to automatically load configuration from environment variables
# and .env file. This provides type validation and default values.
class Settings(BaseSettings):
    # Pydantic v2 configuration
    model_config = SettingsConfigDict(
        env_file='.env',  # Load from .env file in project root
        env_file_encoding='utf-8',  # Handle Unicode characters in env file
        env_prefix='NFL_SCORES_',  # Only load variables starting with this prefix
        extra='ignore'  # Ignore extra environment variables (fixes validation errors)
    )
    
    # Data Collection Parameters
    # ==========================
    season: int = 2025  # NFL season year (2024 = 2024-2025 season)
    season_type: int = 2  # ESPN season type: 1=Preseason, 2=Regular Season, 3=Postseason
    current_week: Optional[int] = None  # Specific week to fetch; None = get recent games
    only_completed_games: bool = True  # Filter to only include finished games
    
    # File Output Configuration
    # ========================
    output_directory: str = "./data/nfl_scores"  # Directory for generated files
    create_csv: bool = False  # Whether to create CSV output
    create_json: bool = False  # Whether to create JSON output
    create_excel: bool = True  # Whether to create Excel output
    create_condensed_excel: bool = True  # Whether to create condensed Excel output
    
    # HTTP Client Settings
    # ===================
    request_timeout: int = 30  # Seconds to wait for ESPN API response
    max_retries: int = 3  # Number of retry attempts for failed requests
    rate_limit_delay: float = 0.5  # Seconds to wait between requests (be nice to ESPN)


# Data Models - Pydantic Models for Type Safety and Validation
# =============================================================
# These models define the structure of our data and provide automatic
# validation, serialization, and documentation.

class Team(BaseModel):
    """Represents an NFL team with all relevant metadata.
    
    ESPN provides extensive team information that we capture here.
    Optional fields handle cases where ESPN doesn't provide all data.
    """
    id: str  # ESPN's unique team identifier
    name: str  # Team name (e.g., "Cowboys")
    display_name: str  # Full display name (e.g., "Dallas Cowboys")
    abbreviation: str  # 3-letter code (e.g., "DAL")
    location: str  # City/location (e.g., "Dallas")
    color: Optional[str] = None  # Primary team color (hex code)
    alternate_color: Optional[str] = None  # Secondary team color
    logo_url: Optional[str] = None  # URL to team logo image
    record: Optional[str] = None  # Season record in "W-L" format


class GameScore(BaseModel):
    """Comprehensive NFL game data model.
    
    Captures everything we might want to know about an NFL game,
    from basic scores to detailed venue and weather information.
    The model automatically calculates derived fields after initialization.
    """
    
    # Core Game Identification
    # ========================
    game_id: str  # ESPN's unique game identifier
    date: datetime  # Game date and time (timezone-aware)
    week: int  # NFL week number (1-18 for regular season)
    season: int  # Season year
    season_type: int  # Season type (preseason, regular, postseason)
    
    # Team Information
    # ================
    home_team: Team  # Complete home team data
    away_team: Team  # Complete away team data
    
    # Final Scores
    # ============
    home_score: int  # Home team final score
    away_score: int  # Away team final score
    
    # Game Status Information
    # ======================
    status: str  # ESPN status code ("STATUS_FINAL", "STATUS_IN_PROGRESS", etc.)
    status_detail: str  # Human-readable status description
    is_completed: bool  # Whether the game is finished
    
    # Venue and Location Details
    # ==========================
    venue_name: Optional[str] = None  # Stadium name (e.g., "AT&T Stadium")
    venue_city: Optional[str] = None  # Stadium city
    venue_state: Optional[str] = None  # Stadium state
    venue_capacity: Optional[int] = None  # Stadium seating capacity
    attendance: Optional[int] = None  # Actual game attendance
    
    # Weather Conditions (if available)
    # ================================
    temperature: Optional[int] = None  # Game temperature in Fahrenheit
    weather_description: Optional[str] = None  # Weather condition description
    wind_speed: Optional[int] = None  # Wind speed in MPH
    
    # Broadcast Information
    # ====================
    tv_network: Optional[str] = None  # TV network broadcasting the game
    
    # Betting Information (if available)
    # =================================
    home_team_odds: Optional[float] = None  # Home team betting odds
    away_team_odds: Optional[float] = None  # Away team betting odds
    over_under: Optional[float] = None  # Total points over/under line
    
    # Basic Game Statistics
    # ====================
    # ESPN sometimes provides summary stats, we capture the most important ones
    home_total_yards: Optional[int] = None  # Home team total offensive yards
    away_total_yards: Optional[int] = None  # Away team total offensive yards
    home_turnovers: Optional[int] = None  # Home team turnovers
    away_turnovers: Optional[int] = None  # Away team turnovers
    
    # Quarter-by-Quarter Scoring
    # =========================
    # Detailed scoring breakdown by quarter (and overtime if applicable)
    home_score_q1: Optional[int] = None  # Home team Q1 score
    home_score_q2: Optional[int] = None  # Home team Q2 score
    home_score_q3: Optional[int] = None  # Home team Q3 score
    home_score_q4: Optional[int] = None  # Home team Q4 score
    home_score_ot: Optional[int] = None  # Home team overtime score
    away_score_q1: Optional[int] = None  # Away team Q1 score
    away_score_q2: Optional[int] = None  # Away team Q2 score
    away_score_q3: Optional[int] = None  # Away team Q3 score
    away_score_q4: Optional[int] = None  # Away team Q4 score
    away_score_ot: Optional[int] = None  # Away team overtime score
    
    # Calculated/Derived Fields
    # ========================
    # These fields are automatically calculated after the model is created
    total_points: int = Field(default=0)  # Combined score of both teams
    point_difference: int = Field(default=0)  # Absolute difference between scores
    winning_team: str = Field(default="")  # Abbreviation of winning team
    is_overtime: bool = Field(default=False)  # Whether game went to overtime
    
    # Record Keeping
    # =============
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))  # When this data was collected
    
    def model_post_init(self, __context):
        """Automatically calculate derived fields after model initialization.
        
        This Pydantic v2 hook runs after all fields are set, allowing us to
        compute additional fields based on the provided data. This ensures
        consistency and reduces the chance of calculation errors.
        """
        # Calculate total points scored in the game
        self.total_points = self.home_score + self.away_score
        
        # Calculate point difference (always positive)
        self.point_difference = abs(self.home_score - self.away_score)
        
        # Determine the winning team
        if self.home_score > self.away_score:
            self.winning_team = self.home_team.abbreviation
        elif self.away_score > self.home_score:
            self.winning_team = self.away_team.abbreviation
        else:
            self.winning_team = "TIE"  # Rare in NFL, but possible in regular season
        
        # Check if the game went to overtime
        # Any non-zero overtime score indicates an overtime game
        self.is_overtime = any([
            self.home_score_ot and self.home_score_ot > 0,
            self.away_score_ot and self.away_score_ot > 0
        ])


class WeeklyScores(BaseModel):
    """Container for a collection of NFL games from a specific time period.
    
    This model groups multiple GameScore objects together with metadata
    about the collection, making it easy to export and analyze.
    """
    week: int  # Week number (0 for multi-week collections)
    season: int  # Season year
    season_type: int  # Season type
    total_games: int  # Total number of games found
    completed_games: int  # Number of finished games
    games: List[GameScore]  # List of all game data
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))  # Collection timestamp


# ESPN API Client - The Heart of Data Collection
# ==============================================
# This class handles all communication with ESPN's public API.
# It implements proper async patterns, retry logic, and rate limiting.

class ESPNScoresClient:
    """Async client for ESPN's NFL scoreboard API.
    
    ESPN provides a free, public API that doesn't require authentication.
    This client implements best practices:
    - Async HTTP requests for better performance
    - Automatic retry with exponential backoff
    - Rate limiting to be respectful to ESPN's servers
    - Comprehensive error handling
    """
    
    def __init__(self, settings: Settings):
        self.settings = settings
        # ESPN's base URL for NFL data - this is their public API endpoint
        self.base_url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl"
        self.client: Optional[httpx.AsyncClient] = None  # HTTP client (created in context manager)
        
        # Setup logging for debugging and monitoring
        logging.basicConfig(level=logging.INFO)
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
            headers={'User-Agent': 'NFL-Scores-Collector/1.0'}
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
            httpx.HTTPStatusError: For HTTP errors after retries exhausted
        """
        self.logger.info(f"Making request to: {url}")
        
        # Rate limiting - be respectful to ESPN's servers
        # This prevents us from overwhelming their API
        await asyncio.sleep(self.settings.rate_limit_delay)
        
        # Make the actual HTTP request
        response = await self.client.get(url, params=params)
        
        # Handle rate limiting explicitly
        if response.status_code == 429:
            # ESPN is telling us to slow down
            retry_after = int(response.headers.get('Retry-After', 30))
            self.logger.warning(f"Rate limited, waiting {retry_after} seconds")
            await asyncio.sleep(retry_after)
            # Raise exception to trigger tenacity retry
            raise httpx.HTTPStatusError("Rate limited", request=response.request, response=response)
        
        # Raise exception for any other HTTP errors (4xx, 5xx)
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        self.logger.info("Request successful")
        
        return data
    
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
                # Parse individual game data
                game_score = self._parse_game_event(event)
                if game_score:
                    # Apply filtering based on settings
                    if not self.settings.only_completed_games or game_score.is_completed:
                        games.append(game_score)
            except Exception as e:
                # Log parsing errors but continue with other games
                # This prevents one bad game from breaking the entire collection
                self.logger.warning(f"Failed to parse game {event.get('id', 'unknown')}: {e}")
        
        self.logger.info(f"Successfully parsed {len(games)} games")
        return games
    
    def _parse_game_event(self, event: Dict[str, Any]) -> Optional[GameScore]:
        """Parse a single game from ESPN's complex nested JSON structure.
        
        ESPN's API returns games as 'events' with deeply nested data structures.
        This method extracts all available information and maps it to our clean model.
        
        The ESPN structure looks like:
        event -> competitions[0] -> competitors[] (home/away teams)
                                 -> venue {}, weather {}, odds [], etc.
        
        Args:
            event: Single game event from ESPN API
            
        Returns:
            GameScore object or None if parsing fails
        """
        try:
            # ESPN wraps game data in a 'competitions' array (usually just one item)
            competition = event['competitions'][0]
            competitors = competition['competitors']  # Array of 2 teams
            
            # Extract home and away team data
            # ESPN marks teams with 'homeAway' field
            home_competitor = next(c for c in competitors if c['homeAway'] == 'home')
            away_competitor = next(c for c in competitors if c['homeAway'] == 'away')
            
            # Parse team information using helper method
            home_team = self._parse_team_data(home_competitor['team'])
            away_team = self._parse_team_data(away_competitor['team'])
            
            # ESPN provides season records separately from team data
            # Records are in "W-L" format (e.g., "10-3")
            if 'records' in home_competitor and home_competitor['records']:
                home_team.record = home_competitor['records'][0].get('summary', '')
            if 'records' in away_competitor and away_competitor['records']:
                away_team.record = away_competitor['records'][0].get('summary', '')
            
            # Parse game status information
            # ESPN uses specific status codes like 'STATUS_FINAL', 'STATUS_IN_PROGRESS', etc.
            status = event['status']['type']['name']
            status_detail = event['status']['type']['description']  # Human-readable description
            is_completed = status == 'STATUS_FINAL'  # Only final games have complete data
            
            # Extract final scores
            # ESPN always provides scores as strings, so we convert to integers
            home_score = int(home_competitor.get('score', 0))
            away_score = int(away_competitor.get('score', 0))
            
            # Extract venue/stadium information
            venue = competition.get('venue', {})
            venue_name = venue.get('fullName')  # Full stadium name
            venue_address = venue.get('address', {})  # Nested address object
            venue_city = venue_address.get('city')
            venue_state = venue_address.get('state')
            venue_capacity = venue.get('capacity')  # Maximum seating capacity
            
            # Game attendance (actual people who attended)
            attendance = competition.get('attendance')
            
            # Extract weather conditions (mostly for outdoor games)
            weather = competition.get('weather', {})
            temperature = weather.get('temperature')  # Fahrenheit
            weather_description = weather.get('conditionId')  # Weather condition code
            wind_speed = None
            if 'wind' in weather:
                wind_speed = weather['wind'].get('speed')  # Wind speed in MPH
            
            # Extract TV broadcast information
            broadcasts = competition.get('broadcasts', [])
            # ESPN provides broadcasts as array; we take the first/primary network
            tv_network = broadcasts[0].get('names', [''])[0] if broadcasts else None
            
            # Extract betting odds (if available)
            # Note: ESPN doesn't always provide odds, and format can vary
            odds = competition.get('odds', [])
            home_team_odds = None
            away_team_odds = None
            over_under = None
            
            if odds:
                # Odds structure can be complex, we extract what's available
                details = odds[0].get('details')  # Spread information
                over_under = odds[0].get('overUnder')  # Total points line
                # TODO: Could parse spread/moneyline odds here if needed
            
            # Extract quarter-by-quarter scoring
            # This gives us detailed scoring progression throughout the game
            linescore = competition.get('linescore', [])
            quarter_scores = self._parse_quarter_scores(linescore, home_competitor, away_competitor)
            
            # Extract basic game statistics (if available)
            # ESPN sometimes provides summary stats, we capture the most important ones
            home_stats = home_competitor.get('statistics', [])
            away_stats = away_competitor.get('statistics', [])
            
            # Use helper method to safely extract specific stats
            home_total_yards = self._get_stat_value(home_stats, 'totalYards')
            away_total_yards = self._get_stat_value(away_stats, 'totalYards')
            home_turnovers = self._get_stat_value(home_stats, 'turnovers')
            away_turnovers = self._get_stat_value(away_stats, 'turnovers')
            
            # Create GameScore object
            game_score = GameScore(
                # Game Identification
                game_id=event['id'],
                date=datetime.fromisoformat(event['date'].replace('Z', '+00:00')),
                week=event.get('week', {}).get('number', 0),
                season=event.get('season', {}).get('year', self.settings.season),
                season_type=event.get('season', {}).get('type', self.settings.season_type),
                
                # Teams
                home_team=home_team,
                away_team=away_team,
                
                # Scores
                home_score=home_score,
                away_score=away_score,
                
                # Game Status
                status=status,
                status_detail=status_detail,
                is_completed=is_completed,
                
                # Venue
                venue_name=venue_name,
                venue_city=venue_city,
                venue_state=venue_state,
                venue_capacity=venue_capacity,
                attendance=attendance,
                
                # Weather
                temperature=temperature,
                weather_description=weather_description,
                wind_speed=wind_speed,
                
                # Broadcast
                tv_network=tv_network,
                
                # Odds
                home_team_odds=home_team_odds,
                away_team_odds=away_team_odds,
                over_under=over_under,
                
                # Statistics
                home_total_yards=home_total_yards,
                away_total_yards=away_total_yards,
                home_turnovers=home_turnovers,
                away_turnovers=away_turnovers,
                
                # Quarter Scores
                **quarter_scores
            )
            
            return game_score
            
        except Exception as e:
            self.logger.error(f"Error parsing game event: {e}")
            return None
    
    def _parse_team_data(self, team_data: Dict[str, Any]) -> Team:
        """Extract team information from ESPN's team data structure.
        
        ESPN provides comprehensive team metadata including colors and logos.
        We map this to our clean Team model.
        
        Args:
            team_data: ESPN team data dictionary
            
        Returns:
            Team object with all available information
        """
        return Team(
            id=team_data['id'],  # ESPN's unique team identifier
            name=team_data['name'],  # Short name (e.g., "Cowboys")
            display_name=team_data['displayName'],  # Full name (e.g., "Dallas Cowboys")
            abbreviation=team_data['abbreviation'],  # 3-letter code (e.g., "DAL")
            location=team_data.get('location', ''),  # City (e.g., "Dallas")
            color=team_data.get('color'),  # Primary team color (hex)
            alternate_color=team_data.get('alternateColor'),  # Secondary color
            logo_url=team_data.get('logo')  # URL to team logo image
        )
    
    def _parse_quarter_scores(self, linescore: List[Dict], home_competitor: Dict, away_competitor: Dict) -> Dict[str, Optional[int]]:
        """Extract quarter-by-quarter scoring details.
        
        ESPN provides detailed scoring progression through each quarter.
        This is valuable for understanding how games developed.
        
        Args:
            linescore: ESPN's linescore array (may be empty)
            home_competitor: Home team competitor data
            away_competitor: Away team competitor data
            
        Returns:
            Dictionary with quarter scores for both teams
        """
        # Initialize all quarter scores to None
        quarter_scores = {
            'home_score_q1': None, 'home_score_q2': None, 'home_score_q3': None, 'home_score_q4': None, 'home_score_ot': None,
            'away_score_q1': None, 'away_score_q2': None, 'away_score_q3': None, 'away_score_q4': None, 'away_score_ot': None
        }
        
        # Return empty scores if no linescore data available
        if not linescore:
            return quarter_scores
        
        # ESPN provides quarter scores in competitor linescores arrays
        home_linescores = home_competitor.get('linescores', [])
        away_linescores = away_competitor.get('linescores', [])
        
        # Process each quarter/period
        for i, (home_line, away_line) in enumerate(zip(home_linescores, away_linescores)):
            if i < 4:  # Regular quarters (Q1-Q4)
                quarter_scores[f'home_score_q{i+1}'] = int(home_line.get('value', 0))
                quarter_scores[f'away_score_q{i+1}'] = int(away_line.get('value', 0))
            else:  # Overtime periods (rare, but possible)
                quarter_scores['home_score_ot'] = int(home_line.get('value', 0))
                quarter_scores['away_score_ot'] = int(away_line.get('value', 0))
        
        return quarter_scores
    
    def _get_stat_value(self, stats: List[Dict], stat_name: str) -> Optional[int]:
        """Safely extract a specific statistic from ESPN's stats array.
        
        ESPN provides team statistics as an array of name-value pairs.
        This helper method finds and safely converts specific stats.
        
        Args:
            stats: Array of ESPN stat objects
            stat_name: Name of the statistic to find (e.g., 'totalYards')
            
        Returns:
            Integer value of the stat, or None if not found/invalid
        """
        for stat in stats:
            if stat.get('name') == stat_name:
                try:
                    # ESPN provides stats as strings, convert to int safely
                    return int(float(stat.get('displayValue', 0)))
                except (ValueError, TypeError):
                    # Return None if conversion fails
                    return None
        return None  # Stat not found in the array


# Data Export Classes - Converting Data to Useful Formats
# =======================================================
# These classes handle converting our structured data into files
# that can be used by other tools, analytics platforms, or humans.

class DataExporter:
    """Handles exporting NFL game data to various file formats.
    
    Supports JSON (for APIs), CSV (for analysis), and Excel (for humans).
    Each format is optimized for its intended use case.
    """
    
    def __init__(self, output_dir: str):
        """Initialize exporter and create output directory.
        
        Args:
            output_dir: Directory path where files will be saved
        """
        self.output_dir = Path(output_dir)
        # Create directory if it doesn't exist
        self.output_dir.mkdir(exist_ok=True)
    
    def export_json(self, data: WeeklyScores) -> str:
        """Export data to JSON format for API consumption or data interchange.
        
        JSON preserves the full data structure and is perfect for:
        - Loading into other applications
        - API responses
        - Data archiving
        
        Args:
            data: WeeklyScores object to export
            
        Returns:
            Path to the created JSON file
        """
        # Create timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if data.week > 0:
            filename = f"nfl_scores_week{data.week}_{timestamp}.json"
        else:
            filename = f"nfl_scores_recent_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        # Write JSON with pretty formatting
        with open(filepath, 'w') as f:
            # Pydantic's model_dump() converts to JSON-serializable dict
            json.dump(data.model_dump(mode='json'), f, indent=2, default=str)
        
        return str(filepath)
    
    def export_csv(self, data: WeeklyScores) -> str:
        """Export to CSV format"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if data.week > 0:
            filename = f"nfl_scores_week{data.week}_{timestamp}.csv"
        else:
            filename = f"nfl_scores_recent_{timestamp}.csv"
        
        filepath = self.output_dir / filename
        
        # Flatten game data for CSV
        rows = []
        for game in data.games:
            row = {
                'game_id': game.game_id,
                'date': game.date.isoformat(),
                'week': game.week,
                'season': game.season,
                
                # Teams and Scores
                'away_team': game.away_team.display_name,
                'away_abbreviation': game.away_team.abbreviation,
                'away_record': game.away_team.record,
                'away_score': game.away_score,
                'home_team': game.home_team.display_name,
                'home_abbreviation': game.home_team.abbreviation,
                'home_record': game.home_team.record,
                'home_score': game.home_score,
                
                # Game Result
                'winning_team': game.winning_team,
                'total_points': game.total_points,
                'point_difference': game.point_difference,
                'is_overtime': game.is_overtime,
                
                # Status
                'status': game.status,
                'is_completed': game.is_completed,
                
                # Venue
                'venue_name': game.venue_name,
                'venue_city': game.venue_city,
                'venue_state': game.venue_state,
                'attendance': game.attendance,
                
                # Weather
                'temperature': game.temperature,
                'weather_description': game.weather_description,
                
                # Broadcast
                'tv_network': game.tv_network,
                
                # Quarter Scores
                'home_q1': game.home_score_q1,
                'home_q2': game.home_score_q2,
                'home_q3': game.home_score_q3,
                'home_q4': game.home_score_q4,
                'home_ot': game.home_score_ot,
                'away_q1': game.away_score_q1,
                'away_q2': game.away_score_q2,
                'away_q3': game.away_score_q3,
                'away_q4': game.away_score_q4,
                'away_ot': game.away_score_ot,
                
                # Statistics
                'home_total_yards': game.home_total_yards,
                'away_total_yards': game.away_total_yards,
                'home_turnovers': game.home_turnovers,
                'away_turnovers': game.away_turnovers,
                
                'updated_at': game.updated_at.isoformat()
            }
            rows.append(row)
        
        df = pd.DataFrame(rows)
        df.to_csv(filepath, index=False)
        
        return str(filepath)
    
    def export_excel(self, data: WeeklyScores) -> str:
        """Export to Excel format with multiple sheets"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if data.week > 0:
            filename = f"nfl_scores_week{data.week}_{timestamp}.xlsx"
        else:
            filename = f"nfl_scores_recent_{timestamp}.xlsx"
        
        filepath = self.output_dir / filename
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # Main scores sheet
            scores_data = []
            for game in data.games:
                scores_data.append({
                    'Date': game.date.strftime('%Y-%m-%d %H:%M'),
                    'Week': game.week,
                    'Away Team': f"{game.away_team.display_name} ({game.away_team.record or 'N/A'})",
                    'Away Score': game.away_score,
                    'Home Team': f"{game.home_team.display_name} ({game.home_team.record or 'N/A'})",
                    'Home Score': game.home_score,
                    'Winner': game.winning_team,
                    'Total Points': game.total_points,
                    'Point Diff': game.point_difference,
                    'OT': 'Yes' if game.is_overtime else 'No',
                    'Venue': game.venue_name,
                    'City': game.venue_city,
                    'Attendance': game.attendance,
                    'TV': game.tv_network,
                    'Status': 'Final' if game.is_completed else game.status_detail
                })
            
            df_scores = pd.DataFrame(scores_data)
            df_scores.to_excel(writer, sheet_name='Game Scores', index=False)
            
            # Quarter by quarter sheet
            if any(game.home_score_q1 is not None for game in data.games):
                quarter_data = []
                for game in data.games:
                    if game.home_score_q1 is not None:
                        quarter_data.append({
                            'Game': f"{game.away_team.abbreviation} @ {game.home_team.abbreviation}",
                            'Date': game.date.strftime('%Y-%m-%d'),
                            'Away Team': game.away_team.abbreviation,
                            'Away Q1': game.away_score_q1,
                            'Away Q2': game.away_score_q2,
                            'Away Q3': game.away_score_q3,
                            'Away Q4': game.away_score_q4,
                            'Away OT': game.away_score_ot if game.away_score_ot else '',
                            'Away Final': game.away_score,
                            'Home Team': game.home_team.abbreviation,
                            'Home Q1': game.home_score_q1,
                            'Home Q2': game.home_score_q2,
                            'Home Q3': game.home_score_q3,
                            'Home Q4': game.home_score_q4,
                            'Home OT': game.home_score_ot if game.home_score_ot else '',
                            'Home Final': game.home_score,
                        })
                
                if quarter_data:
                    df_quarters = pd.DataFrame(quarter_data)
                    df_quarters.to_excel(writer, sheet_name='Quarter Scores', index=False)
            
            # Summary statistics sheet
            completed_games = [g for g in data.games if g.is_completed]
            if completed_games:
                summary_stats = {
                    'Total Games': data.total_games,
                    'Completed Games': data.completed_games,
                    'Average Total Points': sum(g.total_points for g in completed_games) / len(completed_games),
                    'Highest Scoring Game': max(g.total_points for g in completed_games),
                    'Lowest Scoring Game': min(g.total_points for g in completed_games),
                    'Average Point Difference': sum(g.point_difference for g in completed_games) / len(completed_games),
                    'Largest Margin of Victory': max(g.point_difference for g in completed_games),
                    'Overtime Games': sum(1 for g in completed_games if g.is_overtime),
                    'Home Team Wins': sum(1 for g in completed_games if g.home_score > g.away_score),
                    'Away Team Wins': sum(1 for g in completed_games if g.away_score > g.home_score),
                    'Ties': sum(1 for g in completed_games if g.home_score == g.away_score)
                }
                
                df_summary = pd.DataFrame(list(summary_stats.items()), columns=['Statistic', 'Value'])
                df_summary.to_excel(writer, sheet_name='Summary', index=False)
        
        return str(filepath)
    
    def export_condensed_excel(self, data: WeeklyScores) -> str:
        """Export to condensed Excel format with one row per team"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if data.week > 0:
            filename = f"nfl_scores_condensed_week{data.week}_{timestamp}.xlsx"
        else:
            filename = f"nfl_scores_condensed_recent_{timestamp}.xlsx"
        
        filepath = self.output_dir / filename
        
        # Load bye weeks and ADP data to get all teams
        bye_weeks_path = Path(self.output_dir).parent / "bye_weeks.csv"
        adp_path = Path(self.output_dir).parent / "adp.csv"
        
        # Create abbreviation to team name mapping from played games
        abbrev_to_name = {}
        teams_played = set()
        
        # Create team-centric data structure from actual games
        team_data = []
        
        for game in data.games:
            if not game.is_completed:
                continue  # Only include completed games
                
            # Build mapping from abbreviation to team name
            abbrev_to_name[game.home_team.abbreviation] = game.home_team.name
            abbrev_to_name[game.away_team.abbreviation] = game.away_team.name
            
            # Track which teams played
            teams_played.add(game.home_team.abbreviation)
            teams_played.add(game.away_team.abbreviation)
                
            # Add home team row
            team_data.append({
                'Team': game.home_team.name,
                'Opponent': game.away_team.name,
                'Points Scored': game.home_score,
                'Points Allowed': game.away_score
            })
            
            # Add away team row  
            team_data.append({
                'Team': game.away_team.name,
                'Opponent': game.home_team.name,  # Remove @ symbol for cleaner display
                'Points Scored': game.away_score,
                'Points Allowed': game.home_score
            })
        
        # Add bye week teams if we have a specific week and the bye_weeks.csv file exists
        if data.week > 0 and bye_weeks_path.exists():
            try:
                bye_weeks_df = pd.read_csv(bye_weeks_path)
                bye_teams = bye_weeks_df[bye_weeks_df['ByeWeek'] == data.week]['Team'].tolist()
                
                # Build complete team name mapping
                common_names = {
                    'ARI': 'Cardinals', 'ATL': 'Falcons', 'BAL': 'Ravens', 'BUF': 'Bills',
                    'CAR': 'Panthers', 'CHI': 'Bears', 'CIN': 'Bengals', 'CLE': 'Browns',
                    'DAL': 'Cowboys', 'DEN': 'Broncos', 'DET': 'Lions', 'HOU': 'Texans',
                    'IND': 'Colts', 'JAX': 'Jaguars', 'KC': 'Chiefs', 'MIA': 'Dolphins',
                    'MIN': 'Vikings', 'PHI': 'Eagles', 'PIT': 'Steelers', 'SEA': 'Seahawks',
                    'TEN': 'Titans', 'SF': '49ers', 'GB': 'Packers', 'NE': 'Patriots',
                    'NO': 'Saints', 'TB': 'Buccaneers', 'LV': 'Raiders', 'LAC': 'Chargers',
                    'LAR': 'Rams', 'WAS': 'Commanders', 'NYG': 'Giants', 'NYJ': 'Jets'
                }
                
                # Add missing teams to abbrev_to_name mapping
                for abbrev, name in common_names.items():
                    if abbrev not in abbrev_to_name:
                        abbrev_to_name[abbrev] = name
                
                # Add bye week teams that didn't play
                for bye_team_abbrev in bye_teams:
                    if bye_team_abbrev not in teams_played and bye_team_abbrev in abbrev_to_name:
                        team_name = abbrev_to_name[bye_team_abbrev]
                        team_data.append({
                            'Team': team_name,
                            'Opponent': 'BYE',
                            'Points Scored': 'BYE',
                            'Points Allowed': 'BYE'
                        })
                        
            except Exception as e:
                # If bye week processing fails, continue without bye teams
                pass
        
        # Sort by team name alphabetically (49ers will naturally appear first due to numeric sorting)
        team_data.sort(key=lambda x: x['Team'])
        
        # Create DataFrame and export to Excel
        df = pd.DataFrame(team_data)
        df.to_excel(filepath, index=False, engine='openpyxl')
        
        return str(filepath)


# Main Application Orchestrator
# =============================
# This is the main class that coordinates all the components:
# API client, data parsing, and file export.

class NFLScoresCollector:
    """Main application class that orchestrates the entire data collection process.
    
    This class:
    1. Manages the ESPN API client
    2. Coordinates data collection based on settings
    3. Handles data export to multiple formats
    4. Provides user feedback and logging
    """
    
    def __init__(self, settings: Settings):
        """Initialize the collector with configuration settings.
        
        Args:
            settings: Configuration object with all parameters
        """
        self.settings = settings
        self.exporter = DataExporter(settings.output_directory)
        self.logger = logging.getLogger(__name__)
    
    async def collect_scores(self) -> WeeklyScores:
        """Main data collection method - fetches and processes NFL scores.
        
        This method:
        1. Creates an ESPN API client
        2. Fetches game data based on configuration
        3. Processes the data into our structured format
        4. Returns a complete WeeklyScores object
        
        Returns:
            WeeklyScores object containing all collected game data
        """
        # Create API client with our settings
        client = ESPNScoresClient(self.settings)
        
        # Use async context manager for proper connection handling
        async with client.session():
            if self.settings.current_week:
                # Fetch specific week data
                self.logger.info(f"Collecting scores for week {self.settings.current_week}")
                games = await client.get_week_scores(self.settings.current_week)
                week = self.settings.current_week
            else:
                # Fetch recent games from multiple weeks
                self.logger.info("Collecting recent completed games")
                games = await client.get_completed_games_recent()
                # Use first game's week, or 0 if no games found
                week = games[0].week if games else 0
        
        # Count completed vs in-progress games
        completed_games = [g for g in games if g.is_completed]
        
        # Create structured result object
        weekly_scores = WeeklyScores(
            week=week,
            season=self.settings.season,
            season_type=self.settings.season_type,
            total_games=len(games),
            completed_games=len(completed_games),
            games=games
        )
        
        self.logger.info(f"Collected {len(games)} games ({len(completed_games)} completed)")
        return weekly_scores
    
    def export_data(self, scores_data: WeeklyScores) -> List[str]:
        """Export scores data in multiple formats"""
        output_files = []
        
        # Export JSON
        if self.settings.create_json:
            json_file = self.exporter.export_json(scores_data)
            output_files.append(json_file)
        
        # Export CSV
        if self.settings.create_csv:
            csv_file = self.exporter.export_csv(scores_data)
            output_files.append(csv_file)
        
        # Export Excel
        if self.settings.create_excel:
            excel_file = self.exporter.export_excel(scores_data)
            output_files.append(excel_file)

        # Export Condensed Excel
        if self.settings.create_condensed_excel:
            condensed_file = self.exporter.export_condensed_excel(scores_data)
            output_files.append(condensed_file)
        
        return output_files
    
    def print_summary(self, scores_data: WeeklyScores):
        """Print summary of collected scores"""
        print(f"\n[SUCCESS] NFL Team Scores Collection Complete!")
        print(f"Season: {scores_data.season}")
        if scores_data.week > 0:
            print(f"Week: {scores_data.week}")
        else:
            print(f"Recent games from multiple weeks")
        
        print(f"Total Games: {scores_data.total_games}")
        print(f"Completed Games: {scores_data.completed_games}")
        
        if scores_data.completed_games > 0:
            completed_games = [g for g in scores_data.games if g.is_completed]
            
            # Show some interesting stats
            total_points = [g.total_points for g in completed_games]
            avg_points = sum(total_points) / len(total_points)
            highest_game = max(completed_games, key=lambda x: x.total_points)
            
            print(f"\nScore Statistics:")
            print(f"   Average Total Points: {avg_points:.1f}")
            print(f"   Highest Scoring Game: {highest_game.away_team.abbreviation} {highest_game.away_score} - {highest_game.home_score} {highest_game.home_team.abbreviation} ({highest_game.total_points} total)")
            
            # Show recent results
            recent_games = sorted(completed_games, key=lambda x: x.date, reverse=True)[:5]
            print(f"\nRecent Final Scores:")
            for game in recent_games:
                winner_indicator = "HOME" if game.home_score > game.away_score else "AWAY"
                print(f"   {winner_indicator} {game.away_team.abbreviation} {game.away_score} - {game.home_score} {game.home_team.abbreviation} ({game.date.strftime('%m/%d')})")


async def main():
    """Main application entry point and orchestrator.
    
    This function:
    1. Loads configuration from environment variables
    2. Sets up logging for debugging and monitoring
    3. Runs the complete data collection process
    4. Handles errors gracefully and provides user feedback
    """
    # Load configuration from .env file and environment variables
    settings = Settings()
    
    # Configure logging for both file output and console feedback
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting NFL scores collection")
        
        # Create main collector and run data collection
        collector = NFLScoresCollector(settings)
        scores_data = await collector.collect_scores()
        
        # Export to all supported formats
        output_files = collector.export_data(scores_data)
        
        # Show user-friendly summary
        collector.print_summary(scores_data)
        
        # List all created files
        print(f"\nOutput Files:")
        for file in output_files:
            print(f"   {file}")
        
        logger.info("Data collection completed successfully")
        
    except Exception as e:
        # Log detailed error information for debugging
        logger.error(f"Application error: {e}", exc_info=True)
        # Show simple error message to user
        print(f"\n[ERROR] Error: {e}")
        raise  # Re-raise to maintain exit code


# Application Entry Point
# =====================
# This is the standard Python entry point pattern.
# When the script is run directly (not imported), it starts the main async function.

if __name__ == "__main__":
    # Run the async main function using asyncio
    # This handles all the async event loop management for us
    asyncio.run(main())