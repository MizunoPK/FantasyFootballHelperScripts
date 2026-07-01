"""
Config Promoter

Lands the winning combination from a multi-parameter sweep into the live
league_config.json. Reads the accumulated sweep results, ranks them by cumulative
win rate, resolves the winning strategy's DRAFT_ORDER, and writes that DRAFT_ORDER
plus the six draft-side parameters onto league_config.json via the shared
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
from simulation.win_rate.config_overrides import (
    apply_draft_overrides,
    extract_draft_param_values,
)
from simulation.win_rate.strategy_loader import load_valid_strategies
from simulation.win_rate.sweep_summary import rank_combinations
from utils.error_handler import ConfigurationError, FileOperationError
from utils.LoggingManager import get_logger

logger = get_logger()


def compute_promotion(
    store,
    data_folder: Path,
    config_path: Path = Path("data/configs/league_config.json"),
) -> Dict[str, Any]:
    """
    Compute the winning combination and the proposed config WITHOUT writing.

    Performs every step of a promotion except the disk write: ranks the store's
    combinations by cumulative win rate, takes the #1, resolves its DRAFT_ORDER,
    reads the current config, and builds the proposed config via
    apply_draft_overrides — then computes the current -> proposed diff of the
    changed draft-side keys. No file is written and config_path is left untouched.
    This is the no-write path behind the bare ``--promote`` preview; the write path
    (promote_best_combination) delegates here for the computation.

    Args:
        store: A SweepResultsManager exposing get_all_combinations().
        data_folder (Path): Simulation data root, used to resolve the winning
            strategy's DRAFT_ORDER via load_valid_strategies.
        config_path (Path): The live league_config.json read for the current values
            (never written here).

    Returns:
        Dict[str, Any]: {"strategy_id", "param_values", "win_rate", "games",
            "new_config", "diff"} — "new_config" is the proposed config dict and
            "diff" maps each changed key to {"current", "proposed"}.

    Raises:
        ConfigurationError: If the store is empty, the winning strategy cannot be
            resolved, config_path is missing/corrupt, or the config is valid JSON but
            structurally incomplete (missing the "parameters" section or an expected
            nested key). No write occurs.
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
    try:
        new_config = apply_draft_overrides(base_config, draft_order, param_values)
        diff = _build_promotion_diff(base_config, new_config)
    except (KeyError, TypeError) as e:
        raise ConfigurationError(
            f"Config at {config_path} is structurally incomplete — missing key or section: {e}"
        ) from e

    return {
        "strategy_id": strategy_id,
        "param_values": param_values,
        "win_rate": best["win_rate"],
        "games": best["games"],
        "new_config": new_config,
        "diff": diff,
    }


def _build_promotion_diff(base_config: dict, new_config: dict) -> Dict[str, Dict[str, Any]]:
    """
    Build the current -> proposed diff of the keys a promotion changes.

    Compares the six draft-side params (via extract_draft_param_values) and
    DRAFT_ORDER between the current (base) and proposed (new) configs, returning
    only the keys whose value changes. Insertion order is the six params (in
    DRAFT_PARAM_LOCATIONS order) followed by DRAFT_ORDER.

    Args:
        base_config (dict): The current live config.
        new_config (dict): The proposed config from apply_draft_overrides.

    Returns:
        Dict[str, Dict[str, Any]]: {changed_key: {"current": ..., "proposed": ...}}.
    """
    diff: Dict[str, Dict[str, Any]] = {}

    current_params = extract_draft_param_values(base_config)
    proposed_params = extract_draft_param_values(new_config)
    for name, current_value in current_params.items():
        proposed_value = proposed_params[name]
        if current_value != proposed_value:
            diff[name] = {"current": current_value, "proposed": proposed_value}

    current_order = base_config["parameters"].get("DRAFT_ORDER")
    proposed_order = new_config["parameters"].get("DRAFT_ORDER")
    if current_order != proposed_order:
        diff["DRAFT_ORDER"] = {"current": current_order, "proposed": proposed_order}

    return diff


def promote_best_combination(
    store,
    data_folder: Path,
    config_path: Path = Path("data/configs/league_config.json"),
) -> Dict[str, Any]:
    """
    Write the best-ranked sweep combination into league_config.json.

    Ranks the store's combinations by cumulative win rate, takes the #1, resolves
    that strategy's DRAFT_ORDER, and applies it plus the six draft-side params
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
    plan = compute_promotion(store, data_folder, config_path)
    new_config = plan["new_config"]

    if _has_uncommitted_changes(config_path):
        logger.warning(
            f"{config_path} has uncommitted changes — promotion will overwrite "
            f"them (git cannot recover uncommitted edits)."
        )

    _atomic_write_json(new_config, config_path)

    logger.info(
        f"Promoted {plan['strategy_id']} to {config_path} "
        f"(win_rate={plan['win_rate']:.3f} over {plan['games']} games)."
    )
    return {
        "strategy_id": plan["strategy_id"],
        "param_values": plan["param_values"],
        "win_rate": plan["win_rate"],
        "games": plan["games"],
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
