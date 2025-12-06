#!/usr/bin/env python3
"""
Tests for historical_data_compiler/team_data_calculator.py

Tests team data calculation from player stats and schedule.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from historical_data_compiler.team_data_calculator import (
    TeamDataCalculator,
    TEAM_DATA_CSV_COLUMNS,
    calculate_and_write_team_data,
)
from historical_data_compiler.player_data_fetcher import PlayerData
from historical_data_compiler.game_data_fetcher import GameData


@pytest.fixture
def sample_players():
    """Create sample player data for testing"""
    return [
        PlayerData(
            id="1",
            name="QB Player",
            team="KC",
            position="QB",
            bye_week=6,
            week_points={1: 25.0, 2: 20.0, 3: 15.0},
            projected_weeks={1: 22.0, 2: 21.0, 3: 19.0}
        ),
        PlayerData(
            id="2",
            name="RB Player",
            team="KC",
            position="RB",
            bye_week=6,
            week_points={1: 15.0, 2: 12.0, 3: 18.0},
            projected_weeks={1: 14.0, 2: 14.0, 3: 14.0}
        ),
        PlayerData(
            id="3",
            name="Opponent QB",
            team="DEN",
            position="QB",
            bye_week=7,
            week_points={1: 18.0, 2: 22.0, 3: 16.0},
            projected_weeks={1: 17.0, 2: 18.0, 3: 17.0}
        ),
        PlayerData(
            id="4",
            name="Opponent RB",
            team="DEN",
            position="RB",
            bye_week=7,
            week_points={1: 12.0, 2: 8.0, 3: 20.0},
            projected_weeks={1: 11.0, 2: 11.0, 3: 11.0}
        ),
    ]


@pytest.fixture
def sample_schedule():
    """Create sample schedule for testing"""
    return {
        1: {'KC': 'DEN', 'DEN': 'KC'},
        2: {'KC': 'BAL', 'BAL': 'KC', 'DEN': 'LV', 'LV': 'DEN'},
        3: {'KC': 'DEN', 'DEN': 'KC'},
    }


@pytest.fixture
def sample_game_data():
    """Create sample game data for testing"""
    return [
        GameData(
            week=1,
            home_team="KC",
            away_team="DEN",
            temperature=75,
            gust=10,
            precipitation=0.0,
            home_team_score=27,
            away_team_score=20,
            indoor=False,
            neutral_site=False,
            country="USA",
            city="Kansas City",
            state="MO",
            date="2024-09-08T13:00Z"
        ),
        GameData(
            week=3,
            home_team="DEN",
            away_team="KC",
            temperature=65,
            gust=5,
            precipitation=0.1,
            home_team_score=17,
            away_team_score=24,
            indoor=False,
            neutral_site=False,
            country="USA",
            city="Denver",
            state="CO",
            date="2024-09-22T16:25Z"
        ),
    ]


class TestTeamDataCalculator:
    """Tests for TeamDataCalculator class"""

    def test_initialization(self):
        """Calculator should initialize properly"""
        calculator = TeamDataCalculator()
        assert calculator is not None
        assert hasattr(calculator, 'logger')

    def test_calculate_team_data(self, sample_players, sample_schedule, sample_game_data):
        """Should calculate team data correctly"""
        calculator = TeamDataCalculator()
        result = calculator.calculate_team_data(sample_players, sample_schedule, sample_game_data)

        # Should have data for all teams that have players
        assert 'KC' in result
        assert 'DEN' in result

        # KC week 1 should have DEN's players' points as "allowed"
        kc_week1 = result['KC'][0]
        assert kc_week1['week'] == 1
        # DEN's QB scored 18.0 in week 1
        assert kc_week1['pts_allowed_to_QB'] == 18.0
        # DEN's RB scored 12.0 in week 1
        assert kc_week1['pts_allowed_to_RB'] == 12.0

    def test_bye_week_handling(self, sample_players, sample_schedule, sample_game_data):
        """Bye week should have all zeros"""
        calculator = TeamDataCalculator()
        # Add a bye week for KC
        schedule_with_bye = {
            1: {'DEN': 'LV', 'LV': 'DEN'},  # KC not playing
            2: {'KC': 'DEN', 'DEN': 'KC'},
        }
        result = calculator.calculate_team_data(sample_players, schedule_with_bye, sample_game_data)

        kc_week1 = result['KC'][0]
        assert kc_week1['pts_allowed_to_QB'] == 0.0
        assert kc_week1['pts_allowed_to_RB'] == 0.0
        assert kc_week1['points_scored'] == 0.0
        assert kc_week1['points_allowed'] == 0.0


class TestTeamDataCSVColumns:
    """Tests for CSV column definitions"""

    def test_required_columns_present(self):
        """All required columns should be present"""
        required = [
            "week",
            "pts_allowed_to_QB",
            "pts_allowed_to_RB",
            "pts_allowed_to_WR",
            "pts_allowed_to_TE",
            "pts_allowed_to_K",
            "points_scored",
            "points_allowed"
        ]
        for col in required:
            assert col in TEAM_DATA_CSV_COLUMNS

    def test_column_count(self):
        """Should have 8 columns"""
        assert len(TEAM_DATA_CSV_COLUMNS) == 8


class TestWriteTeamDataFiles:
    """Tests for writing team data CSV files"""

    def test_write_team_data_files(self, tmp_path, sample_players, sample_schedule, sample_game_data):
        """Should write team data files correctly"""
        calculator = TeamDataCalculator()
        team_data = calculator.calculate_team_data(sample_players, sample_schedule, sample_game_data)
        calculator.write_team_data_files(team_data, tmp_path)

        # Check that team_data folder was created
        team_data_dir = tmp_path / "team_data"
        assert team_data_dir.exists()

        # Check that team files were created
        kc_file = team_data_dir / "KC.csv"
        assert kc_file.exists()


class TestCalculateAndWriteTeamData:
    """Tests for convenience function"""

    def test_convenience_function(self, tmp_path, sample_players, sample_schedule, sample_game_data):
        """Convenience function should work correctly"""
        result = calculate_and_write_team_data(
            sample_players,
            sample_schedule,
            sample_game_data,
            tmp_path
        )

        # Should return team data dict
        assert isinstance(result, dict)
        assert 'KC' in result

        # Should write files
        assert (tmp_path / "team_data" / "KC.csv").exists()
