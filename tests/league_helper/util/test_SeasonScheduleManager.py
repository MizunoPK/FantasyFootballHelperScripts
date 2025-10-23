#!/usr/bin/env python3
"""
Tests for Season Schedule Manager

Tests for SeasonScheduleManager class including schedule loading,
opponent lookup, future schedule queries, and error handling.

Author: Kai Mizuno
"""

import pytest
import csv
from pathlib import Path
import sys

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from league_helper.util.SeasonScheduleManager import SeasonScheduleManager


@pytest.fixture
def temp_schedule_csv(tmp_path):
    """Create a temporary season_schedule.csv file for testing"""
    data_folder = tmp_path / "data"
    data_folder.mkdir()

    schedule_file = data_folder / "season_schedule.csv"

    # Create sample schedule data
    # KC: plays BAL (week 1), DEN (week 2), bye (week 5), LAC (week 6)
    # PHI: plays DAL (week 1), bye (week 3), NYG (week 4)
    schedule_data = [
        ['week', 'team', 'opponent'],
        ['1', 'KC', 'BAL'],
        ['1', 'BAL', 'KC'],
        ['1', 'PHI', 'DAL'],
        ['1', 'DAL', 'PHI'],
        ['2', 'KC', 'DEN'],
        ['2', 'DEN', 'KC'],
        ['2', 'PHI', 'NYG'],
        ['2', 'NYG', 'PHI'],
        ['3', 'KC', 'LAC'],
        ['3', 'LAC', 'KC'],
        ['3', 'PHI', ''],  # PHI bye week
        ['4', 'KC', 'LV'],
        ['4', 'LV', 'KC'],
        ['4', 'PHI', 'SF'],
        ['4', 'SF', 'PHI'],
        ['5', 'KC', ''],  # KC bye week
        ['5', 'PHI', 'ARI'],
        ['5', 'ARI', 'PHI'],
        ['6', 'KC', 'BUF'],
        ['6', 'BUF', 'KC'],
        ['6', 'PHI', 'CLE'],
        ['6', 'CLE', 'PHI'],
    ]

    with open(schedule_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(schedule_data)

    return data_folder


class TestSeasonScheduleManagerInit:
    """Test SeasonScheduleManager initialization"""

    def test_initialization_with_valid_file(self, temp_schedule_csv):
        """Test initialization with valid season_schedule.csv"""
        manager = SeasonScheduleManager(temp_schedule_csv)

        assert manager.schedule_file == temp_schedule_csv / 'season_schedule.csv'
        assert len(manager.schedule_cache) > 0
        assert manager.is_schedule_available()

    def test_initialization_with_missing_file(self, tmp_path):
        """Test initialization when season_schedule.csv doesn't exist"""
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        manager = SeasonScheduleManager(data_folder)

        assert len(manager.schedule_cache) == 0
        assert not manager.is_schedule_available()

    def test_initialization_stores_logger(self, temp_schedule_csv):
        """Test initialization creates logger"""
        manager = SeasonScheduleManager(temp_schedule_csv)

        assert manager.logger is not None


class TestLoadSchedule:
    """Test _load_schedule method"""

    def test_load_schedule_populates_cache(self, temp_schedule_csv):
        """Test _load_schedule populates schedule cache correctly"""
        manager = SeasonScheduleManager(temp_schedule_csv)

        # Check specific entries
        assert manager.schedule_cache[('KC', 1)] == 'BAL'
        assert manager.schedule_cache[('BAL', 1)] == 'KC'
        assert manager.schedule_cache[('PHI', 1)] == 'DAL'

    def test_load_schedule_handles_bye_weeks(self, temp_schedule_csv):
        """Test _load_schedule converts empty strings to None for bye weeks"""
        manager = SeasonScheduleManager(temp_schedule_csv)

        # KC has bye in week 5
        assert manager.schedule_cache[('KC', 5)] is None

        # PHI has bye in week 3
        assert manager.schedule_cache[('PHI', 3)] is None


class TestGetOpponent:
    """Test get_opponent method"""

    def test_get_opponent_valid_matchup(self, temp_schedule_csv):
        """Test get_opponent returns correct opponent"""
        manager = SeasonScheduleManager(temp_schedule_csv)

        assert manager.get_opponent('KC', 1) == 'BAL'
        assert manager.get_opponent('BAL', 1) == 'KC'
        assert manager.get_opponent('PHI', 1) == 'DAL'
        assert manager.get_opponent('KC', 2) == 'DEN'

    def test_get_opponent_bye_week(self, temp_schedule_csv):
        """Test get_opponent returns None for bye weeks"""
        manager = SeasonScheduleManager(temp_schedule_csv)

        # KC has bye in week 5
        assert manager.get_opponent('KC', 5) is None

        # PHI has bye in week 3
        assert manager.get_opponent('PHI', 3) is None

    def test_get_opponent_invalid_week_too_low(self, temp_schedule_csv):
        """Test get_opponent returns None for week < 1"""
        manager = SeasonScheduleManager(temp_schedule_csv)

        assert manager.get_opponent('KC', 0) is None
        assert manager.get_opponent('KC', -1) is None

    def test_get_opponent_invalid_week_too_high(self, temp_schedule_csv):
        """Test get_opponent returns None for week > 17"""
        manager = SeasonScheduleManager(temp_schedule_csv)

        assert manager.get_opponent('KC', 18) is None
        assert manager.get_opponent('KC', 20) is None

    def test_get_opponent_nonexistent_team(self, temp_schedule_csv):
        """Test get_opponent returns None for unknown team"""
        manager = SeasonScheduleManager(temp_schedule_csv)

        assert manager.get_opponent('FAKE', 1) is None


class TestGetFutureOpponents:
    """Test get_future_opponents method"""

    def test_get_future_opponents_excludes_bye_weeks(self, temp_schedule_csv):
        """Test get_future_opponents excludes bye weeks from result"""
        manager = SeasonScheduleManager(temp_schedule_csv)

        # KC future opponents from week 1 (weeks 2-6, excluding week 5 bye)
        future = manager.get_future_opponents('KC', 1)

        assert 'DEN' in future  # Week 2
        assert 'LAC' in future  # Week 3
        assert 'LV' in future   # Week 4
        # Week 5 is bye, should not be in list
        assert 'BUF' in future  # Week 6
        assert len(future) == 4  # 4 games (week 5 bye excluded)

    def test_get_future_opponents_from_current_week(self, temp_schedule_csv):
        """Test get_future_opponents starts from current_week + 1"""
        manager = SeasonScheduleManager(temp_schedule_csv)

        # PHI future opponents from week 2 (weeks 3-6)
        future = manager.get_future_opponents('PHI', 2)

        # Week 3 is bye, should be excluded
        assert 'SF' in future   # Week 4
        assert 'ARI' in future  # Week 5
        assert 'CLE' in future  # Week 6
        assert len(future) == 3

    def test_get_future_opponents_no_future_games(self, temp_schedule_csv):
        """Test get_future_opponents returns empty list at end of season"""
        manager = SeasonScheduleManager(temp_schedule_csv)

        # No future opponents after week 17
        future = manager.get_future_opponents('KC', 17)

        assert future == []

    def test_get_future_opponents_empty_schedule(self, tmp_path):
        """Test get_future_opponents with empty schedule"""
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        manager = SeasonScheduleManager(data_folder)
        future = manager.get_future_opponents('KC', 1)

        assert future == []


class TestGetRemainingSchedule:
    """Test get_remaining_schedule method"""

    def test_get_remaining_schedule_includes_bye_weeks(self, temp_schedule_csv):
        """Test get_remaining_schedule includes bye weeks as None"""
        manager = SeasonScheduleManager(temp_schedule_csv)

        # KC remaining schedule from week 1
        remaining = manager.get_remaining_schedule('KC', 1)

        assert remaining[2] == 'DEN'
        assert remaining[3] == 'LAC'
        assert remaining[4] == 'LV'
        assert remaining[5] is None  # Bye week
        assert remaining[6] == 'BUF'

    def test_get_remaining_schedule_returns_dict(self, temp_schedule_csv):
        """Test get_remaining_schedule returns dict with week keys"""
        manager = SeasonScheduleManager(temp_schedule_csv)

        remaining = manager.get_remaining_schedule('PHI', 2)

        assert isinstance(remaining, dict)
        assert 3 in remaining
        assert 4 in remaining
        assert 5 in remaining
        assert 6 in remaining

    def test_get_remaining_schedule_no_future_weeks(self, temp_schedule_csv):
        """Test get_remaining_schedule returns empty dict at end of season"""
        manager = SeasonScheduleManager(temp_schedule_csv)

        remaining = manager.get_remaining_schedule('KC', 17)

        assert remaining == {}

    def test_get_remaining_schedule_empty_schedule(self, tmp_path):
        """Test get_remaining_schedule with empty schedule"""
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        manager = SeasonScheduleManager(data_folder)
        remaining = manager.get_remaining_schedule('KC', 1)

        # Should return dict with None values for all weeks
        assert isinstance(remaining, dict)
        for week in range(2, 18):
            assert remaining[week] is None


class TestIsScheduleAvailable:
    """Test is_schedule_available method"""

    def test_is_schedule_available_with_data(self, temp_schedule_csv):
        """Test is_schedule_available returns True when schedule loaded"""
        manager = SeasonScheduleManager(temp_schedule_csv)

        assert manager.is_schedule_available() is True

    def test_is_schedule_available_without_data(self, tmp_path):
        """Test is_schedule_available returns False when no schedule"""
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        manager = SeasonScheduleManager(data_folder)

        assert manager.is_schedule_available() is False


class TestErrorHandling:
    """Test error handling and edge cases"""

    def test_handles_missing_csv_file_gracefully(self, tmp_path):
        """Test initialization doesn't crash when CSV missing"""
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        # Should not raise exception
        manager = SeasonScheduleManager(data_folder)

        assert manager.schedule_cache == {}
        assert not manager.is_schedule_available()

    def test_handles_invalid_csv_format_gracefully(self, tmp_path):
        """Test initialization handles corrupt CSV gracefully"""
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        schedule_file = data_folder / "season_schedule.csv"

        # Create invalid CSV (missing required columns)
        with open(schedule_file, 'w') as f:
            f.write("invalid,csv,headers\n")
            f.write("1,2,3\n")

        # Should not crash, but schedule should be empty
        manager = SeasonScheduleManager(data_folder)

        assert not manager.is_schedule_available()


class TestModuleImports:
    """Test that SeasonScheduleManager can be imported"""

    def test_import_season_schedule_manager(self):
        """Test SeasonScheduleManager can be imported"""
        from league_helper.util.SeasonScheduleManager import SeasonScheduleManager

        assert SeasonScheduleManager is not None
