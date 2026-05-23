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
from typing import Dict, List, Tuple, Optional

from league_helper.trade_simulator_mode.TradeSimTeam import TradeSimTeam
from league_helper.trade_simulator_mode.TradeSnapshot import TradeSnapshot
from league_helper.trade_simulator_mode.trade_display_helper import TradeDisplayHelper
from league_helper.trade_simulator_mode.trade_input_parser import TradeInputParser
from league_helper.trade_simulator_mode.trade_analyzer import TradeAnalyzer
from league_helper.trade_simulator_mode.trade_file_writer import TradeFileWriter
import league_helper.constants as Constants
from league_helper.util.user_input import show_list_selection
from league_helper.util.PlayerManager import PlayerManager
from league_helper.util.ConfigManager import ConfigManager
from league_helper.util.ScoredPlayer import ScoredPlayer
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
        data_folder (Path): Path to data directory containing players.json
        player_manager (PlayerManager): PlayerManager instance with all player data (including drafted_by field)
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
            data_folder (Path): Path to data directory containing players.json
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
            self.init_team_data()

            choice = show_list_selection("TRADE SIMULATOR", ["Waiver Optimizer", "Trade Suggestor", "Manual Trade Visualizer"], "Back to Main Menu")

            my_team_for_file = None
            if choice == 1:
                loop, sorted_trades, mode_name, my_team_for_file = self.start_waiver_optimizer()
                mode = "waiver"
            elif choice == 2:
                loop, sorted_trades = self.start_trade_suggestor()
                mode = "trade"
                mode_name = ""
            elif choice == 3:
                loop, sorted_trades = self.start_manual_trade()
                mode = "manual"
                mode_name = ""
            else:
                loop, sorted_trades = False, []
                mode = None
                mode_name = ""

            if loop and sorted_trades:
                if mode == "waiver":
                    team_for_file = my_team_for_file if my_team_for_file else self.my_team
                    self.file_writer.save_waiver_trades_to_file(sorted_trades, team_for_file, mode_name)
                elif mode == "trade":
                    self.file_writer.save_trades_to_file(sorted_trades, self.my_team, self.opponent_simulated_teams)

                input("Press enter to continue...")

    def init_team_data(self) -> None:
        """
        Initialize team roster data by organizing players by fantasy team.

        Uses the PlayerManager's player list to:
        1. Reload player data from JSON (resets any state changes from previous simulations)
        2. Organize players by drafted_by field (team name)
        3. Create team_rosters dict mapping team names to player lists

        Side Effects:
            - Reloads all player data from JSON (resets drafted, locked, score state)
            - Populates self.team_rosters with Dict[team_name, List[FantasyPlayer]]
        """
        self.player_manager.reload_player_data()

        all_players = self.player_manager.players
        self.logger.info(f"Using {len(all_players)} players from PlayerManager")

        self.team_rosters = self.player_manager.get_players_by_team()

        self.logger.info(f"Organized players into {len(self.team_rosters)} team rosters")

        self.my_team = TradeSimTeam(Constants.FANTASY_TEAM_NAME, self.player_manager.team.roster, self.player_manager, isOpponent=False)

        self.opponent_simulated_teams = []
        self.trade_snapshots = []

        for team_name, team_list in self.team_rosters.items():
            if team_name in Constants.VALID_TEAMS:
                self.opponent_simulated_teams.append(TradeSimTeam(team_name, team_list, self.player_manager))

    
    def start_waiver_optimizer(self) -> Tuple[bool, List[TradeSnapshot], str, Optional[TradeSimTeam]]:
        """
        Find optimal waiver wire pickups by analyzing 1-for-1, 2-for-2, and 3-for-3 trades.

        Prompts user to select between:
        - Rest of Season: Seasonal projections with standard multipliers
        - Current Week: Weekly projections matching Starter Helper scoring

        Returns:
            Tuple[bool, List[TradeSnapshot], str, Optional[TradeSimTeam]]:
                - bool: True to loop back to menu, False to exit
                - List[TradeSnapshot]: Sorted trade recommendations
                - str: Mode name for file output ("Rest of Season" or "Current Week")
                - Optional[TradeSimTeam]: My team with mode-specific scoring (for file output)
        """
        self.logger.info("Starting Waiver Optimizer mode")

        mode_choice = show_list_selection(
            "WAIVER OPTIMIZER - SELECT MODE",
            ["Rest of Season", "Current Week"],
            "Cancel"
        )

        if mode_choice > 2:
            self.logger.info("User cancelled Waiver Optimizer")
            return True, [], "", None

        use_weekly_scoring = (mode_choice == 2)
        mode_name = "Current Week" if use_weekly_scoring else "Rest of Season"
        self.logger.info(f"Waiver Optimizer mode selected: {mode_name}")

        if use_weekly_scoring:
            max_weekly = self.player_manager.calculate_max_weekly_projection(
                self.config.current_nfl_week
            )
            self.player_manager.scoring_calculator.max_weekly_projection = max_weekly
            self.logger.info(
                f"Set max_weekly_projection to {max_weekly:.2f} for week {self.config.current_nfl_week}"
            )

        lowest_scores = self.player_manager.get_lowest_scores_on_roster()
        for pos, score in lowest_scores.items():
            lowest_scores[pos] = score + Constants.MIN_WAIVER_IMPROVEMENT
        waiver_players = self.player_manager.get_player_list(drafted_vals=[0], min_scores=lowest_scores, unlocked_only=True)
        self.logger.info(f"Found {len(waiver_players)} players on waiver wire")

        if not waiver_players:
            print("\nNo players available on waivers.")
            return True, [], mode_name, None

        my_team = TradeSimTeam(
            Constants.FANTASY_TEAM_NAME,
            self.player_manager.team.roster,
            self.player_manager,
            isOpponent=False,
            use_weekly_scoring=use_weekly_scoring
        )

        waiver_team = TradeSimTeam(
            "Waiver Wire",
            waiver_players,
            self.player_manager,
            isOpponent=True,
            use_weekly_scoring=use_weekly_scoring
        )

        self.logger.info("Generating trade combinations...")
        trade_combos = self.analyzer.get_trade_combinations(
            my_team=my_team,
            their_team=waiver_team,
            is_waivers=True,
            one_for_one=True,
            two_for_two=self.config.trade_waivers_two_for_two,
            three_for_three=self.config.trade_waivers_three_for_three,
            two_for_one=False,
            one_for_two=False,
            three_for_one=False,
            one_for_three=False,
            three_for_two=False,
            two_for_three=False,
            ignore_max_positions=False
        )

        self.logger.info(f"Found {len(trade_combos)} valid waiver pickups")

        if not trade_combos:
            print("\nNo valid waiver pickups found that improve your team.")
            return True, [], mode_name, None

        sorted_trades = sorted(
            trade_combos,
            key=lambda t: (t.my_new_team.team_score - my_team.team_score),
            reverse=True
        )

        print("\n" + "="*80)
        print(f"WAIVER OPTIMIZER - {mode_name.upper()}")
        print("="*80)
        print(f"Current team score: {my_team.team_score:.2f}")
        print(f"Found {len(sorted_trades)} beneficial waiver pickups")
        print()

        display_count = min(Constants.NUM_TRADE_RUNNERS_UP + 1, len(sorted_trades))

        for i, trade in enumerate(sorted_trades[:display_count], 1):
            improvement = trade.my_new_team.team_score - my_team.team_score

            num_players = len(trade.my_new_players)
            trade_type = f"{num_players}-for-{num_players}"

            sign = "+" if improvement >= 0 else ""
            print(f"#{i} - {trade_type} Trade - Improvement: {sign}{improvement:.2f} pts")

            print(f"  DROP:")
            for drop_player in trade.my_original_players:
                print(f"    - {drop_player}")

            print(f"  ADD:")
            for add_player in trade.my_new_players:
                print(f"    - {add_player}")

            print(f"  New team score: {trade.my_new_team.team_score:.2f}")
            print()

        return True, sorted_trades, mode_name, my_team

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

        teams_over_limit = []

        if len(self.my_team.team) > self.config.max_players:
            teams_over_limit.append((self.my_team.name, self.my_team.team))

        for opp_team in self.opponent_simulated_teams:
            if len(opp_team.team) > self.config.max_players:
                teams_over_limit.append((opp_team.name, opp_team.team))

        if teams_over_limit:
            self.logger.warning("=" * 80)
            self.logger.warning(f"ROSTER SIZE WARNING: {len(teams_over_limit)} team(s) exceed MAX_PLAYERS ({self.config.max_players})")
            self.logger.warning("=" * 80)

            for team_name, roster in teams_over_limit:
                player_names = [p.name for p in sorted(roster, key=lambda p: p.position)]
                self.logger.warning(f"\n{team_name}: {len(roster)} active players")
                self.logger.warning(f"  Players: {', '.join(player_names)}")

            self.logger.warning("=" * 80 + "\n")

        self.logger.info("=" * 80)
        self.logger.info("BEGINNING TRADE ANALYSIS")
        self.logger.info(f"My Team: {self.my_team.name} (Score: {self.my_team.team_score:.2f})")
        self.logger.info(f"Opponent Teams: {len(self.opponent_simulated_teams)}")
        self.logger.info("=" * 80 + "\n")

        all_trades = []

        print("\nAnalyzing trades with opponent teams...")
        import time
        for opponent_team in self.opponent_simulated_teams:
            start_time = time.time()

            my_unlocked = len([p for p in self.my_team.team if p.locked != 1])
            their_unlocked = len([p for p in opponent_team.team if p.locked != 1])

            one_for_one_combos = my_unlocked * their_unlocked
            two_for_two_combos = (my_unlocked * (my_unlocked - 1) // 2) * (their_unlocked * (their_unlocked - 1) // 2)

            two_for_one_combos = (my_unlocked * (my_unlocked - 1) // 2) * their_unlocked if self.config.trade_enable_two_for_one else 0
            one_for_two_combos = my_unlocked * (their_unlocked * (their_unlocked - 1) // 2) if self.config.trade_enable_one_for_two else 0
            three_for_one_combos = (my_unlocked * (my_unlocked - 1) * (my_unlocked - 2) // 6) * their_unlocked if self.config.trade_enable_three_for_one else 0
            one_for_three_combos = my_unlocked * (their_unlocked * (their_unlocked - 1) * (their_unlocked - 2) // 6) if self.config.trade_enable_one_for_three else 0
            three_for_two_combos = (my_unlocked * (my_unlocked - 1) * (my_unlocked - 2) // 6) * (their_unlocked * (their_unlocked - 1) // 2) if self.config.trade_enable_three_for_two else 0
            two_for_three_combos = (my_unlocked * (my_unlocked - 1) // 2) * (their_unlocked * (their_unlocked - 1) * (their_unlocked - 2) // 6) if self.config.trade_enable_two_for_three else 0

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

            trade_combos = self.analyzer.get_trade_combinations(
                my_team=self.my_team,
                their_team=opponent_team,
                is_waivers=False,
                one_for_one=self.config.trade_enable_one_for_one,
                two_for_two=self.config.trade_enable_two_for_two,
                three_for_three=self.config.trade_enable_three_for_three,
                two_for_one=self.config.trade_enable_two_for_one,
                one_for_two=self.config.trade_enable_one_for_two,
                three_for_one=self.config.trade_enable_three_for_one,
                one_for_three=self.config.trade_enable_one_for_three,
                three_for_two=self.config.trade_enable_three_for_two,
                two_for_three=self.config.trade_enable_two_for_three,
                ignore_max_positions=False
            )

            elapsed = time.time() - start_time
            all_trades.extend(trade_combos)
            self.logger.info(f"Found {len(trade_combos)} valid trades with {opponent_team.name} in {elapsed:.2f}s ({total_expected/elapsed:.0f} combos/sec)")

        self.logger.info(f"Total trades found: {len(all_trades)}")

        if not all_trades:
            print("\nNo mutually beneficial trades found.")
            return (True, [])

        sorted_trades = sorted(
            all_trades,
            key=lambda t: (t.my_new_team.team_score - self.my_team.team_score),
            reverse=True
        )

        print("\n" + "="*80)
        print("TRADE SUGGESTOR - Top Trade Opportunities")
        print("="*80)
        print(f"Current team score: {self.my_team.team_score:.2f}")
        print(f"Found {len(sorted_trades)} mutually beneficial trades")
        print()

        display_count = min(Constants.NUM_TRADE_RUNNERS_UP + 1, len(sorted_trades))

        for i, trade in enumerate(sorted_trades[:display_count], 1):
            my_improvement = trade.my_new_team.team_score - self.my_team.team_score

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
            for player in trade.my_original_players:
                print(f"    - {player}")

            print(f"  I receive:")
            for player in trade.my_new_players:
                print(f"    - {player}")

            if trade.waiver_recommendations:
                print(f"  Recommended Waiver Adds (for me):")
                for player in trade.waiver_recommendations:
                    print(f"    - {player}")

            if trade.their_waiver_recommendations:
                print(f"  Recommended Waiver Adds (for {trade.their_new_team.name}):")
                for player in trade.their_waiver_recommendations:
                    print(f"    - {player}")

            if trade.my_dropped_players:
                print(f"  Players I Must Drop (to make room):")
                for player in trade.my_dropped_players:
                    print(f"    - {player}")

            if trade.their_dropped_players:
                print(f"  Players {trade.their_new_team.name} Must Drop (to make room):")
                for player in trade.their_dropped_players:
                    print(f"    - {player}")

            print()

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

        if len(self.opponent_simulated_teams) == 0:
            print("\nNo opponent teams available for manual trade analysis.")
            self.logger.warning("No opponent teams available")
            return (True, [])

        lowest_scores = self.player_manager.get_lowest_scores_on_roster()
        for pos, score in lowest_scores.items():
            lowest_scores[pos] = score + Constants.MIN_WAIVER_IMPROVEMENT
        waiver_players = self.player_manager.get_player_list(drafted_vals=[0], min_scores=lowest_scores, unlocked_only=True)
        waiver_count = len(waiver_players)
        self.logger.info(f"Found {waiver_count} waiver players (filtered by MIN_WAIVER_IMPROVEMENT)")

        sorted_teams = sorted(self.opponent_simulated_teams, key=lambda t: t.name)
        opponent_names = [team.name for team in sorted_teams]

        opponent_names.append(f"Waiver ({waiver_count} players)")

        print()
        choice = show_list_selection("SELECT OPPONENT TEAM", opponent_names, "Cancel")

        if choice > len(opponent_names):
            print("Trade cancelled.")
            self.logger.info("Trade cancelled - no opponent selected")
            return (True, [])

        if choice == len(opponent_names):
            if waiver_count == 0:
                print("\nNo players available on waivers.")
                self.logger.warning("No waiver players available")
                return (True, [])

            opponent = TradeSimTeam("Waiver Wire", waiver_players, self.player_manager, isOpponent=True)
            is_waivers = True
            self.logger.info("Selected Waiver Wire for manual trade")
        else:
            opponent = sorted_teams[choice - 1]
            is_waivers = False
            self.logger.info(f"Selected opponent: {opponent.name}")

        my_dropped_players = []
        their_dropped_players = []
        my_selected_players = None
        their_selected_players = None

        while True:
            roster_boundary, my_display_order, their_display_order = self.display_helper.display_combined_roster(
                self.my_team.team,
                opponent.team,
                opponent.name
            )

            if my_selected_players is None:
                max_index = len(self.my_team.team) + len(opponent.team)

                print()
                selection_input = input(
                    f"Enter player numbers to trade (comma-separated, or 'exit' to cancel): "
                ).strip()

                parsed_result, error_message = self.input_parser.parse_with_error_message(
                    selection_input,
                    max_index,
                    roster_boundary
                )

                if parsed_result is None:
                    if error_message:
                        print(f"\n{error_message}\n")
                        continue
                    else:
                        print("Trade cancelled.")
                        self.logger.info("Trade cancelled by user")
                        return (True, [])

                my_indices, their_indices = parsed_result

                my_selected_players = self.input_parser.get_players_by_indices(my_display_order, my_indices)
                their_selected_players = self.input_parser.get_players_by_indices(their_display_order, their_indices)

                trade_type = f"{len(my_selected_players)}-for-{len(their_selected_players)}"
                self.logger.info(f"Processing {trade_type} trade")
            else:
                self.logger.info("Retrying trade with previously selected players and new drops")

            snapshot, my_drop_candidates, their_drop_candidates = self.analyzer.process_manual_trade(
                my_team=self.my_team,
                their_team=opponent,
                my_selected_players=my_selected_players,
                their_selected_players=their_selected_players,
                my_dropped_players=my_dropped_players if my_dropped_players else None,
                their_dropped_players=their_dropped_players if their_dropped_players else None,
                is_waivers=is_waivers
            )

            if snapshot is None:
                print("\n" + "="*80)
                print("ROSTER CONSTRAINT VIOLATION")
                print("="*80)

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

                print("\nRetrying trade with selected drops...")
                continue

            break

        original_my_score = self.my_team.team_score
        original_their_score = opponent.team_score

        self.display_helper.display_trade_result(snapshot, original_my_score, original_their_score)

        print()
        save_input = input("Save this trade to a file? (y/n): ").strip().lower()

        if save_input == 'y':
            filename = self.file_writer.save_manual_trade_to_file(snapshot, opponent.name, original_my_score, original_their_score)
            print(f"\nTrade saved to: {filename}")
            self.logger.info(f"Trade saved to {filename}")

            try:
                excel_filename = self.file_writer.save_manual_trade_to_excel(
                    snapshot,
                    opponent.name,
                    original_my_score,
                    original_their_score,
                    self.my_team,
                    opponent
                )
                print(f"Excel file saved: {excel_filename}")
                self.logger.info(f"Excel file saved to {excel_filename}")
            except Exception as e:
                self.logger.error(f"Failed to save Excel file: {e}", exc_info=True)
                print("Note: Excel file could not be created (txt file saved successfully)")

        return (True, [snapshot])


