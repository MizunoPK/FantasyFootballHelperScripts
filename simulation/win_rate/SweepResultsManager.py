"""
Sweep Results Manager

Manages the win_rate_sweep_results.json persistence lifecycle for the multi-parameter
sweep. Records, per (strategy + the 7 draft-side param values) combination, the
cumulative wins/games, best win rate, and run metadata — accumulating across runs so
re-runs add evidence rather than overwriting it.

This is a dedicated store, separate from the single-axis WinRateMetaDataManager /
win_rate_meta_data.json (which it never reads or writes). It mirrors that manager's
absent/corrupt-tolerant load and atomic (tmp -> rename) save.

Author: Kai Mizuno
"""

# Standard library
import datetime
import json
from pathlib import Path
from typing import Dict

# Local
from utils.LoggingManager import get_logger
from utils.error_handler import create_component_error_handler, error_context, FileOperationError
from simulation.win_rate.param_value_generation import DRAFT_SWEEP_PARAMS

logger = get_logger()
_error_handler = create_component_error_handler("SweepResultsManager")


class SweepResultsManager:
    """
    Manages win_rate_sweep_results.json persistence keyed by parameter combination.

    Loads the file on construction (initializes empty if absent or corrupted). Exposes
    update() for recording one combination evaluation and writes atomically after every
    call. Keyed by a canonical combination string built from the strategy id and the 7
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
        """Load sweep results from disk, or initialize empty if file absent or corrupted."""
        if not self._results_path.exists():
            logger.debug(f"No sweep results file at {self._results_path} — starting fresh")
            self._data = {"last_updated": "", "combinations": {}}
            return
        try:
            with open(self._results_path, 'r', encoding='utf-8') as f:
                self._data = json.load(f)
            logger.debug(f"Loaded sweep results: {len(self._data.get('combinations', {}))} combinations")
        except json.JSONDecodeError as e:
            logger.warning(f"Corrupted sweep results at {self._results_path}: {e} — starting fresh")
            self._data = {"last_updated": "", "combinations": {}}

    @staticmethod
    def make_combo_key(strategy_id: str, param_values: Dict[str, float]) -> str:
        """
        Build the canonical combination key from a strategy id and param values.

        The key is a readable, deterministic string: the strategy id followed by each
        of the 7 params (in fixed DRAFT_SWEEP_PARAMS order) as NAME=value. Values are
        assumed already normalized to precision (the sweep produces them via
        generate_candidate_values / apply_draft_overrides), so equal combinations always
        produce equal keys across runs.

        Args:
            strategy_id (str): Strategy identifier (e.g., the strategy filename).
            param_values (Dict[str, float]): The 7 draft-side param values.

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
        best_win_rate when win_rate exceeds it. Writes atomically after every call.

        Args:
            strategy_id (str): Strategy identifier.
            param_values (Dict[str, float]): The 7 draft-side param values.
            win_rate (float): Win rate from this evaluation (0.0-1.0).
            wins (int): Wins in this evaluation batch.
            games (int): Total games in this evaluation batch (wins + losses).
        """
        key = self.make_combo_key(strategy_id, param_values)
        if key not in self._data["combinations"]:
            self._data["combinations"][key] = {
                "strategy_id": strategy_id,
                "param_values": dict(param_values),
                "best_win_rate": 0.0,
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
        if win_rate > entry["best_win_rate"]:
            entry["best_win_rate"] = win_rate
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

    def get_all_combinations(self) -> Dict[str, Dict]:
        """
        Return all combination entries from the sweep results.

        Returns:
            Dict[str, Dict]: Combination key -> entry dict with keys 'strategy_id',
                'param_values', 'best_win_rate', 'total_wins', 'total_games',
                'total_runs', 'last_run'.
        """
        return self._data["combinations"]
