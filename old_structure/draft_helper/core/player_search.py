#!/usr/bin/env python3
"""
Draft Helper Player Search

This module handles all player search functionality including fuzzy name matching.

Author: Kai Mizuno
Last Updated: September 2025
"""

import sys
from pathlib import Path
from typing import List, Optional

# Add parent directories to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from shared_files.FantasyPlayer import FantasyPlayer


class PlayerSearch:
    """Handles player search functionality with fuzzy name matching"""

    def __init__(self, players: List[FantasyPlayer], logger=None):
        """
        Initialize the player search system

        Args:
            players: List of FantasyPlayer objects to search through
            logger: Optional logger for debugging
        """
        self.players = players
        self.logger = logger

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
            # All players if no filter specified, but exclude available when searching drafted
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

    def search_and_mark_player_interactive(self, save_callback) -> bool:
        """
        Interactive search and mark player as drafted by others

        Args:
            save_callback: Function to call to save player data after marking

        Returns:
            True if search completed successfully, False if user cancelled
        """
        while True:
            search_term = input("\nEnter player name (or part of name) to search (or press Enter to return to Main Menu): ").strip()

            # Check if user wants to exit (either 'exit' command or empty input)
            if not search_term or search_term.lower() == 'exit':
                print("Returning to Main Menu...")
                return False

            try:
                # Find matching available players
                matches = self.search_players_by_name(search_term, drafted_filter=0)

                if not matches:
                    print(f"No players found matching '{search_term}'. Try again or type 'exit' to return to Main Menu.")
                    continue

                # Show matches
                print(f"\nFound {len(matches)} matching player(s):")
                for i, player in enumerate(matches, start=1):
                    print(f"{i}. {player}")

                print(f"{len(matches) + 1}. Search again")

                try:
                    choice = int(input(f"Enter your choice (1-{len(matches) + 1}): ").strip())

                    if 1 <= choice <= len(matches):
                        # Mark selected player as drafted
                        selected_player = matches[choice - 1]
                        selected_player.drafted = 1
                        save_callback()
                        print(f"✅ Marked {selected_player.name} as drafted by another team!")
                        if self.logger:
                            self.logger.info(f"Player {selected_player.name} marked as drafted=1")
                        # Continue searching for more players
                        continue
                    elif choice == len(matches) + 1:
                        # Search again
                        continue
                    else:
                        print("Invalid choice. Please try again.")
                        continue

                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue
                except Exception as e:
                    print(f"Error marking player as drafted: {e}")
                    print("Returning to Main Menu...")
                    if self.logger:
                        self.logger.error(f"Error marking player as drafted: {e}")
                    return False

            except Exception as e:
                print(f"Error during search: {e}")
                print("Returning to previous menu...")
                if self.logger:
                    self.logger.error(f"Error during player search: {e}")
                return False

    def search_and_drop_player_interactive(self, save_callback) -> bool:
        """
        Interactive search and drop player from roster

        Args:
            save_callback: Function to call to save player data after dropping

        Returns:
            True if search completed successfully, False if user cancelled
        """
        while True:
            search_term = input("\nEnter player name (or part of name) to search (or press Enter to return to Main Menu): ").strip()

            # Check if user wants to exit (either 'exit' command or empty input)
            if not search_term or search_term.lower() == 'exit':
                print("Returning to Main Menu...")
                return False

            try:
                # Find matching drafted players (both roster and others)
                drafted_players = [p for p in self.players if p.drafted != 0]
                matches = []

                search_lower = search_term.lower()

                # Search for partial matches - use stricter matching for drop to avoid accidents
                for player in drafted_players:
                    name_lower = player.name.lower()
                    name_words = name_lower.split()

                    # Check if search term matches beginning of first or last name
                    for word in name_words:
                        if word.startswith(search_lower):
                            matches.append(player)
                            break

                if not matches:
                    print(f"No drafted players found matching '{search_term}'. Try again or type 'exit' to return to Main Menu.")
                    continue

                # Display matches
                print(f"\nFound {len(matches)} player(s) matching '{search_term}':")
                for i, player in enumerate(matches, 1):
                    status = "On Your Roster" if player.drafted == 2 else "Drafted by Others"
                    print(f"{i}. {player.name} ({player.position}, {player.team}) - {status}")

                choice_input = input(f"Select a player to drop (1-{len(matches)}) or 'exit' to return to Main Menu: ").strip()

                if choice_input.lower() == 'exit':
                    return False

                try:
                    choice = int(choice_input)

                    if 1 <= choice <= len(matches):
                        # Player selected - drop immediately (no confirmation)
                        selected_player = matches[choice - 1]
                        status = "your roster" if selected_player.drafted == 2 else "drafted players"

                        # Drop the player (set drafted=0)
                        selected_player.drafted = 0
                        save_callback()
                        print(f"✅ Dropped {selected_player.name} from {status}!")
                        if self.logger:
                            self.logger.info(f"Player {selected_player.name} dropped (set drafted=0)")
                        continue
                    else:
                        print("Invalid choice. Please try again.")
                        continue

                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue
                except Exception as e:
                    print(f"Error dropping player: {e}")
                    if self.logger:
                        self.logger.error(f"Error dropping player: {e}")
                    continue

            except Exception as e:
                print(f"Error during search: {e}")
                print("Returning to previous menu...")
                if self.logger:
                    self.logger.error(f"Error during player search: {e}")
                return False

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