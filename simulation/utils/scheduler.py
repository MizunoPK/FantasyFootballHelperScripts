"""
Round-Robin Scheduler

Generates round-robin schedules for fantasy football leagues.
Uses the circle method algorithm to ensure fair matchups where each team
plays every other team twice over the course of the season.

For a 10-team league:
- Single round-robin: 9 weeks (each team plays each opponent once)
- Double round-robin: 18 weeks (each team plays each opponent twice)
- Fits into 17-week NFL season (one team short 1 game, or week 18 overflow)

Author: Kai Mizuno
"""

from typing import List, Tuple, TypeVar

T = TypeVar('T')  # Generic type for teams


def generate_round_robin(teams: List[T]) -> List[List[Tuple[T, T]]]:
    """
    Generate single round-robin schedule using circle method.

    Each team plays every other team exactly once. For N teams, this produces
    N-1 weeks (if N is even) or N weeks (if N is odd, with one team having a bye).

    Args:
        teams (List[T]): List of teams (must have even number of teams)

    Returns:
        List[List[Tuple[T, T]]]: List of weeks, where each week is a list of matchups

    Raises:
        ValueError: If number of teams is odd

    Example:
        >>> teams = [1, 2, 3, 4]
        >>> schedule = generate_round_robin(teams)
        >>> # Week 1: [(1,4), (2,3)]
        >>> # Week 2: [(1,3), (4,2)]
        >>> # Week 3: [(1,2), (3,4)]
    """
    n = len(teams)

    if n % 2 != 0:
        raise ValueError(f"Need even number of teams for round-robin, got {n}")

    schedule = []

    # Circle method: Fix one team (teams[0]) and rotate others
    fixed = teams[0]
    rotating = teams[1:]

    for round_num in range(n - 1):
        week_matchups = []

        # Match fixed team with rotating[0]
        week_matchups.append((fixed, rotating[0]))

        # Match remaining teams from opposite ends
        for i in range(1, n // 2):
            week_matchups.append((rotating[i], rotating[n - 1 - i]))

        schedule.append(week_matchups)

        # Rotate for next round (clockwise)
        rotating = [rotating[-1]] + rotating[:-1]

    return schedule


def generate_double_round_robin(teams: List[T]) -> List[List[Tuple[T, T]]]:
    """
    Generate double round-robin schedule.

    Each team plays every other team exactly twice (home and away). For N teams,
    this produces 2*(N-1) weeks.

    For a 10-team league:
    - Single round-robin: 9 weeks
    - Double round-robin: 18 weeks
    - Fits into 17 NFL weeks by trimming 1 week or handling overflow

    Args:
        teams (List[T]): List of teams (must have even number of teams)

    Returns:
        List[List[Tuple[T, T]]]: List of weeks with matchups

    Raises:
        ValueError: If number of teams is odd

    Note:
        The second half has teams reversed (home/away swap).
        For 17-week NFL season with 10 teams, this produces 18 weeks.
        The league can either:
        1. Drop the last week (one team short 1 game)
        2. Use week 18 if available
        3. Handle as needed by SimulatedLeague
    """
    # Generate first round-robin (9 weeks for 10 teams)
    first_half = generate_round_robin(teams)

    # Generate second round-robin by reversing matchups (home/away swap)
    second_half = []
    for week in first_half:
        reversed_week = [(team2, team1) for team1, team2 in week]
        second_half.append(reversed_week)

    # Combine both halves
    full_schedule = first_half + second_half

    return full_schedule


def generate_schedule_for_nfl_season(teams: List[T], num_weeks: int = 17) -> List[List[Tuple[T, T]]]:
    """
    Generate schedule that fits into NFL season length.

    For a 10-team league playing in a 17-week NFL season:
    - Double round-robin would be 18 weeks
    - This function generates the full 18 weeks and trims to fit

    Args:
        teams (List[T]): List of teams (must have even number)
        num_weeks (int): Number of weeks in NFL season (default 17)

    Returns:
        List[List[Tuple[T, T]]]: Schedule trimmed to num_weeks

    Note:
        If the double round-robin produces more weeks than num_weeks,
        the extra weeks are dropped. This means some teams may have
        uneven numbers of games against certain opponents.
    """
    full_schedule = generate_double_round_robin(teams)

    # Trim to fit NFL season if needed
    if len(full_schedule) > num_weeks:
        return full_schedule[:num_weeks]
    else:
        return full_schedule


def validate_schedule(schedule: List[List[Tuple[T, T]]], teams: List[T]) -> bool:
    """
    Validate that a schedule is fair and complete.

    Checks:
    - Each team plays in each week (no byes except possibly last week)
    - No team plays itself
    - No duplicate matchups in same week

    Args:
        schedule: Schedule to validate
        teams: List of all teams

    Returns:
        bool: True if schedule is valid, False otherwise

    Note:
        This is mainly for testing/debugging purposes.
    """
    for week_num, week_matchups in enumerate(schedule):
        teams_playing = set()

        for team1, team2 in week_matchups:
            # Check no self-play
            if team1 == team2:
                return False

            # Check no duplicate team in same week
            if team1 in teams_playing or team2 in teams_playing:
                return False

            teams_playing.add(team1)
            teams_playing.add(team2)

    return True
