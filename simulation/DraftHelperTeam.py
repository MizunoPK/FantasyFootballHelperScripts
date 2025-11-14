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

import sys
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
from league_helper.add_to_roster_mode.AddToRosterModeManager import AddToRosterModeManager
from league_helper.starter_helper_mode.StarterHelperModeManager import StarterHelperModeManager

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
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
            projected_pm (PlayerManager): PlayerManager using players_projected.csv
            actual_pm (PlayerManager): PlayerManager using players_actual.csv
            config (ConfigManager): Configuration with scoring parameters
            team_data_mgr (TeamDataManager): Team data for matchup calculations
        """
        self.logger = get_logger()
        self.logger.debug("Initializing DraftHelperTeam")

        self.projected_pm = projected_pm
        self.actual_pm = actual_pm
        self.config = config
        self.team_data_mgr = team_data_mgr

        self.roster: List[FantasyPlayer] = []

        # Managers created on-demand when needed
        self.add_to_roster_mgr: Optional[AddToRosterModeManager] = None
        self.starter_helper_mgr: Optional[StarterHelperModeManager] = None

    def draft_player(self, player: FantasyPlayer) -> None:
        """
        Add a player to the roster and mark as drafted in both PlayerManagers.

        Args:
            player (FantasyPlayer): Player to add to roster

        Side Effects:
            - Adds player to self.roster
            - Adds player to both PlayerManager.team.roster lists
            - Sets player.drafted = 2 in both projected_pm and actual_pm
            - Updates both PlayerManager CSV files
        """
        self.roster.append(player)

        # Mark as drafted by this team (drafted=2) and add to team roster in both PlayerManagers
        for p in self.projected_pm.players:
            if p.id == player.id:
                p.drafted = 2
                # Add to team roster for StarterHelperModeManager
                if p not in self.projected_pm.team.roster:
                    self.projected_pm.team.roster.append(p)
                break

        for p in self.actual_pm.players:
            if p.id == player.id:
                p.drafted = 2
                # Add to team roster for scoring
                if p not in self.actual_pm.team.roster:
                    self.actual_pm.team.roster.append(p)
                break

        self.logger.debug(f"DraftHelperTeam drafted: {player.name} ({player.position})")

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
        # Create fresh AddToRosterModeManager with current state
        self.add_to_roster_mgr = AddToRosterModeManager(
            self.config,
            self.projected_pm,
            self.team_data_mgr
        )

        # Get recommendations (sorted by score, best first)
        recommendations = self.add_to_roster_mgr.get_recommendations()

        if not recommendations:
            raise ValueError("No draft recommendations available - roster may be full")

        # ALWAYS pick #1 recommendation (no human error for DraftHelperTeam)
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
            3. Calculate actual points from players_actual.csv
            4. Return total points scored
        """
        # Update config to current week
        self.config.current_nfl_week = week

        # Create fresh StarterHelperModeManager for this week
        self.starter_helper_mgr = StarterHelperModeManager(
            self.config,
            self.projected_pm,
            self.team_data_mgr
        )

        # Get optimal lineup based on projections
        lineup = self.starter_helper_mgr.optimize_lineup()

        # Calculate and set max weekly projection for actual_pm (used to get actual points)
        max_weekly_actual = self.actual_pm.calculate_max_weekly_projection(week)
        self.actual_pm.scoring_calculator.max_weekly_projection = max_weekly_actual

        # Calculate actual points scored
        total_actual_points = 0.0

        # Get all starters from the lineup
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

        # Sum actual points for each starter
        for starter in starters:
            if starter and starter.player:
                # Get actual weekly points from actual_pm
                actual_weekly_points, _ = self.actual_pm.get_weekly_projection(starter.player, week)
                total_actual_points += actual_weekly_points

        self.logger.debug(f"DraftHelperTeam Week {week} lineup scored {total_actual_points:.2f} actual points")

        return total_actual_points

    def mark_player_drafted(self, player_id: int) -> None:
        """
        Mark a player as drafted by another team.

        Sets player.drafted = 1 in both PlayerManager instances to indicate
        the player is no longer available.

        Args:
            player_id (int): ID of the player drafted by another team

        Side Effects:
            - Sets player.drafted = 1 in both projected_pm and actual_pm
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

        self.logger.debug(f"Marked player {player_id} as drafted by opponent")

    def get_roster_size(self) -> int:
        """Get current roster size."""
        return len(self.roster)

    def get_roster_players(self) -> List[FantasyPlayer]:
        """Get list of all rostered players."""
        return self.roster.copy()
