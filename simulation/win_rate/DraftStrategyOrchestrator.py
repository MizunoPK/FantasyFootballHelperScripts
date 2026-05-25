import copy
import json
from pathlib import Path

from utils.LoggingManager import get_logger
from utils.error_handler import create_component_error_handler, FileOperationError
from league_helper.util.ConfigManager import ConfigManager
from simulation.win_rate.ParallelLeagueRunner import ParallelLeagueRunner
from simulation.win_rate.WinRateMetaDataManager import WinRateMetaDataManager
from simulation.win_rate.SimDataLoader import SimDataLoader

logger = get_logger()
_error_handler = create_component_error_handler("DraftStrategyOrchestrator")


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
        """
        self._data_folder = data_folder
        self._num_simulations = num_simulations
        self._meta_data_manager = meta_data_manager

        try:
            cm = ConfigManager(config_path.parent.parent)
            self._base_config = {
                "config_name": cm.config_name,
                "description": cm.description,
                "parameters": dict(cm.parameters),
            }
        except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
            raise FileOperationError(f"Failed to load config from {config_path}: {e}") from e

        self._runner = ParallelLeagueRunner(max_workers=max_workers, data_folder=data_folder)

        self._seasons = sorted(data_folder.glob("20*/"))
        if not self._seasons:
            raise FileNotFoundError(
                f"No historical season folders (20XX/) found in {data_folder}. "
                "Run compile_historical_data.py first."
            )

        logger.info(
            f"DraftStrategyOrchestrator initialized: {len(self._seasons)} seasons, "
            f"{num_simulations} sims/season, {max_workers} workers"
        )

    def run(self) -> None:
        """
        Process one full pass through all strategy files.

        Enumerates all JSON files in draft_order_possibilities/, sorted by numeric
        prefix. For each strategy, runs num_simulations across all valid season folders,
        aggregates wins/losses, computes win rate, and calls meta_data_manager.update().
        """
        strategy_dir = self._data_folder / "draft_order_possibilities"
        all_json = list(strategy_dir.glob("*.json"))
        numeric_files = []
        for p in all_json:
            prefix = p.stem.split("_")[0]
            if prefix.isdigit():
                numeric_files.append(p)
            else:
                logger.warning(f"Skipping non-numeric strategy file: {p.name}")
        strategy_files = sorted(numeric_files, key=lambda p: int(p.stem.split("_")[0]))
        if not strategy_files:
            logger.warning(f"No strategy JSON files found in {strategy_dir}")
            raise FileNotFoundError(f"No strategy JSON files found in {strategy_dir}")

        skipped_count = 0

        for strategy_path in strategy_files:
            strategy_filename = strategy_path.name

            try:
                with open(strategy_path, "r") as f:
                    strategy_data = json.load(f)
            except json.JSONDecodeError as e:
                logger.warning(f"Skipping {strategy_filename}: JSON parse error: {e}")
                skipped_count += 1
                continue

            if "DRAFT_ORDER" not in strategy_data:
                logger.warning(f"Skipping {strategy_filename}: missing DRAFT_ORDER key")
                skipped_count += 1
                continue

            name = strategy_data.get("name", strategy_path.stem)

            prior_data = self._meta_data_manager.get_all_strategies().get(strategy_filename, {})
            prior_best = prior_data.get("best_win_rate", -1.0)

            config = copy.deepcopy(self._base_config)
            config["parameters"]["DRAFT_ORDER"] = strategy_data["DRAFT_ORDER"]

            total_wins = 0
            total_losses = 0

            for season_folder in self._seasons:
                loader = SimDataLoader(season_folder)
                if not loader.is_valid:
                    continue

                self._runner.set_data_folder(season_folder)
                results = self._runner.run_simulations_for_config(
                    config, self._num_simulations, preloaded_week_data=loader.week_data_cache
                )

                for wins, losses, _ in results:
                    total_wins += wins
                    total_losses += losses

            total_games = total_wins + total_losses
            win_rate = total_wins / total_games if total_games > 0 else 0.0

            self._meta_data_manager.update(strategy_filename, name, win_rate)

            improved = win_rate > prior_best
            stored_best = win_rate if improved else prior_best
            logger.info(
                f"{strategy_filename} ({name}): win_rate={win_rate:.3f}, "
                f"best={stored_best:.3f}"
                + (" NEW BEST" if improved else "")
            )

        logger.info(
            f"Completed pass: {len(strategy_files)} strategies processed, "
            f"{skipped_count} skipped"
        )
