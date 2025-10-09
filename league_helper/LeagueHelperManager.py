#!/usr/bin/env python3
"""
League Helper Manager

Main entry point for the League Helper application.

Author: Kai Mizuno
"""

from pathlib import Path
import constants as Constants
from util.ConfigManager import ConfigManager
from util.PlayerManager import PlayerManager
from util.TeamDataManager import TeamDataManager
from add_to_roster_mode.AddToRosterModeManager import AddToRosterModeManager
from drop_player_mode.DropPlayerModeManager import DropPlayerModeManager
from lock_player_mode.LockPlayerModeManager import LockPlayerModeManager
from mark_drafted_player_mode.MarkDraftedPlayerModeManager import MarkDraftedPlayerModeManager
from starter_helper_mode.StarterHelperModeManager import StarterHelperModeManager
from trade_simulator_mode.TradeSimulatorModeManager import TradeSimulatorModeManager
from waiver_optimizer_mode.WaiverOptimizerModeManager import WaiverOptimizerModeManager

import constants

import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.LoggingManager import setup_logger, get_logger


class LeagueHelperManager:

    def __init__(self, data_folder: Path):
        self.logger = get_logger()

        # Create single config manager that handles all configuration
        self.config = ConfigManager(data_folder)

        self.team_data_manager = TeamDataManager(data_folder)
        self.player_manager = PlayerManager(data_folder, self.config, self.team_data_manager)

        # Pass config manager to mode managers
        self.add_to_roster_mode_manager = AddToRosterModeManager(self.config, self.player_manager, self.team_data_manager)
        self.drop_player_mode_manager = DropPlayerModeManager()
        self.lock_player_mode_manager = LockPlayerModeManager()
        self.mark_drafted_player_mode_manager = MarkDraftedPlayerModeManager()
        self.starter_helper_mode_manager = StarterHelperModeManager(self.config)
        self.trade_simulator_mode_manager = TradeSimulatorModeManager()
        self.waiver_optimizer_mode_manager = WaiverOptimizerModeManager(self.config)


    def start_interactive_mode(self):
        """Run the interactive draft helper with main menu"""
        print("Welcome to the Start 7 Fantasy League Helper!")
        print(f"Currently drafted players: {self.player_manager.get_roster_len()} / {Constants.MAX_PLAYERS} max")

        # Show initial roster status
        self.player_manager.display_roster_by_draft_order()

        self.logger.info(f"Interactive league helper started. Current roster size: {self.player_manager.get_roster_len()}")

        while True:
            # Reload player data from CSV before showing menu to ensure latest changes
            self.player_manager.reload_player_data()

            choice = self.show_main_menu()
            if choice == 1:
                self.run_add_to_roster_mode()
            elif choice == 2:
                self.run_mark_drafted_player_mode()
            elif choice == 3:
                self.run_trade_analysis_mode()
            elif choice == 4:
                self.run_drop_player_mode()
            elif choice == 5:
                self.run_lock_unlock_player_mode()
            elif choice == 6:
                self.run_starter_helper_mode()
            elif choice == 7:
                self.run_trade_simulator_mode()
            elif choice == 8:
                print("Goodbye!")
                self.logger.info("User exited interactive draft")
                break
            else:
                print("Invalid choice. Please try again.")


    def show_main_menu(self):
        """Display main menu and get user choice"""
        print("\n" + "="*50)
        print("MAIN MENU")
        print("="*50)
        print(f"Current roster: {self.player_manager.get_roster_len()} / {Constants.MAX_PLAYERS} players")
        print("="*50)
        print("1. Add to Roster")
        print("2. Mark Drafted Player")
        print("3. Waiver Optimizer")
        print("4. Drop Player")
        print("5. Lock/Unlock Player")
        print("6. Starter Helper")
        print("7. Trade Simulator")
        print("8. Quit")
        max_choice = 8
        print("="*50)

        try:
            choice = int(input(f"Enter your choice (1-{max_choice}): ").strip())
            return choice
        except ValueError:
            return -1
        

    def run_add_to_roster_mode(self):
        self.add_to_roster_mode_manager.start_interactive_mode(self.player_manager, self.team_data_manager)



def main():
    setup_logger(constants.LOG_NAME, constants.LOGGING_LEVEL, constants.LOGGING_TO_FILE, constants.LOGGING_FILE, constants.LOGGING_FORMAT)

    base_path = Path(__file__).parent.parent
    data_path = base_path / "data"

    leagueHelper = LeagueHelperManager(data_path)
    leagueHelper.start_interactive_mode()


if __name__ == "__main__":
    main()
