"""
Sweep Summary

Per-config ranked readout over the multi-parameter sweep results (the records
produced by SweepResultsManager). Every config is ranked by its single best record's
cumulative win rate (total_wins / total_games) with sample size shown, so a high win
rate over few games is distinguishable from a confident one over many. All configs
always appear — there is no top-N cap.

`rank_combinations`, `format_summary`, and `shape_report_json` are pure (no I/O);
`write_sweep_report` is the one I/O function — it persists the human-readable and
structured JSON reports under the simulation data root via an atomic tmp -> rename
write.

Author: Kai Mizuno
"""

# Standard library
import datetime
import json
from pathlib import Path
from typing import Dict, List, Optional

# Local
from simulation.win_rate.param_value_generation import DRAFT_SWEEP_PARAMS
from utils.LoggingManager import get_logger
from utils.error_handler import error_context, FileOperationError

logger = get_logger()

REPORT_TXT_NAME = "win_rate_sweep_report.txt"
REPORT_JSON_NAME = "win_rate_sweep_report.json"


def rank_combinations(combinations: Dict[str, Dict]) -> List[Dict]:
    """
    Rank every config by its single best combination record (per-config ranking).

    Groups the store's combo records by strategy_id, picks each config's best record
    by cumulative win rate (total_wins / total_games) with the standard tie-break,
    and returns exactly one row per config ordered by win rate descending. There is
    no top-N cap — all configs always appear.

    Args:
        combinations (Dict[str, Dict]): The combo-keyed record map from
            SweepResultsManager.get_all_combinations().

    Returns:
        List[Dict]: One row per config, sorted by cumulative win rate descending,
            tie-broken by games (sample size) descending then combo key ascending.
            Each row carries 'combo_key', 'strategy_id', 'param_values',
            'win_rate' (cumulative), 'games', 'wins', 'best_win_rate', 'total_runs',
            'last_run'. Empty input yields an empty list.
    """
    rows = []
    for combo_key, entry in combinations.items():
        wins = entry.get("total_wins", 0)
        games = entry.get("total_games", 0)
        win_rate = wins / games if games > 0 else 0.0
        rows.append({
            "combo_key": combo_key,
            "strategy_id": entry.get("strategy_id", ""),
            "param_values": entry.get("param_values", {}),
            "win_rate": win_rate,
            "games": games,
            "wins": wins,
            "best_win_rate": entry.get("best_win_rate", 0.0),
            "total_runs": entry.get("total_runs", 0),
            "last_run": entry.get("last_run", ""),
        })

    rows.sort(key=lambda r: (-r["win_rate"], -r["games"], r["combo_key"]))

    best_per_config = {}
    for row in rows:
        if row["strategy_id"] not in best_per_config:
            best_per_config[row["strategy_id"]] = row
    return list(best_per_config.values())


def format_summary(ranked: List[Dict]) -> str:
    """
    Render per-config rows as a printable table string.

    Args:
        ranked (List[Dict]): Per-config rows from rank_combinations.

    Returns:
        str: A table showing rank, win rate, games (sample size), strategy, and param
            values; or a clear message when there are no configs.
    """
    if not ranked:
        return "No sweep combinations recorded yet."

    lines = [
        "Sweep Config Summary (ranked by cumulative win rate)",
        "──────────────────────────────────────────────────────────────",
        "Rank  WinRate  Games  Strategy / Params",
        "────  ───────  ─────  ─────────────────",
    ]
    for rank, row in enumerate(ranked, 1):
        params = ", ".join(f"{k}={v}" for k, v in row["param_values"].items())
        lines.append(
            f"{rank:>4}  {row['win_rate']:>7.3f}  {row['games']:>5}  "
            f"{row['strategy_id']} | {params}"
        )
    lines.append("──────────────────────────────────────────────────────────────")
    return "\n".join(lines)


def shape_report_json(ranked: List[Dict], generated: Optional[str] = None) -> Dict:
    """
    Shape ranked per-config rows into the structured report JSON wrapper object (D2).

    Args:
        ranked (List[Dict]): Per-config rows from rank_combinations (already ordered
            by win rate descending).
        generated (Optional[str]): The report generation date (ISO 8601). Defaults to
            today's date when None.

    Returns:
        Dict: A wrapper object {"generated": <date>, "configs": [...]} where each
            config entry carries 'rank' (1-based), 'strategy_id', 'win_rate', 'games',
            and 'param_values' — the latter keyed in canonical DRAFT_SWEEP_PARAMS order
            for deterministic, diff-stable output. Missing params resolve to None.
    """
    if generated is None:
        generated = datetime.date.today().isoformat()

    configs = []
    for rank, row in enumerate(ranked, 1):
        param_values = row.get("param_values", {})
        ordered_params = {key: param_values.get(key) for key in DRAFT_SWEEP_PARAMS}
        configs.append({
            "rank": rank,
            "strategy_id": row["strategy_id"],
            "win_rate": row["win_rate"],
            "games": row["games"],
            "param_values": ordered_params,
        })

    return {"generated": generated, "configs": configs}


def write_sweep_report(ranked: List[Dict], data_folder: Path,
                       generated: Optional[str] = None) -> None:
    """
    Persist the per-config ranked report to two fixed-name files under data_folder (D3).

    Writes win_rate_sweep_report.txt (human-readable, mirrors the stdout table) and
    win_rate_sweep_report.json (structured, D2 schema). Each file is written via its own
    atomic tmp -> rename, so the two writes are individually atomic but NOT jointly
    atomic: neither file is ever left partial, but the writes are independent. A failure
    on the second (.json) write therefore leaves the first (.txt) already updated to the
    new run. Each write overwrites any prior report. The data root is created if absent.

    Args:
        ranked (List[Dict]): Per-config rows from rank_combinations.
        data_folder (Path): The simulation data root (the CLI --data path); the two
            report files are written directly under it, beside win_rate_sweep_results.json.
        generated (Optional[str]): The report generation date passed to shape_report_json
            (defaults to today when None).

    Raises:
        FileOperationError: If either atomic write fails. The failing file is left
            untouched with no orphaned .tmp; any file already written earlier in the
            call retains its new contents (writes are not jointly atomic).
    """
    data_folder.mkdir(parents=True, exist_ok=True)

    txt_path = data_folder / REPORT_TXT_NAME
    json_path = data_folder / REPORT_JSON_NAME

    _atomic_write_text(format_summary(ranked) + "\n", txt_path)
    _atomic_write_text(
        json.dumps(shape_report_json(ranked, generated), indent=2) + "\n", json_path
    )
    logger.info(f"Sweep report written to {txt_path} and {json_path}")


def _atomic_write_text(content: str, path: Path) -> None:
    """
    Write `content` to `path` atomically via a tmp file -> rename.

    Mirrors SweepResultsManager._save: a mid-write failure leaves `path` untouched and
    the orphaned .tmp is removed before re-raising.

    Raises:
        FileOperationError: On any OSError/PermissionError during the write.
    """
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write(content)
        tmp_path.replace(path)
    except (PermissionError, OSError) as e:
        tmp_path.unlink(missing_ok=True)
        with error_context("writing sweep report", component="sweep_summary",
                           file_path=str(path)):
            raise FileOperationError(
                f"Failed to write sweep report to {path}: {e}"
            ) from e
