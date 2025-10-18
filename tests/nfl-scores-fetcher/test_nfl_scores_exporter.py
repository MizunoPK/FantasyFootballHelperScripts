"""
Unit Tests for NFL Scores Exporter Module

Tests the ScoresDataExporter class including export to various formats
(CSV, JSON, Excel) and data transformation methods.

Author: Kai Mizuno
"""

import pytest
import asyncio
from unittest.mock import Mock, MagicMock, patch, AsyncMock, call
from pathlib import Path
from datetime import datetime, timezone
import pandas as pd
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "nfl-scores-fetcher"))

from nfl_scores_exporter import ScoresDataExporter
from nfl_scores_models import WeeklyScores, GameScore, Team


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def temp_output_dir(tmp_path):
    """Create temporary output directory"""
    return str(tmp_path / "output")


@pytest.fixture
def exporter(temp_output_dir):
    """Create ScoresDataExporter instance"""
    return ScoresDataExporter(temp_output_dir)


@pytest.fixture
def sample_team_home():
    """Sample home team"""
    return Team(
        id="1",
        name="Cowboys",
        display_name="Dallas Cowboys",
        abbreviation="DAL",
        location="Dallas",
        record="8-2"
    )


@pytest.fixture
def sample_team_away():
    """Sample away team"""
    return Team(
        id="2",
        name="Giants",
        display_name="New York Giants",
        abbreviation="NYG",
        location="New York",
        record="4-6"
    )


@pytest.fixture
def sample_game(sample_team_home, sample_team_away):
    """Sample completed game"""
    return GameScore(
        game_id="401547416",
        date=datetime(2025, 9, 15, 13, 0, tzinfo=timezone.utc),
        week=5,
        season=2025,
        season_type=2,
        home_team=sample_team_home,
        away_team=sample_team_away,
        home_score=24,
        away_score=17,
        status="STATUS_FINAL",
        status_detail="Final",
        is_completed=True,
        is_overtime=False,
        venue_name="AT&T Stadium",
        venue_city="Arlington",
        venue_state="TX",
        home_total_yards=385,
        away_total_yards=312,
        home_turnovers=1,
        away_turnovers=2,
        home_score_q1=7,
        home_score_q2=7,
        home_score_q3=3,
        home_score_q4=7,
        away_score_q1=7,
        away_score_q2=3,
        away_score_q3=0,
        away_score_q4=7
    )


@pytest.fixture
def sample_games(sample_game, sample_team_home, sample_team_away):
    """List of sample games"""
    # Create second game
    team3 = Team(id="3", name="Eagles", display_name="Philadelphia Eagles",
                 abbreviation="PHI", location="Philadelphia", record="7-3")
    team4 = Team(id="4", name="Washington", display_name="Washington Commanders",
                 abbreviation="WAS", location="Washington", record="5-5")

    game2 = GameScore(
        game_id="401547417",
        date=datetime(2025, 9, 15, 16, 25, tzinfo=timezone.utc),
        week=5,
        season=2025,
        season_type=2,
        home_team=team3,
        away_team=team4,
        home_score=31,
        away_score=14,
        status="STATUS_FINAL",
        status_detail="Final",
        is_completed=True,
        is_overtime=False
    )

    return [sample_game, game2]


@pytest.fixture
def weekly_scores(sample_games):
    """Sample WeeklyScores container"""
    return WeeklyScores(
        week=5,
        season=2025,
        season_type=2,
        total_games=2,
        completed_games=2,
        games=sample_games
    )


# ============================================================================
# INITIALIZATION TESTS
# ============================================================================

class TestExporterInitialization:
    """Test ScoresDataExporter initialization"""

    def test_exporter_creates_output_directory(self, temp_output_dir):
        """Test exporter creates output directory if not exists"""
        exporter = ScoresDataExporter(temp_output_dir)

        assert Path(temp_output_dir).exists()
        assert exporter.output_dir == Path(temp_output_dir)

    def test_exporter_initializes_file_manager(self, exporter):
        """Test exporter initializes DataFileManager"""
        assert exporter.file_manager is not None

    def test_exporter_default_create_latest_files(self, temp_output_dir):
        """Test exporter defaults to creating latest files"""
        exporter = ScoresDataExporter(temp_output_dir)

        assert exporter.create_latest_files == True

    def test_exporter_can_disable_latest_files(self, temp_output_dir):
        """Test exporter can disable latest file creation"""
        exporter = ScoresDataExporter(temp_output_dir, create_latest_files=False)

        assert exporter.create_latest_files == False


# ============================================================================
# FILE PREFIX TESTS
# ============================================================================

class TestFilePrefix:
    """Test file prefix generation"""

    def test_get_file_prefix_with_week(self, exporter, weekly_scores):
        """Test file prefix includes week number"""
        prefix = exporter._get_file_prefix("nfl_scores", weekly_scores)

        assert prefix == "nfl_scores_week5"

    def test_get_file_prefix_recent_games(self, exporter, weekly_scores):
        """Test file prefix for recent games (week 0)"""
        weekly_scores.week = 0

        prefix = exporter._get_file_prefix("nfl_scores", weekly_scores)

        assert prefix == "nfl_scores_recent"


# ============================================================================
# GAME CONVERSION TESTS
# ============================================================================

class TestGameConversion:
    """Test game data conversion methods"""

    def test_game_to_dict_complete(self, exporter, sample_game):
        """Test converting GameScore to dictionary"""
        result = exporter._game_to_dict(sample_game)

        assert isinstance(result, dict)
        assert result['game_id'] == '401547416'
        assert result['week'] == 5
        assert result['home_team_abbr'] == 'DAL'
        assert result['away_team_abbr'] == 'NYG'
        assert result['home_score'] == 24
        assert result['away_score'] == 17
        assert result['total_points'] == 41
        assert result['winning_team'] == 'DAL'
        assert result['venue_name'] == 'AT&T Stadium'

    def test_game_to_dict_includes_quarter_scores(self, exporter, sample_game):
        """Test dictionary includes quarter-by-quarter scores"""
        result = exporter._game_to_dict(sample_game)

        assert result['home_q1'] == 7
        assert result['home_q2'] == 7
        assert result['home_q3'] == 3
        assert result['home_q4'] == 7
        assert result['away_q1'] == 7
        assert result['away_q2'] == 3
        assert result['away_q3'] == 0
        assert result['away_q4'] == 7

    def test_game_to_dict_includes_statistics(self, exporter, sample_game):
        """Test dictionary includes game statistics"""
        result = exporter._game_to_dict(sample_game)

        assert result['home_total_yards'] == 385
        assert result['away_total_yards'] == 312
        assert result['home_turnovers'] == 1
        assert result['away_turnovers'] == 2


# ============================================================================
# DATAFRAME CREATION TESTS
# ============================================================================

class TestDataFrameCreation:
    """Test DataFrame creation methods"""

    def test_create_dataframe_from_games(self, exporter, sample_games):
        """Test creating DataFrame from list of games"""
        df = exporter._create_dataframe(sample_games)

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert 'game_id' in df.columns
        assert 'home_team_abbr' in df.columns
        assert 'home_score' in df.columns

    def test_create_dataframe_empty_games(self, exporter):
        """Test creating DataFrame from empty games list"""
        df = exporter._create_dataframe([])

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0

    def test_create_condensed_dataframe(self, exporter, sample_games):
        """Test creating condensed team-centric DataFrame"""
        df = exporter._create_condensed_dataframe(sample_games)

        assert isinstance(df, pd.DataFrame)
        # Should have 4 rows (2 teams per game)
        assert len(df) == 4
        assert 'Team' in df.columns
        assert 'Opponent' in df.columns
        assert 'Points Scored' in df.columns
        assert 'Points Allowed' in df.columns

    def test_condensed_dataframe_sorted_by_team(self, exporter, sample_games):
        """Test condensed DataFrame is sorted by team name"""
        df = exporter._create_condensed_dataframe(sample_games)

        # Should be sorted alphabetically
        team_names = df['Team'].tolist()
        assert team_names == sorted(team_names)

    def test_condensed_dataframe_filters_incomplete_games(self, exporter, sample_game):
        """Test condensed DataFrame only includes completed games"""
        incomplete_game = GameScore(
            game_id="401547418",
            date=datetime(2025, 9, 15, 20, 0, tzinfo=timezone.utc),
            week=5,
            season=2025,
            season_type=2,
            home_team=sample_game.home_team,
            away_team=sample_game.away_team,
            home_score=14,
            away_score=10,
            status="STATUS_IN_PROGRESS",
            status_detail="3rd Quarter",
            is_completed=False,
            is_in_progress=True
        )

        df = exporter._create_condensed_dataframe([sample_game, incomplete_game])

        # Should only include the completed game (2 rows)
        assert len(df) == 2


# ============================================================================
# JSON EXPORT TESTS
# ============================================================================

class TestJSONExport:
    """Test JSON export functionality"""

    @pytest.mark.asyncio
    async def test_export_json_success(self, exporter, weekly_scores):
        """Test successful JSON export"""
        with patch.object(exporter.file_manager, 'save_json_data') as mock_save:
            mock_save.return_value = (Path("/tmp/test.json"), Path("/tmp/latest.json"))

            result = await exporter.export_json(weekly_scores)

            assert result is not None
            assert str(result) == "/tmp/test.json"
            mock_save.assert_called_once()

            # Verify JSON data structure
            call_args = mock_save.call_args
            json_data = call_args[0][0]
            assert json_data['week'] == 5
            assert json_data['season'] == 2025
            assert json_data['total_games'] == 2
            assert len(json_data['games']) == 2

    @pytest.mark.asyncio
    async def test_export_json_handles_errors(self, exporter, weekly_scores):
        """Test JSON export handles errors gracefully"""
        with patch.object(exporter.file_manager, 'save_json_data', side_effect=Exception("Write error")):
            result = await exporter.export_json(weekly_scores)

            assert result is None

    @pytest.mark.asyncio
    async def test_export_json_uses_file_prefix(self, exporter, weekly_scores):
        """Test JSON export uses correct file prefix"""
        with patch.object(exporter.file_manager, 'save_json_data') as mock_save:
            mock_save.return_value = (Path("/tmp/test.json"), Path("/tmp/latest.json"))

            await exporter.export_json(weekly_scores, file_prefix="custom_prefix")

            call_args = mock_save.call_args
            prefix_arg = call_args[0][1]
            assert "custom_prefix" in prefix_arg


# ============================================================================
# CSV EXPORT TESTS
# ============================================================================

class TestCSVExport:
    """Test CSV export functionality"""

    @pytest.mark.asyncio
    async def test_export_csv_success(self, exporter, weekly_scores):
        """Test successful CSV export"""
        with patch.object(exporter.file_manager, 'save_dataframe_csv', new=AsyncMock()) as mock_save:
            mock_save.return_value = (Path("/tmp/test.csv"), Path("/tmp/latest.csv"))

            result = await exporter.export_csv(weekly_scores)

            assert result is not None
            assert str(result) == "/tmp/test.csv"
            mock_save.assert_called_once()

            # Verify DataFrame was created
            call_args = mock_save.call_args
            df_arg = call_args[0][0]
            assert isinstance(df_arg, pd.DataFrame)
            assert len(df_arg) == 2

    @pytest.mark.asyncio
    async def test_export_csv_handles_errors(self, exporter, weekly_scores):
        """Test CSV export handles errors gracefully"""
        with patch.object(exporter.file_manager, 'save_dataframe_csv', new=AsyncMock(side_effect=Exception("Write error"))):
            result = await exporter.export_csv(weekly_scores)

            assert result is None

    @pytest.mark.asyncio
    async def test_export_csv_uses_file_prefix(self, exporter, weekly_scores):
        """Test CSV export uses correct file prefix"""
        with patch.object(exporter.file_manager, 'save_dataframe_csv', new=AsyncMock()) as mock_save:
            mock_save.return_value = (Path("/tmp/test.csv"), Path("/tmp/latest.csv"))

            await exporter.export_csv(weekly_scores, file_prefix="custom_prefix")

            call_args = mock_save.call_args
            prefix_arg = call_args[0][1]
            assert "custom_prefix" in prefix_arg


# ============================================================================
# EXCEL EXPORT TESTS
# ============================================================================

class TestExcelExport:
    """Test Excel export functionality"""

    @pytest.mark.asyncio
    async def test_export_excel_success(self, exporter, weekly_scores):
        """Test successful Excel export"""
        with patch.object(exporter.file_manager, 'get_timestamped_path') as mock_path, \
             patch.object(exporter.file_manager, 'enforce_file_caps') as mock_caps, \
             patch.object(exporter, '_write_excel_sheets') as mock_write:

            mock_path.return_value = Path("/tmp/test.xlsx")
            mock_caps.return_value = []

            result = await exporter.export_excel(weekly_scores)

            assert result is not None
            assert str(result) == "/tmp/test.xlsx"
            assert mock_write.call_count >= 1  # At least timestamped file

    @pytest.mark.asyncio
    async def test_export_excel_creates_latest_file(self, exporter, weekly_scores):
        """Test Excel export creates latest file when enabled"""
        exporter.create_latest_files = True

        with patch.object(exporter.file_manager, 'get_timestamped_path') as mock_ts_path, \
             patch.object(exporter.file_manager, 'get_latest_path') as mock_latest_path, \
             patch.object(exporter.file_manager, 'enforce_file_caps') as mock_caps, \
             patch.object(exporter, '_write_excel_sheets') as mock_write:

            mock_ts_path.return_value = Path("/tmp/test.xlsx")
            mock_latest_path.return_value = Path("/tmp/latest.xlsx")
            mock_caps.return_value = []

            await exporter.export_excel(weekly_scores)

            # Should write both timestamped and latest files
            assert mock_write.call_count == 2

    @pytest.mark.asyncio
    async def test_export_excel_handles_errors(self, exporter, weekly_scores):
        """Test Excel export handles errors gracefully"""
        with patch.object(exporter.file_manager, 'get_timestamped_path', side_effect=Exception("Path error")):
            result = await exporter.export_excel(weekly_scores)

            assert result is None


# ============================================================================
# CONDENSED EXCEL EXPORT TESTS
# ============================================================================

class TestCondensedExcelExport:
    """Test condensed Excel export functionality"""

    @pytest.mark.asyncio
    async def test_export_condensed_excel_success(self, exporter, weekly_scores):
        """Test successful condensed Excel export"""
        with patch.object(exporter.file_manager, 'get_timestamped_path') as mock_path, \
             patch.object(exporter.file_manager, 'enforce_file_caps') as mock_caps, \
             patch.object(exporter, '_write_condensed_excel_sheets') as mock_write:

            mock_path.return_value = Path("/tmp/test_condensed.xlsx")
            mock_caps.return_value = []

            result = await exporter.export_condensed_excel(weekly_scores)

            assert result is not None
            assert str(result) == "/tmp/test_condensed.xlsx"
            assert mock_write.call_count >= 1

    @pytest.mark.asyncio
    async def test_export_condensed_excel_uses_condensed_dataframe(self, exporter, weekly_scores):
        """Test condensed Excel export uses condensed DataFrame"""
        with patch.object(exporter.file_manager, 'get_timestamped_path') as mock_path, \
             patch.object(exporter.file_manager, 'enforce_file_caps') as mock_caps, \
             patch.object(exporter, '_write_condensed_excel_sheets') as mock_write:

            mock_path.return_value = Path("/tmp/test_condensed.xlsx")
            mock_caps.return_value = []

            await exporter.export_condensed_excel(weekly_scores)

            # Verify condensed DataFrame was created
            call_args = mock_write.call_args
            df_arg = call_args[0][0]
            assert isinstance(df_arg, pd.DataFrame)
            # Should have Team, Opponent, Points Scored, Points Allowed columns
            assert 'Team' in df_arg.columns
            assert 'Opponent' in df_arg.columns


# ============================================================================
# EXPORT ALL FORMATS TESTS
# ============================================================================

class TestExportAllFormats:
    """Test export_all_formats concurrent export"""

    @pytest.mark.asyncio
    async def test_export_all_formats_default(self, exporter, weekly_scores):
        """Test exporting all default formats (CSV, JSON, Excel)"""
        with patch.object(exporter, 'export_json', new=AsyncMock(return_value="test.json")), \
             patch.object(exporter, 'export_csv', new=AsyncMock(return_value="test.csv")), \
             patch.object(exporter, 'export_excel', new=AsyncMock(return_value="test.xlsx")):

            result = await exporter.export_all_formats(weekly_scores)

            assert len(result) == 3
            assert "test.json" in result
            assert "test.csv" in result
            assert "test.xlsx" in result

    @pytest.mark.asyncio
    async def test_export_all_formats_selective(self, exporter, weekly_scores):
        """Test exporting only selected formats"""
        with patch.object(exporter, 'export_json', new=AsyncMock(return_value="test.json")), \
             patch.object(exporter, 'export_csv', new=AsyncMock(return_value="test.csv")), \
             patch.object(exporter, 'export_excel', new=AsyncMock(return_value="test.xlsx")):

            result = await exporter.export_all_formats(
                weekly_scores,
                create_csv=False,
                create_json=True,
                create_excel=True
            )

            # Should only have JSON and Excel
            assert len(result) == 2
            exporter.export_csv.assert_not_called()

    @pytest.mark.asyncio
    async def test_export_all_formats_handles_exceptions(self, exporter, weekly_scores):
        """Test export_all_formats handles individual format failures"""
        with patch.object(exporter, 'export_json', new=AsyncMock(return_value="test.json")), \
             patch.object(exporter, 'export_csv', new=AsyncMock(side_effect=Exception("CSV error"))), \
             patch.object(exporter, 'export_excel', new=AsyncMock(return_value="test.xlsx")):

            result = await exporter.export_all_formats(weekly_scores)

            # Should have JSON and Excel, but CSV failed
            assert len(result) == 2
            assert "test.json" in result
            assert "test.xlsx" in result

    @pytest.mark.asyncio
    async def test_export_all_formats_empty_when_no_formats(self, exporter, weekly_scores):
        """Test export_all_formats returns empty list when no formats selected"""
        result = await exporter.export_all_formats(
            weekly_scores,
            create_csv=False,
            create_json=False,
            create_excel=False,
            create_condensed_excel=False
        )

        assert result == []

    @pytest.mark.asyncio
    async def test_export_all_formats_includes_condensed(self, exporter, weekly_scores):
        """Test export_all_formats includes condensed Excel when requested"""
        with patch.object(exporter, 'export_json', new=AsyncMock(return_value="test.json")), \
             patch.object(exporter, 'export_csv', new=AsyncMock(return_value="test.csv")), \
             patch.object(exporter, 'export_excel', new=AsyncMock(return_value="test.xlsx")), \
             patch.object(exporter, 'export_condensed_excel', new=AsyncMock(return_value="test_condensed.xlsx")):

            result = await exporter.export_all_formats(
                weekly_scores,
                create_condensed_excel=True
            )

            assert len(result) == 4
            exporter.export_condensed_excel.assert_called_once()


# ============================================================================
# EXCEL WRITING HELPER TESTS
# ============================================================================

class TestExcelWritingHelpers:
    """Test Excel writing helper methods"""

    def test_write_excel_sheets_creates_multiple_sheets(self, exporter, weekly_scores, sample_games, tmp_path):
        """Test _write_excel_sheets creates multiple sheets"""
        df = exporter._create_dataframe(sample_games)
        test_file = tmp_path / "test.xlsx"

        # Use real file path but mock the summary sheet creation to avoid complexity
        with patch.object(exporter, '_create_summary_sheet'):
            exporter._write_excel_sheets(df, str(test_file), weekly_scores)

            # Verify file was created
            assert test_file.exists()

    def test_write_condensed_excel_sheets_single_sheet(self, exporter, weekly_scores, sample_games):
        """Test _write_condensed_excel_sheets creates single sheet"""
        df = exporter._create_condensed_dataframe(sample_games)

        with patch.object(df, 'to_excel') as mock_to_excel:
            exporter._write_condensed_excel_sheets(df, "/tmp/test.xlsx", weekly_scores)

            # Should call to_excel once for single sheet
            mock_to_excel.assert_called_once()
            call_args = mock_to_excel.call_args
            assert call_args[0][0] == "/tmp/test.xlsx"
            assert call_args[1]['index'] == False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
