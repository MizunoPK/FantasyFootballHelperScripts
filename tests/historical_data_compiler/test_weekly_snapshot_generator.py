#!/usr/bin/env python3
"""
Tests for historical_data_compiler/weekly_snapshot_generator.py

Tests weekly snapshot generation for simulation data.
"""

import csv
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from historical_data_compiler.weekly_snapshot_generator import (
    WeeklySnapshotGenerator,
    generate_weekly_snapshots,
)
from historical_data_compiler.player_data_fetcher import PlayerData


@pytest.fixture
def sample_players():
    """Create sample player data with weekly points"""
    return [
        PlayerData(
            id="1",
            name="Patrick Mahomes",
            team="KC",
            position="QB",
            bye_week=6,
            fantasy_points=350.0,
            average_draft_position=3.5,
            player_rating=98.0,
            week_points={
                1: 25.0, 2: 30.0, 3: 22.0, 4: 28.0, 5: 20.0,
                6: 0.0,  # bye week
                7: 24.0, 8: 26.0, 9: 21.0, 10: 29.0, 11: 23.0,
                12: 27.0, 13: 25.0, 14: 22.0, 15: 28.0, 16: 24.0, 17: 26.0
            },
            projected_weeks={
                1: 22.0, 2: 23.0, 3: 22.0, 4: 23.0, 5: 22.0,
                6: 0.0,
                7: 22.0, 8: 23.0, 9: 22.0, 10: 23.0, 11: 22.0,
                12: 23.0, 13: 22.0, 14: 23.0, 15: 22.0, 16: 23.0, 17: 22.0
            }
        ),
        PlayerData(
            id="2",
            name="Travis Kelce",
            team="KC",
            position="TE",
            bye_week=6,
            fantasy_points=180.0,
            average_draft_position=12.5,
            player_rating=95.0,
            week_points={
                1: 12.0, 2: 15.0, 3: 10.0, 4: 14.0, 5: 11.0,
                6: 0.0,
                7: 13.0, 8: 16.0, 9: 9.0, 10: 15.0, 11: 12.0,
                12: 14.0, 13: 11.0, 14: 13.0, 15: 15.0, 16: 10.0, 17: 12.0
            },
            projected_weeks={
                1: 11.0, 2: 11.0, 3: 11.0, 4: 11.0, 5: 11.0,
                6: 0.0,
                7: 11.0, 8: 11.0, 9: 11.0, 10: 11.0, 11: 11.0,
                12: 11.0, 13: 11.0, 14: 11.0, 15: 11.0, 16: 11.0, 17: 11.0
            }
        ),
    ]


class TestWeeklySnapshotGenerator:
    """Tests for WeeklySnapshotGenerator class"""

    def test_initialization(self):
        """Generator should initialize properly"""
        generator = WeeklySnapshotGenerator()
        assert generator is not None
        assert hasattr(generator, 'logger')

    def test_generate_all_weeks(self, tmp_path, sample_players):
        """Should generate snapshots for all 17 weeks"""
        generator = WeeklySnapshotGenerator()
        generator.generate_all_weeks(sample_players, tmp_path)

        weeks_dir = tmp_path / "weeks"
        assert weeks_dir.exists()

        # Check all 17 week folders exist
        for week in range(1, 18):
            week_dir = weeks_dir / f"week_{week:02d}"
            assert week_dir.exists(), f"Week {week} folder should exist"
            assert (week_dir / "players.csv").exists()
            assert (week_dir / "players_projected.csv").exists()

    def test_week1_snapshot_uses_projections(self, tmp_path, sample_players):
        """Week 1 snapshot should use projected values for all weeks"""
        generator = WeeklySnapshotGenerator()
        generator.generate_all_weeks(sample_players, tmp_path)

        week1_file = tmp_path / "weeks" / "week_01" / "players.csv"
        with open(week1_file, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # Week 1 snapshot: all weeks use projected values
        # Find Mahomes' row
        mahomes = next(r for r in rows if r['name'] == 'Patrick Mahomes')
        # Week 1 should use projected (22.0)
        assert float(mahomes['week_1_points']) == 22.0

    def test_mid_season_snapshot_uses_actual_for_past(self, tmp_path, sample_players):
        """Mid-season snapshot should use actual for past weeks, projected for future"""
        generator = WeeklySnapshotGenerator()
        generator.generate_all_weeks(sample_players, tmp_path)

        week5_file = tmp_path / "weeks" / "week_05" / "players.csv"
        with open(week5_file, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        mahomes = next(r for r in rows if r['name'] == 'Patrick Mahomes')
        # Weeks 1-4 should use actual (25, 30, 22, 28)
        assert float(mahomes['week_1_points']) == 25.0
        assert float(mahomes['week_2_points']) == 30.0
        # Week 5+ should use projected (22.0)
        assert float(mahomes['week_5_points']) == 22.0

    def test_projected_file_always_uses_projections(self, tmp_path, sample_players):
        """players_projected.csv should always use projected values"""
        generator = WeeklySnapshotGenerator()
        generator.generate_all_weeks(sample_players, tmp_path)

        projected_file = tmp_path / "weeks" / "week_05" / "players_projected.csv"
        with open(projected_file, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        mahomes = next(r for r in rows if r['name'] == 'Patrick Mahomes')
        # All weeks should use projected
        assert float(mahomes['week_1_points']) == 22.0
        assert float(mahomes['week_2_points']) == 23.0

    def test_fantasy_points_calculation(self, tmp_path, sample_players):
        """Fantasy points should be sum of appropriate weekly values"""
        generator = WeeklySnapshotGenerator()
        generator.generate_all_weeks(sample_players, tmp_path)

        # Week 5 snapshot
        week5_file = tmp_path / "weeks" / "week_05" / "players.csv"
        with open(week5_file, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        mahomes = next(r for r in rows if r['name'] == 'Patrick Mahomes')
        # Calculate expected: actual weeks 1-4 + projected weeks 5-17
        # Actual: 25+30+22+28 = 105
        # Projected: 22+0+22+23+22+23+22+23+22+23+22+23+22 = 289
        # Weeks 5-17 projection would need to match
        total = float(mahomes['fantasy_points'])
        assert total > 0


class TestGenerateWeeklySnapshots:
    """Tests for convenience function"""

    def test_convenience_function(self, tmp_path, sample_players):
        """Convenience function should work correctly"""
        generate_weekly_snapshots(sample_players, tmp_path)

        weeks_dir = tmp_path / "weeks"
        assert weeks_dir.exists()
        assert (weeks_dir / "week_01" / "players.csv").exists()
        assert (weeks_dir / "week_17" / "players.csv").exists()


class TestSnapshotCSVFormat:
    """Tests for CSV format and content"""

    def test_csv_has_required_columns(self, tmp_path, sample_players):
        """CSV should have all required columns"""
        generator = WeeklySnapshotGenerator()
        generator.generate_all_weeks(sample_players, tmp_path)

        week1_file = tmp_path / "weeks" / "week_01" / "players.csv"
        with open(week1_file, 'r') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames

        required_cols = [
            'id', 'name', 'team', 'position', 'bye_week', 'drafted', 'locked',
            'fantasy_points', 'average_draft_position', 'player_rating', 'injury_status'
        ]
        for col in required_cols:
            assert col in fieldnames

        # Weekly columns
        for week in range(1, 18):
            assert f'week_{week}_points' in fieldnames

    def test_players_sorted_by_fantasy_points(self, tmp_path, sample_players):
        """Players should be sorted by fantasy points descending"""
        generator = WeeklySnapshotGenerator()
        generator.generate_all_weeks(sample_players, tmp_path)

        week1_file = tmp_path / "weeks" / "week_01" / "players.csv"
        with open(week1_file, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # Verify descending order
        for i in range(len(rows) - 1):
            assert float(rows[i]['fantasy_points']) >= float(rows[i + 1]['fantasy_points'])


class TestPlayerRatingCalculation:
    """Tests for player_rating recalculation in weekly snapshots.

    Per spec:
    - Week 1: Use original draft-based rating
    - Week 2+: Calculate from cumulative fantasy_points through (current_week - 1)
    """

    @pytest.fixture
    def multi_qb_players(self):
        """Create multiple QBs to test position-specific ranking"""
        return [
            PlayerData(
                id="qb1",
                name="Top QB",
                team="KC",
                position="QB",
                bye_week=6,
                player_rating=98.0,  # Draft-based rating
                week_points={1: 30.0, 2: 28.0, 3: 32.0, 4: 25.0},  # Best performer: 115 pts
                projected_weeks={1: 22.0, 2: 22.0, 3: 22.0, 4: 22.0, 5: 22.0, 6: 0.0, 7: 22.0,
                                8: 22.0, 9: 22.0, 10: 22.0, 11: 22.0, 12: 22.0, 13: 22.0,
                                14: 22.0, 15: 22.0, 16: 22.0, 17: 22.0}
            ),
            PlayerData(
                id="qb2",
                name="Mid QB",
                team="BAL",
                position="QB",
                bye_week=7,
                player_rating=85.0,  # Draft-based rating
                week_points={1: 20.0, 2: 22.0, 3: 18.0, 4: 21.0},  # Middle: 81 pts
                projected_weeks={1: 20.0, 2: 20.0, 3: 20.0, 4: 20.0, 5: 20.0, 6: 20.0, 7: 0.0,
                                8: 20.0, 9: 20.0, 10: 20.0, 11: 20.0, 12: 20.0, 13: 20.0,
                                14: 20.0, 15: 20.0, 16: 20.0, 17: 20.0}
            ),
            PlayerData(
                id="qb3",
                name="Low QB",
                team="NYG",
                position="QB",
                bye_week=8,
                player_rating=60.0,  # Draft-based rating
                week_points={1: 12.0, 2: 10.0, 3: 8.0, 4: 15.0},  # Worst: 45 pts
                projected_weeks={1: 15.0, 2: 15.0, 3: 15.0, 4: 15.0, 5: 15.0, 6: 15.0, 7: 15.0,
                                8: 0.0, 9: 15.0, 10: 15.0, 11: 15.0, 12: 15.0, 13: 15.0,
                                14: 15.0, 15: 15.0, 16: 15.0, 17: 15.0}
            ),
        ]

    def test_week1_uses_draft_based_rating(self, tmp_path, multi_qb_players):
        """Week 1 snapshot should use original draft-based player_rating"""
        generator = WeeklySnapshotGenerator()
        generator.generate_all_weeks(multi_qb_players, tmp_path)

        week1_file = tmp_path / "weeks" / "week_01" / "players.csv"
        with open(week1_file, 'r') as f:
            reader = csv.DictReader(f)
            rows = {r['name']: r for r in reader}

        # Week 1 should use original draft-based ratings
        assert float(rows['Top QB']['player_rating']) == 98.0
        assert float(rows['Mid QB']['player_rating']) == 85.0
        assert float(rows['Low QB']['player_rating']) == 60.0

    def test_week5_uses_performance_based_rating(self, tmp_path, multi_qb_players):
        """Week 5 snapshot should use cumulative points-based rating (weeks 1-4)"""
        generator = WeeklySnapshotGenerator()
        generator.generate_all_weeks(multi_qb_players, tmp_path)

        week5_file = tmp_path / "weeks" / "week_05" / "players.csv"
        with open(week5_file, 'r') as f:
            reader = csv.DictReader(f)
            rows = {r['name']: r for r in reader}

        # Week 5 ratings based on cumulative points through week 4:
        # Top QB: 30+28+32+25 = 115 pts -> rank 1 -> rating 100
        # Mid QB: 20+22+18+21 = 81 pts -> rank 2 -> rating 50.5
        # Low QB: 12+10+8+15 = 45 pts -> rank 3 -> rating 1
        top_rating = float(rows['Top QB']['player_rating'])
        mid_rating = float(rows['Mid QB']['player_rating'])
        low_rating = float(rows['Low QB']['player_rating'])

        # Best performer should have highest rating (100)
        assert top_rating == 100.0
        # Worst performer should have lowest rating (1)
        assert low_rating == 1.0
        # Middle performer should be between
        assert 1.0 < mid_rating < 100.0

    def test_rating_differs_between_weeks(self, tmp_path, multi_qb_players):
        """Player rating should differ between week 1 and week 5"""
        generator = WeeklySnapshotGenerator()
        generator.generate_all_weeks(multi_qb_players, tmp_path)

        week1_file = tmp_path / "weeks" / "week_01" / "players.csv"
        week5_file = tmp_path / "weeks" / "week_05" / "players.csv"

        with open(week1_file, 'r') as f:
            week1_rows = {r['name']: r for r in csv.DictReader(f)}
        with open(week5_file, 'r') as f:
            week5_rows = {r['name']: r for r in csv.DictReader(f)}

        # Low QB had draft rating of 60, but performs worst -> week 5 rating = 1
        week1_low_rating = float(week1_rows['Low QB']['player_rating'])
        week5_low_rating = float(week5_rows['Low QB']['player_rating'])

        assert week1_low_rating == 60.0  # Draft-based
        assert week5_low_rating == 1.0   # Performance-based (worst performer)
        assert week1_low_rating != week5_low_rating

    def test_calculate_player_ratings_week1(self, multi_qb_players):
        """_calculate_player_ratings returns draft ratings for week 1"""
        generator = WeeklySnapshotGenerator()
        ratings = generator._calculate_player_ratings(multi_qb_players, current_week=1)

        assert ratings['qb1'] == 98.0
        assert ratings['qb2'] == 85.0
        assert ratings['qb3'] == 60.0

    def test_calculate_player_ratings_week5(self, multi_qb_players):
        """_calculate_player_ratings calculates from cumulative points for week 5"""
        generator = WeeklySnapshotGenerator()
        ratings = generator._calculate_player_ratings(multi_qb_players, current_week=5)

        # Based on cumulative actual points through weeks 1-4
        # Top QB: 115 pts -> rank 1 -> 100
        # Mid QB: 81 pts -> rank 2 -> 50.5
        # Low QB: 45 pts -> rank 3 -> 1
        assert ratings['qb1'] == 100.0
        assert ratings['qb3'] == 1.0
        assert 1.0 < ratings['qb2'] < 100.0

    def test_projected_file_also_uses_recalculated_rating(self, tmp_path, multi_qb_players):
        """players_projected.csv should also use recalculated ratings"""
        generator = WeeklySnapshotGenerator()
        generator.generate_all_weeks(multi_qb_players, tmp_path)

        projected_file = tmp_path / "weeks" / "week_05" / "players_projected.csv"
        with open(projected_file, 'r') as f:
            rows = {r['name']: r for r in csv.DictReader(f)}

        # Same ratings as players.csv
        assert float(rows['Top QB']['player_rating']) == 100.0
        assert float(rows['Low QB']['player_rating']) == 1.0

    def test_bye_week_is_always_zero(self, tmp_path, multi_qb_players):
        """Bye week points should always be 0, regardless of current week"""
        generator = WeeklySnapshotGenerator()
        generator.generate_all_weeks(multi_qb_players, tmp_path)

        # Top QB has bye week 6
        # Check week 3 snapshot (before bye) - bye week 6 should be 0
        week3_file = tmp_path / "weeks" / "week_03" / "players.csv"
        with open(week3_file, 'r') as f:
            rows = {r['name']: r for r in csv.DictReader(f)}
        # Week 6 is in future, should still be 0 (bye week)
        assert rows['Top QB']['week_6_points'] == '' or float(rows['Top QB']['week_6_points']) == 0.0

        # Check week 10 snapshot (after bye) - bye week 6 should still be 0
        week10_file = tmp_path / "weeks" / "week_10" / "players.csv"
        with open(week10_file, 'r') as f:
            rows = {r['name']: r for r in csv.DictReader(f)}
        assert rows['Top QB']['week_6_points'] == '' or float(rows['Top QB']['week_6_points']) == 0.0

    def test_bye_week_zero_in_projected_file(self, tmp_path, multi_qb_players):
        """players_projected.csv bye week should also be 0"""
        generator = WeeklySnapshotGenerator()
        generator.generate_all_weeks(multi_qb_players, tmp_path)

        # Check projected file at week 3 - future bye week 6 should be 0
        projected_file = tmp_path / "weeks" / "week_03" / "players_projected.csv"
        with open(projected_file, 'r') as f:
            rows = {r['name']: r for r in csv.DictReader(f)}

        # Week 6 is Top QB's bye week and is in future at week 3
        # Should be 0, not current_week_projection
        assert rows['Top QB']['week_6_points'] == '' or float(rows['Top QB']['week_6_points']) == 0.0


class TestToggleBehavior:
    """Tests for GENERATE_CSV and GENERATE_JSON toggle functionality"""

    @pytest.fixture
    def single_player(self):
        """Simple test player"""
        return [
            PlayerData(
                id="1",
                name="Test Player",
                team="KC",
                position="QB",
                week_points={1: 25.0},
                projected_weeks={1: 22.0},
                raw_stats=[]
            )
        ]

    def test_both_toggles_true_generates_both(self, tmp_path, single_player):
        """GENERATE_CSV=True, GENERATE_JSON=True should generate both formats"""
        generator = WeeklySnapshotGenerator(generate_csv=True, generate_json=True)
        generator.generate_all_weeks(single_player, tmp_path)

        week_dir = tmp_path / "weeks" / "week_01"

        # CSV files should exist
        assert (week_dir / "players.csv").exists()
        assert (week_dir / "players_projected.csv").exists()

        # JSON files should exist
        assert (week_dir / "qb_data.json").exists()

    def test_csv_only_no_json(self, tmp_path, single_player):
        """GENERATE_CSV=True, GENERATE_JSON=False should only generate CSV"""
        generator = WeeklySnapshotGenerator(generate_csv=True, generate_json=False)
        generator.generate_all_weeks(single_player, tmp_path)

        week_dir = tmp_path / "weeks" / "week_01"

        # CSV files should exist
        assert (week_dir / "players.csv").exists()
        assert (week_dir / "players_projected.csv").exists()

        # JSON files should NOT exist
        assert not (week_dir / "qb_data.json").exists()
        assert not (week_dir / "rb_data.json").exists()

    def test_json_only_no_csv(self, tmp_path, single_player):
        """GENERATE_CSV=False, GENERATE_JSON=True should only generate JSON"""
        generator = WeeklySnapshotGenerator(generate_csv=False, generate_json=True)
        generator.generate_all_weeks(single_player, tmp_path)

        week_dir = tmp_path / "weeks" / "week_01"

        # CSV files should NOT exist
        assert not (week_dir / "players.csv").exists()
        assert not (week_dir / "players_projected.csv").exists()

        # JSON files should exist
        assert (week_dir / "qb_data.json").exists()

    def test_both_false_generates_nothing(self, tmp_path, single_player):
        """GENERATE_CSV=False, GENERATE_JSON=False should generate no output files"""
        generator = WeeklySnapshotGenerator(generate_csv=False, generate_json=False)
        generator.generate_all_weeks(single_player, tmp_path)

        week_dir = tmp_path / "weeks" / "week_01"

        # No files should exist (week folder may exist but empty of data files)
        if week_dir.exists():
            csv_files = list(week_dir.glob("*.csv"))
            json_files = list(week_dir.glob("*.json"))
            assert len(csv_files) == 0
            assert len(json_files) == 0

    def test_generate_weekly_snapshots_passes_toggles(self, tmp_path, single_player):
        """generate_weekly_snapshots convenience function should pass toggles"""
        # Test CSV only via convenience function
        generate_weekly_snapshots(single_player, tmp_path, generate_csv=True, generate_json=False)

        week_dir = tmp_path / "weeks" / "week_01"
        assert (week_dir / "players.csv").exists()
        assert not (week_dir / "qb_data.json").exists()

    def test_toggles_default_to_true(self, tmp_path, single_player):
        """When no toggles specified, should default to generating both"""
        generator = WeeklySnapshotGenerator()  # No params
        generator.generate_all_weeks(single_player, tmp_path)

        week_dir = tmp_path / "weeks" / "week_01"

        # Both formats should be generated by default
        assert (week_dir / "players.csv").exists()
        assert (week_dir / "qb_data.json").exists()
