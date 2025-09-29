#!/usr/bin/env python3
"""
Trade Analysis Module for Draft Helper

This module handles all trade analysis and optimization functionality,
extracted from the main draft_helper.py for better modularity.

Author: Kai Mizuno
Last Updated: September 2025
"""

import logging
from typing import Dict, List, Optional, Any, Tuple, Set

try:
    from .. import draft_helper_constants as Constants
except ImportError:
    import draft_helper_constants as Constants


class TradeAnalyzer:
    """
    Manages trade analysis and optimization operations for the draft helper.
    """

    def __init__(self, team, logger: Optional[logging.Logger] = None):
        """
        Initialize the TradeAnalyzer.

        Args:
            team: FantasyTeam instance
            logger: Logger instance for debugging
        """
        self.team = team
        self.logger = logger or logging.getLogger(__name__)

    def run_trade_helper(self, available_players: List, score_player_for_trade_func):
        """
        Run the trade helper to optimize the current roster by finding beneficial trades.

        Args:
            available_players: List of available players for trading
            score_player_for_trade_func: Function to score players for trade evaluation
        """
        print("Welcome to the Start 7 Fantasy League Waiver Optimizer!")
        print(f"Current roster: {len(self.team.roster)} / {Constants.MAX_PLAYERS} players")
        print("Your current roster by position:")
        for pos, count in self.team.pos_counts.items():
            print(f"  {pos}: {count}")

        # Get available players for trades (drafted=0)
        available_for_trade = [p for p in available_players if p.drafted == 0 and p.locked == 0]
        print(f"\nAnalyzing {len(available_for_trade)} available players for potential trades...")

        # Calculate initial team score
        initial_score = self.team.get_total_team_score(score_player_for_trade_func)
        print(f"Initial team score: {initial_score:.2f}")

        # Perform iterative improvement
        trades_made, all_player_trades = self.optimize_roster_iteratively(available_for_trade, score_player_for_trade_func)

        # Final results
        final_score = self.team.get_total_team_score(score_player_for_trade_func)
        total_improvement = final_score - initial_score

        print(f"\n{'='*60}")
        print("TRADE OPTIMIZATION COMPLETE")
        print(f"{'='*60}")
        print(f"Initial team score: {initial_score:.2f}")
        print(f"Final team score: {final_score:.2f}")
        print(f"Total improvement: {total_improvement:+.2f}")
        print(f"Number of trades recommended: {len(trades_made)}")

        self.logger.info(f"Trade optimization complete. {len(trades_made)} trades recommended, "
                        f"total improvement: {total_improvement:+.2f}")

        return trades_made, all_player_trades

    def optimize_roster_iteratively(self, available_players: List, score_player_for_trade_func) -> Tuple[List[Dict], Optional[Dict]]:
        """
        Perform iterative improvement on the roster by finding the best possible trades.

        Args:
            available_players: List of available players for trading
            score_player_for_trade_func: Function to score players for trade evaluation

        Returns:
            Tuple of (trades_made, all_player_trades)
        """
        trades_made = []
        iteration = 0
        recent_trades = set()  # Track recent trades to prevent oscillation
        max_iterations = 100  # Safety limit to prevent infinite loops
        all_player_trades = None  # Store runner-up data from last iteration

        while iteration < max_iterations:
            iteration += 1
            self.logger.info(f"Trade optimization iteration {iteration}")

            # Find the best possible trade that hasn't been recently reversed, including runner-ups
            best_trade, current_all_player_trades = self.find_best_trade_with_runners_up(available_players, recent_trades, score_player_for_trade_func)

            if best_trade is None:
                self.logger.info(f"No beneficial trades found in iteration {iteration}. Optimization complete.")
                break

            # Store the runner-up data for this trade before executing it
            if best_trade['out'].id in current_all_player_trades:
                best_trade['runners_up'] = current_all_player_trades[best_trade['out'].id]

            # Execute the trade
            old_player = best_trade['out']
            new_player = best_trade['in']
            improvement = best_trade['improvement']

            self.logger.info(f"Executing trade: {old_player.name} -> {new_player.name} (+{improvement:.2f})")

            if self.team.replace_player(old_player, new_player):
                # Move players between available/roster lists
                available_players.append(old_player)
                available_players.remove(new_player)

                trades_made.append(best_trade)

                # Update all_player_trades with the latest data
                all_player_trades = current_all_player_trades

                # Track this trade to prevent immediate reversal
                trade_key = (old_player.id, new_player.id)
                reverse_key = (new_player.id, old_player.id)
                recent_trades.add(trade_key)

                # Also add the reverse to prevent oscillation
                recent_trades.add(reverse_key)

                # Keep only the last 20 trades in memory to prevent cycles
                if len(recent_trades) > 20:
                    recent_trades = set(list(recent_trades)[-20:])

                print(f"Trade {len(trades_made)}: {old_player.name} ({old_player.position}) -> "
                      f"{new_player.name} ({new_player.position}) (+{improvement:.2f} points)")
            else:
                self.logger.error(f"Failed to execute trade: {old_player.name} -> {new_player.name}")
                break

        if iteration >= max_iterations:
            print(f"Warning: Reached maximum iterations ({max_iterations}). Optimization stopped.")
            self.logger.warning(f"Trade optimization reached maximum iterations ({max_iterations})")

        return trades_made, all_player_trades

    def find_best_trade_with_runners_up(self, available_players: List, recent_trades: Set, score_player_for_trade_func) -> Tuple[Optional[Dict], Dict]:
        """
        Find the best possible trade from the current roster along with runner-up trades for each player.

        Args:
            available_players: List of available players for trading
            recent_trades: Set of recent trades to avoid oscillation
            score_player_for_trade_func: Function to score players for trade evaluation

        Returns:
            Tuple of (best_trade, all_player_trades)
        """
        if recent_trades is None:
            recent_trades = set()

        best_trade = None
        best_improvement = 0
        all_player_trades = {}  # Dictionary to store all potential trades by player being traded out

        # For each player on the roster (excluding locked players)
        for current_player in self.team.roster:
            if current_player.locked == 1:
                continue
            current_score = score_player_for_trade_func(current_player)

            # Find the best available replacement for this position
            same_position_players = [p for p in available_players
                                   if p.position == current_player.position]

            # Also consider FLEX-eligible swaps
            if current_player.position in Constants.FLEX_ELIGIBLE_POSITIONS:
                for other_pos in Constants.FLEX_ELIGIBLE_POSITIONS:
                    if other_pos != current_player.position:
                        flex_candidates = [p for p in available_players if p.position == other_pos]
                        same_position_players.extend(flex_candidates)

            # Collect all valid trades for this player
            player_trades = []

            # Evaluate each potential replacement
            for candidate in same_position_players:
                # Check if this trade was recently made (prevent oscillation)
                trade_key = (current_player.id, candidate.id)
                if trade_key in recent_trades:
                    continue

                # Check if this trade is valid
                if not self.team._can_replace_player(current_player, candidate):
                    continue

                candidate_score = score_player_for_trade_func(candidate)
                improvement = candidate_score - current_score

                # Only consider trades that meet the minimum improvement threshold
                if improvement >= Constants.MIN_TRADE_IMPROVEMENT:
                    trade = {
                        'out': current_player,
                        'in': candidate,
                        'improvement': improvement
                    }
                    player_trades.append(trade)

                    # Check if this is the best overall trade
                    if improvement > best_improvement:
                        best_improvement = improvement
                        best_trade = trade

            # Sort trades for this player by improvement (best first)
            player_trades.sort(key=lambda x: x['improvement'], reverse=True)
            all_player_trades[current_player.id] = player_trades

        return best_trade, all_player_trades

    def consolidate_trades(self, trades_made: List[Dict]) -> List[Dict]:
        """
        Consolidate trades to show only the net result (remove back-and-forth swaps).

        Args:
            trades_made: List of trades that were made

        Returns:
            Consolidated list of trades
        """
        if len(trades_made) <= 10:  # If few trades, show all
            return trades_made

        # For many trades, show only the first meaningful ones before oscillation starts
        consolidated = []
        seen_positions = set()

        for trade in trades_made:
            position_pair = (trade['out'].position, trade['in'].position)
            reverse_pair = (trade['in'].position, trade['out'].position)

            # Add trade if we haven't seen this position pair before
            if position_pair not in seen_positions and reverse_pair not in seen_positions:
                consolidated.append(trade)
                seen_positions.add(position_pair)

                # Stop after we have good trades from each position
                if len(consolidated) >= 8:  # Reasonable limit for meaningful trades
                    break

        return consolidated

    def run_trade_analysis_mode(self, add_basic_matchup_indicators_func, run_trade_helper_func, save_players_func):
        """
        Trade Analysis Mode - run trade helper to optimize current roster.

        Args:
            add_basic_matchup_indicators_func: Function to add matchup indicators
            run_trade_helper_func: Function to run the trade helper
            save_players_func: Function to save player data
        """
        print("\n" + "="*50)
        print("WAIVER OPTIMIZER MODE")
        print("="*50)

        # Check if we have a roster to analyze
        if len(self.team.roster) == 0:
            print("No players in roster to analyze for trades.")
            print("Add players to your roster first using 'Add to Roster' mode.")
            input("\nPress Enter to return to Main Menu...")
            return

        print("Analyzing your current roster for potential trades...")
        print(f"Current roster: {len(self.team.roster)} / {Constants.MAX_PLAYERS} players")

        # Save original player states before trade analysis
        original_player_states = {}
        original_roster = self.team.roster.copy()
        original_slot_assignments = {}
        for slot, player_ids in self.team.slot_assignments.items():
            original_slot_assignments[slot] = player_ids.copy()
        original_pos_counts = self.team.pos_counts.copy()

        for player in self.team.roster + [p for p in self.team.roster]:  # Include all players we might access
            original_player_states[player.id] = player.drafted

        try:
            # Add basic matchup indicators to players
            add_basic_matchup_indicators_func()

            # Run the trade helper analysis
            print("\nStarting trade analysis...")
            run_trade_helper_func()

            print("\nTrade analysis complete!")

        except Exception as e:
            print(f"Error during trade analysis: {e}")
            self.logger.error(f"Error in trade analysis mode: {e}")

        finally:
            # Restore original player states after analysis
            print("Restoring original player states...")
            for player_id, original_state in original_player_states.items():
                # Find the player by ID and restore state
                for player in self.team.roster + [p for p in self.team.roster]:
                    if hasattr(player, 'id') and player.id == player_id:
                        player.drafted = original_state
                        break

            # Restore original team state
            self.team.roster = original_roster
            self.team.slot_assignments = original_slot_assignments
            self.team.pos_counts = original_pos_counts

            self.logger.info("Player states restored after trade analysis")

        input("\nPress Enter to return to Main Menu...")