#!/usr/bin/env python3
"""
NFL Player Projections Data Collection Script - ESPN API (Refactored)
====================================================================

Retrieves fantasy football projections using ESPN's free public API.
No signup or API keys required.

Example Usage:
    # Basic usage (PPR scoring)
    python data_fetcher-players.py
    
    # Specific scoring format
    NFL_PROJ_SCORING_FORMAT=half python data_fetcher-players.py
    
    # Change output directory and formats
    NFL_PROJ_OUTPUT_DIRECTORY=./my_projections NFL_PROJ_CREATE_CSV=false python data_fetcher-players.py
    
    # Using .env file (create .env in project root):
    # NFL_PROJ_SCORING_FORMAT=ppr
    # NFL_PROJ_OUTPUT_DIRECTORY=./projections

Author: Generated for NFL Fantasy Data Collection
Last Updated: September 2025

Dependencies:
    pip install httpx pydantic tenacity python-dotenv pandas openpyxl aiofiles
"""

import asyncio
import logging
from pathlib import Path
from time import sleep
from typing import Dict, List

import pandas as pd
from pydantic_settings import BaseSettings, SettingsConfigDict

# Import our new modular components  
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

# Get the path to the .env file in the parent directory  
ENV_FILE_PATH = Path(__file__).parent.parent / '.env'

from models import ScoringFormat, ProjectionData, DataCollectionError
from espn_client import ESPNClient
from data_exporter import DataExporter
from shared_files.FantasyPlayer import FantasyPlayer


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE_PATH),
        env_file_encoding='utf-8',
        env_prefix='NFL_PROJ_',
        extra='ignore'  # Ignore extra environment variables
    )
    
    # Data Parameters
    scoring_format: ScoringFormat = ScoringFormat.PPR
    season: int = 2025  # Current NFL season
    
    def validate_settings(self) -> None:
        """Validate settings and warn about potential issues"""
        current_year = 2025  # Current NFL season
        
        if self.season > current_year:
            print(f"WARNING: Season {self.season} is in the future. ESPN may not have this data yet.")
        elif self.season < current_year - 1:
            print(f"WARNING: Season {self.season} is quite old. Data may be limited.")
            
        if self.request_timeout < 10:
            print(f"WARNING: Request timeout {self.request_timeout}s may be too short for ESPN API.")
            
        if self.rate_limit_delay < 0.1:
            print(f"WARNING: Rate limit delay {self.rate_limit_delay}s may be too aggressive.")
    
    # Output Configuration  
    output_directory: str = "data"
    create_csv: bool = True  # Whether to create CSV output
    create_json: bool = True  # Whether to create JSON output
    create_excel: bool = True  # Whether to create Excel output
    create_latest_files: bool = True  # Whether to create latest versions
    
    # API Settings
    request_timeout: int = 30
    rate_limit_delay: float = 0.2  # 5 requests per second


class NFLProjectionsCollector:
    """Main collector class that coordinates data collection and export"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.logger = logging.getLogger(__name__)
        
        # Store script directory for path resolution
        self.script_dir = Path(__file__).parent
        
        # Load bye weeks data
        self.bye_weeks = self._load_bye_weeks()
        
        # Initialize exporter with path relative to script location
        output_path = self.script_dir / self.settings.output_directory
        self.exporter = DataExporter(
            output_dir=str(output_path),
            create_latest_files=self.settings.create_latest_files
        )
        
        self.logger.info("Using ESPN hidden API - free but unofficial and may change")
    
    def _load_bye_weeks(self) -> Dict[str, int]:
        """Load bye weeks from CSV file with robust error handling"""
        bye_weeks = {}
        # Look for bye_weeks.csv in parent directory's shared_files folder
        bye_weeks_file = self.script_dir.parent / "shared_files" / "bye_weeks.csv"
        
        if not bye_weeks_file.exists():
            self.logger.warning(f"Bye weeks file not found: {bye_weeks_file}")
            return bye_weeks
            
        try:
            df = pd.read_csv(bye_weeks_file)
            
            # Validate required columns
            if 'Team' not in df.columns or 'ByeWeek' not in df.columns:
                raise ValueError("CSV must contain 'Team' and 'ByeWeek' columns")
            
            # Validate bye week values are reasonable (1-18)
            invalid_weeks = df[~df['ByeWeek'].between(1, 18)]
            if not invalid_weeks.empty:
                self.logger.warning(f"Invalid bye weeks found: {invalid_weeks[['Team', 'ByeWeek']].to_dict('records')}")
            
            # Filter to valid weeks only
            valid_df = df[df['ByeWeek'].between(1, 18)]
            bye_weeks = dict(zip(valid_df['Team'], valid_df['ByeWeek']))
            
            self.logger.info(f"Loaded bye weeks for {len(bye_weeks)} teams")
            self.logger.debug(f"Bye weeks data: {bye_weeks}")
            
        except Exception as e:
            self.logger.error(f"Failed to load bye weeks from {bye_weeks_file}: {e}")
            self.logger.error("Players will not have bye week information")
            
        return bye_weeks
    
    async def collect_all_projections(self) -> Dict[str, ProjectionData]:
        """Collect season projections"""
        client = self._get_api_client()
        # Pass bye weeks data to the client
        client.bye_weeks = self.bye_weeks
        
        async with client.session():
            results = {}
            
            # Get season projections
            self.logger.info("Collecting season projections")
            try:
                season_projections = await client.get_season_projections()
                
                season_data = ProjectionData(
                    season=self.settings.season,
                    scoring_format=self.settings.scoring_format.value,
                    total_players=len(season_projections),
                    players=season_projections
                )
                
                results['season'] = season_data
                self.logger.info(f"Collected {len(season_projections)} season projections")
            except Exception as e:
                self.logger.error(f"Failed to collect season projections: {e}")
            
            return results
    
    def _get_api_client(self) -> ESPNClient:
        """Get ESPN API client"""
        return ESPNClient(self.settings)
    
    async def export_data(self, projection_data: Dict[str, ProjectionData]) -> List[str]:
        """Export all projection data based on configuration settings"""
        output_files = []
        
        for data_type, data in projection_data.items():
            files = await self.exporter.export_all_formats(
                data,
                create_csv=self.settings.create_csv,
                create_json=self.settings.create_json,
                create_excel=self.settings.create_excel
            )
            output_files.extend(files)
            self.logger.info(f"Exported {data_type} projections to configured formats")
        
        return output_files
    
    def get_fantasy_players(self, projection_data: Dict[str, ProjectionData]) -> Dict[str, List[FantasyPlayer]]:
        """
        Convert projection data to FantasyPlayer objects for easy use by other scripts.
        
        Args:
            projection_data: Dictionary containing ProjectionData objects
            
        Returns:
            Dictionary with keys like 'season' and values as lists of FantasyPlayer objects
        """
        fantasy_players = {}
        for data_type, data in projection_data.items():
            fantasy_players[data_type] = self.exporter.get_fantasy_players(data)
        return fantasy_players
    
    def print_summary(self, projection_data: Dict[str, ProjectionData]) -> None:
        """Print summary of collected data"""
        print(f"\n[SUCCESS] NFL Player Projections Collection Complete!")
        print(f"Season: {self.settings.season}")
        print(f"API Source: ESPN")
        print(f"Scoring Format: {self.settings.scoring_format.value.upper()}")
        
        for data_type, data in projection_data.items():
            print(f"\n{data_type.title()} Projections:")
            print(f"   Total Players: {data.total_players}")
            
            # Position breakdown
            position_counts = {}
            position_points = {}
            
            for player in data.players:
                pos = player.position
                if pos not in position_counts:
                    position_counts[pos] = 0
                    position_points[pos] = []
                
                position_counts[pos] += 1
                position_points[pos].append(player.fantasy_points)
            
            print(f"   Position Breakdown:")
            for pos in sorted(position_counts.keys()):
                count = position_counts[pos]
                points_list = position_points[pos]
                avg_points = sum(points_list) / len(points_list) if points_list else 0
                max_points = max(points_list) if points_list else 0
                
                # Find top player for this position
                top_player = None
                for player in data.players:
                    if player.position == pos and player.fantasy_points == max_points:
                        top_player = player
                        break
                
                top_name = top_player.name if top_player else "Unknown"
                print(f"     {pos}: {count} players (Top: {top_name} - {max_points:.1f} pts, Avg: {avg_points:.1f})")


async def main():
    """Main application entry point"""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting NFL projections collection with ESPN API")
        
        # Load and validate settings
        settings = Settings()
        settings.validate_settings()
        
        # Create collector and gather data
        collector = NFLProjectionsCollector(settings)
        projection_data = await collector.collect_all_projections()
        
        if not projection_data:
            print("[ERROR] No projection data collected. Check your configuration.")
            return
        
        # Export data
        output_files = await collector.export_data(projection_data)
        
        # Print summary
        collector.print_summary(projection_data)
        
        # Convert to FantasyPlayer objects for demonstration
        fantasy_players = collector.get_fantasy_players(projection_data)
        
        print(f"\nOutput Files:")
        for file in output_files:
            print(f"   {file}")
        
        # Show API source info
        print(f"\nESPN API Usage:")
        print(f"   Free and no signup required")
        print(f"   Unofficial API - use responsibly")
        
        # Demonstrate FantasyPlayer usage
        if 'season' in fantasy_players:
            season_players = fantasy_players['season']
            print(f"\nFantasyPlayer Integration:")
            print(f"   Converted {len(season_players)} players to FantasyPlayer objects")
            print(f"   Available for import: from fantasy_player import FantasyPlayer")
            print(f"   Load from CSV: FantasyPlayer.from_csv_file('data/nfl_projections/nfl_projections_latest_season.csv')")
        
        logger.info("Data collection completed successfully")
        
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