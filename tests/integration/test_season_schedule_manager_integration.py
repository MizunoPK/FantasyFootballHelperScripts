"""
Integration tests for SeasonScheduleManager week-18 schedule behavior.
"""
import csv
import pytest
from league_helper.util.SeasonScheduleManager import SeasonScheduleManager


class TestWeek18ScheduleIntegration:
    """Integration tests validating week 18 is included in schedule lookups."""

    @pytest.fixture
    def week18_schedule_csv(self, tmp_path):
        data_folder = tmp_path / "data"
        data_folder.mkdir()
        schedule_file = data_folder / "season_schedule.csv"
        with open(schedule_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows([
                ['week', 'team', 'opponent'],
                ['17', 'KC', 'DEN'],
                ['17', 'DEN', 'KC'],
                ['18', 'KC', 'LV'],
                ['18', 'LV', 'KC'],
            ])
        return data_folder

    def test_get_opponent_week18_returns_opponent(self, week18_schedule_csv):
        """get_opponent(team, 18) returns a valid opponent when week-18 data exists."""
        manager = SeasonScheduleManager(week18_schedule_csv)
        assert manager.get_opponent('KC', 18) == 'LV'

    def test_get_opponent_week19_returns_none(self, week18_schedule_csv):
        """get_opponent(team, 19) returns None — week 19 is still invalid."""
        manager = SeasonScheduleManager(week18_schedule_csv)
        assert manager.get_opponent('KC', 19) is None

    def test_get_future_opponents_includes_week18(self, week18_schedule_csv):
        """get_future_opponents(team, 17) includes the week-18 opponent."""
        manager = SeasonScheduleManager(week18_schedule_csv)
        future = manager.get_future_opponents('KC', 17)
        assert 'LV' in future

    def test_get_remaining_schedule_includes_week18(self, week18_schedule_csv):
        """get_remaining_schedule(team, 17) includes key 18 with valid opponent."""
        manager = SeasonScheduleManager(week18_schedule_csv)
        remaining = manager.get_remaining_schedule('KC', 17)
        assert 18 in remaining
        assert remaining[18] == 'LV'
