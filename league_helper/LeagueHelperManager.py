#!/usr/bin/env python3
"""
League Helper Manager

Main orchestrator for the Fantasy Football League Helper application.
Manages the interactive menu system and coordinates between all mode managers,
providing a unified interface for draft assistance, roster optimization, and
weekly lineup recommendations.

This module serves as the central hub that:
- Initializes all managers (Config, Player, TeamData, and Mode Managers)
- Displays the main menu and routes user choices to appropriate modes
- Reloads player data before each menu display to ensure fresh data
- Coordinates data flow between different modes

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
    """
    Central orchestrator for the Fantasy Football League Helper application.

    This class manages the main interactive menu system and coordinates between
    all mode managers. It handles initialization of core managers (Config, Player,
    TeamData) and delegates mode-specific operations to specialized mode managers.

    Attributes:
        logger: Logger instance for tracking application events
        config (ConfigManager): Manages league configuration from JSON
        team_data_manager (TeamDataManager): Handles team rankings and matchups
        player_manager (PlayerManager): Manages player data, scoring, and roster
        add_to_roster_mode_manager (AddToRosterModeManager): Draft mode handler
        drop_player_mode_manager (DropPlayerModeManager): Drop player handler
        lock_player_mode_manager (LockPlayerModeManager): Lock/unlock handler
        mark_drafted_player_mode_manager (MarkDraftedPlayerModeManager): Mark drafted handler
        starter_helper_mode_manager (StarterHelperModeManager): Weekly lineup handler
        trade_simulator_mode_manager (TradeSimulatorModeManager): Trade simulation handler
        waiver_optimizer_mode_manager (WaiverOptimizerModeManager): Waiver optimization handler
    """

    def __init__(self, data_folder: Path):
        """
        Initialize the League Helper Manager and all sub-managers.

        Args:
            data_folder (Path): Path to the data directory containing:
                - league_config.json: League configuration
                - players.csv: Player database
                - teams.csv: Team rankings
                - bye_weeks.csv: Bye week schedule

        Raises:
            FileNotFoundError: If required data files are missing
            ValueError: If configuration is invalid
        """
        self.logger = get_logger()
        self.logger.info("Initializing League Helper Manager")

        # Create single config manager that handles all configuration
        self.logger.debug(f"Loading configuration from {data_folder}")
        self.config = ConfigManager(data_folder)
        self.logger.info(f"Configuration loaded: {self.config.config_name} (Week {self.config.current_nfl_week})")

        # Initialize core data managers
        self.logger.debug("Initializing Team Data Manager")
        self.team_data_manager = TeamDataManager(data_folder)

        self.logger.debug("Initializing Player Manager")
        self.player_manager = PlayerManager(data_folder, self.config, self.team_data_manager)
        self.logger.info(f"Player data loaded: {len(self.player_manager.players)} total players")

        # Initialize all mode managers with necessary dependencies
        self.logger.debug("Initializing mode managers")
        self.add_to_roster_mode_manager = AddToRosterModeManager(self.config, self.player_manager, self.team_data_manager)
        self.drop_player_mode_manager = DropPlayerModeManager()
        self.lock_player_mode_manager = LockPlayerModeManager()
        self.mark_drafted_player_mode_manager = MarkDraftedPlayerModeManager()
        self.starter_helper_mode_manager = StarterHelperModeManager(self.config, self.player_manager, self.team_data_manager)
        self.trade_simulator_mode_manager = TradeSimulatorModeManager()
        self.waiver_optimizer_mode_manager = WaiverOptimizerModeManager(self.config)
        self.logger.info("All mode managers initialized successfully")


    def start_interactive_mode(self):
        """
        Start the main interactive menu loop.

        Displays a welcome message and roster status, then enters an infinite loop
        showing the main menu. Player data is reloaded before each menu display to
        ensure the latest changes (from external updates or other modes) are reflected.

        The loop continues until the user selects the Quit option.
        """
        print("Welcome to the Start 7 Fantasy League Helper!")
        print(f"Currently drafted players: {self.player_manager.get_roster_len()} / {Constants.MAX_PLAYERS} max")

        # Show initial roster status
        self.player_manager.display_roster_by_draft_order()

        roster_size = self.player_manager.get_roster_len()
        self.logger.info(f"Interactive league helper started. Current roster size: {roster_size}/{Constants.MAX_PLAYERS}")

        while True:
            # Reload player data from CSV before showing menu to ensure latest changes
            self.logger.debug("Reloading player data before menu display")
            self.player_manager.reload_player_data()

            choice = self.show_main_menu()
            self.logger.debug(f"User selected menu option: {choice}")

            if choice == 1:
                self.logger.info("Starting Add to Roster mode")
                self._run_add_to_roster_mode()
            elif choice == 2:
                self.logger.info("Starting Mark Drafted Player mode")
                self.run_mark_drafted_player_mode()
            elif choice == 3:
                self.logger.info("Starting Waiver Optimizer mode")
                self.run_trade_analysis_mode()
            elif choice == 4:
                self.logger.info("Starting Drop Player mode")
                self.run_drop_player_mode()
            elif choice == 5:
                self.logger.info("Starting Lock/Unlock Player mode")
                self.run_lock_unlock_player_mode()
            elif choice == 6:
                self.logger.info("Starting Starter Helper mode")
                self._run_starter_helper_mode()
            elif choice == 7:
                self.logger.info("Starting Trade Simulator mode")
                self.run_trade_simulator_mode()
            elif choice == 8:
                print("Goodbye!")
                self.logger.info("User exited League Helper application")
                break
            else:
                self.logger.warning(f"Invalid menu choice: {choice}")
                print("Invalid choice. Please try again.")


    def show_main_menu(self):
        """
        Display the main menu and get user's choice.

        Shows all available modes and current roster status. Validates user input
        and returns the selected choice number.

        Returns:
            int: The user's menu choice (1-8), or -1 if invalid input

        Note:
            Menu options:
            1. Add to Roster - Draft players to your roster
            2. Mark Drafted Player - Mark opponents' picks as unavailable
            3. Waiver Optimizer - Find beneficial roster trades
            4. Drop Player - Remove players from roster
            5. Lock/Unlock Player - Protect players from trade suggestions
            6. Starter Helper - Get weekly lineup recommendations
            7. Trade Simulator - Simulate trades without saving
            8. Quit - Exit the application
        """
        print("\n" + "="*50)
        print("MAIN MENU")
        print("="*50)
        roster_len = self.player_manager.get_roster_len()
        print(f"Current roster: {roster_len} / {Constants.MAX_PLAYERS} players")
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
            self.logger.debug("User entered non-numeric input for menu choice")
            return -1


    def _run_add_to_roster_mode(self):
        """
        Delegate to Add to Roster mode manager.

        Passes current player_manager and team_data_manager instances to the mode
        manager to ensure it has the latest data.
        """
        self.add_to_roster_mode_manager.start_interactive_mode(self.player_manager, self.team_data_manager)

    def _run_starter_helper_mode(self):
        """
        Delegate to Add to Roster mode manager.

        Passes current player_manager and team_data_manager instances to the mode
        manager to ensure it has the latest data.
        """
        self.starter_helper_mode_manager.show_recommended_starters(self.player_manager, self.team_data_manager)



def main():
    """
    Main entry point for the League Helper application.

    Sets up logging configuration and initializes the League Helper Manager
    with the data directory path. Then starts the interactive mode.

    The application expects a 'data' directory at the project root containing:
    - league_config.json
    - players.csv
    - teams.csv
    - bye_weeks.csv
    """
    setup_logger(constants.LOG_NAME, constants.LOGGING_LEVEL, constants.LOGGING_TO_FILE, constants.LOGGING_FILE, constants.LOGGING_FORMAT)

    base_path = Path(__file__).parent.parent
    data_path = base_path / "data"

    leagueHelper = LeagueHelperManager(data_path)
    leagueHelper.start_interactive_mode()


if __name__ == "__main__":
    main()
