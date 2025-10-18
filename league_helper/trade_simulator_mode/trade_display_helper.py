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
        # Print header with title
        print("=" * 25)
        print(title)
        print("=" * 25)

        # Display each player with sequential numbering (starting at 1)
        for i, player in enumerate(roster, 1):
            print(f"{i}. {player}")

        # Print footer separator
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
        # Print header
        print("\n" + "=" * 160)
        print("COMBINED ROSTER FOR TRADE")
        print("=" * 160)

        # Position display order (QB, RB, WR, TE, K, DST)
        position_order = ["QB", "RB", "WR", "TE", "K", "DST"]

        # ===== STEP 1: Organize and sort rosters by position =====
        # Create dictionaries to store players grouped by position
        # Within each position group, sort by score (highest first)
        my_by_position = {}
        their_by_position = {}

        for position in position_order:
            # Extract players at this position from MY roster
            my_position_players = [p for p in my_roster if p.position == position]
            # Sort descending by score (best players first)
            my_position_players.sort(key=lambda p: p.score, reverse=True)
            my_by_position[position] = my_position_players

            # Extract players at this position from THEIR roster
            their_position_players = [p for p in their_roster if p.position == position]
            # Sort descending by score (best players first)
            their_position_players.sort(key=lambda p: p.score, reverse=True)
            their_by_position[position] = their_position_players

        # ===== STEP 2: Initialize numbering and tracking =====
        # MY roster starts at number 1
        my_current_number = 1
        # Track display order for both rosters (needed for returning correct order)
        my_display_order = []
        their_display_order = []

        # Create uppercase column headers
        my_team_header = "MY TEAM"
        their_team_header = their_team_name.upper()

        # Print two-column header (78 chars per side with separator)
        print(f"\n{my_team_header:<78} | {their_team_header}")
        print("-" * 78 + "-+-" + "-" * 78)

        # ===== STEP 3: Calculate boundary index for THEIR roster =====
        # Their roster numbering starts AFTER all MY players
        # Example: If I have 14 players, their roster starts at index 15
        # This boundary is returned so caller can split player selections by team
        their_roster_start = 1
        for position in position_order:
            their_roster_start += len(my_by_position[position])

        # THEIR roster starts numbering at the calculated boundary
        their_current_number = their_roster_start

        # ===== STEP 4: Display each position group side-by-side =====
        # Process positions in order (QB, RB, WR, TE, K, DST)
        # Each position section shows MY players on left, THEIR players on right
        for position in position_order:
            my_players = my_by_position[position]
            their_players = their_by_position[position]

            # Print position header (e.g., "QB:", "RB:", etc.)
            print(f"\n{position}:")

            # Determine how many rows needed for this position
            # Use max of both teams' player counts (minimum 1 to show "(No players)" if both empty)
            max_rows = max(len(my_players), len(their_players), 1)

            # Display each row in this position group
            for i in range(max_rows):
                left_side = ""
                right_side = ""

                # Format LEFT side (my team)
                if i < len(my_players):
                    # Player exists at this index - display with number
                    player = my_players[i]
                    my_display_order.append(player)  # Track display order for return value
                    left_side = f"  {my_current_number}. {str(player)}"
                    my_current_number += 1  # Increment for next player
                elif i == 0:
                    # First row and no players - show placeholder
                    left_side = "  (No players)"
                # else: leave empty string for subsequent rows

                # Format RIGHT side (their team)
                if i < len(their_players):
                    # Player exists at this index - display with number
                    player = their_players[i]
                    their_display_order.append(player)  # Track display order for return value
                    right_side = f"  {their_current_number}. {str(player)}"
                    their_current_number += 1  # Increment for next player
                elif i == 0:
                    # First row and no players - show placeholder
                    right_side = "  (No players)"
                # else: leave empty string for subsequent rows

                # Print the row with left and right sides aligned
                # <78 pads left side to 78 characters for proper column alignment
                print(f"{left_side:<78} | {right_side}")

        # Print footer separator
        print("\n" + "=" * 160)

        # Return:
        # 1. Boundary index where their roster numbering starts (for input parsing)
        # 2. My roster in display order (for mapping indices to players)
        # 3. Their roster in display order (for mapping indices to players)
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
        # Calculate score improvements for both teams
        my_improvement = trade.my_new_team.team_score - original_my_score
        # Determine sign for display (+ for positive, - for negative)
        my_improvement_sign = "+" if my_improvement >= 0.0 else "-"

        their_improvement = trade.their_new_team.team_score - original_their_score
        their_improvement_sign = "+" if their_improvement >= 0.0 else "-"

        # Print header
        print("\n" + "=" * 80)
        print("MANUAL TRADE VISUALIZER - Trade Impact Analysis")
        print("=" * 80)

        # Display trade summary with score improvements
        print(f"Trade with {trade.their_new_team.name}")
        # Show improvement with sign and absolute value (handles negative improvements)
        print(f"  My improvement: {my_improvement_sign}{abs(my_improvement):.2f} pts (New score: {trade.my_new_team.team_score:.2f})")
        print(f"  Their improvement: {their_improvement_sign}{abs(their_improvement):.2f} pts (New score: {trade.their_new_team.team_score:.2f})")

        # Display players I'm giving away
        # Uses original scored players (scored in original team context before trade)
        # This shows the true value we're losing
        print(f"  I give:")
        for player in trade.my_original_players:
            print(f"    - {player}")  # ScoredPlayer.__str__() shows name, position, score, reasons

        # Display players I'm receiving
        # Uses new scored players (scored in new team context after trade)
        # This shows the value they bring to our new roster composition
        print(f"  I receive:")
        for player in trade.my_new_players:
            print(f"    - {player}")  # ScoredPlayer.__str__() shows name, position, score, reasons

        # Print footer separator
        print("=" * 80)
