

from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass


sys.path.append(str(Path(__file__).parent))
import constants as Constants

import sys
sys.path.append(str(Path(__file__).parent.parent))
from util.ConfigManager import ConfigManager
from util.PlayerManager import PlayerManager
from util.TeamDataManager import TeamDataManager

sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.LoggingManager import get_logger
from utils.FantasyPlayer import FantasyPlayer


@dataclass
class StartingRecommendation:
    """Represents a starting lineup recommendation"""
    player_id: str
    name: str
    position: str
    team: str
    injury_status: str
    bye_week: int
    adjusted_score: float
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


class StarterHelperModeManager:

    def __init__(self, config: ConfigManager, player_manager : PlayerManager, team_data_manager : TeamDataManager):
        self.config = config
        self.player_manager = player_manager
        self.config = config
        self.logger = get_logger()
        self.logger.debug("Initializing Add to Roster Mode Manager")
        self.set_managers(player_manager, team_data_manager)
    
    def set_managers(self, player_manager : PlayerManager, team_data_manager : TeamDataManager):
        self.player_manager = player_manager
        self.team_data_manager = team_data_manager

    def show_reccommended_starters(self, player_manager, team_data_manager):
        self.set_managers(player_manager, team_data_manager)

    def create_starting_recommendation(self,
                                     player_data: FantasyPlayer) -> StartingRecommendation:
        """
        Create a StartingRecommendation from player data

        Returns:
            StartingRecommendation object
        """

        adjusted_score = self.player_manager.score_player(player_data, adp=False, player_rating=False, team_quality=False, consistency=True, matchup=True)

        return StartingRecommendation(
            player_id=str(player_data.id),
            name=player_data.name,
            position=player_data.position,
            team=player_data.team,
            injury_status=player_data.injury_status,
            bye_week=player_data.bye_week,
            adjusted_score=adjusted_score
        )

    def optimize_lineup(self) -> Tuple[OptimalLineup, List[StartingRecommendation]]:
        """
        Optimize starting lineup based on current week projections

        Args:
            roster_players: DataFrame of roster players (drafted=2)
            projections: Dictionary mapping player_id to current week projections

        Returns:
            OptimalLineup object with best recommendations for each position
        """
        self.logger.info("Optimizing starting lineup for current week")

        scored_players = []
        for player in self.player_manager.team.roster:
            recommendation = self.create_starting_recommendation(
                player
            )
            scored_players.append(recommendation)

        # Sort by adjusted score (highest first)
        scored_players.sort(key=lambda x: x.adjusted_score, reverse=True)

        lineup = OptimalLineup()
        bench = []

        self.logger.info(f"Lineup optimization complete. Total projected points: {lineup.total_projected_points:.1f}")
        return lineup, bench
        