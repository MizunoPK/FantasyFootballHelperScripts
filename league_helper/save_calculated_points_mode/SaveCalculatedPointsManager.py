#!/usr/bin/env python3
"""
Save Calculated Points Mode Manager

Saves calculated projected points for all players to JSON files in the
historical_data folder structure. Uses the same scoring logic as the
Starter Helper mode.

This mode creates a snapshot of:
- Calculated player scores (JSON)
- Input data files (players.csv, configs/, team_data/, etc.)

Output Structure:
- Weekly: data/historical_data/{SEASON}/{WEEK}/calculated_projected_points.json
- Season-long: data/historical_data/{SEASON}/calculated_season_long_projected_points.json

Author: Kai Mizuno
"""

import json
import shutil
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.LoggingManager import get_logger
from league_helper.util.ConfigManager import ConfigManager
from league_helper.util.PlayerManager import PlayerManager


class SaveCalculatedPointsManager:
    """
    Mode manager for saving calculated projected points to historical data.

    This manager:
    - Scores all available players using StarterHelper scoring logic
    - Saves scores to JSON format: {player_id: calculated_score}
    - Copies relevant data files to historical_data folder for reproducibility

    Attributes:
        logger: Logger instance for tracking operations
        config (ConfigManager): Configuration manager with league settings
        player_manager (PlayerManager): Player manager with scoring logic
        data_folder (Path): Path to data directory
    """

    def __init__(self, config: ConfigManager, player_manager: PlayerManager, data_folder: Path):
        """
        Initialize the Save Calculated Points mode manager.

        Args:
            config (ConfigManager): Configuration manager with league settings
            player_manager (PlayerManager): Player manager with scoring capabilities
            data_folder (Path): Path to data directory
        """
        self.logger = get_logger()
        self.config = config
        self.player_manager = player_manager
        self.data_folder = data_folder

        self.logger.debug("Initialized Save Calculated Points Mode Manager")

    def execute(self) -> None:
        """
        Main entry point - score all players and save to historical data.

        Process:
        1. Determine week and output path
        2. Check if folder already exists (idempotent)
        3. Setup max_weekly_projection for weekly scoring
        4. Score all players
        5. Create JSON output with 2 decimal precision
        6. Copy data files to historical_data folder
        7. Display summary message

        Returns:
            None
        """
        week = self.config.current_nfl_week
        season = self.config.nfl_season

        self.logger.info(f"Entering Save Calculated Points mode (Week {week}, Season {season})")

        # Determine output path based on week
        if week == 0:
            # Season-long scoring
            output_path = self.data_folder / "historical_data" / str(season) / "calculated_season_long_projected_points.json"
        else:
            # Weekly scoring
            week_str = f"{week:02d}"
            output_path = self.data_folder / "historical_data" / str(season) / week_str / "calculated_projected_points.json"

        output_folder = output_path.parent

        # Idempotent check: skip if folder already exists
        if output_folder.exists():
            self.logger.info(f"Folder already exists: {output_folder}. Skipping operation.")
            print(f"\nHistorical data already exists for Season {season}, Week {week}. Skipping.")
            return

        # Setup max_weekly_projection for weekly scoring
        if week > 0:
            max_weekly = self.player_manager.calculate_max_weekly_projection(week)
            self.player_manager.scoring_calculator.max_weekly_projection = max_weekly
            self.logger.debug(f"Set max_weekly_projection = {max_weekly:.2f} for week {week}")

        # Score all available players
        self.logger.debug(f"Scoring {len(self.player_manager.players)} players...")
        scored_players = []

        for player in self.player_manager.players:
            scored = self.player_manager.score_player(
                player,
                use_weekly_projection=(week > 0),  # False for week 0, True for 1-17
                adp=False,
                player_rating=False,
                team_quality=True,
                performance=True,
                matchup=True,
                schedule=False,
                bye=False,
                injury=False,
                temperature=True,
                wind=True,
                location=True
            )
            scored_players.append((player, scored))

        # Create JSON dictionary with 2 decimal precision
        results_dict = {}
        for player, scored in scored_players:
            player_id = f"{player.name}_{player.position}_{player.team}"
            results_dict[player_id] = round(scored.score, 2)

        # Create output folder
        output_folder.mkdir(parents=True, exist_ok=True)
        self.logger.debug(f"Created output folder: {output_folder}")

        # Write JSON file
        with open(str(output_path), 'w') as f:
            json.dump(results_dict, f, indent=2)
        self.logger.info(f"Saved {len(results_dict)} player scores to {output_path}")

        # Copy data files to historical_data folder
        files_to_copy = [
            "players.csv",
            "players_projected.csv",
            "game_data.csv",
            "drafted_data.csv"
        ]

        for filename in files_to_copy:
            src = self.data_folder / filename
            dst = output_folder / filename
            if src.exists():
                shutil.copy2(str(src), str(dst))
                self.logger.debug(f"Copied {filename}")
            else:
                self.logger.warning(f"File not found: {filename}. Skipping.")

        # Copy configs/ folder
        configs_src = self.data_folder / "configs"
        configs_dst = output_folder / "configs"
        if configs_src.exists():
            shutil.copytree(str(configs_src), str(configs_dst))
            self.logger.debug("Copied configs/ folder")
        else:
            self.logger.warning("configs/ folder not found. Skipping.")

        # Copy team_data/ folder
        team_data_src = self.data_folder / "team_data"
        team_data_dst = output_folder / "team_data"
        if team_data_src.exists():
            shutil.copytree(str(team_data_src), str(team_data_dst))
            self.logger.debug("Copied team_data/ folder")
        else:
            self.logger.warning("team_data/ folder not found. Skipping.")

        # Summary message
        print(f"\n✓ Operation complete!")
        print(f"  Saved {len(results_dict)} player scores to:")
        print(f"  {output_path}")
        print(f"  Copied data files to: {output_folder}")

        self.logger.info("Exiting Save Calculated Points mode")
