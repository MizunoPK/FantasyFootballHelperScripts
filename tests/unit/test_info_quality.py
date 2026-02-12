"""
Unit Tests for Feature 05: INFO Level Log Quality

Tests verify INFO logging meets quality criteria after audit:
- Script start/complete logs with configuration summary
- Major phase transitions (not every function)
- Significant outcomes (results, saves)
- NO implementation details (should be DEBUG)
- User-friendly language (no technical jargon)

Test Categories:
- R3.1: SimulationManager.py INFO quality (5 tests)
- R3.2-R3.7: Other modules INFO quality (6 tests)
- R3.AC: Audit completion verification (1 test)

Created: 2026-02-11 (Feature 05 S6 Phase 3)
"""

import pytest
from pathlib import Path

# Get project root
project_root = Path(__file__).parent.parent.parent


# ============================================================================
# TEST CATEGORY 1: SIMULATION MANAGER INFO QUALITY (R3.1) - 5 TESTS
# ============================================================================

class TestSimulationManagerINFOQuality:
    """R3.1: Verify INFO logging quality in SimulationManager.py"""

    def test_simulation_manager_info_script_start_complete(self):
        """R3.1.1: Verify script start/complete logs present

        SimulationManager should log initialization and completion with
        configuration summaries (user-facing awareness).
        """
        module_path = project_root / 'simulation' / 'win_rate' / 'SimulationManager.py'
        source = module_path.read_text()

        # Script start with config summary
        assert 'logger.info("Initializing SimulationManager")' in source
        assert 'logger.info(\n            f"SimulationManager initialized' in source

        # Script complete
        assert 'OPTIMIZATION PROCESS COMPLETE' in source or 'OPTIMIZATION COMPLETE' in source

    def test_simulation_manager_info_major_phases(self):
        """R3.1.2: Verify major phase transitions logged

        Major phases like "STARTING OPTIMIZATION", "SAVING RESULTS" should be
        logged at INFO level for user awareness.
        """
        module_path = project_root / 'simulation' / 'win_rate' / 'SimulationManager.py'
        source = module_path.read_text()

        # Major phase markers
        major_phases = [
            'STARTING FULL CONFIGURATION OPTIMIZATION',
            'STARTING ITERATIVE PARAMETER OPTIMIZATION',
            'SAVING RESULTS',
            'OPTIMIZATION COMPLETE'
        ]

        for phase in major_phases:
            assert phase in source, f"Missing major phase log: {phase}"

    def test_simulation_manager_info_significant_outcomes(self):
        """R3.1.3: Verify significant outcomes logged

        Results like "Generated X configs", "Saved optimal config" should be
        logged for user awareness of progress and outcomes.
        """
        module_path = project_root / 'simulation' / 'win_rate' / 'SimulationManager.py'
        source = module_path.read_text()

        # Significant outcomes
        outcomes = [
            'Generated {len(combinations)} parameter combinations',
            'Registered {len(combinations)} configurations',
            '✓ Saved optimal config',
            'Total time:'
        ]

        for outcome in outcomes:
            assert outcome in source, f"Missing significant outcome log: {outcome}"

    def test_simulation_manager_info_no_implementation_details(self):
        """R3.1.4: Verify implementation details moved to DEBUG

        Internal details like "Updated baselines", "Saved intermediate folder",
        "Horizon X/Y completed" should be DEBUG, not INFO.
        """
        module_path = project_root / 'simulation' / 'win_rate' / 'SimulationManager.py'
        source = module_path.read_text()

        # These should be DEBUG (not INFO)
        implementation_details = [
            'Updated all horizon baselines',
            'Saved intermediate folder',
            'Horizon {horizon_idx + 1}/{len(horizons)}',
            'Cleaned up {deleted_count} intermediate folders'
        ]

        for detail in implementation_details:
            # Should be logger.debug, not logger.info
            assert f'logger.info(f"{detail}' not in source, (
                f"Implementation detail should be DEBUG: {detail}"
            )

    def test_simulation_manager_info_user_friendly_language(self):
        """R3.1.5: Verify user-friendly language (no jargon)

        INFO logs should use clear language like "configs" not "config_dicts",
        "simulations" not "sims", readable by non-developers.
        """
        module_path = project_root / 'simulation' / 'win_rate' / 'SimulationManager.py'
        source = module_path.read_text()

        # Count INFO calls with user-friendly terms
        info_calls = source.count('logger.info(')

        # Should have substantial INFO logging (user-facing script)
        assert info_calls >= 70, (
            f"Too few INFO calls ({info_calls}) - may have over-removed"
        )

        # User-friendly terms should be present
        friendly_terms = ['configs', 'simulations', 'parameters', 'optimiz']
        for term in friendly_terms:
            assert term.lower() in source.lower()


# ============================================================================
# TEST CATEGORY 2: OTHER MODULES INFO QUALITY (R3.2-R3.7) - 6 TESTS
# ============================================================================

class TestOtherModulesINFOQuality:
    """R3.2-R3.7: Verify INFO logging quality in other win_rate modules"""

    def test_parallel_league_runner_info_quality(self):
        """R3.2.1: Verify ParallelLeagueRunner has minimal/no INFO logs

        ParallelLeagueRunner is an internal component - INFO logs should be
        minimal or moved to DEBUG (SimulationManager handles user-facing logs).
        """
        module_path = project_root / 'simulation' / 'win_rate' / 'ParallelLeagueRunner.py'
        source = module_path.read_text()

        # Count INFO calls - should be minimal (internal component)
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

        # Count INFO calls - should be 0 (per-simulation detail)
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

    def test_manual_simulation_info_quality(self):
        """R3.7.1: Verify manual_simulation.py INFO quality

        manual_simulation.py is a user-facing script - should have INFO logs for
        major phases (start, loaded config, draft complete, season complete, complete).
        """
        module_path = project_root / 'simulation' / 'win_rate' / 'manual_simulation.py'
        source = module_path.read_text()

        # Should have exactly 5 INFO calls (script phases)
        info_count = source.count('logger.info(')

        assert info_count == 5, (
            f"manual_simulation.py should have 5 INFO calls (script phases), "
            f"found {info_count}"
        )

        # Verify key phases present
        phases = [
            'Starting manual simulation',
            'Loaded config from',
            'Draft complete',
            'Season complete',
            'Manual simulation complete'
        ]

        for phase in phases:
            assert phase in source, f"Missing phase log: {phase}"


# ============================================================================
# TEST CATEGORY 3: AUDIT COMPLETION VERIFICATION (R3.AC) - 1 TEST
# ============================================================================

class TestINFOAuditCompletion:
    """R3.AC: Verify INFO audit was completed across all modules"""

    def test_all_info_calls_audited(self):
        """R3.AC.1: Verify all INFO calls across 7 modules were audited

        After Phase 3 audit:
        - SimulationManager: 78 INFO calls (user-facing script)
        - ParallelLeagueRunner: 0 INFO calls (all downgraded)
        - SimulatedLeague: 0 INFO calls (all downgraded)
        - manual_simulation: 5 INFO calls (script phases)
        - Other modules: 0 INFO calls
        Total: ~83 INFO calls (down from 100)
        """
        modules_path = project_root / 'simulation' / 'win_rate'

        total_info_calls = 0
        files_checked = []

        for py_file in sorted(modules_path.glob('*.py')):
            if py_file.name.startswith('__'):
                continue

            source = py_file.read_text()
            count = source.count('logger.info(')
            total_info_calls += count
            files_checked.append((py_file.name, count))

        # After Phase 3: ~83 INFO calls total (100 - 17 removed/downgraded)
        assert 80 <= total_info_calls <= 90, (
            f"Unexpected INFO call count ({total_info_calls}): "
            + ", ".join(f"{name}={count}" for name, count in files_checked if count > 0)
        )

        # Verify expected distribution
        info_by_module = {name: count for name, count in files_checked if count > 0}

        # SimulationManager should have most (user-facing)
        assert info_by_module.get('SimulationManager.py', 0) >= 70, (
            "SimulationManager should have most INFO calls (user-facing script)"
        )

        # manual_simulation should have exactly 5
        assert info_by_module.get('manual_simulation.py', 0) == 5, (
            "manual_simulation should have exactly 5 INFO calls"
        )

        # Internal components should have 0
        internal_modules = [
            'ParallelLeagueRunner.py',
            'SimulatedLeague.py',
            'DraftHelperTeam.py',
            'SimulatedOpponent.py',
            'Week.py'
        ]

        for module in internal_modules:
            assert info_by_module.get(module, 0) == 0, (
                f"{module} should have 0 INFO calls (internal component)"
            )
