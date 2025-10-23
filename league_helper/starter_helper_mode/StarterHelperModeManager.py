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

from pathlib import Path
from typing import List, Tuple, Optional
import sys

sys.path.append(str(Path(__file__).parent))
import constants as Constants

sys.path.append(str(Path(__file__).parent.parent))
from util.ConfigManager import ConfigManager
from util.PlayerManager import PlayerManager
from util.TeamDataManager import TeamDataManager
from util.ScoredPlayer import ScoredPlayer

sys.path.append(str(Path(__file__).parent.parent.parent))
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
        # Initialize all starting positions to None (unfilled slots)
        # IMPORTANT: Must initialize bench in __init__ to avoid sharing list across instances
        # Python class variables are shared, so we explicitly create instance variables
        self.qb: Optional[ScoredPlayer] = None
        self.rb1: Optional[ScoredPlayer] = None
        self.rb2: Optional[ScoredPlayer] = None
        self.wr1: Optional[ScoredPlayer] = None
        self.wr2: Optional[ScoredPlayer] = None
        self.te: Optional[ScoredPlayer] = None
        self.flex: Optional[ScoredPlayer] = None  # Can be filled by RB or WR (NOT TE or DST)
        self.k: Optional[ScoredPlayer] = None
        self.dst: Optional[ScoredPlayer] = None
        self.bench: List[ScoredPlayer] = []  # Must be instance variable, not class variable

        # Sort players by score in descending order (highest scores first)
        # This ensures we assign the best players to starting slots before bench overflow
        # For example: If we have 3 RBs scoring 20, 18, 15 - they'll fill RB1, RB2, FLEX in that order
        scored_players.sort(key=lambda x: x.score, reverse=True)

        # Iterate through sorted players and assign to optimal starting positions
        # Assignment logic:
        # 1. Fill dedicated position slots first (QB, RB1/RB2, WR1/WR2, TE, K, DST)
        # 2. Then fill FLEX with remaining RB/WR (highest scoring flex-eligible player)
        # 3. Overflow players go to bench
        for scored_player in scored_players:
            player = scored_player.player

            # QB: Only 1 starting slot, overflow to bench
            if player.position == Constants.QB:
                if self.qb is None:
                    self.qb = scored_player  # Assign first (highest-scoring) QB to starter
                else:
                    self.bench.append(scored_player)  # 2nd+ QB goes to bench

            # RB: 2 dedicated slots (RB1, RB2) + eligible for FLEX (3rd RB can start)
            elif player.position == Constants.RB:
                if self.rb1 is None:
                    self.rb1 = scored_player  # Highest-scoring RB → RB1
                elif self.rb2 is None:
                    self.rb2 = scored_player  # 2nd RB → RB2
                elif self.flex is None:
                    # 3rd RB can fill FLEX if unfilled (RB/WR compete for FLEX by score)
                    self.flex = scored_player
                else:
                    # 4th+ RB goes to bench (RB1, RB2, FLEX all filled)
                    self.bench.append(scored_player)

            # WR: 2 dedicated slots (WR1, WR2) + eligible for FLEX (3rd WR can start)
            elif player.position == Constants.WR:
                if self.wr1 is None:
                    self.wr1 = scored_player  # Highest-scoring WR → WR1
                elif self.wr2 is None:
                    self.wr2 = scored_player  # 2nd WR → WR2
                elif self.flex is None:
                    # 3rd WR can fill FLEX if unfilled (RB/WR compete for FLEX by score)
                    self.flex = scored_player
                else:
                    # 4th+ WR goes to bench (WR1, WR2, FLEX all filled)
                    self.bench.append(scored_player)

            # TE: Only 1 starting slot, NOT eligible for FLEX in this league format
            elif player.position == Constants.TE:
                if self.te is None:
                    self.te = scored_player  # Assign first TE to starter
                else:
                    # 2nd+ TE goes to bench (cannot fill FLEX)
                    self.bench.append(scored_player)

            # DST: Only 1 starting slot, NOT eligible for FLEX in this league format
            elif player.position == Constants.DST:
                if self.dst is None:
                    self.dst = scored_player  # Assign first DST to starter
                else:
                    # 2nd+ DST goes to bench (cannot fill FLEX)
                    self.bench.append(scored_player)

            # K: Only 1 starting slot, overflow to bench
            elif player.position == Constants.K:
                if self.k is None:
                    self.k = scored_player  # Assign first K to starter
                else:
                    self.bench.append(scored_player)  # 2nd+ K goes to bench

            # Unknown position: Send directly to bench
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

    # ========================================================================
    # INITIALIZATION
    # ========================================================================

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
        self.logger.debug("Initializing Starter Helper Mode Manager")
        self.set_managers(player_manager, team_data_manager)

    # ========================================================================
    # MANAGER SETUP
    # ========================================================================

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

    # ========================================================================
    # PUBLIC INTERFACE METHODS
    # ========================================================================

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

        # Update manager references to ensure we have latest roster data
        # This is important if user made changes in another mode
        self.set_managers(player_manager, team_data_manager)

        # Optimize lineup: score all roster players using weekly projections
        # and assign best players to starting slots (QB, RB1/2, WR1/2, TE, FLEX, K, DST)
        lineup = self.optimize_lineup()

        # Display the starting lineup header with current week and scoring format
        # Format example: "OPTIMAL STARTING LINEUP - WEEK 8 (PPR SCORING)"
        print(f"\n{'='*50}")
        print(f"OPTIMAL STARTING LINEUP - WEEK {self.config.current_nfl_week} ({self.config.nfl_scoring_format.upper()} SCORING)")
        print(f"{'='*50}")

        # Create list of starting positions in display order
        # Each tuple is (position_label, scored_player)
        # Position labels are simplified for display (e.g., "DEF" instead of "DST")
        starter_positions = [
            ("QB", lineup.qb),
            ("RB", lineup.rb1),
            ("RB", lineup.rb2),
            ("WR", lineup.wr1),
            ("WR", lineup.wr2),
            ("TE", lineup.te),
            ("FLEX", lineup.flex),  # Can be RB or WR (highest scoring flex-eligible)
            ("K", lineup.k),
            ("DEF", lineup.dst)  # Display as "DEF" instead of "DST" for brevity
        ]
        # Bench players don't need position labels (empty string)
        bench_positions = [("", x) for x in lineup.bench]

        # Print starting lineup with formatted player information
        # Each line shows: position label, player name, team, projected points, scoring reasons
        self.print_player_list(starter_positions)

        # Display bench section
        print(f"\n{'='*50}")
        print(f"BENCH")
        print(f"{'='*50}")
        self.print_player_list(bench_positions)

        # Wait for user acknowledgment before returning to main menu
        # This prevents lineup from disappearing immediately
        input("Press Enter to Continue...")

        self.logger.info(f"Exiting Starter Helper mode (Total projected: {lineup.total_projected_points:.1f} pts)")

    # ========================================================================
    # LINEUP OPTIMIZATION HELPERS
    # ========================================================================

    def create_starting_recommendation(self,
                                     player_data: FantasyPlayer) -> ScoredPlayer:
        """
        Create a ScoredPlayer using weekly projection scoring.

        This method scores a player specifically for weekly lineup decisions,
        using weekly projections instead of seasonal projections and enabling
        only performance and matchup multipliers (not ADP, rating, or team quality).

        Scoring configuration:
        - use_weekly_projection=True: Use week-specific projection data
        - performance=True: Apply actual vs projected performance adjustment
        - matchup=True: Apply opponent defensive strength adjustment (THIS WEEK)
        - schedule=False: Don't use future schedule strength (irrelevant for weekly)
        - adp=False: Don't use draft position (irrelevant for in-season)
        - player_rating=False: Don't use expert ratings (irrelevant for weekly)
        - team_quality=False: Don't use team rankings (irrelevant for weekly)

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
            team_quality=False,
            performance=True,
            matchup=True,
            schedule=False,  # EXPLICIT: No schedule scoring for weekly decisions
            bye=False,
            injury=False
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
        # Log optimization start with week and scoring format context
        # This helps debug lineup decisions and track optimization runs
        self.logger.debug(
            f"Optimizing starting lineup for Week {self.config.current_nfl_week} "
            f"({self.config.nfl_scoring_format.upper()} scoring)"
        )
        self.logger.debug(f"Roster size: {len(self.player_manager.team.roster)} players")

        # Score all rostered players using weekly projections and performance/matchup adjustments
        # This uses use_weekly_projection=True (NOT seasonal projections)
        # Scoring factors: performance=True, matchup=True (ADP/rating/team_quality disabled for weekly)
        scored_players = []
        for player in self.player_manager.team.roster:
            # Create ScoredPlayer with weekly projection score
            # Each player gets a score based on:
            # - Weekly projected fantasy points (base score)
            # - Performance multiplier (recent actual vs projected)
            # - Matchup multiplier (opponent defensive strength)
            recommendation = self.create_starting_recommendation(player)
            scored_players.append(recommendation)

            # Log each player's calculated score for debugging
            # Format: "Scored Patrick Mahomes (QB): 25.50 pts"
            self.logger.debug(
                f"Scored {player.name} ({player.position}): {recommendation.score:.2f} pts"
            )

        # Create OptimalLineup which automatically:
        # 1. Sorts players by score (highest first)
        # 2. Assigns players to optimal starting positions
        # 3. Handles FLEX logic (RB/WR compete for 3rd flex slot)
        # 4. Sends overflow players to bench
        lineup = OptimalLineup(scored_players)

        # Log the final starting lineup composition for debugging
        # Format: "QB:Patrick Mahomes(25.5), RB:Christian McCaffrey(22.3), ..."
        starters = lineup.get_all_starters()
        starter_names = [
            f"{s.player.position}:{s.player.name}({s.score:.1f})"
            for s in starters if s is not None
        ]
        self.logger.debug(f"Optimal starters: {', '.join(starter_names)}")

        # Log optimization completion with total projected points and bench size
        # Total points = sum of all starter scores (bench excluded)
        self.logger.debug(
            f"Lineup optimization complete. Total projected points: {lineup.total_projected_points:.1f}, "
            f"Bench: {len(lineup.bench)} players"
        )
        return lineup

    # ========================================================================
    # DISPLAY HELPERS
    # ========================================================================

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
        # Log the number of players being displayed (helps debug display issues)
        filled_slots = sum(1 for _, p in player_list if p is not None)
        self.logger.debug(f"Displaying {filled_slots}/{len(player_list)} filled positions")

        for i, (pos_label, recommendation) in enumerate(player_list, 1):
            if recommendation:
                print(f"{i:2d}. {pos_label:4s}: {recommendation}")
            else:
                print(f"{i:2d}. {pos_label:4s}: No available player")

        print(f"{'-'*50}")
        