"""
Tests for simulation.win_rate.sweep_summary.

Covers ranking by cumulative win rate, top-N truncation, tie-break by sample size,
per-row content, empty handling, and formatting. Pure functions over synthetic
combination records (shape per SweepResultsManager.get_all_combinations()).

Author: Kai Mizuno
"""

# Local
from simulation.win_rate.sweep_summary import (
    rank_combinations,
    format_summary,
    shape_report_json,
    write_sweep_report,
)


def _entry(strategy_id, wins, games, **params):
    return {
        "strategy_id": strategy_id,
        "param_values": params or {"PRIMARY_BONUS": 67},
        "best_single_run_win_rate": (wins / games) if games else 0.0,
        "total_wins": wins,
        "total_games": games,
        "total_runs": 1,
        "last_run": "2026-06-10",
    }


class TestSweepSummary:
    """Tests for rank_combinations and format_summary."""

    def test_rank_orders_by_cumulative_win_rate(self):
        # Three distinct configs -> three rows, ordered by win rate descending.
        combos = {
            "a": _entry("s_a", wins=5, games=10),   # 0.5
            "b": _entry("s_b", wins=9, games=10),   # 0.9
            "c": _entry("s_c", wins=7, games=10),   # 0.7
        }
        ranked = rank_combinations(combos)
        assert [r["combo_key"] for r in ranked] == ["b", "c", "a"]
        assert ranked[0]["win_rate"] == 0.9

    def test_rank_one_row_per_config_no_cap(self):
        # 5 records across 2 configs; per-config ranking yields exactly 2 rows.
        combos = {
            "a1": _entry("s_a", wins=5, games=10),   # 0.5
            "a2": _entry("s_a", wins=9, games=10),   # 0.9 (s_a best)
            "a3": _entry("s_a", wins=3, games=10),   # 0.3
            "b1": _entry("s_b", wins=8, games=10),   # 0.8 (s_b best)
            "b2": _entry("s_b", wins=2, games=10),   # 0.2
        }
        ranked = rank_combinations(combos)
        assert len(ranked) == 2  # one row per config, no cap
        assert {r["strategy_id"] for r in ranked} == {"s_a", "s_b"}

    def test_rank_picks_each_configs_best_record(self):
        combos = {
            "a1": _entry("s_a", wins=5, games=10),
            "a2": _entry("s_a", wins=9, games=10),   # best for s_a
            "b1": _entry("s_b", wins=8, games=10),   # best for s_b
            "b2": _entry("s_b", wins=2, games=10),
        }
        ranked = rank_combinations(combos)
        by_config = {r["strategy_id"]: r for r in ranked}
        assert by_config["s_a"]["win_rate"] == 0.9
        assert by_config["s_b"]["win_rate"] == 0.8
        # ordered by win rate descending across configs
        assert [r["strategy_id"] for r in ranked] == ["s_a", "s_b"]

    def test_rank_tie_break_by_sample_size(self):
        # Two distinct configs, equal win rate -> more games (sample size) first.
        combos = {
            "few": _entry("s_few", wins=8, games=10),    # 0.8 over 10
            "many": _entry("s_many", wins=80, games=100),  # 0.8 over 100
        }
        ranked = rank_combinations(combos)
        assert ranked[0]["combo_key"] == "many"

    def test_rank_rows_carry_required_fields(self):
        combos = {"a": _entry("s_a", wins=3, games=0)}  # games == 0 -> win_rate 0.0
        row = rank_combinations(combos)[0]
        assert row["strategy_id"] == "s_a"
        assert row["param_values"] == {"PRIMARY_BONUS": 67}
        assert row["win_rate"] == 0.0
        assert row["games"] == 0
        assert "wins" in row
        assert "best_win_rate" not in row
        assert "best_single_run_win_rate" not in row

    def test_rank_rows_drop_single_run_best_field(self):
        # D3: even when the stored combination entry carries the diagnostic single-run best,
        # rank_combinations must NOT propagate it into the report row (the report never rendered it).
        combos = {"a": _entry("s_a", wins=7, games=10)}
        assert "best_single_run_win_rate" in combos["a"]  # present in the store entry
        row = rank_combinations(combos)[0]
        assert "best_single_run_win_rate" not in row
        assert "best_win_rate" not in row

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


# Full 6-param vector for D2 key-order assertions.
_FULL_PARAMS = {
    "SAME_POS_BYE_WEIGHT": 2,
    "DIFF_POS_BYE_WEIGHT": 3,
    "PRIMARY_BONUS": 80,
    "SECONDARY_BONUS": 40,
    "ADP_SCORING_WEIGHT": 0.5,
    "PLAYER_RATING_SCORING_WEIGHT": 0.5,
}


class TestShapeReportJson:
    """Tests for shape_report_json (the D2 wrapper-object schema)."""

    def test_wrapper_shape_and_generated(self):
        combos = {"a": _entry("s_a", wins=9, games=10, **_FULL_PARAMS)}
        report = shape_report_json(rank_combinations(combos), generated="2026-06-22")
        assert report["generated"] == "2026-06-22"
        assert isinstance(report["configs"], list)
        assert len(report["configs"]) == 1

    def test_config_entry_fields(self):
        combos = {"a": _entry("s_a", wins=9, games=10, **_FULL_PARAMS)}
        entry = shape_report_json(rank_combinations(combos))["configs"][0]
        assert entry["rank"] == 1
        assert entry["strategy_id"] == "s_a"
        assert entry["win_rate"] == 0.9
        assert entry["games"] == 10
        assert set(entry.keys()) == {"rank", "strategy_id", "win_rate", "games", "param_values"}

    def test_param_values_in_canonical_order(self):
        combos = {"a": _entry("s_a", wins=9, games=10, **_FULL_PARAMS)}
        entry = shape_report_json(rank_combinations(combos))["configs"][0]
        assert list(entry["param_values"].keys()) == [
            "SAME_POS_BYE_WEIGHT",
            "DIFF_POS_BYE_WEIGHT",
            "PRIMARY_BONUS",
            "SECONDARY_BONUS",
            "ADP_SCORING_WEIGHT",
            "PLAYER_RATING_SCORING_WEIGHT",
        ]
        assert entry["param_values"]["PRIMARY_BONUS"] == 80

    def test_ranks_increment_with_descending_win_rate(self):
        combos = {
            "a": _entry("s_a", wins=9, games=10, **_FULL_PARAMS),  # 0.9
            "b": _entry("s_b", wins=5, games=10, **_FULL_PARAMS),  # 0.5
        }
        configs = shape_report_json(rank_combinations(combos))["configs"]
        assert [c["rank"] for c in configs] == [1, 2]
        assert [c["strategy_id"] for c in configs] == ["s_a", "s_b"]

    def test_missing_param_resolves_to_none(self):
        # _entry with a single param; the other five canonical keys resolve to None.
        combos = {"a": _entry("s_a", wins=9, games=10, PRIMARY_BONUS=80)}
        params = shape_report_json(rank_combinations(combos))["configs"][0]["param_values"]
        assert params["PRIMARY_BONUS"] == 80
        assert params["SAME_POS_BYE_WEIGHT"] is None


class TestWriteSweepReport:
    """Tests for write_sweep_report (the D3 two-file atomic persistence)."""

    def test_writes_both_files_under_data_root(self, tmp_path):
        combos = {"a": _entry("1_zero_rb.json", wins=9, games=10, **_FULL_PARAMS)}
        ranked = rank_combinations(combos)
        write_sweep_report(ranked, tmp_path)
        txt = tmp_path / "win_rate_sweep_report.txt"
        json_file = tmp_path / "win_rate_sweep_report.json"
        assert txt.exists()
        assert json_file.exists()

    def test_txt_mirrors_format_summary(self, tmp_path):
        combos = {"a": _entry("1_zero_rb.json", wins=9, games=10, **_FULL_PARAMS)}
        ranked = rank_combinations(combos)
        write_sweep_report(ranked, tmp_path)
        content = (tmp_path / "win_rate_sweep_report.txt").read_text(encoding="utf-8")
        assert format_summary(ranked) in content
        assert "1_zero_rb.json" in content

    def test_json_matches_shape_report_json(self, tmp_path):
        import json as _json
        combos = {"a": _entry("s_a", wins=9, games=10, **_FULL_PARAMS)}
        ranked = rank_combinations(combos)
        write_sweep_report(ranked, tmp_path, generated="2026-06-22")
        data = _json.loads(
            (tmp_path / "win_rate_sweep_report.json").read_text(encoding="utf-8")
        )
        assert data == shape_report_json(ranked, generated="2026-06-22")
        assert data["generated"] == "2026-06-22"

    def test_overwrite_not_accumulate(self, tmp_path):
        first = rank_combinations({"a": _entry("s_a", wins=9, games=10, **_FULL_PARAMS)})
        write_sweep_report(first, tmp_path)
        second = rank_combinations({"b": _entry("s_b", wins=5, games=10, **_FULL_PARAMS)})
        write_sweep_report(second, tmp_path)
        # only the two fixed-name files exist (no timestamped accumulation, no .tmp left).
        names = sorted(p.name for p in tmp_path.iterdir())
        assert names == ["win_rate_sweep_report.json", "win_rate_sweep_report.txt"]
        content = (tmp_path / "win_rate_sweep_report.txt").read_text(encoding="utf-8")
        assert "s_b" in content
        assert "s_a" not in content

    def test_creates_missing_data_root(self, tmp_path):
        nested = tmp_path / "does_not_exist_yet"
        ranked = rank_combinations({"a": _entry("s_a", wins=9, games=10, **_FULL_PARAMS)})
        write_sweep_report(ranked, nested)
        assert (nested / "win_rate_sweep_report.txt").exists()
        assert (nested / "win_rate_sweep_report.json").exists()
