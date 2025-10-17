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
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.FantasyPlayer import FantasyPlayer

class ScoredPlayer:
    """
    Data model combining a FantasyPlayer with their calculated draft score and scoring breakdown.

    This class is returned by the PlayerScoringEngine and used to display draft recommendations
    with transparent explanations of how each player's score was calculated.
    """

    def __init__(self, player : FantasyPlayer, score : float, reasons : List[str] = []):
        """
        Initialize a ScoredPlayer with a player, score, and scoring reasons.

        Args:
            player: FantasyPlayer instance with player data
            score: Calculated draft score (higher = better draft pick)
            reasons: List of human-readable scoring factor explanations
                    (e.g., "ADP: EXCELLENT", "Matchup: FAVORABLE")
        """
        # Store the base player object with all player data (name, position, team, etc.)
        self.player = player

        # Store the calculated draft score
        # Higher scores indicate better draft targets based on multiple factors
        self.score = score

        # Store list of scoring reasons for transparency
        # Allows users to understand WHY a player received their score
        # Format: ["Base Projected Points: 20.5", "ADP: EXCELLENT", "Health: QUESTIONABLE"]
        self.reason = reasons


    # Example output format from __str__:
    # [QB] [KC] Patrick Mahomes - 123.45 pts (Bye=7)
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

        Example:
            [RB] [SF] Christian McCaffrey - 145.67 pts (Bye=9)
                    - Base Projected Points: 22.5
                    - ADP: EXCELLENT
        """
        # Build header line: [Position] [Team] Player Name - Score pts (Bye=week)
        # Format: [RB] [SF] Christian McCaffrey - 145.67 pts (Bye=9)
        header = f"[{self.player.position}] [{self.player.team}] {self.player.name} - {self.score:.2f} pts (Bye={self.player.bye_week})"

        # Build the full output with scoring reasons as indented bullet points
        # Start with header, then add each reason on its own line
        lines = [header]
        for reason in self.reason:
            # 12 spaces of indentation to align with player name above
            lines.append(f"            - {reason}")

        # Join all lines with newlines for multi-line output
        return "\n".join(lines)