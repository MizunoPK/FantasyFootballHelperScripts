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
Date: 2025-10-10
"""

from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass
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
    qb: Optional[ScoredPlayer] = None
    rb1: Optional[ScoredPlayer] = None
    rb2: Optional[ScoredPlayer] = None
    wr1: Optional[ScoredPlayer] = None
    wr2: Optional[ScoredPlayer] = None
    te: Optional[ScoredPlayer] = None
    flex: Optional[ScoredPlayer] = None
    k: Optional[ScoredPlayer] = None
    dst: Optional[ScoredPlayer] = None
    bench: List[ScoredPlayer] = []

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
        # Sort by adjusted score (highest first)
        scored_players.sort(key=lambda x: x.score, reverse=True)

        # Iterate through the players and assign to starting positions or bench
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

    def get_all_starters(self) -> List[Optional[ScoredPlayer]]:
        """Get all starting recommendations in order"""
        return [self.qb, self.rb1, self.rb2, self.wr1, self.wr2,
                self.te, self.flex, self.k, self.dst]


class StarterHelperModeManager:
    """
    Manages the Starter Helper mode workflow and lineup optimization.

    This class coordinates weekly lineup optimization by scoring roster players
    using weekly projections and assembling the highest-scoring starting lineup.
    It uses consistency and matchup multipliers to refine weekly projections.

    Scoring Parameters (for weekly lineups):
    - use_weekly_projection=True: Uses week-specific projections, not seasonal
    - consistency=True: Adjusts for player volatility/reliability
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
        self.player_manager = player_manager
        self.config = config
        self.logger = get_logger()
        self.logger.debug("Initializing Starter Helper Mode Manager")
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
        self.set_managers(player_manager, team_data_manager)

        # Optimize lineup based on weekly projections
        lineup = self.optimize_lineup()

        # Display the starting lineup header
        print(f"\n{'='*50}")
        print(f"OPTIMAL STARTING LINEUP - WEEK {self.config.current_nfl_week} ({self.config.nfl_scoring_format.upper()} SCORING)")
        print(f"{'='*50}")
        print(f"\n{'='*50}")
        print(f"OPTIMAL STARTING LINEUP - WEEK {self.config.current_nfl_week} ({self.config.nfl_scoring_format.upper()} SCORING)")
        print(f"{'='*50}")

        # Define the order to display starters (as requested)
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

        print(f"\n{'='*50}")
        print(f"BENCH")
        print(f"{'='*50}")
        self.print_player_list(bench_positions)
        
        input("Press Enter to Continue...")

    def create_starting_recommendation(self,
                                     player_data: FantasyPlayer) -> ScoredPlayer:
        """
        Create a ScoredPlayer from player data

        Returns:
            ScoredPlayer object
        """

        scored_player = self.player_manager.score_player(player_data, use_weekly_projection=True, adp=False, player_rating=False, team_quality=False, consistency=True, matchup=True)

        return scored_player

    def optimize_lineup(self) -> OptimalLineup:
        """
        Optimize starting lineup based on current week projections

        Args:
            roster_players: DataFrame of roster players (drafted=2)
            projections: Dictionary mapping player_id to current week projections

        Returns:
            OptimalLineup object with best recommendations for each position
        """
        self.logger.info("Optimizing starting lineup for current week")

        scored_players = []
        for player in self.player_manager.team.roster:
            recommendation = self.create_starting_recommendation(
                player
            )
            scored_players.append(recommendation)

        # Iterate through the players and compile the lineup and bench
        lineup = OptimalLineup(scored_players)

        self.logger.info(f"Lineup optimization complete. Total projected points: {lineup.total_projected_points:.1f}")
        return lineup
    
    def print_player_list(self, player_list : List[ScoredPlayer]):
        for i, (pos_label, recommendation) in enumerate(player_list, 1):
            if recommendation:
                print(f"{i:2d}. {pos_label:4s}: {recommendation}")

            else:
                print(f"{i:2d}. {pos_label:4s}: No available player")

        print(f"{'-'*50}")
        