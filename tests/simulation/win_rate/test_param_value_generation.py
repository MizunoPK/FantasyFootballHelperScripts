"""
Tests for simulation.win_rate.param_value_generation.generate_candidate_values.

Covers per-param bounds/precision, anchor inclusion, evenly-spaced count,
full-set-when-large, the num_values<=1 edge, determinism, 7-key output shape, and
the three error paths. Pure deterministic transform — synthetic in-memory inputs.

Author: Kai Mizuno
"""

# Third-party
import pytest

# Local
from simulation.win_rate.param_value_generation import (
    generate_candidate_values,
    DRAFT_SWEEP_PARAMS,
    _discrete_grid,
)
from simulation.shared.ConfigGenerator import ConfigGenerator
from utils.error_handler import ConfigurationError


@pytest.fixture
def current_values():
    """The seven current league_config values (all in-bounds, at precision)."""
    return {
        "DRAFT_NORMALIZATION_MAX_SCALE": 150,
        "SAME_POS_BYE_WEIGHT": 0.07,
        "DIFF_POS_BYE_WEIGHT": 0.01,
        "PRIMARY_BONUS": 67,
        "SECONDARY_BONUS": 69,
        "ADP_SCORING_WEIGHT": 4.76,
        "PLAYER_RATING_SCORING_WEIGHT": 3.52,
    }


class TestGenerateCandidateValues:
    """Tests for generate_candidate_values."""

    def test_values_within_bounds_and_precision(self, current_values):
        result = generate_candidate_values(current_values, num_values=5)
        for name in DRAFT_SWEEP_PARAMS:
            min_val, max_val, precision = ConfigGenerator.PARAM_DEFINITIONS[name]
            for v in result[name]:
                assert min_val <= v <= max_val
                if precision == 0:
                    assert isinstance(v, int)
                else:
                    assert round(v, precision) == v

    def test_anchor_included(self, current_values):
        result = generate_candidate_values(current_values, num_values=5)
        for name in DRAFT_SWEEP_PARAMS:
            _, _, precision = ConfigGenerator.PARAM_DEFINITIONS[name]
            raw = current_values[name]
            anchor = int(round(raw)) if precision == 0 else round(raw, precision)
            assert anchor in result[name]

    def test_count_evenly_spaced(self, current_values):
        # On large ranges, num_values=5 evenly-spaced values include both endpoints.
        result = generate_candidate_values(current_values, num_values=5)
        for name in ["ADP_SCORING_WEIGHT", "PRIMARY_BONUS"]:
            min_val, max_val, _ = ConfigGenerator.PARAM_DEFINITIONS[name]
            assert min_val in result[name]
            assert max_val in result[name]
            # 5 evenly-spaced picks, plus the anchor if not among them -> at most 6.
            assert 5 <= len(result[name]) <= 6

    def test_full_set_when_count_exceeds_range(self, current_values):
        result = generate_candidate_values(current_values, num_values=1000)
        # DIFF_POS_BYE_WEIGHT 0.0-0.3 @ 0.01 -> 31 discrete values.
        expected = sorted(set(_discrete_grid(0.0, 0.3, 2)))
        assert result["DIFF_POS_BYE_WEIGHT"] == expected

    def test_num_values_one_returns_anchor(self, current_values):
        result = generate_candidate_values(current_values, num_values=1)
        for name in DRAFT_SWEEP_PARAMS:
            _, _, precision = ConfigGenerator.PARAM_DEFINITIONS[name]
            raw = current_values[name]
            anchor = int(round(raw)) if precision == 0 else round(raw, precision)
            assert result[name] == [anchor]

    def test_deterministic_repeated_calls_equal(self, current_values):
        a = generate_candidate_values(current_values, num_values=5)
        b = generate_candidate_values(current_values, num_values=5)
        assert a == b

    def test_output_has_seven_keys(self, current_values):
        result = generate_candidate_values(current_values, num_values=5)
        assert set(result.keys()) == set(DRAFT_SWEEP_PARAMS)
        for name in DRAFT_SWEEP_PARAMS:
            assert result[name] == sorted(result[name])

    def test_missing_key_raises(self, current_values):
        del current_values["ADP_SCORING_WEIGHT"]
        with pytest.raises(ConfigurationError):
            generate_candidate_values(current_values, num_values=5)

    def test_unknown_key_raises(self, current_values):
        current_values["NOT_A_REAL_PARAM"] = 1.0
        with pytest.raises(ConfigurationError):
            generate_candidate_values(current_values, num_values=5)

    def test_out_of_range_raises(self, current_values):
        current_values["ADP_SCORING_WEIGHT"] = 9.9  # max is 7.0
        with pytest.raises(ConfigurationError):
            generate_candidate_values(current_values, num_values=5)
