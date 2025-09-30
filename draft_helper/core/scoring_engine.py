#!/usr/bin/env python3
"""
Scoring Engine Module for Draft Helper

This module handles all player scoring and penalty calculation functionality,
extracted from the main draft_helper.py for better modularity.

This engine implements four distinct scoring modes:
1. Add to Roster Mode: Draft recommendations with DRAFT_ORDER bonuses
2. Waiver Optimizer: Trade analysis without DRAFT_ORDER bonuses
3. Trade Simulator: Same as Waiver Optimizer
4. Starter Helper: Weekly lineup optimization (separate module)

Author: Kai Mizuno
Last Updated: September 2025
"""

import logging
from typing import Dict, List, Optional, Any

try:
    from .. import draft_helper_constants as Constants
except ImportError:
    import draft_helper_constants as Constants

try:
    from .normalization_calculator import NormalizationCalculator
    from .draft_order_calculator import DraftOrderCalculator
except ImportError:
    from normalization_calculator import NormalizationCalculator
    from draft_order_calculator import DraftOrderCalculator


class ScoringEngine:
    """
    Manages player scoring and penalty calculation operations for the draft helper.
    """

    def __init__(self, team, players: List, logger: Optional[logging.Logger] = None):
        """
        Initialize the ScoringEngine.

        Args:
            team: FantasyTeam instance
            players: List of all players
            logger: Logger instance for debugging
        """
        self.team = team
        self.players = players
        self.logger = logger or logging.getLogger(__name__)

        # Initialize calculator components
        try:
            from .. import draft_helper_config as config
            normalization_scale = config.NORMALIZATION_MAX_SCALE
        except ImportError:
            import draft_helper_config as config
            normalization_scale = config.NORMALIZATION_MAX_SCALE

        self.normalization_calculator = NormalizationCalculator(
            normalization_scale=normalization_scale,
            logger=self.logger
        )
        self.draft_order_calculator = DraftOrderCalculator(
            team=team,
            logger=self.logger
        )

        self.logger.info("ScoringEngine initialized with normalization and DRAFT_ORDER calculators")

    def score_player(self, p, enhanced_scorer=None, team_data_loader=None, positional_ranking_calculator=None):
        """
        Calculate score for Add to Roster Mode (7-step calculation).

        New Scoring System:
        1. Get normalized seasonal fantasy points (0-N scale)
        2. Apply ADP multiplier
        3. Apply Player Ranking multiplier
        4. Apply Team ranking multiplier
        5. Add DRAFT_ORDER bonus (round-based position priority)
        6. Subtract Bye Week penalty
        7. Subtract Injury penalty

        Args:
            p: FantasyPlayer to score
            enhanced_scorer: EnhancedScoringCalculator instance
            team_data_loader: TeamDataLoader instance
            positional_ranking_calculator: PositionalRankingCalculator instance

        Returns:
            float: Total score for the player
        """
        # STEP 1: Normalize seasonal fantasy points to 0-N scale
        normalized_score = self.normalization_calculator.normalize_player(p, self.players)
        self.logger.debug(f"Step 1 - Normalized score for {p.name}: {normalized_score:.2f}")

        # STEPS 2-4: Apply enhanced scoring (ADP, Player Ranking, Team Ranking multipliers)
        enhanced_score = self._apply_enhanced_scoring(
            normalized_score, p, enhanced_scorer, team_data_loader, positional_ranking_calculator
        )
        self.logger.debug(f"Steps 2-4 - Enhanced score for {p.name}: {enhanced_score:.2f}")

        # STEP 5: Add DRAFT_ORDER bonus (round-based position priority)
        draft_bonus = self.draft_order_calculator.calculate_bonus(p)
        draft_bonus_score = enhanced_score + draft_bonus
        self.logger.debug(f"Step 5 - After DRAFT_ORDER bonus for {p.name}: {draft_bonus_score:.2f} (+{draft_bonus:.1f})")

        # STEP 6: Subtract Bye Week penalty
        bye_penalty = self.compute_bye_penalty_for_player(p)
        bye_adjusted_score = draft_bonus_score - bye_penalty
        self.logger.debug(f"Step 6 - After bye penalty for {p.name}: {bye_adjusted_score:.2f} (-{bye_penalty:.1f})")

        # STEP 7: Subtract Injury penalty
        injury_penalty = self.compute_injury_penalty(p)
        final_score = bye_adjusted_score - injury_penalty
        self.logger.debug(f"Step 7 - Final score for {p.name}: {final_score:.2f} (-{injury_penalty:.1f})")

        # Summary logging
        self.logger.info(
            f"Add to Roster scoring for {p.name}: "
            f"norm={normalized_score:.1f} → enhanced={enhanced_score:.1f} → "
            f"draft_bonus={draft_bonus_score:.1f} → bye={bye_adjusted_score:.1f} → "
            f"final={final_score:.1f}"
        )

        return final_score

    def _apply_enhanced_scoring(self, base_score, player, enhanced_scorer=None, team_data_loader=None, positional_ranking_calculator=None):
        """
        Apply enhanced scoring multipliers (Steps 2-4).

        This method applies:
        - Step 2: ADP multiplier
        - Step 3: Player Ranking multiplier
        - Step 4: Team ranking multiplier

        Args:
            base_score: Base score (normalized fantasy points)
            player: FantasyPlayer to score
            enhanced_scorer: EnhancedScoringCalculator instance
            team_data_loader: TeamDataLoader instance
            positional_ranking_calculator: PositionalRankingCalculator instance

        Returns:
            float: Score after all enhanced scoring multipliers
        """
        if not enhanced_scorer or not team_data_loader:
            # No enhanced scoring available
            self.logger.debug(f"Enhanced scoring not available for {player.name}, using base score")
            return base_score

        try:
            # Get team rankings
            team_offensive_rank = team_data_loader.get_team_offensive_rank(player.team)
            team_defensive_rank = team_data_loader.get_team_defensive_rank(player.team)

            # Apply enhanced scoring (ADP, Player Rating, Team Rankings)
            enhanced_result = enhanced_scorer.calculate_enhanced_score(
                base_fantasy_points=base_score,
                position=player.position,
                adp=getattr(player, 'average_draft_position', None),
                player_rating=getattr(player, 'player_rating', None),
                team_offensive_rank=team_offensive_rank,
                team_defensive_rank=team_defensive_rank
            )

            enhanced_score = enhanced_result['enhanced_score']

            # Apply positional ranking adjustment if available
            if (positional_ranking_calculator and
                positional_ranking_calculator.is_positional_ranking_available() and
                player.team and player.position):
                try:
                    from shared_config import CURRENT_NFL_WEEK
                    current_week = CURRENT_NFL_WEEK

                    ranking_adjusted_points, ranking_explanation = positional_ranking_calculator.calculate_positional_adjustment(
                        player_team=player.team,
                        position=player.position,
                        base_points=enhanced_score,
                        current_week=current_week
                    )

                    if ranking_adjusted_points != enhanced_score:
                        self.logger.info(f"Positional ranking adjustment for {player.name}: {enhanced_score:.1f} -> {ranking_adjusted_points:.1f} ({ranking_explanation})")
                        enhanced_score = ranking_adjusted_points
                except Exception as e:
                    self.logger.warning(f"Failed to apply positional ranking adjustment for {player.name}: {e}")

            # Log enhancement details if significant adjustment was made
            if enhanced_result['total_multiplier'] != 1.0:
                adjustment_summary = enhanced_scorer.get_adjustment_summary(enhanced_result)
                self.logger.info(f"Enhanced scoring for {player.name}: {base_score:.1f} -> {enhanced_score:.1f} ({adjustment_summary})")

            return enhanced_score

        except Exception as e:
            # Enhanced scoring failed, fall back to basic scoring
            self.logger.warning(f"Enhanced scoring failed for {player.name}: {e}. Using base score.")
            return base_score


    def compute_bye_penalty_for_player(self, player, exclude_self=False):
        """
        Calculate bye week penalty for a specific player.

        Args:
            player: FantasyPlayer to evaluate
            exclude_self: Whether to exclude this player from roster considerations

        Returns:
            float: Bye week penalty
        """
        try:
            from shared_config import CURRENT_NFL_WEEK
            current_week = CURRENT_NFL_WEEK
        except ImportError:
            current_week = 1

        if not hasattr(player, 'bye_week') or player.bye_week is None:
            return 0

        player_bye_week = int(player.bye_week)

        # No penalty if the bye week has already passed
        if player_bye_week < current_week:
            return 0

        position = player.position

        # Calculate how many players at this position would be on bye the same week
        roster_players = self.team.roster
        if exclude_self:
            roster_players = [p for p in roster_players if p.id != player.id]

        same_position_bye_count = 0
        for roster_player in roster_players:
            if (roster_player.position == position and
                hasattr(roster_player, 'bye_week') and
                roster_player.bye_week == player_bye_week):
                same_position_bye_count += 1

        # Apply penalty based on position and how many would be on bye
        if position in Constants.FLEX_ELIGIBLE_POSITIONS:
            # For FLEX eligible positions, consider cross-position coverage
            all_flex_bye_count = 0
            for roster_player in roster_players:
                if (roster_player.position in Constants.FLEX_ELIGIBLE_POSITIONS and
                    hasattr(roster_player, 'bye_week') and
                    roster_player.bye_week == player_bye_week):
                    all_flex_bye_count += 1

            # Less penalty if we have other FLEX-eligible players not on bye
            if all_flex_bye_count >= 2:
                return Constants.BASE_BYE_PENALTY * 1.5  # High penalty for multiple FLEX on bye
            elif same_position_bye_count >= 1:
                return Constants.BASE_BYE_PENALTY  # Standard penalty
            else:
                return Constants.BASE_BYE_PENALTY * 0.5  # Reduced penalty if covered by other FLEX
        else:
            # For non-FLEX positions, standard penalty
            if same_position_bye_count >= 1:
                return Constants.BASE_BYE_PENALTY * 1.5  # High penalty for position shortage
            else:
                return Constants.BASE_BYE_PENALTY  # Standard penalty

    def compute_injury_penalty(self, p, trade_mode=False):
        """
        Calculate injury penalty based on player's injury status.

        Args:
            p: FantasyPlayer to evaluate
            trade_mode: Whether this is for trade evaluation

        Returns:
            float: Injury penalty
        """
        if not hasattr(p, 'injury_status') or p.injury_status is None:
            return 0

        # Import current config values to get real-time settings
        try:
            from .. import draft_helper_config as config
        except ImportError:
            import draft_helper_config as config

        # Check if we should skip injury penalties for roster players in trade mode
        # Either through config setting OR explicit trade_mode parameter
        in_trade_mode = config.TRADE_HELPER_MODE or trade_mode
        if (in_trade_mode and
            not config.APPLY_INJURY_PENALTY_TO_ROSTER and
            p.drafted == 2):
            return 0  # Skip injury penalty for roster players in trade mode

        # Use the player's risk level method to determine penalty
        risk_level = p.get_risk_level()
        return Constants.INJURY_PENALTIES.get(risk_level, 0)

    def score_player_for_trade(self, player, positional_ranking_calculator=None, enhanced_scorer=None, team_data_loader=None):
        """
        Calculate score for Trade/Waiver Mode (6-step calculation).

        New Scoring System (same as Add to Roster but WITHOUT DRAFT_ORDER bonus):
        1. Get normalized seasonal fantasy points (0-N scale)
        2. Apply ADP multiplier
        3. Apply Player Ranking multiplier
        4. Apply Team ranking multiplier
        5. Subtract Bye Week penalty
        6. Subtract Injury penalty

        Note: No DRAFT_ORDER bonus - that's only for draft recommendations

        Args:
            player: FantasyPlayer to evaluate
            positional_ranking_calculator: PositionalRankingCalculator instance
            enhanced_scorer: EnhancedScoringCalculator instance
            team_data_loader: TeamDataLoader instance

        Returns:
            float: Trade/waiver score for the player
        """
        # STEP 1: Normalize seasonal fantasy points to 0-N scale
        normalized_score = self.normalization_calculator.normalize_player(player, self.players)
        self.logger.debug(f"Step 1 - Normalized score for {player.name}: {normalized_score:.2f}")

        # STEPS 2-4: Apply enhanced scoring (ADP, Player Ranking, Team Ranking multipliers)
        enhanced_score = self._apply_enhanced_scoring(
            normalized_score, player, enhanced_scorer, team_data_loader, positional_ranking_calculator
        )
        self.logger.debug(f"Steps 2-4 - Enhanced score for {player.name}: {enhanced_score:.2f}")

        # NOTE: No DRAFT_ORDER bonus for trade/waiver mode (Step 5 from Add to Roster is skipped)

        # STEP 5: Subtract Bye Week penalty (exclude self if roster player)
        exclude_self = (player.drafted == 2)
        bye_penalty = self.compute_bye_penalty_for_player(player, exclude_self=exclude_self)
        bye_adjusted_score = enhanced_score - bye_penalty
        self.logger.debug(f"Step 5 - After bye penalty for {player.name}: {bye_adjusted_score:.2f} (-{bye_penalty:.1f})")

        # STEP 6: Subtract Injury penalty
        injury_penalty = self.compute_injury_penalty(player, trade_mode=True)
        final_score = bye_adjusted_score - injury_penalty
        self.logger.debug(f"Step 6 - Final score for {player.name}: {final_score:.2f} (-{injury_penalty:.1f})")

        # Summary logging
        self.logger.info(
            f"Trade/Waiver scoring for {player.name}: "
            f"norm={normalized_score:.1f} → enhanced={enhanced_score:.1f} → "
            f"bye={bye_adjusted_score:.1f} → final={final_score:.1f}"
        )

        return final_score