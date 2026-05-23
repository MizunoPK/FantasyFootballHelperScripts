"""
Run Accuracy Simulation

CLI tool for running accuracy simulation to find optimal scoring algorithm
parameters. Evaluates prediction accuracy using MAE (Mean Absolute Error).

Uses tournament optimization where each parameter is optimized across ALL 4
weekly horizons (week1-5, week6-9, week10-13, week14-17) before moving
to the next parameter.

Usage:
    python run_accuracy_simulation.py [options]

Examples:
    # Run with default settings
    python run_accuracy_simulation.py

    # Run with custom baseline config
    python run_accuracy_simulation.py --baseline path/to/config

    # Run with more test values per parameter
    python run_accuracy_simulation.py --test-values 7

Author: Kai Mizuno
"""

import argparse
import json
import signal
import sys
from pathlib import Path
from typing import Dict, Optional

from simulation.accuracy.AccuracySimulationManager import AccuracySimulationManager
from simulation.accuracy.AccuracyResultsManager import propagate_to_configs
from utils.LoggingManager import setup_logger, get_logger


def signal_handler(sig, frame):
    """Handle Ctrl+C by immediately exiting."""
    print("\n\nCtrl+C detected - exiting immediately...")
    sys.exit(1)


signal.signal(signal.SIGINT, signal_handler)


DEFAULT_LOG_LEVEL = 'info'
LOGGING_TO_FILE = False
LOG_NAME = "accuracy_simulation"
LOGGING_FORMAT = "detailed"

DEFAULT_BASELINE = ''
DEFAULT_OUTPUT = 'simulation/simulation_configs'
DEFAULT_DATA = 'simulation/sim_data'
DEFAULT_TEST_VALUES = 3
NUM_PARAMETERS_TO_TEST = 1

DEFAULT_MAX_WORKERS = 8
DEFAULT_USE_PROCESSES = True


PARAMETER_ORDER = [
    'NORMALIZATION_MAX_SCALE',
    'TEAM_QUALITY_SCORING_WEIGHT',
    'TEAM_QUALITY_MIN_WEEKS',
    'PERFORMANCE_SCORING_WEIGHT',
    'PERFORMANCE_SCORING_STEPS',
    'PERFORMANCE_MIN_WEEKS',
    'MATCHUP_IMPACT_SCALE',
    'MATCHUP_SCORING_WEIGHT',
    'MATCHUP_MIN_WEEKS',
    'TEMPERATURE_IMPACT_SCALE',
    'TEMPERATURE_SCORING_WEIGHT',
    'WIND_IMPACT_SCALE',
    'WIND_SCORING_WEIGHT',
    'LOCATION_HOME',
    'LOCATION_AWAY',
    'LOCATION_INTERNATIONAL',
]


WEEK_FILENAMES = {
    'week_1_5': 'week1-5.json',
    'week_6_9': 'week6-9.json',
    'week_10_13': 'week10-13.json',
    'week_14_17': 'week14-17.json',
}


def load_folder_metrics(folder_path: Path) -> Dict[str, Optional[dict]]:
    """Load ranking metrics for all 4 horizons from a config folder.

    Args:
        folder_path: Path to a config folder (accuracy_optimal_* or accuracy_intermediate_*)

    Returns:
        Dict mapping horizon key to ranking metrics dict (or None if not present)

    Raises:
        SystemExit: If folder does not exist, required file missing, or JSON parse error
    """
    logger = get_logger()
    if not folder_path.exists():
        logger.error(f"Compare folder not found: {folder_path}")
        sys.exit(1)

    result = {}
    for horizon_key, filename in WEEK_FILENAMES.items():
        filepath = folder_path / filename
        if not filepath.exists():
            logger.error(f"Folder {folder_path} missing required file: {filename}")
            sys.exit(1)
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse {filepath}: {e}")
            sys.exit(1)
        perf = data.get('performance_metrics', {})
        ranking = perf.get('ranking_metrics')
        if ranking is None:
            logger.debug(f"No ranking_metrics in {filepath} — horizon {horizon_key} will show N/A")
            result[horizon_key] = None
        else:
            result[horizon_key] = ranking
    return result


def print_compare_table(folder_a: Path, folder_b: Path) -> None:
    """Print before/after accuracy comparison for two config folders to stdout.

    Args:
        folder_a: Path to baseline/before folder
        folder_b: Path to optimized/after folder
    """
    metrics_a = load_folder_metrics(folder_a)
    metrics_b = load_folder_metrics(folder_b)

    horizon_display = {
        'week_1_5': 'week_1_5',
        'week_6_9': 'week_6_9',
        'week_10_13': 'week_10_13',
        'week_14_17': 'week_14_17',
    }

    for horizon_key in WEEK_FILENAMES:
        print(f"{horizon_display[horizon_key]}:")
        rm_a = metrics_a[horizon_key]
        rm_b = metrics_b[horizon_key]

        if rm_a is None or rm_b is None:
            print(f"  Pairwise:  N/A")
            print(f"  Top-10:    N/A")
            print(f"  Spearman:  N/A")
            continue

        pairwise_a = rm_a.get('pairwise_accuracy')
        pairwise_b = rm_b.get('pairwise_accuracy')
        top10_a = rm_a.get('top_10_accuracy')
        top10_b = rm_b.get('top_10_accuracy')
        spearman_a = rm_a.get('spearman_correlation')
        spearman_b = rm_b.get('spearman_correlation')

        if pairwise_a is not None and pairwise_b is not None:
            delta = pairwise_b - pairwise_a
            print(f"  Pairwise:  {pairwise_a:.1%} → {pairwise_b:.1%}  ({delta:+.1%})")
        else:
            print(f"  Pairwise:  N/A")

        if top10_a is not None and top10_b is not None:
            delta = top10_b - top10_a
            print(f"  Top-10:    {top10_a:.1%} → {top10_b:.1%}  ({delta:+.1%})")
        else:
            print(f"  Top-10:    N/A")

        if spearman_a is not None and spearman_b is not None:
            delta = spearman_b - spearman_a
            print(f"  Spearman:  {spearman_a:.3f} → {spearman_b:.3f}  ({delta:+.3f})")
        else:
            print(f"  Spearman:  N/A")


def find_baseline_config() -> Path:
    """
    Find the most recent optimal config folder to use as baseline.

    Searches for accuracy_optimal_* folders first, then falls back to
    optimal_* folders from win-rate simulation.

    Returns:
        Path: Path to baseline config FOLDER (not file)

    Raises:
        FileNotFoundError: If no baseline config found
    """
    config_dir = Path("simulation/simulation_configs")

    if not config_dir.exists():
        raise FileNotFoundError(
            f"Config directory not found: {config_dir}. "
            "Please run win-rate simulation first or provide --baseline path."
        )

    required_files = ['league_config.json', 'week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']

    def is_valid_config_folder(folder: Path) -> bool:
        """Check if folder contains all required config files."""
        return all((folder / f).exists() for f in required_files)

    accuracy_folders = sorted([
        p for p in config_dir.iterdir()
        if p.is_dir() and p.name.startswith("accuracy_optimal_") and is_valid_config_folder(p)
    ], key=lambda p: p.stat().st_mtime, reverse=True)

    if accuracy_folders:
        return accuracy_folders[0]

    win_rate_folders = sorted([
        p for p in config_dir.iterdir()
        if p.is_dir() and p.name.startswith("optimal_") and not p.name.startswith("accuracy_") and is_valid_config_folder(p)
    ], key=lambda p: p.stat().st_mtime, reverse=True)

    if win_rate_folders:
        return win_rate_folders[0]

    raise FileNotFoundError(
        "No baseline config folder found. Please run win-rate simulation first "
        "or provide --baseline path to an existing config folder.\n"
        f"Expected folder with: {', '.join(required_files)}"
    )


def main() -> None:
    """Main entry point for accuracy simulation."""
    parser = argparse.ArgumentParser(
        description="Run accuracy simulation to find optimal scoring parameters using tournament optimization"
    )

    parser.add_argument(
        '--baseline',
        type=str,
        default=DEFAULT_BASELINE,
        help="Path to baseline config folder (default: most recent optimal config)"
    )

    parser.add_argument(
        '--output',
        type=str,
        default=DEFAULT_OUTPUT,
        help=f"Output directory for results (default: {DEFAULT_OUTPUT})"
    )

    parser.add_argument(
        '--data',
        type=str,
        default=DEFAULT_DATA,
        help=f"Path to sim_data folder (default: {DEFAULT_DATA})"
    )

    parser.add_argument(
        '--test-values',
        type=int,
        default=DEFAULT_TEST_VALUES,
        help=f"Number of test values per parameter (default: {DEFAULT_TEST_VALUES})"
    )

    parser.add_argument(
        '--num-params',
        type=int,
        default=NUM_PARAMETERS_TO_TEST,
        help=f"Number of parameters to test at once (default: {NUM_PARAMETERS_TO_TEST})"
    )

    parser.add_argument(
        '--max-workers',
        type=int,
        default=DEFAULT_MAX_WORKERS,
        help=f'Number of parallel workers for config evaluation (default: {DEFAULT_MAX_WORKERS})'
    )

    parser.add_argument(
        '--use-processes',
        dest='use_processes',
        action='store_true',
        default=DEFAULT_USE_PROCESSES,
        help='Use ProcessPoolExecutor for true parallelism (default, bypasses GIL)'
    )

    parser.add_argument(
        '--no-use-processes',
        dest='use_processes',
        action='store_false',
        help='Use ThreadPoolExecutor instead of processes (slower, for debugging)'
    )

    parser.add_argument(
        '--log-level',
        choices=['debug', 'info', 'warning', 'error'],
        default=DEFAULT_LOG_LEVEL,
        help=f'Logging level (default: {DEFAULT_LOG_LEVEL}). '
             'debug: all evaluations + parameter updates + worker activity. '
             'info: new bests + parameter completion + summaries. '
             'warning: warnings only. '
             'error: errors only.'
    )

    parser.add_argument(
        '--enable-log-file',
        action='store_true',
        default=False,
        help='Enable file logging to logs/accuracy_simulation/ folder (default: console only). '
             'Logs rotate at 500 lines, max 50 files per folder. '
             'Use with --log-level to control verbosity.'
    )

    parser.add_argument(
        '--promote',
        nargs='?',
        const=True,
        default=None,
        metavar='FOLDER',
        help='Promote optimal configs to data/configs/. Without FOLDER: promotes the '
             'just-produced optimal folder after sim run. With FOLDER: promotes the '
             'specified folder without running the sim (standalone mode).'
    )

    parser.add_argument(
        '--params',
        type=str,
        default=None,
        help="Comma-separated list of parameter names to optimize (default: all). "
             "Example: --params NORMALIZATION_MAX_SCALE,MATCHUP_SCORING_WEIGHT. "
             "Unknown parameter names exit with error."
    )

    parser.add_argument(
        '--compare',
        nargs=2,
        metavar=('FOLDER_A', 'FOLDER_B'),
        type=str,
        default=None,
        help="Print before/after accuracy comparison for two config folders "
             "(stdout only, no sim run). Example: --compare folder_a/ folder_b/"
    )

    args = parser.parse_args()

    setup_logger(LOG_NAME, args.log_level.upper(), args.enable_log_file, None, LOGGING_FORMAT)
    logger = get_logger()

    if args.params is not None and args.compare is not None:
        logger.error("--params and --compare cannot be combined in a single invocation")
        sys.exit(1)

    if args.compare is not None:
        folder_a = Path(args.compare[0])
        folder_b = Path(args.compare[1])
        print_compare_table(folder_a, folder_b)
        sys.exit(0)

    if isinstance(args.promote, str):
        promote_folder = Path(args.promote)
        if not promote_folder.exists():
            logger.error(f"Promote folder not found: {promote_folder}")
            sys.exit(1)
        propagate_to_configs(promote_folder, Path("data/configs"), logger)
        sys.exit(0)

    output_path = Path(args.output)
    data_path = Path(args.data)

    if args.params is not None:
        parts = [p.strip() for p in args.params.split(',')]
        requested_params = [p for p in parts if p]
        if not requested_params:
            logger.error(
                f"--params value produced no valid parameter names after splitting: '{args.params}'"
            )
            sys.exit(1)
        unknown = [p for p in requested_params if p not in PARAMETER_ORDER]
        if unknown:
            logger.error(
                f"Unknown --params value(s): {unknown}. Valid parameters: {PARAMETER_ORDER}"
            )
            sys.exit(1)
        parameter_order = requested_params
    else:
        parameter_order = PARAMETER_ORDER

    required_files = ['league_config.json', 'week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']

    if args.baseline:
        baseline_path = Path(args.baseline)
        if not baseline_path.exists():
            logger.error(f"Baseline config not found: {baseline_path}")
            sys.exit(1)
        if not baseline_path.is_dir():
            logger.error(f"Baseline must be a folder, not a file: {baseline_path}")
            logger.error(f"Expected folder with: {', '.join(required_files)}")
            sys.exit(1)
        missing = [f for f in required_files if not (baseline_path / f).exists()]
        if missing:
            logger.error(f"Baseline folder missing required files: {', '.join(missing)}")
            sys.exit(1)
    else:
        try:
            baseline_path = find_baseline_config()
        except FileNotFoundError as e:
            logger.error(str(e))
            sys.exit(1)

    logger.info(f"Using baseline config: {baseline_path}")

    if not data_path.exists():
        logger.error(f"Data folder not found: {data_path}")
        sys.exit(1)

    total_configs = (args.test_values + 1) ** 6
    print("\n" + "=" * 60)
    print("ACCURACY SIMULATION - TOURNAMENT OPTIMIZATION")
    print("=" * 60)
    print(f"Baseline config: {baseline_path}")
    print(f"Output directory: {output_path}")
    print(f"Data folder: {data_path}")
    print(f"Test values per param: {args.test_values}")
    print(f"Num params to test: {args.num_params}")
    print(f"Configs per parameter: {total_configs:,}")
    print("=" * 60 + "\n")

    try:
        manager = AccuracySimulationManager(
            baseline_config_path=baseline_path,
            output_dir=output_path,
            data_folder=data_path,
            parameter_order=parameter_order,
            num_test_values=args.test_values,
            num_parameters_to_test=args.num_params,
            max_workers=args.max_workers,
            use_processes=args.use_processes
        )
    except Exception as e:
        logger.error(f"Failed to initialize AccuracySimulationManager: {e}")
        sys.exit(1)

    try:
        optimal_path = manager.run_both()

        print("\n" + "=" * 60)
        print("TOURNAMENT OPTIMIZATION COMPLETE")
        print("=" * 60)
        print(f"Results saved to: {optimal_path}")
        print(manager.results_manager.get_summary())
        print("=" * 60 + "\n")

        if args.promote is True:
            propagate_to_configs(optimal_path, Path("data/configs"), logger)

    except KeyboardInterrupt:
        logger.warning("Simulation interrupted by user")
        print("\nSimulation interrupted. Partial results saved.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Simulation failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    while True:
        main()


