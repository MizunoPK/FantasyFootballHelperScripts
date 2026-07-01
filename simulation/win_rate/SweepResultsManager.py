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

    def __init__(self, results_path: Path) -> None:
        """
        Initialize the manager and load existing sweep results from disk.

        Args:
            results_path (Path): Path to win_rate_sweep_results.json. File need not
                exist — if absent, starts with an empty data structure.
        """
        self._results_path = results_path
        self._load()

    def _load(self) -> None:
        """Load sweep results from disk, or initialize empty if file absent or corrupted.

        On a successful load of an existing file, defaults the checkpoint keys
        ``input_fingerprint`` and ``convergence`` when absent, so an old-schema
        (combinations-only) file loads cleanly while its existing ``combinations``
        are preserved untouched.
        """
        if not self._results_path.exists():
            logger.debug(f"No sweep results file at {self._results_path} — starting fresh")
            self._data = {"last_updated": "", "combinations": {}, "input_fingerprint": "", "convergence": {}}
            return
        try:
            with open(self._results_path, 'r', encoding='utf-8') as f:
                self._data = json.load(f)
            logger.debug(f"Loaded sweep results: {len(self._data.get('combinations', {}))} combinations")
        except json.JSONDecodeError as e:
            logger.warning(f"Corrupted sweep results at {self._results_path}: {e} — starting fresh")
            self._data = {"last_updated": "", "combinations": {}, "input_fingerprint": "", "convergence": {}}
            return
        self._data.setdefault("combinations", {})
        self._data.setdefault("input_fingerprint", "")
        self._data.setdefault("convergence", {})

    @staticmethod
    def compute_input_fingerprint(
        strategy_ids: List[str],
        baseline_params: Dict[str, float],
        num_values: int,
        confidence: float,
        min_effect_size: float,
        min_games: int,
        base_seed: int,
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

    def update(
        self,
        strategy_id: str,
        param_values: Dict[str, float],
        win_rate: float,
        wins: int,
        games: int,
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
        """
        key = self.make_combo_key(strategy_id, param_values)
        if key not in self._data["combinations"]:
            self._data["combinations"][key] = {
                "strategy_id": strategy_id,
                "param_values": dict(param_values),
                "best_single_run_win_rate": 0.0,
                "total_wins": 0,
                "total_games": 0,
                "total_runs": 0,
                "last_run": "",
            }
        entry = self._data["combinations"][key]
        entry["total_runs"] = entry.get("total_runs", 0) + 1
        entry["total_wins"] = entry.get("total_wins", 0) + wins
        entry["total_games"] = entry.get("total_games", 0) + games
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
        tmp_path = self._results_path.with_suffix('.tmp')
        try:
            with open(tmp_path, 'w', encoding='utf-8') as f:
                json.dump(self._data, f, indent=2)
            tmp_path.replace(self._results_path)
            logger.debug(f"Sweep results saved to {self._results_path}")
        except (PermissionError, OSError) as e:
            with error_context("saving sweep results", component="SweepResultsManager",
                               file_path=str(self._results_path)):
                raise FileOperationError(
                    f"Failed to save sweep results to {self._results_path}: {e}"
                ) from e

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
            status (str): "converged" or "in_progress".
            best_param_values (Dict[str, float]): The config's current best 6 params.
            best_combo_win_rate (float): The config's current accumulated best-combo
                win rate (total_wins/total_games of the running-best combo, NOT a
                single-run rate). Load-bearing for resume.

        Raises:
            ConfigurationError: If status is not "converged" or "in_progress".
        """
        if status not in ("converged", "in_progress"):
            raise ConfigurationError(
                f"mark_config_progress received invalid status {status!r} for "
                f"strategy {strategy_id!r}; expected 'converged' or 'in_progress'"
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
                'param_values', 'best_single_run_win_rate', 'total_wins', 'total_games',
                'total_runs', 'last_run'.
        """
        return self._data["combinations"]

    def get_combination(self, strategy_id: str, param_values: Dict[str, float]) -> Optional[Dict]:
        """Return the stored entry for one combination, or None if not recorded.

        A single-entry lookup keyed by make_combo_key — avoids re-scanning the full
        get_all_combinations() map when only one combination's accumulated counts are
        needed (the T31 adoption gate reads the trial and running-best entries this way).

        Args:
            strategy_id (str): Strategy identifier keying the combination.
            param_values (Dict[str, float]): The 6 draft-side param values.

        Returns:
            Optional[Dict]: The entry dict ('strategy_id', 'param_values',
                'best_single_run_win_rate', 'total_wins', 'total_games', 'total_runs', 'last_run'),
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
