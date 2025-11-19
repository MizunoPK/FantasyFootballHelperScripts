"""
Trade Simulation Team

Represents a fantasy football team in trade simulation scenarios.
Used by the trade simulator to evaluate trade fairness by scoring both teams
with different scoring configurations (opponent vs user team scoring).

Key responsibilities:
- Managing team roster with injury filtering
- Calculating team scores using PlayerManager scoring engine
- Applying different scoring rules for opponent vs user teams
- Caching ScoredPlayer objects for performance
- Providing scored player data for trade evaluation display

Author: Kai Mizuno
"""

from pathlib import Path
from typing import Dict, Any, List

import sys

sys.path.append(str(Path(__file__).parent.parent))
from util.PlayerManager import PlayerManager
from util.ScoredPlayer import ScoredPlayer

sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.FantasyPlayer import FantasyPlayer

class TradeSimTeam:
    """
    Represents a fantasy football team in trade simulation with customizable scoring.

    This class manages a team's roster and calculates team scores using different
    scoring configurations based on whether it's the user's team or an opponent team.
    """

    def __init__(self, name : str, team : List[FantasyPlayer], player_manager : PlayerManager, isOpponent: bool = True, use_weekly_scoring: bool = False) -> None:
        """
        Initialize TradeSimTeam with roster and scoring configuration.

        Filters out injured players (keeps only ACTIVE and QUESTIONABLE) and
        calculates team score using PlayerManager's scoring engine with
        different configurations for opponent vs user teams.

        Args:
            name (str): Team name for identification
            team (List[FantasyPlayer]): Complete roster including injured players
            player_manager (PlayerManager): PlayerManager instance for scoring
            isOpponent (bool): If True, use simplified opponent scoring;
                              if False, use comprehensive user team scoring. Defaults to True.
            use_weekly_scoring (bool): If True, use weekly projections with matchup scoring
                                      (matches Starter Helper). If False, use seasonal
                                      projections with standard scoring. Defaults to False.
        """
        self.name = name

        # Filter out injured reserve players
        self.team : List[FantasyPlayer] = []
        for p in team:
            if p.injury_status in ['ACTIVE', 'QUESTIONABLE', 'OUT']:
                self.team.append(p)

        self.player_manager = player_manager
        self.isOpponent = isOpponent
        self.use_weekly_scoring = use_weekly_scoring
        self.team_score = 0
        self.scored_players : Dict[int, ScoredPlayer] = {}  # Maps player ID to ScoredPlayer
        self.score_team()

    def score_team(self) -> float:
        """
        Calculate total team score using PlayerManager's scoring engine.

        Uses different scoring configurations based on team type and scoring mode:
        - Weekly scoring (use_weekly_scoring=True): Matches Starter Helper exactly
          (weekly projections, matchup=True, player_rating=False, schedule=False)
        - Seasonal scoring (use_weekly_scoring=False): Standard scoring
          (seasonal projections, matchup=False, player_rating=True, schedule=True)
        - Opponent teams (isOpponent=True): No bye penalties
        - User team (isOpponent=False): Include bye penalties (seasonal mode only)

        Returns:
            float: Total team score (sum of all player scores)
        """
        total = 0

        # Iterate through all active players on the team roster
        for player in self.team:
            # Determine scoring parameters based on mode
            if self.use_weekly_scoring:
                # CURRENT WEEK MODE: Match Starter Helper EXACTLY
                # Uses weekly projections with matchup and performance multipliers
                scored_player = self.player_manager.score_player(
                    player,
                    use_weekly_projection=True,  # Weekly, not seasonal
                    adp=False,
                    player_rating=False,         # Disabled for weekly
                    team_quality=True,           # Included per Q2
                    performance=True,            # Recent actual vs projected
                    matchup=True,                # Enabled for weekly
                    schedule=False,              # Disabled for weekly
                    bye=False,                   # Never penalize in weekly mode
                    injury=False,
                    roster=self.team
                )
            elif self.isOpponent:
                # REST OF SEASON MODE - Opponent scoring (no bye penalties)
                scored_player = self.player_manager.score_player(
                    player, adp=False, player_rating=True, team_quality=True,
                    performance=True, matchup=False, schedule=True, bye=False,
                    injury=False, roster=self.team
                )
            else:
                # REST OF SEASON MODE - User team scoring (includes bye penalties)
                scored_player = self.player_manager.score_player(
                    player, adp=False, player_rating=True, team_quality=True,
                    performance=True, matchup=False, schedule=True, bye=True,
                    injury=False, roster=self.team
                )

            player.score = scored_player.score

            # Cache the ScoredPlayer object for later retrieval
            # Needed for displaying trade details with scoring breakdown
            self.scored_players[player.id] = scored_player

            # Accumulate total team score
            total += scored_player.score

        # Store computed team score and return
        self.team_score = total
        return total

    def get_scored_players(self, players: List[FantasyPlayer]) -> List[ScoredPlayer]:
        """
        Get ScoredPlayer objects for a list of FantasyPlayer objects.

        Args:
            players: List of FantasyPlayer objects

        Returns:
            List of corresponding ScoredPlayer objects
        """
        return [self.scored_players[p.id] for p in players if p.id in self.scored_players]