"""
Tests for PlayerManager.load_players_from_json() method - Task 4.4, 4.5, 4.6

Tests verify JSON-based player data loading functionality including:
- Success path (all 6 position files load correctly)
- Error handling (missing directory, malformed JSON, invalid players)
- Round-trip preservation (nested stats survive save/load cycle)

Author: Claude Code (Sub-Feature 1: Core Data Loading)
Date: 2025-12-28
"""

import pytest
import json
from pathlib import Path
from unittest.mock import Mock, MagicMock

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
        "description": "Test configuration for JSON loading tests",
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
                "actual_points": [0.0] * 17,
                "passing": {
                    "completions": [22.5] * 17,
                    "attempts": [35.0] * 17
                }
            },
            {
                "id": "12346",
                "name": "Josh Allen",
                "team": "BUF",
                "position": "QB",
                "bye_week": 12,
                "drafted_by": "Sea Sharp",
                "locked": False,
                "projected_points": [24.0] * 17,
                "actual_points": [0.0] * 17
            }
        ]
    }
    qb_file = player_data_dir / "qb_data.json"
    qb_file.write_text(json.dumps(qb_data))

    rb_data = {
        "rb_data": [
            {
                "id": "23456",
                "name": "Christian McCaffrey",
                "team": "SF",
                "position": "RB",
                "bye_week": 9,
                "drafted_by": "Opponent Team",
                "locked": False,
                "projected_points": [18.5] * 17,
                "actual_points": [0.0] * 17,
                "rushing": {
                    "rush_att": [20.0] * 17,
                    "rush_yds": [95.0] * 17
                },
                "receiving": {
                    "receptions": [4.5] * 17,
                    "rec_yds": [35.0] * 17
                }
            }
        ]
    }
    rb_file = player_data_dir / "rb_data.json"
    rb_file.write_text(json.dumps(rb_data))

    for position in ["wr", "te", "k", "dst"]:
        position_data = {f"{position}_data": []}
        position_file = player_data_dir / f"{position}_data.json"
        position_file.write_text(json.dumps(position_data))

    for week in range(1, 18):
        teams_file = data_folder / f"teams_week_{week}.csv"
        teams_file.write_text("Team,OFF,DEF,DST\nKC,1,15,8\nBUF,3,12,10\nSF,2,5,3\n")

    return data_folder


@pytest.fixture
def mock_config():
    """Create mock ConfigManager."""
    mock = Mock()
    mock.current_nfl_week = 1
    mock.max_positions = {"QB": 2, "RB": 4, "WR": 4, "TE": 1, "K": 1, "DST": 1}
    return mock


@pytest.fixture
def mock_team_data_manager():
    """Create mock TeamDataManager."""
    return Mock()


@pytest.fixture
def mock_season_schedule_manager():
    """Create mock SeasonScheduleManager."""
    mock = Mock()
    mock.get_opponent.return_value = "DAL"
    return mock


class TestPlayerManagerLoadFromJSON:
    """Test suite for PlayerManager.load_players_from_json() - Task 4.4, 4.5"""

    def test_load_players_from_json_success_all_files(self, mock_data_folder, mock_config, mock_team_data_manager, mock_season_schedule_manager):
        """Test load_players_from_json() successfully loads all 6 position files."""
        player_manager = PlayerManager.__new__(PlayerManager)
        player_manager.data_folder = mock_data_folder
        player_manager.config = mock_config
        player_manager.team_data_manager = mock_team_data_manager
        player_manager.season_schedule_manager = mock_season_schedule_manager
        player_manager.players = []
        player_manager.max_projection = 0.0
        player_manager.logger = Mock()

        player_manager.load_team = Mock()

        result = player_manager.load_players_from_json()

        assert result == True
        assert len(player_manager.players) == 3
        assert player_manager.load_team.called

        player_names = [p.name for p in player_manager.players]
        assert "Patrick Mahomes" in player_names
        assert "Josh Allen" in player_names
        assert "Christian McCaffrey" in player_names

    def test_load_players_from_json_combines_all_positions(self, mock_data_folder, mock_config, mock_team_data_manager, mock_season_schedule_manager):
        """Test load_players_from_json() combines players from all position files."""
        player_manager = PlayerManager.__new__(PlayerManager)
        player_manager.data_folder = mock_data_folder
        player_manager.config = mock_config
        player_manager.team_data_manager = mock_team_data_manager
        player_manager.season_schedule_manager = mock_season_schedule_manager
        player_manager.players = []
        player_manager.max_projection = 0.0
        player_manager.logger = Mock()
        player_manager.load_team = Mock()

        player_manager.load_players_from_json()

        positions = [p.position for p in player_manager.players]
        assert "QB" in positions
        assert "RB" in positions

    def test_load_players_from_json_calculates_max_projection(self, mock_data_folder, mock_config, mock_team_data_manager, mock_season_schedule_manager):
        """Test load_players_from_json() calculates max_projection correctly."""
        player_manager = PlayerManager.__new__(PlayerManager)
        player_manager.data_folder = mock_data_folder
        player_manager.config = mock_config
        player_manager.team_data_manager = mock_team_data_manager
        player_manager.season_schedule_manager = mock_season_schedule_manager
        player_manager.players = []
        player_manager.max_projection = 0.0
        player_manager.logger = Mock()
        player_manager.load_team = Mock()

        player_manager.load_players_from_json()

        expected_max = 25.0 * 17
        assert player_manager.max_projection == expected_max

    def test_load_players_from_json_preserves_drafted_by_conversions(self, mock_data_folder, mock_config, mock_team_data_manager, mock_season_schedule_manager):
        """Test load_players_from_json() converts drafted_by correctly."""
        player_manager = PlayerManager.__new__(PlayerManager)
        player_manager.data_folder = mock_data_folder
        player_manager.config = mock_config
        player_manager.team_data_manager = mock_team_data_manager
        player_manager.season_schedule_manager = mock_season_schedule_manager
        player_manager.players = []
        player_manager.max_projection = 0.0
        player_manager.logger = Mock()
        player_manager.load_team = Mock()

        player_manager.load_players_from_json()

        mahomes = next(p for p in player_manager.players if p.name == "Patrick Mahomes")
        allen = next(p for p in player_manager.players if p.name == "Josh Allen")
        mccaffrey = next(p for p in player_manager.players if p.name == "Christian McCaffrey")

        assert mahomes.drafted_by == ""
        assert allen.drafted_by == "Sea Sharp"
        assert mccaffrey.drafted_by == "Opponent Team"

    def test_load_players_from_json_missing_directory_raises_file_not_found(self, tmp_path):
        """Test load_players_from_json() raises FileNotFoundError if player_data directory missing."""
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        player_manager = PlayerManager.__new__(PlayerManager)
        player_manager.data_folder = data_folder
        player_manager.config = Mock()
        player_manager.team_data_manager = Mock()
        player_manager.season_schedule_manager = Mock()
        player_manager.players = []
        player_manager.max_projection = 0.0
        player_manager.logger = Mock()

        with pytest.raises(FileNotFoundError, match="Player data directory not found"):
            player_manager.load_players_from_json()

    def test_load_players_from_json_malformed_json_raises_decode_error(self, mock_data_folder, mock_config, mock_team_data_manager, mock_season_schedule_manager):
        """Test load_players_from_json() raises JSONDecodeError for malformed JSON."""
        player_data_dir = mock_data_folder / "player_data"
        malformed_file = player_data_dir / "qb_data.json"
        malformed_file.write_text("{invalid json content")

        player_manager = PlayerManager.__new__(PlayerManager)
        player_manager.data_folder = mock_data_folder
        player_manager.config = mock_config
        player_manager.team_data_manager = mock_team_data_manager
        player_manager.season_schedule_manager = mock_season_schedule_manager
        player_manager.players = []
        player_manager.max_projection = 0.0
        player_manager.logger = Mock()

        with pytest.raises(json.JSONDecodeError):
            player_manager.load_players_from_json()

    def test_load_players_from_json_missing_position_file_logs_warning_continues(self, mock_data_folder, mock_config, mock_team_data_manager, mock_season_schedule_manager):
        """Test load_players_from_json() logs warning and continues if position file missing."""
        player_data_dir = mock_data_folder / "player_data"
        wr_file = player_data_dir / "wr_data.json"
        wr_file.unlink()

        player_manager = PlayerManager.__new__(PlayerManager)
        player_manager.data_folder = mock_data_folder
        player_manager.config = mock_config
        player_manager.team_data_manager = mock_team_data_manager
        player_manager.season_schedule_manager = mock_season_schedule_manager
        player_manager.players = []
        player_manager.max_projection = 0.0
        player_manager.logger = Mock()
        player_manager.load_team = Mock()

        result = player_manager.load_players_from_json()

        assert result == True
        player_manager.logger.warning.assert_called_with("Position file not found: wr_data.json")
        assert len(player_manager.players) == 3

    def test_load_players_from_json_invalid_player_skips_with_warning(self, mock_data_folder, mock_config, mock_team_data_manager, mock_season_schedule_manager):
        """Test load_players_from_json() skips invalid player and logs warning."""
        player_data_dir = mock_data_folder / "player_data"
        qb_file = player_data_dir / "qb_data.json"
        qb_data = json.loads(qb_file.read_text())
        qb_data["qb_data"].append({
            "id": "99999",
            "team": "KC",
            "position": "QB"
        })
        qb_file.write_text(json.dumps(qb_data))

        player_manager = PlayerManager.__new__(PlayerManager)
        player_manager.data_folder = mock_data_folder
        player_manager.config = mock_config
        player_manager.team_data_manager = mock_team_data_manager
        player_manager.season_schedule_manager = mock_season_schedule_manager
        player_manager.players = []
        player_manager.max_projection = 0.0
        player_manager.logger = Mock()
        player_manager.load_team = Mock()

        result = player_manager.load_players_from_json()

        assert result == True
        assert len(player_manager.players) == 3
        player_manager.logger.warning.assert_called()


class TestRoundTripPreservation:
    """Test suite for round-trip preservation - Task 4.6"""

    def test_round_trip_preservation_nested_stats(self, mock_data_folder, mock_config, mock_team_data_manager, mock_season_schedule_manager):
        """Test that nested stats survive load → modify → save → load cycle."""
        passing_stats = {
            "completions": [22.5, 23.0, 21.5] + [22.0] * 14,
            "attempts": [35.0, 36.0, 34.0] + [35.5] * 14,
            "pass_yds": [320.0, 315.0, 305.0] + [310.0] * 14,
            "pass_tds": [2.5, 2.8, 2.3] + [2.6] * 14,
            "interceptions": [0.8, 0.7, 0.9] + [0.75] * 14
        }

        rushing_stats = {
            "rush_att": [3.0, 4.0, 2.0] + [3.5] * 14,
            "rush_yds": [15.0, 20.0, 10.0] + [12.0] * 14,
            "rush_tds": [0.1, 0.15, 0.05] + [0.1] * 14
        }

        player_data = {
            "id": "12345",
            "name": "Patrick Mahomes",
            "team": "KC",
            "position": "QB",
            "bye_week": 7,
            "drafted_by": "",
            "locked": False,
            "projected_points": [25.3, 28.1, 22.5] + [24.0] * 14,
            "actual_points": [26.0, 27.5, 23.0] + [0.0] * 14,
            "passing": passing_stats,
            "rushing": rushing_stats,
            "misc": {
                "fumbles_lost": [0.2, 0.1, 0.3] + [0.15] * 14
            }
        }

        player = FantasyPlayer.from_json(player_data)

        assert player.passing == passing_stats
        assert player.rushing == rushing_stats
        assert player.misc["fumbles_lost"][0] == 0.2
        assert player.misc["fumbles_lost"][1] == 0.1

        assert player.projected_points[0] == 25.3
        assert player.projected_points[1] == 28.1
        assert player.actual_points[0] == 26.0

        original_passing = player.passing.copy()
        player.drafted_by = "Sea Sharp"
        player.locked = True

        player_dict = player.to_dict()

        assert player_dict["passing"] == original_passing
        assert player_dict["rushing"] == rushing_stats
        assert player_dict["projected_points"][0] == 25.3

        reloaded_player = FantasyPlayer.from_json(player_dict)

        assert reloaded_player.passing == passing_stats
        assert reloaded_player.rushing == rushing_stats
        assert reloaded_player.misc["fumbles_lost"] == player_data["misc"]["fumbles_lost"]
        assert reloaded_player.projected_points == player_data["projected_points"]
        assert reloaded_player.drafted_by == "Sea Sharp"
        assert reloaded_player.locked == True


class TestUpdatePlayersFileSelectiveUpdate:
    """
    Test update_players_file() selective JSON updates.

    Spec Reference: sub_feature_04_file_update_strategy_spec.md
    Tasks: 4.4 (round-trip preservation)
    """

    def test_round_trip_preservation_only_drafted_locked_updated(self, mock_data_folder, mock_config, mock_team_data_manager, mock_season_schedule_manager):
        """
        Test Task 4.4: Round-trip preservation of all fields except drafted_by/locked.

        Load → update drafted/locked → save → reload → verify stats unchanged.
        """
        player_data_dir = mock_data_folder / "player_data"
        player_data_dir.mkdir(exist_ok=True)

        qb_data = {
            "qb_data": [{
                "id": 1,
                "name": "Test QB",
                "team": "KC",
                "position": "QB",
                "bye_week": 7,
                "injury_status": "Healthy",
                "average_draft_position": 1.5,
                "player_rating": 95,
                "drafted_by": "",
                "locked": False,
                "projected_points": [25.0] * 17,
                "actual_points": [22.0] * 17,
                "passing": {
                    "attempts": 600,
                    "completions": 420,
                    "yards": 5000,
                    "touchdowns": 40,
                    "interceptions": 8
                },
                "rushing": {"attempts": 50, "yards": 250, "touchdowns": 3},
                "misc": {"fumbles_lost": 2}
            }]
        }

        with open(player_data_dir / "qb_data.json", 'w') as f:
            json.dump(qb_data, f)

        for pos in ['rb', 'wr', 'te', 'k', 'dst']:
            with open(player_data_dir / f"{pos}_data.json", 'w') as f:
                json.dump({f"{pos}_data": []}, f)

        pm = PlayerManager.__new__(PlayerManager)
        pm.data_folder = mock_data_folder
        pm.config = mock_config
        pm.team_data_manager = mock_team_data_manager
        pm.season_schedule_manager = mock_season_schedule_manager
        pm.players = []
        pm.max_projection = 0.0
        pm.logger = Mock()
        pm.load_team = Mock()

        pm.load_players_from_json()

        assert len(pm.players) == 1
        player = pm.players[0]

        original_projected = player.projected_points.copy()
        original_actual = player.actual_points.copy()
        original_passing = player.passing.copy()
        original_rushing = player.rushing.copy()

        player.drafted_by = "Sea Sharp"
        player.locked = True

        result = pm.update_players_file()

        assert "successfully" in result.lower()

        pm.load_players_from_json()

        assert len(pm.players) == 1
        reloaded_player = pm.players[0]

        assert reloaded_player.drafted_by == "Sea Sharp"
        assert reloaded_player.locked == True

        assert reloaded_player.projected_points == original_projected
        assert reloaded_player.actual_points == original_actual
        assert reloaded_player.passing == original_passing
        assert reloaded_player.rushing == original_rushing
        assert reloaded_player.name == "Test QB"
        assert reloaded_player.team == "KC"
        assert reloaded_player.position == "QB"
        assert reloaded_player.bye_week == 7
        assert reloaded_player.average_draft_position == 1.5
        assert reloaded_player.player_rating == 95

    def test_selective_update_preserves_opponent_team_name(self, mock_data_folder, mock_config, mock_team_data_manager, mock_season_schedule_manager):
        """
        Test Task 2.1: Verify drafted=1 (opponent) preserves team name.

        When drafted_by="Opponent Team", drafted_by should NOT be overwritten (preserve opponent name).
        """
        player_data_dir = mock_data_folder / "player_data"
        player_data_dir.mkdir(exist_ok=True)

        qb_data = {
            "qb_data": [{
                "id": 1,
                "name": "Test QB",
                "team": "KC",
                "position": "QB",
                "bye_week": 7,
                "drafted_by": "Opponent Team",
                "locked": False,
                "projected_points": [20.0] * 17,
                "actual_points": [18.0] * 17
            }]
        }

        with open(player_data_dir / "qb_data.json", 'w') as f:
            json.dump(qb_data, f)

        for pos in ['rb', 'wr', 'te', 'k', 'dst']:
            with open(player_data_dir / f"{pos}_data.json", 'w') as f:
                json.dump({f"{pos}_data": []}, f)

        pm = PlayerManager.__new__(PlayerManager)
        pm.data_folder = mock_data_folder
        pm.config = mock_config
        pm.team_data_manager = mock_team_data_manager
        pm.season_schedule_manager = mock_season_schedule_manager
        pm.players = []
        pm.max_projection = 0.0
        pm.logger = Mock()
        pm.load_team = Mock()

        pm.load_players_from_json()

        player = pm.players[0]
        assert player.drafted_by == "Opponent Team"

        player.locked = True
        pm.update_players_file()

        pm.load_players_from_json()
        player = pm.players[0]

        assert player.drafted_by == "Opponent Team"
        assert player.locked == True

        with open(player_data_dir / "qb_data.json", 'r') as f:
            qb_data_after = json.load(f)

        assert qb_data_after["qb_data"][0]["drafted_by"] == "Opponent Team"


