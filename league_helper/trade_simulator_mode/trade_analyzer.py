"""
Trade Analyzer

Helper class for analyzing and generating trade combinations in Trade Simulator Mode.
Handles roster validation, position counting, and trade combination generation.

Author: Kai Mizuno
"""

import copy
from typing import Dict, List, Optional, Tuple
from itertools import combinations

import league_helper.constants as Constants
from league_helper.util.PlayerManager import PlayerManager
from league_helper.util.ConfigManager import ConfigManager
from league_helper.util.FantasyTeam import FantasyTeam
from league_helper.util.ScoredPlayer import ScoredPlayer
from utils.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger
from league_helper.trade_simulator_mode.TradeSimTeam import TradeSimTeam
from league_helper.trade_simulator_mode.TradeSnapshot import TradeSnapshot


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

        for pos in Constants.MIN_POSITIONS.keys():
            min_val = Constants.MIN_POSITIONS[pos]
            max_val = self.config.max_positions.get(pos, 0)
            if min_val > max_val:
                self.logger.warning(
                    f"Configuration warning: MIN_POSITIONS[{pos}]={min_val} "
                    f"exceeds MAX_POSITIONS[{pos}]={max_val}"
                )

    def count_positions(self, roster: List[FantasyPlayer]) -> Dict[str, int]:
        """
        Count the number of players at each position in a roster.

        Args:
            roster (List[FantasyPlayer]): The roster to count

        Returns:
            Dict[str, int]: Dictionary mapping position to count
        """
        position_counts = {pos: 0 for pos in self.config.max_positions.keys()}

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
        if len(roster) > self.config.max_players:
            return False

        if ignore_max_positions:
            return True

        test_team = FantasyTeam(self.config, [])
        for p in roster:
            p_copy = copy.deepcopy(p)
            p_copy.drafted_by = ""
            drafted = test_team.draft_player(p_copy)
            if not drafted:
                return False

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
        position_priority = {
            Constants.QB: 1,
            Constants.RB: 2,
            Constants.WR: 3,
            Constants.TE: 4,
            Constants.K: 5,
            Constants.DST: 6
        }
        sorted_roster = sorted(roster, key=lambda p: (position_priority.get(p.position, 99), p.name))

        from collections import Counter
        pos_counts = Counter(p.position for p in roster)
        flex_eligible_count = pos_counts.get('RB', 0) + pos_counts.get('WR', 0)
        flex_slots = self.config.max_positions.get('FLEX', 0)
        rb_slots = self.config.max_positions.get('RB', 0)
        wr_slots = self.config.max_positions.get('WR', 0)
        max_flex_eligible = rb_slots + wr_slots + flex_slots
        self.logger.debug(f"VALIDATION: Roster has {len(roster)} players: {dict(pos_counts)}")
        self.logger.debug(f"VALIDATION: FLEX-eligible: {flex_eligible_count} (RB={pos_counts.get('RB', 0)}, WR={pos_counts.get('WR', 0)}), max slots={max_flex_eligible} ({rb_slots} RB + {wr_slots} WR + {flex_slots} FLEX)")

        test_team = FantasyTeam(self.config, [])
        violations = 0
        violation_players = []

        for p in sorted_roster:
            p_copy = copy.deepcopy(p)
            p_copy.drafted_by = ""
            p_copy.locked = False
            if p_copy.bye_week is not None and p_copy.bye_week not in Constants.POSSIBLE_BYE_WEEKS:
                p_copy.bye_week = 10

            drafted = test_team.draft_player(p_copy)
            if not drafted:
                violations += 1
                violation_players.append(f"{p.name} ({p.position})")
                slot_info = {pos: len(ids) for pos, ids in test_team.slot_assignments.items()}
                self.logger.debug(f"VALIDATION: FAILED to draft {p.name} ({p.position}) - slots: {slot_info}")

        if violations > 0:
            self.logger.debug(f"Position violations: {violations} players cannot fit: {', '.join(violation_players)}")
        else:
            self.logger.debug(f"VALIDATION: All {len(roster)} players fit - no violations")

        return violations

    def count_min_position_violations(self, roster: List[FantasyPlayer]) -> int:
        """
        Count the number of minimum position requirement violations in a roster.

        A violation occurs when a roster has fewer players at a position than
        the minimum required by Constants.MIN_POSITIONS.

        Args:
            roster (List[FantasyPlayer]): The roster to check

        Returns:
            int: Number of positions below minimum (0 = no violations)

        Example:
            >>> roster_with_1_QB = [qb1, rb1, rb2, wr1, wr2, wr3, te1, k1, dst1]
            >>> count_min_position_violations(roster_with_1_QB)
            0  # Has 1 QB (meets MIN of 1)

            >>> roster_with_0_QB = [rb1, rb2, wr1, wr2, wr3, te1, k1, dst1]
            >>> count_min_position_violations(roster_with_0_QB)
            1  # Missing QB (below MIN of 1)
        """
        position_counts = self.count_positions(roster)

        violations = 0
        violation_details = []

        for position, min_required in Constants.MIN_POSITIONS.items():
            current_count = position_counts.get(position, 0)
            if current_count < min_required:
                violations += 1
                shortage = min_required - current_count
                violation_details.append(f"{position}: {current_count}/{min_required} (short {shortage})")

        if violations > 0:
            self.logger.debug(
                f"Min position violations: {violations} positions below minimum - "
                f"{', '.join(violation_details)}"
            )

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
        if len(new_roster) > self.config.max_players:
            self.logger.debug(f"VALIDATION REJECTED: Roster size {len(new_roster)} > max {self.config.max_players}")
            return False

        from collections import Counter
        orig_pos = Counter(p.position for p in original_roster)
        new_pos = Counter(p.position for p in new_roster)
        self.logger.debug(f"LENIENT VALIDATION: Comparing rosters...")
        self.logger.debug(f"  ORIGINAL ({len(original_roster)} players): {dict(orig_pos)}")
        self.logger.debug(f"  NEW ({len(new_roster)} players): {dict(new_pos)}")

        dropped = [p for p in original_roster if p.id not in [x.id for x in new_roster]]
        added = [p for p in new_roster if p.id not in [x.id for x in original_roster]]
        if dropped or added:
            self.logger.debug(f"  DROPPED: {[f'{p.name} ({p.position})' for p in dropped]}")
            self.logger.debug(f"  ADDED: {[f'{p.name} ({p.position})' for p in added]}")

        self.logger.debug("  Counting ORIGINAL roster violations...")
        violations_before = self.count_position_violations(original_roster)
        self.logger.debug("  Counting NEW roster violations...")
        violations_after = self.count_position_violations(new_roster)

        self.logger.debug(f"VALIDATION RESULT: violations_before={violations_before}, violations_after={violations_after}")

        result = violations_after <= violations_before
        if result:
            self.logger.debug(f"  TRADE ALLOWED: {violations_after} <= {violations_before}")
        else:
            self.logger.debug(f"  TRADE REJECTED: {violations_after} > {violations_before}")
        return result

    def validate_min_positions_lenient(
        self,
        original_roster: List[FantasyPlayer],
        new_roster: List[FantasyPlayer]
    ) -> bool:
        """
        Validate that a new roster doesn't worsen minimum position violations.

        This lenient validation allows trades even if a team already violates
        minimum position requirements, as long as the trade doesn't make the
        violations worse.

        Args:
            original_roster (List[FantasyPlayer]): The roster before the trade
            new_roster (List[FantasyPlayer]): The roster after the trade

        Returns:
            bool: True if trade is acceptable (violations don't increase), False otherwise

        Example:
            Team has 2 RBs (below MIN of 3) = 1 violation
            Trade gives them QB for WR (still 2 RBs) = 1 violation
            Result: True (violations stayed same)

            Trade gives them another QB for RB (now 1 RB) = 2 violations
            Result: False (violations got worse)
        """
        violations_before = self.count_min_position_violations(original_roster)
        violations_after = self.count_min_position_violations(new_roster)

        self.logger.debug(
            f"Min position violations - before: {violations_before}, after: {violations_after}"
        )

        result = violations_after <= violations_before

        if not result:
            self.logger.debug(
                f"Min position validation failed: trade would worsen violations "
                f"({violations_before} → {violations_after})"
            )

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
        if num_spots <= 0:
            self.logger.debug(f"No waiver recommendations needed (num_spots={num_spots})")
            return []

        available_players = self.player_manager.get_player_list(
            drafted_vals=[0],
            unlocked_only=True
        )

        if not available_players:
            self.logger.warning("No waiver wire players available for recommendations")
            return []

        scored_players: List[ScoredPlayer] = []
        for p in available_players:
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

        ranked_players = sorted(scored_players, key=lambda x: x.score, reverse=True)

        if post_trade_roster is not None:
            try:
                temp_team = FantasyTeam(self.config, post_trade_roster)

                filtered_recommendations = []
                for scored_player in ranked_players:
                    if temp_team.can_draft(scored_player.player):
                        filtered_recommendations.append(scored_player)
                        temp_team.draft_player(scored_player.player)

                        if len(filtered_recommendations) >= num_spots:
                            break

                result_count = len(filtered_recommendations)
                self.logger.debug(f"Generated {result_count} position-filtered waiver recommendations (requested: {num_spots})")
                return filtered_recommendations
            except ValueError as e:
                self.logger.debug(f"Cannot create temp team for position filtering: {e}")
                self.logger.debug("Post-trade roster already violates limits - returning no waiver recommendations")
                return []
        else:
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

        position_groups: Dict[str, List[FantasyPlayer]] = {pos: [] for pos in self.config.max_positions.keys()}

        for player in team.team:
            if player in exclude_players:
                continue

            if player.locked:
                continue

            if player.position in position_groups:
                position_groups[player.position].append(player)

        for players in position_groups.values():
            if not players:
                continue

            sorted_players = sorted(players, key=lambda p: p.score)

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
        position_counts = {pos: 0 for pos in self.config.max_positions.keys()}

        for player in post_trade_roster:
            if player.position in position_counts:
                position_counts[player.position] += 1

        over_limit_positions = []
        for position, count in position_counts.items():
            max_allowed = self.config.max_positions[position]
            if count > max_allowed:
                excess = count - max_allowed
                over_limit_positions.append((position, excess))
                self.logger.debug(f"Position {position} over limit: {count}/{max_allowed} (excess: {excess})")

        if over_limit_positions:
            droppable_players = []

            for position, excess in over_limit_positions:
                position_players = []
                for player in team.team:
                    if player in exclude_players:
                        continue

                    if player.locked:
                        continue

                    if player.position == position:
                        position_players.append(player)

                if position_players:
                    sorted_players = sorted(position_players, key=lambda p: p.score)
                    droppable_players.extend(sorted_players[:num_per_position])

            self.logger.info(f"Position-aware drop: Found {len(droppable_players)} candidates from {len(over_limit_positions)} over-limit positions")
            return droppable_players

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
        if my_dropped_players is None:
            my_dropped_players = []
        if their_dropped_players is None:
            their_dropped_players = []


        my_roster_unlocked = [p for p in my_team.team if not p.is_locked() and p.get_risk_level() != "HIGH"]
        my_locked_original = [p for p in my_team.team if p.is_locked() and p.get_risk_level() != "HIGH"]
        my_ir = [p for p in my_team.team if p.get_risk_level() == "HIGH"]

        their_roster_unlocked = [p for p in their_team.team if not p.is_locked() and p.get_risk_level() != "HIGH"]
        their_locked_original = [p for p in their_team.team if p.is_locked() and p.get_risk_level() != "HIGH"]
        their_ir = [p for p in their_team.team if p.get_risk_level() == "HIGH"]

        my_roster = my_roster_unlocked + [p for p in my_locked_original if p in my_selected_players]
        my_locked = [p for p in my_locked_original if p not in my_selected_players]

        their_roster = their_roster_unlocked + [p for p in their_locked_original if p in their_selected_players]
        their_locked = [p for p in their_locked_original if p not in their_selected_players]

        my_net_change = len(their_selected_players) - len(my_selected_players)
        their_net_change = len(my_selected_players) - len(their_selected_players)

        my_new_roster = [p for p in my_roster if p not in my_selected_players and p not in my_dropped_players] + their_selected_players
        their_new_roster = [p for p in their_roster if p not in their_selected_players and p not in their_dropped_players] + my_selected_players

        my_waiver_spots_needed = max(0, -my_net_change)
        their_waiver_spots_needed = max(0, -their_net_change)

        my_waiver_recs = self._get_waiver_recommendations(my_waiver_spots_needed, post_trade_roster=my_new_roster + my_locked)

        if is_waivers:
            their_waiver_recs = []
        else:
            their_waiver_recs = self._get_waiver_recommendations(their_waiver_spots_needed, post_trade_roster=their_new_roster + their_locked)

        my_new_roster_with_waivers = my_new_roster + [rec.player for rec in my_waiver_recs]
        their_new_roster_with_waivers = their_new_roster + [rec.player for rec in their_waiver_recs]

        my_full_roster = my_new_roster_with_waivers + my_locked
        my_original_full_roster = my_roster + my_locked
        my_roster_valid = self.validate_roster_lenient(my_original_full_roster, my_full_roster)

        their_full_roster = their_new_roster_with_waivers + their_locked
        their_original_full_roster = their_roster + their_locked

        self.logger.info(f"Their original roster size: {len(their_original_full_roster)}")
        self.logger.info(f"Their new roster size: {len(their_full_roster)}")
        self.logger.info(f"Their original positions: RB={sum(1 for p in their_original_full_roster if p.position=='RB')}, "
                        f"WR={sum(1 for p in their_original_full_roster if p.position=='WR')}, "
                        f"TE={sum(1 for p in their_original_full_roster if p.position=='TE')}")
        self.logger.info(f"Their new positions: RB={sum(1 for p in their_full_roster if p.position=='RB')}, "
                        f"WR={sum(1 for p in their_full_roster if p.position=='WR')}, "
                        f"TE={sum(1 for p in their_full_roster if p.position=='TE')}")

        if is_waivers:
            their_roster_valid = True
            self.logger.info("Skipping roster validation for waiver team")
        else:
            their_roster_valid = self.validate_roster_lenient(their_original_full_roster, their_full_roster)

        if not my_roster_valid or not their_roster_valid:
            my_drop_candidates = []
            their_drop_candidates = []

            if not my_roster_valid:
                my_drop_candidates = self._get_position_aware_drop_candidates(
                    my_team,
                    post_trade_roster=my_new_roster_with_waivers + my_locked,
                    exclude_players=my_selected_players,
                    num_per_position=2
                )
                self.logger.debug(f"My roster invalid - providing {len(my_drop_candidates)} drop candidates")

            if not their_roster_valid:
                if not is_waivers:
                    their_drop_candidates = self._get_position_aware_drop_candidates(
                        their_team,
                        post_trade_roster=their_new_roster_with_waivers + their_locked,
                        exclude_players=their_selected_players,
                        num_per_position=2
                    )
                    self.logger.debug(f"Their roster invalid - providing {len(their_drop_candidates)} drop candidates")

            return (None, my_drop_candidates, their_drop_candidates)

        my_new_team = TradeSimTeam(my_team.name, my_full_roster, self.player_manager, isOpponent=False, use_weekly_scoring=my_team.use_weekly_scoring)
        their_new_team = TradeSimTeam(their_team.name, their_full_roster, self.player_manager, isOpponent=True, use_weekly_scoring=their_team.use_weekly_scoring)

        my_original_scored = my_team.get_scored_players(my_selected_players)
        my_dropped_scored = my_team.get_scored_players(my_dropped_players) if my_dropped_players else []
        their_dropped_scored = their_team.get_scored_players(their_dropped_players) if their_dropped_players else []

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
        mode = "Waiver Optimizer" if is_waivers else "Trade Suggestor"
        self.logger.info(f"Generating trade combinations ({mode}): 1-for-1={one_for_one}, 2-for-2={two_for_two}, 3-for-3={three_for_three}")

        trade_combos: List[TradeSnapshot] = []


        my_roster = [p for p in my_team.team if not p.is_locked() and p.get_risk_level() != "HIGH"]
        my_locked = [p for p in my_team.team if p.is_locked() and p.get_risk_level() != "HIGH"]
        my_ir = [p for p in my_team.team if p.get_risk_level() == "HIGH"]

        their_roster = [p for p in their_team.team if not p.is_locked() and p.get_risk_level() != "HIGH"]
        their_locked = [p for p in their_team.team if p.is_locked() and p.get_risk_level() != "HIGH"]
        their_ir = [p for p in their_team.team if p.get_risk_level() == "HIGH"]

        my_original_full_roster = my_roster + my_locked
        their_original_full_roster = their_roster + their_locked

        self.logger.debug(f"Filtered rosters: my_tradeable={len(my_roster)}, my_locked={len(my_locked)}, my_ir={len(my_ir)}, their_tradeable={len(their_roster)}, their_locked={len(their_locked)}, their_ir={len(their_ir)}")

        from collections import Counter
        my_pos_counts = Counter(p.position for p in my_original_full_roster)
        self.logger.debug(f"=== MY ORIGINAL ROSTER FOR VALIDATION ===")
        self.logger.debug(f"  Total: {len(my_original_full_roster)} players")
        self.logger.debug(f"  Positions: {dict(my_pos_counts)}")
        self.logger.debug(f"  RB+WR (FLEX-eligible): {my_pos_counts.get('RB', 0) + my_pos_counts.get('WR', 0)}")
        self.logger.debug(f"  Max slots: RB={self.config.max_positions.get('RB', 0)}, WR={self.config.max_positions.get('WR', 0)}, FLEX={self.config.max_positions.get('FLEX', 0)}")
        self.logger.debug(f"  Locked players: {[f'{p.name} ({p.position})' for p in my_locked]}")

        initial_violations = self.count_position_violations(my_original_full_roster)
        self.logger.debug(f"  INITIAL VIOLATIONS: {initial_violations}")
        if initial_violations > 0:
            self.logger.warning(f"WARNING: Original roster already has {initial_violations} position violation(s)!")

        def validate_trade_roster(original_full: List[FantasyPlayer], new_full: List[FantasyPlayer]) -> bool:
            """Helper to validate roster using lenient rules if ignore_max_positions=False"""
            if ignore_max_positions:
                return len(new_full) <= self.config.max_players
            else:
                return self.validate_roster_lenient(original_full, new_full)

        my_unlocked_count = len(my_roster)
        their_unlocked_count = len(their_roster)

        one_for_one_combos = my_unlocked_count * their_unlocked_count if one_for_one else 0
        two_for_two_combos = (my_unlocked_count * (my_unlocked_count - 1) // 2) * (their_unlocked_count * (their_unlocked_count - 1) // 2) if two_for_two else 0
        three_for_three_combos = (my_unlocked_count * (my_unlocked_count - 1) * (my_unlocked_count - 2) // 6) * (their_unlocked_count * (their_unlocked_count - 1) * (their_unlocked_count - 2) // 6) if three_for_three else 0
        two_for_one_combos = (my_unlocked_count * (my_unlocked_count - 1) // 2) * their_unlocked_count if two_for_one else 0
        one_for_two_combos = my_unlocked_count * (their_unlocked_count * (their_unlocked_count - 1) // 2) if one_for_two else 0
        three_for_one_combos = (my_unlocked_count * (my_unlocked_count - 1) * (my_unlocked_count - 2) // 6) * their_unlocked_count if three_for_one else 0
        one_for_three_combos = my_unlocked_count * (their_unlocked_count * (their_unlocked_count - 1) * (their_unlocked_count - 2) // 6) if one_for_three else 0
        three_for_two_combos = (my_unlocked_count * (my_unlocked_count - 1) * (my_unlocked_count - 2) // 6) * (their_unlocked_count * (their_unlocked_count - 1) // 2) if three_for_two else 0
        two_for_three_combos = (my_unlocked_count * (my_unlocked_count - 1) // 2) * (their_unlocked_count * (their_unlocked_count - 1) * (their_unlocked_count - 2) // 6) if two_for_three else 0
        total_combos = (one_for_one_combos + two_for_two_combos + three_for_three_combos +
                        two_for_one_combos + one_for_two_combos + three_for_one_combos +
                        one_for_three_combos + three_for_two_combos + two_for_three_combos)

        if total_combos > self.config.trade_max_combinations:
            type_counts = [
                ("1-for-1", one_for_one_combos),
                ("2-for-2", two_for_two_combos),
                ("3-for-3", three_for_three_combos),
                ("2-for-1", two_for_one_combos),
                ("1-for-2", one_for_two_combos),
                ("3-for-1", three_for_one_combos),
                ("1-for-3", one_for_three_combos),
                ("3-for-2", three_for_two_combos),
                ("2-for-3", two_for_three_combos),
            ]
            enabled_types = [(name, count) for name, count in type_counts if count > 0]
            enabled_types.sort(key=lambda x: x[1], reverse=True)
            enabled_lines = "\n".join(f"  {name}: {count:,} combinations" for name, count in enabled_types)

            key_map = {
                "3-for-3": "ENABLE_THREE_FOR_THREE",
                "2-for-3": "ENABLE_TWO_FOR_THREE",
                "3-for-2": "ENABLE_THREE_FOR_TWO",
                "2-for-2": "ENABLE_TWO_FOR_TWO",
                "3-for-1": "ENABLE_THREE_FOR_ONE",
                "1-for-3": "ENABLE_ONE_FOR_THREE",
                "2-for-1": "ENABLE_TWO_FOR_ONE",
                "1-for-2": "ENABLE_ONE_FOR_TWO",
                "1-for-1": "ENABLE_ONE_FOR_ONE",
            }
            top_disable = [name for name, _ in enabled_types[:3]]
            config_lines = [f'    "{key_map[name]}": false,' for name in top_disable]
            config_snippet = "\n".join(config_lines).rstrip(",")

            print(
                f"\nTRADE COMBINATION LIMIT EXCEEDED\n"
                f"Expected {total_combos:,} combinations (limit: {self.config.trade_max_combinations:,})\n"
                f"\nEnabled trade types contributing most combinations:\n"
                f"{enabled_lines}\n"
                f"\nTo reduce combinations, disable one or more of these trade types in league_config.json:\n"
                f'  "TRADE_SIMULATOR": {{\n'
                f"{config_snippet}\n"
                f"  }}\n"
                f"\nSkipping trade analysis for this opponent.\n"
            )
            self.logger.warning(
                f"Trade combination limit exceeded: {total_combos:,} combinations "
                f"(limit: {self.config.trade_max_combinations:,}). Skipping trade analysis."
            )
            return []

        if one_for_one:
            for my_player in my_roster:
                for their_player in their_roster:

                    my_new_roster = [p for p in my_roster if p.id != my_player.id] + [their_player]
                    their_new_roster = [p for p in their_roster if p.id != their_player.id] + [my_player]

                    my_full_roster = my_new_roster + my_locked
                    if not validate_trade_roster(my_original_full_roster, my_full_roster):
                        continue

                    if not ignore_max_positions:
                        if not self.validate_min_positions_lenient(my_original_full_roster, my_full_roster):
                            self.logger.debug("Trade rejected: would worsen minimum position violations")
                            continue

                    their_full_roster = their_new_roster + their_locked
                    if not is_waivers:
                        if not validate_trade_roster(their_original_full_roster, their_full_roster):
                            continue

                    my_new_team = TradeSimTeam(my_team.name, my_full_roster, self.player_manager, isOpponent=False, use_weekly_scoring=my_team.use_weekly_scoring)
                    their_new_team = TradeSimTeam(their_team.name, their_full_roster, self.player_manager, isOpponent=True, use_weekly_scoring=their_team.use_weekly_scoring)

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
                            my_new_players=my_new_team.get_scored_players([their_player]),
                            their_new_team=their_new_team,
                            their_new_players=their_new_team.get_scored_players([my_player]),
                            my_original_players=my_original_scored
                        )
                        trade_combos.append(snapshot)

        if two_for_two:
            my_combos = list(combinations(my_roster, 2))
            their_combos = list(combinations(their_roster, 2))

            for my_players in my_combos:
                for their_players in their_combos:
                    my_new_roster = [p for p in my_roster if p not in my_players] + list(their_players)
                    their_new_roster = [p for p in their_roster if p not in their_players] + list(my_players)

                    my_full_roster = my_new_roster + my_locked
                    if not validate_trade_roster(my_original_full_roster, my_full_roster):
                        continue

                    if not ignore_max_positions:
                        if not self.validate_min_positions_lenient(my_original_full_roster, my_full_roster):
                            self.logger.debug("Trade rejected: would worsen minimum position violations")
                            continue

                    their_full_roster = their_new_roster + their_locked
                    if not is_waivers:
                        if not validate_trade_roster(their_original_full_roster, their_full_roster):
                            continue

                    my_new_team = TradeSimTeam(my_team.name, my_full_roster, self.player_manager, isOpponent=False, use_weekly_scoring=my_team.use_weekly_scoring)
                    their_new_team = TradeSimTeam(their_team.name, their_full_roster, self.player_manager, isOpponent=True, use_weekly_scoring=their_team.use_weekly_scoring)

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
                            my_original_players=my_original_scored
                        )
                        trade_combos.append(snapshot)

        if three_for_three:
            my_combos = list(combinations(my_roster, 3))
            their_combos = list(combinations(their_roster, 3))

            for my_players in my_combos:
                for their_players in their_combos:
                    my_new_roster = [p for p in my_roster if p not in my_players] + list(their_players)
                    their_new_roster = [p for p in their_roster if p not in their_players] + list(my_players)

                    my_full_roster = my_new_roster + my_locked
                    if not validate_trade_roster(my_original_full_roster, my_full_roster):
                        continue

                    if not ignore_max_positions:
                        if not self.validate_min_positions_lenient(my_original_full_roster, my_full_roster):
                            self.logger.debug("Trade rejected: would worsen minimum position violations")
                            continue

                    their_full_roster = their_new_roster + their_locked
                    if not is_waivers:
                        if not validate_trade_roster(their_original_full_roster, their_full_roster):
                            continue

                    my_new_team = TradeSimTeam(my_team.name, my_full_roster, self.player_manager, isOpponent=False, use_weekly_scoring=my_team.use_weekly_scoring)
                    their_new_team = TradeSimTeam(their_team.name, their_full_roster, self.player_manager, isOpponent=True, use_weekly_scoring=their_team.use_weekly_scoring)

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
                            my_original_players=my_original_scored
                        )
                        trade_combos.append(snapshot)

        if two_for_one:
            my_combos = list(combinations(my_roster, 2))

            for my_players in my_combos:
                for their_player in their_roster:
                    my_new_roster = [p for p in my_roster if p not in my_players] + [their_player]
                    their_new_roster = [p for p in their_roster if p != their_player] + list(my_players)

                    my_waiver_recs = self._get_waiver_recommendations(num_spots=1, post_trade_roster=my_new_roster + my_locked)
                    their_waiver_recs = []

                    my_new_roster_with_waivers = my_new_roster + [rec.player for rec in my_waiver_recs]
                    their_new_roster_with_waivers = their_new_roster

                    my_full_roster = my_new_roster_with_waivers + my_locked
                    if not validate_trade_roster(my_original_full_roster, my_full_roster):
                        continue

                    if not ignore_max_positions:
                        if not self.validate_min_positions_lenient(my_original_full_roster, my_full_roster):
                            self.logger.debug("Trade rejected: would worsen minimum position violations")
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
                            for drop_player in drop_candidates:
                                their_roster_with_drop = [p for p in their_new_roster_with_waivers if p != drop_player]
                                their_full_roster_with_drop = their_roster_with_drop + their_locked

                                if not validate_trade_roster(their_original_full_roster, their_full_roster_with_drop):
                                    continue

                                my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers + my_locked, self.player_manager, isOpponent=False, use_weekly_scoring=my_team.use_weekly_scoring)
                                their_new_team_with_drop = TradeSimTeam(their_team.name, their_roster_with_drop + their_locked, self.player_manager, isOpponent=True, use_weekly_scoring=their_team.use_weekly_scoring)

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

                    my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers + my_locked, self.player_manager, isOpponent=False, use_weekly_scoring=my_team.use_weekly_scoring)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers + their_locked, self.player_manager, isOpponent=True, use_weekly_scoring=their_team.use_weekly_scoring)

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

        if one_for_two:
            their_combos = list(combinations(their_roster, 2))

            for my_player in my_roster:
                for their_players in their_combos:
                    my_new_roster = [p for p in my_roster if p != my_player] + list(their_players)
                    their_new_roster = [p for p in their_roster if p not in their_players] + [my_player]

                    my_waiver_recs = []
                    their_waiver_recs = self._get_waiver_recommendations(num_spots=1, post_trade_roster=their_new_roster + their_locked) if not is_waivers else []

                    my_new_roster_with_waivers = my_new_roster
                    their_new_roster_with_waivers = their_new_roster + [rec.player for rec in their_waiver_recs]

                    my_full_roster = my_new_roster_with_waivers + my_locked
                    my_roster_valid = validate_trade_roster(my_original_full_roster, my_full_roster)

                    if my_roster_valid and not ignore_max_positions:
                        my_roster_valid = self.validate_min_positions_lenient(my_original_full_roster, my_full_roster)
                        if not my_roster_valid:
                            self.logger.debug("Trade rejected: would worsen minimum position violations")

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

                            if not is_waivers:
                                their_full_roster = their_new_roster_with_waivers + their_locked
                                if not validate_trade_roster(their_original_full_roster, their_full_roster):
                                    continue

                            my_new_team_with_drop = TradeSimTeam(my_team.name, my_roster_with_drop + my_locked, self.player_manager, isOpponent=False, use_weekly_scoring=my_team.use_weekly_scoring)
                            their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers + their_locked, self.player_manager, isOpponent=True, use_weekly_scoring=their_team.use_weekly_scoring)

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

                    if not is_waivers:
                        their_full_roster = their_new_roster_with_waivers + their_locked
                        if not validate_trade_roster(their_original_full_roster, their_full_roster):
                            continue

                    my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers + my_locked, self.player_manager, isOpponent=False, use_weekly_scoring=my_team.use_weekly_scoring)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers + their_locked, self.player_manager, isOpponent=True, use_weekly_scoring=their_team.use_weekly_scoring)

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

        if three_for_one:
            my_combos = list(combinations(my_roster, 3))

            for my_players in my_combos:
                for their_player in their_roster:
                    my_new_roster = [p for p in my_roster if p not in my_players] + [their_player]
                    their_new_roster = [p for p in their_roster if p != their_player] + list(my_players)

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

                                my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers + my_locked, self.player_manager, isOpponent=False, use_weekly_scoring=my_team.use_weekly_scoring)
                                their_new_team_with_drops = TradeSimTeam(their_team.name, their_roster_with_drops + their_locked, self.player_manager, isOpponent=True, use_weekly_scoring=their_team.use_weekly_scoring)

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

                    my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers + my_locked, self.player_manager, isOpponent=False, use_weekly_scoring=my_team.use_weekly_scoring)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers + their_locked, self.player_manager, isOpponent=True, use_weekly_scoring=their_team.use_weekly_scoring)

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

        if one_for_three:
            their_combos = list(combinations(their_roster, 3))

            for my_player in my_roster:
                for their_players in their_combos:
                    my_new_roster = [p for p in my_roster if p != my_player] + list(their_players)
                    their_new_roster = [p for p in their_roster if p not in their_players] + [my_player]

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

                            my_new_team_with_drops = TradeSimTeam(my_team.name, my_roster_with_drops + my_locked, self.player_manager, isOpponent=False, use_weekly_scoring=my_team.use_weekly_scoring)
                            their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers + their_locked, self.player_manager, isOpponent=True, use_weekly_scoring=their_team.use_weekly_scoring)

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

                    my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers + my_locked, self.player_manager, isOpponent=False, use_weekly_scoring=my_team.use_weekly_scoring)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers + their_locked, self.player_manager, isOpponent=True, use_weekly_scoring=their_team.use_weekly_scoring)

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

        if three_for_two:
            my_combos = list(combinations(my_roster, 3))
            their_combos = list(combinations(their_roster, 2))

            for my_players in my_combos:
                for their_players in their_combos:
                    my_new_roster = [p for p in my_roster if p not in my_players] + list(their_players)
                    their_new_roster = [p for p in their_roster if p not in their_players] + list(my_players)

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

                                my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers + my_locked, self.player_manager, isOpponent=False, use_weekly_scoring=my_team.use_weekly_scoring)
                                their_new_team_with_drop = TradeSimTeam(their_team.name, their_roster_with_drop + their_locked, self.player_manager, isOpponent=True, use_weekly_scoring=their_team.use_weekly_scoring)

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

                    my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers + my_locked, self.player_manager, isOpponent=False, use_weekly_scoring=my_team.use_weekly_scoring)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers + their_locked, self.player_manager, isOpponent=True, use_weekly_scoring=their_team.use_weekly_scoring)

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

        if two_for_three:
            my_combos = list(combinations(my_roster, 2))
            their_combos = list(combinations(their_roster, 3))

            for my_players in my_combos:
                for their_players in their_combos:
                    my_new_roster = [p for p in my_roster if p not in my_players] + list(their_players)
                    their_new_roster = [p for p in their_roster if p not in their_players] + list(my_players)

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

                            my_new_team_with_drop = TradeSimTeam(my_team.name, my_roster_with_drop + my_locked, self.player_manager, isOpponent=False, use_weekly_scoring=my_team.use_weekly_scoring)
                            their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers + their_locked, self.player_manager, isOpponent=True, use_weekly_scoring=their_team.use_weekly_scoring)

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

                    my_new_team = TradeSimTeam(my_team.name, my_new_roster_with_waivers + my_locked, self.player_manager, isOpponent=False, use_weekly_scoring=my_team.use_weekly_scoring)
                    their_new_team = TradeSimTeam(their_team.name, their_new_roster_with_waivers + their_locked, self.player_manager, isOpponent=True, use_weekly_scoring=their_team.use_weekly_scoring)

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

        self.logger.info(f"Generated {len(trade_combos)} valid trade combinations")

        return trade_combos


