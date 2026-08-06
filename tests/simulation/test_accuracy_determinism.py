"""
Determinism regression tests for the accuracy simulation: candidate-config
generation (T51) AND per-config evaluation (D2 / TD4).

Covers spec D1-D4 (generation):
- Default (no explicit seed) generation is identical across repeated in-process
  calls and across differing PYTHONHASHSEED values.
- --seed reproducibility: the same explicit seed reproduces the candidate array;
  a different seed produces a different array.
- The private per-generator RNG (ConfigGenerator._rng) drives candidate draws;
  the process-global `random` module is NOT consumed on the generation path.
- The seed is threaded CLI -> AccuracySimulationManager -> ConfigGenerator, and
  the accuracy runner exposes a --seed CLI flag.

Also covers D2 ticket.md Success Criterion 1 / context.md TD4 (evaluation):
- Evaluating one fixed config twice via the real production evaluation entry
  point returns byte-identical pairwise_accuracy on every horizon, establishing
  the fixed-config noise floor at exactly 0. See
  TestAccuracyEvaluationDeterminism below for detail.

Author: Kai Mizuno
Date: 2026
"""

import json
import os
import random
import subprocess
import sys
from pathlib import Path

from simulation.shared.ConfigGenerator import ConfigGenerator, DEFAULT_ACCURACY_SEED
from simulation.accuracy.AccuracySimulationManager import AccuracySimulationManager
from simulation.accuracy.ParallelAccuracyRunner import _evaluate_config_tournament_process
from simulation.accuracy.horizon_labels import WEEK_RANGES

# Repo root: tests/simulation/test_accuracy_determinism.py -> parents[2].
REPO_ROOT = Path(__file__).resolve().parents[2]

# Committed real data used by the manager-threading test (construction only, fast).
DATA_FOLDER = REPO_ROOT / "simulation" / "sim_data"
BASELINE_CONFIGS = REPO_ROOT / "data" / "configs"

# Week-specific param, precision 0 (random.randint path); returns the 4-horizon shape.
HORIZON_PARAM = "NORMALIZATION_MAX_SCALE"

# Subprocess body: print the candidate array behind a RESULT: sentinel so the parent
# can isolate it from ConfigGenerator's timestamped INFO log lines (which go to stdout).
_SUBPROCESS_SCRIPT = (
    "import sys\n"
    "from pathlib import Path\n"
    "from simulation.shared.ConfigGenerator import ConfigGenerator\n"
    "vals = ConfigGenerator(Path(sys.argv[1]), num_test_values=2)"
    ".generate_horizon_test_values('NORMALIZATION_MAX_SCALE')\n"
    "print('RESULT:' + repr(vals))\n"
)


def _create_6_file_config_folder(tmp_path: Path) -> Path:
    """Create the 6-file baseline config structure ConfigGenerator expects.

    Reproduced from TestHorizonBasedInterface.create_6_file_config_folder in
    tests/simulation/test_config_generator.py (as a module-level helper shared
    by both test classes, not an instance method) so the two suites build
    identical fixtures.
    """
    config_folder = tmp_path / "test_configs"
    config_folder.mkdir()

    base_config = {
        "config_name": "Test Config",
        "parameters": {
            "CURRENT_NFL_WEEK": 10,
            "NFL_SEASON": 2025,
            "ADP_SCORING": {"WEIGHT": 1.5, "STEPS": 10},
            "NORMALIZATION_MAX_SCALE": 100
        }
    }

    week_config_template = {
        "config_name": "Test Week Config",
        "parameters": {
            "PLAYER_RATING_SCORING": {"WEIGHT": 2.0},
            "TEAM_QUALITY_SCORING": {"WEIGHT": 1.5, "MIN_WEEKS": 4}
        }
    }

    (config_folder / "league_config.json").write_text(json.dumps(base_config, indent=2))
    (config_folder / "week1-5.json").write_text(json.dumps({**week_config_template, "config_name": "Week 1-5"}, indent=2))
    (config_folder / "week6-9.json").write_text(json.dumps({**week_config_template, "config_name": "Week 6-9"}, indent=2))
    (config_folder / "week10-13.json").write_text(json.dumps({**week_config_template, "config_name": "Week 10-13"}, indent=2))
    (config_folder / "week14-17.json").write_text(json.dumps({**week_config_template, "config_name": "Week 14-17"}, indent=2))

    return config_folder


def _candidate_array_via_subprocess(config_folder: Path, hashseed) -> str:
    """Return the repr of the default-seed candidate array from a fresh subprocess.

    `hashseed` is the PYTHONHASHSEED value (int) or None to unset it. The subprocess
    prints a RESULT:-prefixed line so this helper isolates the array from
    ConfigGenerator's timestamped INFO log output on stdout.
    """
    env = dict(os.environ)
    if hashseed is None:
        env.pop("PYTHONHASHSEED", None)
    else:
        env["PYTHONHASHSEED"] = str(hashseed)

    proc = subprocess.run(
        [sys.executable, "-c", _SUBPROCESS_SCRIPT, str(config_folder)],
        cwd=str(REPO_ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert proc.returncode == 0, (
        f"subprocess exited {proc.returncode}\nSTDERR:\n{proc.stderr}\nSTDOUT:\n{proc.stdout}"
    )
    result_lines = [ln for ln in proc.stdout.splitlines() if ln.startswith("RESULT:")]
    assert len(result_lines) == 1, (
        f"expected exactly one RESULT line, got {result_lines!r}; full stdout:\n{proc.stdout}"
    )
    return result_lines[0][len("RESULT:"):]


class TestAccuracyGenerationDeterminism:
    """Candidate generation is reproducible run-to-run (ConfigGenerator level)."""

    def test_default_generation_identical_across_repeated_calls(self, tmp_path):
        """With no explicit seed, two default generators produce identical arrays."""
        config_folder = _create_6_file_config_folder(tmp_path)

        first = ConfigGenerator(config_folder, num_test_values=2).generate_horizon_test_values(HORIZON_PARAM)
        second = ConfigGenerator(config_folder, num_test_values=2).generate_horizon_test_values(HORIZON_PARAM)

        assert first == second

    def test_default_generation_identical_across_pythonhashseed(self, tmp_path):
        """Default generation is identical across PYTHONHASHSEED=0, =1, and unset."""
        config_folder = _create_6_file_config_folder(tmp_path)

        result_hashseed_0 = _candidate_array_via_subprocess(config_folder, 0)
        result_hashseed_1 = _candidate_array_via_subprocess(config_folder, 1)
        result_hashseed_unset = _candidate_array_via_subprocess(config_folder, None)

        assert result_hashseed_0 == result_hashseed_1 == result_hashseed_unset

    def test_same_seed_reproduces_candidate_array(self, tmp_path):
        """Two generators built with the same explicit seed produce equal arrays."""
        config_folder = _create_6_file_config_folder(tmp_path)

        first = ConfigGenerator(config_folder, num_test_values=2, seed=7).generate_horizon_test_values(HORIZON_PARAM)
        second = ConfigGenerator(config_folder, num_test_values=2, seed=7).generate_horizon_test_values(HORIZON_PARAM)

        assert first == second

    def test_different_seed_yields_different_candidate_array(self, tmp_path):
        """Different explicit seeds produce different candidate arrays."""
        config_folder = _create_6_file_config_folder(tmp_path)

        seed_seven = ConfigGenerator(config_folder, num_test_values=2, seed=7).generate_horizon_test_values(HORIZON_PARAM)
        seed_nine = ConfigGenerator(config_folder, num_test_values=2, seed=9).generate_horizon_test_values(HORIZON_PARAM)

        assert seed_seven != seed_nine

    def test_generation_uses_private_rng_not_global_random(self, tmp_path):
        """Candidate draws come from ConfigGenerator._rng, not the module-global random.

        Re-seeding the process-global random.seed() must NOT change output, and two
        generators built with the same explicit seed must match regardless of the
        global RNG state at construction/generation time.
        """
        config_folder = _create_6_file_config_folder(tmp_path)

        generator = ConfigGenerator(config_folder, num_test_values=2, seed=7)
        assert isinstance(generator._rng, random.Random)

        random.seed(111)
        baseline = ConfigGenerator(config_folder, num_test_values=2, seed=7).generate_horizon_test_values(HORIZON_PARAM)
        random.seed(999)
        after_global_reseed = ConfigGenerator(config_folder, num_test_values=2, seed=7).generate_horizon_test_values(HORIZON_PARAM)

        assert baseline == after_global_reseed


class TestAccuracySeedThreading:
    """The seed is threaded CLI -> manager -> generator, and the CLI exposes --seed."""

    def test_default_seed_constant_is_42(self):
        """The documented default accuracy seed constant is 42."""
        assert DEFAULT_ACCURACY_SEED == 42

    def test_manager_threads_seed_into_config_generator(self, tmp_path):
        """AccuracySimulationManager(seed=N) forwards N to its ConfigGenerator's RNG."""
        manager_seed7_a = AccuracySimulationManager(
            baseline_config_path=BASELINE_CONFIGS,
            output_dir=tmp_path / "out_a",
            data_folder=DATA_FOLDER,
            parameter_order=[HORIZON_PARAM],
            num_test_values=2,
            seed=7,
        )
        manager_seed7_b = AccuracySimulationManager(
            baseline_config_path=BASELINE_CONFIGS,
            output_dir=tmp_path / "out_b",
            data_folder=DATA_FOLDER,
            parameter_order=[HORIZON_PARAM],
            num_test_values=2,
            seed=7,
        )
        manager_seed9 = AccuracySimulationManager(
            baseline_config_path=BASELINE_CONFIGS,
            output_dir=tmp_path / "out_c",
            data_folder=DATA_FOLDER,
            parameter_order=[HORIZON_PARAM],
            num_test_values=2,
            seed=9,
        )

        values_seed7_a = manager_seed7_a.config_generator.generate_horizon_test_values(HORIZON_PARAM)
        values_seed7_b = manager_seed7_b.config_generator.generate_horizon_test_values(HORIZON_PARAM)
        values_seed9 = manager_seed9.config_generator.generate_horizon_test_values(HORIZON_PARAM)

        assert values_seed7_a == values_seed7_b
        assert values_seed7_a != values_seed9

    def test_cli_exposes_seed_flag(self):
        """`run_accuracy_simulation.py --help` advertises the --seed flag."""
        proc = subprocess.run(
            [sys.executable, "run_accuracy_simulation.py", "--help"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert proc.returncode == 0, f"--help exited {proc.returncode}\n{proc.stderr}"
        assert "--seed" in proc.stdout


class TestAccuracyEvaluationDeterminism:
    """Per-config evaluation is deterministic: no randomness in `simulation/accuracy/`.

    Complements `TestAccuracyGenerationDeterminism` above, which covers candidate
    GENERATION; this class covers EVALUATION (D2 ticket.md Success Criterion 1 /
    context.md TD4) -- converting the two in-code claims (the
    AccuracySimulationManager docstring in
    simulation/accuracy/AccuracySimulationManager.py; the T69/D2-tagged comment in
    AccuracyResultsManager.is_better_than) plus D11's one-off empirical observation
    into a committed, always-checked guard. Establishes that the fixed-config noise
    floor every D2.2/D2.3 dispersion figure is measured against is exactly 0.

    MUTATION CHECK (CODING_STANDARDS.md "Test Discrimination", performed once at
    implementation time, then reverted -- see the plan's Step 2 verification):
    AccuracyCalculator.calculate_pairwise_accuracy's `accuracy = correct / total`
    line was temporarily changed to introduce a per-call random jitter, and this
    test was confirmed to FAIL against the perturbed calculator; the perturbation
    was then reverted via `git checkout --` and this test re-confirmed to PASS.
    This test is not a tautology.
    """

    def test_fixed_config_evaluates_identically_twice(self, tmp_path):
        """Evaluating one fixed config dict twice, in-process, against the real
        committed corpus (simulation/sim_data + data/configs) via the real
        production evaluation entry point (_evaluate_config_tournament_process)
        returns byte-identical pairwise_accuracy on every WEEK_RANGES horizon."""
        assert DATA_FOLDER.is_dir(), (
            f"committed sim_data corpus not present at {DATA_FOLDER} -- this guard "
            "asserts rather than skips (unlike the pytest.skip convention at "
            "tests/simulation/shared/test_sim_data_coverage.py:98 and "
            "tests/simulation/test_ParallelAccuracyRunner.py:214) because this unit's "
            "entire purpose (D2 ticket.md Success Criterion 1 / TD4) is a determinism "
            "guard that must not pass vacuously by being skipped; restore the "
            "committed corpus rather than skip this test"
        )
        manager = AccuracySimulationManager(
            baseline_config_path=BASELINE_CONFIGS,
            output_dir=tmp_path / "out",
            data_folder=DATA_FOLDER,
            parameter_order=[HORIZON_PARAM],
            num_test_values=2,
        )
        config_dict = manager.config_generator.baseline_configs['1-5']

        _, first_results = _evaluate_config_tournament_process(
            config_dict, DATA_FOLDER, manager.available_seasons
        )
        _, second_results = _evaluate_config_tournament_process(
            config_dict, DATA_FOLDER, manager.available_seasons
        )

        for week_key in WEEK_RANGES:
            first_metrics = first_results[week_key].overall_metrics
            second_metrics = second_results[week_key].overall_metrics
            assert first_metrics is not None and second_metrics is not None, (
                f"{week_key}: overall_metrics unexpectedly None "
                f"(first={first_metrics!r}, second={second_metrics!r})"
            )
            first_pairwise = first_metrics.pairwise_accuracy
            second_pairwise = second_metrics.pairwise_accuracy
            assert first_pairwise is not None and second_pairwise is not None, (
                f"{week_key}: pairwise_accuracy unexpectedly None "
                f"(first={first_pairwise!r}, second={second_pairwise!r})"
            )
            assert first_pairwise == second_pairwise, (
                f"{week_key}: {first_pairwise!r} != {second_pairwise!r}"
            )
