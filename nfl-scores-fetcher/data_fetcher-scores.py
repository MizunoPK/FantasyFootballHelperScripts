#!/usr/bin/env python3
"""
NFL Team Scores Data Collection Script - ESPN API (Modular)
============================================================

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
    NFL_SCORES_OUTPUT_DIRECTORY=./data python data_fetcher-scores.py
    
    # Using .env file (create .env in project root):
    # NFL_SCORES_SEASON=2025
    # NFL_SCORES_CURRENT_WEEK=15
    # NFL_SCORES_OUTPUT_DIRECTORY=./data/nfl_scores

Author: Kai Mizuno
Last Updated: September 2025

Dependencies:
    pip install httpx pydantic python-dotenv pandas openpyxl
"""

import asyncio
import logging
from pathlib import Path
from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

# Import our modular components
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

# Get the path to the .env file in the parent directory
ENV_FILE_PATH = Path(__file__).parent.parent / '.env'

# Import config.py settings
import shared_files.configs.nfl_scores_fetcher_config as config

from nfl_scores_models import GameScore, WeeklyScores, GameDataValidationError
from nfl_api_client import NFLAPIClient
from nfl_scores_exporter import ScoresDataExporter


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE_PATH),
        env_file_encoding='utf-8',
        env_prefix='NFL_SCORES_',
        extra='ignore'  # Ignore extra environment variables
    )
    
    # Data Parameters - use config.py values as defaults
    season: int = config.NFL_SCORES_SEASON
    season_type: int = config.NFL_SCORES_SEASON_TYPE
    current_week: Optional[int] = config.NFL_SCORES_CURRENT_WEEK  # Use config.py value
    only_completed_games: bool = config.NFL_SCORES_ONLY_COMPLETED_GAMES
    
    # Output Configuration - use config.py values as defaults
    output_directory: str = config.OUTPUT_DIRECTORY
    create_csv: bool = config.CREATE_CSV
    create_json: bool = config.CREATE_JSON
    create_excel: bool = config.CREATE_EXCEL
    create_condensed_excel: bool = True
    
    # API Settings - use config.py values as defaults
    request_timeout: int = config.REQUEST_TIMEOUT
    rate_limit_delay: float = config.RATE_LIMIT_DELAY
    
    def validate_settings(self) -> None:
        """Validate settings and warn about potential issues"""
        current_year = 2025  # Current NFL season
        
        if self.season > current_year:
            print(f"WARNING: Season {self.season} is in the future. ESPN may not have this data yet.")
        elif self.season < current_year - 1:
            print(f"WARNING: Season {self.season} is quite old. Data may be limited.")
            
        if self.request_timeout < 10:
            print(f"WARNING: Request timeout {self.request_timeout}s may be too short for ESPN API.")
            
        if self.rate_limit_delay < 0.05:
            print(f"WARNING: Rate limit delay {self.rate_limit_delay}s may be too aggressive.")


class NFLScoresCollector:
    """Main collector class that coordinates score collection and export"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.logger = logging.getLogger(__name__)
        
        # Store script directory for path resolution
        self.script_dir = Path(__file__).parent
        
        # Initialize exporter with path relative to script location
        output_path = self.script_dir / self.settings.output_directory
        self.exporter = ScoresDataExporter(
            output_dir=str(output_path)
        )
        
        self.logger.info("Using ESPN hidden API - free but unofficial and may change")
    
    async def collect_scores(self) -> List[GameScore]:
        """Collect NFL scores based on settings"""
        client = NFLAPIClient(self.settings)
        
        async with client.session():
            if self.settings.current_week is not None:
                # Get specific week
                self.logger.info(f"Collecting scores for week {self.settings.current_week}")
                games = await client.get_week_scores(week=self.settings.current_week)
            else:
                # Get recent games  
                self.logger.info("Collecting recent game scores")
                games = await client.get_completed_games_recent(days_back=10)
            
            if self.settings.only_completed_games:
                completed_games = [g for g in games if g.is_completed]
                self.logger.info(f"Filtered to {len(completed_games)} completed games out of {len(games)} total")
                return completed_games
            
            return games
    
    async def export_data(self, games: List[GameScore]) -> List[str]:
        """Export game data based on configuration settings"""
        # Create WeeklyScores container for the exporter
        week = games[0].week if games else 0
        season = games[0].season if games else self.settings.season
        season_type = games[0].season_type if games else self.settings.season_type
        completed_games = len([g for g in games if g.is_completed])
        
        weekly_scores = WeeklyScores(
            week=week,
            season=season,
            season_type=season_type,
            total_games=len(games),
            completed_games=completed_games,
            games=games
        )
        
        return await self.exporter.export_all_formats(
            weekly_scores,
            create_csv=self.settings.create_csv,
            create_json=self.settings.create_json,
            create_excel=self.settings.create_excel,
            create_condensed_excel=self.settings.create_condensed_excel
        )
    
    def print_summary(self, games: List[GameScore]) -> None:
        """Print summary of collected scores"""
        print(f"\n[SUCCESS] NFL Scores Collection Complete!")
        print(f"Season: {self.settings.season}")
        print(f"API Source: ESPN")
        print(f"Total Games: {len(games)}")
        
        if not games:
            print("No games found for the specified criteria.")
            return
        
        # Game status breakdown
        status_counts = {}
        for game in games:
            status = "Completed" if game.is_completed else "In Progress" if game.is_in_progress else "Scheduled"
            status_counts[status] = status_counts.get(status, 0) + 1
        
        print(f"\nGame Status Breakdown:")
        for status, count in status_counts.items():
            print(f"   {status}: {count} games")
        
        # Show recent completed games
        completed_games = [g for g in games if g.is_completed]
        if completed_games:
            print(f"\nRecent Completed Games:")
            for game in completed_games[-5:]:  # Last 5 completed
                print(f"   {game.away_team.display_name} {game.away_score} - {game.home_score} {game.home_team.display_name}")


async def main():
    """Main application entry point"""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting NFL scores collection with ESPN API")
        
        # Load and validate settings
        settings = Settings()
        settings.validate_settings()
        
        # Create collector and gather data
        collector = NFLScoresCollector(settings)
        games = await collector.collect_scores()
        
        if not games:
            print("[INFO] No games found for the specified criteria.")
            return
        
        # Export data
        output_files = await collector.export_data(games)
        
        # Print summary
        collector.print_summary(games)
        
        print(f"\nOutput Files:")
        for file in output_files:
            print(f"   {file}")
        
        # Show API source info
        print(f"\nESPN API Usage:")
        print(f"   Free and no signup required")
        print(f"   Unofficial API - use responsibly")
        
        logger.info("Score collection completed successfully")
        
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        print(f"\n[ERROR] Error: {e}")
        
        if "api" in str(e).lower():
            print("\nESPN API Help:")
            print("   ESPN API is free but unofficial")
            print("   Check your network connection and try again")
        
        raise


if __name__ == "__main__":
    asyncio.run(main())