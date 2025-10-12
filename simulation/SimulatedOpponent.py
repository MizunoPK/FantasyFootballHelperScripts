"""
Simulated Opponent Team

Represents opponent teams using simpler, strategy-based decision making.
Simulated opponents use predefined strategies for drafting and basic projected
points for weekly lineups.

Strategies:
- 'adp_aggressive': Pick lowest ADP available
- 'projected_points_aggressive': Pick highest projected points
- 'adp_with_draft_order': Use ADP with draft position priorities
- 'projected_points_with_draft_order': Use points with position priorities

Author: Kai Mizuno
"""

import sys
import random
from pathlib import Path
from typing import List, Optional

# Add league_helper to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "league_helper"))
sys.path.append(str(project_root / "league_helper" / "util"))
from league_helper.util.PlayerManager import PlayerManager
from league_helper.util.ConfigManager import ConfigManager
from league_helper.util.TeamDataManager import TeamDataManager
import league_helper.constants as Constants

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger


class SimulatedOpponent:
    """
    Opponent team using strategy-based drafting and simple lineup decisions.

    Simulated opponents use simpler logic than DraftHelperTeam:
    - Draft using predefined strategies (ADP, projected points, etc.)
    - Weekly lineups based solely on highest weekly projected points
    - 20% human error rate (picks from top 5 instead of #1)

    Attributes:
        projected_pm (PlayerManager): PlayerManager with projected data
        actual_pm (PlayerManager): PlayerManager with actual data for scoring
        config (ConfigManager): Configuration manager
        team_data_mgr (TeamDataManager): Team rankings data
        strategy (str): Draft strategy ('adp_aggressive', 'projected_points_aggressive', etc.)
        roster (List[FantasyPlayer]): Current team roster
        logger: Logger instance
    """

    # Strategy constants
    STRATEGY_ADP_AGGRESSIVE = 'adp_aggressive'
    STRATEGY_PROJECTED_POINTS_AGGRESSIVE = 'projected_points_aggressive'
    STRATEGY_ADP_WITH_DRAFT_ORDER = 'adp_with_draft_order'
    STRATEGY_PROJECTED_POINTS_WITH_DRAFT_ORDER = 'projected_points_with_draft_order'

    HUMAN_ERROR_RATE = 0.2  # 20% chance to pick from top 5 instead of #1

    def __init__(
        self,
        projected_pm: PlayerManager,
        actual_pm: PlayerManager,
        config: ConfigManager,
        team_data_mgr: TeamDataManager,
        strategy: str
    ):
        """
        Initialize SimulatedOpponent.

        Args:
            projected_pm (PlayerManager): PlayerManager using players_projected.csv
            actual_pm (PlayerManager): PlayerManager using players_actual.csv
            config (ConfigManager): Configuration with scoring parameters
            team_data_mgr (TeamDataManager): Team data for matchup calculations
            strategy (str): Draft strategy to use

        Raises:
            ValueError: If strategy is not recognized
        """
        self.logger = get_logger()

        valid_strategies = [
            self.STRATEGY_ADP_AGGRESSIVE,
            self.STRATEGY_PROJECTED_POINTS_AGGRESSIVE,
            self.STRATEGY_ADP_WITH_DRAFT_ORDER,
            self.STRATEGY_PROJECTED_POINTS_WITH_DRAFT_ORDER
        ]

        if strategy not in valid_strategies:
            raise ValueError(f"Invalid strategy: {strategy}. Must be one of {valid_strategies}")

        self.logger.debug(f"Initializing SimulatedOpponent with strategy: {strategy}")

        self.projected_pm = projected_pm
        self.actual_pm = actual_pm
        self.config = config
        self.team_data_mgr = team_data_mgr
        self.strategy = strategy

        self.roster: List[FantasyPlayer] = []

    def draft_player(self, player: FantasyPlayer) -> None:
        """
        Add a player to the roster and mark as drafted in both PlayerManagers.

        Args:
            player (FantasyPlayer): Player to add to roster

        Side Effects:
            - Adds player to self.roster
            - Sets player.drafted = 1 in both projected_pm and actual_pm
        """
        self.roster.append(player)

        # Mark as drafted by opponent (drafted=1) in both PlayerManagers
        for p in self.projected_pm.players:
            if p.id == player.id:
                p.drafted = 1
                break

        for p in self.actual_pm.players:
            if p.id == player.id:
                p.drafted = 1
                break

        self.logger.debug(f"SimulatedOpponent ({self.strategy}) drafted: {player.name} ({player.position})")

    def get_draft_recommendation(self) -> FantasyPlayer:
        """
        Get draft recommendation based on team strategy.

        Applies the team's strategy to determine best available player, then
        applies human error (20% chance to pick from top 5 instead of #1).

        Returns:
            FantasyPlayer: Recommended player to draft

        Raises:
            ValueError: If no players are available
        """
        # Get available players (drafted = 0)
        available_players = [p for p in self.projected_pm.players if p.drafted == 0]

        if not available_players:
            raise ValueError("No available players to draft")

        # Get current draft round (based on roster size)
        current_round = len(self.roster)

        # Apply strategy to get ranked list of players
        if self.strategy == self.STRATEGY_ADP_AGGRESSIVE:
            ranked_players = self._rank_by_adp(available_players)
        elif self.strategy == self.STRATEGY_PROJECTED_POINTS_AGGRESSIVE:
            ranked_players = self._rank_by_projected_points(available_players)
        elif self.strategy == self.STRATEGY_ADP_WITH_DRAFT_ORDER:
            ranked_players = self._rank_by_adp_with_draft_order(available_players, current_round)
        elif self.strategy == self.STRATEGY_PROJECTED_POINTS_WITH_DRAFT_ORDER:
            ranked_players = self._rank_by_points_with_draft_order(available_players, current_round)
        else:
            raise ValueError(f"Unknown strategy: {self.strategy}")

        # Apply human error
        selected_player = self._apply_human_error(ranked_players)

        self.logger.debug(f"SimulatedOpponent ({self.strategy}) recommends: {selected_player.name}")

        return selected_player

    def _rank_by_adp(self, players: List[FantasyPlayer]) -> List[FantasyPlayer]:
        """Rank players by ADP (ascending - lower ADP is better)."""
        return sorted(players, key=lambda p: p.average_draft_position if p.average_draft_position else 999.0)

    def _rank_by_projected_points(self, players: List[FantasyPlayer]) -> List[FantasyPlayer]:
        """Rank players by projected points (descending - higher is better)."""
        return sorted(players, key=lambda p: p.fantasy_points if p.fantasy_points else 0.0, reverse=True)

    def _rank_by_adp_with_draft_order(self, players: List[FantasyPlayer], draft_round: int) -> List[FantasyPlayer]:
        """
        Rank players by ADP with draft order bonuses.

        Uses config.draft_order to prioritize certain positions in each round.
        """
        def score_player(player: FantasyPlayer) -> float:
            # Start with ADP (lower is better, so negate for sorting)
            base_score = -(player.average_draft_position if player.average_draft_position else 999.0)

            # Add draft order bonus if position is prioritized this round
            bonus, _ = self.config.get_draft_order_bonus(player.position, draft_round)
            base_score += bonus

            return base_score

        return sorted(players, key=score_player, reverse=True)

    def _rank_by_points_with_draft_order(self, players: List[FantasyPlayer], draft_round: int) -> List[FantasyPlayer]:
        """
        Rank players by projected points with draft order bonuses.

        Uses config.draft_order to prioritize certain positions in each round.
        """
        def score_player(player: FantasyPlayer) -> float:
            # Start with projected points
            base_score = player.fantasy_points if player.fantasy_points else 0.0

            # Add draft order bonus if position is prioritized this round
            bonus, _ = self.config.get_draft_order_bonus(player.position, draft_round)
            base_score += bonus

            return base_score

        return sorted(players, key=score_player, reverse=True)

    def _apply_human_error(self, ranked_players: List[FantasyPlayer]) -> FantasyPlayer:
        """
        Apply 20% human error rate.

        20% of the time, picks randomly from top 5.
        80% of the time, picks #1.

        Args:
            ranked_players (List[FantasyPlayer]): Players ranked by strategy

        Returns:
            FantasyPlayer: Selected player (with possible error)
        """
        if random.random() < self.HUMAN_ERROR_RATE:
            # Human error: pick randomly from top 5
            top_5 = ranked_players[:min(5, len(ranked_players))]
            return random.choice(top_5)
        else:
            # Pick #1 recommendation
            return ranked_players[0]

    def set_weekly_lineup(self, week: int) -> float:
        """
        Set weekly lineup based on highest weekly projected points per position.

        Unlike DraftHelperTeam, SimulatedOpponent uses simple logic:
        - Select highest weekly projected points for each position
        - No optimization or matchup considerations

        Args:
            week (int): Week number (1-17)

        Returns:
            float: Total actual points scored by the starting lineup

        Note:
            Uses same position counts as StarterHelper:
            1 QB, 2 RB, 2 WR, 1 TE, 1 FLEX (RB/WR/TE), 1 K, 1 DST
        """
        # Get roster players grouped by position
        qbs = [p for p in self.roster if p.position == 'QB']
        rbs = [p for p in self.roster if p.position == 'RB']
        wrs = [p for p in self.roster if p.position == 'WR']
        tes = [p for p in self.roster if p.position == 'TE']
        ks = [p for p in self.roster if p.position == 'K']
        dsts = [p for p in self.roster if p.position == 'DST' or p.position == 'DEF']

        # Get weekly projected points for sorting
        def get_weekly_projection(player: FantasyPlayer) -> float:
            projected, _ = self.projected_pm.get_weekly_projection(player, week)
            return projected if projected else 0.0

        # Sort each position by weekly projected points (descending)
        qbs.sort(key=get_weekly_projection, reverse=True)
        rbs.sort(key=get_weekly_projection, reverse=True)
        wrs.sort(key=get_weekly_projection, reverse=True)
        tes.sort(key=get_weekly_projection, reverse=True)
        ks.sort(key=get_weekly_projection, reverse=True)
        dsts.sort(key=get_weekly_projection, reverse=True)

        # Select starters (highest projected for each position)
        starters = []

        # 1 QB
        if qbs:
            starters.append(qbs[0])

        # 2 RBs
        starters.extend(rbs[:2])

        # 2 WRs
        starters.extend(wrs[:2])

        # 1 TE
        if tes:
            starters.append(tes[0])

        # 1 FLEX (best remaining RB/WR/TE)
        flex_candidates = []
        if len(rbs) > 2:
            flex_candidates.extend(rbs[2:])
        if len(wrs) > 2:
            flex_candidates.extend(wrs[2:])
        if len(tes) > 1:
            flex_candidates.extend(tes[1:])

        if flex_candidates:
            flex_candidates.sort(key=get_weekly_projection, reverse=True)
            starters.append(flex_candidates[0])

        # 1 K
        if ks:
            starters.append(ks[0])

        # 1 DST
        if dsts:
            starters.append(dsts[0])

        # Calculate actual points scored
        total_actual_points = 0.0
        for starter in starters:
            actual_weekly_points, _ = self.actual_pm.get_weekly_projection(starter, week)
            total_actual_points += actual_weekly_points if actual_weekly_points else 0.0

        self.logger.debug(f"SimulatedOpponent ({self.strategy}) Week {week} lineup scored {total_actual_points:.2f} actual points")

        return total_actual_points

    def mark_player_drafted(self, player_id: int) -> None:
        """
        Mark a player as drafted by another team.

        Sets player.drafted = 1 in both PlayerManager instances.

        Args:
            player_id (int): ID of the player drafted by another team
        """
        # Mark in projected PlayerManager
        for p in self.projected_pm.players:
            if p.id == player_id:
                p.drafted = 1
                break

        # Mark in actual PlayerManager
        for p in self.actual_pm.players:
            if p.id == player_id:
                p.drafted = 1
                break

        self.logger.debug(f"Marked player {player_id} as drafted by another team")

    def get_roster_size(self) -> int:
        """Get current roster size."""
        return len(self.roster)

    def get_roster_players(self) -> List[FantasyPlayer]:
        """Get list of all rostered players."""
        return self.roster.copy()
