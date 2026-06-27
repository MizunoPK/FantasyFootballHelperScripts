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

from typing import Dict, List

import league_helper.constants as Constants
from league_helper.util.ConfigManager import ConfigManager
from league_helper.util.PlayerManager import PlayerManager
from league_helper.util.TeamDataManager import TeamDataManager
from league_helper.util.ScoredPlayer import ScoredPlayer
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
        self.set_managers(player_manager, team_data_manager)


    def set_managers(self, player_manager : PlayerManager, team_data_manager : TeamDataManager):
        """
        Update manager references with new instances.

        Called at the start of interactive mode to ensure we have the latest
        data after potentially returning from other modes.

        Args:
            player_manager (PlayerManager): Updated player manager instance
            team_data_manager (TeamDataManager): Updated team data manager instance
        """
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

        self.logger.debug(f"Displaying roster for user ({self.player_manager.get_roster_len()}/{self.config.max_players} players)")
        self._display_roster_by_draft_rounds()

        current_round = self._get_current_round()
        self.logger.info(f"Current draft round: {current_round}/{self.config.max_players}")

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

                    if index == len(recommendations):
                        self.logger.info("User chose to return to Main Menu")
                        print("Returning to Main Menu...")
                        break

                    if 0 <= index < len(recommendations):
                        player_to_draft = recommendations[index].player
                        self.logger.info(f"User selected {player_to_draft.name} ({player_to_draft.position}) to draft")

                        success = self.player_manager.draft_player(player_to_draft)

                        if success:
                            print(f"\nSuccessfully added {player_to_draft.name} to your roster!")

                            self.player_manager.update_players_file()
                            self.logger.info(f"Player {player_to_draft.name} drafted to user's team (drafted=2)")

                            self._display_roster_by_draft_rounds()

                            print("Returning to Main Menu...")
                            break
                        else:
                            self.logger.warning(f"Failed to draft {player_to_draft.name} - roster limits or position constraints")
                            print(f"Failed to add {player_to_draft.name}. Check roster limits.")
                            print("Returning to Main Menu...")
                            break
                    else:
                        self.logger.debug(f"Invalid selection: {choice} (out of range 1-{len(recommendations) + 1})")
                        print("Invalid selection. Please try again.")
                else:
                    self.logger.debug(f"Invalid input: non-numeric value '{choice}'")
                    print("Invalid input. Please enter a number.")

            except ValueError:
                print("Invalid input. Please enter a number.")
            except Exception as e:
                print(f"Error: {e}")
                print("Returning to Main Menu...")
                self.logger.error(f"Error in add to roster mode: {e}")
                break

    def get_recommendations(self) -> List[ScoredPlayer]:
        """
        Generate top player recommendations for the current draft round.

        Uses the complete 9-step scoring algorithm plus draft round bonuses to rank
        all available players. Returns the top 10 recommendations sorted by score.

        Returns:
            List[ScoredPlayer]: Top 10 recommended players (or fewer if less available)

        Scoring includes:
            - Step 1: Normalized fantasy points (base score)
            - Step 2: ADP multiplier (draft value adjustment)
            - Step 3: Player rating multiplier (expert consensus)
            - Step 4: Team quality multiplier (offensive/defensive ranks)
            - Step 5: Performance deviation (recent form)
            - Step 6: Matchup multiplier (weekly opponent strength)
            - Step 7: Draft order bonus (position-specific PRIMARY/SECONDARY bonuses)
            - Step 8: Bye week penalty (roster overlap conflicts)
            - Step 9: Injury penalty (health risk assessment)
        """
        available_players = self.player_manager.get_player_list(drafted_vals=[0], can_draft=True)
        self.logger.debug(f"Found {len(available_players)} draftable players for recommendations")

        scored_players : List[ScoredPlayer] = []

        current_round=self._get_current_round()

        for p in available_players:
            scored_player = self.player_manager.score_player(
                p,
                draft_round=current_round - 1,
                adp=True,
                player_rating=True,
                team_quality=True,
                performance=False,
                matchup=False,
                schedule=False,
                bye=True,
                injury=True,
                is_draft_mode=True,
                nfl_team_penalty=True
            )
            scored_players.append(scored_player)

        ranked_players = sorted(scored_players, key=lambda x: x.score, reverse=True)

        self.logger.debug(f"Recommended next picks: {[p.player.name for p in ranked_players[:Constants.RECOMMENDATION_COUNT]]}")

        return ranked_players[:Constants.RECOMMENDATION_COUNT]


    def _display_roster_by_draft_rounds(self):
        """
        Display current roster organized by draft round order.

        Shows all 15 draft rounds with either the player assigned to that round
        or [EMPTY SLOT] if the round is unfilled. Each round displays the ideal
        position from the DRAFT_ORDER config to guide draft strategy.

        The display helps users understand:
        - Which positions they've already filled
        - Which rounds are empty and need players
        - What positions should be prioritized next (based on ideal position)
        - Overall draft progress (X/15 players drafted)

        Returns:
            None: Prints roster display to console
        """
        print(f"\nCurrent Roster by Draft Round:")
        print("-" * 50)

        if not self.player_manager.team.roster:
            print("No players in roster yet.")
            return

        round_assignments = self._match_players_to_rounds()

        for round_num in range(1, self.config.max_players + 1):
            ideal_position = self.config.get_ideal_draft_position(round_num - 1)

            if round_num in round_assignments:
                player = round_assignments[round_num]
                print(f"Round {round_num:2d} (Ideal: {ideal_position:4s}): {player.name} ({player.position}) - {player.fantasy_points:.1f} pts")
            else:
                print(f"Round {round_num:2d} (Ideal: {ideal_position:4s}): [EMPTY SLOT]")

        print(f"\nRoster Status: {self.player_manager.get_roster_len()}/{self.config.max_players} players drafted")


    def _match_players_to_rounds(self) -> Dict[int, FantasyPlayer]:
        """
        Match current roster players to draft round slots using optimal fit strategy.

        Uses a greedy algorithm to assign each roster player to their optimal draft round
        based on the DRAFT_ORDER config. Players are matched to rounds where their position
        perfectly matches the ideal position, ensuring they would have received PRIMARY
        bonuses if drafted in that round.

        The algorithm prioritizes:
        1. Perfect position matches (e.g., QB to QB-ideal rounds)
        2. FLEX conversion for RB/WR/DST (these can match FLEX-ideal rounds)
        3. Sequential processing to avoid conflicts

        Returns:
            Dict[int, FantasyPlayer]: Dictionary mapping round numbers (1-15) to FantasyPlayer objects.
                           Only rounds with assigned players are included as keys.
                           Empty rounds are omitted from the dictionary.

        Example:
            If roster has QB, RB, WR with 3 players total:
            {1: FantasyPlayer(RB1), 2: FantasyPlayer(WR1), 3: FantasyPlayer(QB1)}
        """
        round_assignments = {}

        available_players = list(self.player_manager.team.roster)

        for round_num in range(1, self.config.max_players + 1):
            ideal_position = self.config.get_ideal_draft_position(round_num - 1)

            for player in available_players:
                if self._position_matches_ideal(player.position, ideal_position):
                    round_assignments[round_num] = player

                    available_players.remove(player)

                    break

        self.logger.debug(f"Matched {len(round_assignments)} players to draft rounds using optimal fit algorithm")
        return round_assignments

    def _position_matches_ideal(self, player_position: str, ideal_position: str) -> bool:
        """
        Check if a player's position can fill a round with the given ideal position.

        For FLEX-eligible positions (defined in config.flex_eligible_positions,
        typically RB and WR), players can match both their native position rounds
        AND FLEX-ideal rounds.

        For non-FLEX positions (QB, TE, K, DST), players must match exactly.

        Args:
            player_position: Player's actual position ("RB", "WR", "QB", etc.)
            ideal_position: Ideal position for the round from DRAFT_ORDER

        Returns:
            True if player can fill this round, False otherwise

        Examples:
            >>> self._position_matches_ideal("RB", "RB")     # True (native match)
            >>> self._position_matches_ideal("RB", "FLEX")   # True (FLEX-eligible)
            >>> self._position_matches_ideal("RB", "WR")     # False (different position)
            >>> self._position_matches_ideal("QB", "QB")     # True (exact match)
            >>> self._position_matches_ideal("QB", "FLEX")   # False (QB not FLEX-eligible)
        """
        if player_position in self.config.flex_eligible_positions:
            return player_position == ideal_position or ideal_position == "FLEX"
        else:
            return player_position == ideal_position

    def _get_current_round(self) -> int:
        """
        Calculate which draft round we're currently in based on roster composition.

        Returns:
            int: The current draft round number (1-15), or None if roster is full

        Logic:
            - Matches existing roster players to their optimal rounds
            - Returns the first round number that doesn't have a player assigned
            - If all 15 rounds have players, returns None (roster is full)

        Example:
            If roster has 5 players matched to rounds 1-5, returns 6
        """
        round_assignments = self._match_players_to_rounds()

        for round_num in range(1, self.config.max_players + 1):
            if round_num not in round_assignments:
                self.logger.debug(f"Calculated current round: {round_num} (roster has {len(round_assignments)} players)")
                return round_num

        self.logger.debug("Roster is full (15/15 players) - no current round")


