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

from config import (
    STARTING_LINEUP_REQUIREMENTS, FLEX_ELIGIBLE_POSITIONS,
    INJURY_PENALTIES, BYE_WEEK_PENALTY, CURRENT_NFL_WEEK,
    QB, RB, WR, TE, K, DST, FLEX
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

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def calculate_adjusted_score(self,
                                projected_points: float,
                                injury_status: str,
                                bye_week: int) -> Tuple[float, str]:
        """
        Calculate adjusted score for a player based on projections and penalties

        Args:
            projected_points: Current week projected fantasy points
            injury_status: Player injury status
            bye_week: Player's bye week number

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

        reason = "; ".join(reasons) if reasons else "No penalties"
        return max(0.0, adjusted_score), reason

    def create_starting_recommendation(self,
                                     player_data: Dict,
                                     projected_points: float) -> StartingRecommendation:
        """
        Create a StartingRecommendation from player data

        Args:
            player_data: Player information from CSV
            projected_points: Current week projected points

        Returns:
            StartingRecommendation object
        """
        injury_status = player_data.get('injury_status', 'ACTIVE')
        bye_week = int(player_data.get('bye_week', 0))

        adjusted_score, reason = self.calculate_adjusted_score(
            projected_points, injury_status, bye_week
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
            reason=reason
        )

    def get_position_candidates(self,
                              roster_players: pd.DataFrame,
                              projections: Dict[str, float],
                              position: str) -> List[StartingRecommendation]:
        """
        Get and rank candidates for a specific position

        Args:
            roster_players: DataFrame of roster players (drafted=2)
            projections: Dictionary mapping player_id to current week projections
            position: Position to get candidates for

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

            recommendation = self.create_starting_recommendation(
                player.to_dict(), projected_points
            )
            recommendations.append(recommendation)

        # Sort by adjusted score (highest first)
        recommendations.sort(key=lambda x: x.adjusted_score, reverse=True)

        self.logger.debug(f"Found {len(recommendations)} candidates for {position}")
        return recommendations

    def optimize_lineup(self,
                       roster_players: pd.DataFrame,
                       projections: Dict[str, float]) -> OptimalLineup:
        """
        Optimize starting lineup based on current week projections

        Args:
            roster_players: DataFrame of roster players (drafted=2)
            projections: Dictionary mapping player_id to current week projections

        Returns:
            OptimalLineup object with best recommendations for each position
        """
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
            candidates = self.get_position_candidates(roster_players, projections, position)

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
        flex_candidates = self.get_position_candidates(roster_players, projections, FLEX)
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
                                count: int = 5) -> List[StartingRecommendation]:
        """
        Get top bench players that could be considered for starting

        Args:
            roster_players: DataFrame of roster players
            projections: Dictionary mapping player_id to projections
            used_player_ids: Set of player IDs already in starting lineup
            count: Number of bench recommendations to return

        Returns:
            List of top bench recommendations
        """
        bench_players = []

        for _, player in roster_players.iterrows():
            player_id = str(player['id'])
            if player_id not in used_player_ids:
                projected_points = projections.get(player_id, 0.0)
                recommendation = self.create_starting_recommendation(
                    player.to_dict(), projected_points
                )
                bench_players.append(recommendation)

        # Sort by adjusted score and return top recommendations
        bench_players.sort(key=lambda x: x.adjusted_score, reverse=True)
        return bench_players[:count]