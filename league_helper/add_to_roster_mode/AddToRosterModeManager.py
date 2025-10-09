

from pathlib import Path
from typing import Dict, List, Optional, Any
from add_to_roster_mode.AddToRosterConfigManager import AddToRosterConfigManager

import sys
sys.path.append(str(Path(__file__).parent))
import constants as Constants

sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.LoggingManager import get_logger

class AddToRosterModeManager:

    def __init__(self, config_folder : Path, player_manager, team_data_manager):
        self.config = AddToRosterConfigManager(config_folder)
        self.logger = get_logger()
        self.set_managers(player_manager, team_data_manager)

    def set_managers(self, player_manager, team_data_manager):
        self.player_manager = player_manager
        self.team_data_manager = team_data_manager


    def start_interactive_mode(self, player_manager, team_data_manager):
        self.set_managers(player_manager, team_data_manager)
        print("\n" + "="*50)
        print("ADD TO ROSTER MODE")
        print("="*50)

        # Show enhanced roster display by draft rounds
        self._display_roster_by_draft_rounds()

        while True:
            print("\nTop draft recommendations based on your current roster:")
            recommendations = self.get_recommendations()

            if not recommendations:
                print("No recommendations available (roster may be full or no available players).")
                print("Returning to Main Menu...")
                break

            for i, p in enumerate(recommendations, start=1):
                # Show calculated score (used for ranking) instead of raw fantasy points
                status = f" ({p.injury_status})" if p.injury_status != 'ACTIVE' else ""
                score_display = getattr(p, 'score', p.fantasy_points)  # Use calculated score if available

                # Show consistency category if available
                consistency_indicator = self._get_consistency_indicator(p)

                print(f"{i}. {p.name} ({p.team} {p.position}) - {score_display:.1f} pts{consistency_indicator} {status}")
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
                        player_to_draft = recommendations[index]
                        success = self.team.draft_player(player_to_draft)

                        if success:
                            print(f"\nSuccessfully added {player_to_draft.name} to your roster!")
                            save_players_func()
                            self.logger.info(f"Player {player_to_draft.name} drafted to user's team (drafted=2)")

                            # Show updated roster
                            self.display_roster_by_draft_order()

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
            ideal_position = self._get_ideal_draft_position(round_num - 1)

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
            ideal_position = self._get_ideal_draft_position(round_num - 1)

            for player in available_players:
                if Constants.get_position_with_flex(player) == ideal_position:
                    round_assignments[round_num] = player
                    available_players.remove(player)
                    break

        return round_assignments
    

    def _get_ideal_draft_position(self, round_num: int) -> str:
        """Get the ideal position to draft in a given round"""
        if round_num < len(self.config.draft_order):
            best_position = max(self.config.draft_order[round_num], key=self.config.draft_order[round_num].get)
            return best_position
        return Constants.FLEX
    
    
    def get_recommendations(self):
        # get a list of available players that can be drafted
        available_players = [
            p for p in self.players
            if self.player_manager.team.can_draft(p)
        ]

        # Score each player
        for p in available_players:
            p.score = self.player_manager.score_player(p)

        # Sort available players by score descending
        ranked_players = sorted(available_players, key=lambda x: x.score, reverse=True)

        # Return top recommended players
        self.logger.info(f"Recommended next picks: {[p.name for p in ranked_players[:self.config.recommendation_count]]}")
        return ranked_players[:self.config.recommendation_count]
    
