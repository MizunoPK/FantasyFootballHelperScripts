"""
Unit tests for the ADP-vs-picks-until-next-turn survival estimate (Step 15,
D18.3): _apply_survival_estimate() in isolation, and score_player()'s Step 15
gate exercised through the full pipeline -- the no-op default, the no-ADP
case, and the non-stacking/independent-toggle proof TD4 requires.

Author: Kai Mizuno
"""

import ast
import json
from pathlib import Path

import pytest
from unittest.mock import Mock

from league_helper.util.ConfigManager import ConfigManager
from league_helper.util.player_scoring import PlayerScoringCalculator
from utils.FantasyPlayer import FantasyPlayer


# --- Isolated _apply_survival_estimate tests (mirrors
# test_player_scoring_nfl_team_penalty.py's Mock(spec=FantasyPlayer) + Mock()
# config shape) ---


class TestApplySurvivalEstimateIsolated:
    @pytest.fixture
    def mock_config(self):
        config = Mock()
        config.get_survival_multiplier = Mock(return_value=(1.5, "EXCELLENT"))
        return config

    @pytest.fixture
    def calculator(self, mock_config):
        return PlayerScoringCalculator(
            config=mock_config,
            player_manager=Mock(),
            max_projection=400.0,
            team_data_manager=Mock(),
            season_schedule_manager=Mock(),
            current_nfl_week=1,
        )

    @pytest.fixture
    def player_with_adp(self):
        player = Mock(spec=FantasyPlayer)
        player.name = "Test Player"
        player.adp = 15.0
        return player

    @pytest.fixture
    def player_no_adp(self):
        player = Mock(spec=FantasyPlayer)
        player.name = "No ADP Player"
        player.adp = None
        return player

    def test_margin_computed_as_adp_minus_picks_until_next_turn(self, calculator, mock_config, player_with_adp):
        calculator._apply_survival_estimate(player_with_adp, 3, 100.0)

        mock_config.get_survival_multiplier.assert_called_once_with(12.0)

    def test_score_multiplied_by_returned_multiplier(self, calculator, player_with_adp):
        new_score, reason = calculator._apply_survival_estimate(player_with_adp, 3, 100.0)

        assert new_score == 150.0
        assert reason == "Survival: EXCELLENT (1.5000x)"

    def test_no_adp_passes_none_margin(self, calculator, mock_config, player_no_adp):
        calculator._apply_survival_estimate(player_no_adp, 3, 100.0)

        mock_config.get_survival_multiplier.assert_called_once_with(None)

    def test_no_adp_neutral_result_is_unaffected(self, calculator, mock_config, player_no_adp):
        """D18.3 provision-inertness correction: a multiplier of exactly 1.0 is
        the identity value, so the step must be a genuine no-op -- score AND
        reason both unchanged -- mirroring _apply_location_modifier's own
        `if modifier == 0: return player_score, ""` shape. An unconditional
        "Survival: NEUTRAL (1.0000x)" reason would be a user-visible change
        (reasons is surfaced in the recommendation display) even though the
        score itself never moved, which violates this unit's Rollout Stage:
        provision no-op contract."""
        mock_config.get_survival_multiplier.return_value = (1.0, "NEUTRAL")

        new_score, reason = calculator._apply_survival_estimate(player_no_adp, 3, 100.0)

        assert new_score == 100.0
        assert reason == ""


# --- Full-pipeline tests: real ConfigManager, real score_player() ---


def _base_parameters():
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
            "THRESHOLDS": {"EXCELLENT": 20, "GOOD": 50, "POOR": 100, "VERY_POOR": 150},
            "MULTIPLIERS": {"EXCELLENT": 1.2, "GOOD": 1.1, "POOR": 0.9, "VERY_POOR": 0.7},
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
def config_no_survival(tmp_path):
    """No SURVIVAL_SCORING key -- the real-config absent-key no-op path."""
    data_folder = tmp_path / "data_no_survival"
    data_folder.mkdir()
    cfg = {"config_name": "t", "description": "d", "parameters": _base_parameters()}
    (data_folder / "league_config.json").write_text(json.dumps(cfg))
    return ConfigManager(data_folder)


@pytest.fixture
def config_with_survival(tmp_path):
    """SURVIVAL_SCORING configured with non-neutral values, for the
    non-stacking/independent-toggle proof."""
    data_folder = tmp_path / "data_with_survival"
    data_folder.mkdir()
    params = _base_parameters()
    params["SURVIVAL_SCORING"] = {
        "THRESHOLDS": {"EXCELLENT": -20, "GOOD": -5, "POOR": 5, "VERY_POOR": 20},
        "MULTIPLIERS": {"EXCELLENT": 1.5, "GOOD": 1.2, "POOR": 0.9, "VERY_POOR": 0.6},
        "WEIGHT": 1.0,
    }
    cfg = {"config_name": "t", "description": "d", "parameters": params}
    (data_folder / "league_config.json").write_text(json.dumps(cfg))
    return ConfigManager(data_folder)


def _calculator(config):
    return PlayerScoringCalculator(
        config=config,
        player_manager=Mock(),
        max_projection=250.0,
        team_data_manager=Mock(),
        season_schedule_manager=Mock(),
        current_nfl_week=1,
    )


def _calculator_with_neutral_data(config):
    """Same real ConfigManager as _calculator(), but with the mocked data managers
    pinned to EMPTY rather than left as bare Mocks.

    _calculator()'s bare Mocks are fine for the tests that disable the data-dependent
    steps, but the production call sites replayed below enable schedule/performance, and a
    bare Mock is not iterable. Empty returns make those steps degrade to their own
    documented no-data no-ops, which is what lets the real kwarg shapes actually run.
    game_data_manager is left unset (None), so temperature/wind/location no-op via their
    own `if not self.game_data_manager` guards.
    """
    season_schedule_manager = Mock()
    season_schedule_manager.get_future_opponents.return_value = []
    player_manager = Mock()
    player_manager.get_projected_points.return_value = None
    return PlayerScoringCalculator(
        config=config,
        player_manager=player_manager,
        max_projection=250.0,
        team_data_manager=Mock(),
        season_schedule_manager=season_schedule_manager,
        current_nfl_week=1,
    )


def _normalized_player(adp):
    """A player whose Step 1 normalization yields exactly 100.0, mirroring
    test_PlayerManager_scoring.py's test_score_player_only_normalization setup
    (weeks 5-16 at 250.0/12, normalization_max_scale=100.0, max_projection=250.0)."""
    projected = [0.0] * 17
    for i in range(5, 17):
        projected[i] = 250.0 / 12
    return FantasyPlayer(
        id=1, name="Norm Player", team="KC", position="RB", bye_week=99,
        fantasy_points=100.0, average_draft_position=adp,
        projected_points=projected, actual_points=projected.copy(),
    )


class TestScorePlayerSurvivalAbsentKeyNoOp:
    """SURVIVAL_SCORING absent from a REAL config: no-op, whether or not the
    caller supplies picks_until_next_turn. Compares a with/without pair to EACH
    OTHER rather than to a hardcoded 100.0: 12 * (250.0/12) is not bit-exact
    250.0 in IEEE-754, so _normalized_player's true baseline is not bit-exact
    100.0 either -- an exact pairwise comparison is both the AC-required check
    and immune to that summation drift."""

    _KWARGS = dict(
        adp=False, player_rating=False, team_quality=False, performance=False,
        matchup=False, schedule=False, draft_round=-1, bye=False, injury=False,
    )

    def test_picks_until_next_turn_none_is_a_no_op(self, config_no_survival):
        calc = _calculator(config_no_survival)
        player = _normalized_player(adp=15.0)

        scored = calc.score_player(player, [], **self._KWARGS)

        assert "Survival:" not in "".join(scored.reason)

    def test_picks_until_next_turn_supplied_is_still_a_no_op(self, config_no_survival):
        """The strongest form of the AC: even when the caller DOES pass a real
        picks_until_next_turn value, an absent SURVIVAL_SCORING config key means
        the score is byte-identical to not passing it at all."""
        calc = _calculator(config_no_survival)
        player = _normalized_player(adp=15.0)

        baseline = calc.score_player(player, [], **self._KWARGS)
        scored = calc.score_player(player, [], picks_until_next_turn=3, **self._KWARGS)

        assert scored.score == baseline.score, (
            f"baseline={baseline.score!r}, with_param={scored.score!r}"
        )
        assert "Survival:" not in "".join(scored.reason)


class TestScorePlayerNoADP:
    def test_no_adp_player_survival_step_is_neutral(self, config_with_survival):
        """A no-ADP player under a REAL, non-neutral SURVIVAL_SCORING config:
        margin is None (p.adp is None), so get_survival_multiplier(None) always
        returns (1.0, NEUTRAL) per _get_multiplier's documented val-is-None arm,
        regardless of config. D18.3's provision-inertness correction treats that
        1.0 multiplier as identity -- no score change AND no "Survival:" reason
        -- rather than emitting "Survival: NEUTRAL (1.0000x)", which would
        misrepresent a "no ADP data" no-op as a meaningfully-evaluated NEUTRAL
        tier (the same distinction the other tier labels EXCELLENT/GOOD/POOR/
        VERY_POOR draw)."""
        calc = _calculator(config_with_survival)
        player = _normalized_player(adp=None)

        baseline_kwargs = dict(
            adp=False, player_rating=False, team_quality=False, performance=False,
            matchup=False, schedule=False, draft_round=-1, bye=False, injury=False,
        )
        baseline = calc.score_player(player, [], **baseline_kwargs)
        scored = calc.score_player(player, [], picks_until_next_turn=3, **baseline_kwargs)

        assert scored.score == baseline.score, (
            f"a NEUTRAL (1.0x) survival adjustment must not move the score: "
            f"baseline={baseline.score!r}, with_param={scored.score!r}"
        )
        assert "Survival:" not in "".join(scored.reason)


class TestScorePlayerConfiguredNeutralBand:
    """The THIRD state _apply_survival_estimate's `if multiplier == 1.0` gate covers,
    and the only one that was previously unpinned at score_player level:
    SURVIVAL_SCORING CONFIGURED with a real (non-WEIGHT-0.0) block, the player HAS an
    ADP, and the margin lands inside the BUCKETED NEUTRAL band -- so the signal
    genuinely evaluated on real data and returned the multiplicative identity.

    It is suppressed identically to the two no-data states (TestScorePlayerSurvivalAbsentKeyNoOp,
    TestScorePlayerNoADP). That is the accepted, deliberate behaviour recorded in
    _apply_survival_estimate's own docstring: Step 15 stays silent for a neutral-band
    player while sibling Step 2 emits "ADP: NEUTRAL (1.0000x)" for one. Do not "fix"
    that asymmetry -- this test is what pins it."""

    def test_configured_neutral_band_is_silent_and_leaves_score_unchanged(self, config_with_survival):
        keys = config_with_survival.keys
        thresholds = config_with_survival.survival_scoring[keys.THRESHOLDS]

        # Derive the band rather than assume it: get_survival_multiplier passes
        # rising_thresholds=False, whose BUCKETED neutral arm is GOOD < val < POOR
        # (strictly), and the fixture declares no SCALING key so BUCKETED applies.
        adp, picks = 15.0, 15
        margin = adp - picks
        assert thresholds[keys.GOOD] < margin < thresholds[keys.POOR], (
            f"margin {margin!r} must land STRICTLY inside the NEUTRAL band "
            f"({thresholds[keys.GOOD]!r}, {thresholds[keys.POOR]!r}) or this test "
            f"exercises a tiered state instead of state 3"
        )
        # Second, independent confirmation straight from the accessor, so a future
        # threshold/SCALING/WEIGHT edit cannot leave this test silently green while
        # exercising a tier rather than the identity.
        assert config_with_survival.get_survival_multiplier(margin) == (1.0, keys.NEUTRAL)
        # And confirm the block really is configured and non-inert -- a WEIGHT of 0.0
        # would collapse this back into state 1.
        assert config_with_survival.survival_scoring[keys.WEIGHT] == 1.0

        calc = _calculator(config_with_survival)
        player = _normalized_player(adp=adp)
        baseline_kwargs = dict(
            adp=False, player_rating=False, team_quality=False, performance=False,
            matchup=False, schedule=False, draft_round=-1, bye=False, injury=False,
        )

        baseline = calc.score_player(player, [], **baseline_kwargs)
        scored = calc.score_player(player, [], picks_until_next_turn=picks, **baseline_kwargs)

        assert scored.score == baseline.score, (
            f"a configured-but-NEUTRAL (1.0x) survival adjustment must not move the "
            f"score: baseline={baseline.score!r}, with_param={scored.score!r}"
        )
        assert "Survival:" not in "".join(scored.reason)


class TestScorePlayerSurvivalNonStacking:
    """TD4: the ADP quality multiplier (Step 2) and the survival estimate
    (Step 15) are independently toggleable and their combination, when both
    fire, is exactly one multiplicative application of each -- never a silent
    double-application of either. adp=15.0 tiers EXCELLENT under ADP_SCORING
    (<=20 -> 1.2x); picks_until_next_turn=40 makes margin=15.0-40=-25.0, which
    tiers EXCELLENT under SURVIVAL_SCORING (<=-20 -> 1.5x)."""

    def test_only_adp_flag_applies_only_adp_multiplier(self, config_with_survival):
        calc = _calculator(config_with_survival)
        player = _normalized_player(adp=15.0)

        scored = calc.score_player(
            player, [], adp=True, player_rating=False, team_quality=False,
            performance=False, matchup=False, schedule=False, draft_round=-1,
            bye=False, injury=False,
        )

        assert scored.score == pytest.approx(120.0)
        reasons = "".join(scored.reason)
        assert "ADP:" in reasons
        assert "Survival:" not in reasons

    def test_only_survival_param_applies_only_survival_multiplier(self, config_with_survival):
        calc = _calculator(config_with_survival)
        player = _normalized_player(adp=15.0)

        scored = calc.score_player(
            player, [], adp=False, player_rating=False, team_quality=False,
            performance=False, matchup=False, schedule=False, draft_round=-1,
            bye=False, injury=False, picks_until_next_turn=40,
        )

        assert scored.score == pytest.approx(150.0)
        reasons = "".join(scored.reason)
        assert "ADP:" not in reasons
        assert "Survival:" in reasons

    def test_both_enabled_apply_exactly_once_each_not_double_applied(self, config_with_survival):
        """The falsifiable non-stacking assertion: 100.0 * 1.2 (ADP) * 1.5
        (survival) == 180.0 exactly once each. A defect that accidentally
        double-applies either factor (e.g. calling _apply_survival_estimate
        twice, or folding it into _apply_adp_multiplier AND leaving the Step 15
        gate active) would instead produce 100.0 * 1.2 * 1.5 * 1.5 == 270.0 or
        100.0 * 1.2 * 1.2 * 1.5 == 216.0 -- this assertion fails under either."""
        calc = _calculator(config_with_survival)
        player = _normalized_player(adp=15.0)

        scored = calc.score_player(
            player, [], adp=True, player_rating=False, team_quality=False,
            performance=False, matchup=False, schedule=False, draft_round=-1,
            bye=False, injury=False, picks_until_next_turn=40,
        )

        assert scored.score == pytest.approx(180.0)
        reasons = "".join(scored.reason)
        assert "ADP:" in reasons
        assert "Survival:" in reasons


# Each entry is (site label, the site's REAL kwargs). Transcribed one-for-one from the
# 8 production call sites derived_facts.md Entry 2 records; every scoring-flag value is
# the site's own. The single deliberate substitution is `roster`: three sites pass a live
# roster object (`self.team` / `post_trade_roster`) that has no meaning outside its own
# manager, so `[]` stands in for it -- `roster` feeds the bye-week step and cannot reach
# the Step 15 gate, which keys solely on `picks_until_next_turn`. What matters is that
# NONE of the 8 passes `picks_until_next_turn`, exactly as none of the real sites does.
_PRODUCTION_CALL_SITES = [
    (
        "StarterHelperModeManager.py:346",
        dict(use_weekly_projection=True, adp=False, player_rating=False, team_quality=True,
             performance=True, matchup=True, schedule=False, bye=False, injury=False,
             temperature=True, wind=True, location=True),
    ),
    (
        "ParallelAccuracyRunner.py:141",
        dict(use_weekly_projection=True, adp=False, player_rating=False, team_quality=True,
             performance=True, matchup=True, schedule=False, bye=False, injury=False,
             temperature=True, wind=True, location=True),
    ),
    (
        "TradeSimTeam.py:86",
        dict(use_weekly_projection=True, adp=False, player_rating=False, team_quality=True,
             performance=True, matchup=True, schedule=False, bye=False, injury=False,
             roster=[]),
    ),
    (
        "TradeSimTeam.py:98",
        dict(adp=False, player_rating=True, team_quality=True, performance=True,
             matchup=False, schedule=True, bye=False, injury=False, roster=[]),
    ),
    (
        "TradeSimTeam.py:104",
        dict(adp=False, player_rating=True, team_quality=True, performance=True,
             matchup=False, schedule=True, bye=True, injury=False, roster=[]),
    ),
    (
        "PlayerManager.py:330 (load_team)",
        dict(adp=False, player_rating=True, team_quality=True, performance=True,
             matchup=False, schedule=True, bye=True, injury=True),
    ),
    (
        "PlayerManager.py:647 (display_scored_roster)",
        dict(adp=False, player_rating=True, team_quality=True, performance=True,
             matchup=False, schedule=True, bye=True, injury=True),
    ),
    (
        "trade_analyzer.py:345",
        dict(adp=False, player_rating=True, team_quality=True, performance=True,
             matchup=False, schedule=True, roster=[]),
    ),
]


class TestScorePlayerEightProductionCallSitesUnaffected:
    """Step 15 is unreachable from every existing production call site.

    Two independent arguments, because the weaker one alone reads as more coverage
    than it delivers:

    1. `test_site_shape_produces_no_survival_adjustment` replays each of the 8 sites'
       OWN kwargs (see _PRODUCTION_CALL_SITES for the one documented substitution) --
       so the parameter is load-bearing and the eight cases are genuinely eight
       different executions, not eight repeats of one.
    2. `test_only_sanctioned_production_call_sites_pass_picks_until_next_turn` is the
       STRONGER argument and does not depend on kwarg transcription being exhaustive
       or current: it AST-scans production for every site that supplies the keyword and
       asserts the set is EXACTLY the sanctioned one.

       D18.3 wrote this as an inertness guard asserting the set was EMPTY, and said in
       this docstring that it would fail the moment a caller was wired up -- "which is
       D18.5's job, and is the point at which this test should be revisited rather than
       deleted." D18.5 wired that caller (the draft cockpit), so the guard was re-scoped
       here rather than deleted, and re-scoping made it stronger in BOTH directions: it
       still fails on an UNEXPECTED new caller, and it now also fails if the sanctioned
       cockpit caller DISAPPEARS -- i.e. if the survival signal is ever silently
       un-wired, which the empty-set form could never have caught.

       The eight-call-site parametrization above therefore still means exactly what it
       says: none of those eight passes the keyword, so Step 15 remains unreachable from
       every one of them."""

    @pytest.mark.parametrize(
        "site,kwargs", _PRODUCTION_CALL_SITES, ids=[s for s, _ in _PRODUCTION_CALL_SITES]
    )
    def test_site_shape_produces_no_survival_adjustment(self, config_with_survival, site, kwargs):
        calc = _calculator_with_neutral_data(config_with_survival)
        player = _normalized_player(adp=15.0)

        scored = calc.score_player(player, [], **kwargs)

        assert "Survival:" not in "".join(scored.reason), site

    def test_only_sanctioned_production_call_sites_pass_picks_until_next_turn(self):
        # AST, not a text search: only an actual keyword ARGUMENT counts, so the
        # parameter's own declarations, docstrings and comments cannot trip it and no
        # caller can hide from it behind formatting.
        #
        # The two sanctioned targets, and why each is sanctioned:
        #   self.scoring_calculator.score_player -- PlayerManager.score_player's own
        #       pass-through to the calculator. The parameter's declared forwarding
        #       path, not a caller electing to supply a value.
        #   self.player_manager.score_player     -- DraftModeManager.get_recommendations,
        #       the draft cockpit. THE caller the signal exists for: it supplies the live
        #       geometry.picks_until_our_next_turn read from the ESPN board.
        sanctioned = {
            "self.scoring_calculator.score_player",
            "self.player_manager.score_player",
        }
        repo_root = Path(__file__).resolve().parents[3]
        production_dirs = ["league_helper", "simulation", "utils", "player_data_fetcher"]

        scanned = 0
        found = set()
        offenders = []
        for directory in production_dirs:
            for path in sorted((repo_root / directory).rglob("*.py")):
                scanned += 1
                tree = ast.parse(path.read_text(encoding="utf-8"))
                for node in ast.walk(tree):
                    if not isinstance(node, ast.Call):
                        continue
                    if not any(kw.arg == "picks_until_next_turn" for kw in node.keywords):
                        continue
                    target = ast.unparse(node.func)
                    if target in sanctioned:
                        found.add(target)
                        continue
                    offenders.append(f"{path.relative_to(repo_root)}:{node.lineno} -> {target}")

        # Coverage assertion: proves the walk actually visited the production tree, so
        # neither an empty `offenders` nor a full `found` can pass vacuously on a
        # mis-resolved repo root.
        assert scanned > 50, f"only {scanned} production files scanned from {repo_root}"

        assert offenders == [], (
            "An UNSANCTIONED production caller now supplies picks_until_next_turn. This "
            "is a draft-time signal wired deliberately at ONE place; add a site to "
            "`sanctioned` only with a recorded reason:\n" + "\n".join(offenders)
        )

        assert found == sanctioned, (
            "A SANCTIONED production caller of picks_until_next_turn has disappeared: "
            f"missing {sorted(sanctioned - found)}. If the draft cockpit no longer "
            "passes the live picks-until-our-next-turn, the survival estimate is "
            "silently inert again and ticket D18's Success Criteria are no longer met."
        )
