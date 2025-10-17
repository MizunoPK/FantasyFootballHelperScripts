"""
Trade Simulator Mode Manager

Manages trade simulation and analysis including waiver optimization,
trade suggestions, and manual trade visualization. Evaluates trades using
scoring engine with customizable parameters for user vs opponent teams.

Key responsibilities:
- Loading and organizing league rosters by team
- Generating trade combinations (1-for-1, 2-for-2, 3-for-3)
- Evaluating trade fairness using differential scoring
- Providing interactive trade analysis modes (waiver, suggestor, manual)
- Validating roster constraints and position limits
- Persisting trade analyses to timestamped files

Trade evaluation uses different scoring for user vs opponent:
- User team: Full scoring (ADP, player rating, team quality, performance, bye penalties)
- Opponent team: Simplified scoring (projections only, no external factors)

Author: Kai Mizuno
"""

import copy
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from itertools import combinations
from datetime import datetime

from trade_simulator_mode.TradeSimTeam import TradeSimTeam
from trade_simulator_mode.TradeSnapshot import TradeSnapshot

import sys
sys.path.append(str(Path(__file__).parent))
import constants as Constants

sys.path.append(str(Path(__file__).parent.parent))
from util.user_input import show_list_selection
from util.PlayerManager import PlayerManager
from util.ConfigManager import ConfigManager
from util.FantasyTeam import FantasyTeam

# Add parent directory to path for utils imports
sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.DraftedRosterManager import DraftedRosterManager
from utils.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger

class TradeSimulatorModeManager:
    """
    Manages trade simulation modes with roster validation and impact analysis.

    Provides three interactive modes:
    1. Waiver Optimizer - Find best waiver wire pickups
    2. Trade Suggestor - Discover mutually beneficial trades
    3. Manual Trade Visualizer - Analyze specific trade proposals

    Attributes:
        data_folder (Path): Path to data directory containing drafted_data.csv
        player_manager (PlayerManager): PlayerManager instance with all player data
        config (ConfigManager): Configuration manager
        logger: Logger instance
        team_rosters (Dict[str, List[FantasyPlayer]]): Dictionary mapping team names to their player rosters
        my_team (TradeSimTeam): User's team with scoring
        opponent_simulated_teams (List[TradeSimTeam]): All opponent teams with scoring
    """

    def __init__(self, data_folder: Path, player_manager : PlayerManager, config : ConfigManager) -> None:
        """
        Initialize TradeSimulatorModeManager.

        Args:
            data_folder (Path): Path to data directory containing drafted_data.csv
            player_manager (PlayerManager): PlayerManager instance with all player data
        """
        self.logger = get_logger()
        self.data_folder = data_folder
        self.player_manager = player_manager
        self.config = config
        self.team_rosters: Dict[str, List[FantasyPlayer]] = {}

        self.opponent_simulated_teams : List[TradeSimTeam] = []
        self.trade_snapshots : List[TradeSnapshot] = []
        self.init_team_data()

    def run_interactive_mode(self) -> None:
        loop = True
        while (loop):
            self.init_team_data()
            choice = show_list_selection("TRADE SIMULATOR", ["Waiver Optimizer", "Trade Suggestor", "Manual Trade Visualizer"], "Back to Main Menu")

            # Enter whichever mode was selected
            if choice == 1:
                loop, sorted_trades = self.start_waiver_optimizer()
                mode = "waiver"
            elif choice == 2:
                loop, sorted_trades = self.start_trade_suggestor()
                mode = "trade"
            elif choice == 3:
                loop, sorted_trades = self.start_manual_trade()
                mode = "manual"
            else:
                loop, sorted_trades = False, []
                mode = None

            if loop and sorted_trades:
                # Save to File - use appropriate save method based on mode
                if mode == "waiver":
                    self.save_waiver_trades_to_file(sorted_trades)
                elif mode == "trade":
                    self.save_trades_to_file(sorted_trades)
                # Manual trades are saved within start_manual_trade() method

                # Wait
                input("Press enter to continue...")

    def init_team_data(self) -> None:
        """
        Initialize team roster data by organizing players by fantasy team.

        Uses the PlayerManager's player list and DraftedRosterManager to:
        1. Load drafted_data.csv
        2. Match players to their fantasy teams using fuzzy matching
        3. Create team_rosters dict mapping team names to player lists

        Side Effects:
            - Populates self.team_rosters with Dict[team_name, List[FantasyPlayer]]
        """
        self.logger.info("Initializing team data for Trade Simulator")

        # Get all players from PlayerManager
        all_players = self.player_manager.players
        self.logger.info(f"Using {len(all_players)} players from PlayerManager")

        # Load drafted data and organize by team
        drafted_data_csv = self.data_folder / 'drafted_data.csv'

        self.logger.debug(f"Loading drafted data from {drafted_data_csv}")
        roster_manager = DraftedRosterManager(str(drafted_data_csv), Constants.FANTASY_TEAM_NAME)

        if roster_manager.load_drafted_data():
            # Get players organized by team
            self.team_rosters = roster_manager.get_players_by_team(all_players)

            # Log team roster sizes
            self.logger.info(f"Organized players into {len(self.team_rosters)} team rosters")
            for team_name, roster in self.team_rosters.items():
                self.logger.debug(f"Team '{team_name}': {len(roster)} players")
        else:
            self.logger.warning("Failed to load drafted data, team rosters will be empty")
            self.team_rosters = {}

        # Set up all teams
        self.my_team = TradeSimTeam(Constants.FANTASY_TEAM_NAME, self.player_manager.team.roster, self.player_manager, isOpponent=False)
        self.opponent_simulated_teams = []
        self.trade_snapshots = []
        for team_name, team_list in self.team_rosters.items():
            if team_name != self.my_team.name:
                self.opponent_simulated_teams.append(TradeSimTeam(team_name, team_list, self.player_manager))

    
    def start_waiver_optimizer(self) -> Tuple[bool, List[TradeSnapshot]]:
        """
        Find optimal waiver wire pickups by analyzing 1-for-1, 2-for-2, and 3-for-3 trades.

        Returns:
            bool: True to continue menu loop, False to exit
        """
        self.logger.info("Starting Waiver Optimizer mode")

        # Get all waiver wire players (drafted=0)
        lowest_scores = self.player_manager.get_lowest_scores_on_roster()
        waiver_players = self.player_manager.get_player_list(drafted_vals=[0], min_scores=lowest_scores, unlocked_only=True)
        self.logger.info(f"Found {len(waiver_players)} players on waiver wire")

        if not waiver_players:
            print("\nNo players available on waivers.")
            input("\nPress Enter to continue...")
            return True, []

        # Create a TradeSimTeam for the waiver wire
        waiver_team = TradeSimTeam("Waiver Wire", waiver_players, self.player_manager, isOpponent=True)

        # Get all possible waiver pickups (1-for-1, 2-for-2, and 3-for-3)
        # Waiver optimizer must respect max position limits
        self.logger.info("Generating trade combinations...")
        trade_combos = self.get_trade_combinations(
            my_team=self.my_team,
            their_team=waiver_team,
            is_waivers=True,
            one_for_one=True,
            two_for_two=True,
            three_for_three=False,
            ignore_max_positions=False
        )

        self.logger.info(f"Found {len(trade_combos)} valid waiver pickups")

        if not trade_combos:
            print("\nNo valid waiver pickups found that improve your team.")
            input("\nPress Enter to continue...")
            return True, []

        # Sort by improvement (descending)
        sorted_trades = sorted(
            trade_combos,
            key=lambda t: (t.my_new_team.team_score - self.my_team.team_score),
            reverse=True
        )

        # Display top trades
        print("\n" + "="*80)
        print("WAIVER OPTIMIZER - Top Pickup Opportunities")
        print("="*80)
        print(f"Current team score: {self.my_team.team_score:.2f}")
        print(f"Found {len(sorted_trades)} beneficial waiver pickups")
        print()

        # Show top N trades (or all if fewer than N)
        display_count = min(Constants.NUM_TRADE_RUNNERS_UP + 1, len(sorted_trades))

        for i, trade in enumerate(sorted_trades[:display_count], 1):
            improvement = trade.my_new_team.team_score - self.my_team.team_score

            num_players = len(trade.my_new_players)
            trade_type = f"{num_players}-for-{num_players}"

            print(f"#{i} - {trade_type} Trade - Improvement: +{improvement:.2f} pts")
            print(f"  DROP:")
            # Show original scored players (from original roster context)
            for drop_player in trade.my_original_players:
                print(f"    - {drop_player}")
            print(f"  ADD:")
            for add_player in trade.my_new_players:
                print(f"    - {add_player}")
            print(f"  New team score: {trade.my_new_team.team_score:.2f}")
            print()

        input("\nPress Enter to continue...")
        return True, sorted_trades

    def start_trade_suggestor(self) -> Tuple[bool, List[TradeSnapshot]]:
        """
        Find beneficial trades by analyzing all possible trades with opponent teams.

        Returns:
            bool: True to continue menu loop, False to exit
        """
        self.logger.info("Starting Trade Suggestor mode")

        if not self.opponent_simulated_teams:
            print("\nNo opponent teams found.")
            return True, []

        # Collect all possible trades from all opponents
        all_trades = []

        print("\nAnalyzing trades with opponent teams...")
        for opponent_team in self.opponent_simulated_teams:
            self.logger.info(f"Analyzing trades with {opponent_team.name}")
            print(f"  Checking trades with {opponent_team.name}...")

            # Get trade combinations (both 1-for-1 and 2-for-2)
            # Trade suggestor ignores max position limits to allow more creative trades
            trade_combos = self.get_trade_combinations(
                my_team=self.my_team,
                their_team=opponent_team,
                is_waivers=False,
                one_for_one=True,
                two_for_two=True,
                three_for_three=True,
                ignore_max_positions=True
            )

            all_trades.extend(trade_combos)
            self.logger.info(f"Found {len(trade_combos)} valid trades with {opponent_team.name}")

        self.logger.info(f"Total trades found: {len(all_trades)}")

        if not all_trades:
            print("\nNo mutually beneficial trades found.")
            return (True, [])

        # Sort by my team's improvement (descending)
        sorted_trades = sorted(
            all_trades,
            key=lambda t: (t.my_new_team.team_score - self.my_team.team_score),
            reverse=True
        )

        # Display top trades
        print("\n" + "="*80)
        print("TRADE SUGGESTOR - Top Trade Opportunities")
        print("="*80)
        print(f"Current team score: {self.my_team.team_score:.2f}")
        print(f"Found {len(sorted_trades)} mutually beneficial trades")
        print()

        # Show top N trades (or all if fewer than N)
        display_count = min(Constants.NUM_TRADE_RUNNERS_UP + 1, len(sorted_trades))

        for i, trade in enumerate(sorted_trades[:display_count], 1):
            my_improvement = trade.my_new_team.team_score - self.my_team.team_score

            # Get the original team score for comparison
            original_their_team = None
            for opp in self.opponent_simulated_teams:
                if opp.name == trade.their_new_team.name:
                    original_their_team = opp
                    break

            their_improvement = trade.their_new_team.team_score - original_their_team.team_score if original_their_team else 0

            print(f"#{i} - Trade with {trade.their_new_team.name}")
            print(f"  My improvement: +{my_improvement:.2f} pts (New score: {trade.my_new_team.team_score:.2f})")
            print(f"  Their improvement: +{their_improvement:.2f} pts (New score: {trade.their_new_team.team_score:.2f})")
            print(f"  I give:")
            # Show original scored players (from original roster context)
            for player in trade.my_original_players:
                print(f"    - {player}")
            print(f"  I receive:")
            for player in trade.my_new_players:
                print(f"    - {player}")
            print()

        return True, sorted_trades

    def _display_numbered_roster(self, roster: List[FantasyPlayer], title: str) -> None:
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

    def _display_combined_roster(self, my_roster: List[FantasyPlayer], their_roster: List[FantasyPlayer], their_team_name: str) -> Tuple[int, List[FantasyPlayer], List[FantasyPlayer]]:
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

    def _parse_player_selection(self, input_str: str, max_index: int) -> Optional[List[int]]:
        """
        Parse comma-separated player numbers from user input.

        Args:
            input_str (str): User input string with comma-separated numbers
            max_index (int): Maximum valid index (1-based)

        Returns:
            Optional[List[int]]: List of valid 1-based indices, or None if:
                - Input is 'exit' (case-insensitive)
                - Input contains invalid characters
                - Any number is out of range [1, max_index]
                - Duplicate numbers detected
                - Empty input

        Examples:
            >>> _parse_player_selection("1,2,3", 5)
            [1, 2, 3]
            >>> _parse_player_selection("1, 2, 3", 5)  # Spaces accepted
            [1, 2, 3]
            >>> _parse_player_selection("exit", 5)
            None
            >>> _parse_player_selection("1,99", 5)
            None
        """
        # Strip whitespace
        input_str = input_str.strip()

        # Check for exit
        if input_str.lower() == 'exit':
            return None

        # Check for empty input
        if not input_str:
            return None

        # Split by comma and strip whitespace from each element
        parts = [part.strip() for part in input_str.split(',')]

        # Try to convert to integers
        indices = []
        try:
            for part in parts:
                index = int(part)
                indices.append(index)
        except ValueError:
            # Invalid characters
            return None

        # Validate range [1, max_index]
        for index in indices:
            if index < 1 or index > max_index:
                return None

        # Check for duplicates
        if len(indices) != len(set(indices)):
            return None

        return indices

    def _get_players_by_indices(self, roster: List[FantasyPlayer], indices: List[int]) -> List[FantasyPlayer]:
        """
        Extract players from roster by 1-based indices.

        Args:
            roster (List[FantasyPlayer]): The roster to extract from
            indices (List[int]): 1-based indices of players to extract

        Returns:
            List[FantasyPlayer]: Players at the specified indices
        """
        players = []
        for index in indices:
            # Convert 1-based to 0-based
            players.append(roster[index - 1])
        return players

    def _split_players_by_team(self, unified_indices: List[int], roster_boundary: int) -> Tuple[List[int], List[int]]:
        """
        Split unified player selection into my players and their players.

        Args:
            unified_indices (List[int]): List of all selected player indices (1-based)
            roster_boundary (int): Index where opponent roster starts (1-based)

        Returns:
            Tuple[List[int], List[int]]: (my_indices, their_indices)
                my_indices: Indices from my roster (1-based, relative to my roster)
                their_indices: Indices from their roster (1-based, relative to their roster)

        Example:
            If my roster is numbered 1-13 and their roster starts at 14:
            Input: [2, 6, 14, 21], roster_boundary=14
            Output: ([2, 6], [1, 8])  # Their indices adjusted to be 1-based relative to their roster
        """
        my_indices = []
        their_indices = []

        for index in unified_indices:
            if index < roster_boundary:
                # Player from my roster
                my_indices.append(index)
            else:
                # Player from their roster - adjust to be relative to their roster (1-based)
                their_indices.append(index - roster_boundary + 1)

        return my_indices, their_indices

    def _parse_unified_player_selection(self, input_str: str, max_index: int, roster_boundary: int) -> Optional[Tuple[List[int], List[int]]]:
        """
        Parse unified player selection and split into my players and their players.

        Validates that:
        - Input is valid (numbers, in range, no duplicates)
        - At least 1 player from each team
        - Equal number of players from each team

        Args:
            input_str (str): User input string with comma-separated numbers
            max_index (int): Maximum valid index (1-based)
            roster_boundary (int): Index where opponent roster starts (1-based)

        Returns:
            Optional[Tuple[List[int], List[int]]]: (my_indices, their_indices) or None if:
                - Input is 'exit' (case-insensitive)
                - Input contains invalid characters
                - Any number is out of range [1, max_index]
                - Duplicate numbers detected
                - Empty input
                - Not equal numbers from each team
                - Less than 1 player from either team

        Examples:
            >>> _parse_unified_player_selection("2,6,18,21", 30, 14)
            ([2, 6], [5, 8])  # Valid: 2 from my team, 2 from their team
            >>> _parse_unified_player_selection("1,2,3", 30, 14)
            None  # Invalid: all from my team
        """
        # Use existing parser for basic validation
        unified_indices = self._parse_player_selection(input_str, max_index)

        if unified_indices is None:
            return None

        # Split into my players and their players
        my_indices, their_indices = self._split_players_by_team(unified_indices, roster_boundary)

        # Validate at least 1 player from each team
        if len(my_indices) < 1 or len(their_indices) < 1:
            return None

        # Validate equal numbers from each team
        if len(my_indices) != len(their_indices):
            return None

        return my_indices, their_indices

    def _display_trade_result(self, trade: TradeSnapshot, original_my_score: float, original_their_score: float) -> None:
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

    def _save_manual_trade_to_file(self, trade: TradeSnapshot, opponent_name: str, original_my_score: float, original_their_score: float) -> str:
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

    def start_manual_trade(self) -> Tuple[bool, List[TradeSnapshot]]:
        """
        Manual trade visualization mode.

        Allows user to manually select players for a trade and see the impact.

        New Workflow (redesigned 2025-10-16):
        Step 1: Select opponent team to trade with
        Step 2: Display combined roster (both teams numbered sequentially, organized by position/score)
        Step 3: User enters unified selection (e.g., '2,6,18,21' for players from both rosters)
        Step 4: Process trade with validation loop (restart on constraint violation)

        Returns:
            Tuple[bool, List[TradeSnapshot]]: (True, [trade]) or (True, []) to continue menu loop
        """
        self.logger.info("Starting Manual Trade Visualizer mode")

        # Validate opponent teams exist
        if len(self.opponent_simulated_teams) == 0:
            print("\nNo opponent teams available for manual trade analysis.")
            self.logger.warning("No opponent teams available")
            return (True, [])

        # STEP 1: Select opponent team FIRST (sorted alphabetically)
        # Create a mapping of sorted names to team objects
        sorted_teams = sorted(self.opponent_simulated_teams, key=lambda t: t.name)
        opponent_names = [team.name for team in sorted_teams]
        print()
        choice = show_list_selection("SELECT OPPONENT TEAM", opponent_names, "Cancel")

        if choice > len(opponent_names):
            print("Trade cancelled.")
            self.logger.info("Trade cancelled - no opponent selected")
            return (True, [])

        opponent = sorted_teams[choice - 1]
        self.logger.info(f"Selected opponent: {opponent.name}")

        # STEP 2-4: Validation loop - restart on constraint violation
        while True:
            # STEP 2: Display combined roster
            roster_boundary, my_display_order, their_display_order = self._display_combined_roster(
                self.my_team.team,
                opponent.team,
                opponent.name
            )

            # Calculate max index for validation
            max_index = len(self.my_team.team) + len(opponent.team)

            # STEP 3: Get unified player selection
            print()
            selection_input = input(
                f"Enter player numbers to trade (comma-separated, or 'exit' to cancel): "
            ).strip()

            # Parse and split the selection
            parsed_result = self._parse_unified_player_selection(
                selection_input,
                max_index,
                roster_boundary
            )

            if parsed_result is None:
                print("Trade cancelled.")
                self.logger.info("Trade cancelled by user or invalid selection")
                return (True, [])

            my_indices, their_indices = parsed_result

            # Get selected players using DISPLAY order instead of original roster order
            my_selected_players = self._get_players_by_indices(my_display_order, my_indices)
            their_selected_players = self._get_players_by_indices(their_display_order, their_indices)

            # STEP 4: Create new rosters and validate
            my_new_roster = [p for p in self.my_team.team if p not in my_selected_players] + their_selected_players
            their_new_roster = [p for p in opponent.team if p not in their_selected_players] + my_selected_players

            # Validate both rosters (ignore max position limits for manual trades)
            my_roster_valid = self._validate_roster(my_new_roster, ignore_max_positions=True)
            their_roster_valid = self._validate_roster(their_new_roster, ignore_max_positions=True)

            if not my_roster_valid or not their_roster_valid:
                # Generic error message, restart from Step 2
                print("\nError: Not a valid trade. Please try again.\n")
                self.logger.warning("Trade violates roster constraints")
                # Loop continues - restart from Step 2
                continue

            # Trade is valid - break out of loop
            break

        # Create TradeSnapshot and calculate impact
        my_new_team = TradeSimTeam(self.my_team.name, my_new_roster, self.player_manager, isOpponent=False)
        their_new_team = TradeSimTeam(opponent.name, their_new_roster, self.player_manager, isOpponent=True)

        # Get original scored players from the ORIGINAL team
        my_original_scored = self.my_team.get_scored_players(my_selected_players)

        trade = TradeSnapshot(
            my_new_team=my_new_team,
            my_new_players=my_new_team.get_scored_players(their_selected_players),
            their_new_team=their_new_team,
            their_new_players=their_new_team.get_scored_players(my_selected_players),
            my_original_players=my_original_scored
        )

        original_my_score = self.my_team.team_score
        original_their_score = opponent.team_score

        self._display_trade_result(trade, original_my_score, original_their_score)

        # Save to file option
        print()
        save_input = input("Save this trade to a file? (y/n): ").strip().lower()

        if save_input == 'y':
            filename = self._save_manual_trade_to_file(trade, opponent.name, original_my_score, original_their_score)
            print(f"\nTrade saved to: {filename}")
            self.logger.info(f"Trade saved to {filename}")

        return (True, [trade])

    def _count_positions(self, roster: List[FantasyPlayer]) -> Dict[str, int]:
        """
        Count the number of players at each position in a roster.

        Args:
            roster (List[FantasyPlayer]): The roster to count

        Returns:
            Dict[str, int]: Dictionary mapping position to count
        """
        position_counts = {pos: 0 for pos in Constants.MAX_POSITIONS.keys()}
        for player in roster:
            pos = player.position
            if pos in position_counts:
                position_counts[pos] += 1
        return position_counts

    def _validate_roster(self, roster: List[FantasyPlayer], ignore_max_positions: bool = False) -> bool:
        """
        Validate that a roster meets position limits and total player count.

        Args:
            roster (List[FantasyPlayer]): The roster to validate
            ignore_max_positions (bool): If True, skip max position validation (for manual trades)

        Returns:
            bool: True if roster is valid, False otherwise
        """
        # Check total player count
        if len(roster) > Constants.MAX_PLAYERS:
            return False

        # If ignoring max positions (manual trade mode), only check roster size
        if ignore_max_positions:
            return True

        # Try to make a FantasyTeam object and return false if any player cannot be added to the team
        test_team = FantasyTeam(self.config, [])
        for p in roster:
            p_copy = copy.deepcopy(p)
            p_copy.drafted = 0
            drafted = test_team.draft_player(p_copy)
            if not drafted:
                return False

        return True

    def get_trade_combinations(self, my_team : TradeSimTeam, their_team : TradeSimTeam, is_waivers = False,
                               one_for_one : bool = True, two_for_two : bool = True, three_for_three : bool = False,
                               ignore_max_positions : bool = False) -> List[TradeSnapshot]:
        """
        Generate all valid trade combinations between two teams.

        Args:
            my_team (TradeSimTeam): The user's team
            their_team (TradeSimTeam): The opposing team or waiver wire
            is_waivers (bool): If True, skip position validation for their_team
            one_for_one (bool): If True, generate 1-for-1 trades
            two_for_two (bool): If True, generate 2-for-2 trades
            three_for_three (bool): If True, generate 3-for-3 trades
            ignore_max_positions (bool): If True, skip max position validation (for trade suggestor/visualizer)

        Returns:
            List[TradeSnapshot]: List of all valid trade scenarios
        """
        trade_combos : List[TradeSnapshot] = []

        # Get the current rosters, filtering out locked players
        my_roster = [p for p in my_team.team if p.locked != 1]
        their_roster = [p for p in their_team.team if p.locked != 1]

        # Generate 1-for-1 trades
        if one_for_one:
            for my_player in my_roster:
                for their_player in their_roster:
                    # Create new rosters after the trade
                    my_new_roster = [p for p in my_roster if p.id != my_player.id] + [their_player]
                    their_new_roster = [p for p in their_roster if p.id != their_player.id] + [my_player]

                    # Validate my team's roster (always required)
                    if not self._validate_roster(my_new_roster, ignore_max_positions=ignore_max_positions):
                        continue

                    # Validate their team's roster (only if not waivers)
                    if not is_waivers and not self._validate_roster(their_new_roster, ignore_max_positions=ignore_max_positions):
                        continue

                    # Create new TradeSimTeam objects with updated rosters
                    my_new_team = TradeSimTeam(my_team.name, my_new_roster, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster, self.player_manager, isOpponent=True)

                    our_roster_improved = my_new_team.team_score > my_team.team_score
                    their_roster_improved = is_waivers or (their_new_team.team_score > their_team.team_score)

                    if our_roster_improved and their_roster_improved:
                        # Create TradeSnapshot with ScoredPlayer objects
                        # Get original scored players from the ORIGINAL team
                        my_original_scored = my_team.get_scored_players([my_player])

                        snapshot = TradeSnapshot(
                            my_new_team=my_new_team,
                            my_new_players=my_new_team.get_scored_players([their_player]),
                            their_new_team=their_new_team,
                            their_new_players=their_new_team.get_scored_players([my_player]),
                            my_original_players=my_original_scored
                        )
                        trade_combos.append(snapshot)

        # Generate 2-for-2 trades
        if two_for_two:
            # Get all 2-player combinations from each team
            my_combos = list(combinations(my_roster, 2))
            their_combos = list(combinations(their_roster, 2))

            for my_players in my_combos:
                for their_players in their_combos:
                    # Create new rosters after the trade
                    my_new_roster = [p for p in my_roster if p not in my_players] + list(their_players)
                    their_new_roster = [p for p in their_roster if p not in their_players] + list(my_players)

                    # Validate my team's roster (always required)
                    if not self._validate_roster(my_new_roster, ignore_max_positions=ignore_max_positions):
                        continue

                    # Validate their team's roster (only if not waivers)
                    if not is_waivers and not self._validate_roster(their_new_roster, ignore_max_positions=ignore_max_positions):
                        continue

                    # Create new TradeSimTeam objects with updated rosters
                    my_new_team = TradeSimTeam(my_team.name, my_new_roster, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster, self.player_manager, isOpponent=True)

                    our_roster_improved = my_new_team.team_score > my_team.team_score
                    their_roster_improved = is_waivers or (their_new_team.team_score > their_team.team_score)

                    if our_roster_improved and their_roster_improved:
                        # Create TradeSnapshot with ScoredPlayer objects
                        # Get original scored players from the ORIGINAL team
                        my_original_scored = my_team.get_scored_players(list(my_players))

                        snapshot = TradeSnapshot(
                            my_new_team=my_new_team,
                            my_new_players=my_new_team.get_scored_players(list(their_players)),
                            their_new_team=their_new_team,
                            their_new_players=their_new_team.get_scored_players(list(my_players)),
                            my_original_players=my_original_scored
                        )
                        trade_combos.append(snapshot)

        # Generate 3-for-3 trades
        if three_for_three:
            # Get all 3-player combinations from each team
            my_combos = list(combinations(my_roster, 3))
            their_combos = list(combinations(their_roster, 3))

            for my_players in my_combos:
                for their_players in their_combos:
                    # Create new rosters after the trade
                    my_new_roster = [p for p in my_roster if p not in my_players] + list(their_players)
                    their_new_roster = [p for p in their_roster if p not in their_players] + list(my_players)

                    # Validate my team's roster (always required)
                    if not self._validate_roster(my_new_roster, ignore_max_positions=ignore_max_positions):
                        continue

                    # Validate their team's roster (only if not waivers)
                    if not is_waivers and not self._validate_roster(their_new_roster, ignore_max_positions=ignore_max_positions):
                        continue

                    # Create new TradeSimTeam objects with updated rosters
                    my_new_team = TradeSimTeam(my_team.name, my_new_roster, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster, self.player_manager, isOpponent=True)

                    our_roster_improved = my_new_team.team_score > my_team.team_score
                    their_roster_improved = is_waivers or (their_new_team.team_score > their_team.team_score)

                    if our_roster_improved and their_roster_improved:
                        # Create TradeSnapshot with ScoredPlayer objects
                        # Get original scored players from the ORIGINAL team
                        my_original_scored = my_team.get_scored_players(list(my_players))

                        snapshot = TradeSnapshot(
                            my_new_team=my_new_team,
                            my_new_players=my_new_team.get_scored_players(list(their_players)),
                            their_new_team=their_new_team,
                            their_new_players=their_new_team.get_scored_players(list(my_players)),
                            my_original_players=my_original_scored
                        )
                        trade_combos.append(snapshot)

        return trade_combos
    
    def save_trades_to_file(self, sorted_trades : List[TradeSnapshot]) -> None:
        """
        Save trade suggestions to timestamped file (for Trade Suggestor mode).

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
                my_improvement = trade.my_new_team.team_score - self.my_team.team_score

                # Get the original team score for comparison
                original_their_team = None
                for opp in self.opponent_simulated_teams:
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

    def save_waiver_trades_to_file(self, sorted_trades : List[TradeSnapshot]) -> None:
        """
        Save waiver pickup suggestions to timestamped file (for Waiver Optimizer mode).

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
                improvement = trade.my_new_team.team_score - self.my_team.team_score
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
