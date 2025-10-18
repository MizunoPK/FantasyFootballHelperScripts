"""
Trade Snapshot Data Model

Captures the complete state of a trade evaluation including both teams
before and after the proposed trade. Stores scored player data in both
original and new team contexts for accurate trade impact analysis.

Key responsibilities:
- Storing post-trade team states for both parties
- Tracking players exchanged with scoring in new team context
- Preserving original player scores for comparison
- Providing data structure for trade visualization and analysis

Author: Kai Mizuno
"""

from pathlib import Path
from typing import Dict, Any, List

import sys
from trade_simulator_mode.TradeSimTeam import TradeSimTeam

sys.path.append(str(Path(__file__).parent.parent))
from util.ScoredPlayer import ScoredPlayer

class TradeSnapshot:
    """
    Immutable snapshot of a trade evaluation with before/after team states.

    Stores the complete state of both teams after a proposed trade, including
    the scored players exchanged and the original scores for comparison.
    """

    def __init__(self, my_new_team : TradeSimTeam, my_new_players : List[ScoredPlayer],
                 their_new_team : TradeSimTeam, their_new_players : List[ScoredPlayer],
                 my_original_players : List[ScoredPlayer] = None,
                 waiver_recommendations : List[ScoredPlayer] = None,
                 their_waiver_recommendations : List[ScoredPlayer] = None,
                 my_dropped_players : List[ScoredPlayer] = None,
                 their_dropped_players : List[ScoredPlayer] = None):
        """
        Trade snapshot storing both new team state and original player scores.

        Args:
            my_new_team: My team after the trade (including waiver pickups)
            my_new_players: Players I receive (scored in new team context)
            their_new_team: Their team after the trade (including waiver pickups)
            their_new_players: Players they receive (scored in new team context)
            my_original_players: Players I give up (scored in original team context)
            waiver_recommendations: Recommended waiver wire pickups for my team to fill empty roster spots
            their_waiver_recommendations: Recommended waiver wire pickups for their team to fill empty roster spots
            my_dropped_players: Additional players I drop beyond the trade to make room
            their_dropped_players: Additional players opponent drops beyond the trade to make room
        """
        self.my_new_team = my_new_team
        self.my_new_players = my_new_players
        self.their_new_team = their_new_team
        self.their_new_players = their_new_players
        self.my_original_players = my_original_players if my_original_players is not None else []
        self.waiver_recommendations = waiver_recommendations if waiver_recommendations is not None else []
        self.their_waiver_recommendations = their_waiver_recommendations if their_waiver_recommendations is not None else []
        self.my_dropped_players = my_dropped_players if my_dropped_players is not None else []
        self.their_dropped_players = their_dropped_players if their_dropped_players is not None else []