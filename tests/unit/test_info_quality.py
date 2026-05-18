"""
Unit Tests for Feature 05: INFO Level Log Quality

Tests verify INFO logging meets quality criteria after audit:
- Script start/complete logs with configuration summary
- Major phase transitions (not every function)
- Significant outcomes (results, saves)
- NO implementation details (should be DEBUG)
- User-friendly language (no technical jargon)

Test Categories:
- R3.2-R3.7: Other modules INFO quality (5 tests)

Created: 2026-02-11 (Feature 05 S6 Phase 3)
"""

import pytest
from pathlib import Path

project_root = Path(__file__).parent.parent.parent


class TestOtherModulesINFOQuality:
    """R3.2-R3.7: Verify INFO logging quality in other win_rate modules"""

    def test_parallel_league_runner_info_quality(self):
        """R3.2.1: Verify ParallelLeagueRunner has minimal/no INFO logs

        ParallelLeagueRunner is an internal component - INFO logs should be
        minimal or moved to DEBUG (SimulationManager handles user-facing logs).
        """
        module_path = project_root / 'simulation' / 'win_rate' / 'ParallelLeagueRunner.py'
        source = module_path.read_text()

        info_count = source.count('logger.info(')

        assert info_count == 0, (
            f"ParallelLeagueRunner should have no INFO calls (internal component), "
            f"found {info_count}"
        )

    def test_simulated_league_info_quality(self):
        """R3.3.1: Verify SimulatedLeague has minimal/no INFO logs

        SimulatedLeague runs per-simulation - INFO logs would spam the console.
        Results should be logged at DEBUG, aggregates at INFO (by manager).
        """
        module_path = project_root / 'simulation' / 'win_rate' / 'SimulatedLeague.py'
        source = module_path.read_text()

        info_count = source.count('logger.info(')

        assert info_count == 0, (
            f"SimulatedLeague should have no INFO calls (per-simulation detail), "
            f"found {info_count}"
        )

    def test_draft_helper_team_info_quality(self):
        """R3.4.1: Verify DraftHelperTeam has no INFO logs

        DraftHelperTeam is internal simulation component - no user-facing INFO.
        """
        module_path = project_root / 'simulation' / 'win_rate' / 'DraftHelperTeam.py'
        source = module_path.read_text()

        info_count = source.count('logger.info(')
        assert info_count == 0, f"DraftHelperTeam should have 0 INFO calls, found {info_count}"

    def test_simulated_opponent_info_quality(self):
        """R3.5.1: Verify SimulatedOpponent has no INFO logs

        SimulatedOpponent is internal simulation component - no user-facing INFO.
        """
        module_path = project_root / 'simulation' / 'win_rate' / 'SimulatedOpponent.py'
        source = module_path.read_text()

        info_count = source.count('logger.info(')
        assert info_count == 0, f"SimulatedOpponent should have 0 INFO calls, found {info_count}"

    def test_week_info_quality(self):
        """R3.6.1: Verify Week has no INFO logs

        Week is internal simulation component - no user-facing INFO.
        """
        module_path = project_root / 'simulation' / 'win_rate' / 'Week.py'
        source = module_path.read_text()

        info_count = source.count('logger.info(')
        assert info_count == 0, f"Week should have 0 INFO calls, found {info_count}"
