#!/usr/bin/env python3
"""
NFL Player Projections Data Collection Script - ESPN API
====================================================================

Retrieves fantasy football projections using ESPN's free public API.
No signup or API keys required.

Usage:
    python player_data_fetcher_main.py
    python player_data_fetcher_main.py --enable-log-file

Author: Kai Mizuno
"""

import argparse
import asyncio
import datetime
import json
import logging
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import pandas as pd

from utils.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import setup_logger, get_logger

from player_data_fetcher.player_data_models import ScoringFormat, ProjectionData
from player_data_fetcher.espn_client import ESPNClient
from player_data_fetcher.player_data_exporter import DataExporter

from player_data_fetcher.config import LOG_NAME, LOGGING_FORMAT


MIN_EXPECTED_PLAYER_COUNT = 100
POSITION_CODES = ('qb', 'rb', 'wr', 'te', 'k', 'dst')


@dataclass
class Settings:
    """
    Application settings passed via run_player_fetcher.py CLI args.

    Defaults match historical config.py values. All CLI-configurable values
    are managed via argparse in run_player_fetcher.py; these defaults apply
    only for direct invocation (python player_data_fetcher_main.py).
    """

    scoring_format: ScoringFormat = ScoringFormat.PPR

    season: int = 2025
    current_nfl_week: int = 17

    request_timeout: int = 30
    rate_limit_delay: float = 0.2
    espn_player_limit: int = 2000

    position_json_output: str = '../data/player_data'
    team_data_folder: str = '../data/team_data'
    game_data_csv: str = '../data/game_data.csv'
    enable_historical_save: bool = False
    enable_game_data: bool = True

    load_drafted_data: bool = True
    drafted_data_path: str = '../data/drafted_data.csv'
    my_team_name: str = 'Sea Sharp'

    progress_frequency: int = 10
    log_level: str = 'INFO'
    logging_to_file: bool = False

    e2e_test: bool = False

    def validate_settings(self) -> None:
        """Validate settings and warn about potential issues"""
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


def create_settings_from_dict(args_dict: dict) -> Settings:
    """
    Create Settings from dictionary provided by run_player_fetcher.py.

    Args:
        args_dict: Dictionary with all required settings keys (from create_settings_dict() in runner)

    Returns:
        Settings instance with values from args_dict
    """
    return Settings(
        season=args_dict['season'],
        current_nfl_week=args_dict['current_nfl_week'],
        request_timeout=args_dict['request_timeout'],
        rate_limit_delay=args_dict['rate_limit_delay'],
        espn_player_limit=args_dict['espn_player_limit'],
        position_json_output=args_dict['position_json_output'],
        team_data_folder=args_dict['team_data_folder'],
        game_data_csv=args_dict['game_data_csv'],
        enable_historical_save=args_dict['enable_historical_save'],
        enable_game_data=args_dict['enable_game_data'],
        load_drafted_data=args_dict['load_drafted_data'],
        drafted_data_path=args_dict['drafted_data_path'],
        my_team_name=args_dict['my_team_name'],
        progress_frequency=args_dict['progress_frequency'],
        log_level=args_dict['log_level'],
        logging_to_file=args_dict['logging_to_file'],
        e2e_test=args_dict['e2e_test'],
        scoring_format=ScoringFormat(args_dict['scoring_format']),
    )


class NFLProjectionsCollector:
    """Main collector class that coordinates data collection and export"""


    def __init__(self, settings: Settings):
        """
        Initialize the NFL projections collector.

        Args:
            settings: Application settings including API configuration and output options
        """
        self.settings = settings
        self.logger = get_logger()

        self.script_dir = Path(__file__).parent

        schedule_path = self.script_dir.parent / "data" / "season_schedule.csv"
        if not schedule_path.exists():
            error_msg = (
                f"Error: season_schedule.csv not found at {schedule_path}\n"
                "Please run run_schedule_fetcher.py first to generate this file:\n"
                "  python run_scores_fetcher.py"
            )
            self.logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        self.bye_weeks = self._derive_bye_weeks_from_schedule(schedule_path)

        self.team_rankings = {}
        self.current_week_schedule = {}
        self.position_defense_rankings = {}
        self.team_weekly_data = {}

        output_path = self.script_dir / "data"
        self.exporter = DataExporter(
            output_dir=str(output_path),
            current_nfl_week=self.settings.current_nfl_week,
            position_json_output=self.settings.position_json_output,
            team_data_folder=self.settings.team_data_folder,
            load_drafted_data=self.settings.load_drafted_data,
            drafted_data_path=self.settings.drafted_data_path,
            my_team_name=self.settings.my_team_name,
        )
        
        self.logger.info("Using ESPN hidden API - free but unofficial and may change")
    
    def _derive_bye_weeks_from_schedule(self, schedule_path: Path) -> Dict[str, int]:
        """
        Derive bye week schedule from season_schedule.csv.

        Bye weeks are identified by looking for entries where the opponent field
        is empty (bye week entries have format: week,team,).

        Args:
            schedule_path: Path to season_schedule.csv file

        Returns:
            Dict mapping team abbreviation to bye week number (1-17)
            Example: {'KC': 10, 'SF': 9, 'BUF': 7}

        File format (data/season_schedule.csv):
            week,team,opponent
            1,ARI,NO
            1,ATL,TB
            10,KC,          # Bye week (empty opponent)
            ...
        """
        import pandas as pd

        bye_weeks = {}

        try:
            df = pd.read_csv(schedule_path)

            teams = df['team'].unique()

            if len(teams) != 32:
                self.logger.warning(f"Expected 32 NFL teams, found {len(teams)}")

            for team in teams:
                team_entries = df[df['team'] == team]

                bye_entries = team_entries[
                    team_entries['opponent'].isna() |
                    (team_entries['opponent'].astype(str).str.strip() == '')
                ]

                if len(bye_entries) == 1:
                    bye_weeks[team] = int(bye_entries['week'].iloc[0])
                elif len(bye_entries) == 0:
                    self.logger.warning(f"Team {team} has no bye week entry in schedule")
                else:
                    self.logger.warning(f"Team {team} has multiple bye week entries: weeks {list(bye_entries['week'])}")
                    bye_weeks[team] = int(bye_entries['week'].iloc[0])

            self.logger.info(f"Derived bye weeks for {len(bye_weeks)} teams from schedule")
            self.logger.debug(f"Bye weeks data: {bye_weeks}")

        except Exception as e:
            self.logger.error(f"Failed to derive bye weeks from {schedule_path}: {e}")
            raise

        return bye_weeks


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
        client = self._get_api_client()

        client.bye_weeks = self.bye_weeks

        async with client.session():
            results = {}

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

                team_rankings = client.team_rankings
                current_week_schedule = client.current_week_schedule
                position_defense_rankings = client.position_defense_rankings
                self.logger.info(f"Collected team rankings for {len(team_rankings)} teams")
                self.logger.info(f"Collected current week schedule for {len(current_week_schedule)} teams")
                self.logger.info(f"Collected position defense rankings for {len(position_defense_rankings)} teams")

                self.team_rankings = team_rankings
                self.current_week_schedule = current_week_schedule
                self.position_defense_rankings = position_defense_rankings

                self.team_weekly_data = client._collect_team_weekly_data(
                    season_projections,
                    client.full_season_schedule,
                    self.settings.current_nfl_week
                )
                self.logger.info(f"Collected team weekly data for {len(self.team_weekly_data)} teams")

            except Exception as e:
                self.logger.error(f"Failed to collect season projections: {e}")

            return results
    
    def _get_api_client(self) -> ESPNClient:
        """Get ESPN API client"""
        return ESPNClient(self.settings)


    async def export_data(self, projection_data: Dict[str, ProjectionData]) -> List[str]:
        """
        Export all collected data to position JSON and team data formats.

        Exports to multiple destinations:
        1. Position JSON files in data/player_data/ (qb_data.json, rb_data.json, etc.)
        2. Team data folder in data/team_data/ (per-team historical rankings as CSV)

        Args:
            projection_data: Dict containing ProjectionData objects to export

        Returns:
            List of file paths created during export
        """
        self.exporter.set_team_rankings(self.team_rankings)
        self.exporter.set_current_week_schedule(self.current_week_schedule)
        self.exporter.set_position_defense_rankings(self.position_defense_rankings)
        self.exporter.set_team_weekly_data(self.team_weekly_data)

        output_files = []

        for data_type, data in projection_data.items():
            try:
                position_json_files = await self.exporter.export_position_json_files(data)
                if position_json_files:
                    output_files.extend(position_json_files)
                    self.logger.info(f"Exported {len(position_json_files)} position-based JSON files")
            except Exception as e:
                self.logger.error(f"Error exporting position JSON files: {e}")

            try:
                team_data_path = await self.exporter.export_teams_to_data(data)
                if team_data_path:
                    output_files.append(team_data_path)
                    self.logger.info(f"Exported team data to: {team_data_path}")
            except Exception as e:
                self.logger.error(f"Error exporting team data: {e}")

        return output_files

    def save_to_historical_data(self) -> bool:
        """
        Save current data files to historical data folder for the current week.

        Checks config flag ENABLE_HISTORICAL_DATA_SAVE before proceeding.
        Checks if data/historical_data/{Season}/{WeekNumber}/ exists.
        If not, creates it and copies game_data.csv (when present) and team_data/ (when present).
        If it exists, skips (files already saved for this week).

        Week numbers are zero-padded (01, 02, ..., 11, 12).

        Returns:
            bool: True if files were saved, False if already saved, disabled, or error occurred
        """
        if not self.settings.enable_historical_save:
            self.logger.debug("Historical data auto-save disabled via settings")
            return False

        try:
            week_number = f"{self.settings.current_nfl_week:02d}"

            historical_folder = self.script_dir.parent / "data" / "historical_data" / str(self.settings.season) / week_number

            if historical_folder.exists():
                self.logger.info(f"Historical data already saved for Week {self.settings.current_nfl_week} (folder {week_number} exists)")
                return False

            self.logger.info(f"Creating historical data folder: {historical_folder}")
            historical_folder.mkdir(parents=True, exist_ok=True)

            data_folder = self.script_dir.parent / "data"
            files_to_copy = ["game_data.csv"]

            for filename in files_to_copy:
                source = data_folder / filename
                destination = historical_folder / filename

                if source.exists():
                    shutil.copy2(str(source), str(destination))
                    self.logger.debug(f"Copied {filename} to {historical_folder}")
                else:
                    self.logger.warning(f"Source file not found: {source}")

            team_data_source = data_folder / "team_data"
            team_data_dest = historical_folder / "team_data"
            if team_data_source.exists():
                shutil.copytree(str(team_data_source), str(team_data_dest))
                self.logger.debug(f"Copied team_data folder to {historical_folder}")
            else:
                self.logger.warning(f"Team data folder not found: {team_data_source}")

            self.logger.info(f"Successfully saved historical data for Week {self.settings.current_nfl_week} to {historical_folder}")
            return True

        except Exception as e:
            self.logger.warning(f"Failed to save historical data: {e}")
            return False

    def fetch_game_data(self) -> bool:
        """
        Fetch game-level data (venue, weather, scores) from ESPN and Open-Meteo APIs.

        Checks config flag ENABLE_GAME_DATA_FETCH before proceeding.
        Creates/updates data/game_data.csv with game information.

        Returns:
            bool: True if game data was fetched successfully, False if disabled or error
        """
        if not self.settings.enable_game_data:
            self.logger.debug("Game data fetching disabled via settings")
            return False

        try:
            from player_data_fetcher.game_data_fetcher import fetch_game_data as do_fetch_game_data

            self.logger.info("Fetching game data (venue, weather, scores)...")

            output_path = Path(self.settings.game_data_csv)

            result_path = do_fetch_game_data(
                output_path=output_path,
                season=self.settings.season,
                current_week=self.settings.current_nfl_week,
                request_timeout=self.settings.request_timeout,
                rate_limit_delay=self.settings.rate_limit_delay,
            )

            self.logger.info(f"Game data saved to: {result_path}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to fetch game data: {e}")
            return False


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
                
                top_player = None
                for player in data.players:
                    if player.position == pos and player.fantasy_points == max_points:
                        top_player = player
                        break
                
                top_name = top_player.name if top_player else "Unknown"
                print(f"     {pos}: {count} players (Top: {top_name} - {max_points:.1f} pts, Avg: {avg_points:.1f})")


def validate_output_files(position_json_output: str, logger: logging.Logger) -> None:
    """
    Validate all 6 position JSON output files after export.

    Args:
        position_json_output (str): Directory path containing position JSON files.
        logger (logging.Logger): Logger for error reporting.

    Raises:
        SystemExit: If any position file is missing, invalid JSON, missing root key, or empty.
    """
    output_dir = Path(position_json_output)
    for pos in POSITION_CODES:
        file_path = output_dir / f"{pos}_data.json"
        if not file_path.exists():
            logger.error(f"Output validation failed: {file_path} does not exist")
            sys.exit(1)
        try:
            with open(file_path, encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            logger.error(f"Output validation failed: {file_path} is not valid JSON: {e}")
            sys.exit(1)
        root_key = f"{pos}_data"
        if root_key not in data:
            logger.error(f"Output validation failed: {file_path} missing root key '{root_key}'")
            sys.exit(1)
        players = data[root_key]
        if not isinstance(players, list):
            logger.error(f"Output validation failed: {file_path} root key '{root_key}' is not a list")
            sys.exit(1)
        if len(players) < 1:
            logger.error(f"Output validation failed: {file_path} has 0 players in '{root_key}'")
            sys.exit(1)


async def main(settings_dict: dict | None = None) -> None:
    """
    Main application entry point.

    Args:
        settings_dict: Settings dictionary from run_player_fetcher.py CLI args.
                       If None, runs internal argparse (direct invocation).
    """

    if settings_dict is None:
        parser = argparse.ArgumentParser(description='Collect NFL player projections from ESPN')
        parser.add_argument('--enable-log-file', action='store_true',
                            help='Enable file logging to logs/player_data_fetcher/')
        args = parser.parse_args()
        settings = Settings(logging_to_file=args.enable_log_file)
    else:
        settings = create_settings_from_dict(settings_dict)

    logger = setup_logger(
        name=LOG_NAME,
        level=settings.log_level,
        log_to_file=settings.logging_to_file,
        log_file_path=None,
        log_format=LOGGING_FORMAT
    )

    if settings.load_drafted_data:
        drafted_path = Path(settings.drafted_data_path)
        if not drafted_path.exists():
            if settings.e2e_test:
                logger.info(
                    f"E2E mode: drafted data file not found at {settings.drafted_data_path}, skipping"
                )
                settings.load_drafted_data = False
            else:
                raise FileNotFoundError(
                    f"Drafted data file not found: {settings.drafted_data_path}. "
                    f"Use --no-load-drafted-data to skip or --e2e-test for graceful handling."
                )

    try:
        logger.info("Starting NFL projections collection with ESPN API")

        settings.validate_settings()

        collector = NFLProjectionsCollector(settings)
        projection_data = await collector.collect_all_projections()

        total_players = sum(proj.total_players for proj in projection_data.values())
        if total_players < MIN_EXPECTED_PLAYER_COUNT:
            logger.error(
                f"Insufficient player data: only {total_players} players collected "
                f"(minimum {MIN_EXPECTED_PLAYER_COUNT}). Aborting to protect existing files."
            )
            sys.exit(1)

        loop = asyncio.get_running_loop()
        game_data_future = loop.run_in_executor(None, collector.fetch_game_data)
        gather_results = await asyncio.gather(
            collector.export_data(projection_data),
            game_data_future,
            return_exceptions=True,
        )
        output_files = gather_results[0]
        game_data_result = gather_results[1]

        if isinstance(game_data_result, Exception):
            logger.warning(f"Failed to fetch game data: {game_data_result}")
            print(f"\n[WARNING] Could not fetch game data: {game_data_result}")
        elif game_data_result:
            print(f"\n[INFO] Game data (venue, weather, scores) fetched successfully")
        elif not settings.enable_game_data:
            logger.debug("Game data fetching disabled via settings")

        if isinstance(output_files, Exception):
            raise output_files

        validate_output_files(settings.position_json_output, logger)

        try:
            saved = collector.save_to_historical_data()
            if saved:
                print(f"\n[INFO] Saved weekly data to historical folder")
            elif not settings.enable_historical_save:
                logger.debug("Historical data auto-save disabled via settings")
            else:
                print(f"\n[INFO] Weekly data already saved for Week {settings.current_nfl_week}")
        except Exception as e:
            logger.warning(f"Failed to save historical data: {e}")
            print(f"\n[WARNING] Could not save to historical folder: {e}")

        collector.print_summary(projection_data)
        
        fantasy_players = collector.get_fantasy_players(projection_data)
        
        print(f"\nOutput Files:")
        for file in output_files:
            print(f"   {file}")
        
        print(f"\nESPN API Usage:")
        print(f"   Free and no signup required")
        print(f"   Unofficial API - use responsibly")
        
        if 'season' in fantasy_players:
            season_players = fantasy_players['season']
            print(f"\nFantasyPlayer Integration:")
            print(f"   Converted {len(season_players)} players to FantasyPlayer objects")
            print(f"   Available for import: from fantasy_player import FantasyPlayer")
            print(f"   Load from JSON: See data/player_data/ for position-specific JSON files")

            adp_values = [p.average_draft_position for p in season_players if p.average_draft_position is not None]
            if adp_values and len(set(adp_values)) == 1:
                placeholder_value = adp_values[0]
                print(f"\n{'='*80}")
                print(f"{'='*80}")
                print(f"  WARNING: ESPN ADP DATA IS PLACEHOLDER ({placeholder_value}) - NOT REAL VALUES")
                print(f"{'='*80}")
                print(f"  ESPN only provides real ADP data during draft season (Aug-Sep).")
                print(f"  All {len(adp_values)} players have average_draft_position = {placeholder_value}")
                print(f"")
                print(f"  EXPLANATION:")
                print(f"    - This is ESPN's expected behavior outside of draft season")
                print(f"    - ESPN returns placeholder value of 170.0 from October-December")
                print(f"    - Real ADP data will be available again in August {int(placeholder_value) + 1} draft season")
                print(f"")
                print(f"  IMPACT:")
                print(f"    - If your scoring uses ADP multipliers, they will not differentiate players")
                print(f"    - Consider using player_rating (0-100 scale) instead if available")
                print(f"{'='*80}")
                print(f"{'='*80}\n")
                logger.warning(f"ESPN returning placeholder ADP data ({placeholder_value}) for all players - mid-season behavior")

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