#!/usr/bin/env python3
"""
Scoring Engine Module for Draft Helper

This module handles all player scoring and penalty calculation functionality,
extracted from the main draft_helper.py for better modularity.

Author: Kai Mizuno
Last Updated: September 2025
"""

import logging
from typing import Dict, List, Optional, Any

try:
    from .. import draft_helper_constants as Constants
except ImportError:
    import draft_helper_constants as Constants


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

    def score_player(self, p, enhanced_scorer=None, team_data_loader=None, positional_ranking_calculator=None):
        """
        Calculate the total score for a player based on positional need, projections, penalties, and bonuses.

        Args:
            p: FantasyPlayer to score
            enhanced_scorer: EnhancedScoringCalculator instance
            team_data_loader: TeamDataLoader instance
            positional_ranking_calculator: PositionalRankingCalculator instance

        Returns:
            float: Total score for the player
        """
        # Calculate positional need score
        pos_score = self.compute_positional_need_score(p)
        self.logger.debug(f"Positional need score for {p.name}: {pos_score}")

        # Calculate projection score
        projection_score = self.compute_projection_score(p, enhanced_scorer, team_data_loader, positional_ranking_calculator)
        self.logger.debug(f"Projection score for {p.name}: {projection_score}")

        # Calculate bye week penalty
        bye_penalty = self.compute_bye_penalty_for_player(p)
        self.logger.debug(f"Bye week penalty for {p.name}: {bye_penalty}")

        # Calculate injury penalty
        injury_penalty = self.compute_injury_penalty(p)
        self.logger.debug(f"Injury penalty for {p.name}: {injury_penalty}")

        # Calculate matchup adjustment if available
        matchup_adjustment = 0
        if hasattr(p, 'matchup_adjustment') and p.matchup_adjustment is not None:
            matchup_adjustment = p.matchup_adjustment
            self.logger.debug(f"Matchup adjustment for {p.name}: {matchup_adjustment}")

        # Calculate final score (higher is better)
        total_score = pos_score + projection_score - bye_penalty - injury_penalty + matchup_adjustment

        self.logger.debug(f"Total score for {p.name}: {total_score:.2f} "
                         f"(pos: {pos_score}, proj: {projection_score:.2f}, "
                         f"bye: -{bye_penalty:.2f}, injury: -{injury_penalty}, matchup: +{matchup_adjustment})")

        return total_score

    def compute_positional_need_score(self, p):
        """
        Calculate positional need score based on how many players of this position we have.

        Args:
            p: FantasyPlayer to evaluate

        Returns:
            float: Positional need score
        """
        pos = p.position
        current_count = self.team.pos_counts.get(pos, 0)
        max_limit = Constants.MAX_POSITIONS.get(pos, 0)

        # Base positional need (higher = more needed)
        if current_count < max_limit:
            # Still need players at this position
            need_score = (max_limit - current_count) * Constants.POS_NEEDED_SCORE
        else:
            # Already have enough players at this position
            need_score = 0

        # Apply FLEX considerations for RB/WR positions
        if pos in Constants.FLEX_ELIGIBLE_POSITIONS:
            flex_count = self.team.pos_counts.get("FLEX", 0)
            flex_limit = Constants.MAX_POSITIONS.get("FLEX", 0)

            if flex_count < flex_limit:
                # Can still use FLEX position
                flex_need = (flex_limit - flex_count) * Constants.POS_NEEDED_SCORE * 0.5
                need_score += flex_need

        return need_score

    def compute_projection_score(self, p, enhanced_scorer=None, team_data_loader=None, positional_ranking_calculator=None):
        """
        Calculate projection score based on weekly fantasy points projections.

        Args:
            p: FantasyPlayer to evaluate
            enhanced_scorer: EnhancedScoringCalculator instance
            team_data_loader: TeamDataLoader instance
            positional_ranking_calculator: PositionalRankingCalculator instance

        Returns:
            float: Projection score
        """
        # Use the remaining season projections if available, otherwise use full season
        if hasattr(p, 'remaining_season_projection') and p.remaining_season_projection is not None and p.remaining_season_projection > 0:
            base_score = p.remaining_season_projection
        elif hasattr(p, 'weighted_projection') and p.weighted_projection is not None and p.weighted_projection > 0:
            base_score = p.weighted_projection
        else:
            base_score = p.fantasy_points

        self.logger.debug(f"Base fantasy points for {p.name}: {base_score}")

        # Apply enhanced scoring if available
        if enhanced_scorer and team_data_loader:
            try:
                # Get team rankings from team data loader
                team_offensive_rank = team_data_loader.get_team_offensive_rank(p.team)
                team_defensive_rank = team_data_loader.get_team_defensive_rank(p.team)

                enhanced_result = enhanced_scorer.calculate_enhanced_score(
                    base_fantasy_points=base_score,
                    position=p.position,
                    adp=getattr(p, 'average_draft_position', None),
                    player_rating=getattr(p, 'player_rating', None),
                    team_offensive_rank=team_offensive_rank,
                    team_defensive_rank=team_defensive_rank
                )

                projection_score = enhanced_result['enhanced_score']

                # Apply positional ranking adjustment if available
                if (positional_ranking_calculator and
                    positional_ranking_calculator.is_positional_ranking_available() and
                    p.team and p.position):
                    try:
                        from shared_config import CURRENT_NFL_WEEK
                        current_week = CURRENT_NFL_WEEK

                        ranking_adjusted_points, ranking_explanation = positional_ranking_calculator.calculate_positional_adjustment(
                            player_team=p.team,
                            position=p.position,
                            base_points=projection_score,
                            current_week=current_week
                        )

                        if ranking_adjusted_points != projection_score:
                            self.logger.info(f"Positional ranking adjustment for {p.name}: {projection_score:.1f} -> {ranking_adjusted_points:.1f} ({ranking_explanation})")
                            projection_score = ranking_adjusted_points
                    except Exception as e:
                        self.logger.warning(f"Failed to apply positional ranking adjustment for {p.name}: {e}")

                # Log enhancement details if significant adjustment was made
                if enhanced_result['total_multiplier'] != 1.0:
                    adjustment_summary = enhanced_scorer.get_adjustment_summary(enhanced_result)
                    self.logger.info(f"Enhanced scoring for {p.name}: {base_score:.1f} -> {projection_score:.1f} ({adjustment_summary})")

            except Exception as e:
                # Enhanced scoring failed, fall back to basic scoring
                self.logger.warning(f"Enhanced scoring failed for {p.name}: {e}. Using fallback scoring.")
                projection_score = base_score
        else:
            projection_score = base_score

        return projection_score

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
        Modified scoring function for trade evaluation.
        Sets positional need weight to 0 and focuses on projections, injuries, bye weeks, and matchups.
        Uses enhanced scoring for more accurate player valuations.

        Args:
            player: FantasyPlayer to evaluate
            positional_ranking_calculator: PositionalRankingCalculator instance
            enhanced_scorer: EnhancedScoringCalculator instance for score multipliers
            team_data_loader: TeamDataLoader instance for team rankings

        Returns:
            float: Trade score for the player
        """
        # Use 0 weight for positional need as specified
        pos_score = 0

        # Calculate projection score with enhanced scoring (same as draft mode)
        projection_score = self.compute_projection_score(
            player,
            enhanced_scorer=enhanced_scorer,
            team_data_loader=team_data_loader,
            positional_ranking_calculator=positional_ranking_calculator
        )
        self.logger.debug(f"Projection score for {player.name}: {projection_score}")

        # Positional ranking adjustment is already applied inside compute_projection_score

        # Calculate bye week penalty - exclude self if this is a roster player
        exclude_self = (player.drafted == 2)
        bye_penalty = self.compute_bye_penalty_for_player(player, exclude_self=exclude_self)
        self.logger.debug(f"Bye week penalty for {player.name}: {bye_penalty}")

        # Calculate injury penalty (in trade mode context)
        injury_penalty = self.compute_injury_penalty(player, trade_mode=True)
        self.logger.debug(f"Injury penalty for {player.name}: {injury_penalty}")

        # Calculate matchup adjustment if available
        matchup_adjustment = 0
        if hasattr(player, 'matchup_adjustment') and player.matchup_adjustment is not None:
            matchup_adjustment = player.matchup_adjustment
            self.logger.debug(f"Matchup adjustment for {player.name}: {matchup_adjustment}")

        # Calculate final score (higher is better)
        total_score = pos_score + projection_score - bye_penalty - injury_penalty + matchup_adjustment

        self.logger.debug(f"Total score for {player.name}: {total_score:.2f} "
                         f"(pos: {pos_score}, proj: {projection_score:.2f}, "
                         f"bye: -{bye_penalty:.2f}, injury: -{injury_penalty}, matchup: +{matchup_adjustment})")

        return total_score