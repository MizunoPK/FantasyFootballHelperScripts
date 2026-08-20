"""
Tests for simulation.win_rate.param_value_generation.generate_candidate_values.

Covers per-param bounds/precision, anchor inclusion, evenly-spaced count,
full-set-when-large, the num_values<=1 edge, determinism, 6-key output shape, and
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
    """The six current league_config values (all in-bounds, at precision)."""
    return {
        "SAME_POS_BYE_WEIGHT": 0.07,
        "DIFF_POS_BYE_WEIGHT": 0.01,
        "PRIMARY_BONUS": 67,
        "SECONDARY_BONUS": 69,
        "ADP_SCORING_WEIGHT": 4.76,
        "PLAYER_RATING_SCORING_WEIGHT": 5.52,
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
        # DIFF_POS_BYE_WEIGHT 0.0-0.75 @ 0.01 -> 76 discrete values.
        expected = sorted(set(_discrete_grid(0.0, 0.75, 2)))
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

    def test_output_has_six_keys(self, current_values):
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
        current_values["ADP_SCORING_WEIGHT"] = 20.0  # max is 14.0
        with pytest.raises(ConfigurationError):
            generate_candidate_values(current_values, num_values=5)

    def test_sweep_params_has_six_members_without_scale(self):
        # D1: the swept set drops DRAFT_NORMALIZATION_MAX_SCALE (7 -> 6).
        assert len(DRAFT_SWEEP_PARAMS) == 6
        assert "DRAFT_NORMALIZATION_MAX_SCALE" not in DRAFT_SWEEP_PARAMS

    def test_bye_weight_bounds_widened(self):
        # D2/D3, widened again: the 2026-08-18 sweep left both bye weights flat and
        # inconclusive across their whole range (SAME_POS 0.0-1.0 all within noise of 0.500),
        # so the ceilings rose to give the ascent somewhere new to look.
        #
        # The two ceilings are NOT interchangeable, and DIFF_POS's lower one is not the
        # arbitrary half-of-SAME_POS convention it looks like. _apply_bye_week_penalty sums
        # EVERY rostered player sharing the bye week into the diff-position term regardless
        # of position, but only genuine positional duplicates into the same-position term,
        # so the diff term compounds several times faster over a filling roster. A first
        # attempt at a shared 0.0-2.0 range dropped 100% of leagues: above ~1.05 the penalty
        # drives late-round candidate scores negative, PlayerManager.get_player_list's
        # score >= 0.0 floor filters the pool to empty, and the draft dies at 14/15 with
        # "No draft recommendations available - roster may be full". Measured clean 0/12
        # leagues at every DIFF_POS value through 1.0 and every SAME_POS value through 2.0.
        assert ConfigGenerator.PARAM_DEFINITIONS["SAME_POS_BYE_WEIGHT"] == (0.0, 2.0, 2)
        assert ConfigGenerator.PARAM_DEFINITIONS["DIFF_POS_BYE_WEIGHT"] == (0.0, 0.75, 2)

    def test_draft_order_bonus_floors_dropped_to_zero(self):
        # SECONDARY_BONUS converged to exactly 25 — its old `min`, not an interior optimum.
        # Every upward move lost decisively (87 -> 0.427 at z = -5.37, the largest effect
        # anywhere in the store), so the floor, not the landscape, chose the value. Both
        # bonuses drop to a 0 floor (0 = the bonus off entirely) and gain upward room.
        assert ConfigGenerator.PARAM_DEFINITIONS["PRIMARY_BONUS"] == (0, 300, 0)
        assert ConfigGenerator.PARAM_DEFINITIONS["SECONDARY_BONUS"] == (0, 300, 0)

    def test_scoring_weight_ceilings_widened(self):
        # Raised 7.00 -> 10.00 for BOTH scoring weights. Same failure mode that drove the
        # earlier 4.00 -> 7.00 widening, observed again: the 2026-08-18 sweep converged with
        # ADP_SCORING_WEIGHT and PLAYER_RATING_SCORING_WEIGHT both pinned at exactly 7.00, so
        # every candidate the grid could offer was downward and a true optimum above 7.0 was
        # unreachable — reported as "no improvement", indistinguishable from "7.0 is right".
        assert ConfigGenerator.PARAM_DEFINITIONS["ADP_SCORING_WEIGHT"] == (4.00, 14.00, 2)
        assert ConfigGenerator.PARAM_DEFINITIONS["PLAYER_RATING_SCORING_WEIGHT"] == (4.00, 14.00, 2)

    def test_scoring_weight_grids_reach_above_the_old_ceiling(self, current_values):
        result = generate_candidate_values(current_values, num_values=1000)
        assert max(result["PLAYER_RATING_SCORING_WEIGHT"]) == 14.00
        assert max(result["ADP_SCORING_WEIGHT"]) == 14.00
        # The floor rose too: every value below 4.0 was refuted (ADP 0.5 lost at z = -4.83),
        # so the grid no longer spends evaluations down there.
        assert min(result["ADP_SCORING_WEIGHT"]) == 4.00

    def test_bye_weight_grid_spans_widened_range(self, current_values):
        # The candidate grid reaches above the old 0.5/0.3 ceilings.
        result = generate_candidate_values(current_values, num_values=1000)
        assert max(result["SAME_POS_BYE_WEIGHT"]) == 2.0
        assert max(result["DIFF_POS_BYE_WEIGHT"]) == 0.75
        assert any(v > 1.0 for v in result["SAME_POS_BYE_WEIGHT"])
        assert any(v > 0.5 for v in result["DIFF_POS_BYE_WEIGHT"])
        assert any(v > 0.3 for v in result["DIFF_POS_BYE_WEIGHT"])
