"""
Pytest configuration for Fantasy Football Helper Scripts tests.

This file ensures that pytest can properly import the league_helper modules.
The project uses relative imports that expect league_helper/util to be in the path.
"""

import sys
from pathlib import Path

# Add project root and league_helper/util to sys.path
# This matches how the application runs (from league_helper directory)
project_root = Path(__file__).parent.parent
league_helper_dir = project_root / "league_helper"

sys.path.insert(0, str(project_root))
sys.path.insert(0, str(league_helper_dir / "util"))
sys.path.insert(0, str(league_helper_dir))
