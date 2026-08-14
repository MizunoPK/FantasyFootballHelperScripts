"""
Unit Tests for repair_bye_week_points.py

Tests the one-time bye-week repair of the fetched player pool: the zeroing
predicate through the utility, serialization preservation, idempotence,
--dry-run, the loud-abort arms, and sandbox containment.

Author: Kai Mizuno
"""

import json
from unittest.mock import MagicMock, patch

import pytest

from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.repair_bye_week_points import main, repair_pool

POSITIONS = ('qb', 'rb', 'wr', 'te', 'k', 'dst')


# FIXTURES

def _record(player_id, bye_week, projected_base=10.0, actual_base=20.0):
    """One 17-slot record with distinct per-week values so a zeroed slot is visible."""
    return {
        "id": player_id,
        "name": f"Player {player_id}",
        "team": "KC",
        "position": "RB",
        "bye_week": bye_week,
        "injury_status": "ACTIVE",
        "drafted_by": "",
        "locked": False,
        "average_draft_position": None,
        "player_rating": None,
        "projected_points": [projected_base + week for week in range(1, 18)],
        "actual_points": [actual_base + week for week in range(1, 18)],
    }


def _write_pool(player_data_dir, records_by_position):
    """Write a six-file pool using the exporter's serialization (no trailing newline)."""
    player_data_dir.mkdir(parents=True, exist_ok=True)
    for position in POSITIONS:
        document = {f"{position}_data": records_by_position.get(position, [])}
        (player_data_dir / f"{position}_data.json").write_text(
            json.dumps(document, indent=2, ensure_ascii=False), encoding='utf-8'
        )


def _snapshot(player_data_dir):
    """Every position file's exact bytes, for byte-level unchanged assertions."""
    return {p.name: p.read_text(encoding='utf-8') for p in sorted(player_data_dir.glob('*.json'))}


def _run_cli(argv):
    """Invoke the utility's CLI entry point with a stubbed logger, as the peer tests do."""
    with patch('repair_bye_week_points.get_logger', return_value=MagicMock()), \
         patch('sys.argv', argv):
        return main()


@pytest.fixture
def pool(tmp_path):
    """A data ROOT whose player_data/ holds one violating rb record and five empty files."""
    player_data_dir = tmp_path / 'player_data'
    _write_pool(player_data_dir, {'rb': [_record(1, 6)]})
    return tmp_path


class TestRepairByeWeekPoints:
    """Tests for repair_bye_week_points.py."""

    def test_in_range_bye_zeroes_both_arrays(self, pool):
        """The bye slot of both arrays is zeroed, and no other slot moves."""
        assert _run_cli(['repair_bye_week_points.py', '--data-root', str(pool)]) == 0

        document = json.loads((pool / 'player_data' / 'rb_data.json').read_text(encoding='utf-8'))
        record = document['rb_data'][0]
        assert record['projected_points'] == [
            0.0 if week == 6 else float(10 + week) for week in range(1, 18)
        ]
        assert record['actual_points'] == [
            0.0 if week == 6 else float(20 + week) for week in range(1, 18)
        ]

    def test_compliant_record_is_left_byte_unchanged(self, tmp_path):
        """A pool that already satisfies the invariant is rewritten byte-for-byte."""
        player_data_dir = tmp_path / 'player_data'
        compliant = _record(2, 6)
        compliant['projected_points'][5] = 0.0
        compliant['actual_points'][5] = 0.0
        _write_pool(player_data_dir, {'rb': [compliant]})
        before = _snapshot(player_data_dir)

        assert _run_cli(['repair_bye_week_points.py', '--data-root', str(tmp_path)]) == 0

        assert _snapshot(player_data_dir) == before

    @pytest.mark.parametrize("bye_week", [None, 0, -1, 18])
    def test_invalid_byes_leave_the_file_untouched(self, tmp_path, bye_week):
        """Falsey and out-of-range byes neither mutate the file nor raise (TD1's guard arms)."""
        player_data_dir = tmp_path / 'player_data'
        _write_pool(player_data_dir, {'rb': [_record(3, bye_week)]})
        before = _snapshot(player_data_dir)

        assert _run_cli(['repair_bye_week_points.py', '--data-root', str(tmp_path)]) == 0

        assert _snapshot(player_data_dir) == before

    def test_only_the_bye_slot_lines_differ(self, pool):
        """The diff is value-only: two changed lines, both '0.0', and no trailing newline."""
        before = (pool / 'player_data' / 'rb_data.json').read_text(encoding='utf-8')

        assert _run_cli(['repair_bye_week_points.py', '--data-root', str(pool)]) == 0

        after = (pool / 'player_data' / 'rb_data.json').read_text(encoding='utf-8')
        before_lines = before.split('\n')
        after_lines = after.split('\n')
        assert len(before_lines) == len(after_lines)
        differing = [i for i, (a, b) in enumerate(zip(before_lines, after_lines)) if a != b]
        assert len(differing) == 2
        assert [after_lines[i].strip().rstrip(',') for i in differing] == ['0.0', '0.0']
        assert not after.endswith('\n')

    def test_second_run_changes_nothing(self, pool):
        """The transform is idempotent: a second run is a byte-level no-op."""
        assert _run_cli(['repair_bye_week_points.py', '--data-root', str(pool)]) == 0
        after_first = _snapshot(pool / 'player_data')

        assert _run_cli(['repair_bye_week_points.py', '--data-root', str(pool)]) == 0

        assert _snapshot(pool / 'player_data') == after_first
        with patch('repair_bye_week_points.get_logger', return_value=MagicMock()):
            assert repair_pool(pool / 'player_data', dry_run=True) == 0

    def test_dry_run_writes_nothing_and_reports_the_real_count(self, pool):
        """--dry-run leaves the pool and the directory untouched and counts what a real run changes."""
        before = _snapshot(pool / 'player_data')

        assert _run_cli(['repair_bye_week_points.py', '--data-root', str(pool), '--dry-run']) == 0

        assert _snapshot(pool / 'player_data') == before
        assert list((pool / 'player_data').glob('*.tmp')) == []
        with patch('repair_bye_week_points.get_logger', return_value=MagicMock()):
            dry_count = repair_pool(pool / 'player_data', dry_run=True)
            real_count = repair_pool(pool / 'player_data', dry_run=False)
        assert dry_count == real_count == 1

    @pytest.mark.parametrize(
        "mutate",
        ["root_key", "missing_array", "short_array", "missing_bye", "non_integer_bye"],
    )
    def test_malformed_input_aborts_loudly_without_writing(self, tmp_path, mutate):
        """A broken assumption is an error that aborts the run, never a silently skipped record."""
        player_data_dir = tmp_path / 'player_data'
        _write_pool(player_data_dir, {'rb': [_record(4, 6)]})
        document = json.loads((player_data_dir / 'rb_data.json').read_text(encoding='utf-8'))
        if mutate == "root_key":
            document = {"players": document['rb_data']}
        elif mutate == "missing_array":
            del document['rb_data'][0]['actual_points']
        elif mutate == "short_array":
            document['rb_data'][0]['projected_points'] = [0.0] * 16
        elif mutate == "non_integer_bye":
            document['rb_data'][0]['bye_week'] = "6"
        else:
            del document['rb_data'][0]['bye_week']
        (player_data_dir / 'rb_data.json').write_text(
            json.dumps(document, indent=2, ensure_ascii=False), encoding='utf-8'
        )
        before = _snapshot(player_data_dir)

        mock_logger = MagicMock()
        with patch('repair_bye_week_points.get_logger', return_value=mock_logger), \
             patch('sys.argv', ['repair_bye_week_points.py', '--data-root', str(tmp_path)]):
            result = main()

        assert result == 1
        assert _snapshot(player_data_dir) == before
        assert mock_logger.error.called

    def test_missing_file_aborts(self, pool):
        """A missing position file aborts rather than silently repairing five of six.

        wr is the third entry of POSITION_CODES, so qb and rb are read before the
        failure is discovered -- the byte-level assertion is what pins that the
        two-phase repair wrote neither of them.
        """
        (pool / 'player_data' / 'wr_data.json').unlink()
        before = _snapshot(pool / 'player_data')

        assert _run_cli(['repair_bye_week_points.py', '--data-root', str(pool)]) == 1

        assert _snapshot(pool / 'player_data') == before
        assert list((pool / 'player_data').glob('*.tmp')) == []

    def test_write_failure_aborts_and_leaves_no_orphan_tmp(self, pool):
        """An OSError during the rewrite aborts with exit 1 and removes the temporary file.

        An orphaned data/player_data/*.tmp would dirty the tree and turn every
        later suite run red through run_all_tests.py's cleanliness backstop.
        """
        with patch('pathlib.Path.replace', side_effect=OSError("disk full")):
            assert _run_cli(['repair_bye_week_points.py', '--data-root', str(pool)]) == 1

        assert list((pool / 'player_data').glob('*.tmp')) == []

    def test_missing_player_data_directory_aborts(self, tmp_path):
        """A data root with no player_data/ subdirectory aborts before touching anything."""
        assert _run_cli(['repair_bye_week_points.py', '--data-root', str(tmp_path)]) == 1

    def test_default_data_root_follows_player_data_dir_env(self, pool, monkeypatch):
        """No --data-root: the default resolves through the PLAYER_DATA_DIR redirect.

        This is what keeps every test write inside the sandbox -- the utility
        never reaches the tracked data/player_data/ tree unless pointed there.
        """
        monkeypatch.setenv('PLAYER_DATA_DIR', str(pool))

        assert _run_cli(['repair_bye_week_points.py']) == 0

        document = json.loads((pool / 'player_data' / 'rb_data.json').read_text(encoding='utf-8'))
        assert document['rb_data'][0]['projected_points'][5] == 0.0
