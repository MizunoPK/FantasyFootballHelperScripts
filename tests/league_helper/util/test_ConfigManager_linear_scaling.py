"""
Unit Tests for LINEAR Multiplier Scaling

Covers ConfigManager's SCALING dispatch (D10.1) -- the per-factor selector that chooses
between the retained BUCKETED step function and the new LINEAR piecewise interpolation
over the four threshold-sorted anchors, plus the two load-time validations that gate it
and the LINEAR arm of the tier-reachability guard.

Six concerns, one file:
  * SCALING is validated at CONFIG LOAD -- both legal spellings load, an unrecognized
    value raises, and the check reaches a LITERAL ladder that carries no BASE_POSITION
    (TD4),
  * a LINEAR ladder's four thresholds must be DISTINCT, checked AFTER derived-ladder
    expansion so a BASE_POSITION ladder still loads clean (TD2a),
  * LINEAR is bit- and label-identical to BUCKETED at all four anchors and genuinely
    different strictly between them (TD1, TD3 clause 1),
  * the label follows TD3's three ordered clauses, and the branch is ladder-faithful --
    it neither reads nor can be rescued by `rising_thresholds` (TD2),
  * the BUCKETED branch and the `val is None` arm are RETAINED unchanged,
  * the tier-reachability guard requires five labels for BUCKETED and exactly the four
    configured anchors for LINEAR (D5.1's guard, made mode-aware here).

Every expected value in this file was OBSERVED, not predicted: the bucketed figures come
from running the real ConfigManager over the live data/configs/ store, and the linear
figures from running the interpolation over the same geometry. See the unit's
test_build_plan.md section "Observed-Value Provenance" for the reproduction commands and
the measured corridors these assertions sit inside.

Author: Claude Code
Date: 2026-08-17
"""

import json
from pathlib import Path

import pytest

from league_helper.util.ConfigManager import ConfigManager


LEAGUE_FIXTURE = Path("tests/fixtures/league/league_config.json")
LIVE_CONFIG_ROOT = Path("data")

# The LIVE ladder geometry, transcribed from data/configs/league_config.json as resolved
# by calculate_thresholds (BASE_POSITION 0, STEPS 20). Replicated as a LITERAL fixture
# ladder rather than read from the live store, because a fixture must be able to carry
# SCALING: "LINEAR" and the live store deliberately stays BUCKETED until a cutover (TD4).
# WEIGHT is the live 2.12 / 4.0 and never 1.0 -- at WEIGHT 1.0 the two TD1 orders are
# mathematically identical and the order test would be vacuous.
ADP_THRESHOLDS = {"EXCELLENT": 20, "GOOD": 40, "POOR": 60, "VERY_POOR": 80}
PLAYER_RATING_THRESHOLDS = {"VERY_POOR": 20, "POOR": 40, "GOOD": 60, "EXCELLENT": 80}
MULTIPLIERS = {"VERY_POOR": 0.95, "POOR": 0.975, "GOOD": 1.025, "EXCELLENT": 1.05}
ADP_WEIGHT = 2.12
PLAYER_RATING_WEIGHT = 4.0


# FIXTURES

@pytest.fixture
def league_params():
    """A complete, guard-clean legacy config, re-read so a test may mutate it freely."""
    return json.loads(LEAGUE_FIXTURE.read_text())


def _write_legacy_config(tmp_path, data):
    """Write `data` as a legacy single-file config; return the data folder."""
    (tmp_path / "league_config.json").write_text(json.dumps(data))
    return tmp_path


def _put_literal_ladder(data, scoring_key, thresholds, weight, scaling=None):
    """Replace one scoring block with a LITERAL ladder (no BASE_POSITION).

    A literal ladder is the shape calculate_thresholds never sees, so it is the only
    shape on which TD2a's distinctness raise and TD4's unrecognized-value raise can be
    authored as genuine negatives.

    Args:
        data: The whole config dict, mutated in place.
        scoring_key: The scoring-type key, e.g. "ADP_SCORING".
        thresholds: The four tier thresholds, authored directly.
        weight: The WEIGHT exponent for that block.
        scaling: The SCALING value to author, or None to author no SCALING key at all.

    Returns:
        The mutated config dict.
    """
    block = {
        "THRESHOLDS": dict(thresholds),
        "MULTIPLIERS": dict(MULTIPLIERS),
        "WEIGHT": weight,
    }
    # Non-ladder keys the factor's own accessor still needs are carried over rather than
    # dropped -- rebuilding the block wholesale would otherwise silently delete
    # MIN_WEEKS / IMPACT_SCALE / IDEAL_TEMPERATURE and change an unrelated code path.
    for carried in ("MIN_WEEKS", "IMPACT_SCALE", "IDEAL_TEMPERATURE"):
        if carried in data["parameters"].get(scoring_key, {}):
            block[carried] = data["parameters"][scoring_key][carried]
    if scaling is not None:
        block["SCALING"] = scaling
    data["parameters"][scoring_key] = block
    return data


def _config_with(tmp_path, data):
    """Build a ConfigManager over `data` written into tmp_path."""
    return ConfigManager(_write_legacy_config(tmp_path, data))


def _assert_multiplier(actual, expected):
    """Assert a (multiplier, label) pair: label EXACTLY, multiplier via pytest.approx.

    Multipliers are `MULTIPLIERS[...] ** WEIGHT` results with a non-integer WEIGHT, so
    exact float equality on them is brittle across platforms and libm implementations,
    and inconsistent with this suite's general use of pytest.approx. The LABEL is an
    exact claim and stays one.

    NOTE: this helper is for comparisons against a hard-coded literal only. A direct
    linear-vs-bucketed tuple comparison stays EXACT `==`, because bit-identity at the
    anchors is precisely what TD1 / TD3 clause 1 assert -- both sides are computed in
    the same process by the same expression, so approx there would weaken the claim.

    Args:
        actual: The (multiplier, label) pair returned by an accessor.
        expected: The (multiplier, label) pair expected.
    """
    assert actual[1] == expected[1]
    assert actual[0] == pytest.approx(expected[0], abs=1e-12)


@pytest.fixture
def linear_adp(tmp_path, league_params):
    """ConfigManager whose ADP_SCORING is a LINEAR literal ladder on live geometry."""
    _put_literal_ladder(league_params, "ADP_SCORING", ADP_THRESHOLDS, ADP_WEIGHT,
                        scaling="LINEAR")
    return _config_with(tmp_path, league_params)


@pytest.fixture
def bucketed_adp(tmp_path, league_params):
    """The SAME geometry with SCALING absent -- the byte-identity comparison partner."""
    _put_literal_ladder(league_params, "ADP_SCORING", ADP_THRESHOLDS, ADP_WEIGHT)
    return _config_with(tmp_path, league_params)


@pytest.fixture
def linear_player_rating(tmp_path, league_params):
    """ConfigManager whose PLAYER_RATING_SCORING is a LINEAR literal INCREASING ladder."""
    _put_literal_ladder(league_params, "PLAYER_RATING_SCORING",
                        PLAYER_RATING_THRESHOLDS, PLAYER_RATING_WEIGHT,
                        scaling="LINEAR")
    return _config_with(tmp_path, league_params)


@pytest.fixture
def bucketed_player_rating(tmp_path, league_params):
    """The SAME INCREASING geometry with SCALING absent."""
    _put_literal_ladder(league_params, "PLAYER_RATING_SCORING",
                        PLAYER_RATING_THRESHOLDS, PLAYER_RATING_WEIGHT)
    return _config_with(tmp_path, league_params)


# TD4 -- THE SCALING SELECTOR IS VALIDATED AT CONFIG LOAD (obligation item 8)

class TestScalingValidation:
    """SCALING accepts exactly two spellings and raises on anything else, at load."""

    def test_absent_scaling_loads_and_selects_the_step_branch(self, bucketed_adp):
        """Absent => BUCKETED (TD4) is what makes this unit's landing dark."""
        # Act
        multiplier, label = bucketed_adp.get_adp_multiplier(30)

        # Assert -- label exactly, multiplier via approx: the value comes out of
        # `MULTIPLIERS[...] ** WEIGHT` with a non-integer WEIGHT, and exact float
        # equality on a libm pow result is brittle across platforms. approx is this
        # suite's established convention for computed multipliers.
        assert label == "GOOD"
        assert multiplier == pytest.approx(1.053742737956907, abs=1e-12)

    def test_explicit_bucketed_spelling_loads_and_selects_the_step_branch(
        self, tmp_path, league_params
    ):
        """The explicit spelling must be legal, not merely the absent default."""
        # Arrange
        _put_literal_ladder(league_params, "ADP_SCORING", ADP_THRESHOLDS, ADP_WEIGHT,
                            scaling="BUCKETED")

        # Act
        config = _config_with(tmp_path, league_params)

        # Assert
        multiplier, label = config.get_adp_multiplier(30)
        assert label == "GOOD"
        assert multiplier == pytest.approx(1.053742737956907, abs=1e-12)

    def test_linear_spelling_loads(self, linear_adp):
        """The LINEAR spelling loads and reaches the interpolation branch."""
        # Assert
        multiplier, label = linear_adp.get_adp_multiplier(30)
        assert label == "EXCELLENT"
        assert multiplier == pytest.approx(1.0811719838761076, abs=1e-12)

    def test_unrecognized_scaling_raises_on_a_literal_ladder(
        self, tmp_path, league_params
    ):
        """The check must sit OUTSIDE the BASE_POSITION guard (TD4).

        A literal ladder never enters that guard, so a check placed inside it would let
        an unrecognized value through on exactly this shape.
        """
        # Arrange
        _put_literal_ladder(league_params, "ADP_SCORING", ADP_THRESHOLDS, ADP_WEIGHT,
                            scaling="SIGMOID")

        # Act
        with pytest.raises(ValueError) as excinfo:
            _config_with(tmp_path, league_params)

        # Assert
        message = str(excinfo.value)
        assert "ADP_SCORING" in message
        assert "SCALING" in message
        assert "SIGMOID" in message

    def test_unrecognized_scaling_raises_on_a_derived_ladder(
        self, tmp_path, league_params
    ):
        """The derived shape is the DOMINANT one on disk, so it is covered too."""
        # Arrange -- the fixture's ADP block is already BASE_POSITION-derived
        league_params["parameters"]["ADP_SCORING"]["SCALING"] = "linear"

        # Act
        with pytest.raises(ValueError) as excinfo:
            _config_with(tmp_path, league_params)

        # Assert -- the comparison is exact, so a lowercase spelling is NOT legal
        assert "SCALING" in str(excinfo.value)


# TD2a -- A LINEAR LADDER'S FOUR ANCHORS MUST BE DISTINCT (obligation item 9)

class TestLinearLadderDistinctness:
    """The distinctness guard, its ordering, and the branch's zero-width safety."""

    def test_duplicate_thresholds_raise_on_a_literal_linear_ladder(
        self, tmp_path, league_params
    ):
        """NEGATIVE case. Authorable only on a literal ladder.

        calculate_thresholds can never emit a degenerate ladder (STEPS <= 0 already
        raises, and any positive STEPS yields four distinct multiples), so a derived
        ladder cannot express this defect.
        """
        # Arrange -- GOOD and POOR collide
        degenerate = {"EXCELLENT": 20, "GOOD": 40, "POOR": 40, "VERY_POOR": 80}
        _put_literal_ladder(league_params, "ADP_SCORING", degenerate, ADP_WEIGHT,
                            scaling="LINEAR")

        # Act
        with pytest.raises(ValueError) as excinfo:
            _config_with(tmp_path, league_params)

        # Assert
        message = str(excinfo.value)
        assert "ADP_SCORING" in message
        assert "distinct" in message

    def test_a_derived_linear_ladder_loads_clean(self, tmp_path, league_params):
        """POSITIVE case -- the detector for a MIS-ORDERED distinctness check.

        The four tier keys the check reads are written INSIDE the
        `if BASE_POSITION in thresholds_config:` block. A check placed before that block
        sees only {BASE_POSITION, DIRECTION, STEPS} and would raise on every load of a
        derived ladder -- which is the shape the post-cutover live config carries. This
        test also traverses the mode-aware reachability guard on the way through.
        """
        # Arrange -- keep the fixture's BASE_POSITION-derived ADP ladder, add SCALING
        league_params["parameters"]["ADP_SCORING"]["SCALING"] = "LINEAR"

        # Act
        config = _config_with(tmp_path, league_params)

        # Assert -- the derived ladder resolved and the linear branch is live on it
        thresholds = config.adp_scoring["THRESHOLDS"]
        assert sorted(thresholds[tier] for tier in
                      ("VERY_POOR", "POOR", "GOOD", "EXCELLENT")) == [25, 50, 75, 100]

    def test_a_degenerate_ladder_cannot_divide_by_zero(self, linear_adp):
        """DIRECT no-ZeroDivisionError check over a degenerate ladder.

        This does NOT execute the `width == 0` branch, and no input can: the segment
        loop's strict bounds (`if not lower < val < upper: continue`) skip the degenerate
        segment outright, which is precisely why that branch is a declared
        non-distinguisher (CODING_STANDARDS.md:123-124). What this test pins is the
        reachable claim -- that a post-load-mutated degenerate ladder still returns an
        anchor's own value without raising.

        The ladder is made degenerate AFTER load, which is the only way to reach the
        branch with a ladder config-load validation would have rejected -- i.e. exactly
        the "future caller bypasses load validation" case the clause names. At a
        duplicated threshold the result is that anchor's OWN value and label (TD3
        clause 1); which of the two colliding anchors wins is not asserted, because the
        ladder is contradictory by construction and the load guard rejects it.
        """
        # Arrange
        linear_adp.adp_scoring["THRESHOLDS"] = {
            "EXCELLENT": 20, "GOOD": 40, "POOR": 40, "VERY_POOR": 80}

        # Act -- probing across, at, and outside the zero-width segment
        results = [linear_adp.get_adp_multiplier(val)
                   for val in (10, 30, 40, 50, 90)]

        # Assert -- no exception reached this line, and the at-anchor probe took an
        # anchor's own value rather than an interpolated one
        at_anchor_multiplier, at_anchor_label = results[2]
        assert at_anchor_label in ("GOOD", "POOR")
        assert at_anchor_multiplier == pytest.approx(
            MULTIPLIERS[at_anchor_label] ** ADP_WEIGHT, abs=1e-12)


# THE RETAINED BUCKETED BRANCH (obligation item 10)

class TestBucketedRetention:
    """The step branch is RETAINED, not replaced -- it still serves six live factors."""

    @pytest.mark.parametrize("adp,expected", [
        (10, (1.1089738719028956, "EXCELLENT")),
        (20, (1.1089738719028956, "EXCELLENT")),
        (30, (1.053742737956907, "GOOD")),
        (50, (1.0, "NEUTRAL")),
        (70, (0.9477412538801717, "POOR")),
        (90, (0.8969619974461313, "VERY_POOR")),
    ])
    def test_step_branch_still_returns_its_five_values_and_labels(
        self, bucketed_adp, adp, expected
    ):
        """A direct, asserting test of the bucketed branch -- the first in the suite.

        Existing live-store runs pin aggregates and structural invariants, never a
        factor's multiplier or label, so a bucketed regression would previously have
        surfaced as an unexplained number rather than a named failure.
        """
        # Assert
        _assert_multiplier(bucketed_adp.get_adp_multiplier(adp), expected)


# THE `val is None` ARM IS UNCHANGED (obligation item 11)

class TestNoneIsNeutralUnderLinear:
    """None means "no data", which is a different statement from any tier (TD3)."""

    def test_none_adp_is_neutral_under_linear(self, linear_adp):
        """The arm precedes the mode dispatch and must not be tidied into LINEAR."""
        assert linear_adp.get_adp_multiplier(None) == (1.0, "NEUTRAL")

    def test_none_player_rating_is_neutral_under_linear(self, linear_player_rating):
        """The same arm, the other polarity."""
        assert linear_player_rating.get_player_rating_multiplier(None) == (1.0, "NEUTRAL")


# TD1 / TD3 CLAUSE 1 -- BIT- AND LABEL-IDENTITY AT THE ANCHORS (items 1 and 4)

class TestAnchorIdentity:
    """At an anchor, LINEAR returns that anchor's own multiplier AND label.

    Asserted TWO ways on purpose: against the BUCKETED partner over identical geometry
    (the backward-compatibility claim) and against an absolute observed value (so both
    branches breaking identically cannot pass). Both polarities are covered -- ADP is a
    DECREASING ladder, player rating an INCREASING one.
    """

    @pytest.mark.parametrize("adp,expected", [
        (20, (1.1089738719028956, "EXCELLENT")),
        (40, (1.053742737956907, "GOOD")),
        (60, (0.9477412538801717, "POOR")),
        (80, (0.8969619974461313, "VERY_POOR")),
    ])
    def test_linear_matches_bucketed_at_every_adp_anchor(
        self, linear_adp, bucketed_adp, adp, expected
    ):
        # Act
        linear = linear_adp.get_adp_multiplier(adp)
        bucketed = bucketed_adp.get_adp_multiplier(adp)

        # Assert
        # Bit-identity between the two modes stays an EXACT comparison -- that is the
        # TD1 / TD3-clause-1 claim itself. Only the hard-coded literal uses approx.
        assert linear == bucketed
        _assert_multiplier(linear, expected)

    def test_an_interior_anchor_takes_its_own_value_not_a_segment_interpolation(
        self, linear_adp
    ):
        """TD3 clause 1 IN ISOLATION -- the clause no other test targets on its own.

        ADP 40 is the shared boundary of the 20..40 and 40..60 segments, so clause 3
        alone is ambiguous there, and the two live factors need OPPOSITE segment
        preferences -- which is exactly why clause 1 exists and why no uniform
        prefer-upper / prefer-lower convention substitutes for it. This asserts the
        resolution directly rather than as a by-product of the bucketed comparison:
        ADP 40 takes GOOD's OWN base multiplier under the shared exponent.
        """
        # Act
        multiplier, label = linear_adp.get_adp_multiplier(40)

        # Assert
        assert label == "GOOD"
        assert multiplier == pytest.approx(MULTIPLIERS["GOOD"] ** ADP_WEIGHT, abs=1e-12)
        assert multiplier == pytest.approx(1.053742737956907, abs=1e-12)

    @pytest.mark.parametrize("rating,expected", [
        (20, (0.8145062499999999, "VERY_POOR")),
        (40, (0.9036878906249999, "POOR")),
        (60, (1.1038128906249995, "GOOD")),
        (80, (1.2155062500000002, "EXCELLENT")),
    ])
    def test_linear_matches_bucketed_at_every_player_rating_anchor(
        self, linear_player_rating, bucketed_player_rating, rating, expected
    ):
        # Act
        linear = linear_player_rating.get_player_rating_multiplier(rating)
        bucketed = bucketed_player_rating.get_player_rating_multiplier(rating)

        # Assert
        assert linear == bucketed
        _assert_multiplier(linear, expected)


# TD3 CLAUSE 3 -- STRICTLY BETWEEN ANCHORS (items 2 and 5)

class TestInteriorDiscrimination:
    """Interior points are where LINEAR and BUCKETED genuinely disagree."""

    def test_adp_30_linear_value_differs_from_bucketed(self, linear_adp, bucketed_adp):
        """ADP 30, NOT ADP 50.

        At ADP 50 both modes return exactly 1.0, so an ADP-50 value assertion would pass
        with the interpolation branch entirely absent. ADP 30 also sits outside the
        bucketed NEUTRAL band, so the comparison is not confounded by the band.
        """
        # Act
        linear_multiplier, _ = linear_adp.get_adp_multiplier(30)
        bucketed_multiplier, _ = bucketed_adp.get_adp_multiplier(30)

        # Assert
        assert linear_multiplier == pytest.approx(1.0811719838761076, abs=1e-12)
        assert bucketed_multiplier == pytest.approx(1.053742737956907, abs=1e-12)
        assert linear_multiplier != pytest.approx(bucketed_multiplier, abs=1e-12)

    def test_adp_30_linear_label_is_excellent(self, linear_adp):
        """The better side of a DECREASING ladder is the LOWER-valued anchor (20)."""
        assert linear_adp.get_adp_multiplier(30)[1] == "EXCELLENT"

    def test_player_rating_50_linear_label_is_good(
        self, linear_player_rating, bucketed_player_rating
    ):
        """The opposite polarity: the better side is the HIGHER-valued anchor (60).

        The value ties at 1.0 here, so the LABEL is what discriminates -- BUCKETED calls
        rating 50 NEUTRAL and LINEAR calls it GOOD.
        """
        # Act
        linear = linear_player_rating.get_player_rating_multiplier(50)
        bucketed = bucketed_player_rating.get_player_rating_multiplier(50)

        # Assert
        assert linear == (1.0, "GOOD")
        assert bucketed == (1.0, "NEUTRAL")


# TD1 -- INTERPOLATE THE BASE MULTIPLIER, THEN APPLY THE EXPONENT (item 3)

class TestInterpolationOrder:
    """The exponent is applied AFTER interpolation, not to the four anchor results."""

    def test_base_multiplier_is_interpolated_before_the_weight_exponent(
        self, linear_adp
    ):
        """Discriminating only because WEIGHT is the live 2.12 rather than 1.0.

        At WEIGHT 1.0 the two orders are mathematically identical and this test would be
        vacuous. The two models differ by a measured 6.710138553334133e-05 at ADP 22, so
        the tolerance below is four orders of magnitude tighter than the gap -- the
        assertion sits well inside the measured corridor, not at its edge.
        """
        # Arrange -- interpolating the four POST-exponent anchor values instead gives
        # 1.1034507585082969 at ADP 22 (measured, not predicted).
        base_first = 1.1033836571227635
        post_exponent = 1.1034507585082969

        # Act
        multiplier, label = linear_adp.get_adp_multiplier(22)

        # Assert
        assert multiplier == pytest.approx(base_first, abs=1e-12)
        assert abs(multiplier - post_exponent) > 1e-5
        assert label == "EXCELLENT"


# TD2 -- THE BRANCH IS LADDER-FAITHFUL (item 6)

class TestRisingThresholdsIsInert:
    """`rising_thresholds` is inert on the LINEAR path, and this is load-bearing.

    The bucketed branch encodes polarity twice -- in the ladder's DIRECTION and in the
    caller's argument -- and D4's whole defect was those two disagreeing. Interpolation
    reads the ladder as an ordered curve, so it can neither be rescued by a matching
    argument nor corrupted by a mismatched one. An implementation that picked the better
    side from `rising_thresholds` instead of from the sorted ladder would pass every
    other test in this file while reintroducing exactly the D4 disagreement class,
    because for both live factors the ladder direction and the argument AGREE.
    """

    @pytest.mark.parametrize("adp", [10, 22, 30, 40, 50, 60, 80, 90])
    def test_mismatched_polarity_argument_changes_nothing(self, linear_adp, adp):
        # Arrange -- ADP's ladder is DECREASING, so rising_thresholds=True is the
        # DELIBERATELY MISMATCHED argument here.
        ladder = linear_adp.adp_scoring

        # Act
        mismatched = linear_adp._get_multiplier(ladder, adp, rising_thresholds=True)
        matched = linear_adp._get_multiplier(ladder, adp, rising_thresholds=False)

        # Assert
        assert mismatched == matched
        assert mismatched == linear_adp.get_adp_multiplier(adp)


# TD3 CLAUSE 2 -- CLAMPING, NOT EXTRAPOLATION (item 7)

class TestClamping:
    """Outside the outermost anchors the end anchor's value AND label are returned.

    The VALUE is what these assert: linear extrapolation yields the correct label at both
    ends and the wrong value, so a label-only clamp test would pass against an
    extrapolating implementation.
    """

    def test_clamps_below_the_best_anchor(self, linear_adp):
        # Arrange -- extrapolating the 20..40 segment down to ADP 10 gives
        # 1.1371489379735318 (measured); clamping gives the EXCELLENT anchor's own value.
        # The gap is 2.82e-02, so this assertion is nowhere near a corridor edge.
        # Act
        multiplier, label = linear_adp.get_adp_multiplier(10)

        # Assert
        assert multiplier == pytest.approx(1.1089738719028956, abs=1e-12)
        assert label == "EXCELLENT"
        assert multiplier != pytest.approx(1.1371489379735318, abs=1e-12)

    def test_clamps_above_the_worst_anchor(self, linear_adp):
        # Arrange -- extrapolating the 60..80 segment up to ADP 90 gives
        # 0.872125742973272 (measured); clamping gives the VERY_POOR anchor's own value.
        # Act
        multiplier, label = linear_adp.get_adp_multiplier(90)

        # Assert
        assert multiplier == pytest.approx(0.8969619974461313, abs=1e-12)
        assert label == "VERY_POOR"
        assert multiplier != pytest.approx(0.872125742973272, abs=1e-12)


# THE TIER-REACHABILITY GUARD IS MODE-AWARE (obligation item 12, added 2026-08-17)

class TestTierReachabilityIsModeAware:
    """D5.1's guard, narrowed for LINEAR only.

    The guard raises at CONFIG LOAD, so its blast radius is total rather than per-factor:
    a mis-scoped required-label set fails the live tool and both simulation engines at
    startup. Two directions of failure, each pinned below -- over-narrowing (applying the
    four-anchor set to a BUCKETED block) would silently retire the guard for the six
    factors that never go linear; under-narrowing (leaving the set five-wide for LINEAR)
    is the rejection this arm exists to remove.
    """

    def test_a_bucketed_block_still_requires_all_five_labels(
        self, tmp_path, league_params
    ):
        """12a -- the five-label requirement survives VERBATIM for the default path.

        This ladder is reachable for all four ANCHOR labels and misses only NEUTRAL, so
        it discriminates the five-label set from the four-anchor set exactly: it passes
        under a four-anchor requirement and raises under a five-label one.
        """
        # Arrange -- POOR and GOOD collide at 79, so the rising branch's NEUTRAL
        # fall-through band is empty. SCALING is absent, i.e. BUCKETED.
        no_neutral = {"VERY_POOR": 20, "POOR": 79, "GOOD": 79, "EXCELLENT": 80}
        _put_literal_ladder(league_params, "PLAYER_RATING_SCORING", no_neutral,
                            PLAYER_RATING_WEIGHT)

        # Act
        with pytest.raises(ValueError) as excinfo:
            _config_with(tmp_path, league_params)

        # Assert
        message = str(excinfo.value)
        assert "PLAYER_RATING_SCORING" in message
        assert "NEUTRAL" in message

    def test_a_linear_block_reaching_its_four_anchors_loads_without_neutral(
        self, linear_adp
    ):
        """12b -- the regression this arm exists to prevent.

        Under TD3 a LINEAR factor emits NEUTRAL for no valued input at all, so this
        fixture is rejected outright by the pre-arm five-label guard. That the
        `linear_adp` fixture constructs at all IS the assertion; the sweep below makes
        the premise explicit rather than implicit.
        """
        # Act
        labels = {linear_adp.get_adp_multiplier(val / 2.0)[1]
                  for val in range(0, 400)}

        # Assert
        assert labels == {"EXCELLENT", "GOOD", "POOR", "VERY_POOR"}
        assert "NEUTRAL" not in labels

    def test_a_linear_block_missing_an_anchor_label_still_raises(
        self, tmp_path, league_params
    ):
        """12c -- the arm NARROWS the guard, it does not disable it.

        player_rating's declared input domain is [0, 100], so a VERY_POOR anchor at -50
        is out of domain: every in-domain input below POOR falls in the (-50, 40)
        segment, whose better side is POOR, and VERY_POOR is emitted by nothing. The four
        thresholds are still distinct, so TD2a's check passes and the failure is the
        reachability guard's alone.
        """
        # Arrange
        unreachable_anchor = {"VERY_POOR": -50, "POOR": 40, "GOOD": 60, "EXCELLENT": 80}
        _put_literal_ladder(league_params, "PLAYER_RATING_SCORING", unreachable_anchor,
                            PLAYER_RATING_WEIGHT, scaling="LINEAR")

        # Act
        with pytest.raises(ValueError) as excinfo:
            _config_with(tmp_path, league_params)

        # Assert
        message = str(excinfo.value)
        assert "PLAYER_RATING_SCORING" in message
        assert "VERY_POOR" in message

    def test_the_live_config_tree_still_loads_clean(self):
        """12d -- the byte-identical restatement, pinned at the CONFIG-LOAD boundary.

        Deliberately reads the LIVE store rather than a fixture: the requirement here IS
        that the shipped configuration keeps its current accept verdict, which a temp-dir
        copy could not evidence. As of D10.4 BOTH live cutover factors carry
        SCALING: "LINEAR" -- ADP_SCORING (switched by D10.3) and PLAYER_RATING_SCORING
        (switched by D10.4) -- while the remaining FOUR factors are still BUCKETED (no
        SCALING key exists on disk for them), so this exercises both switched paths and
        the unchanged five-label path together, end to end.

        This test ENUMERATES which live factors carry SCALING, so every cutover unit must
        move its own factor from the negative loop into the positive pinned set above it.
        That is inherent to an enumerating test, not an oversight by any one unit.
        """
        # Act / Assert -- construction performs the whole load-time validation chain
        config = ConfigManager(LIVE_CONFIG_ROOT)

        # Assert -- ADP_SCORING is the live factor D10.3 switched to LINEAR
        assert config.parameters["ADP_SCORING"]["SCALING"] == "LINEAR"

        # Assert -- PLAYER_RATING_SCORING is the live factor D10.4 switched to LINEAR.
        # Pinned POSITIVELY rather than merely dropped from the loop below, so the test
        # still fails on a WRONG value as well as on removal of the key.
        assert config.parameters["PLAYER_RATING_SCORING"]["SCALING"] == "LINEAR"

        # Assert -- and no OTHER live block acquired a SCALING key
        for scoring_key in ("TEAM_QUALITY_SCORING", "MATCHUP_SCORING",
                            "SCHEDULE_SCORING", "PERFORMANCE_SCORING"):
            assert "SCALING" not in config.parameters[scoring_key]
