"""
Tests for simulation.win_rate.config_overrides.apply_draft_overrides.

Covers nested placement + precision, DRAFT_ORDER application, preservation of all
other config keys, input immutability, and the three error paths (out-of-range,
missing key, unknown key). Pure dict transform — synthetic in-memory fixtures, no
file or network I/O.

Author: Kai Mizuno
"""

# Standard library
import copy

# Third-party
import pytest

# Local
from simulation.win_rate.config_overrides import apply_draft_overrides, DRAFT_PARAM_LOCATIONS
from utils.error_handler import ConfigurationError


@pytest.fixture
def base_config():
    """A synthetic config mirroring league_config.json's parameters shape."""
    return {
        "config_name": "test",
        "description": "test base",
        "parameters": {
            "CURRENT_NFL_WEEK": 17,
            "NFL_SEASON": 2025,
            "NFL_SCORING_FORMAT": "ppr",
            "SAME_POS_BYE_WEIGHT": 0.07,
            "DIFF_POS_BYE_WEIGHT": 0.01,
            "INJURY_PENALTIES": {"LOW": 0, "MEDIUM": 0, "HIGH": 0},
            "DRAFT_ORDER_BONUSES": {"PRIMARY": 67, "SECONDARY": 69},
            "DRAFT_ORDER": [{"QB": "P"}],
            "MAX_POSITIONS": {"QB": 2, "RB": 4, "WR": 4},
            "FLEX_ELIGIBLE_POSITIONS": ["RB", "WR"],
            "ADP_SCORING": {
                "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 25},
                "MULTIPLIERS": {"VERY_POOR": 0.95, "GOOD": 1.025},
                "WEIGHT": 4.76,
            },
            "PLAYER_RATING_SCORING": {
                "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 20},
                "MULTIPLIERS": {"VERY_POOR": 0.95, "GOOD": 1.025},
                "WEIGHT": 3.52,
            },
            "DRAFT_NORMALIZATION_MAX_SCALE": 150,
        },
    }


@pytest.fixture
def valid_param_values():
    """In-bounds, precision-correct values for all seven params."""
    return {
        "DRAFT_NORMALIZATION_MAX_SCALE": 160,
        "SAME_POS_BYE_WEIGHT": 0.10,
        "DIFF_POS_BYE_WEIGHT": 0.05,
        "PRIMARY_BONUS": 80,
        "SECONDARY_BONUS": 60,
        "ADP_SCORING_WEIGHT": 5.0,
        "PLAYER_RATING_SCORING_WEIGHT": 3.0,
    }


@pytest.fixture
def new_draft_order():
    return [{"RB": "P"}, {"WR": "S"}]


class TestApplyDraftOverrides:
    """Tests for apply_draft_overrides."""

    def test_placement_all_seven_params(self, base_config, valid_param_values, new_draft_order):
        result = apply_draft_overrides(base_config, new_draft_order, valid_param_values)
        params = result["parameters"]

        assert params["DRAFT_NORMALIZATION_MAX_SCALE"] == 160
        assert params["SAME_POS_BYE_WEIGHT"] == 0.10
        assert params["DIFF_POS_BYE_WEIGHT"] == 0.05
        assert params["DRAFT_ORDER_BONUSES"]["PRIMARY"] == 80
        assert params["DRAFT_ORDER_BONUSES"]["SECONDARY"] == 60
        assert params["ADP_SCORING"]["WEIGHT"] == 5.0
        assert params["PLAYER_RATING_SCORING"]["WEIGHT"] == 3.0

    def test_precision_rounding_applied(self, base_config, valid_param_values, new_draft_order):
        param_values = dict(valid_param_values)
        param_values["SAME_POS_BYE_WEIGHT"] = 0.073          # 2dp -> 0.07
        param_values["ADP_SCORING_WEIGHT"] = 5.756           # 2dp -> 5.76
        param_values["PRIMARY_BONUS"] = 80.4                 # int -> 80
        param_values["DRAFT_NORMALIZATION_MAX_SCALE"] = 160.6  # int -> 161

        result = apply_draft_overrides(base_config, new_draft_order, param_values)
        params = result["parameters"]

        assert params["SAME_POS_BYE_WEIGHT"] == 0.07
        assert params["ADP_SCORING"]["WEIGHT"] == 5.76
        assert params["DRAFT_ORDER_BONUSES"]["PRIMARY"] == 80
        assert params["DRAFT_NORMALIZATION_MAX_SCALE"] == 161

    def test_draft_order_applied_verbatim(self, base_config, valid_param_values, new_draft_order):
        result = apply_draft_overrides(base_config, new_draft_order, valid_param_values)
        assert result["parameters"]["DRAFT_ORDER"] == new_draft_order

    def test_other_keys_preserved(self, base_config, valid_param_values, new_draft_order):
        result = apply_draft_overrides(base_config, new_draft_order, valid_param_values)
        params = result["parameters"]

        assert params["CURRENT_NFL_WEEK"] == 17
        assert params["NFL_SEASON"] == 2025
        assert params["NFL_SCORING_FORMAT"] == "ppr"
        assert params["MAX_POSITIONS"] == {"QB": 2, "RB": 4, "WR": 4}
        assert params["FLEX_ELIGIBLE_POSITIONS"] == ["RB", "WR"]
        assert params["INJURY_PENALTIES"] == {"LOW": 0, "MEDIUM": 0, "HIGH": 0}
        # Sub-blocks of the two scoring sections are left intact (only WEIGHT changes).
        assert params["ADP_SCORING"]["THRESHOLDS"] == {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 25}
        assert params["ADP_SCORING"]["MULTIPLIERS"] == {"VERY_POOR": 0.95, "GOOD": 1.025}
        assert params["PLAYER_RATING_SCORING"]["THRESHOLDS"] == {"BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 20}

    def test_base_config_not_mutated(self, base_config, valid_param_values, new_draft_order):
        before = copy.deepcopy(base_config)
        result = apply_draft_overrides(base_config, new_draft_order, valid_param_values)

        assert base_config == before          # input untouched
        assert result is not base_config       # a new object was returned

    @pytest.mark.parametrize(
        "param, bad_value",
        [
            ("ADP_SCORING_WEIGHT", 9.9),   # above max 7.0
            ("PRIMARY_BONUS", 10),         # below min 25
        ],
    )
    def test_out_of_range_raises(self, base_config, valid_param_values, new_draft_order, param, bad_value):
        param_values = dict(valid_param_values)
        param_values[param] = bad_value
        with pytest.raises(ConfigurationError):
            apply_draft_overrides(base_config, new_draft_order, param_values)

    def test_missing_key_raises(self, base_config, valid_param_values, new_draft_order):
        param_values = dict(valid_param_values)
        del param_values["ADP_SCORING_WEIGHT"]
        with pytest.raises(ConfigurationError):
            apply_draft_overrides(base_config, new_draft_order, param_values)

    def test_unknown_key_raises(self, base_config, valid_param_values, new_draft_order):
        param_values = dict(valid_param_values)
        param_values["NOT_A_REAL_PARAM"] = 1.0
        with pytest.raises(ConfigurationError):
            apply_draft_overrides(base_config, new_draft_order, param_values)

    def test_locations_table_matches_param_definitions(self):
        # Guard: every flat name in the locations table exists in PARAM_DEFINITIONS.
        from simulation.shared.ConfigGenerator import ConfigGenerator
        for name in DRAFT_PARAM_LOCATIONS:
            assert name in ConfigGenerator.PARAM_DEFINITIONS


class TestExtractDraftParamValues:
    """Tests for extract_draft_param_values."""

    def test_extract_returns_seven_current_values(self, base_config):
        from simulation.win_rate.config_overrides import extract_draft_param_values, DRAFT_PARAM_LOCATIONS
        values = extract_draft_param_values(base_config)
        assert set(values.keys()) == set(DRAFT_PARAM_LOCATIONS.keys())
        assert values["DRAFT_NORMALIZATION_MAX_SCALE"] == 150
        assert values["SAME_POS_BYE_WEIGHT"] == 0.07
        assert values["PRIMARY_BONUS"] == 67
        assert values["SECONDARY_BONUS"] == 69
        assert values["ADP_SCORING_WEIGHT"] == 4.76
        assert values["PLAYER_RATING_SCORING_WEIGHT"] == 3.52

    def test_extract_then_apply_is_noop_for_params(self, base_config, new_draft_order):
        # Applying the extracted current values back changes only DRAFT_ORDER.
        from simulation.win_rate.config_overrides import extract_draft_param_values, apply_draft_overrides
        current = extract_draft_param_values(base_config)
        out = apply_draft_overrides(base_config, new_draft_order, current)
        op = out["parameters"]
        bp = base_config["parameters"]
        assert op["DRAFT_ORDER"] == new_draft_order
        assert op["DRAFT_ORDER_BONUSES"] == bp["DRAFT_ORDER_BONUSES"]
        assert op["ADP_SCORING"]["WEIGHT"] == bp["ADP_SCORING"]["WEIGHT"]
        assert op["DRAFT_NORMALIZATION_MAX_SCALE"] == bp["DRAFT_NORMALIZATION_MAX_SCALE"]
