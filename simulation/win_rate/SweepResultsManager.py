"""
Sweep Results Manager

Manages the win_rate_sweep_results.json persistence lifecycle for the multi-parameter
sweep. Records, per (strategy + the 6 draft-side param values) combination, the
cumulative wins/games, best win rate, and run metadata — accumulating across runs so
re-runs add evidence rather than overwriting it.

This is a dedicated store, separate from the single-axis WinRateMetaDataManager /
win_rate_meta_data.json (which it never reads or writes). It mirrors that manager's
absent/corrupt-tolerant load and atomic (tmp -> rename) save.

Author: Kai Mizuno
"""

# Standard library
import datetime
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Optional

# Local
from utils.LoggingManager import get_logger
from utils.error_handler import create_component_error_handler, error_context, ConfigurationError, FileOperationError
from simulation.shared.atomic_io import atomic_write_json
from simulation.win_rate.param_value_generation import DRAFT_SWEEP_PARAMS

logger = get_logger()
_error_handler = create_component_error_handler("SweepResultsManager")


class SweepResultsManager:
    """
    Manages win_rate_sweep_results.json persistence keyed by parameter combination.

    Loads the file on construction (initializes empty if absent or corrupted). Exposes
    update() for recording one combination evaluation and writes atomically after every
    call. Keyed by a canonical combination string built from the strategy id and the 6
    draft-side param values (see make_combo_key).
    """

    def __init__(self, results_path: Path, expected_naive_opponents: Optional[bool] = None) -> None:
        """
        Initialize the manager and load existing sweep results from disk.

        Args:
            results_path (Path): Path to win_rate_sweep_results.json. File need not
                exist — if absent, starts with an empty data structure.
            expected_naive_opponents (Optional[bool]): The opponent regime THIS run will
                accumulate under (T57/D3/D4). When supplied, _incompatibility_reason
                quarantines a store whose RECORDED regime differs (a different estimand).
                Omit (the default None) to disable the regime check entirely — the
                --promote path and every non-sweep caller pass nothing and keep today's
                behavior exactly.
        """
        self._results_path = results_path
        # T57/D3: assigned BEFORE _load() — _load calls _quarantine_if_incompatible, which
        # reads this attribute, so this ordering is load-bearing.
        self._expected_naive_opponents = expected_naive_opponents
        self._load()

    @staticmethod
    def _empty_data() -> Dict:
        """Return a fresh empty store shape (the absent / corrupt / quarantine reset state).

        Returns:
            Dict: A new dict with the canonical top-level keys — an empty combinations map,
                empty input_fingerprint, empty convergence map, discriminating False, and an
                UNKNOWN (None) opponent-regime marker (T57/D8 — None, NOT False, because False
                is the real self-play regime and a restarted store has accumulated nothing
                under any regime yet, so it must never ASSERT one it was not run under).
        """
        return {
            "last_updated": "",
            "combinations": {},
            "input_fingerprint": "",
            "convergence": {},
            "discriminating": False,
            "naive_opponents": None,
        }

    def _load(self) -> None:
        """Load sweep results from disk, or initialize empty if file absent or corrupted.

        On a successful load of an existing file, defaults the checkpoint keys
        ``input_fingerprint`` and ``convergence`` when absent, so an old-schema
        (combinations-only) file loads cleanly while its existing ``combinations``
        are preserved untouched.
        """
        if not self._results_path.exists():
            logger.debug(f"No sweep results file at {self._results_path} — starting fresh")
            self._data = self._empty_data()
            return
        try:
            with open(self._results_path, 'r', encoding='utf-8') as f:
                self._data = json.load(f)
            logger.debug(f"Loaded sweep results: {len(self._data.get('combinations', {}))} combinations")
        except json.JSONDecodeError as e:
            logger.warning(f"Corrupted sweep results at {self._results_path}: {e} — starting fresh")
            self._data = self._empty_data()
            return
        self._data.setdefault("combinations", {})
        self._data.setdefault("input_fingerprint", "")
        self._data.setdefault("convergence", {})
        self._data.setdefault("discriminating", False)
        self._quarantine_if_incompatible()

    def _incompatibility_reason(self) -> Optional[str]:
        """Return why the loaded store is structurally incompatible, or None if it is usable (T68/D3).

        The union trigger set — T68 wired ONE trigger; T57 added the SECOND by extending THIS
        method, reusing the same _quarantine_and_restart primitive (no forked mechanism). T57's
        realized trigger is an OPPONENT-REGIME change, NOT a fingerprint mismatch: quarantine
        keys on the ESTIMAND while the driver's resume decision keeps the FULL input fingerprint
        (T57/D4, spec OQ1 — the two questions must not share a predicate, or unseeded runs could
        never accumulate). Trigger (T68): a NON-EMPTY combinations map in which ANY record lacks the
        by_reference dimension. Such a store holds a pre-fix, reference-free cumulative mixture
        that is mathematically unrecoverable (no per-eval retention). A brand-new EMPTY store is
        NOT pre-fix and must NOT trip this (the `if combinations` guard); a T68-written store
        always carries by_reference on every record. Deliberately structural — it does NOT read
        the `discriminating` flag, which certifies a DIFFERENT property (a discriminating pre-fix
        store must still quarantine).

        Returns:
            Optional[str]: A human-readable reason string when incompatible, else None.
        """
        combinations = self._data.get("combinations", {})
        if combinations and any("by_reference" not in record for record in combinations.values()):
            return (
                "pre-T68 store: at least one combination record has no 'by_reference' "
                "dimension (reference-free cumulative totals are an unrecoverable mixture)"
            )
        # T57/D4: the SECOND trigger — an opponent-regime change. Keyed on the ESTIMAND, never on
        # the input fingerprint: a fresh auto-seed, an added strategy file, or a wider
        # --num-values re-draws from the SAME distribution and must keep accumulating
        # (resume=False, store KEPT), while the regime shifts the estimand itself (~0.84 naive
        # vs ~0.50 self-play). All four guards are required: no expected regime supplied
        # (--promote and every non-sweep caller) -> inert; an absent/null recorded marker is
        # UNKNOWN and is never guessed at (T57/D8 — guessing would move an operator's file on an
        # inference); equal regimes are compatible; and an empty combinations map has nothing to
        # preserve, mirroring T68's `if combinations` guard above.
        stored_naive_opponents = self._data.get("naive_opponents")
        if (
            self._expected_naive_opponents is not None
            and stored_naive_opponents is not None
            and stored_naive_opponents != self._expected_naive_opponents
            and combinations
        ):
            return (
                f"opponent-regime change: this store accumulated its evidence under "
                f"naive_opponents={stored_naive_opponents} but this run is "
                f"naive_opponents={self._expected_naive_opponents} — a DIFFERENT estimand "
                f"(~0.84 naive vs ~0.50 self-play), so the two evidence pools cannot be pooled"
            )
        return None

    def _quarantine_if_incompatible(self) -> None:
        """Quarantine-and-restart the store when it is structurally incompatible, else no-op (T68/D3).

        Run during construction (from _load), before the manager is used for any read/write, so
        no reader can ever consume a pre-fix mixture as if it were same-reference (the no-silent-
        re-pool guarantee).
        """
        reason = self._incompatibility_reason()
        if reason is not None:
            self._quarantine_and_restart(reason)

    def _quarantine_and_restart(self, reason: str) -> None:
        """Preserve the incompatible store on disk and restart empty (T68/D3 — shared primitive).

        Emits a loud WARNING naming the reason, RENAMES (never deletes) the store file to a
        timestamped sibling so the old data is retained for the operator, and resets in-memory
        state to the empty shape. The rename preserves the atomic-write invariant: the live path
        is free for the next _save. The sibling name is disambiguated with an ascending numeric
        suffix when it is already taken (T57/D7), so a repeat quarantine can never overwrite an
        earlier archive.

        Args:
            reason (str): Why the store is being quarantined (from _incompatibility_reason).
        """
        stamp = datetime.datetime.now().strftime("%Y-%m-%dT%H%M")
        base_name = f"{self._results_path.name}.quarantined-{stamp}"
        quarantine_path = self._results_path.with_name(base_name)
        # T57/D7: the stamp is MINUTE-resolution and Path.rename SILENTLY REPLACES an existing
        # destination on POSIX. Under T68 a collision was unreachable (the structural trigger
        # fires at most once per store); T57's regime trigger can fire repeatedly for one store
        # (a regime toggled back and forth), and two quarantines can land inside one clock
        # minute during a smoke run or a scripted pair of --sweep invocations. Disambiguate with
        # an ascending suffix so an earlier archive is NEVER destroyed — otherwise the WARNING
        # below would claim a preservation the code does not hold.
        collision_index = 2
        while quarantine_path.exists():
            quarantine_path = self._results_path.with_name(f"{base_name}-{collision_index}")
            collision_index += 1
        logger.warning(
            f"QUARANTINING incompatible sweep store {self._results_path} — {reason}. "
            f"Renaming to {quarantine_path} (old data preserved, NOT deleted) and starting empty."
        )
        self._results_path.rename(quarantine_path)
        self._data = self._empty_data()

    @staticmethod
    def compute_input_fingerprint(
        strategy_ids: List[str],
        baseline_params: Dict[str, float],
        num_values: int,
        confidence: float,
        min_effect_size: float,
        min_games: int,
        base_seed: int,
        naive_opponents: bool,
    ) -> str:
        """Compute the sweep input fingerprint (D2/T30).

        Returns a sha256 hex digest over a pinned canonical JSON serialization of the
        inputs that fully determine the per-config search space and adoption decision:
        the sorted strategy ids, the baseline param anchor, the grid density, the three
        significance-gate parameters (confidence, minimum effect size, minimum games),
        and the run's base seed. The canonical form is pinned (``sort_keys=True``, compact
        separators) so recomputing on the same inputs always yields the same digest and
        any changed input yields a different one — so changing any gate parameter between
        runs invalidates a stale checkpoint while an unchanged one resumes.

        Including the base seed ensures that an unseeded resume (each run gets a fresh
        auto-seed) produces a fingerprint mismatch and starts fresh rather than silently
        mixing seed pools across runs. An explicit ``--seed N`` resume yields the same
        fingerprint and resumes correctly.

        Including the opponent regime (T57/D1) ensures that toggling ``--naive-opponents``
        between two runs at the same pinned ``--seed`` invalidates the checkpoint: the regime
        changes the ESTIMAND (~0.84 naive vs ~0.50 self-play), not merely the sample, so a
        checkpoint measured under the other regime must never be continued. ``--sims`` stays
        deliberately EXCLUDED (T57/D2): under CRN the per-task key is
        ``(base_seed, season_folder, sim_id)`` over ``range(num_simulations)``, so a larger
        ``--sims`` re-draws the same first N tasks and appends new ones — additive evidence on
        the same estimand, which must keep resuming. NOTE this digest drives the RESUME
        decision ONLY; the quarantine-and-restart trigger keys on the regime ALONE (T57/D4).

        Scope is strategy ids only (not draft_order content) — in-place edits to a
        strategy under the same id are deliberately not detected this slice (D2).

        Args:
            strategy_ids (List[str]): Strategy identifiers (filenames) in the run.
            baseline_params (Dict[str, float]): The 6-param baseline anchor.
            num_values (int): Grid density per parameter.
            confidence (float): Adoption-gate one-sided confidence level.
            min_effect_size (float): Adoption-gate minimum accumulated-rate effect.
            min_games (int): Adoption-gate minimum accumulated games per combination.
            base_seed (int): The run's base seed (auto-assigned or from ``--seed N``).
            naive_opponents (bool): The run's opponent regime — True under
                ``--naive-opponents`` (the legacy ~0.84 field), False for the self-play
                default (~0.50). A ``store_true`` argparse flag, so always a plain bool,
                which canonicalizes cleanly under ``json.dumps(..., sort_keys=True)``.

        Returns:
            str: The sha256 hex digest of the canonical input serialization.
        """
        payload = {
            "strategy_ids": sorted(strategy_ids),
            "baseline_params": baseline_params,
            "num_values": num_values,
            "confidence": confidence,
            "min_effect_size": min_effect_size,
            "min_games": min_games,
            "base_seed": base_seed,
            "naive_opponents": naive_opponents,
        }
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    @staticmethod
    def make_combo_key(strategy_id: str, param_values: Dict[str, float]) -> str:
        """
        Build the canonical combination key from a strategy id and param values.

        The key is a readable, deterministic string: the strategy id followed by each
        of the 6 params (in fixed DRAFT_SWEEP_PARAMS order) as NAME=value. Values are
        assumed already normalized to precision (the sweep produces them via
        generate_candidate_values / apply_draft_overrides), so equal combinations always
        produce equal keys across runs.

        Args:
            strategy_id (str): Strategy identifier (e.g., the strategy filename).
            param_values (Dict[str, float]): The 6 draft-side param values.

        Returns:
            str: The canonical combination key.
        """
        parts = [strategy_id] + [f"{p}={param_values[p]}" for p in DRAFT_SWEEP_PARAMS]
        return "|".join(parts)

    @staticmethod
    def make_reference_key(incumbent_param_values: Optional[Dict[str, float]]) -> str:
        """Build the by_reference bucket key identifying the incumbent an eval was taken against (T68/D1).

        Mirrors make_combo_key's readable value-formatting — the 6 params (in fixed
        DRAFT_SWEEP_PARAMS order) as NAME=value — but WITHOUT the strategy_id prefix, which
        is redundant within a combo row (the incumbent is always the same strategy's config
        with different params). The no-incumbent (symmetric self-play) case maps to the
        distinguished literal sentinel "self_play".

        Args:
            incumbent_param_values (Optional[Dict[str, float]]): The 6-param incumbent set the
                nine opponents drafted with, or None for the symmetric self-play baseline /
                carry-over anchor.

        Returns:
            str: The reference key — "self_play" when incumbent_param_values is None, else the
                NAME=value tail over DRAFT_SWEEP_PARAMS order.
        """
        if incumbent_param_values is None:
            return "self_play"
        return "|".join(f"{p}={incumbent_param_values[p]}" for p in DRAFT_SWEEP_PARAMS)

    def update(
        self,
        strategy_id: str,
        param_values: Dict[str, float],
        win_rate: float,
        wins: int,
        games: int,
        incumbent_param_values: Optional[Dict[str, float]] = None,
    ) -> None:
        """
        Record the result of one combination evaluation.

        Creates the record on first sight (storing strategy_id + param_values), then
        accumulates wins/games, increments total_runs, updates last_run, and raises
        best_single_run_win_rate when win_rate exceeds it (migrating any legacy
        best_win_rate key to the new name on write). Writes atomically after every call.

        Args:
            strategy_id (str): Strategy identifier.
            param_values (Dict[str, float]): The 6 draft-side param values.
            win_rate (float): Win rate from this evaluation (0.0-1.0).
            wins (int): Wins in this evaluation batch.
            games (int): Total games in this evaluation batch (wins + losses).
            incumbent_param_values (Optional[Dict[str, float]]): The incumbent the nine
                opponents drafted with for this evaluation; None (default) for the symmetric
                self-play baseline / carry-over anchor (T68/D1). The wins/games accumulate into
                by_reference[make_reference_key(incumbent_param_values)] so evaluations against
                different references are NEVER pooled into one rate.
        """
        key = self.make_combo_key(strategy_id, param_values)
        if key not in self._data["combinations"]:
            self._data["combinations"][key] = {
                "strategy_id": strategy_id,
                "param_values": dict(param_values),
                "best_single_run_win_rate": 0.0,
                "by_reference": {},
                "total_wins": 0,
                "total_games": 0,
                "total_runs": 0,
                "last_run": "",
            }
        entry = self._data["combinations"][key]
        # T68/D1: accumulate into the per-reference bucket, NEVER a single blended total. The
        # setdefault tolerates a mid-life record predating this key (quarantine removes pre-fix
        # records, so in practice this fires only on a freshly created record).
        by_reference = entry.setdefault("by_reference", {})
        reference_key = self.make_reference_key(incumbent_param_values)
        bucket = by_reference.setdefault(reference_key, {"wins": 0, "games": 0})
        bucket["wins"] += wins
        bucket["games"] += games
        entry["total_runs"] = entry.get("total_runs", 0) + 1
        # T68/D1: total_wins / total_games are a DERIVED cross-bucket SUM kept for back-compat and
        # human inspection ONLY — never again a ranking or report-display input (both readers now
        # read by_reference). Recomputed (not incremented) so they can never drift from the buckets.
        entry["total_wins"] = sum(b["wins"] for b in by_reference.values())
        entry["total_games"] = sum(b["games"] for b in by_reference.values())
        entry["last_run"] = datetime.date.today().isoformat()
        # D4: read-fallback (new key, else legacy ``best_win_rate``) so an old-schema entry
        # loaded from the live store never KeyErrors; then write the new key and pop the legacy
        # key (migrate-on-write) — ``_save`` json.dumps the full entry, so a set-only write would
        # persist both keys side by side.
        prior_best = entry.get("best_single_run_win_rate", entry.get("best_win_rate", 0.0))
        entry["best_single_run_win_rate"] = max(prior_best, win_rate)
        entry.pop("best_win_rate", None)
        self._data["last_updated"] = datetime.date.today().isoformat()
        self._save()

    def _save(self) -> None:
        """Write _data atomically to _results_path via tmp file -> rename."""
        try:
            atomic_write_json(
                self._data,
                self._results_path,
                error_message=f"Failed to save sweep results to {self._results_path}",
            )
        except FileOperationError:
            with error_context("saving sweep results", component="SweepResultsManager",
                               file_path=str(self._results_path)):
                raise
        logger.debug(f"Sweep results saved to {self._results_path}")

    def set_input_fingerprint(self, fingerprint: str) -> None:
        """Set the top-level input fingerprint and persist atomically.

        Args:
            fingerprint (str): The sha256 hex digest from compute_input_fingerprint.
        """
        self._data["input_fingerprint"] = fingerprint
        self._data["last_updated"] = datetime.date.today().isoformat()
        self._save()

    def get_input_fingerprint(self) -> str:
        """Return the stored input fingerprint, or "" when unset.

        Returns:
            str: The stored sha256 hex digest, or an empty string when never set.
        """
        return self._data.get("input_fingerprint", "")

    def set_discriminating(self, value: bool) -> None:
        """Set the top-level discriminating flag and persist atomically (T54/D3).

        Recorded once per sweep run to certify the store was produced under the
        measured-vs-incumbent (discriminating) regime. Read by config_promoter to
        fail-safe-block a promote from a non-discriminating (or pre-fix) store.

        Args:
            value (bool): True to certify the store as discriminating.
        """
        self._data["discriminating"] = value
        self._data["last_updated"] = datetime.date.today().isoformat()
        self._save()

    def get_discriminating(self) -> bool:
        """Return the stored discriminating flag, or False when absent (T54/D3).

        Returns:
            bool: The stored flag; False when never set (a pre-fix store), so absence
                fail-safe-blocks a promote.
        """
        return self._data.get("discriminating", False)

    def set_naive_opponents(self, value: bool) -> None:
        """Set the top-level opponent-regime marker and persist atomically (T57/D8).

        Recorded once per sweep launch to record WHICH opponent regime the store's
        accumulated evidence was drawn under. Read at load time by _incompatibility_reason,
        which quarantines-and-restarts a store whose recorded regime differs from the run's
        (a different estimand). Mirrors set_discriminating's shape — same top-level key, same
        last_updated bump, same atomic _save path; no new mechanism.

        Args:
            value (bool): True when the run uses --naive-opponents, else False (self-play).
        """
        self._data["naive_opponents"] = value
        self._data["last_updated"] = datetime.date.today().isoformat()
        self._save()

    def get_naive_opponents(self) -> Optional[bool]:
        """Return the stored opponent-regime marker, or None when unknown (T57/D8).

        Deliberately has NO False default — the one intentional divergence from
        get_discriminating, whose absent case must fail-safe BLOCK a promote. Here False is a
        REAL regime value (self-play) and so cannot double as "unknown"; a pre-T57 store
        records no regime and nothing can recover it, and an unknown regime must never move an
        operator's file on a guess. The marker is written on every sweep launch, so the unknown
        state self-heals after one run.

        Returns:
            Optional[bool]: True/False when recorded; None when the key is absent or null.
        """
        return self._data.get("naive_opponents")

    def mark_config_progress(
        self,
        strategy_id: str,
        status: str,
        best_param_values: Dict[str, float],
        best_combo_win_rate: float,
    ) -> None:
        """Upsert a per-config convergence entry and persist atomically (D3).

        Records the config's current best params, best win rate, completion status,
        and the write date under ``convergence[strategy_id]``. Overwrites any prior
        entry for the same id (upsert) and writes via the atomic tmp->rename save so
        a Ctrl+C / crash never leaves a half-written file.

        Args:
            strategy_id (str): Strategy identifier (filename) keying the entry.
            status (str): "converged", "in_progress", or "starved" (T61/D4 — a terminal
                mark for a run whose games-per-evaluation could never clear the adoption
                gate's floor, so no parameter could be adopted; deliberately NOT
                "converged" so is_all_converged stays False and a later resume re-tunes).
            best_param_values (Dict[str, float]): The config's current best 6 params.
            best_combo_win_rate (float): The config's current accumulated best-combo
                win rate (total_wins/total_games of the running-best combo, NOT a
                single-run rate). Load-bearing for resume.

        Raises:
            ConfigurationError: If status is not "converged", "in_progress", or "starved".
        """
        # T61/D4: the whitelist is WIDENED by exactly one value, never removed — an unknown or
        # typo'd status must still be rejected so garbage can never enter the persisted record.
        if status not in ("converged", "in_progress", "starved"):
            raise ConfigurationError(
                f"mark_config_progress received invalid status {status!r} for "
                f"strategy {strategy_id!r}; expected 'converged', 'in_progress', or 'starved'"
            )
        self._data["convergence"][strategy_id] = {
            "status": status,
            "best_param_values": dict(best_param_values),
            "best_combo_win_rate": best_combo_win_rate,
            "updated": datetime.date.today().isoformat(),
        }
        self._data["last_updated"] = datetime.date.today().isoformat()
        self._save()

    def get_all_combinations(self) -> Dict[str, Dict]:
        """
        Return all combination entries from the sweep results.

        Returns:
            Dict[str, Dict]: Combination key -> entry dict with keys 'strategy_id',
                'param_values', 'best_single_run_win_rate', 'by_reference'
                (per-reference {wins, games} buckets, incl. the 'self_play' bucket — T68/D1),
                'total_wins', 'total_games' (a DERIVED cross-bucket sum, NON-ranking),
                'total_runs', 'last_run'.
        """
        return self._data["combinations"]

    def get_combination(self, strategy_id: str, param_values: Dict[str, float]) -> Optional[Dict]:
        """Return the stored entry for one combination, or None if not recorded.

        A single-entry lookup keyed by make_combo_key — avoids re-scanning the full
        get_all_combinations() map when only one combination's accumulated counts are
        needed (SweepTournament._accumulated_rate reads a combination's rate this way). NOTE:
        as of T58 the adoption gate no longer reads the store at all — it decides on the
        trial's fresh head-to-head evaluation against the 0.50 null.

        Args:
            strategy_id (str): Strategy identifier keying the combination.
            param_values (Dict[str, float]): The 6 draft-side param values.

        Returns:
            Optional[Dict]: The entry dict ('strategy_id', 'param_values',
                'best_single_run_win_rate', 'by_reference' — per-reference {wins, games} buckets
                incl. 'self_play' (T68/D1), 'total_wins', 'total_games' (a DERIVED cross-bucket
                sum, NON-ranking), 'total_runs', 'last_run'),
                or None when the combination has never been recorded.
        """
        key = self.make_combo_key(strategy_id, param_values)
        return self._data["combinations"].get(key)

    def get_config_convergence(self, strategy_id: str) -> Optional[Dict]:
        """Return the per-config convergence entry for a strategy id, or None.

        Args:
            strategy_id (str): Strategy identifier keying the convergence map.

        Returns:
            Optional[Dict]: The entry dict ('status', 'best_param_values',
                'best_combo_win_rate', 'updated'), or None when no entry exists.
        """
        return self._data["convergence"].get(strategy_id)

    def get_all_convergence(self) -> Dict[str, Dict]:
        """Return the full per-config convergence map.

        Returns:
            Dict[str, Dict]: strategy_id -> per-config convergence entry.
        """
        return self._data["convergence"]

    def is_all_converged(self, strategy_ids: List[str]) -> bool:
        """Return True iff every given id has a convergence entry marked converged (D3).

        This is the derived "all complete" terminal state — there is no stored
        all_complete flag. An empty strategy_ids list is vacuously True.

        Args:
            strategy_ids (List[str]): The strategy ids the run covers.

        Returns:
            bool: True iff every id has a 'converged' convergence entry.
        """
        return all(
            self._data["convergence"].get(sid, {}).get("status") == "converged"
            for sid in strategy_ids
        )
