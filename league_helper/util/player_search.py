#!/usr/bin/env python3
"""
League Helper Player Search

This module handles all player search functionality including fuzzy name matching.
Extracted from old_structure/draft_helper/core/player_search.py for league_helper.

Author: Kai Mizuno
"""

from typing import List, Optional
from utils.FantasyPlayer import FantasyPlayer



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

        if drafted_filter is not None:
            if drafted_filter == 0:
                candidate_players = [p for p in self.players if p.is_free_agent()]
            elif drafted_filter == 1:
                candidate_players = [p for p in self.players if p.is_drafted_by_opponent()]
            elif drafted_filter == 2:
                candidate_players = [p for p in self.players if p.is_rostered()]
            else:
                candidate_players = self.players
        else:
            candidate_players = self.players

        matches = []
        search_lower = search_term.lower()

        for player in candidate_players:
            name_lower = player.name.lower()
            name_words = name_lower.split()

            if exact_match:
                if name_lower == search_lower:
                    matches.append(player)
            else:
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

        candidate_players = [p for p in self.players if not p.is_free_agent()]

        matches = []
        search_lower = search_term.lower()

        for player in candidate_players:
            name_lower = player.name.lower()
            name_words = name_lower.split()

            if exact_match:
                if name_lower == search_lower:
                    matches.append(player)
            else:
                if (search_lower in name_lower or
                    any(search_lower in word or word.startswith(search_lower)
                        for word in name_words)):
                    matches.append(player)

        return matches

    def interactive_search(self, drafted_filter: Optional[int] = None,
                          prompt: str = "Enter player name (or part of name) to search (or press Enter to exit): ",
                          not_available: bool = False,
                          max_search_results: Optional[int] = None) -> Optional[FantasyPlayer]:
        """
        Interactive fuzzy player search with continuous loop

        Args:
            drafted_filter: Filter by drafted status (0, 1, 2, or None for all)
            prompt: Custom prompt to display to user
            not_available: If True, search players with drafted != 0 (for Drop Player mode)
            max_search_results: If set, caps the number of displayed results and prints a truncation message

        Returns:
            Selected FantasyPlayer object, or None if user exits
        """
        while True:
            search_term = input(f"\n{prompt}").strip()

            if not search_term or search_term.lower() == 'exit':
                print("Exiting search...")
                return None

            try:
                if not_available:
                    matches = self.search_players_by_name_not_available(search_term)
                else:
                    matches = self.search_players_by_name(search_term, drafted_filter=drafted_filter)

                if not matches:
                    print(f"No players found matching '{search_term}'. Try again or press Enter to exit.")
                    continue

                total_matches = len(matches)
                if max_search_results is not None and total_matches > max_search_results:
                    matches = matches[:max_search_results]
                    print(f"Showing first {max_search_results} of {total_matches} matches — try a more specific search.")

                print(f"\nFound {len(matches)} matching player(s):")
                for i, player in enumerate(matches, start=1):
                    print(f"{i}. {player}")

                options_count = len(matches)
                print(f"{options_count + 1}. Search again")

                try:
                    choice = int(input(f"Enter your choice (1-{options_count + 1}): ").strip())

                    if 1 <= choice <= options_count:
                        selected_player = matches[choice - 1]
                        return selected_player
                    elif choice == options_count + 1:
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


