"""
Unit and integration tests for ParallelLeagueRunner deterministic seeding (T29).

Covers:
(b) thread-count invariance: workers=1 vs workers=4, same seed -> identical sorted results.
    This is the direct proof that the thread + global-random crux is solved (D1).
(d) config-independence: different configs, same base_seed -> same per-(season,sim_id)
    task seeds (the T30-enabling property, D2).
Task-seed derivation:
    _derive_task_seed produces deterministic, config-independent seeds.
    Seeds differ per sim_id.
    Seed=None passes None to SimulatedLeague (entropy default, D3).
CLI plumbing:
    ParallelLeagueRunner(seed=N) stores self.seed; passes task_seeds to worker methods.

(b) thread-count-invariance uses real committed data (simulation/sim_data/2025/) with a
small num_simulations=2 to keep the test fast. All other tests use mocked SimulatedLeague.

Author: Kai Mizuno
"""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from league_helper.util.ConfigManager import ConfigManager
from simulation.win_rate.ParallelLeagueRunner import ParallelLeagueRunner, _derive_task_seed


# FIXTURES

REAL_DATA_FOLDER = Path("simulation/sim_data/2025")


@pytest.fixture
def base_config_dict():
    """Full reference config dict (merged ConfigManager shape)."""
    cm = ConfigManager(Path("data"))
    return {
        "config_name": cm.config_name,
        "description": cm.description,
        "parameters": dict(cm.parameters),
    }


def _make_mock_league(wins=1, losses=1, points=100.0):
    """Return a Mock that satisfies the SimulatedLeague protocol used by run_single_simulation."""
    m = Mock()
    m.get_draft_helper_results.return_value = (wins, losses, points)
    m.run_draft.return_value = None
    m.run_season.return_value = None
    m.cleanup.return_value = None
    return m


class TestDeriveTaskSeed:
    """Unit tests for the _derive_task_seed module-level function."""

    def test_same_inputs_produce_same_seed(self):
        """_derive_task_seed is deterministic: same inputs -> same output every call."""
        data_folder = Path("simulation/sim_data/2025")
        seed_a = _derive_task_seed(42, data_folder, 0)
        seed_b = _derive_task_seed(42, data_folder, 0)
        assert seed_a == seed_b

    def test_different_sim_ids_produce_different_seeds(self):
        """Each sim_id produces a distinct task_seed (seeds are unique per simulation)."""
        data_folder = Path("simulation/sim_data/2025")
        seeds = [_derive_task_seed(42, data_folder, i) for i in range(8)]
        assert len(set(seeds)) == 8, "All 8 per-sim seeds must be distinct"

    def test_different_base_seeds_produce_different_task_seeds(self):
        """Different base seeds yield different task seeds for the same (season, sim_id)."""
        data_folder = Path("simulation/sim_data/2025")
        seed_x = _derive_task_seed(1, data_folder, 0)
        seed_y = _derive_task_seed(2, data_folder, 0)
        assert seed_x != seed_y

    def test_result_is_non_negative_32bit(self):
        """Task seed is in [0, 2^32) — valid for random.Random seeding."""
        data_folder = Path("simulation/sim_data/2025")
        task_seed = _derive_task_seed(999, data_folder, 5)
        assert 0 <= task_seed < 2 ** 32

    def test_config_independence_same_season_sim_id(self):
        """Task seed depends only on (base_seed, season_folder, sim_id), NOT on config values.

        This is property D2 that the dependent T30 paired/CRN story requires:
        two configs evaluated under the same base_seed see the same draws.
        _derive_task_seed takes no config argument — independence is guaranteed by construction.
        """
        data_folder = Path("simulation/sim_data/2025")
        base_seed = 100
        # Call twice (simulating two config evaluations): same inputs -> same task seed.
        seed_config_a = _derive_task_seed(base_seed, data_folder, 3)
        seed_config_b = _derive_task_seed(base_seed, data_folder, 3)
        assert seed_config_a == seed_config_b


class TestRunnerSeedStorage:
    """ParallelLeagueRunner stores self.seed from the constructor argument."""

    def test_seed_stored_on_init(self):
        """Runner stores the supplied seed as self.seed."""
        runner = ParallelLeagueRunner(seed=42)
        assert runner.seed == 42

    def test_seed_none_default(self):
        """Runner defaults self.seed to None (entropy default, D3)."""
        runner = ParallelLeagueRunner()
        assert runner.seed is None


class TestTaskSeedsPassedToWorker:
    """Runner derives per-task seeds and passes them to run_single_simulation (thread mode)."""

    def test_seeded_runner_passes_task_seeds_to_simulated_league(self):
        """With seed=N, run_simulations_for_config passes a non-None seed to each SimulatedLeague."""
        captured_seeds = []

        def fake_league(*args, **kwargs):
            captured_seeds.append(kwargs.get("seed"))
            return _make_mock_league()

        runner = ParallelLeagueRunner(
            max_workers=1,
            data_folder=REAL_DATA_FOLDER,
            seed=77,
        )
        config = {"config_name": "test", "parameters": {}}
        num_sims = 3

        with patch("simulation.win_rate.ParallelLeagueRunner.SimulatedLeague", side_effect=fake_league):
            runner.run_simulations_for_config(config, num_sims)

        assert len(captured_seeds) == num_sims
        assert all(s is not None for s in captured_seeds), (
            "All tasks must receive a non-None seed when runner.seed is set"
        )

    def test_unseeded_runner_passes_none_seed_to_simulated_league(self):
        """With no seed, run_simulations_for_config passes None to each SimulatedLeague (D3)."""
        captured_seeds = []

        def fake_league(*args, **kwargs):
            captured_seeds.append(kwargs.get("seed"))
            return _make_mock_league()

        runner = ParallelLeagueRunner(
            max_workers=1,
            data_folder=REAL_DATA_FOLDER,
            # no seed
        )
        config = {"config_name": "test", "parameters": {}}

        with patch("simulation.win_rate.ParallelLeagueRunner.SimulatedLeague", side_effect=fake_league):
            runner.run_simulations_for_config(config, 3)

        assert all(s is None for s in captured_seeds), (
            "All tasks must receive seed=None when runner.seed is None (entropy default, D3)"
        )

    def test_task_seeds_are_config_independent(self):
        """Two runners with different config_dicts but same base_seed produce identical task seeds (D2)."""
        captured_a = []
        captured_b = []

        def fake_league_a(*args, **kwargs):
            captured_a.append(kwargs.get("seed"))
            return _make_mock_league()

        def fake_league_b(*args, **kwargs):
            captured_b.append(kwargs.get("seed"))
            return _make_mock_league()

        base_seed = 55
        config_a = {"config_name": "alpha", "parameters": {"X": 1.0}}
        config_b = {"config_name": "beta", "parameters": {"X": 2.0}}
        num_sims = 4

        with patch("simulation.win_rate.ParallelLeagueRunner.SimulatedLeague", side_effect=fake_league_a):
            runner_a = ParallelLeagueRunner(max_workers=1, data_folder=REAL_DATA_FOLDER, seed=base_seed)
            runner_a.run_simulations_for_config(config_a, num_sims)

        with patch("simulation.win_rate.ParallelLeagueRunner.SimulatedLeague", side_effect=fake_league_b):
            runner_b = ParallelLeagueRunner(max_workers=1, data_folder=REAL_DATA_FOLDER, seed=base_seed)
            runner_b.run_simulations_for_config(config_b, num_sims)

        assert captured_a == captured_b, (
            "Task seeds must be identical across different configs with the same base_seed (D2). "
            f"Got config_a seeds={captured_a}, config_b seeds={captured_b}"
        )


class TestThreadCountInvariance:
    """(b) same seed, workers=1 vs workers=4 -> identical sorted (wins, losses, points) per sim.

    This is the direct proof that the thread + global-random crux is resolved (D1):
    because each SimulatedLeague owns its own random.Random(task_seed), the order in
    which worker threads run no longer affects any league's draws.

    Uses real committed data (simulation/sim_data/2025/) with num_simulations=2 for speed.
    Exercises self-play composition. A separate test covers naive (site #3).
    """

    def test_workers_1_vs_4_produce_identical_sorted_results_self_play(self, base_config_dict):
        """workers=1 and workers=4 with the same seed yield the same sorted simulation results."""
        seed = 42
        num_sims = 2

        runner1 = ParallelLeagueRunner(max_workers=1, data_folder=REAL_DATA_FOLDER, seed=seed)
        runner4 = ParallelLeagueRunner(max_workers=4, data_folder=REAL_DATA_FOLDER, seed=seed)

        results1 = sorted(runner1.run_simulations_for_config(base_config_dict, num_sims))
        results4 = sorted(runner4.run_simulations_for_config(base_config_dict, num_sims))

        assert results1 == results4, (
            f"Thread-count invariance failed (self-play): "
            f"workers=1 -> {results1}, workers=4 -> {results4}"
        )

    def test_workers_1_vs_4_produce_identical_sorted_results_naive(self, base_config_dict):
        """workers=1 and workers=4 with the same seed yield the same results (naive; exercises site #3)."""
        seed = 7
        num_sims = 2

        runner1 = ParallelLeagueRunner(max_workers=1, data_folder=REAL_DATA_FOLDER, seed=seed, naive_opponents=True)
        runner4 = ParallelLeagueRunner(max_workers=4, data_folder=REAL_DATA_FOLDER, seed=seed, naive_opponents=True)

        results1 = sorted(runner1.run_simulations_for_config(base_config_dict, num_sims))
        results4 = sorted(runner4.run_simulations_for_config(base_config_dict, num_sims))

        assert results1 == results4, (
            f"Thread-count invariance failed (naive): "
            f"workers=1 -> {results1}, workers=4 -> {results4}"
        )
