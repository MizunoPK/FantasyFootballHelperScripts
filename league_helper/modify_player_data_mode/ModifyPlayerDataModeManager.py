#!/usr/bin/env python3
"""
Modify Player Data Mode Manager

This module manages the Modify Player Data modes including:
- Mark Player as Drafted (drafted=0 → drafted=1)
- Mark Player as Rostered (drafted=0 → drafted=2)
- Drop Player (drafted≠0 → drafted=0)
- Lock Player (toggle locked 0↔1)

Author: Kai Mizuno
Last Updated: October 2025
"""

from pathlib import Path
from typing import Optional
import sys

# Add parent paths for imports
sys.path.append(str(Path(__file__).parent.parent))
from util.PlayerManager import PlayerManager
from util.player_search import PlayerSearch
from util.user_input import show_list_selection

sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.LoggingManager import get_logger
from utils.FantasyPlayer import FantasyPlayer


class ModifyPlayerDataModeManager:
    """Manages the Modify Player Data interactive mode with 4 sub-modes."""

    def __init__(self, player_manager: PlayerManager):
        """
        Initialize the Modify Player Data Mode Manager.

        Args:
            player_manager: PlayerManager instance with player data
        """
        self.player_manager = player_manager
        self.logger = get_logger()
        self.logger.info("Initializing Modify Player Data Mode Manager")

    def set_managers(self, player_manager: PlayerManager):
        """
        Update the player_manager reference.

        This ensures the manager has the latest player data when starting interactive mode.

        Args:
            player_manager: Updated PlayerManager instance
        """
        self.player_manager = player_manager

    def start_interactive_mode(self, player_manager: PlayerManager):
        """
        Start the interactive Modify Player Data mode with 4-option menu.

        Args:
            player_manager: Updated PlayerManager instance
        """
        # Update manager reference
        self.set_managers(player_manager)
        self.logger.info("Entering Modify Player Data interactive mode")

        # Main menu loop
        while True:
            try:
                choice = show_list_selection(
                    "MODIFY PLAYER DATA",
                    [
                        "Mark Player as Drafted",
                        "Mark Player as Rostered",
                        "Drop Player",
                        "Lock Player"
                    ],
                    "Return to Main Menu"
                )

                if choice == 1:
                    self.logger.info("User selected: Mark Player as Drafted")
                    self._mark_player_as_drafted()
                elif choice == 2:
                    self.logger.info("User selected: Mark Player as Rostered")
                    self._mark_player_as_rostered()
                elif choice == 3:
                    self.logger.info("User selected: Drop Player")
                    self._drop_player()
                elif choice == 4:
                    self.logger.info("User selected: Lock Player")
                    self._lock_player()
                elif choice == 5:
                    print("Returning to Main Menu...")
                    self.logger.info("User exited Modify Player Data mode")
                    break
                else:
                    print("Invalid choice. Please try again.")

            except KeyboardInterrupt:
                print("\nReturning to Main Menu...")
                self.logger.info("User interrupted Modify Player Data mode")
                break
            except Exception as e:
                print(f"Error in Modify Player Data mode: {e}")
                self.logger.error(f"Error in Modify Player Data mode: {e}")
                break

    def _mark_player_as_drafted(self):
        """
        Mark a player as drafted by another team (drafted=0 → drafted=1).

        Searches only available players (drafted=0).
        """
        self.logger.info("Starting Mark Player as Drafted mode")

        # Create searcher instance
        searcher = PlayerSearch(self.player_manager.players)

        # Interactive search for available players
        selected_player = searcher.interactive_search(
            drafted_filter=0,
            prompt="Enter player name to mark as drafted (or press Enter to return): "
        )

        # If user exited, return to menu
        if selected_player is None:
            self.logger.info("User exited Mark Player as Drafted mode")
            return

        # Mark player as drafted by another team
        selected_player.drafted = 1

        # Save changes to file
        self.player_manager.update_players_file()

        # Notify user
        print(f"✓ Marked {selected_player.name} as drafted by another team!")
        self.logger.info(f"Player {selected_player.name} marked as drafted=1")

    def _mark_player_as_rostered(self):
        """
        Mark a player as rostered on your team (drafted=0 → drafted=2).

        Searches only available players (drafted=0).
        """
        self.logger.info("Starting Mark Player as Rostered mode")

        # Create searcher instance
        searcher = PlayerSearch(self.player_manager.players)

        # Interactive search for available players
        selected_player = searcher.interactive_search(
            drafted_filter=0,
            prompt="Enter player name to add to your roster (or press Enter to return): "
        )

        # If user exited, return to menu
        if selected_player is None:
            self.logger.info("User exited Mark Player as Rostered mode")
            return

        # Mark player as on your roster
        selected_player.drafted = 2

        # Save changes to file
        self.player_manager.update_players_file()

        # Notify user
        print(f"✓ Added {selected_player.name} to your roster!")
        self.logger.info(f"Player {selected_player.name} marked as drafted=2 (rostered)")

    def _drop_player(self):
        """
        Drop a player from drafted or rostered status (drafted≠0 → drafted=0).

        Searches only players with drafted != 0 (both drafted=1 and drafted=2).
        """
        self.logger.info("Starting Drop Player mode")

        # Create searcher instance
        searcher = PlayerSearch(self.player_manager.players)

        # Interactive search for non-available players (drafted != 0)
        selected_player = searcher.interactive_search(
            drafted_filter=None,
            prompt="Enter player name to drop (or press Enter to return): ",
            not_available=True
        )

        # If user exited, return to menu
        if selected_player is None:
            self.logger.info("User exited Drop Player mode")
            return

        # Store old status for message
        old_status = "your roster" if selected_player.drafted == 2 else "drafted players"

        # Drop the player (set to available)
        selected_player.drafted = 0

        # Save changes to file
        self.player_manager.update_players_file()

        # Notify user
        print(f"✓ Dropped {selected_player.name} from {old_status}!")
        self.logger.info(f"Player {selected_player.name} dropped (set drafted=0)")

    def _lock_player(self):
        """
        Toggle a player's locked status (locked 0↔1).

        Searches all players regardless of drafted status.
        The [LOCKED] indicator automatically appears via FantasyPlayer.__str__().
        """
        self.logger.info("Starting Lock Player mode")

        # Create searcher instance
        searcher = PlayerSearch(self.player_manager.players)

        # Interactive search for all players
        selected_player = searcher.interactive_search(
            drafted_filter=None,
            prompt="Enter player name to lock/unlock (or press Enter to return): "
        )

        # If user exited, return to menu
        if selected_player is None:
            self.logger.info("User exited Lock Player mode")
            return

        # Store old locked state
        was_locked = selected_player.locked == 1

        # Toggle locked state
        selected_player.locked = 0 if was_locked else 1

        # Save changes to file
        self.player_manager.update_players_file()

        # Notify user with appropriate message
        if selected_player.locked == 1:
            print(f"🔒 Locked {selected_player.name}!")
        else:
            print(f"🔓 Unlocked {selected_player.name}!")

        self.logger.info(f"Player {selected_player.name} lock toggled (locked={selected_player.locked})")
