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
from typing import Dict, List

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

    # ========================================================================
    # INITIALIZATION
    # ========================================================================

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

    # ========================================================================
    # PUBLIC MANAGER SETUP
    # ========================================================================

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

    # ========================================================================
    # PUBLIC INTERFACE METHODS
    # ========================================================================

    def start_interactive_mode(self, player_manager, team_data_manager):
        """
        Start the interactive Add to Roster mode.

        Displays current roster and provides player recommendations until
        user drafts a player or chooses to return to main menu.

        Args:
            player_manager (PlayerManager): Updated player manager instance
            team_data_manager (TeamDataManager): Updated team data manager instance
        """
        # Update manager references to ensure we have latest data
        # This is important for when user returns from another mode
        self.set_managers(player_manager, team_data_manager)
        self.logger.info("Entering Add to Roster interactive mode")

        # Display mode header for user clarity
        print("\n" + "="*50)
        print("ADD TO ROSTER MODE")
        print("="*50)

        # Show enhanced roster display by draft rounds
        # This helps user understand their draft strategy and position needs
        self.logger.debug(f"Displaying roster for user ({self.player_manager.get_roster_len()}/{self.config.max_players} players)")
        self._display_roster_by_draft_rounds()

        # Calculate which draft round we're currently in (1-15)
        # This determines which position bonuses apply to recommendations
        current_round = self._get_current_round()
        self.logger.info(f"Current draft round: {current_round}/{self.config.max_players}")

        # Main interaction loop - continues until user drafts a player or exits
        while True:
            # Display header for recommendation section
            print("\nTop draft recommendations based on your current roster:")

            # Get top 10 recommendations with draft round bonuses applied
            # These are scored using the full 9-step algorithm + draft strategy bonuses
            recommendations = self.get_recommendations()

            # Handle case where no players are available (roster full or all players drafted)
            if not recommendations:
                self.logger.warning("No recommendations available - roster full or no available players")
                print("No recommendations available (roster may be full or no available players).")
                print("Returning to Main Menu...")
                break

            # Display numbered list of recommended players
            # Each entry shows player name, position, score, and scoring breakdown
            for i, p in enumerate(recommendations, start=1):
                print(f"{i}. {p}")

            # Add "Back to Main Menu" option after the recommendations
            # This is always option N+1 where N is the number of recommendations
            print(f"{len(recommendations) + 1}. Back to Main Menu")

            try:
                # Get user's selection (1-based indexing for user-friendliness)
                choice = input(f"\nEnter your choice (1-{len(recommendations) + 1}): ").strip()

                # Only process if input is a valid integer
                if choice.isdigit():
                    # Convert to 0-based index for list access
                    index = int(choice) - 1

                    # Check if user selected "Back to Main Menu" option
                    # This is the last option (index equals number of recommendations)
                    if index == len(recommendations):
                        self.logger.info("User chose to return to Main Menu")
                        print("Returning to Main Menu...")
                        break

                    # Validate that selection is within valid range (0 to len-1)
                    # This prevents IndexError when accessing the recommendations list
                    if 0 <= index < len(recommendations):
                        # Extract the FantasyPlayer object from the ScoredPlayer
                        player_to_draft = recommendations[index].player
                        self.logger.info(f"User selected {player_to_draft.name} ({player_to_draft.position}) to draft")

                        # Attempt to draft the player (sets drafted=2, updates roster)
                        # This checks roster limits and position eligibility
                        success = self.player_manager.draft_player(player_to_draft)

                        if success:
                            # Draft succeeded - player added to roster
                            print(f"\nSuccessfully added {player_to_draft.name} to your roster!")

                            # Persist changes to CSV file immediately
                            # This ensures data is saved even if program crashes
                            self.player_manager.update_players_file()
                            self.logger.info(f"Player {player_to_draft.name} drafted to user's team (drafted=2)")

                            # Show updated roster with new player included
                            # This helps user see how the pick fits their draft strategy
                            self._display_roster_by_draft_rounds()

                            # Return to main menu after successful draft
                            print("Returning to Main Menu...")
                            break
                        else:
                            # Draft failed (roster full, position limit reached, or player locked)
                            self.logger.warning(f"Failed to draft {player_to_draft.name} - roster limits or position constraints")
                            print(f"Failed to add {player_to_draft.name}. Check roster limits.")
                            print("Returning to Main Menu...")
                            break
                    else:
                        # Selection was out of range (e.g., 0, negative, or > max_choice)
                        self.logger.debug(f"Invalid selection: {choice} (out of range 1-{len(recommendations) + 1})")
                        print("Invalid selection. Please try again.")
                else:
                    # Input was not a number (e.g., "abc", empty string)
                    self.logger.debug(f"Invalid input: non-numeric value '{choice}'")
                    print("Invalid input. Please enter a number.")

            except ValueError:
                # Catch any remaining conversion errors (shouldn't happen with isdigit() check)
                print("Invalid input. Please enter a number.")
            except Exception as e:
                # Catch any unexpected errors during draft process
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
        # Get list of available players (drafted=0) that can legally be drafted
        # can_draft=True filters by roster limits and position eligibility
        # This ensures we only recommend players the user can actually add
        available_players = self.player_manager.get_player_list(drafted_vals=[0], can_draft=True)
        self.logger.debug(f"Found {len(available_players)} draftable players for recommendations")

        # Score each available player using the full 9-step algorithm
        # We store results as ScoredPlayer objects which include:
        #   - The original FantasyPlayer object
        #   - The calculated score (float)
        #   - A list of scoring reasons (for transparency)
        scored_players : List[ScoredPlayer] = []

        # Get current draft round to apply appropriate position bonuses
        # For example, round 1 might give +50 points to FLEX positions
        # while round 3 might give +50 points to QB (per DRAFT_ORDER config)
        current_round=self._get_current_round()

        # Score each player with all scoring factors enabled
        for p in available_players:
            # Call PlayerManager's score_player method with draft_round parameter
            # This enables draft order bonuses (Step 7) based on current round
            #
            # All scoring flags set to True means we use the full algorithm:
            # - adp: Adjust for average draft position (higher ADP = better)
            # - player_rating: Apply expert rating multiplier
            # - team_quality: Consider offensive/defensive team ranks
            # - performance: Account for recent weekly performance trends
            # - matchup: Apply upcoming opponent difficulty adjustments
            #
            # The draft_round parameter is critical - it determines which positions
            # get PRIMARY (+50) or SECONDARY (+30) bonuses based on DRAFT_ORDER
            scored_player = self.player_manager.score_player(
                p,
                draft_round=current_round,  # Current round for position bonuses
                adp=True,                   # Enable ADP multiplier
                player_rating=True,         # Enable player rating multiplier
                team_quality=True,          # Enable team quality multiplier
                performance=True,           # Enable performance deviation
                matchup=True                # Enable matchup multiplier
            )
            scored_players.append(scored_player)

        # Sort all scored players by their total score in descending order
        # Higher scores = better recommendations
        # The lambda function extracts the score attribute from each ScoredPlayer
        ranked_players = sorted(scored_players, key=lambda x: x.score, reverse=True)

        # Log the top recommendations for debugging/tracking purposes
        # We log player names only (not full ScoredPlayer objects) for readability
        self.logger.debug(f"Recommended next picks: {[p.player.name for p in ranked_players[:Constants.RECOMMENDATION_COUNT]]}")

        # Return top N recommendations (default is 10 per Constants.RECOMMENDATION_COUNT)
        # If fewer than 10 players are available, return all of them
        # Python list slicing handles the case where list is shorter than slice range
        return ranked_players[:Constants.RECOMMENDATION_COUNT]

    # ========================================================================
    # PRIVATE DISPLAY HELPERS
    # ========================================================================

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
        # Display section header
        print(f"\nCurrent Roster by Draft Round:")
        print("-" * 50)

        # Check if roster is empty - if so, show message and return early
        # This avoids unnecessary processing and provides clear feedback
        if not self.player_manager.team.roster:
            print("No players in roster yet.")
            return

        # Match current roster players to their optimal draft rounds
        # This uses the DRAFT_ORDER config to determine ideal position for each round
        # Returns a dict mapping round_number -> player
        round_assignments = self._match_players_to_rounds()

        # Display all 15 draft rounds (even empty ones)
        # This helps user understand their draft strategy and which positions to prioritize
        for round_num in range(1, self.config.max_players + 1):
            # Get the ideal position for this round from the DRAFT_ORDER config
            # For example, round 1 might be "FLEX" (PRIMARY), round 3 might be "QB" (PRIMARY)
            # This uses 0-based indexing for the config list
            ideal_position = self.config.get_ideal_draft_position(round_num - 1)

            # Check if we have a player assigned to this round
            if round_num in round_assignments:
                # Player exists in this round - show their details
                player = round_assignments[round_num]
                print(f"Round {round_num:2d} (Ideal: {ideal_position:4s}): {player.name} ({player.position}) - {player.fantasy_points:.1f} pts")
            else:
                # Round is empty - show placeholder with ideal position
                # This helps user see what position they should target next
                print(f"Round {round_num:2d} (Ideal: {ideal_position:4s}): [EMPTY SLOT]")

        # Display roster status summary (e.g., "5/15 players drafted")
        # This helps user track overall draft progress
        print(f"\nRoster Status: {self.player_manager.get_roster_len()}/{self.config.max_players} players drafted")

    # ========================================================================
    # PRIVATE ROUND CALCULATION HELPERS
    # ========================================================================

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
        # Create dictionary to store round-to-player mappings
        # Key: round number (1-15), Value: FantasyPlayer object
        round_assignments = {}

        # Create working copy of roster to avoid modifying original list
        # Players will be removed from this list as they're assigned to rounds
        available_players = list(self.player_manager.team.roster)

        # ALGORITHM: Optimal fit strategy
        # First pass: Assign players to rounds where their position perfectly matches the ideal
        # This ensures that players go to rounds where they get PRIMARY bonuses
        #
        # Example: If round 1 ideal is "FLEX" and round 3 ideal is "QB":
        #   - QB players will preferentially go to round 3 (perfect match)
        #   - RB/WR players will go to FLEX rounds (rounds 1, 2, etc.)
        #
        # This greedy algorithm works well because:
        # 1. Most positions (QB, TE, K, DST) are non-FLEX and have limited round options
        # 2. FLEX positions (RB, WR, DST) have many valid rounds to choose from
        # 3. We process rounds sequentially, ensuring no conflicts
        for round_num in range(1, self.config.max_players + 1):
            # Get the ideal position for this round (e.g., "QB", "FLEX", "TE")
            # This determines what type of player should go in this round
            ideal_position = self.config.get_ideal_draft_position(round_num - 1)

            # Try to find a player whose position matches this round's ideal
            # We iterate through all available (not yet assigned) players
            for player in available_players:
                # Convert player's actual position to FLEX if eligible (RB/WR/DST)
                # For example, "RB" becomes "FLEX", "QB" stays "QB"
                # This allows RB/WR/DST to match FLEX-ideal rounds
                if Constants.get_position_with_flex(player.position) == ideal_position:
                    # Found a perfect match! Assign player to this round
                    round_assignments[round_num] = player

                    # Remove player from available pool so they can't be assigned twice
                    available_players.remove(player)

                    # Move to next round (we found our player for this round)
                    break

        # Return the round assignments
        # Note: Some rounds may not have assignments if we have fewer players than rounds
        # Or if player positions don't perfectly match all ideal positions
        self.logger.debug(f"Matched {len(round_assignments)} players to draft rounds using optimal fit algorithm")
        return round_assignments
    
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
        # Get dictionary of round assignments (round_num -> player)
        # This tells us which rounds have players and which are empty
        round_assignments = self._match_players_to_rounds()

        # Find the first empty round by checking rounds 1 through 15 sequentially
        # The first round without an assignment is our "current round"
        for round_num in range(1, self.config.max_players + 1):
            if round_num not in round_assignments:
                # Found an empty round - this is where we should draft next
                self.logger.debug(f"Calculated current round: {round_num} (roster has {len(round_assignments)} players)")
                return round_num

        # If we get here, all 15 rounds have players assigned (roster is full)
        # Return None to indicate no current round (no more picks needed)
        # Note: Python functions return None by default if no explicit return,
        # but making it explicit for clarity
        self.logger.debug("Roster is full (15/15 players) - no current round")
