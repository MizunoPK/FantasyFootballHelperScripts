"""
Accuracy Results Manager

Manages results storage and best configuration tracking for accuracy simulation.
Similar to shared/ResultsManager but optimized for MAE-based comparisons
where lower is better (opposite of win-rate).

Key differences from win-rate ResultsManager:
- Lower MAE is better (not higher win-rate)
- Metrics include mae, player_count instead of win_rate, total_wins
- Output folder naming: accuracy_optimal_TIMESTAMP/

Author: Kai Mizuno
"""

import copy
import json
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.LoggingManager import get_logger

# Import cleanup utilities
sys.path.append(str(Path(__file__).parent.parent / "shared"))
from config_cleanup import cleanup_old_accuracy_optimal_folders

# Import from same folder
sys.path.append(str(Path(__file__).parent))
from AccuracyCalculator import AccuracyResult


@dataclass
class RankingMetrics:
    """
    Ranking-based accuracy metrics for a configuration.

    Attributes:
        pairwise_accuracy (float): % of pairwise comparisons correct (0.0-1.0)
        top_5_accuracy (float): % overlap in top-5 predictions (0.0-1.0)
        top_10_accuracy (float): % overlap in top-10 predictions (0.0-1.0)
        top_20_accuracy (float): % overlap in top-20 predictions (0.0-1.0)
        spearman_correlation (float): Rank correlation coefficient (-1.0 to +1.0)
    """
    pairwise_accuracy: float
    top_5_accuracy: float
    top_10_accuracy: float
    top_20_accuracy: float
    spearman_correlation: float


# Week ranges matching win-rate simulation
WEEK_RANGES = {
    'week_1_5': (1, 5),
    'week_6_9': (6, 9),
    'week_10_13': (10, 13),
    'week_14_17': (14, 17),
}


class AccuracyConfigPerformance:
    """
    Performance record for a configuration in accuracy simulation.

    Attributes:
        config_dict (dict): The configuration that was tested
        mae (float): Mean Absolute Error (lower is better)
        player_count (int): Number of players evaluated
        total_error (float): Sum of all absolute errors
        config_id (str): Hash identifier for this config
        timestamp (str): When the test was run
        param_name (Optional[str]): Parameter being optimized (tournament mode)
        test_idx (Optional[int]): Test value index (tournament mode)
        base_horizon (Optional[str]): Horizon this config originated from (tournament mode)
    """

    def __init__(
        self,
        config_dict: dict,
        mae: float,
        player_count: int,
        total_error: float,
        config_id: Optional[str] = None,
        timestamp: Optional[str] = None,
        param_name: Optional[str] = None,
        test_idx: Optional[int] = None,
        base_horizon: Optional[str] = None,
        overall_metrics: Optional[RankingMetrics] = None,
        by_position: Optional[Dict[str, RankingMetrics]] = None
    ) -> None:
        self.config_dict = copy.deepcopy(config_dict)
        self.mae = mae
        self.player_count = player_count
        self.total_error = total_error
        self.config_id = config_id or self._generate_id(config_dict)
        self.timestamp = timestamp or datetime.now().isoformat()
        # Tournament mode metadata (optional)
        self.param_name = param_name
        self.test_idx = test_idx
        self.base_horizon = base_horizon
        # Ranking metrics (optional - for new ranking-based optimization)
        self.overall_metrics = overall_metrics
        self.by_position = by_position or {}

    def _generate_id(self, config: dict) -> str:
        """Generate a hash-based ID for the configuration."""
        import hashlib
        config_str = json.dumps(config, sort_keys=True)
        return hashlib.md5(config_str.encode()).hexdigest()[:8]

    def is_better_than(self, other: 'AccuracyConfigPerformance') -> bool:
        """
        Check if this configuration is better than another.

        Uses pairwise_accuracy as primary metric when available.
        Falls back to MAE for backward compatibility.

        Args:
            other: Configuration to compare against

        Returns:
            bool: True if this config is better, False otherwise.
                  Always returns False if either config has player_count=0.
        """
        # Reject invalid configs FIRST (before checking if other is None)
        # This prevents invalid configs from becoming "best" when no previous best exists
        if self.player_count == 0:
            return False

        if other is None:
            return True

        # Don't replace valid config with invalid one
        if other.player_count == 0:
            return False

        # Use ranking metrics if available (Q12: pairwise_accuracy is primary)
        if self.overall_metrics and other.overall_metrics:
            return self.overall_metrics.pairwise_accuracy > other.overall_metrics.pairwise_accuracy

        # Fallback to MAE for backward compatibility (Q25)
        return self.mae < other.mae

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        result = {
            'config_id': self.config_id,
            'mae': self.mae,
            'player_count': self.player_count,
            'total_error': self.total_error,
            'timestamp': self.timestamp,
            'config': self.config_dict
        }

        # Add ranking metrics if available
        if self.overall_metrics:
            result['pairwise_accuracy'] = self.overall_metrics.pairwise_accuracy
            result['top_5_accuracy'] = self.overall_metrics.top_5_accuracy
            result['top_10_accuracy'] = self.overall_metrics.top_10_accuracy
            result['top_20_accuracy'] = self.overall_metrics.top_20_accuracy
            result['spearman_correlation'] = self.overall_metrics.spearman_correlation

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
        # Calculate total_error if not provided (when loading from standard config files)
        total_error = data.get('total_error', mae * player_count)

        # Load ranking metrics if available (Q25: backward compatibility)
        overall_metrics = None
        if 'pairwise_accuracy' in data:
            overall_metrics = RankingMetrics(
                pairwise_accuracy=data['pairwise_accuracy'],
                top_5_accuracy=data['top_5_accuracy'],
                top_10_accuracy=data['top_10_accuracy'],
                top_20_accuracy=data['top_20_accuracy'],
                spearman_correlation=data['spearman_correlation']
            )

        # Load per-position metrics if available
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
            config_id=data.get('config_id'),
            timestamp=data.get('timestamp'),
            overall_metrics=overall_metrics,
            by_position=by_position
        )

    def __repr__(self) -> str:
        return f"AccuracyConfigPerformance(mae={self.mae:.4f}, players={self.player_count})"


class AccuracyResultsManager:
    """
    Manages accuracy simulation results storage and tracking.

    Tracks best configurations per week range and saves results to disk.
    Uses "lower is better" comparison (opposite of win-rate).

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

        # Track best config per week range (4 weekly ranges)
        self.best_configs: Dict[str, AccuracyConfigPerformance] = {
            'week_1_5': None,
            'week_6_9': None,
            'week_10_13': None,
            'week_14_17': None,
        }

        # All tested configurations
        self.all_results: List[AccuracyConfigPerformance] = []

        self.logger.info(f"AccuracyResultsManager initialized: {output_dir}")

    def add_result(
        self,
        week_range_key: str,
        config_dict: dict,
        accuracy_result: AccuracyResult,
        param_name: Optional[str] = None,
        test_idx: Optional[int] = None,
        base_horizon: Optional[str] = None
    ) -> bool:
        """
        Add a configuration result and check if it's the new best.

        Args:
            week_range_key: 'ros', 'week_1_5', 'week_6_9', etc.
            config_dict: The configuration that was tested
            accuracy_result: AccuracyResult from AccuracyCalculator
            param_name: Parameter being optimized (tournament mode)
            test_idx: Test value index (tournament mode)
            base_horizon: Horizon this config originated from (tournament mode)

        Returns:
            bool: True if this is the new best for the week range
        """
        # Deep copy to prevent shared object references (defense in depth)
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
            by_position=accuracy_result.by_position
        )

        self.all_results.append(perf)
        self.logger.debug(f"add_result({week_range_key}): MAE={perf.mae:.4f}, players={perf.player_count}")

        # Check if better than current best
        current_best = self.best_configs.get(week_range_key)
        if perf.is_better_than(current_best):
            previous_mae = f"{current_best.mae:.4f}" if current_best else "N/A"
            self.best_configs[week_range_key] = perf

            # Log with ranking metrics prominently (Q30)
            if perf.overall_metrics:
                self.logger.info(
                    f"New best for {week_range_key}: "
                    f"Pairwise={perf.overall_metrics.pairwise_accuracy:.1%} | "
                    f"Top-10={perf.overall_metrics.top_10_accuracy:.1%} | "
                    f"Spearman={perf.overall_metrics.spearman_correlation:.3f} | "
                    f"MAE={perf.mae:.4f} (diag) | "
                    f"(prev MAE: {previous_mae})"
                )
            else:
                # Fallback for backward compatibility (no ranking metrics)
                self.logger.info(
                    f"New best for {week_range_key}: MAE={perf.mae:.4f} "
                    f"(previous: {previous_mae})"
                )
            return True

        return False

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

        # Handle nested structure: MATCHUP_SCORING -> SCHEDULE_SCORING
        if 'MATCHUP_SCORING' in synced:
            matchup = synced['MATCHUP_SCORING']
            schedule = synced.get('SCHEDULE_SCORING', {})

            # Copy relevant fields from MATCHUP to SCHEDULE
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
            ├── league_config.json      # Copied from baseline (strategy params)
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
                        f"Pairwise={perf.overall_metrics.pairwise_accuracy:.1%} | "
                        f"Top-10={perf.overall_metrics.top_10_accuracy:.1%} | "
                        f"Spearman={perf.overall_metrics.spearman_correlation:.3f} | "
                        f"MAE={perf.mae:.4f} (diag) | "
                        f"players={perf.player_count} | id={perf.config_id}"
                    )
                else:
                    # Fallback for backward compatibility
                    self.logger.info(f"  {week_key}: MAE={perf.mae:.4f}, players={perf.player_count}, id={perf.config_id}")
            else:
                self.logger.info(f"  {week_key}: None")

        # Clean up old optimal folders if we're at the limit
        cleanup_old_accuracy_optimal_folders(self.output_dir)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        optimal_folder = self.output_dir / f"accuracy_optimal_{timestamp}"
        optimal_folder.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Creating optimal folder: {optimal_folder.name}")

        # Copy league_config.json from baseline (unchanged - contains strategy params)
        baseline_league_config = self.baseline_config_path / 'league_config.json'
        if baseline_league_config.exists():
            shutil.copy(baseline_league_config, optimal_folder / 'league_config.json')
            self.logger.info("Copied league_config.json from baseline")
        else:
            self.logger.warning(f"No league_config.json found in baseline: {self.baseline_config_path}")

        # Map week range keys to output filenames and descriptions
        file_mapping = {
            'week_1_5': ('week1-5.json', 'Weeks 1-5 prediction parameters'),
            'week_6_9': ('week6-9.json', 'Weeks 6-9 prediction parameters'),
            'week_10_13': ('week10-13.json', 'Weeks 10-13 prediction parameters'),
            'week_14_17': ('week14-17.json', 'Weeks 14-17 prediction parameters'),
        }

        # Save each optimal config with proper structure
        for week_key, (filename, description) in file_mapping.items():
            perf = self.best_configs.get(week_key)
            self.logger.info(f"Processing {week_key} -> {filename}")
            if perf:
                self.logger.info(f"  Has results: MAE={perf.mae:.4f}, using real performance data")
                # Sync SCHEDULE params with MATCHUP before saving
                synced_config = self._sync_schedule_params(perf.config_dict)

                # Extract only week-specific parameters (not base/strategy params)
                # Use ResultsManager's helper to filter to WEEK_SPECIFIC_PARAMS
                from simulation.shared.ResultsManager import ResultsManager
                week_params_dict = {
                    key: synced_config.get('parameters', synced_config).get(key)
                    for key in ResultsManager.WEEK_SPECIFIC_PARAMS
                    if key in synced_config.get('parameters', synced_config)
                }

                # Create config with proper nested structure (matches win-rate format)
                config_output = {
                    'config_name': f"Accuracy Optimal {filename.replace('.json', '')} ({timestamp})",
                    'description': description,
                    'parameters': week_params_dict,
                    'performance_metrics': {
                        'mae': perf.mae,
                        'player_count': perf.player_count,
                        'total_error': perf.total_error,
                        'config_id': perf.config_id,
                        'timestamp': perf.timestamp
                    }
                }

                config_path = optimal_folder / filename
                with open(config_path, 'w') as f:
                    json.dump(config_output, f, indent=2)

                self.logger.info(f"  Saved {filename}: MAE={perf.mae:.4f}")
            else:
                self.logger.info(f"  No results - loading params from baseline")
                # No results for this week range - load params from baseline
                # but create proper accuracy format (don't copy win-rate metrics)
                baseline_file = self.baseline_config_path / filename
                if baseline_file.exists():
                    self.logger.info(f"  Baseline file exists: {baseline_file}")
                    with open(baseline_file, 'r') as f:
                        baseline_data = json.load(f)

                    # Extract only parameters from baseline
                    baseline_params = baseline_data.get('parameters', {})

                    # Create config with accuracy format (no performance data available)
                    config_output = {
                        'config_name': f"Accuracy Optimal {filename.replace('.json', '')} ({timestamp})",
                        'description': description,
                        'parameters': baseline_params,
                        'performance_metrics': {
                            'mae': None,
                            'player_count': None,
                            'total_error': None,
                            'config_id': 'baseline',
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

        self.logger.info(f"Saved optimal configs to: {optimal_folder}")
        self.logger.info("=" * 60)
        return optimal_folder

    def save_intermediate_results(
        self,
        param_idx: int,
        param_name: str,
        week_range_prefix: str = ''
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

        # Copy league_config.json from baseline
        baseline_league_config = self.baseline_config_path / 'league_config.json'
        if baseline_league_config.exists():
            shutil.copy(baseline_league_config, intermediate_folder / 'league_config.json')

        # Map week range keys to standard config filenames
        file_mapping = {
            'week_1_5': 'week1-5.json',
            'week_6_9': 'week6-9.json',
            'week_10_13': 'week10-13.json',
            'week_14_17': 'week14-17.json',
        }

        # Save standard config files only (spec says 5-JSON structure, no extra tracking files)
        for week_key, perf in self.best_configs.items():
            if perf:
                # Sync SCHEDULE params before saving
                synced_config = self._sync_schedule_params(perf.config_dict)

                # Extract only week-specific parameters (not base/strategy params)
                # Use ResultsManager's helper to filter to WEEK_SPECIFIC_PARAMS
                from simulation.shared.ResultsManager import ResultsManager
                week_params_dict = {
                    key: synced_config.get('parameters', synced_config).get(key)
                    for key in ResultsManager.WEEK_SPECIFIC_PARAMS
                    if key in synced_config.get('parameters', synced_config)
                }

                # Save standard config file (for use as baseline and resume)
                standard_filename = file_mapping.get(week_key)
                if standard_filename:
                    config_output = {
                        'config_name': f"Accuracy Intermediate {standard_filename.replace('.json', '')} ({timestamp})",
                        'description': f"Intermediate result after optimizing {param_name}",
                        'parameters': week_params_dict,
                        'performance_metrics': {
                            'mae': perf.mae,
                            'player_count': perf.player_count,
                            'config_id': perf.config_id
                        }
                    }
                    with open(intermediate_folder / standard_filename, 'w') as f:
                        json.dump(config_output, f, indent=2)

        # For any week ranges without results yet, load params from baseline
        # but create proper accuracy format (don't copy win-rate metrics)
        for week_key, standard_filename in file_mapping.items():
            if not self.best_configs.get(week_key):
                baseline_file = self.baseline_config_path / standard_filename
                if baseline_file.exists():
                    with open(baseline_file, 'r') as f:
                        baseline_data = json.load(f)

                    # Extract only parameters from baseline
                    baseline_params = baseline_data.get('parameters', {})

                    # Create config with accuracy format (no performance data available)
                    config_output = {
                        'config_name': f"Accuracy Intermediate {standard_filename.replace('.json', '')} ({timestamp})",
                        'description': f"From baseline (no optimization yet)",
                        'parameters': baseline_params,
                        'performance_metrics': {
                            'mae': None,
                            'player_count': None,
                            'total_error': None,
                            'config_id': 'baseline',
                            'timestamp': timestamp,
                            'note': 'No optimization performed - using baseline parameters'
                        }
                    }

                    config_path = intermediate_folder / standard_filename
                    with open(config_path, 'w') as f:
                        json.dump(config_output, f, indent=2)

        # Create metadata.json for tournament mode tracking
        metadata = {
            "param_idx": param_idx,
            "param_name": param_name,
            "horizons_evaluated": list(self.best_configs.keys()),
            "best_mae_per_horizon": {},
            "timestamp": datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        }

        for week_key, best_perf in self.best_configs.items():
            if best_perf:
                metadata["best_mae_per_horizon"][week_key] = {
                    "mae": best_perf.mae,
                    "test_idx": best_perf.test_idx if best_perf.test_idx is not None else -1
                }
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
        return intermediate_folder

    def load_intermediate_results(self, folder_path: Path) -> bool:
        """
        Load intermediate results to resume optimization.

        Loads from standard config files (week1-5.json, week6-9.json, etc.)
        which contain performance_metrics for resume capability.

        Args:
            folder_path: Path to intermediate folder

        Returns:
            bool: True if results were loaded successfully
        """
        if not folder_path.exists():
            self.logger.warning(f"Intermediate folder not found: {folder_path}")
            return False

        # Map week keys to standard config filenames
        file_mapping = {
            'week_1_5': 'week1-5.json',
            'week_6_9': 'week6-9.json',
            'week_10_13': 'week10-13.json',
            'week_14_17': 'week14-17.json',
        }

        loaded_count = 0
        for week_key in self.best_configs.keys():
            standard_filename = file_mapping.get(week_key)
            if not standard_filename:
                continue

            config_path = folder_path / standard_filename
            if config_path.exists():
                with open(config_path, 'r') as f:
                    data = json.load(f)

                # Extract performance metrics and config from standard format
                if 'performance_metrics' in data and 'parameters' in data:
                    metrics = data['performance_metrics']

                    # Only load if this is an accuracy config (has 'mae' field)
                    # Skip win-rate configs which have 'win_rate' instead
                    if 'mae' in metrics and metrics['mae'] is not None:
                        perf_data = {
                            'mae': metrics['mae'],
                            'player_count': metrics['player_count'],
                            'config_id': metrics.get('config_id', ''),
                            'config': data['parameters']
                        }
                        self.best_configs[week_key] = AccuracyConfigPerformance.from_dict(perf_data)
                        loaded_count += 1
                    else:
                        self.logger.debug(f"Skipped {standard_filename} - not accuracy format (missing mae field)")

        self.logger.info(f"Loaded {loaded_count} intermediate configs from {folder_path}")
        return loaded_count > 0

    def get_summary(self) -> str:
        """Get a summary of current best configurations."""
        lines = ["Accuracy Simulation Results:"]
        lines.append("-" * 40)

        for week_key, perf in self.best_configs.items():
            if perf:
                lines.append(f"  {week_key}: MAE={perf.mae:.4f} ({perf.player_count} players)")
            else:
                lines.append(f"  {week_key}: No results yet")

        lines.append("-" * 40)
        lines.append(f"Total configs tested: {len(self.all_results)}")

        return "\n".join(lines)
