"""
Pytest configuration for Fantasy Football Helper Scripts tests.

Adds the project root to sys.path so pytest can import all project modules.
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent

sys.path.insert(0, str(project_root))
