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
from utils.LoggingManager import get_logger

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
        self.logger = get_logger()

    def count_positions(self, roster: List[FantasyPlayer]) -> Dict[str, int]:
        """
        Count the number of players at each position in a roster.

        Args:
            roster (List[FantasyPlayer]): The roster to count

        Returns:
            Dict[str, int]: Dictionary mapping position to count
        """
        # Initialize counter for all positions (QB, RB, WR, TE, K, DST) to 0
        position_counts = {pos: 0 for pos in Constants.MAX_POSITIONS.keys()}

        # Count each player by their position
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
        # STEP 1: Check total player count doesn't exceed league maximum (15 players)
        # This is always enforced regardless of mode
        if len(roster) > Constants.MAX_PLAYERS:
            return False

        # STEP 2: If manual trade mode, only enforce total roster size
        # Manual trades allow creative position arrangements as long as total count is valid
        # This gives user flexibility to optimize their roster manually
        if ignore_max_positions:
            return True

        # STEP 3: Validate position limits using FantasyTeam's draft logic
        # This ensures the roster doesn't violate position maximums (2 QB, 4 RB, 6 WR, etc.)
        # We create a test team and attempt to draft each player
        test_team = FantasyTeam(self.config, [])
        for p in roster:
            # Deep copy to avoid modifying original player
            p_copy = copy.deepcopy(p)
            # Mark as undrafted so FantasyTeam will accept it
            p_copy.drafted = 0
            # Try to draft the player - will fail if position limit exceeded
            drafted = test_team.draft_player(p_copy)
            if not drafted:
                # Player couldn't be added (position limit exceeded)
                return False

        # All players successfully added to test team - roster is valid
        return True

    def get_trade_combinations(self, my_team: TradeSimTeam, their_team: TradeSimTeam, is_waivers=False,
                               one_for_one: bool = True, two_for_two: bool = True, three_for_three: bool = False,
                               ignore_max_positions: bool = False) -> List[TradeSnapshot]:
        """
        Generate all valid trade combinations between two teams.

        This method exhaustively generates all possible trade combinations based on the
        requested trade types (1-for-1, 2-for-2, 3-for-3) and filters them by:
        1. Roster validity (position limits and total player count)
        2. Mutual improvement (both teams must score higher after the trade)

        The method handles three modes:
        - Waiver Optimizer: is_waivers=True, only user team needs to improve
        - Trade Suggestor: is_waivers=False, both teams must improve (enforce position limits)
        - Manual Visualizer: ignore_max_positions=True, allow creative trades

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
        # Log trade generation start with configuration
        mode = "Waiver Optimizer" if is_waivers else "Trade Suggestor"
        self.logger.info(f"Generating trade combinations ({mode}): 1-for-1={one_for_one}, 2-for-2={two_for_two}, 3-for-3={three_for_three}")

        # Initialize list to store all valid trades
        trade_combos: List[TradeSnapshot] = []

        # ===== LOCKED PLAYER HANDLING (BUG FIX) =====
        # Separate locked players from tradeable players on both teams
        # Locked players (player.locked == 1) cannot be included in trades
        # BUT they must be included when validating roster position limits
        # This prevents trades that would violate position limits when accounting for locked players
        #
        # Example: If user has 2 QB and 1 is locked, they can only trade for max 1 QB
        # even though they're only trading 1 QB away, because locked QB still counts toward limit
        my_roster = [p for p in my_team.team if p.locked != 1]  # Tradeable players only
        my_locked = [p for p in my_team.team if p.locked == 1]  # Locked players (not tradeable)
        their_roster = [p for p in their_team.team if p.locked != 1]  # Tradeable players only
        their_locked = [p for p in their_team.team if p.locked == 1]  # Locked players (not tradeable)

        # Log locked player filtering results
        self.logger.debug(f"Filtered rosters: my_tradeable={len(my_roster)}, my_locked={len(my_locked)}, their_tradeable={len(their_roster)}, their_locked={len(their_locked)}")

        # ===== GENERATE 1-FOR-1 TRADES =====
        # Try every combination of swapping 1 player from my team with 1 player from their team
        if one_for_one:
            for my_player in my_roster:  # Iterate through all MY tradeable players
                for their_player in their_roster:  # Iterate through all THEIR tradeable players

                    # STEP 1: Create hypothetical rosters after the trade
                    # Remove the player we're giving away and add the player we're receiving
                    my_new_roster = [p for p in my_roster if p.id != my_player.id] + [their_player]
                    their_new_roster = [p for p in their_roster if p.id != their_player.id] + [my_player]

                    # STEP 2: Validate MY team's roster (always required)
                    # Add locked players to get full roster for position limit validation
                    # Locked players count toward position limits even though they weren't traded
                    my_full_roster = my_new_roster + my_locked
                    if not self.validate_roster(my_full_roster, ignore_max_positions=ignore_max_positions):
                        # Trade would violate position limits or roster size - skip this combination
                        continue

                    # STEP 3: Validate THEIR team's roster (only if not waiver mode)
                    # Waiver wire doesn't have position limits, so skip validation
                    # For regular trades, ensure their roster remains valid too
                    if not is_waivers:
                        their_full_roster = their_new_roster + their_locked
                        if not self.validate_roster(their_full_roster, ignore_max_positions=ignore_max_positions):
                            # Trade would violate opponent's position limits - skip this combination
                            continue

                    # STEP 4: Score the new rosters and check for mutual improvement
                    # Create new TradeSimTeam objects which automatically score the rosters
                    # isOpponent=False for user team (uses full scoring: ADP, rating, team quality, bye, etc.)
                    # isOpponent=True for opponent team (uses simplified scoring: projections + rating only)
                    my_new_team = TradeSimTeam(my_team.name, my_new_roster, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster, self.player_manager, isOpponent=True)

                    # Check if trade improves both teams' scores
                    our_roster_improved = my_new_team.team_score > my_team.team_score
                    # For waivers: their roster doesn't need to improve (we're just adding from free agents)
                    # For regular trades: both teams must improve (mutually beneficial)
                    their_roster_improved = is_waivers or (their_new_team.team_score > their_team.team_score)

                    # STEP 5: If trade is mutually beneficial, create and store TradeSnapshot
                    if our_roster_improved and their_roster_improved:
                        # Get ScoredPlayer objects with full scoring details for display
                        # IMPORTANT: Get original scores from ORIGINAL team context (before trade)
                        # This shows the true value we're giving up
                        my_original_scored = my_team.get_scored_players([my_player])

                        # Create snapshot with all trade details
                        # New players are scored in NEW team context (after trade)
                        # This shows their value in the new roster composition
                        snapshot = TradeSnapshot(
                            my_new_team=my_new_team,  # My team after trade
                            my_new_players=my_new_team.get_scored_players([their_player]),  # Player I receive
                            their_new_team=their_new_team,  # Their team after trade
                            their_new_players=their_new_team.get_scored_players([my_player]),  # Player they receive
                            my_original_players=my_original_scored  # Player I give up (original score)
                        )
                        trade_combos.append(snapshot)

        # ===== GENERATE 2-FOR-2 TRADES =====
        # Same workflow as 1-for-1, but with 2 players swapped from each team
        # This allows for more complex trades (e.g., QB+RB for WR+TE)
        if two_for_two:
            # Generate all possible 2-player combinations from each team
            # combinations(roster, 2) returns all unique pairs (no duplicates, no order)
            my_combos = list(combinations(my_roster, 2))
            their_combos = list(combinations(their_roster, 2))

            # Try every 2-player combination from my team vs every 2-player combination from their team
            for my_players in my_combos:
                for their_players in their_combos:
                    # Create hypothetical rosters (remove 2 players, add 2 players)
                    my_new_roster = [p for p in my_roster if p not in my_players] + list(their_players)
                    their_new_roster = [p for p in their_roster if p not in their_players] + list(my_players)

                    # Validate rosters (include locked players in position limit check)
                    my_full_roster = my_new_roster + my_locked
                    if not self.validate_roster(my_full_roster, ignore_max_positions=ignore_max_positions):
                        continue

                    if not is_waivers:
                        their_full_roster = their_new_roster + their_locked
                        if not self.validate_roster(their_full_roster, ignore_max_positions=ignore_max_positions):
                            continue

                    # Score rosters and check for mutual improvement
                    my_new_team = TradeSimTeam(my_team.name, my_new_roster, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster, self.player_manager, isOpponent=True)

                    our_roster_improved = my_new_team.team_score > my_team.team_score
                    their_roster_improved = is_waivers or (their_new_team.team_score > their_team.team_score)

                    # Store mutually beneficial trades
                    if our_roster_improved and their_roster_improved:
                        # Get original scores for the 2 players we're giving up
                        my_original_scored = my_team.get_scored_players(list(my_players))

                        # Create snapshot (new players scored in new team context)
                        snapshot = TradeSnapshot(
                            my_new_team=my_new_team,
                            my_new_players=my_new_team.get_scored_players(list(their_players)),
                            their_new_team=their_new_team,
                            their_new_players=their_new_team.get_scored_players(list(my_players)),
                            my_original_players=my_original_scored
                        )
                        trade_combos.append(snapshot)

        # ===== GENERATE 3-FOR-3 TRADES =====
        # Same workflow as 1-for-1 and 2-for-2, but with 3 players swapped from each team
        # Allows for very complex multi-player blockbuster trades
        # NOTE: Often disabled due to computational complexity (n^2 combinations)
        if three_for_three:
            # Generate all possible 3-player combinations from each team
            my_combos = list(combinations(my_roster, 3))
            their_combos = list(combinations(their_roster, 3))

            # Try every 3-player combination from my team vs every 3-player combination from their team
            for my_players in my_combos:
                for their_players in their_combos:
                    # Create hypothetical rosters (remove 3 players, add 3 players)
                    my_new_roster = [p for p in my_roster if p not in my_players] + list(their_players)
                    their_new_roster = [p for p in their_roster if p not in their_players] + list(my_players)

                    # Validate rosters (include locked players in position limit check)
                    my_full_roster = my_new_roster + my_locked
                    if not self.validate_roster(my_full_roster, ignore_max_positions=ignore_max_positions):
                        continue

                    if not is_waivers:
                        their_full_roster = their_new_roster + their_locked
                        if not self.validate_roster(their_full_roster, ignore_max_positions=ignore_max_positions):
                            continue

                    # Score rosters and check for mutual improvement
                    my_new_team = TradeSimTeam(my_team.name, my_new_roster, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster, self.player_manager, isOpponent=True)

                    our_roster_improved = my_new_team.team_score > my_team.team_score
                    their_roster_improved = is_waivers or (their_new_team.team_score > their_team.team_score)

                    # Store mutually beneficial trades
                    if our_roster_improved and their_roster_improved:
                        # Get original scores for the 3 players we're giving up
                        my_original_scored = my_team.get_scored_players(list(my_players))

                        # Create snapshot (new players scored in new team context)
                        snapshot = TradeSnapshot(
                            my_new_team=my_new_team,
                            my_new_players=my_new_team.get_scored_players(list(their_players)),
                            their_new_team=their_new_team,
                            their_new_players=their_new_team.get_scored_players(list(my_players)),
                            my_original_players=my_original_scored
                        )
                        trade_combos.append(snapshot)

        # Log trade generation completion with result count
        self.logger.info(f"Generated {len(trade_combos)} valid trade combinations")

        # Return all valid trades found
        return trade_combos
