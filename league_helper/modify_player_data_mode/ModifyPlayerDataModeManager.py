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

from league_helper.util.PlayerManager import PlayerManager
from league_helper.util.player_search import PlayerSearch
from league_helper.util.user_input import show_list_selection
import league_helper.constants as Constants
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
    - PlayerSearch: For interactive player selection

    Player drafted_by field values:
    - "": Available (free agent, can be picked up from waivers)
    - "Team Name": Drafted by opponent team (can be traded for)
    - FANTASY_TEAM_NAME: On user's roster (can be traded away)

    Player locked status values:
    - False: Unlocked (can be included in trades)
    - True: Locked (excluded from trades, but counts toward position limits)
    """

    def __init__(self, player_manager: PlayerManager, data_folder: Path = None):
        """
        Initialize the Modify Player Data Mode Manager.

        Sets up the manager with references to PlayerManager.
        Initializes logging and prepares the manager for interactive mode.

        Args:
            player_manager (PlayerManager): PlayerManager instance with all player data
            data_folder (Path, optional): Path to data directory (unused, kept for compatibility)
        """
        self.player_manager = player_manager
        self.logger = get_logger()

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
        self.set_managers(player_manager)
        self.logger.info("Entering Modify Player Data interactive mode")

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
        Mark a free agent player as drafted by a team (drafted_by="" → drafted_by=team_name).

        Interactive workflow:
        1. Search for an available player (free agents only)
        2. Select the team that drafted the player
        3. Set player's drafted_by field to team name
        4. Save changes to player JSON files

        The drafted_by field is used by Trade Simulator:
        - "": Available for waiver wire pickups
        - "Team Name": Drafted by opponent (can be traded for)
        - FANTASY_TEAM_NAME: On user's roster (can be traded away)
        """
        self.logger.info("Starting Mark Player as Drafted mode")

        searcher = PlayerSearch(self.player_manager.players)
        selected_player = searcher.interactive_search(
            drafted_filter=0,
            prompt="Enter player name to mark as drafted (or press Enter to return): ",
            max_search_results=self.player_manager.config.max_search_results
        )

        if selected_player is None:
            self.logger.info("User exited Mark Player as Drafted mode")
            return

        team_names = set()
        for player in self.player_manager.players:
            if player.drafted_by and player.drafted_by != "":
                team_names.add(player.drafted_by)

        team_names.add(Constants.FANTASY_TEAM_NAME)
        team_names = sorted(list(team_names))

        if not team_names:
            print("Error: No teams found")
            self.logger.error("No teams found in player data")
            return

        print(f"\nSelect the team that drafted {selected_player.name}:")
        team_choice = show_list_selection(
            "TEAM SELECTION",
            team_names,
            "Cancel"
        )

        if team_choice == len(team_names) + 1:
            print("Cancelled.")
            self.logger.info("User cancelled team selection")
            return

        selected_team = team_names[team_choice - 1]

        if selected_team == Constants.FANTASY_TEAM_NAME:
            selected_player.drafted_by = Constants.FANTASY_TEAM_NAME
            print(f"✓ Added {selected_player.name} to your roster ({selected_team})!")
            self.logger.info(f"Player {selected_player.name} marked as drafted_by='{Constants.FANTASY_TEAM_NAME}' (user's team)")
        else:
            selected_player.drafted_by = selected_team
            print(f"✓ Marked {selected_player.name} as drafted by {selected_team}!")
            self.logger.info(f"Player {selected_player.name} marked as drafted_by='{selected_team}'")

        self.player_manager.update_players_file()

    def _drop_player(self):
        """
        Drop a player from drafted or rostered status (drafted_by → "").

        Interactive workflow:
        1. Search for a drafted/rostered player
        2. Determine current status for user feedback
        3. Clear player's drafted_by field (set to "")
        4. Save changes to player JSON files

        This operation reverses the "Mark as Drafted" action, returning the player
        to the available pool for future drafting or waiver wire pickups.
        """
        self.logger.info("Starting Drop Player mode")

        searcher = PlayerSearch(self.player_manager.players)
        selected_player = searcher.interactive_search(
            drafted_filter=None,
            prompt="Enter player name to drop (or press Enter to return): ",
            not_available=True,
            max_search_results=self.player_manager.config.max_search_results
        )

        if selected_player is None:
            self.logger.info("User exited Drop Player mode")
            return

        old_status = "your roster" if selected_player.is_rostered() else "drafted players"

        selected_player.drafted_by = ""

        self.player_manager.update_players_file()

        print(f"✓ Dropped {selected_player.name} from {old_status}!")
        self.logger.info(f"Player {selected_player.name} dropped (set drafted_by='')")

    def _lock_player(self):
        """
        Toggle a player's locked status (locked 0↔1).

        Interactive workflow:
        1. Display all currently locked players
        2. Search for any player (available, drafted, or rostered)
        3. Determine current locked state (locked=0 or locked=1)
        4. Toggle the locked status:
           - If locked (1) → unlock (0)
           - If unlocked (0) → lock (1)
        5. Save changes to players.csv
        6. Display visual feedback (🔒 locked / 🔓 unlocked)

        Locked players have special behavior in Trade Simulator:
        - Excluded from trade combinations (cannot be traded)
        - Still included in roster validation (count toward position limits)
        - Display [LOCKED] indicator via FantasyPlayer.__str__()

        This allows users to protect key players from being suggested in trades.
        """
        self.logger.info("Starting Lock Player mode")

        locked_players = [p for p in self.player_manager.players if p.is_locked()]

        if locked_players:
            print("\n" + "=" * 80)
            print("🔒 CURRENTLY LOCKED PLAYERS")
            print("=" * 80)

            locked_players.sort(key=lambda p: (p.position, p.name))

            current_position = None
            for player in locked_players:
                if player.position != current_position:
                    current_position = player.position
                    print(f"\n{current_position}:")

                drafted_status = ""
                if player.is_rostered():
                    drafted_status = " [YOUR ROSTER]"
                elif player.is_drafted_by_opponent():
                    drafted_status = " [DRAFTED]"

                print(f"  • {player.name} ({player.team}){drafted_status}")

            print("\n" + "=" * 80)
            print(f"Total locked players: {len(locked_players)}")
            print("=" * 80 + "\n")
        else:
            print("\n" + "=" * 80)
            print("🔓 NO LOCKED PLAYERS")
            print("=" * 80)
            print("No players are currently locked.")
            print("=" * 80 + "\n")

        self.logger.info(f"Displayed {len(locked_players)} locked players")

        searcher = PlayerSearch(self.player_manager.players)
        selected_player = searcher.interactive_search(
            drafted_filter=None,
            prompt="Enter player name to lock/unlock (or press Enter to return): ",
            max_search_results=self.player_manager.config.max_search_results
        )

        if selected_player is None:
            self.logger.info("User exited Lock Player mode")
            return

        was_locked = selected_player.is_locked()

        selected_player.locked = False if was_locked else True

        self.player_manager.update_players_file()

        if selected_player.is_locked():
            print(f"🔒 Locked {selected_player.name}!")
        else:
            print(f"🔓 Unlocked {selected_player.name}!")

        self.logger.info(f"Player {selected_player.name} lock toggled (locked={selected_player.locked})")


