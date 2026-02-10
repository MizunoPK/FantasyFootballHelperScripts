#!/usr/bin/env python3
"""
Runner Script for Player Data Fetcher

This script runs the player data fetcher from the parent directory.

Usage:
    python run_player_fetcher.py
    python run_player_fetcher.py --enable-log-file

Author: Kai Mizuno
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Run player data fetcher')
    parser.add_argument('--enable-log-file', action='store_true',
                        help='Enable file logging to logs/player_data_fetcher/')
    # Use parse_known_args to allow future flags to be forwarded without error
    args, unknown_args = parser.parse_known_args()

    # Get the directory where this script is located (project root)
    script_dir = Path(__file__).parent

    # Construct path to the player-data-fetcher module directory
    fetcher_dir = script_dir / "player-data-fetcher"

    # Save current working directory to restore later
    # We need to change directories because player_data_fetcher_main.py
    # expects to run from within its own directory
    original_cwd = os.getcwd()

    try:
        # Change to fetcher directory so relative paths work correctly
        os.chdir(fetcher_dir)

        # Run the data fetcher script with the same Python executable
        # Forward ALL command-line arguments via sys.argv[1:]
        # check=True raises CalledProcessError if script exits with non-zero code
        result = subprocess.run([
            sys.executable,                    # Current Python interpreter path
            "player_data_fetcher_main.py"      # Main script in fetcher directory
        ] + sys.argv[1:], check=True)  # Forward all args (Task 2)

    except subprocess.CalledProcessError as e:
        # Script exited with non-zero code - print error and exit with that code
        print(f"Error running player data fetcher: {e}")
        sys.exit(e.returncode)
    except Exception as e:
        # Unexpected error (e.g., directory not found, permission denied)
        print(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        # Always restore original working directory, even if script fails
        # This ensures we don't leave the process in an unexpected state
        os.chdir(original_cwd)