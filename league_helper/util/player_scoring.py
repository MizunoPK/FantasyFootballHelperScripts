"""
Player Scoring Calculator

Helper class for calculating player scores using the 9-step scoring algorithm.
Handles all scoring-related calculations including normalization, multipliers,
bonuses, and penalties.

The 9-step scoring algorithm:
1. Normalization (based on fantasy_points projection)
2. ADP Multiplier (market wisdom adjustment)
3. Player Rating Multiplier (expert consensus)
4. Team Quality Multiplier (offensive/defensive strength)
5. Performance Multiplier (actual vs projected deviation)
6. Matchup Multiplier (opponent strength)
7. Draft Order Bonus (positional value by round)
8. Bye Week Penalty (same-position and different-position roster conflicts)
9. Injury Penalty (risk assessment)

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

sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.FantasyPlayer import FantasyPlayer
from utils.LoggingManager import get_logger


class PlayerScoringCalculator:
    """
    Calculator for player scoring using the 9-step algorithm.

    Handles all scoring calculations including normalization, multipliers,
    bonuses, and penalties. Separated from PlayerManager to improve
    organization and testability.

    Attributes:
        config (ConfigManager): Configuration manager for scoring parameters
        projected_points_manager (ProjectedPointsManager): Manager for projected points
        max_projection (float): Maximum fantasy points projection for normalization
        logger: Logger instance
    """

    def __init__(self, config: ConfigManager, projected_points_manager: ProjectedPointsManager, max_projection: float) -> None:
        """
        Initialize PlayerScoringCalculator.

        Args:
            config (ConfigManager): Configuration manager with scoring parameters
            projected_points_manager (ProjectedPointsManager): Manager for projected points
            max_projection (float): Maximum fantasy points projection for normalization
        """
        self.config = config
        self.projected_points_manager = projected_points_manager
        self.max_projection = max_projection
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
            # Calculate normalized/weighted projection using same scale as seasonal projections
            # This ensures weekly and seasonal scores are comparable
            if self.max_projection > 0:
                weighted_projection = self.weight_projection(weekly_points)
            else:
                weighted_projection = 0.0
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

    def weight_projection(self, pts: float) -> float:
        """
        Calculate weighted projection using normalization scale.

        Args:
            pts (float): Raw fantasy points

        Returns:
            float: Weighted projection (0-N scale)
        """
        return (pts / self.max_projection) * self.config.normalization_max_scale

    def calculate_consistency(self, player: FantasyPlayer) -> Tuple[float, int]:
        """
        Calculate consistency score for a player based on weekly projections.
        Value equals the coefficient of variation.

        Only uses weeks < CURRENT_NFL_WEEK (weeks that have already occurred).
        Requires minimum MIN_WEEKS weeks of data for reliable calculation.

        Args:
            player: FantasyPlayer object with weekly projection data

        Returns:
            tuple: (consistency_score, weeks_count)
                - consistency_score: the calculated values between 0 and 1 associated with how consistent a player's scores have been
                - weeks_count: number of weeks with data used in calculation
        """
        # Extract weekly scores for weeks that have occurred
        weekly_points = []

        # Only analyze weeks that have occurred (weeks < CURRENT_NFL_WEEK)
        for week in range(1, self.config.current_nfl_week):
            week_attr = f'week_{week}_points'
            if hasattr(player, week_attr):
                points = getattr(player, week_attr)
                # Filter out None values (missing data) and zeros
                # Zeros could be bye weeks, benched players, or data issues
                if points is not None and float(points) > 0:
                    weekly_points.append(float(points))

        weeks_count = len(weekly_points)

        # Handle insufficient data
        min_weeks = self.config.consistency_scoring[self.config.keys.MIN_WEEKS]
        if weeks_count < min_weeks:
            # Return default consistency score without logging individual warnings
            return 0.5, weeks_count

        # Calculate statistics
        mean_points = statistics.mean(weekly_points)

        # Handle zero mean (avoid division by zero)
        if mean_points == 0:
            return 0.5, weeks_count

        # Calculate standard deviation
        if len(weekly_points) == 1:
            std_dev = 0.0
        else:
            std_dev = statistics.stdev(weekly_points)

        # Calculate coefficient of variation
        cv = std_dev / mean_points if mean_points > 0 else 0.0

        self.logger.debug(
                f"Consistency for {player.name}: mean={mean_points:.2f}, "
                f"std_dev={std_dev:.2f}, CV={cv:.3f}"
            )

        return cv, weeks_count

    def calculate_performance_deviation(self, player: FantasyPlayer) -> Optional[float]:
        """
        Calculate performance deviation for a player based on actual vs projected points.

        Measures how much a player's actual performance deviates from projected points
        across historical weeks. Positive deviation = outperforming, negative = underperforming.

        Formula: average((actual - projected) / projected) for all valid weeks

        Only uses weeks < CURRENT_NFL_WEEK (weeks that have already occurred).
        Requires minimum MIN_WEEKS weeks of data for reliable calculation.

        Skipping criteria:
        - Weeks where actual points = 0 (player didn't play)
        - Weeks where projected = 0.0 AND actual ≠ 0.0 (unprojected performances)
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

        # Collect performance deviations for each valid week
        deviations = []

        # Only analyze weeks that have occurred (weeks < CURRENT_NFL_WEEK)
        for week in range(1, self.config.current_nfl_week):
            # Get actual points from player object
            week_attr = f'week_{week}_points'
            if not hasattr(player, week_attr):
                continue

            actual_points = getattr(player, week_attr)
            if actual_points is None:
                continue

            actual_points = float(actual_points)

            # Skip weeks where player didn't play (actual = 0)
            if actual_points == 0:
                continue

            # Get projected points from ProjectedPointsManager
            projected_points = self.projected_points_manager.get_projected_points(player, week)
            if projected_points is None:
                continue

            # IMPORTANT: Skip weeks where projected = 0.0 AND actual ≠ 0.0
            # This prevents division by zero and skewed metrics for unprojected performances
            if projected_points == 0.0 and actual_points != 0.0:
                self.logger.debug(
                    f"Skipping week {week} for {player.name}: projected=0.0 but actual={actual_points:.2f}"
                )
                continue

            # Skip if projected is 0 (even if actual is also 0) to avoid division by zero
            if projected_points == 0.0:
                continue

            # Calculate deviation: (actual - projected) / projected
            deviation = (actual_points - projected_points) / projected_points
            deviations.append(deviation)

            self.logger.debug(
                f"Week {week} performance for {player.name}: "
                f"actual={actual_points:.2f}, projected={projected_points:.2f}, "
                f"deviation={deviation:.3f} ({deviation*100:.1f}%)"
            )

        weeks_count = len(deviations)

        # Handle insufficient data
        min_weeks = self.config.consistency_scoring[self.config.keys.MIN_WEEKS]
        if weeks_count < min_weeks:
            self.logger.debug(
                f"Insufficient performance data for {player.name}: "
                f"{weeks_count} weeks < {min_weeks} required"
            )
            return None

        # Calculate average deviation
        avg_deviation = statistics.mean(deviations)

        self.logger.debug(
            f"Performance deviation for {player.name}: {avg_deviation:.3f} "
            f"({avg_deviation*100:.1f}%) across {weeks_count} weeks"
        )

        return avg_deviation

    def score_player(self, p: FantasyPlayer, team_roster: List[FantasyPlayer], use_weekly_projection=False, adp=False, player_rating=True, team_quality=True, performance=True, matchup=False, draft_round=-1, bye=True, injury=True, roster: Optional[List[FantasyPlayer]] = None) -> ScoredPlayer:
        """
        Calculate score for a player (9-step calculation).

        New Scoring System:
        1. Get normalized seasonal fantasy points (0-N scale)
        2. Apply ADP multiplier
        3. Apply Player Ranking multiplier
        4. Apply Team ranking multiplier
        5. Apply Performance multiplier (actual vs projected deviation)
        6. Apply Matchup multiplier
        7. Add DRAFT_ORDER bonus (round-based position priority)
        8. Subtract Bye Week penalty
        9. Subtract Injury penalty

        Args:
            p: FantasyPlayer to score
            team_roster: The team's roster (used for bye week calculations)
            use_weekly_projection: Use weekly projection instead of rest-of-season
            adp: Apply ADP multiplier
            player_rating: Apply player rating multiplier
            team_quality: Apply team quality multiplier
            performance: Apply performance multiplier (actual vs projected deviation)
            matchup: Apply matchup multiplier
            draft_round: Draft round for position bonus (-1 to disable)
            bye: Apply bye week penalty
            injury: Apply injury penalty
            roster: Optional custom roster to use for bye week calculations (defaults to team_roster)

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

        # STEP 7: Add DRAFT_ORDER bonus (round-based position priority)
        # BUG FIX: Changed from draft_round > 0 to draft_round >= 0
        # This allows round 0 (first round) to get bonuses, -1 is the disabled flag
        if draft_round >= 0:
            player_score, reason = self._apply_draft_order_bonus(p, draft_round, player_score)
            add_to_reasons(reason)
            self.logger.debug(f"Step 7 - After DRAFT_ORDER bonus for {p.name}: {player_score:.2f}")

        # STEP 8: Subtract Bye Week penalty
        if bye:
            player_score, reason = self._apply_bye_week_penalty(p, player_score, roster if roster is not None else team_roster)
            add_to_reasons(reason)
            self.logger.debug(f"Step 8 - After bye penalty for {p.name}: {player_score:.2f}")

        # STEP 9: Subtract Injury penalty
        if injury:
            player_score, reason = self._apply_injury_penalty(p, player_score)
            add_to_reasons(reason)
            self.logger.debug(f"Step 9 - Final score for {p.name}: {player_score:.2f}")

        # Summary logging
        self.logger.debug(
            f"Scoring for {p.name}: final_score={player_score:.1f}"
        )

        p.score = player_score
        return ScoredPlayer(p, player_score, reasons)

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
            weighted_pts = self.weight_projection(orig_pts)

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
        reason = f"ADP: {rating}"
        return player_score * multiplier, reason

    def _apply_player_rating_multiplier(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
        """Apply player rating multiplier (Step 3)."""
        # Get player rating multiplier from config
        # Player rating (0-100) represents expert consensus rankings
        # Higher ratings (80+) = EXCELLENT multiplier (e.g., 1.05x)
        # Lower ratings (<20) = POOR multiplier (e.g., 0.95x)
        multiplier, rating = self.config.get_player_rating_multiplier(p.player_rating)
        reason = f"Player Rating: {rating}"
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
        reason = f"Team Quality: {rating}"
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

        reason = f"Performance: {rating} ({deviation*100:+.1f}%)"
        return player_score * multiplier, reason

    def _apply_matchup_multiplier(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
        """Apply matchup multiplier (Step 6)."""
        # Default to neutral multiplier (no adjustment)
        multiplier = 1.0
        rating = "NEUTRAL"

        # Only apply matchup adjustments to matchup-sensitive positions
        # Matchup score represents opponent strength differential
        # Positive score = favorable matchup (weak opponent)
        # Negative score = unfavorable matchup (strong opponent)
        if p.position in Constants.MATCHUP_ENABLED_POSITIONS:
            multiplier, rating = self.config.get_matchup_multiplier(p.matchup_score)

        reason = f"Matchup: {rating}"
        return player_score * multiplier, reason

    def _apply_draft_order_bonus(self, p: FantasyPlayer, draft_round: int, player_score: float) -> Tuple[float, str]:
        """Add draft order bonus (Step 7)."""
        # Get position-specific bonus for the current draft round
        # Different positions have different values at different rounds
        # Example: QB gets PRIMARY bonus in early rounds, RB/WR get higher bonuses
        # This encourages drafting the right positions at the right time
        bonus, bonus_type = self.config.get_draft_order_bonus(p.position, draft_round)

        # Only add reason text if there's an actual bonus (not empty string)
        reason = ""
        if bonus_type != "":
            reason = f"Draft Order Bonus: {bonus_type}"

        # Add bonus to score (not multiply, since it's a flat point adjustment)
        return player_score + bonus, reason

    def _apply_bye_week_penalty(self, p: FantasyPlayer, player_score: float, roster: List[FantasyPlayer]) -> Tuple[float, str]:
        """
        Apply bye week penalty based on roster conflicts (Step 8).

        Counts both same-position and different-position bye week overlaps separately,
        applying BASE_BYE_PENALTY for same-position conflicts and
        DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY for different-position conflicts.

        Args:
            p: Player to evaluate
            player_score: Current player score
            roster: Roster to check for bye week conflicts

        Returns:
            Tuple[float, str]: (adjusted_score, reason_string)
        """
        # Count bye week conflicts separately by position relationship
        # Same-position conflicts are more severe (e.g., 2 RBs both on bye)
        # Different-position conflicts are less severe (e.g., RB + WR on bye)
        num_same_position = 0
        num_different_position = 0

        # Iterate through roster to find bye week overlaps
        for roster_player in roster:
            # Skip the player being scored (avoid counting them against themselves)
            if roster_player.id == p.id:
                continue

            # Check if this roster player has the same bye week
            if roster_player.bye_week == p.bye_week:
                # Compare positions (use actual position, not FLEX assignment)
                # Same position overlap is worse since it weakens a specific position
                if roster_player.position == p.position:
                    num_same_position += 1
                else:
                    # Different position overlap is less critical
                    num_different_position += 1

        # Calculate total penalty using config-defined weights
        # BASE_BYE_PENALTY applies to same-position overlaps
        # DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY applies to different-position overlaps
        penalty = self.config.get_bye_week_penalty(num_same_position, num_different_position)

        # Build reason string (only show if there are actual conflicts)
        if num_same_position == 0 and num_different_position == 0:
            reason = ""  # No conflicts = no reason string
        else:
            reason = f"Bye Overlaps: {num_same_position} same-position, {num_different_position} different-position"

        # Subtract penalty from score (penalty reduces player value)
        return player_score - penalty, reason

    def _apply_injury_penalty(self, p: FantasyPlayer, player_score: float) -> Tuple[float, str]:
        """Apply injury penalty (Step 9)."""
        # Get injury penalty based on player's risk level
        # Risk levels: ACTIVE (no penalty), QUESTIONABLE (small penalty),
        #              DOUBTFUL/OUT (large penalty), IR (very large penalty)
        penalty = self.config.get_injury_penalty(p.get_risk_level())

        # Only show injury reason if player is not fully active
        # This keeps the reason list clean for healthy players
        reason = "" if p.injury_status == "ACTIVE" else f"Injury: {p.injury_status}"

        # Subtract penalty from score (injury reduces player value)
        return player_score - penalty, reason
