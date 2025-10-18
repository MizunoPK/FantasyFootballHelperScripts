"""
Trade Display Helper

Helper class for displaying trade-related information in Trade Simulator Mode.
Handles formatting and display of rosters, trades, and trade impact analysis.

Author: Kai Mizuno
"""

from typing import List, Tuple

import sys
from pathlib import Path

# Add parent directory to path for utils imports
sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.FantasyPlayer import FantasyPlayer

sys.path.append(str(Path(__file__).parent))
from trade_simulator_mode.TradeSnapshot import TradeSnapshot


class TradeDisplayHelper:
    """
    Helper class for displaying trade-related information.

    Provides methods for:
    - Displaying numbered rosters
    - Displaying combined rosters side-by-side
    - Displaying trade impact analysis
    """

    @staticmethod
    def display_numbered_roster(roster: List[FantasyPlayer], title: str) -> None:
        """
        Display a roster with numbered list format.

        Args:
            roster (List[FantasyPlayer]): List of players to display
            title (str): Title to display above the roster

        Output format:
            =========================
            {title}
            =========================
            1. {player.__str__()}
            2. {player.__str__()}
            ...
            =========================
        """
        print("=" * 25)
        print(title)
        print("=" * 25)
        for i, player in enumerate(roster, 1):
            print(f"{i}. {player}")
        print("=" * 25)

    @staticmethod
    def display_combined_roster(my_roster: List[FantasyPlayer], their_roster: List[FantasyPlayer], their_team_name: str) -> Tuple[int, List[FantasyPlayer], List[FantasyPlayer]]:
        """
        Display combined roster of both teams side-by-side organized by position and score.

        Players are numbered sequentially starting from 1 for my roster,
        continuing with their roster. Within each position group, players
        are sorted by descending score.

        Args:
            my_roster (List[FantasyPlayer]): My team's roster
            their_roster (List[FantasyPlayer]): Opponent team's roster
            their_team_name (str): Name of opponent team

        Returns:
            Tuple containing:
                - int: The boundary index where their roster numbering starts (1-based)
                - List[FantasyPlayer]: My roster in display order
                - List[FantasyPlayer]: Their roster in display order

        Output format: Side-by-side table with MY TEAM on left, THEIR TEAM on right
        """
        print("\n" + "=" * 160)
        print("COMBINED ROSTER FOR TRADE")
        print("=" * 160)

        # Position order as specified
        position_order = ["QB", "RB", "WR", "TE", "K", "DST"]

        # Organize both rosters by position
        my_by_position = {}
        their_by_position = {}

        for position in position_order:
            # Get and sort my players
            my_position_players = [p for p in my_roster if p.position == position]
            my_position_players.sort(key=lambda p: p.score, reverse=True)
            my_by_position[position] = my_position_players

            # Get and sort their players
            their_position_players = [p for p in their_roster if p.position == position]
            their_position_players.sort(key=lambda p: p.score, reverse=True)
            their_by_position[position] = their_position_players

        # Track display orders and numbers
        my_current_number = 1
        my_display_order = []
        their_display_order = []

        # Create column headers
        my_team_header = "MY TEAM"
        their_team_header = their_team_name.upper()

        print(f"\n{my_team_header:<78} | {their_team_header}")
        print("-" * 78 + "-+-" + "-" * 78)

        # Store boundary before processing their team
        their_roster_start = 1
        for position in position_order:
            their_roster_start += len(my_by_position[position])

        their_current_number = their_roster_start

        # Display each position group side by side
        for position in position_order:
            my_players = my_by_position[position]
            their_players = their_by_position[position]

            # Print position header
            print(f"\n{position}:")

            # Determine max rows needed for this position
            max_rows = max(len(my_players), len(their_players), 1)

            for i in range(max_rows):
                left_side = ""
                right_side = ""

                # Format left side (my team)
                if i < len(my_players):
                    player = my_players[i]
                    my_display_order.append(player)
                    left_side = f"  {my_current_number}. {str(player)}"
                    my_current_number += 1
                elif i == 0:
                    left_side = "  (No players)"

                # Format right side (their team)
                if i < len(their_players):
                    player = their_players[i]
                    their_display_order.append(player)
                    right_side = f"  {their_current_number}. {str(player)}"
                    their_current_number += 1
                elif i == 0:
                    right_side = "  (No players)"

                # Print the row with proper spacing
                print(f"{left_side:<78} | {right_side}")

        print("\n" + "=" * 160)

        return their_roster_start, my_display_order, their_display_order

    @staticmethod
    def display_trade_result(trade: TradeSnapshot, original_my_score: float, original_their_score: float) -> None:
        """
        Display trade impact analysis.

        Args:
            trade (TradeSnapshot): The trade to display
            original_my_score (float): Original score of my team
            original_their_score (float): Original score of their team

        Output format:
            ================================================================================
            MANUAL TRADE VISUALIZER - Trade Impact Analysis
            ================================================================================
            Trade with {opponent_name}
              My improvement: +X.XX pts (New score: Y.YY)
              Their improvement: +X.XX pts (New score: Y.YY)
              I give:
                - Player Name (POS) - TEAM
              I receive:
                - Player Name (POS) - TEAM
            ================================================================================
        """
        my_improvement = trade.my_new_team.team_score - original_my_score
        my_improvement_sign = "+" if my_improvement >= 0.0 else "-"
        their_improvement = trade.their_new_team.team_score - original_their_score
        their_improvement_sign = "+" if their_improvement >= 0.0 else "-"

        print("\n" + "=" * 80)
        print("MANUAL TRADE VISUALIZER - Trade Impact Analysis")
        print("=" * 80)
        print(f"Trade with {trade.their_new_team.name}")
        print(f"  My improvement: {my_improvement_sign}{abs(my_improvement):.2f} pts (New score: {trade.my_new_team.team_score:.2f})")
        print(f"  Their improvement: {their_improvement_sign}{abs(their_improvement):.2f} pts (New score: {trade.their_new_team.team_score:.2f})")
        print(f"  I give:")
        # Show original scored players (from original roster context)
        for player in trade.my_original_players:
            print(f"    - {player}")
        print(f"  I receive:")
        for player in trade.my_new_players:
            print(f"    - {player}")
        print("=" * 80)
