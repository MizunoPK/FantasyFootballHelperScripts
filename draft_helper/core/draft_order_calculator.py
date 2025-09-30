#!/usr/bin/env python3
"""
DRAFT_ORDER Calculator Module

This module handles round-based bonus calculations using the DRAFT_ORDER configuration.
Bonuses are applied to players whose positions match the draft strategy for the current round.

The system provides:
- Round-specific position bonuses
- Current draft round detection based on roster size
- Round assignment for existing roster players (display purposes)

Author: Kai Mizuno
Last Updated: September 2025
"""

import logging
from typing import Dict, List, Optional

try:
    from .. import draft_helper_constants as Constants
except ImportError:
    import draft_helper_constants as Constants

try:
    from ...shared_files.FantasyPlayer import FantasyPlayer
except ImportError:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from shared_files.FantasyPlayer import FantasyPlayer


class DraftOrderCalculator:
    """
    Calculates DRAFT_ORDER round-based bonuses for draft recommendations.

    This calculator determines the current draft round and applies position-specific
    bonuses based on the configured draft strategy from DRAFT_ORDER.

    Example:
        Round 1: {FLEX: 50, QB: 25}
        - RB (FLEX-eligible) gets +50 bonus
        - QB gets +25 bonus
        - TE gets +0 bonus (not in priorities)
    """

    def __init__(
        self,
        team,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize the DRAFT_ORDER calculator.

        Args:
            team: FantasyTeam instance
            logger: Logger instance for debugging
        """
        self.team = team
        self.logger = logger or logging.getLogger(__name__)

        self.logger.info("DraftOrderCalculator initialized")

    def get_current_draft_round(self) -> Optional[int]:
        """
        Determine the current draft round based on roster size.

        The current round is the next slot to fill. For example:
        - 0 players drafted → Round 1 (index 0)
        - 4 players drafted → Round 5 (index 4)
        - 15 players drafted → None (draft complete)

        Returns:
            int: Current round index (0-indexed for DRAFT_ORDER access), or None if draft complete
        """
        roster_size = len(self.team.roster)

        if roster_size >= Constants.MAX_PLAYERS:
            self.logger.debug("Draft complete, no current round")
            return None

        self.logger.debug(
            f"Current draft round: {roster_size + 1} (index {roster_size}), "
            f"roster size: {roster_size}/{Constants.MAX_PLAYERS}"
        )

        return roster_size

    def get_round_priorities(self, round_index: int) -> Dict[str, float]:
        """
        Get position priorities for a specific round.

        Args:
            round_index: Zero-indexed round number (0 = Round 1, 4 = Round 5, etc.)

        Returns:
            dict: Position -> bonus points mapping (e.g., {'FLEX': 50, 'QB': 25})
        """
        if round_index is None or round_index >= len(Constants.DRAFT_ORDER):
            return {}

        priorities = Constants.DRAFT_ORDER[round_index]

        self.logger.debug(
            f"Round {round_index + 1} priorities: {priorities}"
        )

        return priorities

    def calculate_bonus(self, player: FantasyPlayer) -> float:
        """
        Calculate DRAFT_ORDER bonus for a player based on current round.

        The bonus is determined by:
        1. Get current draft round
        2. Get position priorities for that round
        3. Check if player's position matches any priority
        4. Return corresponding bonus value (or 0 if no match)

        Args:
            player: Player to calculate bonus for

        Returns:
            float: Bonus points to add to player's score
        """
        # Get current round
        current_round = self.get_current_draft_round()

        if current_round is None:
            self.logger.debug("Draft complete, no bonus")
            return 0.0

        # Get priorities for this round
        round_priorities = self.get_round_priorities(current_round)

        if not round_priorities:
            self.logger.debug(f"No priorities defined for round {current_round + 1}, no bonus")
            return 0.0

        player_position = player.position

        # Check direct position match
        if player_position in round_priorities:
            bonus = round_priorities[player_position]
            self.logger.info(
                f"DRAFT_ORDER bonus for {player.name} ({player_position}): "
                f"+{bonus:.1f} pts (Round {current_round + 1} priority)"
            )
            return bonus

        # Check FLEX eligibility
        if player_position in Constants.FLEX_ELIGIBLE_POSITIONS and Constants.FLEX in round_priorities:
            bonus = round_priorities[Constants.FLEX]
            self.logger.info(
                f"DRAFT_ORDER bonus for {player.name} ({player_position}→FLEX): "
                f"+{bonus:.1f} pts (Round {current_round + 1} priority)"
            )
            return bonus

        # No match
        self.logger.debug(
            f"No DRAFT_ORDER bonus for {player.name} ({player_position}) "
            f"in Round {current_round + 1} (priorities: {list(round_priorities.keys())})"
        )
        return 0.0

    def assign_players_to_rounds(self) -> Dict[int, FantasyPlayer]:
        """
        Assign existing roster players to draft rounds for display purposes.

        This uses a first-fit strategy based on position matching:
        - Loop through each round
        - Find highest priority position for that round
        - Assign first unassigned player matching that position

        Note: Assignment order doesn't matter for scoring - it's only for display.
        The system just ensures enough positions are rostered to fill DRAFT_ORDER slots.

        Returns:
            dict: Mapping of round_number (1-15) -> FantasyPlayer
        """
        round_assignments = {}
        unassigned_players = self.team.roster.copy()

        self.logger.debug(
            f"Assigning {len(unassigned_players)} roster players to rounds..."
        )

        for round_num in range(1, Constants.MAX_PLAYERS + 1):
            if not unassigned_players:
                break

            round_index = round_num - 1
            round_priorities = Constants.DRAFT_ORDER[round_index]

            if not round_priorities:
                continue

            # Find highest priority position for this round
            highest_priority = max(round_priorities, key=round_priorities.get)

            # Find first player matching this position
            for player in unassigned_players:
                position_matches = (
                    player.position == highest_priority or
                    (player.position in Constants.FLEX_ELIGIBLE_POSITIONS and
                     highest_priority == Constants.FLEX)
                )

                if position_matches:
                    round_assignments[round_num] = player
                    unassigned_players.remove(player)
                    self.logger.debug(
                        f"Assigned {player.name} ({player.position}) to Round {round_num} "
                        f"(priority: {highest_priority})"
                    )
                    break

        if unassigned_players:
            self.logger.warning(
                f"{len(unassigned_players)} players could not be assigned to rounds: "
                f"{[p.name for p in unassigned_players]}"
            )

        return round_assignments

    def validate_roster_composition(self) -> bool:
        """
        Verify that roster composition aligns with DRAFT_ORDER position expectations.

        This is a critical invariant - the system should NEVER allow a roster
        that violates DRAFT_ORDER position requirements.

        Returns:
            bool: True if roster matches DRAFT_ORDER expectations, False otherwise
        """
        roster = self.team.roster

        # Count positions in roster
        position_counts = {}
        for player in roster:
            pos = player.position
            position_counts[pos] = position_counts.get(pos, 0) + 1

        # Count expected positions from DRAFT_ORDER (up to roster size)
        expected_position_slots = {}
        for round_index in range(len(roster)):
            if round_index >= len(Constants.DRAFT_ORDER):
                break

            round_priorities = Constants.DRAFT_ORDER[round_index]
            if not round_priorities:
                continue

            highest_priority = max(round_priorities, key=round_priorities.get)

            if highest_priority == Constants.FLEX:
                # FLEX can be RB or WR - check we have enough combined
                expected_position_slots[Constants.FLEX] = expected_position_slots.get(Constants.FLEX, 0) + 1
            else:
                expected_position_slots[highest_priority] = expected_position_slots.get(highest_priority, 0) + 1

        # Verify we have enough of each position type
        for position, expected_count in expected_position_slots.items():
            if position == Constants.FLEX:
                # FLEX can be filled by RB or WR
                flex_count = position_counts.get('RB', 0) + position_counts.get('WR', 0)
                if flex_count < expected_count:
                    self.logger.error(
                        f"Roster composition invalid: Expected at least {expected_count} FLEX-eligible players "
                        f"(RB+WR), but found {flex_count}"
                    )
                    return False
            else:
                actual_count = position_counts.get(position, 0)
                if actual_count < expected_count:
                    self.logger.error(
                        f"Roster composition invalid: Expected at least {expected_count} {position} players, "
                        f"but found {actual_count}"
                    )
                    return False

        self.logger.debug("Roster composition validates against DRAFT_ORDER expectations")
        return True

    def get_bonus_info(self, player: FantasyPlayer) -> dict:
        """
        Get detailed bonus information for debugging/logging.

        Args:
            player: Player to analyze

        Returns:
            dict: Bonus details including round, priorities, match status, and bonus value
        """
        current_round = self.get_current_draft_round()

        if current_round is None:
            return {
                'player_name': player.name,
                'position': player.position,
                'current_round': None,
                'draft_complete': True,
                'bonus': 0.0
            }

        round_priorities = self.get_round_priorities(current_round)
        bonus = self.calculate_bonus(player)

        # Determine match type
        if player.position in round_priorities:
            match_type = 'direct'
        elif player.position in Constants.FLEX_ELIGIBLE_POSITIONS and Constants.FLEX in round_priorities:
            match_type = 'flex'
        else:
            match_type = 'none'

        return {
            'player_name': player.name,
            'position': player.position,
            'current_round': current_round + 1,  # 1-indexed for display
            'round_priorities': round_priorities,
            'match_type': match_type,
            'bonus': bonus,
            'draft_complete': False
        }