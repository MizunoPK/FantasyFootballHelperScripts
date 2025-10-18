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
    """
    Manages the Modify Player Data interactive mode with 4 sub-modes.

    This manager provides a menu-driven interface for modifying player data:
    - Mark Player as Drafted: Move available players to drafted/rostered status
    - Drop Player: Return drafted/rostered players to available status
    - Lock Player: Toggle player's locked status (prevents trading in Trade Simulator)

    The manager integrates with:
    - PlayerManager: For player data access and persistence
    - DraftedDataWriter: For tracking team rosters in drafted_data.csv
    - PlayerSearch: For interactive player selection

    Player drafted status values:
    - 0: Available (can be picked up from waivers)
    - 1: Drafted by opponent (can be traded for)
    - 2: On user's roster (can be traded away)

    Player locked status values:
    - 0: Unlocked (can be included in trades)
    - 1: Locked (excluded from trades, but counts toward position limits)
    """

    def __init__(self, player_manager: PlayerManager, data_folder: Path = None):
        """
        Initialize the Modify Player Data Mode Manager.

        Sets up the manager with references to PlayerManager and DraftedDataWriter.
        Initializes logging and prepares the manager for interactive mode.

        Args:
            player_manager (PlayerManager): PlayerManager instance with all player data
            data_folder (Path, optional): Path to data directory. Defaults to ../data relative to this file.
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
        Update the player_manager reference with latest player data.

        This method ensures the manager has the most recent player data when starting
        interactive mode. Called at the beginning of start_interactive_mode() to sync
        with any changes made in other modes.

        Args:
            player_manager (PlayerManager): Updated PlayerManager instance with current player data
        """
        self.player_manager = player_manager

    def start_interactive_mode(self, player_manager: PlayerManager):
        """
        Start the interactive Modify Player Data mode with 4-option menu.

        Displays a menu-driven interface allowing the user to:
        1. Mark Player as Drafted - Move available players to drafted/rostered status
        2. Drop Player - Return drafted/rostered players to available status
        3. Lock Player - Toggle player's locked status (prevents trading)
        4. Return to Main Menu - Exit the mode

        The mode runs in a loop until the user exits or an exception occurs.
        Handles KeyboardInterrupt (Ctrl+C) and general exceptions gracefully.

        Args:
            player_manager (PlayerManager): Updated PlayerManager instance with current player data
        """
        # STEP 1: Update manager reference to ensure we have latest player data
        # This is crucial as players may have been modified in other modes
        self.set_managers(player_manager)
        self.logger.info("Entering Modify Player Data interactive mode")

        # STEP 2: Main menu loop - continues until user exits or exception occurs
        while True:
            try:
                # STEP 3: Display menu and get user's mode selection
                # Options: Mark as Drafted, Drop Player, Lock Player, or Exit
                choice = show_list_selection(
                    "MODIFY PLAYER DATA",
                    [
                        "Mark Player as Drafted",  # Option 1
                        "Drop Player",              # Option 2
                        "Lock Player"               # Option 3
                    ],
                    "Return to Main Menu"           # Option 4 (exit)
                )

                # STEP 4: Route to appropriate sub-mode based on user selection
                if choice == 1:
                    # User wants to mark a player as drafted by a team
                    self.logger.info("User selected: Mark Player as Drafted")
                    self._mark_player_as_drafted()
                elif choice == 2:
                    # User wants to drop a player back to available status
                    self.logger.info("User selected: Drop Player")
                    self._drop_player()
                elif choice == 3:
                    # User wants to toggle a player's locked status
                    self.logger.info("User selected: Lock Player")
                    self._lock_player()
                elif choice == 4:
                    # User selected Return to Main Menu - exit the loop
                    print("Returning to Main Menu...")
                    self.logger.info("User exited Modify Player Data mode")
                    break
                else:
                    # Invalid choice (shouldn't happen with show_list_selection, but handle anyway)
                    print("Invalid choice. Please try again.")

            except KeyboardInterrupt:
                # User pressed Ctrl+C - exit gracefully
                print("\nReturning to Main Menu...")
                self.logger.info("User interrupted Modify Player Data mode")
                break
            except Exception as e:
                # Unexpected error occurred - log and exit to prevent crash
                print(f"Error in Modify Player Data mode: {e}")
                self.logger.error(f"Error in Modify Player Data mode: {e}")
                break

    def _mark_player_as_drafted(self):
        """
        Mark a player as drafted by a team (drafted=0 → drafted=1 or drafted=2).

        Interactive workflow:
        1. Search for an available player (drafted=0 only)
        2. Select the team that drafted the player
        3. Determine drafted status based on team ownership:
           - User's team (FANTASY_TEAM_NAME) → drafted=2 (rostered)
           - Another team → drafted=1 (drafted by opponent)
        4. Add player to drafted_data.csv for Trade Simulator tracking
        5. Save changes to players.csv

        The drafted status distinction is critical for Trade Simulator:
        - drafted=0: Available for waiver wire pickups
        - drafted=1: Drafted by opponent (can be traded for)
        - drafted=2: On user's roster (can be traded away)
        """
        self.logger.info("Starting Mark Player as Drafted mode")

        # STEP 1: Search for an available player to mark as drafted
        # Only show players with drafted=0 (available/undrafted)
        # This prevents accidentally marking already-drafted players
        searcher = PlayerSearch(self.player_manager.players)
        selected_player = searcher.interactive_search(
            drafted_filter=0,  # Filter to available players only
            prompt="Enter player name to mark as drafted (or press Enter to return): "
        )

        # STEP 2: Handle user exit (pressed Enter without selecting)
        # Return to main menu if no player was selected
        if selected_player is None:
            self.logger.info("User exited Mark Player as Drafted mode")
            return

        # STEP 3: Load all team names from drafted_data.csv
        # This CSV tracks which team has drafted which players
        # Team names are used to determine drafted status (user's team = 2, other team = 1)
        team_names = self.drafted_data_writer.get_all_team_names()

        # STEP 4: Validate that teams exist in the CSV
        # If no teams found, the CSV may be corrupted or missing
        if not team_names:
            print("Error: No teams found in drafted_data.csv")
            self.logger.error("No teams found in drafted_data.csv")
            return

        # STEP 5: Display team selection menu
        # User selects which team drafted this player
        # This determines the drafted status value (1 or 2)
        print(f"\nSelect the team that drafted {selected_player.name}:")
        team_choice = show_list_selection(
            "TEAM SELECTION",
            team_names,
            "Cancel"  # Option to cancel the operation
        )

        # STEP 6: Handle cancellation
        # If user selects "Cancel" option (last option), abort the operation
        if team_choice == len(team_names) + 1:
            print("Cancelled.")
            self.logger.info("User cancelled team selection")
            return

        # STEP 7: Get the selected team name
        # Convert 1-based menu choice to 0-based list index
        selected_team = team_names[team_choice - 1]

        # STEP 8: Determine drafted status based on team ownership
        # drafted=2: Player is on user's roster (FANTASY_TEAM_NAME from constants)
        # drafted=1: Player is drafted by another team (not on user's roster)
        # This distinction allows Trade Simulator to differentiate user's players from others
        if selected_team == Constants.FANTASY_TEAM_NAME:
            # User's team - mark as rostered (drafted=2)
            selected_player.drafted = 2
            print(f"✓ Added {selected_player.name} to your roster ({selected_team})!")
            self.logger.info(f"Player {selected_player.name} marked as drafted=2 (user's team)")
        else:
            # Another team - mark as drafted by opponent (drafted=1)
            selected_player.drafted = 1
            print(f"✓ Marked {selected_player.name} as drafted by {selected_team}!")
            self.logger.info(f"Player {selected_player.name} marked as drafted=1 (team: {selected_team})")

        # STEP 9: Add player to drafted_data.csv
        # This CSV is used by Trade Simulator and other modes to track team rosters
        # Failure is non-critical (player is still marked as drafted in players.csv)
        if self.drafted_data_writer.add_player(selected_player, selected_team):
            self.logger.info(f"Added {selected_player.name} to drafted_data.csv for team {selected_team}")
        else:
            print(f"Warning: Failed to add {selected_player.name} to drafted_data.csv")

        # STEP 10: Persist changes to players.csv
        # This saves the updated drafted status to disk
        self.player_manager.update_players_file()

    def _drop_player(self):
        """
        Drop a player from drafted or rostered status (drafted≠0 → drafted=0).

        Interactive workflow:
        1. Search for a drafted/rostered player (drafted=1 or drafted=2 only)
        2. Determine current status for user feedback:
           - drafted=2 → "your roster"
           - drafted=1 → "drafted players"
        3. Remove player from drafted_data.csv
        4. Mark player as available (drafted=0)
        5. Save changes to players.csv

        This operation reverses the "Mark as Drafted" action, returning the player
        to the available pool for future drafting or waiver wire pickups.
        """
        self.logger.info("Starting Drop Player mode")

        # STEP 1: Search for a drafted/rostered player to drop
        # Only show players with drafted != 0 (excludes available players)
        # not_available=True filters to drafted=1 (other teams) or drafted=2 (user's roster)
        searcher = PlayerSearch(self.player_manager.players)
        selected_player = searcher.interactive_search(
            drafted_filter=None,  # Don't filter by specific drafted value
            prompt="Enter player name to drop (or press Enter to return): ",
            not_available=True  # Only show drafted/rostered players (drafted != 0)
        )

        # STEP 2: Handle user exit (pressed Enter without selecting)
        # Return to main menu if no player was selected
        if selected_player is None:
            self.logger.info("User exited Drop Player mode")
            return

        # STEP 3: Determine the player's current status for user feedback
        # drafted=2: Player is on user's roster ("your roster")
        # drafted=1: Player is drafted by another team ("drafted players")
        # This provides clear feedback about what the user is dropping
        old_status = "your roster" if selected_player.drafted == 2 else "drafted players"

        # STEP 4: Remove player from drafted_data.csv
        # This CSV tracks team rosters for Trade Simulator and other modes
        # Failure is non-critical (player will still be dropped in players.csv)
        if self.drafted_data_writer.remove_player(selected_player):
            self.logger.info(f"Removed {selected_player.name} from drafted_data.csv")
        else:
            print(f"Warning: Failed to remove {selected_player.name} from drafted_data.csv")

        # STEP 5: Mark player as available (drafted=0)
        # This makes the player available for drafting again
        # Works for both drafted=1 (other teams) and drafted=2 (user's roster)
        selected_player.drafted = 0

        # STEP 6: Persist changes to players.csv
        # This saves the updated drafted status to disk
        self.player_manager.update_players_file()

        # STEP 7: Notify user of successful drop
        # Use the old_status to provide context (e.g., "from your roster")
        print(f"✓ Dropped {selected_player.name} from {old_status}!")
        self.logger.info(f"Player {selected_player.name} dropped (set drafted=0)")

    def _lock_player(self):
        """
        Toggle a player's locked status (locked 0↔1).

        Interactive workflow:
        1. Search for any player (available, drafted, or rostered)
        2. Determine current locked state (locked=0 or locked=1)
        3. Toggle the locked status:
           - If locked (1) → unlock (0)
           - If unlocked (0) → lock (1)
        4. Save changes to players.csv
        5. Display visual feedback (🔒 locked / 🔓 unlocked)

        Locked players have special behavior in Trade Simulator:
        - Excluded from trade combinations (cannot be traded)
        - Still included in roster validation (count toward position limits)
        - Display [LOCKED] indicator via FantasyPlayer.__str__()

        This allows users to protect key players from being suggested in trades.
        """
        self.logger.info("Starting Lock Player mode")

        # STEP 1: Search for any player to lock/unlock
        # Search all players regardless of drafted status (drafted=0, 1, or 2)
        # Locked players cannot be traded in Trade Simulator, but are included in roster validation
        searcher = PlayerSearch(self.player_manager.players)
        selected_player = searcher.interactive_search(
            drafted_filter=None,  # Search all players (available, drafted, and rostered)
            prompt="Enter player name to lock/unlock (or press Enter to return): "
        )

        # STEP 2: Handle user exit (pressed Enter without selecting)
        # Return to main menu if no player was selected
        if selected_player is None:
            self.logger.info("User exited Lock Player mode")
            return

        # STEP 3: Determine current locked state for toggle operation
        # locked=1: Player is locked (cannot be traded)
        # locked=0: Player is unlocked (can be traded)
        was_locked = selected_player.locked == 1

        # STEP 4: Toggle the locked status
        # If locked (1) → unlock (0)
        # If unlocked (0) → lock (1)
        # Locked players are excluded from Trade Simulator combinations
        # but still count toward position limits in roster validation
        selected_player.locked = 0 if was_locked else 1

        # STEP 5: Persist changes to players.csv
        # This saves the updated locked status to disk
        self.player_manager.update_players_file()

        # STEP 6: Notify user with visual feedback
        # Use lock/unlock emojis to clearly indicate the new state
        if selected_player.locked == 1:
            print(f"🔒 Locked {selected_player.name}!")
        else:
            print(f"🔓 Unlocked {selected_player.name}!")

        self.logger.info(f"Player {selected_player.name} lock toggled (locked={selected_player.locked})")
