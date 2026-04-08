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

project_root = Path(__file__).parent.parent.parent



class TestINFOLogBehavior:
    """R3.8: Verify INFO logging behavior after quality improvements"""

    def test_info_logging_behavior_preserved(self):
        """R3.8.1: Verify modules can be imported after INFO changes

        After INFO quality audit (13 calls downgraded/removed), the win_rate
        simulation modules should still be importable and functional. This
        verifies no syntax errors or import regressions from log changes.
        """

        try:
            from simulation.win_rate.SimulationManager import SimulationManager
            from simulation.win_rate.ParallelLeagueRunner import ParallelLeagueRunner
            from simulation.win_rate.SimulatedLeague import SimulatedLeague
            from simulation.win_rate.DraftHelperTeam import DraftHelperTeam
            from simulation.win_rate.SimulatedOpponent import SimulatedOpponent
            from simulation.win_rate.Week import Week
        except Exception as e:
            raise AssertionError(
                f"Module import failed after INFO changes: {e}"
            )

        assert SimulationManager is not None, (
            "SimulationManager class not found"
        )
        assert ParallelLeagueRunner is not None, (
            "ParallelLeagueRunner class not found"
        )

    def test_info_logs_contain_user_friendly_content(self):
        """R3.8.2: Verify INFO logs contain user-friendly content

        INFO logs should use clear, non-technical language readable by users
        who aren't developers. Verify key user-facing messages are present.
        """
        sim_manager_path = project_root / 'simulation' / 'win_rate' / 'SimulationManager.py'
        source = sim_manager_path.read_text()

        user_friendly_phrases = [
            'Initializing SimulationManager',
            'initialized:',

            'STARTING',
            'COMPLETE',
            'SAVING',

            'Generated',
            'Registered',
            'configurations',
            'simulations',
            'parameters',

            'Saved optimal',
            'Total time:',
            'Win Rate:',

            'workers',
            'configs'
        ]

        for phrase in user_friendly_phrases:
            assert phrase in source, (
                f"User-friendly phrase missing from INFO logs: {phrase}"
            )

        technical_jargon = [
            'logger.info(f"Updated all horizon baselines',  # Implementation detail
            'logger.info(f"Saved intermediate folder',  # Internal checkpoint
            'logger.info(f"Cleaned up {deleted_count} intermediate',  # Internal cleanup
        ]

        for jargon in technical_jargon:
            assert jargon not in source, (
                f"Technical jargon should be DEBUG, not INFO: {jargon}"
            )

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


