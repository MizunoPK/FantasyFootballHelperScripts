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


class TestPositionJSONExport:
    """Test that position JSON export still works after legacy format removal"""

    @pytest.mark.asyncio
    async def test_position_json_files_created(self, tmp_path):
        """Test that position JSON files are created (regression test)"""
        output_dir = tmp_path / "player-data-fetcher" / "data"

        exporter = DataExporter(output_dir=str(output_dir))

        projection_data = ProjectionData(
            season=2024,
            scoring_format='PPR',
            total_players=2,
            players=[
                PlayerProjection(id="1", name="QB Player", position="QB", team="KC", fantasy_points=300.0),
                PlayerProjection(id="2", name="RB Player", position="RB", team="SF", fantasy_points=250.0)
            ]
        )

        # Set team data required for export
        exporter.set_team_rankings({'KC': {'offense': 1, 'defense': 5}, 'SF': {'offense': 2, 'defense': 3}})

        # Export position JSON files directly
        files = await exporter.export_position_json_files(projection_data)

        # Verify JSON files were created
        assert len(files) > 0, "Position JSON files should be created"
        assert all(f.endswith('.json') for f in files), "All files should be JSON"
