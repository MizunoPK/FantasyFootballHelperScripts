"""
Starter Helper Package

Fantasy football starting lineup optimizer.
"""

__version__ = "1.0.0"

# Import main classes for package-level access
try:
    from .starter_helper import StarterHelper, main
except ImportError:
    # Fallback for when running as script
    pass
