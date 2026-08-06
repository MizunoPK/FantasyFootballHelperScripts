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

DEFAULT_BASELINE = 'data/configs'
DEFAULT_DATA = 'simulation/sim_data'
SCRATCH_ROOT = Path('_internal/data/accuracy_seed_sweep_D2')
RAW_SAMPLE_FILENAME = 'seed_sweep_results.json'


def parse_seeds(raw: str) -> List[int]:
    """Parse a comma-separated --seeds value into a list of ints, in order,
    duplicates preserved (a duplicate seed simply re-uses / re-completes the
    same scratch subdirectory on its second occurrence).

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


def run_seed(seed: int, baseline: Path, seed_output: Path, data: Path) -> Path:
    """Invoke run_accuracy_simulation.py as a subprocess for one seed.

    Never passes --promote or --compare. Returns the completed
    accuracy_optimal_* folder path on success.

    Raises:
        SystemExit: on a non-zero subprocess exit code, or on a zero exit
            code that nonetheless produced no completed folder (a harness-
            side integrity check, not expected in normal operation).
    """
    cmd = [
        sys.executable,
        'run_accuracy_simulation.py',
        '--seed', str(seed),
        '--baseline', str(baseline),
        '--output', str(seed_output),
        '--data', str(data),
    ]
    print(f"seed {seed}: invoking: {' '.join(cmd)}")
    result = subprocess.run(cmd)
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
    """
    per_horizon_promoted_pairwise_accuracy = {}
    for filename, horizon in CONFIG_FILE_TO_HORIZON.items():
        config_path = optimal_folder / filename
        if not config_path.exists():
            per_horizon_promoted_pairwise_accuracy[horizon] = None
            continue
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        ranking_metrics = (
            (config.get('performance_metrics') or {}).get('ranking_metrics') or {}
        )
        per_horizon_promoted_pairwise_accuracy[horizon] = ranking_metrics.get(
            'pairwise_accuracy'
        )

    return {
        'seed': seed,
        'output_folder': str(optimal_folder),
        'per_horizon_promoted_pairwise_accuracy': per_horizon_promoted_pairwise_accuracy,
        'candidate_results_path': str(optimal_folder / DUMP_PROMOTED_FILENAME),
    }


def main() -> int:
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

    seed_results = []
    for seed in seeds:
        seed_output = SCRATCH_ROOT / f"seed_{seed}"
        completed = find_completed_run(seed_output)
        if completed is not None:
            print(f"seed {seed}: already complete at {completed} -- skipping")
        else:
            completed = run_seed(seed, baseline, seed_output, data)
        seed_results.append(collect_seed_result(seed, completed))

    SCRATCH_ROOT.mkdir(parents=True, exist_ok=True)
    raw_sample_path = SCRATCH_ROOT / RAW_SAMPLE_FILENAME
    raw_sample = {
        'seeds': seeds,
        'baseline': str(baseline),
        'data': str(data),
        'results': seed_results,
    }
    with open(raw_sample_path, 'w', encoding='utf-8') as f:
        json.dump(raw_sample, f, indent=2)

    print(f"\nWrote raw-sample JSON to {raw_sample_path}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
