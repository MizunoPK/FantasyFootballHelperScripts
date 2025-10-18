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

# Add simulation directory to path for imports
sys.path.append(str(Path(__file__).parent / "simulation"))
from SimulationManager import SimulationManager


LOGGING_LEVEL = 'INFO'      # ← DEBUG, INFO, WARNING, ERROR, CRITICAL (WARNING+ to reduce spam)
LOGGING_TO_FILE = False        # ← Console vs file logging
LOG_NAME = "simulation"
LOGGING_FILE = './simulation/log.txt'
LOGGING_FORMAT = 'standard'     # detailed / standard / simple

DEFAULT_MODE='iterative'
DEFAULT_SIMS=100
DEFAULT_BASELINE=''
DEFAULT_OUTPUT='simulation/simulation_configs'
DEFAULT_WORKERS=7
DEFAULT_DATA='simulation/sim_data'
DEFAULT_TEST_VALUES=10


def main():
    """Main entry point for simulation CLI."""
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
    setup_logger(LOG_NAME, LOGGING_LEVEL, LOGGING_TO_FILE, LOGGING_FILE, LOGGING_FORMAT)

    # Mode selection
    subparsers = parser.add_subparsers(dest='mode', help='Simulation mode', required=False)

    # Single config mode
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

    # Full optimization mode
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

    # Iterative optimization mode
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

    # Common arguments for all modes
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

    args = parser.parse_args()

    # Set default mode if not provided
    if args.mode is None:
        args.mode = DEFAULT_MODE
        # Set default values for iterative mode when no mode specified
        if not hasattr(args, 'sims'):
            args.sims = DEFAULT_SIMS
        if not hasattr(args, 'baseline'):
            args.baseline = DEFAULT_BASELINE
        if not hasattr(args, 'output'):
            args.output = DEFAULT_OUTPUT
        if not hasattr(args, 'workers'):
            args.workers = DEFAULT_WORKERS
        if not hasattr(args, 'data'):
            args.data = DEFAULT_DATA
        if not hasattr(args, 'test_values'):
            args.test_values = DEFAULT_TEST_VALUES

    # Validate and resolve baseline path
    output_dir = Path(args.output)

    if args.baseline:
        baseline_path = Path(args.baseline)
        if not baseline_path.exists():
            print(f"Warning: Specified baseline config not found: {baseline_path}")
            print(f"  Searched at: {baseline_path.absolute()}")
            print(f"  Attempting to use most recent config from output directory...")
            baseline_path = None
    else:
        baseline_path = None

    # If no baseline or baseline doesn't exist, find most recent optimal config in output_dir
    if baseline_path is None:
        # Look for optimal_*.json files in output directory
        optimal_configs = list(output_dir.glob("optimal_*.json"))

        if optimal_configs:
            # Sort by modification time (most recent first)
            optimal_configs.sort(key=lambda p: p.stat().st_mtime, reverse=True)
            baseline_path = optimal_configs[0]
            print(f"✓ Using most recent config from output directory: {baseline_path.name}")
        else:
            # Fall back to optimal_configs directory
            config_dir = Path("simulation/simulation_configs")
            if config_dir.exists():
                optimal_configs = list(config_dir.glob("optimal_*.json"))
                if optimal_configs:
                    optimal_configs.sort(key=lambda p: p.stat().st_mtime, reverse=True)
                    baseline_path = optimal_configs[0]
                    print(f"✓ Using baseline config from simulation_configs: {baseline_path.name}")
                else:
                    print(f"Error: No optimal config files found in {output_dir} or {config_dir}")
                    print(f"\nPlease provide a baseline config using --baseline argument")
                    sys.exit(1)
            else:
                print(f"Error: No baseline config found")
                print(f"  Output directory: {output_dir.absolute()}")
                print(f"  Config directory: {config_dir.absolute()}")
                print(f"\nPlease provide a baseline config using --baseline argument")
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

    # Display configuration
    print("=" * 80)
    print("FANTASY FOOTBALL SIMULATION OPTIMIZER")
    print("=" * 80)
    print(f"Mode: {args.mode}")
    print(f"Baseline config: {baseline_path}")
    print(f"Data folder: {data_folder}")
    print(f"Output directory: {output_dir}")
    print(f"Worker threads: {args.workers}")

    if args.mode == 'single':
        print(f"Simulations: {args.sims}")
        print("=" * 80)

        # Initialize manager
        manager = SimulationManager(
            baseline_config_path=baseline_path,
            output_dir=output_dir,
            num_simulations_per_config=args.sims,
            max_workers=args.workers,
            data_folder=data_folder,
            num_test_values=args.test_values
        )

        # Run single config test
        manager.run_single_config_test()

    elif args.mode == 'full':
        total_configs = (args.test_values + 1) ** 6
        print(f"Simulations per config: {args.sims}")
        print(f"Total configurations: {total_configs:,}")
        print(f"Total simulations: {total_configs * args.sims:,}")
        print("=" * 80)
        print("")

        while True:
        # Initialize manager
            manager = SimulationManager(
                baseline_config_path=baseline_path,
                output_dir=output_dir,
                num_simulations_per_config=args.sims,
                max_workers=args.workers,
                data_folder=data_folder,
                num_test_values=args.test_values
            )

            # Run full optimization
            baseline_path = manager.run_full_optimization()
            print(f"\nOptimal configuration saved to: {baseline_path}")

    elif args.mode == 'iterative':
        num_params = 24  # 4 scalars + 20 multipliers
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
            # Initialize manager
            manager = SimulationManager(
                baseline_config_path=baseline_path,
                output_dir=output_dir,
                num_simulations_per_config=args.sims,
                max_workers=args.workers,
                data_folder=data_folder,
                num_test_values=args.test_values
            )

            # Run iterative optimization
            baseline_path = manager.run_iterative_optimization()
            print(f"\nOptimal configuration saved to: {baseline_path}")


if __name__ == "__main__":
    main()
