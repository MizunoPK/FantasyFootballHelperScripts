import json
import datetime
import pytest
from simulation.win_rate.WinRateMetaDataManager import WinRateMetaDataManager


def test_load_no_file_creates_empty_structure(tmp_path):
    path = tmp_path / "win_rate_meta_data.json"
    manager = WinRateMetaDataManager(path)
    assert manager.get_all_strategies() == {}


def test_load_existing_file_reads_correctly(tmp_path):
    path = tmp_path / "win_rate_meta_data.json"
    data = {
        "last_updated": "2026-05-01",
        "strategies": {
            "1_zero_rb.json": {
                "name": "Zero RB",
                "best_win_rate": 0.623,
                "total_runs": 47,
                "last_run": "2026-05-01",
            }
        },
    }
    path.write_text(json.dumps(data))
    manager = WinRateMetaDataManager(path)
    strategies = manager.get_all_strategies()
    assert "1_zero_rb.json" in strategies
    assert strategies["1_zero_rb.json"]["best_win_rate"] == 0.623
    assert strategies["1_zero_rb.json"]["total_runs"] == 47


def test_load_corrupted_json_initializes_empty(tmp_path):
    path = tmp_path / "win_rate_meta_data.json"
    path.write_text("not valid json {{{{")
    manager = WinRateMetaDataManager(path)
    assert manager.get_all_strategies() == {}


def test_update_new_strategy_creates_entry(tmp_path):
    path = tmp_path / "win_rate_meta_data.json"
    manager = WinRateMetaDataManager(path)
    manager.update("1_zero_rb.json", "Zero RB", 0.6, 6, 10)
    strategies = manager.get_all_strategies()
    assert "1_zero_rb.json" in strategies


def test_update_always_increments_total_runs(tmp_path):
    path = tmp_path / "win_rate_meta_data.json"
    manager = WinRateMetaDataManager(path)
    manager.update("1_zero_rb.json", "Zero RB", 0.6, 6, 10)
    manager.update("1_zero_rb.json", "Zero RB", 0.5, 5, 10)
    assert manager.get_all_strategies()["1_zero_rb.json"]["total_runs"] == 2
    manager.update("1_zero_rb.json", "Zero RB", 0.4, 4, 10)
    assert manager.get_all_strategies()["1_zero_rb.json"]["total_runs"] == 3


def test_update_always_sets_last_run(tmp_path):
    path = tmp_path / "win_rate_meta_data.json"
    manager = WinRateMetaDataManager(path)
    manager.update("1_zero_rb.json", "Zero RB", 0.6, 6, 10)
    today = datetime.date.today().isoformat()
    assert manager.get_all_strategies()["1_zero_rb.json"]["last_run"] == today


def test_update_updates_best_win_rate_when_improved(tmp_path):
    path = tmp_path / "win_rate_meta_data.json"
    manager = WinRateMetaDataManager(path)
    manager.update("1_zero_rb.json", "Zero RB", 0.5, 5, 10)
    manager.update("1_zero_rb.json", "Zero RB", 0.7, 7, 10)
    assert manager.get_all_strategies()["1_zero_rb.json"]["best_win_rate"] == 0.7


def test_update_does_not_update_best_win_rate_when_not_improved(tmp_path):
    path = tmp_path / "win_rate_meta_data.json"
    manager = WinRateMetaDataManager(path)
    manager.update("1_zero_rb.json", "Zero RB", 0.7, 7, 10)
    manager.update("1_zero_rb.json", "Zero RB", 0.5, 5, 10)
    assert manager.get_all_strategies()["1_zero_rb.json"]["best_win_rate"] == 0.7
    manager.update("1_zero_rb.json", "Zero RB", 0.7, 7, 10)
    assert manager.get_all_strategies()["1_zero_rb.json"]["best_win_rate"] == 0.7


def test_update_writes_file_atomically(tmp_path):
    path = tmp_path / "win_rate_meta_data.json"
    manager = WinRateMetaDataManager(path)
    manager.update("1_zero_rb.json", "Zero RB", 0.6, 6, 10)
    assert path.exists()
    data = json.loads(path.read_text())
    assert "strategies" in data
    assert not path.with_suffix('.tmp').exists()


def test_update_updates_top_level_last_updated(tmp_path):
    path = tmp_path / "win_rate_meta_data.json"
    manager = WinRateMetaDataManager(path)
    manager.update("1_zero_rb.json", "Zero RB", 0.6, 6, 10)
    today = datetime.date.today().isoformat()
    data = json.loads(path.read_text())
    assert data["last_updated"] == today


def test_get_all_strategies_returns_correct_data(tmp_path):
    path = tmp_path / "win_rate_meta_data.json"
    manager = WinRateMetaDataManager(path)
    manager.update("1_zero_rb.json", "Zero RB", 0.6, 6, 10)
    strategies = manager.get_all_strategies()
    assert "1_zero_rb.json" in strategies
    assert strategies["1_zero_rb.json"]["name"] == "Zero RB"
    assert strategies["1_zero_rb.json"]["best_win_rate"] == 0.6
    assert strategies["1_zero_rb.json"]["total_runs"] == 1
