#!/usr/bin/env python3
"""
Runner Script for League Helper

This script runs the league helper from the parent directory.

Usage:
    python run_league_helper.py

Author: Kai Mizuno
"""

import subprocess
import sys
from pathlib import Path

# Default data folder for league helper (contains CSV files and configurations)
DATA_FOLDER = "./data"


def run_league_helper():
    """
    Run the league helper application.

    Executes the LeagueHelperManager.py script from the league_helper directory
    with the configured data folder as an argument.

    Returns:
        int: Exit code from the league helper subprocess (0 = success, non-zero = error)

    Raises:
        subprocess.CalledProcessError: If league helper exits with non-zero code
        Exception: For unexpected errors (file not found, permission denied, etc.)
    """
    # Get the directory where this script is located (project root)
    script_dir = Path(__file__).parent

    # Construct path to league_helper module directory
    league_helper_dir = script_dir / "league_helper"

    # Construct path to the main LeagueHelperManager script
    league_helper_script = league_helper_dir / "LeagueHelperManager.py"

    try:
        # Run the league helper script with DATA_FOLDER as argument
        # Uses sys.executable to ensure same Python interpreter is used
        # check=True raises CalledProcessError if script exits with non-zero code
        result = subprocess.run([
            sys.executable,              # Current Python interpreter path
            str(league_helper_script),   # Path to LeagueHelperManager.py
            DATA_FOLDER                  # Data folder argument
        ], check=True)

        # Return the exit code from the subprocess (0 = success)
        return result.returncode

    except subprocess.CalledProcessError as e:
        # Script exited with non-zero code - print error and return that code
        print(f"Error running league helper: {e}")
        return e.returncode
    except Exception as e:
        # Unexpected error (e.g., script not found, permission denied)
        print(f"Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    # Execute league helper and exit with its return code
    exit_code = run_league_helper()
    sys.exit(exit_code)