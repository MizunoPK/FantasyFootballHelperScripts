"""
Sweep Tournament

A per-draft-order-config convergent coordinate-ascent tournament over the 6 draft-side
params. For each (strategy_id, draft_order) config independently, it runs full
coordinate-ascent passes to convergence: each pass sweeps all 6 numerics (holding the
others at their current best), advancing a param to a candidate value only when that
candidate's FRESH head-to-head evaluation against the incumbent clears the adoption gate
(a one-sided one-sample z-test against the 0.50 null AND-ed with a minimum-effect-size
floor — see _adopt_by_significance). Passes repeat until a full pass moves no parameter —
convergence is the sole stopping rule. The candidate grid is computed once per config from
its baseline and reused across passes (a fixed, finite search space).

Each combination is scored via an injected CombinationEvaluator (called sequentially) and
recorded into an injected SweepResultsManager. The store is the durable record, the
reporting source, and the `--promote` input — it is NOT read by the adoption gate (T58/D2).
The returned per-config map carries each config's converged params and the fresh win rate
of the evaluation that won it.

Author: Kai Mizuno
"""

# Standard library
from math import sqrt
from statistics import NormalDist
from typing import Callable, Dict, List, Optional, Tuple

# Local
from utils.LoggingManager import get_logger
from utils.error_handler import ConfigurationError
from simulation.win_rate.param_value_generation import generate_candidate_values, DRAFT_SWEEP_PARAMS

# Significance-gate parameters (T58/D1/D3). A trial param value is adopted only when its FRESH
# head-to-head win rate (the single evaluation just run against the incumbent, T54) is both
# statistically significantly above the 0.50 null (one-sided ONE-SAMPLE z-test at
# DEFAULT_CONFIDENCE) AND above 0.50 by more than DEFAULT_MIN_EFFECT_SIZE; adoption is held when
# that evaluation yields fewer than DEFAULT_MIN_GAMES games. The 0.50 null is exact by
# construction: the measured team plays the trial config while all nine opponents hold the
# incumbent config, so "trial == incumbent" implies an expected win rate of exactly 0.5. The
# running-best's separately-accumulated rate is a DIFFERENT estimand and is no longer read.
# Module-level so the driver's input fingerprint and the engine's gate share one source of truth
# (no drift -> no spurious resume mismatch).
DEFAULT_CONFIDENCE = 0.95
DEFAULT_MIN_EFFECT_SIZE = 0.01
DEFAULT_MIN_GAMES = 30


def _adopt_by_significance(
    w_trial: int,
    n_trial: int,
    confidence: float,
    min_effect_size: float,
    min_games: int,
) -> bool:
    """Decide whether a trial combination should be adopted over the running best.

    Applies the head-to-head adoption gate (T58/D1/D3): a one-sided ONE-SAMPLE
    normal-approximation z-test of the trial's own win rate against the 0.50 null,
    AND-ed with a minimum-effect-size guard, both over the trial's FRESH head-to-head
    evaluation, held below a minimum-games floor. The 0.50 null is exact by construction:
    under the measured-vs-incumbent design (T54) the measured team plays the trial config
    while all nine opponents hold the incumbent config, so "trial config == incumbent
    config" implies an expected win rate of exactly 0.5. The running-best's separately
    accumulated rate is a DIFFERENT estimand — it mixes symmetric self-play games with
    head-to-head games against OLDER incumbents — and is deliberately not read. Stdlib-only
    (``math.sqrt`` + ``statistics.NormalDist``).

    Args:
        w_trial (int): Wins from the trial's fresh head-to-head evaluation.
        n_trial (int): Games from the trial's fresh head-to-head evaluation.
        confidence (float): One-sided confidence level for the z critical value (0, 1).
        min_effect_size (float): Minimum effect (p_trial - 0.5) required.
        min_games (int): Minimum games required of the trial's own fresh evaluation.

    Returns:
        bool: True iff n_trial >= min_games and z > z_crit and effect > min_effect_size.
    """
    if n_trial < min_games:
        return False  # D3: hold below the minimum-games floor (also guarantees n_trial > 0)
    effect = w_trial / n_trial - 0.5
    # Null standard error: under H0 (p == 0.5) the per-game variance is exactly 0.25, so
    # se = sqrt(0.25 / n) — strictly positive for EVERY n >= 1. The floor above plus the
    # min_games >= 1 constructor validation guarantee n_trial >= 1 here, so the division is
    # unconditionally safe and no zero-standard-error guard is possible or needed (T58/D3).
    se = sqrt(0.25 / n_trial)
    z = effect / se
    z_crit = NormalDist().inv_cdf(confidence)
    return z > z_crit and effect > min_effect_size  # D3: AND-gate, both boundaries strict


def _read_convergence_best_rate(conv: dict) -> float:
    """Read a convergence entry's accumulated best-combo rate, tolerating the legacy key.

    Supports the D4 back-compat alias (new key ``best_combo_win_rate``, else legacy
    ``best_win_rate``) but fails fast on a corrupt entry carrying neither.

    Args:
        conv (dict): A convergence entry as returned by
            ``SweepResultsManager.get_config_convergence``.

    Returns:
        float: The accumulated best-combo win rate stored in the entry.

    Raises:
        KeyError: If the entry carries neither ``best_combo_win_rate`` nor the legacy
            ``best_win_rate`` key — indicates a corrupt or partially-written entry.
    """
    if "best_combo_win_rate" in conv:
        return conv["best_combo_win_rate"]
    if "best_win_rate" in conv:
        return conv["best_win_rate"]
    raise KeyError(
        "convergence entry missing both 'best_combo_win_rate' and legacy 'best_win_rate'"
    )


class SweepTournament:
    """
    Per-config convergent coordinate-ascent tournament over the 6 draft-side params.

    Each (strategy_id, draft_order) config is tuned independently: full coordinate-ascent
    passes (all 6 numerics each pass, holding the others at their current best) repeat to
    convergence under a significance gate — a param adopts a candidate only when that
    candidate's FRESH head-to-head win rate (the single evaluation just run against the
    incumbent, T54) is both significantly above the 0.50 null (one-sided ONE-SAMPLE z-test at
    the configured confidence) AND above 0.50 by more than the minimum effect size, with
    adoption held when that evaluation yields fewer than min_games games. The store is NOT a
    gate input (T58/D2) — it remains the durable record, the reporting source, and the
    `--promote` input. Convergence (a full pass that moves no parameter) is the sole stopping
    rule. The candidate grid is fixed per config (computed once from its baseline).
    Dependencies are injected so the tournament does no file/sim/config loading itself:

    Attributes:
        _evaluator: a CombinationEvaluator (evaluate(draft_order, param_values) ->
            (wins, games, win_rate)).
        _store: a SweepResultsManager (update(...) + get_combination(strategy_id, param_values)).
        _num_values: candidate count per numeric (passed to generate_candidate_values).
        _confidence: one-sided confidence level for the z critical value (0, 1).
        _min_effect_size: minimum effect (p_trial - 0.5) the trial's fresh rate must exceed.
        _min_games: minimum games the trial's own fresh evaluation must yield before a
            decision (a degenerate-input guard, not a live gate at production sample sizes).
    """

    def __init__(
        self,
        evaluator,
        store,
        num_values: int = 5,
        confidence: float = DEFAULT_CONFIDENCE,
        min_effect_size: float = DEFAULT_MIN_EFFECT_SIZE,
        min_games: int = DEFAULT_MIN_GAMES,
    ) -> None:
        """
        Args:
            evaluator: CombinationEvaluator used to score each combination.
            store: SweepResultsManager used to record/accumulate every evaluation.
            num_values (int): Candidate values per numeric parameter (default 5).
            confidence (float): One-sided confidence level for the adoption z-test
                (default DEFAULT_CONFIDENCE = 0.95); must lie in the open interval (0, 1).
            min_effect_size (float): Minimum effect against the 0.50 null (p_trial - 0.5) a
                candidate must exceed to be adopted (default DEFAULT_MIN_EFFECT_SIZE = 0.01).
            min_games (int): Minimum games the trial's OWN fresh head-to-head evaluation must
                yield before a candidate can be adopted (default DEFAULT_MIN_GAMES = 30).

        Raises:
            ConfigurationError: If confidence is not strictly within (0, 1).
            ConfigurationError: If min_games is less than 1.
            ConfigurationError: If min_effect_size is not in [0, 1).
        """
        if not 0 < confidence < 1:
            raise ConfigurationError(
                f"SweepTournament confidence must be in the open interval (0, 1); got {confidence!r}"
            )
        if min_games < 1:
            raise ConfigurationError(
                f"SweepTournament min_games must be a positive integer (>= 1); got {min_games!r}"
            )
        if not 0 <= min_effect_size < 1:
            raise ConfigurationError(
                f"SweepTournament min_effect_size must be in the interval [0, 1); got {min_effect_size!r}"
            )
        self._evaluator = evaluator
        self._store = store
        self._num_values = num_values
        self._confidence = confidence
        self._min_effect_size = min_effect_size
        self._min_games = min_games

    def _accumulated_rate(self, strategy_id: str, param_values: Dict[str, float]) -> float:
        """Return the store's accumulated win rate for one combination.

        Args:
            strategy_id (str): Strategy identifier keying the combination.
            param_values (Dict[str, float]): The 6 draft-side param values.

        Returns:
            float: total_wins / total_games for the combination, or 0.0 when the
                combination is unrecorded or has zero accumulated games.
        """
        entry = self._store.get_combination(strategy_id, param_values)
        if entry is None or entry["total_games"] == 0:
            return 0.0
        return entry["total_wins"] / entry["total_games"]

    def run(
        self,
        strategies: List[Tuple[str, list]],
        baseline_params: Dict[str, float],
        resume: bool = False,
        carry_over_seeds: Optional[Dict[str, Dict[str, float]]] = None,
        progress_callback: Optional[Callable[[str], None]] = None,
    ) -> Dict[str, Dict]:
        """
        Run an independent convergent coordinate-ascent tournament for every draft-order
        config and return the per-config converged result map.

        Args:
            strategies: List of (strategy_id, draft_order) configs, each tuned independently.
            baseline_params: The 6 current draft-side param values (each config's anchor / start).
            resume: When True (D3), consult the injected store's per-config convergence to
                skip configs already marked "converged" and seed an "in_progress" config's
                start point from its checkpointed best values; configs with no convergence
                entry start from baseline. When False (default), every config starts from
                baseline (the pre-T9 behavior). Either way, per-config progress is written
                via the store's mark_config_progress so an interrupt leaves a resumable
                checkpoint.
            carry_over_seeds: When provided (T10/D1a — endless passes 2+ only), a per-config
                {strategy_id: best_param_values} map. A config with a seed starts its
                coordinate ascent from dict(seed) (not baseline), is evaluated ONCE to
                re-establish this pass's best_rate as the ε-gate baseline from fresh
                evidence (recorded via the existing store.update), is marked in_progress,
                and then tunes over the FULL grid — it is NOT skipped. Orthogonal to resume:
                the driver guarantees resume and carry_over_seeds are never both active in one
                pass (pass 1 -> resume=<decision>, carry_over_seeds=None; passes 2+ ->
                resume=False, carry_over_seeds=<map>), so conv is None whenever a seed fires.
                Configs with no seed fall back to the baseline start. Default None ->
                unchanged behavior.
            progress_callback: Optional callback invoked exactly once per config when that
                config reaches a terminal state — on BOTH the resume-skip ("already converged")
                path and the converged path — with the config's strategy_id. When None (the
                default), no progress signal is emitted and behavior is unchanged. The callback
                owns the per-config *progress* output (the TTY bar / non-TTY progress lines); the
                tournament itself does no console (stdout) I/O, though it still emits its own
                status lines (e.g. "Config ... converged") through the logger.

        Returns:
            Dict[str, Dict]: {strategy_id: {"param_values": <6-param dict>, "win_rate": float}}.
                CAVEAT (T58/C2, absorbed by T62/D4) — "win_rate" carries TWO DIFFERENT
                ESTIMANDS and the two are NOT comparable across configs. When the config's
                ascent adopted at least one parameter, it is the FRESH HEAD-TO-HEAD rate of
                the last adopted trial against its incumbent. When the ascent never moved a
                parameter, it is the ACCUMULATED SELF-PLAY rate of the baseline/carry-over
                anchor — symmetric by construction, so ~0.50 and carrying no strength
                information. Ranking configs on this field mixes the two (the
                incommensurability ARCHITECTURE.md Decision 6 describes).

        Raises:
            ConfigurationError: If strategies is empty.
        """
        if not strategies:
            raise ConfigurationError("SweepTournament.run requires a non-empty strategies list")

        logger = get_logger()  # KDD-3: resolve at call time so --log-level governs this output

        candidates = generate_candidate_values(baseline_params, self._num_values)  # KDD-3: fixed grid
        results: Dict[str, Dict] = {}

        for strategy_id, draft_order in strategies:
            # D3: when resuming, consult the per-config convergence to skip / seed.
            conv = self._store.get_config_convergence(strategy_id) if resume else None
            if conv is not None and conv.get("status") == "converged":
                logger.info(f"Config {strategy_id} skipped (already converged)")
                results[strategy_id] = {
                    "param_values": dict(conv["best_param_values"]),
                    # D4: new key, else legacy best_win_rate; corrupt entry (neither key) raises.
                    "win_rate": _read_convergence_best_rate(conv),
                }
                if progress_callback is not None:  # KDD-2: fire on the resume-skip path
                    progress_callback(strategy_id)
                continue
            if conv is not None and conv.get("status") == "in_progress":
                # Resume the interrupted config from its checkpointed best point (NOT re-evaluated).
                # The seed combo already exists in the persisted store from the prior run, so we do
                # NOT re-record it — a 0-win/0-game update() would bump total_runs / last_run with
                # zero evidence and skew the per-combo metadata on every resume (PR #18).
                current = dict(conv["best_param_values"])
                # D4: new key, else legacy best_win_rate; corrupt entry (neither key) raises.
                best_rate = _read_convergence_best_rate(conv)
            elif carry_over_seeds is not None and strategy_id in carry_over_seeds:
                # T10/D1a: seed-and-tune from a prior pass's converged params (endless passes 2+).
                # Unlike the in_progress resume branch, the seed is evaluated ONCE here to
                # re-establish THIS pass's running-best baseline from fresh evidence (the
                # evaluator is non-deterministic and the store accumulates games), recording it
                # via the existing update(). best_rate (T31/F7) is the seed combo's ACCUMULATED
                # rate read back from the store. The config then falls through to the full
                # coordinate-ascent below — it is NOT skipped and the grid is unchanged.
                current = dict(carry_over_seeds[strategy_id])
                wins, games, win_rate = self._evaluator.evaluate(draft_order, current)
                self._store.update(strategy_id, current, win_rate, wins, games)
                best_rate = self._accumulated_rate(strategy_id, current)
            else:
                # Per-config baseline evaluation establishes the starting best (also recorded).
                # best_rate (T31/F7) is the baseline combo's ACCUMULATED rate from the store.
                current = dict(baseline_params)
                wins, games, win_rate = self._evaluator.evaluate(draft_order, current)
                self._store.update(strategy_id, current, win_rate, wins, games)
                best_rate = self._accumulated_rate(strategy_id, current)

            # Record in-progress so an interrupt at any point leaves a resumable checkpoint (D3).
            self._store.mark_config_progress(strategy_id, "in_progress", current, best_rate)

            # Loop full coordinate-ascent passes until a pass moves no parameter (convergence
            # is the sole stopping rule — no wall-time, no pass cap).
            moved = True
            while moved:
                moved = False
                for param in DRAFT_SWEEP_PARAMS:           # all 6 swept every pass
                    for value in candidates[param]:
                        if value == current[param]:
                            continue                       # current best already recorded
                        trial = dict(current)
                        trial[param] = value
                        wins, games, win_rate = self._evaluator.evaluate(draft_order, trial, incumbent_param_values=current)
                        self._store.update(strategy_id, trial, win_rate, wins, games)
                        # T58/D2: decide adoption on the trial's FRESH head-to-head evidence
                        # (the `wins, games` bound from the evaluate() above), tested against the
                        # 0.50 null. The store is deliberately NOT read here: the running-best's
                        # accumulated totals mix symmetric self-play games (the baseline and
                        # carry-over anchors) with head-to-head games against OLDER incumbents,
                        # and the trial's own accumulated totals could likewise span earlier
                        # passes against a different incumbent. The fresh pair is same-reference
                        # by construction, so the old None-entry hold-guard has no failure mode
                        # left to defend (the PR #18 resume path can no longer reach the gate).
                        if _adopt_by_significance(
                            wins, games,
                            self._confidence, self._min_effect_size, self._min_games,
                        ):
                            current[param] = value
                            # After adoption current == trial, so the new running-best's rate is
                            # THIS trial's fresh head-to-head win_rate (T58/R4) — not a
                            # store-accumulated rate blending other incumbents' games.
                            best_rate = win_rate
                            moved = True
                            # Persist the new running best immediately, so an interrupt mid-ascent
                            # leaves the LATEST values on disk (not the stale seed) and a resume
                            # restarts from them rather than losing this run's progress (PR #18).
                            self._store.mark_config_progress(
                                strategy_id, "in_progress", current, best_rate
                            )

            self._store.mark_config_progress(strategy_id, "converged", current, best_rate)
            results[strategy_id] = {"param_values": dict(current), "win_rate": best_rate}
            logger.info(
                f"Config {strategy_id} converged | win_rate={best_rate:.3f} "
                f"(fresh head-to-head rate if a param moved, else the accumulated self-play "
                f"anchor ~0.50 — different estimands, not comparable across configs)"
            )
            if progress_callback is not None:  # KDD-2: fire on the converged path
                progress_callback(strategy_id)

        return results
