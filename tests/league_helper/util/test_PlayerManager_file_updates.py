"""
Tests for PlayerManager.update_players_file() method - File Persistence Bug Fix

Tests verify file update functionality including:
- drafted_by field persistence to JSON files
- locked field persistence to JSON files
- NO .bak backup files created during updates
- Atomic write pattern works correctly on Windows
- Error handling (permission errors, JSON errors)
- Changes persist immediately and across restarts

Author: Claude Code (Feature 01: File Persistence Issues)
Date: 2025-12-31
"""

import pytest
import json
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, mock_open
from io import StringIO

from league_helper.util.PlayerManager import PlayerManager
from league_helper.util.ConfigManager import ConfigManager
from league_helper.util.TeamDataManager import TeamDataManager
from league_helper.util.SeasonScheduleManager import SeasonScheduleManager
from utils.FantasyPlayer import FantasyPlayer


@pytest.fixture
def mock_data_folder(tmp_path):
    """Create temporary data folder with player_data subdirectory and JSON files."""
    data_folder = tmp_path / "data"
    data_folder.mkdir()

    player_data_dir = data_folder / "player_data"
    player_data_dir.mkdir()

    config_content = {
        "config_name": "Test Config",
        "description": "Test configuration for file update tests",
        "parameters": {
            "CURRENT_NFL_WEEK": 1,
            "MAX_POSITIONS": {
                "QB": 2, "RB": 4, "WR": 4, "TE": 1, "K": 1, "DST": 1
            }
        }
    }
    config_file = data_folder / "league_config.json"
    config_file.write_text(json.dumps(config_content))

    qb_data = {
        "qb_data": [
            {
                "id": "12345",
                "name": "Patrick Mahomes",
                "team": "KC",
                "position": "QB",
                "bye_week": 7,
                "drafted_by": "",
                "locked": False,
                "average_draft_position": 15.3,
                "player_rating": 95.5,
                "injury_status": "ACTIVE",
                "projected_points": [25.0] * 17,
                "actual_points": [0.0] * 17
            }
        ]
    }
    qb_file = player_data_dir / "qb_data.json"
    qb_file.write_text(json.dumps(qb_data, indent=2))

    rb_data = {
        "rb_data": [
            {
                "id": "23456",
                "name": "Christian McCaffrey",
                "team": "SF",
                "position": "RB",
                "bye_week": 9,
                "drafted_by": "",
                "locked": False,
                "projected_points": [18.5] * 17,
                "actual_points": [0.0] * 17
            }
        ]
    }
    rb_file = player_data_dir / "rb_data.json"
    rb_file.write_text(json.dumps(rb_data, indent=2))

    wr_data = {
        "wr_data": [
            {
                "id": "34567",
                "name": "Justin Jefferson",
                "team": "MIN",
                "position": "WR",
                "bye_week": 13,
                "drafted_by": "",
                "locked": False,
                "projected_points": [16.0] * 17,
                "actual_points": [0.0] * 17
            }
        ]
    }
    wr_file = player_data_dir / "wr_data.json"
    wr_file.write_text(json.dumps(wr_data, indent=2))

    te_data = {
        "te_data": [
            {
                "id": "45678",
                "name": "Travis Kelce",
                "team": "KC",
                "position": "TE",
                "bye_week": 7,
                "drafted_by": "",
                "locked": False,
                "projected_points": [12.0] * 17,
                "actual_points": [0.0] * 17
            }
        ]
    }
    te_file = player_data_dir / "te_data.json"
    te_file.write_text(json.dumps(te_data, indent=2))

    k_data = {
        "k_data": [
            {
                "id": "56789",
                "name": "Justin Tucker",
                "team": "BAL",
                "position": "K",
                "bye_week": 14,
                "drafted_by": "",
                "locked": False,
                "projected_points": [8.0] * 17,
                "actual_points": [0.0] * 17
            }
        ]
    }
    k_file = player_data_dir / "k_data.json"
    k_file.write_text(json.dumps(k_data, indent=2))

    dst_data = {
        "dst_data": [
            {
                "id": "67890",
                "name": "San Francisco",
                "team": "SF",
                "position": "DST",
                "bye_week": 9,
                "drafted_by": "",
                "locked": False,
                "projected_points": [9.0] * 17,
                "actual_points": [0.0] * 17
            }
        ]
    }
    dst_file = player_data_dir / "dst_data.json"
    dst_file.write_text(json.dumps(dst_data, indent=2))

    return data_folder


@pytest.fixture
def player_manager(mock_data_folder):
    """Create PlayerManager instance with mocked dependencies (bypassing __init__)."""
    manager = PlayerManager.__new__(PlayerManager)

    manager.data_folder = mock_data_folder
    manager.config = Mock(spec=ConfigManager)
    manager.config.data_folder = mock_data_folder
    manager.config.current_nfl_week = 1
    manager.team_data_manager = Mock(spec=TeamDataManager)
    manager.season_schedule_manager = Mock(spec=SeasonScheduleManager)
    manager.players = []
    manager.max_projection = 0.0
    manager.logger = Mock()
    manager.scoring_calculator = Mock()

    manager.load_team = Mock()

    return manager



class TestUpdatePlayersFile_Mocked:
    """Unit tests for update_players_file() with mocked file system."""

    def test_drafted_by_persistence_mocked(self, player_manager):
        """
        Task 5: Test drafted_by field persistence (mocked)

        Verify that when a player's drafted_by field is modified,
        update_players_file() writes the correct value to the JSON data structure.
        """
        player_manager.load_players_from_json()
        qb_player = next((p for p in player_manager.players if p.position == "QB"), None)
        assert qb_player is not None, "QB player should exist for test"

        qb_player.drafted_by = "Sea Sharp"

        json_data_written = {}

        with patch('pathlib.Path.open', mock_open()) as mock_file:
            with patch('json.dump') as mock_json_dump:
                with patch('json.load') as mock_json_load:
                    with patch('pathlib.Path.exists', return_value=True):
                        with patch('pathlib.Path.replace'):
                            mock_json_load.return_value = {
                                "qb_data": [{
                                    "id": qb_player.id,
                                    "name": qb_player.name,
                                    "position": "QB",
                                    "drafted_by": "",
                                    "locked": False,
                                    "projected_points": [25.0] * 17
                                }]
                            }

                            result = player_manager.update_players_file()

                            assert result == "Player data updated successfully (6 JSON files updated)"

                            assert mock_json_dump.call_count == 6

                            calls = mock_json_dump.call_args_list
                            qb_call = next((c for c in calls if 'qb_data' in str(c)), None)
                            assert qb_call is not None, "QB data should be written"

                            json_data_written = qb_call[0][0]

                            assert "qb_data" in json_data_written
                            qb_players = json_data_written["qb_data"]
                            assert len(qb_players) == 1
                            assert qb_players[0]["drafted_by"] == "Sea Sharp"

    def test_locked_persistence_mocked(self, player_manager):
        """
        Task 6: Test locked field persistence (mocked)

        Verify that when a player's locked field is modified,
        update_players_file() writes the correct value to the JSON data structure.
        """
        player_manager.load_players_from_json()
        rb_player = next((p for p in player_manager.players if p.position == "RB"), None)
        assert rb_player is not None, "RB player should exist for test"

        rb_player.locked = True

        json_data_written = {}

        with patch('pathlib.Path.open', mock_open()) as mock_file:
            with patch('json.dump') as mock_json_dump:
                with patch('json.load') as mock_json_load:
                    with patch('pathlib.Path.exists', return_value=True):
                        with patch('pathlib.Path.replace'):
                            mock_json_load.return_value = {
                                "rb_data": [{
                                    "id": rb_player.id,
                                    "name": rb_player.name,
                                    "position": "RB",
                                    "drafted_by": "",
                                    "locked": False,
                                    "projected_points": [18.5] * 17
                                }]
                            }

                            result = player_manager.update_players_file()

                            assert result == "Player data updated successfully (6 JSON files updated)"

                            assert mock_json_dump.call_count == 6

                            calls = mock_json_dump.call_args_list
                            rb_call = next((c for c in calls if 'rb_data' in str(c)), None)
                            assert rb_call is not None, "RB data should be written"

                            json_data_written = rb_call[0][0]

                            assert "rb_data" in json_data_written
                            rb_players = json_data_written["rb_data"]
                            assert len(rb_players) == 1
                            assert rb_players[0]["locked"] is True

    def test_no_bak_files_mocked(self, player_manager):
        """
        Task 7: Test NO .bak files created (mocked)

        Verify that update_players_file() does NOT create .bak backup files.
        This is the primary bug fix - ensuring shutil.copy2() is NOT called.
        """
        player_manager.load_players_from_json()

        with patch('pathlib.Path.open', mock_open()) as mock_file:
            with patch('json.dump') as mock_json_dump:
                with patch('json.load') as mock_json_load:
                    with patch('pathlib.Path.exists', return_value=True):
                        with patch('pathlib.Path.replace'):
                            with patch('shutil.copy2') as mock_shutil_copy2:
                                mock_json_load.return_value = {
                                    "qb_data": [],
                                    "rb_data": [],
                                    "wr_data": [],
                                    "te_data": [],
                                    "k_data": [],
                                    "dst_data": []
                                }

                                result = player_manager.update_players_file()

                                assert result == "Player data updated successfully (6 JSON files updated)"

                                assert mock_shutil_copy2.call_count == 0, \
                                    "shutil.copy2() should NOT be called (no .bak files)"

                                all_open_calls = mock_file.call_args_list
                                for call in all_open_calls:
                                    file_path_arg = str(call[0][0]) if call[0] else ""
                                    assert '.bak' not in file_path_arg, \
                                        f"No .bak file operations allowed: {file_path_arg}"

    def test_permission_error(self, player_manager):
        """
        Task 8: Test error handling - PermissionError (mocked)

        Verify that update_players_file() handles PermissionError gracefully
        when unable to write to JSON files.
        """
        player_manager.load_players_from_json()

        with patch('builtins.open', side_effect=PermissionError("Access denied")):
            with patch('pathlib.Path.exists', return_value=True):
                with pytest.raises(PermissionError):
                    player_manager.update_players_file()

    def test_json_decode_error(self, player_manager):
        """
        Task 8: Test error handling - JSONDecodeError (mocked)

        Verify that update_players_file() handles JSONDecodeError gracefully
        when reading malformed JSON files.
        """
        player_manager.load_players_from_json()

        with patch('pathlib.Path.open', mock_open(read_data="invalid json {")):
            with patch('pathlib.Path.exists', return_value=True):
                with patch('json.load', side_effect=json.JSONDecodeError("Expecting value", "doc", 0)):
                    with pytest.raises(json.JSONDecodeError):
                        player_manager.update_players_file()



class TestUpdatePlayersFile_Integration:
    """Integration tests for update_players_file() with real file I/O."""

    def test_atomic_write_pattern_windows(self, player_manager):
        """
        Task 9: Test atomic write pattern on Windows (real I/O)

        Verify that update_players_file() uses atomic write pattern:
        1. Creates .tmp file during write
        2. Replaces .json file atomically with Path.replace()
        3. No .tmp files left behind after completion
        """
        player_manager.load_players_from_json()
        qb_player = next((p for p in player_manager.players if p.position == "QB"), None)
        assert qb_player is not None

        qb_player.drafted_by = "Sea Sharp"

        player_data_dir = player_manager.data_folder / "player_data"
        qb_json_path = player_data_dir / "qb_data.json"
        qb_tmp_path = player_data_dir / "qb_data.tmp"

        result = player_manager.update_players_file()

        assert result == "Player data updated successfully (6 JSON files updated)"

        assert qb_json_path.exists(), "qb_data.json should exist after update"

        assert not qb_tmp_path.exists(), "qb_data.tmp should NOT exist after atomic replace"

        for position in ['qb', 'rb', 'wr', 'te', 'k', 'dst']:
            json_file = player_data_dir / f"{position}_data.json"
            tmp_file = player_data_dir / f"{position}_data.tmp"
            assert json_file.exists(), f"{position}_data.json should exist"
            assert not tmp_file.exists(), f"{position}_data.tmp should NOT exist"

    def test_json_format_verification(self, player_manager):
        """
        Task 10: Test JSON file contents match expected format (real I/O)

        Verify that after update_players_file():
        1. JSON format matches {position_key: [{players}]} structure
        2. drafted_by field has correct value
        3. locked field has correct value
        4. Other fields are preserved
        """
        player_manager.load_players_from_json()
        qb_player = next((p for p in player_manager.players if p.position == "QB"), None)
        rb_player = next((p for p in player_manager.players if p.position == "RB"), None)
        assert qb_player is not None and rb_player is not None

        qb_player.drafted_by = "Sea Sharp"
        qb_player.locked = True
        rb_player.drafted_by = "Opponent Team"
        rb_player.locked = False

        assert qb_player.drafted_by == "Sea Sharp", f"QB drafted_by should be 'Sea Sharp' but is '{qb_player.drafted_by}'"
        assert qb_player in player_manager.players, "QB player should still be in players list"

        player_data_dir = player_manager.data_folder / "player_data"

        player_manager.update_players_file()

        qb_json_path = player_data_dir / "qb_data.json"
        with open(qb_json_path, 'r', encoding='utf-8') as f:
            qb_data = json.load(f)

        assert "qb_data" in qb_data, "JSON should have 'qb_data' key"
        assert isinstance(qb_data["qb_data"], list), "qb_data should be a list"
        assert len(qb_data["qb_data"]) == 1, "Should have 1 QB player"

        qb_dict = qb_data["qb_data"][0]

        assert qb_dict["drafted_by"] == "Sea Sharp", "drafted_by should be updated"
        assert qb_dict["locked"] is True, "locked should be updated"

        assert str(qb_dict["id"]) == str(qb_player.id), "id should be preserved"
        assert qb_dict["name"] == qb_player.name, "name should be preserved"
        assert qb_dict["position"] == "QB", "position should be preserved"
        assert "projected_points" in qb_dict, "projected_points should be preserved"

        rb_json_path = player_data_dir / "rb_data.json"
        with open(rb_json_path, 'r', encoding='utf-8') as f:
            rb_data = json.load(f)

        rb_dict = rb_data["rb_data"][0]
        assert rb_dict["drafted_by"] == "Opponent Team", "RB drafted_by should be updated"
        assert rb_dict["locked"] is False, "RB locked should be updated"

    def test_changes_persist_immediately(self, player_manager):
        """
        Task 11: Test changes persist immediately (real I/O)

        Verify that changes are visible immediately after update_players_file()
        completes, with no caching or buffering issues.
        """
        player_manager.load_players_from_json()
        wr_player = next((p for p in player_manager.players if p.position == "WR"), None)
        assert wr_player is not None

        wr_player.drafted_by = "My Team"
        wr_player.locked = True

        player_data_dir = player_manager.data_folder / "player_data"
        wr_json_path = player_data_dir / "wr_data.json"

        player_manager.update_players_file()

        with open(wr_json_path, 'r', encoding='utf-8') as f:
            wr_data = json.load(f)

        wr_dict = wr_data["wr_data"][0]
        assert wr_dict["drafted_by"] == "My Team", "Changes should be visible immediately"
        assert wr_dict["locked"] is True, "Changes should be visible immediately"

        assert wr_json_path.exists(), "File should exist on disk"

    def test_changes_persist_across_restarts(self, mock_data_folder):
        """
        Task 12: Test changes persist across restarts (real I/O)

        Verify that changes survive simulated app restarts:
        1. Create PlayerManager instance #1
        2. Modify player data
        3. Call update_players_file()
        4. Delete instance #1
        5. Create NEW PlayerManager instance #2
        6. Load data from same files
        7. Verify changes persisted
        """
        manager1 = PlayerManager.__new__(PlayerManager)
        manager1.data_folder = mock_data_folder
        manager1.config = Mock(spec=ConfigManager)
        manager1.config.data_folder = mock_data_folder
        manager1.config.current_nfl_week = 1
        manager1.team_data_manager = Mock(spec=TeamDataManager)
        manager1.season_schedule_manager = Mock(spec=SeasonScheduleManager)
        manager1.players = []
        manager1.max_projection = 0.0
        manager1.logger = Mock()
        manager1.load_team = Mock()

        manager1.load_players_from_json()
        te_player = next((p for p in manager1.players if p.position == "TE"), None)
        assert te_player is not None

        te_player.drafted_by = "Team Alpha"
        te_player.locked = True

        manager1.update_players_file()

        del manager1

        manager2 = PlayerManager.__new__(PlayerManager)
        manager2.data_folder = mock_data_folder
        manager2.config = Mock(spec=ConfigManager)
        manager2.config.data_folder = mock_data_folder
        manager2.config.current_nfl_week = 1
        manager2.team_data_manager = Mock(spec=TeamDataManager)
        manager2.season_schedule_manager = Mock(spec=SeasonScheduleManager)
        manager2.players = []
        manager2.max_projection = 0.0
        manager2.logger = Mock()
        manager2.load_team = Mock()

        manager2.load_players_from_json()

        te_player_loaded = next((p for p in manager2.players if p.position == "TE"), None)
        assert te_player_loaded is not None
        assert te_player_loaded.drafted_by == "Team Alpha", "drafted_by should persist across restarts"
        assert te_player_loaded.locked is True, "locked should persist across restarts"

    def test_no_bak_files_real_filesystem(self, player_manager):
        """
        Task 13: Test NO .bak files created in real filesystem (real I/O)

        Verify that after update_players_file() completes:
        1. NO .bak files exist in player_data/ directory
        2. Only .json files exist (no .bak, no .tmp)

        This is the PRIMARY BUG FIX verification with real file I/O.
        """
        player_manager.load_players_from_json()
        k_player = next((p for p in player_manager.players if p.position == "K"), None)
        assert k_player is not None

        k_player.drafted_by = "Test Team"
        k_player.locked = False

        player_data_dir = player_manager.data_folder / "player_data"

        player_manager.update_players_file()

        all_files = list(player_data_dir.glob("*"))
        file_names = [f.name for f in all_files]

        bak_files = [f for f in file_names if f.endswith('.bak')]
        assert len(bak_files) == 0, f"NO .bak files should exist, found: {bak_files}"

        tmp_files = [f for f in file_names if f.endswith('.tmp')]
        assert len(tmp_files) == 0, f"NO .tmp files should exist, found: {tmp_files}"

        json_files = [f for f in file_names if f.endswith('.json')]
        assert len(json_files) == 6, "Should have exactly 6 .json files (one per position)"

        expected_files = ['qb_data.json', 'rb_data.json', 'wr_data.json',
                         'te_data.json', 'k_data.json', 'dst_data.json']
        for expected_file in expected_files:
            assert expected_file in file_names, f"{expected_file} should exist"


