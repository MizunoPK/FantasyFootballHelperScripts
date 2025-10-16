import copy
from pathlib import Path
from typing import Dict, Any, List, Tuple
from itertools import combinations

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
            elif choice == 2:
                loop, sorted_trades = self.start_trade_suggestor()
            elif choice == 3:
                loop, sorted_trades = self.start_manual_trade()
            else:
                loop, sorted_trades = False, []

            if loop:
                # Save to File
                self.save_trades_to_file(sorted_trades)

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
        waiver_players = self.player_manager.get_player_list(drafted_vals=[0], min_scores=lowest_scores)
        self.logger.info(f"Found {len(waiver_players)} players on waiver wire")

        if not waiver_players:
            print("\nNo players available on waivers.")
            input("\nPress Enter to continue...")
            return True, []

        # Create a TradeSimTeam for the waiver wire
        waiver_team = TradeSimTeam("Waiver Wire", waiver_players, self.player_manager, isOpponent=True)

        # Get all possible waiver pickups (1-for-1, 2-for-2, and 3-for-3)
        self.logger.info("Generating trade combinations...")
        trade_combos = self.get_trade_combinations(
            my_team=self.my_team,
            their_team=waiver_team,
            is_waivers=True,
            one_for_one=True,
            two_for_two=True,
            three_for_three=False
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
            for drop_player in trade.their_new_players:
                print(f"    - {drop_player.name} ({drop_player.position}) - {drop_player.team}")
            print(f"  ADD:")
            for add_player in trade.my_new_players:
                print(f"    - {add_player.name} ({add_player.position}) - {add_player.team}")
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
            trade_combos = self.get_trade_combinations(
                my_team=self.my_team,
                their_team=opponent_team,
                is_waivers=False,
                one_for_one=False,
                two_for_two=True,
                three_for_three=False
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
            for player in trade.their_new_players:
                print(f"    - {player.name} ({player.position}) - {player.team}")
            print(f"  I receive:")
            for player in trade.my_new_players:
                print(f"    - {player.name} ({player.position}) - {player.team}")
            print()

        return True, sorted_trades

    def start_manual_trade(self) -> bool:
        return False

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

    def _validate_roster(self, roster: List[FantasyPlayer]) -> bool:
        """
        Validate that a roster meets position limits and total player count.

        Args:
            roster (List[FantasyPlayer]): The roster to validate

        Returns:
            bool: True if roster is valid, False otherwise
        """
        # Check total player count
        if len(roster) > Constants.MAX_PLAYERS:
            return False

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
                               one_for_one : bool = True, two_for_two : bool = True, three_for_three : bool = False) -> List[TradeSnapshot]:
        """
        Generate all valid trade combinations between two teams.

        Args:
            my_team (TradeSimTeam): The user's team
            their_team (TradeSimTeam): The opposing team or waiver wire
            is_waivers (bool): If True, skip position validation for their_team
            one_for_one (bool): If True, generate 1-for-1 trades
            two_for_two (bool): If True, generate 2-for-2 trades
            three_for_three (bool): If True, generate 3-for-3 trades

        Returns:
            List[TradeSnapshot]: List of all valid trade scenarios
        """
        trade_combos : List[TradeSnapshot] = []

        # Get the current rosters
        my_roster = my_team.team
        their_roster = their_team.team

        # Generate 1-for-1 trades
        if one_for_one:
            for my_player in my_roster:
                for their_player in their_roster:
                    # Create new rosters after the trade
                    my_new_roster = [p for p in my_roster if p.id != my_player.id] + [their_player]
                    their_new_roster = [p for p in their_roster if p.id != their_player.id] + [my_player]

                    # Validate my team's roster (always required)
                    if not self._validate_roster(my_new_roster):
                        continue

                    # Validate their team's roster (only if not waivers)
                    if not is_waivers and not self._validate_roster(their_new_roster):
                        continue

                    # Create new TradeSimTeam objects with updated rosters
                    my_new_team = TradeSimTeam(my_team.name, my_new_roster, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster, self.player_manager, isOpponent=True)

                    our_roster_improved = my_new_team.team_score > my_team.team_score
                    their_roster_improved = is_waivers or (their_new_team.team_score > their_team.team_score)

                    if our_roster_improved and their_roster_improved:
                        # Create TradeSnapshot
                        snapshot = TradeSnapshot(
                            my_new_team=my_new_team,
                            my_new_players=[their_player],
                            their_new_team=their_new_team,
                            their_new_players=[my_player]
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
                    if not self._validate_roster(my_new_roster):
                        continue

                    # Validate their team's roster (only if not waivers)
                    if not is_waivers and not self._validate_roster(their_new_roster):
                        continue

                    # Create new TradeSimTeam objects with updated rosters
                    my_new_team = TradeSimTeam(my_team.name, my_new_roster, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster, self.player_manager, isOpponent=True)

                    our_roster_improved = my_new_team.team_score > my_team.team_score
                    their_roster_improved = is_waivers or (their_new_team.team_score > their_team.team_score)

                    if our_roster_improved and their_roster_improved:
                        # Create TradeSnapshot
                        snapshot = TradeSnapshot(
                            my_new_team=my_new_team,
                            my_new_players=list(their_players),
                            their_new_team=their_new_team,
                            their_new_players=list(my_players)
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
                    if not self._validate_roster(my_new_roster):
                        continue

                    # Validate their team's roster (only if not waivers)
                    if not is_waivers and not self._validate_roster(their_new_roster):
                        continue

                    # Create new TradeSimTeam objects with updated rosters
                    my_new_team = TradeSimTeam(my_team.name, my_new_roster, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster, self.player_manager, isOpponent=True)

                    our_roster_improved = my_new_team.team_score > my_team.team_score
                    their_roster_improved = is_waivers or (their_new_team.team_score > their_team.team_score)

                    if our_roster_improved and their_roster_improved:
                        # Create TradeSnapshot
                        snapshot = TradeSnapshot(
                            my_new_team=my_new_team,
                            my_new_players=list(their_players),
                            their_new_team=their_new_team,
                            their_new_players=list(my_players)
                        )
                        trade_combos.append(snapshot)

        return trade_combos
    
    def save_trades_to_file(self, sorted_trades : List[TradeSnapshot]):
        # Open the file in write mode (it will create the file if it doesn't exist)
        with open('./league_helper/trade_simulator_mode/trade_info.txt', 'w') as file:
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
                
                for player in trade.their_new_players:
                    file.write(f"    - {player.name} ({player.position}) - {player.team}\n")
                
                file.write(f"  I receive:\n")
                for player in trade.my_new_players:
                    file.write(f"    - {player.name} ({player.position}) - {player.team}\n")
                
                file.write("\n")  # Adds a blank line between trades
