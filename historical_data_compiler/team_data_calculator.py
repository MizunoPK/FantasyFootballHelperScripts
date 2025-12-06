#!/usr/bin/env python3
"""
Team Data Calculator for Historical Data Compiler

Calculates team-level statistics including fantasy points allowed to each position
from player weekly data and schedule information.

Creates team_data/{TEAM}.csv files for simulation.

Author: Kai Mizuno
"""

import csv
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional

from .constants import (
    ALL_NFL_TEAMS,
    FANTASY_POSITIONS,
    REGULAR_SEASON_WEEKS,
    TEAM_DATA_FOLDER,
)
from .player_data_fetcher import PlayerData
from .game_data_fetcher import GameData

import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.LoggingManager import get_logger


# Team data CSV columns
TEAM_DATA_CSV_COLUMNS = [
    "week",
    "pts_allowed_to_QB",
    "pts_allowed_to_RB",
    "pts_allowed_to_WR",
    "pts_allowed_to_TE",
    "pts_allowed_to_K",
    "points_scored",
    "points_allowed"
]


class TeamDataCalculator:
    """
    Calculates team-level statistics from player data.

    For each team and week:
    - Points allowed to each position (from opposing team's player stats)
    - Total fantasy points scored by team
    - NFL points allowed (from game data)
    """

    def __init__(self):
        """Initialize TeamDataCalculator."""
        self.logger = get_logger()

    def calculate_team_data(
        self,
        players: List[PlayerData],
        schedule: Dict[int, Dict[str, str]],
        game_data: List[GameData]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Calculate team data from player stats and schedule.

        Args:
            players: List of PlayerData with weekly points
            schedule: Schedule dict {week: {team: opponent}}
            game_data: List of GameData with scores

        Returns:
            Dict mapping team abbreviation to list of week data dicts
        """
        self.logger.info("Calculating team data from player stats")

        # Build lookup for game scores
        game_scores = self._build_game_scores_lookup(game_data)

        # Build lookup for player points by team and week
        player_points = self._build_player_points_lookup(players)

        # Calculate team data for each team
        team_data: Dict[str, List[Dict[str, Any]]] = {}

        for team in ALL_NFL_TEAMS:
            team_weeks = []

            for week in range(1, REGULAR_SEASON_WEEKS + 1):
                week_schedule = schedule.get(week, {})
                opponent = week_schedule.get(team)

                if not opponent:
                    # Bye week - all zeros
                    week_data = {
                        "week": week,
                        "pts_allowed_to_QB": 0.0,
                        "pts_allowed_to_RB": 0.0,
                        "pts_allowed_to_WR": 0.0,
                        "pts_allowed_to_TE": 0.0,
                        "pts_allowed_to_K": 0.0,
                        "points_scored": 0.0,
                        "points_allowed": 0.0
                    }
                else:
                    # Calculate stats from opponent's players
                    week_data = self._calculate_week_data(
                        team, opponent, week, player_points, game_scores
                    )

                team_weeks.append(week_data)

            team_data[team] = team_weeks

        self.logger.info(f"Calculated data for {len(team_data)} teams")
        return team_data

    def _build_game_scores_lookup(
        self,
        game_data: List[GameData]
    ) -> Dict[tuple, Dict[str, int]]:
        """
        Build lookup for game scores by week and teams.

        Args:
            game_data: List of GameData objects

        Returns:
            Dict mapping (week, home_team, away_team) to {home_score, away_score}
        """
        scores = {}
        for game in game_data:
            key = (game.week, game.home_team, game.away_team)
            scores[key] = {
                "home_score": game.home_team_score or 0,
                "away_score": game.away_team_score or 0
            }
            # Also store reverse lookup
            rev_key = (game.week, game.away_team, game.home_team)
            scores[rev_key] = {
                "home_score": game.away_team_score or 0,
                "away_score": game.home_team_score or 0
            }
        return scores

    def _build_player_points_lookup(
        self,
        players: List[PlayerData]
    ) -> Dict[str, Dict[int, Dict[str, float]]]:
        """
        Build lookup for player fantasy points by team, week, and position.

        Args:
            players: List of PlayerData objects

        Returns:
            Dict mapping team -> week -> position -> total_points
        """
        lookup: Dict[str, Dict[int, Dict[str, float]]] = defaultdict(
            lambda: defaultdict(lambda: defaultdict(float))
        )

        for player in players:
            if player.team == 'UNK':
                continue

            for week in range(1, REGULAR_SEASON_WEEKS + 1):
                points = player.week_points.get(week, 0.0)
                if points and points > 0:
                    lookup[player.team][week][player.position] += points

        return lookup

    def _calculate_week_data(
        self,
        team: str,
        opponent: str,
        week: int,
        player_points: Dict[str, Dict[int, Dict[str, float]]],
        game_scores: Dict[tuple, Dict[str, int]]
    ) -> Dict[str, Any]:
        """
        Calculate stats for a single team-week.

        Args:
            team: Team abbreviation
            opponent: Opponent team abbreviation
            week: Week number
            player_points: Player points lookup
            game_scores: Game scores lookup

        Returns:
            Dict with week data
        """
        # Points allowed to each position = opponent's players' points
        opponent_week_points = player_points.get(opponent, {}).get(week, {})

        pts_allowed_to_qb = opponent_week_points.get('QB', 0.0)
        pts_allowed_to_rb = opponent_week_points.get('RB', 0.0)
        pts_allowed_to_wr = opponent_week_points.get('WR', 0.0)
        pts_allowed_to_te = opponent_week_points.get('TE', 0.0)
        pts_allowed_to_k = opponent_week_points.get('K', 0.0)

        # Points scored by team's players
        team_week_points = player_points.get(team, {}).get(week, {})
        points_scored = sum(team_week_points.values())

        # NFL points allowed (from game data)
        points_allowed = 0.0
        # Find game involving team and opponent
        for key, scores in game_scores.items():
            game_week, home, away = key
            if game_week == week:
                if home == team and away == opponent:
                    points_allowed = float(scores.get("away_score", 0))
                    break
                elif away == team and home == opponent:
                    points_allowed = float(scores.get("home_score", 0))
                    break

        return {
            "week": week,
            "pts_allowed_to_QB": round(pts_allowed_to_qb, 1),
            "pts_allowed_to_RB": round(pts_allowed_to_rb, 1),
            "pts_allowed_to_WR": round(pts_allowed_to_wr, 1),
            "pts_allowed_to_TE": round(pts_allowed_to_te, 1),
            "pts_allowed_to_K": round(pts_allowed_to_k, 1),
            "points_scored": round(points_scored, 1),
            "points_allowed": round(points_allowed, 1)
        }

    def write_team_data_files(
        self,
        team_data: Dict[str, List[Dict[str, Any]]],
        output_dir: Path
    ) -> None:
        """
        Write team data CSV files.

        Creates one CSV per team in {output_dir}/team_data/{TEAM}.csv

        Args:
            team_data: Dict mapping team to list of week data
            output_dir: Base output directory
        """
        team_data_dir = output_dir / TEAM_DATA_FOLDER
        team_data_dir.mkdir(parents=True, exist_ok=True)

        self.logger.info(f"Writing team data to {team_data_dir}")

        for team, weeks_data in team_data.items():
            team_file = team_data_dir / f"{team}.csv"

            with open(team_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=TEAM_DATA_CSV_COLUMNS)
                writer.writeheader()
                writer.writerows(weeks_data)

        self.logger.info(f"Wrote {len(team_data)} team data files")


def calculate_and_write_team_data(
    players: List[PlayerData],
    schedule: Dict[int, Dict[str, str]],
    game_data: List[GameData],
    output_dir: Path
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Convenience function to calculate team data and write files.

    Args:
        players: List of PlayerData objects
        schedule: Schedule dict
        game_data: List of GameData objects
        output_dir: Output directory

    Returns:
        Team data dict for use by other modules
    """
    calculator = TeamDataCalculator()
    team_data = calculator.calculate_team_data(players, schedule, game_data)
    calculator.write_team_data_files(team_data, output_dir)
    return team_data
