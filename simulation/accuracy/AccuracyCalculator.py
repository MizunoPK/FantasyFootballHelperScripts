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

import numpy as np
from scipy.stats import spearmanr

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
        overall_metrics (Optional[RankingMetrics]): Overall ranking metrics across all positions
        by_position (Optional[Dict[str, RankingMetrics]]): Ranking metrics per position
    """

    def __init__(
        self,
        mae: float,
        player_count: int,
        total_error: float,
        errors: Optional[List[float]] = None,
        overall_metrics=None,  # RankingMetrics
        by_position: Optional[dict] = None  # Dict[str, RankingMetrics]
    ) -> None:
        self.mae = mae
        self.player_count = player_count
        self.total_error = total_error
        self.errors = errors or []
        self.overall_metrics = overall_metrics
        self.by_position = by_position or {}

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

        # Aggregate ranking metrics across seasons (Q18: simple average)
        overall_metrics = None
        by_position = {}

        # Check if any season has ranking metrics
        has_ranking_metrics = any(
            result.overall_metrics is not None
            for _, result in season_results
        )

        if has_ranking_metrics:
            import numpy as np

            # Collect metrics from all seasons
            pairwise_values = []
            top_5_values = []
            top_10_values = []
            top_20_values = []
            spearman_z_values = []

            position_data = {'QB': {}, 'RB': {}, 'WR': {}, 'TE': {}}
            for pos in position_data:
                position_data[pos] = {
                    'pairwise': [],
                    'top_5': [],
                    'top_10': [],
                    'top_20': [],
                    'spearman_z': []
                }

            for season_name, result in season_results:
                if result.overall_metrics:
                    pairwise_values.append(result.overall_metrics.pairwise_accuracy)
                    top_5_values.append(result.overall_metrics.top_5_accuracy)
                    top_10_values.append(result.overall_metrics.top_10_accuracy)
                    top_20_values.append(result.overall_metrics.top_20_accuracy)

                    # Fisher z-transform for Spearman (Q9)
                    if not np.isnan(result.overall_metrics.spearman_correlation):
                        z = np.arctanh(result.overall_metrics.spearman_correlation)
                        spearman_z_values.append(z)

                # Aggregate per-position metrics
                if result.by_position:
                    for pos, metrics in result.by_position.items():
                        if pos in position_data:
                            position_data[pos]['pairwise'].append(metrics.pairwise_accuracy)
                            position_data[pos]['top_5'].append(metrics.top_5_accuracy)
                            position_data[pos]['top_10'].append(metrics.top_10_accuracy)
                            position_data[pos]['top_20'].append(metrics.top_20_accuracy)

                            if not np.isnan(metrics.spearman_correlation):
                                z = np.arctanh(metrics.spearman_correlation)
                                position_data[pos]['spearman_z'].append(z)

            # Calculate overall metrics (simple average)
            if pairwise_values:
                # Import RankingMetrics from AccuracyResultsManager
                # We need to do this dynamically to avoid circular import
                from simulation.accuracy.AccuracyResultsManager import RankingMetrics

                overall_spearman = 0.0
                if spearman_z_values:
                    z_mean = np.mean(spearman_z_values)
                    overall_spearman = float(np.tanh(z_mean))

                overall_metrics = RankingMetrics(
                    pairwise_accuracy=float(np.mean(pairwise_values)),
                    top_5_accuracy=float(np.mean(top_5_values)),
                    top_10_accuracy=float(np.mean(top_10_values)),
                    top_20_accuracy=float(np.mean(top_20_values)),
                    spearman_correlation=overall_spearman
                )

            # Calculate per-position metrics
            for pos, data in position_data.items():
                if data['pairwise']:
                    from simulation.accuracy.AccuracyResultsManager import RankingMetrics

                    pos_spearman = 0.0
                    if data['spearman_z']:
                        z_mean = np.mean(data['spearman_z'])
                        pos_spearman = float(np.tanh(z_mean))

                    by_position[pos] = RankingMetrics(
                        pairwise_accuracy=float(np.mean(data['pairwise'])),
                        top_5_accuracy=float(np.mean(data['top_5'])),
                        top_10_accuracy=float(np.mean(data['top_10'])),
                        top_20_accuracy=float(np.mean(data['top_20'])),
                        spearman_correlation=pos_spearman
                    )

        return AccuracyResult(
            mae=aggregated_mae,
            player_count=total_players,
            total_error=total_error,
            overall_metrics=overall_metrics,
            by_position=by_position
        )

    def calculate_pairwise_accuracy(
        self,
        player_data: List[Dict[str, Any]],
        position: str
    ) -> float:
        """
        Calculate pairwise decision accuracy for a position.

        For every pair of players at the same position, checks if the prediction
        correctly identifies which player will score more fantasy points.

        Args:
            player_data: List of dicts with 'projected', 'actual', 'position' keys
            position: Position to filter ('QB', 'RB', 'WR', 'TE')

        Returns:
            float: Percentage of correct pairwise comparisons (0.0-1.0)

        Note:
            - Filters to players with actual >= 3 points (meaningful performances)
            - Skips tie comparisons (when actual points are equal)
            - Returns 0.0 if insufficient data or all ties
        """
        # Filter to position and actual >= 3 (Q1, Q8 decisions)
        players = []
        for player in player_data:
            if player.get('position') == position and player.get('actual', 0) >= 3.0:
                players.append((player.get('projected', 0), player.get('actual', 0)))

        if len(players) < 2:
            self.logger.debug(f"Not enough {position} players for pairwise accuracy")
            return 0.0

        correct = 0
        total = 0

        # Compare all pairs
        for i in range(len(players)):
            for j in range(i + 1, len(players)):
                proj_i, actual_i = players[i]
                proj_j, actual_j = players[j]

                # Skip ties (Q2 decision)
                if actual_i == actual_j:
                    continue

                # Check if prediction matches actual
                predicted_order = proj_i > proj_j
                actual_order = actual_i > actual_j

                if predicted_order == actual_order:
                    correct += 1
                total += 1

        if total == 0:
            self.logger.warning(f"No valid comparisons for {position} (all ties)")
            return 0.0

        accuracy = correct / total
        self.logger.debug(
            f"{position} pairwise accuracy: {accuracy:.1%} ({correct}/{total} correct)"
        )
        return accuracy

    def calculate_top_n_accuracy(
        self,
        player_data: List[Dict[str, Any]],
        n: int,
        position: str
    ) -> float:
        """
        Calculate top-N overlap accuracy for a position.

        Measures how many of the predicted top-N players are actually in the
        top-N scorers.

        Args:
            player_data: List of dicts with 'projected', 'actual', 'position', 'name' keys
            n: Number of top players to compare (5, 10, or 20)
            position: Position to filter

        Returns:
            float: Percentage of overlap in top-N (0.0-1.0)

        Note:
            - Filters to players with actual >= 3 points
            - Returns 0.0 if fewer than N players available
            - Uses set intersection formula: overlap / N
        """
        # Filter to position and actual >= 3 (Q1, Q8)
        players = []
        for player in player_data:
            if player.get('position') == position and player.get('actual', 0) >= 3.0:
                players.append((
                    player.get('name', ''),
                    player.get('projected', 0),
                    player.get('actual', 0)
                ))

        if len(players) < n:
            self.logger.debug(
                f"Only {len(players)} {position} players, less than top-{n}"
            )
            return 0.0

        # Sort by predicted score and get top-N names
        predicted_top_n = set([
            name for name, proj, _ in
            sorted(players, key=lambda x: x[1], reverse=True)[:n]
        ])

        # Sort by actual points and get top-N names
        actual_top_n = set([
            name for name, _, actual in
            sorted(players, key=lambda x: x[2], reverse=True)[:n]
        ])

        # Calculate overlap (Q6: set intersection)
        overlap = len(predicted_top_n & actual_top_n)
        accuracy = overlap / n

        self.logger.debug(
            f"{position} top-{n} accuracy: {accuracy:.1%} ({overlap}/{n} overlap)"
        )
        return accuracy

    def calculate_spearman_correlation(
        self,
        player_data: List[Dict[str, Any]],
        position: str
    ) -> float:
        """
        Calculate Spearman rank correlation for a position.

        Measures how well the predicted rankings correlate with actual rankings.

        Args:
            player_data: List of dicts with 'projected', 'actual', 'position' keys
            position: Position to filter

        Returns:
            float: Spearman correlation coefficient (-1.0 to +1.0)

        Note:
            - Filters to players with actual >= 3 points
            - Returns 0.0 if insufficient data or zero variance
            - Handles NaN and division by zero gracefully
        """
        # Filter to position and actual >= 3 (Q1, Q8)
        projected_scores = []
        actual_scores = []

        for player in player_data:
            if player.get('position') == position and player.get('actual', 0) >= 3.0:
                projected_scores.append(player.get('projected', 0))
                actual_scores.append(player.get('actual', 0))

        if len(projected_scores) < 2:
            self.logger.debug(f"Not enough {position} players for correlation")
            return 0.0

        try:
            corr, pvalue = spearmanr(projected_scores, actual_scores)

            # Handle NaN (zero variance - Q22)
            if np.isnan(corr):
                self.logger.warning(
                    f"Zero variance in {position} predictions or actuals"
                )
                return 0.0

            self.logger.debug(
                f"{position} Spearman correlation: {corr:.3f} (p={pvalue:.4f})"
            )
            return float(corr)

        except (ZeroDivisionError, ValueError) as e:
            # Zero variance edge case (Q22)
            self.logger.warning(
                f"Correlation calculation failed for {position}: {e}"
            )
            return 0.0
