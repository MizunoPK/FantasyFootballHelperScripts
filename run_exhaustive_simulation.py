#!/usr/bin/env python3
"""
Runner Script for Exhaustive Simulation

This script runs the exhaustive parameter optimization simulation with the
exhaustive_start.json configuration file.

Usage:
    python run_big_simulation.py

This is equivalent to:
    python run_simulation.py draft_helper/simulation/parameters/exhaustive_start.json

Author: Kai Mizuno
Last Updated: October 2025
"""
PARAMETER_ARRAY = [
    "NORMALIZATION_MAX_SCALE",
    "DRAFT_ORDER_PRIMARY_BONUS",
    "DRAFT_ORDER_SECONDARY_BONUS",
    "MATCHUP_EXCELLENT_MULTIPLIER", 
    "MATCHUP_GOOD_MULTIPLIER",
    "MATCHUP_NEUTRAL_MULTIPLIER",
    "MATCHUP_POOR_MULTIPLIER",
    "MATCHUP_VERY_POOR_MULTIPLIER",
    "INJURY_PENALTIES_MEDIUM",
    "INJURY_PENALTIES_HIGH",
    "BASE_BYE_PENALTY",
    "ADP_EXCELLENT_MULTIPLIER",
    "ADP_GOOD_MULTIPLIER",
    "ADP_POOR_MULTIPLIER",
    "PLAYER_RATING_EXCELLENT_MULTIPLIER",
    "PLAYER_RATING_GOOD_MULTIPLIER",
    "PLAYER_RATING_POOR_MULTIPLIER", 
    "TEAM_EXCELLENT_MULTIPLIER",
    "TEAM_GOOD_MULTIPLIER",
    "TEAM_POOR_MULTIPLIER",
]
PARAMETER_RANGES = {
    "NORMALIZATION_MAX_SCALE": 20,
    "DRAFT_ORDER_PRIMARY_BONUS": 20,
    "DRAFT_ORDER_SECONDARY_BONUS": 20,
    "MATCHUP_EXCELLENT_MULTIPLIER": 0.2,
    "MATCHUP_GOOD_MULTIPLIER": 0.2,
    "MATCHUP_NEUTRAL_MULTIPLIER": 0.2,
    "MATCHUP_POOR_MULTIPLIER": 0.2,
    "MATCHUP_VERY_POOR_MULTIPLIER": 0.2,
    "INJURY_PENALTIES_MEDIUM": 20,
    "INJURY_PENALTIES_HIGH": 20,
    "BASE_BYE_PENALTY": 20,
    "ADP_EXCELLENT_MULTIPLIER": 0.2,
    "ADP_GOOD_MULTIPLIER": 0.2,
    "ADP_POOR_MULTIPLIER": 0.2,
    "PLAYER_RATING_EXCELLENT_MULTIPLIER": 0.2,
    "PLAYER_RATING_GOOD_MULTIPLIER": 0.2,
    "PLAYER_RATING_POOR_MULTIPLIER": 0.2,
    "TEAM_EXCELLENT_MULTIPLIER": 0.2,
    "TEAM_GOOD_MULTIPLIER": 0.2,
    "TEAM_POOR_MULTIPLIER": 0.2
}
NUMBER_OF_TEST_VALUES = 10  # Number of test values per parameter
NUMBER_OF_RUNS = 50


import sys
import os
import json
from pathlib import Path
from datetime import datetime
import random

def get_decimal_places(num):
    if isinstance(num, float):
        return len(str(num).split('.')[1]) if '.' in str(num) else 0
    return 0

def get_parameter_array(param_name, value, round_number):
    if PARAMETER_ARRAY[round_number % len(PARAMETER_ARRAY)] == param_name:
        # Create array of test values around the optimal value
        range_width = PARAMETER_RANGES[param_name]

        decimals = get_decimal_places(value)
        # Generate the array
        random_values = [value]
        for _ in range(NUMBER_OF_TEST_VALUES):
            for _ in range(20):  # Try up to 20 times to get a unique value
                val = round(random.uniform(value - range_width, value + range_width), decimals)
                if val not in random_values:
                    random_values.append(val)
                    break
        random_values.sort()
        return random_values
    else:
        return [value]


def prepare_json(analysis_data, round_number):
    """
    Prepare the next parameter configuration based on analysis data.

    Args:
        analysis_data: Dictionary returned by run_simulation containing 'optimal_config'
        round_number: Current round number of the simulation

    Returns:
        A new parameter configuration dictionary for the next simulation run
    """
    if not analysis_data or 'optimal_config' not in analysis_data:
        print(">> No optimal configuration found in analysis data")
        return None

    optimal_config = analysis_data['optimal_config']
    if not optimal_config:
        print(">> Optimal configuration is empty")
        return None

    # Extract the configuration parameters
    config_params = optimal_config['config_params']
    performance = optimal_config['performance']

    # Generate timestamp for unique filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Create parameters dict with single-value arrays for each parameter
    parameters = {}
    for param_name, param_value in config_params.items():
        parameters[param_name] = get_parameter_array(param_name, param_value, round_number)

    # Create the JSON structure
    json_data = {
        "config_name": f"optimal_{timestamp}",
        "description": (
            f"Optimal configuration found from simulation run at {timestamp}. "
            f"Win rate: {performance['win_percentage']:.1%}, "
            f"Total points: {performance['total_points']:.1f}, "
            f"PPG: {performance['points_per_game']:.1f}, "
            f"Consistency: {performance['consistency']:.1f}"
        ),
        "parameters": parameters
    }

    return json_data, timestamp, performance


def save_next_config_to_json(analysis_data, output_dir, round_number):
    """
    Save the optimal configuration from simulation results to a JSON parameter file for the next simulation run.

    Args:
        analysis_data: Dictionary returned by run_simulation containing 'optimal_config'
        output_dir: Directory to save the JSON file (typically draft_helper/simulation/parameters)

    Returns:
        Path to the saved JSON file, or None if no optimal config found
    """
    json_data, timestamp, performance = prepare_json(analysis_data, round_number)
    if json_data is None:
        return None

    # Save to file
    file_name = f"optimal_{timestamp}.json"
    output_path = Path(output_dir) / file_name

    with open(output_path, 'w') as f:
        json.dump(json_data, f, indent=2)

    print()
    print(f">> Optimal configuration saved to: {output_path}")
    print(f">> Config name: {json_data['config_name']}")
    print(f">> Win rate: {performance['win_percentage']:.1%}")
    print(f">> Total points: {performance['total_points']:.1f}")

    return file_name


def main():
    """Main entry point for exhaustive simulation runner"""

    # Get the directories
    script_dir = Path(__file__).parent
    parameter_path = script_dir / "draft_helper" / "simulation" / "parameters"
    json_file = "exhaustive_start.json"

    for round_number in range(1, NUMBER_OF_RUNS+1):
        print()
        print("#" * 80)
        print(f">> STARTING ROUND {round_number} OF EXHAUSTIVE SIMULATION")
        print("#" * 80)
        print()

        # Path to the configuration
        config_path = parameter_path / json_file

        # Validate config file exists
        if not config_path.exists():
            print(f"Error: Configuration file not found: {config_path}")
            print("\nPlease ensure exhaustive_start.json exists in draft_helper/simulation/parameters/")
            return 1

        # Add simulation directory to path
        simulation_dir = script_dir / "draft_helper" / "simulation"
        sys.path.insert(0, str(simulation_dir))

        try:
            # Import after path is set
            from main_simulator import run_simulation
            from parameter_loader import load_parameter_config, get_num_combinations

            # Load and display configuration info
            print("=" * 70)
            print(">> EXHAUSTIVE SIMULATION")
            print("=" * 70)
            print(f">> Loading configuration from: {config_path.relative_to(script_dir)}")

            config = load_parameter_config(str(config_path))

            print(f">> Configuration: {config['config_name']}")
            print(f">> Description: {config['description']}")

            # Calculate number of combinations
            num_combinations = get_num_combinations(config['parameters'])
            print(f">> Parameter combinations to test: {num_combinations:,}")

            if num_combinations > 1000:
                print()
                print(f"⚠️  WARNING: Testing {num_combinations:,} combinations may take many hours!")
                print(f"   Estimated time: {num_combinations * 3 / 60:.1f} minutes minimum")
                print()
                response = input(">> Continue with exhaustive simulation? (y/n): ")
                if response.lower() != 'y':
                    print(">> Simulation cancelled.")
                    return 0

            print()
            print("=" * 70)
            print(">> Starting exhaustive simulation run...")
            print("=" * 70)
            print()

            # Run simulation
            results_file, analysis_data = run_simulation(parameter_config_path=str(config_path))

            print()
            print("=" * 70)
            print(">> Exhaustive simulation completed successfully!")
            print(f">> Results saved to: {results_file}")
            print("=" * 70)

            # Save optimal configuration to JSON
            params_dir = script_dir / "draft_helper" / "simulation" / "parameters"
            next_config_file = save_next_config_to_json(analysis_data, params_dir, round_number)
            if next_config_file is None:
                print(">> No optimal configuration to save.")
                return 0

            json_file = next_config_file

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
