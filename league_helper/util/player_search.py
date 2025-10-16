#!/usr/bin/env python3
"""
League Helper Player Search

This module handles all player search functionality including fuzzy name matching.
Extracted from old_structure/draft_helper/core/player_search.py for league_helper.

Author: Kai Mizuno
Last Updated: October 2025
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
        if not search_term:
            return []

        # Filter players by drafted status if specified
        if drafted_filter is not None:
            if drafted_filter == 0:
                # Available players only
                candidate_players = [p for p in self.players if p.drafted == 0]
            elif drafted_filter == 1:
                # Drafted by others only
                candidate_players = [p for p in self.players if p.drafted == 1]
            elif drafted_filter == 2:
                # On roster only
                candidate_players = [p for p in self.players if p.drafted == 2]
            else:
                candidate_players = self.players
        else:
            # All players if no filter specified
            candidate_players = self.players

        matches = []
        search_lower = search_term.lower()

        for player in candidate_players:
            name_lower = player.name.lower()
            name_words = name_lower.split()

            if exact_match:
                # Exact name match
                if name_lower == search_lower:
                    matches.append(player)
            else:
                # Fuzzy matching - check if search term matches any part of the name
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
        if not search_term:
            return []

        # Filter to only non-available players (drafted != 0)
        candidate_players = [p for p in self.players if p.drafted != 0]

        matches = []
        search_lower = search_term.lower()

        for player in candidate_players:
            name_lower = player.name.lower()
            name_words = name_lower.split()

            if exact_match:
                # Exact name match
                if name_lower == search_lower:
                    matches.append(player)
            else:
                # Fuzzy matching - check if search term matches any part of the name
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
        while True:
            search_term = input(f"\n{prompt}").strip()

            # Check if user wants to exit (empty input or 'exit')
            if not search_term or search_term.lower() == 'exit':
                print("Exiting search...")
                return None

            try:
                # Find matching players
                if not_available:
                    # Use special search for drafted != 0 (Drop Player mode)
                    matches = self.search_players_by_name_not_available(search_term)
                else:
                    # Use normal search with drafted_filter
                    matches = self.search_players_by_name(search_term, drafted_filter=drafted_filter)

                if not matches:
                    print(f"No players found matching '{search_term}'. Try again or press Enter to exit.")
                    continue

                # Show matches using show_list_selection
                print(f"\nFound {len(matches)} matching player(s):")
                for i, player in enumerate(matches, start=1):
                    print(f"{i}. {player}")

                # Add "Search again" option
                options_count = len(matches)
                print(f"{options_count + 1}. Search again")

                try:
                    choice = int(input(f"Enter your choice (1-{options_count + 1}): ").strip())

                    if 1 <= choice <= options_count:
                        # Return selected player
                        selected_player = matches[choice - 1]
                        return selected_player
                    elif choice == options_count + 1:
                        # Search again
                        continue
                    else:
                        print("Invalid choice. Please try again.")
                        continue

                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue

            except Exception as e:
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
        """
        return [p for p in self.players if p.drafted == drafted_status]

    def get_roster_players(self) -> List[FantasyPlayer]:
        """Get all players on the user's roster (drafted=2)"""
        return self.find_players_by_drafted_status(2)

    def get_available_players(self) -> List[FantasyPlayer]:
        """Get all available players (drafted=0)"""
        return self.find_players_by_drafted_status(0)

    def get_drafted_players(self) -> List[FantasyPlayer]:
        """Get all players drafted by others (drafted=1)"""
        return self.find_players_by_drafted_status(1)
