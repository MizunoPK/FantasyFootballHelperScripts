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
        # Generate timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Sanitize opponent name (replace spaces with underscores)
        sanitized_name = opponent_name.replace(" ", "_")

        # Create filename
        filename = f"./league_helper/trade_simulator_mode/trade_outputs/trade_info_{sanitized_name}_{timestamp}.txt"

        # Calculate improvements
        my_improvement = trade.my_new_team.team_score - original_my_score
        my_improvement_sign = "+" if my_improvement >= 0.0 else "-"
        their_improvement = trade.their_new_team.team_score - original_their_score
        their_improvement_sign = "+" if their_improvement >= 0.0 else "-"

        # Write to file
        with open(filename, 'w') as file:
            file.write(f"Trade with {opponent_name}\n")
            file.write(f"  My improvement: {my_improvement_sign}{abs(my_improvement):.2f} pts (New score: {trade.my_new_team.team_score:.2f})\n")
            file.write(f"  Their improvement: {their_improvement_sign}{abs(their_improvement):.2f} pts (New score: {trade.their_new_team.team_score:.2f})\n")
            file.write(f"  I give:\n")
            # Show original scored players (from original roster context)
            for player in trade.my_original_players:
                file.write(f"    - {player}\n")
            file.write(f"  I receive:\n")
            for player in trade.my_new_players:
                file.write(f"    - {player}\n")

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
        # Generate timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Create filename with timestamp
        filename = f'./league_helper/trade_simulator_mode/trade_outputs/trade_info_{timestamp}.txt'

        # Open the file in write mode (it will create the file if it doesn't exist)
        with open(filename, 'w') as file:
            for i, trade in enumerate(sorted_trades, 1):
                my_improvement = trade.my_new_team.team_score - my_team.team_score

                # Get the original team score for comparison
                original_their_team = None
                for opp in opponent_simulated_teams:
                    if opp.name == trade.their_new_team.name:
                        original_their_team = opp
                        break

                their_improvement = trade.their_new_team.team_score - original_their_team.team_score if original_their_team else 0

                file.write(f"#{i} - Trade with {trade.their_new_team.name}\n")
                file.write(f"  My improvement: +{my_improvement:.2f} pts (New score: {trade.my_new_team.team_score:.2f})\n")
                file.write(f"  Their improvement: +{their_improvement:.2f} pts (New score: {trade.their_new_team.team_score:.2f})\n")
                file.write(f"  I give:\n")

                # Show original scored players (from original roster context)
                for player in trade.my_original_players:
                    file.write(f"    - {player}\n")

                file.write(f"  I receive:\n")
                for player in trade.my_new_players:
                    file.write(f"    - {player}\n")

                file.write("\n")  # Adds a blank line between trades

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
        # Generate timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Create filename with timestamp
        filename = f'./league_helper/trade_simulator_mode/trade_outputs/waiver_info_{timestamp}.txt'

        # Open the file in write mode (it will create the file if it doesn't exist)
        with open(filename, 'w') as file:
            for i, trade in enumerate(sorted_trades, 1):
                improvement = trade.my_new_team.team_score - my_team.team_score
                num_players = len(trade.my_new_players)
                trade_type = f"{num_players}-for-{num_players}"

                file.write(f"#{i} - {trade_type} Trade - Improvement: +{improvement:.2f} pts\n")
                file.write(f"  DROP:\n")

                # Show original scored players (from original roster context)
                for drop_player in trade.my_original_players:
                    file.write(f"    - {drop_player}\n")

                file.write(f"  ADD:\n")
                for add_player in trade.my_new_players:
                    file.write(f"    - {add_player}\n")

                file.write(f"  New team score: {trade.my_new_team.team_score:.2f}\n")
                file.write("\n")  # Adds a blank line between trades

        self.logger.info(f"Waiver pickups saved to {filename}")
