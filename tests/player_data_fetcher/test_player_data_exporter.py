#!/usr/bin/env python3
"""
Tests for Player Data Exporter Module

Basic smoke tests for data export functionality.

Author: Kai Mizuno
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path

from player_data_fetcher.player_data_exporter import DataExporter
from player_data_fetcher.player_data_models import ProjectionData, PlayerProjection


class TestDataExporterInit:
    """Test DataExporter initialization"""

    def test_exporter_initialization(self, tmp_path):
        """Test DataExporter can be initialized"""
        output_dir = str(tmp_path / "output")
        exporter = DataExporter(output_dir=output_dir)

        assert exporter.output_dir == Path(output_dir)

    def test_exporter_creates_output_directory(self, tmp_path):
        """Test DataExporter creates output directory if it doesn't exist"""
        output_dir = str(tmp_path / "nonexistent" / "output")
        exporter = DataExporter(output_dir=output_dir)

        assert exporter.output_dir.exists()

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
        output_dir = tmp_path / "player_data_fetcher" / "data"

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

        exporter.set_team_rankings({'KC': {'offense': 1, 'defense': 5}, 'SF': {'offense': 2, 'defense': 3}})

        files = await exporter.export_position_json_files(projection_data)

        assert len(files) > 0, "Position JSON files should be created"
        assert all(f.endswith('.json') for f in files), "All files should be JSON"



class TestDataExporterKAI10:
    """
    Tests verifying KAI-10 refactoring: DataExporter constructor accepts
    new parameters and defaults match old config.py values.
    (REQ-07 — 6 tests)
    """

    def test_exporter_accepts_my_team_name_parameter(self, tmp_path):
        """7.1: DataExporter accepts my_team_name constructor parameter"""
        exporter = DataExporter(
            output_dir=str(tmp_path),
            my_team_name='Test Team',
        )
        assert exporter.my_team_name == 'Test Team'

    def test_exporter_accepts_current_nfl_week_parameter(self, tmp_path):
        """7.2: DataExporter accepts current_nfl_week constructor parameter"""
        exporter = DataExporter(
            output_dir=str(tmp_path),
            current_nfl_week=10,
        )
        assert exporter.current_nfl_week == 10

    def test_exporter_backward_compat_no_new_params(self, tmp_path):
        """7.3: DataExporter(output_dir=...) still works without new params (backward compat)"""
        exporter = DataExporter(output_dir=str(tmp_path))
        assert exporter.current_nfl_week == 17
        assert exporter.my_team_name == 'Sea Sharp'
        assert exporter.load_drafted_data is True

    def test_exporter_defaults_match_old_config_values(self, tmp_path):
        """I-8: DataExporter defaults preserve backward compat with old config values"""
        exporter = DataExporter(output_dir=str(tmp_path))
        assert exporter.position_json_output == '../data/player_data'
        assert exporter.team_data_folder == '../data/team_data'
        assert exporter.drafted_data_path == '../data/drafted_data.csv'

    def test_exporter_custom_team_name_used(self, tmp_path):
        """E-14: DataExporter with custom my_team_name stores it correctly"""
        exporter = DataExporter(
            output_dir=str(tmp_path),
            my_team_name='My Custom Team',
        )
        assert exporter.my_team_name == 'My Custom Team'

    def test_exporter_custom_drafted_data_path(self, tmp_path):
        """E-18: DataExporter with custom drafted_data_path stores it correctly"""
        custom_path = str(tmp_path / 'custom_drafted.csv')
        exporter = DataExporter(
            output_dir=str(tmp_path),
            drafted_data_path=custom_path,
        )
        assert exporter.drafted_data_path == custom_path


