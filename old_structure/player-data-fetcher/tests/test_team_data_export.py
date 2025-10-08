#!/usr/bin/env python3
"""
Unit tests for team data export functionality in DataExporter.

Tests the new teams.csv export methods added to the data exporter
for the off/def ranking separation.

Author: Generated for NFL Fantasy Data Collection
Last Updated: September 2025
"""

import pytest
import tempfile
import asyncio
from pathlib import Path
from unittest.mock import patch, MagicMock
import pandas as pd
import os

import sys
sys.path.append(str(Path(__file__).parent.parent))
from player_data_models import ProjectionData, ESPNPlayerData
from player_data_exporter import DataExporter

sys.path.append(str(Path(__file__).parent.parent.parent))
from shared_files.TeamData import load_teams_from_csv


class TestTeamDataExport:
    """Test team data export functionality in DataExporter."""

    def setup_method(self):
        """Set up test fixtures."""
        # Create sample player data
        self.sample_players = [
            ESPNPlayerData(
                id='1',
                name='Patrick Mahomes',
                team='KC',
                position='QB',
                fantasy_points=300.0,
                player_rating=100.0
            ),
            ESPNPlayerData(
                id='2',
                name='Saquon Barkley',
                team='PHI',
                position='RB',
                fantasy_points=250.0,
                player_rating=95.0
            ),
            ESPNPlayerData(
                id='3',
                name='Another KC Player',
                team='KC',
                position='WR',
                fantasy_points=200.0,
                player_rating=90.0
            ),
            ESPNPlayerData(
                id='4',
                name='Buffalo Player',
                team='BUF',
                position='TE',
                fantasy_points=150.0,
                player_rating=85.0
            )
        ]

        self.sample_projection_data = ProjectionData(
            season=2025,
            scoring_format='ppr',
            total_players=len(self.sample_players),
            players=self.sample_players
        )

    @pytest.mark.asyncio
    async def test_export_teams_csv(self):
        """Test exporting teams to CSV format."""
        with tempfile.TemporaryDirectory() as temp_dir:
            exporter = DataExporter(temp_dir)

            # Mock the get_fantasy_players method since we don't have the full conversion
            with patch.object(exporter, 'get_fantasy_players') as mock_get_players:
                # Mock FantasyPlayer objects with team ranking data
                mock_players = [
                    MagicMock(team='KC', team_offensive_rank=1, team_defensive_rank=5),
                    MagicMock(team='PHI', team_offensive_rank=8, team_defensive_rank=17),
                    MagicMock(team='BUF', team_offensive_rank=4, team_defensive_rank=13)
                ]
                mock_get_players.return_value = mock_players

                # Export teams CSV
                result_path = await exporter.export_teams_csv(self.sample_projection_data)

                # Verify file was created
                assert os.path.exists(result_path)
                assert result_path.endswith('.csv')
                assert 'teams_' in result_path

                # Load and verify teams data
                teams = load_teams_from_csv(result_path)
                assert len(teams) == 3

                # Verify team data (should be sorted by team name)
                team_names = [team.team for team in teams]
                assert team_names == ['BUF', 'KC', 'PHI']  # Alphabetical order

                # Check specific team data
                kc_team = next(team for team in teams if team.team == 'KC')
                assert kc_team.offensive_rank == 1
                assert kc_team.defensive_rank == 5

                phi_team = next(team for team in teams if team.team == 'PHI')
                assert phi_team.offensive_rank == 8
                assert phi_team.defensive_rank == 17

    @pytest.mark.asyncio
    async def test_export_teams_csv_latest_file(self):
        """Test that latest teams file is created."""
        with tempfile.TemporaryDirectory() as temp_dir:
            exporter = DataExporter(temp_dir, create_latest_files=True)

            with patch.object(exporter, 'get_fantasy_players') as mock_get_players:
                mock_players = [
                    MagicMock(team='KC', team_offensive_rank=1, team_defensive_rank=5),
                ]
                mock_get_players.return_value = mock_players

                await exporter.export_teams_csv(self.sample_projection_data)

                # Verify latest file was created
                latest_file = Path(temp_dir) / "teams_latest.csv"
                assert latest_file.exists()

                teams = load_teams_from_csv(str(latest_file))
                assert len(teams) == 1
                assert teams[0].team == 'KC'

    @pytest.mark.asyncio
    async def test_export_teams_to_shared_files(self):
        """Test exporting teams to shared_files directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            exporter = DataExporter(temp_dir)

            with patch.object(exporter, 'get_fantasy_players') as mock_get_players:
                mock_players = [
                    MagicMock(team='DAL', team_offensive_rank=12, team_defensive_rank=22),
                    MagicMock(team='NYG', team_offensive_rank=28, team_defensive_rank=2)
                ]
                mock_get_players.return_value = mock_players

                # Mock the save_teams_to_csv function instead of trying to mock Path
                with patch('player_data_exporter.save_teams_to_csv') as mock_save:
                    result_path = await exporter.export_teams_to_shared_files(self.sample_projection_data)

                    # Verify the result path
                    assert 'teams.csv' in result_path

                    # Verify save_teams_to_csv was called
                    mock_save.assert_called_once()
                    call_args = mock_save.call_args
                    teams_data = call_args[0][0]  # First argument (teams list)

                    # Verify the teams data that was passed
                    assert len(teams_data) == 2
                    team_names = [team.team for team in teams_data]
                    assert 'DAL' in team_names
                    assert 'NYG' in team_names

    @pytest.mark.asyncio
    async def test_export_teams_csv_empty_players(self):
        """Test exporting teams with empty player list."""
        with tempfile.TemporaryDirectory() as temp_dir:
            exporter = DataExporter(temp_dir)

            empty_projection_data = ProjectionData(
                season=2025,
                scoring_format='ppr',
                total_players=0,
                players=[]
            )

            with patch.object(exporter, 'get_fantasy_players') as mock_get_players:
                mock_get_players.return_value = []

                result_path = await exporter.export_teams_csv(empty_projection_data)

                # Verify file was created even with no teams
                assert os.path.exists(result_path)

                teams = load_teams_from_csv(result_path)
                assert len(teams) == 0

                # Verify CSV structure is correct (has headers)
                df = pd.read_csv(result_path)
                expected_columns = ['team', 'offensive_rank', 'defensive_rank', 'opponent']
                assert list(df.columns) == expected_columns

    @pytest.mark.asyncio
    async def test_export_teams_csv_duplicate_teams(self):
        """Test that duplicate teams are handled correctly."""
        with tempfile.TemporaryDirectory() as temp_dir:
            exporter = DataExporter(temp_dir)

            with patch.object(exporter, 'get_fantasy_players') as mock_get_players:
                # Multiple players from same team
                mock_players = [
                    MagicMock(team='KC', team_offensive_rank=1, team_defensive_rank=5),
                    MagicMock(team='KC', team_offensive_rank=1, team_defensive_rank=5),
                    MagicMock(team='PHI', team_offensive_rank=8, team_defensive_rank=17),
                    MagicMock(team='PHI', team_offensive_rank=8, team_defensive_rank=17)
                ]
                mock_get_players.return_value = mock_players

                result_path = await exporter.export_teams_csv(self.sample_projection_data)

                teams = load_teams_from_csv(result_path)

                # Should only have unique teams
                assert len(teams) == 2
                team_names = [team.team for team in teams]
                assert 'KC' in team_names
                assert 'PHI' in team_names

    @pytest.mark.asyncio
    async def test_export_all_formats_with_teams(self):
        """Test the new export_all_formats_with_teams method."""
        with tempfile.TemporaryDirectory() as temp_dir:
            exporter = DataExporter(temp_dir)

            with patch.object(exporter, 'get_fantasy_players') as mock_get_players:
                mock_players = [
                    MagicMock(team='KC', team_offensive_rank=1, team_defensive_rank=5)
                ]
                mock_get_players.return_value = mock_players

                # Mock the individual export methods
                with patch.object(exporter, 'export_json') as mock_json, \
                     patch.object(exporter, 'export_csv') as mock_csv, \
                     patch.object(exporter, 'export_excel') as mock_excel, \
                     patch.object(exporter, 'export_to_shared_files') as mock_shared_players, \
                     patch.object(exporter, 'export_teams_csv') as mock_teams_csv, \
                     patch.object(exporter, 'export_teams_to_shared_files') as mock_shared_teams:

                    # Set up return values
                    mock_json.return_value = 'data.json'
                    mock_csv.return_value = 'data.csv'
                    mock_excel.return_value = 'data.xlsx'
                    mock_shared_players.return_value = 'shared_files/players.csv'
                    mock_teams_csv.return_value = 'teams.csv'
                    mock_shared_teams.return_value = 'shared_files/teams.csv'

                    # Test with all formats enabled
                    result_paths = await exporter.export_all_formats_with_teams(
                        self.sample_projection_data,
                        create_csv=True,
                        create_json=True,
                        create_excel=True
                    )

                    # Verify all methods were called
                    mock_json.assert_called_once()
                    mock_csv.assert_called_once()
                    mock_excel.assert_called_once()
                    mock_shared_players.assert_called_once()
                    mock_teams_csv.assert_called_once()
                    mock_shared_teams.assert_called_once()

                    # Verify result paths
                    assert len(result_paths) == 6
                    assert 'data.json' in result_paths
                    assert 'data.csv' in result_paths
                    assert 'teams.csv' in result_paths

    @pytest.mark.asyncio
    async def test_export_all_formats_with_teams_selective(self):
        """Test export_all_formats_with_teams with selective format creation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            exporter = DataExporter(temp_dir)

            with patch.object(exporter, 'get_fantasy_players') as mock_get_players:
                mock_get_players.return_value = []

                # Mock the individual export methods
                with patch.object(exporter, 'export_json') as mock_json, \
                     patch.object(exporter, 'export_csv') as mock_csv, \
                     patch.object(exporter, 'export_excel') as mock_excel, \
                     patch.object(exporter, 'export_to_shared_files') as mock_shared_players, \
                     patch.object(exporter, 'export_teams_csv') as mock_teams_csv, \
                     patch.object(exporter, 'export_teams_to_shared_files') as mock_shared_teams:

                    mock_shared_players.return_value = 'shared_files/players.csv'
                    mock_shared_teams.return_value = 'shared_files/teams.csv'

                    # Test with only JSON enabled
                    await exporter.export_all_formats_with_teams(
                        self.sample_projection_data,
                        create_csv=False,
                        create_json=True,
                        create_excel=False
                    )

                    # Only JSON and shared files should be called
                    mock_json.assert_called_once()
                    mock_csv.assert_not_called()
                    mock_excel.assert_not_called()
                    mock_shared_players.assert_called_once()
                    mock_teams_csv.assert_not_called()  # No CSV creation
                    mock_shared_teams.assert_called_once()  # Always create shared teams

    @pytest.mark.asyncio
    async def test_teams_export_error_handling(self):
        """Test error handling in teams export methods."""
        with tempfile.TemporaryDirectory() as temp_dir:
            exporter = DataExporter(temp_dir)

            with patch.object(exporter, 'get_fantasy_players') as mock_get_players:
                # Make get_fantasy_players raise an exception
                mock_get_players.side_effect = Exception("Test error")

                # Should raise exception
                with pytest.raises(Exception, match="Test error"):
                    await exporter.export_teams_csv(self.sample_projection_data)

    @pytest.mark.asyncio
    async def test_teams_export_file_cleanup(self):
        """Test that file cleanup is called during teams export."""
        with tempfile.TemporaryDirectory() as temp_dir:
            exporter = DataExporter(temp_dir)

            with patch.object(exporter, 'get_fantasy_players') as mock_get_players:
                mock_get_players.return_value = []

                # Mock the file manager cleanup
                with patch.object(exporter.file_manager, 'cleanup_all_file_types') as mock_cleanup:
                    await exporter.export_teams_csv(self.sample_projection_data)

                    # Verify cleanup was called
                    mock_cleanup.assert_called_once()


if __name__ == '__main__':
    pytest.main([__file__])