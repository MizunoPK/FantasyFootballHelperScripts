"""
Reserve Assessment Mode Manager

Identifies high-value reserve/waiver players worth monitoring based on
historical performance. Players are scored using a 5-factor algorithm combining
historical data with current season projections.

Author: Kai Mizuno
"""

import csv
import statistics
from pathlib import Path
from typing import Dict, List, Tuple, Optional

import sys
sys.path.append(str(Path(__file__).parent.parent))
from util.ConfigManager import ConfigManager
from util.PlayerManager import PlayerManager
from util.TeamDataManager import TeamDataManager
from util.SeasonScheduleManager import SeasonScheduleManager
from util.ScoredPlayer import ScoredPlayer
import constants as Constants

sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger


class ReserveAssessmentModeManager:
    """
    Manager for Reserve Assessment mode.

    This mode identifies undrafted players on injury reserve who have high
    potential value based on their historical performance. Uses a 5-factor
    scoring algorithm:
    1. Normalization (historical season points)
    2. Player Rating Multiplier (historical rating)
    3. Team Quality Multiplier (current team rank)
    4. Performance/Consistency Multiplier (historical weekly variance)
    5. Schedule Strength Multiplier (current season schedule)

    Attributes:
        config (ConfigManager): Configuration manager
        player_manager (PlayerManager): Player data manager
        team_data_manager (TeamDataManager): Team rankings manager
        season_schedule_manager (SeasonScheduleManager): Schedule data manager
        data_folder (Path): Path to data directory
        historical_players_dict (Dict): Historical player data indexed by (name, position)
        logger: Logger instance
    """

    def __init__(
        self,
        config: ConfigManager,
        player_manager: PlayerManager,
        team_data_manager: TeamDataManager,
        season_schedule_manager: SeasonScheduleManager,
        data_folder: Path
    ):
        """
        Initialize Reserve Assessment Mode Manager.

        Args:
            config: ConfigManager instance
            player_manager: PlayerManager instance
            team_data_manager: TeamDataManager instance
            season_schedule_manager: SeasonScheduleManager instance
            data_folder: Path to data directory

        Side Effects:
            Loads historical player data from data/last_season/players.csv
        """
        self.config = config
        self.player_manager = player_manager
        self.team_data_manager = team_data_manager
        self.season_schedule_manager = season_schedule_manager
        self.data_folder = data_folder
        self.logger = get_logger()

        # Load historical data once at initialization
        self.logger.debug("Loading historical player data for Reserve Assessment mode")
        self.historical_players_dict = self._load_historical_data()
        self.logger.info(
            f"Reserve Assessment mode initialized with {len(self.historical_players_dict)} "
            f"historical players"
        )

    def set_managers(self, player_manager: PlayerManager, team_data_manager: TeamDataManager):
        """
        Update manager references with fresh instances.

        This ensures the mode always works with the latest reloaded data.

        Args:
            player_manager: Updated PlayerManager instance
            team_data_manager: Updated TeamDataManager instance
        """
        self.player_manager = player_manager
        self.team_data_manager = team_data_manager

    def start_interactive_mode(
        self,
        player_manager: PlayerManager,
        team_data_manager: TeamDataManager
    ):
        """
        Main entry point for Reserve Assessment mode.

        Displays high-value reserve candidates and returns to main menu.
        This is a view-only mode - no player selection or modification.

        Args:
            player_manager: Current PlayerManager instance
            team_data_manager: Current TeamDataManager instance
        """
        # Update manager references with fresh data
        self.set_managers(player_manager, team_data_manager)

        self.logger.info("Starting Reserve Assessment interactive mode")

        # Get reserve recommendations
        recommendations = self.get_recommendations()

        # Display header
        print("\n" + "=" * 70)
        print("RESERVE ASSESSMENT - High-Value Injured Players")
        print("=" * 70)

        if not recommendations:
            print("\nNo reserve candidates found.")
            print("(No undrafted players currently on injury reserve with historical data)")
        else:
            print(f"\nFound {len(recommendations)} reserve candidates on injury reserve:")
            print("(Ranked by potential value based on historical performance)\n")

            # Display each recommendation
            for i, scored_player in enumerate(recommendations, 1):
                print(f"{i}. {scored_player}")

        # Wait for user to return to menu
        input("\nPress Enter to return to Main Menu...")
        self.logger.info("Exiting Reserve Assessment mode")

    def get_recommendations(self) -> List[ScoredPlayer]:
        """
        Generate list of top reserve recommendations.

        Filters for undrafted players on injury reserve, matches them to
        historical data, scores them using the 5-factor algorithm, and
        returns the top 15 candidates.

        Returns:
            List of top 15 ScoredPlayer objects, sorted by score descending.
            Returns empty list if no eligible candidates found.

        Example:
            >>> recommendations = manager.get_recommendations()
            >>> for sp in recommendations:
            ...     print(f"{sp.player.name}: {sp.score:.1f} pts")
        """
        self.logger.debug("Getting reserve recommendations")

        # Step 1: Get all free agent players
        # NOTE: Access players directly instead of using get_player_list() to bypass
        # score filtering. Injured players have negative scores due to injury penalties,
        # but we want to include them for Reserve Assessment custom scoring.
        free_agent_players = [
            player for player in self.player_manager.players
            if player.is_free_agent()
        ]
        self.logger.debug(f"Found {len(free_agent_players)} free agent players")

        # Step 2: Filter for high-risk injured players (eligible positions only)
        high_risk_injured = [
            player for player in free_agent_players
            if player.get_risk_level() == "HIGH"  # INJURY_RESERVE, SUSPENSION, UNKNOWN
            and player.position not in ["K", "DST"]
            and player.fantasy_points > 0
        ]
        self.logger.debug(
            f"Found {len(high_risk_injured)} high-risk injured players "
            f"(free agent, IR, non-K/DST, >0 pts)"
        )

        # Step 3: Match to historical data and score
        scored_players = []
        skipped_count = 0

        for current_player in high_risk_injured:
            # Match by (name, position) - ignoring team to catch team changers
            key = (current_player.name.lower(), current_player.position)
            historical_player = self.historical_players_dict.get(key)

            if historical_player is None:
                # No historical data - skip (rookies, or not in last season's system)
                self.logger.debug(
                    f"No historical data for {current_player.name} ({current_player.position}), skipping"
                )
                skipped_count += 1
                continue

            # Score the reserve candidate
            scored_player = self._score_reserve_candidate(current_player, historical_player)
            scored_players.append(scored_player)

        self.logger.info(
            f"Scored {len(scored_players)} reserve candidates "
            f"(skipped {skipped_count} without historical data)"
        )

        # Step 4: Sort by score and return top 15
        scored_players.sort(key=lambda sp: sp.score, reverse=True)
        top_recommendations = scored_players[:15]

        self.logger.debug(
            f"Returning top {len(top_recommendations)} recommendations "
            f"(from {len(scored_players)} total)"
        )

        return top_recommendations

    def _load_historical_data(self) -> Dict[Tuple[str, str], FantasyPlayer]:
        """
        Load historical player data from last season.

        Loads player data from data/last_season/players.csv and creates a
        dictionary indexed by (name.lower(), position) for fast lookup.

        Returns:
            Dictionary mapping (name, position) tuples to FantasyPlayer objects.
            Returns empty dict if file not found or error occurs.

        Side Effects:
            Logs warnings if file not found or errors occur during loading.
        """
        historical_players_dict = {}
        historical_file = self.data_folder / 'last_season' / 'players.csv'

        try:
            if not historical_file.exists():
                self.logger.warning(
                    f"Historical player data not found: {historical_file}. "
                    f"Reserve Assessment will return no results."
                )
                return historical_players_dict

            with open(str(historical_file), newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                # Validate required columns
                required_columns = ['id', 'name', 'team', 'position', 'fantasy_points', 'player_rating']
                if not all(col in reader.fieldnames for col in required_columns):
                    missing = [col for col in required_columns if col not in reader.fieldnames]
                    self.logger.error(
                        f"Historical player CSV missing required columns: {missing}"
                    )
                    return historical_players_dict

                # Load each player
                for row_num, row in enumerate(reader, start=2):
                    try:
                        player = FantasyPlayer.from_dict(row)

                        # Validate player data
                        if not player.name:
                            self.logger.warning(
                                f"Empty player name in historical data row {row_num}, skipping"
                            )
                            continue

                        # Index by (name.lower(), position) for matching
                        # This ignores team to catch players who changed teams
                        key = (player.name.lower(), player.position)
                        historical_players_dict[key] = player

                    except Exception as e:
                        self.logger.warning(
                            f"Error loading historical player row {row_num}: {e}, skipping"
                        )
                        continue

                self.logger.debug(
                    f"Loaded {len(historical_players_dict)} players from historical data"
                )

        except Exception as e:
            self.logger.error(f"Error loading historical player data: {e}")

        return historical_players_dict

    def _score_reserve_candidate(
        self,
        current_player: FantasyPlayer,
        historical_player: FantasyPlayer
    ) -> ScoredPlayer:
        """
        Score a reserve candidate using 5-factor algorithm.

        Combines historical performance data with current season context to
        calculate a potential value score. All multipliers are optional - if
        data is missing, that factor is skipped gracefully.

        Scoring Factors:
        1. Base Score: Historical season total points
        2. Player Rating: Historical player rating multiplier
        3. Team Quality: Current team's offensive/defensive rank multiplier
        4. Performance: Historical weekly consistency multiplier
        5. Schedule: Current season strength of schedule multiplier

        Args:
            current_player: Current season player data (team, position, injury_status)
            historical_player: Last season player data (points, rating, weekly data)

        Returns:
            ScoredPlayer object with final score and list of scoring reasons.

        Example:
            >>> scored = manager._score_reserve_candidate(current, historical)
            >>> print(scored.score)  # 287.5
            >>> print(scored.reason)  # ['Base: 245.0 pts', 'Player Rating: GOOD (1.15x)', ...]
        """
        reasons = []

        # Factor 1: Normalization - Base score from historical season points
        score = historical_player.fantasy_points
        reasons.append(f"Base: {score:.1f} pts (last season)")

        # Factor 2: Player Rating Multiplier (historical)
        if historical_player.player_rating:
            multiplier, rating = self.config.get_player_rating_multiplier(
                historical_player.player_rating
            )
            score *= multiplier
            reasons.append(f"Player Rating: {rating} ({multiplier:.2f}x)")

        # Factor 3: Team Quality Multiplier (current season)
        # Use offensive rank for offensive players, defensive rank for DST
        if current_player.position in Constants.DEFENSE_POSITIONS:
            team_rank = self.team_data_manager.get_team_defensive_rank(current_player.team)
        else:
            team_rank = self.team_data_manager.get_team_offensive_rank(current_player.team)

        if team_rank:
            multiplier, rating = self.config.get_team_quality_multiplier(team_rank)
            score *= multiplier
            reasons.append(f"Team Quality: {rating} (rank {team_rank}, {multiplier:.2f}x)")

        # Factor 4: Performance/Consistency Multiplier (historical weekly data)
        # UPDATED for Sub-feature 2: Use hybrid weekly data access
        weekly_points = []
        for week in range(1, 18):  # All 17 weeks
            points = historical_player.get_single_weekly_projection(week, self.config)
            if points is not None and float(points) > 0:
                weekly_points.append(float(points))

        if len(weekly_points) >= 3:  # Minimum weeks threshold
            mean_points = statistics.mean(weekly_points)
            std_dev = statistics.stdev(weekly_points) if len(weekly_points) > 1 else 0.0
            cv = std_dev / mean_points if mean_points > 0 else 0.0

            # Get performance multiplier based on coefficient of variation
            multiplier, rating = self.config.get_performance_multiplier(cv)
            score *= multiplier
            reasons.append(f"Performance: {rating} ({multiplier:.2f}x)")

        # Factor 5: Schedule Multiplier (current season)
        schedule_value = self._calculate_schedule_value(current_player)
        if schedule_value is not None:
            multiplier, rating = self.config.get_schedule_multiplier(schedule_value)
            score *= multiplier
            reasons.append(
                f"Schedule: {rating} (avg opp def rank: {schedule_value:.1f}, {multiplier:.2f}x)"
            )

        return ScoredPlayer(player=current_player, score=score, reasons=reasons)

    def _calculate_schedule_value(self, player: FantasyPlayer) -> Optional[float]:
        """
        Calculate schedule strength value based on future opponents.

        Gets the player's team's future opponents and calculates the average
        defensive rank against the player's position. Higher rank means easier
        schedule (facing worse defenses).

        Args:
            player: Player to calculate schedule for

        Returns:
            Average defense rank of future opponents (1-32), or None if:
            - No future opponents (end of season)
            - Less than 2 future games (insufficient data)

        Example:
            >>> value = manager._calculate_schedule_value(player)
            >>> if value:
            ...     print(f"Avg opponent defense rank: {value:.1f}")  # 18.5
        """
        # Get future opponents for the player's team
        future_opponents = self.season_schedule_manager.get_future_opponents(
            player.team,
            self.config.current_nfl_week
        )

        if not future_opponents:
            self.logger.debug(f"{player.name}: No future opponents (end of season)")
            return None

        # Get position-specific defense ranks for each opponent
        defense_ranks = []
        for opponent in future_opponents:
            rank = self.team_data_manager.get_team_defense_vs_position_rank(
                opponent,
                player.position
            )
            if rank is not None:
                defense_ranks.append(rank)

        # Require minimum 2 future games for reliable calculation
        if len(defense_ranks) < 2:
            self.logger.debug(
                f"{player.name}: Insufficient future games ({len(defense_ranks)}) "
                f"for schedule calculation"
            )
            return None

        # Calculate and return average defense rank
        avg_rank = sum(defense_ranks) / len(defense_ranks)
        self.logger.debug(
            f"{player.name}: {len(defense_ranks)} future games, "
            f"avg defense rank: {avg_rank:.1f}"
        )

        return avg_rank
