"""
Integration tests for historical_data_compiler/json_exporter.py dict-wrapper format,
QB receiving section, and misc.fumbles section.
"""
import json
import pytest
from unittest.mock import patch

from historical_data_compiler.json_exporter import JSONSnapshotExporter
from historical_data_compiler.player_data_fetcher import PlayerData


class TestJSONExporterIntegration:
    """Integration tests validating dict-wrapper format and QB receiving/misc additions."""

    @pytest.fixture
    def exporter(self):
        """Create a JSONSnapshotExporter for testing."""
        return JSONSnapshotExporter()

    @pytest.fixture
    def qb_player(self):
        """Create a single QB PlayerData for testing."""
        return PlayerData(id="1001", name="Test QB", team="KC", position="QB", raw_stats=[])

    @pytest.fixture
    def rb_player(self):
        """Create a single RB PlayerData for testing."""
        return PlayerData(id="2001", name="Test RB", team="KC", position="RB", raw_stats=[])

    @patch('historical_data_compiler.json_exporter.DataExporter')
    def test_generate_position_json_dict_wrapper_format(self, mock_exporter_class, exporter, qb_player, tmp_path):
        """generate_position_json output is a dict with a qb_data root key, not a bare list."""
        mock_exporter = mock_exporter_class.return_value
        mock_exporter._extract_passing_stats.return_value = {'attempts': [0.0] * 17}
        mock_exporter._extract_rushing_stats.return_value = {'rush_yds': [0.0] * 17}
        mock_exporter._extract_receiving_stats.return_value = {
            'targets': [0.0] * 17, 'receiving_yds': [0.0] * 17,
            'receiving_tds': [0.0] * 17, 'receptions': [0.0] * 17
        }
        mock_exporter._extract_misc_stats.return_value = {'fumbles': [0.0] * 17}

        output_file = tmp_path / "qb_data.json"
        exporter.generate_position_json([qb_player], "QB", output_file, current_week=1)

        with open(output_file) as f:
            data = json.load(f)

        assert isinstance(data, dict)
        assert 'qb_data' in data
        assert isinstance(data['qb_data'], list)

    @patch('historical_data_compiler.json_exporter.DataExporter')
    def test_qb_player_includes_receiving_and_misc(self, mock_exporter_class, exporter, qb_player, tmp_path):
        """QB player objects include receiving section with 4 sub-keys and misc.fumbles, each 17 elements."""
        mock_exporter = mock_exporter_class.return_value
        mock_exporter._extract_passing_stats.return_value = {'attempts': [0.0] * 17}
        mock_exporter._extract_rushing_stats.return_value = {'rush_yds': [0.0] * 17}
        mock_exporter._extract_receiving_stats.return_value = {
            'targets': [2.0] * 17,
            'receiving_yds': [15.0] * 17,
            'receiving_tds': [0.5] * 17,
            'receptions': [1.5] * 17
        }
        mock_exporter._extract_misc_stats.return_value = {'fumbles': [0.5] * 17}

        output_file = tmp_path / "qb_data.json"
        exporter.generate_position_json([qb_player], "QB", output_file, current_week=1)

        with open(output_file) as f:
            data = json.load(f)

        player = data['qb_data'][0]
        assert 'receiving' in player
        assert 'targets' in player['receiving']
        assert 'receiving_yds' in player['receiving']
        assert 'receiving_tds' in player['receiving']
        assert 'receptions' in player['receiving']
        assert len(player['receiving']['targets']) == 17
        assert 'misc' in player
        assert 'fumbles' in player['misc']
        assert len(player['misc']['fumbles']) == 17

    @patch('historical_data_compiler.json_exporter.DataExporter')
    def test_rb_player_includes_misc_not_qb_stats(self, mock_exporter_class, exporter, rb_player, tmp_path):
        """RB player objects include misc.fumbles and do not include passing."""
        mock_exporter = mock_exporter_class.return_value
        mock_exporter._extract_rushing_stats.return_value = {'rush_yds': [0.0] * 17}
        mock_exporter._extract_receiving_stats.return_value = {
            'targets': [0.0] * 17, 'receiving_yds': [0.0] * 17,
            'receiving_tds': [0.0] * 17, 'receptions': [0.0] * 17
        }
        mock_exporter._extract_misc_stats.return_value = {'fumbles': [0.5] * 17}

        output_file = tmp_path / "rb_data.json"
        exporter.generate_position_json([rb_player], "RB", output_file, current_week=1)

        with open(output_file) as f:
            data = json.load(f)

        player = data['rb_data'][0]
        assert 'misc' in player
        assert 'fumbles' in player['misc']
        assert len(player['misc']['fumbles']) == 17
        assert 'passing' not in player

    def test_empty_position_dict_wrapper(self, exporter, tmp_path):
        """Empty player list writes {qb_data: []} not a bare empty list."""
        output_file = tmp_path / "qb_data.json"
        exporter.generate_position_json([], "QB", output_file, current_week=1)

        with open(output_file) as f:
            data = json.load(f)

        assert data == {'qb_data': []}
