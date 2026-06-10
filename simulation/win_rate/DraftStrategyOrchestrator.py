import json
import time
from pathlib import Path
from typing import Dict, Optional

from utils.LoggingManager import get_logger
from utils.error_handler import create_component_error_handler
from simulation.win_rate.WinRateMetaDataManager import WinRateMetaDataManager
from simulation.win_rate.CombinationEvaluator import CombinationEvaluator
from simulation.win_rate.config_overrides import extract_draft_param_values

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

        if self._strategy_filter is not None:
            strategy_files = [p for p in strategy_files if p.name == self._strategy_filter]
            if not strategy_files:
                raise FileNotFoundError(
                    f"--strategy filter '{self._strategy_filter}' matched no strategy files in {strategy_dir}"
                )

        file_set = {p.name for p in strategy_files}
        meta_set = set(self._meta_data_manager.get_all_strategies().keys())
        new_strategies = file_set - meta_set
        missing_strategies = meta_set - file_set
        for name in sorted(new_strategies):
            logger.info(f"New strategy detected: {name} — will be tested this run.")
        for name in sorted(missing_strategies):
            logger.warning(f"Strategy file missing: {name} — skipping (entry preserved in meta_data).")

        total_strategies = len(strategy_files)
        skipped_count = 0

        for i, strategy_path in enumerate(strategy_files, 1):
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

            if not self._validate_strategy(strategy_filename, strategy_data):
                skipped_count += 1
                continue

            name = strategy_data.get("name", strategy_path.stem)

            start_time = time.monotonic()
            logger.info(
                f"[{i}/{total_strategies}] Testing: {name} ({strategy_filename}) "
                f"| --sims {self._num_simulations}"
            )

            prior_data = self._meta_data_manager.get_all_strategies().get(strategy_filename, {})
            prior_best = prior_data.get("best_win_rate", -1.0)

            total_wins, total_games, win_rate = self._evaluator.evaluate(
                strategy_data["DRAFT_ORDER"], self._baseline_params
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
            f"Completed pass: {len(strategy_files)} strategies processed, "
            f"{skipped_count} skipped"
        )

    def _validate_strategy(self, strategy_filename: str, strategy_data: dict) -> bool:
        """
        Validate strategy DRAFT_ORDER against REQUIREMENTS.TXT rules (fail-fast per C2).

        Args:
            strategy_filename (str): Filename used for log messages (e.g., '1_zero_rb.json').
            strategy_data (dict): Parsed JSON content of the strategy file.

        Returns:
            bool: True if DRAFT_ORDER passes the type pre-check (rule 0) and all 6
                REQUIREMENTS.TXT rules (rules 1-6); False on first rule failure.
        """
        draft_order = strategy_data.get("DRAFT_ORDER")

        if not isinstance(draft_order, list):
            logger.warning(
                f"Skipping {strategy_filename}: DRAFT_ORDER must be a list "
                f"(got {type(draft_order).__name__})"
            )
            return False

        if len(draft_order) != 15:
            logger.warning(
                f"Skipping {strategy_filename}: DRAFT_ORDER has {len(draft_order)} entries (expected 15)"
            )
            return False

        expected_p_counts = {"QB": 2, "RB": 4, "WR": 4, "FLEX": 1, "TE": 2, "K": 1, "DST": 1}
        actual_p_counts = {pos: 0 for pos in expected_p_counts}
        for entry in draft_order:
            for pos, role in entry.items():
                if role == "P" and pos in actual_p_counts:
                    actual_p_counts[pos] += 1
        for pos, exp in expected_p_counts.items():
            got = actual_p_counts[pos]
            if got != exp:
                logger.warning(
                    f"Skipping {strategy_filename}: invalid P-count for {pos} (expected {exp}, got {got})"
                )
                return False

        qb_p_indices = [i for i, entry in enumerate(draft_order) if entry.get("QB") == "P"]
        for idx in range(len(qb_p_indices) - 1):
            i1, i2 = qb_p_indices[idx], qb_p_indices[idx + 1]
            if i2 == i1 + 1:
                logger.warning(
                    f"Skipping {strategy_filename}: QB P-values must have at least one "
                    f"non-QB-P entry between them (indices {i1} and {i2})"
                )
                return False

        te_p_indices = [i for i, entry in enumerate(draft_order) if entry.get("TE") == "P"]
        for idx in range(len(te_p_indices) - 1):
            i1, i2 = te_p_indices[idx], te_p_indices[idx + 1]
            if i2 == i1 + 1:
                logger.warning(
                    f"Skipping {strategy_filename}: TE P-values must have at least one "
                    f"non-TE-P entry between them (indices {i1} and {i2})"
                )
                return False

        for i, entry in enumerate(draft_order):
            p_values = [v for v in entry.values() if v == "P"]
            s_values = [v for v in entry.values() if v == "S"]
            if i == 14:
                if len(p_values) != 1 or len(s_values) != 0:
                    logger.warning(
                        f"Skipping {strategy_filename}: entry {i} has invalid slot structure "
                        f"(must have exactly one P and at most one S; entry 14 must have only P)"
                    )
                    return False
            else:
                if len(p_values) != 1 or len(s_values) > 1:
                    logger.warning(
                        f"Skipping {strategy_filename}: entry {i} has invalid slot structure "
                        f"(must have exactly one P and at most one S; entry 14 must have only P)"
                    )
                    return False

        final_3 = [
            (12, {"K": "P", "FLEX": "S"}),
            (13, {"DST": "P", "FLEX": "S"}),
            (14, {"FLEX": "P"}),
        ]
        for i, expected_entry in final_3:
            actual_entry = draft_order[i]
            if actual_entry != expected_entry:
                logger.warning(
                    f"Skipping {strategy_filename}: entry {i} must be {expected_entry!r}, "
                    f"got {actual_entry!r}"
                )
                return False

        return True
