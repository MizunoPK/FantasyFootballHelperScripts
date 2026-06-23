"""
Config Promoter

Lands the winning combination from a multi-parameter sweep into the live
league_config.json. Reads the accumulated sweep results, ranks them by cumulative
win rate, resolves the winning strategy's DRAFT_ORDER, and writes that DRAFT_ORDER
plus the seven draft-side parameters onto league_config.json via the shared
apply_draft_overrides helper — preserving every other key.

This is the one component that mutates the operator's live config. The write is
atomic (tmp -> rename) so a crash mid-write cannot corrupt the file, and a
read-only git dirty-state check warns before overwriting uncommitted edits (the
only state git cannot recover). Recovery otherwise relies on git: league_config.json
is tracked, so a promote is reviewable / revertable via git diff / git checkout.

Author: Kai Mizuno
"""

# Standard library
import json
import subprocess
from pathlib import Path
from typing import Any, Dict

# Local
from simulation.win_rate.config_overrides import apply_draft_overrides
from simulation.win_rate.strategy_loader import load_valid_strategies
from simulation.win_rate.sweep_summary import rank_combinations
from utils.error_handler import ConfigurationError, FileOperationError
from utils.LoggingManager import get_logger

logger = get_logger()


def promote_best_combination(
    store,
    data_folder: Path,
    config_path: Path = Path("data/configs/league_config.json"),
) -> Dict[str, Any]:
    """
    Write the best-ranked sweep combination into league_config.json.

    Ranks the store's combinations by cumulative win rate, takes the #1, resolves
    that strategy's DRAFT_ORDER, and applies it plus the seven draft-side params
    onto config_path via apply_draft_overrides (all other keys preserved). The
    write is atomic; a git dirty-state warning is logged (but does not block) when
    config_path has uncommitted changes.

    Args:
        store: A SweepResultsManager exposing get_all_combinations().
        data_folder (Path): Simulation data root, used to resolve the winning
            strategy's DRAFT_ORDER via load_valid_strategies.
        config_path (Path): The live league_config.json to overwrite.

    Returns:
        Dict[str, Any]: Exactly {"strategy_id", "param_values", "win_rate", "games"}
            describing the promoted combination.

    Raises:
        ConfigurationError: If the store is empty, the winning strategy cannot be
            resolved, or config_path is missing/corrupt. No write occurs in any of
            these cases.
        FileOperationError: If the atomic write itself fails (config_path is left
            untouched and no orphaned .tmp remains).
    """
    combinations = store.get_all_combinations()
    if not combinations:
        raise ConfigurationError(
            "No sweep combinations to promote — run the sweep first."
        )

    best = rank_combinations(combinations)[0]
    strategy_id = best["strategy_id"]
    param_values = best["param_values"]

    draft_order = _resolve_draft_order(strategy_id, data_folder)
    base_config = _read_config(config_path)
    new_config = apply_draft_overrides(base_config, draft_order, param_values)

    if _has_uncommitted_changes(config_path):
        logger.warning(
            f"{config_path} has uncommitted changes — promotion will overwrite "
            f"them (git cannot recover uncommitted edits)."
        )

    _atomic_write_json(new_config, config_path)

    logger.info(
        f"Promoted {strategy_id} to {config_path} "
        f"(win_rate={best['win_rate']:.3f} over {best['games']} games)."
    )
    return {
        "strategy_id": strategy_id,
        "param_values": param_values,
        "win_rate": best["win_rate"],
        "games": best["games"],
    }


def _resolve_draft_order(strategy_id: str, data_folder: Path) -> list:
    """
    Resolve the winning strategy's DRAFT_ORDER by matching its filename.

    Linear-searches the (filename, DRAFT_ORDER, name) triples from
    load_valid_strategies for filename == strategy_id.

    Raises:
        ConfigurationError: If no strategy matches, or no valid strategy files
            exist (load_valid_strategies raises FileNotFoundError).
    """
    try:
        strategies, _ = load_valid_strategies(data_folder)
    except FileNotFoundError as e:
        raise ConfigurationError(
            f"Cannot resolve winning strategy {strategy_id}: {e}"
        ) from e

    for filename, draft_order, _name in strategies:
        if filename == strategy_id:
            return draft_order

    raise ConfigurationError(
        f"Winning strategy {strategy_id} not found among valid strategies"
    )


def _read_config(config_path: Path) -> dict:
    """
    Read a config file as raw JSON, preserving its exact structure.

    Raises:
        ConfigurationError: If config_path is missing or not valid JSON.
    """
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise ConfigurationError(f"Cannot read config {config_path}: {e}") from e


def _has_uncommitted_changes(path: Path) -> bool:
    """
    Return True if `path` has uncommitted git changes, False otherwise.

    Runs `git status --porcelain <path>` read-only. Degrades gracefully: any
    failure (git missing, not a repo, non-zero exit, subprocess error) returns
    False so the promotion is never blocked or crashed by the git probe.
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain", str(path)],
            capture_output=True,
            text=True,
            check=True,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return bool(result.stdout.strip())


def _atomic_write_json(data: dict, path: Path) -> None:
    """
    Write `data` as JSON to `path` atomically via tmp file -> rename.

    Mirrors SweepResultsManager._save: a mid-write failure leaves `path`
    untouched, and the orphaned .tmp is removed before re-raising.

    Raises:
        FileOperationError: On any OSError/PermissionError during the write.
    """
    tmp_path = path.with_suffix(".tmp")
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        tmp_path.replace(path)
    except (PermissionError, OSError) as e:
        tmp_path.unlink(missing_ok=True)
        raise FileOperationError(f"Failed to write config to {path}: {e}") from e
