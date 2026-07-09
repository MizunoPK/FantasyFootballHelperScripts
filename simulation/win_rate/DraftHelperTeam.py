"""
Draft Helper Team

Represents the team using the DraftHelper system for both draft decisions
and weekly lineup optimization. This is the team being tested/optimized
through simulations.

The DraftHelperTeam uses:
- AddToRosterModeManager for draft recommendations (always picks #1 recommendation, no error)
- StarterHelperModeManager for weekly lineup decisions
- Two PlayerManager instances: one for projected data, one for actual scoring

Author: Kai Mizuno
"""

from typing import List, Optional

from league_helper.util.PlayerManager import PlayerManager
from league_helper.util.ConfigManager import ConfigManager
from league_helper.util.TeamDataManager import TeamDataManager
from league_helper.add_to_roster_mode.AddToRosterModeManager import AddToRosterModeManager
from league_helper.starter_helper_mode.StarterHelperModeManager import StarterHelperModeManager
from utils.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger


class DraftHelperTeam:
    """
    Team that uses DraftHelper system for drafting and lineup optimization.

    This class represents the team being tested in simulations. It uses the
    AddToRosterModeManager for intelligent draft picks and StarterHelperModeManager
    for optimal weekly lineups.

    Key behaviors:
    - Always picks the #1 draft recommendation (no human error)
    - Uses projected data for decision-making
    - Scores based on actual data for results

    Attributes:
        projected_pm (PlayerManager): PlayerManager with projected data for decisions
        actual_pm (PlayerManager): PlayerManager with actual data for scoring
        config (ConfigManager): Configuration manager with scoring parameters
        team_data_mgr (TeamDataManager): Team rankings and matchup data
        roster (List[FantasyPlayer]): Current team roster (max 15 players)
        add_to_roster_mgr (AddToRosterModeManager): Draft assistant manager
        starter_helper_mgr (StarterHelperModeManager): Weekly lineup optimizer
        logger: Logger instance for tracking operations
    """

    def __init__(
        self,
        projected_pm: PlayerManager,
        actual_pm: PlayerManager,
        config: ConfigManager,
        team_data_mgr: TeamDataManager
    ) -> None:
        """
        Initialize DraftHelperTeam.

        Args:
            projected_pm (PlayerManager): PlayerManager with projected player data from JSON files
            actual_pm (PlayerManager): PlayerManager with actual player data from JSON files
            config (ConfigManager): Configuration with scoring parameters
            team_data_mgr (TeamDataManager): Team data for matchup calculations
        """
        self.logger = get_logger()

        self.projected_pm = projected_pm
        self.actual_pm = actual_pm
        self.config = config
        self.team_data_mgr = team_data_mgr

        self.roster: List[FantasyPlayer] = []

        self.add_to_roster_mgr: Optional[AddToRosterModeManager] = None
        self.starter_helper_mgr: Optional[StarterHelperModeManager] = None

    def draft_player(self, player: FantasyPlayer) -> None:
        """
        Add a player to the roster and mark as drafted in both PlayerManagers.

        Uses the proper PlayerManager.draft_player() method to ensure:
        - Slot assignment system is used (assigns players to PRIMARY position rounds)
        - MAX_POSITIONS limits are enforced (can_draft() checks)
        - Position diversity is maintained across the roster

        Args:
            player (FantasyPlayer): Player to add to roster

        Side Effects:
            - Adds player to both PlayerManager.team.roster lists
            - Updates slot_assignments in both PlayerManagers
            - Sets player.drafted_by = "Sea Sharp" in both projected_pm and actual_pm
            - Adds player to self.roster for local tracking
        """

        for p in self.projected_pm.players:
            if p.id == player.id:
                success = self.projected_pm.draft_player(p)
                if not success:
                    self.logger.error(f"Failed to draft {p.name} in projected_pm (position limit reached?)")
                    return
                break

        for p in self.actual_pm.players:
            if p.id == player.id:
                success = self.actual_pm.draft_player(p)
                if not success:
                    self.logger.error(f"Failed to draft {p.name} in actual_pm (position limit reached?)")
                    for proj_p in self.projected_pm.players:
                        if proj_p.id == player.id:
                            self.projected_pm.team.remove_player(proj_p)
                            break
                    return
                break

        self.roster.append(player)

    def get_draft_recommendation(self) -> FantasyPlayer:
        """
        Get the top draft recommendation using AddToRosterModeManager.

        This method ALWAYS returns the #1 recommendation (no human error).
        Uses the current roster state to determine the best available player.

        Returns:
            FantasyPlayer: The top recommended player to draft

        Note:
            Creates a fresh AddToRosterModeManager each time to ensure
            recommendations reflect the current roster state.
        """
        self.add_to_roster_mgr = AddToRosterModeManager(
            self.config,
            self.projected_pm,
            self.team_data_mgr
        )

        recommendations = self.add_to_roster_mgr.get_recommendations()

        if not recommendations:
            raise ValueError("No draft recommendations available - roster may be full")

        top_pick = recommendations[0]
        self.logger.debug(f"DraftHelperTeam recommends: {top_pick.player.name} (score: {top_pick.score:.2f})")

        return top_pick.player

    def set_weekly_lineup(self, week: int) -> float:
        """
        Set optimal lineup for the week and return actual points scored.

        Uses StarterHelperModeManager to determine the best lineup based on
        weekly projections, then calculates actual points scored using actual_pm.

        Args:
            week (int): Week number (1-17)

        Returns:
            float: Total actual points scored by the starting lineup

        Process:
            1. Update config to current week
            2. Use StarterHelperModeManager to get optimal lineup
            3. Calculate actual points from JSON player data (actual_pm)
            4. Return total points scored
        """
        self.config.current_nfl_week = week

        self.starter_helper_mgr = StarterHelperModeManager(
            self.config,
            self.projected_pm,
            self.team_data_mgr
        )

        lineup = self.starter_helper_mgr.optimize_lineup()

        max_weekly_actual = self.actual_pm.calculate_max_weekly_projection(week)
        self.actual_pm.scoring_calculator.max_weekly_projection = max_weekly_actual

        total_actual_points = 0.0

        # D2: score from actual_pm (<- week_N+1) by id, not the projected_pm lineup object
        # (which reads 0.0 for the current week after the D1 in-place swap).
        actual_pm_by_id = {p.id: p for p in self.actual_pm.players}

        starters = [
            lineup.qb,
            lineup.rb1,
            lineup.rb2,
            lineup.wr1,
            lineup.wr2,
            lineup.te,
            lineup.flex,
            lineup.k,
            lineup.dst
        ]

        starters_count = 0
        for starter in starters:
            if starter and starter.player:
                starters_count += 1
                actual_player = actual_pm_by_id.get(starter.player.id)
                if actual_player is not None and 1 <= week <= 17 and len(actual_player.actual_points) >= week:
                    actual_points = actual_player.actual_points[week - 1]
                    if actual_points is not None:
                        total_actual_points += actual_points

        return total_actual_points

    def mark_player_drafted(self, player_id: int) -> None:
        """
        Mark a player as drafted by another team.

        Sets player.drafted_by = "OPPONENT" in both PlayerManager instances to indicate
        the player is no longer available.

        Args:
            player_id (int): ID of the player drafted by another team

        Side Effects:
            - Sets player.drafted_by = "OPPONENT" in both projected_pm and actual_pm
        """
        for p in self.projected_pm.players:
            if p.id == player_id:
                p.drafted_by = "OPPONENT"
                break

        for p in self.actual_pm.players:
            if p.id == player_id:
                p.drafted_by = "OPPONENT"
                break

    def get_roster_size(self) -> int:
        """Get current roster size."""
        return len(self.roster)

    def get_roster_players(self) -> List[FantasyPlayer]:
        """Get list of all rostered players."""
        return self.roster.copy()


