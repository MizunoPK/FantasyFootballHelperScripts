"""
Tests for simulation.win_rate.strategy_loader.

Author: Kai Mizuno
"""

# Standard library
import json

# Third-party
import pytest

# Local
from simulation.win_rate.strategy_loader import load_valid_strategies, validate_strategy

# A valid 15-entry DRAFT_ORDER (the 4 RB / 4 WR / 1 FLEX split, as in
# draft_order_possibilities/51_MINE.json).
VALID_DRAFT_ORDER = [
    {"QB": "P", "FLEX": "S"}, {"TE": "P", "FLEX": "S"}, {"RB": "P", "WR": "S"},
    {"RB": "P", "WR": "S"}, {"WR": "P", "RB": "S"}, {"WR": "P", "RB": "S"},
    {"QB": "P", "FLEX": "S"}, {"TE": "P", "FLEX": "S"}, {"WR": "P", "RB": "S"},
    {"RB": "P", "WR": "S"}, {"WR": "P", "RB": "S"}, {"RB": "P", "WR": "S"},
    {"K": "P", "FLEX": "S"}, {"DST": "P", "FLEX": "S"}, {"FLEX": "P"},
]


def _write_strategy(folder, filename, data):
    (folder / filename).write_text(json.dumps(data))


@pytest.fixture
def strategy_dir(tmp_path):
    d = tmp_path / "draft_order_possibilities"
    d.mkdir()
    return tmp_path, d


class TestStrategyLoader:
    def test_returns_valid_triples(self, strategy_dir):
        data_folder, d = strategy_dir
        _write_strategy(d, "1_zero_rb.json", {"name": "Zero RB", "DRAFT_ORDER": VALID_DRAFT_ORDER})
        strategies, skipped = load_valid_strategies(data_folder)
        assert skipped == 0
        assert strategies == [("1_zero_rb.json", VALID_DRAFT_ORDER, "Zero RB")]

    def test_name_falls_back_to_stem(self, strategy_dir):
        data_folder, d = strategy_dir
        _write_strategy(d, "2_no_name.json", {"DRAFT_ORDER": VALID_DRAFT_ORDER})
        strategies, _ = load_valid_strategies(data_folder)
        assert strategies[0][2] == "2_no_name"

    def test_skips_invalid_and_counts(self, strategy_dir):
        data_folder, d = strategy_dir
        _write_strategy(d, "1_ok.json", {"name": "ok", "DRAFT_ORDER": VALID_DRAFT_ORDER})
        _write_strategy(d, "2_no_draft.json", {"name": "x"})           # missing DRAFT_ORDER
        _write_strategy(d, "3_bad.json", {"DRAFT_ORDER": [{"QB": "P"}]})  # fails validation
        strategies, skipped = load_valid_strategies(data_folder)
        assert [s[0] for s in strategies] == ["1_ok.json"]
        assert skipped == 2

    def test_numeric_prefix_sort(self, strategy_dir):
        data_folder, d = strategy_dir
        _write_strategy(d, "10_b.json", {"DRAFT_ORDER": VALID_DRAFT_ORDER})
        _write_strategy(d, "2_a.json", {"DRAFT_ORDER": VALID_DRAFT_ORDER})
        strategies, _ = load_valid_strategies(data_folder)
        assert [s[0] for s in strategies] == ["2_a.json", "10_b.json"]

    def test_strategy_filter_selects_one(self, strategy_dir):
        data_folder, d = strategy_dir
        _write_strategy(d, "1_a.json", {"DRAFT_ORDER": VALID_DRAFT_ORDER})
        _write_strategy(d, "2_b.json", {"DRAFT_ORDER": VALID_DRAFT_ORDER})
        strategies, _ = load_valid_strategies(data_folder, strategy_filter="2_b.json")
        assert [s[0] for s in strategies] == ["2_b.json"]

    def test_raises_when_no_numeric_files(self, strategy_dir):
        data_folder, d = strategy_dir
        _write_strategy(d, "notes.json", {"DRAFT_ORDER": VALID_DRAFT_ORDER})  # non-numeric prefix
        with pytest.raises(FileNotFoundError):
            load_valid_strategies(data_folder)

    def test_raises_when_filter_matches_none(self, strategy_dir):
        data_folder, d = strategy_dir
        _write_strategy(d, "1_a.json", {"DRAFT_ORDER": VALID_DRAFT_ORDER})
        with pytest.raises(FileNotFoundError):
            load_valid_strategies(data_folder, strategy_filter="9_missing.json")

    def test_validate_strategy_true_and_false(self):
        assert validate_strategy("ok.json", {"DRAFT_ORDER": VALID_DRAFT_ORDER}) is True
        assert validate_strategy("bad.json", {"DRAFT_ORDER": [{"QB": "P"}]}) is False


class TestPooledRbWrFlexPCount:
    """RB / WR / FLEX are validated as one pooled group totalling 9, in any split."""

    def test_accepts_the_live_config_split(self):
        # The live league_config.json order: 2 RB / 2 WR / 5 FLEX. Rejected by the
        # former fixed 4/4/1 counts, accepted now — the rounds left as FLEX are
        # declining to pre-commit RB-vs-WR, not violating the strategy shape.
        live_order = [
            {"RB": "P", "WR": "S"}, {"WR": "P", "RB": "S"}, {"WR": "P", "RB": "S"},
            {"RB": "P", "WR": "S"}, {"QB": "P", "FLEX": "S"}, {"TE": "P", "FLEX": "S"},
            {"FLEX": "P", "QB": "S"}, {"FLEX": "P", "QB": "S"}, {"QB": "P", "FLEX": "S"},
            {"TE": "P", "FLEX": "S"}, {"FLEX": "P"}, {"FLEX": "P"},
            {"K": "P", "FLEX": "S"}, {"DST": "P", "FLEX": "S"}, {"FLEX": "P"},
        ]
        assert validate_strategy("live.json", {"DRAFT_ORDER": live_order}) is True

    def test_accepts_an_all_flex_split(self):
        # The pooled extreme: every one of the 9 rounds left as FLEX.
        order = [
            {"FLEX": "P", "QB": "S"}, {"FLEX": "P", "QB": "S"}, {"FLEX": "P", "QB": "S"},
            {"FLEX": "P", "QB": "S"}, {"QB": "P", "FLEX": "S"}, {"TE": "P", "FLEX": "S"},
            {"FLEX": "P", "QB": "S"}, {"FLEX": "P", "QB": "S"}, {"QB": "P", "FLEX": "S"},
            {"TE": "P", "FLEX": "S"}, {"FLEX": "P"}, {"FLEX": "P"},
            {"K": "P", "FLEX": "S"}, {"DST": "P", "FLEX": "S"}, {"FLEX": "P"},
        ]
        assert validate_strategy("all_flex.json", {"DRAFT_ORDER": order}) is True

    def test_rejects_a_pooled_total_below_nine(self):
        # Reaching the pooled rule takes a P on a position in NEITHER group: with
        # every slot holding exactly one P, the fixed counts satisfied, and 15
        # slots, the pool is 15 - 6 = 9 by arithmetic. So an unrecognized position
        # is the only way to starve it, and it is what this rule actually catches.
        order = list(VALID_DRAFT_ORDER)
        order[2] = {"IDP": "P", "WR": "S"}
        assert validate_strategy("short_pool.json", {"DRAFT_ORDER": order}) is False

    def test_fixed_position_counts_are_still_enforced(self):
        # QB must still be exactly 2 — pooling did not loosen the fixed positions.
        order = list(VALID_DRAFT_ORDER)
        order[2] = {"QB": "P", "FLEX": "S"}
        assert validate_strategy("three_qb.json", {"DRAFT_ORDER": order}) is False
