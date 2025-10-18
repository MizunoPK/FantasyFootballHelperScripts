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
from util.ScoredPlayer import ScoredPlayer

# Add parent directory to path for utils imports
sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.DraftedRosterManager import DraftedRosterManager
from utils.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger

ENABLE_ONE_FOR_ONE = True
ENABLE_TWO_FOR_TWO = True
ENABLE_THREE_FOR_THREE = True

# =============================================================================
# UNEQUAL TRADE CONFIGURATION
# =============================================================================
# Toggle unequal trade types (user can modify these)
ENABLE_TWO_FOR_ONE = True    # Give 2 players, get 1 player
ENABLE_ONE_FOR_TWO = True    # Give 1 player, get 2 players
ENABLE_THREE_FOR_ONE = True  # Give 3 players, get 1 player
ENABLE_ONE_FOR_THREE = True  # Give 1 player, get 3 players
ENABLE_THREE_FOR_TWO = True  # Give 3 players, get 2 players
ENABLE_TWO_FOR_THREE = True  # Give 2 players, get 3 players

class TradeSimulatorModeManager:
    """
    Manages trade simulation modes including waiver optimization and trade analysis.

    Attributes:
        data_folder (Path): Path to data directory containing drafted_data.csv
        player_manager (PlayerManager): PlayerManager instance with all player data
        logger: Logger instance
        team_rosters (Dict[str, List[FantasyPlayer]]): Dictionary mapping team names to their player rosters
    """

    def __init__(self, data_folder: Path, player_manager : PlayerManager, config : ConfigManager):
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

    def run_interactive_mode(self):
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

    def init_team_data(self):
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
            three_for_three=True,
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

        # Check for teams exceeding MAX_PLAYERS and log warnings
        teams_over_limit = []

        # Check my team
        if len(self.my_team.team) > Constants.MAX_PLAYERS:
            teams_over_limit.append((self.my_team.name, self.my_team.team))

        # Check opponent teams
        for opp_team in self.opponent_simulated_teams:
            if len(opp_team.team) > Constants.MAX_PLAYERS:
                teams_over_limit.append((opp_team.name, opp_team.team))

        # Log warnings for teams over the limit
        if teams_over_limit:
            self.logger.warning("=" * 80)
            self.logger.warning(f"ROSTER SIZE WARNING: {len(teams_over_limit)} team(s) exceed MAX_PLAYERS ({Constants.MAX_PLAYERS})")
            self.logger.warning("=" * 80)

            for team_name, roster in teams_over_limit:
                player_names = [p.name for p in sorted(roster, key=lambda p: p.position)]
                self.logger.warning(f"\n{team_name}: {len(roster)} active players")
                self.logger.warning(f"  Players: {', '.join(player_names)}")

            self.logger.warning("=" * 80 + "\n")

        # Log trade analysis start
        self.logger.info("=" * 80)
        self.logger.info("BEGINNING TRADE ANALYSIS")
        self.logger.info(f"My Team: {self.my_team.name} (Score: {self.my_team.team_score:.2f})")
        self.logger.info(f"Opponent Teams: {len(self.opponent_simulated_teams)}")
        self.logger.info("=" * 80 + "\n")

        # Collect all possible trades from all opponents
        all_trades = []

        print("\nAnalyzing trades with opponent teams...")
        import time
        for opponent_team in self.opponent_simulated_teams:
            start_time = time.time()

            # Calculate expected combinations for this team
            my_unlocked = len([p for p in self.my_team.team if p.locked != 1])
            their_unlocked = len([p for p in opponent_team.team if p.locked != 1])

            # Calculate combinations for each trade type
            one_for_one_combos = my_unlocked * their_unlocked
            two_for_two_combos = (my_unlocked * (my_unlocked - 1) // 2) * (their_unlocked * (their_unlocked - 1) // 2)

            # New unequal trade combinations (only count if enabled)
            two_for_one_combos = (my_unlocked * (my_unlocked - 1) // 2) * their_unlocked if ENABLE_TWO_FOR_ONE else 0
            one_for_two_combos = my_unlocked * (their_unlocked * (their_unlocked - 1) // 2) if ENABLE_ONE_FOR_TWO else 0
            three_for_one_combos = (my_unlocked * (my_unlocked - 1) * (my_unlocked - 2) // 6) * their_unlocked if ENABLE_THREE_FOR_ONE else 0
            one_for_three_combos = my_unlocked * (their_unlocked * (their_unlocked - 1) * (their_unlocked - 2) // 6) if ENABLE_ONE_FOR_THREE else 0
            three_for_two_combos = (my_unlocked * (my_unlocked - 1) * (my_unlocked - 2) // 6) * (their_unlocked * (their_unlocked - 1) // 2) if ENABLE_THREE_FOR_TWO else 0
            two_for_three_combos = (my_unlocked * (my_unlocked - 1) // 2) * (their_unlocked * (their_unlocked - 1) * (their_unlocked - 2) // 6) if ENABLE_TWO_FOR_THREE else 0

            total_expected = (one_for_one_combos + two_for_two_combos +
                             two_for_one_combos + one_for_two_combos +
                             three_for_one_combos + one_for_three_combos +
                             three_for_two_combos + two_for_three_combos)

            self.logger.info(f"Analyzing trades with {opponent_team.name}")
            self.logger.info(f"  Team sizes: My={my_unlocked} unlocked, Their={their_unlocked} unlocked")
            self.logger.info(f"  Expected combinations: 1:1={one_for_one_combos:,}, 2:2={two_for_two_combos:,}, "
                           f"2:1={two_for_one_combos:,}, 1:2={one_for_two_combos:,}, "
                           f"3:1={three_for_one_combos:,}, 1:3={one_for_three_combos:,}, "
                           f"3:2={three_for_two_combos:,}, 2:3={two_for_three_combos:,}, Total={total_expected:,}")
            print(f"  Checking trades with {opponent_team.name} ({total_expected:,} combinations)...")

            # Get trade combinations
            # Note: ignore_max_positions=True allows opponent rosters to violate limits
            trade_combos = self.get_trade_combinations(
                my_team=self.my_team,
                their_team=opponent_team,
                is_waivers=False,
                one_for_one=ENABLE_ONE_FOR_ONE,
                two_for_two=ENABLE_TWO_FOR_TWO,
                three_for_three=ENABLE_THREE_FOR_THREE,
                two_for_one=ENABLE_TWO_FOR_ONE,
                one_for_two=ENABLE_ONE_FOR_TWO,
                three_for_one=ENABLE_THREE_FOR_ONE,
                one_for_three=ENABLE_ONE_FOR_THREE,
                three_for_two=ENABLE_THREE_FOR_TWO,
                two_for_three=ENABLE_TWO_FOR_THREE,
                ignore_max_positions=True  # Don't validate opponent roster limits
            )

            elapsed = time.time() - start_time
            all_trades.extend(trade_combos)
            self.logger.info(f"Found {len(trade_combos)} valid trades with {opponent_team.name} in {elapsed:.2f}s ({total_expected/elapsed:.0f} combos/sec)")

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

            # Display waiver recommendations if trade loses roster spots
            if trade.waiver_recommendations:
                print(f"  Recommended Waiver Adds (for me):")
                for player in trade.waiver_recommendations:
                    print(f"    - {player}")

            # Display opponent waiver recommendations
            if trade.their_waiver_recommendations:
                print(f"  Recommended Waiver Adds (for {trade.their_new_team.name}):")
                for player in trade.their_waiver_recommendations:
                    print(f"    - {player}")

            # Display dropped players (beyond the trade itself)
            if trade.my_dropped_players:
                print(f"  Players I Must Drop (to make room):")
                for player in trade.my_dropped_players:
                    print(f"    - {player}")

            # Display opponent dropped players
            if trade.their_dropped_players:
                print(f"  Players {trade.their_new_team.name} Must Drop (to make room):")
                for player in trade.their_dropped_players:
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

    def _get_waiver_recommendations(self, num_spots: int) -> List[ScoredPlayer]:
        """
        Get top N waiver wire recommendations to fill roster spots.

        Uses same logic as Add to Roster mode to score and rank available players.

        Args:
            num_spots (int): Number of waiver players needed

        Returns:
            List[ScoredPlayer]: Top num_spots players sorted by score descending.
                               May return fewer if insufficient players available.

        Example:
            >>> waiver_adds = self._get_waiver_recommendations(2)
            >>> print([p.player.name for p in waiver_adds])
            ['Available Player 1', 'Available Player 2']
        """
        # Handle edge case: no spots needed
        if num_spots <= 0:
            self.logger.debug(f"No waiver recommendations needed (num_spots={num_spots})")
            return []

        # Get available players (drafted=0, unlocked)
        # Note: Don't use can_draft=True filter here because it checks against current roster state,
        # but we're generating recommendations for POST-TRADE roster with open spots
        available_players = self.player_manager.get_player_list(
            drafted_vals=[0],
            unlocked_only=True
        )

        if not available_players:
            self.logger.warning("No waiver wire players available for recommendations")
            return []

        # Score each player
        scored_players: List[ScoredPlayer] = []
        for p in available_players:
            # Use current week for matchup scoring
            scored_player = self.player_manager.score_player(
                p,
                adp=False,
                player_rating=True,
                team_quality=True,
                performance=True,
                matchup=False
            )
            scored_players.append(scored_player)

        # Sort by score descending
        ranked_players = sorted(scored_players, key=lambda x: x.score, reverse=True)

        # Return top num_spots (or fewer if not enough available)
        result_count = min(num_spots, len(ranked_players))
        self.logger.info(f"Generated {result_count} waiver recommendations (requested: {num_spots})")

        return ranked_players[:result_count]

    def _get_lowest_scored_players_per_position(self, team: TradeSimTeam,
                                                 exclude_players: List[FantasyPlayer],
                                                 num_per_position: int = 2) -> List[FantasyPlayer]:
        """
        Get the lowest-scored players from each position for potential drops.

        Used when roster would violate MAX_PLAYERS - identifies drop candidates
        by finding the worst-performing players at each position.

        Args:
            team (TradeSimTeam): Team with scored players
            exclude_players (List[FantasyPlayer]): Players to exclude (e.g., already being traded)
            num_per_position (int): How many lowest players to get per position (default: 2)

        Returns:
            List[FantasyPlayer]: Lowest-scored droppable players, with .score attribute set

        Example:
            >>> drop_candidates = self._get_lowest_scored_players_per_position(my_team, trading_away, 2)
            >>> # Returns up to 2 worst players from each position (QB, RB, WR, TE, K, DST)
        """
        droppable_players = []

        # Group players by position, excluding locked and traded players
        position_groups: Dict[str, List[FantasyPlayer]] = {pos: [] for pos in Constants.MAX_POSITIONS.keys()}

        for player in team.team:
            # Skip players being traded away
            if player in exclude_players:
                continue

            # Skip locked players (can't drop them)
            if player.locked:
                continue

            # Add to position group
            if player.position in position_groups:
                position_groups[player.position].append(player)

        # For each position, get the lowest-scored players
        for players in position_groups.values():
            if not players:
                continue

            # Sort by score (ascending - lowest first)
            sorted_players = sorted(players, key=lambda p: p.score)

            # Take the lowest N players from this position
            droppable_players.extend(sorted_players[:num_per_position])

        self.logger.debug(f"Found {len(droppable_players)} droppable players from {team.name}")
        return droppable_players

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

    def _validate_trade_doesnt_worsen_violations(self, original_roster: List[FantasyPlayer],
                                                  new_roster: List[FantasyPlayer]) -> bool:
        """
        Validate that a trade doesn't make position violations worse for opponent teams.
        Allows starting with violations but prevents worsening them.

        Args:
            original_roster: The team's roster before the trade
            new_roster: The team's roster after the trade

        Returns:
            bool: True if trade doesn't worsen violations, False if it does
        """
        # Count positions before and after
        original_counts = self._count_positions(original_roster)
        new_counts = self._count_positions(new_roster)

        # Check each position - new count must not exceed original count if original was already over limit
        for pos in [Constants.QB, Constants.TE, Constants.K]:
            max_allowed = Constants.MAX_POSITIONS[pos]
            original_count = original_counts.get(pos, 0)
            new_count = new_counts.get(pos, 0)

            # If trade increases violation, reject it
            if new_count > max_allowed and new_count > original_count:
                return False

        # Check FLEX-eligible positions - both individual and total limits
        # Each FLEX-eligible position can have at most MAX_POSITIONS[pos] + 1
        for pos in [Constants.RB, Constants.WR, Constants.DST]:
            max_with_flex = Constants.MAX_POSITIONS[pos] + Constants.MAX_POSITIONS[Constants.FLEX]
            original_count = original_counts.get(pos, 0)
            new_count = new_counts.get(pos, 0)

            # If trade increases individual position violation, reject it
            if new_count > max_with_flex and new_count > original_count:
                return False

        # Also check total FLEX-eligible limit
        flex_limit = (Constants.MAX_POSITIONS[Constants.RB] +
                     Constants.MAX_POSITIONS[Constants.WR] +
                     Constants.MAX_POSITIONS[Constants.DST] +
                     Constants.MAX_POSITIONS[Constants.FLEX])

        original_flex = (original_counts.get(Constants.RB, 0) +
                        original_counts.get(Constants.WR, 0) +
                        original_counts.get(Constants.DST, 0))

        new_flex = (new_counts.get(Constants.RB, 0) +
                   new_counts.get(Constants.WR, 0) +
                   new_counts.get(Constants.DST, 0))

        # If trade increases total FLEX violation, reject it
        if new_flex > flex_limit and new_flex > original_flex:
            return False

        return True

    def _validate_roster(self, roster: List[FantasyPlayer], ignore_max_positions: bool = False,
                        only_validate_non_flex: bool = False) -> bool:
        """
        Validate that a roster meets position limits and total player count.

        Args:
            roster (List[FantasyPlayer]): The roster to validate
            ignore_max_positions (bool): If True, skip ALL validation including roster size (for manual trade visualizer)
            only_validate_non_flex (bool): If True, only validate QB/TE/K limits, skip FLEX validation (for opponent rosters)

        Returns:
            bool: True if roster is valid, False otherwise
        """
        # If ignoring max positions (manual trade visualizer mode), skip all validation
        if ignore_max_positions:
            return True

        # Count players by position
        position_counts = {pos: 0 for pos in Constants.MAX_POSITIONS.keys()}
        for player in roster:
            pos = player.position
            if pos in position_counts:
                position_counts[pos] += 1

        # Validate non-FLEX-eligible positions against their individual max limits
        # Note: RB, WR, and DST are FLEX-eligible, so we only check their combined total later
        for pos in [Constants.QB, Constants.TE, Constants.K]:
            if position_counts[pos] > Constants.MAX_POSITIONS[pos]:
                return False

        # If only validating non-FLEX positions (for opponent teams), skip MAX_PLAYERS and FLEX validation
        if only_validate_non_flex:
            return True

        roster_size = len(roster)

        # Check total player count (only for full validation - user's team)
        if roster_size > Constants.MAX_PLAYERS:
            return False

        # For FLEX-eligible positions (RB, WR, DST), check both individual and total limits
        # Each FLEX-eligible position can have at most MAX_POSITIONS[pos] + 1 (dedicated slots + FLEX)
        # e.g., WR can have max 5 (4 WR slots + 1 FLEX), RB can have max 5 (4 RB slots + 1 FLEX)
        for pos in [Constants.RB, Constants.WR, Constants.DST]:
            max_with_flex = Constants.MAX_POSITIONS[pos] + Constants.MAX_POSITIONS[Constants.FLEX]
            if position_counts[pos] > max_with_flex:
                return False

        # Also check total FLEX-eligible against total available slots
        total_flex_eligible_slots = (Constants.MAX_POSITIONS[Constants.RB] +
                                      Constants.MAX_POSITIONS[Constants.WR] +
                                      Constants.MAX_POSITIONS[Constants.DST] +
                                      Constants.MAX_POSITIONS[Constants.FLEX])

        total_flex_eligible_players = (position_counts[Constants.RB] +
                                        position_counts[Constants.WR] +
                                        position_counts[Constants.DST])

        if total_flex_eligible_players > total_flex_eligible_slots:
            return False

        return True

    def get_trade_combinations(self, my_team : TradeSimTeam, their_team : TradeSimTeam, is_waivers = False,
                               one_for_one : bool = True, two_for_two : bool = True, three_for_three : bool = False,
                               two_for_one : bool = False, one_for_two : bool = False,
                               three_for_one : bool = False, one_for_three : bool = False,
                               three_for_two : bool = False, two_for_three : bool = False,
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
            two_for_one (bool): If True, generate 2-for-1 trades (give 2, get 1)
            one_for_two (bool): If True, generate 1-for-2 trades (give 1, get 2)
            three_for_one (bool): If True, generate 3-for-1 trades (give 3, get 1)
            one_for_three (bool): If True, generate 1-for-3 trades (give 1, get 3)
            three_for_two (bool): If True, generate 3-for-2 trades (give 3, get 2)
            two_for_three (bool): If True, generate 2-for-3 trades (give 2, get 3)
            ignore_max_positions (bool): If True, skip max position validation for BOTH teams (for trade suggestor - allows opponent rosters to violate limits)

        Returns:
            List[TradeSnapshot]: List of all valid trade scenarios
        """
        trade_combos : List[TradeSnapshot] = []

        # Track rejection reasons for diagnostics
        rejection_stats = {
            'my_validation_failed': 0,
            'their_validation_failed': 0,
            'my_team_worse': 0,
            'their_team_worse': 0,
            'both_worse': 0,
            'valid_trades': 0
        }

        # Get the current rosters, filtering out locked players for trading
        # But keep locked players separate for position validation
        my_roster = [p for p in my_team.team if p.locked != 1]
        my_locked = [p for p in my_team.team if p.locked == 1]
        their_roster = [p for p in their_team.team if p.locked != 1]
        their_locked = [p for p in their_team.team if p.locked == 1]

        # Generate 1-for-1 trades
        if one_for_one:
            for my_player in my_roster:
                for their_player in their_roster:
                    # Create new rosters after the trade
                    my_new_roster = [p for p in my_roster if p.id != my_player.id] + [their_player]
                    their_new_roster = [p for p in their_roster if p.id != their_player.id] + [my_player]

                    # Validate my team's roster (always required) - include locked players in validation
                    # For trade suggestor, we always validate our roster but allow opponent violations
                    my_full_roster = my_new_roster + my_locked
                    if not self._validate_roster(my_full_roster, ignore_max_positions=False):
                        rejection_stats['my_validation_failed'] += 1
                        continue

                    # Validate their team's roster (only if not waivers) - include locked players in validation
                    # For trade suggestor (ignore_max_positions=True), allow existing violations but prevent worsening them
                    if not is_waivers:
                        their_full_roster = their_new_roster + their_locked
                        if ignore_max_positions:
                            # Trade suggestor mode: Allow opponent to start with violations, but don't let trade make them worse
                            their_original_roster = their_team.team + their_locked
                            if not self._validate_trade_doesnt_worsen_violations(their_original_roster, their_full_roster):
                                rejection_stats['their_validation_failed'] += 1
                                continue
                        else:
                            # Manual trade mode: Full validation
                            if not self._validate_roster(their_full_roster, ignore_max_positions=False):
                                rejection_stats['their_validation_failed'] += 1
                                continue

                    # Create new TradeSimTeam objects with updated rosters
                    my_new_team = TradeSimTeam(my_team.name, my_new_roster, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster, self.player_manager, isOpponent=True)

                    # Check if trade improves both teams based on mode-specific thresholds
                    if is_waivers:
                        # Waiver mode: use MIN_WAIVER_IMPROVEMENT threshold
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_WAIVER_IMPROVEMENT
                        their_roster_improved = True  # Waivers don't have an opponent team
                    else:
                        # Trade suggestor mode: use MIN_TRADE_IMPROVEMENT threshold for both teams
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
                        their_roster_improved = (their_new_team.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT

                    if our_roster_improved and their_roster_improved:
                        rejection_stats['valid_trades'] += 1
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
                    elif not our_roster_improved and not their_roster_improved:
                        rejection_stats['both_worse'] += 1
                    elif not our_roster_improved:
                        rejection_stats['my_team_worse'] += 1
                    else:
                        rejection_stats['their_team_worse'] += 1

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

                    # Validate my team's roster (always required) - include locked players in validation
                    # For trade suggestor, we always validate our roster but allow opponent violations
                    my_full_roster = my_new_roster + my_locked
                    if not self._validate_roster(my_full_roster, ignore_max_positions=False):
                        rejection_stats['my_validation_failed'] += 1
                        continue

                    # Validate their team's roster (only if not waivers) - include locked players in validation
                    # For trade suggestor (ignore_max_positions=True), allow existing violations but prevent worsening them
                    if not is_waivers:
                        their_full_roster = their_new_roster + their_locked
                        if ignore_max_positions:
                            # Trade suggestor mode: Allow opponent to start with violations, but don't let trade make them worse
                            their_original_roster = their_team.team + their_locked
                            if not self._validate_trade_doesnt_worsen_violations(their_original_roster, their_full_roster):
                                rejection_stats['their_validation_failed'] += 1
                                continue
                        else:
                            # Manual trade mode: Full validation
                            if not self._validate_roster(their_full_roster, ignore_max_positions=False):
                                rejection_stats['their_validation_failed'] += 1
                                continue

                    # Create new TradeSimTeam objects with updated rosters
                    my_new_team = TradeSimTeam(my_team.name, my_new_roster, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster, self.player_manager, isOpponent=True)

                    # Check if trade improves both teams based on mode-specific thresholds
                    if is_waivers:
                        # Waiver mode: use MIN_WAIVER_IMPROVEMENT threshold
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_WAIVER_IMPROVEMENT
                        their_roster_improved = True  # Waivers don't have an opponent team
                    else:
                        # Trade suggestor mode: use MIN_TRADE_IMPROVEMENT threshold for both teams
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
                        their_roster_improved = (their_new_team.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT

                    if our_roster_improved and their_roster_improved:
                        rejection_stats['valid_trades'] += 1
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
                    elif not our_roster_improved and not their_roster_improved:
                        rejection_stats['both_worse'] += 1
                    elif not our_roster_improved:
                        rejection_stats['my_team_worse'] += 1
                    else:
                        rejection_stats['their_team_worse'] += 1

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

                    # Validate my team's roster (always required) - include locked players in validation
                    # For trade suggestor, we always validate our roster but allow opponent violations
                    my_full_roster = my_new_roster + my_locked
                    if not self._validate_roster(my_full_roster, ignore_max_positions=False):
                        rejection_stats['my_validation_failed'] += 1
                        continue

                    # Validate their team's roster (only if not waivers) - include locked players in validation
                    # For trade suggestor (ignore_max_positions=True), allow existing violations but prevent worsening them
                    if not is_waivers:
                        their_full_roster = their_new_roster + their_locked
                        if ignore_max_positions:
                            # Trade suggestor mode: Allow opponent to start with violations, but don't let trade make them worse
                            their_original_roster = their_team.team + their_locked
                            if not self._validate_trade_doesnt_worsen_violations(their_original_roster, their_full_roster):
                                rejection_stats['their_validation_failed'] += 1
                                continue
                        else:
                            # Manual trade mode: Full validation
                            if not self._validate_roster(their_full_roster, ignore_max_positions=False):
                                rejection_stats['their_validation_failed'] += 1
                                continue

                    # Create new TradeSimTeam objects with updated rosters
                    my_new_team = TradeSimTeam(my_team.name, my_new_roster, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster, self.player_manager, isOpponent=True)

                    # Check if trade improves both teams based on mode-specific thresholds
                    if is_waivers:
                        # Waiver mode: use MIN_WAIVER_IMPROVEMENT threshold
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_WAIVER_IMPROVEMENT
                        their_roster_improved = True  # Waivers don't have an opponent team
                    else:
                        # Trade suggestor mode: use MIN_TRADE_IMPROVEMENT threshold for both teams
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
                        their_roster_improved = (their_new_team.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT

                    if our_roster_improved and their_roster_improved:
                        rejection_stats['valid_trades'] += 1
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
                    elif not our_roster_improved and not their_roster_improved:
                        rejection_stats['both_worse'] += 1
                    elif not our_roster_improved:
                        rejection_stats['my_team_worse'] += 1
                    else:
                        rejection_stats['their_team_worse'] += 1

        # Generate 2-for-1 trades (give 2 players, get 1 player)
        if two_for_one:
            # Get all 2-player combinations from my team
            my_combos = list(combinations(my_roster, 2))

            for my_players in my_combos:
                for their_player in their_roster:
                    # Create new rosters after the trade
                    my_new_roster = [p for p in my_roster if p not in my_players] + [their_player]
                    their_new_roster = [p for p in their_roster if p != their_player] + list(my_players)

                    # Calculate waiver recommendations for both teams BEFORE roster validation
                    # 2-for-1: I give 2, get 1 = net -1 (I need waiver), they get 2, give 1 = net +1 (no waiver)
                    my_waiver_recs = self._get_waiver_recommendations(num_spots=1)
                    their_waiver_recs = []  # They gain a roster spot, no waiver needed

                    # Add waiver players to rosters for scoring
                    my_new_roster_with_waivers = my_new_roster + [rec.player for rec in my_waiver_recs]
                    their_new_roster_with_waivers = their_new_roster  # No waivers for them

                    # Validate my team's roster (always required) - include locked players in validation
                    my_full_roster = my_new_roster_with_waivers + my_locked
                    if not self._validate_roster(my_full_roster, ignore_max_positions=False):
                        rejection_stats['my_validation_failed'] += 1
                        continue

                    # Validate their team's roster (only if not waivers) - include locked players in validation
                    their_roster_valid = True
                    if not is_waivers:
                        their_full_roster = their_new_roster_with_waivers + their_locked
                        if ignore_max_positions:
                            # Trade suggestor mode: Allow opponent to start with violations, but don't let trade make them worse
                            their_original_roster = their_team.team + their_locked
                            their_roster_valid = self._validate_trade_doesnt_worsen_violations(their_original_roster, their_full_roster)
                        else:
                            # Manual trade mode: Full validation
                            their_roster_valid = self._validate_roster(their_full_roster, ignore_max_positions=False)

                        # If opponent validation fails, try drop variations (opponent receives more players, needs to drop)
                        if not their_roster_valid:
                            # 2:1 trade: Opponent gets net +1, so need to drop 1 additional player
                            drop_candidates = self._get_lowest_scored_players_per_position(
                                their_team,
                                exclude_players=[their_player],
                                num_per_position=2
                            )

                            # Try dropping each candidate
                            for drop_player in drop_candidates:
                                # Create roster with drop
                                their_roster_with_drop = [p for p in their_new_roster_with_waivers if p != drop_player]
                                their_full_roster_with_drop = their_roster_with_drop + their_locked

                                # Validate with drop
                                if ignore_max_positions:
                                    if not self._validate_trade_doesnt_worsen_violations(their_original_roster, their_full_roster_with_drop):
                                        continue
                                else:
                                    if not self._validate_roster(their_full_roster_with_drop, ignore_max_positions=False):
                                        continue

                                # Create teams with drop included
                                my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers, self.player_manager, isOpponent=False)
                                their_new_team_with_drop = TradeSimTeam(their_team.name, their_roster_with_drop, self.player_manager, isOpponent=True)

                                # Check improvement against ORIGINAL team scores
                                our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
                                their_roster_improved = (their_new_team_with_drop.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT

                                if our_roster_improved and their_roster_improved:
                                    rejection_stats['valid_trades'] += 1
                                    my_original_scored = my_team.get_scored_players(list(my_players))
                                    their_dropped_scored = their_team.get_scored_players([drop_player])

                                    snapshot = TradeSnapshot(
                                        my_new_team=my_new_team,
                                        my_new_players=my_new_team.get_scored_players([their_player]),
                                        their_new_team=their_new_team_with_drop,
                                        their_new_players=their_new_team_with_drop.get_scored_players(list(my_players)),
                                        my_original_players=my_original_scored,
                                        waiver_recommendations=my_waiver_recs,
                                        their_waiver_recommendations=their_waiver_recs,
                                        my_dropped_players=[],
                                        their_dropped_players=their_dropped_scored
                                    )
                                    trade_combos.append(snapshot)

                            # After trying all drops, skip to next trade
                            rejection_stats['their_validation_failed'] += 1
                            continue

                    # Create new TradeSimTeam objects with rosters INCLUDING waiver players
                    my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers, self.player_manager, isOpponent=True)

                    # Check if trade improves both teams based on mode-specific thresholds
                    # NOTE: Team scores now include waiver pickups
                    if is_waivers:
                        # Waiver mode: use MIN_WAIVER_IMPROVEMENT threshold
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_WAIVER_IMPROVEMENT
                        their_roster_improved = True  # Waivers don't have an opponent team
                    else:
                        # Trade suggestor mode: use MIN_TRADE_IMPROVEMENT threshold for both teams
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
                        their_roster_improved = (their_new_team.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT

                    if our_roster_improved and their_roster_improved:
                        rejection_stats['valid_trades'] += 1
                        # Create TradeSnapshot with ScoredPlayer objects
                        my_original_scored = my_team.get_scored_players(list(my_players))

                        snapshot = TradeSnapshot(
                            my_new_team=my_new_team,
                            my_new_players=my_new_team.get_scored_players([their_player]),
                            their_new_team=their_new_team,
                            their_new_players=their_new_team.get_scored_players(list(my_players)),
                            my_original_players=my_original_scored,
                            waiver_recommendations=my_waiver_recs,
                            their_waiver_recommendations=their_waiver_recs
                        )
                        trade_combos.append(snapshot)
                    elif not our_roster_improved and not their_roster_improved:
                        rejection_stats['both_worse'] += 1
                    elif not our_roster_improved:
                        rejection_stats['my_team_worse'] += 1
                    else:
                        rejection_stats['their_team_worse'] += 1

        # Generate 1-for-2 trades (give 1 player, get 2 players)
        if one_for_two:
            # Get all 2-player combinations from their team
            their_combos = list(combinations(their_roster, 2))

            for my_player in my_roster:
                for their_players in their_combos:
                    # Create new rosters after the trade
                    my_new_roster = [p for p in my_roster if p != my_player] + list(their_players)
                    their_new_roster = [p for p in their_roster if p not in their_players] + [my_player]

                    # Calculate waiver recommendations for both teams BEFORE roster validation
                    # 1-for-2: I give 1, get 2 = net +1 (no waiver), they give 2, get 1 = net -1 (they need waiver)
                    my_waiver_recs = []  # I gain a roster spot, no waiver needed
                    their_waiver_recs = self._get_waiver_recommendations(num_spots=1) if not is_waivers else []

                    # Add waiver players to rosters for scoring
                    my_new_roster_with_waivers = my_new_roster  # No waivers for me
                    their_new_roster_with_waivers = their_new_roster + [rec.player for rec in their_waiver_recs]

                    # Validate my team's roster (always required) - include locked players in validation
                    my_full_roster = my_new_roster_with_waivers + my_locked
                    my_roster_valid = self._validate_roster(my_full_roster, ignore_max_positions=False)

                    # If validation fails, try drop variations (user receives more players, needs to drop)
                    if not my_roster_valid:
                        # 1:2 trade: User gets net +1, so need to drop 1 additional player
                        drop_candidates = self._get_lowest_scored_players_per_position(
                            my_team,
                            exclude_players=[my_player],
                            num_per_position=2
                        )

                        # Try dropping each candidate
                        for drop_player in drop_candidates:
                            # Create roster with drop
                            my_roster_with_drop = [p for p in my_new_roster if p != drop_player]
                            my_full_roster_with_drop = my_roster_with_drop + my_locked

                            # Validate with drop
                            if not self._validate_roster(my_full_roster_with_drop, ignore_max_positions=False):
                                continue

                            # Opponent validation (unchanged from original)
                            if not is_waivers:
                                their_full_roster = their_new_roster_with_waivers + their_locked
                                if ignore_max_positions:
                                    their_original_roster = their_team.team + their_locked
                                    if not self._validate_trade_doesnt_worsen_violations(their_original_roster, their_full_roster):
                                        continue
                                else:
                                    if not self._validate_roster(their_full_roster, ignore_max_positions=False):
                                        continue

                            # Create teams with drop included
                            my_new_team_with_drop = TradeSimTeam(my_team.name, my_roster_with_drop, self.player_manager, isOpponent=False)
                            their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers, self.player_manager, isOpponent=True)

                            # Check improvement against ORIGINAL team score
                            if is_waivers:
                                our_roster_improved = (my_new_team_with_drop.team_score - my_team.team_score) >= Constants.MIN_WAIVER_IMPROVEMENT
                                their_roster_improved = True
                            else:
                                our_roster_improved = (my_new_team_with_drop.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
                                their_roster_improved = (their_new_team.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT

                            if our_roster_improved and their_roster_improved:
                                rejection_stats['valid_trades'] += 1
                                my_original_scored = my_team.get_scored_players([my_player])
                                my_dropped_scored = my_team.get_scored_players([drop_player])

                                snapshot = TradeSnapshot(
                                    my_new_team=my_new_team_with_drop,
                                    my_new_players=my_new_team_with_drop.get_scored_players(list(their_players)),
                                    their_new_team=their_new_team,
                                    their_new_players=their_new_team.get_scored_players([my_player]),
                                    my_original_players=my_original_scored,
                                    waiver_recommendations=my_waiver_recs,
                                    their_waiver_recommendations=their_waiver_recs,
                                    my_dropped_players=my_dropped_scored,
                                    their_dropped_players=[]
                                )
                                trade_combos.append(snapshot)

                        # After trying all drops, skip to next trade
                        rejection_stats['my_validation_failed'] += 1
                        continue

                    # Validate their team's roster (only if not waivers) - include locked players in validation
                    if not is_waivers:
                        their_full_roster = their_new_roster_with_waivers + their_locked
                        if ignore_max_positions:
                            # Trade suggestor mode: Allow opponent to start with violations, but don't let trade make them worse
                            their_original_roster = their_team.team + their_locked
                            if not self._validate_trade_doesnt_worsen_violations(their_original_roster, their_full_roster):
                                rejection_stats['their_validation_failed'] += 1
                                continue
                        else:
                            # Manual trade mode: Full validation
                            if not self._validate_roster(their_full_roster, ignore_max_positions=False):
                                rejection_stats['their_validation_failed'] += 1
                                continue

                    # Create new TradeSimTeam objects with rosters INCLUDING waiver players
                    my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers, self.player_manager, isOpponent=True)

                    # Check if trade improves both teams based on mode-specific thresholds
                    # NOTE: Team scores now include waiver pickups
                    if is_waivers:
                        # Waiver mode: use MIN_WAIVER_IMPROVEMENT threshold
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_WAIVER_IMPROVEMENT
                        their_roster_improved = True  # Waivers don't have an opponent team
                    else:
                        # Trade suggestor mode: use MIN_TRADE_IMPROVEMENT threshold for both teams
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
                        their_roster_improved = (their_new_team.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT

                    if our_roster_improved and their_roster_improved:
                        rejection_stats['valid_trades'] += 1
                        # Create TradeSnapshot with ScoredPlayer objects
                        my_original_scored = my_team.get_scored_players([my_player])

                        snapshot = TradeSnapshot(
                            my_new_team=my_new_team,
                            my_new_players=my_new_team.get_scored_players(list(their_players)),
                            their_new_team=their_new_team,
                            their_new_players=their_new_team.get_scored_players([my_player]),
                            my_original_players=my_original_scored,
                            waiver_recommendations=my_waiver_recs,
                            their_waiver_recommendations=their_waiver_recs
                        )
                        trade_combos.append(snapshot)
                    elif not our_roster_improved and not their_roster_improved:
                        rejection_stats['both_worse'] += 1
                    elif not our_roster_improved:
                        rejection_stats['my_team_worse'] += 1
                    else:
                        rejection_stats['their_team_worse'] += 1

        # Generate 3-for-1 trades (give 3 players, get 1 player)
        if three_for_one:
            # Get all 3-player combinations from my team
            my_combos = list(combinations(my_roster, 3))

            for my_players in my_combos:
                for their_player in their_roster:
                    # Create new rosters after the trade
                    my_new_roster = [p for p in my_roster if p not in my_players] + [their_player]
                    their_new_roster = [p for p in their_roster if p != their_player] + list(my_players)

                    # Calculate waiver recommendations for both teams BEFORE roster validation
                    # 3-for-1: I give 3, get 1 = net -2 (I need 2 waivers), they get 3, give 1 = net +2 (no waiver)
                    my_waiver_recs = self._get_waiver_recommendations(num_spots=2)
                    their_waiver_recs = []  # They gain roster spots, no waiver needed

                    # Add waiver players to rosters for scoring
                    my_new_roster_with_waivers = my_new_roster + [rec.player for rec in my_waiver_recs]
                    their_new_roster_with_waivers = their_new_roster  # No waivers for them

                    # Validate my team's roster (always required) - include locked players in validation
                    my_full_roster = my_new_roster_with_waivers + my_locked
                    if not self._validate_roster(my_full_roster, ignore_max_positions=False):
                        rejection_stats['my_validation_failed'] += 1
                        continue

                    # Validate their team's roster (only if not waivers) - include locked players in validation
                    their_roster_valid = True
                    if not is_waivers:
                        their_full_roster = their_new_roster_with_waivers + their_locked
                        if ignore_max_positions:
                            # Trade suggestor mode: Allow opponent to start with violations, but don't let trade make them worse
                            their_original_roster = their_team.team + their_locked
                            their_roster_valid = self._validate_trade_doesnt_worsen_violations(their_original_roster, their_full_roster)
                        else:
                            # Manual trade mode: Full validation
                            their_roster_valid = self._validate_roster(their_full_roster, ignore_max_positions=False)

                        # If opponent validation fails, try drop variations (opponent receives more players, needs to drop 2)
                        if not their_roster_valid:
                            # 3:1 trade: Opponent gets net +2, so need to drop 2 additional players
                            drop_candidates = self._get_lowest_scored_players_per_position(
                                their_team,
                                exclude_players=[their_player],
                                num_per_position=2
                            )

                            # Try dropping combinations of 2 players
                            for drop_combo in combinations(drop_candidates, 2):
                                # Create roster with drops
                                their_roster_with_drops = [p for p in their_new_roster_with_waivers if p not in drop_combo]
                                their_full_roster_with_drops = their_roster_with_drops + their_locked

                                # Validate with drops
                                if ignore_max_positions:
                                    if not self._validate_trade_doesnt_worsen_violations(their_original_roster, their_full_roster_with_drops):
                                        continue
                                else:
                                    if not self._validate_roster(their_full_roster_with_drops, ignore_max_positions=False):
                                        continue

                                # Create teams with drops included
                                my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers, self.player_manager, isOpponent=False)
                                their_new_team_with_drops = TradeSimTeam(their_team.name, their_roster_with_drops, self.player_manager, isOpponent=True)

                                # Check improvement against ORIGINAL team scores
                                our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
                                their_roster_improved = (their_new_team_with_drops.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT

                                if our_roster_improved and their_roster_improved:
                                    rejection_stats['valid_trades'] += 1
                                    my_original_scored = my_team.get_scored_players(list(my_players))
                                    their_dropped_scored = their_team.get_scored_players(list(drop_combo))

                                    snapshot = TradeSnapshot(
                                        my_new_team=my_new_team,
                                        my_new_players=my_new_team.get_scored_players([their_player]),
                                        their_new_team=their_new_team_with_drops,
                                        their_new_players=their_new_team_with_drops.get_scored_players(list(my_players)),
                                        my_original_players=my_original_scored,
                                        waiver_recommendations=my_waiver_recs,
                                        their_waiver_recommendations=their_waiver_recs,
                                        my_dropped_players=[],
                                        their_dropped_players=their_dropped_scored
                                    )
                                    trade_combos.append(snapshot)

                            # After trying all drops, skip to next trade
                            rejection_stats['their_validation_failed'] += 1
                            continue

                    # Create new TradeSimTeam objects with rosters INCLUDING waiver players
                    my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers, self.player_manager, isOpponent=True)

                    # Check if trade improves both teams based on mode-specific thresholds
                    # NOTE: Team scores now include waiver pickups
                    if is_waivers:
                        # Waiver mode: use MIN_WAIVER_IMPROVEMENT threshold
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_WAIVER_IMPROVEMENT
                        their_roster_improved = True  # Waivers don't have an opponent team
                    else:
                        # Trade suggestor mode: use MIN_TRADE_IMPROVEMENT threshold for both teams
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
                        their_roster_improved = (their_new_team.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT

                    if our_roster_improved and their_roster_improved:
                        rejection_stats['valid_trades'] += 1
                        # Create TradeSnapshot with ScoredPlayer objects
                        my_original_scored = my_team.get_scored_players(list(my_players))

                        snapshot = TradeSnapshot(
                            my_new_team=my_new_team,
                            my_new_players=my_new_team.get_scored_players([their_player]),
                            their_new_team=their_new_team,
                            their_new_players=their_new_team.get_scored_players(list(my_players)),
                            my_original_players=my_original_scored,
                            waiver_recommendations=my_waiver_recs,
                            their_waiver_recommendations=their_waiver_recs
                        )
                        trade_combos.append(snapshot)
                    elif not our_roster_improved and not their_roster_improved:
                        rejection_stats['both_worse'] += 1
                    elif not our_roster_improved:
                        rejection_stats['my_team_worse'] += 1
                    else:
                        rejection_stats['their_team_worse'] += 1

        # Generate 1-for-3 trades (give 1 player, get 3 players)
        if one_for_three:
            # Get all 3-player combinations from their team
            their_combos = list(combinations(their_roster, 3))

            for my_player in my_roster:
                for their_players in their_combos:
                    # Create new rosters after the trade
                    my_new_roster = [p for p in my_roster if p != my_player] + list(their_players)
                    their_new_roster = [p for p in their_roster if p not in their_players] + [my_player]

                    # Calculate waiver recommendations for both teams BEFORE roster validation
                    # 1-for-3: I give 1, get 3 = net +2 (no waiver), they give 3, get 1 = net -2 (they need 2 waivers)
                    my_waiver_recs = []  # I gain roster spots, no waiver needed
                    their_waiver_recs = self._get_waiver_recommendations(num_spots=2) if not is_waivers else []

                    # Add waiver players to rosters for scoring
                    my_new_roster_with_waivers = my_new_roster  # No waivers for me
                    their_new_roster_with_waivers = their_new_roster + [rec.player for rec in their_waiver_recs]

                    # Validate my team's roster (always required) - include locked players in validation
                    my_full_roster = my_new_roster_with_waivers + my_locked
                    my_roster_valid = self._validate_roster(my_full_roster, ignore_max_positions=False)

                    # If validation fails, try drop variations (user receives more players, needs to drop 2)
                    if not my_roster_valid:
                        # 1:3 trade: User gets net +2, so need to drop 2 additional players
                        drop_candidates = self._get_lowest_scored_players_per_position(
                            my_team,
                            exclude_players=[my_player],
                            num_per_position=2
                        )

                        # Try dropping combinations of 2 players
                        for drop_combo in combinations(drop_candidates, 2):
                            # Create roster with drops
                            my_roster_with_drops = [p for p in my_new_roster if p not in drop_combo]
                            my_full_roster_with_drops = my_roster_with_drops + my_locked

                            # Validate with drops
                            if not self._validate_roster(my_full_roster_with_drops, ignore_max_positions=False):
                                continue

                            # Opponent validation (unchanged from original)
                            if not is_waivers:
                                their_full_roster = their_new_roster_with_waivers + their_locked
                                if ignore_max_positions:
                                    their_original_roster = their_team.team + their_locked
                                    if not self._validate_trade_doesnt_worsen_violations(their_original_roster, their_full_roster):
                                        continue
                                else:
                                    if not self._validate_roster(their_full_roster, ignore_max_positions=False):
                                        continue

                            # Create teams with drops included
                            my_new_team_with_drops = TradeSimTeam(my_team.name, my_roster_with_drops, self.player_manager, isOpponent=False)
                            their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers, self.player_manager, isOpponent=True)

                            # Check improvement against ORIGINAL team score
                            if is_waivers:
                                our_roster_improved = (my_new_team_with_drops.team_score - my_team.team_score) >= Constants.MIN_WAIVER_IMPROVEMENT
                                their_roster_improved = True
                            else:
                                our_roster_improved = (my_new_team_with_drops.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
                                their_roster_improved = (their_new_team.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT

                            if our_roster_improved and their_roster_improved:
                                rejection_stats['valid_trades'] += 1
                                my_original_scored = my_team.get_scored_players([my_player])
                                my_dropped_scored = my_team.get_scored_players(list(drop_combo))

                                snapshot = TradeSnapshot(
                                    my_new_team=my_new_team_with_drops,
                                    my_new_players=my_new_team_with_drops.get_scored_players(list(their_players)),
                                    their_new_team=their_new_team,
                                    their_new_players=their_new_team.get_scored_players([my_player]),
                                    my_original_players=my_original_scored,
                                    waiver_recommendations=my_waiver_recs,
                                    their_waiver_recommendations=their_waiver_recs,
                                    my_dropped_players=my_dropped_scored,
                                    their_dropped_players=[]
                                )
                                trade_combos.append(snapshot)

                        # After trying all drops, skip to next trade
                        rejection_stats['my_validation_failed'] += 1
                        continue

                    # Validate their team's roster (only if not waivers) - include locked players in validation
                    if not is_waivers:
                        their_full_roster = their_new_roster_with_waivers + their_locked
                        if ignore_max_positions:
                            # Trade suggestor mode: Allow opponent to start with violations, but don't let trade make them worse
                            their_original_roster = their_team.team + their_locked
                            if not self._validate_trade_doesnt_worsen_violations(their_original_roster, their_full_roster):
                                rejection_stats['their_validation_failed'] += 1
                                continue
                        else:
                            # Manual trade mode: Full validation
                            if not self._validate_roster(their_full_roster, ignore_max_positions=False):
                                rejection_stats['their_validation_failed'] += 1
                                continue

                    # Create new TradeSimTeam objects with rosters INCLUDING waiver players
                    my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers, self.player_manager, isOpponent=True)

                    # Check if trade improves both teams based on mode-specific thresholds
                    # NOTE: Team scores now include waiver pickups
                    if is_waivers:
                        # Waiver mode: use MIN_WAIVER_IMPROVEMENT threshold
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_WAIVER_IMPROVEMENT
                        their_roster_improved = True  # Waivers don't have an opponent team
                    else:
                        # Trade suggestor mode: use MIN_TRADE_IMPROVEMENT threshold for both teams
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
                        their_roster_improved = (their_new_team.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT

                    if our_roster_improved and their_roster_improved:
                        rejection_stats['valid_trades'] += 1
                        # Create TradeSnapshot with ScoredPlayer objects
                        my_original_scored = my_team.get_scored_players([my_player])

                        snapshot = TradeSnapshot(
                            my_new_team=my_new_team,
                            my_new_players=my_new_team.get_scored_players(list(their_players)),
                            their_new_team=their_new_team,
                            their_new_players=their_new_team.get_scored_players([my_player]),
                            my_original_players=my_original_scored,
                            waiver_recommendations=my_waiver_recs,
                            their_waiver_recommendations=their_waiver_recs
                        )
                        trade_combos.append(snapshot)
                    elif not our_roster_improved and not their_roster_improved:
                        rejection_stats['both_worse'] += 1
                    elif not our_roster_improved:
                        rejection_stats['my_team_worse'] += 1
                    else:
                        rejection_stats['their_team_worse'] += 1

        # Generate 3-for-2 trades (give 3 players, get 2 players)
        if three_for_two:
            # Get all 3-player combinations from my team
            my_combos = list(combinations(my_roster, 3))
            # Get all 2-player combinations from their team
            their_combos = list(combinations(their_roster, 2))

            for my_players in my_combos:
                for their_players in their_combos:
                    # Create new rosters after the trade
                    my_new_roster = [p for p in my_roster if p not in my_players] + list(their_players)
                    their_new_roster = [p for p in their_roster if p not in their_players] + list(my_players)

                    # Calculate waiver recommendations for both teams BEFORE roster validation
                    # 3-for-2: I give 3, get 2 = net -1 (I need 1 waiver), they get 3, give 2 = net +1 (no waiver)
                    my_waiver_recs = self._get_waiver_recommendations(num_spots=1)
                    their_waiver_recs = []  # They gain a roster spot, no waiver needed

                    # Add waiver players to rosters for scoring
                    my_new_roster_with_waivers = my_new_roster + [rec.player for rec in my_waiver_recs]
                    their_new_roster_with_waivers = their_new_roster  # No waivers for them

                    # Validate my team's roster (always required) - include locked players in validation
                    my_full_roster = my_new_roster_with_waivers + my_locked
                    if not self._validate_roster(my_full_roster, ignore_max_positions=False):
                        rejection_stats['my_validation_failed'] += 1
                        continue

                    # Validate their team's roster (only if not waivers) - include locked players in validation
                    their_roster_valid = True
                    if not is_waivers:
                        their_full_roster = their_new_roster_with_waivers + their_locked
                        if ignore_max_positions:
                            # Trade suggestor mode: Allow opponent to start with violations, but don't let trade make them worse
                            their_original_roster = their_team.team + their_locked
                            their_roster_valid = self._validate_trade_doesnt_worsen_violations(their_original_roster, their_full_roster)
                        else:
                            # Manual trade mode: Full validation
                            their_roster_valid = self._validate_roster(their_full_roster, ignore_max_positions=False)

                        # If opponent validation fails, try drop variations (opponent receives more players, needs to drop)
                        if not their_roster_valid:
                            # 3:2 trade: Opponent gets net +1, so need to drop 1 additional player
                            drop_candidates = self._get_lowest_scored_players_per_position(
                                their_team,
                                exclude_players=list(their_players),
                                num_per_position=2
                            )

                            # Try dropping each candidate
                            for drop_player in drop_candidates:
                                # Create roster with drop
                                their_roster_with_drop = [p for p in their_new_roster_with_waivers if p != drop_player]
                                their_full_roster_with_drop = their_roster_with_drop + their_locked

                                # Validate with drop
                                if ignore_max_positions:
                                    if not self._validate_trade_doesnt_worsen_violations(their_original_roster, their_full_roster_with_drop):
                                        continue
                                else:
                                    if not self._validate_roster(their_full_roster_with_drop, ignore_max_positions=False):
                                        continue

                                # Create teams with drop included
                                my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers, self.player_manager, isOpponent=False)
                                their_new_team_with_drop = TradeSimTeam(their_team.name, their_roster_with_drop, self.player_manager, isOpponent=True)

                                # Check improvement against ORIGINAL team scores
                                our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
                                their_roster_improved = (their_new_team_with_drop.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT

                                if our_roster_improved and their_roster_improved:
                                    rejection_stats['valid_trades'] += 1
                                    my_original_scored = my_team.get_scored_players(list(my_players))
                                    their_dropped_scored = their_team.get_scored_players([drop_player])

                                    snapshot = TradeSnapshot(
                                        my_new_team=my_new_team,
                                        my_new_players=my_new_team.get_scored_players(list(their_players)),
                                        their_new_team=their_new_team_with_drop,
                                        their_new_players=their_new_team_with_drop.get_scored_players(list(my_players)),
                                        my_original_players=my_original_scored,
                                        waiver_recommendations=my_waiver_recs,
                                        their_waiver_recommendations=their_waiver_recs,
                                        my_dropped_players=[],
                                        their_dropped_players=their_dropped_scored
                                    )
                                    trade_combos.append(snapshot)

                            # After trying all drops, skip to next trade
                            rejection_stats['their_validation_failed'] += 1
                            continue

                    # Create new TradeSimTeam objects with rosters INCLUDING waiver players
                    my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers, self.player_manager, isOpponent=True)

                    # Check if trade improves both teams based on mode-specific thresholds
                    # NOTE: Team scores now include waiver pickups
                    if is_waivers:
                        # Waiver mode: use MIN_WAIVER_IMPROVEMENT threshold
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_WAIVER_IMPROVEMENT
                        their_roster_improved = True  # Waivers don't have an opponent team
                    else:
                        # Trade suggestor mode: use MIN_TRADE_IMPROVEMENT threshold for both teams
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
                        their_roster_improved = (their_new_team.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT

                    if our_roster_improved and their_roster_improved:
                        rejection_stats['valid_trades'] += 1
                        # Create TradeSnapshot with ScoredPlayer objects
                        my_original_scored = my_team.get_scored_players(list(my_players))

                        snapshot = TradeSnapshot(
                            my_new_team=my_new_team,
                            my_new_players=my_new_team.get_scored_players(list(their_players)),
                            their_new_team=their_new_team,
                            their_new_players=their_new_team.get_scored_players(list(my_players)),
                            my_original_players=my_original_scored,
                            waiver_recommendations=my_waiver_recs,
                            their_waiver_recommendations=their_waiver_recs
                        )
                        trade_combos.append(snapshot)
                    elif not our_roster_improved and not their_roster_improved:
                        rejection_stats['both_worse'] += 1
                    elif not our_roster_improved:
                        rejection_stats['my_team_worse'] += 1
                    else:
                        rejection_stats['their_team_worse'] += 1

        # Generate 2-for-3 trades (give 2 players, get 3 players)
        if two_for_three:
            # Get all 2-player combinations from my team
            my_combos = list(combinations(my_roster, 2))
            # Get all 3-player combinations from their team
            their_combos = list(combinations(their_roster, 3))

            for my_players in my_combos:
                for their_players in their_combos:
                    # Create new rosters after the trade
                    my_new_roster = [p for p in my_roster if p not in my_players] + list(their_players)
                    their_new_roster = [p for p in their_roster if p not in their_players] + list(my_players)

                    # Calculate waiver recommendations for both teams BEFORE roster validation
                    # 2-for-3: I give 2, get 3 = net +1 (no waiver), they give 3, get 2 = net -1 (they need 1 waiver)
                    my_waiver_recs = []  # I gain a roster spot, no waiver needed
                    their_waiver_recs = self._get_waiver_recommendations(num_spots=1) if not is_waivers else []

                    # Add waiver players to rosters for scoring
                    my_new_roster_with_waivers = my_new_roster  # No waivers for me
                    their_new_roster_with_waivers = their_new_roster + [rec.player for rec in their_waiver_recs]

                    # Validate my team's roster (always required) - include locked players in validation
                    my_full_roster = my_new_roster_with_waivers + my_locked
                    my_roster_valid = self._validate_roster(my_full_roster, ignore_max_positions=False)

                    # If validation fails, try drop variations (user receives more players, needs to drop)
                    if not my_roster_valid:
                        # 2:3 trade: User gets net +1, so need to drop 1 additional player
                        drop_candidates = self._get_lowest_scored_players_per_position(
                            my_team,
                            exclude_players=list(my_players),
                            num_per_position=2
                        )

                        # Try dropping each candidate
                        for drop_player in drop_candidates:
                            # Create roster with drop
                            my_roster_with_drop = [p for p in my_new_roster if p != drop_player]
                            my_full_roster_with_drop = my_roster_with_drop + my_locked

                            # Validate with drop
                            if not self._validate_roster(my_full_roster_with_drop, ignore_max_positions=False):
                                continue

                            # Opponent validation (unchanged from original)
                            if not is_waivers:
                                their_full_roster = their_new_roster_with_waivers + their_locked
                                if ignore_max_positions:
                                    their_original_roster = their_team.team + their_locked
                                    if not self._validate_trade_doesnt_worsen_violations(their_original_roster, their_full_roster):
                                        continue
                                else:
                                    if not self._validate_roster(their_full_roster, ignore_max_positions=False):
                                        continue

                            # Create teams with drop included
                            my_new_team_with_drop = TradeSimTeam(my_team.name, my_roster_with_drop, self.player_manager, isOpponent=False)
                            their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers, self.player_manager, isOpponent=True)

                            # Check improvement against ORIGINAL team score
                            if is_waivers:
                                our_roster_improved = (my_new_team_with_drop.team_score - my_team.team_score) >= Constants.MIN_WAIVER_IMPROVEMENT
                                their_roster_improved = True
                            else:
                                our_roster_improved = (my_new_team_with_drop.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
                                their_roster_improved = (their_new_team.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT

                            if our_roster_improved and their_roster_improved:
                                rejection_stats['valid_trades'] += 1
                                my_original_scored = my_team.get_scored_players(list(my_players))
                                my_dropped_scored = my_team.get_scored_players([drop_player])

                                snapshot = TradeSnapshot(
                                    my_new_team=my_new_team_with_drop,
                                    my_new_players=my_new_team_with_drop.get_scored_players(list(their_players)),
                                    their_new_team=their_new_team,
                                    their_new_players=their_new_team.get_scored_players(list(my_players)),
                                    my_original_players=my_original_scored,
                                    waiver_recommendations=my_waiver_recs,
                                    their_waiver_recommendations=their_waiver_recs,
                                    my_dropped_players=my_dropped_scored,
                                    their_dropped_players=[]
                                )
                                trade_combos.append(snapshot)

                        # After trying all drops, skip to next trade
                        rejection_stats['my_validation_failed'] += 1
                        continue

                    # Validate their team's roster (only if not waivers) - include locked players in validation
                    if not is_waivers:
                        their_full_roster = their_new_roster_with_waivers + their_locked
                        if ignore_max_positions:
                            # Trade suggestor mode: Allow opponent to start with violations, but don't let trade make them worse
                            their_original_roster = their_team.team + their_locked
                            if not self._validate_trade_doesnt_worsen_violations(their_original_roster, their_full_roster):
                                rejection_stats['their_validation_failed'] += 1
                                continue
                        else:
                            # Manual trade mode: Full validation
                            if not self._validate_roster(their_full_roster, ignore_max_positions=False):
                                rejection_stats['their_validation_failed'] += 1
                                continue

                    # Create new TradeSimTeam objects with rosters INCLUDING waiver players
                    my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers, self.player_manager, isOpponent=True)

                    # Check if trade improves both teams based on mode-specific thresholds
                    # NOTE: Team scores now include waiver pickups
                    if is_waivers:
                        # Waiver mode: use MIN_WAIVER_IMPROVEMENT threshold
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_WAIVER_IMPROVEMENT
                        their_roster_improved = True  # Waivers don't have an opponent team
                    else:
                        # Trade suggestor mode: use MIN_TRADE_IMPROVEMENT threshold for both teams
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
                        their_roster_improved = (their_new_team.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT

                    if our_roster_improved and their_roster_improved:
                        rejection_stats['valid_trades'] += 1
                        # Create TradeSnapshot with ScoredPlayer objects
                        my_original_scored = my_team.get_scored_players(list(my_players))

                        snapshot = TradeSnapshot(
                            my_new_team=my_new_team,
                            my_new_players=my_new_team.get_scored_players(list(their_players)),
                            their_new_team=their_new_team,
                            their_new_players=their_new_team.get_scored_players(list(my_players)),
                            my_original_players=my_original_scored,
                            waiver_recommendations=my_waiver_recs,
                            their_waiver_recommendations=their_waiver_recs
                        )
                        trade_combos.append(snapshot)
                    elif not our_roster_improved and not their_roster_improved:
                        rejection_stats['both_worse'] += 1
                    elif not our_roster_improved:
                        rejection_stats['my_team_worse'] += 1
                    else:
                        rejection_stats['their_team_worse'] += 1

        # Log rejection statistics for teams with 0 valid trades
        if len(trade_combos) == 0:
            total_evaluated = sum(rejection_stats.values())
            self.logger.warning(f"No valid trades found with {their_team.name} - Trade rejection breakdown:")
            self.logger.warning(f"  Total combinations evaluated: {total_evaluated:,}")
            self.logger.warning(f"  My team validation failed: {rejection_stats['my_validation_failed']:,}")
            self.logger.warning(f"  Their team validation failed: {rejection_stats['their_validation_failed']:,}")
            self.logger.warning(f"  My team score worse: {rejection_stats['my_team_worse']:,}")
            self.logger.warning(f"  Their team score worse: {rejection_stats['their_team_worse']:,}")
            self.logger.warning(f"  Both teams worse: {rejection_stats['both_worse']:,}")

        return trade_combos
    
    def save_trades_to_file(self, sorted_trades : List[TradeSnapshot]):
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

                # Add waiver recommendations if trade loses roster spots
                if trade.waiver_recommendations:
                    file.write(f"  Recommended Waiver Adds (for me):\n")
                    for player in trade.waiver_recommendations:
                        file.write(f"    - {player}\n")

                # Add opponent waiver recommendations
                if trade.their_waiver_recommendations:
                    file.write(f"  Recommended Waiver Adds (for {trade.their_new_team.name}):\n")
                    for player in trade.their_waiver_recommendations:
                        file.write(f"    - {player}\n")

                # Add dropped players (beyond the trade itself)
                if trade.my_dropped_players:
                    file.write(f"  Players I Must Drop (to make room):\n")
                    for player in trade.my_dropped_players:
                        file.write(f"    - {player}\n")

                # Add opponent dropped players
                if trade.their_dropped_players:
                    file.write(f"  Players {trade.their_new_team.name} Must Drop (to make room):\n")
                    for player in trade.their_dropped_players:
                        file.write(f"    - {player}\n")

                file.write("\n")  # Adds a blank line between trades

        self.logger.info(f"Trades saved to {filename}")

    def save_waiver_trades_to_file(self, sorted_trades : List[TradeSnapshot]):
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
