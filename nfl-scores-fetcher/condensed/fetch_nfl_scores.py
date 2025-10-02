#!/usr/bin/env python3
"""
NFL Scores Fetcher - Standalone Version
========================================

Retrieves NFL game scores using ESPN's free API and exports to Excel format.

This is a simplified, standalone version designed for easy sharing and use.
All configuration is done via constants at the top of this file.

Author: Kai Mizuno
Last Updated: October 2025

Requirements:
    Python 3.12+
    pip install httpx pydantic tenacity pandas openpyxl

Usage:
    1. Edit the CONFIGURATION section below to set your preferences
    2. Run: python fetch_nfl_scores.py
    3. Find Excel files in the ./data/ directory
"""

import asyncio
import sys
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional

import httpx
import pandas as pd
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_random_exponential


# =============================================================================
# CONFIGURATION - Edit these values to customize your data collection
# =============================================================================

# NFL Season Settings
SEASON = 2025                    # NFL season year
SEASON_TYPE = 2                  # 1=preseason, 2=regular, 3=postseason, 4=off-season
CURRENT_WEEK = 4                 # NFL week number (1-18), or None for recent games
ONLY_COMPLETED_GAMES = False     # True = only final scores, False = include live/upcoming

# Output Settings
OUTPUT_DIRECTORY = "./data"      # Where to save Excel files
CREATE_NORMAL_EXCEL = True       # Create detailed Excel with multiple sheets
CREATE_CONDENSED_EXCEL = True    # Create condensed team-comparison Excel

# API Settings (usually don't need to change these)
REQUEST_TIMEOUT = 30             # Seconds to wait for API response
RATE_LIMIT_DELAY = 0.2          # Delay between requests (seconds)

# =============================================================================
# DATA MODELS - Pydantic models for data validation
# =============================================================================

class Team(BaseModel):
    """Represents an NFL team"""
    id: str
    name: str
    display_name: str
    abbreviation: str
    location: str
    color: Optional[str] = None
    alternate_color: Optional[str] = None
    logo_url: Optional[str] = None
    record: Optional[str] = None
    score: Optional[int] = None


class GameScore(BaseModel):
    """Comprehensive NFL game data model"""

    # Core Game Identification
    game_id: str
    date: datetime
    week: int
    season: int
    season_type: int

    # Team Information
    home_team: Team
    away_team: Team

    # Final Scores
    home_score: int
    away_score: int

    # Game Status
    status: str
    status_detail: str
    is_completed: bool
    is_in_progress: bool = Field(default=False)

    # Venue and Location
    venue_name: Optional[str] = None
    venue_city: Optional[str] = None
    venue_state: Optional[str] = None
    venue_capacity: Optional[int] = None
    attendance: Optional[int] = None

    # Weather Conditions
    temperature: Optional[int] = None
    weather_description: Optional[str] = None
    wind_speed: Optional[int] = None

    # Broadcast Information
    tv_network: Optional[str] = None

    # Betting Information
    home_team_odds: Optional[float] = None
    away_team_odds: Optional[float] = None
    over_under: Optional[float] = None

    # Game Statistics
    home_total_yards: Optional[int] = None
    away_total_yards: Optional[int] = None
    home_turnovers: Optional[int] = None
    away_turnovers: Optional[int] = None

    # Quarter-by-Quarter Scoring
    home_score_q1: Optional[int] = None
    home_score_q2: Optional[int] = None
    home_score_q3: Optional[int] = None
    home_score_q4: Optional[int] = None
    home_score_ot: Optional[int] = None
    away_score_q1: Optional[int] = None
    away_score_q2: Optional[int] = None
    away_score_q3: Optional[int] = None
    away_score_q4: Optional[int] = None
    away_score_ot: Optional[int] = None

    # Calculated Fields
    total_points: int = Field(default=0)
    point_difference: int = Field(default=0)
    winning_team: str = Field(default="")
    is_overtime: bool = Field(default=False)

    # Record Keeping
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def model_post_init(self, __context: Any) -> None:
        """Calculate derived fields after initialization"""
        self.total_points = self.home_score + self.away_score
        self.point_difference = abs(self.home_score - self.away_score)

        if self.home_score > self.away_score:
            self.winning_team = self.home_team.abbreviation
        elif self.away_score > self.home_score:
            self.winning_team = self.away_team.abbreviation
        else:
            self.winning_team = "TIE"

        self.is_overtime = any([
            self.home_score_ot and self.home_score_ot > 0,
            self.away_score_ot and self.away_score_ot > 0
        ])


class WeeklyScores(BaseModel):
    """Container for a collection of NFL games"""
    week: int
    season: int
    season_type: int
    total_games: int
    completed_games: int
    games: List[GameScore]
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# =============================================================================
# CONSTANTS
# =============================================================================

ESPN_NFL_BASE_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl"
ESPN_USER_AGENT = "NFL-Scores-Collector/2.0"
STATUS_IN_PROGRESS = "STATUS_IN_PROGRESS"
STATUS_FINAL = "STATUS_FINAL"

NFL_TEAM_NAMES: Dict[str, str] = {
    'ARI': 'Cardinals', 'ATL': 'Falcons', 'BAL': 'Ravens', 'BUF': 'Bills',
    'CAR': 'Panthers', 'CHI': 'Bears', 'CIN': 'Bengals', 'CLE': 'Browns',
    'DAL': 'Cowboys', 'DEN': 'Broncos', 'DET': 'Lions', 'GB': 'Packers',
    'HOU': 'Texans', 'IND': 'Colts', 'JAX': 'Jaguars', 'KC': 'Chiefs',
    'LAC': 'Chargers', 'LAR': 'Rams', 'LV': 'Raiders', 'MIA': 'Dolphins',
    'MIN': 'Vikings', 'NE': 'Patriots', 'NO': 'Saints', 'NYG': 'Giants',
    'NYJ': 'Jets', 'PHI': 'Eagles', 'PIT': 'Steelers', 'SF': '49ers',
    'SEA': 'Seahawks', 'TB': 'Buccaneers', 'TEN': 'Titans', 'WSH': 'Commanders'
}


# =============================================================================
# NFL API CLIENT
# =============================================================================

class NFLAPIClient:
    """Async client for ESPN's NFL scoreboard API"""

    def __init__(self):
        self.base_url = ESPN_NFL_BASE_URL
        self.client: Optional[httpx.AsyncClient] = None

    @asynccontextmanager
    async def session(self):
        """Async context manager for HTTP client lifecycle"""
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(REQUEST_TIMEOUT),
            limits=httpx.Limits(max_keepalive_connections=20, max_connections=100),
            headers={'User-Agent': ESPN_USER_AGENT}
        )
        try:
            yield self
        finally:
            await self.client.aclose()

    @retry(
        wait=wait_random_exponential(min=1, max=30),
        stop=stop_after_attempt(3)
    )
    async def _make_request(self, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Core HTTP request method with error handling"""
        print(f"Making request to ESPN API...")

        await asyncio.sleep(RATE_LIMIT_DELAY)

        try:
            response = await self.client.get(url, params=params)

            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 30))
                print(f"Rate limited by ESPN, waiting {retry_after} seconds...")
                await asyncio.sleep(retry_after)
                raise Exception(f"Rate limited, retry after {retry_after} seconds")

            if response.status_code >= 500:
                raise Exception(f"ESPN server error: {response.status_code}")

            if response.status_code >= 400:
                raise Exception(f"ESPN API error: {response.status_code}")

            response.raise_for_status()
            data = response.json()
            print("Request successful")

            return data

        except httpx.RequestError as e:
            print(f"Network error: {e}")
            raise Exception(f"Network error: {e}")
        except httpx.HTTPStatusError as e:
            print(f"HTTP error {e.response.status_code}: {e}")
            raise Exception(f"HTTP {e.response.status_code}: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    async def get_week_scores(self, week: int) -> List[GameScore]:
        """Fetch scores for a specific NFL week"""
        url = f"{self.base_url}/scoreboard"
        params = {
            "seasontype": SEASON_TYPE,
            "week": week,
            "dates": SEASON
        }
        data = await self._make_request(url, params=params)
        return self._parse_scoreboard_data(data)

    async def get_completed_games_recent(self, days_back: int = 7) -> List[GameScore]:
        """Fetch completed games from the last N days"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)

            url = f"{self.base_url}/scoreboard"
            params = {
                "dates": f"{start_date.strftime('%Y%m%d')}-{end_date.strftime('%Y%m%d')}",
                "limit": 1000
            }

            data = await self._make_request(url, params=params)
            games = self._parse_scoreboard_data(data)

            return [game for game in games if game.is_completed]
        except Exception as e:
            print(f"Error fetching recent completed games: {e}")
            return []

    def _parse_scoreboard_data(self, data: Dict[str, Any]) -> List[GameScore]:
        """Parse ESPN's scoreboard API response into GameScore objects"""
        games = []
        events = data.get('events', [])
        print(f"Processing {len(events)} games")

        for event in events:
            try:
                if not isinstance(event, dict):
                    print(f"Warning: Event is not a dictionary")
                    continue

                game_score = self._parse_game_event(event)
                if game_score:
                    if not ONLY_COMPLETED_GAMES or game_score.is_completed:
                        games.append(game_score)
            except Exception as e:
                event_id = event.get('id', 'unknown') if isinstance(event, dict) else 'non-dict'
                print(f"Warning: Failed to parse game {event_id}: {e}")

        print(f"Successfully parsed {len(games)} games")
        return games

    def _parse_game_event(self, event: Dict[str, Any]) -> Optional[GameScore]:
        """Parse a single game from ESPN's JSON structure"""
        try:
            game_id = event.get('id', '')
            date_str = event.get('date', '')

            if not game_id or not date_str:
                return None

            game_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))

            season_info = event.get('season', {})
            week = season_info.get('week', 0)
            season_year = season_info.get('year', SEASON)
            season_type = season_info.get('type', SEASON_TYPE)

            competitions = event.get('competitions', [])
            if not competitions:
                return None

            competition = competitions[0]

            status = competition.get('status', {})
            if not isinstance(status, dict):
                return None
            status_type = status.get('type', {})
            if not isinstance(status_type, dict):
                return None
            game_status = status_type.get('name', 'UNKNOWN')
            status_detail = status_type.get('detail', 'Unknown Status')
            is_completed = status_type.get('completed', False)
            is_in_progress = status_type.get('name', '').upper() in [STATUS_IN_PROGRESS, 'STATUS_HALFTIME', 'STATUS_END_PERIOD']

            competitors = competition.get('competitors', [])
            if len(competitors) != 2:
                return None

            home_team_data = None
            away_team_data = None

            for competitor in competitors:
                if not isinstance(competitor, dict):
                    return None
                home_away = competitor.get('homeAway')
                if home_away == 'home':
                    home_team_data = competitor
                else:
                    away_team_data = competitor

            if not home_team_data or not away_team_data:
                return None

            home_team_dict = home_team_data.get('team', {})
            home_team = self._parse_team_data(home_team_dict)

            away_team_dict = away_team_data.get('team', {})
            away_team = self._parse_team_data(away_team_dict)

            home_score = int(home_team_data.get('score', 0))
            away_score = int(away_team_data.get('score', 0))

            venue = competition.get('venue', {})
            venue_name = venue.get('fullName')
            venue_address = venue.get('address', {})
            venue_city = venue_address.get('city')
            venue_state = venue_address.get('state')
            venue_capacity = venue.get('capacity')

            attendance = competition.get('attendance')

            weather = competition.get('weather', {})
            temperature = weather.get('temperature')
            weather_desc = weather.get('conditionId')
            wind_speed = weather.get('highTemperature')

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

            odds = competition.get('odds', [])
            home_odds = None
            away_odds = None
            over_under = None

            if odds:
                odd = odds[0]
                home_odds = odd.get('homeTeamOdds', {}).get('moneyLine')
                away_odds = odd.get('awayTeamOdds', {}).get('moneyLine')
                over_under = odd.get('overUnder')

            home_stats = home_team_data.get('statistics', [])
            away_stats = away_team_data.get('statistics', [])

            home_total_yards = self._extract_stat(home_stats, 'totalYards')
            away_total_yards = self._extract_stat(away_stats, 'totalYards')
            home_turnovers = self._extract_stat(home_stats, 'turnovers')
            away_turnovers = self._extract_stat(away_stats, 'turnovers')

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
            print(f"Error parsing game event: {e}")
            return None

    def _parse_team_data(self, team_data: Dict[str, Any]) -> Team:
        """Parse team information from ESPN API format"""
        if not isinstance(team_data, dict):
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
        """Extract a specific statistic from ESPN's stats format"""
        for stat in stats_list:
            if stat.get('name') == stat_name:
                try:
                    return int(stat.get('displayValue', 0))
                except (ValueError, TypeError):
                    return None
        return None

    def _get_quarter_score(self, line_scores: List[Dict], quarter_index: int) -> Optional[int]:
        """Extract score for a specific quarter"""
        if quarter_index < len(line_scores):
            try:
                return int(line_scores[quarter_index].get('value', 0))
            except (ValueError, TypeError):
                return None
        return None


# =============================================================================
# DATA EXPORTER
# =============================================================================

class ScoresDataExporter:
    """Handles exporting NFL game scores to Excel format"""

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)

    def _get_timestamp(self) -> str:
        """Generate timestamp for filenames"""
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    def _game_to_dict(self, game: GameScore) -> dict:
        """Convert GameScore object to dictionary"""
        return {
            'game_id': game.game_id,
            'date': game.date.isoformat(),
            'week': game.week,
            'season': game.season,
            'season_type': game.season_type,
            'home_team_id': game.home_team.id,
            'home_team_name': game.home_team.display_name,
            'home_team_abbr': game.home_team.abbreviation,
            'home_team_record': game.home_team.record,
            'away_team_id': game.away_team.id,
            'away_team_name': game.away_team.display_name,
            'away_team_abbr': game.away_team.abbreviation,
            'away_team_record': game.away_team.record,
            'home_score': game.home_score,
            'away_score': game.away_score,
            'total_points': game.total_points,
            'point_difference': game.point_difference,
            'winning_team': game.winning_team,
            'status': game.status,
            'status_detail': game.status_detail,
            'is_completed': game.is_completed,
            'is_overtime': game.is_overtime,
            'venue_name': game.venue_name,
            'venue_city': game.venue_city,
            'venue_state': game.venue_state,
            'venue_capacity': game.venue_capacity,
            'attendance': game.attendance,
            'temperature': game.temperature,
            'weather_description': game.weather_description,
            'wind_speed': game.wind_speed,
            'tv_network': game.tv_network,
            'home_team_odds': game.home_team_odds,
            'away_team_odds': game.away_team_odds,
            'over_under': game.over_under,
            'home_total_yards': game.home_total_yards,
            'away_total_yards': game.away_total_yards,
            'home_turnovers': game.home_turnovers,
            'away_turnovers': game.away_turnovers,
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
            'updated_at': game.updated_at.isoformat()
        }

    async def export_excel(self, weekly_scores: WeeklyScores) -> Optional[str]:
        """Export weekly scores to Excel format with multiple sheets"""
        try:
            df = pd.DataFrame([self._game_to_dict(game) for game in weekly_scores.games])

            week_suffix = f"_week{weekly_scores.week}" if weekly_scores.week > 0 else "_recent"
            filename = f"nfl_scores{week_suffix}_{self._get_timestamp()}.xlsx"
            filepath = self.output_dir / filename

            with pd.ExcelWriter(str(filepath), engine='openpyxl') as writer:
                # Main games sheet
                df.to_excel(writer, sheet_name='All Games', index=False)

                # Completed games sheet
                if not df.empty and 'is_completed' in df.columns:
                    completed_df = df[df['is_completed'] == True].copy()
                    if not completed_df.empty:
                        completed_df.to_excel(writer, sheet_name='Completed Games', index=False)

                # Summary sheet
                self._create_summary_sheet(writer, weekly_scores, df)

                # High-scoring games sheet
                if not df.empty and 'total_points' in df.columns:
                    high_scoring = df[df['total_points'] >= 50].copy()
                    if not high_scoring.empty:
                        high_scoring = high_scoring.sort_values('total_points', ascending=False)
                        high_scoring.to_excel(writer, sheet_name='High Scoring Games', index=False)

            print(f"Created normal Excel: {filename}")
            return str(filepath)
        except Exception as e:
            print(f"Error exporting Excel: {e}")
            return None

    async def export_condensed_excel(self, weekly_scores: WeeklyScores) -> Optional[str]:
        """Export condensed team-comparison Excel"""
        try:
            team_data = []

            for game in weekly_scores.games:
                # Show scheduled games with 'TBD' instead of skipping them
                if game.is_completed:
                    home_points = game.home_score
                    away_points = game.away_score
                else:
                    home_points = 'TBD'
                    away_points = 'TBD'

                team_data.append({
                    'Team': game.home_team.name,
                    'Opponent': game.away_team.name,
                    'Points Scored': home_points,
                    'Points Allowed': away_points
                })

                team_data.append({
                    'Team': game.away_team.name,
                    'Opponent': game.home_team.name,
                    'Points Scored': away_points,
                    'Points Allowed': home_points
                })

            team_data.sort(key=lambda x: x['Team'])
            df = pd.DataFrame(team_data)

            week_suffix = f"_week{weekly_scores.week}" if weekly_scores.week > 0 else "_recent"
            filename = f"nfl_scores_condensed{week_suffix}_{self._get_timestamp()}.xlsx"
            filepath = self.output_dir / filename

            df.to_excel(str(filepath), index=False, engine='openpyxl')

            print(f"Created condensed Excel: {filename}")
            return str(filepath)
        except Exception as e:
            print(f"Error exporting condensed Excel: {e}")
            return None

    def _create_summary_sheet(self, writer: pd.ExcelWriter, weekly_scores: WeeklyScores, df: pd.DataFrame) -> None:
        """Create a summary statistics sheet"""
        summary_data = {
            'Metric': [
                'Total Games',
                'Completed Games',
                'In Progress Games',
                'Average Total Points',
                'Highest Scoring Game',
                'Lowest Scoring Game',
                'Average Point Difference',
                'Overtime Games',
                'Games with 40+ Points',
                'Games with 60+ Points'
            ],
            'Value': [
                weekly_scores.total_games,
                weekly_scores.completed_games,
                weekly_scores.total_games - weekly_scores.completed_games,
                f"{df['total_points'].mean():.1f}" if not df.empty and 'total_points' in df.columns else 0,
                f"{df['total_points'].max()}" if not df.empty and 'total_points' in df.columns else 0,
                f"{df['total_points'].min()}" if not df.empty and 'total_points' in df.columns else 0,
                f"{df['point_difference'].mean():.1f}" if not df.empty and 'point_difference' in df.columns else 0,
                len(df[df['is_overtime'] == True]) if not df.empty and 'is_overtime' in df.columns else 0,
                len(df[df['total_points'] >= 40]) if not df.empty and 'total_points' in df.columns else 0,
                len(df[df['total_points'] >= 60]) if not df.empty and 'total_points' in df.columns else 0
            ]
        }

        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)


# =============================================================================
# MAIN APPLICATION
# =============================================================================

class NFLScoresCollector:
    """Main collector class that coordinates score collection and export"""

    def __init__(self):
        script_dir = Path(__file__).parent
        output_path = script_dir / OUTPUT_DIRECTORY
        self.exporter = ScoresDataExporter(str(output_path))

    async def collect_scores(self) -> List[GameScore]:
        """Collect NFL scores based on settings"""
        client = NFLAPIClient()

        async with client.session():
            if CURRENT_WEEK is not None:
                print(f"Collecting scores for week {CURRENT_WEEK}")
                games = await client.get_week_scores(week=CURRENT_WEEK)
            else:
                print("Collecting recent game scores")
                games = await client.get_completed_games_recent(days_back=10)

            if ONLY_COMPLETED_GAMES:
                completed_games = [g for g in games if g.is_completed]
                print(f"Filtered to {len(completed_games)} completed games out of {len(games)} total")
                return completed_games

            return games

    async def export_data(self, games: List[GameScore]) -> List[str]:
        """Export game data based on configuration settings"""
        week = games[0].week if games else 0
        season = games[0].season if games else SEASON
        season_type = games[0].season_type if games else SEASON_TYPE
        completed_games = len([g for g in games if g.is_completed])

        weekly_scores = WeeklyScores(
            week=week,
            season=season,
            season_type=season_type,
            total_games=len(games),
            completed_games=completed_games,
            games=games
        )

        output_files = []

        if CREATE_NORMAL_EXCEL:
            file_path = await self.exporter.export_excel(weekly_scores)
            if file_path:
                output_files.append(file_path)

        if CREATE_CONDENSED_EXCEL:
            file_path = await self.exporter.export_condensed_excel(weekly_scores)
            if file_path:
                output_files.append(file_path)

        return output_files

    def print_summary(self, games: List[GameScore]) -> None:
        """Print summary of collected scores"""
        print(f"\n{'='*60}")
        print(f"NFL SCORES COLLECTION COMPLETE")
        print(f"{'='*60}")
        print(f"Season: {SEASON}")
        print(f"API Source: ESPN")
        print(f"Total Games: {len(games)}")

        if not games:
            print("No games found for the specified criteria.")
            return

        status_counts = {}
        for game in games:
            status = "Completed" if game.is_completed else "In Progress" if game.is_in_progress else "Scheduled"
            status_counts[status] = status_counts.get(status, 0) + 1

        print(f"\nGame Status Breakdown:")
        for status, count in status_counts.items():
            print(f"   {status}: {count} games")

        completed_games = [g for g in games if g.is_completed]
        if completed_games:
            print(f"\nRecent Completed Games:")
            for game in completed_games[-5:]:
                print(f"   {game.away_team.display_name} {game.away_score} - {game.home_score} {game.home_team.display_name}")


async def main():
    """Main application entry point"""
    try:
        print("="*60)
        print("NFL SCORES FETCHER - Standalone Version")
        print("="*60)
        print(f"Season: {SEASON}")
        print(f"Week: {CURRENT_WEEK if CURRENT_WEEK else 'Recent games'}")
        print(f"Output Directory: {OUTPUT_DIRECTORY}")
        print("="*60)

        # Validate settings
        if SEASON > 2025:
            print(f"WARNING: Season {SEASON} is in the future. ESPN may not have this data yet.")

        collector = NFLScoresCollector()

        print("\nFetching NFL scores from ESPN...")
        games = await collector.collect_scores()

        if not games:
            print("\nNo games found for the specified criteria.")
            return

        print("\nExporting data to Excel...")
        output_files = await collector.export_data(games)

        collector.print_summary(games)

        if output_files:
            print(f"\nOutput Files Created:")
            for file in output_files:
                print(f"   {file}")

        print(f"\n{'='*60}")
        print("SUCCESS! Check the data directory for your Excel files.")
        print(f"{'='*60}")

    except Exception as e:
        print(f"\n{'='*60}")
        print(f"ERROR: {e}")
        print(f"{'='*60}")

        if "api" in str(e).lower() or "network" in str(e).lower():
            print("\nTROUBLESHOOTING:")
            print("   1. Check your internet connection")
            print("   2. ESPN API may be temporarily unavailable")
            print("   3. Try again in a few minutes")

        sys.exit(1)


if __name__ == "__main__":
    # Check Python version
    if sys.version_info < (3, 12):
        print("ERROR: This script requires Python 3.12 or higher")
        print(f"You are running Python {sys.version_info.major}.{sys.version_info.minor}")
        sys.exit(1)

    asyncio.run(main())
