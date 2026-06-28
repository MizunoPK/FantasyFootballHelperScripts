import time
from pathlib import Path
from typing import Dict, Optional

from utils.LoggingManager import get_logger
from utils.error_handler import create_component_error_handler
from simulation.win_rate.WinRateMetaDataManager import WinRateMetaDataManager
from simulation.win_rate.CombinationEvaluator import CombinationEvaluator
from simulation.win_rate.config_overrides import extract_draft_param_values
from simulation.win_rate.strategy_loader import load_valid_strategies

logger = get_logger()
_error_handler = create_component_error_handler("DraftStrategyOrchestrator")

LOW_SIM_THRESHOLD = 20


class DraftStrategyOrchestrator:
    """
    Enumerates all draft strategy JSON files, simulates each strategy across all
    historical seasons, and records win rates in WinRateMetaDataManager.
    """

    def __init__(
        self,
        data_folder: Path,
        num_simulations: int,
        max_workers: int,
        meta_data_manager: WinRateMetaDataManager,
        config_path: Path = Path("data/configs/league_config.json"),
        strategy_filter: Optional[str] = None,
        naive_opponents: bool = False,
    ) -> None:
        """
        Initialize the orchestrator.

        Args:
            data_folder (Path): Root data folder (contains 20XX/ season folders and
                draft_order_possibilities/ strategy folder).
            num_simulations (int): Number of simulations to run per season per strategy.
            max_workers (int): Number of parallel worker threads for ParallelLeagueRunner.
            meta_data_manager (WinRateMetaDataManager): Instantiated manager for
                reading/writing win_rate_meta_data.json.
            config_path (Path): Path to league_config.json; config_path.parent.parent
                is passed to ConfigManager as the data root, which auto-merges
                week-specific scoring parameters. Defaults to
                data/configs/league_config.json.
            strategy_filter (Optional[str]): If provided, only the strategy file with
                this exact basename is simulated. Comparison is Path.name == strategy_filter
                (exact match, no partial/substring matching). Default None runs all
                strategies.
            naive_opponents (bool): Forwarded to the CombinationEvaluator (and thus the
                ParallelLeagueRunner / SimulatedLeague). False (default) = self-play; True = naive.
        """
        self._data_folder = data_folder
        self._num_simulations = num_simulations
        self._meta_data_manager = meta_data_manager
        self._strategy_filter = strategy_filter

        self._evaluator = CombinationEvaluator(
            data_folder=data_folder,
            num_simulations=num_simulations,
            max_workers=max_workers,
            config_path=config_path,
            naive_opponents=naive_opponents,
        )
        self._baseline_params: Dict[str, float] = extract_draft_param_values(
            self._evaluator.base_config
        )

        if self._num_simulations < LOW_SIM_THRESHOLD:
            logger.warning(
                f"Running {self._num_simulations} simulations per strategy — results may be "
                f"statistically noisy. Consider --sims 30+ for reliable rankings."
            )

    def run(self) -> None:
        """
        Process one full pass through all strategy files.

        Enumerates all JSON files in draft_order_possibilities/, sorted by numeric
        prefix. For each strategy, runs num_simulations across all valid season folders,
        aggregates wins/losses, computes win rate, and calls meta_data_manager.update().
        """
        strategies, skipped_count = load_valid_strategies(self._data_folder, self._strategy_filter)

        file_set = {fname for fname, _, _ in strategies}
        meta_set = set(self._meta_data_manager.get_all_strategies().keys())
        new_strategies = file_set - meta_set
        missing_strategies = meta_set - file_set
        for name in sorted(new_strategies):
            logger.info(f"New strategy detected: {name} — will be tested this run.")
        for name in sorted(missing_strategies):
            logger.warning(f"Strategy file missing: {name} — skipping (entry preserved in meta_data).")

        total_strategies = len(strategies) + skipped_count

        for i, (strategy_filename, draft_order, name) in enumerate(strategies, 1):
            start_time = time.monotonic()
            logger.info(
                f"[{i}/{total_strategies}] Testing: {name} ({strategy_filename}) "
                f"| --sims {self._num_simulations}"
            )

            prior_data = self._meta_data_manager.get_all_strategies().get(strategy_filename, {})
            prior_best = prior_data.get("best_win_rate", -1.0)

            total_wins, total_games, win_rate = self._evaluator.evaluate(
                draft_order, self._baseline_params
            )

            self._meta_data_manager.update(strategy_filename, name, win_rate, total_wins, total_games)

            improved = win_rate > prior_best
            elapsed = int(time.monotonic() - start_time)
            if improved:
                delta = win_rate if prior_best == -1.0 else win_rate - prior_best
                logger.info(
                    f"[{i}/{total_strategies}] {name}: win_rate={win_rate:.3f} "
                    f"| NEW BEST (+{delta:.3f}) | {elapsed}s"
                )
            else:
                logger.info(
                    f"[{i}/{total_strategies}] {name}: win_rate={win_rate:.3f} "
                    f"| best={prior_best:.3f} (no new best) | {elapsed}s"
                )

        logger.info(
            f"Completed pass: {len(strategies) + skipped_count} strategies processed, "
            f"{skipped_count} skipped"
        )
