#!/usr/bin/env python3
"""
Tests for historical_data_compiler/player_data_fetcher.py

Tests PlayerData model and raw_stats field functionality.
"""

import pytest
import sys
from pathlib import Path
from dataclasses import field

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from historical_data_compiler.player_data_fetcher import PlayerData


class TestPlayerDataModel:
    """Tests for PlayerData dataclass"""

    def test_player_data_has_raw_stats_field(self):
        """PlayerData should have raw_stats field"""
        player = PlayerData(
            id="12345",
            name="Test Player",
            team="KC",
            position="QB"
        )
        assert hasattr(player, 'raw_stats')

    def test_raw_stats_defaults_to_empty_list(self):
        """raw_stats should default to empty list"""
        player = PlayerData(
            id="12345",
            name="Test Player",
            team="KC",
            position="QB"
        )
        assert player.raw_stats == []
        assert isinstance(player.raw_stats, list)

    def test_raw_stats_can_be_populated(self):
        """raw_stats should accept list of dicts"""
        test_stats = [
            {'id': '002024', 'stats': [10.0, 20.0, 30.0]},
            {'id': '102024', 'stats': [15.0, 25.0, 35.0]}
        ]
        player = PlayerData(
            id="12345",
            name="Test Player",
            team="KC",
            position="QB",
            raw_stats=test_stats
        )
        assert player.raw_stats == test_stats
        assert len(player.raw_stats) == 2

    def test_raw_stats_preserves_structure(self):
        """raw_stats should preserve ESPN API structure"""
        espn_stats = [
            {
                'id': '002024',
                'seasonId': 2024,
                'statSourceId': 0,  # Actual stats
                'statSplitTypeId': 1,
                'stats': {
                    '0': 25.5,  # Passing attempts
                    '3': 350.2  # Passing yards
                }
            }
        ]
        player = PlayerData(
            id="12345",
            name="Test Player",
            team="KC",
            position="QB",
            raw_stats=espn_stats
        )
        assert player.raw_stats[0]['statSourceId'] == 0
        assert player.raw_stats[0]['stats']['0'] == 25.5

    def test_player_data_all_fields(self):
        """PlayerData should support all fields including raw_stats"""
        player = PlayerData(
            id="12345",
            name="Patrick Mahomes",
            team="KC",
            position="QB",
            bye_week=10,
            fantasy_points=325.5,
            average_draft_position=8.5,
            player_rating=98.5,
            injury_status="ACTIVE",
            week_points={1: 25.5, 2: 30.2},
            projected_weeks={1: 24.0, 2: 28.0},
            raw_stats=[{'id': '002024', 'stats': []}]
        )
        assert player.id == "12345"
        assert player.name == "Patrick Mahomes"
        assert player.position == "QB"
        assert player.raw_stats == [{'id': '002024', 'stats': []}]

    def test_raw_stats_independent_instances(self):
        """Each PlayerData instance should have independent raw_stats"""
        player1 = PlayerData(id="1", name="Player1", team="KC", position="QB")
        player2 = PlayerData(id="2", name="Player2", team="SF", position="RB")

        player1.raw_stats.append({'test': 'data1'})

        assert len(player1.raw_stats) == 1
        assert len(player2.raw_stats) == 0
        assert player1.raw_stats != player2.raw_stats


class TestPlayerDataCSVConversion:
    """Tests for PlayerData to_csv_row method"""

    def test_to_csv_row_does_not_include_raw_stats(self):
        """CSV export should not include raw_stats field"""
        player = PlayerData(
            id="12345",
            name="Test Player",
            team="KC",
            position="QB",
            raw_stats=[{'test': 'data'}]
        )
        csv_row = player.to_csv_row()

        # raw_stats should not be in CSV output
        assert 'raw_stats' not in csv_row

        # Standard fields should be present
        assert 'id' in csv_row
        assert 'name' in csv_row
        assert 'position' in csv_row
