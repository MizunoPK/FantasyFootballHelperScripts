"""
Run Accuracy Simulation

CLI tool for running accuracy simulation to find optimal scoring algorithm
parameters. Evaluates prediction accuracy using MAE (Mean Absolute Error).

Modes:
- ros: Rest of Season mode - optimizes draft_config.json
- weekly: Weekly mode - optimizes week1-5.json, week6-9.json, etc.
- both: Runs both ROS and weekly (default)

Usage:
    python run_accuracy_simulation.py [mode] [options]

Examples:
    # Run both modes (default)
    python run_accuracy_simulation.py

    # Run ROS mode only
    python run_accuracy_simulation.py ros

    # Run weekly mode only
    python run_accuracy_simulation.py weekly

    # Run with custom baseline config
    python run_accuracy_simulation.py both --baseline path/to/config.json

    # Run with more test values per parameter
    python run_accuracy_simulation.py both --test-values 7

Author: Kai Mizuno
"""

import argparse
import sys
from pathlib import Path

# Add simulation/accuracy to path
sys.path.append(str(Path(__file__).parent / "simulation" / "accuracy"))
from AccuracySimulationManager import AccuracySimulationManager

# Add utils to path
sys.path.append(str(Path(__file__).parent))
from utils.LoggingManager import setup_logger, get_logger


# Logging Configuration
LOGGING_LEVEL = "DEBUG"
LOGGING_TO_FILE = True           # True = log to file, False = log to console
LOG_NAME = "accuracy_simulation"
LOGGING_FILE = "./simulation/accuracy_log.txt"  # Log file path (only used if LOGGING_TO_FILE=True)
LOGGING_FORMAT = "detailed"      # detailed / standard / simple

# Simulation Configuration Defaults
DEFAULT_MODE = 'both'
DEFAULT_BASELINE = ''            # Empty = auto-detect most recent optimal config
DEFAULT_OUTPUT = 'simulation/simulation_configs'
DEFAULT_DATA = 'simulation/sim_data'
DEFAULT_TEST_VALUES = 20          # Number of test values per parameter
NUM_PARAMETERS_TO_TEST = 1       # Number of parameters to test simultaneously


# Parameters to optimize for accuracy (16 prediction params)
# These affect how projected points are calculated, NOT draft strategy
#
# Draft strategy parameters (SAME_POS_BYE_WEIGHT, PRIMARY_BONUS, ADP_SCORING_WEIGHT, etc.)
# are optimized by win-rate simulation instead - see run_win_rate_simulation.py
#
# NOTE: PLAYER_RATING_SCORING_WEIGHT is NOT included because StarterHelperModeManager
# (the consuming mode) has player_rating=False, so this parameter has no effect.
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

    # Required files for a valid config folder
    required_files = ['league_config.json', 'week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']

    def is_valid_config_folder(folder: Path) -> bool:
        """Check if folder contains all required config files."""
        return all((folder / f).exists() for f in required_files)

    # Look for accuracy_optimal_* folders first
    accuracy_folders = sorted([
        p for p in config_dir.iterdir()
        if p.is_dir() and p.name.startswith("accuracy_optimal_") and is_valid_config_folder(p)
    ], key=lambda p: p.stat().st_mtime, reverse=True)

    if accuracy_folders:
        return accuracy_folders[0]

    # Fall back to optimal_* folders from win-rate simulation
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
        description="Run accuracy simulation to find optimal scoring parameters"
    )

    parser.add_argument(
        'mode',
        nargs='?',
        default=DEFAULT_MODE,
        choices=['ros', 'weekly', 'both'],
        help=f"Simulation mode: ros (Rest of Season), weekly, or both (default: {DEFAULT_MODE})"
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

    args = parser.parse_args()

    # Setup logging
    setup_logger(LOG_NAME, LOGGING_LEVEL, LOGGING_TO_FILE, LOGGING_FILE, LOGGING_FORMAT)
    logger = get_logger()

    # Convert string paths to Path objects
    output_path = Path(args.output)
    data_path = Path(args.data)

    # Required files for a valid config folder
    required_files = ['league_config.json', 'week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']

    # Find baseline config
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

    # Validate data folder
    if not data_path.exists():
        logger.error(f"Data folder not found: {data_path}")
        sys.exit(1)

    # Show configuration
    total_configs = (args.test_values + 1) ** 6
    print("\n" + "=" * 60)
    print("ACCURACY SIMULATION")
    print("=" * 60)
    print(f"Mode: {args.mode}")
    print(f"Baseline config: {baseline_path}")
    print(f"Output directory: {output_path}")
    print(f"Data folder: {data_path}")
    print(f"Test values per param: {args.test_values}")
    print(f"Num params to test: {args.num_params}")
    print(f"Configs per parameter: {total_configs:,}")
    print("=" * 60 + "\n")

    # Initialize manager
    try:
        manager = AccuracySimulationManager(
            baseline_config_path=baseline_path,
            output_dir=output_path,
            data_folder=data_path,
            parameter_order=PARAMETER_ORDER,
            num_test_values=args.test_values,
            num_parameters_to_test=args.num_params
        )
    except Exception as e:
        logger.error(f"Failed to initialize AccuracySimulationManager: {e}")
        sys.exit(1)

    # Run simulation
    try:
        if args.mode == 'ros':
            optimal_path = manager.run_ros_optimization()
        elif args.mode == 'weekly':
            optimal_path = manager.run_weekly_optimization()
        else:  # both
            optimal_path = manager.run_both()

        print("\n" + "=" * 60)
        print("SIMULATION COMPLETE")
        print("=" * 60)
        print(f"Results saved to: {optimal_path}")
        print(manager.results_manager.get_summary())
        print("=" * 60 + "\n")

    except KeyboardInterrupt:
        logger.warning("Simulation interrupted by user")
        print("\nSimulation interrupted. Partial results saved.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Simulation failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
