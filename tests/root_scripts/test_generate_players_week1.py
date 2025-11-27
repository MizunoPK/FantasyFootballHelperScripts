#!/usr/bin/env python3
"""
Tests for generate_players_week1.py

Comprehensive tests for the players_week1.csv generation script including:
- calculate_position_rating function
- generate_players_week1 function
- Edge cases and error handling

Author: Kai Mizuno
"""

import pytest
import pandas as pd
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from generate_players_week1 import calculate_position_rating, generate_players_week1


class TestCalculatePositionRating:
    """Test suite for calculate_position_rating function."""

    def test_rating_with_normal_range(self):
        """Test rating calculation with normal ADP range."""
        # ADP range: 5.0 (best) to 100.0 (worst)
        adp_series = pd.Series([5.0, 25.0, 50.0, 75.0, 100.0])

        ratings = calculate_position_rating(adp_series)

        # Best ADP (5.0) should get 100
        assert abs(ratings.iloc[0] - 100.0) < 0.01
        # Worst ADP (100.0) should get 0
        assert abs(ratings.iloc[4] - 0.0) < 0.01
        # Middle ADP should be proportional
        assert 0 <= ratings.iloc[2] <= 100

    def test_rating_lowest_adp_gets_100(self):
        """Test that the lowest ADP value gets rating of 100."""
        adp_series = pd.Series([10.0, 50.0, 100.0])

        ratings = calculate_position_rating(adp_series)

        # Player with ADP 10 (lowest) should get rating 100
        assert abs(ratings.iloc[0] - 100.0) < 0.01

    def test_rating_highest_adp_gets_0(self):
        """Test that the highest ADP value gets rating of 0."""
        adp_series = pd.Series([10.0, 50.0, 100.0])

        ratings = calculate_position_rating(adp_series)

        # Player with ADP 100 (highest) should get rating 0
        assert abs(ratings.iloc[2] - 0.0) < 0.01

    def test_rating_all_same_adp_returns_50(self):
        """Test that identical ADP values all get 50.0 rating."""
        adp_series = pd.Series([25.0, 25.0, 25.0])

        ratings = calculate_position_rating(adp_series)

        # All should be 50.0 when min == max
        assert all(abs(r - 50.0) < 0.01 for r in ratings)

    def test_rating_single_player_returns_50(self):
        """Test that a single player gets 50.0 rating."""
        adp_series = pd.Series([42.0])

        ratings = calculate_position_rating(adp_series)

        assert abs(ratings.iloc[0] - 50.0) < 0.01

    def test_rating_preserves_index(self):
        """Test that output preserves input series index."""
        adp_series = pd.Series([10.0, 50.0], index=[100, 200])

        ratings = calculate_position_rating(adp_series)

        assert list(ratings.index) == [100, 200]

    def test_rating_all_values_in_range(self):
        """Test that all ratings are between 0 and 100."""
        adp_series = pd.Series([5.09, 20.67, 50.0, 100.5, 170.06])

        ratings = calculate_position_rating(adp_series)

        assert all(0 <= r <= 100 for r in ratings)

    def test_rating_formula_verification(self):
        """Test the exact formula: rating = 100 * (max - adp) / (max - min)."""
        # min=10, max=110, player_adp=60
        # Expected: 100 * (110 - 60) / (110 - 10) = 100 * 50 / 100 = 50
        adp_series = pd.Series([10.0, 60.0, 110.0])

        ratings = calculate_position_rating(adp_series)

        assert abs(ratings.iloc[1] - 50.0) < 0.01


class TestGeneratePlayersWeek1:
    """Test suite for generate_players_week1 function."""

    @pytest.fixture
    def sample_players_csv(self, tmp_path):
        """Create a sample players.csv file."""
        csv_file = tmp_path / "players.csv"
        data = pd.DataFrame({
            'id': [1, 2, 3, 4],
            'name': ['Player A', 'Player B', 'Player C', 'Player D'],
            'team': ['KC', 'BUF', 'PHI', 'SF'],
            'position': ['QB', 'QB', 'RB', 'RB'],
            'bye_week': [6, 7, 5, 9],
            'fantasy_points': [100.0, 90.0, 80.0, 70.0],  # Will be recalculated
            'injury_status': ['ACTIVE', 'QUESTIONABLE', 'ACTIVE', 'OUT'],
            'drafted': [1, 0, 1, 0],
            'locked': [0, 1, 0, 1],
            'average_draft_position': [20.0, 40.0, 10.0, 50.0],
            'player_rating': [90.0, 80.0, 95.0, 70.0],  # Will be recalculated
            'week_1_points': [25.0, 20.0, 15.0, 12.0],
            'week_2_points': [22.0, 18.0, 14.0, 11.0],
            'week_3_points': [0.0, 0.0, 0.0, 0.0],
            'week_4_points': [0.0, 0.0, 0.0, 0.0],
            'week_5_points': [0.0, 0.0, 0.0, 0.0],
            'week_6_points': [0.0, 0.0, 0.0, 0.0],
            'week_7_points': [0.0, 0.0, 0.0, 0.0],
            'week_8_points': [0.0, 0.0, 0.0, 0.0],
            'week_9_points': [0.0, 0.0, 0.0, 0.0],
            'week_10_points': [0.0, 0.0, 0.0, 0.0],
            'week_11_points': [0.0, 0.0, 0.0, 0.0],
            'week_12_points': [0.0, 0.0, 0.0, 0.0],
            'week_13_points': [0.0, 0.0, 0.0, 0.0],
            'week_14_points': [0.0, 0.0, 0.0, 0.0],
            'week_15_points': [0.0, 0.0, 0.0, 0.0],
            'week_16_points': [0.0, 0.0, 0.0, 0.0],
            'week_17_points': [0.0, 0.0, 0.0, 0.0],
        })
        data.to_csv(csv_file, index=False)
        return csv_file

    @pytest.fixture
    def sample_projected_csv(self, tmp_path):
        """Create a sample players_projected.csv file."""
        csv_file = tmp_path / "players_projected.csv"
        data = pd.DataFrame({
            'id': [1, 2, 3, 4],
            'name': ['Player A', 'Player B', 'Player C', 'Player D'],
            'week_1_points': [30.0, 25.0, 20.0, 18.0],
            'week_2_points': [28.0, 23.0, 19.0, 17.0],
            'week_3_points': [27.0, 22.0, 18.0, 16.0],
            'week_4_points': [26.0, 21.0, 17.0, 15.0],
            'week_5_points': [25.0, 20.0, 16.0, 14.0],
            'week_6_points': [0.0, 19.0, 15.0, 13.0],  # Bye week for Player A
            'week_7_points': [24.0, 0.0, 14.0, 12.0],  # Bye week for Player B
            'week_8_points': [23.0, 18.0, 13.0, 11.0],
            'week_9_points': [22.0, 17.0, 12.0, 0.0],  # Bye week for Player D
            'week_10_points': [21.0, 16.0, 11.0, 10.0],
            'week_11_points': [20.0, 15.0, 10.0, 9.0],
            'week_12_points': [19.0, 14.0, 9.0, 8.0],
            'week_13_points': [18.0, 13.0, 8.0, 7.0],
            'week_14_points': [17.0, 12.0, 7.0, 6.0],
            'week_15_points': [16.0, 11.0, 6.0, 5.0],
            'week_16_points': [15.0, 10.0, 5.0, 4.0],
            'week_17_points': [14.0, 9.0, 4.0, 3.0],
        })
        data.to_csv(csv_file, index=False)
        return csv_file

    def test_generates_output_file(self, tmp_path, sample_players_csv, sample_projected_csv):
        """Test that output file is created."""
        output_path = tmp_path / "players_week1.csv"

        generate_players_week1(sample_players_csv, sample_projected_csv, output_path)

        assert output_path.exists()

    def test_output_has_correct_row_count(self, tmp_path, sample_players_csv, sample_projected_csv):
        """Test that output has same number of rows as input."""
        output_path = tmp_path / "players_week1.csv"

        result = generate_players_week1(sample_players_csv, sample_projected_csv, output_path)

        assert len(result) == 4

    def test_output_has_correct_columns(self, tmp_path, sample_players_csv, sample_projected_csv):
        """Test that output has exactly 28 columns in correct order."""
        output_path = tmp_path / "players_week1.csv"

        result = generate_players_week1(sample_players_csv, sample_projected_csv, output_path)

        expected_cols = [
            'id', 'name', 'team', 'position', 'bye_week', 'fantasy_points',
            'injury_status', 'drafted', 'locked', 'average_draft_position', 'player_rating'
        ] + [f'week_{i}_points' for i in range(1, 18)]

        assert list(result.columns) == expected_cols
        assert len(result.columns) == 28

    def test_drafted_is_always_zero(self, tmp_path, sample_players_csv, sample_projected_csv):
        """Test that drafted column is always 0."""
        output_path = tmp_path / "players_week1.csv"

        result = generate_players_week1(sample_players_csv, sample_projected_csv, output_path)

        assert all(result['drafted'] == 0)

    def test_locked_is_always_zero(self, tmp_path, sample_players_csv, sample_projected_csv):
        """Test that locked column is always 0."""
        output_path = tmp_path / "players_week1.csv"

        result = generate_players_week1(sample_players_csv, sample_projected_csv, output_path)

        assert all(result['locked'] == 0)

    def test_injury_status_is_always_active(self, tmp_path, sample_players_csv, sample_projected_csv):
        """Test that injury_status is always 'ACTIVE'."""
        output_path = tmp_path / "players_week1.csv"

        result = generate_players_week1(sample_players_csv, sample_projected_csv, output_path)

        assert all(result['injury_status'] == 'ACTIVE')

    def test_fantasy_points_is_sum_of_weeks(self, tmp_path, sample_players_csv, sample_projected_csv):
        """Test that fantasy_points equals sum of week columns."""
        output_path = tmp_path / "players_week1.csv"

        result = generate_players_week1(sample_players_csv, sample_projected_csv, output_path)

        week_cols = [f'week_{i}_points' for i in range(1, 18)]
        for idx, row in result.iterrows():
            expected_sum = sum(row[col] for col in week_cols)
            assert abs(row['fantasy_points'] - expected_sum) < 0.01

    def test_week_points_come_from_projected_file(self, tmp_path, sample_players_csv, sample_projected_csv):
        """Test that week points are from projected file, not players file."""
        output_path = tmp_path / "players_week1.csv"

        result = generate_players_week1(sample_players_csv, sample_projected_csv, output_path)

        # Player A (id=1) should have week_1_points=30.0 from projected (not 25.0 from players)
        player_a = result[result['id'] == 1].iloc[0]
        assert abs(player_a['week_1_points'] - 30.0) < 0.01

    def test_player_rating_per_position(self, tmp_path, sample_players_csv, sample_projected_csv):
        """Test that player_rating is calculated per position."""
        output_path = tmp_path / "players_week1.csv"

        result = generate_players_week1(sample_players_csv, sample_projected_csv, output_path)

        # QBs: Player A (ADP 20) should be 100, Player B (ADP 40) should be 0
        qbs = result[result['position'] == 'QB']
        player_a_rating = qbs[qbs['id'] == 1]['player_rating'].iloc[0]
        player_b_rating = qbs[qbs['id'] == 2]['player_rating'].iloc[0]
        assert abs(player_a_rating - 100.0) < 0.01
        assert abs(player_b_rating - 0.0) < 0.01

        # RBs: Player C (ADP 10) should be 100, Player D (ADP 50) should be 0
        rbs = result[result['position'] == 'RB']
        player_c_rating = rbs[rbs['id'] == 3]['player_rating'].iloc[0]
        player_d_rating = rbs[rbs['id'] == 4]['player_rating'].iloc[0]
        assert abs(player_c_rating - 100.0) < 0.01
        assert abs(player_d_rating - 0.0) < 0.01

    def test_player_rating_range_is_0_to_100(self, tmp_path, sample_players_csv, sample_projected_csv):
        """Test that all player ratings are between 0 and 100."""
        output_path = tmp_path / "players_week1.csv"

        result = generate_players_week1(sample_players_csv, sample_projected_csv, output_path)

        assert all(0 <= r <= 100 for r in result['player_rating'])

    def test_preserves_player_metadata(self, tmp_path, sample_players_csv, sample_projected_csv):
        """Test that player metadata (id, name, team, position, bye_week, adp) is preserved."""
        output_path = tmp_path / "players_week1.csv"

        result = generate_players_week1(sample_players_csv, sample_projected_csv, output_path)

        player_a = result[result['id'] == 1].iloc[0]
        assert player_a['name'] == 'Player A'
        assert player_a['team'] == 'KC'
        assert player_a['position'] == 'QB'
        assert player_a['bye_week'] == 6
        assert abs(player_a['average_draft_position'] - 20.0) < 0.01


class TestGeneratePlayersWeek1EdgeCases:
    """Test edge cases for generate_players_week1 function."""

    @pytest.fixture
    def single_player_per_position(self, tmp_path):
        """Create files with single player per position."""
        players = tmp_path / "players.csv"
        projected = tmp_path / "projected.csv"

        player_data = pd.DataFrame({
            'id': [1, 2],
            'name': ['Only QB', 'Only RB'],
            'team': ['KC', 'BUF'],
            'position': ['QB', 'RB'],
            'bye_week': [6, 7],
            'fantasy_points': [100.0, 80.0],
            'injury_status': ['ACTIVE', 'ACTIVE'],
            'drafted': [0, 0],
            'locked': [0, 0],
            'average_draft_position': [20.0, 15.0],
            'player_rating': [90.0, 95.0],
            **{f'week_{i}_points': [0.0, 0.0] for i in range(1, 18)}
        })
        player_data.to_csv(players, index=False)

        proj_data = pd.DataFrame({
            'id': [1, 2],
            'name': ['Only QB', 'Only RB'],
            **{f'week_{i}_points': [10.0, 12.0] for i in range(1, 18)}
        })
        proj_data.to_csv(projected, index=False)

        return players, projected

    def test_single_player_per_position_gets_rating_50(self, tmp_path, single_player_per_position):
        """Test that single player in a position gets rating of 50."""
        players, projected = single_player_per_position
        output_path = tmp_path / "output.csv"

        result = generate_players_week1(players, projected, output_path)

        # Both players should have rating 50 (only player in their position)
        assert all(abs(r - 50.0) < 0.01 for r in result['player_rating'])
