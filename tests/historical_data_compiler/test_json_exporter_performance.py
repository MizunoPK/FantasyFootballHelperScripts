#!/usr/bin/env python3
"""Tests for DataExporter instantiation performance in JSONSnapshotExporter."""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from historical_data_compiler.json_exporter import generate_json_snapshots
from historical_data_compiler.player_data_fetcher import PlayerData
from historical_data_compiler.constants import REGULAR_SEASON_WEEKS


def _make_player(position: str) -> PlayerData:
    return PlayerData(
        id="test_id_01",
        name="Test Player",
        team="KC",
        position=position,
        bye_week=7,
    )


class TestJSONSnapshotExporterPerformance:

    def test_data_exporter_instantiated_once_per_generate_call(self, tmp_path):
        players = [
            _make_player("QB"),
            _make_player("RB"),
            _make_player("WR"),
            _make_player("TE"),
            _make_player("K"),
            _make_player("DST"),
        ]

        with patch("historical_data_compiler.json_exporter.DataExporter") as mock_de:
            mock_instance = mock_de.return_value
            mock_instance._extract_passing_stats.return_value = {}
            mock_instance._extract_rushing_stats.return_value = {}
            mock_instance._extract_receiving_stats.return_value = {}
            mock_instance._extract_misc_stats.return_value = {}
            mock_instance._extract_kicking_stats.return_value = {}
            mock_instance._extract_defense_stats.return_value = {}

            generate_json_snapshots(players, tmp_path, current_week=1)

        assert mock_de.call_count == 1
        mock_de.assert_called_once_with(
            output_dir=str(Path.cwd()),
            current_nfl_week=REGULAR_SEASON_WEEKS + 1,
            load_drafted_data=False,
        )

    def test_no_per_player_instantiation_across_17_weeks(self, tmp_path):
        players = [
            _make_player("QB"),
            _make_player("RB"),
            _make_player("WR"),
            _make_player("TE"),
            _make_player("K"),
            _make_player("DST"),
        ]

        with patch("historical_data_compiler.json_exporter.DataExporter") as mock_de:
            mock_instance = mock_de.return_value
            mock_instance._extract_passing_stats.return_value = {}
            mock_instance._extract_rushing_stats.return_value = {}
            mock_instance._extract_receiving_stats.return_value = {}
            mock_instance._extract_misc_stats.return_value = {}
            mock_instance._extract_kicking_stats.return_value = {}
            mock_instance._extract_defense_stats.return_value = {}

            for week in range(1, 18):
                week_dir = tmp_path / f"week_{week:02d}"
                week_dir.mkdir()
                generate_json_snapshots(players, week_dir, current_week=week)

        assert mock_de.call_count == 17
