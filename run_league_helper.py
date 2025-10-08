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

DATA_FOLDER = "./data"


def run_league_helper():
    """Run the league helper"""
    script_dir = Path(__file__).parent
    league_helper_dir = script_dir / "league_helper"
    league_helper_script = league_helper_dir / "LeagueHelperManager.py"

    try:
        # Run the league helper script with DATA_FOLDER as argument
        result = subprocess.run([
            sys.executable,
            str(league_helper_script),
            DATA_FOLDER
        ], check=True)

        return result.returncode

    except subprocess.CalledProcessError as e:
        print(f"Error running league helper: {e}")
        return e.returncode
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    exit_code = run_league_helper()
    sys.exit(exit_code)