#!/usr/bin/env python3
"""
Drafted Data Writer

Helper class for managing drafted_data.csv file operations.
Handles adding and removing players from the drafted roster CSV.

Author: Kai Mizuno
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

    def __init__(self, csv_path: Path) -> None:
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
        # Check if CSV file exists before attempting to read it
        # This can happen if the user hasn't drafted any players yet
        if not self.csv_path.exists():
            self.logger.debug(f"Drafted data file not found: {self.csv_path}")
            return []

        # Use a set to automatically handle duplicates
        # Same team name may appear multiple times (one per drafted player)
        team_names: Set[str] = set()

        try:
            # Read CSV file with proper encoding
            with open(self.csv_path, 'r', newline='', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    # Each row format: ["Player Name POS - TEAM", "Team Name"]
                    # We need the second column (index 1) for the fantasy team name
                    if len(row) >= 2:
                        team_name = row[1].strip()
                        # Only add non-empty team names to the set
                        if team_name:
                            team_names.add(team_name)

            # Return alphabetically sorted list of unique team names
            # This makes team selection menus easier to navigate
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
            self.logger.debug(f"Drafted data file not found: {self.csv_path}")
            return False

        try:
            # Strategy: Read all rows, filter out the matching player, then write back
            # We can't remove a line from CSV in-place, so we must rewrite the entire file
            rows = []
            player_found = False

            # First pass: Read all rows and identify which one to remove
            with open(self.csv_path, 'r', newline='', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if len(row) >= 2:
                        # First column contains player info: "Player Name POS - TEAM"
                        player_info = row[0].strip()
                        # Use fuzzy matching to identify the player
                        # This handles name variations and formatting differences
                        if self._player_matches(player, player_info):
                            player_found = True
                            self.logger.info(f"Found and removing: {player_info}")
                            continue  # Skip this row (effectively removing it)
                    # Keep all other rows for rewriting
                    rows.append(row)

            # Validate that we actually found and removed a player
            if not player_found:
                self.logger.warning(f"Player {player.name} not found in drafted_data.csv")
                return False

            # Second pass: Write back all rows except the removed one
            # This completely rewrites the CSV file
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
        # Special handling for DST/DEF positions
        # players.csv uses "Steelers D/ST" while drafted_data.csv uses "Pittsburgh Steelers DEF"
        # The team names don't match exactly (nickname vs full name), so we need special logic
        if player.position.upper() == "DST":
            # Check if CSV entry is a DEF/DST entry
            if "DEF" in csv_player_info.upper() or "DST" in csv_player_info.upper():
                # Extract team nickname from player name (e.g., "Steelers" from "Steelers D/ST")
                # DST names in players.csv are formatted as "{Nickname} D/ST"
                player_team_nickname = player.name.replace(" D/ST", "").strip()

                # Normalize and check if nickname appears in CSV entry
                # This handles "Steelers D/ST" matching "Pittsburgh Steelers DEF"
                if self._normalize_name(player_team_nickname) in self._normalize_name(csv_player_info):
                    return True
            return False

        # Regular player matching logic
        player_normalized = self._normalize_name(player.name)
        csv_normalized = self._normalize_name(csv_player_info)

        # Check if player name appears anywhere in CSV entry
        # The CSV entry contains more than just the name (position, team)
        if player_normalized in csv_normalized:
            # Additional validation: also check that position matches
            # This prevents false positives for players with similar names
            # Example: Avoid matching "Mike Williams WR" with "Michael Williams TE"
            position_to_match = player.position.upper()
            if position_to_match in csv_player_info.upper():
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
        # Step 1: Convert to lowercase and collapse multiple spaces into single spaces
        # This handles inconsistent spacing like "Patrick  Mahomes" vs "Patrick Mahomes"
        normalized = ' '.join(name.lower().split())

        # Step 2: Remove common name suffixes that vary in formatting
        # Examples: "Ken Griffey Jr" vs "Ken Griffey Jr." vs "Ken Griffey"
        for suffix in [' jr', ' sr', ' iii', ' ii', ' iv']:
            normalized = normalized.replace(suffix, '')

        # Step 3: Remove punctuation characters that appear in names
        # Periods: "T.J. Hockenson" → "tj hockenson"
        # Apostrophes: "D'Andre Swift" → "dandre swift"
        # Hyphens: "Ka'imi Fairbairn" → "kaimi fairbairn"
        normalized = normalized.replace('.', '').replace("'", '').replace('-', ' ')

        # Step 4: Final cleanup - collapse any double spaces created by punctuation removal
        # Example: "T.J. Hockenson" → "T J  Hockenson" → "tj hockenson"
        return ' '.join(normalized.split())
