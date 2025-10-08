#!/usr/bin/env python3
"""
Data Export Module for NFL Game Scores

This module handles all data export operations (CSV, JSON, Excel) with
async file I/O for better performance.

Author: Kai Mizuno
Last Updated: September 2025
"""

import asyncio
from pathlib import Path
from typing import List, Optional

import pandas as pd

from nfl_scores_models import WeeklyScores, GameScore
from scores_constants import NFL_TEAM_NAMES
from config import DEFAULT_FILE_CAPS

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.data_file_manager import DataFileManager
from utils.LoggingManager import get_logger


class ScoresDataExporter:
    """Handles exporting NFL game scores to various formats with async I/O"""
    
    def __init__(self, output_dir: str, create_latest_files: bool = True):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.create_latest_files = create_latest_files
        self.logger = get_logger()

        # Initialize file manager for automatic file caps
        self.file_manager = DataFileManager(str(self.output_dir), DEFAULT_FILE_CAPS)

    def _get_file_prefix(self, base_prefix: str, weekly_scores: 'WeeklyScores') -> str:
        """Generate file prefix with week information"""
        week_suffix = f"_week{weekly_scores.week}" if weekly_scores.week > 0 else "_recent"
        return f"{base_prefix}{week_suffix}"
    
    async def export_json(self, weekly_scores: WeeklyScores, file_prefix: str = "nfl_scores") -> Optional[str]:
        """Export weekly scores to JSON format asynchronously"""
        try:
            # Convert to JSON-serializable format
            json_data = {
                "week": weekly_scores.week,
                "season": weekly_scores.season,
                "season_type": weekly_scores.season_type,
                "total_games": weekly_scores.total_games,
                "completed_games": weekly_scores.completed_games,
                "generated_at": weekly_scores.generated_at.isoformat(),
                "games": [self._game_to_dict(game) for game in weekly_scores.games]
            }

            # Use enhanced file manager for consistent JSON export
            prefix = self._get_file_prefix(file_prefix, weekly_scores)
            timestamped_path, latest_path = self.file_manager.save_json_data(
                json_data, prefix, create_latest=self.create_latest_files
            )

            return str(timestamped_path)
        except Exception as e:
            self.logger.error(f"Error exporting JSON: {e}")
            return None
    
    async def export_csv(self, weekly_scores: WeeklyScores, file_prefix: str = "nfl_scores") -> Optional[str]:
        """Export weekly scores to CSV format asynchronously"""
        try:
            # Convert to DataFrame
            df = self._create_dataframe(weekly_scores.games)

            # Use enhanced file manager for consistent CSV export
            prefix = self._get_file_prefix(file_prefix, weekly_scores)
            timestamped_path, latest_path = await self.file_manager.save_dataframe_csv(
                df, prefix, create_latest=self.create_latest_files
            )

            return str(timestamped_path)
        except Exception as e:
            self.logger.error(f"Error exporting CSV: {e}")
            return None
    
    async def export_excel(self, weekly_scores: WeeklyScores, file_prefix: str = "nfl_scores") -> Optional[str]:
        """Export weekly scores to Excel format with multiple sheets asynchronously"""
        try:
            # Convert to DataFrame
            df = self._create_dataframe(weekly_scores.games)

            # Use enhanced file manager for path generation, but custom Excel writing
            prefix = self._get_file_prefix(file_prefix, weekly_scores)
            timestamped_path = self.file_manager.get_timestamped_path(prefix, 'xlsx')

            # Create Excel writer and write sheets asynchronously
            await asyncio.get_event_loop().run_in_executor(
                None, self._write_excel_sheets, df, str(timestamped_path), weekly_scores
            )

            # Create latest version if requested
            if self.create_latest_files:
                latest_path = self.file_manager.get_latest_path(prefix, 'xlsx')
                await asyncio.get_event_loop().run_in_executor(
                    None, self._write_excel_sheets, df, str(latest_path), weekly_scores
                )

            # Enforce file caps after successful export
            deleted_files = self.file_manager.enforce_file_caps(str(timestamped_path))
            if deleted_files:
                self.logger.info(f"File caps enforced for Excel: {deleted_files}")

            return str(timestamped_path)
        except Exception as e:
            self.logger.error(f"Error exporting Excel: {e}")
            return None
    
    async def export_condensed_excel(self, weekly_scores: WeeklyScores, file_prefix: str = "nfl_scores_condensed") -> Optional[str]:
        """Export condensed weekly scores to Excel format with team comparison sheets"""
        try:
            # Create condensed data
            condensed_data = self._create_condensed_dataframe(weekly_scores.games)

            # Use enhanced file manager for path generation, but custom Excel writing
            prefix = self._get_file_prefix(file_prefix, weekly_scores)
            timestamped_path = self.file_manager.get_timestamped_path(prefix, 'xlsx')

            # Write condensed Excel file
            await asyncio.get_event_loop().run_in_executor(
                None, self._write_condensed_excel_sheets, condensed_data, str(timestamped_path), weekly_scores
            )

            # Create latest version if requested
            if self.create_latest_files:
                latest_path = self.file_manager.get_latest_path(prefix, 'xlsx')
                await asyncio.get_event_loop().run_in_executor(
                    None, self._write_condensed_excel_sheets, condensed_data, str(latest_path), weekly_scores
                )

            # Enforce file caps after successful export
            deleted_files = self.file_manager.enforce_file_caps(str(timestamped_path))
            if deleted_files:
                self.logger.info(f"File caps enforced for condensed Excel: {deleted_files}")

            return str(timestamped_path)
        except Exception as e:
            self.logger.error(f"Error exporting condensed Excel: {e}")
            return None
    
    def _create_dataframe(self, games: List[GameScore]) -> pd.DataFrame:
        """Convert list of GameScore objects to pandas DataFrame"""
        game_dicts = [self._game_to_dict(game) for game in games]
        return pd.DataFrame(game_dicts)
    
    def _create_condensed_dataframe(self, games: List[GameScore]) -> pd.DataFrame:
        """Create a condensed DataFrame with team-centric format (one row per team)"""
        # Create abbreviation to team name mapping from played games
        abbrev_to_name = {}
        teams_played = set()
        
        # Create team-centric data structure from actual games
        team_data = []
        
        for game in games:
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
                'Opponent': game.home_team.name,
                'Points Scored': game.away_score,
                'Points Allowed': game.home_score
            })
        
        # Get the week number from first game (for bye week handling)
        week_num = games[0].week if games else 0
        
        # Add bye week teams if we have a specific week
        if week_num > 0:
            try:
                # Try to load bye weeks data from shared_files directory
                bye_weeks_path = self.output_dir.parent / "shared_files" / "bye_weeks.csv"
                if bye_weeks_path.exists():
                    bye_weeks_df = pd.read_csv(bye_weeks_path)
                    bye_teams = bye_weeks_df[bye_weeks_df['ByeWeek'] == week_num]['Team'].tolist()
                    
                    # Add missing teams to abbrev_to_name mapping using constants
                    for abbrev, name in NFL_TEAM_NAMES.items():
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
        
        return pd.DataFrame(team_data)
    
    def _game_to_dict(self, game: GameScore) -> dict:
        """Convert GameScore object to dictionary for JSON serialization"""
        return {
            # Basic game info
            'game_id': game.game_id,
            'date': game.date.isoformat(),
            'week': game.week,
            'season': game.season,
            'season_type': game.season_type,
            
            # Teams
            'home_team_id': game.home_team.id,
            'home_team_name': game.home_team.display_name,
            'home_team_abbr': game.home_team.abbreviation,
            'home_team_record': game.home_team.record,
            'away_team_id': game.away_team.id,
            'away_team_name': game.away_team.display_name,
            'away_team_abbr': game.away_team.abbreviation,
            'away_team_record': game.away_team.record,
            
            # Scores
            'home_score': game.home_score,
            'away_score': game.away_score,
            'total_points': game.total_points,
            'point_difference': game.point_difference,
            'winning_team': game.winning_team,
            
            # Status
            'status': game.status,
            'status_detail': game.status_detail,
            'is_completed': game.is_completed,
            'is_overtime': game.is_overtime,
            
            # Venue
            'venue_name': game.venue_name,
            'venue_city': game.venue_city,
            'venue_state': game.venue_state,
            'venue_capacity': game.venue_capacity,
            'attendance': game.attendance,
            
            # Weather
            'temperature': game.temperature,
            'weather_description': game.weather_description,
            'wind_speed': game.wind_speed,
            
            # Media & Betting
            'tv_network': game.tv_network,
            'home_team_odds': game.home_team_odds,
            'away_team_odds': game.away_team_odds,
            'over_under': game.over_under,
            
            # Statistics
            'home_total_yards': game.home_total_yards,
            'away_total_yards': game.away_total_yards,
            'home_turnovers': game.home_turnovers,
            'away_turnovers': game.away_turnovers,
            
            # Quarter scores
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
            
            # Metadata
            'updated_at': game.updated_at.isoformat()
        }
    
    def _write_excel_sheets(self, df: pd.DataFrame, filepath: str, weekly_scores: WeeklyScores) -> None:
        """Write Excel file with multiple sheets (sync helper)"""
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # Main games sheet
            df.to_excel(writer, sheet_name='All Games', index=False)

            # Completed games sheet (only if DataFrame has data and 'is_completed' column exists)
            if not df.empty and 'is_completed' in df.columns:
                completed_df = df[df['is_completed'] == True].copy()
                if not completed_df.empty:
                    completed_df.to_excel(writer, sheet_name='Completed Games', index=False)

            # Summary sheet
            self._create_summary_sheet(writer, weekly_scores, df)

            # High-scoring games sheet (only if DataFrame has data and 'total_points' column exists)
            if not df.empty and 'total_points' in df.columns:
                high_scoring = df[df['total_points'] >= 50].copy()
                if not high_scoring.empty:
                    high_scoring = high_scoring.sort_values('total_points', ascending=False)
                    high_scoring.to_excel(writer, sheet_name='High Scoring Games', index=False)
    
    def _write_condensed_excel_sheets(self, df: pd.DataFrame, filepath: str, weekly_scores: WeeklyScores) -> None:
        """Write condensed Excel file with team-centric format (sync helper)"""
        # Simple single-sheet format like the old version
        df.to_excel(filepath, index=False, engine='openpyxl')
    
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
    
    async def export_all_formats(self, weekly_scores: WeeklyScores,
                                create_csv: bool = True,
                                create_json: bool = True, 
                                create_excel: bool = True,
                                create_condensed_excel: bool = False,
                                file_prefix: str = "nfl_scores") -> List[str]:
        """Export weekly scores to all requested formats concurrently"""
        tasks = []
        
        if create_json:
            tasks.append(self.export_json(weekly_scores, file_prefix))
        if create_csv:
            tasks.append(self.export_csv(weekly_scores, file_prefix))
        if create_excel:
            tasks.append(self.export_excel(weekly_scores, file_prefix))
        if create_condensed_excel:
            tasks.append(self.export_condensed_excel(weekly_scores, file_prefix + "_condensed"))
        
        if not tasks:
            return []
        
        # Run all exports concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and log them
        output_files = []
        for result in results:
            if isinstance(result, Exception):
                self.logger.error(f"Export failed: {result}")
            else:
                output_files.append(result)
        
        return output_files