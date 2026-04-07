"""
Scored Player Data Model

Data model for fantasy football players with calculated draft scores.
Combines player information with numeric scoring and detailed scoring breakdown
for display in draft recommendations and player evaluation.

Key responsibilities:
- Storing player object with associated draft score
- Tracking detailed scoring reasons (ADP, matchup, health, etc.)
- Formatted string representation for display
- Score and reason breakdown for user transparency
- Integration with PlayerScoringEngine scoring output

Author: Kai Mizuno
"""

from typing import List
from utils.FantasyPlayer import FantasyPlayer

class ScoredPlayer:
    """
    Data model combining a FantasyPlayer with their calculated draft score and scoring breakdown.

    This class is returned by the PlayerScoringEngine and used to display draft recommendations
    with transparent explanations of how each player's score was calculated.
    """

    def __init__(self, player : FantasyPlayer, score : float, reasons : List[str] = [], projected_points : float = 0.0):
        """
        Initialize a ScoredPlayer with a player, score, and scoring reasons.

        Args:
            player: FantasyPlayer instance with player data
            score: Calculated draft score (higher = better draft pick)
            reasons: List of human-readable scoring factor explanations
                    (e.g., "ADP: EXCELLENT", "Matchup: FAVORABLE")
            projected_points: Raw fantasy points projection used in scoring calculation
                             (ROS or weekly depending on scoring context). Default 0.0
                             for backward compatibility with existing callers.
        """
        self.player = player

        self.score = score

        self.reason = reasons

        self.projected_points = projected_points



    def __str__(self) -> str:
        """
        Convert ScoredPlayer to a formatted string representation.
        Automatically called when using print() or str() on the object.

        When projected_points is available (> 0), shows the projection prominently
        with the score as secondary. Otherwise falls back to score-only format
        for backward compatibility.

        Returns:
            Formatted string with player info and scoring reasons

        Example (with projection):
            [RB] [SF] Christian McCaffrey - 22.50 pts (Score: 145.67) (Bye=9)
                    - Projected: 22.50 pts, Weighted: 145.67 pts
                    - ADP: EXCELLENT

        Example (without projection):
            [RB] [SF] Christian McCaffrey - 145.67 pts (Bye=9)
                    - Base Projected Points: 22.5
                    - ADP: EXCELLENT
        """
        if self.projected_points > 0:
            header = f"[{self.player.position}] [{self.player.team}] {self.player.name} - {self.projected_points:.2f} pts (Score: {self.score:.2f}) (Bye={self.player.bye_week})"
        else:
            header = f"[{self.player.position}] [{self.player.team}] {self.player.name} - {self.score:.2f} pts (Bye={self.player.bye_week})"

        lines = [header]
        for reason in self.reason:
            lines.append(f"            - {reason}")

        return "\n".join(lines)