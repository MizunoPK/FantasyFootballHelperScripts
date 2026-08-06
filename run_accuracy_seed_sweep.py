"""
Accuracy Seed Sweep Harness

Sweeps run_accuracy_simulation.py across N seeds, each a full ascent against a
PINNED baseline, into a per-seed scratch --output. Orchestrates the existing
CLI entry point as a subprocess -- it does not import AccuracySimulationManager
and does not re-implement the ascent, the evaluation, or the selection rule
(context.md TD5). Never passes --promote or --compare.

Each seed's output goes to its OWN scratch subdirectory (context.md Key Design
Decision D1) so that (a) MAX_OPTIMAL_FOLDERS=5 retention on one seed's folder
can never cross-delete a different seed's result, and (b) "has this seed
finished" is answerable by scanning one small directory. Before invoking a
seed's subprocess, the harness checks for an already-completed run in that
seed's output directory and skips it if found (D1's find_completed_run) --
this is what makes re-invoking the sweep after an interruption safe rather
than silently re-doing a finished seed's ~40-minute ascent from scratch.

A non-zero subprocess exit code halts the sweep immediately -- it does not
silently continue to the next seed, because a broken seed's numbers must not
be silently absent from a downstream verdict without the reader knowing why.

Usage:
    python run_accuracy_seed_sweep.py --seeds 42
    python run_accuracy_seed_sweep.py --seeds 42,1,7,13,99

Author: Kai Mizuno
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional

from simulation.accuracy.AccuracyResultsManager import DUMP_PROMOTED_FILENAME

# Anchored at the repo root via __file__ (not ambient CWD), matching the
# established in-repo convention for a subprocess-invoking runner:
# run_pre_commit_validation.py:30 (`Path(__file__).parent`) and this same
# ticket's sibling tests/simulation/test_accuracy_determinism.py:112
# (`cwd=REPO_ROOT`). An unanchored CWD-relative harness would fail loudly if
# invoked from elsewhere -- except SCRATCH_ROOT, which would instead fail
# silently by writing its scratch tree into whatever directory launched it.
REPO_ROOT = Path(__file__).resolve().parent

# DEFAULT_BASELINE deliberately diverges from run_accuracy_simulation.py's own
# default (`''`, meaning "resolve most-recent accuracy_optimal_*") -- this
# harness's whole measurement depends on a PINNED baseline (TD3/TD4 of
# spec.md), not the most-recent-run default. This is a required divergence,
# not a duplication to reconcile.
DEFAULT_BASELINE = str(REPO_ROOT / 'data/configs')
# DEFAULT_DATA duplicates run_accuracy_simulation.py:65's own DEFAULT_DATA as
# a literal rather than importing it -- importing that module at load time
# would pull in AccuracySimulationManager's full engine import chain for a
# lightweight sweep harness. run_accuracy_simulation.py:65 is the source of
# truth; keep this literal in sync with it.
DEFAULT_DATA = str(REPO_ROOT / 'simulation/sim_data')
SCRATCH_ROOT = REPO_ROOT / '_internal/data/accuracy_seed_sweep_D2'
RAW_SAMPLE_FILENAME = 'seed_sweep_results.json'
# Deliberately a DISTINCT name from RAW_SAMPLE_FILENAME (du5-review CONCERN 2,
# 2026-08-06 re-review): a halted sweep must never truncate a prior
# successful sweep's summary. seed_sweep_results.json is the sole,
# git-ignored, no-VCS-history machine-readable record behind every published
# figure in docs/simulation/ACCURACY_SIM_NOISE_FLOOR_D2.md -- writing a halt
# to the SAME path in 'w' mode would silently destroy it the next time a
# different seed is swept and fails partway. A separate filename means a
# partial file can never overwrite a complete one, at the cost of the
# operator having to notice+merge the two after a halt -- an explicit,
# visible step rather than a silent loss.
RAW_SAMPLE_PARTIAL_FILENAME = 'seed_sweep_results.partial.json'


def parse_seeds(raw: str) -> List[int]:
    """Parse a comma-separated --seeds value into a list of ints, in order,
    duplicates preserved (a duplicate seed simply re-uses / re-completes the
    same scratch subdirectory on its second occurrence).

    NOTE: duplicates are preserved deliberately, so raw_sample['seeds'] (and
    len(raw_sample['results'])) is the INVOCATION list, not a distinct-sample
    count -- `--seeds 42,42` produces two identical entries. A downstream
    N-counting consumer must dedupe 'seeds' itself if it wants a distinct
    sample count.

    Raises:
        argparse.ArgumentTypeError: if raw is empty after stripping, or any
            comma-separated part is not a valid int.
    """
    parts = [p.strip() for p in raw.split(',')]
    parts = [p for p in parts if p]
    if not parts:
        raise argparse.ArgumentTypeError(
            f"--seeds value produced no valid seed values after splitting: '{raw}'"
        )
    seeds = []
    for p in parts:
        try:
            seeds.append(int(p))
        except ValueError:
            raise argparse.ArgumentTypeError(f"--seeds value '{p}' is not a valid integer")
    return seeds


def find_completed_run(seed_output: Path) -> Optional[Path]:
    """Return the most recent COMPLETED accuracy_optimal_* folder under
    seed_output, or None if no completed folder exists.

    A folder counts as complete when it holds the promoted candidate-results
    file (DUMP_PROMOTED_FILENAME). That file is written LAST -- by
    _promote_candidate_dump(), after every per-horizon config file -- so its
    presence means the run reached the end, and a run that crashed before
    promotion leaves the folder without it and is NOT complete (context.md
    TD2a). This is what makes the harness's own completion check stricter
    than "the folder exists."

    Corrected 2026-08-06 (D2.3 /du3-build, found by the unit's own one-seed
    smoke run): this predicate previously ALSO required metadata.json in the
    accuracy_optimal_* folder, which made it permanently unsatisfiable.
    metadata.json is written to the INTERMEDIATE folder
    (AccuracyResultsManager.py:1007, `intermediate_folder / "metadata.json"`),
    never to the optimal folder -- and cleanup_accuracy_intermediate_folders
    deletes every intermediate folder on a SUCCESSFUL run, so metadata.json
    cannot survive one. The "beside metadata.json" phrasing inherited from
    TD2/TD2a describes the artifact's role, not a literal sibling file in this
    folder; do not restore the metadata.json clause on the strength of it.
    """
    if not seed_output.exists():
        return None
    candidate_folders = sorted(
        (p for p in seed_output.iterdir() if p.is_dir() and p.name.startswith('accuracy_optimal_')),
        key=lambda p: p.name,
        reverse=True,
    )
    for folder in candidate_folders:
        if (folder / DUMP_PROMOTED_FILENAME).exists():
            return folder
    return None


# A generous ceiling -- observed ascents run ~40-67 min (docs/simulation/
# ACCURACY_SIM_NOISE_FLOOR_D2.md), so this exists only to turn an indefinite
# hang into a diagnosable failure, not to bound normal runtime.
SUBPROCESS_TIMEOUT_SECONDS = 6 * 60 * 60


def run_seed(seed: int, baseline: Path, seed_output: Path, data: Path) -> Path:
    """Invoke run_accuracy_simulation.py as a subprocess for one seed.

    Never passes --promote or --compare. Returns the completed
    accuracy_optimal_* folder path on success.

    Raises:
        SystemExit: on a non-zero subprocess exit code, on a subprocess that
            exceeds SUBPROCESS_TIMEOUT_SECONDS, or on a zero exit code that
            nonetheless produced no completed folder (a harness-side
            integrity check, not expected in normal operation).
    """
    cmd = [
        sys.executable,
        str(REPO_ROOT / 'run_accuracy_simulation.py'),
        '--seed', str(seed),
        '--baseline', str(baseline),
        '--output', str(seed_output),
        '--data', str(data),
    ]
    print(f"seed {seed}: invoking: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, timeout=SUBPROCESS_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        raise SystemExit(
            f"seed {seed}: run_accuracy_simulation.py exceeded the "
            f"{SUBPROCESS_TIMEOUT_SECONDS}s timeout -- halting sweep "
            f"(not continuing to remaining seeds)"
        )
    if result.returncode != 0:
        raise SystemExit(
            f"seed {seed}: run_accuracy_simulation.py exited {result.returncode} -- "
            f"halting sweep (not continuing to remaining seeds)"
        )
    completed = find_completed_run(seed_output)
    if completed is None:
        raise SystemExit(
            f"seed {seed}: subprocess exited 0 but no completed accuracy_optimal_* "
            f"folder (containing {DUMP_PROMOTED_FILENAME}) was found under {seed_output}"
        )
    return completed


# Promoted per-horizon config filename -> WEEK_RANGES horizon key.
# The hyphenated filename form names the CONFIG FILES; the underscored form is the
# horizon key every consumer (and D2.2's dump) uses. ticket.md calls this out
# explicitly -- do not conflate them.
CONFIG_FILE_TO_HORIZON = {
    'week1-5.json': 'week_1_5',
    'week6-9.json': 'week_6_9',
    'week10-13.json': 'week_10_13',
    'week14-17.json': 'week_14_17',
}


def collect_seed_result(seed: int, optimal_folder: Path) -> Dict:
    """Build this seed's entry for the raw-sample JSON from its completed
    accuracy_optimal_* folder: the promoted pairwise_accuracy per horizon
    (from the four promoted per-horizon config files) plus the folder paths a
    consumer needs to load the full per-candidate distribution
    (candidate_results.json, D2.2's artifact).

    Corrected 2026-08-06 (D2.3 /du3-build, found by the unit's own one-seed
    smoke run): this previously read metadata.json from the optimal folder,
    which does not exist there -- metadata.json is written to the INTERMEDIATE
    folder (AccuracyResultsManager.py:1007) and every intermediate folder is
    deleted on a successful run. The promoted per-horizon accuracy is instead
    read from the promoted config files themselves, which carry it at
    performance_metrics.ranking_metrics.pairwise_accuracy.

    It is read from the promoted CONFIG files rather than derived from
    candidate_results.json deliberately: promotion is NOT a pure argmax of
    pairwise_accuracy (is_better_than applies a per-season consistency gate
    first), so the maximum candidate value is not in general the promoted
    value. On the seed-42 smoke run they differ -- week_1_5 promoted
    0.6101310 vs max candidate 0.6102297. Taking the max would silently
    report a config that was never promoted.

    Raises:
        SystemExit: on either integrity violation below, matching run_seed's
            own "subprocess said success but the artifact is not there"
            fail-fast posture (du5-review CONCERN 1) rather than silently
            recording a null:
            (a) a promoted per-horizon config file is missing even though
                find_completed_run declared this folder complete;
            (b) a promoted per-horizon config file EXISTS but carries no
                performance_metrics.ranking_metrics -- the shape written by
                EITHER of two reachable AccuracyResultsManager.
                save_optimal_configs branches (widened 2026-08-06 re-review
                NITPICK: the prior docstring named only the first):
                - the "No results" branch (:702-731), when a horizon was
                  never optimized (baseline parameters +
                  performance_metrics.mae=None, no ranking_metrics key at
                  all); or
                - the `if perf.overall_metrics:` branch (:681), when a
                  horizon DID produce results but overall_metrics itself is
                  falsy -- writes performance_metrics carrying mae but no
                  ranking_metrics key, a different branch producing the same
                  shape.
                (:702-731's own inner else -- "Baseline file NOT found" --
                is a THIRD reachable producer, but of clause (a) above, not
                (b): it logs a warning and writes no file at all, so it never
                reaches this function's ranking_metrics check.)
                This is the reachable, non-corruption path: `.get(
                'pairwise_accuracy')` on either (b) shape would otherwise
                return None with no missing-file signal, indistinguishable
                from a genuine measurement.
    """
    per_horizon_promoted_pairwise_accuracy = {}
    for filename, horizon in CONFIG_FILE_TO_HORIZON.items():
        config_path = optimal_folder / filename
        if not config_path.exists():
            raise SystemExit(
                f"seed {seed}: {optimal_folder} was detected as complete but is "
                f"missing {filename} -- refusing to record a null promoted accuracy "
                f"for {horizon}"
            )
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        ranking_metrics = (
            (config.get('performance_metrics') or {}).get('ranking_metrics') or {}
        )
        if 'pairwise_accuracy' not in ranking_metrics:
            raise SystemExit(
                f"seed {seed}: {config_path} carries no "
                f"performance_metrics.ranking_metrics.pairwise_accuracy -- this "
                f"horizon was not optimized (save_optimal_configs' no-results branch "
                f"writes baseline params with no ranking_metrics); refusing to record "
                f"it as a measurement"
            )
        per_horizon_promoted_pairwise_accuracy[horizon] = ranking_metrics['pairwise_accuracy']

    candidate_results_path = optimal_folder / DUMP_PROMOTED_FILENAME
    return {
        'seed': seed,
        'output_folder': str(optimal_folder),
        'per_horizon_promoted_pairwise_accuracy': per_horizon_promoted_pairwise_accuracy,
        'candidate_results_path': str(candidate_results_path),
        'candidate_summary': summarize_candidates(candidate_results_path),
    }


def summarize_candidates(candidate_results_path: Path) -> Dict:
    """Compute the between-candidate spread (per horizon), exact-tie rate and
    per-season-gate-rejection rate from a completed seed's
    candidate_results.json (D2.2's per-candidate dump).

    Committed here rather than left as an ad-hoc query reconstructed from
    prose each time (du5-review SUGGESTION "commit the tie/spread/gate
    analysis") -- the follow-up five-seed ticket inherits these exact
    predicates instead of re-deriving them from the verdict document's prose
    across five seeds, where any drift in how the population is keyed would
    silently produce a different number.

    Predicates (independently re-derived during du5-review; reproduce the
    document's published seed-42 figures exactly -- 7744 total, 7740
    comparable, 515 exact ties, 16 gate rejections):
      - "comparable" candidate: incumbent_pairwise is not None (i.e. not the
        first-ever candidate evaluated for its horizon).
      - exact tie: comparable AND pairwise_accuracy == incumbent_pairwise.
      - gate rejection: comparable AND pairwise_accuracy > incumbent_pairwise
        AND not adopted (a higher-mean challenger the per-season consistency
        gate rejected).
      - between-candidate spread, per horizon: min/max/spread of
        pairwise_accuracy over EVERY candidate evaluated for that horizon
        (not only the comparable subset) -- CODING_STANDARDS.md
        "Measurement and Comparison Conventions" min/max/spread convention.
        `horizon` (the range being optimized) is the grouping key, not
        `base_horizon` (the tournament-mode provenance of the candidate
        config) -- the two differ on every record.
    """
    with open(candidate_results_path, 'r', encoding='utf-8') as f:
        records = json.load(f)

    total = len(records)
    comparable = [r for r in records if r.get('incumbent_pairwise') is not None]
    exact_ties = sum(
        1 for r in comparable if r['pairwise_accuracy'] == r['incumbent_pairwise']
    )
    gate_rejections = sum(
        1 for r in comparable
        if r['pairwise_accuracy'] > r['incumbent_pairwise'] and not r.get('adopted')
    )

    per_horizon_spread: Dict[str, Dict] = {}
    for horizon in sorted({r['horizon'] for r in records}):
        values = [r['pairwise_accuracy'] for r in records if r['horizon'] == horizon]
        per_horizon_spread[horizon] = {
            'n': len(values),
            'min': min(values),
            'max': max(values),
            'spread': max(values) - min(values),
        }

    return {
        'total_candidates': total,
        'comparable_candidates': len(comparable),
        'exact_ties': exact_ties,
        'gate_rejections': gate_rejections,
        'per_horizon_spread': per_horizon_spread,
    }


def main() -> int:
    """Returns 1 on a --seeds parse error; raises SystemExit (propagated,
    not returned) from run_seed / collect_seed_result on a failed or
    integrity-violating seed, after emitting a partial raw-sample JSON.
    """
    parser = argparse.ArgumentParser(
        description=(
            'Sweep run_accuracy_simulation.py across N seeds against a pinned baseline, '
            'each into its own scratch --output, and emit the raw-sample JSON.'
        )
    )
    parser.add_argument(
        '--seeds',
        type=str,
        required=True,
        help='Comma-separated seed values, e.g. "42" or "42,1,7,13,99". At least one required.',
    )
    parser.add_argument(
        '--baseline',
        type=str,
        default=DEFAULT_BASELINE,
        help=f'Path to the pinned baseline config folder (default: {DEFAULT_BASELINE})',
    )
    parser.add_argument(
        '--data',
        type=str,
        default=DEFAULT_DATA,
        help=f'Path to the sim_data evaluation corpus (default: {DEFAULT_DATA})',
    )
    args = parser.parse_args()

    try:
        seeds = parse_seeds(args.seeds)
    except argparse.ArgumentTypeError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    baseline = Path(args.baseline)
    data = Path(args.data)

    raw_sample_path = SCRATCH_ROOT / RAW_SAMPLE_FILENAME
    partial_raw_sample_path = SCRATCH_ROOT / RAW_SAMPLE_PARTIAL_FILENAME
    seed_results = []
    for seed in seeds:
        seed_output = SCRATCH_ROOT / f"seed_{seed}"
        try:
            completed = find_completed_run(seed_output)
            if completed is not None:
                print(f"seed {seed}: already complete at {completed} -- skipping")
            else:
                completed = run_seed(seed, baseline, seed_output, data)
            seed_results.append(collect_seed_result(seed, completed))
        except SystemExit as e:
            # Halt: still emit the raw-sample JSON with whatever prior seeds
            # completed, so a sweep that dies partway through does not
            # silently discard the seeds that DID finish (spec.md:176,
            # :343-344 -- "after all seeds attempted (or halted early)").
            # The halt marker makes a partial file impossible to mistake for
            # a complete one (du5-review CONCERN 2). Written to a DISTINCT
            # path (RAW_SAMPLE_PARTIAL_FILENAME, not RAW_SAMPLE_FILENAME) so a
            # halted invocation can never truncate a prior complete sweep's
            # summary (du5-review re-review CONCERN 1, 2026-08-06).
            _write_raw_sample(
                partial_raw_sample_path, seeds, baseline, data, seed_results,
                halt_info={'halted_after_seed': seed, 'halt_reason': str(e)},
            )
            print(
                f"\nWrote PARTIAL raw-sample JSON ({len(seed_results)} of "
                f"{len(seeds)} seeds; halted at seed {seed}) to "
                f"{partial_raw_sample_path} (NOT {raw_sample_path} -- the "
                "complete-run file, if any, is left untouched)",
                file=sys.stderr,
            )
            raise

    _write_raw_sample(raw_sample_path, seeds, baseline, data, seed_results)
    print(f"\nWrote raw-sample JSON to {raw_sample_path}")
    return 0


def _write_raw_sample(
    raw_sample_path: Path,
    seeds: List[int],
    baseline: Path,
    data: Path,
    seed_results: List[Dict],
    halt_info: Optional[Dict] = None,
) -> None:
    """Write the raw-sample JSON to raw_sample_path. When halt_info is given
    (a halted sweep), the emitted file carries 'halted_after_seed' /
    'halt_reason' so a reader can never mistake a partial file for a
    complete one.

    Creates raw_sample_path's own PARENT directory, not the module-global
    SCRATCH_ROOT (du5-review re-review SUGGESTION 3, 2026-08-06): the two
    happen to agree at both call sites today (both derive raw_sample_path
    from SCRATCH_ROOT), but deriving mkdir from the parameter rather than the
    global means this helper's behaviour is fully determined by its argument
    -- a future caller (or a test patching the path but not the global) gets
    a directory that actually matches where the file is written, not a stray
    SCRATCH_ROOT side effect plus a FileNotFoundError from open().
    """
    raw_sample_path.parent.mkdir(parents=True, exist_ok=True)
    raw_sample = {
        'seeds': seeds,
        'baseline': str(baseline),
        'data': str(data),
        'results': seed_results,
    }
    if halt_info is not None:
        raw_sample.update(halt_info)
    with open(raw_sample_path, 'w', encoding='utf-8') as f:
        json.dump(raw_sample, f, indent=2)


if __name__ == '__main__':
    sys.exit(main())
