"""
Unit Tests for the Multiplier Tier-Reachability Guard

Covers ConfigManager._validate_tier_reachability (D5.1) — the load-time check that every
_get_multiplier consumer's threshold ladder can reach all five tier labels over that
factor's declared input domain (MULTIPLIER_INPUT_DOMAINS).

Four concerns, one file:
  * a degenerate config trips the guard, and the guard names every failing factor
    (mutation-checked: deleting the guard call from _extract_parameters makes these fail),
  * the probe's verdict agrees with direct _get_multiplier calls on the same ladder,
    including the rising branch's VERY_POOR-before-POOR evaluation order,
  * all four data/configs/week*.json horizons are reachable, not only the active week
    the load-time guard sees (TD6),
  * a config omitting TEMPERATURE_SCORING / WIND_SCORING still loads AND still scores —
    the latent KeyError that UD8's materialization pass fixes.

Author: Claude Code
Date: 2026-08-11
"""

import json
import shutil
from pathlib import Path

import pytest

from league_helper.util.ConfigManager import MULTIPLIER_INPUT_DOMAINS, ConfigManager


LEAGUE_FIXTURE = Path("tests/fixtures/league/league_config.json")
LIVE_CONFIG_ROOT = Path("data")
ALL_TIERS = {"EXCELLENT", "GOOD", "NEUTRAL", "POOR", "VERY_POOR"}
TIER_KEYS = ("VERY_POOR", "POOR", "GOOD", "EXCELLENT")

# The polarity each accessor passes to _get_multiplier, transcribed from the eight call
# sites (ConfigManager.py:369-448). This table is deliberately a SECOND, independent
# derivation of something the guard does not carry: per UD7 the guard has no polarity
# column, because it calls the accessors. Restating polarity here is exactly what lets the
# agreement test below catch a drifted probe instead of agreeing with it by construction.
ACCESSOR_POLARITY = [
    ("ADP_SCORING", "adp_scoring", "get_adp_multiplier", False),
    ("PLAYER_RATING_SCORING", "player_rating_scoring",
     "get_player_rating_multiplier", True),
    ("TEAM_QUALITY_SCORING", "team_quality_scoring",
     "get_team_quality_multiplier", False),
    ("MATCHUP_SCORING", "matchup_scoring", "get_matchup_multiplier", True),
    ("SCHEDULE_SCORING", "schedule_scoring", "get_schedule_multiplier", True),
    ("PERFORMANCE_SCORING", "performance_scoring",
     "get_performance_multiplier", True),
    ("TEMPERATURE_SCORING", "temperature_scoring",
     "get_temperature_multiplier", False),
    ("WIND_SCORING", "wind_scoring", "get_wind_multiplier", False),
]


# FIXTURES

@pytest.fixture
def league_params():
    """A complete, guard-clean legacy config, re-read so a test may mutate it freely."""
    return json.loads(LEAGUE_FIXTURE.read_text())


@pytest.fixture
def live_config():
    """ConfigManager over the LIVE data store — deliberately not a temp fixture."""
    return ConfigManager(LIVE_CONFIG_ROOT)


@pytest.fixture
def frozen_config(tmp_path, league_params):
    """ConfigManager over the FROZEN league fixture, for assertions about the CODE.

    TestProbeAgreesWithTheComparator asserts a property of the probe, not of the shipped
    ladders, so pinning it to the live data/ store would let a config edit silently change
    what the agreement test exercises (or turn it red for an unrelated reason). D4.3
    (b3ba1c82) cut exactly this dependency out of the win-rate tests. The live store stays
    where it is the requirement: TestAllFourHorizonsAreReachable (TD6).
    """
    return ConfigManager(_write_legacy_config(tmp_path, league_params))


def _write_legacy_config(tmp_path, data):
    """Write `data` as a legacy single-file config; return the data folder."""
    (tmp_path / "league_config.json").write_text(json.dumps(data))
    return tmp_path


def _horizon_root(tmp_path, week):
    """Copy data/configs/ into `tmp_path` and pin CURRENT_NFL_WEEK; return the folder.

    Built on pytest's `tmp_path` rather than `tempfile.mkdtemp()` so cleanup is the
    fixture's responsibility and happens even when an assertion fails -- an inline
    `shutil.rmtree` after the asserts would leak a directory on every red run.
    """
    shutil.copytree(LIVE_CONFIG_ROOT / "configs", tmp_path / "configs")
    config_path = tmp_path / "configs" / "league_config.json"
    data = json.loads(config_path.read_text())
    data["parameters"]["CURRENT_NFL_WEEK"] = week
    config_path.write_text(json.dumps(data))
    return tmp_path


def _dense_labels(config, scoring_dict, domain, rising, samples=2001):
    """Brute-force the reachable label set by sampling the domain evenly.

    An independent ground truth for the probe set: it knows nothing about thresholds and
    simply walks the domain, so a probe that under-reports a reachable tier fails against
    it. A declared-unbounded side is swept over a wide finite window, which is sufficient
    because the label is piecewise-constant with only four breakpoints.
    """
    low, high = (None, None) if domain is None else domain
    start = low if low is not None else -1000.0
    stop = high if high is not None else 1000.0
    step = (stop - start) / (samples - 1)
    return {
        config._get_multiplier(
            scoring_dict, start + index * step, rising_thresholds=rising
        )[1]
        for index in range(samples)
    }


class TestDegenerateConfigTripsTheGuard:
    """A degenerate ladder fails the config load rather than scoring silently (TD4)."""

    def test_the_base_fixture_loads_cleanly(self, tmp_path, league_params):
        """The unmutated fixture is guard-clean, so the tests below fail for their reason."""
        # Arrange
        data_folder = _write_legacy_config(tmp_path, league_params)

        # Act
        config = ConfigManager(data_folder)

        # Assert
        assert config.adp_scoring["THRESHOLDS"]["DIRECTION"] == "DECREASING"

    def test_pre_d4_adp_pairing_raises_naming_the_unreachable_tiers(
        self, tmp_path, league_params
    ):
        """ADP DECREASING -> INCREASING against a rising_thresholds=False consumer.

        This is the mutation-checked test: deleting the _validate_tier_reachability()
        call from _extract_parameters makes it fail, because the load then succeeds.
        """
        # Arrange
        league_params["parameters"]["ADP_SCORING"]["THRESHOLDS"]["DIRECTION"] = (
            "INCREASING"
        )
        data_folder = _write_legacy_config(tmp_path, league_params)

        # Act
        with pytest.raises(ValueError) as excinfo:
            ConfigManager(data_folder)

        # Assert
        message = str(excinfo.value)
        assert "ADP_SCORING" in message
        assert "get_adp_multiplier" in message
        for tier in ("GOOD", "NEUTRAL", "POOR"):
            assert tier in message

    def test_every_failing_factor_is_named_in_one_raise(self, tmp_path, league_params):
        """The guard accumulates all eight factors rather than raising on the first."""
        # Arrange
        parameters = league_params["parameters"]
        parameters["ADP_SCORING"]["THRESHOLDS"]["DIRECTION"] = "INCREASING"
        parameters["TEAM_QUALITY_SCORING"]["THRESHOLDS"]["DIRECTION"] = "INCREASING"
        data_folder = _write_legacy_config(tmp_path, league_params)

        # Act
        with pytest.raises(ValueError) as excinfo:
            ConfigManager(data_folder)

        # Assert
        message = str(excinfo.value)
        assert "ADP_SCORING" in message
        assert "TEAM_QUALITY_SCORING" in message

    def test_a_missing_threshold_key_is_its_own_failure_class(
        self, tmp_path, league_params
    ):
        """A literal ladder short of a tier key is reported distinctly (UD4)."""
        # Arrange
        league_params["parameters"]["MATCHUP_SCORING"]["THRESHOLDS"] = {
            "VERY_POOR": 5,
            "POOR": 10,
            "GOOD": 20,
        }
        data_folder = _write_legacy_config(tmp_path, league_params)

        # Act
        with pytest.raises(ValueError) as excinfo:
            ConfigManager(data_folder)

        # Assert
        message = str(excinfo.value)
        assert "MATCHUP_SCORING" in message
        assert "missing" in message
        assert "EXCELLENT" in message

    def test_a_missing_multiplier_key_is_reported_not_raised_as_keyerror(
        self, tmp_path, league_params
    ):
        """A partial MULTIPLIERS block yields a named ValueError, never a raw KeyError.

        BD4: _get_multiplier reads MULTIPLIERS[label] as well as THRESHOLDS[label], so a
        block carrying every threshold but only some multipliers survives the THRESHOLDS
        pre-check and then raises KeyError from inside the probe -- an unnamed failure
        that tells the config author nothing. This is the same failure class as the
        THRESHOLDS test above and is reported the same way.
        """
        # Arrange
        league_params["parameters"]["MATCHUP_SCORING"]["MULTIPLIERS"] = {
            "EXCELLENT": 1.0,
        }
        data_folder = _write_legacy_config(tmp_path, league_params)

        # Act
        with pytest.raises(ValueError) as excinfo:
            ConfigManager(data_folder)

        # Assert
        message = str(excinfo.value)
        assert "MATCHUP_SCORING" in message
        assert "MULTIPLIERS is missing" in message
        assert "VERY_POOR" in message

    def test_a_missing_weight_is_reported_not_raised_as_keyerror(
        self, tmp_path, league_params
    ):
        """WEIGHT is the third key _get_multiplier reads, and gets the same treatment."""
        # Arrange
        del league_params["parameters"]["MATCHUP_SCORING"]["WEIGHT"]
        data_folder = _write_legacy_config(tmp_path, league_params)

        # Act
        with pytest.raises(ValueError) as excinfo:
            ConfigManager(data_folder)

        # Assert
        message = str(excinfo.value)
        assert "MATCHUP_SCORING" in message
        assert "WEIGHT is missing" in message

    def test_neutral_is_not_required_in_multipliers(self, tmp_path, league_params):
        """The complement of the two tests above: the check must not over-reach.

        _get_multiplier returns a hard-coded 1.0 for the neutral band and never reads
        MULTIPLIERS[NEUTRAL]; no config on disk declares one. Requiring it would reject
        every healthy config, so this pins the four-tier-key boundary of the check.
        """
        # Arrange
        multipliers = league_params["parameters"]["MATCHUP_SCORING"]["MULTIPLIERS"]
        assert "NEUTRAL" not in multipliers
        data_folder = _write_legacy_config(tmp_path, league_params)

        # Act
        config = ConfigManager(data_folder)

        # Assert
        assert config.matchup_scoring["MULTIPLIERS"] == multipliers

    def test_a_factor_with_no_declared_domain_is_named_not_raised_as_keyerror(
        self, tmp_path, league_params, monkeypatch
    ):
        """The two enumerations must agree, and drift must fail with a name.

        _multiplier_factors and MULTIPLIER_INPUT_DOMAINS are separate enumerations of the
        same eight keys, so adding a ninth factor without declaring its domain would
        otherwise raise a bare KeyError at config load -- an opaque traceback on the
        League Helper and both engines. Simulated here by removing a declared entry,
        which is the same divergence from the other side.
        """
        # Arrange
        domains = dict(MULTIPLIER_INPUT_DOMAINS)
        del domains["MATCHUP_SCORING"]
        monkeypatch.setattr(
            "league_helper.util.ConfigManager.MULTIPLIER_INPUT_DOMAINS", domains
        )
        data_folder = _write_legacy_config(tmp_path, league_params)

        # Act
        with pytest.raises(ValueError) as excinfo:
            ConfigManager(data_folder)

        # Assert
        message = str(excinfo.value)
        assert "MULTIPLIER_INPUT_DOMAINS is missing" in message
        assert "MATCHUP_SCORING" in message


class TestProbeAgreesWithTheComparator:
    """The probe reads _get_multiplier correctly — criterion 8 of ticket.md."""

    def test_every_factor_reaches_all_five_tiers(self, frozen_config):
        """The probe's verdict on the frozen fixture config, factor by factor."""
        # Arrange / Act / Assert
        for key, attribute, accessor_name, _rising in ACCESSOR_POLARITY:
            scoring_dict = getattr(frozen_config, attribute)
            probed = frozen_config._probe_tier_labels(
                scoring_dict["THRESHOLDS"],
                MULTIPLIER_INPUT_DOMAINS[key],
                getattr(frozen_config, accessor_name),
            )
            assert probed == ALL_TIERS, key

    def test_the_probe_never_under_reports_against_a_dense_sweep(self, frozen_config):
        """A 2001-sample sweep finds no label the probe missed — the exhaustiveness claim.

        The dense sweep is an INDEPENDENT derivation: it calls _get_multiplier directly
        with the transcribed polarity and knows nothing about the four thresholds, so an
        epsilon too small to separate two adjacent thresholds — the specific way probe-set
        construction can silently under-report — fails this assertion.
        """
        # Arrange / Act / Assert
        for key, attribute, accessor_name, rising in ACCESSOR_POLARITY:
            scoring_dict = getattr(frozen_config, attribute)
            probed = frozen_config._probe_tier_labels(
                scoring_dict["THRESHOLDS"],
                MULTIPLIER_INPUT_DOMAINS[key],
                getattr(frozen_config, accessor_name),
            )
            dense = _dense_labels(
                frozen_config, scoring_dict, MULTIPLIER_INPUT_DOMAINS[key], rising
            )
            assert dense <= probed, f"{key}: probe missed {sorted(dense - probed)}"

    def test_the_rising_branch_tests_very_poor_before_poor(self, frozen_config):
        """The evaluation-order quirk the probe trusts, asserted rather than assumed.

        Both VERY_POOR and POOR match `val <= threshold` at val == 10 on this ladder;
        ConfigManager.py's rising branch tests VERY_POOR first, so VERY_POOR wins. A probe
        built against the opposite order would disagree with production here.
        """
        # Arrange
        ladder = {
            "THRESHOLDS": {"VERY_POOR": 10, "POOR": 20, "GOOD": 70, "EXCELLENT": 90},
            "MULTIPLIERS": {
                "VERY_POOR": 0.95, "POOR": 0.975, "GOOD": 1.025, "EXCELLENT": 1.05
            },
            "WEIGHT": 1.0,
        }

        # Act
        at_very_poor = frozen_config._get_multiplier(
            ladder, 10, rising_thresholds=True
        )[1]
        probed = frozen_config._probe_tier_labels(
            ladder["THRESHOLDS"],
            (0, 100),
            lambda value: frozen_config._get_multiplier(
                ladder, value, rising_thresholds=True
            ),
        )

        # Assert
        assert at_very_poor == "VERY_POOR"
        assert probed == ALL_TIERS


class TestAllFourHorizonsAreReachable:
    """TD6 — the three horizons the active-week load-time guard never sees."""

    @pytest.mark.parametrize("week", [1, 6, 10, 14])
    def test_each_committed_horizon_loads(self, tmp_path, week):
        """Every data/configs/week*.json horizon passes the guard, not only the live one."""
        # Arrange
        data_folder = _horizon_root(tmp_path, week)

        # Act
        config = ConfigManager(data_folder)

        # Assert
        assert config.current_nfl_week == week

    def test_a_deliberately_degenerate_horizon_fails(self, tmp_path):
        """The negative control: the sweep above is not vacuously green."""
        # Arrange
        data_folder = _horizon_root(tmp_path, 1)
        week_path = data_folder / "configs" / "week1-5.json"
        week_data = json.loads(week_path.read_text())
        # MATCHUP_SCORING is mutated rather than ADP_SCORING because week1-5.json really
        # overrides this factor, so the control exercises the realistic path: a degenerate
        # ladder actually shipped in a week horizon. Do NOT "simplify" this to STEPS = 0 --
        # that trips the pre-existing "STEPS must be positive" check and never reaches
        # _validate_tier_reachability, i.e. a false green (BD2).
        week_data["parameters"]["MATCHUP_SCORING"]["THRESHOLDS"]["DIRECTION"] = "DECREASING"
        week_path.write_text(json.dumps(week_data))

        # Act
        with pytest.raises(ValueError) as excinfo:
            ConfigManager(data_folder)

        # Assert
        assert "MATCHUP_SCORING" in str(excinfo.value)


class TestDefaultedLaddersAreMaterialized:
    """UD8 — the latent KeyError the materialization pass fixes."""

    def test_a_config_omitting_temperature_and_wind_loads_and_scores(
        self, tmp_path, league_params
    ):
        """Before UD8 these accessors raised KeyError: 'EXCELLENT' on the in-code default.

        The recalculation loop iterates self.parameters and skips an absent scoring type,
        so the calculated-form temperature/wind defaults never had their tier keys
        computed. Mutation check (re-run 2026-08-12, after the materialization pass was
        hoisted out of the guard): neutralizing the _resolve_calculated_thresholds loop in
        _extract_parameters makes this test -- and only this test -- fail, 1 failed / 16
        passed. It fails with the guard's own accumulated ValueError naming TEMPERATURE_
        SCORING and WIND_SCORING THRESHOLDS as missing all four tier keys, because the
        read-only guard now runs after the materialization rather than owning it.
        Neutralizing the guard call itself is a SEPARATE mutation and no longer touches
        this test: it trips 6 tests, all of them guard tests (mutation A, same date).
        """
        # Arrange
        for key in ("TEMPERATURE_SCORING", "WIND_SCORING"):
            league_params["parameters"].pop(key, None)
        data_folder = _write_legacy_config(tmp_path, league_params)

        # Act
        config = ConfigManager(data_folder)

        # Assert
        for attribute in ("temperature_scoring", "wind_scoring"):
            thresholds = getattr(config, attribute)["THRESHOLDS"]
            for key in TIER_KEYS:
                assert key in thresholds, f"{attribute} missing {key}"
        assert config.get_temperature_multiplier(10)[1] in ALL_TIERS
        assert config.get_wind_multiplier(10)[1] in ALL_TIERS

    def test_an_author_supplied_literal_ladder_is_not_overwritten(
        self, tmp_path, league_params
    ):
        """The pass adds absent keys only; it never rewrites a literal ladder."""
        # Arrange
        league_params["parameters"]["MATCHUP_SCORING"]["THRESHOLDS"] = {
            "VERY_POOR": 3, "POOR": 8, "GOOD": 24, "EXCELLENT": 30
        }
        data_folder = _write_legacy_config(tmp_path, league_params)

        # Act
        config = ConfigManager(data_folder)

        # Assert
        assert config.matchup_scoring["THRESHOLDS"] == {
            "VERY_POOR": 3, "POOR": 8, "GOOD": 24, "EXCELLENT": 30
        }
