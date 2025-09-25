#!/usr/bin/env python3
"""
Unit tests for TeamData class and related functionality.

Tests the team data model, CSV import/export, and team data extraction
from player lists.

Author: Generated for NFL Fantasy Data Collection
Last Updated: September 2025
"""

import pytest
import tempfile
import os
from pathlib import Path
import pandas as pd

import sys
sys.path.append(str(Path(__file__).parent.parent))
from TeamData import TeamData, load_teams_from_csv, save_teams_to_csv, extract_teams_from_players
from FantasyPlayer import FantasyPlayer


class TestTeamData:
    """Test the TeamData class functionality."""

    def test_team_data_creation(self):
        """Test basic TeamData object creation."""
        team = TeamData(
            team='PHI',
            offensive_rank=8,
            defensive_rank=17,
            opponent='NYG'
        )

        assert team.team == 'PHI'
        assert team.offensive_rank == 8
        assert team.defensive_rank == 17
        assert team.opponent == 'NYG'

    def test_team_data_creation_with_defaults(self):
        """Test TeamData creation with default values."""
        team = TeamData(team='KC')

        assert team.team == 'KC'
        assert team.offensive_rank is None
        assert team.defensive_rank is None
        assert team.opponent is None

    def test_team_data_from_dict(self):
        """Test TeamData creation from dictionary."""
        data = {
            'team': 'BUF',
            'offensive_rank': '4',  # String should be converted to int
            'defensive_rank': '13',
            'opponent': 'MIA'
        }

        team = TeamData.from_dict(data)

        assert team.team == 'BUF'
        assert team.offensive_rank == 4
        assert team.defensive_rank == 13
        assert team.opponent == 'MIA'

    def test_team_data_from_dict_invalid_ranks(self):
        """Test TeamData creation with invalid rank values."""
        data = {
            'team': 'DAL',
            'offensive_rank': 'invalid',
            'defensive_rank': '',
            'opponent': None
        }

        team = TeamData.from_dict(data)

        assert team.team == 'DAL'
        assert team.offensive_rank is None  # Invalid string should be None
        assert team.defensive_rank is None  # Empty string should be None
        assert team.opponent is None

    def test_team_data_to_dict(self):
        """Test TeamData conversion to dictionary."""
        team = TeamData(
            team='SF',
            offensive_rank=23,
            defensive_rank=20,
            opponent='LAR'
        )

        data_dict = team.to_dict()

        expected = {
            'team': 'SF',
            'offensive_rank': 23,
            'defensive_rank': 20,
            'opponent': 'LAR'
        }

        assert data_dict == expected

    def test_team_data_to_dict_with_none_values(self):
        """Test TeamData to_dict with None values."""
        team = TeamData(team='NYG')

        data_dict = team.to_dict()

        expected = {
            'team': 'NYG',
            'offensive_rank': None,
            'defensive_rank': None,
            'opponent': None
        }

        assert data_dict == expected


class TestTeamDataCSVOperations:
    """Test CSV import/export functionality for TeamData."""

    def test_save_and_load_teams_csv(self):
        """Test saving and loading teams to/from CSV."""
        teams = [
            TeamData(team='PHI', offensive_rank=8, defensive_rank=17, opponent='NYG'),
            TeamData(team='KC', offensive_rank=1, defensive_rank=5, opponent='LV'),
            TeamData(team='BUF', offensive_rank=4, defensive_rank=13)  # No opponent
        ]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_path = f.name

        try:
            # Save teams to CSV
            save_teams_to_csv(teams, temp_path)

            # Load teams from CSV
            loaded_teams = load_teams_from_csv(temp_path)

            assert len(loaded_teams) == 3

            # Check first team
            assert loaded_teams[0].team == 'PHI'
            assert loaded_teams[0].offensive_rank == 8
            assert loaded_teams[0].defensive_rank == 17
            assert loaded_teams[0].opponent == 'NYG'

            # Check second team
            assert loaded_teams[1].team == 'KC'
            assert loaded_teams[1].offensive_rank == 1
            assert loaded_teams[1].defensive_rank == 5
            assert loaded_teams[1].opponent == 'LV'

            # Check third team (no opponent)
            assert loaded_teams[2].team == 'BUF'
            assert loaded_teams[2].offensive_rank == 4
            assert loaded_teams[2].defensive_rank == 13
            assert loaded_teams[2].opponent is None

        finally:
            os.unlink(temp_path)

    def test_save_empty_teams_csv(self):
        """Test saving empty teams list to CSV."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_path = f.name

        try:
            # Save empty list
            save_teams_to_csv([], temp_path)

            # Load and verify structure
            loaded_teams = load_teams_from_csv(temp_path)

            assert len(loaded_teams) == 0

            # Verify CSV has correct headers
            df = pd.read_csv(temp_path)
            expected_columns = ['team', 'offensive_rank', 'defensive_rank', 'opponent']
            assert list(df.columns) == expected_columns

        finally:
            os.unlink(temp_path)

    def test_load_teams_nonexistent_file(self):
        """Test loading from nonexistent file."""
        with pytest.raises(FileNotFoundError):
            load_teams_from_csv('/nonexistent/path/teams.csv')

    def test_load_teams_malformed_csv(self):
        """Test loading from malformed CSV file with missing required columns."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("invalid,csv,data\nwith,wrong,columns,too,many")
            temp_path = f.name

        try:
            # Should load successfully but with empty team data due to missing columns
            teams = load_teams_from_csv(temp_path)

            # Should have one row with empty/default values
            assert len(teams) == 1
            assert teams[0].team == ''  # No 'team' column, so defaults to empty
            assert teams[0].offensive_rank is None
            assert teams[0].defensive_rank is None
            assert teams[0].opponent is None
        finally:
            os.unlink(temp_path)


class TestExtractTeamsFromPlayers:
    """Test team data extraction from player lists."""

    def test_extract_teams_from_players(self):
        """Test extracting unique teams from player list."""
        # Create mock players with team ranking attributes using MagicMock
        from unittest.mock import MagicMock

        players = []

        # Create mock player for PHI
        phi_player = MagicMock()
        phi_player.team = 'PHI'
        phi_player.team_offensive_rank = 8
        phi_player.team_defensive_rank = 17
        players.append(phi_player)

        # Create another PHI player to test deduplication
        phi_player2 = MagicMock()
        phi_player2.team = 'PHI'
        phi_player2.team_offensive_rank = 8
        phi_player2.team_defensive_rank = 17
        players.append(phi_player2)

        # Create KC player
        kc_player = MagicMock()
        kc_player.team = 'KC'
        kc_player.team_offensive_rank = 1
        kc_player.team_defensive_rank = 5
        players.append(kc_player)

        # Create DAL player
        dal_player = MagicMock()
        dal_player.team = 'DAL'
        dal_player.team_offensive_rank = 12
        dal_player.team_defensive_rank = 22
        players.append(dal_player)

        teams = extract_teams_from_players(players)

        # Should get 3 unique teams, sorted by name
        assert len(teams) == 3
        assert teams[0].team == 'DAL'
        assert teams[1].team == 'KC'
        assert teams[2].team == 'PHI'

        # Check team data extraction
        phi_team = teams[2]  # PHI is last alphabetically
        assert phi_team.offensive_rank == 8
        assert phi_team.defensive_rank == 17
        assert phi_team.opponent is None  # Not populated by extraction

        kc_team = teams[1]  # KC is second
        assert kc_team.offensive_rank == 1
        assert kc_team.defensive_rank == 5

    def test_extract_teams_missing_attributes(self):
        """Test extraction when players don't have team ranking attributes."""
        # Create players without team ranking attributes
        players = [
            FantasyPlayer(id='1', name='Player 1', team='PHI', position='QB'),
            FantasyPlayer(id='2', name='Player 2', team='KC', position='RB')
        ]

        teams = extract_teams_from_players(players)

        assert len(teams) == 2
        assert teams[1].team == 'PHI'  # Second alphabetically
        assert teams[1].offensive_rank is None  # No attribute found
        assert teams[1].defensive_rank is None

    def test_extract_teams_empty_list(self):
        """Test extraction from empty player list."""
        teams = extract_teams_from_players([])
        assert len(teams) == 0

    def test_extract_teams_no_team_names(self):
        """Test extraction when players have empty team names."""
        players = [
            FantasyPlayer(id='1', name='Player 1', team='', position='QB'),
            FantasyPlayer(id='2', name='Player 2', team=None, position='RB')
        ]

        teams = extract_teams_from_players(players)
        assert len(teams) == 0  # No valid teams to extract

    def test_extract_teams_duplicate_handling(self):
        """Test that duplicate teams are properly handled."""
        from unittest.mock import MagicMock

        players = []
        for i in range(3):
            player = MagicMock()
            player.team = 'PHI'
            player.team_offensive_rank = 8
            player.team_defensive_rank = 17
            players.append(player)

        teams = extract_teams_from_players(players)

        # Should only get one PHI team entry
        assert len(teams) == 1
        assert teams[0].team == 'PHI'
        assert teams[0].offensive_rank == 8

    def test_extract_teams_sorting(self):
        """Test that extracted teams are sorted alphabetically."""
        players = [
            FantasyPlayer(id='1', name='Player 1', team='ZZZ', position='QB'),
            FantasyPlayer(id='2', name='Player 2', team='AAA', position='RB'),
            FantasyPlayer(id='3', name='Player 3', team='MMM', position='WR')
        ]

        teams = extract_teams_from_players(players)

        assert len(teams) == 3
        assert teams[0].team == 'AAA'
        assert teams[1].team == 'MMM'
        assert teams[2].team == 'ZZZ'


if __name__ == '__main__':
    pytest.main([__file__])