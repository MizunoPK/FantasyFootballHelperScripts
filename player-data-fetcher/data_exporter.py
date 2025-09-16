#!/usr/bin/env python3
"""
Data Export Module for NFL Fantasy Football Data

This module handles all data export operations (CSV, JSON, Excel) with
async file I/O for better performance.

Author: Generated for NFL Fantasy Data Collection
Last Updated: September 2025
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import csv

import aiofiles
import pandas as pd

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from models import ProjectionData, ESPNPlayerData
from shared_files.FantasyPlayer import FantasyPlayer
from player_data_constants import EXCEL_POSITION_SHEETS, EXPORT_COLUMNS, PRESERVE_DRAFTED_VALUES, PRESERVE_LOCKED_VALUES, DRAFT_HELPER_PLAYERS_FILE, SKIP_DRAFTED_PLAYER_UPDATES


class DataExporter:
    """Handles exporting projection data to various formats with async I/O"""
    
    def __init__(self, output_dir: str, create_latest_files: bool = True):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.create_latest_files = create_latest_files
        self.logger = logging.getLogger(__name__)
        
        # Load existing drafted and locked values if preservation is enabled
        self.existing_drafted_values = {}
        self.existing_locked_values = {}
        if PRESERVE_DRAFTED_VALUES:
            self._load_existing_drafted_values()
        if PRESERVE_LOCKED_VALUES:
            self._load_existing_locked_values()
    
    async def export_json(self, data: ProjectionData) -> str:
        """Export data to JSON format asynchronously"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_suffix = f"_{data.scoring_format}"
        
        filename = f"nfl_projections_season_{timestamp}{filename_suffix}.json"
        filepath = self.output_dir / filename
        
        # Convert to JSON-serializable format
        json_data = {
            "season": data.season,
            "scoring_format": data.scoring_format,
            "total_players": data.total_players,
            "generated_at": data.generated_at.isoformat(),
            "players": [player.model_dump() for player in data.players]
        }
        
        # Write JSON file asynchronously
        async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(json_data, indent=2, default=str))
        
        # Create latest version if requested
        if self.create_latest_files:
            latest_filename = f"nfl_projections_latest_season.json"
            latest_filepath = self.output_dir / latest_filename
            
            async with aiofiles.open(latest_filepath, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(json_data, indent=2, default=str))
        
        return str(filepath)
    
    async def export_csv(self, data: ProjectionData) -> str:
        """Export data to CSV format asynchronously"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_suffix = f"_{data.scoring_format}"
        
        filename = f"nfl_projections_season_{timestamp}{filename_suffix}.csv"
        filepath = self.output_dir / filename
        
        # Prepare DataFrame with standard column ordering
        df = self._prepare_export_dataframe(data)
        
        # Write CSV asynchronously using asyncio thread pool  
        await asyncio.get_event_loop().run_in_executor(
            None, lambda: df.to_csv(str(filepath), index=False)
        )
        
        # Create latest version if requested
        if self.create_latest_files:
            latest_filename = f"nfl_projections_latest_season.csv"
            latest_filepath = self.output_dir / latest_filename
            
            await asyncio.get_event_loop().run_in_executor(
                None, lambda: df.to_csv(str(latest_filepath), index=False)
            )
        
        return str(filepath)
    
    async def export_excel(self, data: ProjectionData) -> str:
        """Export data to Excel format with position sheets asynchronously"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_suffix = f"_{data.scoring_format}"
        
        filename = f"nfl_projections_season_{timestamp}{filename_suffix}.xlsx"
        filepath = self.output_dir / filename
        
        # Prepare DataFrame with standard column ordering
        df = self._prepare_export_dataframe(data)
        
        # Create Excel writer and write sheets asynchronously
        await asyncio.get_event_loop().run_in_executor(
            None, self._write_excel_sheets, df, str(filepath)
        )
        
        # Create latest version if requested
        if self.create_latest_files:
            latest_filename = f"nfl_projections_latest_season.xlsx"
            latest_filepath = self.output_dir / latest_filename
            
            await asyncio.get_event_loop().run_in_executor(
                None, self._write_excel_sheets, df, str(latest_filepath)
            )
        
        return str(filepath)
    
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
    
    def _load_existing_drafted_values(self):
        """Load existing drafted values from draft helper players file"""
        # Resolve path relative to the player-data-fetcher directory (parent of output_dir)
        draft_file_path = Path(__file__).parent / DRAFT_HELPER_PLAYERS_FILE
        
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
        draft_file_path = Path(__file__).parent / DRAFT_HELPER_PLAYERS_FILE
        
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

    def _merge_skipped_drafted_players(self, espn_fantasy_players: List[FantasyPlayer]) -> List[FantasyPlayer]:
        """Merge ESPN players with drafted players that were skipped during API fetching"""
        # Create a set of existing ESPN player IDs for fast lookup
        espn_player_ids = {player.id for player in espn_fantasy_players}

        # Load existing players from CSV
        draft_file_path = Path(__file__).parent / DRAFT_HELPER_PLAYERS_FILE
        skipped_players = []

        try:
            with open(draft_file_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    player_id = row.get('id', '')
                    drafted_value = int(row.get('drafted', 0))

                    # Only include drafted=1 players that were skipped (not in ESPN data)
                    if drafted_value == 1 and player_id not in espn_player_ids:
                        # Create FantasyPlayer from existing CSV data
                        fantasy_player = FantasyPlayer(
                            id=player_id,
                            name=row.get('name', ''),
                            team=row.get('team', ''),
                            position=row.get('position', ''),
                            bye_week=int(row.get('bye_week', 0)),
                            drafted=drafted_value,
                            locked=int(row.get('locked', 0)),
                            fantasy_points=float(row.get('fantasy_points', 0.0)),
                            average_draft_position=float(row.get('average_draft_position', 999.0)) if row.get('average_draft_position') else 999.0,
                            injury_status=row.get('injury_status', 'ACTIVE')
                        )
                        skipped_players.append(fantasy_player)

            if skipped_players:
                self.logger.info(f"Merged {len(skipped_players)} drafted players that were skipped during API fetching")
                return espn_fantasy_players + skipped_players

        except FileNotFoundError:
            self.logger.warning(f"Players file not found at {draft_file_path} - cannot merge skipped drafted players")
        except Exception as e:
            self.logger.error(f"Error merging skipped drafted players: {e}")

        return espn_fantasy_players

    def _espn_player_to_fantasy_player(self, player_data: ESPNPlayerData) -> FantasyPlayer:
        """Convert ESPNPlayerData to FantasyPlayer object"""
        
        # Use existing drafted value if preservation is enabled, otherwise use default (0)
        drafted_value = player_data.drafted  # Default from ESPN (always 0)
        if PRESERVE_DRAFTED_VALUES and player_data.id in self.existing_drafted_values:
            drafted_value = self.existing_drafted_values[player_data.id]
        
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
            injury_status=player_data.injury_status
        )
    
    def get_fantasy_players(self, data: ProjectionData) -> List[FantasyPlayer]:
        """Convert ProjectionData to list of FantasyPlayer objects"""
        fantasy_players = [self._espn_player_to_fantasy_player(player) for player in data.players]

        # Add drafted players that were skipped during ESPN data fetching (optimization)
        if SKIP_DRAFTED_PLAYER_UPDATES:
            fantasy_players = self._merge_skipped_drafted_players(fantasy_players)

        return fantasy_players
    
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
    
    async def export_to_shared_files(self, data: ProjectionData) -> str:
        """Export data to shared_files/players.csv for use by draft helper"""
        # Resolve path to shared_files/players.csv
        draft_file_path = Path(__file__).parent / DRAFT_HELPER_PLAYERS_FILE
        
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