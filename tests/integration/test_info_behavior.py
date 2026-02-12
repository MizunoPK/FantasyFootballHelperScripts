"""
Integration Tests for Feature 05: INFO Level Log Behavior

Tests verify INFO logging works correctly after audit:
- Test suite still passes after INFO message changes
- INFO logs contain expected user-friendly content

Test Categories:
- R3.8.1: Regression testing (test suite passes)
- R3.8.2: Content verification (user-friendly messages)

Created: 2026-02-11 (Feature 05 S6 Phase 3)
"""

import pytest
from pathlib import Path

# Get project root
project_root = Path(__file__).parent.parent.parent


# ============================================================================
# INFO LOG BEHAVIOR INTEGRATION TESTS (R3.8) - 2 TESTS
# ============================================================================

class TestINFOLogBehavior:
    """R3.8: Verify INFO logging behavior after quality improvements"""

    def test_info_logging_behavior_preserved(self):
        """R3.8.1: Verify modules can be imported after INFO changes

        After INFO quality audit (13 calls downgraded/removed), the win_rate
        simulation modules should still be importable and functional. This
        verifies no syntax errors or import regressions from log changes.
        """
        # Verify all win_rate modules can be imported successfully
        # (INFO changes should not break module loading)
        import sys
        from pathlib import Path

        # Add simulation/win_rate to path
        win_rate_path = project_root / 'simulation' / 'win_rate'
        if str(win_rate_path) not in sys.path:
            sys.path.insert(0, str(win_rate_path))

        # Import key modules (will fail if syntax errors from INFO changes)
        try:
            import SimulationManager
            import ParallelLeagueRunner
            import SimulatedLeague
            import DraftHelperTeam
            import SimulatedOpponent
            import Week
        except Exception as e:
            raise AssertionError(
                f"Module import failed after INFO changes: {e}"
            )

        # Verify modules have expected classes
        assert hasattr(SimulationManager, 'SimulationManager'), (
            "SimulationManager class not found"
        )
        assert hasattr(ParallelLeagueRunner, 'ParallelLeagueRunner'), (
            "ParallelLeagueRunner class not found"
        )

    def test_info_logs_contain_user_friendly_content(self):
        """R3.8.2: Verify INFO logs contain user-friendly content

        INFO logs should use clear, non-technical language readable by users
        who aren't developers. Verify key user-facing messages are present.
        """
        # Check SimulationManager for user-friendly INFO messages
        sim_manager_path = project_root / 'simulation' / 'win_rate' / 'SimulationManager.py'
        source = sim_manager_path.read_text()

        # User-friendly phrases that should be in INFO logs
        user_friendly_phrases = [
            # Initialization and setup
            'Initializing SimulationManager',
            'initialized:',

            # Major phases (not implementation details)
            'STARTING',
            'COMPLETE',
            'SAVING',

            # Progress and results
            'Generated',
            'Registered',
            'configurations',
            'simulations',
            'parameters',

            # Outcomes
            'Saved optimal',
            'Total time:',
            'Win Rate:',

            # Configuration summary
            'workers',
            'configs'
        ]

        for phrase in user_friendly_phrases:
            assert phrase in source, (
                f"User-friendly phrase missing from INFO logs: {phrase}"
            )

        # Technical jargon that should NOT be in INFO logs
        # (should be in DEBUG or removed entirely)
        technical_jargon = [
            'logger.info(f"Updated all horizon baselines',  # Implementation detail
            'logger.info(f"Saved intermediate folder',  # Internal checkpoint
            'logger.info(f"Cleaned up {deleted_count} intermediate',  # Internal cleanup
        ]

        for jargon in technical_jargon:
            assert jargon not in source, (
                f"Technical jargon should be DEBUG, not INFO: {jargon}"
            )

        # Verify manual_simulation.py has user-friendly script phases
        manual_sim_path = project_root / 'simulation' / 'win_rate' / 'manual_simulation.py'
        manual_source = manual_sim_path.read_text()

        script_phases = [
            'Starting manual simulation',
            'Loaded config',
            'Draft complete',
            'Season complete',
            'complete'
        ]

        for phase in script_phases:
            assert phase in manual_source, (
                f"User-friendly script phase missing: {phase}"
            )
