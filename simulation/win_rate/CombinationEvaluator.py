"""
Combination Evaluator

Evaluates a single (draft strategy + draft-side parameter) combination for the
win-rate parameter sweep. Builds its expensive resources once — the base config,
the ParallelLeagueRunner, and the per-season SimDataLoader caches — and then scores
any combination cheaply on each evaluate() call.

This is the reusable scoring unit the budget-aware sweep tournament calls once per
candidate combination. The strategy-only DraftStrategyOrchestrator will later be
refactored to route through this evaluator (until then its per-season loop is
intentionally duplicated here).

Author: Kai Mizuno
"""

# Standard library
import copy
from pathlib import Path
from typing import Dict, Tuple

# Local
from utils.LoggingManager import get_logger
from utils.error_handler import FileOperationError
from league_helper.util.ConfigManager import ConfigManager
from simulation.win_rate.ParallelLeagueRunner import ParallelLeagueRunner
from simulation.win_rate.SimDataLoader import SimDataLoader
from simulation.win_rate.config_overrides import apply_draft_overrides


class CombinationEvaluator:
    """
    Scores one (DRAFT_ORDER + 7-param) combination across all historical seasons.

    Expensive resources are built once in __init__ and reused across evaluate()
    calls, so a sweep that evaluates thousands of combinations does not re-read
    season data per combination.

    Note: evaluate() is NOT safe for concurrent calls on a single instance — it
    mutates the shared runner's data folder via set_data_folder(). The sweep
    tournament calls it sequentially; parallelism lives inside
    ParallelLeagueRunner.run_simulations_for_config().
    """

    def __init__(
        self,
        data_folder: Path,
        num_simulations: int,
        max_workers: int = 8,
        config_path: Path = Path("data/configs/league_config.json"),
    ) -> None:
        """
        Build the evaluator's reusable resources once.

        Args:
            data_folder (Path): Simulation data root containing 20XX/ season folders.
            num_simulations (int): Simulations per season per evaluate() call.
            max_workers (int): Worker threads for ParallelLeagueRunner.
            config_path (Path): Path to league_config.json; config_path.parent.parent
                is the ConfigManager data root. Defaults to data/configs/league_config.json.

        Raises:
            FileOperationError: If the base config cannot be loaded.
            FileNotFoundError: If no 20XX/ season folders exist under data_folder.
        """
        logger = get_logger()  # KDD-3: resolve at call time so --log-level governs this output

        self._num_simulations = num_simulations

        try:
            cm = ConfigManager(config_path.parent.parent)
            self._base_config = {
                "config_name": cm.config_name,
                "description": cm.description,
                "parameters": dict(cm.parameters),
            }
        except (FileNotFoundError, ValueError) as e:
            raise FileOperationError(f"Failed to load config from {config_path}: {e}") from e

        self._runner = ParallelLeagueRunner(max_workers=max_workers, data_folder=data_folder)

        seasons = sorted(data_folder.glob("20*/"))
        if not seasons:
            raise FileNotFoundError(
                f"No historical season folders (20XX/) found in {data_folder}. "
                "Run compile_historical_data.py first."
            )

        self._season_cache: Dict[Path, Dict[int, Dict]] = {}
        for season_folder in seasons:
            loader = SimDataLoader(season_folder)
            if loader.is_valid:
                self._season_cache[season_folder] = loader.week_data_cache

        if not self._season_cache:
            logger.warning(
                f"No valid season data found under {data_folder} "
                f"({len(seasons)} season folder(s) present but none passed validation) — "
                "evaluate() will return zero games for every combination."
            )

        logger.info(
            f"CombinationEvaluator initialized: {len(self._season_cache)} valid season(s), "
            f"{num_simulations} sims/season, {max_workers} workers"
        )

    @property
    def base_config(self) -> dict:
        """Return a deep copy of the base config (callers read only)."""
        return copy.deepcopy(self._base_config)

    def evaluate(
        self,
        draft_order: list,
        param_values: Dict[str, float],
    ) -> Tuple[int, int, float]:
        """
        Score one combination across all cached seasons.

        Args:
            draft_order (list): The strategy's DRAFT_ORDER array (applied verbatim).
            param_values (Dict[str, float]): The 7 draft-side params (see
                config_overrides.apply_draft_overrides; validated/precision-rounded there).

        Returns:
            Tuple[int, int, float]: (total_wins, total_games, win_rate), aggregated
                across all cached seasons. win_rate is 0.0 when total_games == 0.

        Raises:
            ConfigurationError: Propagated from apply_draft_overrides on a bad param set.
        """
        logger = get_logger()  # KDD-3: resolve at call time so --log-level governs this output

        config = apply_draft_overrides(self._base_config, draft_order, param_values)

        total_wins = 0
        total_losses = 0
        eval_dropped = 0
        eval_requested = 0
        for season_folder, week_data_cache in self._season_cache.items():
            self._runner.set_data_folder(season_folder)
            results = self._runner.run_simulations_for_config(
                config, self._num_simulations, preloaded_week_data=week_data_cache
            )
            # D3: read the runner's per-call drop counters immediately after the call (safe
            # because evaluate() runs the runner sequentially per season — see class docstring).
            eval_dropped += self._runner.last_dropped_count
            eval_requested += self._runner.last_requested_count
            for wins, losses, _ in results:
                total_wins += wins
                total_losses += losses

        if eval_dropped > 0:
            drop_rate = eval_dropped / eval_requested if eval_requested else 0.0
            logger.error(
                f"evaluate dropped {eval_dropped}/{eval_requested} leagues across "
                f"{len(self._season_cache)} season(s) (rate={drop_rate:.1%}) — "
                "win_rate is computed over survivors only"
            )

        total_games = total_wins + total_losses
        win_rate = total_wins / total_games if total_games > 0 else 0.0
        return total_wins, total_games, win_rate
