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
from util.ScoredPlayer import ScoredPlayer

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

    def get_trade_combinations(self, my_team: TradeSimTeam, their_team: TradeSimTeam, is_waivers=False,
                               one_for_one: bool = True, two_for_two: bool = True, three_for_three: bool = False,
                               two_for_one: bool = False, one_for_two: bool = False,
                               three_for_one: bool = False, one_for_three: bool = False,
                               three_for_two: bool = False, two_for_three: bool = False,
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
                    # Waiver mode: use MIN_WAIVER_IMPROVEMENT threshold (allows smaller improvements)
                    # Trade mode: use MIN_TRADE_IMPROVEMENT threshold (requires 30+ point improvement)
                    if is_waivers:
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) > Constants.MIN_WAIVER_IMPROVEMENT
                        their_roster_improved = True  # Waiver wire doesn't need improvement
                    else:
                        # Trade suggestor mode: both teams must improve by at least MIN_TRADE_IMPROVEMENT
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
                        their_roster_improved = (their_new_team.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT

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

                    # Waiver mode: use MIN_WAIVER_IMPROVEMENT threshold
                    # Trade mode: use MIN_TRADE_IMPROVEMENT threshold (30 points minimum)
                    if is_waivers:
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) > Constants.MIN_WAIVER_IMPROVEMENT
                        their_roster_improved = True  # Waiver wire doesn't need improvement
                    else:
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
                        their_roster_improved = (their_new_team.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT

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

                    # Waiver mode: use MIN_WAIVER_IMPROVEMENT threshold
                    # Trade mode: use MIN_TRADE_IMPROVEMENT threshold (30 points minimum)
                    if is_waivers:
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) > Constants.MIN_WAIVER_IMPROVEMENT
                        their_roster_improved = True  # Waiver wire doesn't need improvement
                    else:
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
                        their_roster_improved = (their_new_team.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT

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

        # ===== GENERATE 2-FOR-1 TRADES =====
        # Give 2 players, get 1 player (net -1 roster spot - need waiver recommendation)
        if two_for_one:
            my_combos = list(combinations(my_roster, 2))

            for my_players in my_combos:
                for their_player in their_roster:
                    # Create new rosters after the trade
                    my_new_roster = [p for p in my_roster if p not in my_players] + [their_player]
                    their_new_roster = [p for p in their_roster if p != their_player] + list(my_players)

                    # Calculate waiver recommendations BEFORE roster validation
                    # 2:1 trade: I give 2, get 1 = net -1 (I need waiver), they get 2, give 1 = net +1 (no waiver)
                    my_waiver_recs = self._get_waiver_recommendations(num_spots=1)
                    their_waiver_recs = []

                    # Add waiver PLAYERS to rosters for scoring
                    my_new_roster_with_waivers = my_new_roster + [rec.player for rec in my_waiver_recs]
                    their_new_roster_with_waivers = their_new_roster

                    # Validate my team's roster (include locked players)
                    my_full_roster = my_new_roster_with_waivers + my_locked
                    if not self.validate_roster(my_full_roster, ignore_max_positions=ignore_max_positions):
                        continue

                    # Validate their team's roster (only if not waivers)
                    if not is_waivers:
                        their_full_roster = their_new_roster_with_waivers + their_locked
                        their_roster_valid = self.validate_roster(their_full_roster, ignore_max_positions=ignore_max_positions)

                        # If opponent validation fails, try drop variations
                        if not their_roster_valid:
                            drop_candidates = self._get_lowest_scored_players_per_position(
                                their_team, exclude_players=[their_player], num_per_position=2
                            )

                            # Try dropping each candidate
                            found_valid_drop = False
                            for drop_player in drop_candidates:
                                their_roster_with_drop = [p for p in their_new_roster_with_waivers if p != drop_player]
                                their_full_roster_with_drop = their_roster_with_drop + their_locked

                                if not self.validate_roster(their_full_roster_with_drop, ignore_max_positions=ignore_max_positions):
                                    continue

                                # Create teams with drop
                                my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers, self.player_manager, isOpponent=False)
                                their_new_team_with_drop = TradeSimTeam(their_team.name, their_roster_with_drop, self.player_manager, isOpponent=True)

                                # Check improvement
                                our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
                                their_roster_improved = (their_new_team_with_drop.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT

                                if our_roster_improved and their_roster_improved:
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
                                    found_valid_drop = True

                            if found_valid_drop:
                                continue
                            else:
                                continue

                    # Create teams with waivers
                    my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers, self.player_manager, isOpponent=True)

                    # Check improvement (waiver vs trade thresholds)
                    if is_waivers:
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) > Constants.MIN_WAIVER_IMPROVEMENT
                        their_roster_improved = True
                    else:
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
                        their_roster_improved = (their_new_team.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT

                    if our_roster_improved and their_roster_improved:
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

        # ===== GENERATE 1-FOR-2 TRADES =====
        # Give 1 player, get 2 players (net +1 roster spot - may need to drop)
        if one_for_two:
            their_combos = list(combinations(their_roster, 2))

            for my_player in my_roster:
                for their_players in their_combos:
                    # Create new rosters after the trade
                    my_new_roster = [p for p in my_roster if p != my_player] + list(their_players)
                    their_new_roster = [p for p in their_roster if p not in their_players] + [my_player]

                    # Calculate waiver recommendations
                    # 1:2 trade: I give 1, get 2 = net +1 (no waiver), they give 2, get 1 = net -1 (they need waiver)
                    my_waiver_recs = []
                    their_waiver_recs = self._get_waiver_recommendations(num_spots=1) if not is_waivers else []

                    my_new_roster_with_waivers = my_new_roster
                    their_new_roster_with_waivers = their_new_roster + [rec.player for rec in their_waiver_recs]

                    # Validate my team's roster
                    my_full_roster = my_new_roster_with_waivers + my_locked
                    my_roster_valid = self.validate_roster(my_full_roster, ignore_max_positions=ignore_max_positions)

                    # If my validation fails, try drop variations
                    if not my_roster_valid:
                        drop_candidates = self._get_lowest_scored_players_per_position(
                            my_team, exclude_players=[my_player], num_per_position=2
                        )

                        found_valid_drop = False
                        for drop_player in drop_candidates:
                            my_roster_with_drop = [p for p in my_new_roster if p != drop_player]
                            my_full_roster_with_drop = my_roster_with_drop + my_locked

                            if not self.validate_roster(my_full_roster_with_drop, ignore_max_positions=ignore_max_positions):
                                continue

                            # Validate opponent
                            if not is_waivers:
                                their_full_roster = their_new_roster_with_waivers + their_locked
                                if not self.validate_roster(their_full_roster, ignore_max_positions=ignore_max_positions):
                                    continue

                            # Create teams with drop
                            my_new_team_with_drop = TradeSimTeam(my_team.name, my_roster_with_drop, self.player_manager, isOpponent=False)
                            their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers, self.player_manager, isOpponent=True)

                            # Check improvement
                            if is_waivers:
                                our_roster_improved = (my_new_team_with_drop.team_score - my_team.team_score) > Constants.MIN_WAIVER_IMPROVEMENT
                                their_roster_improved = True
                            else:
                                our_roster_improved = (my_new_team_with_drop.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
                                their_roster_improved = (their_new_team.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT

                            if our_roster_improved and their_roster_improved:
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
                                found_valid_drop = True

                        if found_valid_drop:
                            continue
                        else:
                            continue

                    # Validate their team's roster
                    if not is_waivers:
                        their_full_roster = their_new_roster_with_waivers + their_locked
                        if not self.validate_roster(their_full_roster, ignore_max_positions=ignore_max_positions):
                            continue

                    # Create teams
                    my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers, self.player_manager, isOpponent=True)

                    # Check improvement
                    if is_waivers:
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) > Constants.MIN_WAIVER_IMPROVEMENT
                        their_roster_improved = True
                    else:
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
                        their_roster_improved = (their_new_team.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT

                    if our_roster_improved and their_roster_improved:
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

        # ===== GENERATE 3-FOR-1 TRADES =====
        # Give 3 players, get 1 player (net -2 roster spots - need 2 waivers)
        if three_for_one:
            my_combos = list(combinations(my_roster, 3))

            for my_players in my_combos:
                for their_player in their_roster:
                    my_new_roster = [p for p in my_roster if p not in my_players] + [their_player]
                    their_new_roster = [p for p in their_roster if p != their_player] + list(my_players)

                    my_waiver_recs = self._get_waiver_recommendations(num_spots=2)
                    their_waiver_recs = []

                    my_new_roster_with_waivers = my_new_roster + [rec.player for rec in my_waiver_recs]
                    their_new_roster_with_waivers = their_new_roster

                    my_full_roster = my_new_roster_with_waivers + my_locked
                    if not self.validate_roster(my_full_roster, ignore_max_positions=ignore_max_positions):
                        continue

                    if not is_waivers:
                        their_full_roster = their_new_roster_with_waivers + their_locked
                        their_roster_valid = self.validate_roster(their_full_roster, ignore_max_positions=ignore_max_positions)

                        if not their_roster_valid:
                            drop_candidates = self._get_lowest_scored_players_per_position(
                                their_team, exclude_players=[their_player], num_per_position=2
                            )

                            found_valid_drop = False
                            for drop_combo in combinations(drop_candidates, 2):
                                their_roster_with_drops = [p for p in their_new_roster_with_waivers if p not in drop_combo]
                                their_full_roster_with_drops = their_roster_with_drops + their_locked

                                if not self.validate_roster(their_full_roster_with_drops, ignore_max_positions=ignore_max_positions):
                                    continue

                                my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers, self.player_manager, isOpponent=False)
                                their_new_team_with_drops = TradeSimTeam(their_team.name, their_roster_with_drops, self.player_manager, isOpponent=True)

                                our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
                                their_roster_improved = (their_new_team_with_drops.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT

                                if our_roster_improved and their_roster_improved:
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
                                    found_valid_drop = True

                            if found_valid_drop:
                                continue
                            else:
                                continue

                    my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers, self.player_manager, isOpponent=True)

                    if is_waivers:
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) > Constants.MIN_WAIVER_IMPROVEMENT
                        their_roster_improved = True
                    else:
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
                        their_roster_improved = (their_new_team.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT

                    if our_roster_improved and their_roster_improved:
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

        # ===== GENERATE 1-FOR-3 TRADES =====
        # Give 1 player, get 3 players (net +2 roster spots - may need to drop 2)
        if one_for_three:
            their_combos = list(combinations(their_roster, 3))

            for my_player in my_roster:
                for their_players in their_combos:
                    my_new_roster = [p for p in my_roster if p != my_player] + list(their_players)
                    their_new_roster = [p for p in their_roster if p not in their_players] + [my_player]

                    my_waiver_recs = []
                    their_waiver_recs = self._get_waiver_recommendations(num_spots=2) if not is_waivers else []

                    my_new_roster_with_waivers = my_new_roster
                    their_new_roster_with_waivers = their_new_roster + [rec.player for rec in their_waiver_recs]

                    my_full_roster = my_new_roster_with_waivers + my_locked
                    my_roster_valid = self.validate_roster(my_full_roster, ignore_max_positions=ignore_max_positions)

                    if not my_roster_valid:
                        drop_candidates = self._get_lowest_scored_players_per_position(
                            my_team, exclude_players=[my_player], num_per_position=2
                        )

                        found_valid_drop = False
                        for drop_combo in combinations(drop_candidates, 2):
                            my_roster_with_drops = [p for p in my_new_roster if p not in drop_combo]
                            my_full_roster_with_drops = my_roster_with_drops + my_locked

                            if not self.validate_roster(my_full_roster_with_drops, ignore_max_positions=ignore_max_positions):
                                continue

                            if not is_waivers:
                                their_full_roster = their_new_roster_with_waivers + their_locked
                                if not self.validate_roster(their_full_roster, ignore_max_positions=ignore_max_positions):
                                    continue

                            my_new_team_with_drops = TradeSimTeam(my_team.name, my_roster_with_drops, self.player_manager, isOpponent=False)
                            their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers, self.player_manager, isOpponent=True)

                            if is_waivers:
                                our_roster_improved = (my_new_team_with_drops.team_score - my_team.team_score) > Constants.MIN_WAIVER_IMPROVEMENT
                                their_roster_improved = True
                            else:
                                our_roster_improved = (my_new_team_with_drops.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
                                their_roster_improved = (their_new_team.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT

                            if our_roster_improved and their_roster_improved:
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
                                found_valid_drop = True

                        if found_valid_drop:
                            continue
                        else:
                            continue

                    if not is_waivers:
                        their_full_roster = their_new_roster_with_waivers + their_locked
                        if not self.validate_roster(their_full_roster, ignore_max_positions=ignore_max_positions):
                            continue

                    my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers, self.player_manager, isOpponent=True)

                    if is_waivers:
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) > Constants.MIN_WAIVER_IMPROVEMENT
                        their_roster_improved = True
                    else:
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
                        their_roster_improved = (their_new_team.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT

                    if our_roster_improved and their_roster_improved:
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

        # ===== GENERATE 3-FOR-2 TRADES =====
        # Give 3 players, get 2 players (net -1 roster spot - need 1 waiver)
        if three_for_two:
            my_combos = list(combinations(my_roster, 3))
            their_combos = list(combinations(their_roster, 2))

            for my_players in my_combos:
                for their_players in their_combos:
                    my_new_roster = [p for p in my_roster if p not in my_players] + list(their_players)
                    their_new_roster = [p for p in their_roster if p not in their_players] + list(my_players)

                    my_waiver_recs = self._get_waiver_recommendations(num_spots=1)
                    their_waiver_recs = []

                    my_new_roster_with_waivers = my_new_roster + [rec.player for rec in my_waiver_recs]
                    their_new_roster_with_waivers = their_new_roster

                    my_full_roster = my_new_roster_with_waivers + my_locked
                    if not self.validate_roster(my_full_roster, ignore_max_positions=ignore_max_positions):
                        continue

                    if not is_waivers:
                        their_full_roster = their_new_roster_with_waivers + their_locked
                        their_roster_valid = self.validate_roster(their_full_roster, ignore_max_positions=ignore_max_positions)

                        if not their_roster_valid:
                            drop_candidates = self._get_lowest_scored_players_per_position(
                                their_team, exclude_players=list(their_players), num_per_position=2
                            )

                            found_valid_drop = False
                            for drop_player in drop_candidates:
                                their_roster_with_drop = [p for p in their_new_roster_with_waivers if p != drop_player]
                                their_full_roster_with_drop = their_roster_with_drop + their_locked

                                if not self.validate_roster(their_full_roster_with_drop, ignore_max_positions=ignore_max_positions):
                                    continue

                                my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers, self.player_manager, isOpponent=False)
                                their_new_team_with_drop = TradeSimTeam(their_team.name, their_roster_with_drop, self.player_manager, isOpponent=True)

                                our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
                                their_roster_improved = (their_new_team_with_drop.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT

                                if our_roster_improved and their_roster_improved:
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
                                    found_valid_drop = True

                            if found_valid_drop:
                                continue
                            else:
                                continue

                    my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers, self.player_manager, isOpponent=True)

                    if is_waivers:
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) > Constants.MIN_WAIVER_IMPROVEMENT
                        their_roster_improved = True
                    else:
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
                        their_roster_improved = (their_new_team.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT

                    if our_roster_improved and their_roster_improved:
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

        # ===== GENERATE 2-FOR-3 TRADES =====
        # Give 2 players, get 3 players (net +1 roster spot - may need to drop 1)
        if two_for_three:
            my_combos = list(combinations(my_roster, 2))
            their_combos = list(combinations(their_roster, 3))

            for my_players in my_combos:
                for their_players in their_combos:
                    my_new_roster = [p for p in my_roster if p not in my_players] + list(their_players)
                    their_new_roster = [p for p in their_roster if p not in their_players] + list(my_players)

                    my_waiver_recs = []
                    their_waiver_recs = self._get_waiver_recommendations(num_spots=1) if not is_waivers else []

                    my_new_roster_with_waivers = my_new_roster
                    their_new_roster_with_waivers = their_new_roster + [rec.player for rec in their_waiver_recs]

                    my_full_roster = my_new_roster_with_waivers + my_locked
                    my_roster_valid = self.validate_roster(my_full_roster, ignore_max_positions=ignore_max_positions)

                    if not my_roster_valid:
                        drop_candidates = self._get_lowest_scored_players_per_position(
                            my_team, exclude_players=list(my_players), num_per_position=2
                        )

                        found_valid_drop = False
                        for drop_player in drop_candidates:
                            my_roster_with_drop = [p for p in my_new_roster if p != drop_player]
                            my_full_roster_with_drop = my_roster_with_drop + my_locked

                            if not self.validate_roster(my_full_roster_with_drop, ignore_max_positions=ignore_max_positions):
                                continue

                            if not is_waivers:
                                their_full_roster = their_new_roster_with_waivers + their_locked
                                if not self.validate_roster(their_full_roster, ignore_max_positions=ignore_max_positions):
                                    continue

                            my_new_team_with_drop = TradeSimTeam(my_team.name, my_roster_with_drop, self.player_manager, isOpponent=False)
                            their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers, self.player_manager, isOpponent=True)

                            if is_waivers:
                                our_roster_improved = (my_new_team_with_drop.team_score - my_team.team_score) > Constants.MIN_WAIVER_IMPROVEMENT
                                their_roster_improved = True
                            else:
                                our_roster_improved = (my_new_team_with_drop.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
                                their_roster_improved = (their_new_team.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT

                            if our_roster_improved and their_roster_improved:
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
                                found_valid_drop = True

                        if found_valid_drop:
                            continue
                        else:
                            continue

                    if not is_waivers:
                        their_full_roster = their_new_roster_with_waivers + their_locked
                        if not self.validate_roster(their_full_roster, ignore_max_positions=ignore_max_positions):
                            continue

                    my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers, self.player_manager, isOpponent=True)

                    if is_waivers:
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) > Constants.MIN_WAIVER_IMPROVEMENT
                        their_roster_improved = True
                    else:
                        our_roster_improved = (my_new_team.team_score - my_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT
                        their_roster_improved = (their_new_team.team_score - their_team.team_score) >= Constants.MIN_TRADE_IMPROVEMENT

                    if our_roster_improved and their_roster_improved:
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

        # Log trade generation completion with result count
        self.logger.info(f"Generated {len(trade_combos)} valid trade combinations")

        # Return all valid trades found
        return trade_combos
