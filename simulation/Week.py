"""
Week

Represents a single week of fantasy football matchups in the simulated league.
Manages matchups between teams and calculates results based on weekly lineups.

Each week:
- Teams are paired into matchups
- Each team sets their optimal weekly lineup
- Actual points are calculated and compared
- Winners are determined (higher score wins, ties = both lose)

Author: Kai Mizuno
"""

import sys
from pathlib import Path
from typing import List, Tuple, Dict, Union

# Import team classes
sys.path.append(str(Path(__file__).parent))
from DraftHelperTeam import DraftHelperTeam
from SimulatedOpponent import SimulatedOpponent

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils.LoggingManager import get_logger

# Type alias for team (can be either DraftHelperTeam or SimulatedOpponent)
Team = Union[DraftHelperTeam, SimulatedOpponent]


class WeekResult:
    """
    Results for a single team in a week.

    Attributes:
        team: The team
        points_scored (float): Points scored by this team
        points_against (float): Points scored by opponent
        won (bool): True if team won, False if lost or tied
    """

    def __init__(self, team: Team, points_scored: float, points_against: float, won: bool) -> None:
        self.team = team
        self.points_scored = points_scored
        self.points_against = points_against
        self.won = won

    def __repr__(self) -> str:
        result = "W" if self.won else "L"
        return f"WeekResult({result}, {self.points_scored:.2f}-{self.points_against:.2f})"


class Week:
    """
    Represents a single week of fantasy football matchups.

    Manages all matchups for the week, simulates each game, and tracks results.

    Attributes:
        week_number (int): Week number (1-17)
        matchups (List[Tuple[Team, Team]]): List of (team1, team2) matchups
        results (Dict[Team, WeekResult]): Results for each team after simulation
        logger: Logger instance
    """

    def __init__(self, week_number: int, matchups: List[Tuple[Team, Team]]) -> None:
        """
        Initialize Week with matchups.

        Args:
            week_number (int): Week number (1-16)
            matchups (List[Tuple[Team, Team]]): List of team matchups

        Raises:
            ValueError: If week_number is not between 1 and 16
        """
        if not (1 <= week_number <= 16):
            raise ValueError(f"Week number must be between 1 and 16, got {week_number}")

        self.logger = get_logger()
        self.week_number = week_number
        self.matchups = matchups
        self.results: Dict[Team, WeekResult] = {}

        self.logger.debug(f"Initialized Week {week_number} with {len(matchups)} matchups")

    def simulate_week(self) -> Dict[Team, WeekResult]:
        """
        Simulate all matchups for this week.

        For each matchup:
        1. Both teams set their weekly lineup
        2. Actual points are calculated
        3. Winner is determined (higher score wins, tie = both lose)
        4. Results are stored

        Returns:
            Dict[Team, WeekResult]: Results for each team

        Note:
            Teams with higher points win. Ties count as losses for both teams.
        """
        self.logger.debug(f"Simulating Week {self.week_number} with {len(self.matchups)} matchups")

        for team1, team2 in self.matchups:
            # Both teams set their weekly lineup and get actual points scored
            points1 = team1.set_weekly_lineup(self.week_number)
            points2 = team2.set_weekly_lineup(self.week_number)

            # Determine winner (ties = both lose)
            team1_won = points1 > points2
            team2_won = points2 > points1

            # Store results
            self.results[team1] = WeekResult(team1, points1, points2, team1_won)
            self.results[team2] = WeekResult(team2, points2, points1, team2_won)

            # Log matchup result
            if team1_won:
                self.logger.debug(f"Week {self.week_number}: Team 1 wins {points1:.2f}-{points2:.2f}")
            elif team2_won:
                self.logger.debug(f"Week {self.week_number}: Team 2 wins {points2:.2f}-{points1:.2f}")
            else:
                self.logger.debug(f"Week {self.week_number}: Tie {points1:.2f}-{points2:.2f} (both lose)")

        self.logger.debug(f"Week {self.week_number} simulation complete")
        return self.results

    def get_result(self, team: Team) -> WeekResult:
        """
        Get the result for a specific team.

        Args:
            team: Team to get result for

        Returns:
            WeekResult: Result for the team

        Raises:
            ValueError: If team did not play in this week
        """
        if team not in self.results:
            raise ValueError(f"Team did not play in week {self.week_number}")

        return self.results[team]

    def get_all_results(self) -> Dict[Team, WeekResult]:
        """Get all results for this week."""
        return self.results.copy()

    def get_matchups(self) -> List[Tuple[Team, Team]]:
        """Get all matchups for this week."""
        return self.matchups.copy()

    def __repr__(self) -> str:
        return f"Week({self.week_number}, {len(self.matchups)} matchups)"
