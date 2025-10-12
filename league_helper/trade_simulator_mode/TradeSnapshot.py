from pathlib import Path
from typing import Dict, Any, List

import sys
from trade_simulator_mode.TradeSimTeam import TradeSimTeam

sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.FantasyPlayer import FantasyPlayer

class TradeSnapshot:

    def __init__(self, my_new_team : TradeSimTeam, my_new_players : List[FantasyPlayer],
                 their_new_team : TradeSimTeam, their_new_players : List[FantasyPlayer]):
        self.my_new_team = my_new_team
        self.my_new_players = my_new_players
        self.their_new_team = their_new_team
        self.their_new_players = their_new_players