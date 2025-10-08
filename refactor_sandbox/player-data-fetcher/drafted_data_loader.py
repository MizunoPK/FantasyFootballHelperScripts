#!/usr/bin/env python3
"""
Drafted Data Loader Module

This module handles loading and processing drafted player data from external CSV files.
Provides fuzzy matching functionality to identify players and assign drafted states.

Author: Kai Mizuno
Created: September 2025
"""

import csv
import re
from difflib import SequenceMatcher
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set

from config import LOAD_DRAFTED_DATA_FROM_FILE, DRAFTED_DATA, MY_TEAM_NAME

import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.LoggingManager import get_logger


class DraftedDataLoader:
    """Handles loading and fuzzy matching of drafted player data from CSV files"""

    def __init__(self):
        self.logger = get_logger()
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

        # Remove common noise text that appears in CSV entries (be more specific)
        normalized = re.sub(r'\b(q view news|view news)\b', '', normalized)
        normalized = re.sub(r'\b(sus|ir|nfi-r)\b', '', normalized)
        # Only remove single letters that are clearly status indicators (not part of names)
        normalized = re.sub(r'\s+(o|q)(\s|$)', r'\1', normalized)  # Only remove O or Q at word boundaries after spaces

        # Normalize punctuation
        normalized = normalized.replace('.', '').replace("'", '').replace('-', ' ')

        # Clean up multiple spaces
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
        # Pattern to match: "Name Position - Team"
        # Handles cases like "Amon-Ra St. Brown WR - DET" or "Tucker Kraft TE - GB Q View News"
        pattern = r'^(.+?)\s+([A-Z]{1,3})\s*-\s*([A-Z]{2,4})'

        match = re.match(pattern, player_info.strip())
        if match:
            name = match.group(1).strip()
            position = match.group(2).strip()
            team = match.group(3).strip().split()[0]  # Take first part in case of extra info
            return name, position, team

        # Special case for defenses: "Seattle Seahawks DEF" or "Seattle Seahawks DEF View News" -> extract team from name
        parts = player_info.strip().split()
        defense_position = None

        # Look for defense position anywhere in the parts (not just at the end due to "View News" suffix)
        for i, part in enumerate(parts):
            if part.upper() in ['DEF', 'DST'] or part.upper() == 'D/ST':
                defense_position = part.upper()
                name_parts = parts[:i]  # Everything before the position marker
                break

        if defense_position and len(name_parts) >= 1:
            # For defenses, extract team abbreviation from team name
            team = ""
            full_name = ' '.join(name_parts).lower()

            # Common team name mappings
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

            team = team_mappings.get(full_name, "")

            return ' '.join(name_parts), defense_position, team

        # Fallback: try to extract what we can for regular players
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

    def _positions_equivalent(self, pos1: str, pos2: str) -> bool:
        """Check if two position strings are equivalent (handling DST/DEF variations)"""
        pos1_upper = pos1.upper()
        pos2_upper = pos2.upper()

        # Direct match
        if pos1_upper == pos2_upper:
            return True

        # Defense equivalency: DST, DEF, and D/ST are the same
        defense_positions = {"DST", "DEF", "D/ST"}
        if pos1_upper in defense_positions and pos2_upper in defense_positions:
            return True

        return False

    def _normalize_defense_name(self, name: str) -> str:
        """Normalize defense names to handle variations like 'Seahawks D/ST' vs 'Seattle Seahawks'"""
        name_lower = name.lower()

        # Handle common defense name variations
        defense_name_mappings = {
            'seahawks d/st': 'seattle seahawks',
            'seahawks': 'seattle seahawks',
            'ravens d/st': 'baltimore ravens',
            'ravens': 'baltimore ravens',
            '49ers d/st': 'san francisco 49ers',
            '49ers': 'san francisco 49ers',
            'packers d/st': 'green bay packers',
            'packers': 'green bay packers',
            'steelers d/st': 'pittsburgh steelers',
            'steelers': 'pittsburgh steelers',
            'cowboys d/st': 'dallas cowboys',
            'cowboys': 'dallas cowboys',
            'patriots d/st': 'new england patriots',
            'patriots': 'new england patriots',
            'broncos d/st': 'denver broncos',
            'broncos': 'denver broncos',
            'bills d/st': 'buffalo bills',
            'bills': 'buffalo bills',
        }

        return defense_name_mappings.get(name_lower, name_lower)

    def _find_original_info_for_key(self, drafted_key: str) -> Optional[str]:
        """Find the original CSV data for a given normalized key"""
        try:
            for row_data in self._get_original_data():
                if len(row_data) >= 1 and self._normalize_player_info(row_data[0]) == drafted_key:
                    return row_data[0]
            return None
        except Exception:
            return None

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

        # For defenses, also try normalized defense name variations
        defense_searches = [normalized_search]
        if player_position.upper() in ['DST', 'DEF', 'D/ST']:
            normalized_def_name = self._normalize_defense_name(player_name)
            alt_search = f"{normalized_def_name} {player_position} - {player_team}".lower()
            alt_normalized = self._normalize_player_info(alt_search)
            if alt_normalized != normalized_search:
                defense_searches.append(alt_normalized)

        best_match_score = 0.0
        best_match_team = None
        best_drafted_key = None

        # Search through all drafted players
        for drafted_key, fantasy_team in self.drafted_players.items():
            # Calculate similarity score for each search variation
            for search_variant in defense_searches:
                score = self._similarity_score(search_variant, drafted_key)

                if score > best_match_score and score >= 0.8:  # Must be above minimum threshold
                    # Extract components for basic validation
                    original_info = self._find_original_info_for_key(drafted_key)

                    if original_info:
                        drafted_name, drafted_pos, drafted_team_csv = self._extract_player_components(original_info)

                        # Check if position and team are compatible
                        position_match = self._positions_equivalent(drafted_pos, player_position)
                        team_match = drafted_team_csv.upper() == player_team.upper()

                        if position_match and team_match:
                            # Full match - use original score
                            best_match_score = score
                            best_match_team = fantasy_team
                            best_drafted_key = drafted_key
                        # If position or team don't match, ignore this candidate
                    else:
                        # Can't validate, but if score is very high, accept it
                        if score >= 0.9:
                            best_match_score = score
                            best_match_team = fantasy_team
                            best_drafted_key = drafted_key

        # Return result if we have a good match
        if best_match_score >= 0.8:
            if best_match_team == MY_TEAM_NAME:
                self.logger.debug(f"Found player on user's team: {player_name} {player_position} - {player_team} (matched '{best_drafted_key}', score: {best_match_score:.3f})")
                return 2
            else:
                self.logger.debug(f"Found drafted player: {player_name} {player_position} - {player_team} (team: {best_match_team}, score: {best_match_score:.3f})")
                return 1

        return 0

    def apply_drafted_data_to_players(self, fantasy_players: List) -> List:
        """
        Apply drafted data from CSV to a list of FantasyPlayer objects (REVERSE SEARCH APPROACH).

        Instead of checking each player against CSV, iterate through CSV entries and find matches in player data.
        This is more reliable for ensuring all CSV players are found.

        Args:
            fantasy_players: List of FantasyPlayer objects to update

        Returns:
            List of FantasyPlayer objects with updated drafted values
        """
        if not LOAD_DRAFTED_DATA_FROM_FILE or not self.drafted_players:
            return fantasy_players

        # Create lookup dictionary for fast player access by various keys
        player_lookup = self._create_player_lookup(fantasy_players)

        # Track matches for logging
        matches_found = 0

        # Iterate through each CSV entry and find corresponding player
        for drafted_key, fantasy_team in self.drafted_players.items():
            # Find original CSV entry to extract components
            original_info = self._find_original_info_for_key(drafted_key)
            if not original_info:
                self.logger.warning(f"Could not find original CSV data for: {drafted_key}")
                continue

            # Extract player components from CSV entry
            drafted_name, drafted_pos, drafted_team_abbr = self._extract_player_components(original_info)
            if not drafted_name or not drafted_pos:
                self.logger.warning(f"Could not parse CSV entry: {original_info}")
                continue

            # Find matching player using progressive matching strategy
            matched_player = self._find_matching_player(
                drafted_name, drafted_pos, drafted_team_abbr, player_lookup
            )

            if matched_player:
                # Update drafted value: 2 for MY_TEAM_NAME, 1 for others
                drafted_value = 2 if fantasy_team == MY_TEAM_NAME else 1
                matched_player.drafted = drafted_value
                matches_found += 1

                self.logger.debug(f"Applied drafted={drafted_value} to {matched_player.name} (matched '{original_info}')")
            else:
                self.logger.warning(f"Could not find player in data for CSV entry: {original_info}")

        self.logger.info(f"Applied drafted data: {matches_found}/{len(self.drafted_players)} CSV entries matched")
        return fantasy_players

    def _create_player_lookup(self, fantasy_players: List) -> Dict[str, any]:
        """Create optimized lookup dictionaries for different matching strategies"""
        lookup = {
            'by_full_name': {},
            'by_last_name': {},
            'by_first_name': {},
            'by_position_team': {},
            'all_players': fantasy_players
        }

        for player in fantasy_players:
            # Full name lookup
            full_name_key = player.name.lower().strip()
            lookup['by_full_name'][full_name_key] = player

            # Last name lookup (for exact matching first)
            name_parts = player.name.split()
            if name_parts:
                last_name_key = name_parts[-1].lower().strip()
                if last_name_key not in lookup['by_last_name']:
                    lookup['by_last_name'][last_name_key] = []
                lookup['by_last_name'][last_name_key].append(player)

                # First name lookup
                first_name_key = name_parts[0].lower().strip()
                if first_name_key not in lookup['by_first_name']:
                    lookup['by_first_name'][first_name_key] = []
                lookup['by_first_name'][first_name_key].append(player)

            # Position + team lookup for additional validation
            pos_team_key = f"{player.position}_{player.team}".lower()
            if pos_team_key not in lookup['by_position_team']:
                lookup['by_position_team'][pos_team_key] = []
            lookup['by_position_team'][pos_team_key].append(player)

        return lookup

    def _find_defense_match(self, drafted_name: str, drafted_pos: str, drafted_team: str, player_lookup: Dict) -> any:
        """Special defense matching to handle name format differences"""

        # Common defense name patterns to try
        # CSV might be "Seattle Seahawks" while ESPN is "Seahawks D/ST"
        name_variations = []

        # Remove "DEF" suffix if present and add common variations
        base_name = drafted_name.lower().strip()
        if base_name.endswith(' def'):
            base_name = base_name[:-4].strip()

        # For team names, try both full and short versions
        name_parts = base_name.split()
        if len(name_parts) >= 2:
            # Try just the team nickname (last word)
            team_nickname = name_parts[-1]
            name_variations.extend([
                team_nickname,                    # "seahawks"
                f"{team_nickname} d/st",         # "seahawks d/st"
                f"{team_nickname} def",          # "seahawks def"
                f"{team_nickname} dst",          # "seahawks dst"
            ])

        # Try full name variations too
        name_variations.extend([
            base_name,                           # "seattle seahawks"
            f"{base_name} d/st",                # "seattle seahawks d/st"
            f"{base_name} def",                 # "seattle seahawks def"
            f"{base_name} dst",                 # "seattle seahawks dst"
        ])

        # Search for matches using each variation
        for variation in name_variations:
            variation_key = variation.lower().strip()
            if variation_key in player_lookup['by_full_name']:
                player = player_lookup['by_full_name'][variation_key]
                if self._validate_player_match(player, drafted_pos, drafted_team):
                    return player

        # Try position + team matching for defenses (fallback)
        pos_team_key = f"{drafted_pos.upper()}_{drafted_team.upper()}"
        if pos_team_key in player_lookup['by_position_team']:
            candidates = player_lookup['by_position_team'][pos_team_key]
            if len(candidates) == 1:
                return candidates[0]  # Unique match by position and team

        return None

    def _find_matching_player(self, drafted_name: str, drafted_pos: str, drafted_team: str, player_lookup: Dict) -> any:
        """Find matching player using progressive exact -> fuzzy matching strategy"""

        # Strategy 1: Exact full name match
        full_name_key = drafted_name.lower().strip()
        if full_name_key in player_lookup['by_full_name']:
            player = player_lookup['by_full_name'][full_name_key]
            if self._validate_player_match(player, drafted_pos, drafted_team):
                return player

        # Strategy 2: Defense-specific matching (special case for name format differences)
        if drafted_pos.upper() in ['DEF', 'DST', 'D/ST']:
            # Handle common defense name variations
            defense_match = self._find_defense_match(drafted_name, drafted_pos, drafted_team, player_lookup)
            if defense_match:
                return defense_match

        # Strategy 3: Exact last name + position/team validation
        name_parts = drafted_name.split()
        if name_parts:
            last_name = name_parts[-1].lower().strip()
            if last_name in player_lookup['by_last_name']:
                for player in player_lookup['by_last_name'][last_name]:
                    if self._validate_player_match(player, drafted_pos, drafted_team):
                        return player

        # Strategy 4: Exact first name + position/team validation (for unique names)
        if name_parts:
            first_name = name_parts[0].lower().strip()
            if first_name in player_lookup['by_first_name']:
                candidates = player_lookup['by_first_name'][first_name]
                if len(candidates) == 1:  # Only if unique first name
                    player = candidates[0]
                    if self._validate_player_match(player, drafted_pos, drafted_team):
                        return player

        # Strategy 5: Fuzzy matching fallback (existing logic)
        return self._fuzzy_match_player(drafted_name, drafted_pos, drafted_team, player_lookup['all_players'])

    def _validate_player_match(self, player: any, drafted_pos: str, drafted_team: str) -> bool:
        """Validate that player matches position and team requirements"""
        # Position validation
        if not self._positions_equivalent(player.position, drafted_pos):
            return False

        # Team validation with abbreviation normalization
        if drafted_team and not self._teams_equivalent(player.team, drafted_team):
            return False

        return True

    def _teams_equivalent(self, espn_team: str, csv_team: str) -> bool:
        """Check if team abbreviations are equivalent, handling common inconsistencies"""
        espn_normalized = self._normalize_team_abbr(espn_team.upper())
        csv_normalized = self._normalize_team_abbr(csv_team.upper())
        return espn_normalized == csv_normalized

    def _normalize_team_abbr(self, team_abbr: str) -> str:
        """Normalize team abbreviations to handle ESPN vs CSV inconsistencies"""
        # Common team abbreviation mappings (ESPN -> Standard)
        team_mapping = {
            'WSH': 'WAS',  # Washington: ESPN uses WSH, CSV uses WAS
            'WAS': 'WAS',  # Keep WAS as standard
            # Add other mappings as discovered
        }

        return team_mapping.get(team_abbr.upper(), team_abbr.upper())

    def _fuzzy_match_player(self, drafted_name: str, drafted_pos: str, drafted_team: str, all_players: List) -> any:
        """Fallback fuzzy matching using existing similarity logic"""
        best_score = 0.0
        best_match = None

        # Create search string similar to existing approach
        search_string = f"{drafted_name} {drafted_pos} - {drafted_team}".lower()
        normalized_search = self._normalize_player_info(search_string)

        for player in all_players:
            player_string = f"{player.name} {player.position} - {player.team}".lower()
            normalized_player = self._normalize_player_info(player_string)

            score = self._similarity_score(normalized_search, normalized_player)

            # Use slightly lower threshold since we know these players should exist
            if score >= 0.75 and score > best_score:
                if self._validate_player_match(player, drafted_pos, drafted_team):
                    best_score = score
                    best_match = player

        return best_match

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