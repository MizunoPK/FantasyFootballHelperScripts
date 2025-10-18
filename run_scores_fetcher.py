#!/usr/bin/env python3
"""
Runner Script for NFL Scores Fetcher

This script runs the NFL scores fetcher from the parent directory.

Usage:
    python run_nfl_scores_fetcher.py

Author: Kai Mizuno
"""

import os
import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    # Get the directory where this script is located (project root)
    script_dir = Path(__file__).parent

    # Construct path to the nfl-scores-fetcher module directory
    fetcher_dir = script_dir / "nfl-scores-fetcher"

    # Save current working directory to restore later
    # We need to change directories because nfl_scores_fetcher_main.py
    # expects to run from within its own directory
    original_cwd = os.getcwd()

    try:
        # Change to fetcher directory so relative paths work correctly
        os.chdir(fetcher_dir)

        # Run the NFL scores fetcher script with the same Python executable
        # check=True raises CalledProcessError if script exits with non-zero code
        result = subprocess.run([
            sys.executable,                    # Current Python interpreter path
            "nfl_scores_fetcher_main.py"       # Main script in fetcher directory
        ], check=True)

    except subprocess.CalledProcessError as e:
        # Script exited with non-zero code - print error and exit with that code
        print(f"Error running NFL scores fetcher: {e}")
        sys.exit(e.returncode)
    except Exception as e:
        # Unexpected error (e.g., directory not found, permission denied)
        print(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        # Always restore original working directory, even if script fails
        # This ensures we don't leave the process in an unexpected state
        os.chdir(original_cwd)