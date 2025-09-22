#!/usr/bin/env python3
"""
Fantasy Football Lineup Optimizer

This module handles the core logic for recommending optimal starting lineups
based on current week projections and league requirements.

Author: Generated for NFL Fantasy Data Collection
Last Updated: September 2025
"""

import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import pandas as pd

from starter_helper_config import (
    STARTING_LINEUP_REQUIREMENTS, FLEX_ELIGIBLE_POSITIONS,
    INJURY_PENALTIES, BYE_WEEK_PENALTY, CURRENT_NFL_WEEK,
    QB, RB, WR, TE, K, DST, FLEX,
    ENABLE_MATCHUP_ANALYSIS, MATCHUP_WEIGHT_FACTOR
)


@dataclass
class StartingRecommendation:
    """Represents a starting lineup recommendation"""
    player_id: str
    name: str
    position: str
    team: str
    projected_points: float
    injury_status: str
    bye_week: int
    adjusted_score: float
    reason: str = ""
    # Matchup analysis fields (optional)
    matchup_rating: Optional[float] = None
    matchup_indicator: Optional[str] = None
    opponent_team: Optional[str] = None
    is_home_game: Optional[bool] = None


@dataclass
class OptimalLineup:
    """Represents a complete optimal starting lineup"""
    qb: Optional[StartingRecommendation] = None
    rb1: Optional[StartingRecommendation] = None
    rb2: Optional[StartingRecommendation] = None
    wr1: Optional[StartingRecommendation] = None
    wr2: Optional[StartingRecommendation] = None
    te: Optional[StartingRecommendation] = None
    flex: Optional[StartingRecommendation] = None
    k: Optional[StartingRecommendation] = None
    dst: Optional[StartingRecommendation] = None

    @property
    def total_projected_points(self) -> float:
        """Calculate total projected points for the lineup"""
        total = 0.0
        for recommendation in self.get_all_starters():
            if recommendation:
                total += recommendation.projected_points
        return total

    def get_all_starters(self) -> List[Optional[StartingRecommendation]]:
        """Get all starting recommendations in order"""
        return [self.qb, self.rb1, self.rb2, self.wr1, self.wr2,
                self.te, self.flex, self.k, self.dst]


class LineupOptimizer:
    """Handles optimal starting lineup recommendations"""

    def __init__(self, matchup_analyzer=None):
        self.logger = logging.getLogger(__name__)
        self.matchup_analyzer = matchup_analyzer

        # Import matchup analysis components if enabled
        if ENABLE_MATCHUP_ANALYSIS and matchup_analyzer is None:
            try:
                from matchup_analyzer import MatchupAnalyzer
                from matchup_models import FantasyPosition
                self.matchup_analyzer = MatchupAnalyzer()
                self.logger.info("Matchup analysis enabled")
            except ImportError as e:
                self.logger.warning(f"Matchup analysis disabled due to import error: {e}")
                self.matchup_analyzer = None

    def calculate_adjusted_score(self,
                                projected_points: float,
                                injury_status: str,
                                bye_week: int,
                                matchup_rating: Optional[float] = None) -> Tuple[float, str]:
        """
        Calculate adjusted score for a player based on projections, penalties, and matchup analysis

        Args:
            projected_points: Current week projected fantasy points
            injury_status: Player injury status
            bye_week: Player's bye week number
            matchup_rating: Optional matchup rating (1-100 scale)

        Returns:
            Tuple of (adjusted_score, reason_string)
        """
        adjusted_score = projected_points
        reasons = []

        # Apply injury penalty
        if injury_status in INJURY_PENALTIES:
            penalty = INJURY_PENALTIES[injury_status]
            adjusted_score -= penalty
            if penalty > 0:
                reasons.append(f"-{penalty} injury penalty ({injury_status})")

        # Apply bye week penalty
        if bye_week == CURRENT_NFL_WEEK:
            adjusted_score -= BYE_WEEK_PENALTY
            reasons.append(f"-{BYE_WEEK_PENALTY} bye week penalty")

        # Apply matchup analysis adjustment if enabled and available
        if ENABLE_MATCHUP_ANALYSIS and matchup_rating is not None and self.matchup_analyzer:
            matchup_adjustment = self._calculate_matchup_adjustment(projected_points, matchup_rating)
            adjusted_score += matchup_adjustment
            if abs(matchup_adjustment) >= 0.1:
                sign = "+" if matchup_adjustment > 0 else ""
                reasons.append(f"{sign}{matchup_adjustment:.1f} matchup adjustment")

        reason = "; ".join(reasons) if reasons else "No penalties"
        return max(0.0, adjusted_score), reason

    def _calculate_matchup_adjustment(self, projected_points: float, matchup_rating: float) -> float:
        """
        Calculate matchup adjustment to projected points based on rating.

        Args:
            projected_points: Base projected fantasy points
            matchup_rating: Matchup rating (1-100 scale)

        Returns:
            Points adjustment (positive for good matchups, negative for bad)
        """
        # Convert 1-100 rating to adjustment factor
        # Rating 50 = no adjustment, 100 = max positive, 1 = max negative
        rating_factor = (matchup_rating - 50.0) / 50.0  # Range: -0.98 to +1.0

        # Calculate maximum possible adjustment (percentage of projected points)
        max_adjustment = projected_points * MATCHUP_WEIGHT_FACTOR

        # Apply rating factor to get final adjustment
        adjustment = max_adjustment * rating_factor

        return adjustment

    def create_starting_recommendation(self,
                                     player_data: Dict,
                                     projected_points: float,
                                     matchup_rating_obj=None) -> StartingRecommendation:
        """
        Create a StartingRecommendation from player data

        Args:
            player_data: Player information from CSV
            projected_points: Current week projected points
            matchup_rating_obj: Optional MatchupRating object for this player

        Returns:
            StartingRecommendation object
        """
        injury_status = player_data.get('injury_status', 'ACTIVE')
        bye_week = int(player_data.get('bye_week', 0))

        # Extract matchup information if available
        matchup_rating = None
        matchup_indicator = None
        opponent_team = None
        is_home_game = None

        if matchup_rating_obj and ENABLE_MATCHUP_ANALYSIS:
            matchup_rating = matchup_rating_obj.overall_rating
            matchup_indicator = self.matchup_analyzer.get_matchup_display_indicator(matchup_rating)
            opponent_team = matchup_rating_obj.player_context.opponent_team_abbreviation
            is_home_game = matchup_rating_obj.player_context.is_home_game

        adjusted_score, reason = self.calculate_adjusted_score(
            projected_points, injury_status, bye_week, matchup_rating
        )

        return StartingRecommendation(
            player_id=str(player_data['id']),
            name=player_data['name'],
            position=player_data['position'],
            team=player_data['team'],
            projected_points=projected_points,
            injury_status=injury_status,
            bye_week=bye_week,
            adjusted_score=adjusted_score,
            reason=reason,
            matchup_rating=matchup_rating,
            matchup_indicator=matchup_indicator,
            opponent_team=opponent_team,
            is_home_game=is_home_game
        )

    def get_position_candidates(self,
                              roster_players: pd.DataFrame,
                              projections: Dict[str, float],
                              position: str,
                              matchup_analysis=None) -> List[StartingRecommendation]:
        """
        Get and rank candidates for a specific position

        Args:
            roster_players: DataFrame of roster players (drafted=2)
            projections: Dictionary mapping player_id to current week projections
            position: Position to get candidates for
            matchup_analysis: Optional WeeklyMatchupAnalysis object

        Returns:
            List of StartingRecommendation objects sorted by adjusted_score (descending)
        """
        if position == FLEX:
            # FLEX can be RB or WR
            candidates = roster_players[
                roster_players['position'].isin(FLEX_ELIGIBLE_POSITIONS)
            ]
        else:
            # Regular position
            candidates = roster_players[roster_players['position'] == position]

        recommendations = []
        for _, player in candidates.iterrows():
            player_id = str(player['id'])
            projected_points = projections.get(player_id, 0.0)

            # Get matchup rating for this player if available
            matchup_rating_obj = None
            if matchup_analysis and ENABLE_MATCHUP_ANALYSIS:
                matchup_rating_obj = matchup_analysis.get_player_rating(player_id)

            recommendation = self.create_starting_recommendation(
                player.to_dict(), projected_points, matchup_rating_obj
            )
            recommendations.append(recommendation)

        # Sort by adjusted score (highest first)
        recommendations.sort(key=lambda x: x.adjusted_score, reverse=True)

        self.logger.debug(f"Found {len(recommendations)} candidates for {position}")
        return recommendations

    def optimize_lineup(self,
                       roster_players: pd.DataFrame,
                       projections: Dict[str, float],
                       matchup_analysis=None) -> OptimalLineup:
        """
        Optimize starting lineup based on current week projections and optional matchup analysis

        Args:
            roster_players: DataFrame of roster players (drafted=2)
            projections: Dictionary mapping player_id to current week projections
            matchup_analysis: Optional WeeklyMatchupAnalysis object for enhanced scoring

        Returns:
            OptimalLineup object with best recommendations for each position
        """
        if ENABLE_MATCHUP_ANALYSIS and matchup_analysis:
            self.logger.info("Optimizing starting lineup with matchup analysis")
        else:
            self.logger.info("Optimizing starting lineup for current week")

        lineup = OptimalLineup()
        used_player_ids = set()

        # Fill required positions first (non-FLEX)
        required_positions = [
            (QB, 1, 'qb'),
            (RB, 2, ['rb1', 'rb2']),
            (WR, 2, ['wr1', 'wr2']),
            (TE, 1, 'te'),
            (K, 1, 'k'),
            (DST, 1, 'dst')
        ]

        for position, count, attr_names in required_positions:
            candidates = self.get_position_candidates(roster_players, projections, position, matchup_analysis)

            # Filter out already used players
            available_candidates = [
                c for c in candidates if c.player_id not in used_player_ids
            ]

            if isinstance(attr_names, str):
                # Single position (QB, TE, K, DST)
                if available_candidates:
                    best_candidate = available_candidates[0]
                    setattr(lineup, attr_names, best_candidate)
                    used_player_ids.add(best_candidate.player_id)
                    self.logger.debug(f"Selected {best_candidate.name} for {position}")
                else:
                    self.logger.warning(f"No available candidates for {position}")

            else:
                # Multiple positions (RB1/RB2, WR1/WR2)
                selected_count = 0
                for i, attr_name in enumerate(attr_names):
                    if selected_count < len(available_candidates):
                        candidate = available_candidates[selected_count]
                        setattr(lineup, attr_name, candidate)
                        used_player_ids.add(candidate.player_id)
                        selected_count += 1
                        self.logger.debug(f"Selected {candidate.name} for {attr_name}")

        # Fill FLEX position (best available RB or WR)
        flex_candidates = self.get_position_candidates(roster_players, projections, FLEX, matchup_analysis)
        available_flex = [
            c for c in flex_candidates if c.player_id not in used_player_ids
        ]

        if available_flex:
            best_flex = available_flex[0]
            lineup.flex = best_flex
            used_player_ids.add(best_flex.player_id)
            self.logger.debug(f"Selected {best_flex.name} ({best_flex.position}) for FLEX")
        else:
            self.logger.warning("No available candidates for FLEX position")

        self.logger.info(f"Lineup optimization complete. Total projected points: {lineup.total_projected_points:.1f}")
        return lineup

    def get_bench_recommendations(self,
                                roster_players: pd.DataFrame,
                                projections: Dict[str, float],
                                used_player_ids: set,
                                count: int = 5,
                                matchup_analysis=None) -> List[StartingRecommendation]:
        """
        Get top bench players that could be considered for starting

        Args:
            roster_players: DataFrame of roster players
            projections: Dictionary mapping player_id to projections
            used_player_ids: Set of player IDs already in starting lineup
            count: Number of bench recommendations to return
            matchup_analysis: Optional WeeklyMatchupAnalysis object

        Returns:
            List of top bench recommendations
        """
        bench_players = []

        for _, player in roster_players.iterrows():
            player_id = str(player['id'])
            if player_id not in used_player_ids:
                projected_points = projections.get(player_id, 0.0)

                # Get matchup rating for bench player if available
                matchup_rating_obj = None
                if matchup_analysis and ENABLE_MATCHUP_ANALYSIS:
                    matchup_rating_obj = matchup_analysis.get_player_rating(player_id)

                recommendation = self.create_starting_recommendation(
                    player.to_dict(), projected_points, matchup_rating_obj
                )
                bench_players.append(recommendation)

        # Sort by adjusted score and return top recommendations
        bench_players.sort(key=lambda x: x.adjusted_score, reverse=True)
        return bench_players[:count]

    async def close(self):
        """Close any open resources"""
        if self.matchup_analyzer:
            await self.matchup_analyzer.close()