"""
Accuracy Results Manager

Manages results storage and best configuration tracking for accuracy simulation.
Similar to shared/ResultsManager but selection compares pairwise ranking accuracy
(higher is better); MAE is stored as a reported diagnostic.

Key differences from win-rate ResultsManager:
- Selection optimizes pairwise ranking accuracy (higher is better); MAE stored as a diagnostic
- Metrics include mae, player_count instead of win_rate, total_wins
- Output folder naming: accuracy_optimal_TIMESTAMP/

Selection optimizes pairwise ranking accuracy, NOT MAE — do not revert `is_better_than` to an
MAE comparison; the League Helper's decisions are ordinal. MAE is a reported diagnostic only.

Author: Kai Mizuno
"""

import copy
import json
import math
from datetime import datetime
from logging import Logger
from pathlib import Path
from typing import Dict, List, Optional, Any

from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.utils.LoggingManager import get_logger
from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.utils.error_handler import FileOperationError
from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.simulation.shared.atomic_io import atomic_write_json
from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.simulation.shared.config_cleanup import cleanup_old_accuracy_optimal_folders
from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.simulation.shared.config_constants import WEEK_SPECIFIC_PARAMS
from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.simulation.shared.config_filters import extract_base_params

from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.simulation.shared.ConfigGenerator import ConfigGenerator
from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.simulation.accuracy.accuracy_types import RankingMetrics
from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.simulation.accuracy.AccuracyCalculator import AccuracyResult

# Re-exported, not redefined: the single definition lives in
# simulation/accuracy/horizon_labels.py (T77 D1/D2). Kept importable from here
# so the three existing importers - AccuracySimulationManager,
# tests/simulation/test_AccuracyResultsManager.py and
# tests/integration/test_accuracy_simulation_integration.py - are untouched.
from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.simulation.accuracy.horizon_labels import WEEK_RANGES  # noqa: F401
# T69/D2: the per-season consistency gate's supermajority fraction. The THRESHOLD is derived
# from the season count at comparison time -- never hardcoded -- because seasons are
# discovered at runtime by scanning the --data folder (AccuracySimulationManager._discover_
# seasons), so N varies by corpus.
ADOPTION_SEASON_WIN_FRACTION = 0.8

# D2.2 (TD2/TD2a/D1): the per-candidate results dump. Both filenames are FIXED, concrete
# constants -- never runtime-discovered or globbed -- because D11 and D16 consume the
# promoted artifact as a cross-ticket interface (context.md "Interfaces and Boundaries").
# DUMP_SCRATCH_FILENAME lives at self.output_dir ROOT (never inside an accuracy_intermediate_*
# folder), so cleanup_accuracy_intermediate_folders never targets it (Trap 1 closed by
# construction) and a resumed process's fresh AccuracyResultsManager reopens the SAME path in
# append mode (Trap 2 closed by a fixed, output_dir-relative path). DUMP_PROMOTED_FILENAME is
# the durable per-candidate JSON array save_optimal_configs() writes into the accuracy_optimal_*
# folder once promotion succeeds; the scratch file is deleted at that point.
DUMP_SCRATCH_FILENAME = '_accuracy_candidate_dump.jsonl'
DUMP_PROMOTED_FILENAME = 'candidate_results.json'


def _min_season_wins(n_seasons: int) -> int:
    """Seasons a candidate must win to be adoptable, derived from the ACTUAL season count.

    NEVER replace this with a literal count. A hardcoded threshold tuned for the default
    5-season corpus would be UNSATISFIABLE on a smaller one -- nothing would ever be
    adopted, every horizon would freeze on the first pass, and the run would report
    convergence having optimized nothing. That failure is invisible from outside: it
    terminates cleanly and looks like success.

    ceil(0.8 * n) <= n for all n >= 1, so the threshold is always satisfiable.

    Args:
        n_seasons (int): Number of seasons shared by the two configs being compared.

    Returns:
        int: Minimum season wins required for adoption.
    """
    return math.ceil(ADOPTION_SEASON_WIN_FRACTION * n_seasons)


def format_metric_pct(value: Optional[float]) -> str:
    """Format a ranking metric as a percentage for display.

    Args:
        value: A metric in 0.0-1.0, or None when the metric had zero valid weeks.

    Returns:
        The value formatted as a percentage (e.g. "68.0%"), or "N/A" when value is None.
    """
    return f"{value:.1%}" if value is not None else "N/A"


def format_metric_corr(value: Optional[float]) -> str:
    """Format a correlation metric to three decimals for display.

    Args:
        value: A correlation in -1.0 to 1.0, or None when the metric had zero valid weeks.

    Returns:
        The value formatted to three decimals (e.g. "0.820"), or "N/A" when value is None.
    """
    return f"{value:.3f}" if value is not None else "N/A"


class AccuracyConfigPerformance:
    """
    Performance record for a configuration in accuracy simulation.

    Attributes:
        config_dict (dict): The configuration that was tested
        mae (float): Mean Absolute Error — diagnostic metric (lower = better absolute-value fidelity; NOT the selection objective)
        player_count (int): Number of players evaluated
        total_error (float): Sum of all absolute errors
        config_value (Optional[Any]): Value of the parameter that was tested (tournament mode)
        timestamp (str): When the test was run
        param_name (Optional[str]): Parameter being optimized (tournament mode)
        test_idx (Optional[int]): Test value index (tournament mode)
        base_horizon (Optional[str]): Horizon this config originated from (tournament mode)
        weeks_evaluated (int): Weeks actually scored (observability; default 0)
        weeks_requested (int): Weeks requested by the horizon range (observability; default 0)
    """

    def __init__(
        self,
        config_dict: dict,
        mae: float,
        player_count: int,
        total_error: float,
        config_value: Optional[Any] = None,
        timestamp: Optional[str] = None,
        param_name: Optional[str] = None,
        test_idx: Optional[int] = None,
        base_horizon: Optional[str] = None,
        overall_metrics: Optional[RankingMetrics] = None,
        by_position: Optional[Dict[str, RankingMetrics]] = None,
        weeks_evaluated: int = 0,
        weeks_requested: int = 0,
        per_season_pairwise: Optional[Dict[str, float]] = None
    ) -> None:
        self.config_dict = copy.deepcopy(config_dict)
        self.mae = mae
        self.player_count = player_count
        self.total_error = total_error
        self.config_value = config_value if config_value is not None else self._extract_param_value(config_dict, param_name)
        self.timestamp = timestamp or datetime.now().isoformat()
        self.param_name = param_name
        self.test_idx = test_idx
        self.base_horizon = base_horizon
        self.overall_metrics = overall_metrics
        self.by_position = by_position or {}
        self.weeks_evaluated = weeks_evaluated
        self.weeks_requested = weeks_requested
        # T69/D3: per-season pairwise accuracies backing the consistency gate in
        # is_better_than. Empty for a config reconstructed from a pre-T69 artifact, which
        # is why the gate degrades rather than assuming presence.
        self.per_season_pairwise = per_season_pairwise or {}

    def _extract_param_value(self, config: dict, param_name: Optional[str]) -> Optional[Any]:
        """
        Extract the parameter value from config_dict based on param_name.

        Args:
            config: Configuration dictionary (may have 'parameters' wrapper or be raw)
            param_name: Parameter being optimized (e.g., "WIND_SCORING_WEIGHT")

        Returns:
            The value of the parameter, or None if not found
        """
        if not param_name:
            return None

        params = config.get('parameters', config)

        if param_name.startswith('LOCATION_'):
            location_type = param_name[len('LOCATION_'):]
            return params.get('LOCATION_MODIFIERS', {}).get(location_type)

        if param_name in params:
            return params[param_name]

        for suffix in ['_WEIGHT', '_IMPACT_SCALE', '_MIN_WEEKS', '_STEPS']:
            if param_name.endswith(suffix):
                component = param_name[:-len(suffix)]
                param = suffix[1:]
                return params.get(component, {}).get(param)

        return None

    def is_better_than(self, other: 'AccuracyConfigPerformance') -> bool:
        """
        Check if this configuration is better than another.

        ALWAYS uses pairwise_accuracy as the primary metric (no MAE fallback).
        MAE is for diagnostics/user visibility only.

        Args:
            other: Configuration to compare against

        Returns:
            bool: True if this config is better, False otherwise.
                  Returns False if this config has player_count=0 or missing overall_metrics.
                  Returns True if other is None or has missing overall_metrics.
                  When overall_metrics is present but pairwise_accuracy is None (no usable
                  primary metric), the same policy applies: returns False if this config's
                  pairwise_accuracy is None (not better), and True if only the other's is None
                  (this config wins). Both None resolves to False (this config checked first).
        """
        if self.player_count == 0:
            return False

        if not self.overall_metrics:
            return False

        if other is None:
            return True

        if other.player_count == 0:
            return False

        if not other.overall_metrics:
            return True

        if self.overall_metrics.pairwise_accuracy is None:
            return False

        if other.overall_metrics.pairwise_accuracy is None:
            return True

        # T69/D2: per-season consistency gate. Guards against a difference driven by one or
        # two idiosyncratic seasons -- NOT against sampling noise. Accuracy evaluation is
        # DETERMINISTIC (no random draws), so re-evaluating a config yields an identical
        # number; the win-rate side's z-test solves a different problem and this must not be
        # "aligned" with it.
        shared = sorted(set(self.per_season_pairwise) & set(other.per_season_pairwise))
        if len(shared) >= 2:
            wins = sum(
                self.per_season_pairwise[s] > other.per_season_pairwise[s]
                for s in shared
            )
            if wins < _min_season_wins(len(shared)):
                return False
        # Fewer than 2 shared seasons -> degrade to the pre-T69 mean comparison (a config
        # reconstructed from an older artifact carries no per-season map, and one season
        # cannot evidence consistency). Reaching here also means the consistency check
        # PASSED, so the original mean comparison still decides.
        return self.overall_metrics.pairwise_accuracy > other.overall_metrics.pairwise_accuracy

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        result = {
            'config_value': self.config_value,
            'mae': self.mae,
            'player_count': self.player_count,
            'total_error': self.total_error,
            'timestamp': self.timestamp,
            'config': self.config_dict
        }

        if self.overall_metrics:
            result['pairwise_accuracy'] = self.overall_metrics.pairwise_accuracy
            result['top_5_accuracy'] = self.overall_metrics.top_5_accuracy
            result['top_10_accuracy'] = self.overall_metrics.top_10_accuracy
            result['top_20_accuracy'] = self.overall_metrics.top_20_accuracy
            result['spearman_correlation'] = self.overall_metrics.spearman_correlation

        if self.per_season_pairwise:
            result['per_season_pairwise'] = dict(self.per_season_pairwise)

        if self.by_position:
            result['by_position'] = {
                pos: {
                    'pairwise_accuracy': metrics.pairwise_accuracy,
                    'top_5_accuracy': metrics.top_5_accuracy,
                    'top_10_accuracy': metrics.top_10_accuracy,
                    'top_20_accuracy': metrics.top_20_accuracy,
                    'spearman_correlation': metrics.spearman_correlation
                }
                for pos, metrics in self.by_position.items()
            }

        return result

    @classmethod
    def from_dict(cls, data: dict) -> 'AccuracyConfigPerformance':
        """Create from dictionary.

        Handles both old format (MAE only) and new format (with ranking metrics).
        Provides backward compatibility (Q25) for loading old result files.
        """
        mae = data['mae']
        player_count = data['player_count']
        total_error = data.get('total_error', mae * player_count)

        overall_metrics = None
        if 'pairwise_accuracy' in data:
            overall_metrics = RankingMetrics(
                pairwise_accuracy=data['pairwise_accuracy'],
                top_5_accuracy=data['top_5_accuracy'],
                top_10_accuracy=data['top_10_accuracy'],
                top_20_accuracy=data['top_20_accuracy'],
                spearman_correlation=data['spearman_correlation']
            )

        by_position = {}
        if 'by_position' in data:
            for pos, metrics_dict in data['by_position'].items():
                by_position[pos] = RankingMetrics(
                    pairwise_accuracy=metrics_dict['pairwise_accuracy'],
                    top_5_accuracy=metrics_dict['top_5_accuracy'],
                    top_10_accuracy=metrics_dict['top_10_accuracy'],
                    top_20_accuracy=metrics_dict['top_20_accuracy'],
                    spearman_correlation=metrics_dict['spearman_correlation']
                )

        return cls(
            config_dict=data['config'],
            mae=mae,
            player_count=player_count,
            total_error=total_error,
            config_value=data.get('config_value'),
            timestamp=data.get('timestamp'),
            overall_metrics=overall_metrics,
            by_position=by_position,
            # T69/D3: .get() not [] -- an artifact written before T69 has no such key, and
            # AC6 requires those to still compare (the gate degrades to the mean).
            per_season_pairwise=data.get('per_season_pairwise', {})
        )

    def __repr__(self) -> str:
        return f"AccuracyConfigPerformance(mae={self.mae:.4f}, players={self.player_count})"


class AccuracyResultsManager:
    """
    Manages accuracy simulation results storage and tracking.

    Tracks best configurations per week range and saves results to disk.
    Selects the best config by pairwise ranking accuracy (higher is better); MAE is a reported diagnostic.

    Attributes:
        output_dir (Path): Base directory for results
        baseline_config_path (Path): Path to baseline config folder
        best_configs (Dict): Best config per week range
        all_results (List): All tested configurations
        logger: Logger instance
    """

    def __init__(self, output_dir: Path, baseline_config_path: Path) -> None:
        """
        Initialize AccuracyResultsManager.

        Args:
            output_dir (Path): Directory to save results
            baseline_config_path (Path): Path to baseline config folder
        """
        self.logger = get_logger()
        self.output_dir = output_dir
        self.baseline_config_path = baseline_config_path
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.best_configs: Dict[str, AccuracyConfigPerformance] = {
            'week_1_5': None,
            'week_6_9': None,
            'week_10_13': None,
            'week_14_17': None,
        }

        self.all_results: List[AccuracyConfigPerformance] = []

        # D2.2 Polish finding 7: latches after the first per-candidate scratch-append
        # failure so a persistent fault (disk full, read-only mount) logs one WARNING
        # per run rather than once per evaluated candidate (up to the spec's own
        # ~7,040-candidate upper bound). See _append_candidate_record.
        self._candidate_dump_write_failed = False
        self._candidate_dump_write_failures = 0

        self.logger.info(f"AccuracyResultsManager initialized: {output_dir}")

    def add_result(
        self,
        week_range_key: str,
        config_dict: dict,
        accuracy_result: AccuracyResult,
        param_name: Optional[str] = None,
        test_idx: Optional[int] = None,
        base_horizon: Optional[str] = None,
        pass_idx: Optional[int] = None
    ) -> bool:
        """
        Add a configuration result and check if it's the new best.

        D2.2: every call also appends one record to the per-candidate scratch dump
        (see _append_candidate_record) -- write-only, additive, no resume role (TD2a).

        Args:
            week_range_key: 'ros', 'week_1_5', 'week_6_9', etc.
            config_dict: The configuration that was tested
            accuracy_result: AccuracyResult from AccuracyCalculator
            param_name: Parameter being optimized (tournament mode)
            test_idx: Test value index (tournament mode)
            base_horizon: Horizon this config originated from (tournament mode)
            pass_idx: Coordinate-ascent pass index this candidate was evaluated in
                (threaded from AccuracySimulationManager._run_ascent_pass)

        Returns:
            bool: True if this is the new best for the week range
        """
        config_copy = copy.deepcopy(config_dict)

        perf = AccuracyConfigPerformance(
            config_dict=config_copy,
            mae=accuracy_result.mae,
            player_count=accuracy_result.player_count,
            total_error=accuracy_result.total_error,
            param_name=param_name,
            test_idx=test_idx,
            base_horizon=base_horizon,
            overall_metrics=accuracy_result.overall_metrics,
            by_position=accuracy_result.by_position,
            weeks_evaluated=accuracy_result.weeks_evaluated,
            weeks_requested=accuracy_result.weeks_requested,
            per_season_pairwise=accuracy_result.per_season_pairwise
        )

        self.all_results.append(perf)
        self.logger.debug(f"add_result({week_range_key}): MAE={perf.mae:.4f}, players={perf.player_count}")

        current_best = self.best_configs.get(week_range_key)
        adopted = perf.is_better_than(current_best)

        # D2.2/D1: unconditional -- every evaluated candidate gets one scratch record,
        # adopted or not, so the promoted artifact carries the full per-candidate
        # distribution (context.md TD2), not only the winners best_configs already tracks.
        # `base_horizon` is included (widening the cross-ticket interface from nine fields
        # to ten -- Polish D2.2 finding 4) because a fixed (horizon, pass_idx, param_name,
        # test_idx) tuple is produced by up to four distinct base horizons in tournament
        # mode (AccuracySimulationManager._run_ascent_pass), so it is the only field that
        # uniquely keys a record.
        self._append_candidate_record({
            'horizon': week_range_key,
            'pass_idx': pass_idx,
            'param_name': param_name,
            'test_idx': test_idx,
            'base_horizon': base_horizon,
            'config_value': perf.config_value,
            'pairwise_accuracy': perf.overall_metrics.pairwise_accuracy if perf.overall_metrics else None,
            'per_season_pairwise': dict(perf.per_season_pairwise),
            'adopted': adopted,
            'incumbent_pairwise': (
                current_best.overall_metrics.pairwise_accuracy
                if (current_best and current_best.overall_metrics) else None
            ),
        })

        if adopted:
            previous_mae = f"{current_best.mae:.4f}" if current_best else "N/A"
            self.best_configs[week_range_key] = perf

            if perf.overall_metrics:
                self.logger.info(
                    f"New best for {week_range_key}: "
                    f"Pairwise={format_metric_pct(perf.overall_metrics.pairwise_accuracy)} | "
                    f"Top-10={format_metric_pct(perf.overall_metrics.top_10_accuracy)} | "
                    f"Spearman={format_metric_corr(perf.overall_metrics.spearman_correlation)} | "
                    f"MAE={perf.mae:.4f} (diag) | "
                    f"(prev MAE: {previous_mae})"
                )
            else:
                self.logger.info(
                    f"New best for {week_range_key}: MAE={perf.mae:.4f} "
                    f"(previous: {previous_mae})"
                )
            return True

        return False

    def _append_candidate_record(self, record: dict) -> None:
        """Append one per-candidate record to the scratch dump (D1/D2).

        Opened in append mode against a FIXED output_dir-relative path
        (DUMP_SCRATCH_FILENAME) so a resumed process's fresh AccuracyResultsManager
        reopens and continues the SAME file (Trap 2, TD2a) -- process-boundary-
        transparent by construction. One write() call for the complete JSON line
        minimizes the torn-write window to a single syscall (D2);
        save_optimal_configs()'s promotion step tolerates the rare remaining
        torn-line case by dropping it, position-independent, rather than
        preventing it here. Write-only: nothing in the engine reads this file back
        (TD2a's no-resume-role prohibition).

        Non-essential instrumentation, never the measurement: an OSError here
        (disk full, read-only mount, permissions) is logged at WARNING and
        swallowed rather than propagated, so a failure to write this scratch
        record can never abort the multi-hour sweep it is merely observing
        (Polish D2.2 finding 2, following the house pattern stated at
        simulation/shared/config_cleanup.py:81-84). A persistent fault is by
        construction repeated on every subsequent call, so the WARNING is
        latched: only the FIRST failure this run logs at WARNING, every
        subsequent failure logs at DEBUG, and the total dropped-record count is
        surfaced once more as a single summary WARNING when this run's dump is
        promoted (Polish D2.2 finding 7 -- unlatched, a persistent failure would
        log up to the spec's own ~7,040-candidate upper bound of identical
        lines per run).

        Args:
            record: The ten-field candidate record (JSON-serializable dict).
        """
        scratch_path = self.output_dir / DUMP_SCRATCH_FILENAME
        try:
            with open(scratch_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(record) + "\n")
        except OSError as e:
            self._candidate_dump_write_failures += 1
            message = (
                f"Failed to append candidate-dump record to {scratch_path.name}: {e} "
                "-- continuing without this record (instrumentation only, not the run)"
            )
            if self._candidate_dump_write_failed:
                self.logger.debug(message)
            else:
                self._candidate_dump_write_failed = True
                self.logger.warning(message)

    def reset_candidate_dump(self) -> None:
        """Delete the scratch candidate dump so a fresh (non-resumed) ascent never
        merges an abandoned run's records into its own promoted dump.

        `AccuracySimulationManager._detect_resume_state` has three branches that
        return `should_resume=False` while a scratch file can still be on disk
        (no intermediate folders found; a parameter-order mismatch; all
        parameters complete and all horizons frozen) and none of them reset the
        scratch -- so the caller invokes this method whenever it decides NOT to
        resume, before evaluating the first candidate of the new ascent
        (Polish D2.2 finding 1). Idempotent and safe to call even when no
        scratch file exists.
        """
        scratch_path = self.output_dir / DUMP_SCRATCH_FILENAME
        try:
            scratch_path.unlink(missing_ok=True)
        except OSError as e:
            self.logger.warning(
                f"Failed to reset candidate-dump scratch file {scratch_path.name}: {e} "
                "-- a fresh ascent may merge with a prior abandoned run's records"
            )

    def get_best_config(self, week_range_key: str) -> Optional[AccuracyConfigPerformance]:
        """Get the best configuration for a week range."""
        return self.best_configs.get(week_range_key)

    def _sync_schedule_params(self, config: dict) -> dict:
        """
        Sync SCHEDULE params with MATCHUP params.

        SCHEDULE and MATCHUP should use the same values because schedule strength
        is a forward-looking version of matchup strength. Keeping them in sync
        ensures consistent opponent evaluation.

        Params synced:
        - SCHEDULE_SCORING.IMPACT_SCALE = MATCHUP_SCORING.IMPACT_SCALE
        - SCHEDULE_SCORING.WEIGHT = MATCHUP_SCORING.WEIGHT
        - SCHEDULE_SCORING.MIN_WEEKS = MATCHUP_SCORING.MIN_WEEKS

        Args:
            config: Configuration dictionary to update (nested structure)

        Returns:
            dict: Updated config with synced SCHEDULE params
        """
        import copy
        synced = copy.deepcopy(config)

        if 'MATCHUP_SCORING' in synced:
            matchup = synced['MATCHUP_SCORING']
            schedule = synced.get('SCHEDULE_SCORING', {})

            if 'IMPACT_SCALE' in matchup:
                schedule['IMPACT_SCALE'] = matchup['IMPACT_SCALE']
            if 'WEIGHT' in matchup:
                schedule['WEIGHT'] = matchup['WEIGHT']
            if 'MIN_WEEKS' in matchup:
                schedule['MIN_WEEKS'] = matchup['MIN_WEEKS']

            synced['SCHEDULE_SCORING'] = schedule

        return synced

    def save_optimal_configs(self) -> Path:
        """
        Save all optimal configurations to a timestamped folder.

        Creates folder structure that can be used as baseline for future runs:
            accuracy_optimal_TIMESTAMP/
            ├── league_config.json      # Baseline base params, filtered to BASE_CONFIG_PARAMS
            ├── week1-5.json            # Weekly optimal (prediction params)
            ├── week6-9.json
            ├── week10-13.json
            └── week14-17.json

        Returns:
            Path: Path to the created optimal folder
        """
        self.logger.info("=" * 60)
        self.logger.info("SAVING OPTIMAL CONFIGS")
        self.logger.info("=" * 60)
        self.logger.info(f"Current best_configs state:")
        for week_key, perf in self.best_configs.items():
            if perf:
                if perf.overall_metrics:
                    self.logger.info(
                        f"  {week_key}: "
                        f"Pairwise={format_metric_pct(perf.overall_metrics.pairwise_accuracy)} | "
                        f"Top-10={format_metric_pct(perf.overall_metrics.top_10_accuracy)} | "
                        f"Spearman={format_metric_corr(perf.overall_metrics.spearman_correlation)} | "
                        f"MAE={perf.mae:.4f} (diag) | "
                        f"players={perf.player_count} | value={perf.config_value}"
                    )
                else:
                    self.logger.info(f"  {week_key}: MAE={perf.mae:.4f}, players={perf.player_count}, value={perf.config_value}")
            else:
                self.logger.info(f"  {week_key}: None")

        cleanup_old_accuracy_optimal_folders(self.output_dir)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        optimal_folder = self.output_dir / f"accuracy_optimal_{timestamp}"
        optimal_folder.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Creating optimal folder: {optimal_folder.name}")

        baseline_league_config = self.baseline_config_path / 'league_config.json'
        if baseline_league_config.exists():
            # Ownership filter (T90 D1): the --baseline folder's base config is
            # written FILTERED to BASE_CONFIG_PARAMS, never copied verbatim, so a
            # new accuracy_optimal_* folder is born free of week-owned keys. This
            # matches the WEEK_SPECIFIC_PARAMS filter the week branch below already
            # applies to the other half of the ownership split.
            with open(baseline_league_config, 'r') as f:
                baseline_config = json.load(f)

            base_config_output = extract_base_params(baseline_config)

            # Atomic: this folder is reusable as a `--promote` source, so a
            # truncated league_config.json here would be promoted to live as a
            # corrupt base config. T64 established atomicity for the promote
            # path; the same reasoning applies to the file that feeds it.
            atomic_write_json(base_config_output, optimal_folder / 'league_config.json')

            self.logger.info("Wrote league_config.json from baseline (base params only)")
        else:
            self.logger.warning(f"No league_config.json found in baseline: {self.baseline_config_path}")

        file_mapping = {
            'week_1_5': ('week1-5.json', 'Weeks 1-5 prediction parameters'),
            'week_6_9': ('week6-9.json', 'Weeks 6-9 prediction parameters'),
            'week_10_13': ('week10-13.json', 'Weeks 10-13 prediction parameters'),
            'week_14_17': ('week14-17.json', 'Weeks 14-17 prediction parameters'),
        }

        for week_key, (filename, description) in file_mapping.items():
            perf = self.best_configs.get(week_key)
            self.logger.info(f"Processing {week_key} -> {filename}")
            if perf:
                self.logger.info(f"  Has results: MAE={perf.mae:.4f}, using real performance data")
                synced_config = self._sync_schedule_params(perf.config_dict)

                week_params_dict = {
                    key: synced_config.get('parameters', synced_config).get(key)
                    for key in WEEK_SPECIFIC_PARAMS
                    if key in synced_config.get('parameters', synced_config)
                }

                perf_metrics = {
                    'mae': perf.mae,
                    'player_count': perf.player_count,
                    'total_error': perf.total_error,
                    'config_value': perf.config_value,
                    'timestamp': perf.timestamp,
                    'weeks_evaluated': perf.weeks_evaluated,
                    'weeks_requested': perf.weeks_requested
                }
                if perf.overall_metrics:
                    perf_metrics['ranking_metrics'] = {
                        'pairwise_accuracy': perf.overall_metrics.pairwise_accuracy,
                        'top_5_accuracy': perf.overall_metrics.top_5_accuracy,
                        'top_10_accuracy': perf.overall_metrics.top_10_accuracy,
                        'top_20_accuracy': perf.overall_metrics.top_20_accuracy,
                        'spearman_correlation': perf.overall_metrics.spearman_correlation
                    }

                config_output = {
                    'config_name': f"Accuracy Optimal {filename.replace('.json', '')} ({timestamp})",
                    'description': description,
                    'parameters': week_params_dict,
                    'performance_metrics': perf_metrics
                }

                config_path = optimal_folder / filename
                with open(config_path, 'w') as f:
                    json.dump(config_output, f, indent=2)

                self.logger.info(f"  Saved {filename}: MAE={perf.mae:.4f}")
            else:
                self.logger.info(f"  No results - loading params from baseline")
                baseline_file = self.baseline_config_path / filename
                if baseline_file.exists():
                    self.logger.info(f"  Baseline file exists: {baseline_file}")
                    with open(baseline_file, 'r') as f:
                        baseline_data = json.load(f)

                    baseline_params = baseline_data.get('parameters', {})

                    config_output = {
                        'config_name': f"Accuracy Optimal {filename.replace('.json', '')} ({timestamp})",
                        'description': description,
                        'parameters': baseline_params,
                        'performance_metrics': {
                            'mae': None,
                            'player_count': None,
                            'total_error': None,
                            'config_value': None,
                            'timestamp': timestamp,
                            'note': 'No optimization performed - using baseline parameters'
                        }
                    }

                    config_path = optimal_folder / filename
                    with open(config_path, 'w') as f:
                        json.dump(config_output, f, indent=2)

                    self.logger.info(f"  Saved {filename} with baseline params (mae=None)")
                else:
                    self.logger.warning(f"  Baseline file NOT found: {baseline_file}")

        configs_saved = len(file_mapping) + 1
        self.logger.info(
            f"Saved {configs_saved} optimal config files "
            f"(1 league config + {len(file_mapping)} weekly configs). "
            f"Location: {optimal_folder}"
        )

        self._promote_candidate_dump(optimal_folder)

        self.logger.info("=" * 60)
        return optimal_folder

    def _promote_candidate_dump(self, optimal_folder: Path) -> None:
        """Promote the scratch candidate dump into optimal_folder (D1), dropping any
        torn line with a logged warning rather than raising (D2).

        An interrupted-then-resumed run loses at most TWO candidate records per resume
        boundary -- the killed process's partial record and the resuming process's
        complete first append, which merge into one unparseable line and are dropped
        together -- never a crash or a corrupted artifact for D11/D16 (Polish D2.2
        finding 5; the bound is two, not one, per test_promote_drops_nonterminal_torn_line).

        Absent scratch file (pre-existing engine, or a run that evaluated zero
        candidates) is skipped without promoting (logged at INFO) -- never fabricates
        an empty dump. Runs BEFORE cleanup_accuracy_intermediate_folders
        (AccuracySimulationManager.py, called after save_optimal_configs() returns),
        so the promoted artifact exists before that cleanup pass runs; it lives in
        this accuracy_optimal_* folder, never an accuracy_intermediate_* one, so
        cleanup never targets it either way (Trap 1, closed by construction).

        Non-essential instrumentation, never the measurement: a failure anywhere in this
        method's body -- the scratch read, the promoted-artifact write, or the final
        scratch unlink -- (disk full, read-only mount, permissions, a corrupted-beyond-
        per-line-recovery scratch file) is logged at WARNING and swallowed rather than
        propagated, so a promotion failure can never make save_optimal_configs() raise
        for a run whose real deliverable -- the five optimal config files, already
        written and logged above -- landed correctly (Polish D2.2 findings 2 and 6,
        following the house pattern at simulation/shared/config_cleanup.py:81-84). The
        guard is method-wide, not write-only, precisely so this claim is exactly true
        rather than true only of the write.

        Args:
            optimal_folder: The just-created accuracy_optimal_* folder.
        """
        scratch_path = self.output_dir / DUMP_SCRATCH_FILENAME
        if not scratch_path.exists():
            self.logger.info(
                "No candidate dump scratch file found -- skipping promotion "
                "(pre-existing engine, or zero candidates evaluated this run)"
            )
            return

        try:
            records = []
            dropped = 0
            with open(scratch_path, 'r', encoding='utf-8') as f:
                for line_num, raw_line in enumerate(f, start=1):
                    line = raw_line.strip()
                    if not line:
                        continue
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        dropped += 1
                        self.logger.warning(
                            f"Dropping unparseable candidate-dump line {line_num} in "
                            f"{scratch_path.name} (likely a torn write from a killed process)"
                        )
        except OSError as e:
            self.logger.warning(
                f"Failed to read candidate-dump scratch file {scratch_path.name}: {e} "
                "-- the run's real deliverable (optimal config files) is unaffected; "
                "the per-candidate distribution for this run is unavailable"
            )
            return

        promoted_path = optimal_folder / DUMP_PROMOTED_FILENAME
        try:
            atomic_write_json(records, promoted_path)
        except (OSError, FileOperationError) as e:
            self.logger.warning(
                f"Failed to promote candidate dump to {promoted_path.name}: {e} "
                "-- the run's real deliverable (optimal config files) is unaffected; "
                "the per-candidate distribution for this run is unavailable"
            )
            return

        try:
            scratch_path.unlink(missing_ok=True)
        except OSError as e:
            self.logger.warning(
                f"Failed to remove promoted scratch file {scratch_path.name}: {e} "
                "-- the promoted candidate dump was written successfully; the stale "
                "scratch file will be re-read (and its records re-promoted) next run"
            )

        self.logger.info(
            f"Promoted {len(records)} candidate record(s) to {promoted_path.name}"
            + (f" ({dropped} torn line(s) dropped)" if dropped else "")
        )

        # D2.2 Polish finding 7: the per-candidate append WARNING is latched to one
        # per run (_append_candidate_record); this is the promised single summary,
        # naming the total count so a persistent write failure is still visible.
        if self._candidate_dump_write_failures:
            self.logger.warning(
                f"{self._candidate_dump_write_failures} candidate record(s) were not "
                f"recorded this run due to scratch-append failures -- "
                "see the first-failure WARNING above for the cause"
            )

    def save_intermediate_results(
        self,
        param_idx: int,
        param_name: str,
        week_range_prefix: str = '',
        pass_idx: int = 0,
        frozen_horizons: Optional[set] = None
    ) -> Path:
        """
        Save intermediate results during iterative optimization.

        Creates folder that can serve as baseline for future runs:
            accuracy_intermediate_{idx}_{prefix}_{param}/
            ├── league_config.json      # Copied from baseline
            ├── week1-5.json            # Weekly best (or from baseline)
            ├── week6-9.json
            ├── week10-13.json
            └── week14-17.json

        Args:
            param_idx: Current parameter index
            param_name: Name of the parameter being optimized
            week_range_prefix: Optional prefix for week range being optimized

        Returns:
            Path: Path to the created intermediate folder
        """
        if week_range_prefix:
            folder_name = f"accuracy_intermediate_{param_idx:02d}_{week_range_prefix}_{param_name}"
        else:
            folder_name = f"accuracy_intermediate_{param_idx:02d}_{param_name}"
        intermediate_folder = self.output_dir / folder_name
        intermediate_folder.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        baseline_league_config = self.baseline_config_path / 'league_config.json'
        if baseline_league_config.exists():
            # Filtered for the same reason as save_optimal_configs above: this
            # folder's docstring promises it "can serve as baseline for future
            # runs", so a verbatim copy would let an intermediate folder carry
            # week-owned keys into a later `--promote`. propagate_to_configs
            # would reject them, but a folder that is documented as promotable
            # should not be born inflated in the first place.
            with open(baseline_league_config, 'r') as f:
                baseline_config = json.load(f)
            atomic_write_json(
                extract_base_params(baseline_config),
                intermediate_folder / 'league_config.json',
            )

        file_mapping = {
            'week_1_5': 'week1-5.json',
            'week_6_9': 'week6-9.json',
            'week_10_13': 'week10-13.json',
            'week_14_17': 'week14-17.json',
        }

        for week_key, perf in self.best_configs.items():
            if perf:
                synced_config = self._sync_schedule_params(perf.config_dict)

                week_params_dict = {
                    key: synced_config.get('parameters', synced_config).get(key)
                    for key in WEEK_SPECIFIC_PARAMS
                    if key in synced_config.get('parameters', synced_config)
                }

                standard_filename = file_mapping.get(week_key)
                if standard_filename:
                    perf_metrics = {
                        'mae': perf.mae,
                        'player_count': perf.player_count,
                        'config_value': perf.config_value,
                        'weeks_evaluated': perf.weeks_evaluated,
                        'weeks_requested': perf.weeks_requested
                    }
                    if perf.overall_metrics:
                        perf_metrics['ranking_metrics'] = {
                            'pairwise_accuracy': perf.overall_metrics.pairwise_accuracy,
                            'top_5_accuracy': perf.overall_metrics.top_5_accuracy,
                            'top_10_accuracy': perf.overall_metrics.top_10_accuracy,
                            'top_20_accuracy': perf.overall_metrics.top_20_accuracy,
                            'spearman_correlation': perf.overall_metrics.spearman_correlation
                        }
                        if perf.by_position:
                            perf_metrics['ranking_metrics']['by_position'] = {
                                pos: {
                                    'pairwise_accuracy': metrics.pairwise_accuracy,
                                    'top_5_accuracy': metrics.top_5_accuracy,
                                    'top_10_accuracy': metrics.top_10_accuracy,
                                    'top_20_accuracy': metrics.top_20_accuracy,
                                    'spearman_correlation': metrics.spearman_correlation
                                }
                                for pos, metrics in perf.by_position.items()
                            }

                    config_output = {
                        'config_name': f"Accuracy Intermediate {standard_filename.replace('.json', '')} ({timestamp})",
                        'description': f"Intermediate result after optimizing {param_name}",
                        'parameters': week_params_dict,
                        'performance_metrics': perf_metrics
                    }
                    with open(intermediate_folder / standard_filename, 'w') as f:
                        json.dump(config_output, f, indent=2)

        for week_key, standard_filename in file_mapping.items():
            if not self.best_configs.get(week_key):
                baseline_file = self.baseline_config_path / standard_filename
                if baseline_file.exists():
                    with open(baseline_file, 'r') as f:
                        baseline_data = json.load(f)

                    baseline_params = baseline_data.get('parameters', {})

                    config_output = {
                        'config_name': f"Accuracy Intermediate {standard_filename.replace('.json', '')} ({timestamp})",
                        'description': f"From baseline (no optimization yet)",
                        'parameters': baseline_params,
                        'performance_metrics': {
                            'mae': None,
                            'player_count': None,
                            'total_error': None,
                            'config_value': None,
                            'timestamp': timestamp,
                            'note': 'No optimization performed - using baseline parameters'
                        }
                    }

                    config_path = intermediate_folder / standard_filename
                    with open(config_path, 'w') as f:
                        json.dump(config_output, f, indent=2)

        metadata = {
            "param_idx": param_idx,
            "param_name": param_name,
            "horizons_evaluated": list(self.best_configs.keys()),
            "best_mae_per_horizon": {},
            "timestamp": datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        }

        for week_key, best_perf in self.best_configs.items():
            if best_perf:
                horizon_data = {
                    "mae": best_perf.mae,
                    "test_idx": best_perf.test_idx if best_perf.test_idx is not None else -1
                }
                if best_perf.overall_metrics:
                    horizon_data["ranking_metrics"] = {
                        "pairwise_accuracy": best_perf.overall_metrics.pairwise_accuracy,
                        "top_5_accuracy": best_perf.overall_metrics.top_5_accuracy,
                        "top_10_accuracy": best_perf.overall_metrics.top_10_accuracy,
                        "top_20_accuracy": best_perf.overall_metrics.top_20_accuracy,
                        "spearman_correlation": best_perf.overall_metrics.spearman_correlation
                    }
                metadata["best_mae_per_horizon"][week_key] = horizon_data
            else:
                metadata["best_mae_per_horizon"][week_key] = {
                    "mae": None,
                    "test_idx": -1
                }

        metadata_path = intermediate_folder / "metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

        self.logger.info(f"Saved metadata to {metadata_path.name}")
        self.logger.info(f"Saved intermediate results to: {intermediate_folder}")
        # T69/D5: record the ascent state INSIDE the folder it describes, so the resume
        # record stays a single artifact -- same glob, same cleanup, no parallel state file
        # elsewhere. Absent in a pre-T69 folder, which _detect_resume_state treats as
        # "pass 0, nothing frozen" rather than raising.
        atomic_write_json(
            {
                'pass_idx': pass_idx,
                'frozen_horizons': sorted(frozen_horizons or set()),
                'param_idx': param_idx,
                'param_name': param_name,
            },
            intermediate_folder / '_ascent_state.json'
        )

        return intermediate_folder

    def load_intermediate_results(self, folder_path: Path) -> bool:
        """
        Load intermediate results to resume optimization.

        Fully reconstructs each optimized horizon's AccuracyConfigPerformance into
        self.best_configs from the metrics the intermediate folder already persists
        (no re-evaluation), so a resumed run's best_configs matches a cold run's state
        at the same resume point. Horizons saved baseline-only
        (performance_metrics.mae is None) remain None, matching cold-run state.

        The merged per-horizon config_dict comes from
        ConfigGenerator.load_baseline_from_folder (league_config.json + the horizon's
        week file), which requires the folder's full 5-file set.

        Args:
            folder_path: Path to intermediate folder

        Returns:
            bool: True if at least one horizon was reconstructed
        """
        if not folder_path.exists():
            self.logger.warning(f"Intermediate folder not found: {folder_path}")
            return False

        file_mapping = {
            'week_1_5': 'week1-5.json',
            'week_6_9': 'week6-9.json',
            'week_10_13': 'week10-13.json',
            'week_14_17': 'week14-17.json',
        }
        horizon_mapping = {
            'week_1_5': '1-5',
            'week_6_9': '6-9',
            'week_10_13': '10-13',
            'week_14_17': '14-17',
        }

        try:
            merged_configs = ConfigGenerator.load_baseline_from_folder(folder_path)
        except (ValueError, FileNotFoundError) as e:
            self.logger.warning(
                f"Cannot reconstruct best_configs from incomplete intermediate folder "
                f"{folder_path}: {e}"
            )
            return False

        metadata = {}
        metadata_path = folder_path / 'metadata.json'
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
        best_mae_per_horizon = metadata.get('best_mae_per_horizon', {})

        loaded_count = 0
        for week_key in self.best_configs.keys():
            standard_filename = file_mapping.get(week_key)
            if not standard_filename:
                continue

            config_path = folder_path / standard_filename
            if not config_path.exists():
                continue

            with open(config_path, 'r') as f:
                data = json.load(f)

            metrics = data.get('performance_metrics', {})
            mae = metrics.get('mae')
            if mae is None:
                self.logger.debug(f"Skipped {standard_filename} - baseline-only horizon (mae is None)")
                continue

            ranking_metrics = metrics.get('ranking_metrics', {})
            overall_metrics = None
            if ranking_metrics:
                overall_metrics = RankingMetrics(
                    pairwise_accuracy=ranking_metrics.get('pairwise_accuracy'),
                    top_5_accuracy=ranking_metrics.get('top_5_accuracy'),
                    top_10_accuracy=ranking_metrics.get('top_10_accuracy'),
                    top_20_accuracy=ranking_metrics.get('top_20_accuracy'),
                    spearman_correlation=ranking_metrics.get('spearman_correlation')
                )

            by_position = {}
            for pos, pos_metrics in ranking_metrics.get('by_position', {}).items():
                by_position[pos] = RankingMetrics(
                    pairwise_accuracy=pos_metrics.get('pairwise_accuracy'),
                    top_5_accuracy=pos_metrics.get('top_5_accuracy'),
                    top_10_accuracy=pos_metrics.get('top_10_accuracy'),
                    top_20_accuracy=pos_metrics.get('top_20_accuracy'),
                    spearman_correlation=pos_metrics.get('spearman_correlation')
                )

            player_count = metrics.get('player_count')
            config_value = metrics.get('config_value')
            total_error = mae * player_count if player_count is not None else None
            test_idx = best_mae_per_horizon.get(week_key, {}).get('test_idx')
            weeks_evaluated = metrics.get('weeks_evaluated', 0)
            weeks_requested = metrics.get('weeks_requested', 0)

            horizon_key = horizon_mapping[week_key]
            config_dict = merged_configs[horizon_key]

            self.best_configs[week_key] = AccuracyConfigPerformance(
                config_dict=config_dict,
                mae=mae,
                player_count=player_count,
                total_error=total_error,
                config_value=config_value,
                overall_metrics=overall_metrics,
                by_position=by_position,
                test_idx=test_idx,
                weeks_evaluated=weeks_evaluated,
                weeks_requested=weeks_requested,
                # T69/D3: .get() -- absent in a pre-T69 artifact; the gate degrades.
                per_season_pairwise=metrics.get('per_season_pairwise', {})
            )
            loaded_count += 1
            self.logger.debug(
                f"Reconstructed best_config for {week_key} from {standard_filename} "
                f"(mae={mae}, player_count={player_count})"
            )

        self.logger.info(f"Loaded {loaded_count} intermediate configs from {folder_path}")
        return loaded_count > 0

    def get_summary(self) -> str:
        """Get a summary of current best configurations."""
        lines = ["Accuracy Simulation Results:"]
        lines.append("-" * 40)

        for week_key, perf in self.best_configs.items():
            if perf and perf.overall_metrics:
                lines.append(
                    f"  {week_key}: Pairwise={format_metric_pct(perf.overall_metrics.pairwise_accuracy)}"
                    f" | Top-10={format_metric_pct(perf.overall_metrics.top_10_accuracy)}"
                    f" | Spearman={format_metric_corr(perf.overall_metrics.spearman_correlation)}"
                    f" | MAE={perf.mae:.4f} (diag) ({perf.player_count} players)"
                )
            elif perf:
                lines.append(f"  {week_key}: MAE={perf.mae:.4f} ({perf.player_count} players)")
            else:
                lines.append(f"  {week_key}: No results yet")

        lines.append("-" * 40)
        lines.append(f"Total configs tested: {len(self.all_results)}")

        return "\n".join(lines)


def propagate_to_configs(
    optimal_folder: Path,
    target_folder: Path,
    logger: Logger
) -> None:
    """
    Copy optimal accuracy configs to target folder, preserving user-maintained fields.

    Copies all 5 standard config files from optimal_folder to target_folder.
    For league_config.json the source 'parameters' block is FIRST filtered to
    BASE_CONFIG_PARAMS (simulation.shared.config_filters.extract_base_params), so
    week-file-owned keys in any source folder can never ride into the live base
    config (T90). Only the filtered 'parameters' is taken, so the source's own
    config_name/description survive. THEN CURRENT_NFL_WEEK, NFL_SEASON,
    MAX_POSITIONS, FLEX_ELIGIBLE_POSITIONS, INJURY_PENALTIES, OPPONENT_TEAMS are
    preserved from the existing target file (if present), so live-only
    user-maintained keys are never dropped by the atomic replace. The live
    ADP_SCORING.THRESHOLDS sub-block is preserved as well (D4.1) whenever the
    source folder's filtered parameters carries an ADP_SCORING block to graft
    onto, so an accuracy promote can no longer overwrite the hand-owned threshold
    ladder, while the sibling ADP_SCORING.WEIGHT continues to promote from the
    source.
    For weekly config files: copies as-is (MATCHUP->SCHEDULE sync already applied
    by save_optimal_configs() at write time). The simulation-only 'performance_metrics'
    block is stripped from all written files before writing.

    All five payloads are built in memory (Phase 1: read + preserve-merge + strip)
    BEFORE any target write (Phase 2: atomic tmp->rename each). So a malformed source
    file (files 2-5) or a write/permission/ENOSPC error (files 2-5) raises with
    data/configs/ left entirely untouched (no partial promotion). Each Phase-2 write
    is atomic, so no target is ever observed truncated and no .tmp residue survives.
    Residual: a mid-rename I/O failure BETWEEN two of the five Phase-2 writes can
    still leave a mixed set (set-level five-file transactionality is out of scope).

    Args:
        optimal_folder (Path): Path to accuracy_optimal_* folder with source configs.
        target_folder (Path): Destination folder (e.g., Path("data/configs")).
        logger (Logger): Logger instance from the calling context.
    """
    CONFIG_FILES = [
        'league_config.json',
        'week1-5.json',
        'week6-9.json',
        'week10-13.json',
        'week14-17.json',
    ]
    PRESERVE_KEYS = [
        'CURRENT_NFL_WEEK',
        'NFL_SEASON',
        'MAX_POSITIONS',
        'FLEX_ELIGIBLE_POSITIONS',
        'INJURY_PENALTIES',
        # T90 D2: OPPONENT_TEAMS is a BASE_CONFIG_PARAMS member that lives only in
        # the live file (no source folder carries it), so without preservation every
        # promote DELETES it. No subtractive filter can fix that direction.
        'OPPONENT_TEAMS',
    ]
    # D4.1: nested counterpart of PRESERVE_KEYS. Each entry is a
    # (section, subkey) path under 'parameters' whose LIVE value survives a
    # promote, provided the promoted payload already carries the parent section
    # (graft-onto-existing; a source lacking the section drops the block
    # wholesale, exactly as today). ADP_SCORING.THRESHOLDS is the hand-owned
    # threshold ladder that no sweep tunes; the sibling ADP_SCORING.WEIGHT is
    # deliberately absent so the simulate -> promote -> use-live loop stays
    # intact for it.
    # NOTE (TD6): "no sweep tunes it" is true only while the ADP_SCORING_STEPS
    # sweep dial writes the sibling ADP_SCORING.STEPS rather than
    # THRESHOLDS.STEPS (ConfigGenerator._apply_param_value). If that mis-nesting
    # is ever corrected, revisit this entry — it would begin suppressing a value
    # the sweep legitimately tunes.
    PRESERVE_SUBPATHS = [
        ('ADP_SCORING', 'THRESHOLDS'),
    ]

    target_folder.mkdir(parents=True, exist_ok=True)

    # ---- Phase 1: validate + build all payloads (NO writes) ----
    # A missing source is warned + skipped (contributes no payload); a malformed
    # source, or the league_config.json preserve-merge target read, raises here —
    # before any write — so data/configs/ is left entirely untouched on failure.
    built = []  # list of (config_file, target_path, updated_config)
    for config_file in CONFIG_FILES:
        optimal_path = optimal_folder / config_file
        target_path = target_folder / config_file

        if not optimal_path.exists():
            logger.warning(f"Optimal config not found: {optimal_path}")
            continue

        with open(optimal_path, 'r') as f:
            optimal_config = json.load(f)

        if config_file == 'league_config.json':
            # Ownership filter (T90 D1): week-file-owned keys present in an
            # arbitrary --promote <folder> source must never ride into the live
            # base config. Only the filtered 'parameters' block is taken and it is
            # spread over the source dict, so the source's own config_name /
            # description survive and the performance_metrics strip below is
            # unchanged. (save_optimal_configs consumes the SAME helper but writes
            # its whole return value — the two call sites differ deliberately.)
            optimal_config = {
                **optimal_config,
                'parameters': extract_base_params(optimal_config)['parameters'],
            }

        if config_file == 'league_config.json' and target_path.exists():
            with open(target_path, 'r') as f:
                original_config = json.load(f)
            updated_config = optimal_config.copy()
            if 'parameters' not in updated_config:
                updated_config['parameters'] = {}
            for key in PRESERVE_KEYS:
                if 'parameters' in original_config and key in original_config['parameters']:
                    updated_config['parameters'][key] = original_config['parameters'][key]
            for section, subkey in PRESERVE_SUBPATHS:
                live_section = original_config.get('parameters', {}).get(section)
                payload_section = updated_config['parameters'].get(section)
                if not isinstance(live_section, dict) or subkey not in live_section:
                    continue
                if not isinstance(payload_section, dict):
                    continue
                if payload_section.get(subkey) != live_section[subkey]:
                    logger.warning(
                        f"propagate_to_configs: retaining live {section}.{subkey} "
                        f"for {target_path}; suppressing promoted value "
                        f"{payload_section.get(subkey)} in favor of live value "
                        f"{live_section[subkey]}"
                    )
                payload_section[subkey] = live_section[subkey]
        else:
            updated_config = optimal_config

        updated_config.pop('performance_metrics', None)

        built.append((config_file, target_path, updated_config))

    # ---- Phase 2: write each built payload atomically (tmp -> rename) ----
    copied_count = 0
    for config_file, target_path, updated_config in built:
        atomic_write_json(
            updated_config,
            target_path,
            error_message=f"Failed to write config to {target_path}",
        )
        logger.info(f"Copied {config_file} → {target_folder}/{config_file}")
        copied_count += 1

    logger.info(f"Promoted {copied_count} files to {target_folder}")
