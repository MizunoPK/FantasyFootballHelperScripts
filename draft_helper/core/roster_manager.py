#!/usr/bin/env python3
"""
Roster Management Module for Draft Helper

This module handles all roster display and modification functionality,
extracted from the main draft_helper.py for better modularity.

Author: Kai Mizuno
Last Updated: September 2025
"""

import logging
from typing import Dict, List, Optional, Any

try:
    from .. import draft_helper_constants as Constants
except ImportError:
    import draft_helper_constants as Constants


class RosterManager:
    """
    Manages roster display and modification operations for the draft helper.
    """

    def __init__(self, team, logger: Optional[logging.Logger] = None):
        """
        Initialize the RosterManager.

        Args:
            team: FantasyTeam instance
            logger: Logger instance for debugging
        """
        self.team = team
        self.logger = logger or logging.getLogger(__name__)

    def _get_consistency_indicator(self, player):
        """
        Get consistency indicator text for display.

        Returns:
            str: Consistency indicator text or empty string
        """
        if hasattr(player, 'consistency_category') and player.consistency_category:
            consistency_map = {"LOW": " [Consistent]", "MEDIUM": " [Average]", "HIGH": " [Volatile]"}
            return consistency_map.get(player.consistency_category, "")
        return ""

    def display_roster_by_draft_order(self):
        """Display current roster organized by assigned slots in draft order"""
        print(f"\nCurrent Roster by Position:")
        print("-" * 40)

        # Create a map from player ID to player object for quick lookup
        player_map = {player.id: player for player in self.team.roster}

        # Display each position based on slot assignments (not original position)
        for pos in Constants.MAX_POSITIONS.keys():
            max_count = Constants.MAX_POSITIONS[pos]

            # Get players assigned to this slot (using slot_assignments, not position filtering)
            assigned_player_ids = self.team.slot_assignments.get(pos, [])
            assigned_players = [player_map[pid] for pid in assigned_player_ids if pid in player_map]
            current_count = len(assigned_players)

            print(f"\n{pos} ({current_count}/{max_count}):")
            if assigned_players:
                # Sort by fantasy points (highest first) for display
                sorted_players = sorted(assigned_players, key=lambda p: p.fantasy_points, reverse=True)
                for i, player in enumerate(sorted_players, 1):
                    locked_indicator = " (LOCKED)" if getattr(player, 'locked', False) else ""
                    print(f"  {pos}{i}: {player.name} ({player.team}) - {player.fantasy_points:.1f} pts{locked_indicator}")
            else:
                print(f"  (No {pos} players)")

        print(f"\nTotal roster: {len(self.team.roster)}/{Constants.MAX_PLAYERS} players")

    def display_roster_by_draft_rounds(self):
        """Display current roster organized by draft round order based on DRAFT_ORDER config"""
        print(f"\nCurrent Roster by Draft Round:")
        print("-" * 50)

        if not self.team.roster:
            print("No players in roster yet.")
            return

        # Match players to their optimal draft rounds
        round_assignments = self._match_players_to_rounds()

        for round_num in range(1, Constants.MAX_PLAYERS + 1):
            ideal_position = Constants.get_ideal_draft_position(round_num - 1)

            if round_num in round_assignments:
                player = round_assignments[round_num]
                position_match = "OK" if player.position == ideal_position else "!!"
                print(f"Round {round_num:2d} (Ideal: {ideal_position:4s}): {player.name} ({player.position}) - {player.fantasy_points:.1f} pts {position_match}")
            else:
                print(f"Round {round_num:2d} (Ideal: {ideal_position:4s}): [EMPTY SLOT]")

        print(f"\nRoster Status: {len(self.team.roster)}/{Constants.MAX_PLAYERS} players drafted")

    def _match_players_to_rounds(self) -> Dict[int, Any]:
        """
        Match current roster players to draft round slots using optimal fit strategy.
        Returns dictionary mapping round numbers to players.
        """
        round_assignments = {}  # round_num -> player
        available_players = list(self.team.roster)  # Copy of roster players

        # First pass: Assign players to rounds where their position perfectly matches the ideal
        for round_num in range(1, Constants.MAX_PLAYERS + 1):
            ideal_position = Constants.get_ideal_draft_position(round_num - 1)

            # Find best matching player for this round
            best_player = None
            best_score = -1

            for player in available_players:
                # Calculate fit score for this player in this round
                fit_score = self._calculate_round_fit_score(player, round_num, ideal_position)

                if fit_score > best_score:
                    best_score = fit_score
                    best_player = player

            # Assign best fitting player to this round
            if best_player and best_score > 0:
                round_assignments[round_num] = best_player
                available_players.remove(best_player)

        return round_assignments

    def _calculate_round_fit_score(self, player, round_num: int, ideal_position: str) -> float:
        """
        Calculate how well a player fits in a specific draft round.
        Returns higher scores for better fits.
        """
        base_score = player.fantasy_points  # Base score on player quality

        # Position match bonuses
        if player.position == ideal_position:
            # Perfect position match
            base_score += 1000
        elif ideal_position == "FLEX" and player.position in Constants.FLEX_ELIGIBLE_POSITIONS:
            # FLEX eligible
            base_score += 500
        elif player.position in Constants.FLEX_ELIGIBLE_POSITIONS and ideal_position in ["RB", "WR"]:
            # FLEX player could fit RB/WR slot
            base_score += 100
        else:
            # Position mismatch - still possible but heavily penalized
            base_score -= 500

        # Round number proximity bonus (prefer assigning high-value players to early rounds)
        proximity_bonus = (Constants.MAX_PLAYERS - round_num + 1) * 10
        base_score += proximity_bonus

        return base_score

    def run_add_to_roster_mode(self, recommend_next_picks_func, save_players_func):
        """
        Add to Roster Mode - shows recommendations and allows drafting to our team.

        Args:
            recommend_next_picks_func: Function to get draft recommendations
            save_players_func: Function to save player data
        """
        print("\n" + "="*50)
        print("ADD TO ROSTER MODE")
        print("="*50)

        # Show enhanced roster display by draft rounds
        self.display_roster_by_draft_rounds()

        while True:
            print("\nTop draft recommendations based on your current roster:")
            recommendations = recommend_next_picks_func()

            if not recommendations:
                print("No recommendations available (roster may be full or no available players).")
                print("Returning to Main Menu...")
                break

            for i, p in enumerate(recommendations, start=1):
                # Show calculated score (used for ranking) instead of raw fantasy points
                status = f" ({p.injury_status})" if p.injury_status != 'ACTIVE' else ""
                drafted_status = " [DRAFTED]" if p.drafted == 1 else ""
                score_display = getattr(p, 'score', p.fantasy_points)  # Use calculated score if available

                # Show consistency category if available
                consistency_indicator = self._get_consistency_indicator(p)

                print(f"{i}. {p.name} ({p.team} {p.position}) - {score_display:.1f} pts{consistency_indicator}{status}{drafted_status}")
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
                            print(f"\n✅ Successfully added {player_to_draft.name} to your roster!")
                            save_players_func()
                            self.logger.info(f"Player {player_to_draft.name} drafted to user's team (drafted=2)")

                            # Show updated roster
                            self.display_roster_by_draft_order()

                            print("Returning to Main Menu...")
                            break
                        else:
                            print(f"❌ Failed to add {player_to_draft.name}. Check roster limits.")
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

    def show_roster_comparison(self, trades_made: List[Dict], all_player_trades: Optional[Dict] = None, score_player_for_trade_func = None):
        """
        Display a clear comparison between original and final roster, including runner-up trades.

        Args:
            trades_made: List of trades that were made
            all_player_trades: Dictionary of all potential trades by player ID
            score_player_for_trade_func: Function to score players for trades
        """
        if not trades_made:
            print("\nNo beneficial trades found. Your roster is already optimized!")

            # Still show runner-up trades if available for current players
            if all_player_trades:
                self._show_current_roster_with_alternatives(all_player_trades, score_player_for_trade_func)
            else:
                print(f"\nCurrent roster:")
                for p in sorted(self.team.roster, key=lambda x: x.position):
                    if score_player_for_trade_func:
                        score = score_player_for_trade_func(p)
                        consistency_indicator = self._get_consistency_indicator(p)
                        print(f"  {p.name} ({p.position}) - {score:.2f} pts{consistency_indicator}")
                    else:
                        print(f"  {p.name} ({p.position}) - {p.fantasy_points:.1f} pts")
            return

        # Get original roster by reversing all trades (using player IDs for comparison)
        original_roster_ids = set(p.id for p in self.team.roster)
        players_out = []
        players_in = []

        # Reverse the trades to find original roster
        for trade in reversed(trades_made):
            # Remove players that were traded in
            if trade['in'].id in original_roster_ids:
                original_roster_ids.remove(trade['in'].id)
                players_in.append(trade['in'])

            # Add back players that were traded out
            original_roster_ids.add(trade['out'].id)
            players_out.append(trade['out'])

        # Remove duplicates while preserving order (last occurrence wins)
        seen_out = set()
        players_out_unique = []
        for p in reversed(players_out):
            if p.id not in seen_out:
                seen_out.add(p.id)
                players_out_unique.append(p)
        players_out_unique.reverse()

        seen_in = set()
        players_in_unique = []
        for p in reversed(players_in):
            if p.id not in seen_in:
                seen_in.add(p.id)
                players_in_unique.append(p)
        players_in_unique.reverse()

        # Current final roster
        final_roster_ids = set(p.id for p in self.team.roster)

        # Players that stayed (in both original and final)
        players_kept_ids = original_roster_ids.intersection(final_roster_ids)
        players_kept = [p for p in self.team.roster if p.id in players_kept_ids]

        print(f"\nROSTER ANALYSIS:")
        print("="*60)
        print(f"Players kept: {len(players_kept)}")
        print(f"Players traded out: {len(players_out_unique)}")
        print(f"Players traded in: {len(players_in_unique)}")

        # Show kept players first
        if players_kept:
            print(f"\n[KEPT] PLAYERS REMAINING ON ROSTER:")
            for p in sorted(players_kept, key=lambda x: x.position):
                if score_player_for_trade_func:
                    score = score_player_for_trade_func(p)
                    consistency_indicator = self._get_consistency_indicator(p)
                    print(f"  {p.name} ({p.position}) - {score:.2f} pts{consistency_indicator}")
                else:
                    print(f"  {p.name} ({p.position}) - {p.fantasy_points:.1f} pts")

        print(f"\n[TRADES] RECOMMENDED CHANGES ({len(trades_made)} trades):")
        for i, trade in enumerate(trades_made, 1):
            if score_player_for_trade_func:
                out_score = score_player_for_trade_func(trade['out'])
                in_score = score_player_for_trade_func(trade['in'])

                out_consistency = self._get_consistency_indicator(trade['out'])
                in_consistency = self._get_consistency_indicator(trade['in'])

                print(f"  {i}. OUT: {trade['out'].name} ({trade['out'].position}) - {out_score:.2f} pts{out_consistency}")
                print(f"     IN:  {trade['in'].name} ({trade['in'].position}) - {in_score:.2f} pts{in_consistency}")
                print(f"     Net Improvement: +{trade['improvement']:.2f} pts")
            else:
                print(f"  {i}. OUT: {trade['out'].name} ({trade['out'].position}) - {trade['out'].fantasy_points:.1f} pts")
                print(f"     IN:  {trade['in'].name} ({trade['in'].position}) - {trade['in'].fantasy_points:.1f} pts")
                print(f"     Net Improvement: +{trade['improvement']:.2f} pts")

            # Show runner-ups for this trade (use stored data from when trade was made)
            if 'runners_up' in trade:
                player_trades = trade['runners_up']
                # Find runner-ups (skip the main trade we just showed)
                runners_up = []
                for pt in player_trades:
                    if pt['in'].id != trade['in'].id:  # Skip the main trade
                        runners_up.append(pt)
                    if len(runners_up) >= Constants.NUM_TRADE_RUNNERS_UP:
                        break

                if runners_up:
                    for j, runner_up in enumerate(runners_up, 1):
                        if score_player_for_trade_func:
                            ru_score = score_player_for_trade_func(runner_up['in'])
                            ru_consistency = self._get_consistency_indicator(runner_up['in'])
                            print(f"        Runner-up {j}: {runner_up['in'].name} - {ru_score:.2f} pts{ru_consistency} ({runner_up['improvement']:+.2f})")
                        else:
                            print(f"        Runner-up {j}: {runner_up['in'].name} - {runner_up['in'].fantasy_points:.1f} pts ({runner_up['improvement']:+.2f})")
            print()

    def _show_current_roster_with_alternatives(self, all_player_trades: Dict, score_player_for_trade_func = None):
        """
        Show current roster with alternative trade options when no beneficial trades exist.
        """
        print(f"\nCurrent roster with potential alternatives:")
        print("-"*60)

        for p in sorted(self.team.roster, key=lambda x: x.position):
            if p.locked == 1:
                continue

            if score_player_for_trade_func:
                score = score_player_for_trade_func(p)
                consistency_indicator = self._get_consistency_indicator(p)
                print(f"  {p.name} ({p.position}) - {score:.2f} pts{consistency_indicator}")
            else:
                print(f"  {p.name} ({p.position}) - {p.fantasy_points:.1f} pts")

            # Show alternatives that don't meet the threshold
            if p.id in all_player_trades:
                player_trades = all_player_trades[p.id]
                alternatives = player_trades[:Constants.NUM_TRADE_RUNNERS_UP]

                if alternatives:
                    for j, alt in enumerate(alternatives, 1):
                        if score_player_for_trade_func:
                            alt_score = score_player_for_trade_func(alt['in'])
                            alt_consistency = self._get_consistency_indicator(alt['in'])
                            print(f"        Alternative {j}: {alt['in'].name} - {alt_score:.2f} pts{alt_consistency} ({alt['improvement']:+.2f})")
                        else:
                            print(f"        Alternative {j}: {alt['in'].name} - {alt['in'].fantasy_points:.1f} pts ({alt['improvement']:+.2f})")
            print()