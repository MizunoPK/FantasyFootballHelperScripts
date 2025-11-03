"""
Trade Analyzer

Helper class for analyzing and generating trade combinations in Trade Simulator Mode.
Handles roster validation, position counting, and trade combination generation.

Author: Kai Mizuno
"""

import copy
from typing import Dict, List, Optional, Tuple
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
        position_counts = {pos: 0 for pos in self.config.max_positions.keys()}

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
        if len(roster) > self.config.max_players:
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

    def count_position_violations(self, roster: List[FantasyPlayer]) -> int:
        """
        Count the number of position limit violations in a roster.

        A violation occurs when a roster exceeds the maximum allowed players at a position.
        This method attempts to construct a valid team and counts how many players can't fit.

        IMPORTANT: Sorts roster by position priority before counting to ensure consistent results
        regardless of roster order. This prevents false positives when comparing before/after trades.

        Args:
            roster (List[FantasyPlayer]): The roster to check

        Returns:
            int: Number of players that exceed position limits (0 = no violations)

        Example:
            >>> roster_with_2_TE = [player1_TE, player2_TE, ...]  # Max TE is 1
            >>> count_position_violations(roster_with_2_TE)
            1  # One TE over the limit
        """
        # Sort roster by position priority to ensure consistent slot assignment
        # Priority: QB, RB, WR, TE, FLEX, K, DST (positions with single slots first)
        # This ensures the same players always get the same slots regardless of list order
        position_priority = {
            Constants.QB: 1,
            Constants.RB: 2,
            Constants.WR: 3,
            Constants.TE: 4,
            Constants.K: 5,
            Constants.DST: 6
        }
        sorted_roster = sorted(roster, key=lambda p: (position_priority.get(p.position, 99), p.name))

        # Try to draft all players into a test team
        test_team = FantasyTeam(self.config, [])
        violations = 0
        violation_players = []

        for p in sorted_roster:
            # Deep copy to avoid modifying original
            p_copy = copy.deepcopy(p)
            p_copy.drafted = 0
            p_copy.locked = 0  # Unlock for testing - we're just counting violations, not enforcing lock status

            # Try to draft - if it fails, it's a violation
            drafted = test_team.draft_player(p_copy)
            if not drafted:
                violations += 1
                violation_players.append(f"{p.name} ({p.position})")

        if violations > 0:
            self.logger.debug(f"Position violations: {violations} players cannot fit: {', '.join(violation_players)}")

        return violations

    def validate_roster_lenient(self, original_roster: List[FantasyPlayer], new_roster: List[FantasyPlayer]) -> bool:
        """
        Validate that a new roster doesn't worsen position violations.

        This lenient validation allows trades even if a team already violates position limits,
        as long as the trade doesn't make the violations worse.

        Args:
            original_roster (List[FantasyPlayer]): The roster before the trade
            new_roster (List[FantasyPlayer]): The roster after the trade

        Returns:
            bool: True if trade is acceptable (violations don't increase), False otherwise

        Example:
            Team has 2 TEs (max 1) = 1 violation
            Trade gives them a RB for a WR (still 2 TEs) = 1 violation
            Result: True (violations stayed same)

            Trade gives them another TE (now 3 TEs) = 2 violations
            Result: False (violations got worse)
        """
        # Always enforce MAX_PLAYERS limit
        if len(new_roster) > self.config.max_players:
            return False

        # Count violations before and after trade
        violations_before = self.count_position_violations(original_roster)
        violations_after = self.count_position_violations(new_roster)

        # DEBUG: Log violation counts
        self.logger.debug(f"Violations before: {violations_before}, after: {violations_after}")

        # Allow trade if violations don't increase
        # (violations_after <= violations_before)
        result = violations_after <= violations_before
        self.logger.debug(f"Validation result: {result} (violations_after <= violations_before)")
        return result

    def _get_waiver_recommendations(self, num_spots: int, post_trade_roster: List[FantasyPlayer] = None) -> List[ScoredPlayer]:
        """
        Get top N waiver wire recommendations to fill roster spots.

        Uses same logic as Add to Roster mode to score and rank available players,
        but filters by position limits to ensure recommendations don't violate MAX_POSITIONS.

        Args:
            num_spots (int): Number of waiver players needed
            post_trade_roster (List[FantasyPlayer]): Optional roster after trade (including locked players)
                                                     to check position limits. If None, returns top N by score.

        Returns:
            List[ScoredPlayer]: Top num_spots players sorted by score descending.
                               May return fewer if insufficient players available or position limits prevent it.

        Example:
            >>> waiver_adds = self._get_waiver_recommendations(2, my_new_roster + my_locked)
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
            # IMPORTANT: Pass post_trade_roster to calculate bye week overlaps correctly
            # If post_trade_roster is None, score_player will calculate bye overlaps as 0 (no context)
            scored_player = self.player_manager.score_player(
                p,
                adp=False,
                player_rating=True,
                team_quality=True,
                performance=True,
                matchup=False,
                schedule=True,
                roster=post_trade_roster
            )
            scored_players.append(scored_player)

        # Sort by score descending
        ranked_players = sorted(scored_players, key=lambda x: x.score, reverse=True)

        # If post_trade_roster provided, filter by position limits
        if post_trade_roster is not None:
            try:
                # Create a temporary FantasyTeam to test if each player can be drafted
                # Note: This may fail if post_trade_roster already violates position limits
                temp_team = FantasyTeam(self.config, post_trade_roster)

                filtered_recommendations = []
                for scored_player in ranked_players:
                    # Check if this player can be added without violating position limits
                    if temp_team.can_draft(scored_player.player):
                        filtered_recommendations.append(scored_player)
                        # Add player to temp team for next iteration's check
                        temp_team.draft_player(scored_player.player)

                        # Stop once we have enough recommendations
                        if len(filtered_recommendations) >= num_spots:
                            break

                result_count = len(filtered_recommendations)
                self.logger.debug(f"Generated {result_count} position-filtered waiver recommendations (requested: {num_spots})")
                return filtered_recommendations
            except ValueError as e:
                # Post-trade roster already violates position limits - can't create FantasyTeam
                # This happens when the roster exceeds MAX_PLAYERS or position limits
                # In this case, return no recommendations since roster is already invalid
                self.logger.debug(f"Cannot create temp team for position filtering: {e}")
                self.logger.debug("Post-trade roster already violates limits - returning no waiver recommendations")
                return []
        else:
            # No position filtering - return top N by score
            result_count = min(num_spots, len(ranked_players))
            self.logger.debug(f"Generated {result_count} waiver recommendations (requested: {num_spots})")
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
        position_groups: Dict[str, List[FantasyPlayer]] = {pos: [] for pos in self.config.max_positions.keys()}

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

    def _get_position_aware_drop_candidates(
        self,
        team: TradeSimTeam,
        post_trade_roster: List[FantasyPlayer],
        exclude_players: List[FantasyPlayer],
        num_per_position: int = 2
    ) -> List[FantasyPlayer]:
        """
        Get drop candidates from positions that exceed MAX_POSITIONS limits.

        This is smarter than _get_lowest_scored_players_per_position because it:
        1. Identifies which positions are over the limit
        2. Only suggests drops from those over-limit positions
        3. Prevents suggesting drops from unrelated positions

        Example:
            User receives QB in 2-for-1 trade (already has 2 QBs, max is 2)
            - Post-trade: 3 QBs (over limit!)
            - Should suggest: Drop lowest-scoring QB
            - NOT suggest: Drop lowest-scoring DST (globally worst player)

        Args:
            team (TradeSimTeam): Original team for scoring context
            post_trade_roster (List[FantasyPlayer]): Roster after trade (to check position counts)
            exclude_players (List[FantasyPlayer]): Players to exclude (being traded away)
            num_per_position (int): How many drops to suggest per over-limit position (default: 2)

        Returns:
            List[FantasyPlayer]: Drop candidates from over-limit positions only
        """
        # STEP 1: Calculate position counts in post-trade roster
        position_counts = {pos: 0 for pos in self.config.max_positions.keys()}

        for player in post_trade_roster:
            if player.position in position_counts:
                position_counts[player.position] += 1

        # STEP 2: Identify positions that exceed MAX_POSITIONS limits
        over_limit_positions = []
        for position, count in position_counts.items():
            max_allowed = self.config.max_positions[position]
            if count > max_allowed:
                excess = count - max_allowed
                over_limit_positions.append((position, excess))
                self.logger.debug(f"Position {position} over limit: {count}/{max_allowed} (excess: {excess})")

        # STEP 3: If any positions are over-limit, suggest drops from those positions only
        if over_limit_positions:
            droppable_players = []

            for position, excess in over_limit_positions:
                # Get all players at this position (excluding locked and traded players)
                position_players = []
                for player in team.team:
                    # Skip players being traded away
                    if player in exclude_players:
                        continue

                    # Skip locked players (can't drop them)
                    if player.locked:
                        continue

                    # Only include players from this over-limit position
                    if player.position == position:
                        position_players.append(player)

                # Sort by score (ascending - lowest first) and take N lowest
                if position_players:
                    sorted_players = sorted(position_players, key=lambda p: p.score)
                    droppable_players.extend(sorted_players[:num_per_position])

            self.logger.info(f"Position-aware drop: Found {len(droppable_players)} candidates from {len(over_limit_positions)} over-limit positions")
            return droppable_players

        # STEP 4: No positions over-limit, but total roster > MAX_PLAYERS
        # Fall back to original behavior: suggest lowest-scoring from all positions
        self.logger.debug("No specific positions over-limit, using global lowest-scoring players")
        return self._get_lowest_scored_players_per_position(team, exclude_players, num_per_position)

    def process_manual_trade(
        self,
        my_team: TradeSimTeam,
        their_team: TradeSimTeam,
        my_selected_players: List[FantasyPlayer],
        their_selected_players: List[FantasyPlayer],
        my_dropped_players: Optional[List[FantasyPlayer]] = None,
        their_dropped_players: Optional[List[FantasyPlayer]] = None,
        is_waivers: bool = False
    ) -> Tuple[Optional[TradeSnapshot], List[FantasyPlayer], List[FantasyPlayer]]:
        """
        Process a manual trade with waiver/drop handling.

        This is the shared logic for manual trade processing that handles:
        1. Calculating net roster changes and waiver needs
        2. Adding waiver recommendations when losing roster spots
        3. Validating rosters with all adjustments
        4. Returning drop candidates if roster invalid

        Args:
            my_team (TradeSimTeam): My current team
            their_team (TradeSimTeam): Opponent's current team
            my_selected_players (List[FantasyPlayer]): Players I'm giving away
            their_selected_players (List[FantasyPlayer]): Players I'm receiving
            my_dropped_players (Optional[List[FantasyPlayer]]): Players I'm dropping (if any)
            their_dropped_players (Optional[List[FantasyPlayer]]): Players they're dropping (if any)
            is_waivers (bool): If True, skip validation and waiver recommendations for their team
                              (used when trading with waiver wire). Defaults to False.

        Returns:
            Tuple containing:
                - TradeSnapshot: Trade snapshot if valid, None if roster invalid
                - List[FantasyPlayer]: My drop candidates (if roster invalid and no drops provided)
                - List[FantasyPlayer]: Their drop candidates (if roster invalid and no drops provided)

        Example workflow:
            # First attempt (no drops)
            snapshot, my_drops, their_drops = process_manual_trade(my_team, their_team, [p1], [p2, p3])
            if snapshot:
                # Trade valid, display it
            else:
                # Trade invalid, prompt user to select from my_drops/their_drops
                # Then retry with selected drops
                snapshot, _, _ = process_manual_trade(..., my_dropped_players=[user_selection])
        """
        # Initialize dropped players lists
        if my_dropped_players is None:
            my_dropped_players = []
        if their_dropped_players is None:
            their_dropped_players = []

        # Get tradeable and locked players
        # Manual Trade Visualizer: Allow trading locked players if explicitly selected
        # Strategy: Move selected locked players to the tradeable roster
        # IR players (HIGH risk) don't count toward limits and can't be traded

        # First, separate players normally (locked vs unlocked)
        my_roster_unlocked = [p for p in my_team.team if p.locked != 1 and p.get_risk_level() != "HIGH"]
        my_locked_original = [p for p in my_team.team if p.locked == 1 and p.get_risk_level() != "HIGH"]
        my_ir = [p for p in my_team.team if p.get_risk_level() == "HIGH"]

        their_roster_unlocked = [p for p in their_team.team if p.locked != 1 and p.get_risk_level() != "HIGH"]
        their_locked_original = [p for p in their_team.team if p.locked == 1 and p.get_risk_level() != "HIGH"]
        their_ir = [p for p in their_team.team if p.get_risk_level() == "HIGH"]

        # Move selected locked players to tradeable roster
        # This allows manually selected locked players to be traded
        my_roster = my_roster_unlocked + [p for p in my_locked_original if p in my_selected_players]
        my_locked = [p for p in my_locked_original if p not in my_selected_players]

        their_roster = their_roster_unlocked + [p for p in their_locked_original if p in their_selected_players]
        their_locked = [p for p in their_locked_original if p not in their_selected_players]

        # Calculate net roster change (positive = gaining players, negative = losing players)
        my_net_change = len(their_selected_players) - len(my_selected_players)
        their_net_change = len(my_selected_players) - len(their_selected_players)

        # Create new rosters after trade (without waivers yet)
        my_new_roster = [p for p in my_roster if p not in my_selected_players and p not in my_dropped_players] + their_selected_players
        their_new_roster = [p for p in their_roster if p not in their_selected_players and p not in their_dropped_players] + my_selected_players

        # Get waiver recommendations based on net roster change
        # If losing players (net negative), recommend waivers to fill spots
        # IMPORTANT: Must pass full roster (including locked) for position filtering
        # Locked players count toward position limits even though they can't be traded
        my_waiver_spots_needed = max(0, -my_net_change)
        their_waiver_spots_needed = max(0, -their_net_change)

        my_waiver_recs = self._get_waiver_recommendations(my_waiver_spots_needed, post_trade_roster=my_new_roster + my_locked)

        # Skip waiver recommendations for waiver "team"
        if is_waivers:
            their_waiver_recs = []
        else:
            their_waiver_recs = self._get_waiver_recommendations(their_waiver_spots_needed, post_trade_roster=their_new_roster + their_locked)

        # Add waiver recommendations to rosters
        my_new_roster_with_waivers = my_new_roster + [rec.player for rec in my_waiver_recs]
        their_new_roster_with_waivers = their_new_roster + [rec.player for rec in their_waiver_recs]

        # Validate my team's roster (include locked/IR players)
        # Use lenient validation that allows trades as long as roster doesn't get worse
        # This supports users who may already be over MAX_PLAYERS due to extra DSTs, etc.
        my_full_roster = my_new_roster_with_waivers + my_locked
        my_original_full_roster = my_roster + my_locked
        my_roster_valid = self.validate_roster_lenient(my_original_full_roster, my_full_roster)

        # Validate their team's roster (include locked/IR players)
        their_full_roster = their_new_roster_with_waivers + their_locked
        their_original_full_roster = their_roster + their_locked

        # DEBUG: Log roster sizes and composition
        self.logger.info(f"Their original roster size: {len(their_original_full_roster)}")
        self.logger.info(f"Their new roster size: {len(their_full_roster)}")
        self.logger.info(f"Their original positions: RB={sum(1 for p in their_original_full_roster if p.position=='RB')}, "
                        f"WR={sum(1 for p in their_original_full_roster if p.position=='WR')}, "
                        f"TE={sum(1 for p in their_original_full_roster if p.position=='TE')}")
        self.logger.info(f"Their new positions: RB={sum(1 for p in their_full_roster if p.position=='RB')}, "
                        f"WR={sum(1 for p in their_full_roster if p.position=='WR')}, "
                        f"TE={sum(1 for p in their_full_roster if p.position=='TE')}")

        # Skip validation for waiver "team"
        if is_waivers:
            their_roster_valid = True
            self.logger.info("Skipping roster validation for waiver team")
        else:
            their_roster_valid = self.validate_roster_lenient(their_original_full_roster, their_full_roster)

        # If either roster is invalid, return drop candidates
        if not my_roster_valid or not their_roster_valid:
            my_drop_candidates = []
            their_drop_candidates = []

            if not my_roster_valid:
                # Get position-aware drop candidates for my team
                # Pass the full post-trade roster to identify which positions are over-limit
                my_drop_candidates = self._get_position_aware_drop_candidates(
                    my_team,
                    post_trade_roster=my_new_roster_with_waivers + my_locked,
                    exclude_players=my_selected_players,
                    num_per_position=2
                )
                self.logger.debug(f"My roster invalid - providing {len(my_drop_candidates)} drop candidates")

            if not their_roster_valid:
                # Get position-aware drop candidates for their team
                # Skip for waiver team - they have no roster constraints
                if not is_waivers:
                    # Pass the full post-trade roster to identify which positions are over-limit
                    their_drop_candidates = self._get_position_aware_drop_candidates(
                        their_team,
                        post_trade_roster=their_new_roster_with_waivers + their_locked,
                        exclude_players=their_selected_players,
                        num_per_position=2
                    )
                    self.logger.debug(f"Their roster invalid - providing {len(their_drop_candidates)} drop candidates")

            return (None, my_drop_candidates, their_drop_candidates)

        # Both rosters valid - create trade snapshot
        # Use full rosters (including locked players) for accurate scoring
        my_new_team = TradeSimTeam(my_team.name, my_full_roster, self.player_manager, isOpponent=False)
        their_new_team = TradeSimTeam(their_team.name, their_full_roster, self.player_manager, isOpponent=True)

        # Get scored representations
        my_original_scored = my_team.get_scored_players(my_selected_players)
        my_dropped_scored = my_team.get_scored_players(my_dropped_players) if my_dropped_players else []
        their_dropped_scored = their_team.get_scored_players(their_dropped_players) if their_dropped_players else []

        # Create snapshot
        snapshot = TradeSnapshot(
            my_new_team=my_new_team,
            my_new_players=my_new_team.get_scored_players(their_selected_players),
            their_new_team=their_new_team,
            their_new_players=their_new_team.get_scored_players(my_selected_players),
            my_original_players=my_original_scored,
            waiver_recommendations=my_waiver_recs,
            their_waiver_recommendations=their_waiver_recs,
            my_dropped_players=my_dropped_scored,
            their_dropped_players=their_dropped_scored
        )

        self.logger.info(f"Manual trade processed successfully: {len(my_selected_players)}-for-{len(their_selected_players)}")
        return (snapshot, [], [])

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

        # ===== LOCKED PLAYER AND INJURY RESERVE HANDLING =====
        # Separate locked/IR players from tradeable players on both teams
        #
        # IMPORTANT: Locked vs IR players are handled differently:
        # - LOCKED players (player.locked == 1): Cannot be traded BUT count toward position limits
        # - IR players (HIGH risk like INJURY_RESERVE): Cannot be traded AND don't count toward limits
        #
        # IR players occupy a separate IR slot and don't count toward MAX_PLAYERS or position limits.
        # Locked players are active roster members who are just marked as unavailable for trades.
        #
        # Example: User has 15 active players + 1 IR player
        # - Validation should check the 15 active players against MAX_PLAYERS=15 ✓
        # - NOT check all 16 players against MAX_PLAYERS=15 ✗

        # Filter players by availability and injury status
        my_roster = [p for p in my_team.team if p.locked != 1 and p.get_risk_level() != "HIGH"]  # Tradeable players only
        my_locked = [p for p in my_team.team if p.locked == 1 and p.get_risk_level() != "HIGH"]  # Locked but not IR
        my_ir = [p for p in my_team.team if p.get_risk_level() == "HIGH"]  # IR players (excluded from validation)

        their_roster = [p for p in their_team.team if p.locked != 1 and p.get_risk_level() != "HIGH"]  # Tradeable players only
        their_locked = [p for p in their_team.team if p.locked == 1 and p.get_risk_level() != "HIGH"]  # Locked but not IR
        their_ir = [p for p in their_team.team if p.get_risk_level() == "HIGH"]  # IR players (excluded from validation)

        # Store original full rosters for lenient validation (includes locked players but NOT IR)
        # IR players are in a separate slot and don't count toward position limits
        my_original_full_roster = my_roster + my_locked
        their_original_full_roster = their_roster + their_locked

        # Log player filtering results
        self.logger.debug(f"Filtered rosters: my_tradeable={len(my_roster)}, my_locked={len(my_locked)}, my_ir={len(my_ir)}, their_tradeable={len(their_roster)}, their_locked={len(their_locked)}, their_ir={len(their_ir)}")

        # Define lenient validation helper that allows trades if violations don't worsen
        def validate_trade_roster(original_full: List[FantasyPlayer], new_full: List[FantasyPlayer]) -> bool:
            """Helper to validate roster using lenient rules if ignore_max_positions=False"""
            if ignore_max_positions:
                # Manual trade mode - only check MAX_PLAYERS
                return len(new_full) <= self.config.max_players
            else:
                # Trade suggestor mode - allow if violations don't increase
                return self.validate_roster_lenient(original_full, new_full)

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
                    # Add locked/IR players to get full roster for position limit validation
                    # Locked/IR players count toward position limits even though they weren't traded
                    my_full_roster = my_new_roster + my_locked
                    if not validate_trade_roster(my_original_full_roster, my_full_roster):
                        # Trade would violate position limits or roster size - skip this combination
                        continue

                    # STEP 3: Create their full roster and validate (only validate if not waiver mode)
                    # Waiver wire doesn't have position limits, so skip validation
                    # For regular trades, ensure their roster remains valid too
                    their_full_roster = their_new_roster + their_locked
                    if not is_waivers:
                        if not validate_trade_roster(their_original_full_roster, their_full_roster):
                            # Trade would violate opponent's position limits - skip this combination
                            continue

                    # STEP 4: Score the new rosters and check for mutual improvement
                    # Create new TradeSimTeam objects which automatically score the rosters
                    # IMPORTANT: Must include locked players in scoring to get accurate team scores
                    # my_full_roster = my_new_roster (tradeable) + my_locked (locked but not IR)
                    # IR players are auto-filtered by TradeSimTeam.__init__ so we don't add them here
                    # isOpponent=False for user team (uses full scoring: ADP, rating, team quality, bye, etc.)
                    # isOpponent=True for opponent team (uses simplified scoring: projections + rating only)
                    my_new_team = TradeSimTeam(my_team.name, my_full_roster, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_full_roster, self.player_manager, isOpponent=True)

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

                    # Validate rosters (include locked/IR players in position limit check)
                    my_full_roster = my_new_roster + my_locked
                    if not validate_trade_roster(my_original_full_roster, my_full_roster):
                        continue

                    # Create their full roster and validate (only validate if not waiver mode)
                    their_full_roster = their_new_roster + their_locked
                    if not is_waivers:
                        if not validate_trade_roster(their_original_full_roster, their_full_roster):
                            continue

                    # Score rosters and check for mutual improvement
                    # Include locked players in scoring for accurate team score comparison
                    my_new_team = TradeSimTeam(my_team.name, my_full_roster, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_full_roster, self.player_manager, isOpponent=True)

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

                    # Validate rosters (include locked/IR players in position limit check)
                    my_full_roster = my_new_roster + my_locked
                    if not validate_trade_roster(my_original_full_roster, my_full_roster):
                        continue

                    # Create their full roster and validate (only validate if not waiver mode)
                    their_full_roster = their_new_roster + their_locked
                    if not is_waivers:
                        if not validate_trade_roster(their_original_full_roster, their_full_roster):
                            continue

                    # Score rosters and check for mutual improvement
                    # Include locked players in scoring for accurate team score comparison
                    my_new_team = TradeSimTeam(my_team.name, my_full_roster, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_full_roster, self.player_manager, isOpponent=True)

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
                    # Pass post-trade roster (including locked players) to filter by position limits
                    my_waiver_recs = self._get_waiver_recommendations(num_spots=1, post_trade_roster=my_new_roster + my_locked)
                    their_waiver_recs = []

                    # Add waiver PLAYERS to rosters for scoring
                    my_new_roster_with_waivers = my_new_roster + [rec.player for rec in my_waiver_recs]
                    their_new_roster_with_waivers = their_new_roster

                    # Validate my team's roster (include locked players)
                    my_full_roster = my_new_roster_with_waivers + my_locked
                    if not validate_trade_roster(my_original_full_roster, my_full_roster):
                        continue

                    # Validate their team's roster (only if not waivers)
                    if not is_waivers:
                        their_full_roster = their_new_roster_with_waivers + their_locked
                        their_roster_valid = validate_trade_roster(their_original_full_roster, their_full_roster)

                        # If opponent validation fails, try drop variations
                        if not their_roster_valid:
                            drop_candidates = self._get_position_aware_drop_candidates(
                                their_team,
                                post_trade_roster=their_new_roster_with_waivers + their_locked,
                                exclude_players=[their_player],
                                num_per_position=2
                            )

                            # Try dropping each candidate
                            found_valid_drop = False
                            for drop_player in drop_candidates:
                                their_roster_with_drop = [p for p in their_new_roster_with_waivers if p != drop_player]
                                their_full_roster_with_drop = their_roster_with_drop + their_locked

                                if not validate_trade_roster(their_original_full_roster, their_full_roster_with_drop):
                                    continue

                                # Create teams with drop
                                my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers + my_locked, self.player_manager, isOpponent=False)
                                their_new_team_with_drop = TradeSimTeam(their_team.name, their_roster_with_drop + their_locked, self.player_manager, isOpponent=True)

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

                    # Create teams with waivers (include locked players for accurate scoring)
                    my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers + my_locked, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers + their_locked, self.player_manager, isOpponent=True)

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
                    # Pass post-trade roster (including locked players) to filter by position limits
                    my_waiver_recs = []
                    their_waiver_recs = self._get_waiver_recommendations(num_spots=1, post_trade_roster=their_new_roster + their_locked) if not is_waivers else []

                    my_new_roster_with_waivers = my_new_roster
                    their_new_roster_with_waivers = their_new_roster + [rec.player for rec in their_waiver_recs]

                    # Validate my team's roster using lenient validation (allows existing violations)
                    my_full_roster = my_new_roster_with_waivers + my_locked
                    my_roster_valid = validate_trade_roster(my_original_full_roster, my_full_roster)

                    # If my validation fails, try drop variations
                    if not my_roster_valid:
                        drop_candidates = self._get_position_aware_drop_candidates(
                            my_team,
                            post_trade_roster=my_new_roster_with_waivers + my_locked,
                            exclude_players=[my_player],
                            num_per_position=2
                        )

                        found_valid_drop = False
                        for drop_player in drop_candidates:
                            my_roster_with_drop = [p for p in my_new_roster if p != drop_player]
                            my_full_roster_with_drop = my_roster_with_drop + my_locked

                            if not validate_trade_roster(my_original_full_roster, my_full_roster_with_drop):
                                continue

                            # Validate opponent using lenient validation
                            if not is_waivers:
                                their_full_roster = their_new_roster_with_waivers + their_locked
                                if not validate_trade_roster(their_original_full_roster, their_full_roster):
                                    continue

                            # Create teams with drop
                            my_new_team_with_drop = TradeSimTeam(my_team.name, my_roster_with_drop + my_locked, self.player_manager, isOpponent=False)
                            their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers + their_locked, self.player_manager, isOpponent=True)

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

                    # Validate their team's roster using lenient validation
                    if not is_waivers:
                        their_full_roster = their_new_roster_with_waivers + their_locked
                        if not validate_trade_roster(their_original_full_roster, their_full_roster):
                            continue

                    # Create teams (include locked players for accurate scoring)
                    my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers + my_locked, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers + their_locked, self.player_manager, isOpponent=True)

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

                    # Pass post-trade roster (including locked players) to filter by position limits
                    my_waiver_recs = self._get_waiver_recommendations(num_spots=2, post_trade_roster=my_new_roster + my_locked)
                    their_waiver_recs = []

                    my_new_roster_with_waivers = my_new_roster + [rec.player for rec in my_waiver_recs]
                    their_new_roster_with_waivers = their_new_roster

                    my_full_roster = my_new_roster_with_waivers + my_locked
                    if not validate_trade_roster(my_original_full_roster, my_full_roster):
                        continue

                    if not is_waivers:
                        their_full_roster = their_new_roster_with_waivers + their_locked
                        their_roster_valid = validate_trade_roster(their_original_full_roster, their_full_roster)

                        if not their_roster_valid:
                            drop_candidates = self._get_position_aware_drop_candidates(
                                their_team,
                                post_trade_roster=their_new_roster_with_waivers + their_locked,
                                exclude_players=[their_player],
                                num_per_position=2
                            )

                            found_valid_drop = False
                            for drop_combo in combinations(drop_candidates, 2):
                                their_roster_with_drops = [p for p in their_new_roster_with_waivers if p not in drop_combo]
                                their_full_roster_with_drops = their_roster_with_drops + their_locked

                                if not validate_trade_roster(their_original_full_roster, their_full_roster_with_drops):
                                    continue

                                my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers + my_locked, self.player_manager, isOpponent=False)
                                their_new_team_with_drops = TradeSimTeam(their_team.name, their_roster_with_drops + their_locked, self.player_manager, isOpponent=True)

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

                    # Create teams (include locked players for accurate scoring)
                    my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers + my_locked, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers + their_locked, self.player_manager, isOpponent=True)

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

                    # Pass post-trade roster (including locked players) to filter by position limits
                    my_waiver_recs = []
                    their_waiver_recs = self._get_waiver_recommendations(num_spots=2, post_trade_roster=their_new_roster + their_locked) if not is_waivers else []

                    my_new_roster_with_waivers = my_new_roster
                    their_new_roster_with_waivers = their_new_roster + [rec.player for rec in their_waiver_recs]

                    my_full_roster = my_new_roster_with_waivers + my_locked
                    my_roster_valid = validate_trade_roster(my_original_full_roster, my_full_roster)

                    if not my_roster_valid:
                        drop_candidates = self._get_position_aware_drop_candidates(
                            my_team,
                            post_trade_roster=my_new_roster_with_waivers + my_locked,
                            exclude_players=[my_player],
                            num_per_position=2
                        )

                        found_valid_drop = False
                        for drop_combo in combinations(drop_candidates, 2):
                            my_roster_with_drops = [p for p in my_new_roster if p not in drop_combo]
                            my_full_roster_with_drops = my_roster_with_drops + my_locked

                            if not validate_trade_roster(my_original_full_roster, my_full_roster_with_drops):
                                continue

                            if not is_waivers:
                                their_full_roster = their_new_roster_with_waivers + their_locked
                                if not validate_trade_roster(their_original_full_roster, their_full_roster):
                                    continue

                            my_new_team_with_drops = TradeSimTeam(my_team.name, my_roster_with_drops + my_locked, self.player_manager, isOpponent=False)
                            their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers + their_locked, self.player_manager, isOpponent=True)

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
                        if not validate_trade_roster(their_original_full_roster, their_full_roster):
                            continue

                    # Create teams (include locked players for accurate scoring)
                    my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers + my_locked, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers + their_locked, self.player_manager, isOpponent=True)

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

                    # Pass post-trade roster (including locked players) to filter by position limits
                    my_waiver_recs = self._get_waiver_recommendations(num_spots=1, post_trade_roster=my_new_roster + my_locked)
                    their_waiver_recs = []

                    my_new_roster_with_waivers = my_new_roster + [rec.player for rec in my_waiver_recs]
                    their_new_roster_with_waivers = their_new_roster

                    my_full_roster = my_new_roster_with_waivers + my_locked
                    if not validate_trade_roster(my_original_full_roster, my_full_roster):
                        continue

                    if not is_waivers:
                        their_full_roster = their_new_roster_with_waivers + their_locked
                        their_roster_valid = validate_trade_roster(their_original_full_roster, their_full_roster)

                        if not their_roster_valid:
                            drop_candidates = self._get_position_aware_drop_candidates(
                                their_team,
                                post_trade_roster=their_new_roster_with_waivers + their_locked,
                                exclude_players=list(their_players),
                                num_per_position=2
                            )

                            found_valid_drop = False
                            for drop_player in drop_candidates:
                                their_roster_with_drop = [p for p in their_new_roster_with_waivers if p != drop_player]
                                their_full_roster_with_drop = their_roster_with_drop + their_locked

                                if not validate_trade_roster(their_original_full_roster, their_full_roster_with_drop):
                                    continue

                                my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers + my_locked, self.player_manager, isOpponent=False)
                                their_new_team_with_drop = TradeSimTeam(their_team.name, their_roster_with_drop + their_locked, self.player_manager, isOpponent=True)

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

                    # Create teams (include locked players for accurate scoring)
                    my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers + my_locked, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers + their_locked, self.player_manager, isOpponent=True)

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

                    # Pass post-trade roster (including locked players) to filter by position limits
                    my_waiver_recs = []
                    their_waiver_recs = self._get_waiver_recommendations(num_spots=1, post_trade_roster=their_new_roster + their_locked) if not is_waivers else []

                    my_new_roster_with_waivers = my_new_roster
                    their_new_roster_with_waivers = their_new_roster + [rec.player for rec in their_waiver_recs]

                    my_full_roster = my_new_roster_with_waivers + my_locked
                    my_roster_valid = validate_trade_roster(my_original_full_roster, my_full_roster)

                    if not my_roster_valid:
                        drop_candidates = self._get_position_aware_drop_candidates(
                            my_team,
                            post_trade_roster=my_new_roster_with_waivers + my_locked,
                            exclude_players=list(my_players),
                            num_per_position=2
                        )

                        found_valid_drop = False
                        for drop_player in drop_candidates:
                            my_roster_with_drop = [p for p in my_new_roster if p != drop_player]
                            my_full_roster_with_drop = my_roster_with_drop + my_locked

                            if not validate_trade_roster(my_original_full_roster, my_full_roster_with_drop):
                                continue

                            if not is_waivers:
                                their_full_roster = their_new_roster_with_waivers + their_locked
                                if not validate_trade_roster(their_original_full_roster, their_full_roster):
                                    continue

                            my_new_team_with_drop = TradeSimTeam(my_team.name, my_roster_with_drop + my_locked, self.player_manager, isOpponent=False)
                            their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers + their_locked, self.player_manager, isOpponent=True)

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
                        if not validate_trade_roster(their_original_full_roster, their_full_roster):
                            continue

                    # Create teams (include locked players for accurate scoring)
                    my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers + my_locked, self.player_manager, isOpponent=False)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers + their_locked, self.player_manager, isOpponent=True)

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
