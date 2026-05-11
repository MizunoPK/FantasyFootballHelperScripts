"""
Unit Tests for validate_sim_data.py

Tests CLI validation, CSV file checks, week folder checks, JSON spot-checks,
and exit codes for the validate_sim_data feature.
"""

import json
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

from historical_data_compiler.constants import (
    SEASON_SCHEDULE_FILE,
    GAME_DATA_FILE,
    TEAM_DATA_FOLDER,
    WEEKS_FOLDER,
    VALIDATION_WEEKS,
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
        for i in range(32):
            (team_dir / f"team_{i:02d}.csv").write_text("abbrev,name\n")
        weeks_dir = base_dir / WEEKS_FOLDER
        weeks_dir.mkdir()
        for w in range(1, VALIDATION_WEEKS + 1):
            week_dir = weeks_dir / f"week_{w:02d}"
            week_dir.mkdir()
            for pos, fname in POSITION_JSON_FILES.items():
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
        assert mock_logger.error.called

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
        assert mock_logger.error.called

    def test_missing_week_folder_exits_1_and_logs_error(self, tmp_path):
        self._build_valid_tree(tmp_path)
        shutil.rmtree(tmp_path / WEEKS_FOLDER / "week_18")
        mock_logger = MagicMock()
        with patch('validate_sim_data.get_logger', return_value=mock_logger), \
             patch('sys.argv', ['validate_sim_data.py', '--year', '2025',
                                '--output-dir', str(tmp_path)]):
            result = main()
        assert result == 1
        assert mock_logger.error.called

    def test_missing_json_file_exits_1_and_logs_error(self, tmp_path):
        self._build_valid_tree(tmp_path)
        (tmp_path / WEEKS_FOLDER / "week_01" / POSITION_JSON_FILES['RB']).unlink()
        mock_logger = MagicMock()
        with patch('validate_sim_data.get_logger', return_value=mock_logger), \
             patch('sys.argv', ['validate_sim_data.py', '--year', '2025',
                                '--output-dir', str(tmp_path)]):
            result = main()
        assert result == 1
        assert mock_logger.error.called

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
        assert mock_logger.error.called

    def test_output_dir_not_found_exits_1_and_logs_error(self, tmp_path):
        nonexistent = tmp_path / "does_not_exist"
        mock_logger = MagicMock()
        with patch('validate_sim_data.get_logger', return_value=mock_logger), \
             patch('sys.argv', ['validate_sim_data.py', '--year', '2025',
                                '--output-dir', str(nonexistent)]):
            result = main()
        assert result == 1
        assert mock_logger.error.called
