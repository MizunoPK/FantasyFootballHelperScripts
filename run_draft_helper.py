#!/usr/bin/env python3
"""
Runner Script for Draft Helper

This script runs the draft helper from the parent directory.

Usage:
    python run_draft_helper.py                    # Normal draft helper
    python run_draft_helper.py --simulate         # Run draft simulation analysis

Author: Generated for NFL Fantasy Data Collection
Last Updated: September 2025
"""

import os
import subprocess
import sys
import argparse
from pathlib import Path

def run_simulation():
    """Run the draft simulation analysis"""
    try:
        # Import and run the simulation
        script_dir = Path(__file__).parent
        simulation_dir = script_dir / "draft_helper" / "simulation"

        # Add to Python path
        sys.path.insert(0, str(simulation_dir))

        from main_simulator import run_simulation

        print(">> Starting Draft Simulation Analysis")
        print()

        results_file = run_simulation()

        print()
        print(">> Simulation completed successfully!")
        print(f">> Results available at: {results_file}")

        return 0

    except Exception as e:
        print(f">> Simulation failed: {e}")
        return 1

def run_normal_draft_helper():
    """Run the normal draft helper"""
    script_dir = Path(__file__).parent
    draft_dir = script_dir / "draft_helper"

    # Change to the draft directory and run the script
    original_cwd = os.getcwd()

    try:
        os.chdir(draft_dir)

        # Run the draft helper script with the same Python executable
        result = subprocess.run([
            sys.executable,
            "draft_helper.py"
        ], check=True)

        return result.returncode

    except subprocess.CalledProcessError as e:
        print(f"Error running draft helper: {e}")
        return e.returncode
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1
    finally:
        os.chdir(original_cwd)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Draft Helper or Simulation Analysis')
    parser.add_argument('--simulate', action='store_true',
                       help='Run draft simulation analysis instead of normal draft helper')

    args = parser.parse_args()

    if args.simulate:
        exit_code = run_simulation()
    else:
        exit_code = run_normal_draft_helper()

    sys.exit(exit_code)