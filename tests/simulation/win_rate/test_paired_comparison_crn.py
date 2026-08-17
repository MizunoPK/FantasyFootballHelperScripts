"""
Tests for paired (common-random-number) trial-vs-current comparison in the sweep
(T30: paired-comparison-in-ascent).

The pairing T30 delivers is *emergent*: under a fixed base seed, ParallelLeagueRunner's
config-independent per-task key (base_seed, season, sim_id) — _derive_task_seed (T29/D2) —
hands two different configs the SAME per-(season, sim_id) draws, so the coordinate-ascent
trial-vs-current win-rate difference is computed on common random numbers (CRN) and its
variance collapses, without biasing any single config's aggregate estimate.

These tests verify that statistical property directly on the *real* production seeding key
(_derive_task_seed) using a fast, deterministic Bernoulli win-model kernel rather than the
full multi-second SimulatedLeague replay (which, in the default self-play regime, is also
~0.50 by symmetry for every config and so carries no constructible win-rate gap). The kernel
models each per-task draw as a uniform u in [0, 1) drawn from random.Random(task_seed); a
config with skill p "wins" that draw when u < p. Two configs sharing a base seed therefore
share every u (CRN); under independent base seeds they do not.

Covers:
(a) Variance reduction (F3): Var(paired win-rate difference) << Var(unpaired difference)
    for a known small gap.
(b) No aggregate bias (F4): the seeded mean aggregate win-rate matches the analytic
    expectation p (seeding shifts variance, not expectation).
(c) Pairing backbone (F1): the real _derive_task_seed is config-independent, which is what
    makes the kernel's CRN — and the production sweep's pairing — hold.
(d) Sweep seed policy (F2): _resolve_sweep_seed returns an explicit --seed verbatim and,
    when absent, auto-assigns an in-range base seed and logs the reproduce hint.

Author: Kai Mizuno
"""

# Standard library
import logging
import random
import statistics
from argparse import Namespace
from pathlib import Path

# Local
import run_win_rate_simulation as rws
from simulation.win_rate.ParallelLeagueRunner import _derive_task_seed


# FIXTURES

SEASON = Path("simulation/sim_data/2025")  # a stable season-folder name for the key (no I/O)

# Kernel parameters (calibrated offline for a clear, non-flaky separation):
#   N_DRAWS  — per-"evaluate" draw count (each is one (season, sim_id) task seed)
#   P_A/P_B  — two configs with a known small win-rate gap (0.05)
#   R        — replicates used to estimate the variance of the difference
#   M        — base seeds averaged for the no-bias check
N_DRAWS = 200
P_A = 0.55
P_B = 0.50
R = 30
M = 60
REPLICATE_SEED = 2024  # fixes the replicate base-seed stream -> fully deterministic test


def _win_rate(base_seed: int, p: float) -> float:
    """Kernel win rate for a config of skill p under a fixed base seed.

    Each per-task draw uses the REAL production key _derive_task_seed(base_seed, season,
    sim_id) to seed a private random.Random, then draws u in [0, 1); the config wins when
    u < p. Two configs sharing base_seed share every u (common random numbers).
    """
    wins = 0
    for sim_id in range(N_DRAWS):
        task_seed = _derive_task_seed(base_seed, SEASON, sim_id)
        if random.Random(task_seed).random() < p:
            wins += 1
    return wins / N_DRAWS


class TestPairedVarianceReduction:
    """F3: the paired win-rate difference has materially lower variance than unpaired."""

    def test_paired_difference_variance_is_materially_lower(self):
        # Arrange: a deterministic stream of replicate base seeds.
        rep_rng = random.Random(REPLICATE_SEED)
        paired_diffs = []
        unpaired_diffs = []

        # Act: per replicate, compute A - B paired (same base seed -> CRN) and A - B
        # unpaired (independent base seeds). A's value is shared across both arms.
        for _ in range(R):
            seed_shared = rep_rng.randrange(2 ** 32)
            seed_independent = rep_rng.randrange(2 ** 32)
            wr_a = _win_rate(seed_shared, P_A)
            paired_diffs.append(wr_a - _win_rate(seed_shared, P_B))
            unpaired_diffs.append(wr_a - _win_rate(seed_independent, P_B))

        var_paired = statistics.pvariance(paired_diffs)
        var_unpaired = statistics.pvariance(unpaired_diffs)

        # Assert: pairing collapses the difference's variance (observed ~10.6x; assert a
        # conservative >=3x with a large safety margin so the test is not flaky).
        assert var_paired < var_unpaired, (
            f"paired var ({var_paired:.3e}) must be below unpaired var ({var_unpaired:.3e})"
        )
        assert var_unpaired >= 3.0 * var_paired, (
            f"expected >=3x variance reduction; got {var_unpaired / var_paired:.2f}x "
            f"(paired={var_paired:.3e}, unpaired={var_unpaired:.3e})"
        )

    def test_paired_difference_recovers_the_true_gap(self):
        # The paired difference should center on the true gap (P_A - P_B), confirming the
        # variance reduction is around the correct mean rather than a degenerate constant.
        # Own dedicated RNG — independent of the F3 test's stream.
        rep_rng = random.Random(REPLICATE_SEED + 1)
        paired_diffs = []
        for _ in range(R):
            seed_shared = rep_rng.randrange(2 ** 32)
            paired_diffs.append(_win_rate(seed_shared, P_A) - _win_rate(seed_shared, P_B))

        assert abs(statistics.fmean(paired_diffs) - (P_A - P_B)) < 0.03


class TestNoAggregateBias:
    """F4: seeding does not bias a single config's aggregate win-rate estimate."""

    def test_seeded_mean_matches_analytic_expectation(self):
        # Two INDEPENDENT deterministic base-seed streams; each averages M seeded win rates.
        # Both must land on the analytic expectation p — seeding shifts variance, not the mean.
        stream_one = random.Random(99)
        stream_two = random.Random(7)
        mean_one = statistics.fmean(_win_rate(stream_one.randrange(2 ** 32), P_A) for _ in range(M))
        mean_two = statistics.fmean(_win_rate(stream_two.randrange(2 ** 32), P_A) for _ in range(M))

        assert abs(mean_one - P_A) < 0.03, f"seeded mean {mean_one:.4f} biased vs p={P_A}"
        assert abs(mean_two - P_A) < 0.03, f"seeded mean {mean_two:.4f} biased vs p={P_A}"
        assert abs(mean_one - mean_two) < 0.03, (
            f"two independent seeded estimators disagree: {mean_one:.4f} vs {mean_two:.4f}"
        )


class TestPairingBackbone:
    """F1: the real per-task key is config-independent, which is what realizes CRN pairing."""

    def test_derive_task_seed_is_config_independent_under_fixed_base_seed(self):
        # _derive_task_seed takes no config input, so a trial and the current-best under the
        # same base seed receive identical per-(season, sim_id) seeds -> identical draws.
        base_seed = 12345
        trial_seeds = [_derive_task_seed(base_seed, SEASON, sid) for sid in range(N_DRAWS)]
        current_seeds = [_derive_task_seed(base_seed, SEASON, sid) for sid in range(N_DRAWS)]
        assert trial_seeds == current_seeds

    def test_distinct_base_seeds_give_distinct_draws(self):
        # Independent base seeds (the unpaired arm) yield different per-task seeds.
        a = [_derive_task_seed(1, SEASON, sid) for sid in range(N_DRAWS)]
        b = [_derive_task_seed(2, SEASON, sid) for sid in range(N_DRAWS)]
        assert a != b


class TestResolveSweepSeed:
    """F2: the sweep-mode seed policy (auto-assign + log; explicit verbatim)."""

    def test_explicit_seed_returned_verbatim_no_autolog(self, caplog):
        # Arrange
        args = Namespace(seed=42)
        logger = logging.getLogger("test_resolve_sweep_seed_explicit")

        # Act
        with caplog.at_level(logging.INFO, logger="test_resolve_sweep_seed_explicit"):
            resolved = rws._resolve_sweep_seed(args, logger)

        # Assert
        assert resolved == 42
        assert not any("Auto-assigned sweep base seed" in r.getMessage() for r in caplog.records)

    def test_missing_seed_autoassigns_in_range_and_logs_reproduce_hint(self, caplog):
        # Arrange
        args = Namespace(seed=None)
        logger = logging.getLogger("test_resolve_sweep_seed_auto")

        # Act
        with caplog.at_level(logging.INFO, logger="test_resolve_sweep_seed_auto"):
            resolved = rws._resolve_sweep_seed(args, logger)

        # Assert: an in-range base seed and a logged reproduce hint naming that exact seed.
        assert 0 <= resolved < 2 ** 32
        messages = [r.getMessage() for r in caplog.records]
        assert any(
            "Auto-assigned sweep base seed" in m and f"--seed {resolved}" in m
            for m in messages
        ), f"expected an auto-assign reproduce hint naming seed {resolved}; got {messages}"

    def test_missing_seed_varies_across_calls(self, monkeypatch):
        # Patch SystemRandom so the test is fully deterministic while proving the code does
        # NOT return a constant — it passes through the RNG output on each call.
        # The explicit-seed path must be unaffected (it bypasses the entropy RNG entirely).
        call_idx = [0]
        known_values = [1234567, 7654321]

        class FakeSystemRandom:
            def randrange(self, n):
                val = known_values[call_idx[0]]
                call_idx[0] += 1
                return val

        monkeypatch.setattr(random, "SystemRandom", FakeSystemRandom)
        logger = logging.getLogger("test_resolve_sweep_seed_vary")

        # Two unseeded calls return the patched non-constant sequence.
        s1 = rws._resolve_sweep_seed(Namespace(seed=None), logger)
        s2 = rws._resolve_sweep_seed(Namespace(seed=None), logger)
        assert s1 == 1234567
        assert s2 == 7654321
        assert s1 != s2

        # The explicit-seed path bypasses SystemRandom entirely.
        s_explicit = rws._resolve_sweep_seed(Namespace(seed=99), logger)
        assert s_explicit == 99
        assert call_idx[0] == 2  # no extra randrange call for the explicit path
