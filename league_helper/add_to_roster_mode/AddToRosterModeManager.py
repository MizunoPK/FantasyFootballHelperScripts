"""
Add to Roster Mode Manager

Manages the draft assistant mode for building your fantasy roster.
Provides intelligent player recommendations based on draft position strategy,
team needs, and the 9-step scoring algorithm.

Key features:
- Real-time draft recommendations based on current round
- Position-aware draft strategy (follows DRAFT_ORDER config)
- Interactive player selection
- Roster display by draft rounds
- Automatic CSV updates after each pick

The mode uses the configured DRAFT_ORDER to determine which positions
should be prioritized in each round, applying appropriate bonuses to
guide recommendations.

Author: Kai Mizuno
"""

from pathlib import Path
from typing import Dict, Any, List

import sys
sys.path.append(str(Path(__file__).parent))
import constants as Constants

sys.path.append(str(Path(__file__).parent.parent))
from util.ConfigManager import ConfigManager
from util.PlayerManager import PlayerManager
from util.TeamDataManager import TeamDataManager
from util.ScoredPlayer import ScoredPlayer

sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.LoggingManager import get_logger
from utils.FantasyPlayer import FantasyPlayer

class AddToRosterModeManager:
    """
    Manages the Add to Roster (draft assistant) mode.

    This mode helps users build their fantasy roster by providing intelligent
    player recommendations that consider:
    - Current draft round and position strategy (PRIMARY/SECONDARY bonuses)
    - Team composition and positional needs
    - Player scores calculated via the 9-step algorithm
    - Availability and roster limits

    Attributes:
        config (ConfigManager): Configuration manager with draft strategy
        logger: Logger instance for tracking draft events
        player_manager (PlayerManager): Manages player data and scoring
        team_data_manager (TeamDataManager): Provides team rankings

    Example workflow:
        1. User enters Add to Roster mode
        2. System shows current roster organized by draft rounds
        3. System calculates top recommendations for current round
        4. User selects a player to draft
        5. Roster updated and saved to CSV
        6. Returns to main menu
    """

    def __init__(self, config: ConfigManager, player_manager : PlayerManager, team_data_manager : TeamDataManager):
        """
        Initialize Add to Roster Mode Manager.

        Args:
            config (ConfigManager): Configuration with draft order strategy
            player_manager (PlayerManager): Manages players and scoring
            team_data_manager (TeamDataManager): Provides team data
        """
        self.config = config
        self.logger = get_logger()
        self.logger.debug("Initializing Add to Roster Mode Manager")
        self.set_managers(player_manager, team_data_manager)

    def set_managers(self, player_manager : PlayerManager, team_data_manager : TeamDataManager):
        self.player_manager = player_manager
        self.team_data_manager = team_data_manager


    def start_interactive_mode(self, player_manager, team_data_manager):
        """
        Start the interactive Add to Roster mode.

        Displays current roster and provides player recommendations until
        user drafts a player or chooses to return to main menu.

        Args:
            player_manager (PlayerManager): Updated player manager instance
            team_data_manager (TeamDataManager): Updated team data manager instance
        """
        self.set_managers(player_manager, team_data_manager)
        self.logger.info("Entering Add to Roster interactive mode")

        print("\n" + "="*50)
        print("ADD TO ROSTER MODE")
        print("="*50)

        # Show enhanced roster display by draft rounds
        self._display_roster_by_draft_rounds()

        current_round = self._get_current_round()
        self.logger.info(f"Current draft round: {current_round}/{Constants.MAX_PLAYERS}")

        while True:
            print("\nTop draft recommendations based on your current roster:")
            recommendations = self.get_recommendations()

            if not recommendations:
                self.logger.warning("No recommendations available - roster full or no available players")
                print("No recommendations available (roster may be full or no available players).")
                print("Returning to Main Menu...")
                break

            for i, p in enumerate(recommendations, start=1):
                print(f"{i}. {p}")
            print(f"{len(recommendations) + 1}. Back to Main Menu")

            try:
                choice = input(f"\nEnter your choice (1-{len(recommendations) + 1}): ").strip()

                if choice.isdigit():
                    index = int(choice) - 1

                    # Check for Back option
                    if index == len(recommendations):
                        print("Returning to Main Menu...")
                        break

                    # Validate player selection
                    if 0 <= index < len(recommendations):
                        player_to_draft = recommendations[index].player
                        success = self.player_manager.draft_player(player_to_draft)

                        if success:
                            print(f"\nSuccessfully added {player_to_draft.name} to your roster!")
                            self.player_manager.update_players_file()
                            self.logger.info(f"Player {player_to_draft.name} drafted to user's team (drafted=2)")

                            # Show updated roster
                            self._display_roster_by_draft_rounds()

                            print("Returning to Main Menu...")
                            break
                        else:
                            print(f"Failed to add {player_to_draft.name}. Check roster limits.")
                            print("Returning to Main Menu...")
                            break
                    else:
                        print("Invalid selection. Please try again.")
                else:
                    print("Invalid input. Please enter a number.")

            except ValueError:
                print("Invalid input. Please enter a number.")
            except Exception as e:
                print(f"Error: {e}")
                print("Returning to Main Menu...")
                self.logger.error(f"Error in add to roster mode: {e}")
                break

    
    def _display_roster_by_draft_rounds(self):
        """Display current roster organized by draft round order based on DRAFT_ORDER config"""
        print(f"\nCurrent Roster by Draft Round:")
        print("-" * 50)

        if not self.player_manager.team.roster:
            print("No players in roster yet.")
            return

        # Match players to their optimal draft rounds
        round_assignments = self._match_players_to_rounds()

        for round_num in range(1, Constants.MAX_PLAYERS + 1):
            ideal_position = self.config.get_ideal_draft_position(round_num - 1)

            if round_num in round_assignments:
                player = round_assignments[round_num]
                print(f"Round {round_num:2d} (Ideal: {ideal_position:4s}): {player.name} ({player.position}) - {player.fantasy_points:.1f} pts")
            else:
                print(f"Round {round_num:2d} (Ideal: {ideal_position:4s}): [EMPTY SLOT]")

        print(f"\nRoster Status: {self.player_manager.get_roster_len()}/{Constants.MAX_PLAYERS} players drafted")


    def _match_players_to_rounds(self) -> Dict[int, Any]:
        """
        Match current roster players to draft round slots using optimal fit strategy.
        Returns dictionary mapping round numbers to players.
        """
        round_assignments = {}  # round_num -> player
        available_players = list(self.player_manager.team.roster)  # Copy of roster players

        # First pass: Assign players to rounds where their position perfectly matches the ideal
        for round_num in range(1, Constants.MAX_PLAYERS + 1):
            ideal_position = self.config.get_ideal_draft_position(round_num - 1)

            for player in available_players:
                if Constants.get_position_with_flex(player.position) == ideal_position:
                    round_assignments[round_num] = player
                    available_players.remove(player)
                    break

        return round_assignments
    
    def _get_current_round(self) -> int:
        round_assignments = self._match_players_to_rounds()
        for round_num in range(1, Constants.MAX_PLAYERS + 1):
            if round_num not in round_assignments:
                return round_num 
    
    
    def get_recommendations(self) -> List[ScoredPlayer]:
        # get a list of available players that can be drafted
        available_players = self.player_manager.get_player_list(drafted_vals=[0], can_draft=True)

        # Score each player
        scored_players : List[ScoredPlayer] = []
        current_round=self._get_current_round()
        for p in available_players:
            scored_player = self.player_manager.score_player(p, draft_round=current_round)
            scored_players.append(scored_player)

        # Sort available players by score descending
        ranked_players = sorted(scored_players, key=lambda x: x.score, reverse=True)

        # Return top recommended players
        self.logger.info(f"Recommended next picks: {[p.player.name for p in ranked_players[:Constants.RECOMMENDATION_COUNT]]}")
        return ranked_players[:Constants.RECOMMENDATION_COUNT]
    
