"""
Paired A/B Comparison (Common Random Numbers)

A small, dependency-light before/after win-rate comparator for the win-rate engine.
Given a CURRENT config and a RECOMMENDED config (both in-memory dicts), it runs the two
on SHARED per-(season, sim_id) seeds — common random numbers (CRN) — in the ASYMMETRIC
measured-vs-reference setup: for each arm the measured DraftHelperTeam scores with the
config under test while every opponent holds the fixed reference config. Because the
per-task key is config-independent (ParallelLeagueRunner._derive_task_seed, T29/T30), both
arms see identical draws, so the variance of the before/after DIFFERENCE collapses — the
empirically discriminating regime the investigation validated (Exp 6).

This is the measurement half of the T35 baseline re-tune (the sweep SELECTS candidates; this
helper MEASURES the delta) and is designed for reuse by the T24 discrimination-validation
feature. It is deterministic under a fixed seed and stdlib-only for statistics (a pooled
two-proportion z, the same statistic SweepTournament._adopt_by_significance gates on, T31).

Purity / no live-config write: the signature takes config dicts + a data_folder, never a
config *path*. It never imports, reads, or writes data/configs/league_config.json — the
caller loads the current live params read-only and passes them in (D4).

Author: Kai Mizuno
"""

# Standard library
from dataclasses import dataclass
from math import sqrt
from pathlib import Path
from typing import Dict, Optional, Tuple

# Local
from utils.LoggingManager import get_logger
from simulation.win_rate.SimDataLoader import SimDataLoader
from simulation.win_rate.SimulatedLeague import SimulatedLeague
from simulation.win_rate.ParallelLeagueRunner import _derive_task_seed


@dataclass(frozen=True)
class PairedComparisonResult:
    """Outcome of a CRN-paired before/after win-rate comparison.

    Attributes:
        current_rate (float): Measured-team win rate for the CURRENT config arm.
        recommended_rate (float): Measured-team win rate for the RECOMMENDED config arm.
        delta (float): recommended_rate - current_rate (the before/after improvement).
        z (float): Pooled two-proportion z for (recommended - current); 0.0 on a degenerate
            (zero standard error) pool. Same pooled-SE statistic as
            SweepTournament._adopt_by_significance (T31).
        games (int): Games evaluated per arm (equal across arms under CRN — identical
            seeds/seasons/sims).
        seed (int): The base seed used for the run (echoed for reproducibility).
    """

    current_rate: float
    recommended_rate: float
    delta: float
    z: float
    games: int
    seed: int


def _pooled_two_proportion_z(w_a: int, n_a: int, w_b: int, n_b: int) -> float:
    """Signed pooled two-proportion z for (p_b - p_a).

    Mirrors the pooled standard-error construction in
    SweepTournament._adopt_by_significance (T31): z = (p_b - p_a) / sqrt(p_pool *
    (1 - p_pool) * (1/n_a + 1/n_b)). Stdlib-only (math.sqrt). Returns 0.0 on a degenerate
    pool (either arm has zero games, or the pooled standard error is zero — an all-wins /
    all-losses pool where z is undefined), the same zero-SE guard the T31 gate applies.

    Args:
        w_a (int): Arm A wins. n_a (int): Arm A games.
        w_b (int): Arm B wins. n_b (int): Arm B games.

    Returns:
        float: The signed z statistic, or 0.0 on a degenerate pool.
    """
    if n_a == 0 or n_b == 0:
        return 0.0
    p_a = w_a / n_a
    p_b = w_b / n_b
    p_pool = (w_a + w_b) / (n_a + n_b)
    se = sqrt(p_pool * (1.0 - p_pool) * (1.0 / n_a + 1.0 / n_b))
    if se == 0:
        return 0.0
    return (p_b - p_a) / se


def _run_arm(
    reference_config: dict,
    measured_config: dict,
    season_folder: Path,
    week_data_cache: Dict[int, Dict],
    seed: int,
) -> Tuple[int, int]:
    """Run one asymmetric measured-vs-reference league and return (wins, games).

    Builds a SimulatedLeague whose measured DraftHelperTeam scores with measured_config
    while every opponent holds reference_config, runs the draft + season, and reads the
    measured team's wins/games. The league's private RNG is seeded with the shared per-task
    seed, so two arms sharing seed see identical draws (CRN). Always cleaned up.

    Args:
        reference_config (dict): Opponents' fixed config (SimulatedLeague config_dict).
        measured_config (dict): The config under test (SimulatedLeague measured_config_dict).
        season_folder (Path): The committed season directory (data_folder for the league).
        week_data_cache (Dict[int, Dict]): Preloaded week data from SimDataLoader.
        seed (int): The shared per-(season, sim_id) task seed.

    Returns:
        Tuple[int, int]: (wins, games) for the measured DraftHelperTeam; games = wins + losses.
    """
    league = None
    try:
        league = SimulatedLeague(
            reference_config,
            season_folder,
            week_data_cache,
            measured_config_dict=measured_config,
            seed=seed,
        )
        league.run_draft()
        league.run_season()
        wins, losses, _ = league.get_draft_helper_results()
        return wins, wins + losses
    finally:
        if league:
            league.cleanup()


def run_paired_ab_comparison(
    current_config: dict,
    recommended_config: dict,
    data_folder: Path,
    seed: int,
    *,
    reference_config: Optional[dict] = None,
    num_simulations: int = 1,
    max_workers: int = 8,
) -> PairedComparisonResult:
    """Measure the CRN-paired before/after win-rate delta of two configs.

    For every valid committed season under data_folder and every sim_id in
    range(num_simulations), derives the config-independent per-task seed
    (_derive_task_seed, T29/T30) and runs BOTH arms (current, recommended) at that same seed
    in the asymmetric measured-vs-reference setup, so the two arms share every draw (CRN) and
    the variance of the difference collapses. Aggregates measured-team wins/games per arm and
    returns the paired result. Deterministic under a fixed seed. Reads only the committed
    offline season data + the passed-in dicts — NEVER data/configs/league_config.json (D4).

    Args:
        current_config (dict): The CURRENT (live-baseline) full config dict — the "before" arm.
        recommended_config (dict): The RECOMMENDED full config dict — the "after" arm.
        data_folder (Path): Simulation data root containing 20XX/ season folders.
        seed (int): Base seed for the run (fixed for reproducibility + CRN pairing).
        reference_config (Optional[dict]): Opponents' fixed config held constant across both
            arms. Default None uses current_config (opponents hold the current baseline).
        num_simulations (int): Simulations per season per arm (default 1).
        max_workers (int): Reserved for future parallel-arm execution (T24). The arms run
            sequentially per season here — this helper is called once per bounded operational
            run, not in a hot loop — so it is accepted for API/signature stability and not
            yet threaded into an executor.

    Returns:
        PairedComparisonResult: (current_rate, recommended_rate, delta, z, games, seed).

    Raises:
        FileNotFoundError: If no 20XX/ season folders exist under data_folder.
    """
    logger = get_logger()
    reference = reference_config if reference_config is not None else current_config

    seasons = sorted(Path(data_folder).glob("20*/"))
    if not seasons:
        raise FileNotFoundError(
            f"run_paired_ab_comparison: no historical season folders (20XX/) found in "
            f"{data_folder}. Run compile_historical_data.py first."
        )

    wins_current = games_current = 0
    wins_recommended = games_recommended = 0

    for season_folder in seasons:
        loader = SimDataLoader(season_folder)
        if not loader.is_valid:
            logger.warning(
                f"run_paired_ab_comparison: skipping invalid season {season_folder.name}"
            )
            continue
        week_data_cache = loader.week_data_cache
        for sim_id in range(num_simulations):
            task_seed = _derive_task_seed(seed, season_folder, sim_id)
            cw, cg = _run_arm(reference, current_config, season_folder, week_data_cache, task_seed)
            rw, rg = _run_arm(reference, recommended_config, season_folder, week_data_cache, task_seed)
            wins_current += cw
            games_current += cg
            wins_recommended += rw
            games_recommended += rg

    current_rate = wins_current / games_current if games_current else 0.0
    recommended_rate = wins_recommended / games_recommended if games_recommended else 0.0
    delta = recommended_rate - current_rate
    z = _pooled_two_proportion_z(wins_current, games_current, wins_recommended, games_recommended)

    return PairedComparisonResult(
        current_rate=current_rate,
        recommended_rate=recommended_rate,
        delta=delta,
        z=z,
        games=games_current,
        seed=seed,
    )
