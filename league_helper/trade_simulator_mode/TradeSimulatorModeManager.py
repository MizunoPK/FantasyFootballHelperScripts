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

from pathlib import Path
from typing import Dict, List, Tuple

from trade_simulator_mode.TradeSimTeam import TradeSimTeam
from trade_simulator_mode.TradeSnapshot import TradeSnapshot
from trade_simulator_mode.trade_display_helper import TradeDisplayHelper
from trade_simulator_mode.trade_input_parser import TradeInputParser
from trade_simulator_mode.trade_analyzer import TradeAnalyzer
from trade_simulator_mode.trade_file_writer import TradeFileWriter

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
ENABLE_THREE_FOR_THREE = False

# =============================================================================
# UNEQUAL TRADE CONFIGURATION
# =============================================================================
# Toggle unequal trade types (user can modify these)
ENABLE_TWO_FOR_ONE = True    # Give 2 players, get 1 player
ENABLE_ONE_FOR_TWO = True    # Give 1 player, get 2 players
ENABLE_THREE_FOR_ONE = False  # Give 3 players, get 1 player
ENABLE_ONE_FOR_THREE = False  # Give 1 player, get 3 players
ENABLE_THREE_FOR_TWO = False  # Give 3 players, get 2 players
ENABLE_TWO_FOR_THREE = False  # Give 2 players, get 3 players

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
        display_helper (TradeDisplayHelper): Helper for display operations
        input_parser (TradeInputParser): Helper for input parsing
        analyzer (TradeAnalyzer): Helper for trade analysis
        file_writer (TradeFileWriter): Helper for file I/O
    """

    def __init__(self, data_folder: Path, player_manager : PlayerManager, config : ConfigManager) -> None:
        """
        Initialize TradeSimulatorModeManager.

        Args:
            data_folder (Path): Path to data directory containing drafted_data.csv
            player_manager (PlayerManager): PlayerManager instance with all player data
            config (ConfigManager): Configuration manager
        """
        self.logger = get_logger()
        self.data_folder = data_folder
        self.player_manager = player_manager
        self.config = config
        self.team_rosters: Dict[str, List[FantasyPlayer]] = {}

        self.opponent_simulated_teams : List[TradeSimTeam] = []
        self.trade_snapshots : List[TradeSnapshot] = []

        # Initialize helper classes
        self.display_helper = TradeDisplayHelper()
        self.input_parser = TradeInputParser()
        self.analyzer = TradeAnalyzer(player_manager, config)
        self.file_writer = TradeFileWriter()

        self.init_team_data()

    def run_interactive_mode(self) -> None:
        """
        Main interactive loop for Trade Simulator mode.

        Continuously displays menu and processes user selection until user exits.
        Each iteration refreshes team data to reflect any external roster changes.

        Workflow:
        1. Refresh team data
        2. Show mode selection menu
        3. Execute selected mode (Waiver Optimizer / Trade Suggestor / Manual Visualizer)
        4. Save results to file if applicable
        5. Repeat until user selects "Back to Main Menu"
        """
        loop = True
        while (loop):
            # Refresh team data each iteration (in case rosters changed externally)
            self.init_team_data()

            # Show mode selection menu
            choice = show_list_selection("TRADE SIMULATOR", ["Waiver Optimizer", "Trade Suggestor", "Manual Trade Visualizer"], "Back to Main Menu")

            # Execute selected mode and capture results
            # Each mode returns (continue_loop, sorted_trades)
            if choice == 1:
                # Waiver Optimizer: Find best waiver wire pickups
                loop, sorted_trades = self.start_waiver_optimizer()
                mode = "waiver"
            elif choice == 2:
                # Trade Suggestor: Find mutually beneficial trades with opponents
                loop, sorted_trades = self.start_trade_suggestor()
                mode = "trade"
            elif choice == 3:
                # Manual Trade Visualizer: Analyze specific user-proposed trade
                loop, sorted_trades = self.start_manual_trade()
                mode = "manual"
            else:
                # User selected "Back to Main Menu"
                loop, sorted_trades = False, []
                mode = None

            # Save results to file if mode completed successfully with trade data
            if loop and sorted_trades:
                # Use mode-specific save method
                if mode == "waiver":
                    # Waiver file format: DROP/ADD with improvement per trade
                    self.file_writer.save_waiver_trades_to_file(sorted_trades, self.my_team)
                elif mode == "trade":
                    # Trade suggestor file format: numbered trades with both teams' improvements
                    self.file_writer.save_trades_to_file(sorted_trades, self.my_team, self.opponent_simulated_teams)
                # Note: Manual trades are saved within start_manual_trade() method (user prompted for confirmation)

                # Pause before returning to menu
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

        # Get all players from PlayerManager (includes projections, ADPs, and injury data)
        all_players = self.player_manager.players
        self.logger.info(f"Using {len(all_players)} players from PlayerManager")

        # Load drafted data and organize by team
        # drafted_data.csv contains: FantasyTeam, Name, Team, Position, ADP
        drafted_data_csv = self.data_folder / 'drafted_data.csv'

        self.logger.debug(f"Loading drafted data from {drafted_data_csv}")
        roster_manager = DraftedRosterManager(str(drafted_data_csv), Constants.FANTASY_TEAM_NAME)

        if roster_manager.load_drafted_data():
            # Get players organized by team
            # Uses fuzzy matching to match CSV names to FantasyPlayer objects
            self.team_rosters = roster_manager.get_players_by_team(all_players)

            # Log team roster sizes for debugging
            self.logger.info(f"Organized players into {len(self.team_rosters)} team rosters")
            for team_name, roster in self.team_rosters.items():
                self.logger.debug(f"Team '{team_name}': {len(roster)} players")
        else:
            # Failed to load CSV - likely file doesn't exist or malformed
            self.logger.warning("Failed to load drafted data, team rosters will be empty")
            self.team_rosters = {}

        # Create TradeSimTeam objects for scoring and analysis
        # My team uses PlayerManager's roster (already has full player data)
        # isOpponent=False means full scoring (ADP, player rating, team quality, etc.)
        self.my_team = TradeSimTeam(Constants.FANTASY_TEAM_NAME, self.player_manager.team.roster, self.player_manager, isOpponent=False)

        # Reset opponent teams and trade snapshots
        self.opponent_simulated_teams = []
        self.trade_snapshots = []

        # Create TradeSimTeam for each opponent
        # isOpponent=True (default) means simplified scoring (projections only)
        for team_name, team_list in self.team_rosters.items():
            if team_name in Constants.VALID_TEAMS:
                self.opponent_simulated_teams.append(TradeSimTeam(team_name, team_list, self.player_manager))

    
    def start_waiver_optimizer(self) -> Tuple[bool, List[TradeSnapshot]]:
        """
        Find optimal waiver wire pickups by analyzing 1-for-1, 2-for-2, and 3-for-3 trades.

        Returns:
            Tuple[bool, List[TradeSnapshot]]: (True to continue, sorted trades)
        """
        self.logger.info("Starting Waiver Optimizer mode")

        # Get all waiver wire players (drafted=0)
        # Only consider players with scores above our weakest roster players
        # This filters out truly unrosterable players
        lowest_scores = self.player_manager.get_lowest_scores_on_roster()
        waiver_players = self.player_manager.get_player_list(drafted_vals=[0], min_scores=lowest_scores, unlocked_only=True)
        self.logger.info(f"Found {len(waiver_players)} players on waiver wire")

        if not waiver_players:
            print("\nNo players available on waivers.")
            input("\nPress Enter to continue...")
            return True, []

        # Create a TradeSimTeam for the waiver wire
        # Waiver "team" is treated as opponent for scoring purposes
        waiver_team = TradeSimTeam("Waiver Wire", waiver_players, self.player_manager, isOpponent=True)

        # Generate all possible waiver pickups
        # - 1-for-1 and 2-for-2 enabled, 3-for-3 disabled (too many combinations)
        # - is_waivers=True: Skip validation of waiver "team" roster (doesn't apply)
        # - ignore_max_positions=False: MUST respect position limits (real roster constraint)
        self.logger.info("Generating trade combinations...")
        trade_combos = self.analyzer.get_trade_combinations(
            my_team=self.my_team,
            their_team=waiver_team,
            is_waivers=True,
            one_for_one=True,
            two_for_two=True,
            three_for_three=False,  # Disabled: too many combinations
            two_for_one=False,  # Unequal trades disabled in waiver mode for now
            one_for_two=False,
            three_for_one=False,
            one_for_three=False,
            three_for_two=False,
            two_for_three=False,
            ignore_max_positions=False  # Enforce position limits
        )

        self.logger.info(f"Found {len(trade_combos)} valid waiver pickups")

        if not trade_combos:
            print("\nNo valid waiver pickups found that improve your team.")
            input("\nPress Enter to continue...")
            return True, []

        # Sort by improvement (highest improvement first)
        sorted_trades = sorted(
            trade_combos,
            key=lambda t: (t.my_new_team.team_score - self.my_team.team_score),
            reverse=True
        )

        # Display header
        print("\n" + "="*80)
        print("WAIVER OPTIMIZER - Top Pickup Opportunities")
        print("="*80)
        print(f"Current team score: {self.my_team.team_score:.2f}")
        print(f"Found {len(sorted_trades)} beneficial waiver pickups")
        print()

        # Show top N trades (constants define how many to display)
        display_count = min(Constants.NUM_TRADE_RUNNERS_UP + 1, len(sorted_trades))

        # Display each waiver pickup in numbered format
        for i, trade in enumerate(sorted_trades[:display_count], 1):
            # Calculate improvement from trade
            improvement = trade.my_new_team.team_score - self.my_team.team_score

            # Determine trade type label (1-for-1, 2-for-2, etc.)
            num_players = len(trade.my_new_players)
            trade_type = f"{num_players}-for-{num_players}"

            # Display trade header
            print(f"#{i} - {trade_type} Trade - Improvement: +{improvement:.2f} pts")

            # Show players being dropped
            print(f"  DROP:")
            for drop_player in trade.my_original_players:
                print(f"    - {drop_player}")  # ScoredPlayer __str__ shows name, position, team, score

            # Show players being added
            print(f"  ADD:")
            for add_player in trade.my_new_players:
                print(f"    - {add_player}")

            # Show new team score
            print(f"  New team score: {trade.my_new_team.team_score:.2f}")
            print()

        # Pause before returning to menu
        input("\nPress Enter to continue...")
        return True, sorted_trades

    def start_trade_suggestor(self) -> Tuple[bool, List[TradeSnapshot]]:
        """
        Find beneficial trades by analyzing all possible trades with opponent teams.

        Returns:
            Tuple[bool, List[TradeSnapshot]]: (True to continue, sorted trades)
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

            # Get trade combinations with configurable trade types
            # - Uses ENABLE_* constants for flexible configuration
            # - is_waivers=False: Both teams must improve
            # - ignore_max_positions=False: Enforce position limits (BUG FIX from origin/main)
            trade_combos = self.analyzer.get_trade_combinations(
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
                ignore_max_positions=False  # Enforce position limits (BUG FIX)
            )

            elapsed = time.time() - start_time
            all_trades.extend(trade_combos)
            self.logger.info(f"Found {len(trade_combos)} valid trades with {opponent_team.name} in {elapsed:.2f}s ({total_expected/elapsed:.0f} combos/sec)")

        self.logger.info(f"Total trades found: {len(all_trades)}")

        if not all_trades:
            print("\nNo mutually beneficial trades found.")
            return (True, [])

        # Sort by my team's improvement (highest improvement first)
        sorted_trades = sorted(
            all_trades,
            key=lambda t: (t.my_new_team.team_score - self.my_team.team_score),
            reverse=True
        )

        # Display header
        print("\n" + "="*80)
        print("TRADE SUGGESTOR - Top Trade Opportunities")
        print("="*80)
        print(f"Current team score: {self.my_team.team_score:.2f}")
        print(f"Found {len(sorted_trades)} mutually beneficial trades")
        print()

        # Show top N trades (constants define how many to display)
        display_count = min(Constants.NUM_TRADE_RUNNERS_UP + 1, len(sorted_trades))

        # Display each trade showing improvements for BOTH teams
        for i, trade in enumerate(sorted_trades[:display_count], 1):
            # Calculate my improvement
            my_improvement = trade.my_new_team.team_score - self.my_team.team_score

            # Find opponent's original team to calculate their improvement
            original_their_team = None
            for opp in self.opponent_simulated_teams:
                if opp.name == trade.their_new_team.name:
                    original_their_team = opp
                    break

            # Calculate their improvement (0 if team not found)
            their_improvement = trade.their_new_team.team_score - original_their_team.team_score if original_their_team else 0

            # Display trade details
            print(f"#{i} - Trade with {trade.their_new_team.name}")
            print(f"  My improvement: +{my_improvement:.2f} pts (New score: {trade.my_new_team.team_score:.2f})")
            print(f"  Their improvement: +{their_improvement:.2f} pts (New score: {trade.their_new_team.team_score:.2f})")

            # Show players I'm giving away
            print(f"  I give:")
            for player in trade.my_original_players:
                print(f"    - {player}")  # ScoredPlayer __str__ shows name, position, team, score

            # Show players I'm receiving
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

        # Pause before returning to menu
        return True, sorted_trades

    def start_manual_trade(self) -> Tuple[bool, List[TradeSnapshot]]:
        """
        Manual trade visualization mode with unequal trade support.

        Allows user to manually select players for a trade and see the impact.
        Supports equal trades (1-for-1, 2-for-2) and unequal trades (1-for-2, 2-for-1, etc.)
        with automatic waiver recommendations and interactive drop selection.

        Workflow:
        Step 1: Select opponent team to trade with
        Step 2: Display combined roster (both teams numbered sequentially, organized by position/score)
        Step 3: User enters unified selection (e.g., '4,17,18' for 1-for-2 trade)
        Step 4: Process trade with waiver/drop handling
        Step 5: If drops needed, prompt user to select which player(s) to drop

        Returns:
            Tuple[bool, List[TradeSnapshot]]: (True, [trade]) or (True, []) to continue menu loop
        """
        self.logger.info("Starting Manual Trade Visualizer mode")

        # Validate that opponent teams exist
        if len(self.opponent_simulated_teams) == 0:
            print("\nNo opponent teams available for manual trade analysis.")
            self.logger.warning("No opponent teams available")
            return (True, [])

        # ========== STEP 1: Select opponent team ==========
        # Sort teams alphabetically for consistent display
        sorted_teams = sorted(self.opponent_simulated_teams, key=lambda t: t.name)
        opponent_names = [team.name for team in sorted_teams]

        # Show opponent selection menu
        print()
        choice = show_list_selection("SELECT OPPONENT TEAM", opponent_names, "Cancel")

        # Handle cancellation
        if choice > len(opponent_names):
            print("Trade cancelled.")
            self.logger.info("Trade cancelled - no opponent selected")
            return (True, [])

        # Get selected opponent
        opponent = sorted_teams[choice - 1]
        self.logger.info(f"Selected opponent: {opponent.name}")

        # ========== STEP 2-5: Input and processing loop ==========
        # Loop until user provides valid trade or cancels
        my_dropped_players = []
        their_dropped_players = []

        while True:
            # ========== STEP 2: Display combined roster ==========
            # Shows both rosters side-by-side, organized by position and score
            # Returns:
            #   - roster_boundary: Index where opponent's roster starts
            #   - my_display_order: Players from my team sorted by position/score
            #   - their_display_order: Players from their team sorted by position/score
            roster_boundary, my_display_order, their_display_order = self.display_helper.display_combined_roster(
                self.my_team.team,
                opponent.team,
                opponent.name
            )

            # Calculate max valid index for input validation
            max_index = len(self.my_team.team) + len(opponent.team)

            # ========== STEP 3: Get unified player selection ==========
            # User enters comma-separated numbers (e.g., "4,17,18" for 1-for-2 trade)
            print()
            selection_input = input(
                f"Enter player numbers to trade (comma-separated, or 'exit' to cancel): "
            ).strip()

            # Parse input with detailed error messages
            parsed_result, error_message = self.input_parser.parse_with_error_message(
                selection_input,
                max_index,
                roster_boundary
            )

            # Handle cancellation or invalid input
            if parsed_result is None:
                if error_message:
                    print(f"\n{error_message}\n")
                    continue  # Loop back to input prompt
                else:
                    print("Trade cancelled.")
                    self.logger.info("Trade cancelled by user")
                    return (True, [])

            # Extract indices for each team
            my_indices, their_indices = parsed_result

            # Convert indices to actual FantasyPlayer objects
            # IMPORTANT: Use DISPLAY order (sorted by position/score) not original roster order
            my_selected_players = self.input_parser.get_players_by_indices(my_display_order, my_indices)
            their_selected_players = self.input_parser.get_players_by_indices(their_display_order, their_indices)

            # Log trade type
            trade_type = f"{len(my_selected_players)}-for-{len(their_selected_players)}"
            self.logger.info(f"Processing {trade_type} trade")

            # ========== STEP 4: Process trade with shared waiver/drop logic ==========
            # Use TradeAnalyzer's shared method for processing manual trades
            # This handles:
            #   - Calculating waiver needs based on net roster change
            #   - Adding waiver recommendations
            #   - Validating rosters
            #   - Returning drop candidates if roster invalid
            snapshot, my_drop_candidates, their_drop_candidates = self.analyzer.process_manual_trade(
                my_team=self.my_team,
                their_team=opponent,
                my_selected_players=my_selected_players,
                their_selected_players=their_selected_players,
                my_dropped_players=my_dropped_players if my_dropped_players else None,
                their_dropped_players=their_dropped_players if their_dropped_players else None
            )

            # ========== STEP 5: Handle drops if needed ==========
            if snapshot is None:
                # Roster invalid - need to select players to drop
                print("\n" + "="*80)
                print("ROSTER CONSTRAINT VIOLATION")
                print("="*80)

                # Handle MY team drops
                if my_drop_candidates:
                    print("\nYour roster would exceed limits. Select a player to drop:")
                    print()
                    for i, player in enumerate(my_drop_candidates, 1):
                        print(f"  {i}. {player.name} ({player.position}) - {player.team} - Score: {player.score:.2f}")
                    print()

                    while True:
                        drop_input = input("Enter player number to drop (or 'cancel'): ").strip()
                        if drop_input.lower() == 'cancel':
                            print("Trade cancelled.")
                            return (True, [])

                        try:
                            drop_idx = int(drop_input)
                            if 1 <= drop_idx <= len(my_drop_candidates):
                                my_dropped_players = [my_drop_candidates[drop_idx - 1]]
                                self.logger.info(f"User selected to drop: {my_dropped_players[0].name}")
                                break
                            else:
                                print(f"Invalid selection. Please enter a number between 1 and {len(my_drop_candidates)}.")
                        except ValueError:
                            print("Invalid input. Please enter a number.")

                # Handle THEIR team drops (for display purposes)
                if their_drop_candidates:
                    print(f"\n{opponent.name}'s roster would exceed limits. They would need to drop one of:")
                    print()
                    for i, player in enumerate(their_drop_candidates, 1):
                        print(f"  {i}. {player.name} ({player.position}) - {player.team} - Score: {player.score:.2f}")
                    print()

                    while True:
                        drop_input = input("Enter player number they would drop (or 'cancel'): ").strip()
                        if drop_input.lower() == 'cancel':
                            print("Trade cancelled.")
                            return (True, [])

                        try:
                            drop_idx = int(drop_input)
                            if 1 <= drop_idx <= len(their_drop_candidates):
                                their_dropped_players = [their_drop_candidates[drop_idx - 1]]
                                self.logger.info(f"Selected drop for {opponent.name}: {their_dropped_players[0].name}")
                                break
                            else:
                                print(f"Invalid selection. Please enter a number between 1 and {len(their_drop_candidates)}.")
                        except ValueError:
                            print("Invalid input. Please enter a number.")

                # Retry trade processing with selected drops
                print("\nRetrying trade with selected drops...")
                continue

            # ========== Trade valid - break out of loop ==========
            break

        # ========== Display trade results ==========
        # Capture original scores for impact calculation
        original_my_score = self.my_team.team_score
        original_their_score = opponent.team_score

        # Display trade impact analysis (already shows waivers/drops if present)
        self.display_helper.display_trade_result(snapshot, original_my_score, original_their_score)

        # ========== Optionally save to file ==========
        print()
        save_input = input("Save this trade to a file? (y/n): ").strip().lower()

        if save_input == 'y':
            # Save to timestamped file in trade_outputs/
            filename = self.file_writer.save_manual_trade_to_file(snapshot, opponent.name, original_my_score, original_their_score)
            print(f"\nTrade saved to: {filename}")
            self.logger.info(f"Trade saved to {filename}")

        return (True, [snapshot])
