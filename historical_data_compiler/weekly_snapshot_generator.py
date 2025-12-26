#!/usr/bin/env python3
"""
Weekly Snapshot Generator for Historical Data Compiler

Generates point-in-time snapshots for each week of the season.
Each snapshot represents what the system would know at that week:
- Actual data for completed weeks (1 to current_week-1)
- Projected data for current and future weeks

Creates weeks/week_NN/ folders with players.csv and players_projected.csv.

Author: Kai Mizuno
"""

import csv
from pathlib import Path
from typing import Dict, List, Any

from .constants import (
    REGULAR_SEASON_WEEKS,
    WEEKS_FOLDER,
    PLAYERS_FILE,
    PLAYERS_PROJECTED_FILE,
)
from .player_data_fetcher import PlayerData, PLAYERS_CSV_COLUMNS

import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.LoggingManager import get_logger


class WeeklySnapshotGenerator:
    """
    Generates point-in-time weekly snapshots for simulation.

    For week N snapshot:
    - week_N/players.csv: Actual points for weeks 1 to N-1, projected for N to 17
    - week_N/players_projected.csv: All projected values (what was projected at that time)
    - week_N/*.json: Position-specific JSON files (if GENERATE_JSON=True)

    This simulates what data would be available when running the system at week N.
    """

    def __init__(self, generate_csv: bool = True, generate_json: bool = True):
        """
        Initialize WeeklySnapshotGenerator.

        Args:
            generate_csv: Whether to generate CSV files (default True)
            generate_json: Whether to generate JSON files (default True)
        """
        self.logger = get_logger()
        self.generate_csv = generate_csv
        self.generate_json = generate_json

    def _calculate_player_ratings(
        self,
        players: List[PlayerData],
        current_week: int
    ) -> Dict[str, float]:
        """
        Calculate player ratings for a specific week snapshot.

        Per spec:
        - Week 1: Use original player_rating (based on draft rank)
        - Week 2+: Calculate from cumulative fantasy_points through (current_week - 1)

        Formula: player_rating = max(1, 100 - ((position_rank - 1) / total_in_position) * 99)
        Higher cumulative points = better rank = higher rating (100 = best)

        Args:
            players: List of PlayerData
            current_week: Current week (1-17)

        Returns:
            Dict mapping player_id to calculated rating
        """
        ratings: Dict[str, float] = {}

        if current_week == 1:
            # Week 1: Use original draft-based rating
            for player in players:
                ratings[player.id] = player.player_rating if player.player_rating else 50.0
            return ratings

        # Week 2+: Calculate from cumulative actual points through (current_week - 1)
        # Group players by position
        position_players: Dict[str, List[tuple]] = {}  # position -> [(player_id, cumulative_points)]

        for player in players:
            # Calculate cumulative actual points through (current_week - 1)
            cumulative_points = 0.0
            for week in range(1, current_week):
                points = player.week_points.get(week, 0.0)
                if points:
                    cumulative_points += points

            if player.position not in position_players:
                position_players[player.position] = []
            position_players[player.position].append((player.id, cumulative_points))

        # Calculate ratings for each position
        for position, player_list in position_players.items():
            # Sort by cumulative points descending (best performers first)
            player_list.sort(key=lambda x: x[1], reverse=True)
            total_in_position = len(player_list)

            for rank_index, (player_id, _) in enumerate(player_list):
                position_rank = rank_index + 1  # 1-based rank
                if total_in_position > 1:
                    # Formula: higher rank (lower number) = higher rating
                    rating = 100 - ((position_rank - 1) / (total_in_position - 1)) * 99
                else:
                    rating = 100.0
                ratings[player_id] = max(1.0, min(100.0, rating))

        return ratings

    def generate_all_weeks(
        self,
        players: List[PlayerData],
        output_dir: Path
    ) -> None:
        """
        Generate snapshots for all 17 weeks.

        Args:
            players: List of PlayerData with full season data
            output_dir: Base output directory
        """
        self.logger.info("Generating weekly snapshots for weeks 1-17")

        weeks_dir = output_dir / WEEKS_FOLDER

        for week in range(1, REGULAR_SEASON_WEEKS + 1):
            self._generate_week_snapshot(players, weeks_dir, week)

        self.logger.info(f"Generated {REGULAR_SEASON_WEEKS} weekly snapshots")

    def _generate_week_snapshot(
        self,
        players: List[PlayerData],
        weeks_dir: Path,
        current_week: int
    ) -> None:
        """
        Generate snapshot for a single week.

        For current_week N:
        - players.csv: Uses actual points for weeks 1 to N-1, projected for N to 17 (if GENERATE_CSV=True)
        - players_projected.csv: Uses all projected values (if GENERATE_CSV=True)
        - *.json: Position-specific JSON files (if GENERATE_JSON=True)

        Args:
            players: List of PlayerData
            weeks_dir: Weeks directory path
            current_week: Week number for this snapshot
        """
        week_dir = weeks_dir / f"week_{current_week:02d}"
        week_dir.mkdir(parents=True, exist_ok=True)

        # Generate CSV files (if enabled)
        if self.generate_csv:
            # Generate players.csv (smart values based on current week)
            players_path = week_dir / PLAYERS_FILE
            self._write_players_snapshot(players, players_path, current_week)

            # Generate players_projected.csv (point-in-time projections)
            projected_path = week_dir / PLAYERS_PROJECTED_FILE
            self._write_projected_snapshot(players, projected_path, current_week)

        # Generate JSON files (if enabled)
        if self.generate_json:
            from .json_exporter import generate_json_snapshots
            generate_json_snapshots(players, week_dir, current_week)

        self.logger.debug(f"Generated week {current_week} snapshot")

    def _write_players_snapshot(
        self,
        players: List[PlayerData],
        output_path: Path,
        current_week: int
    ) -> None:
        """
        Write players.csv snapshot for a specific week.

        Uses actual points for completed weeks (1 to current_week-1),
        and projected points for current and future weeks (current_week to 17).

        The fantasy_points field is calculated as sum of:
        - Actual points for weeks 1 to current_week-1
        - Projected points for weeks current_week to 17

        Player rating is calculated per spec:
        - Week 1: Use draft-based rating
        - Week 2+: Calculate from cumulative actual points through (current_week - 1)

        Args:
            players: List of PlayerData
            output_path: Output file path
            current_week: Current week (1-17)
        """
        # Calculate player ratings for this week's snapshot
        player_ratings = self._calculate_player_ratings(players, current_week)

        rows = []

        for player in players:
            # Build week points using actual for past, projected for future
            week_points = {}
            total_points = 0.0

            for week in range(1, REGULAR_SEASON_WEEKS + 1):
                # Bye week is always 0, regardless of current week
                if player.bye_week and week == player.bye_week:
                    points = 0.0
                elif week < current_week:
                    # Past weeks: use actual (from week_points, which has smart values)
                    points = player.week_points.get(week, 0.0)
                else:
                    # Current and future weeks: use projected
                    points = player.projected_weeks.get(week, 0.0)

                week_points[week] = points
                total_points += points if points else 0.0

            # Get calculated rating for this snapshot
            rating = player_ratings.get(player.id)

            # Build row
            row = {
                "id": player.id,
                "name": player.name,
                "team": player.team,
                "position": player.position,
                "bye_week": player.bye_week if player.bye_week is not None else "",
                "drafted": player.drafted,
                "locked": player.locked,
                "fantasy_points": round(total_points, 1),
                "average_draft_position": round(player.average_draft_position, 1) if player.average_draft_position else "",
                "player_rating": round(rating, 1) if rating else "",
                "injury_status": player.injury_status,
            }

            # Add weekly points
            for week in range(1, REGULAR_SEASON_WEEKS + 1):
                points = week_points.get(week)
                row[f"week_{week}_points"] = round(points, 1) if points else ""

            rows.append(row)

        # Sort by fantasy points
        rows.sort(key=lambda r: r.get("fantasy_points", 0), reverse=True)

        # Write CSV
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=PLAYERS_CSV_COLUMNS)
            writer.writeheader()
            writer.writerows(rows)

    def _write_projected_snapshot(
        self,
        players: List[PlayerData],
        output_path: Path,
        current_week: int
    ) -> None:
        """
        Write players_projected.csv with point-in-time projected values.

        Per spec:
        - Week < current_week: Use historical week-specific projection
        - Week >= current_week: Use current week's projection for ALL future weeks

        Player rating is calculated per spec:
        - Week 1: Use draft-based rating
        - Week 2+: Calculate from cumulative actual points through (current_week - 1)

        This creates a point-in-time view where at week X, future weeks
        use the best available projection (current week's projection).

        Args:
            players: List of PlayerData
            output_path: Output file path
            current_week: Current week (1-17)
        """
        # Calculate player ratings for this week's snapshot
        player_ratings = self._calculate_player_ratings(players, current_week)

        rows = []

        for player in players:
            # Get current week's projection for use in future weeks
            current_week_projection = player.projected_weeks.get(current_week, 0.0) or 0.0

            # Build week points per spec
            week_points = {}
            total_projected = 0.0

            for week in range(1, REGULAR_SEASON_WEEKS + 1):
                # Bye week is always 0, regardless of current week
                if player.bye_week and week == player.bye_week:
                    points = 0.0
                elif week < current_week:
                    # Past weeks: use historical week-specific projection
                    points = player.projected_weeks.get(week, 0.0) or 0.0
                else:
                    # Current and future weeks: use current week's projection
                    points = current_week_projection

                week_points[week] = points
                total_projected += points

            # Get calculated rating for this snapshot
            rating = player_ratings.get(player.id)

            row = {
                "id": player.id,
                "name": player.name,
                "team": player.team,
                "position": player.position,
                "bye_week": player.bye_week if player.bye_week is not None else "",
                "drafted": player.drafted,
                "locked": player.locked,
                "fantasy_points": round(total_projected, 1),
                "average_draft_position": round(player.average_draft_position, 1) if player.average_draft_position else "",
                "player_rating": round(rating, 1) if rating else "",
                "injury_status": player.injury_status,
            }

            # Add projected weekly points
            for week in range(1, REGULAR_SEASON_WEEKS + 1):
                points = week_points.get(week)
                row[f"week_{week}_points"] = round(points, 1) if points else ""

            rows.append(row)

        # Sort by fantasy points
        rows.sort(key=lambda r: r.get("fantasy_points", 0), reverse=True)

        # Write CSV
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=PLAYERS_CSV_COLUMNS)
            writer.writeheader()
            writer.writerows(rows)


def generate_weekly_snapshots(
    players: List[PlayerData],
    output_dir: Path,
    generate_csv: bool = True,
    generate_json: bool = True
) -> None:
    """
    Convenience function to generate all weekly snapshots.

    Args:
        players: List of PlayerData with full season data
        output_dir: Output directory
        generate_csv: Whether to generate CSV files (default True)
        generate_json: Whether to generate JSON files (default True)
    """
    generator = WeeklySnapshotGenerator(generate_csv=generate_csv, generate_json=generate_json)
    generator.generate_all_weeks(players, output_dir)
