#!/usr/bin/env python3
"""
Draft Helper Menu System

This module handles all menu display and user interaction functionality.

Author: Kai Mizuno
Last Updated: September 2025
"""

import sys
from pathlib import Path

# Add parent directories to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    from ..draft_helper_constants import (
        MAX_PLAYERS, MAX_POSITIONS, FLEX_ELIGIBLE_POSITIONS,
        get_ideal_draft_position
    )
    # Create a Constants-like object for backward compatibility
    class Constants:
        MAX_PLAYERS = MAX_PLAYERS
        MAX_POSITIONS = MAX_POSITIONS
        FLEX_ELIGIBLE_POSITIONS = FLEX_ELIGIBLE_POSITIONS
        get_ideal_draft_position = staticmethod(get_ideal_draft_position)
except ImportError:
    # Fallback to absolute imports when run directly
    from draft_helper_constants import (
        MAX_PLAYERS, MAX_POSITIONS, FLEX_ELIGIBLE_POSITIONS,
        get_ideal_draft_position
    )
    # Create a Constants-like object for backward compatibility
    class Constants:
        MAX_PLAYERS = MAX_PLAYERS
        MAX_POSITIONS = MAX_POSITIONS
        FLEX_ELIGIBLE_POSITIONS = FLEX_ELIGIBLE_POSITIONS
        get_ideal_draft_position = staticmethod(get_ideal_draft_position)


class MenuSystem:
    """Handles all menu display and user interaction for the draft helper"""

    def __init__(self, team, starter_helper_available=False, draft_helper=None):
        """
        Initialize the menu system

        Args:
            team: FantasyTeam object representing the user's team
            starter_helper_available: Whether starter helper functionality is available
            draft_helper: Reference to the DraftHelper instance for accessing helper methods
        """
        self.team = team
        self.starter_helper_available = starter_helper_available
        self.draft_helper = draft_helper

    def show_main_menu(self):
        """Display main menu and get user choice"""
        print("\n" + "="*50)
        print("MAIN MENU")
        print("="*50)
        print(f"Current roster: {len(self.team.roster)} / {Constants.MAX_PLAYERS} players")
        print("="*50)
        print("1. Add to Roster")
        print("2. Mark Drafted Player")
        print("3. Trade Analysis")
        print("4. Drop Player")
        print("5. Lock/Unlock Player")
        if self.starter_helper_available:
            print("6. Starter Helper")
            print("7. Quit")
            max_choice = 7
        else:
            print("6. Quit")
            max_choice = 6
        print("="*50)

        try:
            choice = int(input(f"Enter your choice (1-{max_choice}): ").strip())
            return choice
        except ValueError:
            return -1

    def display_roster_by_draft_order(self):
        """Display current roster organized by assigned slots in draft order"""
        print("\nCurrent Roster by Position:")
        print("-" * 40)

        # Get draft order positions
        draft_order_positions = ['QB', 'RB', 'WR', 'TE', 'FLEX', 'K', 'DST']

        # Create a map from player ID to player object for quick lookup
        player_map = {player.id: player for player in self.team.roster}

        # Display each position based on slot assignments
        for position in draft_order_positions:
            max_for_position = Constants.MAX_POSITIONS.get(position, 0)

            if max_for_position > 0:
                # Get players assigned to this slot
                assigned_player_ids = self.team.slot_assignments.get(position, [])
                assigned_players = [player_map[pid] for pid in assigned_player_ids if pid in player_map]

                print(f"{position} ({len(assigned_players)}/{max_for_position}):")

                if assigned_players:
                    for i, player in enumerate(assigned_players, 1):
                        position_label = f"{position}{i}"
                        points_str = f"{getattr(player, 'fantasy_points', 0):.1f} pts"
                        locked_indicator = " (LOCKED)" if getattr(player, 'locked', False) else ""
                        print(f"  {position_label}: {player.name} ({player.team}) - {points_str}{locked_indicator}")
                else:
                    print(f"  No players assigned to {position}")
                print()

        print(f"Total roster: {len(self.team.roster)}/{Constants.MAX_PLAYERS} players")

    def display_roster_by_draft_rounds(self):
        """Display current roster organized by draft rounds with position matching"""
        print("\nCurrent Roster by Draft Round:")
        print("=" * 50)

        if self.draft_helper:
            # Use the draft helper's method to get round assignments
            round_assignments = self.draft_helper._match_players_to_rounds()

            # Display each round
            for round_num in range(1, Constants.MAX_PLAYERS + 1):
                # Get ideal position for this round (0-indexed for DRAFT_ORDER)
                ideal_position = Constants.get_ideal_draft_position(round_num - 1)

                # Get assigned player for this round
                assigned_player = round_assignments.get(round_num)

                if assigned_player:
                    # Player assigned - show with position match indicator
                    position_match = "OK" if assigned_player.position == ideal_position or \
                                   (ideal_position == "FLEX" and assigned_player.position in Constants.FLEX_ELIGIBLE_POSITIONS) \
                                   else "!!"

                    print(f"Round {round_num:2d} (Ideal: {ideal_position:4s}): {assigned_player.name:20s} "
                          f"({assigned_player.position}) - {assigned_player.fantasy_points:6.1f} pts {position_match}")
                else:
                    # No player assigned
                    print(f"Round {round_num:2d} (Ideal: {ideal_position:4s}): {'[Empty]':20s}")

            print("\nLegend: OK = Matches ideal position, !! = Different from ideal")
            print(f"Total: {len([p for p in round_assignments.values() if p])}/{Constants.MAX_PLAYERS} rounds filled")
        else:
            print("Draft helper not available for advanced display.")

    def display_starter_lineup(self, optimal_lineup):
        """Display optimal starting lineup"""
        print("\n" + "="*60)
        print("OPTIMAL STARTING LINEUP")
        print("="*60)

        if not optimal_lineup:
            print("No optimal lineup available.")
            return

        position_order = ['qb', 'rb1', 'rb2', 'wr1', 'wr2', 'te', 'flex', 'k', 'dst']

        for pos_key in position_order:
            recommendation = getattr(optimal_lineup, pos_key, None)
            if recommendation:
                matchup_indicator = getattr(recommendation, 'matchup_indicator', '')
                matchup_display = f" {matchup_indicator}" if matchup_indicator else ""

                print(f"{pos_key.upper():>4}: {recommendation.name} ({recommendation.team})")
                print(f"      {recommendation.projected_points:.1f} pts{matchup_display}")
                if recommendation.reason and recommendation.reason != "No penalties":
                    print(f"      {recommendation.reason}")
                print()

        total_points = getattr(optimal_lineup, 'total_projected_points', 0)
        print(f"Total Projected Points: {total_points:.1f}")
        print("="*60)

    def display_bench_alternatives(self, bench_recommendations):
        """Display bench alternatives"""
        if not bench_recommendations:
            print("\nNo bench alternatives available.")
            return

        print("\n" + "="*50)
        print("TOP BENCH ALTERNATIVES")
        print("="*50)

        for i, recommendation in enumerate(bench_recommendations, 1):
            matchup_indicator = getattr(recommendation, 'matchup_indicator', '')
            matchup_display = f" {matchup_indicator}" if matchup_indicator else ""

            print(f"{i}. {recommendation.name} ({recommendation.position} - {recommendation.team})")
            print(f"   {recommendation.projected_points:.1f} pts{matchup_display}")
            if recommendation.reason and recommendation.reason != "No penalties":
                print(f"   {recommendation.reason}")
            print()