"""
Sweep Summary

Ranked top-N readout over the multi-parameter sweep results (the records produced by
SweepResultsManager). Combinations are ranked by cumulative win rate
(total_wins / total_games) with sample size shown, so a high win rate over few games
is distinguishable from a confident one over many.

Pure functions — `rank_combinations` returns structured rows and `format_summary`
renders a table string; neither does any I/O.

Author: Kai Mizuno
"""

# Standard library
from typing import Dict, List

DEFAULT_TOP_N = 20


def rank_combinations(combinations: Dict[str, Dict], n: int = DEFAULT_TOP_N) -> List[Dict]:
    """
    Rank combination records by cumulative win rate and return the top N rows.

    Args:
        combinations (Dict[str, Dict]): The combo-keyed record map from
            SweepResultsManager.get_all_combinations().
        n (int): Maximum number of rows to return (default DEFAULT_TOP_N).

    Returns:
        List[Dict]: Up to n rows sorted by cumulative win rate descending, tie-broken
            by games (sample size) descending then combo key ascending. Each row carries
            'strategy_id', 'param_values', 'win_rate' (cumulative), 'games', 'wins',
            'best_win_rate', 'total_runs', 'last_run'. Empty input yields an empty list.
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
    return rows[:n]


def format_summary(ranked: List[Dict]) -> str:
    """
    Render ranked combination rows as a printable table string.

    Args:
        ranked (List[Dict]): Rows from rank_combinations.

    Returns:
        str: A table showing rank, win rate, games (sample size), strategy, and param
            values; or a clear message when there are no combinations.
    """
    if not ranked:
        return "No sweep combinations recorded yet."

    lines = [
        "Sweep Combination Summary (ranked by cumulative win rate)",
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
