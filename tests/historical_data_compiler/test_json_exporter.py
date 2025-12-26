#!/usr/bin/env python3
"""
Tests for historical_data_compiler/json_exporter.py

Tests JSON snapshot generation, PlayerDataAdapter bridge pattern,
and point-in-time logic.
"""

import pytest
import json
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from historical_data_compiler.json_exporter import (
    PlayerDataAdapter,
    JSONSnapshotExporter,
    generate_json_snapshots
)
from historical_data_compiler.player_data_fetcher import PlayerData


class TestPlayerDataAdapter:
    """Tests for PlayerDataAdapter bridge pattern"""

    def test_adapter_converts_player_data(self):
        """Adapter should convert PlayerData to ESPNPlayerData-like object"""
        player = PlayerData(
            id="12345",
            name="Patrick Mahomes",
            team="KC",
            position="QB",
            bye_week=10,
            injury_status="ACTIVE",
            average_draft_position=8.5,
            raw_stats=[{'test': 'data'}]
        )

        adapter = PlayerDataAdapter(player)

        assert adapter.id == "12345"
        assert adapter.name == "Patrick Mahomes"
        assert adapter.team == "KC"
        assert adapter.position == "QB"
        assert adapter.bye_week == 10
        assert adapter.injury_status == "ACTIVE"
        assert adapter.average_draft_position == 8.5
        assert adapter.raw_stats == [{'test': 'data'}]

    def test_adapter_handles_null_injury_status(self):
        """Adapter should convert null injury_status to ACTIVE"""
        player = PlayerData(
            id="12345",
            name="Test Player",
            team="KC",
            position="QB",
            injury_status=None
        )

        adapter = PlayerDataAdapter(player)

        assert adapter.injury_status == "ACTIVE"

    def test_adapter_preserves_raw_stats(self):
        """Adapter should preserve raw_stats for stat extraction"""
        raw_stats = [
            {'id': '002024', 'stats': {'0': 25.5, '3': 350.2}},
            {'id': '102024', 'stats': {'0': 24.0, '3': 340.0}}
        ]
        player = PlayerData(
            id="12345",
            name="Test Player",
            team="KC",
            position="QB",
            raw_stats=raw_stats
        )

        adapter = PlayerDataAdapter(player)

        assert adapter.raw_stats == raw_stats
        assert len(adapter.raw_stats) == 2


class TestJSONSnapshotExporter:
    """Tests for JSONSnapshotExporter"""

    @pytest.fixture
    def exporter(self):
        """Create JSONSnapshotExporter instance"""
        return JSONSnapshotExporter()

    @pytest.fixture
    def sample_players(self):
        """Create sample PlayerData objects for testing"""
        return [
            PlayerData(
                id="1001",
                name="QB Player 1",
                team="KC",
                position="QB",
                bye_week=10,
                fantasy_points=300.0,
                player_rating=95.0,
                week_points={1: 25.5, 2: 30.2, 3: 28.0},
                projected_weeks={1: 24.0, 2: 28.0, 3: 27.0, 4: 25.0},
                raw_stats=[]
            ),
            PlayerData(
                id="1002",
                name="QB Player 2",
                team="SF",
                position="QB",
                fantasy_points=280.0,
                player_rating=88.0,
                week_points={1: 22.0, 2: 24.5, 3: 26.0},
                projected_weeks={1: 23.0, 2: 25.0, 3: 26.0, 4: 24.0},
                raw_stats=[]
            )
        ]

    def test_calculate_player_ratings_week_1(self, exporter, sample_players):
        """Week 1 should use original draft-based ratings"""
        ratings = exporter._calculate_player_ratings(sample_players, current_week=1)

        assert ratings["1001"] == 95.0
        assert ratings["1002"] == 88.0

    def test_calculate_player_ratings_week_2_plus(self, exporter, sample_players):
        """Week 2+ should recalculate from cumulative actual points"""
        # Week 2: Only week 1 actuals count
        ratings_week2 = exporter._calculate_player_ratings(sample_players, current_week=2)

        # Player 1 had 25.5 points in week 1 (better than Player 2's 22.0)
        # Player 1 should have higher rating
        assert ratings_week2["1001"] > ratings_week2["1002"]
        assert 1.0 <= ratings_week2["1001"] <= 100.0
        assert 1.0 <= ratings_week2["1002"] <= 100.0

    def test_apply_point_in_time_logic_actual_array(self, exporter):
        """Actual arrays should have actuals for past, 0.0 for future"""
        full_array = [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0,
                      110.0, 120.0, 130.0, 140.0, 150.0, 160.0, 170.0]
        current_week = 5

        result = exporter._apply_point_in_time_logic(
            full_array,
            current_week,
            "actual"
        )

        # Weeks 1-4: actual values
        assert result[0] == 10.0
        assert result[1] == 20.0
        assert result[2] == 30.0
        assert result[3] == 40.0

        # Weeks 5-17: 0.0
        assert result[4] == 0.0
        assert result[5] == 0.0
        assert result[16] == 0.0

    def test_apply_point_in_time_logic_projected_array(self, exporter):
        """Projected arrays should have historical for past, current for future"""
        full_array = [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0,
                      110.0, 120.0, 130.0, 140.0, 150.0, 160.0, 170.0]
        current_week = 5
        current_week_value = 99.9

        result = exporter._apply_point_in_time_logic(
            full_array,
            current_week,
            "projected",
            current_week_value=current_week_value
        )

        # Weeks 1-4: historical projections
        assert result[0] == 10.0
        assert result[1] == 20.0
        assert result[2] == 30.0
        assert result[3] == 40.0

        # Weeks 5-17: current week projection
        assert result[4] == 99.9
        assert result[5] == 99.9
        assert result[16] == 99.9

    def test_apply_point_in_time_logic_stat_array(self, exporter):
        """Stat arrays should have actuals for past, 0.0 for future"""
        full_array = [5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0,
                      55.0, 60.0, 65.0, 70.0, 75.0, 80.0, 85.0]
        current_week = 3

        result = exporter._apply_point_in_time_logic(
            full_array,
            current_week,
            "stat"
        )

        # Weeks 1-2: actual stats
        assert result[0] == 5.0
        assert result[1] == 10.0

        # Weeks 3-17: 0.0
        assert result[2] == 0.0
        assert result[3] == 0.0
        assert result[16] == 0.0

    @patch('historical_data_compiler.json_exporter.DataExporter')
    def test_extract_stats_for_player_qb(self, mock_exporter_class, exporter):
        """Should extract QB stats using bridge adapter"""
        mock_exporter = Mock()
        mock_exporter._extract_passing_stats.return_value = {
            'attempts': [30.0] * 17,
            'completions': [20.0] * 17
        }
        mock_exporter._extract_rushing_stats.return_value = {
            'rush_att': [5.0] * 17,
            'rush_yds': [25.0] * 17
        }
        mock_exporter_class.return_value = mock_exporter

        player = PlayerData(
            id="1001",
            name="QB Test",
            team="KC",
            position="QB",
            raw_stats=[{'test': 'data'}]
        )

        stats = exporter._extract_stats_for_player(player, current_week=5)

        # Should call QB stat extraction methods
        assert mock_exporter._extract_passing_stats.called
        assert mock_exporter._extract_rushing_stats.called
        # Stats should be wrapped in position keys
        assert 'passing' in stats
        assert 'rushing' in stats
        assert 'attempts' in stats['passing']
        assert 'rush_att' in stats['rushing']

    def test_build_player_json_object_structure(self, exporter):
        """JSON object should have all required fields"""
        player = PlayerData(
            id="1001",
            name="Test Player",
            team="KC",
            position="QB",
            bye_week=10,
            injury_status="ACTIVE",
            average_draft_position=8.5,
            week_points={1: 25.5, 2: 30.2},
            projected_weeks={1: 24.0, 2: 28.0, 3: 27.0},
            raw_stats=[]
        )

        with patch.object(exporter, '_extract_stats_for_player', return_value={}):
            result = exporter._build_player_json_object(player, current_week=3, player_rating=95.0)

        # Check all required fields
        assert result['id'] == "1001"
        assert result['name'] == "Test Player"
        assert result['team'] == "KC"
        assert result['position'] == "QB"
        assert result['injury_status'] == "ACTIVE"
        assert result['drafted_by'] == ""
        assert result['locked'] is False
        assert result['average_draft_position'] == 8.5
        assert result['player_rating'] == 95.0
        assert 'projected_points' in result
        assert 'actual_points' in result
        assert len(result['projected_points']) == 17
        assert len(result['actual_points']) == 17

    def test_build_player_json_object_bye_week(self, exporter):
        """Bye week should be 0.0 in all arrays"""
        player = PlayerData(
            id="1001",
            name="Test Player",
            team="KC",
            position="QB",
            bye_week=5,  # Week 5 is bye
            week_points={1: 25.5, 2: 30.2, 5: 10.0},  # Week 5 shouldn't count
            projected_weeks={1: 24.0, 2: 28.0, 5: 27.0},
            raw_stats=[]
        )

        with patch.object(exporter, '_extract_stats_for_player', return_value={}):
            result = exporter._build_player_json_object(player, current_week=10, player_rating=95.0)

        # Bye week (week 5, index 4) should be 0.0
        assert result['actual_points'][4] == 0.0
        assert result['projected_points'][4] == 0.0

    def test_generate_position_json_creates_file(self, exporter, sample_players, tmp_path):
        """Should generate JSON file for position"""
        output_file = tmp_path / "qb_data.json"

        with patch.object(exporter, '_extract_stats_for_player', return_value={}):
            exporter.generate_position_json(sample_players, "QB", output_file, current_week=3)

        assert output_file.exists()

        # Verify JSON structure
        with open(output_file) as f:
            data = json.load(f)

        assert isinstance(data, list)
        assert len(data) == 2  # Both QB players
        assert data[0]['position'] == 'QB'
        assert data[1]['position'] == 'QB'

    def test_generate_position_json_sorts_by_rating(self, exporter, sample_players, tmp_path):
        """Should sort players by rating descending"""
        output_file = tmp_path / "qb_data.json"

        with patch.object(exporter, '_extract_stats_for_player', return_value={}):
            exporter.generate_position_json(sample_players, "QB", output_file, current_week=1)

        with open(output_file) as f:
            data = json.load(f)

        # Player 1 (95.0 rating) should be first
        assert data[0]['id'] == "1001"
        assert data[0]['player_rating'] == 95.0
        assert data[1]['id'] == "1002"
        assert data[1]['player_rating'] == 88.0


class TestGenerateJSONSnapshots:
    """Tests for generate_json_snapshots function"""

    @pytest.fixture
    def sample_players(self):
        """Create sample players for all positions"""
        return [
            PlayerData(id="1", name="QB1", team="KC", position="QB", raw_stats=[]),
            PlayerData(id="2", name="RB1", team="SF", position="RB", raw_stats=[]),
            PlayerData(id="3", name="WR1", team="DAL", position="WR", raw_stats=[]),
            PlayerData(id="4", name="TE1", team="KC", position="TE", raw_stats=[]),
            PlayerData(id="5", name="K1", team="BAL", position="K", raw_stats=[]),
            PlayerData(id="6", name="DST1", team="BUF", position="DST", raw_stats=[]),
        ]

    @patch('historical_data_compiler.json_exporter.JSONSnapshotExporter')
    def test_generate_json_snapshots_all_positions(self, mock_exporter_class, sample_players, tmp_path):
        """Should generate JSON for all 6 positions"""
        mock_exporter = Mock()
        mock_exporter_class.return_value = mock_exporter

        generate_json_snapshots(sample_players, tmp_path, current_week=5)

        # Should call generate_position_json 6 times (one per position)
        assert mock_exporter.generate_position_json.call_count == 6

        # Verify each position was called
        calls = mock_exporter.generate_position_json.call_args_list
        positions_called = [call[0][1] for call in calls]
        expected_positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DST']
        assert set(positions_called) == set(expected_positions)
