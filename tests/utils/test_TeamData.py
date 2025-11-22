#!/usr/bin/env python3
"""
Tests for TeamData module.

Comprehensive tests for TeamData class, conversion helpers, and
team data extraction functions.

Author: Kai Mizuno
"""

import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import Mock

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from utils.TeamData import (
    TeamData,
    _safe_int_conversion,
    _safe_string_conversion,
    load_team_weekly_data,
    save_team_weekly_data,
    load_single_team_data,
    save_single_team_data,
    NFL_TEAMS
)
from utils.FantasyPlayer import FantasyPlayer

# Note: Old functions (load_teams_from_csv, save_teams_to_csv, extract_teams_from_players,
# extract_teams_from_rankings) have been removed as part of team_data refactor.
# Tests using these functions are marked with pytest.skip until updated.


class TestTeamDataInit:
    """Test suite for TeamData initialization."""

    def test_team_data_initialization_minimal(self):
        """Test TeamData initializes with just team name."""
        team = TeamData(team='KC')

        assert team.team == 'KC'
        assert team.offensive_rank is None
        assert team.defensive_rank is None

    def test_team_data_initialization_complete(self):
        """Test TeamData initializes with all fields."""
        team = TeamData(
            team='PHI',
            offensive_rank=5,
            defensive_rank=12
        )

        assert team.team == 'PHI'
        assert team.offensive_rank == 5
        assert team.defensive_rank == 12


class TestTeamDataFromDict:
    """Test suite for TeamData.from_dict() method."""

    def test_from_dict_complete_data(self):
        """Test from_dict() with all fields present."""
        data = {
            'team': 'BUF',
            'offensive_rank': 3,
            'defensive_rank': 8
        }

        team = TeamData.from_dict(data)

        assert team.team == 'BUF'
        assert team.offensive_rank == 3
        assert team.defensive_rank == 8

    def test_from_dict_missing_optional_fields(self):
        """Test from_dict() with only team field."""
        data = {'team': 'KC'}

        team = TeamData.from_dict(data)

        assert team.team == 'KC'
        assert team.offensive_rank is None
        assert team.defensive_rank is None

    def test_from_dict_handles_string_ranks(self):
        """Test from_dict() converts string ranks to int."""
        data = {
            'team': 'SF',
            'offensive_rank': '10',
            'defensive_rank': '15'
        }

        team = TeamData.from_dict(data)

        assert team.offensive_rank == 10
        assert team.defensive_rank == 15

    def test_from_dict_handles_nan_values(self):
        """Test from_dict() converts NaN to None."""
        data = {
            'team': 'NE',
            'offensive_rank': 'nan',
            'defensive_rank': float('nan')
        }

        team = TeamData.from_dict(data)

        assert team.offensive_rank is None
        assert team.defensive_rank is None

    def test_from_dict_empty_team(self):
        """Test from_dict() with empty team field."""
        data = {}

        team = TeamData.from_dict(data)

        assert team.team == ''


class TestTeamDataToDict:
    """Test suite for TeamData.to_dict() method."""

    def test_to_dict_complete_data(self):
        """Test to_dict() with all fields populated."""
        team = TeamData(
            team='DAL',
            offensive_rank=7,
            defensive_rank=20,
            def_vs_qb_rank=5,
            def_vs_rb_rank=12,
            def_vs_wr_rank=8,
            def_vs_te_rank=15,
            def_vs_k_rank=20
        )

        result = team.to_dict()

        assert result == {
            'team': 'DAL',
            'offensive_rank': 7,
            'defensive_rank': 20,
            'def_vs_qb_rank': 5,
            'def_vs_rb_rank': 12,
            'def_vs_wr_rank': 8,
            'def_vs_te_rank': 15,
            'def_vs_k_rank': 20
        }

    def test_to_dict_partial_data(self):
        """Test to_dict() with some None fields."""
        team = TeamData(team='GB', offensive_rank=4)

        result = team.to_dict()

        assert result['team'] == 'GB'
        assert result['offensive_rank'] == 4
        assert result['defensive_rank'] is None


class TestSafeIntConversion:
    """Test suite for _safe_int_conversion() helper."""

    def test_safe_int_conversion_valid_int(self):
        """Test converts valid integer."""
        assert _safe_int_conversion(5) == 5
        assert _safe_int_conversion(0) == 0
        assert _safe_int_conversion(-10) == -10

    def test_safe_int_conversion_valid_string(self):
        """Test converts valid string to int."""
        assert _safe_int_conversion('15') == 15
        assert _safe_int_conversion('0') == 0

    def test_safe_int_conversion_float(self):
        """Test converts float to int."""
        assert _safe_int_conversion(12.7) == 12
        assert _safe_int_conversion(9.1) == 9

    def test_safe_int_conversion_float_string(self):
        """Test converts string representation of float."""
        assert _safe_int_conversion('12.7') == 12
        assert _safe_int_conversion('9.1') == 9

    def test_safe_int_conversion_none(self):
        """Test returns default for None."""
        assert _safe_int_conversion(None) is None
        assert _safe_int_conversion(None, default=0) == 0

    def test_safe_int_conversion_empty_string(self):
        """Test returns default for empty string."""
        assert _safe_int_conversion('') is None
        assert _safe_int_conversion('', default=-1) == -1

    def test_safe_int_conversion_nan_string(self):
        """Test returns default for 'nan' string."""
        assert _safe_int_conversion('nan') is None
        assert _safe_int_conversion('NaN', default=0) == 0
        assert _safe_int_conversion('none') is None
        assert _safe_int_conversion('null') is None

    def test_safe_int_conversion_infinity(self):
        """Test returns default for infinity values."""
        assert _safe_int_conversion(float('inf')) is None
        assert _safe_int_conversion(float('-inf')) is None

    def test_safe_int_conversion_actual_nan(self):
        """Test returns default for actual NaN."""
        assert _safe_int_conversion(float('nan')) is None

    def test_safe_int_conversion_invalid_string(self):
        """Test returns default for non-numeric string."""
        assert _safe_int_conversion('abc') is None
        # Note: '12abc' extracts the '12' digits, so it returns 12 not default
        assert _safe_int_conversion('12abc', default=0) == 12

    def test_safe_int_conversion_string_with_extras(self):
        """Test handles string with non-numeric characters."""
        assert _safe_int_conversion('$15') == 15
        assert _safe_int_conversion('rank: 10') == 10


class TestSafeStringConversion:
    """Test suite for _safe_string_conversion() helper."""

    def test_safe_string_conversion_valid_string(self):
        """Test returns valid string unchanged."""
        assert _safe_string_conversion('KC') == 'KC'
        assert _safe_string_conversion('BUF') == 'BUF'

    def test_safe_string_conversion_none(self):
        """Test returns None for None."""
        assert _safe_string_conversion(None) is None

    def test_safe_string_conversion_nan_string(self):
        """Test returns None for 'nan' strings."""
        assert _safe_string_conversion('nan') is None
        assert _safe_string_conversion('NaN') is None
        assert _safe_string_conversion('none') is None
        assert _safe_string_conversion('null') is None

    def test_safe_string_conversion_empty_string(self):
        """Test returns None for empty string."""
        assert _safe_string_conversion('') is None
        assert _safe_string_conversion('   ') is None

    def test_safe_string_conversion_pandas_nan(self):
        """Test handles pandas NaN values."""
        assert _safe_string_conversion(pd.NA) is None
        assert _safe_string_conversion(float('nan')) is None

    def test_safe_string_conversion_numeric(self):
        """Test converts numeric values to string."""
        assert _safe_string_conversion(123) == '123'
        assert _safe_string_conversion(12.5) == '12.5'

    def test_safe_string_conversion_strips_whitespace(self):
        """Test strips leading/trailing whitespace."""
        assert _safe_string_conversion('  PHI  ') == 'PHI'


@pytest.mark.skip(reason="Function load_teams_from_csv removed in team_data refactor")
class TestLoadTeamsFromCsv:
    """Test suite for load_teams_from_csv() function."""

    def test_load_teams_from_csv_valid_file(self, tmp_path):
        """Test loads teams from valid CSV file."""
        csv_file = tmp_path / "teams.csv"
        csv_file.write_text(
            "team,offensive_rank,defensive_rank\n"
            "KC,5,12\n"
            "BUF,3,8\n"
        )

        teams = load_teams_from_csv(str(csv_file))

        assert len(teams) == 2
        assert teams[0].team == 'KC'
        assert teams[0].offensive_rank == 5
        assert teams[1].team == 'BUF'
        assert teams[1].offensive_rank == 3

    def test_load_teams_from_csv_with_none_values(self, tmp_path):
        """Test loads teams with missing/NaN values."""
        csv_file = tmp_path / "teams.csv"
        csv_file.write_text(
            "team,offensive_rank,defensive_rank\n"
            "PHI,10,\n"
            "NE,,15\n"
        )

        teams = load_teams_from_csv(str(csv_file))

        assert len(teams) == 2
        assert teams[0].offensive_rank == 10
        assert teams[0].defensive_rank is None
        assert teams[1].offensive_rank is None
        assert teams[1].defensive_rank == 15

    def test_load_teams_from_csv_missing_file(self, tmp_path):
        """Test raises FileNotFoundError for missing file."""
        missing_file = tmp_path / "nonexistent.csv"

        with pytest.raises(FileNotFoundError, match="teams.csv file not found"):
            load_teams_from_csv(str(missing_file))

    def test_load_teams_from_csv_empty_file(self, tmp_path):
        """Test handles empty CSV file."""
        csv_file = tmp_path / "teams.csv"
        csv_file.write_text("team,offensive_rank,defensive_rank\n")

        teams = load_teams_from_csv(str(csv_file))

        assert len(teams) == 0


@pytest.mark.skip(reason="Function save_teams_to_csv removed in team_data refactor")
class TestSaveTeamsToCsv:
    """Test suite for save_teams_to_csv() function."""

    def test_save_teams_to_csv_valid_data(self, tmp_path):
        """Test saves teams to CSV file."""
        csv_file = tmp_path / "output.csv"
        teams = [
            TeamData(team='KC', offensive_rank=5, defensive_rank=12),
            TeamData(team='BUF', offensive_rank=3, defensive_rank=8)
        ]

        save_teams_to_csv(teams, str(csv_file))

        assert csv_file.exists()
        df = pd.read_csv(csv_file)
        assert len(df) == 2
        assert list(df.columns) == ['team', 'offensive_rank', 'defensive_rank',
                                     'def_vs_qb_rank', 'def_vs_rb_rank', 'def_vs_wr_rank',
                                     'def_vs_te_rank', 'def_vs_k_rank']
        assert df.iloc[0]['team'] == 'KC'

    def test_save_teams_to_csv_empty_list(self, tmp_path):
        """Test saves empty CSV with headers."""
        csv_file = tmp_path / "empty.csv"
        teams = []

        save_teams_to_csv(teams, str(csv_file))

        assert csv_file.exists()
        df = pd.read_csv(csv_file)
        assert len(df) == 0
        assert list(df.columns) == ['team', 'offensive_rank', 'defensive_rank',
                                     'def_vs_qb_rank', 'def_vs_rb_rank', 'def_vs_wr_rank',
                                     'def_vs_te_rank', 'def_vs_k_rank']

    def test_save_teams_to_csv_with_none_values(self, tmp_path):
        """Test saves teams with None values."""
        csv_file = tmp_path / "with_nones.csv"
        teams = [
            TeamData(team='PHI', offensive_rank=10),
            TeamData(team='NE', defensive_rank=15)
        ]

        save_teams_to_csv(teams, str(csv_file))

        df = pd.read_csv(csv_file)
        assert len(df) == 2
        # pandas reads None as NaN
        assert pd.isna(df.iloc[0]['defensive_rank'])
        assert pd.isna(df.iloc[1]['offensive_rank'])


@pytest.mark.skip(reason="Function extract_teams_from_players removed in team_data refactor")
class TestExtractTeamsFromPlayers:
    """Test suite for extract_teams_from_players() function."""

    @pytest.fixture
    def sample_players(self):
        """Create sample FantasyPlayer objects."""
        return [
            FantasyPlayer(id=1, name="Patrick Mahomes", position="QB", team="KC"),
            FantasyPlayer(id=2, name="Josh Allen", position="QB", team="BUF"),
            FantasyPlayer(id=3, name="Travis Kelce", position="TE", team="KC"),
            FantasyPlayer(id=4, name="Stefon Diggs", position="WR", team="BUF"),
            FantasyPlayer(id=5, name="Jalen Hurts", position="QB", team="PHI")
        ]

    def test_extract_teams_from_players_unique_teams(self, sample_players):
        """Test extracts unique teams from players."""
        teams = extract_teams_from_players(sample_players)

        assert len(teams) == 3
        team_names = [t.team for t in teams]
        assert 'BUF' in team_names
        assert 'KC' in team_names
        assert 'PHI' in team_names

    def test_extract_teams_from_players_sorted(self, sample_players):
        """Test returns teams sorted by team name."""
        teams = extract_teams_from_players(sample_players)

        team_names = [t.team for t in teams]
        assert team_names == sorted(team_names)

    def test_extract_teams_from_players_no_rankings(self, sample_players):
        """Test extracted teams have no ranking data (deprecated)."""
        teams = extract_teams_from_players(sample_players)

        for team in teams:
            assert team.offensive_rank is None
            assert team.defensive_rank is None

    def test_extract_teams_from_players_skips_empty_teams(self):
        """Test skips players with empty team field."""
        players = [
            FantasyPlayer(id=1, name="Player 1", position="QB", team="KC"),
            FantasyPlayer(id=2, name="Player 2", position="WR", team=""),
            FantasyPlayer(id=3, name="Player 3", position="RB", team=None)
        ]

        teams = extract_teams_from_players(players)

        assert len(teams) == 1
        assert teams[0].team == 'KC'

    def test_extract_teams_from_players_empty_list(self):
        """Test handles empty player list."""
        teams = extract_teams_from_players([])

        assert len(teams) == 0


@pytest.mark.skip(reason="Function extract_teams_from_rankings removed in team_data refactor")
class TestExtractTeamsFromRankings:
    """Test suite for extract_teams_from_rankings() function."""

    @pytest.fixture
    def sample_players(self):
        """Create sample FantasyPlayer objects."""
        return [
            FantasyPlayer(id=1, name="Patrick Mahomes", position="QB", team="KC"),
            FantasyPlayer(id=2, name="Josh Allen", position="QB", team="BUF"),
            FantasyPlayer(id=3, name="Travis Kelce", position="TE", team="KC")
        ]

    @pytest.fixture
    def team_rankings(self):
        """Create sample team rankings."""
        return {
            'KC': {'offensive_rank': 5, 'defensive_rank': 12},
            'BUF': {'offensive_rank': 3, 'defensive_rank': 8},
            'PHI': {'offensive_rank': 2, 'defensive_rank': 10}
        }

    def test_extract_teams_from_rankings_basic(self, sample_players, team_rankings):
        """Test extracts teams with rankings."""
        teams = extract_teams_from_rankings(sample_players, team_rankings)

        assert len(teams) == 2
        kc_team = next(t for t in teams if t.team == 'KC')
        assert kc_team.offensive_rank == 5
        assert kc_team.defensive_rank == 12

    def test_extract_teams_from_rankings_with_schedule(self, sample_players, team_rankings):
        """Test extracts teams with opponent schedule."""
        schedule = {'KC': 'DEN', 'BUF': 'MIA'}

        teams = extract_teams_from_rankings(sample_players, team_rankings, schedule)

        # Schedule parameter is deprecated but function should still work
        assert len(teams) == 2

    def test_extract_teams_from_rankings_missing_team_ranking(self, sample_players):
        """Test handles teams not in rankings."""
        rankings = {'PHI': {'offensive_rank': 2, 'defensive_rank': 10}}

        teams = extract_teams_from_rankings(sample_players, rankings)

        kc_team = next(t for t in teams if t.team == 'KC')
        assert kc_team.offensive_rank is None
        assert kc_team.defensive_rank is None

    def test_extract_teams_from_rankings_sorted(self, sample_players, team_rankings):
        """Test returns teams sorted by name."""
        teams = extract_teams_from_rankings(sample_players, team_rankings)

        team_names = [t.team for t in teams]
        assert team_names == sorted(team_names)

    def test_extract_teams_from_rankings_no_schedule(self, sample_players, team_rankings):
        """Test works without schedule data."""
        teams = extract_teams_from_rankings(sample_players, team_rankings)

        # Should work without schedule parameter
        assert len(teams) == 2

    def test_extract_teams_from_rankings_skips_duplicates(self):
        """Test processes each team only once."""
        players = [
            FantasyPlayer(id=1, name="Player 1", position="QB", team="KC"),
            FantasyPlayer(id=2, name="Player 2", position="WR", team="KC"),
            FantasyPlayer(id=3, name="Player 3", position="RB", team="KC")
        ]
        rankings = {'KC': {'offensive_rank': 5, 'defensive_rank': 12}}

        teams = extract_teams_from_rankings(players, rankings)

        assert len(teams) == 1
        assert teams[0].team == 'KC'
