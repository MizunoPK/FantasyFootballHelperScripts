#!/usr/bin/env python3
"""
Data Export Module for NFL Fantasy Football Data

This module handles position-based JSON export and team data export
with async file I/O for better performance.

Author: Kai Mizuno
"""

import asyncio
import math
from pathlib import Path
from typing import Any, List, Dict, Optional
import json

import aiofiles

from player_data_fetcher.config import data_root
from player_data_fetcher.player_data_models import ProjectionData, ESPNPlayerData, PlayerDataValidationError
from player_data_fetcher.espn_attribution import (
    normalize_our_team_attribution,
    reconcile_espn_attribution_or_raise,
)
from player_data_fetcher.espn_league_snapshot_models import LeagueSnapshot

from utils.FantasyPlayer import FantasyPlayer
from utils.TeamData import save_team_weekly_data
from utils.data_file_manager import DataFileManager
from utils.LoggingManager import get_logger


def zero_bye_week_points(
    projected_points: List[float],
    actual_points: List[float],
    bye_week: Optional[int],
) -> None:
    """Zero both weekly point arrays at a valid fantasy bye week.

    The single owner of the bye-week invariant (Spec: D3 context.md TD1).
    Two callers: DataExporter._zero_bye_week_points on the live fetch path,
    and repair_bye_week_points.py's one-time repair of the tracked pool
    (Spec: D3.2 UD6).

    Args:
        projected_points: The 17-slot projected-points array to update.
        actual_points: The 17-slot actual-points array to update.
        bye_week: One-based fantasy bye week, if known.
    """
    if bye_week:
        bye_idx = bye_week - 1
        if 0 <= bye_idx < 17:
            actual_points[bye_idx] = 0.0
            projected_points[bye_idx] = 0.0


class DataExporter:
    """Handles exporting projection data to position JSON and team CSV formats with async I/O"""


    def __init__(
        self,
        output_dir: str,
        current_nfl_week: int = 17,
        position_json_output: Optional[str] = None,
        team_data_folder: Optional[str] = None,
        espn_settings: Optional[Any] = None
    ):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.current_nfl_week = current_nfl_week
        # T91: resolve the path defaults HERE, at construction time -- not in the
        # signature. A def-time default is baked into __defaults__ once at import,
        # so a later PLAYER_DATA_DIR (or a _DATA_ROOT monkeypatch) would be a
        # silent no-op. See spec.md D2 / AC4.
        _root = data_root()
        self.position_json_output = (
            position_json_output if position_json_output is not None
            else str(_root / 'player_data')
        )
        self.team_data_folder = (
            team_data_folder if team_data_folder is not None
            else str(_root / 'team_data')
        )
        self.logger = get_logger()

        self.file_manager = DataFileManager(str(self.output_dir), None)

        self.team_rankings = {}
        self.current_week_schedule = {}
        self.position_defense_rankings = {}
        self.team_weekly_data = {}

        self.espn_settings = espn_settings
        self._espn_attribution: Optional[Dict[str, str]] = None

    async def load_espn_attribution(self, players: List[ESPNPlayerData]) -> None:
        """Fetch + reconcile ESPN draft attribution when the ESPN supplier is selected.

        The ESPN league snapshot is the SOLE ownership supplier since D17.6's
        contraction. This method calls D17.3's authenticated ESPNClient method, then
        `reconcile_espn_attribution` (D17.4), then normalizes our own team's
        picks to `FANTASY_TEAM_NAME` (`_normalize_our_team_attribution`, D17.5
        D3/D6), and only then stores the complete map on
        `self._espn_attribution`. Must be awaited before any
        `get_fantasy_players` call this run can reach (spec.md D2 ordering
        requirement) -- the caller (player_data_fetcher_main.py) is responsible
        for that ordering; this method itself performs no scheduling.

        Nothing is stored, and no `drafted_by` is mutated, unless every step
        above succeeds (ticket TD2 -- atomic, fail-closed).

        Args:
            players: The complete local ProjectionData player pool for this
                run (the same pool get_fantasy_players will later convert).

        Raises:
            ESPNAPIError (or subclass): propagated unchanged from D17.3's
                client on transport/auth/validation failure -- never caught or
                re-wrapped here (spec.md D2/D3).
            PlayerDataValidationError: when `reconcile_espn_attribution` returns
                None (a completed playerId has no local match), naming every
                offending playerId (spec.md D3); when the configured
                `ESPN_TEAM_ID` is absent from `snapshot.teams[]`; or when another
                team's name collides with `FANTASY_TEAM_NAME` (D17.5 D6). Never a
                silent fallback -- there is no second supplier (D17.6).
        """
        if self.espn_settings is None:
            raise PlayerDataValidationError(
                "load_espn_attribution requires espn_settings; DataExporter was "
                "constructed without an espn_settings object."
            )

        from league_helper.util.ConfigManager import ConfigManager, ConfigKeys
        from player_data_fetcher.espn_client import ESPNClient

        config_manager = ConfigManager(data_root())
        league_id = config_manager.get_parameter(ConfigKeys.ESPN_LEAGUE_ID)
        our_team_id = config_manager.get_parameter(ConfigKeys.ESPN_TEAM_ID)

        espn_client = ESPNClient(self.espn_settings)
        try:
            async with espn_client.session():
                snapshot = await espn_client.get_league_snapshot(league_id, self.espn_settings.season)
        finally:
            await espn_client.close()

        self._espn_attribution = reconcile_espn_attribution_or_raise(
            snapshot, players, our_team_id, self.logger
        )

    def _normalize_our_team_attribution(
        self,
        snapshot: LeagueSnapshot,
        attribution: Dict[str, str],
        our_team_id: int,
    ) -> Dict[str, str]:
        """Rewrite our configured team's picks to the in-app ownership token.

        D17.5 D3/D6. `reconcile_espn_attribution` returns raw ESPN league names
        and stays pure/unchanged, but every downstream ownership reader compares
        `drafted_by` against `league_helper.constants.FANTASY_TEAM_NAME` by string
        equality (`FantasyPlayer.is_rostered`, utils/FantasyPlayer.py:367).
        Normalizing here -- at the seam, keyed on the stable `teamId` rather than
        on a name -- makes `drafted_by` carry the exact token those readers
        compare against, so an ESPN-side team rename cannot break our own identity.

        Args:
            snapshot: The validated ESPN league snapshot `attribution` came from.
            attribution: `reconcile_espn_attribution`'s complete
                `local playerId -> raw ESPN team name` map.
            our_team_id: The configured `ESPN_TEAM_ID`.

        Returns:
            A new map identical to `attribution` except that every pick belonging
            to `our_team_id` carries `FANTASY_TEAM_NAME`.

        Raises:
            PlayerDataValidationError: when `our_team_id` is absent from
                `snapshot.teams[]`, or when any OTHER team carries a name equal to
                `FANTASY_TEAM_NAME` (compared case-insensitively and
                whitespace-stripped). Both are fail-closed halts raised BEFORE the
                caller stores anything, so no `drafted_by` is ever mutated.
                Messages name team ids only -- never a credential value.
        """
        return normalize_our_team_attribution(
            snapshot, attribution, our_team_id, self.logger
        )

    def set_team_rankings(self, team_rankings: dict):
        """Set team rankings data from ESPN client for team exports"""
        self.team_rankings = team_rankings
        self.logger.info(f"Team rankings set for {len(team_rankings)} teams")

    def set_current_week_schedule(self, schedule: dict):
        """Set current week schedule data from ESPN client for team exports"""
        self.current_week_schedule = schedule
        self.logger.info(f"Current week schedule set for {len(schedule)} teams")

    def set_position_defense_rankings(self, rankings: dict):
        """Set position-specific defense rankings from ESPN client"""
        self.position_defense_rankings = rankings
        self.logger.info(f"Position defense rankings set for {len(rankings)} teams")

    def set_team_weekly_data(self, data: dict):
        """Set per-team, per-week data for new team_data format export"""
        self.team_weekly_data = data
        self.logger.info(f"Team weekly data set for {len(data)} teams")


    def _espn_player_to_fantasy_player(self, player_data: ESPNPlayerData) -> FantasyPlayer:
        """Convert ESPNPlayerData to FantasyPlayer object"""

        drafted_by_value = player_data.drafted_by

        locked_value = 0

        projected_points = [
            player_data.week_1_points, player_data.week_2_points, player_data.week_3_points,
            player_data.week_4_points, player_data.week_5_points, player_data.week_6_points,
            player_data.week_7_points, player_data.week_8_points, player_data.week_9_points,
            player_data.week_10_points, player_data.week_11_points, player_data.week_12_points,
            player_data.week_13_points, player_data.week_14_points, player_data.week_15_points,
            player_data.week_16_points, player_data.week_17_points
        ]
        actual_points = projected_points.copy()

        return FantasyPlayer(
            id=player_data.id,
            name=player_data.name,
            team=player_data.team,
            position=player_data.position,
            bye_week=player_data.bye_week,
            drafted_by=drafted_by_value,
            locked=locked_value,
            fantasy_points=player_data.fantasy_points,
            average_draft_position=player_data.average_draft_position,
            player_rating=player_data.player_rating,
            injury_status=player_data.injury_status,
            projected_points=projected_points,
            actual_points=actual_points
        )
    
    def get_fantasy_players(self, data: ProjectionData) -> List[FantasyPlayer]:
        """Convert ProjectionData to list of FantasyPlayer objects"""
        fantasy_players = [self._espn_player_to_fantasy_player(player) for player in data.players]

        if self._espn_attribution is None:
            raise PlayerDataValidationError(
                "get_fantasy_players reached but ESPN attribution is not "
                "loaded; load_espn_attribution must be awaited first."
            )
        for player in fantasy_players:
            team_name = self._espn_attribution.get(str(player.id))
            if team_name is not None:
                player.drafted_by = team_name

        return fantasy_players


    async def export_position_json_files(self, data: ProjectionData) -> List[str]:
        """
        Export position-based JSON files concurrently.

        Creates 6 JSON files (one per position: QB, RB, WR, TE, K, DST)
        in position_json_output folder.

        Spec: specs.md lines 14-19, USER_DECISIONS_SUMMARY.md Decision 1

        Args:
            data: ProjectionData containing player data

        Returns:
            List of file paths created
        """
        output_path = Path(self.position_json_output)
        output_path.mkdir(parents=True, exist_ok=True)

        position_file_manager = DataFileManager(str(output_path), None)

        positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']
        tasks = []
        for position in positions:
            tasks.append(self._export_single_position_json(data, position, position_file_manager))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        file_paths = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                position = positions[i]
                self.logger.error(f"Failed to export {position} data: {result}", exc_info=result)
            else:
                file_paths.append(result)

        self.logger.info(f"Position JSON export complete: {len(file_paths)}/6 files created")
        return file_paths

    async def _export_single_position_json(self, data: ProjectionData, position: str, file_manager: DataFileManager) -> str:
        """
        Export JSON file for a single position.

        Spec: specs.md lines 14-19, Complete Data Structures section

        Args:
            data: ProjectionData containing all player data
            position: Position code (QB, RB, WR, TE, K, or DST)
            file_manager: DataFileManager for position JSON output folder

        Returns:
            File path of created JSON file
        """
        fantasy_players = self.get_fantasy_players(data)

        espn_player_map = {p.id: p for p in data.players}

        position_players = [p for p in fantasy_players if p.position == position]

        players_json = []
        for player in position_players:
            espn_data = espn_player_map.get(str(player.id))
            player_json = self._prepare_position_json_data(player, espn_data, position)
            players_json.append(player_json)

        root_key = f"{position.lower()}_data"
        output_data = {root_key: players_json}

        file_path = Path(self.position_json_output) / f'{position.lower()}_data.json'

        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)

            async with aiofiles.open(str(file_path), mode='w', encoding='utf-8') as f:
                json_string = json.dumps(output_data, indent=2, ensure_ascii=False)
                await f.write(json_string)

            self.logger.info(f"Exported {len(players_json)} {position} players to {file_path}")
            return str(file_path)

        except PermissionError as e:
            self.logger.error(f"Permission denied writing to {file_path}: {e}")
            raise
        except OSError as e:
            self.logger.error(f"OS error writing to {file_path}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error exporting position JSON: {e}")
            raise

    def _prepare_position_json_data(self, player: FantasyPlayer, espn_data: Optional[ESPNPlayerData], position: str) -> Dict:
        """
        Transform player data to position-specific JSON structure.

        Both weekly arrays are zeroed at the player's bye week before
        serialization (Spec: D3 context.md TD1), so this method -- not the array
        builders -- owns the bye-week invariant on what reaches disk.

        Spec: specs.md Complete Data Structures section, USER_DECISIONS_SUMMARY.md

        Args:
            player: FantasyPlayer object (has drafted state applied)
            espn_data: ESPNPlayerData object (has raw ESPN data)
            position: Position code (QB, RB, WR, TE, K, DST)

        Returns:
            Dictionary with player data in position-specific JSON format
        """
        projected_points = self._get_projected_points_array(espn_data)
        actual_points = self._get_actual_points_array(espn_data)
        self._zero_bye_week_points(projected_points, actual_points, player.bye_week)

        json_data = {
            "id": player.id,
            "name": player.name,
            "team": player.team,
            "position": player.position,
            "bye_week": player.bye_week,
            "injury_status": player.injury_status,
            "drafted_by": self._get_drafted_by(player),
            "locked": bool(player.locked),
            "average_draft_position": player.average_draft_position,
            "player_rating": player.player_rating,
            "projected_points": projected_points,
            "actual_points": actual_points
        }

        if position == "QB":
            json_data["passing"] = self._extract_passing_stats(espn_data)
            json_data["rushing"] = self._extract_rushing_stats(espn_data)
            json_data["receiving"] = self._extract_receiving_stats(espn_data)
            json_data["misc"] = self._extract_misc_stats(espn_data, include_return_stats=False)
        elif position == "RB":
            json_data["rushing"] = self._extract_rushing_stats(espn_data)
            json_data["receiving"] = self._extract_receiving_stats(espn_data)
            json_data["misc"] = self._extract_misc_stats(espn_data, include_return_stats=False)
        elif position == "WR":
            json_data["receiving"] = self._extract_receiving_stats(espn_data)
            json_data["rushing"] = self._extract_rushing_stats(espn_data)
            json_data["misc"] = self._extract_misc_stats(espn_data, include_return_stats=False)
        elif position == "TE":
            json_data["receiving"] = self._extract_receiving_stats(espn_data)
            json_data["misc"] = self._extract_misc_stats(espn_data, include_return_stats=False)
        elif position == "K":
            json_data["extra_points"] = self._extract_kicking_stats(espn_data)["extra_points"]
            json_data["field_goals"] = self._extract_kicking_stats(espn_data)["field_goals"]
        elif position == "DST":
            json_data["defense"] = self._extract_defense_stats(espn_data)

        return json_data

    def _zero_bye_week_points(
        self,
        projected_points: List[float],
        actual_points: List[float],
        bye_week: Optional[int],
    ) -> None:
        """Zero both weekly point arrays at a valid fantasy bye week.

        Delegates to the module-level zero_bye_week_points, which owns the
        invariant (Spec: D3 context.md TD1, D3.2 UD6). Retained so the record
        builder keeps calling the method rather than the module function.

        Args:
            projected_points: The 17-slot projected-points array to update.
            actual_points: The 17-slot actual-points array to update.
            bye_week: One-based fantasy bye week, if known.
        """
        zero_bye_week_points(projected_points, actual_points, bye_week)

    def _get_drafted_by(self, player: FantasyPlayer) -> str:
        """
        Get drafted_by value from player (team name or empty string).

        Player already has its drafted_by value populated by `get_fantasy_players`
        from the reconciled ESPN league snapshot (the sole ownership supplier since
        D17.6). This accessor reads the field only and maintains the abstraction
        layer for future flexibility.

        Args:
            player: FantasyPlayer with drafted_by field populated

        Returns:
            Team name string or empty string for free agents
        """
        return player.drafted_by

    def _get_projected_points_array(self, espn_data: Optional[ESPNPlayerData]) -> List[float]:
        """
        Get projected points array from ESPN pre-game projections (17 elements, Spec: Decision 2).

        Extracts projected points from statSourceId=1 (pre-game projections).
        This should be DIFFERENT from actual_points (which uses statSourceId=0).

        Args:
            espn_data: ESPNPlayerData object with raw_stats

        Returns:
            List of 17 projected point values (pre-game ESPN projections)
        """
        if espn_data is None or not espn_data.raw_stats:
            return [0.0] * 17

        season = self._espn_season()
        projected_points = []
        for week in range(1, 18):
            projected = self._select_week_stat(
                espn_data.raw_stats, week, stat_source_id=1, season=season
            )
            projected_points.append(projected if projected else 0.0)
        return projected_points

    def _espn_season(self) -> Optional[int]:
        """Return the season this export is for, or None when it is not known.

        The live fetcher constructs this exporter with `espn_settings`, so the
        season is always known on that path. `historical_data_compiler` does not
        pass one; there the value is None and season filtering is skipped, which
        keeps that producer's output byte-identical to its pre-fix behaviour. Its
        raw_stats come from a single-season fetch, so it has no cross-season
        collision to guard against.

        Returns:
            The configured ESPN season as an int, or None when unavailable.
        """
        season = getattr(self.espn_settings, 'season', None)
        try:
            return int(season) if season is not None else None
        except (TypeError, ValueError):
            return None

    def _select_week_stat(
        self,
        raw_stats: List[Dict],
        week: int,
        stat_source_id: int,
        season: Optional[int]
    ) -> Optional[float]:
        """Select one week's appliedTotal, scoped to the requested SEASON.

        ESPN returns entries for MULTIPLE seasons under the same
        `scoringPeriodId`. Matching on (`scoringPeriodId`, `statSourceId`) alone
        and taking the first hit therefore reads whichever season happens to sort
        first. Measured live on 2026-08-18: ARI week 8 carried
        {2025: 24, 2026: 20} entries, and across the corpus the first match was a
        PRIOR-season entry for 2,445 zeroed player-weeks. Because a team's prior
        bye week has appliedTotal 0.0, that read blanked the ENTIRE roster for the
        week that was the team's bye in the PREVIOUS season -- 24 of 32 teams,
        2,021 recoverable player-weeks, e.g. Jahmyr Gibbs week 8 stored as 0.0
        against a true 2026 projection of 21.53.

        Mirrors `ESPNClient._extract_raw_espn_week_points`, which already filters
        on `seasonId == self.settings.season`; this is that same guard applied to
        the exporter's own extraction rather than a second convention.

        A malformed, non-numeric or NaN appliedTotal is skipped rather than
        raising. Scanning continues past a zero so a non-zero sibling entry for
        the same season wins, which is the analogue of the sibling's
        "first positive among valid entries" selection.

        Args:
            raw_stats: The player's raw ESPN stat entries.
            week: One-based scoring period to select.
            stat_source_id: 1 for ESPN projections, 0 for actual results.
            season: Season to scope to; None skips season filtering entirely.

        Returns:
            The selected appliedTotal as a float, or None when no entry matches.
        """
        selected = None
        for stat in raw_stats:
            if not isinstance(stat, dict):
                continue
            if stat.get('scoringPeriodId') != week:
                continue
            if stat.get('statSourceId') != stat_source_id:
                continue
            if season is not None and stat.get('seasonId') != season:
                continue

            value = stat.get('appliedTotal')
            if value is None:
                continue
            try:
                value = float(value)
            except (TypeError, ValueError):
                continue
            if math.isnan(value):
                continue

            selected = value
            if selected:
                break
        return selected

    def _get_actual_points_array(self, espn_data: Optional[ESPNPlayerData]) -> List[float]:
        """
        Get actual points array from ESPN post-game results (17 elements, Spec: Decision 5,8,9).

        Extracts actual points from statSourceId=0 (post-game results).
        This should be DIFFERENT from projected_points (which uses statSourceId=1).

        IMPORTANT: Only uses statSourceId=0 data for weeks <= current_nfl_week.
        ESPN pre-populates statSourceId=0 with projection data for future weeks,
        so we filter to only completed weeks to avoid showing "actual" data for
        games that haven't been played yet.

        Args:
            espn_data: ESPNPlayerData object with raw_stats

        Returns:
            List of 17 actual point values (what actually happened in games)
        """
        if espn_data is None or not espn_data.raw_stats:
            return [0.0] * 17

        season = self._espn_season()
        actual_points = []
        for week in range(1, 18):
            actual = None
            if week < self.current_nfl_week:
                actual = self._select_week_stat(
                    espn_data.raw_stats, week, stat_source_id=0, season=season
                )
            actual_points.append(actual if actual else 0.0)
        return actual_points

    def _extract_stat_value(self, raw_stats: List[Dict], week: int, stat_id: str) -> float:
        """
        Extract a single stat value from raw_stats array for a specific week,
        scoped to the requested SEASON.

        Pattern from compile_historical_data.py:
        - Find stat entry with scoringPeriodId == week AND statSourceId == 0
        - Extract from the entry's stats dict using stat_id as a string key
        - Return 0.0 if not found

        IMPORTANT: Only extracts stats for weeks <= current_nfl_week to avoid
        showing "actual" stats for games that haven't been played yet.

        IMPORTANT: ESPN returns entries for MULTIPLE seasons under the same
        `scoringPeriodId`, so matching on (`scoringPeriodId`, `statSourceId`)
        alone reads whichever season happens to sort first. That made a 2026
        preseason pull emit PRIOR-season box scores -- receptions, rushing
        yards, sacks, field goals -- for games that had not been played, while
        the season-scoped `actual_points` array beside them was correctly all
        zeroes. This is the same `seasonId` guard `_select_week_stat` already
        applies, extended to the detail-stat path it was missed on; see that
        method's docstring for the measured evidence.

        Scanning continues past a zero or a missing key so a non-zero sibling
        entry for the same season wins, mirroring `_select_week_stat`'s
        "first positive among valid entries" selection.

        Args:
            raw_stats: List of stat dictionaries from ESPN API
            week: Week number (1-17)
            stat_id: ESPN stat ID as string (e.g., '0', '1', '3')

        Returns:
            Stat value as float, or 0.0 if not found
        """
        if week >= self.current_nfl_week:
            return 0.0

        season = self._espn_season()
        for stat in raw_stats:
            if not isinstance(stat, dict):
                continue
            if stat.get('scoringPeriodId') != week:
                continue
            if stat.get('statSourceId') != 0:
                continue
            if season is not None and stat.get('seasonId') != season:
                continue

            stats_dict = stat.get('stats')
            if not isinstance(stats_dict, dict):
                continue
            value = stats_dict.get(stat_id)
            if value is None:
                continue
            try:
                value = float(value)
            except (TypeError, ValueError):
                continue
            if value != value:  # NaN
                continue
            if value:
                return value
        return 0.0

    def _extract_combined_stat(self, raw_stats: List[Dict], week: int, stat_ids: List[str]) -> float:
        """
        Sum multiple stat IDs for a specific week.

        Used for combined stats like return yards (stat_114 + stat_115) or
        two-point conversions (multiple stat IDs).

        Args:
            raw_stats: List of stat dictionaries from ESPN API
            week: Week number (1-17)
            stat_ids: List of ESPN stat IDs to sum (as strings)

        Returns:
            Sum of all stat values as float
        """
        total = 0.0
        for stat_id in stat_ids:
            total += self._extract_stat_value(raw_stats, week, stat_id)
        return total

    def _extract_passing_stats(self, espn_data: Optional[ESPNPlayerData]) -> Dict:
        """Extract passing stats (Spec: specs.md lines 351-358)."""
        if espn_data is None or not espn_data.raw_stats:
            return {
                "completions": [0.0] * 17,
                "attempts": [0.0] * 17,
                "pass_yds": [0.0] * 17,
                "pass_tds": [0.0] * 17,
                "interceptions": [0.0] * 17,
                "sacks": [0.0] * 17
            }

        return {
            "completions": [self._extract_stat_value(espn_data.raw_stats, week, '1') for week in range(1, 18)],
            "attempts": [self._extract_stat_value(espn_data.raw_stats, week, '0') for week in range(1, 18)],
            "pass_yds": [self._extract_stat_value(espn_data.raw_stats, week, '3') for week in range(1, 18)],
            "pass_tds": [self._extract_stat_value(espn_data.raw_stats, week, '4') for week in range(1, 18)],
            "interceptions": [self._extract_stat_value(espn_data.raw_stats, week, '20') for week in range(1, 18)],
            "sacks": [self._extract_stat_value(espn_data.raw_stats, week, '64') for week in range(1, 18)]
        }

    def _extract_rushing_stats(self, espn_data: Optional[ESPNPlayerData]) -> Dict:
        """Extract rushing stats (Spec: specs.md lines 359-363)."""
        if espn_data is None or not espn_data.raw_stats:
            return {
                "attempts": [0.0] * 17,
                "rush_yds": [0.0] * 17,
                "rush_tds": [0.0] * 17
            }

        return {
            "attempts": [self._extract_stat_value(espn_data.raw_stats, week, '23') for week in range(1, 18)],
            "rush_yds": [self._extract_stat_value(espn_data.raw_stats, week, '24') for week in range(1, 18)],
            "rush_tds": [self._extract_stat_value(espn_data.raw_stats, week, '25') for week in range(1, 18)]
        }

    def _extract_receiving_stats(self, espn_data: Optional[ESPNPlayerData]) -> Dict:
        """Extract receiving stats (Spec: specs.md lines 364-369, Decision 3)."""
        if espn_data is None or not espn_data.raw_stats:
            return {
                "targets": [0.0] * 17,
                "receiving_yds": [0.0] * 17,
                "receiving_tds": [0.0] * 17,
                "receptions": [0.0] * 17
            }

        return {
            "targets": [self._extract_stat_value(espn_data.raw_stats, week, '58') for week in range(1, 18)],
            "receiving_yds": [self._extract_stat_value(espn_data.raw_stats, week, '42') for week in range(1, 18)],
            "receiving_tds": [self._extract_stat_value(espn_data.raw_stats, week, '43') for week in range(1, 18)],
            "receptions": [self._extract_stat_value(espn_data.raw_stats, week, '53') for week in range(1, 18)]
        }

    def _extract_misc_stats(self, espn_data: Optional[ESPNPlayerData], include_return_stats: bool = False) -> Dict:
        """
        Extract misc stats (Spec: specs.md lines 370-373, Decision 6).

        Args:
            espn_data: ESPNPlayerData object
            include_return_stats: If True, include ret_yds and ret_tds (DST only)

        Returns:
            Dictionary with misc stats
        """
        if espn_data is None or not espn_data.raw_stats:
            misc_stats = {"fumbles": [0.0] * 17}
            if include_return_stats:
                misc_stats["ret_yds"] = [0.0] * 17
                misc_stats["ret_tds"] = [0.0] * 17
            return misc_stats

        misc_stats = {
            "fumbles": [self._extract_stat_value(espn_data.raw_stats, week, '68') for week in range(1, 18)]
        }

        if include_return_stats:
            misc_stats["ret_yds"] = [self._extract_combined_stat(espn_data.raw_stats, week, ['114', '115']) for week in range(1, 18)]
            misc_stats["ret_tds"] = [self._extract_combined_stat(espn_data.raw_stats, week, ['101', '102']) for week in range(1, 18)]

        return misc_stats

    def _extract_kicking_stats(self, espn_data: Optional[ESPNPlayerData]) -> Dict:
        """Extract kicking stats (Spec: specs.md lines 430-437, Decision 7)."""
        if espn_data is None or not espn_data.raw_stats:
            return {
                "extra_points": {
                    "made": [0.0] * 17,
                    "missed": [0.0] * 17
                },
                "field_goals": {
                    "made": [0.0] * 17,
                    "missed": [0.0] * 17
                }
            }

        return {
            "extra_points": {
                "made": [self._extract_stat_value(espn_data.raw_stats, week, '86') for week in range(1, 18)],
                "missed": [self._extract_stat_value(espn_data.raw_stats, week, '88') for week in range(1, 18)]
            },
            "field_goals": {
                "made": [self._extract_stat_value(espn_data.raw_stats, week, '83') for week in range(1, 18)],
                "missed": [self._extract_stat_value(espn_data.raw_stats, week, '85') for week in range(1, 18)]
            }
        }

    def _extract_defense_stats(self, espn_data: Optional[ESPNPlayerData]) -> Dict:
        """Extract defense stats (Spec: specs.md lines 461-472)."""
        if espn_data is None or not espn_data.raw_stats:
            return {
                "yds_g": [0.0] * 17,
                "pts_g": [0.0] * 17,
                "def_td": [0.0] * 17,
                "sacks": [0.0] * 17,
                "safety": [0.0] * 17,
                "interceptions": [0.0] * 17,
                "forced_fumble": [0.0] * 17,
                "fumbles_recovered": [0.0] * 17,
                "ret_yds": [0.0] * 17,
                "ret_tds": [0.0] * 17
            }

        return {
            "yds_g": [self._extract_stat_value(espn_data.raw_stats, week, '127') for week in range(1, 18)],
            "pts_g": [self._extract_stat_value(espn_data.raw_stats, week, '120') for week in range(1, 18)],
            "def_td": [self._extract_stat_value(espn_data.raw_stats, week, '94') for week in range(1, 18)],
            "sacks": [self._extract_stat_value(espn_data.raw_stats, week, '99') for week in range(1, 18)],
            "safety": [self._extract_stat_value(espn_data.raw_stats, week, '98') for week in range(1, 18)],
            "interceptions": [self._extract_stat_value(espn_data.raw_stats, week, '95') for week in range(1, 18)],
            "forced_fumble": [self._extract_stat_value(espn_data.raw_stats, week, '106') for week in range(1, 18)],
            "fumbles_recovered": [self._extract_stat_value(espn_data.raw_stats, week, '96') for week in range(1, 18)],
            "ret_yds": [self._extract_combined_stat(espn_data.raw_stats, week, ['114', '115']) for week in range(1, 18)],
            "ret_tds": [self._extract_combined_stat(espn_data.raw_stats, week, ['101', '102']) for week in range(1, 18)]
        }


    async def export_teams_to_data(self, data: ProjectionData) -> str:
        """
        Export team data to shared data directory for consumption by other modules.

        Creates team_data folder with individual CSV files for each NFL team.

        Args:
            data: ProjectionData containing player information

        Returns:
            str: Path to the team_data folder
        """
        try:
            shared_team_data_folder = Path(__file__).parent / self.team_data_folder

            if not hasattr(self, 'team_weekly_data') or not self.team_weekly_data:
                self.logger.warning("No team weekly data available for export")
                return ""

            save_team_weekly_data(str(shared_team_data_folder), self.team_weekly_data)

            self.logger.info(f"Exported team data for {len(self.team_weekly_data)} teams to: {shared_team_data_folder}")
            return str(shared_team_data_folder)

        except Exception as e:
            self.logger.error(f"Error exporting team data to shared folder: {e}")
            raise
