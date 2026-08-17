"""
Unit Tests for validate_sim_data.py

Tests CLI validation, CSV file checks, week folder checks, JSON spot-checks,
and exit codes for the validate_sim_data feature.

Test Category: R1-R7 — Validate Sim Data checks (13 tests)
"""

import json
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from historical_data_compiler.constants import (
    SEASON_SCHEDULE_FILE,
    GAME_DATA_FILE,
    TEAM_DATA_FOLDER,
    WEEKS_FOLDER,
    VALIDATION_WEEKS,
    EXPECTED_NFL_TEAMS,
    POSITION_JSON_FILES,
)

from validate_sim_data import main


class TestValidateSimData:
    """Tests for validate_sim_data.py (R1-R7)."""

    def _build_valid_tree(self, base_dir: Path) -> None:
        (base_dir / SEASON_SCHEDULE_FILE).write_text("year,week\n2025,1\n")
        (base_dir / GAME_DATA_FILE).write_text("game_id,week\n1,1\n")
        team_dir = base_dir / TEAM_DATA_FOLDER
        team_dir.mkdir()
        for i in range(EXPECTED_NFL_TEAMS):
            (team_dir / f"team_{i:02d}.csv").write_text("abbrev,name\n")
        weeks_dir = base_dir / WEEKS_FOLDER
        weeks_dir.mkdir()
        for w in range(1, VALIDATION_WEEKS + 1):
            week_dir = weeks_dir / f"week_{w:02d}"
            week_dir.mkdir()
            for fname in POSITION_JSON_FILES.values():
                key = Path(fname).stem
                (week_dir / fname).write_text(json.dumps({key: [{"id": 1}]}))

    def test_valid_tree_exits_0(self, tmp_path):
        self._build_valid_tree(tmp_path)
        mock_logger = MagicMock()
        with patch('validate_sim_data.get_logger', return_value=mock_logger), \
             patch('sys.argv', ['validate_sim_data.py', '--year', '2025',
                                '--output-dir', str(tmp_path)]):
            result = main()
        assert result == 0

    def test_missing_csv_exits_1_and_logs_error(self, tmp_path):
        self._build_valid_tree(tmp_path)
        (tmp_path / SEASON_SCHEDULE_FILE).unlink()
        mock_logger = MagicMock()
        with patch('validate_sim_data.get_logger', return_value=mock_logger), \
             patch('sys.argv', ['validate_sim_data.py', '--year', '2025',
                                '--output-dir', str(tmp_path)]):
            result = main()
        assert result == 1
        error_messages = [c.args[0] for c in mock_logger.error.call_args_list]
        assert any("Missing required CSV" in msg and SEASON_SCHEDULE_FILE in msg
                   for msg in error_messages)

    def test_wrong_team_data_count_exits_1_and_logs_error(self, tmp_path):
        self._build_valid_tree(tmp_path)
        team_dir = tmp_path / TEAM_DATA_FOLDER
        list(team_dir.glob("*.csv"))[0].unlink()
        mock_logger = MagicMock()
        with patch('validate_sim_data.get_logger', return_value=mock_logger), \
             patch('sys.argv', ['validate_sim_data.py', '--year', '2025',
                                '--output-dir', str(tmp_path)]):
            result = main()
        assert result == 1
        error_messages = [c.args[0] for c in mock_logger.error.call_args_list]
        assert any(f"Expected {EXPECTED_NFL_TEAMS} team CSV files" in msg
                   and f"found {EXPECTED_NFL_TEAMS - 1}" in msg
                   for msg in error_messages)

    def test_missing_week_folder_exits_1_and_logs_error(self, tmp_path):
        self._build_valid_tree(tmp_path)
        shutil.rmtree(tmp_path / WEEKS_FOLDER / "week_18")
        mock_logger = MagicMock()
        with patch('validate_sim_data.get_logger', return_value=mock_logger), \
             patch('sys.argv', ['validate_sim_data.py', '--year', '2025',
                                '--output-dir', str(tmp_path)]):
            result = main()
        assert result == 1
        error_messages = [c.args[0] for c in mock_logger.error.call_args_list]
        assert any("Missing week folder" in msg and "week_18" in msg
                   for msg in error_messages)

    def test_missing_json_file_exits_1_and_logs_error(self, tmp_path):
        self._build_valid_tree(tmp_path)
        (tmp_path / WEEKS_FOLDER / "week_01" / POSITION_JSON_FILES['RB']).unlink()
        mock_logger = MagicMock()
        with patch('validate_sim_data.get_logger', return_value=mock_logger), \
             patch('sys.argv', ['validate_sim_data.py', '--year', '2025',
                                '--output-dir', str(tmp_path)]):
            result = main()
        assert result == 1
        error_messages = [c.args[0] for c in mock_logger.error.call_args_list]
        assert any("Missing JSON file" in msg and POSITION_JSON_FILES['RB'] in msg
                   for msg in error_messages)

    def test_bad_json_structure_exits_1_and_logs_error(self, tmp_path):
        self._build_valid_tree(tmp_path)
        qb_path = tmp_path / WEEKS_FOLDER / "week_01" / POSITION_JSON_FILES['QB']
        qb_path.write_text(json.dumps([{"id": 1}]))
        mock_logger = MagicMock()
        with patch('validate_sim_data.get_logger', return_value=mock_logger), \
             patch('sys.argv', ['validate_sim_data.py', '--year', '2025',
                                '--output-dir', str(tmp_path)]):
            result = main()
        assert result == 1
        error_messages = [c.args[0] for c in mock_logger.error.call_args_list]
        assert any("Unexpected structure" in msg and "qb_data" in msg
                   for msg in error_messages)

    def test_output_dir_not_found_exits_1_and_logs_error(self, tmp_path):
        nonexistent = tmp_path / "does_not_exist"
        mock_logger = MagicMock()
        with patch('validate_sim_data.get_logger', return_value=mock_logger), \
             patch('sys.argv', ['validate_sim_data.py', '--year', '2025',
                                '--output-dir', str(nonexistent)]):
            result = main()
        assert result == 1
        error_messages = [c.args[0] for c in mock_logger.error.call_args_list]
        assert any("Output directory does not exist" in msg for msg in error_messages)

    def test_invalid_json_in_qb_data_exits_1_and_logs_error(self, tmp_path):
        self._build_valid_tree(tmp_path)
        qb_path = tmp_path / WEEKS_FOLDER / "week_01" / POSITION_JSON_FILES['QB']
        qb_path.write_text("{not valid json")
        mock_logger = MagicMock()
        with patch('validate_sim_data.get_logger', return_value=mock_logger), \
             patch('sys.argv', ['validate_sim_data.py', '--year', '2025',
                                '--output-dir', str(tmp_path)]):
            result = main()
        assert result == 1
        error_messages = [c.args[0] for c in mock_logger.error.call_args_list]
        assert any("Invalid JSON" in msg for msg in error_messages)

    def test_empty_qb_data_list_exits_1_and_logs_error(self, tmp_path):
        self._build_valid_tree(tmp_path)
        qb_path = tmp_path / WEEKS_FOLDER / "week_01" / POSITION_JSON_FILES['QB']
        qb_path.write_text(json.dumps({"qb_data": []}))
        mock_logger = MagicMock()
        with patch('validate_sim_data.get_logger', return_value=mock_logger), \
             patch('sys.argv', ['validate_sim_data.py', '--year', '2025',
                                '--output-dir', str(tmp_path)]):
            result = main()
        assert result == 1
        error_messages = [c.args[0] for c in mock_logger.error.call_args_list]
        assert any("non-empty list" in msg for msg in error_messages)

    def test_qb_data_value_not_a_list_exits_1_and_logs_error(self, tmp_path):
        self._build_valid_tree(tmp_path)
        qb_path = tmp_path / WEEKS_FOLDER / "week_01" / POSITION_JSON_FILES['QB']
        qb_path.write_text(json.dumps({"qb_data": {"oops": "dict"}}))
        mock_logger = MagicMock()
        with patch('validate_sim_data.get_logger', return_value=mock_logger), \
             patch('sys.argv', ['validate_sim_data.py', '--year', '2025',
                                '--output-dir', str(tmp_path)]):
            result = main()
        assert result == 1
        error_messages = [c.args[0] for c in mock_logger.error.call_args_list]
        assert any("non-empty list" in msg for msg in error_messages)

    def test_empty_csv_exits_1_and_logs_error(self, tmp_path):
        self._build_valid_tree(tmp_path)
        (tmp_path / GAME_DATA_FILE).write_text("")
        mock_logger = MagicMock()
        with patch('validate_sim_data.get_logger', return_value=mock_logger), \
             patch('sys.argv', ['validate_sim_data.py', '--year', '2025',
                                '--output-dir', str(tmp_path)]):
            result = main()
        assert result == 1
        error_messages = [c.args[0] for c in mock_logger.error.call_args_list]
        assert any("Empty CSV file" in msg and GAME_DATA_FILE in msg
                   for msg in error_messages)

    def test_output_dir_is_file_exits_1_and_logs_error(self, tmp_path):
        regular_file = tmp_path / "regular_file.txt"
        regular_file.write_text("")
        mock_logger = MagicMock()
        with patch('validate_sim_data.get_logger', return_value=mock_logger), \
             patch('sys.argv', ['validate_sim_data.py', '--year', '2025',
                                '--output-dir', str(regular_file)]):
            result = main()
        assert result == 1
        assert mock_logger.error.call_count == 1
        assert "is not a directory" in mock_logger.error.call_args_list[0].args[0]

    def test_coverage_check_is_called_with_the_output_dir(self, tmp_path):
        self._build_valid_tree(tmp_path)
        with patch('validate_sim_data.check_coverage', return_value=True) as mock_coverage, \
             patch('validate_sim_data.get_logger', return_value=MagicMock()), \
             patch('sys.argv', ['validate_sim_data.py', '--year', '2025',
                                '--output-dir', str(tmp_path)]):
            result = main()
        assert result == 0
        assert mock_coverage.call_count == 1
        assert mock_coverage.call_args.args[0] == tmp_path

    def test_coverage_check_result_now_decides_the_exit_code(self, tmp_path):
        # Arrange - the inverted form of D8.2's idle guard, rewritten in place
        # rather than deleted so the cutover shows up in the diff as a reversed
        # assertion instead of a vanished guard. Before D8.3 this asserted 0.
        self._build_valid_tree(tmp_path)

        # Act
        with patch('validate_sim_data.check_coverage', return_value=False), \
             patch('validate_sim_data.get_logger', return_value=MagicMock()), \
             patch('sys.argv', ['validate_sim_data.py', '--year', '2025',
                                '--output-dir', str(tmp_path)]):
            result = main()

        # Assert - a structurally valid tree still exits 1 on a coverage failure,
        # which is only possible if the result is an operand of all_passed.
        assert result == 1

    def test_exit_code_and_verdict_survive_a_coverage_decode_error(self, tmp_path):
        # Arrange - a non-UTF-8 position file surfaces as UnicodeDecodeError,
        # which check_coverage must absorb rather than let escape past main().
        self._build_valid_tree(tmp_path)
        mock_logger = MagicMock()
        decode_error = UnicodeDecodeError('utf-8', b'\xff', 0, 1, 'invalid start byte')

        # Act
        with patch('simulation.shared.sim_data_coverage.compute_season_coverage',
                   side_effect=decode_error), \
             patch('validate_sim_data.get_logger', return_value=mock_logger), \
             patch('sys.argv', ['validate_sim_data.py', '--year', '2025',
                                '--output-dir', str(tmp_path)]):
            result = main()

        # Assert - identical exit code AND the verdict line still printed
        assert result == 0
        info_messages = [c.args[0] for c in mock_logger.info.call_args_list]
        assert "All validation checks passed." in info_messages

    def test_an_unhandled_coverage_exception_is_not_swallowed_at_the_call_site(self, tmp_path):
        # Arrange - pins the deliberate design: the exception-tightness fix lives
        # in check_coverage's own arms, NOT in a bare-Exception guard at the call
        # site (CODING_STANDARDS discourages bare Exception). If a future change
        # adds such a guard, this test fails and the decision gets re-made openly.
        self._build_valid_tree(tmp_path)

        # Act / Assert
        with patch('validate_sim_data.check_coverage', side_effect=RuntimeError('boom')), \
             patch('validate_sim_data.get_logger', return_value=MagicMock()), \
             patch('sys.argv', ['validate_sim_data.py', '--year', '2025',
                                '--output-dir', str(tmp_path)]):
            with pytest.raises(RuntimeError, match='boom'):
                main()

    def test_enable_log_file_passes_log_to_file_true(self, tmp_path):
        self._build_valid_tree(tmp_path)
        with patch('validate_sim_data.setup_logger') as mock_setup, \
             patch('validate_sim_data.get_logger', return_value=MagicMock()), \
             patch('sys.argv', ['validate_sim_data.py', '--year', '2025',
                                '--output-dir', str(tmp_path), '--enable-log-file']):
            main()
        assert mock_setup.call_args.kwargs['log_to_file'] is True
