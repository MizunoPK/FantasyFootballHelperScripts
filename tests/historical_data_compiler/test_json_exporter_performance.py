#!/usr/bin/env python3
"""Tests for DataExporter instantiation performance in JSONSnapshotExporter."""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from historical_data_compiler.json_exporter import generate_json_snapshots
from historical_data_compiler.player_data_fetcher import PlayerData


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
        players = [_make_player("QB")]

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
