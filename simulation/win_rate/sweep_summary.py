"""
Sweep Summary

Per-config ranked readout of the multi-parameter sweep results (the records produced by
SweepResultsManager). Every config is ranked by a Wilson lower confidence bound (lcb) over
its single best record's cumulative totals, so a high rate over few games no longer outranks
a confident one over many (T62/D1 — sample size used to be a mere tie-break). All configs
always appear — there is no top-N cap, and the games floor is opt-in (only --promote passes
it).

These rows are CANDIDATES, not estimates. The pooled totals mix games played against
different reference configs and the store carries no reference dimension (T68), so the lcb is
a better-behaved heuristic filter over incommensurable numbers rather than a confidence
statement. The displayed rate is max_selected — the in-sample maximum over a config's
recorded combinations. The number an operator should trust is the fresh re-measurement
config_promoter performs at --promote time, never a number from this report.

`rank_combinations`, `format_summary`, and `shape_report_json` are pure (no I/O);
`write_sweep_report` is the one I/O function — it persists the human-readable and
structured JSON reports under the simulation data root via an atomic tmp -> rename
write.

Author: Kai Mizuno
"""

# Standard library
import datetime
import json
from math import sqrt
from pathlib import Path
from statistics import NormalDist
from typing import Dict, List, Optional, Tuple

# Local
from simulation.win_rate.param_value_generation import DRAFT_SWEEP_PARAMS
from simulation.win_rate.SweepTournament import DEFAULT_CONFIDENCE
from utils.LoggingManager import get_logger
from utils.error_handler import error_context, FileOperationError

logger = get_logger()

REPORT_TXT_NAME = "win_rate_sweep_report.txt"
REPORT_JSON_NAME = "win_rate_sweep_report.json"

# T62/D1: the report's rate semantics, carried in the JSON so a reader of the file (not just
# a reader of this module) knows what the numbers are and are not.
RATE_SEMANTICS_LABEL = (
    "Candidates are ordered by 'lcb', a Wilson lower confidence bound over each config's "
    "pooled sweep totals, used ONLY as a shortlist filter. 'win_rate' is max_selected — the "
    "in-sample MAXIMUM over that config's recorded combinations, not an estimate of its true "
    "rate. The promoted headline comes from a fresh re-measurement (--promote), not from here."
)
POOLING_CAVEAT = (
    "Pooled totals mix games played against DIFFERENT reference/incumbent configs, and the "
    "sweep store has no reference dimension, so the mixture is unrecoverable "
    "(T68-winrate-heterogeneous-reference-pooling). Treat 'lcb' and 'win_rate' as a heuristic "
    "filter over incommensurable totals, never as a confidence statement about any config."
)


def wilson_interval(wins: int, games: int, confidence: float,
                    se_inflation: float = 1.0) -> Tuple[float, float]:
    """Two-sided Wilson score interval for a binomial proportion (stdlib-only).

    The score-test interval rather than the naive Wald interval, so it stays inside [0, 1]
    and behaves at small n. ``se_inflation`` multiplies the critical value, widening the
    interval by a clustering variance-inflation factor (T62/D5); the default 1.0 leaves the
    nominal interval unchanged.

    Args:
        wins (int): Observed successes.
        games (int): Observed trials.
        confidence (float): Two-sided confidence level (e.g. 0.95).
        se_inflation (float): Multiplier applied to the critical value (default 1.0 — no
            inflation).

    Returns:
        Tuple[float, float]: (lower, upper), each clamped to [0.0, 1.0]. Returns (0.0, 0.0)
            when games <= 0, mirroring rank_combinations' zero-games win_rate guard.
    """
    if games <= 0:
        return (0.0, 0.0)
    z = NormalDist().inv_cdf(1.0 - (1.0 - confidence) / 2.0) * se_inflation
    p = wins / games
    denominator = 1.0 + z * z / games
    centre = (p + z * z / (2 * games)) / denominator
    half_width = z * sqrt(p * (1.0 - p) / games + z * z / (4 * games * games)) / denominator
    return (max(0.0, centre - half_width), min(1.0, centre + half_width))


def _wilson_lower_bound(wins: int, games: int, confidence: float) -> float:
    """One-sided Wilson lower confidence bound at ``confidence`` (T62/D1).

    The lower endpoint of the two-sided Wilson interval at level ``2 * confidence - 1``, so a
    one-sided 0.95 bound reuses wilson_interval at the 0.90 two-sided level rather than
    re-deriving the same algebra. Deliberately NOT clustering-inflated: this bound is an
    internal shortlist FILTER over pooled, heterogeneous-reference totals, so widening it
    would imply a precision the quantity cannot support (T62/D5).

    Args:
        wins (int): Cumulative wins for the combination.
        games (int): Cumulative games for the combination.
        confidence (float): One-sided confidence level (e.g. 0.95).

    Returns:
        float: The lower bound in [0.0, 1.0]; 0.0 when games <= 0.
    """
    return wilson_interval(wins, games, 2.0 * confidence - 1.0)[0]


def rank_combinations(combinations: Dict[str, Dict], min_games: int = 0) -> List[Dict]:
    """
    Rank every config's best CANDIDATE combination by a Wilson lower confidence bound (T62/D1).

    Groups the store's combo records by strategy_id, picks each config's best record by
    Wilson lower confidence bound over its cumulative totals, and returns exactly one row per
    config ordered by that bound descending. Replaces the former rate-first ordering, under
    which sample size was only a tie-break — so a 170-game 0.62 strictly outranked a
    10,000-game 0.55. An LCB penalises the small sample in the ordering itself.

    The bound is a candidate FILTER, not an estimate: the pooled totals mix games played
    against different reference configs and the store has no reference dimension to separate
    them by (T68), so the ordering is a better-behaved heuristic over incommensurable numbers.
    The promoted headline comes from config_promoter's fresh re-measurement, never from here.

    There is no top-N cap — with the default min_games=0 all configs always appear, preserving
    the report's documented contract. Only the promote path passes a floor.

    Args:
        combinations (Dict[str, Dict]): The combo-keyed record map from
            SweepResultsManager.get_all_combinations().
        min_games (int): Minimum cumulative games a combination must have to be considered.
            Records below the floor are excluded entirely. Default 0 (no floor) — the report
            path takes this default; config_promoter passes DEFAULT_MIN_SHORTLIST_GAMES.

    Returns:
        List[Dict]: One row per config, sorted by Wilson lower confidence bound descending,
            tie-broken by games (sample size) descending then combo key ascending (a
            deterministic final tie-break, since float bounds make exact ties rarer but not
            impossible). Each row carries 'combo_key', 'strategy_id', 'param_values',
            'win_rate' (cumulative — the in-sample maximum, i.e. max_selected), 'lcb',
            'games', 'wins', 'total_runs', 'last_run'. Empty input, or input entirely below
            min_games, yields an empty list.
    """
    rows = []
    for combo_key, entry in combinations.items():
        wins = entry.get("total_wins", 0)
        games = entry.get("total_games", 0)
        if games < min_games:
            continue
        win_rate = wins / games if games > 0 else 0.0
        rows.append({
            "combo_key": combo_key,
            "strategy_id": entry.get("strategy_id", ""),
            "param_values": entry.get("param_values", {}),
            "win_rate": win_rate,
            "lcb": _wilson_lower_bound(wins, games, DEFAULT_CONFIDENCE),
            "games": games,
            "wins": wins,
            "total_runs": entry.get("total_runs", 0),
            "last_run": entry.get("last_run", ""),
        })

    rows.sort(key=lambda r: (-r["lcb"], -r["games"], r["combo_key"]))

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
        str: A table showing rank, Wilson lower confidence bound (the ordering key), the
            max_selected in-sample rate, games (sample size), strategy, and param values; or
            a clear message when there are no configs.
    """
    if not ranked:
        return "No sweep combinations recorded yet."

    lines = [
        "Sweep Config Candidates (ranked by Wilson lower confidence bound)",
        "MaxSel = in-sample maximum over the config's records — NOT an estimate of its rate.",
        "──────────────────────────────────────────────────────────────",
        "Rank      LCB   MaxSel  Games  Strategy / Params",
        "────  ───────  ───────  ─────  ─────────────────",
    ]
    for rank, row in enumerate(ranked, 1):
        params = ", ".join(f"{k}={v}" for k, v in row["param_values"].items())
        lines.append(
            f"{rank:>4}  {row['lcb']:>7.3f}  {row['win_rate']:>7.3f}  {row['games']:>5}  "
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
        Dict: A wrapper object {"generated": <date>, "rate_semantics": <str>,
            "pooling_caveat": <str>, "configs": [...]} where each config entry carries
            'rank' (1-based), 'strategy_id', 'lcb' (the ordering key), 'win_rate'
            (max_selected — the in-sample maximum, not an estimate), 'games', 'wins', and
            'param_values' — the latter keyed in canonical DRAFT_SWEEP_PARAMS order for
            deterministic, diff-stable output. Missing params resolve to None. The two
            top-level label strings state the rate semantics and the T68 heterogeneous-
            pooling caveat in the file itself (T62).
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
            "lcb": row["lcb"],
            "win_rate": row["win_rate"],
            "games": row["games"],
            "wins": row["wins"],
            "param_values": ordered_params,
        })

    return {
        "generated": generated,
        "rate_semantics": RATE_SEMANTICS_LABEL,
        "pooling_caveat": POOLING_CAVEAT,
        "configs": configs,
    }


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
