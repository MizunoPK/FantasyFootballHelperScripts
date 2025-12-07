#!/usr/bin/env python3
"""
Data Export Module for NFL Fantasy Football Data

This module handles all data export operations (CSV, JSON, Excel) with
async file I/O for better performance.

Author: Kai Mizuno
"""

import asyncio
from datetime import datetime
from pathlib import Path
from typing import List
import csv

import aiofiles
import pandas as pd

from player_data_models import ProjectionData, ESPNPlayerData

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.FantasyPlayer import FantasyPlayer
from utils.TeamData import save_team_weekly_data, NFL_TEAMS
from utils.data_file_manager import DataFileManager
from utils.LoggingManager import get_logger
from utils.DraftedRosterManager import DraftedRosterManager
from config import DEFAULT_FILE_CAPS
from config import EXCEL_POSITION_SHEETS, EXPORT_COLUMNS, PRESERVE_DRAFTED_VALUES, PRESERVE_LOCKED_VALUES, PLAYERS_CSV, TEAM_DATA_FOLDER, LOAD_DRAFTED_DATA_FROM_FILE, DRAFTED_DATA, MY_TEAM_NAME


class DataExporter:
    """Handles exporting projection data to various formats with async I/O"""

    # ============================================================================
    # INITIALIZATION & CONFIGURATION
    # ============================================================================

    def __init__(self, output_dir: str, create_latest_files: bool = True):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.create_latest_files = create_latest_files
        self.logger = get_logger()

        # Initialize file manager for automatic file caps
        self.file_manager = DataFileManager(str(self.output_dir), DEFAULT_FILE_CAPS)

        # Initialize team rankings and schedule data (will be set by data collector)
        self.team_rankings = {}
        self.current_week_schedule = {}
        self.position_defense_rankings = {}
        self.team_weekly_data = {}  # Per-team, per-week data for new format

        # Load existing drafted and locked values if preservation is enabled
        self.existing_drafted_values = {}
        self.existing_locked_values = {}
        if PRESERVE_DRAFTED_VALUES:
            self._load_existing_drafted_values()
        if PRESERVE_LOCKED_VALUES:
            self._load_existing_locked_values()

        # Initialize drafted roster manager if enabled
        self.drafted_roster_manager = DraftedRosterManager(DRAFTED_DATA, MY_TEAM_NAME)
        if LOAD_DRAFTED_DATA_FROM_FILE:
            self.drafted_roster_manager.load_drafted_data()

    def set_team_rankings(self, team_rankings: dict):
        """Set team rankings data from ESPN client for team exports"""
        self.team_rankings = team_rankings
        self.logger.info(f"Team rankings set for {len(team_rankings)} teams")

    def set_current_week_schedule(self, schedule: dict):
        """Set current week schedule data from ESPN client for team exports"""
        self.current_week_schedule = schedule
        self.logger.info(f"Current week schedule set for {len(schedule)} teams")

    def set_position_defense_rankings(self, rankings: dict):
        """Set position-specific defense rankings from ESPN client"""
        self.position_defense_rankings = rankings
        self.logger.info(f"Position defense rankings set for {len(rankings)} teams")

    def set_team_weekly_data(self, data: dict):
        """Set per-team, per-week data for new team_data format export"""
        self.team_weekly_data = data
        self.logger.info(f"Team weekly data set for {len(data)} teams")

    # ============================================================================
    # FORMAT-SPECIFIC EXPORTS (JSON, CSV, Excel)
    # ============================================================================

    async def export_json(self, data: ProjectionData) -> str:
        """Export data to JSON format asynchronously"""
        try:
            # Convert to JSON-serializable format
            json_data = {
                "season": data.season,
                "scoring_format": data.scoring_format,
                "total_players": data.total_players,
                "generated_at": data.generated_at.isoformat(),
                "players": [player.model_dump() for player in data.players]
            }

            # Use enhanced file manager for consistent JSON export
            prefix = f"nfl_projections_season_{data.scoring_format}"
            timestamped_path, latest_path = self.file_manager.save_json_data(
                json_data, prefix, create_latest=self.create_latest_files
            )

            return str(timestamped_path)

        except PermissionError as e:
            self.logger.error(f"Permission denied writing JSON file: {e}")
            raise
        except OSError as e:
            self.logger.error(f"OS error writing JSON file: {e}")
            raise
        except (TypeError, ValueError) as e:
            self.logger.error(f"JSON serialization error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error exporting JSON file: {e}")
            raise
    
    async def export_csv(self, data: ProjectionData) -> str:
        """Export data to CSV format asynchronously"""
        try:
            # Prepare DataFrame with standard column ordering
            df = self._prepare_export_dataframe(data)

            # Use enhanced file manager for consistent CSV export
            prefix = f"nfl_projections_season_{data.scoring_format}"
            timestamped_path, latest_path = await self.file_manager.save_dataframe_csv(
                df, prefix, create_latest=self.create_latest_files
            )

            return str(timestamped_path)

        except PermissionError as e:
            self.logger.error(f"Permission denied writing CSV file: {e}")
            raise
        except OSError as e:
            self.logger.error(f"OS error writing CSV file: {e}")
            raise
        except ValueError as e:
            self.logger.error(f"Data validation error for CSV export: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error exporting CSV file: {e}")
            raise
    
    async def export_excel(self, data: ProjectionData) -> str:
        """Export data to Excel format with position sheets asynchronously"""
        # Prepare DataFrame with standard column ordering
        df = self._prepare_export_dataframe(data)

        # Use enhanced file manager, but we need custom Excel writing for position sheets
        prefix = f"nfl_projections_season_{data.scoring_format}"
        timestamped_path = self.file_manager.get_timestamped_path(prefix, 'xlsx')

        # Create Excel writer and write sheets asynchronously
        await asyncio.get_event_loop().run_in_executor(
            None, self._write_excel_sheets, df, str(timestamped_path)
        )

        # Create latest version if requested
        if self.create_latest_files:
            latest_path = self.file_manager.get_latest_path(prefix, 'xlsx')
            await asyncio.get_event_loop().run_in_executor(
                None, self._write_excel_sheets, df, str(latest_path)
            )

        # Enforce file caps after successful export
        deleted_files = self.file_manager.enforce_file_caps(str(timestamped_path))
        if deleted_files:
            self.logger.info(f"File caps enforced for Excel: {deleted_files}")

        return str(timestamped_path)

    # ============================================================================
    # DATAFRAME PREPARATION & HELPERS
    # ============================================================================

    def _create_dataframe(self, data: ProjectionData) -> pd.DataFrame:
        """Convert ProjectionData to pandas DataFrame"""
        return pd.DataFrame([player.model_dump() for player in data.players])
    
    def _prepare_export_dataframe(self, data: ProjectionData) -> pd.DataFrame:
        """Create and prepare DataFrame with standard column ordering for export"""
        # Use converted FantasyPlayer objects to ensure drafted values are preserved
        fantasy_players = self.get_fantasy_players(data)
        df = pd.DataFrame([player.to_dict() for player in fantasy_players])
        
        # Ensure all required columns exist, add missing ones with default values
        for col in EXPORT_COLUMNS:
            if col not in df.columns:
                df[col] = None

        # Replace NaN values in weekly projection columns with 0.0
        weekly_columns = [col for col in EXPORT_COLUMNS if col.startswith('week_') and col.endswith('_points')]
        for col in weekly_columns:
            if col in df.columns:
                df[col] = df[col].fillna(0.0).infer_objects(copy=False)

        # Return DataFrame with standardized column order
        return df[EXPORT_COLUMNS]
    
    def _write_excel_sheets(self, df: pd.DataFrame, filepath: str):
        """Write Excel file with multiple sheets (sync helper)"""
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # Write "All Players" sheet
            df_sorted = df.sort_values('fantasy_points', ascending=False)
            df_sorted.to_excel(writer, sheet_name='All Players', index=False)
            
            # Write position-specific sheets
            for position in EXCEL_POSITION_SHEETS:
                position_df = df[df['position'] == position].copy()
                if not position_df.empty:
                    position_df = position_df.sort_values('fantasy_points', ascending=False)
                    position_df.to_excel(writer, sheet_name=position, index=False)

    # ============================================================================
    # DATA LOADING (Existing drafted/locked values)
    # ============================================================================

    def _load_existing_drafted_values(self):
        """Load existing drafted values from draft helper players file"""
        # Resolve path relative to the player-data-fetcher directory (parent of output_dir)
        draft_file_path = Path(__file__).parent / PLAYERS_CSV
        
        try:
            with open(draft_file_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    player_id = row.get('id')
                    drafted_value = int(row.get('drafted', 0))
                    if player_id:
                        self.existing_drafted_values[player_id] = drafted_value
            
            self.logger.info(f"Loaded {len(self.existing_drafted_values)} existing drafted values from {draft_file_path}")
            
        except FileNotFoundError:
            self.logger.warning(f"Draft helper file not found at {draft_file_path}. All drafted values will be set to 0.")
        except Exception as e:
            self.logger.error(f"Error loading existing drafted values: {e}. All drafted values will be set to 0.")
    
    def _load_existing_locked_values(self):
        """Load existing locked values from draft helper players file"""
        # Resolve path relative to the player-data-fetcher directory (parent of output_dir)
        draft_file_path = Path(__file__).parent / PLAYERS_CSV
        
        try:
            with open(draft_file_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    player_id = row.get('id')
                    locked_value = int(row.get('locked', 0))
                    if player_id:
                        self.existing_locked_values[player_id] = locked_value
            
            self.logger.info(f"Loaded {len(self.existing_locked_values)} existing locked values from {draft_file_path}")
            
        except FileNotFoundError:
            self.logger.warning(f"Draft helper file not found at {draft_file_path}. All locked values will be set to 0.")
        except Exception as e:
            self.logger.error(f"Error loading existing locked values: {e}. All locked values will be set to 0.")

    # ============================================================================
    # PLAYER CONVERSION (ESPN → FantasyPlayer)
    # ============================================================================

    def _espn_player_to_fantasy_player(self, player_data: ESPNPlayerData) -> FantasyPlayer:
        """Convert ESPNPlayerData to FantasyPlayer object"""
        
        # Determine drafted value based on configuration
        drafted_value = player_data.drafted  # Default from ESPN (always 0)

        if PRESERVE_DRAFTED_VALUES and player_data.id in self.existing_drafted_values:
            # Use existing drafted values from previous runs
            drafted_value = self.existing_drafted_values[player_data.id]
        # Note: LOAD_DRAFTED_DATA_FROM_FILE now handled in post-processing step
        # If neither option is enabled, all players get drafted=0 (default)
        
        # Use existing locked value if preservation is enabled, otherwise use default (0)
        locked_value = 0  # Default
        if PRESERVE_LOCKED_VALUES and player_data.id in self.existing_locked_values:
            locked_value = self.existing_locked_values[player_data.id]
        
        return FantasyPlayer(
            id=player_data.id,
            name=player_data.name,
            team=player_data.team,
            position=player_data.position,
            bye_week=player_data.bye_week,
            drafted=drafted_value,
            locked=locked_value,
            fantasy_points=player_data.fantasy_points,
            average_draft_position=player_data.average_draft_position,
            # Enhanced scoring fields (NEW)
            player_rating=player_data.player_rating,
            injury_status=player_data.injury_status,
            # Weekly projections (weeks 1-17 fantasy regular season only)
            week_1_points=player_data.week_1_points,
            week_2_points=player_data.week_2_points,
            week_3_points=player_data.week_3_points,
            week_4_points=player_data.week_4_points,
            week_5_points=player_data.week_5_points,
            week_6_points=player_data.week_6_points,
            week_7_points=player_data.week_7_points,
            week_8_points=player_data.week_8_points,
            week_9_points=player_data.week_9_points,
            week_10_points=player_data.week_10_points,
            week_11_points=player_data.week_11_points,
            week_12_points=player_data.week_12_points,
            week_13_points=player_data.week_13_points,
            week_14_points=player_data.week_14_points,
            week_15_points=player_data.week_15_points,
            week_16_points=player_data.week_16_points,
            week_17_points=player_data.week_17_points
        )
    
    def get_fantasy_players(self, data: ProjectionData) -> List[FantasyPlayer]:
        """Convert ProjectionData to list of FantasyPlayer objects"""
        fantasy_players = [self._espn_player_to_fantasy_player(player) for player in data.players]

        # Apply drafted data from CSV file to players using DraftedRosterManager
        fantasy_players = self.drafted_roster_manager.apply_drafted_state_to_players(fantasy_players)

        return fantasy_players

    # ============================================================================
    # HIGH-LEVEL EXPORT ORCHESTRATION
    # ============================================================================

    async def export_all_formats(self, data: ProjectionData, 
                                create_csv: bool = True, 
                                create_json: bool = True, 
                                create_excel: bool = True) -> List[str]:
        """Export data to all requested formats concurrently"""
        tasks = []
        
        if create_json:
            tasks.append(self.export_json(data))
        if create_csv:
            tasks.append(self.export_csv(data))
        if create_excel:
            tasks.append(self.export_excel(data))
        
        if not tasks:
            return []
        
        # Run all exports concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and log them with more detail
        output_files = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                export_type = ['JSON', 'CSV', 'Excel'][i] if i < 3 else f'Export {i+1}'
                self.logger.error(f"{export_type} export failed: {result.__class__.__name__}: {result}")
            else:
                output_files.append(result)

        return output_files

    # ============================================================================
    # SHARED FILE EXPORTS (Integration with draft helper and other modules)
    # ============================================================================

    async def export_to_data(self, data: ProjectionData) -> str:
        """Export data to data/players.csv for use by draft helper"""
        # Resolve path to data/players.csv
        draft_file_path = Path(__file__).parent / PLAYERS_CSV

        try:
            # Ensure the directory exists
            draft_file_path.parent.mkdir(parents=True, exist_ok=True)

            # Prepare DataFrame with preserved drafted/locked values
            df = self._prepare_export_dataframe(data)

            # Export to CSV asynchronously
            async with aiofiles.open(str(draft_file_path), mode='w', newline='', encoding='utf-8') as csvfile:
                # Write header
                await csvfile.write(','.join(EXPORT_COLUMNS) + '\n')

                # Write data rows
                for _, row in df.iterrows():
                    row_data = [str(row[col]) for col in EXPORT_COLUMNS]
                    await csvfile.write(','.join(row_data) + '\n')

            self.logger.info(f"Exported {len(df)} players to shared files: {draft_file_path}")
            return str(draft_file_path)

        except PermissionError as e:
            self.logger.error(f"Permission denied writing to {draft_file_path}: {e}")
            raise
        except OSError as e:
            self.logger.error(f"OS error writing to {draft_file_path}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error exporting to shared files: {e}")
            raise

    # ============================================================================
    # TEAM DATA EXPORTS
    # ============================================================================

    async def export_teams_csv(self, data: ProjectionData) -> str:
        """
        Export team data to local data directory in team_data folder format.

        Creates individual CSV files for each NFL team containing weekly data.

        Args:
            data: ProjectionData containing player information

        Returns:
            str: Path to the team_data folder
        """
        try:
            # Create team_data folder in output directory
            team_data_folder = self.output_dir / "team_data"
            team_data_folder.mkdir(exist_ok=True)

            # Get team weekly data from ESPN client (should be set by caller)
            if not hasattr(self, 'team_weekly_data') or not self.team_weekly_data:
                self.logger.warning("No team weekly data available for export")
                return ""

            # Save to team_data folder
            save_team_weekly_data(str(team_data_folder), self.team_weekly_data)

            self.logger.info(f"Exported team data for {len(self.team_weekly_data)} teams to: {team_data_folder}")
            return str(team_data_folder)

        except Exception as e:
            self.logger.error(f"Error exporting team data: {e}")
            raise

    async def export_teams_to_data(self, data: ProjectionData) -> str:
        """
        Export team data to shared data directory for consumption by other modules.

        Creates team_data folder with individual CSV files for each NFL team.

        Args:
            data: ProjectionData containing player information

        Returns:
            str: Path to the team_data folder
        """
        try:
            # Resolve path to team_data folder (configured in config.py)
            shared_team_data_folder = Path(__file__).parent / TEAM_DATA_FOLDER

            # Get team weekly data from ESPN client (should be set by caller)
            if not hasattr(self, 'team_weekly_data') or not self.team_weekly_data:
                self.logger.warning("No team weekly data available for export")
                return ""

            # Save to shared team_data folder
            save_team_weekly_data(str(shared_team_data_folder), self.team_weekly_data)

            self.logger.info(f"Exported team data for {len(self.team_weekly_data)} teams to: {shared_team_data_folder}")
            return str(shared_team_data_folder)

        except Exception as e:
            self.logger.error(f"Error exporting team data to shared folder: {e}")
            raise

    async def export_projected_points_data(self, data: ProjectionData) -> str:
        """
        Export players_projected.csv with projection-only data.

        Creates file from scratch using statSourceId=1 projection values (from
        the projected_weeks dictionary) for ALL weeks 1-17. Does NOT require
        existing file - completely regenerates on each run.

        This ensures players_projected.csv contains only ESPN projection data
        (statSourceId=1), not actual game scores.

        Args:
            data: ProjectionData containing player projections with projected_weeks populated

        Returns:
            str: Path to the created players_projected.csv file

        Raises:
            Exception: For errors during file operations
        """
        try:
            # Path to players_projected.csv
            projected_file_path = Path(__file__).parent.parent / "data" / "players_projected.csv"

            # Ensure directory exists
            projected_file_path.parent.mkdir(parents=True, exist_ok=True)

            # Build rows directly from ESPNPlayerData projected_weeks dictionary
            rows = []
            for player in data.players:
                row = {'id': player.id, 'name': player.name}
                for week in range(1, 18):
                    # Use the projected_weeks dictionary (statSourceId=1 values)
                    row[f'week_{week}_points'] = player.get_week_projected(week) or 0.0
                rows.append(row)

            df = pd.DataFrame(rows)

            # Write to CSV (full recreation)
            async with aiofiles.open(str(projected_file_path), mode='w', newline='', encoding='utf-8') as csvfile:
                await csvfile.write(df.to_csv(index=False))

            self.logger.info(f"Exported {len(df)} players to players_projected.csv (full recreation with projection-only data)")

            return str(projected_file_path)

        except Exception as e:
            self.logger.error(f"Error exporting players_projected.csv: {e}")
            raise

    async def export_all_formats_with_teams(self, data: ProjectionData,
                                           create_csv: bool = True,
                                           create_json: bool = True,
                                           create_excel: bool = True) -> List[str]:
        """
        Export projection data and team data to all formats concurrently.

        Args:
            data: ProjectionData to export
            create_csv: Whether to create CSV files
            create_json: Whether to create JSON files
            create_excel: Whether to create Excel files

        Returns:
            List of file paths created
        """
        try:
            tasks = []

            # Player data exports (same as original)
            if create_json:
                tasks.append(self.export_json(data))
            if create_csv:
                tasks.append(self.export_csv(data))
            if create_excel:
                tasks.append(self.export_excel(data))

            # Always export to shared files for integration
            tasks.append(self.export_to_data(data))

            # Team data exports (new functionality)
            if create_csv:  # Only export teams CSV if CSV creation is enabled
                tasks.append(self.export_teams_csv(data))
            tasks.append(self.export_teams_to_data(data))

            results = await asyncio.gather(*tasks)

            # Filter out None results and return list of paths
            return [path for path in results if path]

        except Exception as e:
            self.logger.error(f"Error in concurrent export with teams: {e}")
            raise