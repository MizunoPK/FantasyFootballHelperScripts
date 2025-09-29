#!/usr/bin/env python3
"""
Roster Calculator Module for Draft Helper

This module contains shared roster display and calculation logic used by both
the Waiver Optimizer and Trade Simulator.

Author: Kai Mizuno
Last Updated: September 2025
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Callable

# Add parent directories to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    from .. import draft_helper_constants as Constants
except ImportError:
    import draft_helper_constants as Constants


class RosterCalculator:
    """
    Handles shared roster display and calculation logic for fantasy team analysis.
    """

    def __init__(self, team, logger=None):
        """
        Initialize the RosterCalculator.

        Args:
            team: FantasyTeam instance
            logger: Optional logger for debugging
        """
        self.team = team
        self.logger = logger

    def display_roster_summary(self):
        """
        Display roster summary showing count and position breakdown.
        Same format as used in waiver optimizer.
        """
        print(f"Current roster: {len(self.team.roster)} / {Constants.MAX_PLAYERS} players")
        print("Your current roster by position:")
        for pos, count in self.team.pos_counts.items():
            print(f"  {pos}: {count}")

    def display_numbered_roster(self):
        """
        Display roster as numbered list 1-15 for trade simulator.
        Shows players in roster order with their details.

        Returns:
            List of players in display order for selection reference
        """
        print("\nCurrent Roster:")
        print("-" * 50)

        if not self.team.roster:
            print("No players in roster.")
            return []

        # Display each player with number
        for i, player in enumerate(self.team.roster, 1):
            locked_indicator = " (LOCKED)" if getattr(player, 'locked', False) else ""
            points_str = f"{getattr(player, 'fantasy_points', 0):.1f} pts"
            print(f"{i:2d}. {player.name} ({player.position} - {player.team}) - {points_str}{locked_indicator}")

        return self.team.roster

    def calculate_total_score(self, scoring_function: Callable) -> float:
        """
        Calculate total team score using the provided scoring function.

        Args:
            scoring_function: Function that takes a player and returns a score

        Returns:
            Total team score as float
        """
        return self.team.get_total_team_score(scoring_function)

    def calculate_position_scores(self, scoring_function: Callable) -> Dict[str, float]:
        """
        Calculate scores broken down by position.

        Args:
            scoring_function: Function that takes a player and returns a score

        Returns:
            Dictionary mapping position to total score for that position
        """
        position_scores = {}

        # Initialize all positions with 0
        for pos in Constants.MAX_POSITIONS.keys():
            position_scores[pos] = 0.0

        # Calculate scores for each player
        for player in self.team.roster:
            score = scoring_function(player)
            position = player.position

            # Add to position total
            if position in position_scores:
                position_scores[position] += score
            else:
                position_scores[position] = score

        return position_scores

    def display_score_breakdown(self, scoring_function: Callable, title: str = "Team Score Breakdown"):
        """
        Display total score and per-position breakdown.

        Args:
            scoring_function: Function that takes a player and returns a score
            title: Title to display above the breakdown
        """
        total_score = self.calculate_total_score(scoring_function)
        position_scores = self.calculate_position_scores(scoring_function)

        print(f"\n{title}")
        print("-" * len(title))
        print(f"Total Score: {total_score:.2f}")
        print("\nBy Position:")

        for pos, score in position_scores.items():
            if score > 0:  # Only show positions with players
                print(f"  {pos}: {score:.2f}")

    def compare_scores(self, scoring_function: Callable,
                      original_score: float,
                      original_position_scores: Dict[str, float],
                      title: str = "Score Comparison"):
        """
        Display score comparison between original and current roster.

        Args:
            scoring_function: Function that takes a player and returns a score
            original_score: Original total team score
            original_position_scores: Original position score breakdown
            title: Title to display above the comparison
        """
        current_score = self.calculate_total_score(scoring_function)
        current_position_scores = self.calculate_position_scores(scoring_function)

        total_difference = current_score - original_score

        print(f"\n{title}")
        print("=" * len(title))
        print(f"Original Score: {original_score:.2f}")
        print(f"Current Score:  {current_score:.2f}")
        print(f"Difference:     {total_difference:+.2f}")

        print("\nBy Position:")
        for pos in Constants.MAX_POSITIONS.keys():
            original = original_position_scores.get(pos, 0.0)
            current = current_position_scores.get(pos, 0.0)
            difference = current - original

            if original > 0 or current > 0:  # Only show positions with players
                print(f"  {pos}: {original:.2f} → {current:.2f} ({difference:+.2f})")

    def get_roster_state_snapshot(self):
        """
        Get a snapshot of current roster state for restoration later.

        Returns:
            Dictionary containing roster state information
        """
        return {
            'roster_copy': self.team.roster.copy(),
            'slot_assignments_copy': {slot: player_ids.copy()
                                    for slot, player_ids in self.team.slot_assignments.items()},
            'pos_counts_copy': self.team.pos_counts.copy(),
            'player_drafted_states': {player.id: player.drafted for player in self.team.roster}
        }

    def restore_roster_state(self, snapshot: Dict[str, Any]):
        """
        Restore roster state from a snapshot.

        Args:
            snapshot: State snapshot from get_roster_state_snapshot()
        """
        # Restore team state
        self.team.roster = snapshot['roster_copy']
        self.team.slot_assignments = snapshot['slot_assignments_copy']
        self.team.pos_counts = snapshot['pos_counts_copy']

        # Restore individual player drafted states
        for player_id, drafted_state in snapshot['player_drafted_states'].items():
            for player in self.team.roster:
                if hasattr(player, 'id') and player.id == player_id:
                    player.drafted = drafted_state
                    break