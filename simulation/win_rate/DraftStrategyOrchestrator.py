import copy
import json
from pathlib import Path

from utils.LoggingManager import get_logger
from utils.error_handler import create_component_error_handler, FileOperationError
from league_helper.util.ConfigManager import ConfigManager
from simulation.win_rate.ParallelLeagueRunner import ParallelLeagueRunner
from simulation.win_rate.WinRateMetaDataManager import WinRateMetaDataManager

logger = get_logger()
_error_handler = create_component_error_handler("DraftStrategyOrchestrator")

MIN_VALID_PLAYERS = 150


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
                if not self._validate_season_data(season_folder):
                    continue

                self._runner.set_data_folder(season_folder)
                results = self._runner.run_simulations_for_config(config, self._num_simulations)

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

    def _validate_season_data(self, season_folder: Path) -> bool:
        """
        Return True if season_folder contains at least MIN_VALID_PLAYERS undrafted
        players with positive projected_points in week_01; False otherwise.

        Args:
            season_folder (Path): Season directory (e.g. data/2023/).

        Returns:
            bool: True if season data is valid for simulation, False otherwise.
        """
        week_01_folder = season_folder / "weeks" / "week_01"
        if not week_01_folder.is_dir():
            logger.warning(f"Season {season_folder.name}: week_01 folder missing — skipping")
            return False

        position_files = [
            "qb_data.json",
            "rb_data.json",
            "wr_data.json",
            "te_data.json",
            "k_data.json",
            "dst_data.json",
        ]

        try:
            valid_count = 0
            for position_file in position_files:
                json_file = week_01_folder / position_file
                if not json_file.exists():
                    logger.warning(
                        f"Season {season_folder.name}: Missing {position_file} in week_01"
                    )
                    continue

                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for player_dict in data:
                        drafted_by = player_dict.get("drafted_by", "")
                        projected_points = player_dict.get("projected_points", [])
                        fp_val = projected_points[0] if len(projected_points) > 0 else 0

                        if drafted_by == "" and fp_val > 0:
                            valid_count += 1

            if valid_count < MIN_VALID_PLAYERS:
                logger.warning(
                    f"Season {season_folder.name}: only {valid_count} valid players "
                    f"(need 150+) — skipping"
                )
                return False

            logger.debug(f"Season {season_folder.name}: {valid_count} valid players - OK")
            return True

        except Exception as e:
            logger.warning(
                f"Season {season_folder.name}: Error reading player data: {e}"
            )
            return False
