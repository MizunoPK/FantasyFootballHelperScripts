from unittest.mock import MagicMock

from league_helper.util.PlayerManager import PlayerManager


POSITION_FILES = [
    'qb_data.json', 'rb_data.json', 'wr_data.json',
    'te_data.json', 'k_data.json', 'dst_data.json'
]


def _make_fp_mocks(mtime_map):
    """
    Build per-file Path mocks for the 6 position files.

    Args:
        mtime_map (dict): Maps position filename to float mtime.
            All 6 position files must be present as keys.

    Returns:
        tuple: (fp_mocks, last_mtimes)
            fp_mocks: dict mapping position filename -> MagicMock Path
            last_mtimes: dict mapping str(filepath) -> mtime (for _last_mtimes seed)
    """
    fp_mocks = {}
    last_mtimes = {}
    for pf in POSITION_FILES:
        fp = MagicMock()
        fp.exists.return_value = True
        fp_str = f"/data/player_data/{pf}"
        fp.__str__ = MagicMock(return_value=fp_str)
        stat_result = MagicMock()
        stat_result.st_mtime = mtime_map[pf]
        fp.stat.return_value = stat_result
        fp_mocks[pf] = fp
        last_mtimes[fp_str] = mtime_map[pf]
    return fp_mocks, last_mtimes


def _make_manager(fp_mocks, last_mtimes):
    """
    Create a PlayerManager bypassing __init__ with controlled state.

    Args:
        fp_mocks (dict): Maps position filename -> MagicMock Path (from _make_fp_mocks).
        last_mtimes (dict): Pre-seeded _last_mtimes dict. Pass {} for first-call test.

    Returns:
        PlayerManager: Configured manager with all dependencies mocked.
    """
    manager = PlayerManager.__new__(PlayerManager)
    manager.logger = MagicMock()
    manager.team = MagicMock()
    manager.team.roster = []
    manager.load_players_from_json = MagicMock(return_value=True)
    manager.load_team = MagicMock()
    manager._last_mtimes = last_mtimes

    fake_player_data_dir = MagicMock()
    fake_player_data_dir.__truediv__ = lambda self, pf: fp_mocks.get(pf, MagicMock())

    manager.data_folder = MagicMock()
    manager.data_folder.__truediv__ = (
        lambda self, other: fake_player_data_dir if other == 'player_data' else MagicMock()
    )
    return manager


class TestReloadPlayerDataMtimeOptimization:
    """Unit tests for mtime-based reload optimization in reload_player_data()."""

    def test_skip_reload_when_files_unchanged(self):
        """R4: reload_player_data() does NOT call load_players_from_json() when all mtimes match."""
        fixed_mtime = 1700000000.0
        mtime_map = {pf: fixed_mtime for pf in POSITION_FILES}
        fp_mocks, last_mtimes = _make_fp_mocks(mtime_map)
        manager = _make_manager(fp_mocks, last_mtimes)

        manager.reload_player_data()

        manager.load_players_from_json.assert_not_called()

    def test_reload_triggered_when_file_changes(self):
        """R5: reload_player_data() calls load_players_from_json() when any file has a newer mtime."""
        old_mtime = 1700000000.0
        new_mtime = 1700000001.0
        mtime_map = {pf: old_mtime for pf in POSITION_FILES}
        fp_mocks, last_mtimes = _make_fp_mocks(mtime_map)

        stat_result_new = MagicMock()
        stat_result_new.st_mtime = new_mtime
        fp_mocks[POSITION_FILES[0]].stat.return_value = stat_result_new

        manager = _make_manager(fp_mocks, last_mtimes)

        manager.reload_player_data()

        manager.load_players_from_json.assert_called_once()

    def test_first_call_always_reloads(self):
        """R6: reload_player_data() calls load_players_from_json() when _last_mtimes is empty."""
        mtime_map = {pf: 1700000000.0 for pf in POSITION_FILES}
        fp_mocks, _ = _make_fp_mocks(mtime_map)
        manager = _make_manager(fp_mocks, last_mtimes={})

        manager.reload_player_data()

        manager.load_players_from_json.assert_called_once()

    def test_mtimes_recorded_after_reload(self):
        """R3: After a successful reload, _last_mtimes contains current mtime for all position files."""
        fixed_mtime = 1700000000.0
        mtime_map = {pf: fixed_mtime for pf in POSITION_FILES}
        fp_mocks, _ = _make_fp_mocks(mtime_map)
        manager = _make_manager(fp_mocks, last_mtimes={})

        manager.reload_player_data()

        for pf in POSITION_FILES:
            expected_key = f"/data/player_data/{pf}"
            assert expected_key in manager._last_mtimes
            assert manager._last_mtimes[expected_key] == fixed_mtime
