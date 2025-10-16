from pathlib import Path
from typing import Dict, Any, List

import sys

sys.path.append(str(Path(__file__).parent.parent))
from util.PlayerManager import PlayerManager

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
        self.score_team()

    def score_team(self) -> float:
        total = 0
        for player in self.team:
            if self.isOpponent:
                scored_player = self.player_manager.score_player(player, adp=False, player_rating=False, team_quality=False, performance=False, matchup=False, bye=False, injury=False)
            else:
                scored_player = self.player_manager.score_player(player, adp=False, player_rating=True, team_quality=True, performance=True, matchup=False, bye=True, injury=False)
            player.score = scored_player.score
            total += scored_player.score

        self.team_score = total
        return total