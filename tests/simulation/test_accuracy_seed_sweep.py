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

import json
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
        with pytest.raises(Exception):
            sweep.parse_seeds("")

    def test_non_integer_raises(self):
        with pytest.raises(Exception):
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
