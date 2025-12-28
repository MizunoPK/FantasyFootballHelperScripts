#!/usr/bin/env python3
"""
JSON Snapshot Exporter for Historical Data Compiler

Generates position-specific JSON files (qb_data.json, rb_data.json, etc.)
for each week snapshot with point-in-time logic.

Uses bridge adapter pattern to reuse stat extraction methods from
player-data-fetcher/player_data_exporter.py without modifications.

Author: Kai Mizuno
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional

import sys
sys.path.append(str(Path(__file__).parent.parent))  # Add project root
sys.path.append(str(Path(__file__).parent.parent / "player-data-fetcher"))  # Add player-data-fetcher folder

from player_data_exporter import DataExporter

from .constants import POSITION_JSON_FILES, REGULAR_SEASON_WEEKS, FANTASY_POSITIONS
from .player_data_fetcher import PlayerData
from utils.LoggingManager import get_logger


class PlayerDataAdapter:
    """
    Minimal ESPNPlayerData-like object for bridge pattern.

    Converts historical PlayerData to format compatible with
    player_data_exporter stat extraction methods.

    Note: Does NOT take current_week parameter because stat extraction
    methods extract ALL 17 weeks at once. Point-in-time logic is applied
    AFTER extraction in the JSON generation methods.
    """

    def __init__(self, player_data: PlayerData):
        """
        Initialize adapter with PlayerData.

        Args:
            player_data: PlayerData object from historical data fetcher
        """
        # Core fields (match ESPNPlayerData from player_data_models.py:25-81)
        self.id = player_data.id
        self.name = player_data.name
        self.team = player_data.team
        self.position = player_data.position
        self.bye_week = player_data.bye_week
        self.injury_status = player_data.injury_status if player_data.injury_status else "ACTIVE"
        self.average_draft_position = player_data.average_draft_position

        # Critical: raw_stats for stat extraction methods
        self.raw_stats = player_data.raw_stats  # List[Dict[str, Any]]


class JSONSnapshotExporter:
    """
    Generates position-specific JSON files for weekly snapshots.

    For week N snapshot:
    - actual_points: Actual for weeks 1 to N-1, 0.0 for weeks N to 17
    - projected_points: Historical for weeks 1 to N-1, current week projection for N to 17
    - Stat arrays: Actual for weeks 1 to N-1, 0.0 for weeks N to 17
    - player_rating: Week 1 uses draft-based, Week 2+ recalculated from cumulative actuals

    Uses bridge adapter pattern to call player_data_exporter stat extraction methods.
    """

    def __init__(self):
        """Initialize JSONSnapshotExporter."""
        self.logger = get_logger()

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

    def _apply_point_in_time_logic(
        self,
        full_array: List[float],
        current_week: int,
        array_type: str,
        current_week_value: Optional[float] = None
    ) -> List[float]:
        """
        Apply point-in-time logic to stat arrays.

        Args:
            full_array: Full 17-week array from stat extraction
            current_week: Current week (1-17)
            array_type: Type of array ("actual", "projected", or "stat")
            current_week_value: For projected arrays, the value to repeat for future weeks

        Returns:
            Modified array with point-in-time logic applied
        """
        result = []

        for week_idx in range(REGULAR_SEASON_WEEKS):
            week_num = week_idx + 1

            if week_num < current_week:
                # Past weeks: use actual values from array
                result.append(full_array[week_idx] if week_idx < len(full_array) else 0.0)
            else:
                # Current and future weeks
                if array_type == "actual" or array_type == "stat":
                    # Actual/stat arrays: 0.0 for current and future weeks
                    result.append(0.0)
                elif array_type == "projected":
                    # Projected arrays: use current week's projection for all future weeks
                    result.append(current_week_value if current_week_value is not None else 0.0)
                else:
                    result.append(0.0)

        return result

    def _extract_stats_for_player(
        self,
        player_data: PlayerData,
        current_week: int
    ) -> Dict[str, Any]:
        """
        Extract position-specific stats for a player using bridge adapter pattern.

        Args:
            player_data: PlayerData object
            current_week: Current week for point-in-time logic

        Returns:
            Dict with position-specific stat arrays (with point-in-time logic applied)
        """
        # Create adapter for this player
        adapter = PlayerDataAdapter(player_data)

        # Create DataExporter instance (just for calling stat extraction methods)
        # We don't actually use the output_dir since we only call the private methods
        exporter = DataExporter(output_dir=str(Path.cwd()), create_latest_files=False)

        # Extract stats based on position (returns dict with arrays of 17 floats)
        result = {}

        if player_data.position == 'QB':
            passing_stats = exporter._extract_passing_stats(adapter)
            rushing_stats = exporter._extract_rushing_stats(adapter)

            # Apply point-in-time logic and wrap in position keys
            result['passing'] = {}
            for stat_name, stat_array in passing_stats.items():
                if isinstance(stat_array, list):
                    result['passing'][stat_name] = self._apply_point_in_time_logic(
                        stat_array, current_week, "stat"
                    )

            result['rushing'] = {}
            for stat_name, stat_array in rushing_stats.items():
                if isinstance(stat_array, list):
                    result['rushing'][stat_name] = self._apply_point_in_time_logic(
                        stat_array, current_week, "stat"
                    )

        elif player_data.position == 'RB':
            rushing_stats = exporter._extract_rushing_stats(adapter)
            receiving_stats = exporter._extract_receiving_stats(adapter)

            result['rushing'] = {}
            for stat_name, stat_array in rushing_stats.items():
                if isinstance(stat_array, list):
                    result['rushing'][stat_name] = self._apply_point_in_time_logic(
                        stat_array, current_week, "stat"
                    )

            result['receiving'] = {}
            for stat_name, stat_array in receiving_stats.items():
                if isinstance(stat_array, list):
                    result['receiving'][stat_name] = self._apply_point_in_time_logic(
                        stat_array, current_week, "stat"
                    )

        elif player_data.position in ['WR', 'TE']:
            rushing_stats = exporter._extract_rushing_stats(adapter)
            receiving_stats = exporter._extract_receiving_stats(adapter)

            result['rushing'] = {}
            for stat_name, stat_array in rushing_stats.items():
                if isinstance(stat_array, list):
                    result['rushing'][stat_name] = self._apply_point_in_time_logic(
                        stat_array, current_week, "stat"
                    )

            result['receiving'] = {}
            for stat_name, stat_array in receiving_stats.items():
                if isinstance(stat_array, list):
                    result['receiving'][stat_name] = self._apply_point_in_time_logic(
                        stat_array, current_week, "stat"
                    )

        elif player_data.position == 'K':
            kicking_stats = exporter._extract_kicking_stats(adapter)

            result['kicking'] = {}
            for stat_name, stat_array in kicking_stats.items():
                if isinstance(stat_array, list):
                    result['kicking'][stat_name] = self._apply_point_in_time_logic(
                        stat_array, current_week, "stat"
                    )

        elif player_data.position == 'DST':
            defense_stats = exporter._extract_defense_stats(adapter)

            result['defense'] = {}
            for stat_name, stat_array in defense_stats.items():
                if isinstance(stat_array, list):
                    result['defense'][stat_name] = self._apply_point_in_time_logic(
                        stat_array, current_week, "stat"
                    )
        else:
            self.logger.warning(f"Unknown position {player_data.position} for player {player_data.name}")
            return {}

        return result

    def _build_player_json_object(
        self,
        player_data: PlayerData,
        current_week: int,
        player_rating: float
    ) -> Dict[str, Any]:
        """
        Build JSON object for a single player with all fields.

        Args:
            player_data: PlayerData object
            current_week: Current week for point-in-time logic
            player_rating: Calculated player rating for this week

        Returns:
            Dict with all player fields for JSON output
        """
        # Build actual_points array (actuals for weeks 1 to N-1, 0.0 for N to 17)
        actual_points = []
        for week in range(1, REGULAR_SEASON_WEEKS + 1):
            if week < current_week:
                # Past weeks: use actual points
                points = player_data.week_points.get(week, 0.0)
                actual_points.append(points if points else 0.0)
            else:
                # Current and future weeks: 0.0
                actual_points.append(0.0)

        # Build projected_points array (historical for 1 to N-1, current week projection for N to 17)
        current_week_projection = player_data.projected_weeks.get(current_week, 0.0) or 0.0
        projected_points = []
        for week in range(1, REGULAR_SEASON_WEEKS + 1):
            if week < current_week:
                # Past weeks: use historical projection
                proj = player_data.projected_weeks.get(week, 0.0)
                projected_points.append(proj if proj else 0.0)
            else:
                # Current and future weeks: use current week's projection
                projected_points.append(current_week_projection)

        # Handle bye weeks: Set to 0.0 in all arrays
        if player_data.bye_week:
            bye_idx = player_data.bye_week - 1
            if 0 <= bye_idx < REGULAR_SEASON_WEEKS:
                actual_points[bye_idx] = 0.0
                projected_points[bye_idx] = 0.0

        # Extract position-specific stats with point-in-time logic
        stats = self._extract_stats_for_player(player_data, current_week)

        # Build player object
        player_obj = {
            "id": player_data.id,
            "name": player_data.name,
            "team": player_data.team,
            "position": player_data.position,
            "bye_week": player_data.bye_week,
            "injury_status": player_data.injury_status if player_data.injury_status else "ACTIVE",
            "drafted_by": "",    # Historical data has no league context
            "locked": False,     # Historical data not locked
            "average_draft_position": player_data.average_draft_position,
            "player_rating": round(player_rating, 1),
            "projected_points": [round(p, 1) for p in projected_points],
            "actual_points": [round(p, 1) for p in actual_points],
        }

        # Add position-specific stats
        if player_data.position == 'QB' and 'passing' in stats:
            player_obj['passing'] = stats['passing']
        if player_data.position in ['QB', 'RB'] and 'rushing' in stats:
            player_obj['rushing'] = stats['rushing']
        if player_data.position in ['QB', 'RB', 'WR', 'TE'] and 'receiving' in stats:
            player_obj['receiving'] = stats['receiving']
        if player_data.position == 'K' and 'kicking' in stats:
            player_obj['kicking'] = stats['kicking']
        if player_data.position == 'DST' and 'defense' in stats:
            player_obj['defense'] = stats['defense']

        return player_obj

    def generate_position_json(
        self,
        players: List[PlayerData],
        position: str,
        output_path: Path,
        current_week: int
    ) -> None:
        """
        Generate JSON file for a single position.

        Args:
            players: List of all PlayerData objects
            position: Position to generate (QB, RB, WR, TE, K, DST)
            output_path: Full path to output JSON file
            current_week: Current week for point-in-time logic
        """
        # Filter players by position
        position_players = [p for p in players if p.position == position]

        if not position_players:
            self.logger.warning(f"No players found for position {position} in week {current_week}")
            # Create empty JSON file
            with open(output_path, 'w') as f:
                json.dump([], f, indent=2)
            return

        # Calculate player ratings for this week
        player_ratings = self._calculate_player_ratings(players, current_week)

        # Build JSON objects for each player
        json_objects = []
        for player in position_players:
            rating = player_ratings.get(player.id, 50.0)
            player_obj = self._build_player_json_object(player, current_week, rating)
            json_objects.append(player_obj)

        # Sort by player_rating descending (best players first)
        json_objects.sort(key=lambda x: x.get('player_rating', 0), reverse=True)

        # Write JSON file
        with open(output_path, 'w') as f:
            json.dump(json_objects, f, indent=2)

        self.logger.debug(f"Generated {position} JSON: {len(json_objects)} players ({output_path.name})")


def generate_json_snapshots(
    players: List[PlayerData],
    week_dir: Path,
    current_week: int
) -> None:
    """
    Generate all 6 position-specific JSON files for a week snapshot.

    Args:
        players: List of PlayerData with full season data
        week_dir: Week directory path (e.g., weeks/week_01/)
        current_week: Current week (1-17)
    """
    logger = get_logger()
    exporter = JSONSnapshotExporter()

    logger.info(f"Generating JSON snapshots for week {current_week}")

    # Generate JSON for each position
    for position in FANTASY_POSITIONS:
        json_file = POSITION_JSON_FILES[position]
        output_path = week_dir / json_file
        exporter.generate_position_json(players, position, output_path, current_week)

    logger.debug(f"Generated {len(FANTASY_POSITIONS)} JSON files for week {current_week}")
