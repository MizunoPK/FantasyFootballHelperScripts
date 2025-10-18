"""
Trade Analyzer

Helper class for analyzing and generating trade combinations in Trade Simulator Mode.
Handles roster validation, position counting, and trade combination generation.

Author: Kai Mizuno
"""

import copy
from typing import Dict, List
from itertools import combinations
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).parent))
import constants as Constants

sys.path.append(str(Path(__file__).parent.parent))
from util.PlayerManager import PlayerManager
from util.ConfigManager import ConfigManager
from util.FantasyTeam import FantasyTeam

# Add parent directory to path for utils imports
sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.FantasyPlayer import FantasyPlayer

from trade_simulator_mode.TradeSimTeam import TradeSimTeam
from trade_simulator_mode.TradeSnapshot import TradeSnapshot


class TradeAnalyzer:
    """
    Helper class for analyzing trades and generating trade combinations.

    Provides methods for:
    - Counting position occurrences in rosters
    - Validating roster constraints
    - Generating all valid trade combinations
    """

    def __init__(self, player_manager: PlayerManager, config: ConfigManager) -> None:
        """
        Initialize TradeAnalyzer.

        Args:
            player_manager (PlayerManager): PlayerManager instance with all player data
            config (ConfigManager): Configuration manager
        """
        self.player_manager = player_manager
        self.config = config

    def count_positions(self, roster: List[FantasyPlayer]) -> Dict[str, int]:
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

    def validate_roster(self, roster: List[FantasyPlayer], ignore_max_positions: bool = False) -> bool:
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

    def get_trade_combinations(self, my_team: TradeSimTeam, their_team: TradeSimTeam, is_waivers=False,
                               one_for_one: bool = True, two_for_two: bool = True, three_for_three: bool = False,
                               ignore_max_positions: bool = False) -> List[TradeSnapshot]:
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
        trade_combos: List[TradeSnapshot] = []

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
                    if not self.validate_roster(my_new_roster, ignore_max_positions=ignore_max_positions):
                        continue

                    # Validate their team's roster (only if not waivers)
                    if not is_waivers and not self.validate_roster(their_new_roster, ignore_max_positions=ignore_max_positions):
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
                    if not self.validate_roster(my_new_roster, ignore_max_positions=ignore_max_positions):
                        continue

                    # Validate their team's roster (only if not waivers)
                    if not is_waivers and not self.validate_roster(their_new_roster, ignore_max_positions=ignore_max_positions):
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
                    if not self.validate_roster(my_new_roster, ignore_max_positions=ignore_max_positions):
                        continue

                    # Validate their team's roster (only if not waivers)
                    if not is_waivers and not self.validate_roster(their_new_roster, ignore_max_positions=ignore_max_positions):
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
