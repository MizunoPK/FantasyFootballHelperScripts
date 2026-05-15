"""
Integration tests for WinRateMetaDataManager.
"""
import json
import datetime
import pytest
from simulation.win_rate.WinRateMetaDataManager import WinRateMetaDataManager


class TestWinRateMetaDataManagerIntegration:
    """Integration tests for WinRateMetaDataManager end-to-end file I/O lifecycle."""

    def test_initializes_with_absent_file(self, tmp_path):
        """Manager initializes without error when file absent — strategies empty."""
        path = tmp_path / "win_rate_meta_data.json"
        manager = WinRateMetaDataManager(path)
        assert manager.get_all_strategies() == {}

    def test_update_creates_valid_json_on_disk(self, tmp_path):
        """After update(), JSON file exists at meta_data_path and is valid JSON."""
        path = tmp_path / "win_rate_meta_data.json"
        manager = WinRateMetaDataManager(path)
        manager.update("1_zero_rb.json", "Zero RB", 0.6)
        assert path.exists()
        data = json.loads(path.read_text())
        assert "strategies" in data

    def test_update_entry_has_all_required_fields(self, tmp_path):
        """JSON entry contains name, best_win_rate, total_runs, last_run — all correct."""
        path = tmp_path / "win_rate_meta_data.json"
        manager = WinRateMetaDataManager(path)
        manager.update("1_zero_rb.json", "Zero RB", 0.6)
        data = json.loads(path.read_text())
        entry = data["strategies"]["1_zero_rb.json"]
        assert entry["name"] == "Zero RB"
        assert entry["best_win_rate"] == 0.6
        assert entry["total_runs"] == 1
        assert len(entry["last_run"]) == 10

    def test_second_update_increments_runs_preserves_best(self, tmp_path):
        """Second update: total_runs==2, best_win_rate unchanged when new rate is lower."""
        path = tmp_path / "win_rate_meta_data.json"
        manager = WinRateMetaDataManager(path)
        manager.update("1_zero_rb.json", "Zero RB", 0.6)
        manager.update("1_zero_rb.json", "Zero RB", 0.5)
        entry = manager.get_all_strategies()["1_zero_rb.json"]
        assert entry["total_runs"] == 2
        assert entry["best_win_rate"] == 0.6

    def test_get_all_strategies_matches_disk(self, tmp_path):
        """get_all_strategies() return matches the strategies dict in the JSON file on disk."""
        path = tmp_path / "win_rate_meta_data.json"
        manager = WinRateMetaDataManager(path)
        manager.update("1_zero_rb.json", "Zero RB", 0.6)
        data = json.loads(path.read_text())
        assert manager.get_all_strategies() == data["strategies"]
