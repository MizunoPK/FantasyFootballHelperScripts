"""
Tests for --promote/sweep-selection reproducibility across independent RNG seeds
(T36: promote-reproducibility-test-three-seeds).

Drives the REAL selection machinery — SweepTournament (coordinate-ascent + the T31
significance-adoption gate), a real SweepResultsManager (tmp_path JSON store), and the real
rank_combinations that config_promoter/--promote uses to pick the winner — seeded via the REAL
production per-task key _derive_task_seed (T29/T30). Only the slow CombinationEvaluator is
replaced, by a fast Bernoulli-kernel FakeEvaluator over a CONSTRUCTED discriminating landscape
with a single genuinely-best config: skill p is a separable, monotone function of the 6 draft
params (each param at its max grid endpoint adds GAP/6 to p) plus a per-strategy bonus, so
coordinate ascent climbs the same way and rank_combinations selects the same winner under every
base seed. Because _derive_task_seed is config-independent, all configs under one base seed share
the same u-draw stream (CRN), so a higher-p config deterministically records at least as many
wins — the winner is the constructed optimum, reproducibly, across every seed.

Covers (mirrors the spec Test Strategy):
(a) Same winner (strategy_id + param_values) across 3 independent base seeds {2024, 20260701, 13}.
(b) Same-seed determinism — one base seed run twice yields the identical selection.
(c) No live-config access — the selection path never opens data/configs/league_config.json.

Author: Kai Mizuno
"""

# Standard library
import builtins
import random
from pathlib import Path

# Local
from simulation.win_rate.SweepTournament import SweepTournament
from simulation.win_rate.SweepResultsManager import SweepResultsManager
from simulation.win_rate.sweep_summary import rank_combinations
from simulation.win_rate.param_value_generation import (
    DRAFT_SWEEP_PARAMS,
    generate_candidate_values,
)
from simulation.win_rate.ParallelLeagueRunner import _derive_task_seed
from simulation.shared.ConfigGenerator import ConfigGenerator


# FIXTURES

SEASON = Path("simulation/sim_data/2025")  # a stable season-folder name for the key (no I/O)
BASE_SEEDS = (2024, 20260701, 13)          # 3 independent base seeds (spec D2)

# Kernel parameters (calibrated offline for a clear, non-flaky separation):
#   N_DRAWS     — per-"evaluate" Bernoulli draw count; >= min_games (30) and large enough that
#                 (i) each single-param step's ~GAP/6 effect clears the T31 unpaired z-gate and
#                 (ii) the optimum is separated from its nearest recorded neighbor by many draws.
#   P_BASE      — baseline skill (all params at their min grid endpoint).
#   GAP         — total param contribution; each of the 6 params adds GAP/6 at its max endpoint.
#   STRAT_BONUS — skill edge of the winner strategy over the runner-up (a clear, seed-stable gap).
N_DRAWS = 1500
P_BASE = 0.50
GAP = 0.30
STRAT_BONUS = 0.08

# The constructed strategies: (strategy_id, draft_order). draft_order[0] encodes the skill tier
# the FakeEvaluator reads (1 = winner, 0 = runner-up) — the only per-strategy signal.
WINNER_ID = "winner_strategy"
RUNNER_UP_ID = "runner_up_strategy"
STRATEGIES = [(WINNER_ID, [1]), (RUNNER_UP_ID, [0])]

# baseline anchor = each param's MIN grid endpoint, so with num_values=2 the per-param grid is
# exactly {min, max} and coordinate ascent climbs from all-min toward the all-max optimum.
BASELINE_PARAMS = {name: ConfigGenerator.PARAM_DEFINITIONS[name][0] for name in DRAFT_SWEEP_PARAMS}


def _param_progress(name: str, value: float) -> float:
    """Normalized position of `value` in the param's [min, max] bounds (0 at min, 1 at max)."""
    min_val, max_val, _ = ConfigGenerator.PARAM_DEFINITIONS[name]
    return (value - min_val) / (max_val - min_val)


class FakeEvaluator:
    """Fast Bernoulli-kernel stand-in for CombinationEvaluator (no season replay, no I/O).

    Scores one (draft_order, param_values) combo by drawing N_DRAWS Bernoulli outcomes, each
    seeded by the REAL production key _derive_task_seed(base_seed, SEASON, sim_id): draw
    u = random.Random(task_seed).random(), win when u < p. Skill p is separable and monotone —
    P_BASE + a per-strategy bonus + (GAP/6) * sum of each param's normalized progress toward its
    max endpoint — so p peaks at the all-max optimum and each single-param step adds ~GAP/6.
    """

    def __init__(self, base_seed: int) -> None:
        self._base_seed = base_seed

    def _skill(self, draft_order, param_values) -> float:
        bonus = STRAT_BONUS if draft_order and draft_order[0] == 1 else 0.0
        progress = sum(_param_progress(name, param_values[name]) for name in DRAFT_SWEEP_PARAMS)
        return P_BASE + bonus + (GAP / len(DRAFT_SWEEP_PARAMS)) * progress

    def evaluate(self, draft_order, param_values, incumbent_param_values=None):
        p = self._skill(draft_order, param_values)
        wins = 0
        for sim_id in range(N_DRAWS):
            task_seed = _derive_task_seed(self._base_seed, SEASON, sim_id)
            if random.Random(task_seed).random() < p:
                wins += 1
        return wins, N_DRAWS, wins / N_DRAWS


def _run_selection(base_seed: int, store_path: Path) -> dict:
    """Drive the REAL SweepTournament end-to-end over the constructed landscape and return the
    selected winner row (rank_combinations(...)[0]) — exactly the config --promote would pick."""
    store = SweepResultsManager(store_path)
    tournament = SweepTournament(evaluator=FakeEvaluator(base_seed), store=store, num_values=2)
    tournament.run(STRATEGIES, dict(BASELINE_PARAMS))
    return rank_combinations(store.get_all_combinations())[0]


def _expected_optimum() -> tuple:
    """The constructed global optimum (winner strategy + each param at its max grid endpoint)."""
    candidates = generate_candidate_values(BASELINE_PARAMS, 2)
    return WINNER_ID, {name: max(candidates[name]) for name in DRAFT_SWEEP_PARAMS}


class TestSameWinnerAcrossThreeSeeds:
    """(a) The selection picks the same winning config across 3 independent base seeds."""

    def test_same_winner_across_three_seeds(self, tmp_path):
        # Arrange
        expected_id, expected_params = _expected_optimum()

        # Act: drive the real selection under each base seed with a fresh store each time.
        winners = []
        for base_seed in BASE_SEEDS:
            winner = _run_selection(base_seed, tmp_path / f"results_{base_seed}.json")
            winners.append((winner["strategy_id"], winner["param_values"]))

        # Assert: every seed selects the constructed optimum (winner strategy + all-max params).
        for strat_id, params in winners:
            assert strat_id == expected_id, f"seed selected {strat_id!r}, expected {expected_id!r}"
            assert params == expected_params, f"seed selected params {params}, expected {expected_params}"

        # And all three selections are identical to each other (reproducible, not sampling luck).
        assert winners[0] == winners[1] == winners[2]


class TestSameSeedDeterminism:
    """(b) One base seed run twice yields the identical selection (pure determinism, T29)."""

    def test_same_seed_is_deterministic(self, tmp_path):
        # Act: same base seed, two independent fresh stores.
        winner_a = _run_selection(20260701, tmp_path / "run_a.json")
        winner_b = _run_selection(20260701, tmp_path / "run_b.json")

        # Assert: byte-identical selection (strategy, params, and cumulative rate).
        assert winner_a["strategy_id"] == winner_b["strategy_id"]
        assert winner_a["param_values"] == winner_b["param_values"]
        assert winner_a["win_rate"] == winner_b["win_rate"]


class TestNoLiveConfigAccess:
    """(c) The selection path never opens data/configs/league_config.json (D5 no-write)."""

    def test_selection_never_opens_live_config(self, tmp_path, monkeypatch):
        # Arrange: record every path opened during the selection run.
        opened = []
        real_open = builtins.open

        def _tracking_open(file, *args, **kwargs):
            opened.append(str(file))
            return real_open(file, *args, **kwargs)

        monkeypatch.setattr(builtins, "open", _tracking_open)

        # Act: drive selection only (never calls promote_best_combination).
        _run_selection(2024, tmp_path / "results.json")

        # Assert: no opened path resolves to the live config.
        assert not any(
            p.replace("\\", "/").endswith("configs/league_config.json") for p in opened
        ), f"selection opened the live config path: {opened}"
