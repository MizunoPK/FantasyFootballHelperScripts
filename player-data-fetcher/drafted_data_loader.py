#!/usr/bin/env python3
"""
Drafted Data Loader Module

This module handles loading and processing drafted player data from external CSV files.
Provides fuzzy matching functionality to identify players and assign drafted states.

Author: Generated for NFL Fantasy Data Collection
Created: September 2025
"""

import csv
import logging
import re
from difflib import SequenceMatcher
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set

from player_data_constants import LOAD_DRAFTED_DATA_FROM_FILE, DRAFTED_DATA, MY_TEAM_NAME


class DraftedDataLoader:
    """Handles loading and fuzzy matching of drafted player data from CSV files"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.drafted_players: Dict[str, str] = {}  # player_key -> team_name
        self.processed_players: Set[str] = set()  # Track processed players to avoid duplicates

    def load_drafted_data(self) -> bool:
        """
        Load drafted player data from CSV file.

        Returns:
            bool: True if data loaded successfully, False otherwise
        """
        if not LOAD_DRAFTED_DATA_FROM_FILE:
            self.logger.debug("LOAD_DRAFTED_DATA_FROM_FILE is disabled, skipping drafted data loading")
            return False

        drafted_file_path = Path(DRAFTED_DATA)

        # Handle relative paths from player-data-fetcher directory
        if not drafted_file_path.is_absolute():
            script_dir = Path(__file__).parent
            drafted_file_path = script_dir / drafted_file_path

        if not drafted_file_path.exists():
            self.logger.warning(f"Drafted data file not found: {drafted_file_path}")
            self.logger.warning("Treating LOAD_DRAFTED_DATA_FROM_FILE as disabled")
            return False

        try:
            with open(drafted_file_path, 'r', newline='', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                row_count = 0

                for row in csv_reader:
                    row_count += 1

                    # Skip empty rows
                    if not row or len(row) < 2:
                        continue

                    # Parse player info and team
                    player_info = row[0].strip()
                    team_name = row[1].strip()

                    if not player_info or not team_name:
                        continue

                    # Create a normalized key for player identification
                    player_key = self._normalize_player_info(player_info)

                    # Handle duplicates - only use first occurrence
                    if player_key in self.drafted_players:
                        self.logger.debug(f"Duplicate entry found for {player_info}, skipping")
                        continue

                    self.drafted_players[player_key] = team_name

                self.logger.info(f"Loaded {len(self.drafted_players)} drafted players from {drafted_file_path}")
                return True

        except Exception as e:
            self.logger.error(f"Error loading drafted data from {drafted_file_path}: {e}")
            self.logger.warning("Treating LOAD_DRAFTED_DATA_FROM_FILE as disabled")
            return False

    def _normalize_player_info(self, player_info: str) -> str:
        """
        Normalize player info string for consistent matching.

        Args:
            player_info: Raw player info string like "Amon-Ra St. Brown WR - DET"

        Returns:
            str: Normalized string for matching
        """
        # Remove extra whitespace and convert to lowercase
        normalized = re.sub(r'\s+', ' ', player_info.strip().lower())

        # Remove common suffixes and prefixes that might cause mismatches
        normalized = re.sub(r'\b(jr\.?|sr\.?|iii?|iv)\b', '', normalized)

        # Normalize punctuation
        normalized = normalized.replace('.', '').replace("'", '').replace('-', ' ')

        return normalized

    def _extract_player_components(self, player_info: str) -> Tuple[str, str, str]:
        """
        Extract name, position, and team from player info string.

        Args:
            player_info: Player info like "Amon-Ra St. Brown WR - DET"

        Returns:
            Tuple of (name, position, team) - empty strings if not found
        """
        # Pattern to match: "Name Position - Team"
        # Handles cases like "Amon-Ra St. Brown WR - DET" or "Tucker Kraft TE - GB Q View News"
        pattern = r'^(.+?)\s+([A-Z]{1,3})\s*-\s*([A-Z]{2,4})'

        match = re.match(pattern, player_info.strip())
        if match:
            name = match.group(1).strip()
            position = match.group(2).strip()
            team = match.group(3).strip().split()[0]  # Take first part in case of extra info
            return name, position, team

        # Fallback: try to extract what we can
        parts = player_info.strip().split()
        if len(parts) >= 3:
            # Assume last part with '-' contains team, second to last is position
            name_parts = []
            position = ""
            team = ""

            for i, part in enumerate(parts):
                if '-' in part:
                    team = part.split('-')[-1].strip()
                    if i > 0:
                        position = parts[i-1]
                    name_parts = parts[:i-1] if i > 0 else []
                    break

            name = ' '.join(name_parts)
            return name, position, team

        return "", "", ""

    def _similarity_score(self, s1: str, s2: str) -> float:
        """Calculate similarity score between two strings (0.0 to 1.0)"""
        return SequenceMatcher(None, s1.lower(), s2.lower()).ratio()

    def find_drafted_state(self, player_name: str, player_position: str, player_team: str) -> int:
        """
        Find the drafted state for a player using fuzzy matching.

        Args:
            player_name: Player's name
            player_position: Player's position (QB, RB, WR, etc.)
            player_team: Player's NFL team

        Returns:
            int: 0 = not drafted, 1 = drafted by others, 2 = on user's team
        """
        if not LOAD_DRAFTED_DATA_FROM_FILE or not self.drafted_players:
            return 0

        # Create normalized search string for the current player
        search_string = f"{player_name} {player_position} - {player_team}".lower()
        normalized_search = self._normalize_player_info(search_string)

        best_match_score = 0.0
        best_match_team = None

        # Search through all drafted players
        for drafted_key, fantasy_team in self.drafted_players.items():
            # Calculate similarity score
            score = self._similarity_score(normalized_search, drafted_key)

            if score > best_match_score:
                # For potential matches, do additional verification
                if score >= 0.8:  # High similarity threshold
                    # Extract components from drafted data for verification
                    original_info = None
                    for orig_key, team in self.drafted_players.items():
                        if team == fantasy_team and self._similarity_score(drafted_key, orig_key) > 0.95:
                            # Find original non-normalized version
                            for row_data in self._get_original_data():
                                if self._normalize_player_info(row_data[0]) == drafted_key:
                                    original_info = row_data[0]
                                    break
                            break

                    if original_info:
                        drafted_name, drafted_pos, drafted_team = self._extract_player_components(original_info)

                        # Verify position and team match
                        if (drafted_pos.upper() == player_position.upper() and
                            drafted_team.upper() == player_team.upper()):
                            best_match_score = score
                            best_match_team = fantasy_team
                        else:
                            # Position or team mismatch, reduce score
                            score *= 0.5
                            if score > best_match_score:
                                best_match_score = score
                                best_match_team = fantasy_team

        # Only accept matches above threshold
        if best_match_score >= 0.7:  # Require 70% similarity minimum
            if best_match_team == MY_TEAM_NAME:
                self.logger.debug(f"Found player on user's team: {player_name} {player_position} - {player_team}")
                return 2
            else:
                self.logger.debug(f"Found drafted player: {player_name} {player_position} - {player_team} (team: {best_match_team})")
                return 1

        # Check for multiple potential matches - if found, skip to avoid errors
        potential_matches = []
        for drafted_key, fantasy_team in self.drafted_players.items():
            score = self._similarity_score(normalized_search, drafted_key)
            if score >= 0.7:
                potential_matches.append((score, fantasy_team, drafted_key))

        if len(potential_matches) > 1:
            self.logger.debug(f"Multiple potential matches found for {player_name}, skipping to avoid errors")
            return 0

        return 0

    def _get_original_data(self) -> List[List[str]]:
        """Get original CSV data for verification purposes"""
        drafted_file_path = Path(DRAFTED_DATA)

        # Handle relative paths
        if not drafted_file_path.is_absolute():
            script_dir = Path(__file__).parent
            drafted_file_path = script_dir / drafted_file_path

        if not drafted_file_path.exists():
            return []

        try:
            with open(drafted_file_path, 'r', newline='', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                return [row for row in csv_reader if len(row) >= 2]
        except Exception:
            return []

    def get_stats(self) -> Dict[str, int]:
        """Get statistics about loaded drafted data"""
        if not self.drafted_players:
            return {"total_players": 0, "user_team_players": 0, "other_team_players": 0}

        user_team_count = sum(1 for team in self.drafted_players.values() if team == MY_TEAM_NAME)
        other_team_count = len(self.drafted_players) - user_team_count

        return {
            "total_players": len(self.drafted_players),
            "user_team_players": user_team_count,
            "other_team_players": other_team_count
        }