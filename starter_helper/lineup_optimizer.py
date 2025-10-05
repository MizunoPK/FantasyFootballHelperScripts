#!/usr/bin/env python3
"""
Fantasy Football Lineup Optimizer

This module handles the core logic for recommending optimal starting lineups
based on current week projections and league requirements.

Author: Kai Mizuno
Last Updated: September 2025
"""

import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import pandas as pd

from shared_files.configs.starter_helper_config import (
    STARTING_LINEUP_REQUIREMENTS, FLEX_ELIGIBLE_POSITIONS,
    INJURY_PENALTIES, BYE_WEEK_PENALTY, CURRENT_NFL_WEEK,
    STARTER_HELPER_ACTIVE_STATUSES,
    QB, RB, WR, TE, K, DST, FLEX
)
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from matchup_calculator import MatchupCalculator
from shared_files.consistency_calculator import ConsistencyCalculator


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
    matchup_indicator: str = ""  # For matchup analysis display (^, o, v, or empty)


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

        # Initialize matchup calculator
        try:
            self.matchup_calculator = MatchupCalculator()
            if self.matchup_calculator.is_matchup_available():
                self.logger.info("Matchup multiplier calculations enabled")
            else:
                self.logger.info("Matchup multiplier calculations disabled (teams.csv not available)")
        except Exception as e:
            self.logger.warning(f"Failed to initialize matchup calculator: {e}")
            self.matchup_calculator = None

        # Initialize consistency calculator
        self.consistency_calculator = ConsistencyCalculator(logger=self.logger)
        self.logger.info("Consistency calculator initialized")

    def calculate_adjusted_score(self,
                                projected_points: float,
                                injury_status: str,
                                bye_week: int,
                                player_team: Optional[str] = None,
                                player_position: Optional[str] = None,
                                player_data: Optional[Dict] = None) -> Tuple[float, str]:
        """
        Calculate adjusted score for a player based on projections and binary injury system

        Scoring System (4 steps):
        1. Start with projected points for current week
        2. Apply matchup multiplier (if positional ranking available)
        3. Apply consistency multiplier (CV-based volatility scoring)
        4. Apply binary injury penalty (zero out non-ACTIVE/QUESTIONABLE players)

        Args:
            projected_points: Current week projected fantasy points
            injury_status: Player injury status
            bye_week: Player's bye week number (not used in current scoring)
            player_team: Player's team abbreviation (e.g., 'PHI', 'KC')
            player_position: Player position (e.g., 'QB', 'RB', 'WR')
            player_data: Optional dict with full player data for consistency calculation

        Returns:
            Tuple of (adjusted_score, reason_string)
        """
        adjusted_score = projected_points
        reasons = []

        # Step 2: Apply matchup multiplier if available
        if (self.matchup_calculator and
            self.matchup_calculator.is_matchup_available() and
            player_team and player_position):

            matchup_adjusted_points, matchup_explanation = self.matchup_calculator.calculate_matchup_adjustment(
                player_team=player_team,
                position=player_position,
                base_points=adjusted_score
            )

            # Apply the matchup adjustment
            adjusted_score = matchup_adjusted_points

            # Add explanation if provided
            if matchup_explanation:
                reasons.append(matchup_explanation)

        # Step 3: Apply consistency multiplier if player_data available
        if player_data:
            consistency_score, consistency_category = self._apply_consistency_scoring(adjusted_score, player_data)
            adjusted_score = consistency_score
            reasons.append(f"[{consistency_category} volatility]")
            self.logger.debug(f"Consistency applied: {consistency_category} volatility")

        # Step 4: Apply binary injury penalty (zero out non-active players)
        # Players must be ACTIVE or QUESTIONABLE to play; all others get zero score
        if injury_status.upper() not in STARTER_HELPER_ACTIVE_STATUSES:
            adjusted_score = 0.0
            reasons.append(f"Inactive ({injury_status})")
            self.logger.debug(f"Player zeroed out due to injury status: {injury_status}")

        reason = "; ".join(reasons) if reasons else "No adjustments"
        return max(0.0, adjusted_score), reason

    def _apply_consistency_scoring(self, base_score: float, player_data: Dict) -> Tuple[float, str]:
        """
        Apply consistency/volatility multiplier based on week-to-week performance variance.

        Args:
            base_score: Score before consistency adjustment
            player_data: Dict containing player data with weekly projections

        Returns:
            tuple: (adjusted_score, volatility_category)
        """
        try:
            # Import config to check if enabled
            from shared_files.configs.draft_helper_config import (
                ENABLE_CONSISTENCY_SCORING,
                CONSISTENCY_MULTIPLIERS
            )

            if not ENABLE_CONSISTENCY_SCORING:
                return base_score, 'MEDIUM'

            # Create a simple object with name and weekly projection attributes
            # ConsistencyCalculator only needs weekly_X_points attributes
            class PlayerProxy:
                def __init__(self, data):
                    self.name = data.get('name', 'Unknown')
                    # Copy all weekly projection attributes
                    for week in range(1, 18):
                        week_key = f'week_{week}_points'
                        if week_key in data:
                            setattr(self, week_key, data[week_key])
                        else:
                            setattr(self, week_key, None)

            player = PlayerProxy(player_data)

            # Calculate consistency metrics
            consistency_result = self.consistency_calculator.calculate_consistency_score(player)
            volatility_category = consistency_result['volatility_category']

            # Get multiplier from config
            multiplier = CONSISTENCY_MULTIPLIERS.get(volatility_category, 1.0)

            # Apply multiplier
            adjusted_score = base_score * multiplier

            self.logger.debug(
                f"Consistency for {player_data.get('name', 'Unknown')}: "
                f"CV={consistency_result['coefficient_of_variation']:.3f}, "
                f"category={volatility_category}, multiplier={multiplier:.2f}"
            )

            return adjusted_score, volatility_category

        except Exception as e:
            self.logger.warning(f"Consistency calculation failed: {e}. Using base score.")
            return base_score, 'MEDIUM'

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
            projected_points, injury_status, bye_week,
            player_team=player_data['team'],
            player_position=player_data['position'],
            player_data=player_data
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

    async def close(self):
        """Close any open resources"""
        pass