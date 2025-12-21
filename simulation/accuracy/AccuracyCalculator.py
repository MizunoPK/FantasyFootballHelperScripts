"""
Accuracy Calculator

Calculates Mean Absolute Error (MAE) between projected and actual fantasy points.
Used by AccuracySimulationManager to evaluate scoring algorithm configurations.

MAE Formula: mean(|actual - projected|) across all eligible players

Player Filtering Rules (from specs):
- Exclude players with 0 actual points (didn't play)
- Include all players regardless of projection value
- Skip player-week combinations with missing data
- Equal weight for all players

Author: Kai Mizuno
"""

import csv
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.LoggingManager import get_logger


class AccuracyResult:
    """
    Results from an accuracy calculation.

    Attributes:
        mae (float): Mean Absolute Error
        player_count (int): Number of players evaluated
        total_error (float): Sum of all absolute errors
        errors (List[float]): Individual player errors (for debugging)
    """

    def __init__(
        self,
        mae: float,
        player_count: int,
        total_error: float,
        errors: Optional[List[float]] = None
    ) -> None:
        self.mae = mae
        self.player_count = player_count
        self.total_error = total_error
        self.errors = errors or []

    def __repr__(self) -> str:
        return f"AccuracyResult(mae={self.mae:.4f}, players={self.player_count})"


class AccuracyCalculator:
    """
    Calculates prediction accuracy using Mean Absolute Error.

    Compares projected points (from scoring algorithm) to actual points
    (from historical data) to evaluate configuration quality.

    Attributes:
        logger: Logger instance
    """

    def __init__(self) -> None:
        """Initialize AccuracyCalculator."""
        self.logger = get_logger()
        self.logger.debug("AccuracyCalculator initialized")

    def calculate_mae(
        self,
        player_data: List[Dict[str, Any]],
        include_individual_errors: bool = False
    ) -> AccuracyResult:
        """
        Calculate Mean Absolute Error for a list of player projections.

        Args:
            player_data: List of dicts with 'projected' and 'actual' keys
                Example: [{'projected': 15.5, 'actual': 12.3}, ...]
            include_individual_errors: If True, include per-player errors in result

        Returns:
            AccuracyResult: MAE calculation results

        Note:
            - Skips players with actual points <= 0 (didn't play)
            - Returns MAE of 0 with 0 players if no valid data
        """
        errors = []
        skipped_count = 0

        for player in player_data:
            projected = player.get('projected', 0)
            actual = player.get('actual', 0)

            # Skip players who didn't play (0 actual points)
            if actual <= 0:
                skipped_count += 1
                continue

            # Calculate absolute error
            error = abs(actual - projected)
            errors.append(error)

        # Calculate MAE
        if not errors:
            self.logger.warning("No valid players for MAE calculation")
            return AccuracyResult(mae=0.0, player_count=0, total_error=0.0)

        total_error = sum(errors)
        mae = total_error / len(errors)

        self.logger.debug(
            f"MAE calculation: {mae:.4f} from {len(errors)} players "
            f"(skipped {skipped_count} with 0 actual points)"
        )

        return AccuracyResult(
            mae=mae,
            player_count=len(errors),
            total_error=total_error,
            errors=errors if include_individual_errors else None
        )

    def calculate_weekly_mae(
        self,
        week_projections: Dict[int, Dict[int, float]],
        week_actuals: Dict[int, Dict[int, float]],
        week_range: Tuple[int, int]
    ) -> AccuracyResult:
        """
        Calculate MAE for a range of weeks.

        Compares weekly projections to actual weekly performance.

        Args:
            week_projections: Dict of week -> {player_id -> projected}
            week_actuals: Dict of week -> {player_id -> actual}
            week_range: Tuple of (start_week, end_week) inclusive

        Returns:
            AccuracyResult: MAE calculation results for the week range
        """
        start_week, end_week = week_range
        player_data = []

        for week in range(start_week, end_week + 1):
            if week not in week_projections or week not in week_actuals:
                self.logger.warning(f"Week {week} data missing, skipping")
                continue

            week_proj = week_projections[week]
            week_act = week_actuals[week]

            for player_id, projected in week_proj.items():
                if player_id in week_act:
                    player_data.append({
                        'player_id': player_id,
                        'week': week,
                        'projected': projected,
                        'actual': week_act[player_id]
                    })

        self.logger.debug(
            f"Weekly MAE for weeks {start_week}-{end_week}: "
            f"{len(player_data)} player-week combinations"
        )

        return self.calculate_mae(player_data)

    def aggregate_season_results(
        self,
        season_results: List[Tuple[str, AccuracyResult]],
        horizon: str = None,
        config_label: str = None
    ) -> AccuracyResult:
        """
        Aggregate MAE results across multiple seasons.

        Uses weighted average based on player counts (equal weight per player).

        Args:
            season_results: List of (season_name, AccuracyResult) tuples
            horizon: Optional horizon identifier (e.g., 'week_1_5', 'week_6_9') for logging
            config_label: Optional config identifier (e.g., 'NORMALIZATION_MAX_SCALE=54 [week_1_5]') for logging

        Returns:
            AccuracyResult: Aggregated MAE across all seasons
        """
        total_error = 0.0
        total_players = 0

        for season_name, result in season_results:
            total_error += result.total_error
            total_players += result.player_count
            self.logger.debug(
                f"Season {season_name}: MAE={result.mae:.4f}, "
                f"players={result.player_count}"
            )

        if total_players == 0:
            self.logger.warning("No players across all seasons")
            return AccuracyResult(mae=0.0, player_count=0, total_error=0.0)

        aggregated_mae = total_error / total_players

        # Build descriptive log message
        if config_label and horizon:
            # Full context: "Config: PARAM=value [config_horizon] | Evaluating: eval_horizon | MAE: ..."
            # Use debug level for individual horizon evaluations (summary will be logged separately)
            self.logger.debug(
                f"Config: {config_label} | Eval: {horizon} | MAE={aggregated_mae:.4f} | "
                f"Players={total_players} | Seasons={len(season_results)}"
            )
        elif horizon:
            # Just horizon context
            self.logger.info(
                f"[{horizon}] Aggregated MAE: {aggregated_mae:.4f} from {total_players} players "
                f"across {len(season_results)} seasons"
            )
        else:
            # No context (backward compatibility)
            self.logger.info(
                f"Aggregated MAE: {aggregated_mae:.4f} from {total_players} players "
                f"across {len(season_results)} seasons"
            )

        return AccuracyResult(
            mae=aggregated_mae,
            player_count=total_players,
            total_error=total_error
        )
