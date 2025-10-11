import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "league_helper"))
from league_helper.util.PlayerManager import PlayerManager


class SimulatedOpponent:

    def __init__(self, projected_player_manager : PlayerManager, actual_player_manager : PlayerManager, strategy : str):
        pass