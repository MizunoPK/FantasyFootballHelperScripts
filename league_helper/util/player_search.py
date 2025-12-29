#!/usr/bin/env python3
"""
League Helper Player Search

This module handles all player search functionality including fuzzy name matching.
Extracted from old_structure/draft_helper/core/player_search.py for league_helper.

Author: Kai Mizuno
"""

from typing import List, Optional
from utils.FantasyPlayer import FantasyPlayer
from league_helper.util.user_input import show_list_selection


class PlayerSearch:
    """Handles player search functionality with fuzzy name matching"""

    def __init__(self, players: List[FantasyPlayer]):
        """
        Initialize the player search system

        Args:
            players: List of FantasyPlayer objects to search through
        """
        self.players = players

    def search_players_by_name(self, search_term: str,
                              drafted_filter: Optional[int] = None,
                              exact_match: bool = False) -> List[FantasyPlayer]:
        """
        Search for players by name with fuzzy matching

        Args:
            search_term: Name or partial name to search for
            drafted_filter: Filter by drafted status (0=available, 1=drafted by others, 2=on roster, None=all)
            exact_match: Whether to require exact matches vs fuzzy matching

        Returns:
            List of matching FantasyPlayer objects
        """
        # Handle empty search term early
        if not search_term:
            return []

        # Filter players by drafted status if specified
        # This allows searching within specific groups (available, drafted, or roster)
        if drafted_filter is not None:
            if drafted_filter == 0:
                # Available players only (not yet drafted)
                candidate_players = [p for p in self.players if p.is_free_agent()]
            elif drafted_filter == 1:
                # Drafted by others only (not on user's roster)
                candidate_players = [p for p in self.players if p.is_drafted_by_opponent()]
            elif drafted_filter == 2:
                # On user's roster only
                candidate_players = [p for p in self.players if p.is_rostered()]
            else:
                # Invalid filter value - search all players
                candidate_players = self.players
        else:
            # No filter specified - search all players
            candidate_players = self.players

        matches = []
        # Convert search term to lowercase for case-insensitive matching
        search_lower = search_term.lower()

        # Check each candidate player for a match
        for player in candidate_players:
            name_lower = player.name.lower()
            name_words = name_lower.split()

            if exact_match:
                # Exact name match (full name must match exactly)
                # Example: "patrick mahomes" matches "Patrick Mahomes" but not "Patrick"
                if name_lower == search_lower:
                    matches.append(player)
            else:
                # Fuzzy matching with multiple strategies:
                # 1. Substring match: "mahom" matches "Patrick Mahomes"
                # 2. Word match: "pat" matches "Patrick Mahomes" (word starts with "pat")
                # 3. Word contains: "trick" matches "Patrick Mahomes" (word contains "trick")
                if (search_lower in name_lower or
                    any(search_lower in word or word.startswith(search_lower)
                        for word in name_words)):
                    matches.append(player)

        return matches

    def search_players_by_name_not_available(self, search_term: str,
                                            exact_match: bool = False) -> List[FantasyPlayer]:
        """
        Search for players who are NOT available (drafted != 0)

        This is a helper method for Drop Player mode which needs to search
        players with drafted=1 OR drafted=2.

        Args:
            search_term: Name or partial name to search for
            exact_match: Whether to require exact matches vs fuzzy matching

        Returns:
            List of matching FantasyPlayer objects with drafted != 0
        """
        # Handle empty search term early
        if not search_term:
            return []

        # Filter to only non-available players (not free agents)
        # This includes both drafted by opponents and on our roster
        # Used primarily in Drop Player mode where we need to search across both groups
        candidate_players = [p for p in self.players if not p.is_free_agent()]

        matches = []
        # Convert search term to lowercase for case-insensitive matching
        search_lower = search_term.lower()

        # Check each candidate player for a match
        for player in candidate_players:
            name_lower = player.name.lower()
            name_words = name_lower.split()

            if exact_match:
                # Exact name match (full name must match exactly)
                if name_lower == search_lower:
                    matches.append(player)
            else:
                # Fuzzy matching with multiple strategies:
                # 1. Substring match: "mahom" matches "Patrick Mahomes"
                # 2. Word match: "pat" matches "Patrick Mahomes" (word starts with "pat")
                # 3. Word contains: "trick" matches "Patrick Mahomes" (word contains "trick")
                if (search_lower in name_lower or
                    any(search_lower in word or word.startswith(search_lower)
                        for word in name_words)):
                    matches.append(player)

        return matches

    def interactive_search(self, drafted_filter: Optional[int] = None,
                          prompt: str = "Enter player name (or part of name) to search (or press Enter to exit): ",
                          not_available: bool = False) -> Optional[FantasyPlayer]:
        """
        Interactive fuzzy player search with continuous loop

        Args:
            drafted_filter: Filter by drafted status (0, 1, 2, or None for all)
            prompt: Custom prompt to display to user
            not_available: If True, search players with drafted != 0 (for Drop Player mode)

        Returns:
            Selected FantasyPlayer object, or None if user exits
        """
        # Continuous loop until user selects a player or exits
        while True:
            # Get search term from user
            search_term = input(f"\n{prompt}").strip()

            # Check for exit conditions: empty input or explicit 'exit' command
            if not search_term or search_term.lower() == 'exit':
                print("Exiting search...")
                return None

            try:
                # Find matching players based on search mode
                if not_available:
                    # Special search for Drop Player mode: search both drafted=1 and drafted=2
                    matches = self.search_players_by_name_not_available(search_term)
                else:
                    # Normal search with optional drafted status filter
                    matches = self.search_players_by_name(search_term, drafted_filter=drafted_filter)

                # Handle no matches case - prompt user to try again
                if not matches:
                    print(f"No players found matching '{search_term}'. Try again or press Enter to exit.")
                    continue

                # Display all matching players with numbered options
                print(f"\nFound {len(matches)} matching player(s):")
                for i, player in enumerate(matches, start=1):
                    print(f"{i}. {player}")

                # Add "Search again" option at the end
                # This allows users to refine their search if they don't see their intended player
                options_count = len(matches)
                print(f"{options_count + 1}. Search again")

                try:
                    # Get user's selection
                    choice = int(input(f"Enter your choice (1-{options_count + 1}): ").strip())

                    if 1 <= choice <= options_count:
                        # User selected a player from the matches
                        # Convert 1-based index to 0-based index
                        selected_player = matches[choice - 1]
                        return selected_player
                    elif choice == options_count + 1:
                        # User chose to search again - continue the loop
                        continue
                    else:
                        # Choice out of valid range
                        print("Invalid choice. Please try again.")
                        continue

                except ValueError:
                    # Handle non-integer input
                    print("Invalid input. Please enter a number.")
                    continue

            except Exception as e:
                # Handle unexpected errors gracefully
                print(f"Error during search: {e}")
                print("Returning to previous menu...")
                return None

    def find_players_by_drafted_status(self, drafted_status: int) -> List[FantasyPlayer]:
        """
        Find all players with a specific drafted status

        Args:
            drafted_status: 0=available, 1=drafted by others, 2=on roster

        Returns:
            List of players with the specified status

        Note: This method maintains backward compatibility with the legacy int API.
        Internally uses helper methods (is_free_agent(), is_drafted_by_opponent(), is_rostered()).
        """
        if drafted_status == 0:
            return [p for p in self.players if p.is_free_agent()]
        elif drafted_status == 1:
            return [p for p in self.players if p.is_drafted_by_opponent()]
        elif drafted_status == 2:
            return [p for p in self.players if p.is_rostered()]
        else:
            return []

    def get_roster_players(self) -> List[FantasyPlayer]:
        """Get all players on the user's roster."""
        return [p for p in self.players if p.is_rostered()]

    def get_available_players(self) -> List[FantasyPlayer]:
        """Get all available players (free agents)."""
        return [p for p in self.players if p.is_free_agent()]

    def get_drafted_players(self) -> List[FantasyPlayer]:
        """Get all players drafted by opponent teams."""
        return [p for p in self.players if p.is_drafted_by_opponent()]
