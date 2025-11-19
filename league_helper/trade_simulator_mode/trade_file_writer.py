"""
Trade File Writer

Helper class for saving trade analysis results to files in Trade Simulator Mode.
Handles file I/O operations for different trade modes (manual, suggestor, waiver).

Author: Kai Mizuno
"""

from typing import List, Dict, Optional, Any
from datetime import datetime
import re

import sys
from pathlib import Path
import pandas as pd

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

    def save_manual_trade_to_excel(
        self,
        trade: TradeSnapshot,
        opponent_name: str,
        original_my_score: float,
        original_their_score: float,
        my_original_team: TradeSimTeam,
        their_original_team: TradeSimTeam
    ) -> str:
        """
        Save trade results to Excel file with detailed analysis.

        Creates Excel workbook with 4 sheets:
        - Summary: Trade overview with score improvements
        - Initial Rosters: Side-by-side comparison of pre-trade rosters
        - Final Rosters: Side-by-side comparison of post-trade rosters with status markers
        - Detailed Calculations: Scoring breakdown for all players

        Args:
            trade (TradeSnapshot): The trade to save
            opponent_name (str): Name of opponent team
            original_my_score (float): Original score of my team
            original_their_score (float): Original score of their team
            my_original_team (TradeSimTeam): My team before trade (for scored players)
            their_original_team (TradeSimTeam): Their team before trade (for scored players)

        Returns:
            str: Path to the created Excel file

        Raises:
            Exception: If Excel file creation fails
        """
        try:
            self.logger.info(f"Creating Excel export for trade with {opponent_name}")

            # STEP 1: Generate unique timestamp and filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            sanitized_name = opponent_name.replace(" ", "_")
            filename = f"./league_helper/trade_simulator_mode/trade_outputs/trade_info_{sanitized_name}_{timestamp}.xlsx"

            # STEP 2: Calculate score improvements
            my_improvement = trade.my_new_team.team_score - original_my_score
            their_improvement = trade.their_new_team.team_score - original_their_score

            # STEP 3: Create Excel writer
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # Sheet 1: Summary
                self._create_summary_sheet(
                    writer, trade, opponent_name,
                    my_improvement, their_improvement
                )

                # Sheet 2: Trade Impact Analysis (NEW - IDEA 1)
                self._create_trade_impact_analysis_sheet(
                    writer, trade, my_original_team, their_original_team,
                    opponent_name, original_my_score, original_their_score
                )

                # Sheet 3: Initial Rosters
                self._create_initial_rosters_sheet(
                    writer, my_original_team, their_original_team, opponent_name
                )

                # Sheet 4: Final Rosters
                self._create_final_rosters_sheet(
                    writer, trade, opponent_name
                )

                # Sheet 5: Detailed Calculations
                self._create_detailed_calculations_sheet(
                    writer, trade, my_original_team, their_original_team, opponent_name
                )

            self.logger.info(f"Excel file created: {filename}")
            return filename

        except Exception as e:
            self.logger.error(f"Failed to create Excel file: {e}", exc_info=True)
            raise

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

    def save_waiver_trades_to_file(self, sorted_trades: List[TradeSnapshot], my_team: TradeSimTeam, mode: str = "Rest of Season") -> None:
        """
        Save waiver pickup suggestions to timestamped file (for Waiver Optimizer mode).

        Args:
            sorted_trades (List[TradeSnapshot]): List of trade snapshots to save
            my_team (TradeSimTeam): The user's team
            mode (str): Scoring mode used ("Rest of Season" or "Current Week")

        File naming: waiver_{mode_suffix}_{timestamp}.txt (format: YYYY-MM-DD_HH-MM-SS)
        Location: ./league_helper/trade_simulator_mode/trade_outputs/
        """
        # Generate unique timestamp for filename (YYYY-MM-DD_HH-MM-SS format)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Determine mode suffix for filename (Q4: include mode in filename)
        mode_suffix = "weekly" if mode == "Current Week" else "ros"

        # Construct filename with mode suffix
        filename = f'./league_helper/trade_simulator_mode/trade_outputs/waiver_{mode_suffix}_{timestamp}.txt'

        # Write all waiver pickup suggestions to file
        with open(filename, 'w') as file:
            # Write header with mode (Q3: minimal display - show mode name only)
            file.write("=" * 80 + "\n")
            file.write(f"WAIVER OPTIMIZER - {mode.upper()}\n")
            file.write("=" * 80 + "\n\n")
            # Process each waiver pickup in ranked order (best first)
            for i, trade in enumerate(sorted_trades, 1):
                # Calculate score improvement
                improvement = trade.my_new_team.team_score - my_team.team_score

                # Determine trade type label (1-for-1, 2-for-2, 3-for-3)
                # All waivers are balanced (same number dropped as added)
                num_players = len(trade.my_new_players)
                trade_type = f"{num_players}-for-{num_players}"

                # Write trade header with rank, type, and improvement (dynamic sign)
                sign = "+" if improvement >= 0 else ""
                file.write(f"#{i} - {trade_type} Trade - Improvement: {sign}{improvement:.2f} pts\n")

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

    # ===== EXCEL EXPORT HELPER METHODS =====

    def _create_summary_sheet(
        self,
        writer: pd.ExcelWriter,
        trade: TradeSnapshot,
        opponent_name: str,
        my_improvement: float,
        their_improvement: float
    ) -> None:
        """Create Summary sheet with trade overview."""
        # Build summary data
        summary_data = []

        # Row 1: Trade participants
        summary_data.append({"Category": "Trade Participants", "Details": f"My Team vs {opponent_name}"})
        summary_data.append({"Category": "", "Details": ""})  # Blank row

        # Row 2: My improvement
        my_sign = "+" if my_improvement >= 0 else ""
        summary_data.append({
            "Category": "My Improvement",
            "Details": f"{my_sign}{my_improvement:.2f} pts (New score: {trade.my_new_team.team_score:.2f})"
        })

        # Row 3: Their improvement
        their_sign = "+" if their_improvement >= 0 else ""
        summary_data.append({
            "Category": "Their Improvement",
            "Details": f"{their_sign}{their_improvement:.2f} pts (New score: {trade.their_new_team.team_score:.2f})"
        })
        summary_data.append({"Category": "", "Details": ""})  # Blank row

        # Players I give
        summary_data.append({"Category": "I Give", "Details": ""})
        for player in trade.my_original_players:
            summary_data.append({
                "Category": "",
                "Details": f"{player.player.name} ({player.player.position}) - {player.player.team} - {player.score:.2f} pts"
            })
        summary_data.append({"Category": "", "Details": ""})  # Blank row

        # Players I receive
        summary_data.append({"Category": "I Receive", "Details": ""})
        for player in trade.my_new_players:
            summary_data.append({
                "Category": "",
                "Details": f"{player.player.name} ({player.player.position}) - {player.player.team} - {player.score:.2f} pts"
            })

        # Create DataFrame and write to Excel
        df = pd.DataFrame(summary_data)
        df.to_excel(writer, sheet_name="Summary", index=False)

        # Apply formatting
        self._apply_sheet_formatting(writer.sheets["Summary"], df, "Summary")
        self.logger.info("Created Summary sheet")

    def _create_initial_rosters_sheet(
        self,
        writer: pd.ExcelWriter,
        my_original_team: TradeSimTeam,
        their_original_team: TradeSimTeam,
        opponent_name: str
    ) -> None:
        """Create Initial Rosters sheet with side-by-side pre-trade rosters."""
        # Get scored players lists
        my_players = list(my_original_team.scored_players.values())
        their_players = list(their_original_team.scored_players.values())

        # Build roster data (side-by-side)
        roster_data = []
        max_players = max(len(my_players), len(their_players))

        for i in range(max_players):
            row = {}

            # My team data
            if i < len(my_players):
                player = my_players[i]
                row["My Player"] = player.player.name
                row["My Pos"] = player.player.position
                row["My Team"] = player.player.team
                row["My Score"] = player.score
            else:
                row["My Player"] = ""
                row["My Pos"] = ""
                row["My Team"] = ""
                row["My Score"] = ""

            # Their team data
            if i < len(their_players):
                player = their_players[i]
                row[f"{opponent_name} Player"] = player.player.name
                row[f"{opponent_name} Pos"] = player.player.position
                row[f"{opponent_name} Team"] = player.player.team
                row[f"{opponent_name} Score"] = player.score
            else:
                row[f"{opponent_name} Player"] = ""
                row[f"{opponent_name} Pos"] = ""
                row[f"{opponent_name} Team"] = ""
                row[f"{opponent_name} Score"] = ""

            roster_data.append(row)

        # Add totals row
        roster_data.append({
            "My Player": "TOTAL",
            "My Pos": "",
            "My Team": "",
            "My Score": my_original_team.team_score,
            f"{opponent_name} Player": "TOTAL",
            f"{opponent_name} Pos": "",
            f"{opponent_name} Team": "",
            f"{opponent_name} Score": their_original_team.team_score
        })

        # Create DataFrame and write to Excel
        df = pd.DataFrame(roster_data)
        df.to_excel(writer, sheet_name="Initial Rosters", index=False)

        # Apply formatting
        self._apply_sheet_formatting(writer.sheets["Initial Rosters"], df, "Initial Rosters")
        self.logger.info("Created Initial Rosters sheet")

    def _create_final_rosters_sheet(
        self,
        writer: pd.ExcelWriter,
        trade: TradeSnapshot,
        opponent_name: str
    ) -> None:
        """Create Final Rosters sheet with post-trade rosters and status markers."""
        # Get scored players lists
        my_players = list(trade.my_new_team.scored_players.values())
        their_players = list(trade.their_new_team.scored_players.values())

        # Determine player statuses based on who was received in the trade
        my_new_ids = {p.player.id for p in trade.my_new_players}
        their_new_ids = {p.player.id for p in trade.their_new_players}

        # Build roster data (side-by-side)
        roster_data = []
        max_players = max(len(my_players), len(their_players))

        for i in range(max_players):
            row = {}

            # My team data
            if i < len(my_players):
                player = my_players[i]
                # Determine status
                if player.player.id in my_new_ids:
                    status = "Received"
                else:
                    status = "Kept"

                row["My Player"] = player.player.name
                row["My Pos"] = player.player.position
                row["My Team"] = player.player.team
                row["My Score"] = player.score
                row["My Status"] = status
            else:
                row["My Player"] = ""
                row["My Pos"] = ""
                row["My Team"] = ""
                row["My Score"] = ""
                row["My Status"] = ""

            # Their team data
            if i < len(their_players):
                player = their_players[i]
                # Determine status
                if player.player.id in their_new_ids:
                    status = "Received"
                else:
                    status = "Kept"

                row[f"{opponent_name} Player"] = player.player.name
                row[f"{opponent_name} Pos"] = player.player.position
                row[f"{opponent_name} Team"] = player.player.team
                row[f"{opponent_name} Score"] = player.score
                row[f"{opponent_name} Status"] = status
            else:
                row[f"{opponent_name} Player"] = ""
                row[f"{opponent_name} Pos"] = ""
                row[f"{opponent_name} Team"] = ""
                row[f"{opponent_name} Score"] = ""
                row[f"{opponent_name} Status"] = ""

            roster_data.append(row)

        # Add totals row
        roster_data.append({
            "My Player": "TOTAL",
            "My Pos": "",
            "My Team": "",
            "My Score": trade.my_new_team.team_score,
            "My Status": "",
            f"{opponent_name} Player": "TOTAL",
            f"{opponent_name} Pos": "",
            f"{opponent_name} Team": "",
            f"{opponent_name} Score": trade.their_new_team.team_score,
            f"{opponent_name} Status": ""
        })

        # Add waiver recommendations section if present
        if trade.waiver_recommendations:
            roster_data.append({
                "My Player": "",
                "My Pos": "",
                "My Team": "",
                "My Score": "",
                "My Status": ""
            })
            roster_data.append({
                "My Player": "RECOMMENDED WAIVER ADDS",
                "My Pos": "",
                "My Team": "",
                "My Score": "",
                "My Status": ""
            })
            for player in trade.waiver_recommendations:
                roster_data.append({
                    "My Player": player.player.name,
                    "My Pos": player.player.position,
                    "My Team": player.player.team,
                    "My Score": player.score,
                    "My Status": "Waiver Add"
                })

        # Create DataFrame and write to Excel
        df = pd.DataFrame(roster_data)
        df.to_excel(writer, sheet_name="Final Rosters", index=False)

        # Apply formatting
        self._apply_sheet_formatting(writer.sheets["Final Rosters"], df, "Final Rosters")
        self.logger.info("Created Final Rosters sheet")

    def _calculate_score_changes(
        self,
        my_original_team: TradeSimTeam,
        their_original_team: TradeSimTeam,
        trade: TradeSnapshot
    ) -> Dict[int, Dict[str, Any]]:
        """
        Identify players whose scores changed due to the trade.

        Args:
            my_original_team: My team before the trade
            their_original_team: Their team before the trade
            trade: The trade snapshot with post-trade teams

        Returns:
            Dict mapping player_id to change info:
                {
                    'owner': 'My Team' or opponent name,
                    'initial_score': float,
                    'final_score': float,
                    'delta': float,
                    'reason_summary': str (detailed format)
                }

        Raises:
            ValueError: If scored_players dictionaries are empty
        """
        # Validate input
        if not my_original_team.scored_players:
            self.logger.warning("My original team has no scored players")
        if not their_original_team.scored_players:
            self.logger.warning("Their original team has no scored players")

        score_changes = {}
        threshold = 0.01

        # Check for players on my team whose scores changed
        for player_id, original_player in my_original_team.scored_players.items():
            if player_id in trade.my_new_team.scored_players:
                new_player = trade.my_new_team.scored_players[player_id]
                delta = new_player.score - original_player.score

                # If score changed by more than threshold, record it
                if abs(delta) > threshold:
                    reason_summary = self._extract_change_reasons(
                        original_player.reason,
                        new_player.reason
                    )
                    score_changes[player_id] = {
                        'owner': 'My Team',
                        'initial_score': original_player.score,
                        'final_score': new_player.score,
                        'delta': delta,
                        'reason_summary': reason_summary
                    }

        # Check for players on their team whose scores changed
        for player_id, original_player in their_original_team.scored_players.items():
            if player_id in trade.their_new_team.scored_players:
                new_player = trade.their_new_team.scored_players[player_id]
                delta = new_player.score - original_player.score

                # If score changed by more than threshold, record it
                if abs(delta) > threshold:
                    reason_summary = self._extract_change_reasons(
                        original_player.reason,
                        new_player.reason
                    )
                    score_changes[player_id] = {
                        'owner': their_original_team.name,
                        'initial_score': original_player.score,
                        'final_score': new_player.score,
                        'delta': delta,
                        'reason_summary': reason_summary
                    }

        self.logger.info(f"Found {len(score_changes)} players with score changes")
        return score_changes

    def _extract_change_reasons(self, initial_reasons: List[str], final_reasons: List[str]) -> str:
        """
        Extract detailed reason for score change by comparing reason lists.

        Focuses on bye week and injury changes (per user requirement Q3).

        Args:
            initial_reasons: Reason strings from initial scoring
            final_reasons: Reason strings from final scoring

        Returns:
            Detailed reason string (e.g., "Bye penalty: +2 same-pos overlaps (-10.5 pts)")
            Multiple changes separated by "; "
        """
        changes = []

        # Extract bye week reasons
        initial_bye = None
        final_bye = None
        for reason in initial_reasons:
            if "Bye Overlaps:" in reason:
                initial_bye = reason
        for reason in final_reasons:
            if "Bye Overlaps:" in reason:
                final_bye = reason

        # If bye reason changed, include it
        if initial_bye != final_bye:
            if final_bye and not initial_bye:
                changes.append(f"Bye penalty added: {final_bye}")
            elif initial_bye and not final_bye:
                changes.append(f"Bye penalty removed: {initial_bye}")
            elif initial_bye and final_bye:
                changes.append(f"Bye penalty changed: {initial_bye} → {final_bye}")

        # Extract injury reasons
        initial_injury = None
        final_injury = None
        for reason in initial_reasons:
            if "Injury:" in reason:
                initial_injury = reason
        for reason in final_reasons:
            if "Injury:" in reason:
                final_injury = reason

        # If injury reason changed, include it
        if initial_injury != final_injury:
            if final_injury and not initial_injury:
                changes.append(f"Injury penalty added: {final_injury}")
            elif initial_injury and not final_injury:
                changes.append(f"Injury penalty removed: {initial_injury}")
            elif initial_injury and final_injury:
                changes.append(f"Injury status changed: {initial_injury} → {final_injury}")

        # If no specific changes found but score changed, note generic change
        if not changes:
            return "Score changed (reason not specific to bye/injury)"

        return "; ".join(changes)

    def _analyze_score_component_changes(
        self,
        initial_scored_player: 'ScoredPlayer',
        final_scored_player: 'ScoredPlayer'
    ) -> Dict[str, Any]:
        """
        Analyze specific scoring component changes (bye week and injury only).

        Focuses on bye week and injury changes per user requirement Q3.
        Other scoring components are out of scope.

        Args:
            initial_scored_player: Player's scoring before trade
            final_scored_player: Player's scoring after trade

        Returns:
            Dict with component-specific changes:
                {
                    'initial_bye_same_pos': int,
                    'final_bye_same_pos': int,
                    'initial_bye_diff_pos': int,
                    'final_bye_diff_pos': int,
                    'bye_points_delta': float,
                    'initial_injury_status': str,
                    'final_injury_status': str,
                    'injury_points_delta': float,
                    'total_score_delta': float
                }
        """
        import re

        result = {
            'initial_bye_same_pos': 0,
            'final_bye_same_pos': 0,
            'initial_bye_diff_pos': 0,
            'final_bye_diff_pos': 0,
            'bye_points_delta': 0.0,
            'initial_injury_status': 'ACTIVE',
            'final_injury_status': 'ACTIVE',
            'injury_points_delta': 0.0,
            'total_score_delta': final_scored_player.score - initial_scored_player.score
        }

        # Extract bye week overlaps from initial state
        for reason in initial_scored_player.reason:
            if "Bye Overlaps:" in reason:
                match = re.search(r'Bye Overlaps: (\d+) same-position, (\d+) different-position \(([+-]?[\d.]+) pts\)', reason)
                if match:
                    result['initial_bye_same_pos'] = int(match.group(1))
                    result['initial_bye_diff_pos'] = int(match.group(2))
                    # Note: The reason shows the negative penalty, so we store it as-is
                    initial_bye_penalty = float(match.group(3))

        # Extract bye week overlaps from final state
        for reason in final_scored_player.reason:
            if "Bye Overlaps:" in reason:
                match = re.search(r'Bye Overlaps: (\d+) same-position, (\d+) different-position \(([+-]?[\d.]+) pts\)', reason)
                if match:
                    result['final_bye_same_pos'] = int(match.group(1))
                    result['final_bye_diff_pos'] = int(match.group(2))
                    final_bye_penalty = float(match.group(3))

                    # Calculate delta (change in penalty, already negative)
                    result['bye_points_delta'] = final_bye_penalty - initial_bye_penalty

        # Extract injury status from initial state
        for reason in initial_scored_player.reason:
            if "Injury:" in reason:
                match = re.search(r'Injury: ([A-Z]+) \(([+-]?[\d.]+) pts\)', reason)
                if match:
                    result['initial_injury_status'] = match.group(1)
                    initial_injury_penalty = float(match.group(2))

        # Extract injury status from final state
        for reason in final_scored_player.reason:
            if "Injury:" in reason:
                match = re.search(r'Injury: ([A-Z]+) \(([+-]?[\d.]+) pts\)', reason)
                if match:
                    result['final_injury_status'] = match.group(1)
                    final_injury_penalty = float(match.group(2))

                    # Calculate delta
                    result['injury_points_delta'] = final_injury_penalty - initial_injury_penalty

        return result

    def _create_score_change_breakdown_sheet(
        self,
        writer: pd.ExcelWriter,
        trade: TradeSnapshot,
        my_original_team: TradeSimTeam,
        their_original_team: TradeSimTeam,
        opponent_name: str
    ) -> None:
        """
        Create Score Change Breakdown sheet showing bye week and injury changes.

        Implements IDEA 4 from specification - focuses on bye week and injury
        component changes only (per user requirement Q3).

        Args:
            writer: pandas ExcelWriter object
            trade: TradeSnapshot with trade details
            my_original_team: My team before trade
            their_original_team: Opponent's team before trade
            opponent_name: Name of opponent team
        """
        try:
            self.logger.info("Creating Score Change Breakdown sheet...")

            # STEP 1: Get all players with score changes
            score_changes = self._calculate_score_changes(
                my_original_team,
                their_original_team,
                trade
            )

            # STEP 2: Analyze component changes for each player
            breakdown_rows = []

            for player_id, change_info in score_changes.items():
                # Get the ScoredPlayer objects
                owner = change_info['owner']
                if owner == 'MY TEAM':
                    initial_team = my_original_team
                    final_team = trade.my_new_team
                else:
                    initial_team = their_original_team
                    final_team = trade.their_new_team

                # Handle traded players (may not be in final team)
                if player_id not in final_team.scored_players:
                    # Player was traded away - skip for breakdown
                    continue

                # Handle received players (may not be in initial team)
                if player_id not in initial_team.scored_players:
                    # Player was received - skip for breakdown (no "before" state to compare)
                    continue

                initial_scored = initial_team.scored_players[player_id]
                final_scored = final_team.scored_players[player_id]

                # Analyze component changes
                component_changes = self._analyze_score_component_changes(
                    initial_scored,
                    final_scored
                )

                # Check if there are any bye or injury changes
                bye_changed = (
                    component_changes['initial_bye_same_pos'] != component_changes['final_bye_same_pos'] or
                    component_changes['initial_bye_diff_pos'] != component_changes['final_bye_diff_pos']
                )
                injury_changed = (
                    component_changes['initial_injury_status'] != component_changes['final_injury_status']
                )

                # Only include if bye or injury changed (per user requirement Q3)
                if bye_changed or injury_changed:
                    player = initial_scored.player
                    breakdown_rows.append({
                        'Player': player.name,
                        'Position': player.position,
                        'NFL Team': player.team,
                        'Owner': owner,
                        'Initial Bye Overlaps': f"{component_changes['initial_bye_same_pos']} same-pos, {component_changes['initial_bye_diff_pos']} diff-pos",
                        'Final Bye Overlaps': f"{component_changes['final_bye_same_pos']} same-pos, {component_changes['final_bye_diff_pos']} diff-pos",
                        'Bye Δ': f"{component_changes['bye_points_delta']:.2f}" if component_changes['bye_points_delta'] != 0 else "-",
                        'Initial Injury': component_changes['initial_injury_status'],
                        'Final Injury': component_changes['final_injury_status'],
                        'Injury Δ': f"{component_changes['injury_points_delta']:.2f}" if component_changes['injury_points_delta'] != 0 else "-",
                        'Total Δ': f"{component_changes['total_score_delta']:.2f}"
                    })

            # STEP 3: Create DataFrame
            if breakdown_rows:
                df = pd.DataFrame(breakdown_rows)
                self.logger.info(f"Found {len(breakdown_rows)} player(s) with bye/injury changes")
            else:
                # Per user requirement Q4: Create empty sheet with informational message
                df = pd.DataFrame([{
                    'Message': 'No bye week or injury changes detected from this trade.'
                }])
                self.logger.info("No bye/injury changes detected - creating informational message")

            # STEP 4: Write to Excel
            df.to_excel(writer, sheet_name='Score Change Breakdown', index=False)

            # STEP 5: Apply formatting
            self._apply_sheet_formatting(writer.sheets['Score Change Breakdown'], df, 'Score Change Breakdown')

            self.logger.info("Score Change Breakdown sheet created successfully")

        except Exception as e:
            self.logger.error(f"Error creating Score Change Breakdown sheet: {e}", exc_info=True)
            # Create error message sheet as fallback
            error_df = pd.DataFrame([{
                'Error': f'Failed to create breakdown: {str(e)}'
            }])
            error_df.to_excel(writer, sheet_name='Score Change Breakdown', index=False)

    def _create_trade_impact_analysis_sheet(
        self,
        writer: pd.ExcelWriter,
        trade: TradeSnapshot,
        my_original_team: TradeSimTeam,
        their_original_team: TradeSimTeam,
        opponent_name: str,
        original_my_score: float,
        original_their_score: float
    ) -> None:
        """
        Create Trade Impact Analysis sheet showing what changed in the trade.

        Shows traded players, received players, and kept players whose scores changed.
        Separate sections for MY TEAM and THEIR TEAM.

        Args:
            writer: pandas ExcelWriter object
            trade: TradeSnapshot with post-trade teams
            my_original_team: My team before trade
            their_original_team: Their team before trade
            opponent_name: Name of opponent team
            original_my_score: My team score before trade
            original_their_score: Their team score before trade

        Raises:
            Exception: If DataFrame creation or writing fails
        """
        try:
            self.logger.info("Creating Trade Impact Analysis sheet")

            # Get score changes for kept players
            score_changes = self._calculate_score_changes(my_original_team, their_original_team, trade)

            # Get IDs for categorization
            my_traded_away_ids = {p.player.id for p in trade.my_original_players}
            my_received_ids = {p.player.id for p in trade.my_new_players}
            their_received_ids = {p.player.id for p in trade.their_new_players}

            impact_data = []

            # === MY TEAM SECTION ===
            # Add header row
            impact_data.append({
                "Team": "MY TEAM",
                "Status": f"(Before → After: {original_my_score:.2f} → {trade.my_new_team.team_score:.2f}, {trade.my_new_team.team_score - original_my_score:+.2f} pts)",
                "Player": "",
                "Position": "",
                "Initial Score": "",
                "Final Score": "",
                "Δ Score": "",
                "Reason for Change": ""
            })

            my_traded_count = 0
            my_received_count = 0
            my_changed_count = 0

            # Add traded away players
            for scored_player in trade.my_original_players:
                my_traded_count += 1
                impact_data.append({
                    "Team": "",
                    "Status": "TRADED AWAY",
                    "Player": scored_player.player.name,
                    "Position": scored_player.player.position,
                    "Initial Score": f"{scored_player.score:.2f}",
                    "Final Score": "-",
                    "Δ Score": "-",
                    "Reason for Change": "Sent to opponent"
                })

            # Add received players
            for scored_player in trade.my_new_players:
                my_received_count += 1
                impact_data.append({
                    "Team": "",
                    "Status": "RECEIVED",
                    "Player": scored_player.player.name,
                    "Position": scored_player.player.position,
                    "Initial Score": "-",
                    "Final Score": f"{scored_player.score:.2f}",
                    "Δ Score": "-",
                    "Reason for Change": "New to roster"
                })

            # Add waiver pickups
            for scored_player in (trade.waiver_recommendations or []):
                impact_data.append({
                    "Team": "",
                    "Status": "ADDED FROM WAIVER",
                    "Player": scored_player.player.name,
                    "Position": scored_player.player.position,
                    "Initial Score": "-",
                    "Final Score": f"{scored_player.score:.2f}",
                    "Δ Score": "-",
                    "Reason for Change": "Waiver wire pickup"
                })

            # Add dropped players
            for scored_player in (trade.my_dropped_players or []):
                impact_data.append({
                    "Team": "",
                    "Status": "DROPPED",
                    "Player": scored_player.player.name,
                    "Position": scored_player.player.position,
                    "Initial Score": f"{scored_player.score:.2f}",
                    "Final Score": "-",
                    "Δ Score": "-",
                    "Reason for Change": "Dropped to make room"
                })

            # Add kept players with score changes
            for player_id, change_info in score_changes.items():
                if change_info['owner'] == 'My Team':
                    my_changed_count += 1
                    # Get player details from new team
                    scored_player = trade.my_new_team.scored_players[player_id]
                    impact_data.append({
                        "Team": "",
                        "Status": "KEPT (CHANGED)",
                        "Player": scored_player.player.name,
                        "Position": scored_player.player.position,
                        "Initial Score": f"{change_info['initial_score']:.2f}",
                        "Final Score": f"{change_info['final_score']:.2f}",
                        "Δ Score": f"{change_info['delta']:+.2f}",
                        "Reason for Change": change_info['reason_summary']
                    })

            # Blank row separator
            impact_data.append({
                "Team": "",
                "Status": "",
                "Player": "",
                "Position": "",
                "Initial Score": "",
                "Final Score": "",
                "Δ Score": "",
                "Reason for Change": ""
            })

            # === THEIR TEAM SECTION ===
            # Add header row
            impact_data.append({
                "Team": f"{opponent_name.upper()}",
                "Status": f"(Before → After: {original_their_score:.2f} → {trade.their_new_team.team_score:.2f}, {trade.their_new_team.team_score - original_their_score:+.2f} pts)",
                "Player": "",
                "Position": "",
                "Initial Score": "",
                "Final Score": "",
                "Δ Score": "",
                "Reason for Change": ""
            })

            their_traded_count = 0
            their_received_count = 0
            their_changed_count = 0

            # Add traded away players (players I received)
            for scored_player in trade.my_new_players:
                their_traded_count += 1
                # Find this player in their original team to get initial score
                initial_score = "-"
                for orig_player in their_original_team.scored_players.values():
                    if orig_player.player.id == scored_player.player.id:
                        initial_score = f"{orig_player.score:.2f}"
                        break

                impact_data.append({
                    "Team": "",
                    "Status": "TRADED AWAY",
                    "Player": scored_player.player.name,
                    "Position": scored_player.player.position,
                    "Initial Score": initial_score,
                    "Final Score": "-",
                    "Δ Score": "-",
                    "Reason for Change": "Sent to me"
                })

            # Add received players (players they got from me)
            for scored_player in trade.their_new_players:
                their_received_count += 1
                impact_data.append({
                    "Team": "",
                    "Status": "RECEIVED",
                    "Player": scored_player.player.name,
                    "Position": scored_player.player.position,
                    "Initial Score": "-",
                    "Final Score": f"{scored_player.score:.2f}",
                    "Δ Score": "-",
                    "Reason for Change": "New to roster"
                })

            # Add their waiver pickups
            for scored_player in (trade.their_waiver_recommendations or []):
                impact_data.append({
                    "Team": "",
                    "Status": "ADDED FROM WAIVER",
                    "Player": scored_player.player.name,
                    "Position": scored_player.player.position,
                    "Initial Score": "-",
                    "Final Score": f"{scored_player.score:.2f}",
                    "Δ Score": "-",
                    "Reason for Change": "Waiver wire pickup"
                })

            # Add their dropped players
            for scored_player in (trade.their_dropped_players or []):
                impact_data.append({
                    "Team": "",
                    "Status": "DROPPED",
                    "Player": scored_player.player.name,
                    "Position": scored_player.player.position,
                    "Initial Score": f"{scored_player.score:.2f}",
                    "Final Score": "-",
                    "Δ Score": "-",
                    "Reason for Change": "Dropped to make room"
                })

            # Add kept players with score changes
            for player_id, change_info in score_changes.items():
                if change_info['owner'] != 'My Team':
                    their_changed_count += 1
                    # Get player details from new team
                    scored_player = trade.their_new_team.scored_players[player_id]
                    impact_data.append({
                        "Team": "",
                        "Status": "KEPT (CHANGED)",
                        "Player": scored_player.player.name,
                        "Position": scored_player.player.position,
                        "Initial Score": f"{change_info['initial_score']:.2f}",
                        "Final Score": f"{change_info['final_score']:.2f}",
                        "Δ Score": f"{change_info['delta']:+.2f}",
                        "Reason for Change": change_info['reason_summary']
                    })

            # Create DataFrame
            if not impact_data:
                self.logger.warning("No trade impact data to display")
                impact_data.append({
                    "Team": "No trade data available",
                    "Status": "",
                    "Player": "",
                    "Position": "",
                    "Initial Score": "",
                    "Final Score": "",
                    "Δ Score": "",
                    "Reason for Change": ""
                })

            df = pd.DataFrame(impact_data)
            df.to_excel(writer, sheet_name="Trade Impact Analysis", index=False)

            # Apply formatting
            self._apply_sheet_formatting(writer.sheets["Trade Impact Analysis"], df, "Trade Impact Analysis")

            self.logger.info(f"Created Trade Impact Analysis sheet with {len(impact_data)} rows")
            self.logger.info(f"MY TEAM: {my_traded_count} traded, {my_received_count} received, {my_changed_count} changed | "
                           f"THEIR TEAM: {their_traded_count} traded, {their_received_count} received, {their_changed_count} changed")

        except Exception as e:
            self.logger.error(f"Failed to create Trade Impact Analysis sheet: {e}", exc_info=True)
            raise

    def _create_detailed_calculations_sheet(
        self,
        writer: pd.ExcelWriter,
        trade: TradeSnapshot,
        my_original_team: TradeSimTeam,
        their_original_team: TradeSimTeam,
        opponent_name: str
    ) -> None:
        """
        Create Detailed Calculations sheet with side-by-side scoring breakdown.

        NEW FORMAT (IDEA 2): Shows Initial/Final/Δ in same row for easier comparison.

        Only shows:
        1. Players directly involved in the trade
        2. Players whose scores changed due to the trade (e.g., bye week penalties changed)
        """
        # Get IDs of players involved in the trade
        my_traded_away_ids = {p.player.id for p in trade.my_original_players}
        my_received_ids = {p.player.id for p in trade.my_new_players}
        their_received_ids = {p.player.id for p in trade.their_new_players}
        my_waiver_ids = {p.player.id for p in (trade.waiver_recommendations or [])}
        their_waiver_ids = {p.player.id for p in (trade.their_waiver_recommendations or [])}
        my_dropped_ids = {p.player.id for p in (trade.my_dropped_players or [])}
        their_dropped_ids = {p.player.id for p in (trade.their_dropped_players or [])}

        # Build set of all player IDs that should be included
        included_player_ids = set()

        # Always include players directly involved in the trade
        included_player_ids.update(my_traded_away_ids)
        included_player_ids.update(my_received_ids)
        included_player_ids.update(their_received_ids)

        # Include waiver pickups and dropped players
        included_player_ids.update(my_waiver_ids)
        included_player_ids.update(their_waiver_ids)
        included_player_ids.update(my_dropped_ids)
        included_player_ids.update(their_dropped_ids)

        # Check for players whose scores changed (likely due to bye week penalty changes)
        # For my team: compare original vs new scores
        for player_id, original_player in my_original_team.scored_players.items():
            if player_id in trade.my_new_team.scored_players:
                new_player = trade.my_new_team.scored_players[player_id]
                # If score changed by more than 0.01, include this player
                if abs(original_player.score - new_player.score) > 0.01:
                    included_player_ids.add(player_id)

        # For their team: compare original vs new scores
        for player_id, original_player in their_original_team.scored_players.items():
            if player_id in trade.their_new_team.scored_players:
                new_player = trade.their_new_team.scored_players[player_id]
                # If score changed by more than 0.01, include this player
                if abs(original_player.score - new_player.score) > 0.01:
                    included_player_ids.add(player_id)

        # Build player data map (player_id -> {initial_data, final_data, owner, status})
        player_data_map = {}

        # Process my team players
        for player_id in included_player_ids:
            # Check initial state
            initial_scored = my_original_team.scored_players.get(player_id)
            final_scored = trade.my_new_team.scored_players.get(player_id)

            if initial_scored or final_scored:
                # Determine status
                if player_id in my_traded_away_ids:
                    status = "TRADED AWAY"
                elif player_id in my_received_ids:
                    status = "RECEIVED"
                elif player_id in my_waiver_ids:
                    status = "ADDED FROM WAIVER"
                elif player_id in my_dropped_ids:
                    status = "DROPPED"
                elif initial_scored and final_scored and abs(initial_scored.score - final_scored.score) > 0.01:
                    status = "KEPT (CHANGED)"
                else:
                    status = "KEPT (UNCHANGED)"

                player_data_map[player_id] = {
                    'player': (initial_scored or final_scored).player,
                    'owner': 'MY TEAM',
                    'status': status,
                    'initial': initial_scored,
                    'final': final_scored
                }

        # Process their team players
        for player_id in included_player_ids:
            # Skip if already processed (shouldn't happen, but safety check)
            if player_id in player_data_map:
                continue

            initial_scored = their_original_team.scored_players.get(player_id)
            final_scored = trade.their_new_team.scored_players.get(player_id)

            if initial_scored or final_scored:
                # Determine status
                if player_id in their_received_ids:
                    status = "RECEIVED"
                elif player_id in their_waiver_ids:
                    status = "ADDED FROM WAIVER"
                elif player_id in their_dropped_ids:
                    status = "DROPPED"
                elif initial_scored and final_scored and abs(initial_scored.score - final_scored.score) > 0.01:
                    status = "KEPT (CHANGED)"
                else:
                    status = "KEPT (UNCHANGED)"

                player_data_map[player_id] = {
                    'player': (initial_scored or final_scored).player,
                    'owner': opponent_name,
                    'status': status,
                    'initial': initial_scored,
                    'final': final_scored
                }

        # Build rows with side-by-side Initial/Final/Δ format
        calc_data = []
        for player_id, data in player_data_map.items():
            row = self._build_side_by_side_row(
                data['player'],
                data['owner'],
                data['status'],
                data['initial'],
                data['final']
            )
            calc_data.append(row)

        # Create DataFrame
        df = pd.DataFrame(calc_data)

        # Filter out columns where all values are "-" or empty
        # Only filter if we have data and df has iterable columns (not during testing with mocks)
        if calc_data:
            try:
                # Keep base columns (Player, Position, NFL Team, Owner, Status)
                base_columns = ['Player', 'Position', 'NFL Team', 'Owner', 'Status']
                columns_to_keep = base_columns.copy()

                for col in df.columns:
                    if col in base_columns:
                        continue

                    # Check if column has any non-dash, non-null values
                    non_empty = df[col].dropna()
                    has_data = any(str(val) != "-" for val in non_empty)

                    if has_data:
                        columns_to_keep.append(col)

                # Filter DataFrame to only keep non-empty columns
                df = df[columns_to_keep]

                self.logger.info(f"Filtered Detailed Calculations: kept {len(columns_to_keep)} columns (removed {len(calc_data[0]) - len(columns_to_keep)} empty columns)")
            except (TypeError, AttributeError):
                # In test environment with mocks, skip filtering
                pass

        # Write to Excel
        df.to_excel(writer, sheet_name="Detailed Calculations", index=False)

        # Apply formatting
        self._apply_sheet_formatting(writer.sheets["Detailed Calculations"], df, "Detailed Calculations")
        self.logger.info(f"Created Detailed Calculations sheet with {len(calc_data)} player entries (side-by-side format)")
        self.logger.info(f"Players included: {len(included_player_ids)} total ({len(my_traded_away_ids)} traded away, {len(my_received_ids)} received, {len(included_player_ids) - len(my_traded_away_ids) - len(my_received_ids)} score-changed)")

    def _build_side_by_side_row(
        self,
        player: 'FantasyPlayer',
        owner: str,
        status: str,
        initial_scored: Optional['ScoredPlayer'],
        final_scored: Optional['ScoredPlayer']
    ) -> Dict[str, Any]:
        """
        Build a single row with Initial/Final/Δ columns for all scoring components.

        Args:
            player: FantasyPlayer object
            owner: Owner name (e.g., "MY TEAM" or opponent name)
            status: Player status (TRADED AWAY, RECEIVED, KEPT (CHANGED), KEPT (UNCHANGED))
            initial_scored: ScoredPlayer before trade (None if received)
            final_scored: ScoredPlayer after trade (None if traded away)

        Returns:
            Dict with all columns for the row
        """
        # Base columns
        row = {
            'Player': player.name,
            'Position': player.position,
            'NFL Team': player.team,
            'Owner': owner,
            'Status': status
        }

        # Parse scoring reasons
        initial_parsed = self._parse_scoring_reasons(initial_scored.reason) if initial_scored else {}
        final_parsed = self._parse_scoring_reasons(final_scored.reason) if final_scored else {}

        # Score columns
        initial_score = initial_scored.score if initial_scored else None
        final_score = final_scored.score if final_scored else None
        row['Initial Score'] = f"{initial_score:.2f}" if initial_score is not None else "-"
        row['Final Score'] = f"{final_score:.2f}" if final_score is not None else "-"

        if initial_score is not None and final_score is not None:
            delta = final_score - initial_score
            row['Δ Score'] = f"{delta:+.2f}" if abs(delta) > 0.01 else "-"
        else:
            row['Δ Score'] = "-"

        # Single-value components (intrinsic to player, don't change during trade)
        # Only show one column since initial and final are always the same
        single_value_components = [
            ('Base Projected', 'Base Projected', float, 2),
            ('Weighted Proj', 'Weighted Proj', float, 2),
            ('ADP Rating', 'ADP Rating', str, None),
            ('ADP Mult', 'ADP Multiplier', float, 3),
            ('Player Rating', 'Player Rating', str, None),
            ('Player Mult', 'Player Rating Multiplier', float, 3),
            ('Team Quality', 'Team Quality', str, None),
            ('Team Mult', 'Team Quality Multiplier', float, 3),
            ('Performance', 'Performance', str, None),
            ('Perf %', 'Perf %', str, None),
            ('Perf Mult', 'Performance Multiplier', float, 3),
            ('Matchup', 'Matchup', str, None),
            ('Matchup Mult', 'Matchup Multiplier', float, 3),
            ('Schedule', 'Schedule', str, None),
            ('Avg Opp Rank', 'Avg Opp Rank', float, 1),
            ('Sched Mult', 'Schedule Multiplier', float, 3),
            ('Draft Bonus', 'Draft Bonus', str, None),
            ('Injury Status', 'Injury Status', str, None)
        ]

        for col_name, parsed_key, data_type, precision in single_value_components:
            # Use final value if available, otherwise initial (for traded away players)
            val = final_parsed.get(parsed_key) or initial_parsed.get(parsed_key)

            if val is not None:
                if data_type == float and precision is not None:
                    row[col_name] = f"{val:.{precision}f}"
                elif data_type == int:
                    row[col_name] = str(int(val))
                else:
                    row[col_name] = str(val)
            else:
                row[col_name] = "-"

        # Multi-value components (change based on roster composition)
        # Show Initial/Final/Δ for these
        multi_value_components = [
            ('Bye Same-Pos', 'Bye Same-Pos', int, 0),
            ('Bye Diff-Pos', 'Bye Diff-Pos', int, 0),
            ('Bye Penalty', 'Bye Penalty', float, 2)
        ]

        for col_name, parsed_key, data_type, precision in multi_value_components:
            initial_val = initial_parsed.get(parsed_key)
            final_val = final_parsed.get(parsed_key)

            # Initial column
            if initial_val is not None:
                if data_type == int:
                    row[f'Initial {col_name}'] = str(int(initial_val))
                else:
                    row[f'Initial {col_name}'] = f"{initial_val:.{precision}f}"
            else:
                row[f'Initial {col_name}'] = "-"

            # Final column
            if final_val is not None:
                if data_type == int:
                    row[f'Final {col_name}'] = str(int(final_val))
                else:
                    row[f'Final {col_name}'] = f"{final_val:.{precision}f}"
            else:
                row[f'Final {col_name}'] = "-"

            # Delta column
            if initial_val is not None and final_val is not None:
                delta = final_val - initial_val
                if abs(delta) > 0.001:
                    if data_type == int:
                        row[f'Δ {col_name}'] = f"{int(delta):+d}"
                    else:
                        row[f'Δ {col_name}'] = f"{delta:+.{precision}f}"
                else:
                    row[f'Δ {col_name}'] = "-"
            else:
                row[f'Δ {col_name}'] = "-"

        return row

    def _parse_scoring_reasons(self, reasons: List[str]) -> Dict[str, Any]:
        """
        Parse scoring reason strings to extract readable values.

        Args:
            reasons: List of reason strings from ScoredPlayer

        Returns:
            Dict with parsed values for each scoring component
        """
        parsed = {}

        for reason in reasons:
            if not reason:
                continue

            # Step 1: Projected points
            if "Projected:" in reason:
                match = re.search(r'Projected: ([\d.]+) pts, Weighted: ([\d.]+) pts', reason)
                if match:
                    parsed["Base Projected"] = float(match.group(1))
                    parsed["Weighted Proj"] = float(match.group(2))

            # Step 2: ADP
            elif "ADP:" in reason:
                match = re.search(r'ADP: ([A-Z_]+) \(([\d.]+)x\)', reason)
                if match:
                    parsed["ADP Rating"] = match.group(1)
                    parsed["ADP Multiplier"] = float(match.group(2))

            # Step 3: Player Rating
            elif "Player Rating:" in reason:
                match = re.search(r'Player Rating: ([A-Z_]+) \(([\d.]+)x\)', reason)
                if match:
                    parsed["Player Rating"] = match.group(1)
                    parsed["Player Rating Multiplier"] = float(match.group(2))

            # Step 4: Team Quality
            elif "Team Quality:" in reason:
                match = re.search(r'Team Quality: ([A-Z_]+) \(([\d.]+)x\)', reason)
                if match:
                    parsed["Team Quality"] = match.group(1)
                    parsed["Team Quality Multiplier"] = float(match.group(2))

            # Step 5: Performance
            elif "Performance:" in reason:
                match = re.search(r'Performance: ([A-Z_]+) \(([+-][\d.]+)%, ([\d.]+)x\)', reason)
                if match:
                    parsed["Performance"] = match.group(1)
                    parsed["Perf %"] = match.group(2)
                    parsed["Performance Multiplier"] = float(match.group(3))

            # Step 6: Matchup
            elif "Matchup:" in reason:
                match = re.search(r'Matchup: ([A-Z_]+) \(([\d.]+)x\)', reason)
                if match:
                    parsed["Matchup"] = match.group(1)
                    parsed["Matchup Multiplier"] = float(match.group(2))

            # Step 7: Schedule
            elif "Schedule:" in reason:
                match = re.search(r'Schedule: ([A-Z_]+) \(avg opp def rank: ([\d.]+), ([\d.]+)x\)', reason)
                if match:
                    parsed["Schedule"] = match.group(1)
                    parsed["Avg Opp Rank"] = float(match.group(2))
                    parsed["Schedule Multiplier"] = float(match.group(3))

            # Step 8: Draft Order Bonus
            elif "Draft Order Bonus:" in reason:
                match = re.search(r'Draft Order Bonus: ([A-Z_]+)', reason)
                if match:
                    parsed["Draft Bonus"] = match.group(1)

            # Step 9: Bye Week Penalty
            elif "Bye Overlaps:" in reason:
                match = re.search(r'Bye Overlaps: (\d+) same-position, (\d+) different-position \(([+-]?[\d.]+) pts\)', reason)
                if match:
                    parsed["Bye Same-Pos"] = int(match.group(1))
                    parsed["Bye Diff-Pos"] = int(match.group(2))
                    parsed["Bye Penalty"] = float(match.group(3))

            # Step 10: Injury
            elif "Injury:" in reason:
                match = re.search(r'Injury: ([A-Z]+)', reason)
                if match:
                    parsed["Injury Status"] = match.group(1)

        return parsed

    def _apply_sheet_formatting(self, worksheet: Any, df: pd.DataFrame, sheet_name: str) -> None:
        """
        Apply formatting to Excel worksheet.

        Args:
            worksheet: openpyxl worksheet object
            df: DataFrame that was written to the sheet
            sheet_name: Name of the sheet (for conditional formatting)
        """
        from openpyxl.styles import Font

        # Bold the header row
        for cell in worksheet[1]:
            cell.font = Font(bold=True)

        # Set column widths
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter

            for cell in column:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass

            # Set width with some padding
            adjusted_width = min(max_length + 2, 30)  # Cap at 30 chars
            worksheet.column_dimensions[column_letter].width = adjusted_width

        # Format score columns with 2 decimal places
        for row in worksheet.iter_rows(min_row=2):
            for cell in row:
                if cell.column_letter in ['D', 'H'] or 'Score' in str(worksheet.cell(1, cell.column).value):
                    if isinstance(cell.value, (int, float)):
                        cell.number_format = '0.00'
