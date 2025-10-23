"""
Tests for TradeFileWriter class

Tests file I/O operations for trade analysis results.
Covers manual trade saving, trade suggestor output, and waiver optimizer output.

Author: Kai Mizuno
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, mock_open
import sys
from pathlib import Path

# Add parent directories to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from league_helper.trade_simulator_mode.trade_file_writer import TradeFileWriter
from league_helper.trade_simulator_mode.TradeSimTeam import TradeSimTeam
from league_helper.trade_simulator_mode.TradeSnapshot import TradeSnapshot


@pytest.fixture
def writer():
    """Create a TradeFileWriter instance"""
    with patch('league_helper.trade_simulator_mode.trade_file_writer.get_logger') as mock_logger:
        mock_logger.return_value = Mock()
        return TradeFileWriter()


@pytest.fixture
def mock_trade():
    """Create a mock TradeSnapshot"""
    trade = Mock(spec=TradeSnapshot)

    # Mock my_new_team
    trade.my_new_team = Mock()
    trade.my_new_team.team_score = 85.0
    trade.my_new_team.name = "My Team"

    # Mock their_new_team
    trade.their_new_team = Mock()
    trade.their_new_team.team_score = 75.0
    trade.their_new_team.name = "Their Team"

    # Mock players
    trade.my_original_players = ["QB1 (QB) - KC", "RB1 (RB) - SF"]
    trade.my_new_players = ["WR1 (WR) - MIA", "TE1 (TE) - KC"]
    trade.their_new_players = ["QB1 (QB) - KC", "RB1 (RB) - SF"]

    # Add new unequal trade fields (default to None/empty for basic tests)
    trade.waiver_recommendations = None
    trade.their_waiver_recommendations = None
    trade.my_dropped_players = None
    trade.their_dropped_players = None

    return trade


@pytest.fixture
def mock_team():
    """Create a mock TradeSimTeam"""
    team = Mock(spec=TradeSimTeam)
    team.team_score = 80.0
    team.name = "Test Team"
    return team


class TestTradeFileWriterInitialization:
    """Test TradeFileWriter class initialization"""

    def test_class_initialization(self):
        """Test that TradeFileWriter initializes correctly"""
        with patch('league_helper.trade_simulator_mode.trade_file_writer.get_logger') as mock_logger:
            mock_logger.return_value = Mock()
            writer = TradeFileWriter()
            assert writer is not None

    def test_logger_attribute_exists(self, writer):
        """Test that logger attribute is initialized"""
        assert hasattr(writer, 'logger')
        assert writer.logger is not None


class TestSaveManualTradeToFile:
    """Test save_manual_trade_to_file method"""

    @patch('builtins.open', new_callable=mock_open)
    @patch('league_helper.trade_simulator_mode.trade_file_writer.datetime')
    def test_save_trade_with_positive_improvements(self, mock_datetime, mock_file, writer, mock_trade):
        """Test saving trade with positive improvements for both teams"""
        mock_datetime.now.return_value.strftime.return_value = "20251017_120000"

        filename = writer.save_manual_trade_to_file(
            mock_trade,
            "Opponent Team",
            original_my_score=80.0,
            original_their_score=70.0
        )

        # Verify filename format
        assert filename == "./league_helper/trade_simulator_mode/trade_outputs/trade_info_Opponent_Team_20251017_120000.txt"

        # Verify file was opened for writing
        mock_file.assert_called_once_with(filename, 'w')

        # Verify file content
        handle = mock_file()
        assert handle.write.called

        # Check key content was written
        calls = [str(call) for call in handle.write.call_args_list]
        assert any("Trade with Opponent Team" in call for call in calls)
        assert any("My improvement: +5.00 pts" in call for call in calls)
        assert any("Their improvement: +5.00 pts" in call for call in calls)

    @patch('builtins.open', new_callable=mock_open)
    @patch('league_helper.trade_simulator_mode.trade_file_writer.datetime')
    def test_save_trade_with_negative_improvements(self, mock_datetime, mock_file, writer, mock_trade):
        """Test saving trade with negative improvements"""
        mock_datetime.now.return_value.strftime.return_value = "20251017_120000"

        # Adjust scores for negative improvement
        mock_trade.my_new_team.team_score = 75.0  # Down from 80.0
        mock_trade.their_new_team.team_score = 65.0  # Down from 70.0

        writer.save_manual_trade_to_file(
            mock_trade,
            "Opponent",
            original_my_score=80.0,
            original_their_score=70.0
        )

        handle = mock_file()
        calls = [str(call) for call in handle.write.call_args_list]

        # Verify negative signs
        assert any("My improvement: -5.00 pts" in call for call in calls)
        assert any("Their improvement: -5.00 pts" in call for call in calls)

    @patch('builtins.open', new_callable=mock_open)
    @patch('league_helper.trade_simulator_mode.trade_file_writer.datetime')
    def test_filename_timestamp_format(self, mock_datetime, mock_file, writer, mock_trade):
        """Test that filename includes proper timestamp"""
        mock_datetime.now.return_value.strftime.return_value = "20251231_235959"

        filename = writer.save_manual_trade_to_file(
            mock_trade,
            "Test",
            original_my_score=80.0,
            original_their_score=70.0
        )

        assert "20251231_235959" in filename

    @patch('builtins.open', new_callable=mock_open)
    @patch('league_helper.trade_simulator_mode.trade_file_writer.datetime')
    def test_opponent_name_sanitization(self, mock_datetime, mock_file, writer, mock_trade):
        """Test that opponent name spaces are replaced with underscores"""
        mock_datetime.now.return_value.strftime.return_value = "20251017_120000"

        filename = writer.save_manual_trade_to_file(
            mock_trade,
            "Opponent With Spaces",
            original_my_score=80.0,
            original_their_score=70.0
        )

        assert "Opponent_With_Spaces" in filename
        assert "Opponent With Spaces" not in filename

    @patch('builtins.open', new_callable=mock_open)
    @patch('league_helper.trade_simulator_mode.trade_file_writer.datetime')
    def test_file_content_structure(self, mock_datetime, mock_file, writer, mock_trade):
        """Test that file content has correct structure"""
        mock_datetime.now.return_value.strftime.return_value = "20251017_120000"

        writer.save_manual_trade_to_file(
            mock_trade,
            "Opponent",
            original_my_score=80.0,
            original_their_score=70.0
        )

        handle = mock_file()
        calls = [str(call) for call in handle.write.call_args_list]

        # Verify structure: Trade header, improvements, give/receive sections
        assert any("I give:" in call for call in calls)
        assert any("I receive:" in call for call in calls)
        assert any("QB1 (QB) - KC" in call for call in calls)
        assert any("WR1 (WR) - MIA" in call for call in calls)

    @patch('builtins.open', new_callable=mock_open)
    @patch('league_helper.trade_simulator_mode.trade_file_writer.datetime')
    def test_returns_filename(self, mock_datetime, mock_file, writer, mock_trade):
        """Test that method returns the created filename"""
        mock_datetime.now.return_value.strftime.return_value = "20251017_120000"

        result = writer.save_manual_trade_to_file(
            mock_trade,
            "Test",
            original_my_score=80.0,
            original_their_score=70.0
        )

        assert isinstance(result, str)
        assert result.startswith("./league_helper/trade_simulator_mode/trade_outputs/")
        assert result.endswith(".txt")


class TestSaveTradesToFile:
    """Test save_trades_to_file method"""

    @patch('builtins.open', new_callable=mock_open)
    @patch('league_helper.trade_simulator_mode.trade_file_writer.datetime')
    def test_save_single_trade(self, mock_datetime, mock_file, writer, mock_trade, mock_team):
        """Test saving a single trade"""
        mock_datetime.now.return_value.strftime.return_value = "2025-10-17_12-00-00"

        opponent = Mock()
        opponent.name = "Their Team"
        opponent.team_score = 70.0

        writer.save_trades_to_file([mock_trade], mock_team, [opponent])

        # Verify file was opened
        mock_file.assert_called_once()
        filename = mock_file.call_args[0][0]
        assert "trade_info_2025-10-17_12-00-00.txt" in filename

        # Verify content written
        handle = mock_file()
        assert handle.write.called

    @patch('builtins.open', new_callable=mock_open)
    @patch('league_helper.trade_simulator_mode.trade_file_writer.datetime')
    def test_save_multiple_trades(self, mock_datetime, mock_file, writer, mock_trade, mock_team):
        """Test saving multiple trades"""
        mock_datetime.now.return_value.strftime.return_value = "2025-10-17_12-00-00"

        # Create second trade
        trade2 = Mock(spec=TradeSnapshot)
        trade2.my_new_team = Mock()
        trade2.my_new_team.team_score = 82.0
        trade2.my_new_team.name = "My Team"
        trade2.their_new_team = Mock()
        trade2.their_new_team.team_score = 72.0
        trade2.their_new_team.name = "Other Team"
        trade2.my_original_players = ["RB2 (RB) - BUF"]
        trade2.my_new_players = ["WR2 (WR) - DAL"]
        # Add new unequal trade fields
        trade2.waiver_recommendations = None
        trade2.their_waiver_recommendations = None
        trade2.my_dropped_players = None
        trade2.their_dropped_players = None

        opponent1 = Mock()
        opponent1.name = "Their Team"
        opponent1.team_score = 70.0

        opponent2 = Mock()
        opponent2.name = "Other Team"
        opponent2.team_score = 70.0

        writer.save_trades_to_file([mock_trade, trade2], mock_team, [opponent1, opponent2])

        handle = mock_file()
        calls = [str(call) for call in handle.write.call_args_list]

        # Verify both trades are numbered
        assert any("#1 - Trade with" in call for call in calls)
        assert any("#2 - Trade with" in call for call in calls)

    @patch('builtins.open', new_callable=mock_open)
    @patch('league_helper.trade_simulator_mode.trade_file_writer.datetime')
    def test_file_format_validation(self, mock_datetime, mock_file, writer, mock_trade, mock_team):
        """Test that file format is correct"""
        mock_datetime.now.return_value.strftime.return_value = "2025-10-17_12-00-00"

        opponent = Mock()
        opponent.name = "Their Team"
        opponent.team_score = 70.0

        writer.save_trades_to_file([mock_trade], mock_team, [opponent])

        handle = mock_file()
        calls = [str(call) for call in handle.write.call_args_list]

        # Verify format elements
        assert any("#1 - Trade with" in call for call in calls)
        assert any("My improvement:" in call for call in calls)
        assert any("Their improvement:" in call for call in calls)
        assert any("I give:" in call for call in calls)
        assert any("I receive:" in call for call in calls)

    @patch('builtins.open', new_callable=mock_open)
    @patch('league_helper.trade_simulator_mode.trade_file_writer.datetime')
    def test_logger_called(self, mock_datetime, mock_file, writer, mock_trade, mock_team):
        """Test that logger.info is called after saving"""
        mock_datetime.now.return_value.strftime.return_value = "2025-10-17_12-00-00"

        opponent = Mock()
        opponent.name = "Their Team"
        opponent.team_score = 70.0

        writer.save_trades_to_file([mock_trade], mock_team, [opponent])

        # Verify logger was called
        assert writer.logger.info.called

    @patch('builtins.open', new_callable=mock_open)
    @patch('league_helper.trade_simulator_mode.trade_file_writer.datetime')
    def test_opponent_team_lookup(self, mock_datetime, mock_file, writer, mock_trade, mock_team):
        """Test that opponent team is correctly looked up"""
        mock_datetime.now.return_value.strftime.return_value = "2025-10-17_12-00-00"

        # Create opponent with specific name
        opponent = Mock()
        opponent.name = "Their Team"
        opponent.team_score = 70.0

        # Trade references "Their Team"
        mock_trade.their_new_team.name = "Their Team"

        writer.save_trades_to_file([mock_trade], mock_team, [opponent])

        handle = mock_file()
        calls = [str(call) for call in handle.write.call_args_list]

        # Should calculate their improvement correctly
        assert any("Their improvement:" in call for call in calls)


class TestSaveWaiverTradesToFile:
    """Test save_waiver_trades_to_file method"""

    @patch('builtins.open', new_callable=mock_open)
    @patch('league_helper.trade_simulator_mode.trade_file_writer.datetime')
    def test_save_single_waiver_trade(self, mock_datetime, mock_file, writer, mock_trade, mock_team):
        """Test saving a single waiver trade"""
        mock_datetime.now.return_value.strftime.return_value = "2025-10-17_12-00-00"

        writer.save_waiver_trades_to_file([mock_trade], mock_team)

        # Verify file was opened with correct name
        mock_file.assert_called_once()
        filename = mock_file.call_args[0][0]
        assert "waiver_info_2025-10-17_12-00-00.txt" in filename

    @patch('builtins.open', new_callable=mock_open)
    @patch('league_helper.trade_simulator_mode.trade_file_writer.datetime')
    def test_save_multiple_waiver_trades(self, mock_datetime, mock_file, writer, mock_trade, mock_team):
        """Test saving multiple waiver trades"""
        mock_datetime.now.return_value.strftime.return_value = "2025-10-17_12-00-00"

        # Create second waiver trade
        trade2 = Mock(spec=TradeSnapshot)
        trade2.my_new_team = Mock()
        trade2.my_new_team.team_score = 83.0
        trade2.my_original_players = ["K1 (K) - BAL"]
        trade2.my_new_players = ["K2 (K) - SF"]
        # Add new unequal trade fields
        trade2.waiver_recommendations = None
        trade2.my_dropped_players = None

        writer.save_waiver_trades_to_file([mock_trade, trade2], mock_team)

        handle = mock_file()
        calls = [str(call) for call in handle.write.call_args_list]

        # Verify both trades are numbered
        assert any("#1 -" in call for call in calls)
        assert any("#2 -" in call for call in calls)

    @patch('builtins.open', new_callable=mock_open)
    @patch('league_helper.trade_simulator_mode.trade_file_writer.datetime')
    def test_waiver_file_format_drop_add(self, mock_datetime, mock_file, writer, mock_trade, mock_team):
        """Test that waiver file uses DROP/ADD format"""
        mock_datetime.now.return_value.strftime.return_value = "2025-10-17_12-00-00"

        writer.save_waiver_trades_to_file([mock_trade], mock_team)

        handle = mock_file()
        calls = [str(call) for call in handle.write.call_args_list]

        # Verify DROP/ADD format (not "I give"/"I receive")
        assert any("DROP:" in call for call in calls)
        assert any("ADD:" in call for call in calls)
        assert not any("I give:" in call for call in calls)
        assert not any("I receive:" in call for call in calls)

    @patch('builtins.open', new_callable=mock_open)
    @patch('league_helper.trade_simulator_mode.trade_file_writer.datetime')
    def test_waiver_logger_called(self, mock_datetime, mock_file, writer, mock_trade, mock_team):
        """Test that logger.info is called after saving waivers"""
        mock_datetime.now.return_value.strftime.return_value = "2025-10-17_12-00-00"

        writer.save_waiver_trades_to_file([mock_trade], mock_team)

        # Verify logger was called
        assert writer.logger.info.called

    @patch('builtins.open', new_callable=mock_open)
    @patch('league_helper.trade_simulator_mode.trade_file_writer.datetime')
    def test_trade_type_label(self, mock_datetime, mock_file, writer, mock_team):
        """Test that trade type label is correct (1-for-1, 2-for-2, etc.)"""
        mock_datetime.now.return_value.strftime.return_value = "2025-10-17_12-00-00"

        # Create trade with 2 players
        trade = Mock(spec=TradeSnapshot)
        trade.my_new_team = Mock()
        trade.my_new_team.team_score = 85.0
        trade.my_original_players = ["QB1", "RB1"]  # 2 players
        trade.my_new_players = ["WR1", "TE1"]  # 2 players
        # Add new unequal trade fields
        trade.waiver_recommendations = None
        trade.my_dropped_players = None

        writer.save_waiver_trades_to_file([trade], mock_team)

        handle = mock_file()
        calls = [str(call) for call in handle.write.call_args_list]

        # Verify "2-for-2" label appears
        assert any("2-for-2" in call for call in calls)

    @patch('builtins.open', new_callable=mock_open)
    @patch('league_helper.trade_simulator_mode.trade_file_writer.datetime')
    def test_waiver_new_team_score(self, mock_datetime, mock_file, writer, mock_trade, mock_team):
        """Test that new team score is included in waiver output"""
        mock_datetime.now.return_value.strftime.return_value = "2025-10-17_12-00-00"

        writer.save_waiver_trades_to_file([mock_trade], mock_team)

        handle = mock_file()
        calls = [str(call) for call in handle.write.call_args_list]

        # Verify new team score appears
        assert any("New team score:" in call for call in calls)
        assert any("85.00" in call for call in calls)  # mock_trade.my_new_team.team_score


class TestSaveManualTradeToExcel:
    """Test save_manual_trade_to_excel method"""

    @pytest.fixture
    def mock_scored_player(self):
        """Create a mock ScoredPlayer with reason list"""
        player_obj = Mock()
        player_obj.name = "Test Player"
        player_obj.position = "RB"
        player_obj.team = "KC"
        player_obj.id = 1
        player_obj.bye_week = 7

        scored_player = Mock()
        scored_player.player = player_obj
        scored_player.score = 25.5
        scored_player.reason = [
            "Projected: 20.0 pts, Weighted: 22.0 pts",
            "Player Rating: EXCELLENT (1.05x)",
            "Team Quality: GOOD (1.02x)",
            "Performance: GOOD (+15.3%, 1.03x)",
            "Schedule: GOOD (avg opp def rank: 15.2, 1.02x)"
        ]
        return scored_player

    @pytest.fixture
    def mock_team_for_excel(self, mock_scored_player):
        """Create a mock TradeSimTeam for Excel export"""
        team = Mock(spec=TradeSimTeam)
        team.name = "Test Team"
        team.team_score = 100.0
        team.scored_players = {1: mock_scored_player}
        return team

    @pytest.fixture
    def mock_trade_for_excel(self, mock_scored_player, mock_team_for_excel):
        """Create a mock TradeSnapshot for Excel export"""
        trade = Mock(spec=TradeSnapshot)

        # Mock teams
        trade.my_new_team = mock_team_for_excel
        trade.their_new_team = mock_team_for_excel

        # Mock player lists
        trade.my_original_players = [mock_scored_player]
        trade.my_new_players = [mock_scored_player]
        trade.their_original_players = [mock_scored_player]
        trade.their_new_players = [mock_scored_player]

        # Mock optional lists
        trade.waiver_recommendations = None
        trade.their_waiver_recommendations = None
        trade.my_dropped_players = None
        trade.their_dropped_players = None

        return trade

    @patch.object(TradeFileWriter, '_apply_sheet_formatting')
    @patch('league_helper.trade_simulator_mode.trade_file_writer.pd.DataFrame.to_excel')
    @patch('league_helper.trade_simulator_mode.trade_file_writer.pd.ExcelWriter')
    @patch('league_helper.trade_simulator_mode.trade_file_writer.datetime')
    def test_creates_excel_file_with_correct_name(
        self, mock_datetime, mock_excel_writer, mock_to_excel, mock_formatting, writer,
        mock_trade_for_excel, mock_team_for_excel
    ):
        """Test that Excel file is created with correct filename"""
        mock_datetime.now.return_value.strftime.return_value = "20251017_120000"

        # Mock ExcelWriter context manager
        mock_writer_instance = MagicMock()
        mock_excel_writer.return_value.__enter__.return_value = mock_writer_instance
        mock_writer_instance.sheets = {
            "Summary": Mock(),
            "Trade Impact Analysis": Mock(),
            "Initial Rosters": Mock(),
            "Final Rosters": Mock(),
            "Detailed Calculations": Mock()
        }

        filename = writer.save_manual_trade_to_excel(
            mock_trade_for_excel,
            "Opponent Team",
            80.0,
            70.0,
            mock_team_for_excel,
            mock_team_for_excel
        )

        # Verify filename
        assert filename == "./league_helper/trade_simulator_mode/trade_outputs/trade_info_Opponent_Team_20251017_120000.xlsx"

        # Verify ExcelWriter was called with engine='openpyxl'
        mock_excel_writer.assert_called_once_with(filename, engine='openpyxl')

    @patch.object(TradeFileWriter, '_apply_sheet_formatting')
    @patch('league_helper.trade_simulator_mode.trade_file_writer.pd.DataFrame.to_excel')
    @patch('league_helper.trade_simulator_mode.trade_file_writer.pd.ExcelWriter')
    @patch('league_helper.trade_simulator_mode.trade_file_writer.pd.DataFrame')
    @patch('league_helper.trade_simulator_mode.trade_file_writer.datetime')
    def test_creates_all_required_sheets(
        self, mock_datetime, mock_dataframe, mock_excel_writer, mock_to_excel, mock_formatting, writer,
        mock_trade_for_excel, mock_team_for_excel
    ):
        """Test that all 5 sheets are created"""
        mock_datetime.now.return_value.strftime.return_value = "20251017_120000"

        # Mock ExcelWriter
        mock_writer_instance = MagicMock()
        mock_excel_writer.return_value.__enter__.return_value = mock_writer_instance
        mock_writer_instance.sheets = {
            "Summary": Mock(),
            "Trade Impact Analysis": Mock(),
            "Initial Rosters": Mock(),
            "Final Rosters": Mock(),
            "Detailed Calculations": Mock()
        }

        # Mock DataFrame
        mock_df = Mock()
        mock_dataframe.return_value = mock_df

        writer.save_manual_trade_to_excel(
            mock_trade_for_excel,
            "Opponent",
            80.0,
            70.0,
            mock_team_for_excel,
            mock_team_for_excel
        )

        # Verify to_excel was called with correct sheet names
        sheet_names = [call[1].get('sheet_name') for call in mock_df.to_excel.call_args_list]
        assert "Summary" in sheet_names
        assert "Trade Impact Analysis" in sheet_names
        assert "Initial Rosters" in sheet_names
        assert "Final Rosters" in sheet_names
        assert "Detailed Calculations" in sheet_names

    @patch.object(TradeFileWriter, '_apply_sheet_formatting')
    @patch('league_helper.trade_simulator_mode.trade_file_writer.pd.DataFrame.to_excel')
    @patch('league_helper.trade_simulator_mode.trade_file_writer.pd.ExcelWriter')
    @patch('league_helper.trade_simulator_mode.trade_file_writer.datetime')
    def test_sanitizes_opponent_name_in_filename(
        self, mock_datetime, mock_excel_writer, mock_to_excel, mock_formatting, writer,
        mock_trade_for_excel, mock_team_for_excel
    ):
        """Test that opponent name spaces are replaced with underscores"""
        mock_datetime.now.return_value.strftime.return_value = "20251017_120000"

        mock_writer_instance = MagicMock()
        mock_excel_writer.return_value.__enter__.return_value = mock_writer_instance
        mock_writer_instance.sheets = {
            "Summary": Mock(),
            "Trade Impact Analysis": Mock(),
            "Initial Rosters": Mock(),
            "Final Rosters": Mock(),
            "Detailed Calculations": Mock()
        }

        filename = writer.save_manual_trade_to_excel(
            mock_trade_for_excel,
            "Team With Spaces",
            80.0,
            70.0,
            mock_team_for_excel,
            mock_team_for_excel
        )

        assert "Team_With_Spaces" in filename
        assert "Team With Spaces" not in filename

    @patch.object(TradeFileWriter, '_apply_sheet_formatting')
    @patch('league_helper.trade_simulator_mode.trade_file_writer.pd.DataFrame.to_excel')
    @patch('league_helper.trade_simulator_mode.trade_file_writer.pd.ExcelWriter')
    @patch('league_helper.trade_simulator_mode.trade_file_writer.datetime')
    def test_logs_excel_creation(
        self, mock_datetime, mock_excel_writer, mock_to_excel, mock_formatting, writer,
        mock_trade_for_excel, mock_team_for_excel
    ):
        """Test that logger is called during Excel creation"""
        mock_datetime.now.return_value.strftime.return_value = "20251017_120000"

        mock_writer_instance = MagicMock()
        mock_excel_writer.return_value.__enter__.return_value = mock_writer_instance
        mock_writer_instance.sheets = {
            "Summary": Mock(),
            "Trade Impact Analysis": Mock(),
            "Initial Rosters": Mock(),
            "Final Rosters": Mock(),
            "Detailed Calculations": Mock()
        }

        writer.save_manual_trade_to_excel(
            mock_trade_for_excel,
            "Opponent",
            80.0,
            70.0,
            mock_team_for_excel,
            mock_team_for_excel
        )

        # Verify logger.info was called
        assert writer.logger.info.called

    @patch('league_helper.trade_simulator_mode.trade_file_writer.pd.ExcelWriter')
    @patch('league_helper.trade_simulator_mode.trade_file_writer.datetime')
    def test_exception_handling(
        self, mock_datetime, mock_excel_writer, writer,
        mock_trade_for_excel, mock_team_for_excel
    ):
        """Test that exceptions are caught and logged"""
        mock_datetime.now.return_value.strftime.return_value = "20251017_120000"

        # Make ExcelWriter raise an exception
        mock_excel_writer.side_effect = Exception("Excel creation failed")

        with pytest.raises(Exception):
            writer.save_manual_trade_to_excel(
                mock_trade_for_excel,
                "Opponent",
                80.0,
                70.0,
                mock_team_for_excel,
                mock_team_for_excel
            )

        # Verify error was logged
        assert writer.logger.error.called


class TestParseScoringReasons:
    """Test _parse_scoring_reasons helper method"""

    def test_parses_projected_points(self, writer):
        """Test parsing of projected points"""
        reasons = ["Projected: 20.5 pts, Weighted: 22.0 pts"]
        parsed = writer._parse_scoring_reasons(reasons)

        assert parsed["Base Projected"] == 20.5
        assert parsed["Weighted Proj"] == 22.0

    def test_parses_adp_rating(self, writer):
        """Test parsing of ADP rating and multiplier"""
        reasons = ["ADP: EXCELLENT (1.05x)"]
        parsed = writer._parse_scoring_reasons(reasons)

        assert parsed["ADP Rating"] == "EXCELLENT"
        assert parsed["ADP Multiplier"] == 1.05

    def test_parses_player_rating(self, writer):
        """Test parsing of player rating and multiplier"""
        reasons = ["Player Rating: GOOD (1.02x)"]
        parsed = writer._parse_scoring_reasons(reasons)

        assert parsed["Player Rating"] == "GOOD"
        assert parsed["Player Rating Multiplier"] == 1.02

    def test_parses_team_quality(self, writer):
        """Test parsing of team quality and multiplier"""
        reasons = ["Team Quality: VERY_POOR (0.95x)"]
        parsed = writer._parse_scoring_reasons(reasons)

        assert parsed["Team Quality"] == "VERY_POOR"
        assert parsed["Team Quality Multiplier"] == 0.95

    def test_parses_performance_with_percentage(self, writer):
        """Test parsing of performance with percentage and multiplier"""
        reasons = ["Performance: GOOD (+15.3%, 1.03x)"]
        parsed = writer._parse_scoring_reasons(reasons)

        assert parsed["Performance"] == "GOOD"
        assert parsed["Perf %"] == "+15.3"
        assert parsed["Performance Multiplier"] == 1.03

    def test_parses_schedule_with_rank(self, writer):
        """Test parsing of schedule with opponent rank and multiplier"""
        reasons = ["Schedule: EXCELLENT (avg opp def rank: 12.5, 1.05x)"]
        parsed = writer._parse_scoring_reasons(reasons)

        assert parsed["Schedule"] == "EXCELLENT"
        assert parsed["Avg Opp Rank"] == 12.5
        assert parsed["Schedule Multiplier"] == 1.05

    def test_parses_bye_overlaps(self, writer):
        """Test parsing of bye week overlaps and penalty points"""
        reasons = ["Bye Overlaps: 2 same-position, 3 different-position (-10.5 pts)"]
        parsed = writer._parse_scoring_reasons(reasons)

        assert parsed["Bye Same-Pos"] == 2
        assert parsed["Bye Diff-Pos"] == 3
        assert parsed["Bye Penalty"] == -10.5

    def test_parses_injury_status(self, writer):
        """Test parsing of injury status"""
        reasons = ["Injury: QUESTIONABLE (-5.0 pts)"]
        parsed = writer._parse_scoring_reasons(reasons)

        assert parsed["Injury Status"] == "QUESTIONABLE"

    def test_handles_empty_reasons(self, writer):
        """Test handling of empty reason list"""
        parsed = writer._parse_scoring_reasons([])
        assert parsed == {}

    def test_handles_empty_strings(self, writer):
        """Test handling of empty strings in reasons"""
        reasons = ["", "ADP: EXCELLENT (1.05x)", ""]
        parsed = writer._parse_scoring_reasons(reasons)

        assert parsed["ADP Rating"] == "EXCELLENT"
        assert parsed["ADP Multiplier"] == 1.05
        assert len(parsed) == 2

    def test_parses_multiple_reasons(self, writer):
        """Test parsing multiple reasons together"""
        reasons = [
            "Projected: 20.5 pts, Weighted: 22.0 pts",
            "ADP: EXCELLENT (1.05x)",
            "Player Rating: GOOD (1.02x)",
            "Team Quality: EXCELLENT (1.05x)",
            "Performance: GOOD (+15.3%, 1.03x)",
            "Schedule: GOOD (avg opp def rank: 15.2, 1.02x)",
            "Bye Overlaps: 1 same-position, 0 different-position (-5.0 pts)",
            "Injury: ACTIVE (-0.0 pts)"
        ]
        parsed = writer._parse_scoring_reasons(reasons)

        assert len(parsed) >= 10  # Should have multiple fields
        assert parsed["Base Projected"] == 20.5
        assert parsed["ADP Rating"] == "EXCELLENT"
        assert parsed["Performance"] == "GOOD"
