#!/usr/bin/env python3
"""
Tests for Player Data Exporter Module

Basic smoke tests for data export functionality.
Tests export to CSV, JSON, and Excel formats.

Author: Kai Mizuno
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path
import pandas as pd
import sys

# Add project root and player-data-fetcher to path
sys.path.append(str(Path(__file__).parent.parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent / "player-data-fetcher"))

from player_data_exporter import DataExporter
from player_data_models import ProjectionData, PlayerProjection


class TestDataExporterInit:
    """Test DataExporter initialization"""

    def test_exporter_initialization(self, tmp_path):
        """Test DataExporter can be initialized"""
        output_dir = str(tmp_path / "output")
        exporter = DataExporter(output_dir=output_dir)

        assert exporter.output_dir == Path(output_dir)
        assert exporter.create_latest_files == True

    def test_exporter_creates_output_directory(self, tmp_path):
        """Test DataExporter creates output directory if it doesn't exist"""
        output_dir = str(tmp_path / "nonexistent" / "output")
        exporter = DataExporter(output_dir=output_dir)

        assert exporter.output_dir.exists()

    def test_exporter_custom_latest_files_setting(self, tmp_path):
        """Test DataExporter respects create_latest_files setting"""
        output_dir = str(tmp_path / "output")
        exporter = DataExporter(output_dir=output_dir, create_latest_files=False)

        assert exporter.create_latest_files == False


class TestSetTeamData:
    """Test setting team rankings and schedules"""

    def test_set_team_rankings(self, tmp_path):
        """Test set_team_rankings stores data correctly"""
        exporter = DataExporter(output_dir=str(tmp_path))

        team_rankings = {'KC': {'offense': 1, 'defense': 5}}
        exporter.set_team_rankings(team_rankings)

        assert exporter.team_rankings == team_rankings

    def test_set_current_week_schedule(self, tmp_path):
        """Test set_current_week_schedule stores data correctly"""
        exporter = DataExporter(output_dir=str(tmp_path))

        schedule = {'KC': 'vs SF'}
        exporter.set_current_week_schedule(schedule)

        assert exporter.current_week_schedule == schedule


class TestCreateDataFrame:
    """Test DataFrame creation from projection data"""

    def test_create_dataframe_with_players(self, tmp_path):
        """Test _create_dataframe converts projection data to DataFrame"""
        exporter = DataExporter(output_dir=str(tmp_path))

        projection_data = ProjectionData(
            season=2024,
            scoring_format='PPR',
            total_players=2,
            players=[
                PlayerProjection(id="1", name="Player 1", position="QB", team="KC", fantasy_points=300.0),
                PlayerProjection(id="2", name="Player 2", position="RB", team="SF", fantasy_points=250.0)
            ]
        )

        df = exporter._create_dataframe(projection_data)

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert 'name' in df.columns
        assert 'position' in df.columns

    def test_create_dataframe_with_empty_data(self, tmp_path):
        """Test _create_dataframe handles empty player list"""
        exporter = DataExporter(output_dir=str(tmp_path))

        projection_data = ProjectionData(
            season=2024,
            scoring_format='PPR',
            total_players=0,
            players=[]
        )

        df = exporter._create_dataframe(projection_data)

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0


class TestPrepareExportDataFrame:
    """Test DataFrame preparation for export"""

    def test_prepare_export_dataframe(self, tmp_path):
        """Test _prepare_export_dataframe formats data correctly"""
        exporter = DataExporter(output_dir=str(tmp_path))

        projection_data = ProjectionData(
            season=2024,
            scoring_format='PPR',
            total_players=1,
            players=[
                PlayerProjection(id="1", name="Test Player", position="QB", team="KC", fantasy_points=300.0)
            ]
        )

        df = exporter._prepare_export_dataframe(projection_data)

        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0


class TestGetFantasyPlayers:
    """Test converting to FantasyPlayer objects"""

    def test_get_fantasy_players_returns_list(self, tmp_path):
        """Test get_fantasy_players returns list of FantasyPlayer objects"""
        exporter = DataExporter(output_dir=str(tmp_path))

        projection_data = ProjectionData(
            season=2024,
            scoring_format='PPR',
            total_players=1,
            players=[
                PlayerProjection(id="1", name="Test", position="QB", team="KC", fantasy_points=300.0)
            ]
        )

        result = exporter.get_fantasy_players(projection_data)

        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_fantasy_players_with_empty_data(self, tmp_path):
        """Test get_fantasy_players handles empty data"""
        exporter = DataExporter(output_dir=str(tmp_path))

        projection_data = ProjectionData(
            season=2024,
            scoring_format='PPR',
            total_players=0,
            players=[]
        )

        result = exporter.get_fantasy_players(projection_data)

        assert isinstance(result, list)
        assert len(result) == 0


class TestExportJSON:
    """Test JSON export functionality"""

    @pytest.mark.asyncio
    async def test_export_json_creates_file(self, tmp_path):
        """Test export_json creates JSON file"""
        exporter = DataExporter(output_dir=str(tmp_path))

        projection_data = ProjectionData(
            season=2024,
            scoring_format='PPR',
            total_players=1,
            players=[
                PlayerProjection(id="1", name="Test", position="QB", team="KC", fantasy_points=300.0)
            ]
        )

        filepath = await exporter.export_json(projection_data)

        assert Path(filepath).exists()
        assert filepath.endswith('.json')

    @pytest.mark.asyncio
    async def test_export_json_with_empty_data(self, tmp_path):
        """Test export_json handles empty data"""
        exporter = DataExporter(output_dir=str(tmp_path))

        projection_data = ProjectionData(
            season=2024,
            scoring_format='PPR',
            total_players=0,
            players=[]
        )

        filepath = await exporter.export_json(projection_data)

        assert Path(filepath).exists()


class TestExportCSV:
    """Test CSV export functionality"""

    @pytest.mark.asyncio
    async def test_export_csv_creates_file(self, tmp_path):
        """Test export_csv creates CSV file"""
        exporter = DataExporter(output_dir=str(tmp_path))

        projection_data = ProjectionData(
            season=2024,
            scoring_format='PPR',
            total_players=1,
            players=[
                PlayerProjection(id="1", name="Test", position="QB", team="KC", fantasy_points=300.0)
            ]
        )

        filepath = await exporter.export_csv(projection_data)

        assert Path(filepath).exists()
        assert filepath.endswith('.csv')

    @pytest.mark.asyncio
    async def test_export_csv_with_multiple_players(self, tmp_path):
        """Test export_csv with multiple players"""
        exporter = DataExporter(output_dir=str(tmp_path))

        projection_data = ProjectionData(
            season=2024,
            scoring_format='PPR',
            total_players=3,
            players=[
                PlayerProjection(id="1", name="Player 1", position="QB", team="KC", fantasy_points=300.0),
                PlayerProjection(id="2", name="Player 2", position="RB", team="SF", fantasy_points=250.0),
                PlayerProjection(id="3", name="Player 3", position="WR", team="BUF", fantasy_points=200.0)
            ]
        )

        filepath = await exporter.export_csv(projection_data)

        assert Path(filepath).exists()
        # Verify file has content
        df = pd.read_csv(filepath)
        assert len(df) == 3


class TestExportExcel:
    """Test Excel export functionality"""

    @pytest.mark.asyncio
    async def test_export_excel_creates_file(self, tmp_path):
        """Test export_excel creates Excel file"""
        exporter = DataExporter(output_dir=str(tmp_path))

        projection_data = ProjectionData(
            season=2024,
            scoring_format='PPR',
            total_players=1,
            players=[
                PlayerProjection(id="1", name="Test", position="QB", team="KC", fantasy_points=300.0)
            ]
        )

        filepath = await exporter.export_excel(projection_data)

        assert Path(filepath).exists()
        assert filepath.endswith('.xlsx')


class TestExportAllFormats:
    """Test exporting to all formats"""

    @pytest.mark.asyncio
    async def test_export_all_formats(self, tmp_path):
        """Test export_all_formats creates CSV, JSON, and Excel files"""
        exporter = DataExporter(output_dir=str(tmp_path))

        projection_data = ProjectionData(
            season=2024,
            scoring_format='PPR',
            total_players=1,
            players=[
                PlayerProjection(id="1", name="Test", position="QB", team="KC", fantasy_points=300.0)
            ]
        )

        files = await exporter.export_all_formats(
            projection_data,
            create_csv=True,
            create_json=True,
            create_excel=True
        )

        assert len(files) > 0
        # Should have created at least some files
        csv_files = [f for f in files if f.endswith('.csv')]
        json_files = [f for f in files if f.endswith('.json')]
        excel_files = [f for f in files if f.endswith('.xlsx')]

        assert len(csv_files) > 0
        assert len(json_files) > 0
        assert len(excel_files) > 0

    @pytest.mark.asyncio
    async def test_export_all_formats_selective(self, tmp_path):
        """Test export_all_formats with selective format creation"""
        exporter = DataExporter(output_dir=str(tmp_path))

        projection_data = ProjectionData(
            season=2024,
            scoring_format='PPR',
            total_players=1,
            players=[
                PlayerProjection(id="1", name="Test", position="QB", team="KC", fantasy_points=300.0)
            ]
        )

        files = await exporter.export_all_formats(
            projection_data,
            create_csv=True,
            create_json=False,
            create_excel=False
        )

        # Should only have CSV files
        assert all(f.endswith('.csv') for f in files)
