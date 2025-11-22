#!/usr/bin/env python3
"""
NFL Player Projections Data Collection Script - ESPN API
====================================================================

Retrieves fantasy football projections using ESPN's free public API.
No signup or API keys required.

Author: Kai Mizuno
"""

import asyncio
import shutil
import sys
from pathlib import Path
from time import sleep
from typing import Dict, List

import pandas as pd
from pydantic_settings import BaseSettings, SettingsConfigDict

# Add parent directory to path for data access BEFORE importing data
sys.path.append(str(Path(__file__).parent.parent))
from utils.csv_utils import read_csv_with_validation
from utils.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import setup_logger, get_logger

from player_data_models import ScoringFormat, ProjectionData
from espn_client import ESPNClient
from player_data_exporter import DataExporter

# Import NFL season configuration
from config import (
    NFL_SEASON, CURRENT_NFL_WEEK,
    SKIP_DRAFTED_PLAYER_UPDATES, USE_SCORE_THRESHOLD, PLAYER_SCORE_THRESHOLD,
    OUTPUT_DIRECTORY, CREATE_CSV, CREATE_JSON, CREATE_EXCEL,
    REQUEST_TIMEOUT, RATE_LIMIT_DELAY, LOGGING_LEVEL, LOGGING_TO_FILE, LOGGING_FILE,
    LOG_NAME, LOGGING_FORMAT,
    ENABLE_HISTORICAL_DATA_SAVE
)


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables and .env file.

    Supports configuration via environment variables with NFL_PROJ_ prefix.
    Falls back to default values if environment variables are not set.

    Attributes:
        scoring_format: Fantasy scoring format (PPR, Half-PPR, or Standard)
        season: NFL season year
        current_nfl_week: Current NFL week (1-18)
        output_directory: Directory for output files
        create_csv: Whether to create CSV output
        create_json: Whether to create JSON output
        create_excel: Whether to create Excel output
    """
    model_config = SettingsConfigDict(
        env_file_encoding='utf-8',
        env_prefix='NFL_PROJ_',
        extra='ignore'  # Ignore extra environment variables
    )

    # Data Parameters
    scoring_format: ScoringFormat = ScoringFormat.PPR
    season: int = NFL_SEASON  # Current NFL season (from config)

    # Week-by-Week Projection Settings (from config)
    current_nfl_week: int = CURRENT_NFL_WEEK  # Current NFL week (1-18, from config)

    # Optimization Settings (from config)
    skip_drafted_player_updates: bool = SKIP_DRAFTED_PLAYER_UPDATES  # Skip API calls for drafted=1 players (from config)
    use_score_threshold: bool = USE_SCORE_THRESHOLD  # Only update players above score threshold (from config)
    player_score_threshold: float = PLAYER_SCORE_THRESHOLD  # Minimum fantasy points to trigger API update (from config)
    
    def validate_settings(self) -> None:
        """Validate settings and warn about potential issues"""
        import datetime
        current_year = datetime.datetime.now().year
        logger = get_logger()
        
        if self.season > current_year:
            logger.warning(f"Season {self.season} is in the future. ESPN may not have this data yet.")
        elif self.season < current_year - 1:
            logger.warning(f"Season {self.season} is quite old. Data may be limited.")
            
        if self.request_timeout < 10:
            logger.warning(f"Request timeout {self.request_timeout}s may be too short for ESPN API.")
            
        if self.rate_limit_delay < 0.1:
            logger.warning(f"Rate limit delay {self.rate_limit_delay}s may be too aggressive.")
    
    # Output Configuration (from config)
    output_directory: str = OUTPUT_DIRECTORY  # Output directory (from config)
    create_csv: bool = CREATE_CSV  # Whether to create CSV output (from config)
    create_json: bool = CREATE_JSON  # Whether to create JSON output (from config)
    create_excel: bool = CREATE_EXCEL  # Whether to create Excel output (from config)
    create_latest_files: bool = True  # Whether to create latest versions

    # API Settings (from config)
    request_timeout: int = REQUEST_TIMEOUT  # Request timeout in seconds (from config)
    rate_limit_delay: float = RATE_LIMIT_DELAY  # Delay between requests (from config)


class NFLProjectionsCollector:
    """Main collector class that coordinates data collection and export"""

    # ============================================================================
    # INITIALIZATION & SETUP
    # ============================================================================

    def __init__(self, settings: Settings):
        """
        Initialize the NFL projections collector.

        Args:
            settings: Application settings including API configuration and output options
        """
        self.settings = settings
        self.logger = get_logger()

        # Store script directory for path resolution
        self.script_dir = Path(__file__).parent

        # Load bye weeks data
        self.bye_weeks = self._load_bye_weeks()

        # Initialize team rankings and schedule data (will be populated during data collection)
        self.team_rankings = {}
        self.current_week_schedule = {}
        self.position_defense_rankings = {}
        self.team_weekly_data = {}

        # Initialize exporter with path relative to script location
        output_path = self.script_dir / self.settings.output_directory
        self.exporter = DataExporter(
            output_dir=str(output_path),
            create_latest_files=self.settings.create_latest_files
        )
        
        self.logger.info("Using ESPN hidden API - free but unofficial and may change")
    
    def _load_bye_weeks(self) -> Dict[str, int]:
        """
        Load bye week schedule from CSV file with robust error handling.

        Bye weeks are when NFL teams don't play (1 week per team per season).
        Players on bye weeks score 0 points and shouldn't be started.

        File format (data/bye_weeks.csv):
        Team,ByeWeek
        KC,10
        SF,9
        ...

        Returns:
            Dict mapping team abbreviation to bye week number (1-18)
            Example: {'KC': 10, 'SF': 9, 'BUF': 7}
        """
        bye_weeks = {}

        # Look for bye_weeks.csv in parent directory's data folder
        # Path: player-data-fetcher/../data/bye_weeks.csv = project_root/data/bye_weeks.csv
        bye_weeks_file = self.script_dir.parent / "data" / "bye_weeks.csv"

        if not bye_weeks_file.exists():
            # File missing = first run or file deleted
            # Not fatal: players just won't have bye week data
            self.logger.warning(f"Bye weeks file not found: {bye_weeks_file}")
            return bye_weeks

        try:
            # Use standardized CSV reading with column validation
            # Ensures file has required 'Team' and 'ByeWeek' columns
            required_columns = ['Team', 'ByeWeek']
            df = read_csv_with_validation(bye_weeks_file, required_columns)

            # Data validation: Bye weeks must be between 1-18 (NFL regular season length)
            # Invalid values could be typos or old data
            invalid_weeks = df[~df['ByeWeek'].between(1, 18)]
            if not invalid_weeks.empty:
                # Log but don't crash - just filter out invalid entries
                self.logger.warning(f"Invalid bye weeks found: {invalid_weeks[['Team', 'ByeWeek']].to_dict('records')}")

            # Filter to only valid bye weeks (between 1 and 18)
            valid_df = df[df['ByeWeek'].between(1, 18)]

            # Convert DataFrame to dictionary for fast lookups
            # Format: {'KC': 10, 'SF': 9, ...}
            bye_weeks = dict(zip(valid_df['Team'], valid_df['ByeWeek']))

            self.logger.info(f"Loaded bye weeks for {len(bye_weeks)} teams")
            self.logger.debug(f"Bye weeks data: {bye_weeks}")

        except Exception as e:
            # CSV read failed or column missing
            # Not fatal: proceed without bye week data
            self.logger.error(f"Failed to load bye weeks from {bye_weeks_file}: {e}")
            self.logger.error("Players will not have bye week information")

        return bye_weeks

    # ============================================================================
    # DATA COLLECTION
    # ============================================================================

    async def collect_all_projections(self) -> Dict[str, ProjectionData]:
        """
        Collect all projection data from ESPN API.

        Main data collection workflow:
        1. Create ESPN API client
        2. Pass bye weeks data to client for player enrichment
        3. Fetch season projections (includes week-by-week data)
        4. Fetch team rankings (offensive/defensive quality)
        5. Fetch current week schedule (matchups)
        6. Package everything into ProjectionData objects

        Returns:
            Dict with 'season' key containing ProjectionData for all players
        """
        # Create ESPN API client with configured settings
        client = self._get_api_client()

        # Pass bye weeks data to client so it can enrich player data
        # Client will add bye_week field to each player based on their team
        client.bye_weeks = self.bye_weeks

        # Use async context manager to ensure HTTP client is properly closed
        async with client.session():
            results = {}

            # Fetch season projections from ESPN API
            self.logger.info("Collecting season projections")
            try:
                # get_season_projections() returns List[ESPNPlayerData]
                # This makes one API call to get basic player info, then
                # additional calls for each player to get week-by-week projections
                season_projections = await client.get_season_projections()

                # Package raw player data into ProjectionData model
                # This validates data structure and adds metadata
                season_data = ProjectionData(
                    season=self.settings.season,
                    scoring_format=self.settings.scoring_format.value,
                    total_players=len(season_projections),
                    players=season_projections
                )

                results['season'] = season_data
                self.logger.info(f"Collected {len(season_projections)} season projections")

                # Extract team data that was cached during projection fetching
                # Team rankings: offensive/defensive quality (1-32 ranking)
                # Schedule: current week matchups (team → opponent)
                # Position defense rankings: position-specific defense rankings (1-32 per position)
                team_rankings = client.team_rankings
                current_week_schedule = client.current_week_schedule
                position_defense_rankings = client.position_defense_rankings
                self.logger.info(f"Collected team rankings for {len(team_rankings)} teams")
                self.logger.info(f"Collected current week schedule for {len(current_week_schedule)} teams")
                self.logger.info(f"Collected position defense rankings for {len(position_defense_rankings)} teams")

                # Store for later use by exporter (needs this for team_data)
                self.team_rankings = team_rankings
                self.current_week_schedule = current_week_schedule
                self.position_defense_rankings = position_defense_rankings

                # Collect per-team, per-week data for new team_data format
                self.team_weekly_data = client._collect_team_weekly_data(
                    season_projections,
                    client.full_season_schedule,
                    self.settings.current_nfl_week
                )
                self.logger.info(f"Collected team weekly data for {len(self.team_weekly_data)} teams")

            except Exception as e:
                # Don't crash entire app if projection fetch fails
                # Return empty results dict instead
                self.logger.error(f"Failed to collect season projections: {e}")

            return results
    
    def _get_api_client(self) -> ESPNClient:
        """Get ESPN API client"""
        return ESPNClient(self.settings)

    # ============================================================================
    # DATA EXPORT
    # ============================================================================

    async def export_data(self, projection_data: Dict[str, ProjectionData]) -> List[str]:
        """
        Export all collected data to configured output formats.

        Exports to multiple destinations:
        1. Timestamped files in player-data-fetcher/data/ (CSV/JSON/Excel)
        2. Shared data/players.csv (for draft helper integration) [configured via PLAYERS_CSV]
        3. Shared data/team_data/ folder (per-team historical rankings)
        4. Shared data/players_projected.csv (week-by-week projections for performance tracking)

        File organization:
        - player-data-fetcher/data/nfl_projections_season_PPR_20241018_120000.csv (timestamped)
        - player-data-fetcher/data/nfl_projections_season_PPR_latest.csv (latest version)
        - player-data-fetcher/data/teams_20241018_120000.csv (timestamped team data)
        - player-data-fetcher/data/teams_latest.csv (latest team data)
        - data/players.csv (shared with draft helper - full player data) [path: PLAYERS_CSV in config.py]
        - data/team_data/*.csv (shared with league helper - per-team historical data)
        - data/players_projected.csv (shared with league helper - week-by-week projections)

        Args:
            projection_data: Dict containing ProjectionData objects to export

        Returns:
            List of file paths created during export
        """
        # Pass team data to exporter so it can create team_data files
        # Team rankings: offensive/defensive quality (used for matchup evaluation)
        # Schedule: current week matchups (used for opponent strength)
        # Position defense rankings: position-specific defense rankings (used for schedule scoring)
        self.exporter.set_team_rankings(self.team_rankings)
        self.exporter.set_current_week_schedule(self.current_week_schedule)
        self.exporter.set_position_defense_rankings(self.position_defense_rankings)
        self.exporter.set_team_weekly_data(self.team_weekly_data)

        output_files = []

        # Export each projection type (typically just 'season')
        for data_type, data in projection_data.items():
            # Export to all configured formats (CSV/JSON/Excel)
            # Also creates timestamped and latest versions
            # Also creates team_data folder with per-team historical data
            files = await self.exporter.export_all_formats_with_teams(
                data,
                create_csv=self.settings.create_csv,
                create_json=self.settings.create_json,
                create_excel=self.settings.create_excel
            )
            output_files.extend(files)
            self.logger.info(f"Exported {data_type} projections to configured formats")

            # Export to shared data/players.csv for draft helper integration
            # This file is read by the draft helper to get current player projections
            # Format: Full player data with all fields (id, name, team, position, fantasy_points, etc.)
            shared_file = await self.exporter.export_to_data(data)
            output_files.append(shared_file)

            # Update players_projected.csv with current and future week projections
            # Per requirement #6: "Update current week and everything upcoming"
            # This preserves historical weeks and only updates current + future weeks
            # Used by league helper for performance tracking against projections
            try:
                projected_file = await self.exporter.export_projected_points_data(
                    data,
                    self.settings.current_nfl_week  # Only update this week and beyond
                )
                output_files.append(projected_file)
                self.logger.info("Updated players_projected.csv with current/future week projections")
            except FileNotFoundError as e:
                # File doesn't exist yet - this is normal for first run
                # Skip update but don't crash the entire export
                self.logger.warning(f"Skipping players_projected.csv update: {e}")
            except Exception as e:
                # Unexpected error updating projected points
                # Log error but don't fail entire export - this is a supplementary feature
                self.logger.error(f"Error updating players_projected.csv: {e}")
                # Don't append to output_files since update failed

        return output_files

    def save_to_historical_data(self) -> bool:
        """
        Save current data files to historical data folder for the current week.

        Checks config flag ENABLE_HISTORICAL_DATA_SAVE before proceeding.
        Checks if data/historical_data/{Season}/{WeekNumber}/ exists.
        If not, creates it and copies players.csv, players_projected.csv, team_data/.
        If it exists, skips (files already saved for this week).

        Week numbers are zero-padded (01, 02, ..., 11, 12).

        Returns:
            bool: True if files were saved, False if already saved, disabled, or error occurred
        """
        # Check if feature is enabled
        if not ENABLE_HISTORICAL_DATA_SAVE:
            self.logger.debug("Historical data auto-save disabled via config")
            return False

        try:
            # Construct zero-padded week number (e.g., "01", "11")
            week_number = f"{CURRENT_NFL_WEEK:02d}"

            # Construct historical data path: data/historical_data/{Season}/{WeekNumber}/
            # Use parent of script_dir to get project root, then navigate to data folder
            historical_folder = self.script_dir.parent / "data" / "historical_data" / str(NFL_SEASON) / week_number

            # Check if folder already exists
            if historical_folder.exists():
                self.logger.info(f"Historical data already saved for Week {CURRENT_NFL_WEEK} (folder {week_number} exists)")
                return False

            # Create folder with parents=True to create season folder if needed
            self.logger.info(f"Creating historical data folder: {historical_folder}")
            historical_folder.mkdir(parents=True, exist_ok=True)

            # Define source files to copy
            data_folder = self.script_dir.parent / "data"
            files_to_copy = ["players.csv", "players_projected.csv"]

            # Copy each file using shutil.copy2 to preserve metadata
            for filename in files_to_copy:
                source = data_folder / filename
                destination = historical_folder / filename

                if source.exists():
                    shutil.copy2(str(source), str(destination))
                    self.logger.debug(f"Copied {filename} to {historical_folder}")
                else:
                    self.logger.warning(f"Source file not found: {source}")

            # Copy team_data folder (replaces teams.csv in historical data)
            team_data_source = data_folder / "team_data"
            team_data_dest = historical_folder / "team_data"
            if team_data_source.exists():
                shutil.copytree(str(team_data_source), str(team_data_dest))
                self.logger.debug(f"Copied team_data folder to {historical_folder}")
            else:
                self.logger.warning(f"Team data folder not found: {team_data_source}")

            self.logger.info(f"Successfully saved historical data for Week {CURRENT_NFL_WEEK} to {historical_folder}")
            return True

        except Exception as e:
            # Log warning but don't crash - this is a supplementary feature
            self.logger.warning(f"Failed to save historical data: {e}")
            return False

    # ============================================================================
    # UTILITY METHODS (Conversion & Display)
    # ============================================================================

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

    logger = setup_logger(LOG_NAME, LOGGING_LEVEL, LOGGING_TO_FILE, LOGGING_FILE, LOGGING_FORMAT)
    
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

        # Auto-save to historical data folder (if enabled via config)
        try:
            saved = collector.save_to_historical_data()
            if saved:
                print(f"\n[INFO] Saved weekly data to historical folder")
            elif not ENABLE_HISTORICAL_DATA_SAVE:
                logger.debug("Historical data auto-save disabled via config")
            else:
                print(f"\n[INFO] Weekly data already saved for Week {settings.current_nfl_week}")
        except Exception as e:
            logger.warning(f"Failed to save historical data: {e}")
            print(f"\n[WARNING] Could not save to historical folder: {e}")

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