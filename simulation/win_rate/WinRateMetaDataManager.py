import json
import datetime
from pathlib import Path
from typing import Dict

from utils.LoggingManager import get_logger
from utils.error_handler import create_component_error_handler, error_context, FileOperationError

logger = get_logger()
_error_handler = create_component_error_handler("WinRateMetaDataManager")


class WinRateMetaDataManager:
    """
    Manages win_rate_meta_data.json persistence lifecycle.

    Loads file on construction (initializes empty if absent or corrupted).
    Exposes update() for recording strategy evaluation results and writes
    atomically after every call.
    """

    def __init__(self, meta_data_path: Path) -> None:
        """
        Initialize manager and load existing meta data from disk.

        Args:
            meta_data_path (Path): Path to win_rate_meta_data.json.
                File need not exist — if absent, starts with empty data structure.
        """
        self._meta_data_path = meta_data_path
        self._load()

    def _load(self) -> None:
        """Load meta data from disk, or initialize empty structure if file absent or corrupted."""
        if not self._meta_data_path.exists():
            logger.debug(f"No meta data file at {self._meta_data_path} — starting fresh")
            self._data = {"last_updated": "", "strategies": {}}
            return
        try:
            with open(self._meta_data_path, 'r', encoding='utf-8') as f:
                self._data = json.load(f)
            logger.debug(f"Loaded meta data: {len(self._data.get('strategies', {}))} strategies")
        except json.JSONDecodeError as e:
            logger.warning(f"Corrupted meta data at {self._meta_data_path}: {e} — starting fresh")
            self._data = {"last_updated": "", "strategies": {}}

    def update(self, strategy_filename: str, name: str, win_rate: float, wins: int, games: int) -> None:
        """
        Record result of one strategy evaluation run.

        Always increments total_runs and updates last_run. Updates
        best_win_rate only if win_rate strictly exceeds the stored best.
        Accumulates total_wins and total_games cumulatively across all calls.
        Atomically writes updated data to disk after every call.

        Args:
            strategy_filename (str): Filename key (e.g., '1_zero_rb.json').
            name (str): Human-readable strategy name from strategy file's 'name' field.
            win_rate (float): Win rate from this evaluation run (0.0-1.0).
            wins (int): Number of wins in this evaluation batch.
            games (int): Total games in this evaluation batch (wins + losses).
        """
        if strategy_filename not in self._data["strategies"]:
            self._data["strategies"][strategy_filename] = {
                "name": "",
                "best_win_rate": 0.0,
                "total_wins": 0,
                "total_games": 0,
                "total_runs": 0,
                "last_run": "",
            }
        entry = self._data["strategies"][strategy_filename]
        entry["name"] = name
        entry["total_runs"] = entry.get("total_runs", 0) + 1
        entry["total_wins"] = entry.get("total_wins", 0) + wins
        entry["total_games"] = entry.get("total_games", 0) + games
        entry["last_run"] = datetime.date.today().isoformat()
        if win_rate > entry["best_win_rate"]:
            old = entry["best_win_rate"]
            entry["best_win_rate"] = win_rate
            logger.info(f"New best for {strategy_filename}: {win_rate:.3f} (prev: {old:.3f})")
        self._data["last_updated"] = datetime.date.today().isoformat()
        self._save()

    def _save(self) -> None:
        """Write _data atomically to _meta_data_path via tmp file -> rename."""
        tmp_path = self._meta_data_path.with_suffix('.tmp')
        try:
            with open(tmp_path, 'w', encoding='utf-8') as f:
                json.dump(self._data, f, indent=2)
            tmp_path.replace(self._meta_data_path)
            logger.debug(f"Meta data saved to {self._meta_data_path}")
        except (PermissionError, OSError) as e:
            with error_context("saving meta data", component="WinRateMetaDataManager",
                               file_path=str(self._meta_data_path)):
                raise FileOperationError(
                    f"Failed to save meta data to {self._meta_data_path}: {e}"
                ) from e

    def get_all_strategies(self) -> Dict[str, Dict]:
        """
        Return all strategy entries from the meta data.

        Returns:
            Dict[str, Dict]: Strategy filename -> entry dict with keys
                'name', 'best_win_rate', 'total_wins', 'total_games',
                'total_runs', 'last_run'.
        """
        return self._data["strategies"]
