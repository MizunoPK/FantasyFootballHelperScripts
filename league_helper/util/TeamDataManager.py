#!/usr/bin/env python3
"""
Team Data Loader for Draft Helper

This module handles loading team offensive/defensive rankings from teams.csv
for use in enhanced scoring calculations.

Author: Kai Mizuno
Last Updated: September 2025
"""

from pathlib import Path
from typing import Dict, Optional

import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.TeamData import TeamData, load_teams_from_csv
from utils.LoggingManager import get_logger


class TeamDataManager:
    """Loads and manages team ranking data from teams.csv file."""

    def __init__(self, data_folder: Path):
        """
        Initialize TeamDataManager.

        Args:
            teams_file_path: Path to teams.csv file. If None, uses shared_files/teams.csv
        """
        self.logger = get_logger()

        self.teams_file = data_folder / 'teams.csv'
        self.team_data_cache: Dict[str, TeamData] = {}
        self._load_team_data()

    def _load_team_data(self) -> None:
        """Load team data from teams.csv file."""
        try:
            if not self.teams_file.exists():
                self.logger.warning(f"Teams file not found: {self.teams_file}. Team rankings will not be available.")
                return

            teams = load_teams_from_csv(str(self.teams_file))

            # Build team lookup cache
            self.team_data_cache = {team.team: team for team in teams}

            self.logger.info(f"Loaded team data for {len(self.team_data_cache)} teams from {self.teams_file}")

        except Exception as e:
            self.logger.warning(f"Error loading team data from {self.teams_file}: {e}. Team rankings will not be available.")
            self.team_data_cache = {}

    def get_team_offensive_rank(self, team: str) -> Optional[int]:
        """
        Get team offensive ranking.

        Args:
            team: Team abbreviation (e.g., 'PHI', 'KC')

        Returns:
            Team offensive rank (1-32) or None if not available
        """
        team_data = self.team_data_cache.get(team)
        return team_data.offensive_rank if team_data else None

    def get_team_defensive_rank(self, team: str) -> Optional[int]:
        """
        Get team defensive ranking.

        Args:
            team: Team abbreviation (e.g., 'PHI', 'KC')

        Returns:
            Team defensive rank (1-32) or None if not available
        """
        team_data = self.team_data_cache.get(team)
        return team_data.defensive_rank if team_data else None

    def get_team_opponent(self, team: str) -> Optional[str]:
        """
        Get team's next opponent.

        Args:
            team: Team abbreviation (e.g., 'PHI', 'KC')

        Returns:
            Opponent team abbreviation or None if not available
        """
        team_data = self.team_data_cache.get(team)
        return team_data.opponent if team_data else None

    def get_team_data(self, team: str) -> Optional[TeamData]:
        """
        Get complete team data object.

        Args:
            team: Team abbreviation (e.g., 'PHI', 'KC')

        Returns:
            TeamData object or None if not available
        """
        return self.team_data_cache.get(team)

    def is_team_data_available(self) -> bool:
        """Check if team data is loaded and available."""
        return bool(self.team_data_cache)

    def get_available_teams(self) -> list[str]:
        """Get list of all teams for which data is available."""
        return list(self.team_data_cache.keys())
    
    def is_matchup_available(self) -> bool:
        """
        Check if matchup calculations are available.

        Returns:
            True if team data is loaded and valid, False otherwise
        """
        return self.team_data_cache is not None and len(self.team_data_cache) > 0

    def reload_team_data(self) -> None:
        """Reload team data from teams.csv file (useful if file was updated)."""
        self.team_data_cache = {}
        self._load_team_data()


    def get_rank_difference(self, player_team: str, is_defense = False) -> int:
        """
        Calculate rank difference for a player's team matchup.

        Formula for Offensive positions: (Opponent Defensive Rank) - (Player's Team Offensive Rank)
        Formula for Defensive positions: (Opponent Offensive Rank) - (Player's Team Defensive Rank)

        Args:
            player_team: Team abbreviation (e.g., 'KC', 'BUF')
            is_defense: True if player is on defense/DST, False for offensive positions

        Returns:
            Rank difference integer, or 0 if data unavailable
        """
        if not self.is_matchup_available():
            return 0

        # Find player's team data
        if is_defense:
            team_rank = self.get_team_defensive_rank(player_team)
        else:
            team_rank = self.get_team_offensive_rank(player_team)

        if team_rank is None:
            self.logger.debug(f"Team not found in matchup data: {player_team}")
            return 0

        opponent_abbr = self.get_team_opponent(player_team)
        if opponent_abbr is None:
            self.logger.debug(f"No opponent found for team: {player_team}")
            return 0

        # Find opponent's rank (opposite side of ball)
        if is_defense:
            opponent_rank = self.get_team_offensive_rank(opponent_abbr)
        else:
            opponent_rank = self.get_team_defensive_rank(opponent_abbr)

        if opponent_rank is None:
            self.logger.debug(f"Opponent rank not found in matchup data: {opponent_abbr}")
            return 0

        # Calculate rank difference
        rank_diff = int(opponent_rank) - int(team_rank)

        if is_defense:
            self.logger.debug(
                f"Matchup for {player_team} vs {opponent_abbr}: "
                f"DEF#{team_rank} vs OFF#{opponent_rank} = {rank_diff:+d}"
            )
        else:
            self.logger.debug(
                f"Matchup for {player_team} vs {opponent_abbr}: "
                f"OFF#{team_rank} vs DEF#{opponent_rank} = {rank_diff:+d}"
            )

        return rank_diff