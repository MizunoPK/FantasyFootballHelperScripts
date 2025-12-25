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
from typing import List, Dict, Optional
import csv
import json

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
from config import DEFAULT_FILE_CAPS, CREATE_POSITION_JSON, POSITION_JSON_OUTPUT, CURRENT_NFL_WEEK
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

    async def export_position_json_files(self, data: ProjectionData) -> List[str]:
        """
        Export position-based JSON files concurrently.

        Creates 6 JSON files (one per position: QB, RB, WR, TE, K, DST)
        in POSITION_JSON_OUTPUT folder.

        Spec: specs.md lines 14-19, USER_DECISIONS_SUMMARY.md Decision 1

        Args:
            data: ProjectionData containing player data

        Returns:
            List of file paths created (empty if CREATE_POSITION_JSON=False)
        """
        # Check config toggle (Spec: Decision 1)
        if not CREATE_POSITION_JSON:
            self.logger.info("Position JSON export disabled (CREATE_POSITION_JSON=False)")
            return []

        # Ensure output folder exists and create dedicated file manager (Spec: specs.md output location)
        output_path = Path(POSITION_JSON_OUTPUT)
        output_path.mkdir(parents=True, exist_ok=True)

        # Create dedicated DataFileManager for position JSON exports
        # This ensures files are saved to POSITION_JSON_OUTPUT, not OUTPUT_DIRECTORY
        position_file_manager = DataFileManager(str(output_path), DEFAULT_FILE_CAPS)

        # Create tasks for parallel export (Spec: Reusable Pattern 1 - asyncio.gather)
        positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']
        tasks = []
        for position in positions:
            tasks.append(self._export_single_position_json(data, position, position_file_manager))

        # Execute concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions, log them, return successful paths
        file_paths = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                position = positions[i]
                self.logger.error(f"Failed to export {position} data: {result}", exc_info=result)
            else:
                file_paths.append(result)

        self.logger.info(f"Position JSON export complete: {len(file_paths)}/6 files created")
        return file_paths

    async def _export_single_position_json(self, data: ProjectionData, position: str, file_manager: DataFileManager) -> str:
        """
        Export JSON file for a single position.

        Spec: specs.md lines 14-19, Complete Data Structures section

        Args:
            data: ProjectionData containing all player data
            position: Position code (QB, RB, WR, TE, K, or DST)
            file_manager: DataFileManager for position JSON output folder

        Returns:
            File path of created JSON file
        """
        # Get all fantasy players with drafted state applied
        fantasy_players = self.get_fantasy_players(data)

        # Create mapping from player ID to ESPNPlayerData (for stat extraction)
        espn_player_map = {p.id: p for p in data.players}

        # Filter to position (Spec: specs.md lines 14-19)
        position_players = [p for p in fantasy_players if p.position == position]

        # Transform to JSON structure (Spec: Complete Data Structures)
        players_json = []
        for player in position_players:
            # Get corresponding ESPN data for detailed stats
            espn_data = espn_player_map.get(str(player.id))  # ESPNPlayerData.id is str
            player_json = self._prepare_position_json_data(player, espn_data, position)
            players_json.append(player_json)

        # Wrap in position-specific root key (Spec: example files analysis)
        # Format: {"qb_data": [...]} or {"rb_data": [...]}
        root_key = f"{position.lower()}_data"
        output_data = {root_key: players_json}

        # Save to data/player_data/ folder with fixed filename (no timestamps, no prefix)
        # Matches pattern of players.csv export - each run overwrites previous file
        file_path = Path(__file__).parent / f'../data/player_data/{position.lower()}_data.json'

        try:
            # Ensure the directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Write JSON file asynchronously
            async with aiofiles.open(str(file_path), mode='w', encoding='utf-8') as f:
                json_string = json.dumps(output_data, indent=2, ensure_ascii=False)
                await f.write(json_string)

            self.logger.info(f"Exported {len(players_json)} {position} players to {file_path}")
            return str(file_path)

        except PermissionError as e:
            self.logger.error(f"Permission denied writing to {file_path}: {e}")
            raise
        except OSError as e:
            self.logger.error(f"OS error writing to {file_path}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error exporting position JSON: {e}")
            raise

    def _prepare_position_json_data(self, player: FantasyPlayer, espn_data: Optional[ESPNPlayerData], position: str) -> Dict:
        """
        Transform player data to position-specific JSON structure.

        Spec: specs.md Complete Data Structures section, USER_DECISIONS_SUMMARY.md

        Args:
            player: FantasyPlayer object (has drafted state applied)
            espn_data: ESPNPlayerData object (has raw ESPN data)
            position: Position code (QB, RB, WR, TE, K, DST)

        Returns:
            Dictionary with player data in position-specific JSON format
        """
        # Build common fields (Spec: specs.md lines 24-35)
        json_data = {
            "id": player.id,
            "name": player.name,
            "team": player.team,
            "position": player.position,
            "injury_status": player.injury_status,
            # drafted_by uses get_team_name_for_player() (Spec: Decision 10)
            "drafted_by": self._get_drafted_by(player),
            # locked is boolean (Spec: transformation table)
            "locked": bool(player.locked),
            "average_draft_position": player.average_draft_position,
            "player_rating": player.player_rating,
            # projected_points array (17 elements, Spec: Decision 2) - uses statSourceId=1
            "projected_points": self._get_projected_points_array(espn_data),
            # actual_points array (17 elements, Spec: Decision 5,8,9) - uses statSourceId=0
            "actual_points": self._get_actual_points_array(espn_data)
        }

        # Add position-specific stat arrays (Spec: Complete Data Structures)
        if position == "QB":
            json_data["passing"] = self._extract_passing_stats(espn_data)
            json_data["rushing"] = self._extract_rushing_stats(espn_data)
            json_data["receiving"] = self._extract_receiving_stats(espn_data)
            json_data["misc"] = self._extract_misc_stats(espn_data, include_return_stats=False)
        elif position == "RB":
            json_data["rushing"] = self._extract_rushing_stats(espn_data)
            json_data["receiving"] = self._extract_receiving_stats(espn_data)
            json_data["misc"] = self._extract_misc_stats(espn_data, include_return_stats=False)
        elif position == "WR":
            json_data["receiving"] = self._extract_receiving_stats(espn_data)
            json_data["rushing"] = self._extract_rushing_stats(espn_data)
            json_data["misc"] = self._extract_misc_stats(espn_data, include_return_stats=False)
        elif position == "TE":
            json_data["receiving"] = self._extract_receiving_stats(espn_data)
            json_data["misc"] = self._extract_misc_stats(espn_data, include_return_stats=False)
        elif position == "K":
            json_data["extra_points"] = self._extract_kicking_stats(espn_data)["extra_points"]
            json_data["field_goals"] = self._extract_kicking_stats(espn_data)["field_goals"]
        elif position == "DST":
            json_data["defense"] = self._extract_defense_stats(espn_data)

        return json_data

    def _get_drafted_by(self, player: FantasyPlayer) -> str:
        """
        Get drafted_by field value (Spec: Decision 10).

        Args:
            player: FantasyPlayer with drafted field set

        Returns:
            Team name string or empty string for free agents
        """
        if player.drafted == 0:
            return ""  # Free agent
        elif player.drafted == 2:
            return MY_TEAM_NAME  # User's team
        else:  # drafted == 1
            # Look up team name from DraftedRosterManager
            return self.drafted_roster_manager.get_team_name_for_player(player)

    def _get_projected_points_array(self, espn_data: Optional[ESPNPlayerData]) -> List[float]:
        """
        Get projected points array from ESPN pre-game projections (17 elements, Spec: Decision 2).

        Extracts projected points from statSourceId=1 (pre-game projections).
        This should be DIFFERENT from actual_points (which uses statSourceId=0).

        Args:
            espn_data: ESPNPlayerData object with raw_stats

        Returns:
            List of 17 projected point values (pre-game ESPN projections)
        """
        if espn_data is None or not espn_data.raw_stats:
            return [0.0] * 17

        projected_points = []
        for week in range(1, 18):  # Weeks 1-17
            projected = None
            for stat in espn_data.raw_stats:
                if stat.get('scoringPeriodId') == week and stat.get('statSourceId') == 1:
                    projected = stat.get('appliedTotal')
                    break
            projected_points.append(float(projected) if projected else 0.0)
        return projected_points

    def _get_actual_points_array(self, espn_data: Optional[ESPNPlayerData]) -> List[float]:
        """
        Get actual points array from ESPN post-game results (17 elements, Spec: Decision 5,8,9).

        Extracts actual points from statSourceId=0 (post-game results).
        This should be DIFFERENT from projected_points (which uses statSourceId=1).

        IMPORTANT: Only uses statSourceId=0 data for weeks <= CURRENT_NFL_WEEK.
        ESPN pre-populates statSourceId=0 with projection data for future weeks,
        so we filter to only completed weeks to avoid showing "actual" data for
        games that haven't been played yet.

        Args:
            espn_data: ESPNPlayerData object with raw_stats

        Returns:
            List of 17 actual point values (what actually happened in games)
        """
        if espn_data is None or not espn_data.raw_stats:
            return [0.0] * 17

        actual_points = []
        for week in range(1, 18):  # Weeks 1-17
            actual = None
            # Only use statSourceId=0 for completed weeks (weeks < CURRENT_NFL_WEEK)
            # ESPN pre-populates statSourceId=0 for current and future weeks with projections
            if week < CURRENT_NFL_WEEK:
                for stat in espn_data.raw_stats:
                    if stat.get('scoringPeriodId') == week and stat.get('statSourceId') == 0:
                        actual = stat.get('appliedTotal')
                        break
            actual_points.append(float(actual) if actual else 0.0)
        return actual_points

    def _extract_stat_value(self, raw_stats: List[Dict], week: int, stat_id: str) -> float:
        """
        Extract a single stat value from raw_stats array for a specific week.

        Pattern from compile_historical_data.py:
        - Find stat entry with scoringPeriodId == week AND statSourceId == 0
        - Extract from appliedStats dict using stat_id as string key
        - Return 0.0 if not found

        IMPORTANT: Only extracts stats for weeks <= CURRENT_NFL_WEEK to avoid
        showing "actual" stats for games that haven't been played yet.

        Args:
            raw_stats: List of stat dictionaries from ESPN API
            week: Week number (1-17)
            stat_id: ESPN stat ID as string (e.g., '0', '1', '3')

        Returns:
            Stat value as float, or 0.0 if not found
        """
        # Only extract stats for completed weeks (weeks < CURRENT_NFL_WEEK)
        # ESPN pre-populates statSourceId=0 for current and future weeks
        if week >= CURRENT_NFL_WEEK:
            return 0.0

        for stat in raw_stats:
            if stat.get('scoringPeriodId') == week and stat.get('statSourceId') == 0:
                # ESPN uses 'stats' not 'appliedStats' in the API response
                stats_dict = stat.get('stats', {})
                value = stats_dict.get(stat_id, 0.0)
                return float(value) if value else 0.0
        return 0.0

    def _extract_combined_stat(self, raw_stats: List[Dict], week: int, stat_ids: List[str]) -> float:
        """
        Sum multiple stat IDs for a specific week.

        Used for combined stats like return yards (stat_114 + stat_115) or
        two-point conversions (multiple stat IDs).

        Args:
            raw_stats: List of stat dictionaries from ESPN API
            week: Week number (1-17)
            stat_ids: List of ESPN stat IDs to sum (as strings)

        Returns:
            Sum of all stat values as float
        """
        total = 0.0
        for stat_id in stat_ids:
            total += self._extract_stat_value(raw_stats, week, stat_id)
        return total

    def _extract_passing_stats(self, espn_data: Optional[ESPNPlayerData]) -> Dict:
        """Extract passing stats (Spec: specs.md lines 351-358)."""
        if espn_data is None or not espn_data.raw_stats:
            return {
                "completions": [0.0] * 17,
                "attempts": [0.0] * 17,
                "pass_yds": [0.0] * 17,
                "pass_tds": [0.0] * 17,
                "interceptions": [0.0] * 17,
                "sacks": [0.0] * 17
            }

        return {
            "completions": [self._extract_stat_value(espn_data.raw_stats, week, '1') for week in range(1, 18)],
            "attempts": [self._extract_stat_value(espn_data.raw_stats, week, '0') for week in range(1, 18)],
            "pass_yds": [self._extract_stat_value(espn_data.raw_stats, week, '3') for week in range(1, 18)],
            "pass_tds": [self._extract_stat_value(espn_data.raw_stats, week, '4') for week in range(1, 18)],
            "interceptions": [self._extract_stat_value(espn_data.raw_stats, week, '20') for week in range(1, 18)],
            "sacks": [self._extract_stat_value(espn_data.raw_stats, week, '64') for week in range(1, 18)]
        }

    def _extract_rushing_stats(self, espn_data: Optional[ESPNPlayerData]) -> Dict:
        """Extract rushing stats (Spec: specs.md lines 359-363)."""
        if espn_data is None or not espn_data.raw_stats:
            return {
                "attempts": [0.0] * 17,
                "rush_yds": [0.0] * 17,
                "rush_tds": [0.0] * 17
            }

        return {
            "attempts": [self._extract_stat_value(espn_data.raw_stats, week, '23') for week in range(1, 18)],
            "rush_yds": [self._extract_stat_value(espn_data.raw_stats, week, '24') for week in range(1, 18)],
            "rush_tds": [self._extract_stat_value(espn_data.raw_stats, week, '25') for week in range(1, 18)]
        }

    def _extract_receiving_stats(self, espn_data: Optional[ESPNPlayerData]) -> Dict:
        """Extract receiving stats (Spec: specs.md lines 364-369, Decision 3)."""
        if espn_data is None or not espn_data.raw_stats:
            return {
                "targets": [0.0] * 17,
                "receiving_yds": [0.0] * 17,
                "receiving_tds": [0.0] * 17,
                "receptions": [0.0] * 17
            }

        return {
            "targets": [self._extract_stat_value(espn_data.raw_stats, week, '58') for week in range(1, 18)],
            "receiving_yds": [self._extract_stat_value(espn_data.raw_stats, week, '42') for week in range(1, 18)],
            "receiving_tds": [self._extract_stat_value(espn_data.raw_stats, week, '43') for week in range(1, 18)],
            "receptions": [self._extract_stat_value(espn_data.raw_stats, week, '53') for week in range(1, 18)]
        }

    def _extract_misc_stats(self, espn_data: Optional[ESPNPlayerData], include_return_stats: bool = False) -> Dict:
        """
        Extract misc stats (Spec: specs.md lines 370-373, Decision 6).

        Args:
            espn_data: ESPNPlayerData object
            include_return_stats: If True, include ret_yds and ret_tds (DST only)

        Returns:
            Dictionary with misc stats
        """
        if espn_data is None or not espn_data.raw_stats:
            misc_stats = {"fumbles": [0.0] * 17}
            if include_return_stats:
                misc_stats["ret_yds"] = [0.0] * 17
                misc_stats["ret_tds"] = [0.0] * 17
            return misc_stats

        # Only fumbles - two_pt removed per user decision
        misc_stats = {
            "fumbles": [self._extract_stat_value(espn_data.raw_stats, week, '68') for week in range(1, 18)]
        }

        # Only include return stats for DST (Spec: Decision 6)
        if include_return_stats:
            misc_stats["ret_yds"] = [self._extract_combined_stat(espn_data.raw_stats, week, ['114', '115']) for week in range(1, 18)]
            misc_stats["ret_tds"] = [self._extract_combined_stat(espn_data.raw_stats, week, ['101', '102']) for week in range(1, 18)]

        return misc_stats

    def _extract_kicking_stats(self, espn_data: Optional[ESPNPlayerData]) -> Dict:
        """Extract kicking stats (Spec: specs.md lines 430-437, Decision 7)."""
        if espn_data is None or not espn_data.raw_stats:
            return {
                "extra_points": {
                    "made": [0.0] * 17,
                    "missed": [0.0] * 17
                },
                "field_goals": {
                    "made": [0.0] * 17,
                    "missed": [0.0] * 17
                }
            }

        return {
            "extra_points": {
                "made": [self._extract_stat_value(espn_data.raw_stats, week, '86') for week in range(1, 18)],
                "missed": [self._extract_stat_value(espn_data.raw_stats, week, '88') for week in range(1, 18)]
            },
            "field_goals": {
                "made": [self._extract_stat_value(espn_data.raw_stats, week, '83') for week in range(1, 18)],
                "missed": [self._extract_stat_value(espn_data.raw_stats, week, '85') for week in range(1, 18)]
            }
        }

    def _extract_defense_stats(self, espn_data: Optional[ESPNPlayerData]) -> Dict:
        """Extract defense stats (Spec: specs.md lines 461-472)."""
        if espn_data is None or not espn_data.raw_stats:
            return {
                "yds_g": [0.0] * 17,
                "pts_g": [0.0] * 17,
                "def_td": [0.0] * 17,
                "sacks": [0.0] * 17,
                "safety": [0.0] * 17,
                "interceptions": [0.0] * 17,
                "forced_fumble": [0.0] * 17,
                "fumbles_recovered": [0.0] * 17,
                "ret_yds": [0.0] * 17,
                "ret_tds": [0.0] * 17
            }

        return {
            "yds_g": [self._extract_stat_value(espn_data.raw_stats, week, '127') for week in range(1, 18)],
            "pts_g": [self._extract_stat_value(espn_data.raw_stats, week, '120') for week in range(1, 18)],
            "def_td": [self._extract_stat_value(espn_data.raw_stats, week, '94') for week in range(1, 18)],
            "sacks": [self._extract_stat_value(espn_data.raw_stats, week, '99') for week in range(1, 18)],
            "safety": [self._extract_stat_value(espn_data.raw_stats, week, '98') for week in range(1, 18)],
            "interceptions": [self._extract_stat_value(espn_data.raw_stats, week, '95') for week in range(1, 18)],
            "forced_fumble": [self._extract_stat_value(espn_data.raw_stats, week, '106') for week in range(1, 18)],
            "fumbles_recovered": [self._extract_stat_value(espn_data.raw_stats, week, '96') for week in range(1, 18)],
            "ret_yds": [self._extract_combined_stat(espn_data.raw_stats, week, ['114', '115']) for week in range(1, 18)],
            "ret_tds": [self._extract_combined_stat(espn_data.raw_stats, week, ['101', '102']) for week in range(1, 18)]
        }

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