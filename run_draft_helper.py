#!/usr/bin/env python3
"""
Runner Script for Draft Helper

This script runs the draft helper from the parent directory.

Usage:
    python run_draft_helper.py

Author: Generated for NFL Fantasy Data Collection
Last Updated: September 2025
"""

import os
import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    # Get the path to the draft_helper directory
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
        
    except subprocess.CalledProcessError as e:
        print(f"Error running draft helper: {e}")
        sys.exit(e.returncode)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        os.chdir(original_cwd)