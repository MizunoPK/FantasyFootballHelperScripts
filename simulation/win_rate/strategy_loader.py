"""
Strategy Loader

Enumerates and validates draft-strategy files for the win-rate simulation. Globs the
numeric-prefixed draft_order_possibilities/*.json strategy files, validates each
DRAFT_ORDER, and returns the valid (filename, DRAFT_ORDER, name) triples plus the count
of skipped files. Shared by DraftStrategyOrchestrator (strategy-only mode) and the
sweep mode in run_win_rate_simulation.py.

Author: Kai Mizuno
"""

# Standard library
import json
from pathlib import Path
from typing import List, Optional, Tuple

# Local
from utils.LoggingManager import get_logger

logger = get_logger()


def load_valid_strategies(
    data_folder: Path,
    strategy_filter: Optional[str] = None,
) -> Tuple[List[Tuple[str, list, str]], int]:
    """
    Load and validate the draft-strategy files under data_folder/draft_order_possibilities/.

    Args:
        data_folder (Path): Simulation data root (contains draft_order_possibilities/).
        strategy_filter (Optional[str]): If given, only the strategy file with this exact
            basename is returned.

    Returns:
        Tuple[List[Tuple[str, list, str]], int]: (valid_strategies, skipped_count). Each
            valid entry is (filename, DRAFT_ORDER, name) where name = the file's "name"
            field or the filename stem. skipped_count is the number of numeric files
            dropped (JSON error / missing DRAFT_ORDER / failed validation).

    Raises:
        FileNotFoundError: If no numeric strategy files exist, or strategy_filter matches none.
    """
    strategy_dir = data_folder / "draft_order_possibilities"
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

    if strategy_filter is not None:
        strategy_files = [p for p in strategy_files if p.name == strategy_filter]
        if not strategy_files:
            raise FileNotFoundError(
                f"--strategy filter '{strategy_filter}' matched no strategy files in {strategy_dir}"
            )

    valid: List[Tuple[str, list, str]] = []
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
        if not validate_strategy(strategy_filename, strategy_data):
            skipped_count += 1
            continue
        name = strategy_data.get("name", strategy_path.stem)
        valid.append((strategy_filename, strategy_data["DRAFT_ORDER"], name))

    return valid, skipped_count


def validate_strategy(strategy_filename: str, strategy_data: dict) -> bool:
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
