#!/usr/bin/env python3
"""
Trade Simulator Module for Draft Helper

This module implements the Trade Simulator functionality that allows users to
simulate multiple trades without affecting the actual roster data in players.csv.

Author: Kai Mizuno
Last Updated: September 2025
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import copy

# Add parent directories to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    from .. import draft_helper_constants as Constants
    from .roster_calculator import RosterCalculator
    from .player_search import PlayerSearch
    from .bye_week_visualizer import ByeWeekVisualizer
except ImportError:
    import draft_helper_constants as Constants
    from core.roster_calculator import RosterCalculator
    from core.player_search import PlayerSearch
    from core.bye_week_visualizer import ByeWeekVisualizer

from shared_files.FantasyPlayer import FantasyPlayer
from shared_files.configs.shared_config import CURRENT_NFL_WEEK


class TradeSimulator:
    """
    Handles trade simulation functionality without modifying persistent data.
    """

    def __init__(self, team, all_players: List[FantasyPlayer], scoring_function, logger=None):
        """
        Initialize the Trade Simulator.

        Args:
            team: FantasyTeam instance
            all_players: List of all available players
            scoring_function: Function to score players for trade evaluation
            logger: Optional logger for debugging
        """
        self.team = team
        self.all_players = all_players
        self.scoring_function = scoring_function
        self.logger = logger
        self.roster_calculator = RosterCalculator(team, logger)
        self.player_search = PlayerSearch(all_players, logger)

        # Store original state for restoration
        self.original_state = self.roster_calculator.get_roster_state_snapshot()
        self.original_player_states = {player.id: player.drafted for player in all_players} if all_players else {}

        # Track simulated trades for undo functionality
        self.trade_history = []

    def run_trade_simulator(self):
        """
        Main entry point for the Trade Simulator mode.
        """
        print("\n" + "="*60)
        print("TRADE SIMULATOR")
        print("="*60)
        print("Simulate trades without affecting your actual roster data.")
        print("You can simulate multiple trades and undo previous trades.")
        print("="*60)

        # Check if we have a roster to simulate trades with
        if len(self.team.roster) == 0:
            print("No players in roster to simulate trades with.")
            print("Add players to your roster first using 'Add to Roster' mode.")
            input("\nPress Enter to return to Main Menu...")
            return

        try:
            while True:
                # Display current simulated roster state
                self._display_current_state()

                # Show trade simulation options
                choice = self._show_simulator_menu()

                if choice == 1:
                    # Simulate a trade
                    self._simulate_trade()
                elif choice == 2:
                    # Undo last trade
                    self._undo_last_trade()
                elif choice == 3:
                    # Reset to original roster
                    self._reset_to_original()
                elif choice == 4:
                    # Exit simulator
                    break
                else:
                    print("Invalid choice. Please try again.")

        except Exception as e:
            print(f"Error in trade simulator: {e}")
            if self.logger:
                self.logger.error(f"Error in trade simulator: {e}")

        finally:
            # Always restore original state when exiting
            self._restore_original_state()
            print("Returning to Main Menu...")

    def _display_current_state(self):
        """
        Display the current simulated roster state with scores.
        """
        print(f"\nCURRENT SIMULATED ROSTER ({len(self.trade_history)} trades made)")
        print("-" * 60)

        # Display numbered roster (1-15) sorted by score
        current_roster = self.roster_calculator.display_numbered_roster(self.scoring_function)

        # Calculate and display scores
        current_score = self.roster_calculator.calculate_total_score(self.scoring_function)
        original_score = self._calculate_original_score()
        total_difference = current_score - original_score

        print(f"\nCurrent Total Score: {current_score:.2f}")
        print(f"Original Score:      {original_score:.2f}")
        print(f"Difference:          {total_difference:+.2f}")

        # Show position breakdown if there are differences
        if abs(total_difference) > 0.01:  # Only show if meaningful difference
            original_position_scores = self._calculate_original_position_scores()
            self.roster_calculator.compare_scores(
                self.scoring_function,
                original_score,
                original_position_scores,
                "DETAILED SCORE COMPARISON"
            )

        # Display bye week summary for current roster
        visualizer = ByeWeekVisualizer(self.logger)
        bye_summary = visualizer.generate_bye_week_summary(list(self.team.roster), CURRENT_NFL_WEEK)
        print(bye_summary)

    def _show_simulator_menu(self) -> int:
        """
        Display the trade simulator menu and get user choice.

        Returns:
            User's choice as integer
        """
        print(f"\nTRADE SIMULATOR OPTIONS")
        print("-" * 30)
        print("1. Simulate Trade")
        print("2. Undo Last Trade")
        print("3. Reset to Original Roster")
        print("4. Exit Trade Simulator")
        print("-" * 30)

        try:
            choice = int(input("Enter your choice (1-4): ").strip())
            return choice
        except ValueError:
            return -1

    def _simulate_trade(self):
        """
        Simulate a single trade by selecting a player to trade away and searching for a replacement.
        """
        # Step 1: Select player from roster to trade away
        if not self.team.roster:
            print("No players in roster to trade away.")
            return

        print("\nSelect a player from your roster to trade away:")
        roster_list = self.roster_calculator.display_numbered_roster(self.scoring_function)

        try:
            choice = int(input(f"\nEnter player number (1-{len(roster_list)}): ").strip())
            if 1 <= choice <= len(roster_list):
                player_to_trade_away = roster_list[choice - 1]
            else:
                print("Invalid selection.")
                return
        except ValueError:
            print("Invalid input.")
            return

        # Check if player is locked
        if getattr(player_to_trade_away, 'locked', False):
            print(f"{player_to_trade_away.name} is locked and cannot be traded.")
            return

        print(f"Selected to trade away: {player_to_trade_away.name} ({player_to_trade_away.position})")

        # Step 2: Search for replacement player
        replacement_player = self._search_for_replacement_player(player_to_trade_away)
        if replacement_player is None:
            print("Trade simulation cancelled.")
            return

        # Step 3: Execute the simulated trade
        success = self._execute_simulated_trade(player_to_trade_away, replacement_player)
        if success:
            print(f"\nTrade simulated: {player_to_trade_away.name} → {replacement_player.name}")
            print("\nUpdated roster:")
            self.roster_calculator.display_numbered_roster(self.scoring_function)
        else:
            print("Failed to simulate trade.")

    def _search_for_replacement_player(self, player_to_trade_away: FantasyPlayer) -> Optional[FantasyPlayer]:
        """
        Search for a replacement player using the player search functionality.

        Args:
            player_to_trade_away: Player being traded away

        Returns:
            Selected replacement player or None if cancelled
        """
        print(f"\nSearch for a replacement for {player_to_trade_away.name} ({player_to_trade_away.position}):")

        while True:
            search_term = input("Enter player name (or part of name) to search (or 'back' to cancel): ").strip()

            if search_term.lower() in ['back', 'cancel', '']:
                return None

            # Search both available (drafted=0) and drafted by others (drafted=1) players
            available_matches = self.player_search.search_players_by_name(search_term, drafted_filter=0)
            drafted_matches = self.player_search.search_players_by_name(search_term, drafted_filter=1)

            # Combine and filter out current roster players (drafted=2)
            all_matches = available_matches + drafted_matches
            all_matches = [p for p in all_matches if p.drafted != 2]

            if not all_matches:
                print(f"No players found matching '{search_term}'. Try again or type 'back' to cancel.")
                continue

            # Display matches
            print(f"\nFound {len(all_matches)} matching player(s):")
            for i, player in enumerate(all_matches, start=1):
                availability = "Available" if player.drafted == 0 else "Drafted by others"
                print(f"{i}. {player.name} ({player.position} - {player.team}) [{availability}]")

            print(f"{len(all_matches) + 1}. Search again")
            print(f"{len(all_matches) + 2}. Cancel trade")

            try:
                choice = int(input(f"Enter your choice (1-{len(all_matches) + 2}): ").strip())

                if 1 <= choice <= len(all_matches):
                    selected_player = all_matches[choice - 1]

                    # Validate trade compatibility
                    if self._validate_trade_compatibility(player_to_trade_away, selected_player):
                        # Check for bye week conflicts and warn user
                        self._check_bye_week_conflicts(selected_player, player_to_trade_away)
                        return selected_player
                    else:
                        print("This trade is not valid. Please select a different player.")
                        continue
                elif choice == len(all_matches) + 1:
                    continue  # Search again
                elif choice == len(all_matches) + 2:
                    return None  # Cancel
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input.")

    def _validate_trade_compatibility(self, player_out: FantasyPlayer, player_in: FantasyPlayer) -> bool:
        """
        Validate that a trade is compatible with roster construction rules.

        Args:
            player_out: Player being traded away
            player_in: Player being traded in

        Returns:
            True if trade is valid, False otherwise
        """
        # Use the team's existing validation logic
        return self.team._can_replace_player(player_out, player_in)

    def _check_bye_week_conflicts(self, player_in: FantasyPlayer, player_out: FantasyPlayer) -> None:
        """
        Check if the incoming player has the same bye week as other roster players and warn user.

        Args:
            player_in: Player being traded in
            player_out: Player being traded away (will be excluded from check)
        """
        # Check if the incoming player has a bye week
        if not hasattr(player_in, 'bye_week') or player_in.bye_week is None:
            return

        incoming_bye = player_in.bye_week

        # Find other roster players with the same bye week (excluding the player being traded away)
        conflicting_players = []
        for roster_player in self.team.roster:
            if roster_player.id == player_out.id:
                continue  # Skip the player being traded away

            if (hasattr(roster_player, 'bye_week') and
                roster_player.bye_week is not None and
                roster_player.bye_week == incoming_bye):
                conflicting_players.append(roster_player)

        # Display warning if conflicts found
        if conflicting_players:
            print(f"\n⚠️  BYE WEEK CONFLICT WARNING ⚠️")
            print(f"{player_in.name} has bye week {incoming_bye}")
            print(f"Other players with bye week {incoming_bye}:")
            for p in conflicting_players:
                print(f"  - {p.name} ({p.position} - {p.team})")
            print()

    def _execute_simulated_trade(self, player_out: FantasyPlayer, player_in: FantasyPlayer) -> bool:
        """
        Execute a simulated trade and track it for undo functionality.

        Args:
            player_out: Player being traded away
            player_in: Player being traded in

        Returns:
            True if trade executed successfully, False otherwise
        """
        # Store trade information for undo
        trade_info = {
            'player_out': player_out,
            'player_in': player_in,
            'player_out_original_drafted': player_out.drafted,
            'player_in_original_drafted': player_in.drafted
        }

        # Temporarily mark the incoming player as available so draft_player can add them
        # (replace_player calls draft_player which checks is_available())
        original_player_in_drafted = player_in.drafted
        player_in.drafted = 0

        # Execute the trade using team's replace_player method
        success = self.team.replace_player(player_out, player_in)

        if success:
            # Player states are already updated by draft_player and remove_player
            # player_out.drafted is set to 0 by remove_player
            # player_in.drafted is set to 2 by draft_player

            # Track this trade
            self.trade_history.append(trade_info)

            if self.logger:
                self.logger.info(f"Simulated trade: {player_out.name} → {player_in.name}")
        else:
            # If trade failed, restore the original drafted state
            player_in.drafted = original_player_in_drafted

        return success

    def _undo_last_trade(self):
        """
        Undo the last simulated trade.
        """
        if not self.trade_history:
            print("No trades to undo.")
            return

        # Get the last trade
        last_trade = self.trade_history.pop()

        # Reverse the trade
        player_out = last_trade['player_out']  # This was traded away, bring back
        player_in = last_trade['player_in']    # This was traded in, remove

        # Temporarily mark the original player as available so we can bring them back
        original_player_out_drafted = player_out.drafted
        player_out.drafted = 0

        # Execute reverse trade
        success = self.team.replace_player(player_in, player_out)

        if success:
            # Restore original player states
            player_out.drafted = last_trade['player_out_original_drafted']
            player_in.drafted = last_trade['player_in_original_drafted']

            print(f"Undid trade: {player_in.name} → {player_out.name}")
            print("\nUpdated roster:")
            self.roster_calculator.display_numbered_roster(self.scoring_function)

            if self.logger:
                self.logger.info(f"Undid simulated trade: {player_in.name} → {player_out.name}")
        else:
            # If reverse failed, restore original state and put the trade back
            player_out.drafted = original_player_out_drafted
            self.trade_history.append(last_trade)
            print("Failed to undo trade.")

    def _reset_to_original(self):
        """
        Reset the simulated roster back to the original state.
        """
        if not self.trade_history:
            print("Roster is already in original state.")
            return

        # Restore original state
        self.roster_calculator.restore_roster_state(self.original_state)

        # Restore all player drafted states
        for player in self.all_players:
            if player.id in self.original_player_states:
                player.drafted = self.original_player_states[player.id]

        # Clear trade history
        self.trade_history.clear()

        print("Roster reset to original state.")

        if self.logger:
            self.logger.info("Trade simulator reset to original state")

    def _restore_original_state(self):
        """
        Restore the original state when exiting the simulator.
        """
        # Restore team state
        self.roster_calculator.restore_roster_state(self.original_state)

        # Restore all player drafted states
        for player in self.all_players:
            if player.id in self.original_player_states:
                player.drafted = self.original_player_states[player.id]

        if self.logger:
            self.logger.info("Trade simulator: original state restored on exit")

    def _calculate_original_score(self) -> float:
        """
        Calculate the total score of the original roster.

        Returns:
            Original roster total score
        """
        original_total = 0.0
        for player_id in self.original_state['player_drafted_states']:
            if self.original_state['player_drafted_states'][player_id] == 2:  # Was on roster
                # Find the player and calculate score
                for player in self.all_players:
                    if hasattr(player, 'id') and player.id == player_id:
                        original_total += self.scoring_function(player)
                        break
        return original_total

    def _calculate_original_position_scores(self) -> Dict[str, float]:
        """
        Calculate position scores for the original roster.

        Returns:
            Dictionary mapping position to original score
        """
        position_scores = {}

        # Initialize all positions with 0
        for pos in Constants.MAX_POSITIONS.keys():
            position_scores[pos] = 0.0

        # Calculate original position scores
        for player_id in self.original_state['player_drafted_states']:
            if self.original_state['player_drafted_states'][player_id] == 2:  # Was on roster
                # Find the player and add to position score
                for player in self.all_players:
                    if hasattr(player, 'id') and player.id == player_id:
                        score = self.scoring_function(player)
                        position = player.position
                        if position in position_scores:
                            position_scores[position] += score
                        else:
                            position_scores[position] = score
                        break

        return position_scores