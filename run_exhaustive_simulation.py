#!/usr/bin/env python3
"""
Runner Script for Exhaustive Simulation

This script runs the exhaustive parameter optimization simulation.

On first run:
- Automatically finds the most recent optimal_*.json file in draft_helper/simulation/parameters/
- Determines which parameter has the most values (the parameter currently being tested)
- Sets the starting round to match that parameter's position in PARAMETER_ARRAY

This allows seamless continuation of exhaustive testing after interruption.

Usage:
    python run_exhaustive_simulation.py

Author: Kai Mizuno
Last Updated: October 2025
"""
PARAMETER_ARRAY = [
    "NORMALIZATION_MAX_SCALE",
    "DRAFT_ORDER_PRIMARY_BONUS",
    "DRAFT_ORDER_SECONDARY_BONUS",
    "MATCHUP_EXCELLENT_MULTIPLIER",
    "MATCHUP_GOOD_MULTIPLIER",
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
    "CONSISTENCY_LOW_MULTIPLIER",
    "CONSISTENCY_MEDIUM_MULTIPLIER",
    "CONSISTENCY_HIGH_MULTIPLIER",
]
PARAMETER_RANGES = {
    "NORMALIZATION_MAX_SCALE": 30,
    "DRAFT_ORDER_PRIMARY_BONUS": 30,
    "DRAFT_ORDER_SECONDARY_BONUS": 30,
    "MATCHUP_EXCELLENT_MULTIPLIER": 0.3,
    "MATCHUP_GOOD_MULTIPLIER": 0.3,
    "MATCHUP_POOR_MULTIPLIER": 0.3,
    "MATCHUP_VERY_POOR_MULTIPLIER": 0.3,
    "INJURY_PENALTIES_MEDIUM": 30,
    "INJURY_PENALTIES_HIGH": 30,
    "BASE_BYE_PENALTY": 30,
    "ADP_EXCELLENT_MULTIPLIER": 0.3,
    "ADP_GOOD_MULTIPLIER": 0.3,
    "ADP_POOR_MULTIPLIER": 0.3,
    "PLAYER_RATING_EXCELLENT_MULTIPLIER": 0.3,
    "PLAYER_RATING_GOOD_MULTIPLIER": 0.3,
    "PLAYER_RATING_POOR_MULTIPLIER": 0.3,
    "TEAM_EXCELLENT_MULTIPLIER": 0.3,
    "TEAM_GOOD_MULTIPLIER": 0.3,
    "TEAM_POOR_MULTIPLIER": 0.3,
    "CONSISTENCY_LOW_MULTIPLIER": 0.3,
    "CONSISTENCY_MEDIUM_MULTIPLIER": 0.3,
    "CONSISTENCY_HIGH_MULTIPLIER": 0.3
}

# Absolute min/max bounds for each parameter (enforced regardless of PARAMETER_RANGES)
# These bounds ensure generated values stay within valid ranges.
# For example, ADP_POOR_MULTIPLIER: (0.5, 2.0) means generated values will never be < 0.5 or > 2.0
# even if the optimal value ± PARAMETER_RANGES would go outside that range.
PARAMETER_BOUNDS = {
    "NORMALIZATION_MAX_SCALE": (60, 140),
    "DRAFT_ORDER_PRIMARY_BONUS": (25, 100),
    "DRAFT_ORDER_SECONDARY_BONUS": (25, 100),
    "MATCHUP_EXCELLENT_MULTIPLIER": (1.0, 2.0),
    "MATCHUP_GOOD_MULTIPLIER": (1.0, 2.0),
    "MATCHUP_POOR_MULTIPLIER": (0.1, 1.0),
    "MATCHUP_VERY_POOR_MULTIPLIER": (0.1, 1.0),
    "INJURY_PENALTIES_MEDIUM": (0, 100),
    "INJURY_PENALTIES_HIGH": (0, 100),
    "BASE_BYE_PENALTY": (0, 100),
    "ADP_EXCELLENT_MULTIPLIER": (1.0, 2.0),
    "ADP_GOOD_MULTIPLIER": (1.0, 2.0),
    "ADP_POOR_MULTIPLIER": (0.1, 1.0),
    "PLAYER_RATING_EXCELLENT_MULTIPLIER": (1.0, 2.0),
    "PLAYER_RATING_GOOD_MULTIPLIER": (1.0, 2.0),
    "PLAYER_RATING_POOR_MULTIPLIER": (0.1, 1.0),
    "TEAM_EXCELLENT_MULTIPLIER": (1.0, 2.0),
    "TEAM_GOOD_MULTIPLIER": (1.0, 2.0),
    "TEAM_POOR_MULTIPLIER": (0.1, 1.0),
    "CONSISTENCY_LOW_MULTIPLIER": (0.3, 2.0),
    "CONSISTENCY_MEDIUM_MULTIPLIER": (0.3, 2.0),
    "CONSISTENCY_HIGH_MULTIPLIER": (0.3, 2.0)
}
NUMBER_OF_TEST_VALUES = 0  # Number of test values per parameter
NUMBER_OF_RUNS = 100
STARTING_PARAMETER = "MATCHUP_EXCELLENT_MULTIPLIER"
STARTING_FILE = "optimal_2025-10-02_15-29-14.json"


import sys
import os
import json
from pathlib import Path
from datetime import datetime
import random

def get_parameter_array(param_name, value, round_number):
    if PARAMETER_ARRAY[round_number % len(PARAMETER_ARRAY)] == param_name:
        # Create array of test values around the optimal value
        range_width = PARAMETER_RANGES[param_name]
        min_bound, max_bound = PARAMETER_BOUNDS.get(param_name, (0, float('inf')))

        # Calculate search range, constrained by absolute bounds
        search_min = max(value - range_width, min_bound)
        search_max = min(value + range_width, max_bound)

        # Generate the array
        random_values = [value]
        for _ in range(NUMBER_OF_TEST_VALUES):
            for _ in range(20):  # Try up to 20 times to get a unique value
                val = round(random.uniform(search_min, search_max), 2)
                # Ensure value is within bounds
                val = max(min_bound, min(max_bound, val))
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
    # Round all values to 2 decimal places to avoid long decimals
    parameters = {}
    for param_name, param_value in config_params.items():
        if param_name in PARAMETER_ARRAY:
            # Round the base value to 2 decimals before creating array
            rounded_value = round(param_value, 2)
            parameters[param_name] = get_parameter_array(param_name, rounded_value, round_number)
        else:
            parameters[param_name] = [round(param_value, 2)]

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


def find_most_recent_optimal_json(parameter_path):
    """
    Find the most recent optimal_*.json file in the parameters directory.

    Args:
        parameter_path: Path to the parameters directory

    Returns:
        Filename of the most recent optimal JSON, or None if none found
    """
    optimal_files = list(parameter_path.glob("optimal_*.json"))
    if not optimal_files:
        return None

    # Sort by modification time, most recent first
    optimal_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return optimal_files[0].name


def determine_starting_round(json_path):
    """
    Determine the starting round based on which parameter has the most values.

    Args:
        json_path: Path to the JSON configuration file

    Returns:
        Round number (1-indexed) to start from
    """
    with open(json_path, 'r') as f:
        config = json.load(f)

    parameters = config.get('parameters', {})

    # Find parameter with most values
    max_values = 0
    max_param = None

    for param_name, param_values in parameters.items():
        if len(param_values) > max_values:
            max_values = len(param_values)
            max_param = param_name

    if max_param is None or max_param not in PARAMETER_ARRAY:
        # Default to first parameter if not found
        return 1

    # Return 1-indexed position in PARAMETER_ARRAY
    return PARAMETER_ARRAY.index(max_param) + 1


def main():
    """Main entry point for exhaustive simulation runner"""

    print(">> EXHAUSTIVE SIMULATION STARTING...", flush=True)

    # Get the directories
    script_dir = Path(__file__).parent
    parameter_path = script_dir / "draft_helper" / "simulation" / "parameters" / "parameter_sets"

    print(f">> Parameter path: {parameter_path}", flush=True)

    # Find most recent optimal JSON file
    json_file = find_most_recent_optimal_json(parameter_path)
    print(f">> Found file: {json_file}", flush=True)

    if json_file is None:
        # Fall back to hardcoded values if no optimal file found
        print(">> No optimal_*.json files found, using hardcoded starting values")
        json_file = STARTING_FILE
        starting_round = PARAMETER_ARRAY.index(STARTING_PARAMETER) + 1
    else:
        print(f">> Found most recent optimal file: {json_file}")
        json_path = parameter_path / json_file
        starting_round = determine_starting_round(json_path)
        print(f">> Determined starting round: {starting_round} (parameter: {PARAMETER_ARRAY[starting_round - 1]})")

    for round_number in range(starting_round, NUMBER_OF_RUNS+1):
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
