"""
Starter Helper Mode Manager

Manages the Starter Helper mode which optimizes weekly fantasy football starting
lineups based on player projections and scoring factors. The module provides
recommendations for which players to start and which to bench.

Key Features:
- Optimizes starting lineup using weekly projections
- Fills all starting positions (QB, RB1, RB2, WR1, WR2, TE, FLEX, K, DST)
- Handles bench overflow for positions with multiple players
- Calculates total projected points for optimal lineup
- Displays formatted lineup with scoring reasons

Classes:
- OptimalLineup: Represents a complete fantasy lineup with starters and bench
- StarterHelperModeManager: Manages lineup optimization workflow

Author: Kai Mizuno
"""

from typing import List, Tuple, Optional

import league_helper.constants as Constants
from league_helper.util.ConfigManager import ConfigManager
from league_helper.util.PlayerManager import PlayerManager
from league_helper.util.TeamDataManager import TeamDataManager
from league_helper.util.ScoredPlayer import ScoredPlayer
from utils.LoggingManager import get_logger
from utils.FantasyPlayer import FantasyPlayer


class OptimalLineup:
    """
    Represents a complete optimal starting lineup with starters and bench.

    This class takes a list of ScoredPlayer objects and automatically assigns them
    to optimal starting positions based on their scores. Players are assigned to
    positions in order: QB, RB1, RB2, WR1, WR2, TE, FLEX (RB/WR/TE), K, DST.

    Attributes:
        qb (Optional[ScoredPlayer]): Starting quarterback
        rb1 (Optional[ScoredPlayer]): Starting running back 1
        rb2 (Optional[ScoredPlayer]): Starting running back 2
        wr1 (Optional[ScoredPlayer]): Starting wide receiver 1
        wr2 (Optional[ScoredPlayer]): Starting wide receiver 2
        te (Optional[ScoredPlayer]): Starting tight end
        flex (Optional[ScoredPlayer]): Flex position (RB/WR/TE)
        k (Optional[ScoredPlayer]): Starting kicker
        dst (Optional[ScoredPlayer]): Starting defense/special teams
        bench (List[ScoredPlayer]): Players not in starting lineup

    The FLEX position is filled by the highest-scoring RB/WR/TE not already
    in a starting slot. Overflow players at each position go to the bench.

    Example:
        >>> scored_players = [...]  # List of ScoredPlayer objects
        >>> lineup = OptimalLineup(scored_players)
        >>> print(f"Total projected: {lineup.total_projected_points:.1f} pts")
        >>> for starter in lineup.get_all_starters():
        ...     if starter:
        ...         print(starter)
    """
    def __init__(self, scored_players : List[ScoredPlayer]):
        """
        Initialize lineup by assigning players to optimal starting positions.

        Players are sorted by score (highest first) and assigned to positions
        based on eligibility. Once all starting slots are filled, overflow
        players go to the bench.

        Position assignment priority:
        1. QB → qb slot (1 starter, overflow to bench)
        2. RB → rb1, rb2, then flex (2-3 starters, overflow to bench)
        3. WR → wr1, wr2, then flex (2-3 starters, overflow to bench)
        4. TE → te slot (1 starter, overflow to bench)
        5. K → k slot (1 starter, overflow to bench)
        6. DST → dst slot (1 starter, overflow to bench)

        Args:
            scored_players (List[ScoredPlayer]): All roster players with calculated scores

        Side Effects:
            - Sorts scored_players by score (highest first)
            - Assigns players to starting positions
            - Moves overflow players to bench
        """
        self.qb: Optional[ScoredPlayer] = None
        self.rb1: Optional[ScoredPlayer] = None
        self.rb2: Optional[ScoredPlayer] = None
        self.wr1: Optional[ScoredPlayer] = None
        self.wr2: Optional[ScoredPlayer] = None
        self.te: Optional[ScoredPlayer] = None
        self.flex: Optional[ScoredPlayer] = None
        self.k: Optional[ScoredPlayer] = None
        self.dst: Optional[ScoredPlayer] = None
        self.bench: List[ScoredPlayer] = []

        scored_players.sort(key=lambda x: x.score, reverse=True)

        for scored_player in scored_players:
            player = scored_player.player

            if player.position == Constants.QB:
                if self.qb is None:
                    self.qb = scored_player
                else:
                    self.bench.append(scored_player)

            elif player.position == Constants.RB:
                if self.rb1 is None:
                    self.rb1 = scored_player
                elif self.rb2 is None:
                    self.rb2 = scored_player
                elif self.flex is None:
                    self.flex = scored_player
                else:
                    self.bench.append(scored_player)

            elif player.position == Constants.WR:
                if self.wr1 is None:
                    self.wr1 = scored_player
                elif self.wr2 is None:
                    self.wr2 = scored_player
                elif self.flex is None:
                    self.flex = scored_player
                else:
                    self.bench.append(scored_player)

            elif player.position == Constants.TE:
                if self.te is None:
                    self.te = scored_player
                else:
                    self.bench.append(scored_player)

            elif player.position == Constants.DST:
                if self.dst is None:
                    self.dst = scored_player
                else:
                    self.bench.append(scored_player)

            elif player.position == Constants.K:
                if self.k is None:
                    self.k = scored_player
                else:
                    self.bench.append(scored_player)

            else:
                self.bench.append(scored_player)

    @property
    def total_projected_points(self) -> float:
        """
        Calculate total projected points for the starting lineup.

        Returns:
            float: Sum of all starters' projected points (bench excluded)
        """
        total = 0.0
        for recommendation in self.get_all_starters():
            if recommendation:
                total += recommendation.score
        return total

    def get_total_raw_projected_points(self, current_week: int, config) -> float:
        """
        Calculate total unweighted projected points for the starting lineup.

        This sums the raw weekly projection for each starter (before any
        scoring multipliers are applied), giving the expected fantasy points.

        Args:
            current_week (int): The current NFL week number (1-17)
            config: ConfigManager instance for hybrid weekly data

        Returns:
            float: Sum of all starters' raw weekly projected points
        """
        total = 0.0
        for recommendation in self.get_all_starters():
            if recommendation:
                weekly_projection = recommendation.player.get_single_weekly_projection(current_week, config)
                if weekly_projection is not None:
                    total += weekly_projection
        return total

    def get_all_starters(self) -> List[Optional[ScoredPlayer]]:
        """
        Get all starting positions in standard lineup order.

        Returns:
            List[Optional[ScoredPlayer]]: List of 9 starters in order:
                [QB, RB1, RB2, WR1, WR2, TE, FLEX, K, DST]
                Empty slots return None in their position.
        """
        return [self.qb, self.rb1, self.rb2, self.wr1, self.wr2,
                self.te, self.flex, self.k, self.dst]


class StarterHelperModeManager:
    """
    Manages the Starter Helper mode workflow and lineup optimization.

    This class coordinates weekly lineup optimization by scoring roster players
    using weekly projections and assembling the highest-scoring starting lineup.
    It uses performance and matchup multipliers to refine weekly projections.

    Scoring Parameters (for weekly lineups):
    - use_weekly_projection=True: Uses week-specific projections, not seasonal
    - performance=True: Adjusts based on actual vs projected performance
    - matchup=True: Factors in opponent defensive strength
    - adp=False, player_rating=False, team_quality=False: Not used for weekly

    Attributes:
        config (ConfigManager): Configuration with scoring parameters and settings
        player_manager (PlayerManager): Manages player data and scoring calculations
        team_data_manager (TeamDataManager): Provides team rankings and matchup data
        logger: Logger instance for tracking optimization operations

    Example:
        >>> manager = StarterHelperModeManager(config, player_mgr, team_data_mgr)
        >>> manager.show_recommended_starters(player_mgr, team_data_mgr)
    """


    def __init__(self, config: ConfigManager, player_manager : PlayerManager, team_data_manager : TeamDataManager):
        """
        Initialize the Starter Helper Mode Manager.

        Args:
            config (ConfigManager): Configuration manager with scoring parameters
            player_manager (PlayerManager): Player manager with roster data
            team_data_manager (TeamDataManager): Team data for matchup calculations
        """
        self.config = config
        self.logger = get_logger()
        self.set_managers(player_manager, team_data_manager)


    def set_managers(self, player_manager : PlayerManager, team_data_manager : TeamDataManager):
        """
        Update manager references (used for refreshing data between operations).

        Args:
            player_manager (PlayerManager): Updated player manager instance
            team_data_manager (TeamDataManager): Updated team data manager instance
        """
        self.player_manager = player_manager
        self.team_data_manager = team_data_manager
        self.logger.debug(f"Updated managers (roster size: {len(player_manager.team.roster)} players)")


    def show_recommended_starters(self, player_manager, team_data_manager):
        """
        Display optimal starting lineup and bench for current week.

        This is the main entry point for Starter Helper mode. It optimizes
        the lineup and displays formatted results with position labels,
        player names, projected points, and scoring reasons.

        Args:
            player_manager (PlayerManager): Player manager with current roster
            team_data_manager (TeamDataManager): Team data for matchups

        Side Effects:
            - Prints formatted lineup to console
            - Waits for user input before continuing
        """
        self.logger.info(f"Entering Starter Helper mode (Week {self.config.current_nfl_week})")

        self.set_managers(player_manager, team_data_manager)

        lineup = self.optimize_lineup()

        print(f"\n{'='*50}")
        print(f"OPTIMAL STARTING LINEUP - WEEK {self.config.current_nfl_week} ({self.config.nfl_scoring_format.upper()} SCORING)")
        print(f"{'='*50}")

        starter_positions = [
            ("QB", lineup.qb),
            ("RB", lineup.rb1),
            ("RB", lineup.rb2),
            ("WR", lineup.wr1),
            ("WR", lineup.wr2),
            ("TE", lineup.te),
            ("FLEX", lineup.flex),
            ("K", lineup.k),
            ("DEF", lineup.dst)
        ]
        bench_positions = [("", x) for x in lineup.bench]

        self.print_player_list(starter_positions)

        total_raw_projected = lineup.get_total_raw_projected_points(self.config.current_nfl_week, self.config)
        print(f"\n{'='*50}")
        print(f"COMBINED PROJECTED POINTS: {total_raw_projected:.1f} pts")

        total_weighted_score = lineup.total_projected_points
        max_weekly = self.player_manager.scoring_calculator.max_weekly_projection
        normalization_scale = self.config.normalization_max_scale

        if normalization_scale > 0 and max_weekly > 0:
            adjusted_projected = (total_weighted_score / normalization_scale) * max_weekly
            print(f"ADJUSTED PROJECTED POINTS: {adjusted_projected:.1f} pts")

        print(f"\n{'='*50}")
        print(f"BENCH")
        print(f"{'='*50}")
        self.print_player_list(bench_positions)

        input("Press Enter to Continue...")

        self.logger.info(f"Exiting Starter Helper mode (Total projected: {lineup.total_projected_points:.1f} pts)")


    def create_starting_recommendation(self,
                                     player_data: FantasyPlayer) -> ScoredPlayer:
        """
        Create a ScoredPlayer using weekly projection scoring.

        This method scores a player specifically for weekly lineup decisions,
        using weekly projections instead of seasonal projections and enabling
        performance, matchup, team quality, and game condition multipliers.

        Scoring configuration:
        - use_weekly_projection=True: Use week-specific projection data
        - performance=True: Apply actual vs projected performance adjustment
        - matchup=True: Apply opponent defensive strength adjustment (THIS WEEK)
        - team_quality=True: Apply team offensive/defensive strength (quality context)
        - temperature=True: Apply temperature bonus/penalty based on game conditions
        - wind=True: Apply wind bonus/penalty (QB/WR/K only)
        - location=True: Apply home/away/international bonus/penalty
        - schedule=False: Don't use future schedule strength (irrelevant for weekly)
        - adp=False: Don't use draft position (irrelevant for in-season)
        - player_rating=False: Don't use expert ratings (irrelevant for weekly)

        Args:
            player_data (FantasyPlayer): Player to score for weekly lineup

        Returns:
            ScoredPlayer: Player with calculated weekly score and reasoning
        """
        scored_player = self.player_manager.score_player(
            player_data,
            use_weekly_projection=True,
            adp=False,
            player_rating=False,
            team_quality=True,
            performance=True,
            matchup=True,
            schedule=False,
            bye=False,
            injury=False,
            temperature=True,
            wind=True,
            location=True
        )

        return scored_player

    def optimize_lineup(self) -> OptimalLineup:
        """
        Optimize starting lineup based on current week projections.

        This method scores all rostered players using weekly projections and
        creates an OptimalLineup that automatically assigns the highest-scoring
        players to starting positions (QB, RB1, RB2, WR1, WR2, TE, FLEX, K, DST).

        Process:
        1. Score each rostered player using weekly projections
        2. Create OptimalLineup which sorts by score and assigns positions
        3. Log total projected points for the optimal lineup

        Returns:
            OptimalLineup: Complete lineup with starters and bench assignments

        Side Effects:
            - Logs lineup optimization start and completion
            - Logs total projected points for optimal lineup
        """
        self.logger.debug(
            f"Optimizing starting lineup for Week {self.config.current_nfl_week} "
            f"({self.config.nfl_scoring_format.upper()} scoring)"
        )
        self.logger.debug(f"Roster size: {len(self.player_manager.team.roster)} players")

        max_weekly = self.player_manager.calculate_max_weekly_projection(self.config.current_nfl_week)
        self.player_manager.scoring_calculator.max_weekly_projection = max_weekly

        scored_players = []
        for player in self.player_manager.team.roster:
            recommendation = self.create_starting_recommendation(player)
            scored_players.append(recommendation)

            self.logger.debug(
                f"Scored {player.name} ({player.position}): {recommendation.score:.2f} pts"
            )

        lineup = OptimalLineup(scored_players)

        starters = lineup.get_all_starters()
        starter_names = [
            f"{s.player.position}:{s.player.name}({s.score:.1f})"
            for s in starters if s is not None
        ]
        self.logger.debug(f"Optimal starters: {', '.join(starter_names)}")

        self.logger.debug(
            f"Lineup optimization complete. Total projected points: {lineup.total_projected_points:.1f}, "
            f"Bench: {len(lineup.bench)} players"
        )
        return lineup


    def print_player_list(self, player_list : List[Tuple[str, Optional[ScoredPlayer]]]):
        """
        Print formatted list of players with position labels and scores.

        Displays each player in numbered list format with position label,
        player information (from ScoredPlayer.__str__), and projected points.
        Handles empty slots by printing "No available player".

        Args:
            player_list (List[Tuple[str, Optional[ScoredPlayer]]]): List of
                (position_label, scored_player) tuples to display

        Side Effects:
            - Prints formatted player list to console
            - Prints separator line after list
        """
        filled_slots = sum(1 for _, p in player_list if p is not None)
        self.logger.debug(f"Displaying {filled_slots}/{len(player_list)} filled positions")

        for i, (pos_label, recommendation) in enumerate(player_list, 1):
            if recommendation:
                print(f"{i:2d}. {pos_label:4s}: {recommendation}")
            else:
                print(f"{i:2d}. {pos_label:4s}: No available player")

        print(f"{'-'*50}")
        