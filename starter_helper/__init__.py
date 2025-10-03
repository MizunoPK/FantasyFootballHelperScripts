"""
Starter Helper Package

Fantasy football starting lineup optimizer.
"""

__version__ = "1.0.0"

# Import main classes and all module-level attributes for package-level access
# This ensures tests can patch 'starter_helper.ATTR' regardless of whether
# starter_helper is imported as a package or module
try:
    from .starter_helper import *
    from .starter_helper import StarterHelper, main
except ImportError:
    # Fallback for when running as script
    pass
