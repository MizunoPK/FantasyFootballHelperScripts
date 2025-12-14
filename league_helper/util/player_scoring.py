"""
Player Scoring Calculator

Helper class for calculating player scores using the 10-step scoring algorithm.
Handles all scoring-related calculations including normalization, multipliers,
bonuses, and penalties.

The 10-step scoring algorithm:
1. Normalization (based on fantasy_points projection)
2. ADP Multiplier (market wisdom adjustment)
3. Player Rating Multiplier (expert consensus)
4. Team Quality Multiplier (offensive/defensive strength)
5. Performance Multiplier (actual vs projected deviation)
6. Matchup Bonus/Penalty (opponent strength)
7. Schedule Bonus/Penalty (future opponent strength)
8. Draft Order Bonus (positional value by round)
9. Bye Week Penalty (same-position and different-position roster conflicts)
10. Injury Penalty (risk assessment)

Author: Kai Mizuno
"""

import statistics
from typing import Tuple, Optional, List, Dict
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).parent))
import constants as Constants
from ConfigManager import ConfigManager
from ScoredPlayer import ScoredPlayer
from ProjectedPointsManager import ProjectedPointsManager
from TeamDataManager import TeamDataManager
from SeasonScheduleManager import SeasonScheduleManager
from GameDataManager import GameDataManager
from upcoming_game_model import UpcomingGame

sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger


class PlayerScoringCalculator:
    """
    Calculator for player scoring using the 10-step algorithm.

    Handles all scoring calculations including normalization, multipliers,
    bonuses, and penalties. Separated from PlayerManager to improve
    organization and testability.

    Attributes:
        config (ConfigManager): Configuration manager for scoring parameters
        projected_points_manager (ProjectedPointsManager): Manager for projected points
        max_projection (float): Maximum fantasy points projection for normalization
        team_data_manager (TeamDataManager): Manager for team rankings and matchups
        season_schedule_manager (SeasonScheduleManager): Manager for season schedule data
        current_nfl_week (int): Current NFL week number
        logger: Logger instance
    """

    def __init__(
        self,
        config: ConfigManager,
        projected_points_manager: ProjectedPointsManager,
        max_projection: float,
        team_data_manager: TeamDataManager,
        season_schedule_manager: SeasonScheduleManager,
        current_nfl_week: int,
        game_data_manager: Optional[GameDataManager] = None
    ) -> None:
        """
        Initialize PlayerScoringCalculator.

        Args:
            config (ConfigManager): Configuration manager with scoring parameters
            projected_points_manager (ProjectedPointsManager): Manager for projected points
            max_projection (float): Maximum fantasy points projection for normalization
            team_data_manager (TeamDataManager): Manager for team rankings and matchups
            season_schedule_manager (SeasonScheduleManager): Manager for season schedule data
            current_nfl_week (int): Current NFL week number
            game_data_manager (Optional[GameDataManager]): Manager for game conditions
                (temperature, wind, location). If None, game condition scoring is disabled.
        """
        self.config = config
        self.projected_points_manager = projected_points_manager
        self.max_projection = max_projection
        self.max_weekly_projection: float = 0.0  # Current weekly max for normalization
        self.team_data_manager = team_data_manager
        self.season_schedule_manager = season_schedule_manager
        self.current_nfl_week = current_nfl_week
        self.game_data_manager = game_data_manager
        self.logger = get_logger()

    def get_weekly_projection(self, player: FantasyPlayer, week=0) -> Tuple[float, float]:
        """
        Get weekly projection for a specific player and week.

        This method retrieves the projected fantasy points for a player in a specific week
        and calculates the normalized/weighted projection using the same scale as seasonal
        projections (0-N scale based on normalization_max_scale).

        Args:
            player (FantasyPlayer): Player to get projection for
            week (int): NFL week number (1-17). If 0 or outside valid range, uses current_nfl_week

        Returns:
            Tuple[float, float]: (original_points, weighted_points)
                - original_points: Raw fantasy points projection for the week
                - weighted_points: Normalized projection (0-N scale) calculated as
                  (weekly_points / max_projection) * normalization_max_scale
                - Returns (0.0, 0.0) if no valid projection data exists

        Example:
            >>> orig_pts, weighted_pts = calculator.get_weekly_projection(player, week=5)
            >>> print(f"Week 5 projection: {orig_pts:.1f} pts (normalized: {weighted_pts:.1f})")
        """
        # If week isn't in the valid range (1-17), use current week from config
        if week not in range(1, 18):
            week = self.config.current_nfl_week

        weekly_points = player.get_single_weekly_projection(week)
        if weekly_points is not None and float(weekly_points) > 0:
            weekly_points = float(weekly_points)
            # Calculate normalized/weighted projection using weekly max for normalization
            # This uses use_weekly_max=True to normalize against the week's top projection
            weighted_projection = self.weight_projection(weekly_points, use_weekly_max=True)
            self.logger.debug(
                f"Week {week} projection for {player.name}: {weekly_points:.2f} pts "
                f"(weighted: {weighted_projection:.2f})"
            )
            return weekly_points, weighted_projection

        # Return zeros if no valid projection found
        self.logger.debug(
            f"No valid projection data for {player.name} in week {week}"
        )
        return 0.0, 0.0

    def weight_projection(self, pts: float, use_weekly_max: bool = False) -> float:
        """
        Calculate weighted projection using normalization scale.

        Args:
            pts (float): Raw fantasy points
            use_weekly_max (bool): If True, use max_weekly_projection for normalization.
                                   If False, use max_projection (ROS). Default: False.

        Returns:
            float: Weighted projection (0-N scale)
        """
        # Choose which max to use for normalization
        chosen_max = self.max_weekly_projection if use_weekly_max else self.max_projection

        # Safety check: if max is 0, log warning and return 0.0
        if chosen_max == 0:
            self.logger.warning(
                f"Max projection is 0.0 ({'weekly' if use_weekly_max else 'ROS'}), "
                f"returning 0.0 normalized score (data quality issue)"
            )
            return 0.0

        # Calculate normalized score
        normalized_score = (pts / chosen_max) * self.config.normalization_max_scale

        # Debug logging
        self.logger.debug(
            f"Normalization: {pts:.2f} pts / {chosen_max:.2f} ({'weekly' if use_weekly_max else 'ROS'} max) "
            f"* {self.config.normalization_max_scale} = {normalized_score:.2f}"
        )

        return normalized_score

    def calculate_performance_deviation(self, player: FantasyPlayer) -> Optional[float]:
        """
        Calculate performance deviation for a player based on actual vs projected points.

        Measures how much a player's actual performance deviates from projected points
        across recent weeks using dynamic lookback. Positive deviation = outperforming,
        negative = underperforming.

        Formula: average((actual - projected) / projected) for valid weeks

        Dynamic Lookback Logic:
        - Looks back from current_week - 1 to find MIN_WEEKS valid (non-zero) weeks
        - Skips bye weeks and injury weeks (actual = 0) automatically
        - Maximum lookback limit: 2 * MIN_WEEKS weeks to ensure data freshness
        - Returns None if MIN_WEEKS valid weeks cannot be found within the limit

        Skipping criteria:
        - Weeks where actual points = 0 (player didn't play - bye/injury)
        - Weeks where projected = 0.0 (no projection data available)
        - DST position players (insufficient historical projection data)

        Args:
            player: FantasyPlayer object with weekly projection and actual data

        Returns:
            Optional[float]: Average performance deviation as a percentage (e.g., 0.15 = +15%)
                           Returns None if insufficient data or DST position
        """
        # Skip DST teams - insufficient historical projection data
        if player.position == 'DST':
            self.logger.debug(f"Skipping performance calculation for DST player: {player.name}")
            return None

        # Get MIN_WEEKS for minimum valid weeks requirement
        min_weeks = self.config.performance_scoring[self.config.keys.MIN_WEEKS]

        # Calculate maximum lookback limit (2x MIN_WEEKS for data freshness)
        max_lookback = min_weeks * 2
        earliest_week = max(1, self.config.current_nfl_week - max_lookback)

        # Collect performance deviations using dynamic lookback
        # Start from most recent completed week and work backwards
        deviations = []
        week = self.config.current_nfl_week - 1

        while len(deviations) < min_weeks and week >= earliest_week:
            # Get actual points from player object
            week_attr = f'week_{week}_points'
            if hasattr(player, week_attr):
                actual_points = getattr(player, week_attr)

                if actual_points is not None:
                    actual_points = float(actual_points)

                    # Skip weeks where player didn't play (actual = 0)
                    # This handles bye weeks and injury weeks automatically
                    if actual_points > 0:
                        # Get projected points from ProjectedPointsManager
                        projected_points = self.projected_points_manager.get_projected_points(player, week)

                        if projected_points is not None and projected_points > 0:
                            # Calculate deviation: (actual - projected) / projected
                            deviation = (actual_points - projected_points) / projected_points
                            deviations.append(deviation)

                            self.logger.debug(
                                f"Week {week} performance for {player.name}: "
                                f"actual={actual_points:.2f}, projected={projected_points:.2f}, "
                                f"deviation={deviation:.3f} ({deviation*100:.1f}%)"
                            )
                        elif projected_points == 0.0:
                            self.logger.debug(
                                f"Skipping week {week} for {player.name}: projected=0.0"
                            )

            week -= 1

        weeks_count = len(deviations)

        # Handle insufficient data (MIN_WEEKS is strict minimum requirement)
        if weeks_count < min_weeks:
            self.logger.debug(
                f"Insufficient performance data for {player.name}: "
                f"{weeks_count} valid weeks found < {min_weeks} required "
                f"(looked back to week {earliest_week})"
            )
            return None

        # Calculate average deviation
        avg_deviation = statistics.mean(deviations)

        self.logger.debug(
            f"Performance deviation for {player.name}: {avg_deviation:.3f} "
            f"({avg_deviation*100:.1f}%) across {weeks_count} weeks"
        )

        return avg_deviation

    def _calculate_schedule_value(self, player: FantasyPlayer) -> Optional[float]:
        """
        Calculate schedule strength value based on future opponents.

        Minimum 2 future games required for calculation.
        End of season returns None.

        Args:
            player: Player to calculate schedule for

        Returns:
            Average defense rank of future opponents (1-32)
            Higher rank = easier schedule (facing worse defenses)
            None if insufficient future games (< 2)
        """
        # Get future opponents
        future_opponents = self.season_schedule_manager.get_future_opponents(
            player.team,
            self.current_nfl_week
        )

        if not future_opponents:
            self.logger.debug(f"{player.name}: No future games (end of season)")
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

        # Require minimum 2 future games
        if len(defense_ranks) < 2:
            self.logger.debug(
                f"{player.name}: Insufficient future games ({len(defense_ranks)}) "
                f"for schedule calculation (minimum 2 required)"
            )
            return None

        # Calculate average defense rank
        avg_rank = sum(defense_ranks) / len(defense_ranks)

        self.logger.debug(
            f"{player.name} schedule: {len(defense_ranks)} future games, "
            f"avg defense rank: {avg_rank:.1f}"
        )

        return avg_rank

    def score_player(self, p: FantasyPlayer, team_roster: List[FantasyPlayer], use_weekly_projection=False, adp=False, player_rating=True, team_quality=True, performance=True, matchup=False, schedule=True, draft_round=-1, bye=True, injury=True, roster: Optional[List[FantasyPlayer]] = None, temperature=False, wind=False, location=False) -> ScoredPlayer:
        """
        Calculate score for a player (13-step calculation).

        Scoring System:
        1. Get normalized seasonal fantasy points (0-N scale)
        2. Apply ADP multiplier
        3. Apply Player Ranking multiplier
        4. Apply Team ranking multiplier
        5. Apply Performance multiplier (actual vs projected deviation)
        6. Apply Matchup multiplier (current week opponent)
        7. Apply Schedule multiplier (future opponents strength)
        8. Add DRAFT_ORDER bonus (round-based position priority)
        9. Subtract Bye Week penalty
        10. Subtract Injury penalty
        11. Apply Temperature bonus/penalty (game conditions)
        12. Apply Wind bonus/penalty (game conditions, QB/WR/K only)
        13. Apply Location bonus/penalty (home/away/international)

        Args:
            p: FantasyPlayer to score
            team_roster: The team's roster (used for bye week calculations)
            use_weekly_projection: Use weekly projection instead of rest-of-season
            adp: Apply ADP multiplier
            player_rating: Apply player rating multiplier
            team_quality: Apply team quality multiplier
            performance: Apply performance multiplier (actual vs projected deviation)
            matchup: Apply matchup multiplier (current week opponent)
            schedule: Apply schedule strength multiplier (future opponents) - DEFAULT TRUE
            draft_round: Draft round for position bonus (-1 to disable)
            bye: Apply bye week penalty
            injury: Apply injury penalty
            roster: Optional custom roster to use for bye week calculations (defaults to team_roster)
            temperature: Apply temperature bonus/penalty (game conditions)
            wind: Apply wind bonus/penalty (game conditions, QB/WR/K only)
            location: Apply location bonus/penalty (home/away/international)

        Returns:
            ScoredPlayer: Scored player object with final score and reasons
        """
        reasons = []
        def add_to_reasons(r: str) -> None:
            if r is not None and r != "":
                reasons.append(r)

        # STEP 1: Normalize seasonal fantasy points to 0-N scale
        player_score, reason = self._get_normalized_fantasy_points(p, use_weekly_projection)
        add_to_reasons(reason)
        self.logger.debug(f"Step 1 - Normalized score for {p.name}: {player_score:.2f}")

        # STEP 2: Apply ADP multiplier
        if adp:
            player_score, reason = self._apply_adp_multiplier(p, player_score)
            add_to_reasons(reason)
            self.logger.debug(f"Step 2 - ADP Enhanced score for {p.name}: {player_score:.2f}")

        # STEP 3: Apply Player Rating multiplier
        if player_rating:
            player_score, reason = self._apply_player_rating_multiplier(p, player_score)
            add_to_reasons(reason)
            self.logger.debug(f"Step 3 - Player Rating Enhanced score for {p.name}: {player_score:.2f}")

        # STEP 4: Apply Team Quality multiplier
        if team_quality:
            player_score, reason = self._apply_team_quality_multiplier(p, player_score)
            add_to_reasons(reason)
            self.logger.debug(f"Step 4 - Team Quality Enhanced score for {p.name}: {player_score:.2f}")

        # STEP 5: Apply Performance multiplier (actual vs projected deviation)
        if performance:
            player_score, reason = self._apply_performance_multiplier(p, player_score)
            add_to_reasons(reason)
            self.logger.debug(f"Step 5 - After performance for {p.name}: {player_score:.2f}")

        # STEP 6: Apply Matchup multiplier
        if matchup:
            player_score, reason = self._apply_matchup_multiplier(p, player_score)
            add_to_reasons(reason)
            self.logger.debug(f"Step 6 - After matchup multiplier for {p.name}: {player_score:.2f}")

        # STEP 7: Apply Schedule multiplier (future opponent difficulty)
        if schedule:
            player_score, reason = self._apply_schedule_multiplier(p, player_score)
            add_to_reasons(reason)
            self.logger.debug(f"Step 7 - After schedule multiplier for {p.name}: {player_score:.2f}")

        # STEP 8: Add DRAFT_ORDER bonus (round-based position priority)
        # BUG FIX: Changed from draft_round > 0 to draft_round >= 0
        # This allows round 0 (first round) to get bonuses, -1 is the disabled flag
        if draft_round >= 0:
            player_score, reason = self._apply_draft_order_bonus(p, draft_round, player_score)
            add_to_reasons(reason)
            self.logger.debug(f"Step 8 - After DRAFT_ORDER bonus for {p.name}: {player_score:.2f}")

        # STEP 9: Subtract Bye Week penalty
        if bye:
            player_score, reason = self._apply_bye_week_penalty(p, player_score, roster if roster is not None else team_roster)
            add_to_reasons(reason)
            self.logger.debug(f"Step 9 - After bye penalty for {p.name}: {player_score:.2f}")

        # STEP 10: Subtract Injury penalty
        if injury:
            player_score, reason = self._apply_injury_penalty(p, player_score)
            add_to_reasons(reason)
            self.logger.debug(f"Step 10 - After injury penalty for {p.name}: {player_score:.2f}")

        # STEP 11: Apply Temperature bonus/penalty (game conditions)
        if temperature:
            player_score, reason = self._apply_temperature_scoring(p, player_score)
            add_to_reasons(reason)
            self.logger.debug(f"Step 11 - After temperature scoring for {p.name}: {player_score:.2f}")

        # STEP 12: Apply Wind bonus/penalty (game conditions, QB/WR/K only)
        if wind:
            player_score, reason = self._apply_wind_scoring(p, player_score)
            add_to_reasons(reason)
            self.logger.debug(f"Step 12 - After wind scoring for {p.name}: {player_score:.2f}")

        # STEP 13: Apply Location bonus/penalty (home/away/international)
        if location:
            player_score, reason = self._apply_location_modifier(p, player_score)
            add_to_reasons(reason)
            self.logger.debug(f"Step 13 - Final score for {p.name}: {player_score:.2f}")

        # Summary logging
        self.logger.debug(
            f"Scoring for {p.name}: final_score={player_score:.1f}"
        )

        p.score = player_score

        # Calculate the "calculated projection" by reversing the normalization
        # This shows what the adjusted fantasy points would be after all scoring steps
        # Formula: calculated_pts = (final_score / normalization_scale) * max_projection
        normalization_scale = self.config.normalization_max_scale
        chosen_max = self.max_weekly_projection if use_weekly_projection else self.max_projection

        if normalization_scale > 0 and chosen_max > 0:
            calculated_projection = (player_score / normalization_scale) * chosen_max
        else:
            calculated_projection = 0.0

        return ScoredPlayer(p, player_score, reasons, projected_points=calculated_projection)

    def _get_normalized_fantasy_points(self, p: FantasyPlayer, use_weekly_projection: bool) -> Tuple[float, str]:
        """Get normalized fantasy points (Step 1)."""
        # Determine which projection type to use
        if use_weekly_projection:
            # Use projection for current week only (for weekly recommendations)
            orig_pts, weighted_pts = self.get_weekly_projection(p)
        else:
            # Use rest-of-season projection (for season-long evaluation)
            # This sums all remaining weeks from current week through week 17
            orig_pts = p.get_rest_of_season_projection(self.config.current_nfl_week)
            # Normalize to 0-N scale for comparability across all players
            # Check for zero max_projection to avoid division by zero
            if self.max_projection > 0:
                weighted_pts = self.weight_projection(orig_pts)
            else:
                weighted_pts = 0.0

        # Format reason string showing both raw and normalized values
        reason = f"Projected: {orig_pts:.2f} pts, Weighted: {weighted_pts:.2f} pts"
        return weighted_pts, reason

    def _apply_adp_multiplier(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
        """Calculate ADP-based market wisdom adjustment multiplier (Step 2)."""
        # Get ADP-based multiplier from config
        # ADP (Average Draft Position) reflects market consensus on player value
        # Lower ADP (earlier picks) = higher multiplier (e.g., 1.05x)
        # Higher ADP (later picks) = lower multiplier (e.g., 0.95x)
        multiplier, rating = self.config.get_adp_multiplier(p.adp)
        reason = f"ADP: {rating} ({multiplier:.2f}x)"
        return player_score * multiplier, reason

    def _apply_player_rating_multiplier(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
        """Apply player rating multiplier (Step 3)."""
        # Get player rating multiplier from config
        # Player rating (0-100) represents expert consensus rankings
        # Higher ratings (80+) = EXCELLENT multiplier (e.g., 1.05x)
        # Lower ratings (<20) = POOR multiplier (e.g., 0.95x)
        multiplier, rating = self.config.get_player_rating_multiplier(p.player_rating)
        reason = f"Player Rating: {rating} ({multiplier:.2f}x)"
        return player_score * multiplier, reason

    def _apply_team_quality_multiplier(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
        """Apply team quality multiplier (Step 4)."""
        # Determine which team ranking to use based on player type
        # Offensive players (QB, RB, WR, TE, K) use offensive rank
        # Defensive players (DST) use defensive rank
        quality_val = p.team_offensive_rank
        if p.position in Constants.DEFENSE_POSITIONS:
            quality_val = p.team_defensive_rank

        # Get multiplier based on team quality rank (1-32)
        # Better teams (rank 1-10) = higher multiplier
        # Worse teams (rank 23-32) = lower multiplier
        multiplier, rating = self.config.get_team_quality_multiplier(quality_val)
        reason = f"Team Quality: {rating} ({multiplier:.2f}x)"
        return player_score * multiplier, reason

    def _apply_performance_multiplier(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
        """
        Apply performance-based multiplier to player score (Step 5).

        Performance measures actual vs projected deviation. Players who consistently
        outperform projections get a boost, underperformers get penalized.

        Thresholds (based on average deviation):
        - < -20%: VERY_POOR (0.95x multiplier)
        - -20% to -10%: POOR (0.975x multiplier)
        - -10% to +10%: AVERAGE (1.0x multiplier)
        - +10% to +20%: GOOD (1.025x multiplier)
        - > +20%: EXCELLENT (1.05x multiplier)

        Args:
            p: FantasyPlayer to evaluate
            player_score: Current score before performance adjustment

        Returns:
            Tuple[float, str]: (adjusted_score, reason_string)
                - If insufficient data or DST: returns (score, "")
                - Otherwise: returns (score * multiplier, "Performance: RATING")
        """
        # Calculate performance deviation
        deviation = self.calculate_performance_deviation(p)

        # If insufficient data or DST, return neutral multiplier (no change)
        if deviation is None:
            return player_score, ""

        # Get multiplier and rating from ConfigManager
        multiplier, rating = self.config.get_performance_multiplier(deviation)

        reason = f"Performance: {rating} ({deviation*100:+.1f}%, {multiplier:.2f}x)"
        return player_score * multiplier, reason

    def _apply_matchup_multiplier(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
        """Apply matchup additive bonus (Step 6)."""
        # Apply matchup adjustments to all positions as additive bonuses
        # Matchup score represents opponent strength differential
        # Positive score = favorable matchup (weak opponent) → positive bonus
        # Negative score = unfavorable matchup (strong opponent) → negative penalty
        # All players get same absolute bonus for same matchup (environmental factor)
        multiplier, rating = self.config.get_matchup_multiplier(p.matchup_score)
        impact_scale = self.config.matchup_scoring['IMPACT_SCALE']
        bonus = (impact_scale * multiplier) - impact_scale

        reason = f"Matchup: {rating} ({bonus:+.1f} pts)"
        return player_score + bonus, reason

    def _apply_schedule_multiplier(self, player: FantasyPlayer, player_score: float) -> Tuple[float, str]:
        """
        Apply schedule strength additive bonus based on future opponent difficulty.

        Schedule bonuses are additive (not multiplicative) because schedule represents
        environmental opportunity available equally to all players, not ability multipliers.

        Args:
            player: Player to score
            player_score: Current score before schedule adjustment

        Returns:
            Tuple (new_score, reason_string)
        """
        # Calculate schedule value
        schedule_value = self._calculate_schedule_value(player)

        if schedule_value is None:
            return player_score, ""

        # Get multiplier and rating
        multiplier, rating = self.config.get_schedule_multiplier(schedule_value)

        # Calculate additive bonus
        impact_scale = self.config.schedule_scoring['IMPACT_SCALE']
        bonus = (impact_scale * multiplier) - impact_scale

        # Apply bonus
        new_score = player_score + bonus
        reason = f"Schedule: {rating} (avg opp def rank: {schedule_value:.1f}, {bonus:+.1f} pts)"

        self.logger.debug(
            f"{player.name}: Schedule bonus {bonus:+.1f} pts "
            f"({schedule_value:.1f} avg rank) -> {player_score:.2f} to {new_score:.2f}"
        )

        return new_score, reason

    def _apply_draft_order_bonus(self, p: FantasyPlayer, draft_round: int, player_score: float) -> Tuple[float, str]:
        """Add draft order bonus (Step 8)."""
        # Get position-specific bonus for the current draft round
        # Different positions have different values at different rounds
        # Example: QB gets PRIMARY bonus in early rounds, RB/WR get higher bonuses
        # This encourages drafting the right positions at the right time
        bonus, bonus_type = self.config.get_draft_order_bonus(p.position, draft_round)

        # Only add reason text if there's an actual bonus (not empty string)
        reason = ""
        if bonus_type != "":
            reason = f"Draft Order Bonus: {bonus_type} ({bonus:+.1f} pts)"

        # Add bonus to score (not multiply, since it's a flat point adjustment)
        return player_score + bonus, reason

    def _apply_bye_week_penalty(self, p: FantasyPlayer, player_score: float, roster: List[FantasyPlayer]) -> Tuple[float, str]:
        """
        Apply bye week penalty based on roster conflicts (Step 9).

        Collects players with same-position and different-position bye week overlaps,
        then calculates penalty based on median weekly scores using linear scaling.
        Penalty calculation: (same_median_total * SAME_POS_BYE_WEIGHT) + (diff_median_total * DIFF_POS_BYE_WEIGHT)

        Args:
            p: Player to evaluate
            player_score: Current player score
            roster: Roster to check for bye week conflicts

        Returns:
            Tuple[float, str]: (adjusted_score, reason_string)
        """
        # Collect bye week conflicts separately by position relationship
        # Same-position conflicts are more severe (e.g., 2 RBs both on bye)
        # Different-position conflicts are less severe (e.g., RB + WR on bye)
        same_pos_players = []
        diff_pos_players = []

        # Return if the player's bye week is None or has already passed
        if p.bye_week is None:
            return player_score, "No bye week information available"

        if p.bye_week < self.config.current_nfl_week:
            return player_score, "The player's bye week has already passed."

        # Iterate through roster to find bye week overlaps
        for roster_player in roster:
            # Skip the player being scored (avoid counting them against themselves)
            # Also skip roster players with None bye_week or bye week already passed
            if roster_player.id == p.id:
                continue
            if roster_player.bye_week is None or roster_player.bye_week < self.config.current_nfl_week:
                continue

            # Check if this roster player has the same bye week
            if roster_player.bye_week == p.bye_week:
                # Compare positions (use actual position, not FLEX assignment)
                # Same position overlap is worse since it weakens a specific position
                if roster_player.position == p.position:
                    same_pos_players.append(roster_player)
                else:
                    # Different position overlap is less critical
                    diff_pos_players.append(roster_player)

        # Calculate total penalty using median-based exponential scaling
        penalty = self.config.get_bye_week_penalty(same_pos_players, diff_pos_players)

        # Build reason string (only show if there are actual conflicts)
        if len(same_pos_players) == 0 and len(diff_pos_players) == 0:
            reason = ""  # No conflicts = no reason string
        else:
            reason = f"Bye Overlaps: {len(same_pos_players)} same-position, {len(diff_pos_players)} different-position ({-penalty:.1f} pts)"

        # Subtract penalty from score (penalty reduces player value)
        return player_score - penalty, reason

    def _apply_injury_penalty(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
        """Apply injury penalty (Step 10)."""
        # Get injury penalty based on player's risk level
        # Risk levels: ACTIVE (no penalty), QUESTIONABLE (small penalty),
        #              DOUBTFUL/OUT (large penalty), IR (very large penalty)
        penalty = self.config.get_injury_penalty(p.get_risk_level())

        # Only show injury reason if player is not fully active
        # This keeps the reason list clean for healthy players
        reason = "" if p.injury_status == "ACTIVE" else f"Injury: {p.injury_status} ({-penalty:.1f} pts)"

        # Subtract penalty from score (injury reduces player value)
        return player_score - penalty, reason

    # ============================================================================
    # GAME CONDITION SCORING (Steps 11-13)
    # ============================================================================

    def _apply_temperature_scoring(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
        """
        Apply temperature bonus/penalty (Step 11).

        Temperature affects all positions. Players perform best around 60°F (ideal).
        Extreme cold or heat degrades performance.

        Args:
            p (FantasyPlayer): Player being scored
            player_score (float): Current score before temperature adjustment

        Returns:
            Tuple[float, str]: (adjusted_score, reason_string)
                - reason_string is empty if no adjustment applied
        """
        # Skip if no game data manager
        if not self.game_data_manager:
            return player_score, ""

        # Get game for player's team (use config week for simulation support)
        game = self.game_data_manager.get_game(p.team, self.config.current_nfl_week)

        # Skip if bye week (no game)
        if not game:
            return player_score, ""

        # Skip if indoor game (no weather effects)
        if game.indoor:
            return player_score, ""

        # Skip if no temperature data
        if game.temperature is None:
            return player_score, ""

        # Calculate temperature distance from ideal
        temp_distance = self.config.get_temperature_distance(game.temperature)

        # Get multiplier (lower distance = better = higher multiplier)
        multiplier, tier = self.config.get_temperature_multiplier(temp_distance)

        # Calculate additive bonus using IMPACT_SCALE
        # Formula: bonus = (IMPACT_SCALE * multiplier) - IMPACT_SCALE
        impact_scale = self.config.temperature_scoring.get('IMPACT_SCALE', 50.0)
        weight = self.config.temperature_scoring.get('WEIGHT', 1.0)
        bonus = ((impact_scale * multiplier) - impact_scale) * weight

        # Build reason string
        ideal_temp = self.config.temperature_scoring.get('IDEAL_TEMPERATURE', 60)
        if bonus >= 0:
            reason = f"Temp: {game.temperature}°F ({tier}, +{bonus:.1f} pts)"
        else:
            reason = f"Temp: {game.temperature}°F ({tier}, {bonus:.1f} pts)"

        return player_score + bonus, reason

    def _apply_wind_scoring(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
        """
        Apply wind bonus/penalty (Step 12).

        Wind only affects QB, WR, and K positions (passing game and kicking).
        Other positions (RB, TE, DST) are not affected.

        Args:
            p (FantasyPlayer): Player being scored
            player_score (float): Current score before wind adjustment

        Returns:
            Tuple[float, str]: (adjusted_score, reason_string)
                - reason_string is empty if no adjustment applied
        """
        # Skip if position not affected by wind
        if p.position not in Constants.WIND_AFFECTED_POSITIONS:
            return player_score, ""

        # Skip if no game data manager
        if not self.game_data_manager:
            return player_score, ""

        # Get game for player's team (use config week for simulation support)
        game = self.game_data_manager.get_game(p.team, self.config.current_nfl_week)

        # Skip if bye week (no game)
        if not game:
            return player_score, ""

        # Skip if indoor game (no wind effects)
        if game.indoor:
            return player_score, ""

        # Skip if no wind data
        if game.wind_gust is None:
            return player_score, ""

        # Get multiplier (lower wind = better = higher multiplier)
        multiplier, tier = self.config.get_wind_multiplier(game.wind_gust)

        # Calculate additive bonus using IMPACT_SCALE
        # Formula: bonus = (IMPACT_SCALE * multiplier) - IMPACT_SCALE
        impact_scale = self.config.wind_scoring.get('IMPACT_SCALE', 60.0)
        weight = self.config.wind_scoring.get('WEIGHT', 1.0)
        bonus = ((impact_scale * multiplier) - impact_scale) * weight

        # Build reason string
        if bonus >= 0:
            reason = f"Wind: {game.wind_gust}mph ({tier}, +{bonus:.1f} pts)"
        else:
            reason = f"Wind: {game.wind_gust}mph ({tier}, {bonus:.1f} pts)"

        return player_score + bonus, reason

    def _apply_location_modifier(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
        """
        Apply location bonus/penalty (Step 13).

        Home games provide a bonus, away games a penalty, and international
        games have a larger penalty due to travel and unfamiliar environment.

        Args:
            p (FantasyPlayer): Player being scored
            player_score (float): Current score before location adjustment

        Returns:
            Tuple[float, str]: (adjusted_score, reason_string)
                - reason_string is empty if no adjustment applied
        """
        # Skip if no game data manager
        if not self.game_data_manager:
            return player_score, ""

        # Get game for player's team (use config week for simulation support)
        game = self.game_data_manager.get_game(p.team, self.config.current_nfl_week)

        # Skip if bye week (no game)
        if not game:
            return player_score, ""

        # Determine location type
        is_home = game.is_home_game(p.team)
        is_international = game.is_international()

        # Get location modifier
        modifier = self.config.get_location_modifier(is_home, is_international)

        # Build reason string
        if is_international:
            location_type = f"International ({game.country})"
        elif is_home:
            location_type = "Home"
        else:
            location_type = "Away"

        if modifier == 0:
            return player_score, ""
        elif modifier > 0:
            reason = f"Location: {location_type} (+{modifier:.1f} pts)"
        else:
            reason = f"Location: {location_type} ({modifier:.1f} pts)"

        return player_score + modifier, reason
