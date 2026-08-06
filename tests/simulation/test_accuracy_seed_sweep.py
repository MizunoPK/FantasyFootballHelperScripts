"""
Unit tests for the accuracy seed-sweep harness (run_accuracy_seed_sweep.py).

Covers D2.3's own §Requirements / §Test Strategy coverage list (spec.md):
1. No prior seed folders -> the subprocess is invoked once per seed, in order,
   with --baseline, --seed, and a per-seed --output.
2. A completed seed folder (promoted week*.json config files +
   candidate_results.json present) is skipped -- no subprocess invocation for
   that seed.
3. A completed-but-partial folder (promoted config files only, no
   candidate_results.json -- a crash between config-writing and promotion) is
   NOT treated as complete -- the seed is re-invoked.
4. A non-zero subprocess exit code halts the sweep before the next seed's
   subprocess is invoked.
5. The raw-sample JSON is emitted with the expected shape once all seeds have
   either completed or the sweep has halted.
6. --promote and --compare are never present in any constructed subprocess
   command line, across every case above.
7. collect_seed_result reports the PROMOTED per-horizon pairwise_accuracy
   (read from the promoted config files), not max(pairwise_accuracy) over
   candidate_results.json -- promotion is not a pure argmax (is_better_than
   applies a per-season consistency gate first), so the two can and do
   differ on a real run.

Corrected 2026-08-06 (D2.3 /du3-build, found by the unit's own one-seed smoke
run): find_completed_run and collect_seed_result no longer key on
metadata.json -- it is written to the INTERMEDIATE folder
(AccuracyResultsManager.py:1007) and deleted by
cleanup_accuracy_intermediate_folders on every successful run, so it can never
be present in an accuracy_optimal_* folder. The fixtures below instead write
the four promoted per-horizon config files (week1-5.json, week6-9.json,
week10-13.json, week14-17.json) carrying
performance_metrics.ranking_metrics.pairwise_accuracy, matching what
AccuracyResultsManager.save_optimal_configs() actually writes there.

No test in this file invokes the real ~40-minute accuracy engine -- every
subprocess boundary is mocked (CODING_STANDARDS.md "Test Discrimination";
spec.md "The harness has its own automated tests ... that do NOT invoke the
real ... accuracy engine").

Author: Kai Mizuno
"""

import argparse
import json
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

import run_accuracy_seed_sweep as sweep


def _write_promoted_configs(folder: Path, pairwise_accuracy_by_horizon=None):
    """Write minimal-but-well-formed promoted per-horizon config files
    (week1-5.json, week6-9.json, week10-13.json, week14-17.json) into folder,
    matching the shape AccuracyResultsManager.save_optimal_configs() writes:
    performance_metrics.ranking_metrics.pairwise_accuracy per file.

    pairwise_accuracy_by_horizon: optional dict of horizon key
    (sweep.CONFIG_FILE_TO_HORIZON values) -> pairwise_accuracy value; defaults
    to 0.6 for every horizon.
    """
    if pairwise_accuracy_by_horizon is None:
        pairwise_accuracy_by_horizon = {
            h: 0.6 for h in sweep.CONFIG_FILE_TO_HORIZON.values()
        }
    for filename, horizon in sweep.CONFIG_FILE_TO_HORIZON.items():
        config = {
            'config_name': f"Accuracy Optimal {filename.replace('.json', '')}",
            'description': 'test fixture',
            'parameters': {},
            'performance_metrics': {
                'mae': 0.5,
                'ranking_metrics': {
                    'pairwise_accuracy': pairwise_accuracy_by_horizon[horizon],
                },
            },
        }
        with open(folder / filename, 'w', encoding='utf-8') as f:
            json.dump(config, f)


def _write_candidate_results(folder: Path):
    """Write a minimal-but-well-formed candidate_results.json into folder."""
    records = [
        {
            'horizon': 'week_1_5', 'pass_idx': 0, 'param_name': 'NORMALIZATION_MAX_SCALE',
            'test_idx': 0, 'base_horizon': 'week_1_5', 'config_value': 1.0,
            'pairwise_accuracy': 0.6, 'per_season_pairwise': {}, 'adopted': True,
            'incumbent_pairwise': None,
        },
    ]
    with open(folder / sweep.DUMP_PROMOTED_FILENAME, 'w', encoding='utf-8') as f:
        json.dump(records, f)


def _make_completed_folder(seed_output: Path, timestamp: str, with_candidate_results: bool = True,
                            pairwise_accuracy_by_horizon=None) -> Path:
    """Create a completed (or partial, if with_candidate_results=False)
    accuracy_optimal_* folder under seed_output and return its path.
    """
    folder = seed_output / f"accuracy_optimal_{timestamp}"
    folder.mkdir(parents=True)
    _write_promoted_configs(folder, pairwise_accuracy_by_horizon)
    if with_candidate_results:
        _write_candidate_results(folder)
    return folder


def _mock_subprocess_run_creating_folder(timestamp: str = "2026-08-06_00-00-00"):
    """Return a MagicMock for subprocess.run whose side_effect creates a
    completed accuracy_optimal_* folder under the --output path each call
    receives, and returns a Mock with returncode=0 -- simulating a
    successful run_accuracy_simulation.py invocation without running it.
    """
    def _side_effect(cmd, *args, **kwargs):
        output_idx = cmd.index('--output') + 1
        seed_output = Path(cmd[output_idx])
        _make_completed_folder(seed_output, timestamp)
        result = MagicMock()
        result.returncode = 0
        return result

    return MagicMock(side_effect=_side_effect)


class TestParseSeeds:
    """parse_seeds: the --seeds value parser."""

    def test_single_seed(self):
        assert sweep.parse_seeds("42") == [42]

    def test_multiple_seeds_in_order(self):
        assert sweep.parse_seeds("42,1,7,13,99") == [42, 1, 7, 13, 99]

    def test_whitespace_tolerant(self):
        assert sweep.parse_seeds(" 42 , 1 ") == [42, 1]

    def test_empty_raises(self):
        """Asserts the SPECIFIC exception type parse_seeds documents/raises,
        not a bare Exception -- du5-review SUGGESTION + Copilot finding
        (test_accuracy_seed_sweep.py:141). A bare pytest.raises(Exception)
        cannot fail for any exception at all: main() (line ~227) catches
        exactly argparse.ArgumentTypeError to print 'error: ...' and return
        1, so a regression to a bare ValueError would leave this test green
        while main() crashed with an uncaught traceback instead of exiting 1
        cleanly.
        """
        with pytest.raises(argparse.ArgumentTypeError):
            sweep.parse_seeds("")

    def test_non_integer_raises(self):
        """Same discrimination fix as test_empty_raises above -- Copilot
        finding also named line 143 (this test)."""
        with pytest.raises(argparse.ArgumentTypeError):
            sweep.parse_seeds("42,abc")


class TestFindCompletedRun:
    """find_completed_run: the D1 completion-detection predicate."""

    def test_no_seed_output_directory(self, tmp_path):
        assert sweep.find_completed_run(tmp_path / "does_not_exist") is None

    def test_empty_seed_output_directory(self, tmp_path):
        seed_output = tmp_path / "seed_42"
        seed_output.mkdir()
        assert sweep.find_completed_run(seed_output) is None

    def test_complete_folder_is_found(self, tmp_path):
        seed_output = tmp_path / "seed_42"
        folder = _make_completed_folder(seed_output, "2026-08-06_00-00-00")
        assert sweep.find_completed_run(seed_output) == folder

    def test_partial_folder_configs_only_is_not_complete(self, tmp_path):
        """Coverage item 3: the four promoted config files are present but
        candidate_results.json is absent (e.g. a crash between
        save_optimal_configs and _promote_candidate_dump) -- must NOT be
        treated as complete.

        Mutation check (verified live, see report): if find_completed_run's
        `(folder / DUMP_PROMOTED_FILENAME).exists()` check is replaced with
        an always-true predicate, this assertion flips to a completed folder
        being returned and this test fails.
        """
        seed_output = tmp_path / "seed_42"
        _make_completed_folder(seed_output, "2026-08-06_00-00-00", with_candidate_results=False)
        assert sweep.find_completed_run(seed_output) is None

    def test_most_recent_complete_folder_is_returned(self, tmp_path):
        seed_output = tmp_path / "seed_42"
        _make_completed_folder(seed_output, "2026-08-01_00-00-00")
        newest = _make_completed_folder(seed_output, "2026-08-06_00-00-00")
        assert sweep.find_completed_run(seed_output) == newest


class TestRunSeed:
    """run_seed: the per-seed subprocess invocation."""

    def test_constructs_expected_command_line(self, tmp_path):
        """Coverage items 1 and 6: --baseline, --seed, --output, --data are all
        present with the right values; --promote / --compare never appear.
        """
        mock_run = _mock_subprocess_run_creating_folder()
        seed_output = tmp_path / "seed_42"
        with patch.object(sweep.subprocess, 'run', mock_run):
            sweep.run_seed(42, Path('data/configs'), seed_output, Path('simulation/sim_data'))

        cmd = mock_run.call_args[0][0]
        assert '--seed' in cmd and cmd[cmd.index('--seed') + 1] == '42'
        assert '--baseline' in cmd and cmd[cmd.index('--baseline') + 1] == 'data/configs'
        assert '--output' in cmd and cmd[cmd.index('--output') + 1] == str(seed_output)
        assert '--data' in cmd and cmd[cmd.index('--data') + 1] == 'simulation/sim_data'
        assert '--promote' not in cmd
        assert '--compare' not in cmd

    def test_invokes_repo_root_anchored_script_path(self, tmp_path):
        """CONCERN 3 / Copilot finding (run_accuracy_seed_sweep.py:123): the
        simulation script is invoked by an ABSOLUTE path derived from
        __file__ (REPO_ROOT), not the bare relative
        'run_accuracy_simulation.py' -- which only worked when the process
        CWD happened to be the repo root. Matches the in-repo convention at
        run_pre_commit_validation.py:30 (Path(__file__).parent) and this same
        ticket's sibling tests/simulation/test_accuracy_determinism.py:112
        (cwd=REPO_ROOT).
        """
        mock_run = _mock_subprocess_run_creating_folder()
        seed_output = tmp_path / "seed_42"
        with patch.object(sweep.subprocess, 'run', mock_run):
            sweep.run_seed(42, Path('data/configs'), seed_output, Path('simulation/sim_data'))

        cmd = mock_run.call_args[0][0]
        assert cmd[1] == str(sweep.REPO_ROOT / 'run_accuracy_simulation.py')
        assert Path(cmd[1]).is_absolute()

    def test_passes_subprocess_timeout(self, tmp_path):
        """NITPICK: subprocess.run must be called with a timeout so a hung
        ascent fails loudly and diagnosably instead of hanging the sweep
        indefinitely."""
        mock_run = _mock_subprocess_run_creating_folder()
        seed_output = tmp_path / "seed_42"
        with patch.object(sweep.subprocess, 'run', mock_run):
            sweep.run_seed(42, Path('data/configs'), seed_output, Path('simulation/sim_data'))

        assert mock_run.call_args.kwargs.get('timeout') == sweep.SUBPROCESS_TIMEOUT_SECONDS

    def test_timeout_expired_raises_system_exit_naming_seed(self, tmp_path):
        seed_output = tmp_path / "seed_42"
        mock_run = MagicMock(
            side_effect=subprocess.TimeoutExpired(cmd='run_accuracy_simulation.py', timeout=1)
        )
        with patch.object(sweep.subprocess, 'run', mock_run):
            with pytest.raises(SystemExit, match='seed 42'):
                sweep.run_seed(42, Path('data/configs'), seed_output, Path('simulation/sim_data'))

    def test_returns_completed_folder_on_success(self, tmp_path):
        mock_run = _mock_subprocess_run_creating_folder("2026-08-06_00-00-00")
        seed_output = tmp_path / "seed_42"
        with patch.object(sweep.subprocess, 'run', mock_run):
            completed = sweep.run_seed(42, Path('data/configs'), seed_output, Path('simulation/sim_data'))
        assert completed == seed_output / "accuracy_optimal_2026-08-06_00-00-00"

    def test_nonzero_exit_code_raises(self, tmp_path):
        """Coverage item 4 (first half): a non-zero exit from THIS seed's
        subprocess raises rather than returning a folder.

        The mocked subprocess DOES create a completed folder despite
        returning returncode=1 -- an adversarial fixture, deliberately, so
        this test isolates the returncode guard specifically. Without it, a
        removed returncode check would still raise via the separate
        "no completed folder" fallback in run_seed, and this test would pass
        either way (not discriminating) -- verified by mutation-testing both
        guards independently at plan-authoring time.

        Mutation check: if run_seed's `if result.returncode != 0: raise ...`
        guard is removed, this test fails, because the completed folder this
        fixture creates makes find_completed_run succeed and run_seed return
        normally instead of raising.
        """
        seed_output = tmp_path / "seed_42"

        def _side_effect(cmd, *args, **kwargs):
            _make_completed_folder(seed_output, "2026-08-06_00-00-00")
            result = MagicMock()
            result.returncode = 1
            return result

        mock_run = MagicMock(side_effect=_side_effect)
        with patch.object(sweep.subprocess, 'run', mock_run):
            with pytest.raises(SystemExit):
                sweep.run_seed(42, Path('data/configs'), seed_output, Path('simulation/sim_data'))

    def test_zero_exit_but_no_completed_folder_raises(self, tmp_path):
        """A zero exit that produced no completed folder is a harness-side
        integrity failure, not silently treated as success.
        """
        mock_run = MagicMock(return_value=MagicMock(returncode=0))
        seed_output = tmp_path / "seed_42"
        with patch.object(sweep.subprocess, 'run', mock_run):
            with pytest.raises(SystemExit):
                sweep.run_seed(42, Path('data/configs'), seed_output, Path('simulation/sim_data'))


class TestCollectSeedResult:
    """collect_seed_result: builds one seed's raw-sample-JSON entry."""

    def test_expected_shape(self, tmp_path):
        seed_output = tmp_path / "seed_42"
        folder = _make_completed_folder(seed_output, "2026-08-06_00-00-00")

        entry = sweep.collect_seed_result(42, folder)

        assert entry['seed'] == 42
        assert entry['output_folder'] == str(folder)
        assert entry['candidate_results_path'] == str(folder / sweep.DUMP_PROMOTED_FILENAME)
        per_horizon = entry['per_horizon_promoted_pairwise_accuracy']
        assert set(per_horizon.keys()) == {'week_1_5', 'week_6_9', 'week_10_13', 'week_14_17'}
        assert all(v == 0.6 for v in per_horizon.values())
        assert entry['candidate_summary']['total_candidates'] == 1

    def test_missing_config_file_fails_fast(self, tmp_path):
        """CONCERN 1 path (a): a promoted per-horizon config file is missing
        even though the folder was detected as complete -- must raise
        SystemExit naming the seed/horizon/folder rather than silently
        recording a null. Prior behaviour (before du5-review CONCERN 1)
        recorded None here with no missing-file signal.
        """
        seed_output = tmp_path / "seed_42"
        folder = seed_output / "accuracy_optimal_2026-08-06_00-00-00"
        folder.mkdir(parents=True)
        _write_promoted_configs(folder)
        _write_candidate_results(folder)
        (folder / 'week6-9.json').unlink()

        with pytest.raises(SystemExit, match='week6-9.json'):
            sweep.collect_seed_result(42, folder)

    def test_no_results_shape_fails_fast(self, tmp_path):
        """CONCERN 1 path (b) -- the reachable, non-corruption one: a
        promoted config file EXISTS but carries the
        AccuracyResultsManager.save_optimal_configs 'No results' branch
        shape (performance_metrics.mae=None, no ranking_metrics key at all,
        AccuracyResultsManager.py:702-731). Must raise SystemExit rather than
        `.get('pairwise_accuracy')` silently returning None with no
        missing-file signal -- this is the path Copilot's line-180 finding
        named and du5-review's CONCERN 1 escalated as the more dangerous of
        the two, since the folder is genuinely 'complete' by
        find_completed_run's predicate.
        """
        seed_output = tmp_path / "seed_42"
        folder = seed_output / "accuracy_optimal_2026-08-06_00-00-00"
        folder.mkdir(parents=True)
        _write_promoted_configs(folder)
        _write_candidate_results(folder)
        no_results_config = {
            'config_name': 'Accuracy Optimal week6-9',
            'description': 'test fixture: no-results shape',
            'parameters': {},
            'performance_metrics': {'mae': None, 'note': 'no results for this horizon'},
        }
        with open(folder / 'week6-9.json', 'w', encoding='utf-8') as f:
            json.dump(no_results_config, f)

        with pytest.raises(SystemExit, match='ranking_metrics'):
            sweep.collect_seed_result(42, folder)

    def test_reports_promoted_value_not_argmax_of_candidates(self, tmp_path):
        """Pins the load-bearing not-argmax property: promotion is not a pure
        argmax of pairwise_accuracy (is_better_than applies a per-season
        consistency gate first), so collect_seed_result must report the value
        from the PROMOTED config file, not max(pairwise_accuracy) over
        candidate_results.json's records.

        Real evidence from the D2.3 seed-42 smoke run: week_1_5 promoted
        0.610131089536813 vs max candidate 0.6102297496625587 -- the promoted
        value is LOWER than the max candidate. A fixture where they coincide
        would not catch a regression to argmax; this fixture deliberately
        makes them differ, with the max candidate on a horizon/record the
        promoted config does NOT carry.
        """
        seed_output = tmp_path / "seed_42"
        folder = seed_output / "accuracy_optimal_2026-08-06_00-00-00"
        folder.mkdir(parents=True)

        promoted_week_1_5 = 0.610131089536813
        max_candidate_week_1_5 = 0.6102297496625587
        _write_promoted_configs(folder, {
            'week_1_5': promoted_week_1_5,
            'week_6_9': 0.6,
            'week_10_13': 0.6,
            'week_14_17': 0.6,
        })
        # candidate_results.json holds a HIGHER value than the promoted
        # config for week_1_5 -- an argmax-based reader would wrongly report
        # this value instead of the promoted one.
        records = [
            {
                'horizon': 'week_1_5', 'pass_idx': 0, 'param_name': 'NORMALIZATION_MAX_SCALE',
                'test_idx': 0, 'base_horizon': 'week_1_5', 'config_value': 1.0,
                'pairwise_accuracy': max_candidate_week_1_5, 'per_season_pairwise': {},
                'adopted': False, 'incumbent_pairwise': promoted_week_1_5,
            },
        ]
        with open(folder / sweep.DUMP_PROMOTED_FILENAME, 'w', encoding='utf-8') as f:
            json.dump(records, f)

        entry = sweep.collect_seed_result(42, folder)

        assert entry['per_horizon_promoted_pairwise_accuracy']['week_1_5'] == promoted_week_1_5
        assert entry['per_horizon_promoted_pairwise_accuracy']['week_1_5'] != max_candidate_week_1_5


class TestMainSweep:
    """main(): the end-to-end sweep loop, scratch root patched to tmp_path."""

    def test_no_prior_folders_invokes_subprocess_once_per_seed_in_order(self, tmp_path, monkeypatch):
        """Coverage item 1: fresh scratch root -> one subprocess call per seed,
        in the order given.
        """
        monkeypatch.setattr(sweep, 'SCRATCH_ROOT', tmp_path)
        mock_run = _mock_subprocess_run_creating_folder()
        monkeypatch.setattr(sweep.sys, 'argv', ['run_accuracy_seed_sweep.py', '--seeds', '42,1,7'])

        with patch.object(sweep.subprocess, 'run', mock_run):
            exit_code = sweep.main()

        assert exit_code == 0
        assert mock_run.call_count == 3
        invoked_seeds = []
        for call in mock_run.call_args_list:
            cmd = call[0][0]
            invoked_seeds.append(cmd[cmd.index('--seed') + 1])
        assert invoked_seeds == ['42', '1', '7']

    def test_completed_seed_is_skipped(self, tmp_path, monkeypatch):
        """Coverage item 2: seed 42 already has a completed folder -> its
        subprocess is never invoked; seed 1 (no prior folder) still runs.

        Mutation check: if main()'s `if completed is not None: ... continue`
        skip branch is removed (always falling through to run_seed), this
        test fails because mock_run.call_count becomes 2, not 1, and the
        skipped seed's args appear in call_args_list.
        """
        monkeypatch.setattr(sweep, 'SCRATCH_ROOT', tmp_path)
        _make_completed_folder(tmp_path / "seed_42", "2026-08-01_00-00-00")
        mock_run = _mock_subprocess_run_creating_folder()
        monkeypatch.setattr(sweep.sys, 'argv', ['run_accuracy_seed_sweep.py', '--seeds', '42,1'])

        with patch.object(sweep.subprocess, 'run', mock_run):
            exit_code = sweep.main()

        assert exit_code == 0
        assert mock_run.call_count == 1
        cmd = mock_run.call_args[0][0]
        assert cmd[cmd.index('--seed') + 1] == '1'

    def test_partial_folder_is_not_skipped(self, tmp_path, monkeypatch):
        """Coverage item 3, at the main()-loop level: a completed-but-partial
        folder for seed 42 does not prevent its subprocess from being invoked.
        """
        monkeypatch.setattr(sweep, 'SCRATCH_ROOT', tmp_path)
        _make_completed_folder(tmp_path / "seed_42", "2026-08-01_00-00-00", with_candidate_results=False)
        mock_run = _mock_subprocess_run_creating_folder()
        monkeypatch.setattr(sweep.sys, 'argv', ['run_accuracy_seed_sweep.py', '--seeds', '42'])

        with patch.object(sweep.subprocess, 'run', mock_run):
            exit_code = sweep.main()

        assert exit_code == 0
        assert mock_run.call_count == 1

    def test_nonzero_exit_halts_before_next_seed(self, tmp_path, monkeypatch, capsys):
        """Coverage item 4 (second half): seed 42's subprocess fails ->
        seed 1's subprocess is never invoked.

        Also covers coverage item 5's "or the sweep has halted" half
        (du5-review CONCERN 2 / gap-hunt finding): the halt must still emit
        the raw-sample JSON -- with a halt marker so it can never be
        mistaken for a complete file -- carrying zero results, since seed 42
        (the only seed attempted) never completed. Before this test asserted
        only the call log, the suite stayed green while spec.md's stated
        "emitted even when the sweep halts" behaviour was unimplemented; this
        is the fix for that discrimination gap.
        """
        monkeypatch.setattr(sweep, 'SCRATCH_ROOT', tmp_path)

        call_log = []

        def _side_effect(cmd, *args, **kwargs):
            call_log.append(cmd)
            result = MagicMock()
            result.returncode = 1
            return result

        mock_run = MagicMock(side_effect=_side_effect)
        monkeypatch.setattr(sweep.sys, 'argv', ['run_accuracy_seed_sweep.py', '--seeds', '42,1'])

        with patch.object(sweep.subprocess, 'run', mock_run):
            with pytest.raises(SystemExit):
                sweep.main()

        assert len(call_log) == 1
        assert call_log[0][call_log[0].index('--seed') + 1] == '42'

        raw_sample_path = tmp_path / sweep.RAW_SAMPLE_FILENAME
        assert raw_sample_path.exists()
        with open(raw_sample_path, 'r', encoding='utf-8') as f:
            raw_sample = json.load(f)
        assert raw_sample['results'] == []
        assert raw_sample['halted_after_seed'] == 42
        assert 'halt_reason' in raw_sample and raw_sample['halt_reason']

        stderr = capsys.readouterr().err
        assert 'PARTIAL' in stderr
        assert 'seed 42' in stderr

    def test_halt_after_one_completed_seed_preserves_it_in_partial_json(self, tmp_path, monkeypatch):
        """A sweep that completes seed 42 and then fails on seed 1 must not
        discard seed 42's already-collected result from the partial JSON --
        only the summary is at risk on a halt, not prior seeds' ascent work
        (per-seed scratch folders always survive; this pins the JSON side).
        """
        monkeypatch.setattr(sweep, 'SCRATCH_ROOT', tmp_path)

        def _side_effect(cmd, *args, **kwargs):
            seed = cmd[cmd.index('--seed') + 1]
            result = MagicMock()
            if seed == '42':
                output_idx = cmd.index('--output') + 1
                _make_completed_folder(Path(cmd[output_idx]), "2026-08-06_00-00-00")
                result.returncode = 0
            else:
                result.returncode = 1
            return result

        mock_run = MagicMock(side_effect=_side_effect)
        monkeypatch.setattr(sweep.sys, 'argv', ['run_accuracy_seed_sweep.py', '--seeds', '42,1'])

        with patch.object(sweep.subprocess, 'run', mock_run):
            with pytest.raises(SystemExit):
                sweep.main()

        raw_sample_path = tmp_path / sweep.RAW_SAMPLE_FILENAME
        with open(raw_sample_path, 'r', encoding='utf-8') as f:
            raw_sample = json.load(f)
        assert raw_sample['halted_after_seed'] == 1
        assert len(raw_sample['results']) == 1
        assert raw_sample['results'][0]['seed'] == 42

    def test_seeds_parse_error_exits_1_with_message(self, capsys):
        """main()'s error path (SUGGESTION: the currently-unused capsys
        parameter's real home) -- a --seeds parse failure returns 1 and
        prints 'error: ...' to stderr, rather than propagating an uncaught
        exception."""
        with patch.object(
            sweep.sys, 'argv', ['run_accuracy_seed_sweep.py', '--seeds', 'abc'],
        ):
            exit_code = sweep.main()

        assert exit_code == 1
        stderr = capsys.readouterr().err
        assert 'error:' in stderr

    def test_raw_sample_json_shape(self, tmp_path, monkeypatch):
        """Coverage item 5: the raw-sample JSON has the expected top-level
        shape and one entry per completed seed.
        """
        monkeypatch.setattr(sweep, 'SCRATCH_ROOT', tmp_path)
        mock_run = _mock_subprocess_run_creating_folder()
        monkeypatch.setattr(sweep.sys, 'argv', ['run_accuracy_seed_sweep.py', '--seeds', '42,1'])

        with patch.object(sweep.subprocess, 'run', mock_run):
            exit_code = sweep.main()

        assert exit_code == 0
        raw_sample_path = tmp_path / sweep.RAW_SAMPLE_FILENAME
        assert raw_sample_path.exists()
        with open(raw_sample_path, 'r', encoding='utf-8') as f:
            raw_sample = json.load(f)

        assert raw_sample['seeds'] == [42, 1]
        assert raw_sample['baseline'] == sweep.DEFAULT_BASELINE
        assert raw_sample['data'] == sweep.DEFAULT_DATA
        assert len(raw_sample['results']) == 2
        assert {r['seed'] for r in raw_sample['results']} == {42, 1}
        for r in raw_sample['results']:
            assert set(r['per_horizon_promoted_pairwise_accuracy'].keys()) == {
                'week_1_5', 'week_6_9', 'week_10_13', 'week_14_17',
            }


class TestSummarizeCandidates:
    """summarize_candidates: the committed tie/spread/gate analysis
    (du5-review SUGGESTION "commit the tie/spread/gate analysis" -- folds
    the ad-hoc query the follow-up ticket would otherwise have to
    reconstruct from the verdict document's prose into code).

    Fixture pins the four predicates against a hand-built, mixed-horizon
    candidate set so each is exercised independently.
    """

    @staticmethod
    def _write_candidates(path: Path, records):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(records, f)

    def test_predicates_on_hand_built_fixture(self, tmp_path):
        path = tmp_path / 'candidate_results.json'
        records = [
            # week_1_5: first-ever candidate (incumbent_pairwise None) -- not comparable.
            {'horizon': 'week_1_5', 'base_horizon': 'week_1_5', 'pairwise_accuracy': 0.60,
             'incumbent_pairwise': None, 'adopted': True},
            # week_1_5: exact tie (comparable).
            {'horizon': 'week_1_5', 'base_horizon': 'week_1_5', 'pairwise_accuracy': 0.60,
             'incumbent_pairwise': 0.60, 'adopted': False},
            # week_1_5: gate rejection -- higher mean but not adopted (comparable).
            {'horizon': 'week_1_5', 'base_horizon': 'week_6_9', 'pairwise_accuracy': 0.65,
             'incumbent_pairwise': 0.60, 'adopted': False},
            # week_6_9: ordinary improvement, adopted (comparable, not a tie, not a rejection).
            {'horizon': 'week_6_9', 'base_horizon': 'week_1_5', 'pairwise_accuracy': 0.70,
             'incumbent_pairwise': 0.55, 'adopted': True},
        ]
        self._write_candidates(path, records)

        summary = sweep.summarize_candidates(path)

        assert summary['total_candidates'] == 4
        assert summary['comparable_candidates'] == 3
        assert summary['exact_ties'] == 1
        assert summary['gate_rejections'] == 1

        week_1_5 = summary['per_horizon_spread']['week_1_5']
        assert week_1_5['n'] == 3
        assert week_1_5['min'] == 0.60
        assert week_1_5['max'] == 0.65
        assert week_1_5['spread'] == pytest.approx(0.05)

        week_6_9 = summary['per_horizon_spread']['week_6_9']
        assert week_6_9['n'] == 1
        assert week_6_9['min'] == week_6_9['max'] == 0.70
        assert week_6_9['spread'] == 0.0

    def test_groups_by_horizon_not_base_horizon(self, tmp_path):
        """horizon (the range being optimized) is the grouping key, not
        base_horizon (the tournament-mode provenance of the candidate
        config) -- the two differ on real records and grouping by the wrong
        one would silently collapse or split populations."""
        path = tmp_path / 'candidate_results.json'
        records = [
            {'horizon': 'week_1_5', 'base_horizon': 'week_14_17', 'pairwise_accuracy': 0.5,
             'incumbent_pairwise': None, 'adopted': True},
            {'horizon': 'week_1_5', 'base_horizon': 'week_10_13', 'pairwise_accuracy': 0.5,
             'incumbent_pairwise': None, 'adopted': True},
        ]
        self._write_candidates(path, records)

        summary = sweep.summarize_candidates(path)

        assert set(summary['per_horizon_spread'].keys()) == {'week_1_5'}
        assert summary['per_horizon_spread']['week_1_5']['n'] == 2
