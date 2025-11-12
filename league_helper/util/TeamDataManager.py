#!/usr/bin/env python3
"""
Team Data Manager

Manages NFL team rankings and matchup data for scoring calculations.
Loads team offensive/defensive rankings from teams.csv and provides
matchup analysis for player scoring adjustments.

Key responsibilities:
- Loading team data from teams.csv
- Caching team rankings (offensive and defensive)
- Calculating matchup differentials for players
- Providing opponent information for each team

Matchup calculations:
- Offensive players: opponent_defensive_rank - team_offensive_rank
- Defensive players: opponent_offensive_rank - team_defensive_rank
- Positive values indicate favorable matchups

Author: Kai Mizuno
"""

from pathlib import Path
from typing import Dict, Optional, TYPE_CHECKING

import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.TeamData import TeamData, load_teams_from_csv
from utils.LoggingManager import get_logger

if TYPE_CHECKING:
    from league_helper.util.SeasonScheduleManager import SeasonScheduleManager


class TeamDataManager:
    """
    Loads and manages team ranking data from teams.csv file.

    This class caches team data for efficient lookup during scoring calculations
    and provides methods for matchup analysis.

    Attributes:
        logger: Logger instance for tracking operations
        teams_file (Path): Path to teams.csv data file
        team_data_cache (Dict[str, TeamData]): Cached team data by team abbreviation
        season_schedule_manager (SeasonScheduleManager): Manager for season schedule data
        current_nfl_week (int): Current NFL week number
    """

    def __init__(self, data_folder: Path, season_schedule_manager: Optional['SeasonScheduleManager'] = None, current_nfl_week: int = 1):
        """
        Initialize TeamDataManager and load team data.

        Args:
            data_folder (Path): Path to data directory containing teams.csv
            season_schedule_manager (Optional[SeasonScheduleManager]): Season schedule manager for opponent lookups
            current_nfl_week (int): Current NFL week number (default: 1)

        Side Effects:
            - Loads teams.csv into memory cache
            - Logs warning if teams.csv is not found
        """
        self.logger = get_logger()
        self.logger.debug("Initializing Team Data Manager")

        self.teams_file = data_folder / 'teams.csv'
        self.team_data_cache: Dict[str, TeamData] = {}
        self.season_schedule_manager = season_schedule_manager
        self.current_nfl_week = current_nfl_week
        self._load_team_data()

    def _load_team_data(self) -> None:
        """Load team data from teams.csv file."""
        try:
            if not self.teams_file.exists():
                self.logger.warning(f"Teams file not found: {self.teams_file}. Team rankings will not be available.")
                return

            teams = load_teams_from_csv(str(self.teams_file))

            # Build team lookup cache
            self.team_data_cache = {team.team: team for team in teams}

            self.logger.debug(f"Loaded team data for {len(self.team_data_cache)} teams from {self.teams_file}")

        except Exception as e:
            self.logger.warning(f"Error loading team data from {self.teams_file}: {e}. Team rankings will not be available.")
            self.team_data_cache = {}

    def get_team_offensive_rank(self, team: str) -> Optional[int]:
        """
        Get team offensive ranking.

        Args:
            team: Team abbreviation (e.g., 'PHI', 'KC')

        Returns:
            Team offensive rank (1-32) or None if not available
        """
        team_data = self.team_data_cache.get(team)
        return team_data.offensive_rank if team_data else None

    def get_team_defensive_rank(self, team: str) -> Optional[int]:
        """
        Get team defensive ranking.

        Args:
            team: Team abbreviation (e.g., 'PHI', 'KC')

        Returns:
            Team defensive rank (1-32) or None if not available
        """
        team_data = self.team_data_cache.get(team)
        return team_data.defensive_rank if team_data else None

    def get_team_defense_vs_position_rank(self, team: str, position: str) -> Optional[int]:
        """
        Get team's defense ranking against a specific position.

        Uses position-specific defense rankings (e.g., def_vs_qb_rank) to provide
        more accurate matchup analysis. For defensive positions (DST, DEF, D/ST),
        returns the overall defensive rank.

        Args:
            team: Team abbreviation (e.g., 'PHI', 'KC')
            position: Player position (QB, RB, WR, TE, K, DST, DEF, D/ST)

        Returns:
            Position-specific defense rank (1-32) or None if not found.
            Lower rank = better defense against that position.

        Example:
            >>> manager.get_team_defense_vs_position_rank('PHI', 'QB')
            5  # PHI has 5th-best defense vs QB
            >>> manager.get_team_defense_vs_position_rank('KC', 'RB')
            20  # KC has 20th-ranked defense vs RB
        """
        team_data = self.team_data_cache.get(team)
        if not team_data:
            return None

        # Check if position is defense (use overall defensive rank)
        import sys
        sys.path.append(str(Path(__file__).parent))
        from constants import DEFENSE_POSITIONS

        if position in DEFENSE_POSITIONS:
            return team_data.defensive_rank

        # Return position-specific rank
        position_rank_map = {
            'QB': team_data.def_vs_qb_rank,
            'RB': team_data.def_vs_rb_rank,
            'WR': team_data.def_vs_wr_rank,
            'TE': team_data.def_vs_te_rank,
            'K': team_data.def_vs_k_rank
        }

        rank = position_rank_map.get(position)

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
        return bool(self.team_data_cache)

    def get_available_teams(self) -> list[str]:
        """Get list of all teams for which data is available."""
        return list(self.team_data_cache.keys())
    
    def is_matchup_available(self) -> bool:
        """
        Check if matchup calculations are available.

        Returns:
            True if team data is loaded and valid, False otherwise
        """
        return self.team_data_cache is not None and len(self.team_data_cache) > 0

    def reload_team_data(self) -> None:
        """Reload team data from teams.csv file (useful if file was updated)."""
        self.team_data_cache = {}
        self._load_team_data()


    def get_rank_difference(self, player_team: str, position: str) -> int:
        """
        Calculate matchup quality using position-specific defense rankings.

        Formula for Offensive positions: (Opponent Position-Specific DEF Rank)
        Formula for Defensive positions: (Opponent OFF Rank)

        Args:
            player_team: Team abbreviation (e.g., 'KC', 'BUF')
            position: Player position (QB, RB, WR, TE, K, DST, DEF, D/ST)
                     Determines which opponent defense rank to use

        Returns:
            Opponent defense rank integer, or 0 if data unavailable
            Higher rank = weaker defense = favorable matchup
            Lower rank = stronger defense = tough matchup

        Example:
            KC QB vs BUF (DEF vs QB rank #25):
            matchup_score = 25 (favorable - BUF weak vs QB)

            KC RB vs BUF (DEF vs RB rank #5):
            matchup_score = 5 (tough - BUF strong vs RB)

            MIA DST vs NYJ (OFF rank #28):
            matchup_score = 28 (favorable - NYJ weak offense)
        """
        # Check if team data is loaded
        if not self.is_matchup_available():
            return 0

        # Get the opponent team abbreviation
        opponent_abbr = self.get_team_opponent(player_team)
        if opponent_abbr is None:
            self.logger.debug(f"No opponent found for team: {player_team}")
            return 0

        # Check if player is on defense
        import sys
        sys.path.append(str(Path(__file__).parent))
        from constants import DEFENSE_POSITIONS
        is_defense = position in DEFENSE_POSITIONS

        # Get opponent's rank (position-specific defense for offensive players, offensive rank for DST)
        if is_defense:
            # For DST: use opponent's offensive rank
            opponent_rank = self.get_team_offensive_rank(opponent_abbr)
        else:
            # For offensive positions: use opponent's position-specific defense rank
            opponent_rank = self.get_team_defense_vs_position_rank(opponent_abbr, position)

        # Handle missing opponent data
        if opponent_rank is None:
            self.logger.debug(f"Opponent rank not found: {opponent_abbr} vs {position}")
            return 0

        # Return opponent defense rank directly
        # Higher rank = weaker defense = favorable matchup (e.g., rank 32 = weakest defense)
        # Lower rank = stronger defense = tough matchup (e.g., rank 1 = strongest defense)
        matchup_score = int(opponent_rank)

        self.logger.debug(
            f"Matchup for {player_team} {position}: "
            f"vs {opponent_abbr} Def rank {opponent_rank} "
            f"= {matchup_score}"
        )

        return matchup_score