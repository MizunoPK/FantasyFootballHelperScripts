#!/usr/bin/env python3
"""
Runner Script for Draft Helper Simulation

This script runs parameter optimization simulations with JSON configuration files.

Usage:
    python run_simulation.py <path_to_config.json>
    python run_simulation.py draft_helper/simulation/parameters/baseline_parameters.json

Author: Generated for NFL Fantasy Data Collection
Last Updated: September 2025
"""

import sys
import os
import argparse
from pathlib import Path

def main():
    """Main entry point for simulation runner"""

    parser = argparse.ArgumentParser(
        description='Run draft helper simulation with parameter configuration',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_simulation.py draft_helper/simulation/parameters/baseline_parameters.json
  python run_simulation.py draft_helper/simulation/parameters/parameter_template.json

Configuration files should be JSON format with all 20 required parameters.
See draft_helper/simulation/parameters/README.md for documentation.
        """
    )

    parser.add_argument(
        'config_path',
        type=str,
        help='Path to JSON parameter configuration file'
    )

    parser.add_argument(
        '--sims',
        type=int,
        default=None,
        help='Number of simulations per configuration (overrides config setting)'
    )

    args = parser.parse_args()

    # Validate config file exists
    config_path = Path(args.config_path)
    if not config_path.exists():
        print(f"Error: Configuration file not found: {args.config_path}")
        print("\nAvailable example configurations:")
        params_dir = Path(__file__).parent / "draft_helper" / "simulation" / "parameters"
        if params_dir.exists():
            for json_file in sorted(params_dir.glob("*.json")):
                print(f"  - {json_file.relative_to(Path(__file__).parent)}")
        sys.exit(1)

    # Add simulation directory to path
    script_dir = Path(__file__).parent
    simulation_dir = script_dir / "draft_helper" / "simulation"
    sys.path.insert(0, str(simulation_dir))

    try:
        # Import after path is set
        from main_simulator import run_simulation
        from parameter_loader import load_parameter_config, get_num_combinations

        # Load and validate configuration
        print(f">> Loading configuration from: {args.config_path}")
        config = load_parameter_config(str(config_path))

        print(f">> Configuration: {config['config_name']}")
        print(f">> Description: {config['description']}")

        # Calculate number of combinations
        num_combinations = get_num_combinations(config['parameters'])
        print(f">> Parameter combinations to test: {num_combinations:,}")

        if num_combinations > 1000:
            print(f">> WARNING: Testing {num_combinations:,} combinations may take a very long time!")
            response = input(">> Continue? (y/n): ")
            if response.lower() != 'y':
                print(">> Simulation cancelled.")
                sys.exit(0)

        # Override simulation count if specified
        if args.sims:
            print(f">> Simulations per config: {args.sims} (from --sims argument)")
            # Note: This would require modifying config module, not implemented yet
            print(">> Warning: --sims override not yet implemented, using config default")

        print()
        print("=" * 70)
        print(">> Starting simulation run...")
        print("=" * 70)
        print()

        # Run simulation
        results_file = run_simulation(parameter_config_path=str(config_path))

        print()
        print("=" * 70)
        print(">> Simulation completed successfully!")
        print(f">> Results saved to: {results_file}")
        print("=" * 70)
        print()
        print("Next steps:")
        print("  1. Tell Claude: 'new simulation result file is ready'")
        print("  2. Claude will analyze results and update execution tracker")
        print("  3. Claude will generate next parameter configuration to test")
        print()

        return 0

    except KeyboardInterrupt:
        print("\n>> Simulation interrupted by user")
        return 1
    except Exception as e:
        print(f"\n>> Simulation failed with error:")
        print(f">> {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
