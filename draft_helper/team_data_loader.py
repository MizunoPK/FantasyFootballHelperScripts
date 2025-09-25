#!/usr/bin/env python3
"""
Team Data Loader for Draft Helper

This module handles loading team offensive/defensive rankings from teams.csv
for use in enhanced scoring calculations.

Author: Generated for NFL Fantasy Data Collection
Last Updated: September 2025
"""

import logging
from pathlib import Path
from typing import Dict, Optional

import sys
sys.path.append(str(Path(__file__).parent.parent))
from shared_files.TeamData import TeamData, load_teams_from_csv


class TeamDataLoader:
    """Loads and manages team ranking data from teams.csv file."""

    def __init__(self, teams_file_path: Optional[str] = None):
        """
        Initialize TeamDataLoader.

        Args:
            teams_file_path: Path to teams.csv file. If None, uses shared_files/teams.csv
        """
        self.logger = logging.getLogger(__name__)

        if teams_file_path:
            self.teams_file = Path(teams_file_path)
        else:
            # Default to shared_files/teams.csv
            shared_files_dir = Path(__file__).parent.parent / "shared_files"
            self.teams_file = shared_files_dir / "teams.csv"

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

    def reload_team_data(self) -> None:
        """Reload team data from teams.csv file (useful if file was updated)."""
        self.team_data_cache = {}
        self._load_team_data()