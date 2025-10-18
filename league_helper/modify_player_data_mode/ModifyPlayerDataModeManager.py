#!/usr/bin/env python3
"""
Modify Player Data Mode Manager

This module manages the Modify Player Data modes including:
- Mark Player as Drafted (drafted=0 → drafted=1)
- Mark Player as Rostered (drafted=0 → drafted=2)
- Drop Player (drafted≠0 → drafted=0)
- Lock Player (toggle locked 0↔1)

Author: Kai Mizuno
"""

from pathlib import Path
from typing import Optional
import sys

# Add parent paths for imports
sys.path.append(str(Path(__file__).parent.parent))
from util.PlayerManager import PlayerManager
from util.player_search import PlayerSearch
from util.user_input import show_list_selection
from util.DraftedDataWriter import DraftedDataWriter
import constants as Constants

sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.LoggingManager import get_logger
from utils.FantasyPlayer import FantasyPlayer


class ModifyPlayerDataModeManager:
    """Manages the Modify Player Data interactive mode with 4 sub-modes."""

    def __init__(self, player_manager: PlayerManager, data_folder: Path = None):
        """
        Initialize the Modify Player Data Mode Manager.

        Args:
            player_manager: PlayerManager instance with player data
            data_folder: Path to data directory (optional, defaults to ../data relative to this file)
        """
        self.player_manager = player_manager
        self.logger = get_logger()

        # Initialize drafted data writer
        if data_folder is None:
            data_folder = Path(__file__).parent.parent.parent / "data"
        self.drafted_data_writer = DraftedDataWriter(data_folder / "drafted_data.csv")

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
                        "Drop Player",
                        "Lock Player"
                    ],
                    "Return to Main Menu"
                )

                if choice == 1:
                    self.logger.info("User selected: Mark Player as Drafted")
                    self._mark_player_as_drafted()
                elif choice == 2:
                    self.logger.info("User selected: Drop Player")
                    self._drop_player()
                elif choice == 3:
                    self.logger.info("User selected: Lock Player")
                    self._lock_player()
                elif choice == 4:
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
        Mark a player as drafted by a team (drafted=0 → drafted=1 or drafted=2).

        Searches only available players (drafted=0).
        After selecting a player, prompts for team selection.
        If team matches user's team (from constants), marks as drafted=2.
        Otherwise marks as drafted=1 and adds to drafted_data.csv.
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

        # Get all team names from drafted_data.csv
        team_names = self.drafted_data_writer.get_all_team_names()

        if not team_names:
            print("Error: No teams found in drafted_data.csv")
            self.logger.error("No teams found in drafted_data.csv")
            return

        # Show team selection menu
        print(f"\nSelect the team that drafted {selected_player.name}:")
        team_choice = show_list_selection(
            "TEAM SELECTION",
            team_names,
            "Cancel"
        )

        # Check if user cancelled
        if team_choice == len(team_names) + 1:
            print("Cancelled.")
            self.logger.info("User cancelled team selection")
            return

        # Get selected team name
        selected_team = team_names[team_choice - 1]

        # Check if it's the user's team
        if selected_team == Constants.FANTASY_TEAM_NAME:
            # Mark as drafted=2 (on user's roster)
            selected_player.drafted = 2
            print(f"✓ Added {selected_player.name} to your roster ({selected_team})!")
            self.logger.info(f"Player {selected_player.name} marked as drafted=2 (user's team)")
        else:
            # Mark as drafted=1 (drafted by another team)
            selected_player.drafted = 1
            print(f"✓ Marked {selected_player.name} as drafted by {selected_team}!")
            self.logger.info(f"Player {selected_player.name} marked as drafted=1 (team: {selected_team})")

        # Add to drafted_data.csv
        if self.drafted_data_writer.add_player(selected_player, selected_team):
            self.logger.info(f"Added {selected_player.name} to drafted_data.csv for team {selected_team}")
        else:
            print(f"Warning: Failed to add {selected_player.name} to drafted_data.csv")

        # Save changes to players.csv
        self.player_manager.update_players_file()

    def _drop_player(self):
        """
        Drop a player from drafted or rostered status (drafted≠0 → drafted=0).

        Searches only players with drafted != 0 (both drafted=1 and drafted=2).
        Also removes the player from drafted_data.csv.
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

        # Remove from drafted_data.csv
        if self.drafted_data_writer.remove_player(selected_player):
            self.logger.info(f"Removed {selected_player.name} from drafted_data.csv")
        else:
            print(f"Warning: Failed to remove {selected_player.name} from drafted_data.csv")

        # Drop the player (set to available)
        selected_player.drafted = 0

        # Save changes to players.csv
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
