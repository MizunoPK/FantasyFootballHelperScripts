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
    wilson_interval,
    write_sweep_report,
)


def _entry(strategy_id, wins, games, **params):
    # T68: wins/games live in ONE non-self-play reference bucket so rank_combinations (which now
    # pools only non-self-play buckets) has rankable head-to-head evidence. total_wins/total_games
    # are kept as the derived sum for any consumer that still reads them.
    return {
        "strategy_id": strategy_id,
        "param_values": params or {"PRIMARY_BONUS": 67},
        "best_single_run_win_rate": (wins / games) if games else 0.0,
        "by_reference": {"ref_A": {"wins": wins, "games": games}},
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
        combos = {"a": _entry("s_a", wins=3, games=10)}
        row = rank_combinations(combos)[0]
        assert row["strategy_id"] == "s_a"
        assert row["param_values"] == {"PRIMARY_BONUS": 67}
        assert row["win_rate"] == 0.3
        assert row["games"] == 10
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

    def test_self_play_bucket_excluded_from_ranking(self):
        # T68/D2: a combo's ~0.50 self_play bucket never enters the pooled margin — only the
        # non-self-play bucket feeds the row (60/100), NOT the blended 110/200.
        entry = {
            "strategy_id": "s_a", "param_values": {"PRIMARY_BONUS": 67},
            "by_reference": {
                "self_play": {"wins": 50, "games": 100},
                "refA": {"wins": 60, "games": 100},
            },
            "total_wins": 110, "total_games": 200, "total_runs": 2, "last_run": "2026-07-20",
        }
        row = rank_combinations({"a": entry})[0]
        assert row["games"] == 100
        assert row["wins"] == 60
        assert row["win_rate"] == 0.6

    def test_self_play_only_combo_is_excluded(self):
        # A combo with ONLY a self_play bucket has no reference-relative evidence -> excluded.
        entry = {
            "strategy_id": "s_a", "param_values": {"PRIMARY_BONUS": 67},
            "by_reference": {"self_play": {"wins": 50, "games": 100}},
            "total_wins": 50, "total_games": 100, "total_runs": 1, "last_run": "x",
        }
        assert rank_combinations({"a": entry}) == []

    def test_two_incumbents_pool_but_self_play_does_not(self):
        # AC6 at the ranking layer: two head-to-head buckets pool (60+70)/(100+100); self_play excluded.
        entry = {
            "strategy_id": "s_a", "param_values": {"PRIMARY_BONUS": 67},
            "by_reference": {
                "self_play": {"wins": 50, "games": 100},
                "refA": {"wins": 60, "games": 100},
                "refB": {"wins": 70, "games": 100},
            },
            "total_wins": 180, "total_games": 300, "total_runs": 3, "last_run": "x",
        }
        row = rank_combinations({"a": entry})[0]
        assert row["wins"] == 130 and row["games"] == 200
        assert row["win_rate"] == 0.65


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
        # T62: the entry gains 'lcb' (the ordering key) and 'wins'. 'win_rate' is retained but
        # is now max_selected — the in-sample maximum, not an estimate.
        combos = {"a": _entry("s_a", wins=9, games=10, **_FULL_PARAMS)}
        entry = shape_report_json(rank_combinations(combos))["configs"][0]
        assert entry["rank"] == 1
        assert entry["strategy_id"] == "s_a"
        assert entry["win_rate"] == 0.9
        assert entry["games"] == 10
        assert entry["wins"] == 9
        assert round(entry["lcb"], 6) == 0.152281  # T68: margin-over-reference (0.652281 - 0.50)
        assert set(entry.keys()) == {
            "rank", "strategy_id", "lcb", "win_rate", "games", "wins", "param_values",
        }

    def test_wrapper_carries_rate_semantics_and_pooling_caveat(self):
        # T62: the report JSON states its own rate semantics + the T68 pooling caveat, so a
        # reader of the FILE (not just of the module) knows what the numbers are not.
        combos = {"a": _entry("s_a", wins=9, games=10, **_FULL_PARAMS)}
        report = shape_report_json(rank_combinations(combos))
        assert "shortlist filter" in report["rate_semantics"]
        assert "T68" in report["pooling_caveat"]

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


class TestWilsonShortlistCoverage:
    """T62/D1 + D5: LCB ordering, the opt-in games floor, and what is NOT inflated.

    New coverage owned by T62's test_build_plan.md — none of these behaviours existed before
    the Wilson shortlist replaced the rate-first sort at sweep_summary.py:71.
    """

    def test_small_sample_high_rate_loses_to_accumulated_higher_lcb(self):
        # THE ordering regression (spec.md "New coverage required", bullet 2). Under the old
        # (-win_rate, -games, combo_key) sort the 170-game 0.588 draw ranked FIRST, because the
        # rate came first and sample size was only a tie-break. Under the Wilson LCB ordering
        # the 10,000-game 0.550 accumulation ranks first:
        #     LCB(100/170)    = 0.525238
        #     LCB(5500/10000) = 0.541805
        # Both values were executed with the one-sided helper before being written down.
        combos = {
            "lucky": _entry("s_lucky", wins=100, games=170),     # 0.588 over 170
            "steady": _entry("s_steady", wins=5500, games=10000),  # 0.550 over 10,000
        }
        ranked = rank_combinations(combos)
        assert [r["combo_key"] for r in ranked] == ["steady", "lucky"]
        # The raw rate still favours the small sample — proving it is the ORDERING that
        # changed, not the underlying data.
        assert ranked[1]["win_rate"] > ranked[0]["win_rate"]
        # T68: lcb is now the margin over the 0.50 reference null (raw LCB - 0.50).
        assert round(ranked[0]["lcb"], 6) == 0.041805  # steady: 0.541805 - 0.50
        assert round(ranked[1]["lcb"], 6) == 0.025238  # lucky:  0.525238 - 0.50

    def test_min_games_floor_excludes_below_floor_rows(self):
        combos = {
            "tiny": _entry("s_tiny", wins=20, games=29),
            "ok": _entry("s_ok", wins=20, games=30),
        }
        # No floor by default: both survive.
        assert {r["combo_key"] for r in rank_combinations(combos)} == {"tiny", "ok"}
        # With the floor the below-floor row is excluded ENTIRELY, not merely demoted.
        assert [r["combo_key"] for r in rank_combinations(combos, min_games=30)] == ["ok"]

    def test_min_games_floor_can_empty_the_shortlist(self):
        # The precondition for config_promoter's empty-shortlist refusal.
        combos = {"tiny": _entry("s_tiny", wins=8, games=10)}
        assert rank_combinations(combos, min_games=30) == []

    def test_report_path_keeps_every_config_at_the_default_floor(self):
        # sweep_summary.py's documented "all configs always appear — there is no top-N cap"
        # contract survives, because min_games defaults to 0 and only --promote passes a floor.
        combos = {"tiny": _entry("s_tiny", wins=1, games=2)}
        assert len(rank_combinations(combos)) == 1

    def test_shortlist_lcb_is_not_clustering_inflated(self):
        # T62/D5's asymmetry, asserted rather than assumed: the shortlist bound is an internal
        # FILTER over incommensurable pooled totals and carries NO inflation. Only the
        # operator-facing re-measured interval (config_promoter) is widened by 1.28.
        row = rank_combinations({"a": _entry("s_a", wins=105, games=170)})[0]
        uninflated = wilson_interval(105, 170, 0.90)[0]
        inflated = wilson_interval(105, 170, 0.90, se_inflation=1.28)[0]
        # T68: the reported lcb is the MARGIN of the uninflated bound (raw - 0.50), still uninflated.
        assert row["lcb"] == uninflated - 0.50
        assert row["lcb"] != inflated - 0.50
        # A wider interval has a LOWER lower endpoint — so the two are genuinely distinguishable
        # and this assertion could not pass by coincidence.
        assert inflated < uninflated

    def test_se_inflation_widens_the_interval_in_both_directions(self):
        # 935/1700 -> plain (0.526265, 0.573510); x1.28 -> (0.519600, 0.580031). Values
        # executed before being written down. This is the exact interval config_promoter
        # reports for the stubbed re-measurement used in test_config_promoter.py.
        plain_low, plain_high = wilson_interval(935, 1700, 0.95)
        wide_low, wide_high = wilson_interval(935, 1700, 0.95, se_inflation=1.28)
        assert (round(plain_low, 6), round(plain_high, 6)) == (0.526265, 0.57351)
        assert (round(wide_low, 6), round(wide_high, 6)) == (0.5196, 0.580031)
        assert wide_low < plain_low
        assert wide_high > plain_high

    def test_wilson_interval_zero_games_is_degenerate_not_a_crash(self):
        assert wilson_interval(0, 0, 0.95) == (0.0, 0.0)
