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
from shared_files.enhanced_scoring import EnhancedScoringCalculator
from draft_helper.FantasyTeam import FantasyTeam
from shared_files.configs import draft_helper_config as base_config
from draft_helper.team_data_loader import TeamDataLoader
from draft_helper.core.normalization_calculator import NormalizationCalculator


class TeamStrategyManager:
    """Manages different team strategies for draft simulation"""

    def __init__(self, config_params: Dict[str, Any], draft_teams_csv_path: Optional[str] = None):
        self.config_params = config_params
        self.draft_teams_csv_path = draft_teams_csv_path

        # Override base config with simulation parameters
        self.injury_penalties = {
            "LOW": 0,
            "MEDIUM": config_params.get('INJURY_PENALTIES_MEDIUM', 25),
            "HIGH": config_params.get('INJURY_PENALTIES_HIGH', 50)
        }
        # DEPRECATED: Legacy scoring weights (no longer used in current scoring system)
        # self.pos_needed_score = config_params.get('POS_NEEDED_SCORE', 50)
        # self.projection_base_score = config_params.get('PROJECTION_BASE_SCORE', 100)
        self.base_bye_penalty = config_params.get('BASE_BYE_PENALTY', 20)

        # DRAFT_ORDER bonus configuration from simulation parameters
        self.draft_order_primary_bonus = config_params.get('DRAFT_ORDER_PRIMARY_BONUS', base_config.DRAFT_ORDER_PRIMARY_BONUS)
        self.draft_order_secondary_bonus = config_params.get('DRAFT_ORDER_SECONDARY_BONUS', base_config.DRAFT_ORDER_SECONDARY_BONUS)

        # Rebuild DRAFT_ORDER array with simulation-specific bonus values
        self.draft_order = self._build_draft_order()

        # Enhanced scoring configuration from simulation parameters
        enhanced_scoring_config = {
            # ADP multipliers
            'adp_excellent_multiplier': config_params.get('ADP_EXCELLENT_MULTIPLIER', 1.15),
            'adp_good_multiplier': config_params.get('ADP_GOOD_MULTIPLIER', 1.08),
            'adp_poor_multiplier': config_params.get('ADP_POOR_MULTIPLIER', 0.92),

            # Player rating multipliers
            'player_rating_excellent_multiplier': config_params.get('PLAYER_RATING_EXCELLENT_MULTIPLIER', 1.20),
            'player_rating_good_multiplier': config_params.get('PLAYER_RATING_GOOD_MULTIPLIER', 1.10),
            'player_rating_poor_multiplier': config_params.get('PLAYER_RATING_POOR_MULTIPLIER', 0.90),

            # Team quality multipliers
            'team_excellent_multiplier': config_params.get('TEAM_EXCELLENT_MULTIPLIER', 1.12),
            'team_good_multiplier': config_params.get('TEAM_GOOD_MULTIPLIER', 1.06),
            'team_poor_multiplier': config_params.get('TEAM_POOR_MULTIPLIER', 0.94),

            # Adjustment caps
            'max_total_adjustment': config_params.get('MAX_TOTAL_ADJUSTMENT', 1.50),
            'min_total_adjustment': config_params.get('MIN_TOTAL_ADJUSTMENT', 0.70)
        }

        # Consistency/Volatility multipliers from simulation parameters
        # Store these separately for dynamic config override
        self.consistency_multipliers = {
            'LOW': config_params.get('CONSISTENCY_LOW_MULTIPLIER', 1.08),
            'MEDIUM': config_params.get('CONSISTENCY_MEDIUM_MULTIPLIER', 1.00),
            'HIGH': config_params.get('CONSISTENCY_HIGH_MULTIPLIER', 0.92)
        }

        # Normalization scale from simulation parameters
        normalization_scale = config_params.get('NORMALIZATION_MAX_SCALE', 100.0)
        self.normalization_calculator = NormalizationCalculator(normalization_scale)

        # Initialize enhanced scoring calculator with configuration
        self.enhanced_scorer = EnhancedScoringCalculator(enhanced_scoring_config)

        # Initialize team data loader for offensive/defensive rankings using week 0 teams data
        if draft_teams_csv_path:
            self.team_data_loader = TeamDataLoader(draft_teams_csv_path)
        else:
            self.team_data_loader = TeamDataLoader()

    def _build_draft_order(self) -> List[Dict[str, float]]:
        """Build DRAFT_ORDER array using simulation-specific bonus values"""
        P = self.draft_order_primary_bonus
        S = self.draft_order_secondary_bonus

        # Same structure as draft_helper_config.py but with simulation values
        return [
            {base_config.FLEX: P, base_config.QB: S},        # Round 1
            {base_config.FLEX: P, base_config.QB: S},        # Round 2
            {base_config.FLEX: P, base_config.QB: S+5},      # Round 3
            {base_config.FLEX: P, base_config.QB: S+5},      # Round 4
            {base_config.QB: P, base_config.FLEX: S},        # Round 5
            {base_config.TE: P, base_config.FLEX: S},        # Round 6
            {base_config.FLEX: P},                           # Round 7
            {base_config.QB: P, base_config.FLEX: S},        # Round 8
            {base_config.TE: P, base_config.FLEX: S},        # Round 9
            {base_config.FLEX: P},                           # Round 10
            {base_config.FLEX: P},                           # Round 11
            {base_config.K: P},                              # Round 12
            {base_config.DST: P},                            # Round 13
            {base_config.FLEX: P},                           # Round 14
            {base_config.FLEX: P}                            # Round 15
        ]

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
        """Draft helper strategy: uses enhanced scoring with simulation parameter variations"""

        scored_players = []

        # STEP 1: Calculate max player points for normalization (done once per strategy call)
        max_player_points = max(
            (self._get_player_total_points(p) for p in available_players if not team_roster.can_draft(p) is False),
            default=1.0
        )

        for player in available_players:
            if not team_roster.can_draft(player):
                continue

            # Calculate player's total points and normalize using simulation's normalization scale
            player_total_points = self._get_player_total_points(player)
            normalized_points = self.normalization_calculator.normalize_player_score(
                player_total_points, max_player_points
            )

            # STEP 2: Apply enhanced scoring with current parameter configuration
            try:
                team_offensive_rank = self.team_data_loader.get_team_offensive_rank(player.team)
                team_defensive_rank = self.team_data_loader.get_team_defensive_rank(player.team)

                enhanced_result = self.enhanced_scorer.calculate_enhanced_score(
                    base_fantasy_points=normalized_points,
                    position=player.position,
                    adp=getattr(player, 'average_draft_position', None),
                    player_rating=getattr(player, 'player_rating', None),
                    team_offensive_rank=team_offensive_rank,
                    team_defensive_rank=team_defensive_rank
                )

                # Get enhanced score (projection_base_score deprecated - no longer used)
                enhanced_score = enhanced_result['enhanced_score']
            except Exception:
                # Fallback to basic scoring if enhanced scoring fails
                enhanced_score = normalized_points

            # Apply consistency/volatility multiplier
            consistency_score = self._apply_consistency_multiplier(enhanced_score, player)

            # Add DRAFT_ORDER bonus based on current round (roster size)
            draft_order_bonus = self._calculate_draft_order_bonus(player.position, team_roster)
            final_score = consistency_score + draft_order_bonus

            # Apply injury penalties
            injury_penalty = self.injury_penalties.get(player.injury_status, 0)
            final_score -= injury_penalty

            # Add bye week considerations (scaled by position capacity)
            bye_conflicts = self._calculate_bye_conflicts(player, team_roster)
            max_position_slots = base_config.MAX_POSITIONS.get(player.position, 1)
            if max_position_slots > 0:
                bye_penalty = (bye_conflicts / max_position_slots) * self.base_bye_penalty
                final_score -= bye_penalty

            scored_players.append((final_score, player))

        # Sort by score descending
        scored_players.sort(reverse=True, key=lambda x: x[0])
        return [player for score, player in scored_players]

    def _calculate_draft_order_bonus(self, position: str, team_roster: FantasyTeam) -> float:
        """Calculate DRAFT_ORDER bonus based on current round (roster size)"""
        current_round = len(team_roster.roster)  # 0-indexed

        # Check if roster is full
        if current_round >= len(self.draft_order):
            return 0.0

        round_priorities = self.draft_order[current_round]

        # Check direct position match
        if position in round_priorities:
            return round_priorities[position]

        # Check FLEX eligibility (RB or WR)
        if position in base_config.FLEX_ELIGIBLE_POSITIONS and base_config.FLEX in round_priorities:
            return round_priorities[base_config.FLEX]

        return 0.0

    def _calculate_bye_conflicts(self, player: FantasyPlayer, team_roster: FantasyTeam) -> int:
        """Calculate number of same-position bye week conflicts with current roster"""
        if not hasattr(player, 'bye_week'):
            return 0

        conflicts = 0
        for roster_player in team_roster.roster:
            if (roster_player.position == player.position and
                hasattr(roster_player, 'bye_week') and
                roster_player.bye_week == player.bye_week):
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

    def _apply_consistency_multiplier(self, base_score: float, player: FantasyPlayer) -> float:
        """
        Apply consistency/volatility multiplier based on player's week-to-week variance.

        Uses coefficient of variation (CV) to categorize players:
        - LOW volatility (CV < 0.3): Consistent performers
        - MEDIUM volatility (0.3 <= CV <= 0.6): Neutral
        - HIGH volatility (CV > 0.6): Boom/bust players

        Args:
            base_score: Score before consistency adjustment
            player: Player to analyze

        Returns:
            Score after applying consistency multiplier
        """
        # Import ConsistencyCalculator
        from shared_files.consistency_calculator import ConsistencyCalculator

        try:
            # Calculate consistency metrics
            consistency_calc = ConsistencyCalculator()
            result = consistency_calc.calculate_consistency_score(player)

            # Get multiplier from simulation config (overrides base config if provided)
            category = result['volatility_category']
            multiplier = self.consistency_multipliers.get(category, 1.0)

            return base_score * multiplier

        except Exception:
            # If consistency calculation fails, return base score unchanged
            return base_score