"""
Tests for simulation.win_rate.sweep_summary.

Covers ranking by cumulative win rate, top-N truncation, tie-break by sample size,
per-row content, empty handling, and formatting. Pure functions over synthetic
combination records (shape per SweepResultsManager.get_all_combinations()).

Author: Kai Mizuno
"""

# Local
from simulation.win_rate.sweep_summary import rank_combinations, format_summary, DEFAULT_TOP_N


def _entry(strategy_id, wins, games, **params):
    return {
        "strategy_id": strategy_id,
        "param_values": params or {"PRIMARY_BONUS": 67},
        "best_win_rate": (wins / games) if games else 0.0,
        "total_wins": wins,
        "total_games": games,
        "total_runs": 1,
        "last_run": "2026-06-10",
    }


class TestSweepSummary:
    """Tests for rank_combinations and format_summary."""

    def test_rank_orders_by_cumulative_win_rate(self):
        combos = {
            "a": _entry("s_a", wins=5, games=10),   # 0.5
            "b": _entry("s_b", wins=9, games=10),   # 0.9
            "c": _entry("s_c", wins=7, games=10),   # 0.7
        }
        ranked = rank_combinations(combos)
        assert [r["combo_key"] for r in ranked] == ["b", "c", "a"]
        assert ranked[0]["win_rate"] == 0.9

    def test_rank_top_n_truncates(self):
        combos = {k: _entry(f"s_{k}", wins=i, games=10) for i, k in enumerate("abcde")}
        assert len(rank_combinations(combos, n=2)) == 2
        assert len(rank_combinations(combos, n=99)) == 5  # n >= count returns all

    def test_rank_tie_break_by_sample_size(self):
        combos = {
            "few": _entry("s_few", wins=8, games=10),    # 0.8 over 10
            "many": _entry("s_many", wins=80, games=100),  # 0.8 over 100
        }
        ranked = rank_combinations(combos)
        # equal win rate -> more games (sample size) first
        assert ranked[0]["combo_key"] == "many"

    def test_rank_rows_carry_required_fields(self):
        combos = {"a": _entry("s_a", wins=3, games=0)}  # games == 0 -> win_rate 0.0
        row = rank_combinations(combos)[0]
        assert row["strategy_id"] == "s_a"
        assert row["param_values"] == {"PRIMARY_BONUS": 67}
        assert row["win_rate"] == 0.0
        assert row["games"] == 0
        assert "best_win_rate" in row and "wins" in row

    def test_rank_empty_returns_empty(self):
        assert rank_combinations({}) == []

    def test_format_summary_empty_message(self):
        out = format_summary([])
        assert isinstance(out, str) and out.strip() != ""
        assert "No sweep combinations" in out

    def test_format_summary_includes_rows(self):
        combos = {"a": _entry("1_zero_rb.json", wins=9, games=10, PRIMARY_BONUS=80)}
        out = format_summary(rank_combinations(combos))
        assert "1_zero_rb.json" in out
        assert "PRIMARY_BONUS=80" in out
        assert "0.900" in out   # win rate
        assert "10" in out      # games / sample size
