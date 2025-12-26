#!/usr/bin/env python3
"""
Drafted Roster Manager

Shared class for managing drafted player data across fantasy teams.
Handles loading drafted_data.csv, fuzzy matching, and organizing players by team.

This module provides:
- Loading and processing drafted player data from CSV
- Fuzzy matching to identify players across different data sources
- Team-based player organization
- Helper functions for managing drafted state

Used by:
- player-data-fetcher: Initial data loading and player state management
- league_helper: Team roster management and draft analysis

Author: Kai Mizuno
Created: October 2025
"""

import csv
import re
from difflib import SequenceMatcher
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set

import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.LoggingManager import get_logger
from utils.FantasyPlayer import FantasyPlayer


class DraftedRosterManager:
    """
    Manages drafted player rosters across fantasy teams.

    Provides functionality to:
    - Load drafted data from CSV
    - Match players using fuzzy search
    - Organize players by fantasy team
    - Update FantasyPlayer objects with drafted state

    Attributes:
        drafted_players (Dict[str, str]): Normalized player key -> team name mapping
        csv_path (Path): Path to drafted_data.csv file
        my_team_name (str): Name of user's fantasy team
        logger: Logger instance
    """

    def __init__(self, csv_path: str, my_team_name: str):
        """
        Initialize DraftedRosterManager.

        Args:
            csv_path: Path to drafted_data.csv file
            my_team_name: Name of user's fantasy team (for drafted=2 identification)
        """
        self.logger = get_logger()
        self.csv_path = Path(csv_path)
        self.my_team_name = my_team_name
        self.drafted_players: Dict[str, str] = {}  # Normalized player key -> team name
        self._original_csv_data: List[List[str]] = []  # Cache for original CSV data

    def load_drafted_data(self) -> bool:
        """
        Load drafted player data from CSV file.

        CSV Format:
            player_info, team_name
            "Amon-Ra St. Brown WR - DET", "Sea Sharp"
            "Josh Allen QB - BUF", "Team Alpha"

        Returns:
            bool: True if data loaded successfully, False otherwise
        """
        if not self.csv_path.exists():
            self.logger.debug(f"Drafted data file not found: {self.csv_path}")
            return False

        try:
            self.drafted_players.clear()
            self._original_csv_data.clear()

            with open(self.csv_path, 'r', newline='', encoding='utf-8') as file:
                csv_reader = csv.reader(file)

                for row in csv_reader:
                    # Skip empty rows or malformed data
                    # Expected format: ["Player Name POS - TEAM", "Fantasy Team Name"]
                    if not row or len(row) < 2:
                        continue

                    # Store original data for later reverse lookup
                    # This allows us to extract components from unnormalized strings
                    self._original_csv_data.append(row)

                    # Parse player info and team
                    player_info = row[0].strip()  # "Amon-Ra St. Brown WR - DET"
                    team_name = row[1].strip()    # "Sea Sharp"

                    if not player_info or not team_name:
                        continue

                    # Create normalized key for matching
                    # Normalization removes punctuation, suffixes, injury tags, etc.
                    # This improves fuzzy matching reliability
                    player_key = self._normalize_player_info(player_info)

                    # Handle duplicates - only use first occurrence
                    # Duplicates can occur from CSV export errors or trades
                    if player_key in self.drafted_players:
                        self.logger.debug(f"Duplicate entry found for {player_info}, skipping")
                        continue

                    # Store mapping: normalized_key -> fantasy_team_name
                    self.drafted_players[player_key] = team_name

                self.logger.info(f"Loaded {len(self.drafted_players)} drafted players from {self.csv_path}")
                return True

        except Exception as e:
            self.logger.error(f"Error loading drafted data from {self.csv_path}: {e}")
            return False

    def get_stats(self) -> Dict[str, int]:
        """
        Get statistics about loaded drafted data.

        Returns:
            Dict with keys: total_players, user_team_players, other_team_players
        """
        if not self.drafted_players:
            return {"total_players": 0, "user_team_players": 0, "other_team_players": 0}

        user_team_count = sum(1 for team in self.drafted_players.values() if team == self.my_team_name)
        other_team_count = len(self.drafted_players) - user_team_count

        return {
            "total_players": len(self.drafted_players),
            "user_team_players": user_team_count,
            "other_team_players": other_team_count
        }

    def get_all_team_names(self) -> Set[str]:
        """
        Get set of all unique fantasy team names.

        Returns:
            Set of team names
        """
        return set(self.drafted_players.values())

    def get_players_by_team(self, fantasy_players: List[FantasyPlayer]) -> Dict[str, List[FantasyPlayer]]:
        """
        Organize FantasyPlayer objects by their fantasy team.

        This method matches FantasyPlayer objects against the drafted_data.csv
        and returns a dictionary mapping each fantasy team name to a list of
        FantasyPlayer objects on that team.

        Args:
            fantasy_players: List of FantasyPlayer objects to organize

        Returns:
            Dict[str, List[FantasyPlayer]]: Team name -> list of players on that team

        Example:
            >>> manager = DraftedRosterManager("data/drafted_data.csv", "Sea Sharp")
            >>> manager.load_drafted_data()
            >>> players = FantasyPlayer.from_csv_file("data/players.csv")
            >>> teams = manager.get_players_by_team(players)
            >>> print(teams["Sea Sharp"])  # List of FantasyPlayer objects on Sea Sharp
        """
        if not self.drafted_players:
            self.logger.debug("No drafted data loaded, returning empty dict")
            return {}

        # Initialize dict with all team names
        teams: Dict[str, List[FantasyPlayer]] = {team: [] for team in self.get_all_team_names()}

        # Create lookup for fast player access
        player_lookup = self._create_player_lookup(fantasy_players)

        # Match each CSV entry to a FantasyPlayer and organize by team
        for drafted_key, fantasy_team in self.drafted_players.items():
            # Find original CSV entry to extract components
            original_info = self._find_original_info_for_key(drafted_key)
            if not original_info:
                continue

            # Extract player components
            drafted_name, drafted_pos, drafted_team_abbr = self._extract_player_components(original_info)
            if not drafted_name or not drafted_pos:
                continue

            # Find matching player
            matched_player = self._find_matching_player(
                drafted_name, drafted_pos, drafted_team_abbr, player_lookup
            )

            if matched_player and fantasy_team in teams:
                teams[fantasy_team].append(matched_player)

        # Log team roster sizes
        for team_name, roster in teams.items():
            self.logger.debug(f"Team '{team_name}': {len(roster)} players")

        return teams

    def apply_drafted_state_to_players(self, fantasy_players: List[FantasyPlayer]) -> List[FantasyPlayer]:
        """
        Apply drafted state from CSV to FantasyPlayer objects.

        Updates the 'drafted' field on each player:
        - 0: Not drafted
        - 1: Drafted by another team
        - 2: On user's team (my_team_name)

        Args:
            fantasy_players: List of FantasyPlayer objects to update

        Returns:
            Updated list of FantasyPlayer objects (same references)
        """
        if not self.drafted_players:
            self.logger.debug("No drafted data loaded, skipping state application")
            return fantasy_players

        # Create lookup for fast player access
        player_lookup = self._create_player_lookup(fantasy_players)

        matches_found = 0

        # Iterate through CSV entries and apply drafted state
        for drafted_key, fantasy_team in self.drafted_players.items():
            # Find original CSV entry
            original_info = self._find_original_info_for_key(drafted_key)
            if not original_info:
                continue

            # Extract player components
            drafted_name, drafted_pos, drafted_team_abbr = self._extract_player_components(original_info)
            if not drafted_name or not drafted_pos:
                continue

            # Find matching player
            matched_player = self._find_matching_player(
                drafted_name, drafted_pos, drafted_team_abbr, player_lookup
            )

            if matched_player:
                # Set drafted value: 2 for user's team, 1 for others
                drafted_value = 2 if fantasy_team == self.my_team_name else 1
                matched_player.drafted = drafted_value
                matches_found += 1

                self.logger.debug(f"Applied drafted={drafted_value} to {matched_player.name} (team: {fantasy_team})")
            else:
                self.logger.warning(f"Could not find player in data for CSV entry: {original_info}")

        self.logger.info(f"Applied drafted data: {matches_found}/{len(self.drafted_players)} CSV entries matched")
        return fantasy_players

    def get_team_name_for_player(self, player: FantasyPlayer) -> str:
        """
        Get fantasy team name for a player.

        This method looks up which fantasy team drafted the player by normalizing
        the player's info and checking against the drafted_players dictionary.

        Args:
            player: FantasyPlayer object to look up

        Returns:
            Team name string if player is drafted, empty string otherwise

        Example:
            >>> manager = DraftedRosterManager("data/drafted_data.csv", "Sea Sharp")
            >>> manager.load_drafted_data()
            >>> team = manager.get_team_name_for_player(player)
            >>> print(team)  # "Sea Sharp" or "Team Alpha" or ""
        """
        # Build normalized player key (same format as apply_drafted_state_to_players)
        # Format: "{name} {position} - {team}"
        player_info = f"{player.name} {player.position} - {player.team}"
        player_key = self._normalize_player_info(player_info)

        # Look up in drafted_players dict (O(1) lookup)
        team_name = self.drafted_players.get(player_key, "")

        # Special handling for DST: Try matching by team abbreviation if initial lookup fails
        if not team_name and player.position.upper() in ['DST', 'DEF', 'D/ST']:
            team_name = self._match_dst_by_team_abbr(player.team)

        return team_name

    # ========================================
    # Internal Helper Methods
    # ========================================

    def _normalize_player_info(self, player_info: str) -> str:
        """
        Normalize player info string for consistent matching.

        Args:
            player_info: Raw player info like "Amon-Ra St. Brown WR - DET"

        Returns:
            Normalized string for matching
        """
        # Collapse multiple spaces and convert to lowercase for case-insensitive matching
        normalized = re.sub(r'\s+', ' ', player_info.strip().lower())

        # Remove common name suffixes/prefixes (Jr., Sr., III, IV)
        # These often differ between data sources (ESPN vs CSV)
        normalized = re.sub(r'\b(jr\.?|sr\.?|iii?|iv)\b', '', normalized)

        # Remove noise text from CSV entries that ESPN includes
        # "Q View News" = questionable with news link
        # "Sus" = suspended, "IR" = injured reserve, "NFI-R" = non-football injury reserve
        normalized = re.sub(r'\b(q view news|view news)\b', '', normalized)
        normalized = re.sub(r'\b(sus|ir|nfi-r)\b', '', normalized)
        # Remove standalone injury indicators (O = out, Q = questionable)
        normalized = re.sub(r'\s+(o|q)(\s|$)', r'\1', normalized)

        # Normalize punctuation to handle name variations
        # St. Brown -> St Brown, O'Dell -> ODell, Amon-Ra -> Amon Ra
        normalized = normalized.replace('.', '').replace("'", '').replace('-', ' ')

        # Clean up any multiple spaces created by removals
        normalized = re.sub(r'\s+', ' ', normalized).strip()

        return normalized

    def _extract_player_components(self, player_info: str) -> Tuple[str, str, str]:
        """
        Extract name, position, and team from player info string.

        Args:
            player_info: Player info like "Amon-Ra St. Brown WR - DET" or "Seattle Seahawks DEF"

        Returns:
            Tuple of (name, position, team) - empty strings if not found
        """
        # Pattern: "Name Position - Team"
        pattern = r'^(.+?)\s+([A-Z]{1,3})\s*-\s*([A-Z]{2,4})'

        match = re.match(pattern, player_info.strip())
        if match:
            name = match.group(1).strip()
            position = match.group(2).strip()
            team = match.group(3).strip().split()[0]
            return name, position, team

        # Special case for defenses: "Seattle Seahawks DEF"
        parts = player_info.strip().split()
        defense_position = None

        for i, part in enumerate(parts):
            if part.upper() in ['DEF', 'DST', 'D/ST']:
                defense_position = part.upper()
                name_parts = parts[:i]
                break

        if defense_position and len(name_parts) >= 1:
            # Extract team abbreviation from full team name
            full_name = ' '.join(name_parts).lower()
            team = self._get_team_abbr_from_name(full_name)
            return ' '.join(name_parts), defense_position, team

        # Fallback for regular players
        if len(parts) >= 3:
            for i, part in enumerate(parts):
                if '-' in part:
                    team = part.split('-')[-1].strip()
                    position = parts[i-1] if i > 0 else ""
                    name_parts = parts[:i-1] if i > 0 else []
                    name = ' '.join(name_parts)
                    return name, position, team

        return "", "", ""

    def _get_team_abbr_from_name(self, full_name: str) -> str:
        """Get NFL team abbreviation from full team name."""
        team_mappings = {
            'seattle seahawks': 'SEA', 'baltimore ravens': 'BAL', 'san francisco 49ers': 'SF',
            'green bay packers': 'GB', 'pittsburgh steelers': 'PIT', 'dallas cowboys': 'DAL',
            'new england patriots': 'NE', 'denver broncos': 'DEN', 'buffalo bills': 'BUF',
            'miami dolphins': 'MIA', 'new york jets': 'NYJ', 'philadelphia eagles': 'PHI',
            'kansas city chiefs': 'KC', 'los angeles chargers': 'LAC', 'las vegas raiders': 'LV',
            'cincinnati bengals': 'CIN', 'cleveland browns': 'CLE', 'houston texans': 'HOU',
            'indianapolis colts': 'IND', 'tennessee titans': 'TEN', 'jacksonville jaguars': 'JAX',
            'new york giants': 'NYG', 'washington commanders': 'WAS', 'chicago bears': 'CHI',
            'detroit lions': 'DET', 'minnesota vikings': 'MIN', 'atlanta falcons': 'ATL',
            'carolina panthers': 'CAR', 'new orleans saints': 'NO', 'tampa bay buccaneers': 'TB',
            'arizona cardinals': 'ARI', 'los angeles rams': 'LAR'
        }
        return team_mappings.get(full_name, "")

    def _similarity_score(self, s1: str, s2: str) -> float:
        """Calculate similarity score between two strings (0.0 to 1.0)."""
        return SequenceMatcher(None, s1.lower(), s2.lower()).ratio()

    def _positions_equivalent(self, pos1: str, pos2: str) -> bool:
        """Check if two position strings are equivalent (handles DST/DEF variations)."""
        pos1_upper = pos1.upper()
        pos2_upper = pos2.upper()

        if pos1_upper == pos2_upper:
            return True

        # Defense equivalency
        defense_positions = {"DST", "DEF", "D/ST"}
        if pos1_upper in defense_positions and pos2_upper in defense_positions:
            return True

        return False

    def _teams_equivalent(self, espn_team: str, csv_team: str) -> bool:
        """Check if team abbreviations are equivalent."""
        espn_normalized = self._normalize_team_abbr(espn_team.upper())
        csv_normalized = self._normalize_team_abbr(csv_team.upper())
        return espn_normalized == csv_normalized

    def _normalize_team_abbr(self, team_abbr: str) -> str:
        """Normalize team abbreviations to handle inconsistencies."""
        team_mapping = {
            'WSH': 'WAS',  # Washington
            'WAS': 'WAS',
        }
        return team_mapping.get(team_abbr.upper(), team_abbr.upper())

    def _match_dst_by_team_abbr(self, team_abbr: str) -> str:
        """
        Match a DST player by team abbreviation when normal lookup fails.

        This handles the format mismatch between CSV ("Denver Broncos DEF")
        and JSON ("Broncos D/ST DST - DEN") by matching on team abbreviation.

        Args:
            team_abbr: Team abbreviation from player (e.g., "DEN", "HOU")

        Returns:
            Fantasy team name if match found, empty string otherwise
        """
        # Build reverse mapping from full team names to abbreviations
        full_name_to_abbr = {
            'seattle seahawks': 'SEA', 'baltimore ravens': 'BAL', 'san francisco 49ers': 'SF',
            'green bay packers': 'GB', 'pittsburgh steelers': 'PIT', 'dallas cowboys': 'DAL',
            'new england patriots': 'NE', 'denver broncos': 'DEN', 'buffalo bills': 'BUF',
            'miami dolphins': 'MIA', 'new york jets': 'NYJ', 'philadelphia eagles': 'PHI',
            'kansas city chiefs': 'KC', 'los angeles chargers': 'LAC', 'las vegas raiders': 'LV',
            'cincinnati bengals': 'CIN', 'cleveland browns': 'CLE', 'houston texans': 'HOU',
            'indianapolis colts': 'IND', 'tennessee titans': 'TEN', 'jacksonville jaguars': 'JAX',
            'new york giants': 'NYG', 'washington commanders': 'WAS', 'chicago bears': 'CHI',
            'detroit lions': 'DET', 'minnesota vikings': 'MIN', 'atlanta falcons': 'ATL',
            'carolina panthers': 'CAR', 'new orleans saints': 'NO', 'tampa bay buccaneers': 'TB',
            'arizona cardinals': 'ARI', 'los angeles rams': 'LAR'
        }

        # Normalize the incoming team abbreviation
        normalized_team = self._normalize_team_abbr(team_abbr)

        # Search through all drafted_players entries for DST matches
        for drafted_key, fantasy_team in self.drafted_players.items():
            # Check if this is a DST entry (contains "def" or "dst")
            if 'def' in drafted_key or 'dst' in drafted_key:
                # Extract team name from key (format: "denver broncos def" or "broncos dst")
                # Try to match against full team names
                for full_name, abbr in full_name_to_abbr.items():
                    if full_name in drafted_key and self._normalize_team_abbr(abbr) == normalized_team:
                        return fantasy_team

        return ""

    def _find_original_info_for_key(self, drafted_key: str) -> Optional[str]:
        """Find the original CSV data for a normalized key."""
        for row_data in self._original_csv_data:
            if len(row_data) >= 1 and self._normalize_player_info(row_data[0]) == drafted_key:
                return row_data[0]
        return None

    def _create_player_lookup(self, fantasy_players: List[FantasyPlayer]) -> Dict[str, any]:
        """
        Create optimized lookup dictionaries for different matching strategies.

        Creates multiple indexes for O(1) lookups during matching:
        - by_full_name: Single player per exact name (fastest match)
        - by_last_name: List of players with same last name (handles first name variations)
        - by_first_name: List of players with same first name (for unique names)
        - by_position_team: List of players at position on team (for defenses)
        - all_players: Full list for fuzzy matching fallback
        """
        lookup = {
            'by_full_name': {},      # Dict[str, FantasyPlayer]
            'by_last_name': {},      # Dict[str, List[FantasyPlayer]]
            'by_first_name': {},     # Dict[str, List[FantasyPlayer]]
            'by_position_team': {},  # Dict[str, List[FantasyPlayer]]
            'all_players': fantasy_players
        }

        for player in fantasy_players:
            # Full name lookup (O(1) access by exact name)
            full_name_key = player.name.lower().strip()
            lookup['by_full_name'][full_name_key] = player

            # Last name lookup (handles "Josh Allen" vs "Joshua Allen")
            name_parts = player.name.split()
            if name_parts:
                last_name_key = name_parts[-1].lower().strip()
                if last_name_key not in lookup['by_last_name']:
                    lookup['by_last_name'][last_name_key] = []
                lookup['by_last_name'][last_name_key].append(player)

                # First name lookup (for unique names like "Amon-Ra")
                first_name_key = name_parts[0].lower().strip()
                if first_name_key not in lookup['by_first_name']:
                    lookup['by_first_name'][first_name_key] = []
                lookup['by_first_name'][first_name_key].append(player)

            # Position + team lookup (useful for defense matching: "DEF_SEA")
            pos_team_key = f"{player.position}_{player.team}".lower()
            if pos_team_key not in lookup['by_position_team']:
                lookup['by_position_team'][pos_team_key] = []
            lookup['by_position_team'][pos_team_key].append(player)

        return lookup

    def _find_matching_player(
        self,
        drafted_name: str,
        drafted_pos: str,
        drafted_team: str,
        player_lookup: Dict
    ) -> Optional[FantasyPlayer]:
        """
        Find matching player using progressive exact -> fuzzy matching strategy.

        Progressive strategy (fastest to slowest, most reliable to least):
        1. Exact full name match (O(1) lookup)
        2. Defense-specific matching (handles name format variations)
        3. Exact last name + position/team validation (O(1) lookup)
        4. Exact first name for unique names (O(1) lookup)
        5. Fuzzy matching fallback (O(n) with similarity scoring)
        """

        # Strategy 1: Exact full name match (fastest, most reliable)
        # Example: "Josh Allen" -> finds player with exact name match
        full_name_key = drafted_name.lower().strip()
        if full_name_key in player_lookup['by_full_name']:
            player = player_lookup['by_full_name'][full_name_key]
            if self._validate_player_match(player, drafted_pos, drafted_team):
                return player

        # Strategy 2: Defense-specific matching
        # Defenses have inconsistent naming: "Seattle Seahawks DEF" vs "Seahawks D/ST"
        # Requires special handling to match across formats
        if drafted_pos.upper() in ['DEF', 'DST', 'D/ST']:
            defense_match = self._find_defense_match(drafted_name, drafted_pos, drafted_team, player_lookup)
            if defense_match:
                return defense_match

        # Strategy 3: Exact last name + validation
        # Handles cases where first name differs slightly (nickname vs full name)
        # Example: "Josh Allen" and "Joshua Allen" both match on "Allen"
        name_parts = drafted_name.split()
        if name_parts:
            last_name = name_parts[-1].lower().strip()
            if last_name in player_lookup['by_last_name']:
                for player in player_lookup['by_last_name'][last_name]:
                    if self._validate_player_match(player, drafted_pos, drafted_team):
                        return player

        # Strategy 4: Exact first name + validation (for unique names)
        # Only used when there's exactly one player with that first name
        # Example: "Amon-Ra" is unique enough to match without last name
        if name_parts:
            first_name = name_parts[0].lower().strip()
            if first_name in player_lookup['by_first_name']:
                candidates = player_lookup['by_first_name'][first_name]
                # Only use if unambiguous (single candidate)
                if len(candidates) == 1:
                    player = candidates[0]
                    if self._validate_player_match(player, drafted_pos, drafted_team):
                        return player

        # Strategy 5: Fuzzy matching fallback (slowest, least reliable)
        # Uses string similarity scoring (threshold >= 0.75)
        # Example: "St Brown" matches "St. Brown" with high similarity
        return self._fuzzy_match_player(drafted_name, drafted_pos, drafted_team, player_lookup['all_players'])

    def _find_defense_match(
        self,
        drafted_name: str,
        drafted_pos: str,
        drafted_team: str,
        player_lookup: Dict
    ) -> Optional[FantasyPlayer]:
        """
        Special defense matching to handle name format differences.

        Defenses have inconsistent naming across data sources:
        - CSV: "Seattle Seahawks DEF" or "Seattle Seahawks"
        - ESPN: "Seahawks D/ST" or "SEA D/ST"

        This method tries multiple variations to find matches:
        1. Team nickname variations (Seahawks, Seahawks D/ST, etc.)
        2. Full name variations (Seattle Seahawks DEF, etc.)
        3. Position + team code matching (DEF_SEA)
        """

        name_variations = []
        base_name = drafted_name.lower().strip()
        # Remove trailing "def" if present
        if base_name.endswith(' def'):
            base_name = base_name[:-4].strip()

        # Generate nickname variations (last word of team name)
        # "Seattle Seahawks" -> "Seahawks", "Seahawks D/ST", etc.
        name_parts = base_name.split()
        if len(name_parts) >= 2:
            team_nickname = name_parts[-1]  # "Seahawks"
            name_variations.extend([
                team_nickname,
                f"{team_nickname} d/st",
                f"{team_nickname} def",
                f"{team_nickname} dst",
            ])

        # Generate full name variations
        # "Seattle Seahawks" -> "Seattle Seahawks D/ST", etc.
        name_variations.extend([
            base_name,
            f"{base_name} d/st",
            f"{base_name} def",
            f"{base_name} dst",
        ])

        # Try each name variation for exact match
        for variation in name_variations:
            variation_key = variation.lower().strip()
            if variation_key in player_lookup['by_full_name']:
                player = player_lookup['by_full_name'][variation_key]
                if self._validate_player_match(player, drafted_pos, drafted_team):
                    return player

        # Fallback: position + team matching (DEF_SEA, DST_SEA, etc.)
        # This works when name format is too different but team code matches
        pos_team_key = f"{drafted_pos.upper()}_{drafted_team.upper()}"
        if pos_team_key in player_lookup['by_position_team']:
            candidates = player_lookup['by_position_team'][pos_team_key]
            # Only use if unambiguous (exactly one defense for that team)
            if len(candidates) == 1:
                return candidates[0]

        return None

    def _validate_player_match(self, player: FantasyPlayer, drafted_pos: str, drafted_team: str) -> bool:
        """Validate that player matches position and team requirements."""
        if not self._positions_equivalent(player.position, drafted_pos):
            return False

        if drafted_team and not self._teams_equivalent(player.team, drafted_team):
            return False

        return True

    def _fuzzy_match_player(
        self,
        drafted_name: str,
        drafted_pos: str,
        drafted_team: str,
        all_players: List[FantasyPlayer]
    ) -> Optional[FantasyPlayer]:
        """
        Fallback fuzzy matching using similarity scoring.

        Uses SequenceMatcher to calculate string similarity ratio (0.0 to 1.0).
        Threshold of 0.75 provides good balance between accuracy and recall.

        Example matches:
        - "St. Brown WR - DET" vs "St Brown WR - DET" = 0.98 (match)
        - "Josh Allen QB - BUF" vs "Josh Allen QB - BUF" = 1.0 (perfect)
        - "Chris Jones DT - KC" vs "Chris Smith DT - KC" = 0.87 (match)
        - "Josh Allen QB - BUF" vs "Josh Allen QB - CLE" = 0.87 (rejected - wrong team)
        """
        best_score = 0.0
        best_match = None

        # Build normalized search string with position and team for context
        search_string = f"{drafted_name} {drafted_pos} - {drafted_team}".lower()
        normalized_search = self._normalize_player_info(search_string)

        # Check each player for similarity
        for player in all_players:
            player_string = f"{player.name} {player.position} - {player.team}".lower()
            normalized_player = self._normalize_player_info(player_string)

            # Calculate similarity ratio (0.0 to 1.0)
            score = self._similarity_score(normalized_search, normalized_player)

            # Accept matches >= 0.75 similarity that pass validation
            # 0.75 threshold avoids false positives while catching minor variations
            if score >= 0.75 and score > best_score:
                if self._validate_player_match(player, drafted_pos, drafted_team):
                    best_score = score
                    best_match = player

        return best_match
