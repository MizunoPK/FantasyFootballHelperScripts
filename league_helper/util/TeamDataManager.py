#!/usr/bin/env python3
"""
Team Data Manager

Manages NFL team rankings and matchup data for scoring calculations.
Loads per-team historical data from team_data folder and calculates
rankings on-the-fly using configurable rolling windows.

Key responsibilities:
- Loading team weekly data from team_data/*.csv files
- Calculating offensive/defensive rankings from rolling window
- Calculating position-specific defense rankings
- Providing matchup analysis for player scoring adjustments

Author: Kai Mizuno
"""

from pathlib import Path
from typing import Dict, List, Optional, Any, TYPE_CHECKING
import csv
import json

import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.TeamData import TeamData, load_team_weekly_data, NFL_TEAMS
from utils.LoggingManager import get_logger

if TYPE_CHECKING:
    from league_helper.util.SeasonScheduleManager import SeasonScheduleManager
    from league_helper.util.ConfigManager import ConfigManager


class TeamDataManager:
    """
    Loads and manages team ranking data calculated from per-team historical files.

    This class loads weekly data from team_data/*.csv files and calculates
    rankings on-the-fly based on configurable MIN_WEEKS rolling windows.

    Attributes:
        logger: Logger instance for tracking operations
        data_folder (Path): Path to data directory containing team_data folder
        config_manager (ConfigManager): Configuration manager for MIN_WEEKS values
        team_weekly_data (Dict): Raw weekly data for each team
        offensive_ranks (Dict[str, int]): Calculated offensive rankings
        defensive_ranks (Dict[str, int]): Calculated defensive rankings
        position_ranks (Dict[str, Dict[str, int]]): Position-specific defense rankings
        season_schedule_manager (SeasonScheduleManager): Manager for season schedule data
        current_nfl_week (int): Current NFL week number
    """

    def __init__(self, data_folder: Path, config_manager: 'ConfigManager',
                 season_schedule_manager: Optional['SeasonScheduleManager'] = None,
                 current_nfl_week: int = 1):
        """
        Initialize TeamDataManager and load team data.

        Args:
            data_folder (Path): Path to data directory containing team_data folder
            config_manager (ConfigManager): Configuration manager for MIN_WEEKS access
            season_schedule_manager (Optional[SeasonScheduleManager]): Season schedule manager
            current_nfl_week (int): Current NFL week number (default: 1)

        Side Effects:
            - Loads team_data/*.csv files into memory
            - Calculates rankings based on MIN_WEEKS rolling window
        """
        self.logger = get_logger()
        self.logger.debug("Initializing Team Data Manager")

        self.data_folder = Path(data_folder)
        self.config_manager = config_manager
        self.team_data_folder = self.data_folder / 'team_data'

        # Raw weekly data: {team: [{week: 1, QB: 18.5, ...}, ...]}
        self.team_weekly_data: Dict[str, List[Dict[str, Any]]] = {}

        # Calculated rankings
        self.offensive_ranks: Dict[str, int] = {}
        self.defensive_ranks: Dict[str, int] = {}
        self.position_ranks: Dict[str, Dict[str, int]] = {}  # {team: {QB: rank, RB: rank, ...}}
        self.dst_fantasy_ranks: Dict[str, int] = {}  # D/ST fantasy performance rankings

        # D/ST player data: {team: [week_1_points, week_2_points, ..., week_17_points]}
        self.dst_player_data: Dict[str, List[Optional[float]]] = {}

        # Legacy cache for compatibility (stores TeamData objects)
        self.team_data_cache: Dict[str, TeamData] = {}

        self.season_schedule_manager = season_schedule_manager
        self.current_nfl_week = current_nfl_week

        self._load_team_data()
        self._load_dst_player_data()
        self._calculate_rankings()

    def _load_team_data(self) -> None:
        """Load team weekly data from team_data folder."""
        try:
            if not self.team_data_folder.exists():
                self.logger.warning(f"Team data folder not found: {self.team_data_folder}. Team rankings will not be available.")
                return

            self.team_weekly_data = load_team_weekly_data(str(self.team_data_folder))
            self.logger.debug(f"Loaded team data for {len(self.team_weekly_data)} teams from {self.team_data_folder}")

        except Exception as e:
            self.logger.warning(f"Error loading team data from {self.team_data_folder}: {e}. Team rankings will not be available.")
            self.team_weekly_data = {}

    def _load_dst_player_data(self) -> None:
        """
        Load D/ST weekly fantasy scores from dst_data.json actual_points arrays.

        Extracts D/ST player entries and stores their weekly fantasy points for
        ranking calculation. This data is used to rank D/ST units by their actual
        fantasy performance rather than points allowed to opponents.

        Side Effects:
            - Populates self.dst_player_data with {team: [week_1_points, ..., week_17_points]}
            - Logs error if dst_data.json is not found or has errors
        """
        try:
            # Spec: sub_feature_06_team_data_manager_dst_migration_spec.md lines 77-92
            dst_json_path = self.data_folder / 'player_data' / 'dst_data.json'

            with open(dst_json_path, 'r') as f:
                data = json.load(f)

            dst_players = data.get('dst_data', [])

            for dst_player in dst_players:
                team = dst_player.get('team', '').upper()
                actual_points = dst_player.get('actual_points', [0.0] * 17)

                # Store in same format: {team: [week_1, ..., week_17]}
                self.dst_player_data[team] = actual_points

            self.logger.debug(f"Loaded D/ST data for {len(self.dst_player_data)} teams from {dst_json_path}")

        except FileNotFoundError:
            self.logger.error(f"D/ST data file not found: {dst_json_path}")
            self.dst_player_data = {}
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in D/ST data file: {e}")
            self.dst_player_data = {}
        except (PermissionError, OSError) as e:
            self.logger.error(f"Error reading D/ST data file {dst_json_path}: {e}")
            self.dst_player_data = {}

    def _calculate_rankings(self) -> None:
        """
        Calculate all rankings based on current week and MIN_WEEKS settings.

        Uses different rolling windows for different ranking types:
        - Offensive/defensive ranks: TEAM_QUALITY_MIN_WEEKS window
        - Position-specific defense ranks: MATCHUP_MIN_WEEKS window
        """
        if not self.team_weekly_data:
            self.logger.debug("No team data available for ranking calculation")
            return

        # Get MIN_WEEKS values from config
        team_quality_min_weeks = self.config_manager.get_team_quality_min_weeks()
        matchup_min_weeks = self.config_manager.get_matchup_min_weeks()

        # Check if we have enough weeks of data (use smaller of the two)
        min_required = min(team_quality_min_weeks, matchup_min_weeks)
        if self.current_nfl_week <= min_required:
            self.logger.debug(f"Week {self.current_nfl_week} < MIN_WEEKS {min_required}, using neutral rankings")
            self._set_neutral_rankings()
            return

        end_week = self.current_nfl_week - 1  # Last completed week
        positions = ['QB', 'RB', 'WR', 'TE', 'K']

        # Calculate offensive/defensive rankings using team_quality_min_weeks
        tq_start_week = max(1, end_week - team_quality_min_weeks + 1)
        self.logger.debug(f"Team quality rankings from weeks {tq_start_week}-{end_week}")

        offensive_totals = {}
        defensive_totals = {}

        for team, weeks_data in self.team_weekly_data.items():
            off_total = 0.0
            def_total = 0.0
            games = 0

            for week_data in weeks_data:
                week_num = week_data.get('week', 0)
                if tq_start_week <= week_num <= end_week:
                    points_scored = week_data.get('points_scored', 0)
                    points_allowed = week_data.get('points_allowed', 0)

                    # Skip bye weeks (all zeros)
                    if points_scored == 0 and points_allowed == 0:
                        continue

                    off_total += points_scored
                    def_total += points_allowed
                    games += 1

            offensive_totals[team] = (off_total, games)
            defensive_totals[team] = (def_total, games)

        # Calculate position-specific rankings using matchup_min_weeks
        mu_start_week = max(1, end_week - matchup_min_weeks + 1)
        self.logger.debug(f"Position rankings from weeks {mu_start_week}-{end_week}")

        position_totals = {}

        for team, weeks_data in self.team_weekly_data.items():
            pos_totals = {pos: [0.0, 0] for pos in positions}

            for week_data in weeks_data:
                week_num = week_data.get('week', 0)
                if mu_start_week <= week_num <= end_week:
                    points_scored = week_data.get('points_scored', 0)
                    points_allowed = week_data.get('points_allowed', 0)

                    # Skip bye weeks (all zeros)
                    if points_scored == 0 and points_allowed == 0:
                        continue

                    for pos in positions:
                        pos_points = week_data.get(f'pts_allowed_to_{pos}', 0)
                        pos_totals[pos][0] += pos_points
                        pos_totals[pos][1] += 1

            position_totals[team] = pos_totals

        # Calculate D/ST fantasy rankings using team_quality_min_weeks (same window as offensive/defensive)
        dst_totals = {}
        for team, weekly_points in self.dst_player_data.items():
            dst_total = 0.0
            games = 0

            # Loop through weeks in rolling window
            for week_num in range(tq_start_week, end_week + 1):
                # week_num is 1-indexed, list is 0-indexed
                week_index = week_num - 1
                if week_index < len(weekly_points):
                    points = weekly_points[week_index]
                    # Skip bye weeks (None or 0)
                    if points is not None and points != 0:
                        dst_total += points
                        games += 1

            dst_totals[team] = (dst_total, games)

        # Calculate per-game averages and rank
        self._rank_offensive(offensive_totals)
        self._rank_defensive(defensive_totals)
        self._rank_dst_fantasy(dst_totals)
        self._rank_positions(position_totals, positions)

        # Build team_data_cache for compatibility
        self._build_team_data_cache()

        self.logger.debug(f"Calculated rankings for {len(self.offensive_ranks)} teams")

    def _set_neutral_rankings(self) -> None:
        """Set all rankings to neutral (16) for early season."""
        for team in NFL_TEAMS:
            self.offensive_ranks[team] = 16
            self.defensive_ranks[team] = 16
            self.dst_fantasy_ranks[team] = 16
            self.position_ranks[team] = {
                'QB': 16, 'RB': 16, 'WR': 16, 'TE': 16, 'K': 16
            }
        self._build_team_data_cache()

    def _rank_offensive(self, totals: Dict[str, tuple]) -> None:
        """Rank teams by offensive production (higher points = better = rank 1)."""
        # Calculate per-game averages
        averages = []
        for team, (total, games) in totals.items():
            avg = total / games if games > 0 else 0
            averages.append((team, avg))

        # Sort by average descending (most points = rank 1)
        averages.sort(key=lambda x: x[1], reverse=True)

        for rank, (team, _) in enumerate(averages, 1):
            self.offensive_ranks[team] = rank

    def _rank_defensive(self, totals: Dict[str, tuple]) -> None:
        """Rank teams by defensive production (fewer points allowed = better = rank 1)."""
        # Calculate per-game averages
        averages = []
        for team, (total, games) in totals.items():
            avg = total / games if games > 0 else float('inf')
            averages.append((team, avg))

        # Sort by average ascending (fewest points = rank 1)
        averages.sort(key=lambda x: x[1])

        for rank, (team, _) in enumerate(averages, 1):
            self.defensive_ranks[team] = rank

    def _rank_dst_fantasy(self, totals: Dict[str, tuple]) -> None:
        """
        Rank teams by D/ST fantasy points scored (higher points = better = rank 1).

        This ranks D/ST units by their actual fantasy performance, NOT by points
        allowed to opponents. Uses the same descending sort as offensive rankings
        since more D/ST fantasy points = better performance.

        Args:
            totals: Dict mapping team abbreviation to (total_points, games_played)

        Side Effects:
            - Populates self.dst_fantasy_ranks with rankings (1-32)
        """
        # Calculate per-game averages
        averages = []
        for team, (total, games) in totals.items():
            avg = total / games if games > 0 else 0
            averages.append((team, avg))

        # Sort by average descending (most points = rank 1, like offensive)
        averages.sort(key=lambda x: x[1], reverse=True)

        for rank, (team, _) in enumerate(averages, 1):
            self.dst_fantasy_ranks[team] = rank

    def _rank_positions(self, totals: Dict[str, Dict], positions: List[str]) -> None:
        """Rank teams by position-specific defense (fewer points = better = rank 1)."""
        for pos in positions:
            averages = []
            for team, pos_data in totals.items():
                total, games = pos_data[pos]
                avg = total / games if games > 0 else float('inf')
                averages.append((team, avg))

            # Sort by average ascending (fewest points allowed = rank 1)
            averages.sort(key=lambda x: x[1])

            for rank, (team, _) in enumerate(averages, 1):
                if team not in self.position_ranks:
                    self.position_ranks[team] = {}
                self.position_ranks[team][pos] = rank

    def _build_team_data_cache(self) -> None:
        """Build team_data_cache from calculated rankings for compatibility."""
        for team in self.offensive_ranks.keys():
            pos_ranks = self.position_ranks.get(team, {})
            self.team_data_cache[team] = TeamData(
                team=team,
                offensive_rank=self.offensive_ranks.get(team),
                defensive_rank=self.defensive_ranks.get(team),
                def_vs_qb_rank=pos_ranks.get('QB'),
                def_vs_rb_rank=pos_ranks.get('RB'),
                def_vs_wr_rank=pos_ranks.get('WR'),
                def_vs_te_rank=pos_ranks.get('TE'),
                def_vs_k_rank=pos_ranks.get('K')
            )

    def set_current_week(self, week_num: int) -> None:
        """
        Update current week and recalculate rankings.

        Used by simulation to update rankings each week.

        Args:
            week_num: New NFL week number
        """
        self.current_nfl_week = week_num
        self._calculate_rankings()

    def get_team_offensive_rank(self, team: str) -> Optional[int]:
        """
        Get team offensive ranking.

        Args:
            team: Team abbreviation (e.g., 'PHI', 'KC')

        Returns:
            Team offensive rank (1-32) or None if not available
        """
        return self.offensive_ranks.get(team)

    def get_team_defensive_rank(self, team: str) -> Optional[int]:
        """
        Get team defensive ranking.

        Args:
            team: Team abbreviation (e.g., 'PHI', 'KC')

        Returns:
            Team defensive rank (1-32) or None if not available
        """
        return self.defensive_ranks.get(team)

    def get_team_dst_fantasy_rank(self, team: str) -> Optional[int]:
        """
        Get team D/ST fantasy performance ranking.

        This rank is based on D/ST fantasy points scored (sacks, INTs, TDs, etc.),
        NOT on points allowed to opponents. Higher fantasy points = better rank.

        Args:
            team: Team abbreviation (e.g., 'PHI', 'KC')

        Returns:
            D/ST fantasy rank (1-32) or None if not available
        """
        return self.dst_fantasy_ranks.get(team)

    def get_team_defense_vs_position_rank(self, team: str, position: str) -> Optional[int]:
        """
        Get team's defense ranking against a specific position.

        Args:
            team: Team abbreviation (e.g., 'PHI', 'KC')
            position: Player position (QB, RB, WR, TE, K, DST, DEF, D/ST)

        Returns:
            Position-specific defense rank (1-32) or None if not found.
        """
        # Check if position is defense (use overall defensive rank)
        import sys
        sys.path.append(str(Path(__file__).parent))
        from constants import DEFENSE_POSITIONS

        if position in DEFENSE_POSITIONS:
            return self.defensive_ranks.get(team)

        pos_ranks = self.position_ranks.get(team, {})
        rank = pos_ranks.get(position)

        if rank is None:
            self.logger.warning(f"No position-specific defense rank for {team} vs {position}")

        return rank

    def get_team_opponent(self, team: str) -> Optional[str]:
        """
        Get team's current week opponent from season schedule.

        Args:
            team: Team abbreviation (e.g., 'PHI', 'KC')

        Returns:
            Opponent team abbreviation or None if not available or bye week
        """
        if self.season_schedule_manager is None:
            self.logger.warning("SeasonScheduleManager not available for opponent lookup")
            return None

        return self.season_schedule_manager.get_opponent(team, self.current_nfl_week)

    def get_team_data(self, team: str) -> Optional[TeamData]:
        """
        Get complete team data object.

        Args:
            team: Team abbreviation (e.g., 'PHI', 'KC')

        Returns:
            TeamData object or None if not available
        """
        return self.team_data_cache.get(team)

    def is_team_data_available(self) -> bool:
        """Check if team data is loaded and available."""
        return bool(self.offensive_ranks)

    def get_available_teams(self) -> list[str]:
        """Get list of all teams for which data is available."""
        return list(self.offensive_ranks.keys())

    def is_matchup_available(self) -> bool:
        """
        Check if matchup calculations are available.

        Returns:
            True if team data is loaded and valid, False otherwise
        """
        return bool(self.offensive_ranks)

    def reload_team_data(self) -> None:
        """Reload team data from team_data folder and recalculate rankings."""
        self.team_weekly_data = {}
        self.offensive_ranks = {}
        self.defensive_ranks = {}
        self.position_ranks = {}
        self.team_data_cache = {}
        self._load_team_data()
        self._calculate_rankings()

    def get_rank_difference(self, player_team: str, position: str) -> int:
        """
        Calculate matchup quality using position-specific defense rankings.

        Args:
            player_team: Team abbreviation (e.g., 'KC', 'BUF')
            position: Player position (QB, RB, WR, TE, K, DST, DEF, D/ST)

        Returns:
            Opponent defense rank integer, or 0 if data unavailable
        """
        if not self.is_matchup_available():
            return 0

        opponent_abbr = self.get_team_opponent(player_team)
        if opponent_abbr is None:
            self.logger.debug(f"No opponent found for team: {player_team}")
            return 0

        # Check if player is on defense
        import sys
        sys.path.append(str(Path(__file__).parent))
        from constants import DEFENSE_POSITIONS
        is_defense = position in DEFENSE_POSITIONS

        if is_defense:
            opponent_rank = self.get_team_offensive_rank(opponent_abbr)
        else:
            opponent_rank = self.get_team_defense_vs_position_rank(opponent_abbr, position)

        if opponent_rank is None:
            self.logger.debug(f"Opponent rank not found: {opponent_abbr} vs {position}")
            return 0

        matchup_score = int(opponent_rank)

        self.logger.debug(
            f"Matchup for {player_team} {position}: "
            f"vs {opponent_abbr} Def rank {opponent_rank} "
            f"= {matchup_score}"
        )

        return matchup_score
