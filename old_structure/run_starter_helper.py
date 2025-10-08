#!/usr/bin/env python3
"""
Runner Script for Starter Helper

This script runs the starter helper from the parent directory.

Usage:
    python run_starter_helper.py

Author: Generated for NFL Fantasy Data Collection
Last Updated: September 2025
"""

import os
import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    # Get the path to the starter_helper directory
    script_dir = Path(__file__).parent
    starter_dir = script_dir / "starter_helper"

    # Change to the starter directory and run the script
    original_cwd = os.getcwd()

    try:
        os.chdir(starter_dir)

        # Run the starter helper script with the same Python executable
        result = subprocess.run([
            sys.executable,
            "starter_helper.py"
        ], check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error running starter helper: {e}")
        sys.exit(e.returncode)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        os.chdir(original_cwd)