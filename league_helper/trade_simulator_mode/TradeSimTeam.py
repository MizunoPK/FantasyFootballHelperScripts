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

    def __init__(self, name : str, team : List[FantasyPlayer], player_manager : PlayerManager, isOpponent: bool = True) -> None:
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
        """
        self.name = name

        # Filter out injured players
        self.team : List[FantasyPlayer] = []
        for p in team:
            if p.injury_status in ['ACTIVE', 'QUESTIONABLE']:
                self.team.append(p)

        self.player_manager = player_manager
        self.isOpponent = isOpponent
        self.team_score = 0
        self.scored_players : Dict[int, ScoredPlayer] = {}  # Maps player ID to ScoredPlayer
        self.score_team()

    def score_team(self) -> float:
        """
        Calculate total team score using PlayerManager's scoring engine.

        Uses different scoring configurations based on team type:
        - Opponent teams: Simplified scoring (projections + player rating only)
        - User team: Comprehensive scoring (projections + rating + team quality + performance + bye penalties)

        Returns:
            float: Total team score (sum of all player scores)
        """
        total = 0

        # Iterate through all active players on the team roster
        for player in self.team:
            # ===== OPPONENT TEAM SCORING (Simplified) =====
            # For opponent/waiver teams, use minimal scoring factors to approximate their value
            # This gives a fair but simplified evaluation of their team strength
            if self.isOpponent:
                scored_player = self.player_manager.score_player(
                    player,
                    adp=False,              # No ADP bonus (opponent rosters don't benefit from draft position)
                    player_rating=True,     # Include player rating (skill level assessment)
                    team_quality=False,     # No team quality factor (opponent teams aren't optimized)
                    performance=False,      # No performance history (simplify opponent scoring)
                    matchup=False,          # No matchup bonus (not relevant for trade evaluation)
                    bye=False,              # No bye week penalties (opponent rosters already account for this)
                    injury=False,           # No injury penalty (injured players already filtered out in __init__)
                    roster=self.team        # Pass roster for position context
                )
            # ===== USER TEAM SCORING (Comprehensive) =====
            # For user team, use full scoring to accurately evaluate roster strength
            # This includes all factors that affect user's team performance
            else:
                scored_player = self.player_manager.score_player(
                    player,
                    adp=False,              # No ADP bonus (trade evaluation uses current performance, not draft position)
                    player_rating=True,     # Include player rating (skill level assessment)
                    team_quality=True,      # Include team quality (offensive line, coaching, scheme fit)
                    performance=True,       # Include performance history (consistency, recent form)
                    matchup=False,          # No matchup bonus (trade evaluation is season-long, not weekly)
                    bye=True,               # Include bye week penalties (affects roster optimization)
                    injury=False,           # No injury penalty (injured players already filtered out in __init__)
                    roster=self.team        # Pass roster for position context
                )

            # Update the player object with computed score
            # This allows direct access to score without re-calculation
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