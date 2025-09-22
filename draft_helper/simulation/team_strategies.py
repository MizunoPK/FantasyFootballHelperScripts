"""
Team strategy implementations for draft simulation.

Implements different AI opponent behaviors and decision-making strategies.
"""

import random
from typing import List, Dict, Any, Optional
import sys
import os

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from shared_files.FantasyPlayer import FantasyPlayer
from draft_helper.FantasyTeam import FantasyTeam
from draft_helper import draft_helper_config as base_config


class TeamStrategyManager:
    """Manages different team strategies for draft simulation"""

    def __init__(self, config_params: Dict[str, Any]):
        self.config_params = config_params

        # Override base config with simulation parameters
        self.injury_penalties = {
            "LOW": 0,
            "MEDIUM": config_params.get('INJURY_PENALTIES_MEDIUM', 25),
            "HIGH": config_params.get('INJURY_PENALTIES_HIGH', 50)
        }
        self.pos_needed_score = config_params.get('POS_NEEDED_SCORE', 50)
        self.projection_base_score = config_params.get('PROJECTION_BASE_SCORE', 100)
        self.base_bye_penalty = config_params.get('BASE_BYE_PENALTY', 20)

    def get_team_picks(self, strategy: str, available_players: List[FantasyPlayer],
                      team_roster: FantasyTeam, round_num: int) -> List[FantasyPlayer]:
        """Get prioritized list of picks for a team based on strategy"""

        if strategy == 'conservative':
            return self._conservative_strategy(available_players, team_roster, round_num)
        elif strategy == 'aggressive':
            return self._aggressive_strategy(available_players, team_roster, round_num)
        elif strategy == 'positional':
            return self._positional_strategy(available_players, team_roster, round_num)
        elif strategy == 'value':
            return self._value_strategy(available_players, team_roster, round_num)
        elif strategy == 'draft_helper':
            return self._draft_helper_strategy(available_players, team_roster, round_num)
        else:
            # Fallback to value strategy
            return self._value_strategy(available_players, team_roster, round_num)

    def _conservative_strategy(self, available_players: List[FantasyPlayer],
                             team_roster: FantasyTeam, round_num: int) -> List[FantasyPlayer]:
        """Conservative strategy: follows projections closely, avoids injury risk"""

        scored_players = []

        for player in available_players:
            if not team_roster.can_draft(player):
                continue

            # Base score from projections
            total_points = self._get_player_total_points(player)
            score = total_points

            # Heavy penalty for injury risk (conservative approach)
            injury_penalty = self.injury_penalties.get(player.injury_status, 0) * 2
            score -= injury_penalty

            # Slight positional need bonus
            positional_need = self._calculate_positional_need(player.position, team_roster)
            score += positional_need * 10

            scored_players.append((score, player))

        # Sort by score descending
        scored_players.sort(reverse=True, key=lambda x: x[0])
        return [player for score, player in scored_players]

    def _aggressive_strategy(self, available_players: List[FantasyPlayer],
                           team_roster: FantasyTeam, round_num: int) -> List[FantasyPlayer]:
        """Aggressive strategy: prioritizes high-upside players, ignores some risk"""

        scored_players = []

        for player in available_players:
            if not team_roster.can_draft(player):
                continue

            # Base score from projections
            total_points = self._get_player_total_points(player)
            score = total_points

            # Look for high weekly ceiling (upside)
            max_week_points = self._get_player_max_week_points(player)
            if max_week_points > 25:  # High ceiling bonus
                score += 50

            # Reduced injury penalty (risk tolerance)
            injury_penalty = self.injury_penalties.get(player.injury_status, 0) * 0.5
            score -= injury_penalty

            # Bonus for skill positions early
            if round_num <= 6 and player.position in ['RB', 'WR', 'QB']:
                score += 30

            scored_players.append((score, player))

        # Sort by score descending
        scored_players.sort(reverse=True, key=lambda x: x[0])
        return [player for score, player in scored_players]

    def _positional_strategy(self, available_players: List[FantasyPlayer],
                           team_roster: FantasyTeam, round_num: int) -> List[FantasyPlayer]:
        """Positional strategy: strict adherence to positional needs"""

        # Determine most needed position
        needed_positions = self._get_needed_positions(team_roster)

        if not needed_positions:
            # If no specific needs, fall back to value
            return self._value_strategy(available_players, team_roster, round_num)

        # Focus on most needed position
        primary_need = needed_positions[0]

        scored_players = []

        for player in available_players:
            if not team_roster.can_draft(player):
                continue

            # Base score from projections
            total_points = self._get_player_total_points(player)
            score = total_points

            # Heavy bonus for needed positions
            if player.position == primary_need:
                score += 100
            elif player.position in needed_positions:
                score += 50
            else:
                score -= 50  # Penalty for non-needed positions

            # Standard injury penalty
            injury_penalty = self.injury_penalties.get(player.injury_status, 0)
            score -= injury_penalty

            scored_players.append((score, player))

        # Sort by score descending
        scored_players.sort(reverse=True, key=lambda x: x[0])
        return [player for score, player in scored_players]

    def _value_strategy(self, available_players: List[FantasyPlayer],
                       team_roster: FantasyTeam, round_num: int) -> List[FantasyPlayer]:
        """Value strategy: best available player regardless of position"""

        scored_players = []

        for player in available_players:
            if not team_roster.can_draft(player):
                continue

            # Pure value: just total projected points
            total_points = self._get_player_total_points(player)
            score = total_points

            # Minimal positional adjustment
            positional_need = self._calculate_positional_need(player.position, team_roster)
            score += positional_need * 5

            # Standard injury penalty
            injury_penalty = self.injury_penalties.get(player.injury_status, 0)
            score -= injury_penalty

            scored_players.append((score, player))

        # Sort by score descending
        scored_players.sort(reverse=True, key=lambda x: x[0])
        return [player for score, player in scored_players]

    def _draft_helper_strategy(self, available_players: List[FantasyPlayer],
                             team_roster: FantasyTeam, round_num: int) -> List[FantasyPlayer]:
        """Draft helper strategy: uses similar logic to the actual draft helper"""

        # For now, use a simplified scoring approach similar to draft helper
        # Creating a full DraftHelper instance would be complex due to its dependencies
        scored_players = []

        for player in available_players:
            if not team_roster.can_draft(player):
                continue

            # Simplified draft helper-like scoring
            total_points = self._get_player_total_points(player)
            score = total_points * self.projection_base_score / 100

            # Add positional need score similar to draft helper
            positional_need = self._calculate_positional_need(player.position, team_roster)
            score += positional_need * self.pos_needed_score

            # Apply injury penalties
            injury_penalty = self.injury_penalties.get(player.injury_status, 0)
            score -= injury_penalty

            # Add bye week considerations
            bye_conflicts = self._calculate_bye_conflicts(player, team_roster)
            score -= bye_conflicts * self.base_bye_penalty

            scored_players.append((score, player))

        # Sort by score descending
        scored_players.sort(reverse=True, key=lambda x: x[0])
        return [player for score, player in scored_players]

    def _calculate_bye_conflicts(self, player: FantasyPlayer, team_roster: FantasyTeam) -> int:
        """Calculate number of bye week conflicts with current roster"""
        if not hasattr(player, 'bye_week'):
            return 0

        conflicts = 0
        for roster_player in team_roster.roster:
            if hasattr(roster_player, 'bye_week') and roster_player.bye_week == player.bye_week:
                conflicts += 1

        return conflicts

    def _calculate_positional_need(self, position: str, team_roster: FantasyTeam) -> float:
        """Calculate how much a position is needed (0-1 scale)"""

        if position == base_config.FLEX:
            # FLEX can be filled by RB or WR
            rb_count = len([p for p in team_roster.roster if p.position == 'RB'])
            wr_count = len([p for p in team_roster.roster if p.position == 'WR'])
            rb_need = max(0, base_config.MAX_POSITIONS.get('RB', 0) - rb_count)
            wr_need = max(0, base_config.MAX_POSITIONS.get('WR', 0) - wr_count)
            return max(rb_need, wr_need) / max(base_config.MAX_POSITIONS.get('RB', 1), 1)

        current_count = len([p for p in team_roster.roster if p.position == position])
        max_needed = base_config.MAX_POSITIONS.get(position, 0)

        if max_needed == 0:
            return 0.0

        need = max(0, max_needed - current_count)
        return need / max_needed

    def _get_needed_positions(self, team_roster: FantasyTeam) -> List[str]:
        """Get list of positions needed, ordered by priority"""

        needs = []

        for position, max_count in base_config.MAX_POSITIONS.items():
            current_count = len([p for p in team_roster.roster if p.position == position])
            if current_count < max_count:
                need_level = max_count - current_count
                needs.append((need_level, position))

        # Sort by need level descending
        needs.sort(reverse=True, key=lambda x: x[0])
        return [position for need_level, position in needs]

    def _get_player_total_points(self, player: FantasyPlayer) -> float:
        """Get total points for a player across all weeks"""
        total = 0.0
        for week in range(1, 18):
            week_attr = f'week_{week}_points'
            points = getattr(player, week_attr, 0.0) or 0.0
            total += points
        return total

    def _get_player_week_points(self, player: FantasyPlayer, week: int) -> float:
        """Get points for a player for a specific week"""
        week_attr = f'week_{week}_points'
        return getattr(player, week_attr, 0.0) or 0.0

    def _get_player_max_week_points(self, player: FantasyPlayer) -> float:
        """Get maximum weekly points for a player"""
        max_points = 0.0
        for week in range(1, 18):
            week_points = self._get_player_week_points(player, week)
            max_points = max(max_points, week_points)
        return max_points