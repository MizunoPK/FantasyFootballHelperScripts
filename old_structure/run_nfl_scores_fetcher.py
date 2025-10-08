#!/usr/bin/env python3
"""
Runner Script for NFL Scores Fetcher

This script runs the NFL scores fetcher from the parent directory.

Usage:
    python run_nfl_scores_fetcher.py

Author: Generated for NFL Fantasy Data Collection
Last Updated: September 2025
"""

import os
import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    # Get the path to the nfl-scores-fetcher directory
    script_dir = Path(__file__).parent
    fetcher_dir = script_dir / "nfl-scores-fetcher"
    
    # Change to the fetcher directory and run the script
    original_cwd = os.getcwd()
    
    try:
        os.chdir(fetcher_dir)
        
        # Run the NFL scores fetcher script with the same Python executable
        result = subprocess.run([
            sys.executable, 
            "data_fetcher-scores.py"
        ], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Error running NFL scores fetcher: {e}")
        sys.exit(e.returncode)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        os.chdir(original_cwd)