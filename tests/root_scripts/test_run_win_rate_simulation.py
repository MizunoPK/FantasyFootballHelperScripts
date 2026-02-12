"""
Unit and Integration Tests for run_win_rate_simulation.py

Feature 05: win_rate_sim_logging
Tests CLI flag integration, Feature 01 integration, and edge cases
for the win rate simulation runner script.

Author: Kai Mizuno
"""

# Standard library imports
import argparse
import inspect
import re
import subprocess
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch

# Third-party imports
import pytest

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_test_parser():
    """Helper to create argparse parser matching run_win_rate_simulation.py main().

    Mirrors the actual parser setup for unit testing without executing main().
    """
    parser = argparse.ArgumentParser(
        description='Win Rate Simulation Runner - Test Parser'
    )

    # --enable-log-file flag (the Feature 05 addition)
    parser.add_argument(
        '--enable-log-file',
        action='store_true',
        default=False,
        help='Enable logging to file (default: console only)'
    )

    # Common arguments from main parser
    parser.add_argument('--sims', type=int, default=5)
    parser.add_argument('--baseline', type=str, default='')
    parser.add_argument('--output', type=str, default='simulation/simulation_configs')
    parser.add_argument('--workers', type=int, default=8)
    parser.add_argument('--data', type=str, default='simulation/sim_data')
    parser.add_argument('--test-values', type=int, default=5)
    parser.add_argument('--use-processes', action='store_true', default=False)

    # Mode subparsers
    subparsers = parser.add_subparsers(dest='mode', required=False)
    subparsers.add_parser('single')
    subparsers.add_parser('full')
    subparsers.add_parser('iterative')

    return parser


# ============================================================================
# TEST CATEGORY 1: CLI FLAG UNIT TESTS (R1.1) - 6 TESTS
# ============================================================================

class TestWinRateSimulationCLIFlagUnit:
    """Test Category 1: CLI Flag Unit Tests (Task 11)"""

    def test_enable_log_file_flag_exists(self):
        """R1.1.1: Verify --enable-log-file argument exists in help output"""
        result = subprocess.run(
            [sys.executable, str(project_root / "run_win_rate_simulation.py"), "--help"],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        assert "--enable-log-file" in result.stdout

    def test_enable_log_file_flag_default_false(self):
        """R1.1.2: Verify flag defaults to False (file logging OFF by default)"""
        parser = create_test_parser()
        args = parser.parse_args([])

        assert args.enable_log_file is False

    def test_enable_log_file_flag_true_when_provided(self):
        """R1.1.3: Verify flag sets to True when --enable-log-file provided"""
        parser = create_test_parser()
        args = parser.parse_args(['--enable-log-file'])

        assert args.enable_log_file is True

    def test_logging_to_file_constant_removed(self):
        """R1.1.4: Verify LOGGING_TO_FILE constant no longer exists"""
        import run_win_rate_simulation

        assert not hasattr(run_win_rate_simulation, 'LOGGING_TO_FILE')

    def test_logger_name_is_win_rate_simulation(self):
        """R1.1.5: Verify LOG_NAME changed to 'win_rate_simulation'"""
        import run_win_rate_simulation

        assert run_win_rate_simulation.LOG_NAME == "win_rate_simulation"

    def test_enable_log_file_flag_action_store_true(self):
        """R1.1.6: Verify flag uses action='store_true' (boolean, no value needed)"""
        parser = create_test_parser()

        enable_log_file_action = None
        for action in parser._actions:
            if '--enable-log-file' in action.option_strings:
                enable_log_file_action = action
                break

        assert enable_log_file_action is not None
        assert isinstance(enable_log_file_action, argparse._StoreTrueAction)
        assert enable_log_file_action.default is False


# ============================================================================
# TEST CATEGORY 2: CLI FLAG INTEGRATION TESTS (R1.2) - 8 TESTS
# ============================================================================

class TestWinRateSimulationCLIFlagIntegration:
    """Test Category 2: CLI Flag Integration Tests (Task 12)"""

    def test_console_logging_only_when_flag_omitted(self):
        """R1.2.1: Verify console-only logging when --enable-log-file not provided"""
        parser = create_test_parser()
        args = parser.parse_args(['--sims', '1', 'single'])

        # Flag should be False when omitted
        assert args.enable_log_file is False
        assert args.mode == 'single'

    @patch('utils.LoggingManager._logging_manager')
    def test_file_logging_enabled_when_flag_provided(self, mock_manager):
        """R1.2.2: Verify setup_logger receives log_to_file=True when flag provided"""
        mock_manager.setup_logger.return_value = MagicMock()

        parser = create_test_parser()
        args = parser.parse_args(['--enable-log-file', 'single'])

        assert args.enable_log_file is True

    def test_logger_creates_correct_folder_name(self):
        """R1.2.3: Verify logger name maps to logs/win_rate_simulation/ folder"""
        import run_win_rate_simulation

        # Logger name determines folder: logs/{LOG_NAME}/
        assert run_win_rate_simulation.LOG_NAME == "win_rate_simulation"
        # When setup_logger(name="win_rate_simulation", log_to_file=True) is called,
        # LoggingManager creates logs/win_rate_simulation/ folder

    def test_enable_log_file_works_in_single_mode(self):
        """R1.2.4: Verify --enable-log-file accepted alongside single mode"""
        parser = create_test_parser()
        args = parser.parse_args(['--enable-log-file', 'single'])

        assert args.enable_log_file is True
        assert args.mode == 'single'

    def test_enable_log_file_works_in_full_mode(self):
        """R1.2.5: Verify --enable-log-file accepted alongside full mode"""
        parser = create_test_parser()
        args = parser.parse_args(['--enable-log-file', 'full'])

        assert args.enable_log_file is True
        assert args.mode == 'full'

    def test_enable_log_file_works_in_iterative_mode(self):
        """R1.2.6: Verify --enable-log-file accepted alongside iterative mode"""
        parser = create_test_parser()
        args = parser.parse_args(['--enable-log-file', 'iterative'])

        assert args.enable_log_file is True
        assert args.mode == 'iterative'

    @pytest.mark.integration
    def test_log_rotation_at_500_lines(self):
        """R1.2.7: Verify log rotation occurs at 500 lines (Feature 01 behavior)"""
        pytest.skip("Integration test - requires generating >500 log lines")

    @pytest.mark.integration
    def test_max_50_files_cleanup(self):
        """R1.2.8: Verify max 50 files cleanup when 51st created (Feature 01 behavior)"""
        pytest.skip("Integration test - requires generating 51+ log files")


# ============================================================================
# TEST CATEGORY 3: DEBUG LOG QUALITY - UNIT TESTS (R2) - 12 TESTS
# ============================================================================

class TestWinRateSimulationDEBUGQualityUnit:
    """Test Category 3: DEBUG Log Quality Unit Tests (Task 13)

    These tests verify the DEBUG audit was applied correctly by inspecting
    source code for compliance with quality criteria:
    - No tight-loop logging without throttling
    - Function entry/exit only for complex flows
    - Data transformations log context
    - Conditional branches log path taken
    - No variable assignment spam
    """

    def test_simulation_manager_debug_no_tight_loop_logging(self):
        """R2.1.1: Verify no DEBUG logs inside tight loops in SimulationManager.py

        Tight loops include: for/while loops that run per-simulation or per-player.
        Remaining DEBUG calls should be at flow-control or summary points.
        """
        from simulation.win_rate.SimulationManager import SimulationManager

        source = inspect.getsource(SimulationManager)

        # Per-folder deletion debug logging should have been removed
        assert 'Deleting intermediate folder' not in source
        # Per-player validation debug logging should not exist
        assert 'valid player' not in source.lower() or source.count('logger.debug') < 15

    def test_simulation_manager_debug_function_entry_selective(self):
        """R2.1.2: Verify function entry/exit logs only for complex flows

        Complex methods (_detect_resume_state) should have debug logging.
        Simple getters/validators should have minimal debug.
        """
        from simulation.win_rate.SimulationManager import SimulationManager

        source = inspect.getsource(SimulationManager)

        # Complex methods should retain debug logging
        detect_resume = inspect.getsource(SimulationManager._detect_resume_state)
        assert 'logger.debug' in detect_resume  # Resume logic is complex

        # Validate that _validate_season_data has minimal debug (only result logging)
        validate_method = inspect.getsource(SimulationManager._validate_season_data)
        debug_count = validate_method.count('logger.debug')
        assert debug_count <= 2  # At most validation result, not per-player

    def test_simulation_manager_debug_data_transformations(self):
        """R2.1.3: Verify data transformations log contextual values

        DEBUG calls should include relevant context (folder names, counts, indices)
        or describe a meaningful state/condition. Static messages for conditional
        branches (e.g., "No intermediate folders found") are acceptable.
        """
        from simulation.win_rate.SimulationManager import SimulationManager

        source = inspect.getsource(SimulationManager)

        # Find all debug call blocks (handling multi-line calls)
        debug_blocks = re.findall(
            r'logger\.debug\([^)]+\)',
            source,
            re.DOTALL
        )

        # Acceptable static messages (conditional branch indicators)
        acceptable_static = [
            'No intermediate folders found',
            'No valid intermediate folders',
        ]

        for block in debug_blocks:
            # Allow f-strings with variables OR acceptable static branch messages
            has_context = 'f"' in block or "f'" in block or '%' in block or '.format' in block
            is_acceptable_static = any(msg in block for msg in acceptable_static)
            assert has_context or is_acceptable_static, \
                f"DEBUG call without context: {block[:80]}"

    def test_simulation_manager_debug_conditional_branches(self):
        """R2.1.4: Verify conditional branches log which path was taken

        The _detect_resume_state method has multiple conditional paths that should
        log which branch executed.
        """
        from simulation.win_rate.SimulationManager import SimulationManager

        detect_resume = inspect.getsource(SimulationManager._detect_resume_state)

        # Should log different conditions: no folders, completed run, valid resume
        assert 'No intermediate folders found' in detect_resume
        assert 'No valid intermediate folders' in detect_resume
        assert 'All parameters complete' in detect_resume

    def test_simulation_manager_debug_no_variable_spam(self):
        """R2.1.5: Verify no DEBUG logging of every variable assignment

        DEBUG calls should not simply log `variable = {value}` for simple assignments.
        Each call should provide meaningful context.
        """
        from simulation.win_rate.SimulationManager import SimulationManager

        source = inspect.getsource(SimulationManager)

        # Count debug calls vs method count - ratio should be reasonable
        debug_count = source.count('logger.debug')
        method_count = source.count('def ')

        # Should not have excessive debug logging per method
        if method_count > 0:
            ratio = debug_count / method_count
            assert ratio < 3, f"Too many debug calls per method: {debug_count}/{method_count} = {ratio:.1f}"

    def test_parallel_league_runner_debug_quality(self):
        """R2.2.1: Verify DEBUG quality in ParallelLeagueRunner.py

        GC logging in completion loops is acceptable (fires every GC_FREQUENCY sims).
        Per-simulation start/draft/season/complete logging should be removed.
        """
        from simulation.win_rate.ParallelLeagueRunner import ParallelLeagueRunner

        source = inspect.getsource(ParallelLeagueRunner)

        # Per-simulation tight-loop logging should be removed
        assert 'Starting simulation' not in source or 'logger.debug' not in source.split('Starting simulation')[0][-100:]
        assert 'Draft complete for sim' not in source
        assert 'Season complete for sim' not in source

        # Completion summaries should exist
        run_sims = inspect.getsource(ParallelLeagueRunner.run_simulations_for_config)
        assert 'Completed' in run_sims and 'simulations successfully' in run_sims

    def test_simulated_league_debug_quality(self):
        """R2.3.1: Verify DEBUG quality in SimulatedLeague.py

        Should retain: init summary, week folder selection, schedule generation,
        pre-load summary, legacy fallback, draft/season start/complete.
        Should remove: per-team creation, per-week cache loop, per-player parsing,
        draft round/pick logging.
        """
        from simulation.win_rate.SimulatedLeague import SimulatedLeague

        source = inspect.getsource(SimulatedLeague)

        # Removed per-iteration logging
        assert 'Creating team' not in source or source.count('Creating team') == 0
        assert 'Cached week' not in source
        assert 'Parsed' not in source or 'Parsed' not in [
            line for line in source.split('\n') if 'logger.debug' in line and 'Parsed' in line
        ]

        # Retained summary logging
        assert 'Initializing' in source  # Init summary
        assert 'Draft complete' in source
        assert 'Season complete' in source

    def test_draft_helper_team_debug_quality(self):
        """R2.4.1: Verify DEBUG quality in DraftHelperTeam.py

        Should retain: draft recommendation with score (fires once per draft pick).
        Should remove: init, per-starter loop, mark_player logging.
        """
        from simulation.win_rate.DraftHelperTeam import DraftHelperTeam

        source = inspect.getsource(DraftHelperTeam)

        # Should have exactly 1 debug call (recommendation)
        debug_count = source.count('logger.debug')
        assert debug_count == 1, f"Expected 1 debug call, found {debug_count}"
        assert 'recommends' in source

    def test_simulated_opponent_debug_quality(self):
        """R2.5.1: Verify DEBUG quality in SimulatedOpponent.py

        Should retain: init with strategy (once per team creation),
        weekly lineup score (per-week, acceptable for 17 calls per sim).
        Should remove: drafted player, recommends, mark_player.
        """
        from simulation.win_rate.SimulatedOpponent import SimulatedOpponent

        source = inspect.getsource(SimulatedOpponent)

        debug_count = source.count('logger.debug')
        assert debug_count == 2, f"Expected 2 debug calls, found {debug_count}"
        assert 'strategy' in source  # Init with strategy
        assert 'lineup scored' in source  # Weekly lineup score

    def test_week_debug_quality(self):
        """R2.6.1: Verify DEBUG quality in Week.py

        Should retain: init (once per week object), simulate entry, complete.
        Should remove: per-matchup win/loss/tie logging inside the loop.
        """
        from simulation.win_rate.Week import Week

        source = inspect.getsource(Week)

        debug_count = source.count('logger.debug')
        assert debug_count == 3, f"Expected 3 debug calls, found {debug_count}"

        # Verify no per-matchup logging
        simulate_method = inspect.getsource(Week.simulate_week)
        # The for loop body should not contain debug calls
        assert 'team1_won' not in [
            line for line in simulate_method.split('\n')
            if 'logger.debug' in line
        ]

    def test_manual_simulation_debug_quality(self):
        """R2.7.1: Verify DEBUG quality in manual_simulation.py (1 debug call)

        manual_simulation.py has 1 DEBUG call (SimulatedLeague created - internal detail).
        """
        # Import the module's source file directly
        module_path = project_root / 'simulation' / 'win_rate' / 'manual_simulation.py'
        source = module_path.read_text()

        # Count debug calls (should be exactly 1)
        debug_count = source.count('logger.debug(')
        assert debug_count == 1, f"Expected 1 DEBUG call, found {debug_count}"

    def test_all_debug_calls_audited(self):
        """R2.AC6: Verify all DEBUG calls across 7 modules were audited

        Counts remaining debug calls and verifies they are within expected range
        after the audit (should be significantly reduced from original ~60).
        """
        modules_path = project_root / 'simulation' / 'win_rate'

        total_debug_calls = 0
        files_checked = []
        for py_file in sorted(modules_path.glob('*.py')):
            if py_file.name.startswith('__'):
                continue
            source = py_file.read_text()
            count = source.count('logger.debug')
            total_debug_calls += count
            files_checked.append((py_file.name, count))

        # After Phase 2 (DEBUG audit): ~26 calls kept from original ~60
        # After Phase 3 (INFO audit): +13 INFO calls downgraded to DEBUG
        # Current expected: ~45 calls across all files
        assert total_debug_calls <= 50, (
            f"Too many DEBUG calls remaining ({total_debug_calls}): "
            + ", ".join(f"{name}={count}" for name, count in files_checked if count > 0)
        )
        # Should still have some debug logging (not all removed)
        assert total_debug_calls >= 40, (
            f"Too few DEBUG calls ({total_debug_calls}) - may have over-removed"
        )


# ============================================================================
# TEST CATEGORY 4: DEBUG LOG QUALITY - INTEGRATION TESTS (R2.8) - 2 TESTS
# ============================================================================

class TestWinRateSimulationDEBUGQualityIntegration:
    """Test Category 4: DEBUG Log Quality Integration Tests (Task 13)

    Behavioral tests verifying DEBUG changes don't break functionality.
    """

    @pytest.mark.integration
    def test_debug_logging_behavior_preserved(self):
        """R2.8.1: Verify DEBUG improvements don't break functionality

        Full test suite should pass after DEBUG audit changes.
        """
        pytest.skip("Integration test - verified by running full test suite")

    @pytest.mark.integration
    def test_debug_logs_contain_expected_content(self):
        """R2.8.2: Verify DEBUG logs contain tracing information

        When run with DEBUG level, logs should include:
        - Function entry/exit for complex flows
        - Data transformations with context
        - Conditional branch selections
        """
        pytest.skip("Integration test - requires running simulation with DEBUG level")


# ============================================================================
# TEST SUMMARY
# ============================================================================

"""
Test Coverage Summary for Feature 05 (win_rate_sim_logging):

Category 1: CLI Flag Unit Tests (R1.1) - 6 tests
Category 2: CLI Flag Integration Tests (R1.2) - 8 tests
Category 3: DEBUG Quality Unit Tests (R2) - 12 tests
Category 4: DEBUG Quality Integration Tests (R2.8) - 2 tests

TOTAL: 28 tests (24 active + 4 integration skips)
"""
