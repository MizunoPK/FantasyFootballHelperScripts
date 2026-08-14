#!/usr/bin/env python3
"""
Tests for tests/run_all_tests.py's data/ cleanliness backstop (T91, spec D3)

Covers AC8 (the backstop fires on a newly dirtied data/ path), AC9 (it does not
false-red on a path already dirty before the run), and AC10 (it degrades to a
notice when git is unavailable or the runner is outside a work tree).

Every test drives the real runner code against a THROWAWAY git work tree under
tmp_path. No test here ever points the backstop at the real project root, so no
test here can dirty the tracked data/ tree -- which is the defect this whole
story exists to eliminate.

Author: Kai Mizuno
"""

import subprocess
import sys
from pathlib import Path

import pytest

project_root = Path(__file__).parent.parent.parent
if str(project_root / 'tests') not in sys.path:
    sys.path.insert(0, str(project_root / 'tests'))

import FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.tests.run_all_tests as run_all_tests  # noqa: E402


# FIXTURES

@pytest.fixture
def sandbox_repo(tmp_path):
    """A throwaway git work tree with a committed data/ file.

    Returns the repo root. Skips the test when git is unavailable, which is the
    same condition AC10 requires the production code to degrade on.
    """
    repo = tmp_path / 'sandbox_repo'
    (repo / 'data').mkdir(parents=True)
    (repo / 'data' / 'tracked.txt').write_text('baseline\n')

    try:
        subprocess.run(
            ['git', 'init'],
            capture_output=True,
            text=True,
            cwd=str(repo),
            timeout=60
        )
        subprocess.run(
            ['git', 'add', 'data/tracked.txt'],
            capture_output=True,
            text=True,
            cwd=str(repo),
            timeout=60
        )
        subprocess.run(
            ['git', '-c', 'user.email=t91@example.com', '-c', 'user.name=T91',
             'commit', '-m', 'baseline'],
            capture_output=True,
            text=True,
            cwd=str(repo),
            timeout=60
        )
    except OSError:
        pytest.skip('git is not available on this machine')

    status = subprocess.run(
        ['git', 'status', '--porcelain'],
        capture_output=True,
        text=True,
        cwd=str(repo),
        timeout=60
    )
    if status.returncode != 0:
        pytest.skip('git is not usable on this machine')

    return repo


@pytest.fixture
def drive_main(monkeypatch, capsys):
    """Drive run_all_tests.main() with a stubbed runner rooted at a sandbox repo.

    Returns a callable(repo, during_run) -> (exit_code, captured_stdout). The
    stub stands in for the whole test suite: it returns True (every test passed)
    and optionally performs `during_run(repo)` between the backstop's before- and
    after-snapshots. That is the only way to exercise the dirty branch without
    writing a real test that dirties a real data/ tree.
    """
    def _drive(repo, during_run=None):
        class _StubRunner:
            def __init__(self, verbose=False, detailed=False):
                self.project_root = repo

            def run_all_tests(self):
                if during_run is not None:
                    during_run(repo)
                return True

            def run_all_tests_single_command(self):
                return self.run_all_tests()

        monkeypatch.setattr(run_all_tests, 'TestRunner', _StubRunner)
        monkeypatch.setattr(sys, 'argv', ['run_all_tests.py'])

        with pytest.raises(SystemExit) as excinfo:
            run_all_tests.main()

        return excinfo.value.code, capsys.readouterr().out

    return _drive


class TestDataStatusPaths:
    """T91: the _data_status_paths helper (spec D3, AC10)"""

    def test_returns_a_set_of_dirty_paths(self, sandbox_repo):
        """T91-18: an untracked data/ file appears in the returned set"""
        (sandbox_repo / 'data' / 'probe.txt').write_text('probe\n')

        paths = run_all_tests._data_status_paths(sandbox_repo)

        assert isinstance(paths, set)
        assert 'data/probe.txt' in paths

    def test_returns_empty_set_on_a_clean_data_tree(self, sandbox_repo):
        """T91-19: a clean data/ tree yields an empty set, not None"""
        paths = run_all_tests._data_status_paths(sandbox_repo)

        assert paths == set()

    def test_returns_none_outside_a_git_work_tree(self, tmp_path):
        """T91-20 (AC10): a non-work-tree directory degrades to None"""
        outside = tmp_path / 'not_a_repo'
        outside.mkdir()

        assert run_all_tests._data_status_paths(outside) is None

    def test_returns_none_when_git_is_unavailable(self, sandbox_repo, monkeypatch):
        """T91-21 (AC10): a missing git binary degrades to None, never an exception"""
        monkeypatch.setenv('PATH', '/nonexistent')

        assert run_all_tests._data_status_paths(sandbox_repo) is None


class TestBackstopWiring:
    """T91: the backstop as wired into main() (spec D3, AC8/AC9/AC10)"""

    def test_fires_when_the_run_newly_dirties_data(self, sandbox_repo, drive_main):
        """T91-22 (AC8): a run that dirties data/ exits non-zero even though every test passed"""
        def dirty(repo):
            (repo / 'data' / 'written_by_a_test.txt').write_text('oops\n')

        exit_code, out = drive_main(sandbox_repo, during_run=dirty)

        assert exit_code == 1
        assert 'THIS TEST RUN DIRTIED PATHS UNDER data/' in out
        assert 'data/written_by_a_test.txt' in out
        assert 'git checkout -- data/' in out

    def test_names_every_newly_dirtied_path(self, sandbox_repo, drive_main):
        """T91-23 (AC8): each newly dirtied path is reported, not just the first"""
        def dirty(repo):
            (repo / 'data' / 'one.txt').write_text('1\n')
            (repo / 'data' / 'two.txt').write_text('2\n')

        exit_code, out = drive_main(sandbox_repo, during_run=dirty)

        assert exit_code == 1
        assert 'data/one.txt' in out
        assert 'data/two.txt' in out

    def test_exits_zero_on_a_clean_run(self, sandbox_repo, drive_main):
        """T91-24: a passing run that touches nothing exits 0 with no complaint"""
        exit_code, out = drive_main(sandbox_repo)

        assert exit_code == 0
        assert 'THIS TEST RUN DIRTIED' not in out

    def test_does_not_flag_a_path_already_dirty_before_the_run(self, sandbox_repo, drive_main):
        """T91-25 (AC9): a pre-existing dirty path is in the baseline, so it is not a finding.

        This is what makes the check a baseline DIFF rather than a clean-tree
        assertion: a developer with legitimate in-flight data/ edits must not get
        a false red.
        """
        (sandbox_repo / 'data' / 'in_flight.txt').write_text('developer edit\n')

        exit_code, out = drive_main(sandbox_repo)

        assert exit_code == 0
        assert 'NEWLY DIRTIED' not in out

    def test_does_not_flag_a_pre_existing_modified_tracked_file(self, sandbox_repo, drive_main):
        """T91-26 (AC9): the same holds for a MODIFIED tracked file, not just an untracked one"""
        (sandbox_repo / 'data' / 'tracked.txt').write_text('edited before the run\n')

        exit_code, out = drive_main(sandbox_repo)

        assert exit_code == 0
        assert 'NEWLY DIRTIED' not in out

    def test_flags_only_the_new_path_when_a_baseline_dirty_path_exists(self, sandbox_repo, drive_main):
        """T91-27 (AC8+AC9): with both present, only the newly dirtied path is reported"""
        (sandbox_repo / 'data' / 'in_flight.txt').write_text('developer edit\n')

        def dirty(repo):
            (repo / 'data' / 'written_by_a_test.txt').write_text('oops\n')

        exit_code, out = drive_main(sandbox_repo, during_run=dirty)

        assert exit_code == 1
        assert 'data/written_by_a_test.txt' in out
        assert 'data/in_flight.txt' not in out

    def test_degrades_to_a_notice_outside_a_git_work_tree(self, tmp_path, drive_main):
        """T91-28 (AC10): outside a work tree the check is skipped and the tests decide the exit"""
        outside = tmp_path / 'not_a_repo'
        (outside / 'data').mkdir(parents=True)

        exit_code, out = drive_main(outside)

        assert exit_code == 0
        assert 'NOTICE' in out
        assert 'skipping the data/ cleanliness check' in out
        assert 'THIS TEST RUN DIRTIED' not in out

    def test_a_dirty_run_outside_a_work_tree_still_exits_zero(self, tmp_path, drive_main):
        """T91-29 (AC10): infrastructure absence never turns into a red suite"""
        outside = tmp_path / 'not_a_repo'
        (outside / 'data').mkdir(parents=True)

        def dirty(repo):
            (repo / 'data' / 'written_by_a_test.txt').write_text('oops\n')

        exit_code, out = drive_main(outside, during_run=dirty)

        assert exit_code == 0
        assert 'NOTICE' in out
