"""
Unit Tests for ConfigManager.get_survival_multiplier() and the SURVIVAL_SCORING
optional-key no-op default (D18.3, provision stage).

Two fixtures exercise the two independent no-op axes and the real-config path:
- config_default: SURVIVAL_SCORING absent from league_config.json -> the .get()
  fallback (WEIGHT: 0.0) applies, so get_survival_multiplier must return exactly
  (1.0, <any label>) for every margin, including a no-ADP (None) margin and an
  out-of-range margin.
- config_survival: SURVIVAL_SCORING present with non-neutral values -> tier
  selection must match _get_multiplier's documented rising_thresholds=False
  BUCKETED logic exactly, the same logic ADP_SCORING already exercises in
  test_ConfigManager_adp_ladder.py.

Author: Kai Mizuno
"""

import json

import pytest

from league_helper.util.ConfigManager import ConfigManager, ConfigKeys


def _base_parameters():
    """The required-parameters skeleton every ConfigManager fixture in this
    suite needs at load time (test_ConfigManager_draft_order_bonus.py's exact
    shape); SURVIVAL_SCORING is deliberately NOT included here since it is the
    one key each fixture below varies."""
    return {
        "CURRENT_NFL_WEEK": 1,
        "NFL_SEASON": 2026,
        "NFL_SCORING_FORMAT": "ppr",
        "NORMALIZATION_MAX_SCALE": 100.0,
        "DRAFT_NORMALIZATION_MAX_SCALE": 150,
        "SAME_POS_BYE_WEIGHT": 1.0,
        "DIFF_POS_BYE_WEIGHT": 1.0,
        "INJURY_PENALTIES": {"LOW": 0, "MEDIUM": 10, "HIGH": 75},
        "DRAFT_ORDER_BONUSES": {"PRIMARY": 50, "SECONDARY": 30},
        "DRAFT_ORDER": [{"WR": "P", "RB": "S"}],
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
    }


@pytest.fixture
def temp_data_folder(tmp_path):
    data_folder = tmp_path / "data"
    data_folder.mkdir()
    return data_folder


@pytest.fixture
def config_default(temp_data_folder):
    """SURVIVAL_SCORING absent -- the D18.3 .get() no-op default must apply."""
    cfg = {
        "config_name": "test",
        "description": "survival scoring absent-key no-op",
        "parameters": _base_parameters(),
    }
    (temp_data_folder / "league_config.json").write_text(json.dumps(cfg))
    return ConfigManager(temp_data_folder)


@pytest.fixture
def config_survival(tmp_path):
    """SURVIVAL_SCORING present with non-neutral values -- real tier selection."""
    data_folder = tmp_path / "data_survival"
    data_folder.mkdir()
    params = _base_parameters()
    params["SURVIVAL_SCORING"] = {
        "THRESHOLDS": {"EXCELLENT": -20, "GOOD": -5, "POOR": 5, "VERY_POOR": 20},
        "MULTIPLIERS": {"EXCELLENT": 1.5, "GOOD": 1.2, "POOR": 0.9, "VERY_POOR": 0.6},
        "WEIGHT": 1.0,
    }
    cfg = {
        "config_name": "test",
        "description": "survival scoring configured",
        "parameters": params,
    }
    (data_folder / "league_config.json").write_text(json.dumps(cfg))
    return ConfigManager(data_folder)


@pytest.fixture
def config_malformed(tmp_path):
    """SURVIVAL_SCORING present but missing WEIGHT -- must raise KeyError lazily,
    at first use, not at ConfigManager construction (D18.3's deliberate
    unregistered-in-_multiplier_factors() scope decision)."""
    data_folder = tmp_path / "data_malformed"
    data_folder.mkdir()
    params = _base_parameters()
    params["SURVIVAL_SCORING"] = {
        "THRESHOLDS": {"EXCELLENT": -20, "GOOD": -5, "POOR": 5, "VERY_POOR": 20},
        "MULTIPLIERS": {"EXCELLENT": 1.5, "GOOD": 1.2, "POOR": 0.9, "VERY_POOR": 0.6},
        # WEIGHT deliberately omitted
    }
    cfg = {
        "config_name": "test",
        "description": "survival scoring malformed (missing WEIGHT)",
        "parameters": params,
    }
    (data_folder / "league_config.json").write_text(json.dumps(cfg))
    return ConfigManager(data_folder)


class TestSurvivalScoringAbsentKeyNoOp:
    """SURVIVAL_SCORING absent from league_config.json: verified no-op."""

    def test_construction_does_not_raise(self, config_default):
        # ConfigManager() succeeding at all is itself part of the no-op guarantee --
        # an absent OPTIONAL key must never fail config load.
        assert config_default.survival_scoring["WEIGHT"] == 0.0

    def test_multiplier_is_always_1_0_regardless_of_margin(self, config_default):
        for margin in (-500, -100, -25, -1, 0, 1, 25, 100, 500, 1e9):
            multiplier, _label = config_default.get_survival_multiplier(margin)
            assert multiplier == 1.0, f"margin={margin} produced multiplier={multiplier}"

    def test_none_margin_returns_neutral(self, config_default):
        multiplier, label = config_default.get_survival_multiplier(None)
        assert multiplier == 1.0
        assert label == ConfigKeys.NEUTRAL


class TestSurvivalScoringConfiguredTierSelection:
    """SURVIVAL_SCORING present: real BUCKETED tier selection, mirroring
    _get_multiplier's documented rising_thresholds=False logic (ConfigManager.py,
    same logic test_ConfigManager_adp_ladder.py already pins for ADP_SCORING)."""

    def test_margin_at_or_below_excellent_threshold(self, config_survival):
        multiplier, label = config_survival.get_survival_multiplier(-25)
        assert (multiplier, label) == (1.5, "EXCELLENT")

    def test_margin_at_or_below_good_threshold(self, config_survival):
        multiplier, label = config_survival.get_survival_multiplier(-5)
        assert (multiplier, label) == (1.2, "GOOD")

    def test_margin_between_good_and_poor_is_neutral(self, config_survival):
        multiplier, label = config_survival.get_survival_multiplier(0)
        assert (multiplier, label) == (1.0, "NEUTRAL")

    def test_margin_at_or_above_poor_threshold(self, config_survival):
        multiplier, label = config_survival.get_survival_multiplier(5)
        assert (multiplier, label) == (0.9, "POOR")

    def test_margin_at_or_above_very_poor_threshold(self, config_survival):
        multiplier, label = config_survival.get_survival_multiplier(20)
        assert (multiplier, label) == (0.6, "VERY_POOR")

    def test_margin_far_beyond_very_poor_clamps_not_raises(self, config_survival):
        """Out-of-range: _get_multiplier's BUCKETED branch clamps to the outermost
        matching tier rather than raising -- the same graceful behavior every
        other _get_multiplier consumer already has."""
        multiplier, label = config_survival.get_survival_multiplier(999999)
        assert (multiplier, label) == (0.6, "VERY_POOR")

    def test_none_margin_returns_neutral_even_when_configured(self, config_survival):
        multiplier, label = config_survival.get_survival_multiplier(None)
        assert multiplier == 1.0
        assert label == ConfigKeys.NEUTRAL


class TestSurvivalScoringMalformedConfig:
    """A malformed SURVIVAL_SCORING block raises KeyError lazily, at first use --
    the deliberate, documented consequence of D18.3's provision-stage scope
    decision to leave this key out of _multiplier_factors()' eager guard."""

    def test_missing_weight_raises_keyerror_on_first_use(self, config_malformed):
        with pytest.raises(KeyError):
            config_malformed.get_survival_multiplier(0)

    def test_construction_itself_does_not_raise(self, config_malformed):
        # The malformed block is accepted at load time (unregistered in
        # _multiplier_factors()) -- the failure is deferred to first use, by design.
        assert "WEIGHT" not in config_malformed.survival_scoring
