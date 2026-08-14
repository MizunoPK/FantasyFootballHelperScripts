"""
Unit Tests for ConfigManager.get_draft_order_bonus()

Regression coverage for the draft-order-bonus position lookup. The prior
implementation remapped the player's position through get_position_with_flex()
BEFORE looking it up in the round's DRAFT_ORDER dict, so a round keyed on the
literal flex-eligible names (e.g. round 1 {"WR": "P", "RB": "S"}) silently
returned no bonus for WR/RB — the exact shape of every live/sim draft strategy.
These tests exercise both the literal-position path (the gap the old tests
missed, which all keyed rounds on "FLEX") and the FLEX-fallback path.

Author: Kai Mizuno
"""

import json

import pytest

from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.league_helper.util.ConfigManager import ConfigManager


@pytest.fixture
def temp_data_folder(tmp_path):
    data_folder = tmp_path / "data"
    data_folder.mkdir()
    return data_folder


@pytest.fixture
def config(temp_data_folder):
    """ConfigManager loaded from a config whose DRAFT_ORDER mixes literal
    position keys, a FLEX key, and a round with both."""
    cfg = {
        "config_name": "test",
        "description": "draft order bonus regression",
        "parameters": {
            "CURRENT_NFL_WEEK": 1,
            "NFL_SEASON": 2026,
            "NFL_SCORING_FORMAT": "ppr",
            "NORMALIZATION_MAX_SCALE": 100.0,
            "DRAFT_NORMALIZATION_MAX_SCALE": 150,
            "SAME_POS_BYE_WEIGHT": 1.0,
            "DIFF_POS_BYE_WEIGHT": 1.0,
            "INJURY_PENALTIES": {"LOW": 0, "MEDIUM": 10, "HIGH": 75},
            "DRAFT_ORDER_BONUSES": {"PRIMARY": 50, "SECONDARY": 30},
            "DRAFT_ORDER": [
                {"WR": "P", "RB": "S"},      # 0: literal flex-eligible names (the bug case)
                {"QB": "P", "FLEX": "S"},    # 1: non-flex literal + FLEX fallback
                {"TE": "P"},                 # 2: non-flex literal only
                {"WR": "P", "FLEX": "S"},    # 3: literal WR must win over FLEX; RB uses FLEX
            ],
            "MAX_POSITIONS": {"QB": 2, "RB": 4, "WR": 4, "FLEX": 2, "TE": 1, "K": 1, "DST": 1},
            "FLEX_ELIGIBLE_POSITIONS": ["RB", "WR"],
            "ADP_SCORING": {
                "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 35},
                "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                "WEIGHT": 1.0,
            },
            "PLAYER_RATING_SCORING": {
                "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 22},
                "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                "WEIGHT": 1.0,
            },
            "TEAM_QUALITY_SCORING": {
                "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 5},
                "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                "WEIGHT": 1.0,
            },
            "PERFORMANCE_SCORING": {
                "MIN_WEEKS": 3,
                "THRESHOLDS": {"BASE_POSITION": 0.0, "DIRECTION": "BI_EXCELLENT_HI", "STEPS": 0.15},
                "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                "WEIGHT": 1.0,
            },
            "MATCHUP_SCORING": {
                "IMPACT_SCALE": 150.0,
                "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 6},
                "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                "WEIGHT": 1.0,
            },
            "SCHEDULE_SCORING": {
                "IMPACT_SCALE": 80.0,
                "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 8},
                "MULTIPLIERS": {"EXCELLENT": 1.0, "GOOD": 1.0, "POOR": 1.0, "VERY_POOR": 1.0},
                "WEIGHT": 0.0,
            },
        },
    }
    (temp_data_folder / "league_config.json").write_text(json.dumps(cfg))
    return ConfigManager(temp_data_folder)


class TestLiteralFlexPositionKeys:
    """Round keyed on literal WR/RB names — the path the old FLEX-only tests missed."""

    def test_literal_wr_key_gets_primary(self, config):
        assert config.get_draft_order_bonus("WR", 0) == (50, "PRIMARY")

    def test_literal_rb_key_gets_secondary(self, config):
        assert config.get_draft_order_bonus("RB", 0) == (30, "SECONDARY")

    def test_non_listed_position_gets_no_bonus(self, config):
        assert config.get_draft_order_bonus("QB", 0) == (0, "")


class TestFlexFallback:
    """Flex-eligible positions still match a FLEX key when not listed literally."""

    def test_qb_literal_primary(self, config):
        assert config.get_draft_order_bonus("QB", 1) == (50, "PRIMARY")

    def test_rb_matches_flex_key_secondary(self, config):
        assert config.get_draft_order_bonus("RB", 1) == (30, "SECONDARY")

    def test_wr_matches_flex_key_secondary(self, config):
        assert config.get_draft_order_bonus("WR", 1) == (30, "SECONDARY")


class TestNonFlexLiteralOnly:
    def test_te_literal_primary(self, config):
        assert config.get_draft_order_bonus("TE", 2) == (50, "PRIMARY")

    def test_rb_no_flex_key_no_bonus(self, config):
        # round 2 = {"TE": "P"} — no literal RB and no FLEX key
        assert config.get_draft_order_bonus("RB", 2) == (0, "")


class TestLiteralPrecedenceOverFlex:
    """When a round lists both a literal flex-eligible name and FLEX, literal wins."""

    def test_literal_wr_wins_over_flex(self, config):
        # round 3 = {"WR": "P", "FLEX": "S"} — WR should take the literal PRIMARY, not FLEX
        assert config.get_draft_order_bonus("WR", 3) == (50, "PRIMARY")

    def test_rb_falls_back_to_flex(self, config):
        # RB is not listed literally in round 3, so it uses the FLEX key
        assert config.get_draft_order_bonus("RB", 3) == (30, "SECONDARY")


class TestNonFlexEligibleNeverMatchesFlex:
    """A position outside FLEX_ELIGIBLE_POSITIONS must never collect a round's FLEX bonus.

    Guards the `position in self.flex_eligible_positions` clause of the FLEX-fallback
    branch. Without that clause every non-flex position would silently inherit the FLEX
    tier, and the rest of this file would still pass — so these are the only two cases
    that pin it. FLEX_ELIGIBLE_POSITIONS is ["RB", "WR"] in this fixture, so TE and DST
    are outside it.
    """

    def test_te_does_not_match_flex_key(self, config):
        # round 3 = {"WR": "P", "FLEX": "S"} — TE is not named natively and is not
        # FLEX-eligible, so it must take nothing (not the SECONDARY the FLEX key offers)
        assert config.get_draft_order_bonus("TE", 3) == (0, "")

    def test_dst_does_not_match_flex_key(self, config):
        # round 1 = {"QB": "P", "FLEX": "S"} — same rule for DST
        assert config.get_draft_order_bonus("DST", 1) == (0, "")
