"""
Trade File Writer

Helper class for saving trade analysis results to files in Trade Simulator Mode.
Handles file I/O operations for different trade modes (manual, suggestor, waiver).

Author: Kai Mizuno
"""

from typing import List
from datetime import datetime

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.LoggingManager import get_logger

sys.path.append(str(Path(__file__).parent))
from trade_simulator_mode.TradeSnapshot import TradeSnapshot
from trade_simulator_mode.TradeSimTeam import TradeSimTeam


class TradeFileWriter:
    """
    Helper class for saving trade results to files.

    Provides methods for:
    - Saving manual trade results
    - Saving trade suggestor results
    - Saving waiver optimizer results
    """

    def __init__(self) -> None:
        """Initialize TradeFileWriter."""
        self.logger = get_logger()

    def save_manual_trade_to_file(self, trade: TradeSnapshot, opponent_name: str, original_my_score: float, original_their_score: float) -> str:
        """
        Save trade results to timestamped file.

        Args:
            trade (TradeSnapshot): The trade to save
            opponent_name (str): Name of opponent team
            original_my_score (float): Original score of my team
            original_their_score (float): Original score of their team

        Returns:
            str: Path to the created file

        File format:
            Trade with {opponent_name}
              My improvement: +X.XX pts (New score: Y.YY)
              Their improvement: +X.XX pts (New score: Y.YY)
              I give:
                - Player Name (POS) - TEAM
              I receive:
                - Player Name (POS) - TEAM
        """
        # STEP 1: Generate unique timestamp for filename (YYYYMMDD_HHMMSS format)
        # Ensures each file has a unique name and is easily sortable by time
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # STEP 2: Sanitize opponent name for filesystem compatibility
        # Replace spaces with underscores (e.g., "Team Name" → "Team_Name")
        sanitized_name = opponent_name.replace(" ", "_")

        # STEP 3: Construct filename with opponent name and timestamp
        # Example: trade_info_Team_Name_20251017_143022.txt
        filename = f"./league_helper/trade_simulator_mode/trade_outputs/trade_info_{sanitized_name}_{timestamp}.txt"

        # STEP 4: Calculate score improvements for both teams
        my_improvement = trade.my_new_team.team_score - original_my_score
        # Determine sign for display (+ for gains, - for losses)
        my_improvement_sign = "+" if my_improvement >= 0.0 else "-"
        their_improvement = trade.their_new_team.team_score - original_their_score
        their_improvement_sign = "+" if their_improvement >= 0.0 else "-"

        # STEP 5: Write trade details to file
        with open(filename, 'w') as file:
            # Write header with opponent name
            file.write(f"Trade with {opponent_name}\n")
            # Write score improvements with absolute values (sign already included)
            file.write(f"  My improvement: {my_improvement_sign}{abs(my_improvement):.2f} pts (New score: {trade.my_new_team.team_score:.2f})\n")
            file.write(f"  Their improvement: {their_improvement_sign}{abs(their_improvement):.2f} pts (New score: {trade.their_new_team.team_score:.2f})\n")

            # Write players I'm giving up (original scores from old roster context)
            file.write(f"  I give:\n")
            for player in trade.my_original_players:
                file.write(f"    - {player}\n")  # ScoredPlayer.__str__() includes score details

            # Write players I'm receiving (new scores from new roster context)
            file.write(f"  I receive:\n")
            for player in trade.my_new_players:
                file.write(f"    - {player}\n")  # ScoredPlayer.__str__() includes score details

            # Write waiver recommendations if trade loses roster spots
            # These are automatically suggested pickups to fill empty roster spots
            if trade.waiver_recommendations:
                file.write(f"  Recommended Waiver Adds (for me):\n")
                for player in trade.waiver_recommendations:
                    file.write(f"    - {player}\n")

            # Write opponent waiver recommendations (if applicable)
            if trade.their_waiver_recommendations:
                file.write(f"  Recommended Waiver Adds (for {opponent_name}):\n")
                for player in trade.their_waiver_recommendations:
                    file.write(f"    - {player}\n")

            # Write players I must drop (beyond the trade itself)
            # Required when receiving more players than giving away violates MAX_PLAYERS
            if trade.my_dropped_players:
                file.write(f"  Players I Must Drop (to make room):\n")
                for player in trade.my_dropped_players:
                    file.write(f"    - {player}\n")

            # Write opponent dropped players (if applicable)
            if trade.their_dropped_players:
                file.write(f"  Players {opponent_name} Must Drop (to make room):\n")
                for player in trade.their_dropped_players:
                    file.write(f"    - {player}\n")

        # Return filename so caller can display success message
        return filename

    def save_trades_to_file(self, sorted_trades: List[TradeSnapshot], my_team: TradeSimTeam, opponent_simulated_teams: List[TradeSimTeam]) -> None:
        """
        Save trade suggestions to timestamped file (for Trade Suggestor mode).

        Args:
            sorted_trades (List[TradeSnapshot]): List of trade snapshots to save
            my_team (TradeSimTeam): The user's team
            opponent_simulated_teams (List[TradeSimTeam]): List of opponent teams

        File naming: trade_info_{timestamp}.txt (format: YYYY-MM-DD_HH-MM-SS)
        Location: ./league_helper/trade_simulator_mode/trade_outputs/
        """
        # Generate unique timestamp for filename (YYYY-MM-DD_HH-MM-SS format)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Construct filename (no opponent name - this file contains trades with ALL opponents)
        filename = f'./league_helper/trade_simulator_mode/trade_outputs/trade_info_{timestamp}.txt'

        # Write all trade suggestions to file
        with open(filename, 'w') as file:
            # Process each trade in ranked order (best first)
            for i, trade in enumerate(sorted_trades, 1):
                # Calculate MY improvement (compare new score vs original my_team score)
                my_improvement = trade.my_new_team.team_score - my_team.team_score

                # Look up ORIGINAL opponent team score for comparison
                # TradeSnapshot has NEW team scores, but we need original for improvement calculation
                original_their_team = None
                for opp in opponent_simulated_teams:
                    if opp.name == trade.their_new_team.name:
                        original_their_team = opp
                        break

                # Calculate THEIR improvement (or 0 if opponent team not found)
                their_improvement = trade.their_new_team.team_score - original_their_team.team_score if original_their_team else 0

                # Write trade header with rank number
                file.write(f"#{i} - Trade with {trade.their_new_team.name}\n")
                # Note: Assumes positive improvements (trades are pre-filtered to be mutually beneficial)
                file.write(f"  My improvement: +{my_improvement:.2f} pts (New score: {trade.my_new_team.team_score:.2f})\n")
                file.write(f"  Their improvement: +{their_improvement:.2f} pts (New score: {trade.their_new_team.team_score:.2f})\n")

                # Write players I give (original scores from old roster context)
                file.write(f"  I give:\n")
                for player in trade.my_original_players:
                    file.write(f"    - {player}\n")

                # Write players I receive (new scores from new roster context)
                file.write(f"  I receive:\n")
                for player in trade.my_new_players:
                    file.write(f"    - {player}\n")

                # Write waiver recommendations if trade loses roster spots
                # These are automatically suggested pickups to fill empty roster spots
                if trade.waiver_recommendations:
                    file.write(f"  Recommended Waiver Adds (for me):\n")
                    for player in trade.waiver_recommendations:
                        file.write(f"    - {player}\n")

                # Write opponent waiver recommendations (if applicable)
                if trade.their_waiver_recommendations:
                    file.write(f"  Recommended Waiver Adds (for {trade.their_new_team.name}):\n")
                    for player in trade.their_waiver_recommendations:
                        file.write(f"    - {player}\n")

                # Write players I must drop (beyond the trade itself)
                # Required when receiving more players than giving away violates MAX_PLAYERS
                if trade.my_dropped_players:
                    file.write(f"  Players I Must Drop (to make room):\n")
                    for player in trade.my_dropped_players:
                        file.write(f"    - {player}\n")

                # Write opponent dropped players (if applicable)
                if trade.their_dropped_players:
                    file.write(f"  Players {trade.their_new_team.name} Must Drop (to make room):\n")
                    for player in trade.their_dropped_players:
                        file.write(f"    - {player}\n")

                # Add blank line separator between trades for readability
                file.write("\n")

        # Log success message
        self.logger.info(f"Trades saved to {filename}")

    def save_waiver_trades_to_file(self, sorted_trades: List[TradeSnapshot], my_team: TradeSimTeam) -> None:
        """
        Save waiver pickup suggestions to timestamped file (for Waiver Optimizer mode).

        Args:
            sorted_trades (List[TradeSnapshot]): List of trade snapshots to save
            my_team (TradeSimTeam): The user's team

        File naming: waiver_info_{timestamp}.txt (format: YYYY-MM-DD_HH-MM-SS)
        Location: ./league_helper/trade_simulator_mode/trade_outputs/
        """
        # Generate unique timestamp for filename (YYYY-MM-DD_HH-MM-SS format)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Construct filename (waiver_info prefix differentiates from trade files)
        filename = f'./league_helper/trade_simulator_mode/trade_outputs/waiver_info_{timestamp}.txt'

        # Write all waiver pickup suggestions to file
        with open(filename, 'w') as file:
            # Process each waiver pickup in ranked order (best first)
            for i, trade in enumerate(sorted_trades, 1):
                # Calculate score improvement
                improvement = trade.my_new_team.team_score - my_team.team_score

                # Determine trade type label (1-for-1, 2-for-2, 3-for-3)
                # All waivers are balanced (same number dropped as added)
                num_players = len(trade.my_new_players)
                trade_type = f"{num_players}-for-{num_players}"

                # Write trade header with rank, type, and improvement
                file.write(f"#{i} - {trade_type} Trade - Improvement: +{improvement:.2f} pts\n")

                # Write players to DROP from roster (original scores from old roster context)
                file.write(f"  DROP:\n")
                for drop_player in trade.my_original_players:
                    file.write(f"    - {drop_player}\n")

                # Write players to ADD from waivers (new scores from new roster context)
                file.write(f"  ADD:\n")
                for add_player in trade.my_new_players:
                    file.write(f"    - {add_player}\n")

                # Write new total team score after waiver moves
                file.write(f"  New team score: {trade.my_new_team.team_score:.2f}\n")

                # Write additional waiver recommendations if trade loses roster spots
                # These are automatically suggested pickups to fill empty roster spots
                # (Note: Regular waiver mode usually has balanced trades, but unequal trades may generate these)
                if trade.waiver_recommendations:
                    file.write(f"  Additional Waiver Recommendations:\n")
                    for player in trade.waiver_recommendations:
                        file.write(f"    - {player}\n")

                # Write additional dropped players if needed
                # Required when receiving more players than giving away violates MAX_PLAYERS
                if trade.my_dropped_players:
                    file.write(f"  Additional Players to Drop (to make room):\n")
                    for player in trade.my_dropped_players:
                        file.write(f"    - {player}\n")

                # Add blank line separator between pickups for readability
                file.write("\n")

        # Log success message
        self.logger.info(f"Waiver pickups saved to {filename}")
