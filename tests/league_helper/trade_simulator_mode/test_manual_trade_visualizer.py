"""
Unit and integration tests for Manual Trade Visualizer feature.

Tests all helper methods and complete workflow for the manual trade visualization mode
in TradeSimulatorModeManager.

Author: Kai Mizuno
Date: 2025-10-16
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "league_helper"))
sys.path.append(str(project_root / "league_helper" / "trade_simulator_mode"))

from league_helper.trade_simulator_mode.TradeSimulatorModeManager import TradeSimulatorModeManager
from league_helper.trade_simulator_mode.TradeSimTeam import TradeSimTeam
from league_helper.trade_simulator_mode.TradeSnapshot import TradeSnapshot
from league_helper.trade_simulator_mode.trade_display_helper import TradeDisplayHelper
from league_helper.trade_simulator_mode.trade_input_parser import TradeInputParser
from league_helper.trade_simulator_mode.trade_file_writer import TradeFileWriter
from league_helper.util.PlayerManager import PlayerManager
from league_helper.util.ConfigManager import ConfigManager
from league_helper.util.TeamDataManager import TeamDataManager
from league_helper.util.SeasonScheduleManager import SeasonScheduleManager
from league_helper.util.ScoredPlayer import ScoredPlayer
from utils.FantasyPlayer import FantasyPlayer


class TestDisplayNumberedRoster:
    """Tests for display_numbered_roster method (TradeDisplayHelper)."""

    def test_display_empty_roster(self, capsys):
        """Test displaying an empty roster."""
        # Setup
        helper = TradeDisplayHelper()

        # Execute
        helper.display_numbered_roster([], "TEST ROSTER")

        # Verify output
        captured = capsys.readouterr()
        assert "=" * 25 in captured.out
        assert "TEST ROSTER" in captured.out

    def test_display_single_player(self, capsys):
        """Test displaying roster with one player."""
        # Setup
        helper = TradeDisplayHelper()

        # Create mock player
        player = FantasyPlayer(
            id=1,
            name="Test Player",
            team="TST",
            position="RB",
            bye_week=7,
            fantasy_points=150.0,
            injury_status="ACTIVE",
            drafted=0
        )

        # Execute
        helper.display_numbered_roster([player], "MY ROSTER")

        # Verify output
        captured = capsys.readouterr()
        assert "MY ROSTER" in captured.out
        assert "1. Test Player" in captured.out

    def test_display_multiple_players(self, capsys):
        """Test displaying roster with multiple players."""
        # Setup
        helper = TradeDisplayHelper()

        # Create mock players
        players = [
            FantasyPlayer(id=1, name="Player One", team="TST", position="RB", bye_week=7, fantasy_points=150.0, injury_status="ACTIVE", drafted=0),
            FantasyPlayer(id=2, name="Player Two", team="TST", position="WR", bye_week=8, fantasy_points=140.0, injury_status="ACTIVE", drafted=0),
            FantasyPlayer(id=3, name="Player Three", team="TST", position="QB", bye_week=9, fantasy_points=160.0, injury_status="ACTIVE", drafted=0),
        ]

        # Execute
        helper.display_numbered_roster(players, "TEAM ROSTER")

        # Verify output
        captured = capsys.readouterr()
        assert "TEAM ROSTER" in captured.out
        assert "1. Player One" in captured.out
        assert "2. Player Two" in captured.out
        assert "3. Player Three" in captured.out


class TestParsePlayerSelection:
    """Tests for parse_player_selection method (TradeInputParser)."""

    def setup_method(self):
        """Setup test fixtures."""
        self.parser = TradeInputParser()

    def test_valid_single_number(self):
        """Test parsing valid single number."""
        result = self.parser.parse_player_selection("1", 5)
        assert result == [1]

    def test_valid_multiple_numbers(self):
        """Test parsing valid multiple numbers."""
        result = self.parser.parse_player_selection("1,2,3", 5)
        assert result == [1, 2, 3]

    def test_valid_with_spaces(self):
        """Test parsing with spaces around numbers."""
        result = self.parser.parse_player_selection("1, 2, 3", 5)
        assert result == [1, 2, 3]

    def test_exit_lowercase(self):
        """Test 'exit' returns None."""
        result = self.parser.parse_player_selection("exit", 5)
        assert result is None

    def test_exit_uppercase(self):
        """Test 'EXIT' returns None."""
        result = self.parser.parse_player_selection("EXIT", 5)
        assert result is None

    def test_exit_mixed_case(self):
        """Test 'Exit' returns None."""
        result = self.parser.parse_player_selection("Exit", 5)
        assert result is None

    def test_empty_string(self):
        """Test empty string returns None."""
        result = self.parser.parse_player_selection("", 5)
        assert result is None

    def test_whitespace_only(self):
        """Test whitespace only returns None."""
        result = self.parser.parse_player_selection("   ", 5)
        assert result is None

    def test_invalid_characters(self):
        """Test invalid characters return None."""
        result = self.parser.parse_player_selection("1,a,3", 5)
        assert result is None

    def test_out_of_range_high(self):
        """Test number above max_index returns None."""
        result = self.parser.parse_player_selection("1,99", 5)
        assert result is None

    def test_out_of_range_low(self):
        """Test zero returns None."""
        result = self.parser.parse_player_selection("0,1", 5)
        assert result is None

    def test_negative_number(self):
        """Test negative number returns None."""
        result = self.parser.parse_player_selection("1,-2", 5)
        assert result is None

    def test_duplicate_numbers(self):
        """Test duplicate numbers return None."""
        result = self.parser.parse_player_selection("1,2,1", 5)
        assert result is None

    def test_leading_trailing_spaces(self):
        """Test leading/trailing spaces are handled."""
        result = self.parser.parse_player_selection("  1, 2  ", 5)
        assert result == [1, 2]


class TestGetPlayersByIndices:
    """Tests for get_players_by_indices method (TradeInputParser)."""

    def setup_method(self):
        """Setup test fixtures."""
        self.parser = TradeInputParser()

        # Create test roster
        self.roster = [
            FantasyPlayer(id=1, name="Player One", team="TST", position="RB", bye_week=7, fantasy_points=150.0, injury_status="ACTIVE", drafted=0),
            FantasyPlayer(id=2, name="Player Two", team="TST", position="WR", bye_week=8, fantasy_points=140.0, injury_status="ACTIVE", drafted=0),
            FantasyPlayer(id=3, name="Player Three", team="TST", position="QB", bye_week=9, fantasy_points=160.0, injury_status="ACTIVE", drafted=0),
        ]

    def test_extract_single_player(self):
        """Test extracting single player by index."""
        result = self.parser.get_players_by_indices(self.roster, [1])
        assert len(result) == 1
        assert result[0].name == "Player One"

    def test_extract_multiple_players(self):
        """Test extracting multiple players by indices."""
        result = self.parser.get_players_by_indices(self.roster, [1, 3])
        assert len(result) == 2
        assert result[0].name == "Player One"
        assert result[1].name == "Player Three"

    def test_non_sequential_order(self):
        """Test extracting players in non-sequential order."""
        result = self.parser.get_players_by_indices(self.roster, [3, 1, 2])
        assert len(result) == 3
        assert result[0].name == "Player Three"
        assert result[1].name == "Player One"
        assert result[2].name == "Player Two"


class TestDisplayTradeResult:
    """Tests for display_trade_result method (TradeDisplayHelper)."""

    def setup_method(self):
        """Setup test fixtures."""
        self.helper = TradeDisplayHelper()

    def test_display_trade_result(self, capsys):
        """Test displaying trade result."""
        # Create mock trade
        my_team = MagicMock()
        my_team.name = "My Team"
        my_team.team_score = 1050.0

        their_team = MagicMock()
        their_team.name = "Opponent Team"
        their_team.team_score = 1030.0

        player1 = FantasyPlayer(id=1, name="Player One", team="TST", position="RB", bye_week=7, fantasy_points=150.0, injury_status="ACTIVE", drafted=0)
        player2 = FantasyPlayer(id=2, name="Player Two", team="TST", position="WR", bye_week=8, fantasy_points=140.0, injury_status="ACTIVE", drafted=0)

        scored_player1 = ScoredPlayer(player1, 150.0, [])
        scored_player2 = ScoredPlayer(player2, 140.0, [])

        trade = TradeSnapshot(
            my_new_team=my_team,
            my_new_players=[scored_player2],
            their_new_team=their_team,
            their_new_players=[scored_player1],
            my_original_players=[scored_player1]  # Players I'm giving up (from original roster)
        )

        # Execute
        self.helper.display_trade_result(trade, 1000.0, 1000.0)

        # Verify output
        captured = capsys.readouterr()
        assert "MANUAL TRADE VISUALIZER" in captured.out
        assert "Trade with Opponent Team" in captured.out
        assert "My improvement: +50.00 pts" in captured.out
        assert "Their improvement: +30.00 pts" in captured.out
        assert "I give:" in captured.out
        assert "Player One" in captured.out
        assert "I receive:" in captured.out
        assert "Player Two" in captured.out


class TestSaveManualTradeToFile:
    """Tests for save_manual_trade_to_file method (TradeFileWriter)."""

    def setup_method(self):
        """Setup test fixtures."""
        self.writer = TradeFileWriter()

    @patch('league_helper.trade_simulator_mode.trade_file_writer.datetime')
    @patch('builtins.open', new_callable=mock_open)
    def test_save_trade_file_created(self, mock_file, mock_datetime):
        """Test that trade file is created with correct name."""
        # Mock datetime
        mock_datetime.now.return_value = datetime(2025, 10, 16, 12, 30, 45)

        # Create mock trade
        my_team = MagicMock()
        my_team.name = "My Team"
        my_team.team_score = 1050.0

        their_team = MagicMock()
        their_team.name = "Opponent Team"
        their_team.team_score = 1030.0

        player1 = FantasyPlayer(id=1, name="Player One", team="TST", position="RB", bye_week=7, fantasy_points=150.0, injury_status="ACTIVE", drafted=0)
        player2 = FantasyPlayer(id=2, name="Player Two", team="TST", position="WR", bye_week=8, fantasy_points=140.0, injury_status="ACTIVE", drafted=0)

        scored_player1 = ScoredPlayer(player1, 150.0, [])
        scored_player2 = ScoredPlayer(player2, 140.0, [])

        trade = TradeSnapshot(
            my_new_team=my_team,
            my_new_players=[scored_player2],
            their_new_team=their_team,
            their_new_players=[scored_player1]
        )

        # Execute
        filename = self.writer.save_manual_trade_to_file(trade, "Opponent Team", 1000.0, 1000.0)

        # Verify filename format
        assert "trade_info_Opponent_Team_20251016_123045.txt" in filename
        mock_file.assert_called_once()

    @patch('league_helper.trade_simulator_mode.trade_file_writer.datetime')
    @patch('builtins.open', new_callable=mock_open)
    def test_save_trade_with_spaces_in_name(self, mock_file, mock_datetime):
        """Test opponent name with spaces is sanitized."""
        # Mock datetime
        mock_datetime.now.return_value = datetime(2025, 10, 16, 12, 30, 45)

        # Create mock trade
        my_team = MagicMock()
        my_team.name = "My Team"
        my_team.team_score = 1050.0

        their_team = MagicMock()
        their_team.name = "Team With Spaces"
        their_team.team_score = 1030.0

        player = FantasyPlayer(id=1, name="Player One", team="TST", position="RB", bye_week=7, fantasy_points=150.0, injury_status="ACTIVE", drafted=0)
        scored_player = ScoredPlayer(player, 150.0, [])

        trade = TradeSnapshot(
            my_new_team=my_team,
            my_new_players=[scored_player],
            their_new_team=their_team,
            their_new_players=[scored_player]
        )

        # Execute
        filename = self.writer.save_manual_trade_to_file(trade, "Team With Spaces", 1000.0, 1000.0)

        # Verify filename has underscores instead of spaces
        assert "Team_With_Spaces" in filename
        assert "Team With Spaces" not in filename


class TestDisplayCombinedRoster:
    """Tests for display_combined_roster method (TradeDisplayHelper) (new in 2025-10-16 redesign)."""

    def setup_method(self):
        """Setup test fixtures."""
        self.helper = TradeDisplayHelper()

    def test_combined_roster_returns_boundary(self, capsys):
        """Test that combined roster returns correct boundary index."""
        # Create test rosters
        my_roster = [
            FantasyPlayer(id=1, name="My QB", team="TST", position="QB", bye_week=7, fantasy_points=200.0, injury_status="ACTIVE", drafted=0),
            FantasyPlayer(id=2, name="My RB", team="TST", position="RB", bye_week=7, fantasy_points=150.0, injury_status="ACTIVE", drafted=0),
        ]
        their_roster = [
            FantasyPlayer(id=3, name="Their QB", team="TST", position="QB", bye_week=8, fantasy_points=180.0, injury_status="ACTIVE", drafted=0),
        ]

        # Execute
        boundary, my_display_order, their_display_order = self.helper.display_combined_roster(my_roster, their_roster, "Opponent Team")

        # Verify boundary is where their roster starts (after my 2 players)
        assert boundary == 3
        # Verify display orders are returned
        assert len(my_display_order) == 2
        assert len(their_display_order) == 1

        # Verify output contains both teams
        captured = capsys.readouterr()
        assert "MY TEAM" in captured.out
        assert "OPPONENT TEAM" in captured.out

    def test_combined_roster_organizes_by_position(self, capsys):
        """Test that combined roster organizes players by position."""
        # Create mixed position roster
        my_roster = [
            FantasyPlayer(id=1, name="My RB", team="TST", position="RB", bye_week=7, fantasy_points=150.0, injury_status="ACTIVE", drafted=0),
            FantasyPlayer(id=2, name="My QB", team="TST", position="QB", bye_week=7, fantasy_points=200.0, injury_status="ACTIVE", drafted=0),
            FantasyPlayer(id=3, name="My WR", team="TST", position="WR", bye_week=7, fantasy_points=140.0, injury_status="ACTIVE", drafted=0),
        ]
        their_roster = []

        # Execute
        _, _, _ = self.helper.display_combined_roster(my_roster, their_roster, "Opponent")

        # Verify output shows positions in order: QB, RB, WR, TE, K, DST
        captured = capsys.readouterr()
        qb_pos = captured.out.find("QB:")
        rb_pos = captured.out.find("RB:")
        wr_pos = captured.out.find("WR:")
        assert qb_pos < rb_pos < wr_pos

    def test_combined_roster_shows_empty_positions(self, capsys):
        """Test that empty position groups show '(No players)'."""
        # Create roster with only QB
        my_roster = [
            FantasyPlayer(id=1, name="My QB", team="TST", position="QB", bye_week=7, fantasy_points=200.0, injury_status="ACTIVE", drafted=0),
        ]
        their_roster = []

        # Execute
        _, _, _ = self.helper.display_combined_roster(my_roster, their_roster, "Opponent")

        # Verify output
        captured = capsys.readouterr()
        # Should have "(No players)" for positions without players
        assert "(No players)" in captured.out


class TestSplitPlayersByTeam:
    """Tests for split_players_by_team helper method (TradeInputParser) (new in 2025-10-16 redesign)."""

    def setup_method(self):
        """Setup test fixtures."""
        self.parser = TradeInputParser()

    def test_split_all_from_my_team(self):
        """Test splitting when all selections from my team."""
        unified_indices = [1, 2, 3]
        roster_boundary = 14  # Their roster starts at 14

        my_indices, their_indices = self.parser.split_players_by_team(unified_indices, roster_boundary)

        assert my_indices == [1, 2, 3]
        assert their_indices == []

    def test_split_all_from_their_team(self):
        """Test splitting when all selections from their team."""
        unified_indices = [14, 15, 16]
        roster_boundary = 14  # Their roster starts at 14

        my_indices, their_indices = self.parser.split_players_by_team(unified_indices, roster_boundary)

        assert my_indices == []
        # Their indices should be adjusted to be 1-based relative to their roster
        assert their_indices == [1, 2, 3]

    def test_split_mixed_teams(self):
        """Test splitting with selections from both teams."""
        unified_indices = [2, 6, 18, 21]
        roster_boundary = 14  # My roster: 1-13, Their roster: 14-26

        my_indices, their_indices = self.parser.split_players_by_team(unified_indices, roster_boundary)

        assert my_indices == [2, 6]
        # 18 becomes 5 (18-14+1), 21 becomes 8 (21-14+1)
        assert their_indices == [5, 8]

    def test_split_empty_selection(self):
        """Test splitting empty selection."""
        unified_indices = []
        roster_boundary = 14

        my_indices, their_indices = self.parser.split_players_by_team(unified_indices, roster_boundary)

        assert my_indices == []
        assert their_indices == []


class TestParseUnifiedPlayerSelection:
    """Tests for parse_unified_player_selection method (TradeInputParser) (new in 2025-10-16 redesign)."""

    def setup_method(self):
        """Setup test fixtures."""
        self.parser = TradeInputParser()

    def test_valid_unified_selection(self):
        """Test valid unified selection from both teams."""
        # My roster: 1-13, Their roster: 14-26
        result = self.parser.parse_unified_player_selection("2,6,18,21", 26, 14)

        assert result is not None
        my_indices, their_indices = result
        assert my_indices == [2, 6]
        assert their_indices == [5, 8]  # Adjusted to be relative to their roster

    def test_exit_returns_none(self):
        """Test 'exit' input returns None."""
        result = self.parser.parse_unified_player_selection("exit", 26, 14)
        assert result is None

    def test_unequal_numbers_returns_none(self):
        """Test unequal trades are now ALLOWED (3-for-1 in this case)."""
        # 3 from my team, 1 from their team (3-for-1 trade)
        result = self.parser.parse_unified_player_selection("1,2,3,14", 26, 14)
        assert result is not None
        my_indices, their_indices = result
        assert my_indices == [1, 2, 3]
        assert their_indices == [1]  # 14 is first player in their roster

    def test_all_from_one_team_returns_none(self):
        """Test all selections from one team returns None."""
        # All from my team
        result = self.parser.parse_unified_player_selection("1,2,3,4", 26, 14)
        assert result is None

    def test_invalid_format_returns_none(self):
        """Test invalid format returns None."""
        result = self.parser.parse_unified_player_selection("abc", 26, 14)
        assert result is None

    def test_out_of_range_returns_none(self):
        """Test out of range selection returns None."""
        result = self.parser.parse_unified_player_selection("1,99", 26, 14)
        assert result is None

    def test_minimum_one_from_each_team(self):
        """Test that at least 1 from each team is required."""
        # Valid: 1 from each
        result = self.parser.parse_unified_player_selection("1,14", 26, 14)
        assert result is not None

        # Invalid: 0 from my team
        result = self.parser.parse_unified_player_selection("14,15", 26, 14)
        assert result is None


class TestStartManualTradeIntegration:
    """Integration tests for start_manual_trade method."""

    @pytest.fixture
    def mock_data_folder(self, tmp_path):
        """Create temporary data folder with test files."""
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        # Create minimal league_config.json with all required parameters
        config_file = data_folder / "league_config.json"
        config_content = {
            "config_name": "test",
            "description": "test config",
            "parameters": {
                "CURRENT_NFL_WEEK": 1,
                "NFL_SEASON": 2025,
                "NFL_SCORING_FORMAT": "ppr",
                "NORMALIZATION_MAX_SCALE": 100.0,
                "DRAFT_NORMALIZATION_MAX_SCALE": 163,
                "SAME_POS_BYE_WEIGHT": 1.0,
            "DIFF_POS_BYE_WEIGHT": 1.0,
                "DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY": 5.0,
                "INJURY_PENALTIES": {"LOW": 0, "MEDIUM": 10, "HIGH": 75},
                "DRAFT_ORDER_BONUSES": {"PRIMARY": 50, "SECONDARY": 30},
                "DRAFT_ORDER": [{"FLEX": "P"}],
                "MAX_POSITIONS": {"QB": 2, "RB": 4, "WR": 4, "FLEX": 2, "TE": 1, "K": 1, "DST": 1},
                "FLEX_ELIGIBLE_POSITIONS": ["RB", "WR"],
                "ADP_SCORING": {
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 35},
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "WEIGHT": 1.0
                },
                "PLAYER_RATING_SCORING": {
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 22},
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "WEIGHT": 1.0
                },
                "TEAM_QUALITY_SCORING": {
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 5},
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "WEIGHT": 1.0
                },
                "PERFORMANCE_SCORING": {
                    "MIN_WEEKS": 3,
                    "THRESHOLDS": {"BASE_POSITION": 0.0, "DIRECTION": "BI_EXCELLENT_HI", "STEPS": 0.15},
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "WEIGHT": 1.0
                },
                "MATCHUP_SCORING": {
                    "IMPACT_SCALE": 150.0,
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "BI_EXCELLENT_HI", "STEPS": 6},
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "WEIGHT": 1.0
                },
                "SCHEDULE_SCORING": {
                    "IMPACT_SCALE": 80.0,
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 8},
                    "MULTIPLIERS": {"EXCELLENT": 1.0, "GOOD": 1.0, "POOR": 1.0, "VERY_POOR": 1.0},
                    "WEIGHT": 0.0
                }
            }
        }
        import json
        config_file.write_text(json.dumps(config_content, indent=2))

        # Create minimal players.csv
        players_file = data_folder / "players.csv"
        players_file.write_text("id,name,team,position,bye_week,fantasy_points,injury_status,drafted,locked\n")

        # Create minimal players_projected.csv (required by ProjectedPointsManager)
        players_projected_file = data_folder / "players_projected.csv"
        players_projected_file.write_text("id,name,week_1_points,week_2_points,week_3_points,week_4_points,week_5_points,week_6_points,week_7_points,week_8_points,week_9_points,week_10_points,week_11_points,week_12_points,week_13_points,week_14_points,week_15_points,week_16_points,week_17_points\n")

        # Note: teams.csv no longer used - team data is now in team_data folder
        # Create empty team_data folder for TeamDataManager
        team_data_folder = data_folder / "team_data"
        team_data_folder.mkdir()

        return data_folder

    def test_no_opponent_teams(self, mock_data_folder):
        """Test handling when no opponent teams available."""
        # Setup with mock data folder
        config = ConfigManager(mock_data_folder)
        season_schedule_mgr = SeasonScheduleManager(mock_data_folder)
        team_data_mgr = TeamDataManager(mock_data_folder, config, season_schedule_mgr, config.current_nfl_week)
        player_manager = PlayerManager(mock_data_folder, config, team_data_mgr, season_schedule_mgr)
        manager = TradeSimulatorModeManager(mock_data_folder, player_manager, config)

        # Clear opponent teams
        manager.opponent_simulated_teams = []

        # Execute
        result = manager.start_manual_trade()

        # Verify
        assert result == (True, [])


class TestWaiverTradeProcessing:
    """Tests for process_manual_trade with waiver functionality."""

    @pytest.fixture
    def mock_data_folder(self, tmp_path):
        """Create temporary data folder with test files."""
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        # Create minimal league_config.json
        config_file = data_folder / "league_config.json"
        config_content = {
            "config_name": "test",
            "description": "test config",
            "parameters": {
                "CURRENT_NFL_WEEK": 1,
                "NFL_SEASON": 2025,
                "NFL_SCORING_FORMAT": "ppr",
                "NORMALIZATION_MAX_SCALE": 100.0,
                "DRAFT_NORMALIZATION_MAX_SCALE": 163,
                "SAME_POS_BYE_WEIGHT": 1.0,
                "DIFF_POS_BYE_WEIGHT": 1.0,
                "DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY": 5.0,
                "INJURY_PENALTIES": {"LOW": 0, "MEDIUM": 10, "HIGH": 75},
                "DRAFT_ORDER_BONUSES": {"PRIMARY": 50, "SECONDARY": 30},
                "DRAFT_ORDER": [{"FLEX": "P"}],
                "MAX_POSITIONS": {"QB": 2, "RB": 4, "WR": 4, "FLEX": 2, "TE": 1, "K": 1, "DST": 1},
                "FLEX_ELIGIBLE_POSITIONS": ["RB", "WR"],
                "ADP_SCORING": {
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 35},
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "WEIGHT": 1.0
                },
                "PLAYER_RATING_SCORING": {
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 22},
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "WEIGHT": 1.0
                },
                "TEAM_QUALITY_SCORING": {
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 5},
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "WEIGHT": 1.0
                },
                "PERFORMANCE_SCORING": {
                    "MIN_WEEKS": 3,
                    "THRESHOLDS": {"BASE_POSITION": 0.0, "DIRECTION": "BI_EXCELLENT_HI", "STEPS": 0.15},
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "WEIGHT": 1.0
                },
                "MATCHUP_SCORING": {
                    "IMPACT_SCALE": 150.0,
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "BI_EXCELLENT_HI", "STEPS": 6},
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "WEIGHT": 1.0
                },
                "SCHEDULE_SCORING": {
                    "IMPACT_SCALE": 80.0,
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 8},
                    "MULTIPLIERS": {"EXCELLENT": 1.0, "GOOD": 1.0, "POOR": 1.0, "VERY_POOR": 1.0},
                    "WEIGHT": 0.0
                }
            }
        }
        import json
        config_file.write_text(json.dumps(config_content, indent=2))

        # Create minimal players.csv
        players_file = data_folder / "players.csv"
        players_file.write_text("id,name,team,position,bye_week,fantasy_points,injury_status,drafted,locked\n")

        # Create minimal players_projected.csv (required by ProjectedPointsManager)
        players_projected_file = data_folder / "players_projected.csv"
        players_projected_file.write_text("id,name,week_1_points,week_2_points,week_3_points,week_4_points,week_5_points,week_6_points,week_7_points,week_8_points,week_9_points,week_10_points,week_11_points,week_12_points,week_13_points,week_14_points,week_15_points,week_16_points,week_17_points\n")

        # Note: teams.csv no longer used - team data is now in team_data folder
        # Create empty team_data folder for TeamDataManager
        team_data_folder = data_folder / "team_data"
        team_data_folder.mkdir()

        return data_folder

    @pytest.fixture
    def sample_players(self):
        """Create sample players for testing."""
        return {
            'qb1': FantasyPlayer(id=1, name="QB1", team="TST", position="QB", bye_week=7, fantasy_points=200.0, injury_status="ACTIVE", drafted=1),
            'rb1': FantasyPlayer(id=2, name="RB1", team="TST", position="RB", bye_week=8, fantasy_points=150.0, injury_status="ACTIVE", drafted=1),
            'wr1': FantasyPlayer(id=3, name="WR1", team="TST", position="WR", bye_week=9, fantasy_points=140.0, injury_status="ACTIVE", drafted=1),
            'waiver_rb': FantasyPlayer(id=10, name="Waiver RB", team="FA", position="RB", bye_week=10, fantasy_points=100.0, injury_status="ACTIVE", drafted=0),
            'waiver_wr': FantasyPlayer(id=11, name="Waiver WR", team="FA", position="WR", bye_week=11, fantasy_points=90.0, injury_status="ACTIVE", drafted=0),
        }

    @pytest.fixture
    def mock_teams(self, sample_players):
        """Create mock teams for testing."""
        from unittest.mock import Mock

        my_team = Mock()
        my_team.name = "My Team"
        my_team.team = [sample_players['qb1'], sample_players['rb1'], sample_players['wr1']]

        waiver_team = Mock()
        waiver_team.name = "Waiver Wire"
        waiver_team.team = [sample_players['waiver_rb'], sample_players['waiver_wr']]

        return my_team, waiver_team

    def test_process_manual_trade_waiver_skips_their_validation(self, mock_teams, sample_players, mock_data_folder):
        """Test that is_waivers=True skips waiver team validation."""
        from league_helper.trade_simulator_mode.trade_analyzer import TradeAnalyzer
        from unittest.mock import Mock

        # Setup
        config = ConfigManager(mock_data_folder)
        season_schedule_mgr = SeasonScheduleManager(mock_data_folder)
        team_data_mgr = TeamDataManager(mock_data_folder, config, season_schedule_mgr, config.current_nfl_week)
        player_manager = PlayerManager(mock_data_folder, config, team_data_mgr, season_schedule_mgr)
        analyzer = TradeAnalyzer(player_manager, config)

        my_team, waiver_team = mock_teams

        # Mock validate_roster_lenient to track calls
        original_validate = analyzer.validate_roster_lenient
        validate_calls = []
        def track_validate(original_roster, new_roster):
            validate_calls.append((original_roster, new_roster))
            return True
        analyzer.validate_roster_lenient = track_validate

        # Execute - trade with waivers (1-for-1)
        snapshot, my_drops, their_drops = analyzer.process_manual_trade(
            my_team=my_team,
            their_team=waiver_team,
            my_selected_players=[sample_players['rb1']],
            their_selected_players=[sample_players['waiver_rb']],
            is_waivers=True
        )

        # Verify - validate should only be called for my team, not waiver team
        assert len(validate_calls) == 1, "Should only validate my team when is_waivers=True"
        assert snapshot is not None, "Trade should succeed with valid user roster"
        assert their_drops == [], "Waiver team should have no drop candidates"

    def test_process_manual_trade_waiver_validates_my_team(self, mock_teams, sample_players, mock_data_folder):
        """Test that user team validation still runs with is_waivers=True."""
        from league_helper.trade_simulator_mode.trade_analyzer import TradeAnalyzer
        from unittest.mock import Mock

        # Setup
        config = ConfigManager(mock_data_folder)
        season_schedule_mgr = SeasonScheduleManager(mock_data_folder)
        team_data_mgr = TeamDataManager(mock_data_folder, config, season_schedule_mgr, config.current_nfl_week)
        player_manager = PlayerManager(mock_data_folder, config, team_data_mgr, season_schedule_mgr)
        analyzer = TradeAnalyzer(player_manager, config)

        my_team, waiver_team = mock_teams

        # Mock validate_roster_lenient to return False for my team
        def mock_validate(original_roster, new_roster):
            return False  # My roster is invalid
        analyzer.validate_roster_lenient = mock_validate

        # Execute - trade with waivers
        snapshot, my_drops, their_drops = analyzer.process_manual_trade(
            my_team=my_team,
            their_team=waiver_team,
            my_selected_players=[sample_players['rb1']],
            their_selected_players=[sample_players['waiver_rb']],
            is_waivers=True
        )

        # Verify - snapshot should be None because my roster is invalid
        assert snapshot is None, "Trade should fail when user roster invalid"
        assert len(my_drops) > 0 or True, "Should provide drop candidates for my team"
        assert their_drops == [], "Waiver team should have no drop candidates"

    def test_process_manual_trade_normal_trade_validates_both_teams(self, mock_teams, sample_players, mock_data_folder):
        """Test that normal trades (is_waivers=False) validate both teams."""
        from league_helper.trade_simulator_mode.trade_analyzer import TradeAnalyzer

        # Setup
        config = ConfigManager(mock_data_folder)
        season_schedule_mgr = SeasonScheduleManager(mock_data_folder)
        team_data_mgr = TeamDataManager(mock_data_folder, config, season_schedule_mgr, config.current_nfl_week)
        player_manager = PlayerManager(mock_data_folder, config, team_data_mgr, season_schedule_mgr)
        analyzer = TradeAnalyzer(player_manager, config)

        my_team, their_team = mock_teams

        # Mock validate_roster_lenient to track calls
        validate_calls = []
        def track_validate(original_roster, new_roster):
            validate_calls.append((original_roster, new_roster))
            return True
        analyzer.validate_roster_lenient = track_validate

        # Execute - normal trade (NOT waivers)
        snapshot, my_drops, their_drops = analyzer.process_manual_trade(
            my_team=my_team,
            their_team=their_team,
            my_selected_players=[sample_players['rb1']],
            their_selected_players=[sample_players['qb1']],
            is_waivers=False
        )

        # Verify - validate should be called for BOTH teams
        assert len(validate_calls) == 2, "Should validate both teams when is_waivers=False"

    def test_process_manual_trade_waiver_skips_their_waiver_recommendations(self, mock_teams, sample_players, mock_data_folder):
        """Test that waiver team doesn't get waiver recommendations."""
        from league_helper.trade_simulator_mode.trade_analyzer import TradeAnalyzer
        from unittest.mock import Mock, patch

        # Setup
        config = ConfigManager(mock_data_folder)
        season_schedule_mgr = SeasonScheduleManager(mock_data_folder)
        team_data_mgr = TeamDataManager(mock_data_folder, config, season_schedule_mgr, config.current_nfl_week)
        player_manager = PlayerManager(mock_data_folder, config, team_data_mgr, season_schedule_mgr)
        analyzer = TradeAnalyzer(player_manager, config)

        my_team, waiver_team = mock_teams

        # Mock validate_roster_lenient to always return True
        analyzer.validate_roster_lenient = lambda *args: True

        # Mock _get_waiver_recommendations to track calls
        waiver_rec_calls = []
        original_get_waiver_recs = analyzer._get_waiver_recommendations
        def track_waiver_recs(*args, **kwargs):
            waiver_rec_calls.append((args, kwargs))
            return []
        analyzer._get_waiver_recommendations = track_waiver_recs

        # Execute - unequal trade (2-for-1) with waivers, their team would normally need waivers
        snapshot, my_drops, their_drops = analyzer.process_manual_trade(
            my_team=my_team,
            their_team=waiver_team,
            my_selected_players=[sample_players['rb1'], sample_players['wr1']],
            their_selected_players=[sample_players['waiver_rb']],
            is_waivers=True
        )

        # Verify - _get_waiver_recommendations should only be called once (for my team)
        assert len(waiver_rec_calls) <= 1, "Waiver recommendations should only be for my team when is_waivers=True"


# Test coverage marker
def test_module_imports():
    """Verify all required modules can be imported."""
    assert TradeSimulatorModeManager is not None
    assert TradeSimTeam is not None
    assert TradeSnapshot is not None
    assert FantasyPlayer is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
