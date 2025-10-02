#!/usr/bin/env python3
"""
Bye Week Visualizer Module for Draft Helper

This module provides bye week visualization functionality for the waiver optimizer
and trade simulator. It displays bye week summaries showing which players have
bye weeks in upcoming NFL weeks, and detects potential bye week conflicts.

Author: Kai Mizuno
Last Updated: October 2025
"""

import logging
from typing import List, Dict, Set, Optional
from collections import defaultdict

try:
    from shared_files.FantasyPlayer import FantasyPlayer
    from shared_files.configs.shared_config import CURRENT_NFL_WEEK
except ImportError:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from shared_files.FantasyPlayer import FantasyPlayer
    from shared_files.configs.shared_config import CURRENT_NFL_WEEK


class ByeWeekVisualizer:
    """
    Handles bye week visualization and conflict detection for fantasy rosters.
    """

    # Position sort order for display
    POSITION_ORDER = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']

    # Positions where having 2+ players on bye is a conflict
    STARTER_POSITIONS = {
        'RB': 2,  # Need 2 RBs to start (can use FLEX but conflict if both RBs out)
        'WR': 2,  # Need 2 WRs to start (can use FLEX but conflict if both WRs out)
        'QB': 1,  # Only start 1 QB
        'TE': 1,  # Only start 1 TE
        'K': 1,   # Only start 1 K
        'DST': 1  # Only start 1 DST
    }

    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize the ByeWeekVisualizer.

        Args:
            logger: Optional logger instance for debugging
        """
        self.logger = logger or logging.getLogger(__name__)

    def generate_bye_week_summary(self, roster: List[FantasyPlayer], current_week: int) -> str:
        """
        Generate a formatted bye week summary for the given roster.

        Shows all future weeks (current_week through week 18) with players who have
        bye weeks, sorted by position then alphabetically. Highlights bye week conflicts
        when multiple starters at the same position have the same bye week.

        Args:
            roster: List of FantasyPlayer objects in the roster
            current_week: Current NFL week number (from config)

        Returns:
            Formatted string containing the bye week summary
        """
        if not roster:
            return "\nBye Week Summary:\n" + "-" * 50 + "\nNo players in roster.\n"

        # Get players grouped by bye week
        bye_week_dict = self._get_players_by_bye_week(roster, current_week)

        # Detect bye week conflicts
        conflict_weeks = self._detect_bye_conflicts(bye_week_dict)

        # Build the summary string
        summary_lines = ["\nBye Week Summary:"]
        summary_lines.append("-" * 50)

        # Show all weeks from current_week through week 18
        for week in range(current_week, 19):
            if week in bye_week_dict and bye_week_dict[week]:
                # Sort players by position then name
                sorted_players = self._sort_players(bye_week_dict[week])

                # Format player list
                player_strings = [f"{p.name} ({p.position})" for p in sorted_players]
                player_list = ", ".join(player_strings)

                # Add conflict warning if applicable
                conflict_marker = " ⚠️ BYE WEEK CONFLICT" if week in conflict_weeks else ""

                summary_lines.append(f"Week {week}: {player_list}{conflict_marker}")
            else:
                summary_lines.append(f"Week {week}: None")

        return "\n".join(summary_lines)

    def _get_players_by_bye_week(
        self,
        roster: List[FantasyPlayer],
        current_week: int
    ) -> Dict[int, List[FantasyPlayer]]:
        """
        Group roster players by their bye week.

        Only includes weeks >= current_week (filters out past bye weeks).

        Args:
            roster: List of FantasyPlayer objects
            current_week: Current NFL week number

        Returns:
            Dictionary mapping week number to list of players with that bye week
        """
        bye_week_dict = defaultdict(list)

        for player in roster:
            # Get bye week, handle None or 0 as no bye week
            bye_week = getattr(player, 'bye_week', 0)
            if bye_week is None:
                bye_week = 0

            # Only include future bye weeks (>= current_week and <= 18)
            if bye_week >= current_week and bye_week <= 18:
                bye_week_dict[bye_week].append(player)

        return dict(bye_week_dict)

    def _sort_players(self, players: List[FantasyPlayer]) -> List[FantasyPlayer]:
        """
        Sort players by position order, then alphabetically by name.

        Position order: QB, RB, WR, TE, K, DST
        Unknown positions are sorted to the end.

        Args:
            players: List of FantasyPlayer objects to sort

        Returns:
            Sorted list of FantasyPlayer objects
        """
        def sort_key(player):
            # Get position index (unknown positions get high number)
            try:
                pos_index = self.POSITION_ORDER.index(player.position)
            except ValueError:
                pos_index = len(self.POSITION_ORDER)  # Unknown positions go last

            # Return tuple: (position_index, name) for sorting
            return (pos_index, player.name.lower())

        return sorted(players, key=sort_key)

    def _detect_bye_conflicts(self, bye_week_dict: Dict[int, List[FantasyPlayer]]) -> Set[int]:
        """
        Detect bye week conflicts where multiple starters at the same position have the same bye.

        Conflict rules:
        - 2+ RBs with same bye = conflict (need 2 RBs to start)
        - 2+ WRs with same bye = conflict (need 2 WRs to start)
        - 2+ of same single-starter position (QB, TE, K, DST) = conflict

        Args:
            bye_week_dict: Dictionary mapping week to list of players

        Returns:
            Set of week numbers that have bye week conflicts
        """
        conflict_weeks = set()

        for week, players in bye_week_dict.items():
            # Count players by position for this week
            position_counts = defaultdict(int)
            for player in players:
                position_counts[player.position] += 1

            # Check for conflicts based on starter requirements
            for position, count in position_counts.items():
                if position in self.STARTER_POSITIONS:
                    required_starters = self.STARTER_POSITIONS[position]
                    # Conflict if we have >= required starters on bye
                    # (e.g., 2+ RBs, 2+ WRs, or 2+ of any single-starter position)
                    if count >= required_starters and count >= 2:
                        conflict_weeks.add(week)
                        self.logger.debug(
                            f"Bye week conflict detected: Week {week} has {count} {position}s on bye"
                        )
                        break  # One conflict per week is enough

        return conflict_weeks

    def get_player_bye_week_string(self, player: FantasyPlayer) -> str:
        """
        Get a formatted bye week string for a single player.

        Useful for displaying player summaries in trade recommendations.

        Args:
            player: FantasyPlayer object

        Returns:
            String like "Bye: Week 7" or "Bye: None"
        """
        bye_week = getattr(player, 'bye_week', 0)
        if bye_week is None or bye_week == 0:
            return "Bye: None"
        return f"Bye: Week {bye_week}"
