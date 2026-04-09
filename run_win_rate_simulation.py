"""
Run Simulation Script

Command-line interface for running fantasy football league simulations.
Can be run from the project root directory.

Provides three modes:
- single: Test a single config (fast, for debugging)
- full: Test all configs via grid search (slow, for exhaustive optimization)
- iterative: Test parameters one at a time (fast, for coordinate descent)

Usage (from project root):
    python run_simulation.py                       # defaults to iterative mode
    python run_simulation.py single --sims 5
    python run_simulation.py full --sims 100
    python run_simulation.py iterative --sims 100

Author: Kai Mizuno
"""

import argparse
import sys
from pathlib import Path
from utils.LoggingManager import setup_logger
from simulation.win_rate.SimulationManager import SimulationManager


LOGGING_LEVEL = 'INFO'
LOG_NAME = "win_rate_simulation"
LOGGING_FORMAT = 'standard'

DEFAULT_MODE='iterative'
DEFAULT_SIMS=5
DEFAULT_BASELINE=''
DEFAULT_OUTPUT='simulation/simulation_configs'
DEFAULT_WORKERS=8
DEFAULT_DATA='simulation/sim_data'
DEFAULT_TEST_VALUES=5
NUM_PARAMETERS_TO_TEST=1

PARAMETER_ORDER = [
    'DRAFT_NORMALIZATION_MAX_SCALE',
    'SAME_POS_BYE_WEIGHT',
    'DIFF_POS_BYE_WEIGHT',
    'PRIMARY_BONUS',
    'SECONDARY_BONUS',
    'ADP_SCORING_WEIGHT',
    'PLAYER_RATING_SCORING_WEIGHT',
]


def main():
    """
    Main entry point for simulation CLI.

    Provides three simulation modes:````````````````````````
    - single: Test baseline config (fast, for debugging)
    - full: Grid search all parameter combinations (exhaustive, slow)
    - iterative: Coordinate descent optimization (fast, local optimum)

    Parses command-line arguments, validates paths, initializes SimulationManager,
    and executes the selected optimization mode.

    Command-line Arguments:
        mode (str): Required. One of: single, full, iterative
        --sims (int): Number of simulations per config
        --baseline (str): Path to baseline configuration JSON
        --output (str): Output directory for results
        --workers (int): Number of parallel worker threads
        --data (str): Path to simulation data folder
        --test-values (int): Number of test values per parameter

    Raises:
        SystemExit: If baseline config or data folder not found
    """
    parser = argparse.ArgumentParser(
        description="Run fantasy football league simulations for parameter optimization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run iterative optimization (default mode)
  python run_simulation.py

  # Test single config with 5 simulations
  python run_simulation.py single --sims 5

  # Run full grid search optimization (exhaustive but slow)
  python run_simulation.py full --sims 100 --workers 8

  # Run iterative optimization with custom settings
  python run_simulation.py iterative --sims 100 --test-values 5

  # Use custom baseline config and output directory
  python run_simulation.py --baseline my_config.json --output results/test1
        """
    )

    parser.add_argument(
        '--enable-log-file',
        action='store_true',
        default=False,
        help='Enable logging to file (default: console only)'
    )

    parser.add_argument('--sims', type=int, default=DEFAULT_SIMS, help='Number of simulations per config')
    parser.add_argument('--baseline', type=str, default=DEFAULT_BASELINE, help='Path to baseline configuration')
    parser.add_argument('--output', type=str, default=DEFAULT_OUTPUT, help='Output directory for results')
    parser.add_argument('--workers', type=int, default=DEFAULT_WORKERS, help='Number of parallel workers')
    parser.add_argument('--data', type=str, default=DEFAULT_DATA, help='Path to simulation data folder')
    parser.add_argument('--test-values', type=int, default=DEFAULT_TEST_VALUES, help='Number of test values per parameter')
    parser.add_argument('--use-processes', action='store_true', default=False,
                        help='Use ProcessPoolExecutor for true parallelism (bypasses GIL)')

    subparsers = parser.add_subparsers(dest='mode', help='Simulation mode', required=False)

    single_parser = subparsers.add_parser(
        'single',
        help='Test a single configuration (fast, for debugging)'
    )
    single_parser.add_argument(
        '--sims',
        type=int,
        default=DEFAULT_SIMS,
        help='Number of simulations to run (default: 5)'
    )

    full_parser = subparsers.add_parser(
        'full',
        help='Run full optimization on all configs (slow)'
    )
    full_parser.add_argument(
        '--sims',
        type=int,
        default=DEFAULT_SIMS,
        help='Number of simulations per config (default: 50)'
    )

    iterative_parser = subparsers.add_parser(
        'iterative',
        help='Run iterative parameter optimization (coordinate descent)'
    )
    iterative_parser.add_argument(
        '--sims',
        type=int,
        default=DEFAULT_SIMS,
        help='Number of simulations per config (default: 50)'
    )

    for subparser in [single_parser, full_parser, iterative_parser]:
        subparser.add_argument(
            '--baseline',
            type=str,
            default=DEFAULT_BASELINE,
            help='Path to baseline configuration JSON (default: takes the most recent file in the output directory)'
        )
        subparser.add_argument(
            '--output',
            type=str,
            default=DEFAULT_OUTPUT,
            help='Output directory for results (default: simulation/simulation_configs)'
        )
        subparser.add_argument(
            '--workers',
            type=int,
            default=DEFAULT_WORKERS,
            help='Number of parallel worker threads (default: 7)'
        )
        subparser.add_argument(
            '--data',
            type=str,
            default=DEFAULT_DATA,
            help='Path to simulation data folder (default: simulation/sim_data)'
        )
        subparser.add_argument(
            '--test-values',
            type=int,
            default=DEFAULT_TEST_VALUES,
            help='Number of test values per parameter.'
        )
        subparser.add_argument(
            '--use-processes',
            action='store_true',
            default=False,
            help='Use ProcessPoolExecutor for true parallelism (bypasses GIL). '
                 'Default uses ThreadPoolExecutor. Recommended for CPU-bound simulations '
                 'on multi-core systems.'
        )

    args = parser.parse_args()

    setup_logger(LOG_NAME, LOGGING_LEVEL, args.enable_log_file, None, LOGGING_FORMAT)

    if args.mode is None:
        args.mode = DEFAULT_MODE

    output_dir = Path(args.output)


    def find_config_folders(search_dir: Path, pattern: str) -> list:
        """Find config folders matching pattern, sorted by modification time (newest first)."""
        folders = [p for p in search_dir.glob(pattern) if p.is_dir()]
        required_files = ['league_config.json', 'week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']
        valid_folders = []
        for folder in folders:
            if all((folder / f).exists() for f in required_files):
                valid_folders.append(folder)
        valid_folders.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        return valid_folders

    if args.baseline:
        baseline_path = Path(args.baseline)
        if not baseline_path.exists():
            print(f"Warning: Specified baseline config not found: {baseline_path}")
            print(f"  Searched at: {baseline_path.absolute()}")
            print(f"  Attempting to use most recent config from output directory...")
            baseline_path = None
    else:
        baseline_path = None

    if baseline_path is None:

        if args.mode == 'iterative':
            intermediate_folders = find_config_folders(output_dir, "intermediate_*")
            if intermediate_folders:
                baseline_path = intermediate_folders[0]
                print(f"[OK] Found intermediate folders - resuming from: {baseline_path.name}")

        if baseline_path is None:
            optimal_folders = find_config_folders(output_dir, "optimal_*")

            if optimal_folders:
                baseline_path = optimal_folders[0]
                print(f"[OK] Using most recent config folder from output directory: {baseline_path.name}")
            else:
                config_dir = Path("simulation/simulation_configs")
                if config_dir.exists():
                    optimal_folders = find_config_folders(config_dir, "optimal_*")
                    if optimal_folders:
                        baseline_path = optimal_folders[0]
                        print(f"[OK] Using baseline config folder from simulation_configs: {baseline_path.name}")
                    else:
                        print(f"Error: No optimal config folders found in {output_dir} or {config_dir}")
                        print(f"\nExpected folder structure with files:")
                        print(f"  optimal_*/league_config.json")
                        print(f"  optimal_*/week1-5.json")
                        print(f"  optimal_*/week6-9.json")
                        print(f"  optimal_*/week10-13.json")
                        print(f"  optimal_*/week14-17.json")
                        print(f"\nPlease provide a baseline config folder using --baseline argument")
                        sys.exit(1)
                else:
                    print(f"Error: No baseline config found")
                    print(f"  Output directory: {output_dir.absolute()}")
                    print(f"  Config directory: {config_dir.absolute()}")
                    print(f"\nPlease provide a baseline config folder using --baseline argument")
                    sys.exit(1)

    data_folder = Path(args.data)
    if not data_folder.exists():
        print(f"Error: Data folder not found: {data_folder}")
        print(f"  Searched at: {data_folder.absolute()}")
        print(f"\nExpected structure:")
        print(f"  {data_folder}/players_projected.csv")
        print(f"  {data_folder}/players_actual.csv")
        print(f"  {data_folder}/teams_week_N.csv")
        sys.exit(1)

    executor_type = "ProcessPoolExecutor" if args.use_processes else "ThreadPoolExecutor"
    print("=" * 80)
    print("FANTASY FOOTBALL SIMULATION OPTIMIZER")
    print("=" * 80)
    print(f"Mode: {args.mode}")
    print(f"Baseline config: {baseline_path}")
    print(f"Data folder: {data_folder}")
    print(f"Output directory: {output_dir}")
    print(f"Workers: {args.workers} ({executor_type})")

    if args.mode == 'single':
        print(f"Simulations: {args.sims}")
        print(f"Note: Single mode uses 2025 season data for quick testing")
        print("=" * 80)

        manager = SimulationManager(
            baseline_config_path=baseline_path,
            output_dir=output_dir,
            num_simulations_per_config=args.sims,
            max_workers=args.workers,
            data_folder=data_folder,
            parameter_order=PARAMETER_ORDER,
            num_test_values=args.test_values,
            num_parameters_to_test=NUM_PARAMETERS_TO_TEST,
            use_processes=args.use_processes
        )

        manager.run_single_config_test(season='2025')

    elif args.mode == 'full':
        total_configs = (args.test_values + 1) ** 6
        print(f"Simulations per config: {args.sims}")
        print(f"Total configurations: {total_configs:,}")
        print(f"Total simulations: {total_configs * args.sims:,}")
        print("=" * 80)
        print("")

        while True:
            manager = SimulationManager(
                baseline_config_path=baseline_path,
                output_dir=output_dir,
                num_simulations_per_config=args.sims,
                max_workers=args.workers,
                data_folder=data_folder,
                parameter_order=PARAMETER_ORDER,
                num_test_values=args.test_values,
                use_processes=args.use_processes
            )

            baseline_path = manager.run_full_optimization()
            print(f"\nOptimal configuration saved to: {baseline_path}")

    elif args.mode == 'iterative':
        num_params = 24
        configs_per_param = args.test_values + 1
        total_configs = num_params * configs_per_param
        print(f"Simulations per config: {args.sims}")
        print(f"Parameters to optimize: {num_params}")
        print(f"Configs per parameter: {configs_per_param}")
        print(f"Total configurations: {total_configs}")
        print(f"Total simulations: {total_configs * args.sims:,}")
        print("=" * 80)
        print("")

        while True:
            manager = SimulationManager(
                baseline_config_path=baseline_path,
                output_dir=output_dir,
                num_simulations_per_config=args.sims,
                max_workers=args.workers,
                data_folder=data_folder,
                parameter_order=PARAMETER_ORDER,
                num_test_values=args.test_values,
                num_parameters_to_test=NUM_PARAMETERS_TO_TEST,
                use_processes=args.use_processes
            )

            baseline_path = manager.run_iterative_optimization()
            print(f"\nOptimal configuration saved to: {baseline_path}")


if __name__ == "__main__":
    main()


