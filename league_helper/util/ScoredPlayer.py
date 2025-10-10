
from typing import List
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.FantasyPlayer import FantasyPlayer

class ScoredPlayer:

    def __init__(self, player : FantasyPlayer, score : float, reasons : List[str] = []):
        self.player = player
        self.score = score
        self.reason = reasons


    # Example to_string:
    # [QB] [KC] Patrick Mahomes - 123.45 pts
    #       - Base Projected Points: 20
    #       - ADP: EXCELLENT
    #       - Player Quality: EXCELLENT
    #       - Team Quality: GOOD
    #       - MATCHUP: NEUTRAL
    #       - Health: QUESTIONABLE

    def __str__(self) -> str:
        """
        Convert ScoredPlayer to a formatted string representation.
        Automatically called when using print() or str() on the object.

        Returns:
            Formatted string with player info and scoring reasons
        """
        # Header line with position, team, name, and score
        header = f"[{self.player.position}] [{self.player.team}] {self.player.name} - {self.score:.2f} pts"

        # Build the full string with reasons as bullet points
        lines = [header]
        for reason in self.reason:
            lines.append(f"            - {reason}")

        return "\n".join(lines)