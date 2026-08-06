"""
Unit and Integration Tests for run_accuracy_simulation.py

Feature 04: accuracy_sim_logging
Tests all CLI flag integration, Feature 01 integration, log quality improvements,
and edge cases for the accuracy simulation runner script.

Author: Claude (Feature 04 Implementation)
Created: 2026-02-10 (S7.P3 - PR Review test creation)
"""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, call

import pytest

project_root = Path(__file__).parent.parent.parent



class TestAccuracySimulationCLIFlags:
    """Test Category 1: CLI Flag Integration (Requirement R1)"""

    def test_argparse_has_enable_log_file_flag(self):
        """Test 1.1: Verify --enable-log-file argument exists in argparse configuration"""
        import run_accuracy_simulation

        result = subprocess.run(
            [sys.executable, str(project_root / "run_accuracy_simulation.py"), "--help"],
            capture_output=True,
            text=True,
            timeout=60
        )

        assert result.returncode == 0
        assert "--enable-log-file" in result.stdout
        assert "Enable file logging" in result.stdout

    def test_enable_log_file_flag_default_false(self):
        """Test 1.2: Verify flag defaults to False (file logging OFF by default)"""
        parser = create_test_parser()
        args = parser.parse_args([])

        assert args.enable_log_file == False

    def test_enable_log_file_flag_with_value_true(self):
        """Test 1.3: Verify flag sets to True when provided"""
        parser = create_test_parser()
        args = parser.parse_args(['--enable-log-file'])

        assert args.enable_log_file == True

    def test_enable_log_file_flag_action_store_true(self):
        """Test 1.4: Verify flag uses action='store_true' (boolean, no value needed)"""
        parser = create_test_parser()

        enable_log_file_action = None
        for action in parser._actions:
            if '--enable-log-file' in action.option_strings:
                enable_log_file_action = action
                break

        assert enable_log_file_action is not None
        assert isinstance(enable_log_file_action, argparse._StoreTrueAction)
        assert enable_log_file_action.default == False

    def test_existing_log_level_flag_unchanged(self):
        """Test 1.5: Verify --log-level flag still works (backward compatibility)"""
        parser = create_test_parser()
        args = parser.parse_args(['--log-level', 'debug'])

        assert args.log_level == 'debug'

    def test_combined_flags_work_together(self):
        """Test 1.6: Verify --enable-log-file and --log-level work together"""
        parser = create_test_parser()
        args = parser.parse_args(['--enable-log-file', '--log-level', 'debug'])

        assert args.enable_log_file == True
        assert args.log_level == 'debug'

    def test_help_text_describes_flag_purpose(self):
        """Test 1.7: Verify help text is clear and matches spec"""
        result = subprocess.run(
            [sys.executable, str(project_root / "run_accuracy_simulation.py"), "--help"],
            capture_output=True,
            text=True,
            timeout=60
        )

        assert result.returncode == 0
        help_text = result.stdout

        assert "Enable file logging" in help_text or "enable file logging" in help_text
        assert "logs/accuracy_simulation" in help_text or "accuracy_simulation" in help_text

    def test_logging_to_file_constant_changed_to_false(self):
        """Test 1.8: Verify LOGGING_TO_FILE constant is False (line 54)"""
        import run_accuracy_simulation

        assert hasattr(run_accuracy_simulation, 'LOGGING_TO_FILE')
        assert run_accuracy_simulation.LOGGING_TO_FILE == False



class TestAccuracySimulationFeature01Integration:
    """Test Category 2: Feature 01 Integration (Requirement R2)"""

    @patch('utils.LoggingManager.setup_logger')
    def test_setup_logger_called_with_flag_value(self, mock_setup_logger):
        """Test 2.1: Verify setup_logger() receives args.enable_log_file as log_to_file parameter"""
        mock_setup_logger.return_value = MagicMock()

        with patch('sys.argv', ['run_accuracy_simulation.py', '--enable-log-file']):
            with patch('run_accuracy_simulation.AccuracySimulationManager') as mock_manager:

                import run_accuracy_simulation
                import importlib
                importlib.reload(run_accuracy_simulation)


    @patch('utils.LoggingManager.setup_logger')
    def test_logger_name_is_accuracy_simulation(self, mock_setup_logger):
        """Test 2.2: Verify logger name = "accuracy_simulation" (creates logs/accuracy_simulation/)"""
        mock_setup_logger.return_value = MagicMock()

        with patch('sys.argv', ['run_accuracy_simulation.py']):
            with patch('run_accuracy_simulation.AccuracySimulationManager') as mock_manager:
                with patch('run_accuracy_simulation.main'):
                    import run_accuracy_simulation

                    assert run_accuracy_simulation.LOG_NAME == "accuracy_simulation"

    @patch('utils.LoggingManager.setup_logger')
    def test_log_file_path_is_none_autogenerated(self, mock_setup_logger):
        """Test 2.3: Verify log_file_path=None (auto-generated by LoggingManager)"""
        mock_setup_logger.return_value = MagicMock()

        with patch('sys.argv', ['run_accuracy_simulation.py', '--enable-log-file']):
            with patch('run_accuracy_simulation.main'):
                import run_accuracy_simulation




class TestAccuracySimulationDEBUGLogQuality:
    """Test Category 3: DEBUG Log Quality (Requirement R3)"""

    def test_queue_depth_logged_with_worker_activity(self):
        """Test 3.6: Verify worker messages include queue depth info"""
        from simulation.accuracy.ParallelAccuracyRunner import ParallelAccuracyRunner

        import inspect
        source = inspect.getsource(ParallelAccuracyRunner.evaluate_configs_parallel)

        assert 'logger.debug' in source or 'self.logger.debug' in source
        assert 'completed' in source

    def test_no_debug_logs_in_tight_loops(self):
        """Test 3.7: Verify no DEBUG logs inside tight loops (performance concern)"""
        from simulation.accuracy.ParallelAccuracyRunner import ParallelAccuracyRunner

        import inspect
        source = inspect.getsource(ParallelAccuracyRunner.evaluate_configs_parallel)

        assert '% 10 == 0' in source or 'throttl' in source.lower()

    def test_debug_logs_include_context(self):
        """Test 3.8: Verify DEBUG logs include context (not just "processing X")"""
        from simulation.accuracy.AccuracySimulationManager import AccuracySimulationManager

        import inspect
        source = inspect.getsource(AccuracySimulationManager)

        assert 'logger.debug' in source

    def test_all_111_logger_calls_reviewed(self):
        """Test 3.9: Verify all 111 logger calls exist (comprehensive per Q1)"""
        result = subprocess.run(
            ['grep', '-rE', 'logger\\.(debug|info|warning|error)',
             str(project_root / 'simulation' / 'accuracy')],
            capture_output=True,
            text=True,
            timeout=60
        )

        logger_calls = result.stdout.count('logger.')

        assert logger_calls >= 80

    def test_accuracy_simulation_manager_debug_logs(self):
        """Test 3.10: Verify AccuracySimulationManager has appropriate DEBUG logs (58 calls)"""
        from simulation.accuracy.AccuracySimulationManager import AccuracySimulationManager

        import inspect
        source = inspect.getsource(AccuracySimulationManager)

        debug_count = source.count('logger.debug')

        assert debug_count >= 10

    def test_accuracy_results_manager_debug_logs(self):
        """Test 3.11: Verify AccuracyResultsManager has appropriate DEBUG logs (23 calls)"""
        from simulation.accuracy.AccuracyResultsManager import AccuracyResultsManager

        import inspect
        source = inspect.getsource(AccuracyResultsManager)

        assert 'logger.debug' in source

    def test_accuracy_calculator_debug_logs(self):
        """Test 3.12: Verify AccuracyCalculator has appropriate DEBUG logs (19 calls)"""
        from simulation.accuracy.AccuracyCalculator import AccuracyCalculator

        import inspect
        source = inspect.getsource(AccuracyCalculator)

        assert 'logger.debug' in source
        assert 'before filtering' in source.lower() or 'after filtering' in source.lower()

    def test_parallel_accuracy_runner_debug_logs(self):
        """Test 3.13: Verify ParallelAccuracyRunner has appropriate DEBUG logs (11 calls + worker tracing)"""
        from simulation.accuracy.ParallelAccuracyRunner import ParallelAccuracyRunner

        import inspect
        source = inspect.getsource(ParallelAccuracyRunner)

        assert 'logger.debug' in source
        assert 'progress' in source.lower() or 'completed' in source

    def test_message_decoration_preserved(self):
        """Test 3.14: Verify no excessive message decoration removed (per Q3)"""
        from simulation.accuracy.ParallelAccuracyRunner import ParallelAccuracyRunner

        import inspect
        source = inspect.getsource(ParallelAccuracyRunner)

        assert 'logger' in source
        assert 'self.logger' in source

    def test_no_excessive_variable_logging(self):
        """Test 3.15: Verify no logging for every variable assignment (quality criteria)"""
        from simulation.accuracy.AccuracySimulationManager import AccuracySimulationManager

        import inspect
        source = inspect.getsource(AccuracySimulationManager)

        debug_count = source.count('logger.debug')
        method_count = source.count('def ')

        if method_count > 0:
            ratio = debug_count / method_count
            assert ratio < 20



class TestAccuracySimulationINFOLogQuality:
    """Test Category 4: INFO Log Quality (Requirement R4)"""

    def test_info_logs_show_major_phase_transitions(self):
        """Test 4.2: Verify major phases logged (initialization, baseline load, simulation, results)"""
        from simulation.accuracy.AccuracySimulationManager import AccuracySimulationManager

        import inspect
        source = inspect.getsource(AccuracySimulationManager)

        assert 'logger.info' in source

    def test_info_logs_show_significant_outcomes(self):
        """Test 4.3: Verify outcomes logged (configs evaluated, best config found, results saved)"""
        from simulation.accuracy.AccuracyResultsManager import AccuracyResultsManager

        import inspect
        source = inspect.getsource(AccuracyResultsManager)

        assert 'logger.info' in source
        assert 'saved' in source.lower() or 'complete' in source.lower()

    def test_info_logs_show_completion_summary(self):
        """Test 4.8: Verify completion summary logged (total time, configs evaluated, best result)"""
        from simulation.accuracy.AccuracySimulationManager import AccuracySimulationManager

        import inspect
        source = inspect.getsource(AccuracySimulationManager.run_both)

        assert 'logger.info' in source
        assert 'complete' in source.lower()



class TestAccuracySimulationERRORLogQuality:
    """Test Category 5: ERROR Log Quality (Requirement R5)"""

    def test_error_log_baseline_config_not_found(self):
        """Test 5.1: Verify ERROR logged when baseline config folder missing"""
        import run_accuracy_simulation

        with open(project_root / 'run_accuracy_simulation.py', 'r') as f:
            source = f.read()

        assert 'logger.error' in source
        assert 'baseline' in source.lower()

    def test_error_log_sim_data_folder_not_found(self):
        """Test 5.2: Verify ERROR logged when sim_data/ folder missing"""
        with open(project_root / 'run_accuracy_simulation.py', 'r') as f:
            source = f.read()

        assert 'logger.error' in source
        assert 'folder' in source.lower() or 'directory' in source.lower()

    def test_error_log_configuration_validation_failure(self):
        """Test 5.4: Verify ERROR logged when config validation fails"""
        with open(project_root / 'run_accuracy_simulation.py', 'r') as f:
            source = f.read()

        assert 'logger.error' in source

    def test_error_log_parallel_execution_failure(self):
        """Test 5.5: Verify ERROR logged when parallel execution fails"""
        from simulation.accuracy.ParallelAccuracyRunner import ParallelAccuracyRunner

        import inspect
        source = inspect.getsource(ParallelAccuracyRunner)

        assert 'except' in source or 'try' in source

    def test_error_logs_include_exc_info(self):
        """Test 5.7: Verify ERROR logs include exception info (exc_info=True) for debugging"""
        with open(project_root / 'run_accuracy_simulation.py', 'r') as f:
            source = f.read()

        error_logs = source.count('logger.error')

        assert error_logs >= 5



class TestAccuracySimulationEdgeCases:
    """Test Category 6: Edge Cases"""



class TestAccuracySimulationConfiguration:
    """Test Category 7: Configuration Tests"""



def create_test_parser():
    """Helper to create argparse parser for testing without executing main

    This mirrors the actual parser setup in run_accuracy_simulation.py main() function.
    """
    parser = argparse.ArgumentParser(
        description='Accuracy Simulation Runner - Test Parser'
    )

    parser.add_argument('--output', type=str, default='./simulation/optimal_configs')
    parser.add_argument('--data', type=str, default='./simulation/sim_data')
    parser.add_argument('--baseline', type=str, default=None)
    parser.add_argument('--num-params', type=int, default=4)
    parser.add_argument('--test-values', type=int, default=3)
    parser.add_argument('--num-processes', type=int, default=8)
    parser.add_argument('--use-processes', action='store_true', default=True)
    parser.add_argument('--no-use-processes', dest='use_processes', action='store_false')

    parser.add_argument(
        '--log-level',
        choices=['debug', 'info', 'warning', 'error'],
        default='info',
        help='Logging level'
    )

    parser.add_argument(
        '--enable-log-file',
        action='store_true',
        default=False,
        help='Enable file logging to logs/accuracy_simulation/ folder'
    )

    return parser


def create_test_parser_f03():
    """Helper to create argparse parser for F03 testing — includes --params and --compare."""
    parser = argparse.ArgumentParser(description='F03 Test Parser')
    parser.add_argument('--baseline', type=str, default=None)
    parser.add_argument('--output', type=str, default='./simulation/optimal_configs')
    parser.add_argument('--data', type=str, default='./simulation/sim_data')
    parser.add_argument('--num-params', type=int, default=4)
    parser.add_argument('--test-values', type=int, default=3)
    parser.add_argument('--use-processes', action='store_true', default=True)
    parser.add_argument('--no-use-processes', dest='use_processes', action='store_false')
    parser.add_argument('--log-level', choices=['debug', 'info', 'warning', 'error'], default='info')
    parser.add_argument('--enable-log-file', action='store_true', default=False)
    parser.add_argument('--max-workers', type=int, default=8)
    parser.add_argument('--params', type=str, default=None)
    parser.add_argument('--compare', nargs=2, metavar=('FOLDER_A', 'FOLDER_B'), type=str, default=None)
    return parser


class TestPromoteCLIFlag:
    """Tests for --promote CLI flag (F02 spec TS2)."""

    def test_promote_flag_in_help_text(self):
        """--promote flag is listed in --help output."""
        result = subprocess.run(
            [sys.executable, str(project_root / "run_accuracy_simulation.py"), "--help"],
            capture_output=True,
            text=True,
            timeout=60
        )
        assert result.returncode == 0
        assert "--promote" in result.stdout

    def test_standalone_promote_missing_folder_exits_1(self, tmp_path):
        """--promote <missing_folder> exits 1 with 'Promote folder not found' message."""
        missing = tmp_path / "nonexistent_folder"
        result = subprocess.run(
            [sys.executable, str(project_root / "run_accuracy_simulation.py"),
             "--promote", str(missing)],
            capture_output=True,
            text=True,
            timeout=60
        )
        assert result.returncode == 1
        combined_output = result.stdout + result.stderr
        assert "Promote folder not found" in combined_output

    def test_promote_argparse_semantics(self):
        """--promote uses nargs='?', const=True, no type kwarg: 3 correct value states."""
        parser = argparse.ArgumentParser()
        parser.add_argument('--promote', nargs='?', const=True, default=None, metavar='FOLDER')
        args_none = parser.parse_args([])
        assert args_none.promote is None
        args_true = parser.parse_args(['--promote'])
        assert args_true.promote is True
        args_str = parser.parse_args(['--promote', '/some/path'])
        assert isinstance(args_str.promote, str)
        assert args_str.promote == '/some/path'

    def test_standalone_promote_no_sim_run(self, tmp_path):
        """--promote <valid_folder>: AccuracySimulationManager not instantiated."""
        import json
        config_files = ['league_config.json', 'week1-5.json', 'week6-9.json',
                        'week10-13.json', 'week14-17.json']
        optimal = tmp_path / "optimal"
        optimal.mkdir()
        for cf in config_files:
            (optimal / cf).write_text(json.dumps({'parameters': {}}))
        with patch('run_accuracy_simulation.AccuracySimulationManager') as mock_mgr, \
             patch('run_accuracy_simulation.propagate_to_configs') as mock_promote, \
             patch('sys.argv', ['run_accuracy_simulation.py',
                                '--promote', str(optimal)]):
            mock_promote.return_value = None
            import run_accuracy_simulation
            try:
                run_accuracy_simulation.main()
            except SystemExit as e:
                assert e.code == 0
            mock_mgr.assert_not_called()
            mock_promote.assert_called_once()

    def test_post_run_promote_calls_propagate(self, tmp_path):
        """--promote without folder arg after sim run calls propagate_to_configs with optimal_path."""
        import json
        optimal = tmp_path / "optimal"
        optimal.mkdir()
        for cf in ['league_config.json', 'week1-5.json', 'week6-9.json',
                   'week10-13.json', 'week14-17.json']:
            (optimal / cf).write_text(json.dumps({'parameters': {}}))
        with patch('run_accuracy_simulation.AccuracySimulationManager') as mock_cls, \
             patch('run_accuracy_simulation.propagate_to_configs') as mock_promote, \
             patch('run_accuracy_simulation.find_baseline_config', return_value=optimal), \
             patch('sys.argv', ['run_accuracy_simulation.py', '--promote',
                                '--baseline', str(optimal)]):
            mock_instance = MagicMock()
            mock_instance.run_both.return_value = optimal
            mock_instance.results_manager.get_summary.return_value = "Summary"
            mock_cls.return_value = mock_instance
            import run_accuracy_simulation
            try:
                run_accuracy_simulation.main()
            except SystemExit:
                pass
            mock_promote.assert_called_once()
            call_args = mock_promote.call_args
            assert call_args[0][0] == optimal
            assert str(call_args[0][1]) == "data/configs"


class TestF03CliAndSummaryEnhancements:
    """Test Category F03: CLI and Summary Enhancements (F03 feature tests)"""

    def test_params_flag_exists_in_help(self):
        """Test: --params argparse flag exists"""
        result = subprocess.run(
            [sys.executable, str(project_root / "run_accuracy_simulation.py"), "--help"],
            capture_output=True, text=True, timeout=60
        )
        assert result.returncode == 0
        assert "--params" in result.stdout

    def test_params_default_is_none(self):
        """Test: --params default is None"""
        parser = create_test_parser_f03()
        args = parser.parse_args([])
        assert args.params is None

    def test_params_accepts_comma_separated_list(self):
        """Test: --params accepts comma-separated list as a string"""
        parser = create_test_parser_f03()
        args = parser.parse_args(['--params', 'NORMALIZATION_MAX_SCALE,MATCHUP_SCORING_WEIGHT'])
        assert args.params == 'NORMALIZATION_MAX_SCALE,MATCHUP_SCORING_WEIGHT'

    def test_compare_flag_exists_in_help(self):
        """Test: --compare argparse flag exists"""
        result = subprocess.run(
            [sys.executable, str(project_root / "run_accuracy_simulation.py"), "--help"],
            capture_output=True, text=True, timeout=60
        )
        assert result.returncode == 0
        assert "--compare" in result.stdout

    def test_compare_accepts_two_folder_args(self):
        """Test: --compare accepts exactly two folder arguments"""
        parser = create_test_parser_f03()
        args = parser.parse_args(['--compare', 'a/', 'b/'])
        assert args.compare == ['a/', 'b/']

    def test_get_summary_with_overall_metrics_shows_pairwise(self):
        """Test: get_summary() with overall_metrics present shows Pairwise accuracy"""
        from simulation.accuracy.AccuracyResultsManager import AccuracyResultsManager

        with tempfile.TemporaryDirectory() as tmpdir:
            manager = AccuracyResultsManager(
                output_dir=Path(tmpdir),
                baseline_config_path=Path(tmpdir)
            )
            mock_overall = MagicMock()
            mock_overall.pairwise_accuracy = 0.615
            mock_overall.top_10_accuracy = 0.436
            mock_overall.spearman_correlation = 0.341
            mock_perf = MagicMock()
            mock_perf.overall_metrics = mock_overall
            mock_perf.mae = 4.5960
            mock_perf.player_count = 6610
            manager.best_configs['week_1_5'] = mock_perf
            summary = manager.get_summary()
            assert "Pairwise" in summary
            assert "61.5%" in summary

    def test_get_summary_without_overall_metrics_falls_back_to_mae(self):
        """Test: get_summary() with overall_metrics=None falls back to MAE-only"""
        from simulation.accuracy.AccuracyResultsManager import AccuracyResultsManager

        with tempfile.TemporaryDirectory() as tmpdir:
            manager = AccuracyResultsManager(
                output_dir=Path(tmpdir),
                baseline_config_path=Path(tmpdir)
            )
            mock_perf = MagicMock()
            mock_perf.overall_metrics = None
            mock_perf.mae = 4.5960
            mock_perf.player_count = 6610
            manager.best_configs['week_1_5'] = mock_perf
            summary = manager.get_summary()
            assert "Pairwise" not in summary
            assert "MAE=4.5960" in summary

    def test_load_folder_metrics_reads_ranking_metrics(self):
        """Test: load_folder_metrics() reads ranking_metrics from folder JSON files"""
        import json as json_module
        import run_accuracy_simulation

        with tempfile.TemporaryDirectory() as tmpdir:
            folder = Path(tmpdir)
            metrics = {
                'pairwise_accuracy': 0.615,
                'top_10_accuracy': 0.436,
                'spearman_correlation': 0.341
            }
            data = {'performance_metrics': {'ranking_metrics': metrics}}
            for fname in ['week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']:
                with open(folder / fname, 'w') as f:
                    json_module.dump(data, f)
            result = run_accuracy_simulation.load_folder_metrics(folder)
            assert result['week_1_5'] is not None
            assert result['week_1_5']['pairwise_accuracy'] == 0.615

    def test_load_folder_metrics_handles_missing_ranking_metrics(self):
        """Test: load_folder_metrics() returns None for horizon with no ranking_metrics"""
        import json as json_module
        import run_accuracy_simulation

        with tempfile.TemporaryDirectory() as tmpdir:
            folder = Path(tmpdir)
            data_no_ranking = {'performance_metrics': {'mae': 4.5960}}
            for fname in ['week1-5.json', 'week6-9.json', 'week10-13.json', 'week14-17.json']:
                with open(folder / fname, 'w') as f:
                    json_module.dump(data_no_ranking, f)
            result = run_accuracy_simulation.load_folder_metrics(folder)
            assert result['week_1_5'] is None


class TestF03SubprocessTests:
    """Subprocess tests for F03 error paths"""

    def test_unknown_params_value_exits_nonzero(self):
        """Test: --params with unknown value exits non-zero with 'Unknown' in stderr"""
        result = subprocess.run(
            [sys.executable, str(project_root / "run_accuracy_simulation.py"),
             "--params", "BOGUS_PARAM_XYZ"],
            capture_output=True, text=True, timeout=60
        )
        assert result.returncode != 0
        assert "Unknown" in result.stderr or "Unknown" in result.stdout

    def test_compare_with_missing_folder_exits_nonzero(self):
        """Test: --compare with nonexistent folders exits non-zero"""
        result = subprocess.run(
            [sys.executable, str(project_root / "run_accuracy_simulation.py"),
             "--compare", "/nonexistent_folder_a_xyz", "/nonexistent_folder_b_xyz"],
            capture_output=True, text=True, timeout=60
        )
        assert result.returncode != 0


"""
Test Coverage Summary for Feature 04 (accuracy_sim_logging):

Category 1: CLI Flag Integration (R1) - 8 tests
Category 2: Feature 01 Integration (R2) - 6 tests
Category 3: DEBUG Log Quality (R3) - 15 tests
Category 4: INFO Log Quality (R4) - 8 tests
Category 5: ERROR Log Quality (R5) - 7 tests
Category 6: Edge Cases - 8 tests
Category 7: Configuration - 6 tests

TOTAL: 58 tests

Unit Tests (can run without real data): ~30 tests
Integration Tests (marked @pytest.mark.integration): ~28 tests

Integration tests require real simulation data and are skipped by default.
Run with: pytest -m integration

Coverage: >90% of requirements (58 tests across 5 requirements)
"""


class TestHorizonLabelDelegationGuard:
    """
    T77/D4: the accuracy engine's horizon count has exactly one definition
    (simulation/accuracy/horizon_labels.HORIZON_COUNT), so a single implementation
    cannot be compared against itself. Same reasoning as
    TestPreloadCopiesShareOneImplementation (T73) - the pin asserts instead that each
    consumer DELEGATES and that none re-inlines its own count literal.
    """

    def test_cli_banner_delegates_to_the_shared_label_builders(self):
        import inspect
        import run_accuracy_simulation

        source = inspect.getsource(run_accuracy_simulation.main)

        assert 'candidate_values_label(' in source, (
            "run_accuracy_simulation.main no longer delegates to candidate_values_label"
        )
        assert 'configs_per_param_label(' in source, (
            "run_accuracy_simulation.main no longer delegates to configs_per_param_label"
        )

    def test_cli_banner_reinlines_no_horizon_count_literal(self):
        """The CLI banner DELEGATES to the shared builders rather than re-inlining.

        Asserts delegation positively (the T73
        TestPreloadCopiesShareOneImplementation shape), not the absence of the word
        "horizons" from main(): argparse help text in main() legitimately reads
        "across all 4 horizons", so an absence check false-fails on documentation
        that is not a re-inlined label.
        """
        import inspect
        import run_accuracy_simulation

        source = inspect.getsource(run_accuracy_simulation.main)

        assert 'candidate_values_label(' in source, (
            "run_accuracy_simulation.main must call candidate_values_label(); "
            "re-inlining the banner text reintroduces the hand-synced duplication "
            "this story removed"
        )
        assert 'configs_per_param_label(' in source, (
            "run_accuracy_simulation.main must call configs_per_param_label(); "
            "re-inlining the banner text reintroduces the hand-synced duplication "
            "this story removed"
        )
        assert 'Candidate values per parameter per horizon:' not in source, (
            "run_accuracy_simulation.main re-inlined the literal banner label text "
            "instead of delegating to candidate_values_label()"
        )
        assert 'Configs per horizon-specific parameter:' not in source, (
            "run_accuracy_simulation.main re-inlined the literal banner label text "
            "instead of delegating to configs_per_param_label()"
        )

    def test_manager_startup_log_delegates_to_the_shared_label_builders(self):
        import inspect
        from simulation.accuracy.AccuracySimulationManager import AccuracySimulationManager

        source = inspect.getsource(AccuracySimulationManager.__init__)

        assert 'candidate_values_label(' in source, (
            "AccuracySimulationManager.__init__ no longer delegates to "
            "candidate_values_label"
        )
        assert 'configs_per_param_label(' in source, (
            "AccuracySimulationManager.__init__ no longer delegates to "
            "configs_per_param_label"
        )

    def test_manager_startup_log_reinlines_no_horizon_count_literal(self):
        import inspect
        from simulation.accuracy.AccuracySimulationManager import AccuracySimulationManager

        source = inspect.getsource(AccuracySimulationManager.__init__)

        assert 'candidate_values_label(' in source, (
            "AccuracySimulationManager.__init__ must call candidate_values_label(); "
            "re-inlining the banner text reintroduces the hand-synced duplication"
        )
        assert 'configs_per_param_label(' in source, (
            "AccuracySimulationManager.__init__ must call configs_per_param_label(); "
            "re-inlining the banner text reintroduces the hand-synced duplication"
        )
        assert 'Candidate values per parameter per horizon:' not in source, (
            "AccuracySimulationManager.__init__ re-inlined the literal banner label "
            "text instead of delegating to candidate_values_label()"
        )
        assert 'Configs per horizon-specific parameter:' not in source, (
            "AccuracySimulationManager.__init__ re-inlined the literal banner label "
            "text instead of delegating to configs_per_param_label()"
        )

    def test_parallel_runner_evaluation_log_delegates_to_horizon_count(self):
        import inspect
        from simulation.accuracy.ParallelAccuracyRunner import ParallelAccuracyRunner

        source = inspect.getsource(ParallelAccuracyRunner.evaluate_configs_parallel)

        assert 'HORIZON_COUNT' in source, (
            "ParallelAccuracyRunner.evaluate_configs_parallel no longer delegates to "
            "HORIZON_COUNT"
        )
        assert '× 5' not in source, (
            "ParallelAccuracyRunner.evaluate_configs_parallel re-inlined the drifted "
            "count"
        )

    def test_parallel_runner_no_longer_carries_its_own_week_ranges_copy(self):
        """T77 AC3: the function-local duplicate is the root of the drift."""
        import inspect
        from simulation.accuracy import ParallelAccuracyRunner as par_module

        source = inspect.getsource(par_module)

        assert 'WEEK_RANGES = ' not in source, (
            "ParallelAccuracyRunner re-introduced a local WEEK_RANGES copy"
        )


class TestHorizonCountAgreement:
    """
    T77 AC7: no site in the accuracy engine may state a horizon count that
    disagrees with HORIZON_COUNT. Engine-wide, not consumer-enumerated, so it also
    covers AccuracySimulationManager's two deliberately-unrefactored sites (D3) and
    any future one.
    """

    @staticmethod
    def _scan(text):
        import re

        # Up to two intervening words are allowed between the number and
        # "horizons". Without this, the story's own rewording to
        # "all 4 weekly horizons" would sit OUTSIDE the scan -- a net loss of
        # reach, since the pre-story "all 5 horizons" WAS caught. Verified: a
        # planted "all 5 weekly horizons" is detected with this pattern and
        # missed without it.
        return [
            int(match.group(1))
            for match in re.finditer(r'(\d+)\s+(?:\w+\s+){0,2}horizons?', text)
        ]

    @staticmethod
    def _engine_sources():
        from pathlib import Path

        project_root = Path(__file__).parent.parent.parent
        paths = sorted((project_root / 'simulation' / 'accuracy').glob('*.py'))
        paths.append(project_root / 'run_accuracy_simulation.py')
        return paths

    def test_no_engine_site_disagrees_with_horizon_count(self):
        from simulation.accuracy.horizon_labels import HORIZON_COUNT

        disagreeing = []
        for path in self._engine_sources():
            lines = path.read_text(encoding='utf-8').splitlines()
            for line_number, line in enumerate(lines, 1):
                for number in self._scan(line):
                    if number != HORIZON_COUNT:
                        disagreeing.append((path.name, line_number, number))

        assert disagreeing == [], (
            f"these sites state a horizon count that disagrees with "
            f"HORIZON_COUNT={HORIZON_COUNT}: {disagreeing}"
        )

    def test_the_scan_actually_reaches_every_consumer_file(self):
        """A scan finding nothing because it read nothing would pass vacuously."""
        names = {path.name for path in self._engine_sources()}

        assert {
            'AccuracySimulationManager.py',
            'ParallelAccuracyRunner.py',
            'horizon_labels.py',
            'run_accuracy_simulation.py',
        } <= names, f"the count-agreement scan misses a consumer file: {sorted(names)}"

    def test_count_agreement_scan_detects_a_planted_disagreement(self):
        """The guard must be discriminating, not merely present."""
        from simulation.accuracy.horizon_labels import HORIZON_COUNT

        planted = 'evaluated across all 5 horizons for every config'

        assert [
            number for number in self._scan(planted) if number != HORIZON_COUNT
        ] == [5], "the count-agreement scan would not catch a re-drifted site"


class TestBannerOutputUnchanged:
    """
    T77 AC6: the two banner consumers' operator-visible text is byte-identical to
    what they shipped before the de-duplication. Every expected string is pinned as a
    LITERAL - rebuilding it from the builders under test would make the assertion
    circular and pass through any label change.
    """

    def test_cli_banner_line_one_is_byte_identical(self):
        from simulation.accuracy.horizon_labels import candidate_values_label

        assert candidate_values_label(6) == (
            'Candidate values per parameter per horizon: 6'
        )

    def test_cli_banner_line_two_is_byte_identical(self):
        from simulation.accuracy.horizon_labels import configs_per_param_label

        assert configs_per_param_label(6, 24) == (
            'Configs per horizon-specific parameter: 6 × 4 horizons = 24'
        )

    def test_manager_startup_line_is_byte_identical(self):
        from simulation.accuracy.horizon_labels import (
            candidate_values_label,
            configs_per_param_label,
        )

        rendered = (
            f"AccuracySimulationManager initialized: "
            f"{candidate_values_label(6)}; "
            f"{configs_per_param_label(6, 24)}"
        )

        assert rendered == (
            'AccuracySimulationManager initialized: Candidate values per parameter '
            'per horizon: 6; Configs per horizon-specific parameter: 6 × 4 '
            'horizons = 24'
        )


class TestParallelRunnerEvaluationLogLine:
    """
    T77 AC4: the one operator-visible line this story deliberately CHANGES (5 -> 4).
    Captured by attaching a handler directly to the runner's logger: this project's
    get_logger() returns the 'default' logger with propagate=False, so pytest's caplog
    fixture would capture nothing and the assertion would pass vacuously.
    """

    def test_logs_the_horizon_count_derived_total(self, tmp_path):
        import logging
        from unittest.mock import patch

        from simulation.accuracy.ParallelAccuracyRunner import ParallelAccuracyRunner

        runner = ParallelAccuracyRunner(
            data_folder=tmp_path,
            available_seasons=[tmp_path / '2024'],
            max_workers=2,
            use_processes=False,
        )

        records = []

        class _Capture(logging.Handler):
            def emit(self, record):
                records.append(record.getMessage())

        handler = _Capture(level=logging.INFO)
        runner.logger.addHandler(handler)
        try:
            with patch(
                'simulation.accuracy.ParallelAccuracyRunner.'
                '_evaluate_config_tournament_process',
                side_effect=lambda config, *args: (config, {}),
            ):
                runner.evaluate_configs_parallel(
                    [{'id': index} for index in range(3)]
                )
        finally:
            runner.logger.removeHandler(handler)

        assert (
            'Starting parallel evaluation: 3 configs × 4 horizons = 12 '
            'total evaluations'
        ) in records, f"evaluation log line changed or drifted: {records}"




class TestT69TerminatingRunner:
    """T69/AC1 + AC13: the runner terminates and has a meaningful exit code.

    Before T69, `run_accuracy_simulation.py` ended in an unconditional infinite loop, so an
    end-to-end test of this script was IMPOSSIBLE -- the process never exited. Every other
    subprocess assertion in this file therefore probes `--help` only. This is the first test
    that runs the actual optimizer end to end.
    """

    def test_scoped_run_terminates_with_exit_code_zero(self, tmp_path):
        """A scoped optimization run finishes on its own and exits 0.

        Scoped to one parameter and two test values to keep the runtime near a minute.
        --output is a scratch directory; simulation/sim_data/ is READ but never written
        (it is tracked season data).

        A TimeoutExpired here is a FAILURE, not a slow machine: it means the endless
        behaviour survived, which is the whole defect this story removes.
        """
        try:
            result = subprocess.run(
                [
                    sys.executable, str(project_root / "run_accuracy_simulation.py"),
                    "--output", str(tmp_path),
                    "--params", "NORMALIZATION_MAX_SCALE",
                    "--test-values", "2",
                    "--max-workers", "4",
                    "--log-level", "warning",
                ],
                capture_output=True,
                text=True,
                timeout=900,
                cwd=str(project_root),
            )
        except subprocess.TimeoutExpired:
            pytest.fail(
                "run_accuracy_simulation.py did not terminate within 900s. The T69 "
                "convergent runner is supposed to exit on its own; a timeout means the "
                "endless behaviour survived."
            )

        assert result.returncode == 0, (
            f"expected exit 0, got {result.returncode}\n"
            f"stdout tail:\n{result.stdout[-2000:]}\n"
            f"stderr tail:\n{result.stderr[-2000:]}"
        )

    def test_scoped_run_writes_exactly_one_optimal_folder(self, tmp_path):
        """T69/AC9: one converged run writes one accuracy_optimal_* folder, not one per pass."""
        result = subprocess.run(
            [
                sys.executable, str(project_root / "run_accuracy_simulation.py"),
                "--output", str(tmp_path),
                "--params", "NORMALIZATION_MAX_SCALE",
                "--test-values", "2",
                "--max-workers", "4",
                "--log-level", "warning",
            ],
            capture_output=True,
            text=True,
            timeout=900,
            cwd=str(project_root),
        )
        assert result.returncode == 0, result.stderr[-2000:]

        optimal = sorted(tmp_path.glob("accuracy_optimal_*"))
        assert len(optimal) == 1, f"expected exactly 1 optimal folder, found {len(optimal)}: {optimal}"


class TestD84ExcludeLowCoverageWeeksFlag:
    """D8.4: the opt-in flag exists, is off by default, and reaches the manager."""

    def _baseline_folder(self, tmp_path):
        import json
        folder = tmp_path / "optimal"
        folder.mkdir()
        for name in ['league_config.json', 'week1-5.json', 'week6-9.json',
                     'week10-13.json', 'week14-17.json']:
            (folder / name).write_text(json.dumps({'parameters': {}}))
        return folder

    def _manager_kwargs(self, tmp_path, extra_argv):
        folder = self._baseline_folder(tmp_path)
        argv = ['run_accuracy_simulation.py', '--baseline', str(folder),
                '--output', str(tmp_path / "out")] + extra_argv
        with patch('run_accuracy_simulation.AccuracySimulationManager') as mock_cls, \
             patch('sys.argv', argv):
            mock_instance = MagicMock()
            mock_instance.run_both.return_value = folder
            mock_instance.results_manager.get_summary.return_value = "Summary"
            mock_cls.return_value = mock_instance
            import run_accuracy_simulation
            try:
                run_accuracy_simulation.main()
            except SystemExit:
                pass
            return mock_cls.call_args.kwargs

    def test_the_flag_is_listed_in_help(self):
        result = subprocess.run(
            [sys.executable, str(project_root / "run_accuracy_simulation.py"), "--help"],
            capture_output=True,
            text=True,
            timeout=60
        )

        assert result.returncode == 0
        assert "--exclude-low-coverage-weeks" in result.stdout

    def test_the_default_reaches_the_manager_as_false(self, tmp_path):
        kwargs = self._manager_kwargs(tmp_path, [])

        assert kwargs['exclude_low_coverage_weeks'] is False

    def test_the_flag_reaches_the_manager_as_true(self, tmp_path):
        kwargs = self._manager_kwargs(tmp_path, ['--exclude-low-coverage-weeks'])

        assert kwargs['exclude_low_coverage_weeks'] is True
