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

from typing import List, Dict, Tuple, Optional, Any

import numpy as np
from scipy.stats import spearmanr

from utils.LoggingManager import get_logger
from simulation.accuracy.accuracy_types import RankingMetrics


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
        overall_metrics=None,
        by_position: Optional[dict] = None
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
        self.logger.debug(
            f"calculate_mae: Processing {len(player_data)} players (before filtering)"
        )

        errors = []
        skipped_count = 0

        for player in player_data:
            projected = player.get('projected', 0)
            actual = player.get('actual', 0)

            if actual <= 0:
                skipped_count += 1
                continue

            error = abs(actual - projected)
            errors.append(error)

        if not errors:
            self.logger.warning("No valid players for MAE calculation")
            return AccuracyResult(mae=0.0, player_count=0, total_error=0.0)

        total_error = sum(errors)
        mae = total_error / len(errors)

        self.logger.debug(
            f"calculate_mae: MAE={mae:.4f} from {len(errors)} players after filtering "
            f"(skipped {skipped_count} with actual<=0)"
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

        if config_label and horizon:
            self.logger.debug(
                f"Config: {config_label} | Eval: {horizon} | MAE={aggregated_mae:.4f} | "
                f"Players={total_players} | Seasons={len(season_results)}"
            )
        elif horizon:
            self.logger.info(
                f"[{horizon}] Aggregated MAE: {aggregated_mae:.4f} from {total_players} players "
                f"across {len(season_results)} seasons"
            )
        else:
            self.logger.info(
                f"Aggregated MAE: {aggregated_mae:.4f} from {total_players} players "
                f"across {len(season_results)} seasons"
            )

        overall_metrics = None
        by_position = {}

        has_ranking_metrics = any(
            result.overall_metrics is not None
            for _, result in season_results
        )

        if has_ranking_metrics:
            import numpy as np

            pairwise_values = []
            top_5_values = []
            top_10_values = []
            top_20_values = []
            spearman_z_values = []

            position_data = {'QB': {}, 'RB': {}, 'WR': {}, 'TE': {}, 'K': {}, 'DST': {}}
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
                    om = result.overall_metrics
                    if om.pairwise_accuracy is not None:
                        pairwise_values.append(om.pairwise_accuracy)
                    if om.top_5_accuracy is not None:
                        top_5_values.append(om.top_5_accuracy)
                    if om.top_10_accuracy is not None:
                        top_10_values.append(om.top_10_accuracy)
                    if om.top_20_accuracy is not None:
                        top_20_values.append(om.top_20_accuracy)

                    if om.spearman_correlation is not None and not np.isnan(om.spearman_correlation):
                        z = np.arctanh(np.clip(om.spearman_correlation, -1 + 1e-6, 1 - 1e-6))
                        spearman_z_values.append(z)

                if result.by_position:
                    for pos, metrics in result.by_position.items():
                        if pos in position_data:
                            if metrics.pairwise_accuracy is not None:
                                position_data[pos]['pairwise'].append(metrics.pairwise_accuracy)
                            if metrics.top_5_accuracy is not None:
                                position_data[pos]['top_5'].append(metrics.top_5_accuracy)
                            if metrics.top_10_accuracy is not None:
                                position_data[pos]['top_10'].append(metrics.top_10_accuracy)
                            if metrics.top_20_accuracy is not None:
                                position_data[pos]['top_20'].append(metrics.top_20_accuracy)

                            if metrics.spearman_correlation is not None and not np.isnan(metrics.spearman_correlation):
                                z = np.arctanh(np.clip(metrics.spearman_correlation, -1 + 1e-6, 1 - 1e-6))
                                position_data[pos]['spearman_z'].append(z)

            if pairwise_values or top_5_values or top_10_values or top_20_values or spearman_z_values:
                overall_spearman = None
                if spearman_z_values:
                    z_mean = np.mean(spearman_z_values)
                    overall_spearman = float(np.tanh(z_mean))

                overall_metrics = RankingMetrics(
                    pairwise_accuracy=float(np.mean(pairwise_values)) if pairwise_values else None,
                    top_5_accuracy=float(np.mean(top_5_values)) if top_5_values else None,
                    top_10_accuracy=float(np.mean(top_10_values)) if top_10_values else None,
                    top_20_accuracy=float(np.mean(top_20_values)) if top_20_values else None,
                    spearman_correlation=overall_spearman
                )

            for pos, data in position_data.items():
                if data['pairwise'] or data['top_5'] or data['top_10'] or data['top_20'] or data['spearman_z']:
                    pos_spearman = None
                    if data['spearman_z']:
                        z_mean = np.mean(data['spearman_z'])
                        pos_spearman = float(np.tanh(z_mean))

                    by_position[pos] = RankingMetrics(
                        pairwise_accuracy=float(np.mean(data['pairwise'])) if data['pairwise'] else None,
                        top_5_accuracy=float(np.mean(data['top_5'])) if data['top_5'] else None,
                        top_10_accuracy=float(np.mean(data['top_10'])) if data['top_10'] else None,
                        top_20_accuracy=float(np.mean(data['top_20'])) if data['top_20'] else None,
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
            position: Position to filter ('QB', 'RB', 'WR', 'TE', 'K', 'DST')

        Returns:
            float: Percentage of correct pairwise comparisons (0.0-1.0)

        Note:
            - Filters to players with actual >= 3 points (meaningful performances)
            - Skips tie comparisons (when actual points are equal)
            - Returns np.nan (insufficient-data sentinel) if fewer than 2 qualifying
              players or all ties; a genuine 0.0 accuracy (all comparisons wrong) is 0.0
        """
        players = []
        for player in player_data:
            if player.get('position') == position and player.get('actual', 0) >= 3.0:
                players.append((player.get('projected', 0), player.get('actual', 0)))

        if len(players) < 2:
            self.logger.debug(f"Not enough {position} players for pairwise accuracy")
            return np.nan

        correct = 0
        total = 0

        for i in range(len(players)):
            for j in range(i + 1, len(players)):
                proj_i, actual_i = players[i]
                proj_j, actual_j = players[j]

                if actual_i == actual_j:
                    continue

                predicted_order = proj_i > proj_j
                actual_order = actual_i > actual_j

                if predicted_order == actual_order:
                    correct += 1
                total += 1

        if total == 0:
            self.logger.warning(f"No valid comparisons for {position} (all ties)")
            return np.nan

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
            - Returns np.nan (insufficient-data sentinel) if fewer than N qualifying
              players; a genuine 0.0 overlap is returned as 0.0
            - Uses set intersection formula: overlap / N
        """
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
            return np.nan

        predicted_top_n = set([
            name for name, proj, _ in
            sorted(players, key=lambda x: x[1], reverse=True)[:n]
        ])

        actual_top_n = set([
            name for name, _, actual in
            sorted(players, key=lambda x: x[2], reverse=True)[:n]
        ])

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
            - Returns np.nan (insufficient-data sentinel) if fewer than 2 qualifying
              players, zero variance, or a calculation error; a genuine 0.0 correlation is 0.0
            - Handles NaN and division by zero gracefully
        """
        projected_scores = []
        actual_scores = []

        for player in player_data:
            if player.get('position') == position and player.get('actual', 0) >= 3.0:
                projected_scores.append(player.get('projected', 0))
                actual_scores.append(player.get('actual', 0))

        if len(projected_scores) < 2:
            self.logger.debug(f"Not enough {position} players for correlation")
            return np.nan

        try:
            corr, pvalue = spearmanr(projected_scores, actual_scores)

            if np.isnan(corr):
                self.logger.warning(
                    f"Zero variance in {position} predictions or actuals"
                )
                return np.nan

            self.logger.debug(
                f"{position} Spearman correlation: {corr:.3f} (p={pvalue:.4f})"
            )
            return float(corr)

        except (ZeroDivisionError, ValueError) as e:
            self.logger.warning(
                f"Correlation calculation failed for {position}: {e}"
            )
            return np.nan

    def calculate_ranking_metrics_for_season(
        self,
        player_data_by_week: Dict[int, List[Dict[str, Any]]]
    ) -> Tuple['RankingMetrics', Dict[str, 'RankingMetrics']]:
        """
        Calculate ranking metrics across weeks and positions for a season.

        Aggregates using:
        - Pairwise/Top-N: Simple average across weeks
        - Spearman: Fisher z-transformation for proper averaging

        Args:
            player_data_by_week: Dict of week -> list of player dicts with keys:
                - 'name': Player name
                - 'position': Player position (QB, RB, WR, TE, K, DST)
                - 'projected': Projected points
                - 'actual': Actual points

        Returns:
            Tuple of (overall_metrics, by_position_metrics)
        """
        positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']

        position_data = {pos: {
            'pairwise_sum': 0.0,
            'pairwise_count': 0,
            'top_5_sum': 0.0,
            'top_5_count': 0,
            'top_10_sum': 0.0,
            'top_10_count': 0,
            'top_20_sum': 0.0,
            'top_20_count': 0,
            'spearman_z_values': []
        } for pos in positions}

        for week_num, player_list in player_data_by_week.items():
            for pos in positions:
                pairwise = self.calculate_pairwise_accuracy(
                    player_list, pos
                )
                if not np.isnan(pairwise):
                    position_data[pos]['pairwise_sum'] += pairwise
                    position_data[pos]['pairwise_count'] += 1

                for n in [5, 10, 20]:
                    top_n = self.calculate_top_n_accuracy(
                        player_list, n, pos
                    )
                    if not np.isnan(top_n):
                        position_data[pos][f'top_{n}_sum'] += top_n
                        position_data[pos][f'top_{n}_count'] += 1

                corr = self.calculate_spearman_correlation(
                    player_list, pos
                )
                if not np.isnan(corr):
                    z = np.arctanh(np.clip(corr, -1 + 1e-6, 1 - 1e-6))
                    position_data[pos]['spearman_z_values'].append(z)

        by_position = {}
        for pos in positions:
            data = position_data[pos]

            has_any_metric = (
                data['pairwise_count'] > 0
                or data['top_5_count'] > 0
                or data['top_10_count'] > 0
                or data['top_20_count'] > 0
                or bool(data['spearman_z_values'])
            )
            if not has_any_metric:
                self.logger.debug(f"No valid data for {pos}, skipping ranking metrics")
                continue

            if data['spearman_z_values']:
                z_mean = np.mean(data['spearman_z_values'])
                spearman = float(np.tanh(z_mean))
            else:
                spearman = None

            by_position[pos] = RankingMetrics(
                pairwise_accuracy=(data['pairwise_sum'] / data['pairwise_count']) if data['pairwise_count'] > 0 else None,
                top_5_accuracy=(data['top_5_sum'] / data['top_5_count']) if data['top_5_count'] > 0 else None,
                top_10_accuracy=(data['top_10_sum'] / data['top_10_count']) if data['top_10_count'] > 0 else None,
                top_20_accuracy=(data['top_20_sum'] / data['top_20_count']) if data['top_20_count'] > 0 else None,
                spearman_correlation=spearman
            )

        if by_position:
            all_z_values = []
            for data in position_data.values():
                all_z_values.extend(data['spearman_z_values'])

            overall_spearman = None
            if all_z_values:
                z_mean = np.mean(all_z_values)
                overall_spearman = float(np.tanh(z_mean))

            pairwise_vals = [m.pairwise_accuracy for m in by_position.values() if m.pairwise_accuracy is not None]
            top_5_vals = [m.top_5_accuracy for m in by_position.values() if m.top_5_accuracy is not None]
            top_10_vals = [m.top_10_accuracy for m in by_position.values() if m.top_10_accuracy is not None]
            top_20_vals = [m.top_20_accuracy for m in by_position.values() if m.top_20_accuracy is not None]

            overall_metrics = RankingMetrics(
                pairwise_accuracy=float(np.mean(pairwise_vals)) if pairwise_vals else None,
                top_5_accuracy=float(np.mean(top_5_vals)) if top_5_vals else None,
                top_10_accuracy=float(np.mean(top_10_vals)) if top_10_vals else None,
                top_20_accuracy=float(np.mean(top_20_vals)) if top_20_vals else None,
                spearman_correlation=overall_spearman
            )
        else:
            overall_metrics = None

        return overall_metrics, by_position


