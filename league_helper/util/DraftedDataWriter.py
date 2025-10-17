#!/usr/bin/env python3
"""
Drafted Data Writer

Helper class for managing drafted_data.csv file operations.
Handles adding and removing players from the drafted roster CSV.

Author: Kai Mizuno
Last Updated: October 2025
"""

import csv
from pathlib import Path
from typing import List, Set
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger


class DraftedDataWriter:
    """Manages reading and writing to drafted_data.csv file."""

    def __init__(self, csv_path: Path):
        """
        Initialize DraftedDataWriter.

        Args:
            csv_path: Path to drafted_data.csv file
        """
        self.csv_path = csv_path
        self.logger = get_logger()

    def get_all_team_names(self) -> List[str]:
        """
        Get all unique team names from drafted_data.csv in alphabetical order.

        Returns:
            List of team names sorted alphabetically
        """
        if not self.csv_path.exists():
            self.logger.warning(f"Drafted data file not found: {self.csv_path}")
            return []

        team_names: Set[str] = set()

        try:
            with open(self.csv_path, 'r', newline='', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if len(row) >= 2:
                        team_name = row[1].strip()
                        if team_name:
                            team_names.add(team_name)

            return sorted(list(team_names))

        except Exception as e:
            self.logger.error(f"Error reading team names from {self.csv_path}: {e}")
            return []

    def add_player(self, player: FantasyPlayer, team_name: str) -> bool:
        """
        Add a player to drafted_data.csv.

        Args:
            player: FantasyPlayer to add
            team_name: Name of the fantasy team

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Format: "Player Name POS - TEAM", "Team Name"
            player_info = f"{player.name} {player.position} - {player.team}"

            # Append to file
            with open(self.csv_path, 'a', newline='', encoding='utf-8') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow([player_info, team_name])

            self.logger.info(f"Added {player.name} to drafted_data.csv for team {team_name}")
            return True

        except Exception as e:
            self.logger.error(f"Error adding player to {self.csv_path}: {e}")
            return False

    def remove_player(self, player: FantasyPlayer) -> bool:
        """
        Remove a player from drafted_data.csv.

        Uses fuzzy matching to find and remove the player entry.

        Args:
            player: FantasyPlayer to remove

        Returns:
            bool: True if successful, False otherwise
        """
        if not self.csv_path.exists():
            self.logger.warning(f"Drafted data file not found: {self.csv_path}")
            return False

        try:
            # Read all rows
            rows = []
            player_found = False

            with open(self.csv_path, 'r', newline='', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if len(row) >= 2:
                        player_info = row[0].strip()
                        # Check if this row matches our player
                        if self._player_matches(player, player_info):
                            player_found = True
                            self.logger.info(f"Found and removing: {player_info}")
                            continue  # Skip this row (remove it)
                    rows.append(row)

            if not player_found:
                self.logger.warning(f"Player {player.name} not found in drafted_data.csv")
                return False

            # Write back all rows except the removed one
            with open(self.csv_path, 'w', newline='', encoding='utf-8') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerows(rows)

            self.logger.info(f"Removed {player.name} from drafted_data.csv")
            return True

        except Exception as e:
            self.logger.error(f"Error removing player from {self.csv_path}: {e}")
            return False

    def _player_matches(self, player: FantasyPlayer, csv_player_info: str) -> bool:
        """
        Check if a player matches a CSV entry using fuzzy matching.

        Args:
            player: FantasyPlayer object
            csv_player_info: CSV entry like "Patrick Mahomes QB - KC"

        Returns:
            bool: True if match found
        """
        # Normalize both strings
        player_normalized = self._normalize_name(player.name)
        csv_normalized = self._normalize_name(csv_player_info)

        # Check if player name appears in CSV entry
        if player_normalized in csv_normalized:
            # Also check position matches
            if player.position.upper() in csv_player_info.upper():
                return True

        return False

    def _normalize_name(self, name: str) -> str:
        """
        Normalize a name for matching.

        Args:
            name: Name string to normalize

        Returns:
            Normalized lowercase name
        """
        # Convert to lowercase and remove extra whitespace
        normalized = ' '.join(name.lower().split())

        # Remove common suffixes
        for suffix in [' jr', ' sr', ' iii', ' ii', ' iv']:
            normalized = normalized.replace(suffix, '')

        # Remove punctuation
        normalized = normalized.replace('.', '').replace("'", '').replace('-', ' ')

        return ' '.join(normalized.split())
