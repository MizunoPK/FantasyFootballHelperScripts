#!/usr/bin/env python3
"""
Enhanced Fantasy Football Scoring Algorithm

This module provides scoring adjustments based on market wisdom and contextual factors
to improve accuracy over pure projection-based scoring. Integrates Average Draft Position (ADP),
ESPN player ratings, and team quality context to better align with real fantasy manager evaluations.

Author: Kai Mizuno
Last Updated: September 2025
"""

from typing import Optional, Dict, Any
from shared_files.logging_utils import setup_module_logging

# Configuration constants - can be overridden by config files
DEFAULT_SCORING_CONFIG = {
    # Enable/disable individual adjustment factors
    "enable_adp_adjustment": True,
    "enable_player_rating_adjustment": True,
    "enable_team_quality_adjustment": True,

    # ADP-based market wisdom adjustments
    "adp_excellent_threshold": 50,      # Better than 50th overall pick
    "adp_good_threshold": 100,          # Better than 100th overall pick
    "adp_poor_threshold": 200,          # Worse than 200th overall pick
    "adp_excellent_multiplier": 1.15,   # 15% boost for excellent ADP
    "adp_good_multiplier": 1.08,        # 8% boost for good ADP
    "adp_poor_multiplier": 0.92,        # 8% penalty for poor ADP

    # ESPN player rating adjustments
    "player_rating_excellent_threshold": 80,    # ESPN rating > 80
    "player_rating_good_threshold": 60,         # ESPN rating > 60
    "player_rating_poor_threshold": 30,         # ESPN rating < 30
    "player_rating_excellent_multiplier": 1.20, # 20% boost for excellent rating
    "player_rating_good_multiplier": 1.10,      # 10% boost for good rating
    "player_rating_poor_multiplier": 0.90,      # 10% penalty for poor rating
    "player_rating_max_boost": 1.25,            # Cap total rating boost at 25%

    # Team quality context adjustments
    "team_excellent_threshold": 5,      # Top 5 team
    "team_good_threshold": 12,          # Top 12 team
    "team_poor_threshold": 25,          # Bottom 8 teams (32-25)
    "team_excellent_multiplier": 1.12,  # 12% boost for excellent team
    "team_good_multiplier": 1.06,       # 6% boost for good team
    "team_poor_multiplier": 0.94,       # 6% penalty for poor team

    # Position-specific settings
    "skill_positions": ["QB", "RB", "WR", "TE", "K"],  # Use offensive rankings
    "defense_positions": ["DEF", "DST", "D/ST"]        # Use defensive rankings
}


class EnhancedScoringCalculator:
    """
    Calculator for enhanced fantasy football scoring with market wisdom integration.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the enhanced scoring calculator.

        Args:
            config: Optional configuration dictionary to override defaults
        """
        self.config = DEFAULT_SCORING_CONFIG.copy()
        if config:
            self.config.update(config)

        self.logger = setup_module_logging(__name__)

    def calculate_enhanced_score(
        self,
        base_fantasy_points: float,
        position: str,
        adp: Optional[float] = None,
        player_rating: Optional[float] = None,
        team_offensive_rank: Optional[int] = None,
        team_defensive_rank: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Calculate enhanced fantasy score with all adjustments applied.

        Args:
            base_fantasy_points: Base fantasy points projection
            position: Player position (QB, RB, WR, TE, K, DEF, etc.)
            adp: Average Draft Position (lower is better)
            player_rating: ESPN player rating (higher is better)
            team_offensive_rank: Team offensive quality rank (lower is better)
            team_defensive_rank: Team defensive quality rank (lower is better)

        Returns:
            Dictionary with enhanced score and breakdown of adjustments
        """
        if base_fantasy_points <= 0:
            return {
                "enhanced_score": 0.0,
                "base_score": base_fantasy_points,
                "total_multiplier": 1.0,
                "adjustments": {},
                "missing_data": []
            }

        adjustments = {}
        missing_data = []
        total_multiplier = 1.0

        # ADP-based market wisdom adjustment
        if self.config["enable_adp_adjustment"] and adp is not None:
            adp_multiplier = self._calculate_adp_adjustment(adp)
            adjustments["adp"] = adp_multiplier
            total_multiplier *= adp_multiplier
        elif self.config["enable_adp_adjustment"]:
            missing_data.append("adp")

        # ESPN player rating adjustment
        if self.config["enable_player_rating_adjustment"] and player_rating is not None:
            rating_multiplier = self._calculate_player_rating_adjustment(player_rating)
            adjustments["player_rating"] = rating_multiplier
            total_multiplier *= rating_multiplier
        elif self.config["enable_player_rating_adjustment"]:
            missing_data.append("player_rating")

        # Team quality context adjustment
        if self.config["enable_team_quality_adjustment"]:
            team_multiplier = self._calculate_team_quality_adjustment(
                position, team_offensive_rank, team_defensive_rank
            )
            if team_multiplier != 1.0:
                adjustments["team_quality"] = team_multiplier
                total_multiplier *= team_multiplier
            elif position in self.config["skill_positions"] and team_offensive_rank is None:
                missing_data.append("team_offensive_rank")
            elif position in self.config["defense_positions"] and team_defensive_rank is None:
                missing_data.append("team_defensive_rank")

        # Apply adjustment caps
        total_multiplier = max(
            self.config["min_total_adjustment"],
            min(self.config["max_total_adjustment"], total_multiplier)
        )

        enhanced_score = base_fantasy_points * total_multiplier

        return {
            "enhanced_score": round(enhanced_score, 2),
            "base_score": base_fantasy_points,
            "total_multiplier": round(total_multiplier, 3),
            "adjustments": adjustments,
            "missing_data": missing_data
        }

    def _calculate_adp_adjustment(self, adp: float) -> float:
        """Calculate ADP-based market wisdom adjustment multiplier."""
        if adp <= self.config["adp_excellent_threshold"]:
            return self.config["adp_excellent_multiplier"]
        elif adp <= self.config["adp_good_threshold"]:
            return self.config["adp_good_multiplier"]
        elif adp >= self.config["adp_poor_threshold"]:
            return self.config["adp_poor_multiplier"]
        else:
            # Linear interpolation for middle range
            if adp <= self.config["adp_good_threshold"]:
                # Between good and neutral (100-150 range)
                neutral_point = (self.config["adp_good_threshold"] + self.config["adp_poor_threshold"]) / 2
                if adp <= neutral_point:
                    ratio = (neutral_point - adp) / (neutral_point - self.config["adp_good_threshold"])
                    return 1.0 + ratio * (self.config["adp_good_multiplier"] - 1.0)

            return 1.0  # Neutral adjustment for middle range

    def _calculate_player_rating_adjustment(self, player_rating: float) -> float:
        """Calculate ESPN player rating adjustment multiplier."""
        if player_rating >= self.config["player_rating_excellent_threshold"]:
            multiplier = self.config["player_rating_excellent_multiplier"]
        elif player_rating >= self.config["player_rating_good_threshold"]:
            multiplier = self.config["player_rating_good_multiplier"]
        elif player_rating <= self.config["player_rating_poor_threshold"]:
            multiplier = self.config["player_rating_poor_multiplier"]
        else:
            # Linear interpolation for middle range (30-60)
            if player_rating <= 45:  # Poor to neutral range
                ratio = (player_rating - self.config["player_rating_poor_threshold"]) / (45 - self.config["player_rating_poor_threshold"])
                multiplier = self.config["player_rating_poor_multiplier"] + ratio * (1.0 - self.config["player_rating_poor_multiplier"])
            else:  # Neutral to good range (45-60)
                ratio = (player_rating - 45) / (self.config["player_rating_good_threshold"] - 45)
                multiplier = 1.0 + ratio * (self.config["player_rating_good_multiplier"] - 1.0)

        # Apply rating-specific cap
        return min(self.config["player_rating_max_boost"], multiplier)

    def _calculate_team_quality_adjustment(
        self,
        position: str,
        team_offensive_rank: Optional[int],
        team_defensive_rank: Optional[int]
    ) -> float:
        """Calculate team quality context adjustment multiplier."""
        # Determine which ranking to use based on position
        if position in self.config["skill_positions"]:
            team_rank = team_offensive_rank
        elif position in self.config["defense_positions"]:
            team_rank = team_defensive_rank
        else:
            return 1.0  # No adjustment for unknown positions

        if team_rank is None:
            return 1.0  # No adjustment if data unavailable

        # Apply team quality multipliers (lower rank = better team)
        if team_rank <= self.config["team_excellent_threshold"]:
            return self.config["team_excellent_multiplier"]
        elif team_rank <= self.config["team_good_threshold"]:
            return self.config["team_good_multiplier"]
        elif team_rank >= self.config["team_poor_threshold"]:
            return self.config["team_poor_multiplier"]
        else:
            return 1.0  # Neutral adjustment for middle-tier teams

    def get_adjustment_summary(self, calculation_result: Dict[str, Any]) -> str:
        """
        Generate human-readable summary of scoring adjustments.

        Args:
            calculation_result: Result from calculate_enhanced_score()

        Returns:
            Formatted string summarizing the adjustments made
        """
        if calculation_result["total_multiplier"] == 1.0:
            return "No adjustments applied"

        summary_parts = []
        adjustments = calculation_result["adjustments"]

        if "adp" in adjustments:
            adp_mult = adjustments["adp"]
            if adp_mult > 1.0:
                summary_parts.append(f"ADP boost (+{(adp_mult-1)*100:.1f}%)")
            else:
                summary_parts.append(f"ADP penalty ({(1-adp_mult)*100:.1f}%)")

        if "player_rating" in adjustments:
            rating_mult = adjustments["player_rating"]
            if rating_mult > 1.0:
                summary_parts.append(f"Rating boost (+{(rating_mult-1)*100:.1f}%)")
            else:
                summary_parts.append(f"Rating penalty ({(1-rating_mult)*100:.1f}%)")

        if "team_quality" in adjustments:
            team_mult = adjustments["team_quality"]
            if team_mult > 1.0:
                summary_parts.append(f"Team boost (+{(team_mult-1)*100:.1f}%)")
            else:
                summary_parts.append(f"Team penalty ({(1-team_mult)*100:.1f}%)")

        total_change = calculation_result["total_multiplier"]
        if total_change > 1.0:
            total_summary = f"Total: +{(total_change-1)*100:.1f}%"
        else:
            total_summary = f"Total: -{(1-total_change)*100:.1f}%"

        return f"{', '.join(summary_parts)} -> {total_summary}"


# Convenience function for single player calculations
def calculate_enhanced_player_score(
    base_fantasy_points: float,
    position: str,
    adp: Optional[float] = None,
    player_rating: Optional[float] = None,
    team_offensive_rank: Optional[int] = None,
    team_defensive_rank: Optional[int] = None,
    config: Optional[Dict[str, Any]] = None
) -> float:
    """
    Calculate enhanced score for a single player (simplified interface).

    Returns:
        Enhanced fantasy points score as float
    """
    calculator = EnhancedScoringCalculator(config)
    result = calculator.calculate_enhanced_score(
        base_fantasy_points, position, adp, player_rating,
        team_offensive_rank, team_defensive_rank
    )
    return result["enhanced_score"]


# Example usage and testing
if __name__ == "__main__":
    # Test the Hunt vs Henderson case
    calculator = EnhancedScoringCalculator()

    # Kareem Hunt example (higher projections, but older veteran)
    hunt_result = calculator.calculate_enhanced_score(
        base_fantasy_points=135.54,
        position="RB",
        adp=120.0,  # Later draft position (worse)
        player_rating=45.0,  # Medium rating
        team_offensive_rank=8,  # Good team offense
        team_defensive_rank=None
    )

    # TreVeyon Henderson example (lower projections, but younger with upside)
    henderson_result = calculator.calculate_enhanced_score(
        base_fantasy_points=121.97,
        position="RB",
        adp=85.0,   # Earlier draft position (better)
        player_rating=65.0,  # Better rating
        team_offensive_rank=18,  # Average team offense
        team_defensive_rank=None
    )

    print("Hunt vs Henderson Scoring Comparison:")
    print(f"Hunt: {hunt_result['base_score']:.2f} -> {hunt_result['enhanced_score']:.2f}")
    print(f"  {calculator.get_adjustment_summary(hunt_result)}")
    print(f"Henderson: {henderson_result['base_score']:.2f} -> {henderson_result['enhanced_score']:.2f}")
    print(f"  {calculator.get_adjustment_summary(henderson_result)}")

    if henderson_result['enhanced_score'] > hunt_result['enhanced_score']:
        print("SUCCESS: Henderson now scores higher than Hunt (expected outcome)")
    else:
        print("ISSUE: Hunt still scores higher than Henderson")