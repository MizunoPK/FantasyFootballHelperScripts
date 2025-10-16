from pathlib import Path
from typing import Dict, Any, List

import sys

sys.path.append(str(Path(__file__).parent.parent))
from util.PlayerManager import PlayerManager
from util.ScoredPlayer import ScoredPlayer

sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.DraftedRosterManager import DraftedRosterManager
from utils.FantasyPlayer import FantasyPlayer

class TradeSimTeam:

    def __init__(self, name : str, team : List[FantasyPlayer], player_manager : PlayerManager, isOpponent = True):
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
        total = 0
        for player in self.team:
            if self.isOpponent:
                scored_player = self.player_manager.score_player(player, adp=False, player_rating=False, team_quality=False, performance=False, matchup=False, bye=False, injury=False, roster=self.team)
            else:
                scored_player = self.player_manager.score_player(player, adp=False, player_rating=True, team_quality=True, performance=True, matchup=False, bye=True, injury=False, roster=self.team)
            player.score = scored_player.score
            self.scored_players[player.id] = scored_player  # Store the ScoredPlayer object
            total += scored_player.score

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