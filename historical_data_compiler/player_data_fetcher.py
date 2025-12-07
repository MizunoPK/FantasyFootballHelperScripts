#!/usr/bin/env python3
"""
Player Data Fetcher for Historical Data Compiler

Fetches player data from ESPN Fantasy API for complete historical seasons.
Creates players.csv with actual/projected weekly fantasy points.

Adapted from player-data-fetcher/espn_client.py.

Author: Kai Mizuno
"""

import csv
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from .http_client import BaseHTTPClient
from .constants import (
    ESPN_FANTASY_API_URL,
    ESPN_TEAM_MAPPINGS,
    ESPN_POSITION_MAPPINGS,
    FANTASY_POSITIONS,
    REGULAR_SEASON_WEEKS,
    ESPN_USER_AGENT,
    PLAYERS_FILE,
    PLAYERS_PROJECTED_FILE,
    normalize_team_abbrev,
)

import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.LoggingManager import get_logger


# ESPN API constants
ESPN_PLAYER_LIMIT = 1500  # Max players to fetch


# CSV columns for players.csv
PLAYERS_CSV_COLUMNS = [
    "id", "name", "team", "position", "bye_week", "drafted", "locked",
    "fantasy_points", "average_draft_position", "player_rating", "injury_status",
    "week_1_points", "week_2_points", "week_3_points", "week_4_points",
    "week_5_points", "week_6_points", "week_7_points", "week_8_points",
    "week_9_points", "week_10_points", "week_11_points", "week_12_points",
    "week_13_points", "week_14_points", "week_15_points", "week_16_points",
    "week_17_points"
]


@dataclass
class PlayerData:
    """
    Player data with fantasy projections.

    Attributes:
        id: ESPN player ID
        name: Player full name
        team: Team abbreviation
        position: Position (QB, RB, WR, TE, K, DST)
        bye_week: Team bye week
        fantasy_points: Season total fantasy points
        average_draft_position: ESPN ADP
        player_rating: Normalized positional rank (1-100, 100=best)
        injury_status: Injury status string
        week_points: Dict of week -> actual/smart points
        projected_weeks: Dict of week -> projected points only
    """
    id: str
    name: str
    team: str
    position: str
    bye_week: Optional[int] = None
    drafted: int = 0
    locked: int = 0
    fantasy_points: float = 0.0
    average_draft_position: Optional[float] = None
    player_rating: Optional[float] = None
    injury_status: str = "ACTIVE"
    week_points: Dict[int, float] = field(default_factory=dict)
    projected_weeks: Dict[int, float] = field(default_factory=dict)

    def to_csv_row(self) -> Dict[str, Any]:
        """Convert to CSV row dict."""
        row = {
            "id": self.id,
            "name": self.name,
            "team": self.team,
            "position": self.position,
            "bye_week": self.bye_week if self.bye_week is not None else "",
            "drafted": self.drafted,
            "locked": self.locked,
            "fantasy_points": round(self.fantasy_points, 1),
            "average_draft_position": round(self.average_draft_position, 1) if self.average_draft_position else "",
            "player_rating": round(self.player_rating, 1) if self.player_rating else "",
            "injury_status": self.injury_status,
        }
        # Add weekly points
        for week in range(1, REGULAR_SEASON_WEEKS + 1):
            points = self.week_points.get(week)
            row[f"week_{week}_points"] = round(points, 1) if points is not None else ""
        return row

    def to_projected_csv_row(self) -> Dict[str, Any]:
        """Convert to CSV row dict for players_projected.csv (projection-only values)."""
        row = {
            "id": self.id,
            "name": self.name,
            "team": self.team,
            "position": self.position,
            "bye_week": self.bye_week if self.bye_week is not None else "",
            "drafted": self.drafted,
            "locked": self.locked,
            "fantasy_points": round(self.fantasy_points, 1),
            "average_draft_position": round(self.average_draft_position, 1) if self.average_draft_position else "",
            "player_rating": round(self.player_rating, 1) if self.player_rating else "",
            "injury_status": self.injury_status,
        }
        # Add projected weekly points
        for week in range(1, REGULAR_SEASON_WEEKS + 1):
            points = self.projected_weeks.get(week)
            row[f"week_{week}_points"] = round(points, 1) if points is not None else ""
        return row


class PlayerDataFetcher:
    """
    Fetches player data from ESPN Fantasy API.

    For historical data compilation:
    - Fetches all players with season projections
    - Fetches week-by-week data for each player
    - Extracts actual (statSourceId=0) and projected (statSourceId=1) points
    """

    def __init__(self, http_client: BaseHTTPClient, ppr_id: int = 3):
        """
        Initialize PlayerDataFetcher.

        Args:
            http_client: Shared HTTP client instance
            ppr_id: ESPN scoring format ID (1=Standard, 2=Half-PPR, 3=PPR)
        """
        self.http_client = http_client
        self.ppr_id = ppr_id
        self.logger = get_logger()

    async def fetch_all_players(
        self,
        year: int,
        bye_weeks: Dict[str, int]
    ) -> List[PlayerData]:
        """
        Fetch all players for a season.

        Args:
            year: NFL season year
            bye_weeks: Dict mapping team abbreviation to bye week

        Returns:
            List of PlayerData objects
        """
        self.logger.info(f"Fetching all players for {year} season")

        # Build API URL
        url = ESPN_FANTASY_API_URL.format(year=year)

        # Request params
        params = {
            "view": "kona_player_info",
            "scoringPeriodId": 0  # 0 = all weeks
        }

        # Headers with player filter
        headers = {
            "User-Agent": ESPN_USER_AGENT,
            "X-Fantasy-Filter": f'{{"players":{{"limit":{ESPN_PLAYER_LIMIT},"sortPercOwned":{{"sortPriority":4,"sortAsc":false}}}}}}'
        }

        data = await self.http_client.get(url, headers=headers, params=params)

        # Parse player data
        players = await self._parse_players(data, year, bye_weeks)
        self.logger.info(f"Fetched {len(players)} players for {year} season")

        return players

    async def _parse_players(
        self,
        data: dict,
        year: int,
        bye_weeks: Dict[str, int]
    ) -> List[PlayerData]:
        """
        Parse ESPN API response into PlayerData objects.

        Args:
            data: ESPN API response
            year: NFL season year
            bye_weeks: Dict mapping team to bye week

        Returns:
            List of PlayerData objects
        """
        players_list: List[PlayerData] = []
        raw_players = data.get('players', [])

        self.logger.info(f"Processing {len(raw_players)} raw players from ESPN API")

        # First pass: collect positional rank ranges for normalization
        position_rank_ranges: Dict[str, Dict[str, float]] = {}
        player_positional_ranks: Dict[str, float] = {}

        for player in raw_players:
            player_info = player.get('player', {})
            player_id = str(player_info.get('id', ''))
            if not player_id:
                continue

            position_id = player_info.get('defaultPositionId')
            position = ESPN_POSITION_MAPPINGS.get(position_id, 'UNKNOWN')
            if position == 'UNKNOWN' or position not in FANTASY_POSITIONS:
                continue

            # Extract positional rank from rankings
            positional_rank = self._extract_positional_rank(player_info, position)

            if positional_rank is not None:
                player_positional_ranks[player_id] = positional_rank

                if position not in position_rank_ranges:
                    position_rank_ranges[position] = {'min': positional_rank, 'max': positional_rank}
                else:
                    position_rank_ranges[position]['min'] = min(
                        position_rank_ranges[position]['min'], positional_rank
                    )
                    position_rank_ranges[position]['max'] = max(
                        position_rank_ranges[position]['max'], positional_rank
                    )

        # Second pass: parse all players
        processed = 0
        for player in raw_players:
            try:
                player_data = await self._parse_single_player(
                    player, year, bye_weeks, player_positional_ranks, position_rank_ranges
                )
                if player_data:
                    players_list.append(player_data)
                    processed += 1

                if processed % 100 == 0:
                    self.logger.debug(f"Processed {processed} players")

            except Exception as e:
                self.logger.warning(f"Error parsing player: {e}")
                continue

        return players_list

    def _extract_positional_rank(self, player_info: dict, position: str) -> Optional[float]:
        """
        Extract positional rank from ESPN player info.

        Args:
            player_info: ESPN player dict
            position: Player position

        Returns:
            Positional rank (averageRank) or None
        """
        # Get slot ID for position
        slot_mapping = {
            'QB': 0, 'RB': 2, 'WR': 4, 'TE': 6, 'K': 17, 'DST': 16
        }
        expected_slot_id = slot_mapping.get(position, -1)

        # Try to find rankings in 'rankings' dict
        all_rankings = player_info.get('rankings', {})

        # Try current week's rankings (key '0' is often preseason/overall)
        for key in ['0', '1', '2', '3', '4', '5']:
            if key in all_rankings:
                rankings_ros = all_rankings[key]
                if rankings_ros:
                    for entry in rankings_ros:
                        if (entry.get('rankType') == 'PPR' and
                            entry.get('slotId') == expected_slot_id and
                            'averageRank' in entry):
                            return entry['averageRank']

        # Fallback: use draftRanksByRankType
        draft_ranks = player_info.get('draftRanksByRankType', {})
        ppr_rank_data = draft_ranks.get('PPR', {})
        if ppr_rank_data and 'rank' in ppr_rank_data:
            return float(ppr_rank_data['rank'])

        return None

    async def _parse_single_player(
        self,
        player: dict,
        year: int,
        bye_weeks: Dict[str, int],
        player_positional_ranks: Dict[str, float],
        position_rank_ranges: Dict[str, Dict[str, float]]
    ) -> Optional[PlayerData]:
        """
        Parse a single player from ESPN API response.

        Args:
            player: Raw player dict from ESPN
            year: NFL season year
            bye_weeks: Dict mapping team to bye week
            player_positional_ranks: Dict of player_id -> positional rank
            position_rank_ranges: Dict of position -> {min, max} ranks

        Returns:
            PlayerData or None if player should be skipped
        """
        player_info = player.get('player', {})

        # Extract basic info
        player_id = str(player_info.get('id', ''))
        if not player_id:
            return None

        # Name
        name_parts = []
        if player_info.get('firstName'):
            name_parts.append(player_info['firstName'])
        if player_info.get('lastName'):
            name_parts.append(player_info['lastName'])
        name = ' '.join(name_parts) if name_parts else 'Unknown'

        # Team
        pro_team_id = player_info.get('proTeamId')
        team = ESPN_TEAM_MAPPINGS.get(pro_team_id, 'UNK')
        if team == 'UNK':
            return None

        # Position
        position_id = player_info.get('defaultPositionId')
        position = ESPN_POSITION_MAPPINGS.get(position_id, 'UNKNOWN')
        if position == 'UNKNOWN' or position not in FANTASY_POSITIONS:
            return None

        # Bye week
        bye_week = bye_weeks.get(team)

        # ADP
        adp = None
        ownership = player_info.get('ownership', {})
        if ownership and 'averageDraftPosition' in ownership:
            adp = ownership['averageDraftPosition']

        # Player rating (normalized 1-100)
        player_rating = None
        positional_rank = player_positional_ranks.get(player_id)
        if positional_rank is not None and position in position_rank_ranges:
            ranges = position_rank_ranges[position]
            if ranges['max'] > ranges['min']:
                # Normalize: lower rank = better = higher rating
                player_rating = 100 - ((positional_rank - ranges['min']) /
                                       (ranges['max'] - ranges['min']) * 99)
                player_rating = max(1.0, min(100.0, player_rating))

        # Injury status
        injury_status = player_info.get('injuryStatus', 'ACTIVE')

        # Extract weekly points
        week_points, projected_weeks = await self._extract_weekly_points(
            player_info, year, position
        )

        # Calculate total fantasy points (sum of smart week values)
        fantasy_points = sum(week_points.values())

        return PlayerData(
            id=player_id,
            name=name,
            team=team,
            position=position,
            bye_week=bye_week,
            fantasy_points=fantasy_points,
            average_draft_position=adp,
            player_rating=player_rating,
            injury_status=injury_status,
            week_points=week_points,
            projected_weeks=projected_weeks
        )

    async def _extract_weekly_points(
        self,
        player_info: dict,
        year: int,
        position: str
    ) -> tuple:
        """
        Extract weekly fantasy points from player stats.

        For historical data, uses:
        - statSourceId=0 (actual) when available
        - statSourceId=1 (projected) as fallback

        Args:
            player_info: ESPN player dict with 'stats' array
            year: NFL season year
            position: Player position

        Returns:
            Tuple of (week_points, projected_weeks) dicts
        """
        week_points: Dict[int, float] = {}
        projected_weeks: Dict[int, float] = {}

        stats = player_info.get('stats', [])
        if not stats:
            return week_points, projected_weeks

        # Group stats by week and source
        for week in range(1, REGULAR_SEASON_WEEKS + 1):
            actual_points = None
            projected_points = None

            for stat in stats:
                if not isinstance(stat, dict):
                    continue

                season_id = stat.get('seasonId')
                scoring_period = stat.get('scoringPeriodId')

                if season_id == year and scoring_period == week:
                    stat_source = stat.get('statSourceId')
                    applied_total = stat.get('appliedTotal')

                    if applied_total is not None:
                        try:
                            points = float(applied_total)
                            if not math.isnan(points):
                                if stat_source == 0:  # Actual
                                    actual_points = points
                                elif stat_source == 1:  # Projected
                                    projected_points = points
                        except (ValueError, TypeError):
                            continue

            # Smart value: actual if available, else projected
            if actual_points is not None:
                # DST can have negative points
                if position == 'DST' or actual_points > 0:
                    week_points[week] = actual_points
            elif projected_points is not None:
                if position == 'DST' or projected_points > 0:
                    week_points[week] = projected_points

            # Projected value (always projection)
            if projected_points is not None:
                if position == 'DST' or projected_points > 0:
                    projected_weeks[week] = projected_points

        return week_points, projected_weeks

    def write_players_csv(
        self,
        players: List[PlayerData],
        output_path: Path
    ) -> None:
        """
        Write players.csv (smart values - actual for past, projected for future).

        Args:
            players: List of PlayerData objects
            output_path: Path to output CSV file
        """
        self.logger.info(f"Writing players to {output_path}")

        # Sort by fantasy points (descending)
        players_sorted = sorted(players, key=lambda p: p.fantasy_points, reverse=True)

        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=PLAYERS_CSV_COLUMNS)
            writer.writeheader()
            for player in players_sorted:
                writer.writerow(player.to_csv_row())

        self.logger.info(f"Wrote {len(players)} players to {output_path}")

    def write_players_projected_csv(
        self,
        players: List[PlayerData],
        output_path: Path
    ) -> None:
        """
        Write players_projected.csv (projection-only values for all weeks).

        Args:
            players: List of PlayerData objects
            output_path: Path to output CSV file
        """
        self.logger.info(f"Writing projected players to {output_path}")

        # Sort by fantasy points (descending)
        players_sorted = sorted(players, key=lambda p: p.fantasy_points, reverse=True)

        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=PLAYERS_CSV_COLUMNS)
            writer.writeheader()
            for player in players_sorted:
                writer.writerow(player.to_projected_csv_row())

        self.logger.info(f"Wrote {len(players)} players to {output_path}")


async def fetch_player_data(
    year: int,
    http_client: BaseHTTPClient,
    bye_weeks: Dict[str, int]
) -> List[PlayerData]:
    """
    Fetch player data from ESPN Fantasy API.

    Note: This function only fetches data. Player CSV files are written
    by the weekly_snapshot_generator which creates point-in-time snapshots
    in the weeks/week_NN/ folders.

    Args:
        year: NFL season year
        http_client: HTTP client instance
        bye_weeks: Dict mapping team to bye week

    Returns:
        List of PlayerData for use by other modules
    """
    fetcher = PlayerDataFetcher(http_client)
    players = await fetcher.fetch_all_players(year, bye_weeks)
    return players
