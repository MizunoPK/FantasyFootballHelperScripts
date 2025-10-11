"""
Run Simulation Script

Command-line interface for running fantasy football league simulations.
Provides three modes:
- single: Test a single config (fast, for debugging)
- subset: Test a small subset of configs (moderate, for validation)
- full: Test all 46,656 configs (slow, for full optimization)

Usage:
    python run_simulation.py single --sims 5
    python run_simulation.py subset --configs 20 --sims 10 --workers 4
    python run_simulation.py full --sims 100 --workers 8

Author: Kai Mizuno
Date: 2024
"""

import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from SimulationManager import SimulationManager


def main():
    """Main entry point for simulation CLI."""
    parser = argparse.ArgumentParser(
        description="Run fantasy football league simulations for parameter optimization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test single config with 5 simulations
  python run_simulation.py single --sims 5

  # Test 20 configs with 10 simulations each using 4 workers
  python run_simulation.py subset --configs 20 --sims 10 --workers 4

  # Run full optimization of 46,656 configs with 100 sims each
  python run_simulation.py full --sims 100 --workers 8

  # Use custom baseline config and output directory
  python run_simulation.py subset --baseline my_config.json --output results/test1
        """
    )

    # Mode selection
    subparsers = parser.add_subparsers(dest='mode', help='Simulation mode', required=True)

    # Single config mode
    single_parser = subparsers.add_parser(
        'single',
        help='Test a single configuration (fast, for debugging)'
    )
    single_parser.add_argument(
        '--sims',
        type=int,
        default=5,
        help='Number of simulations to run (default: 5)'
    )

    # Subset mode
    subset_parser = subparsers.add_parser(
        'subset',
        help='Test a subset of configurations (for validation)'
    )
    subset_parser.add_argument(
        '--configs',
        type=int,
        default=10,
        help='Number of configs to test (default: 10)'
    )
    subset_parser.add_argument(
        '--sims',
        type=int,
        default=10,
        help='Number of simulations per config (default: 10)'
    )

    # Full optimization mode
    full_parser = subparsers.add_parser(
        'full',
        help='Run full optimization on all 46,656 configs (slow)'
    )
    full_parser.add_argument(
        '--sims',
        type=int,
        default=100,
        help='Number of simulations per config (default: 100)'
    )

    # Common arguments for all modes
    for subparser in [single_parser, subset_parser, full_parser]:
        subparser.add_argument(
            '--baseline',
            type=str,
            default='simulation/simulated_configs/optimal_2025-10-02_15-29-14.json.json',
            help='Path to baseline configuration JSON (default: simulation/simulated_configs/optimal_2025-10-02_15-29-14.json.json)'
        )
        subparser.add_argument(
            '--output',
            type=str,
            default='simulation/results',
            help='Output directory for results (default: simulation/results)'
        )
        subparser.add_argument(
            '--workers',
            type=int,
            default=4,
            help='Number of parallel worker threads (default: 4)'
        )
        subparser.add_argument(
            '--data',
            type=str,
            default='simulation/sim_data',
            help='Path to simulation data folder (default: simulation/sim_data)'
        )

    args = parser.parse_args()

    # Validate paths
    baseline_path = Path(args.baseline)
    if not baseline_path.exists():
        print(f"Error: Baseline config not found: {baseline_path}")
        sys.exit(1)

    data_folder = Path(args.data)
    if not data_folder.exists():
        print(f"Error: Data folder not found: {data_folder}")
        sys.exit(1)

    output_dir = Path(args.output)

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
            data_folder=data_folder
        )

        # Run single config test
        manager.run_single_config_test()

    elif args.mode == 'subset':
        print(f"Configs to test: {args.configs}")
        print(f"Simulations per config: {args.sims}")
        print(f"Total simulations: {args.configs * args.sims}")
        print("=" * 80)

        # Initialize manager
        manager = SimulationManager(
            baseline_config_path=baseline_path,
            output_dir=output_dir,
            num_simulations_per_config=args.sims,
            max_workers=args.workers,
            data_folder=data_folder
        )

        # Run subset test
        optimal_path = manager.run_subset_test(num_configs=args.configs)
        print(f"\nOptimal configuration saved to: {optimal_path}")

    elif args.mode == 'full':
        print(f"Configs to test: 46,656")
        print(f"Simulations per config: {args.sims}")
        print(f"Total simulations: {46656 * args.sims:,}")
        print("=" * 80)
        print("\nWARNING: Full optimization can take a long time!")
        print(f"Estimated time: ~{estimate_time(args.sims, args.workers)}")
        print("")

        response = input("Do you want to continue? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("Aborted.")
            sys.exit(0)

        # Initialize manager
        manager = SimulationManager(
            baseline_config_path=baseline_path,
            output_dir=output_dir,
            num_simulations_per_config=args.sims,
            max_workers=args.workers,
            data_folder=data_folder
        )

        # Run full optimization
        optimal_path = manager.run_full_optimization()
        print(f"\nOptimal configuration saved to: {optimal_path}")


def estimate_time(sims_per_config: int, workers: int) -> str:
    """
    Estimate total runtime for full optimization.

    Args:
        sims_per_config (int): Number of simulations per config
        workers (int): Number of parallel workers

    Returns:
        str: Human-readable time estimate
    """
    # Rough estimate: 1 simulation takes ~0.7 seconds
    # With parallelization, effective rate is ~0.7/workers seconds per sim
    total_sims = 46656 * sims_per_config
    seconds_per_sim = 0.7 / workers
    total_seconds = total_sims * seconds_per_sim

    # Add 10% overhead for config generation, result aggregation, etc.
    total_seconds *= 1.1

    # Format as human-readable
    if total_seconds < 3600:
        minutes = int(total_seconds / 60)
        return f"{minutes} minutes"
    elif total_seconds < 86400:
        hours = int(total_seconds / 3600)
        minutes = int((total_seconds % 3600) / 60)
        return f"{hours}h {minutes}m"
    else:
        days = int(total_seconds / 86400)
        hours = int((total_seconds % 86400) / 3600)
        return f"{days}d {hours}h"


if __name__ == "__main__":
    main()
