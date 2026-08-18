"""MISSING_VALUE_TIER: which tier an ABSENT (None) input scores as.

Before this key, a None input returned (1.0, NEUTRAL) for every factor. But 1.0
is not neutral with respect to the POPULATION -- it sits wherever the multiplier
curve crosses 1.0, around rating 55 on PLAYER_RATING_SCORING's current ladder. An
unrated player therefore outscored every rated player below that point (364 of
819 in the 2026 corpus), and ESPN omits ratings precisely for fringe players.
"""

import json
import shutil
from pathlib import Path

import pytest

from league_helper.util.ConfigManager import ConfigManager


LIVE_DATA_ROOT = Path("data")


@pytest.fixture
def data_root(tmp_path):
    """A writable copy of the live config tree."""
    root = tmp_path / "data"
    shutil.copytree(LIVE_DATA_ROOT / "configs", root / "configs")
    return root


def _write(root, mutate):
    path = root / "configs" / "league_config.json"
    config = json.loads(path.read_text())
    mutate(config["parameters"])
    path.write_text(json.dumps(config))
    return root


class TestConfiguredTier:
    def test_absent_rating_scores_as_very_poor(self, data_root):
        """The shipped setting: an unrated player is scored weak, not neutral."""
        cm = ConfigManager(data_root)
        assert cm.get_player_rating_multiplier(None) == (
            pytest.approx(0.8145062499999999), "VERY_POOR"
        )

    def test_absent_matches_a_real_input_in_that_tier_exactly(self, data_root):
        """None must land on the SAME value a real VERY_POOR input scores.

        Pins that the shared `** WEIGHT` step still applies to the substituted
        base multiplier (0.95 ** 4.0), rather than the tier's base leaking out
        unexponentiated.
        """
        cm = ConfigManager(data_root)
        assert cm.get_player_rating_multiplier(None) == cm.get_player_rating_multiplier(10)

    def test_absent_no_longer_outranks_a_weak_rating(self, data_root):
        """The defect this key exists to close."""
        cm = ConfigManager(data_root)
        missing, _ = cm.get_player_rating_multiplier(None)
        for rating in (0, 1, 10, 25, 40, 54):
            rated, _ = cm.get_player_rating_multiplier(rating)
            assert missing <= rated, f"absent still outranks rating={rating}"

    def test_real_inputs_are_unaffected(self, data_root):
        cm = ConfigManager(data_root)
        assert cm.get_player_rating_multiplier(100)[1] == "EXCELLENT"
        assert cm.get_player_rating_multiplier(55) == (pytest.approx(1.0), "GOOD")
        assert cm.get_player_rating_multiplier(10)[1] == "VERY_POOR"


class TestDefaultLandsDark:
    def test_unconfigured_factor_still_returns_neutral(self, data_root):
        """ADP does not configure the key, so its None behaviour is unchanged.

        NEUTRAL stays correct for a factor whose absence means "does not apply".
        """
        cm = ConfigManager(data_root)
        assert cm.get_adp_multiplier(None) == (pytest.approx(1.0), "NEUTRAL")

    def test_removing_the_key_restores_neutral(self, data_root):
        root = _write(data_root, lambda p: p["PLAYER_RATING_SCORING"].pop("MISSING_VALUE_TIER"))
        cm = ConfigManager(root)
        assert cm.get_player_rating_multiplier(None) == (pytest.approx(1.0), "NEUTRAL")

    def test_explicit_neutral_is_accepted(self, data_root):
        root = _write(
            data_root,
            lambda p: p["PLAYER_RATING_SCORING"].update({"MISSING_VALUE_TIER": "NEUTRAL"}),
        )
        cm = ConfigManager(root)
        assert cm.get_player_rating_multiplier(None) == (pytest.approx(1.0), "NEUTRAL")


class TestEveryTierIsSelectable:
    @pytest.mark.parametrize("tier", ["VERY_POOR", "POOR", "GOOD", "EXCELLENT"])
    def test_configured_tier_matches_that_tier(self, data_root, tier):
        root = _write(
            data_root,
            lambda p, t=tier: p["PLAYER_RATING_SCORING"].update({"MISSING_VALUE_TIER": t}),
        )
        cm = ConfigManager(root)
        multiplier, label = cm.get_player_rating_multiplier(None)
        assert label == tier
        base = json.loads((root / "configs" / "league_config.json").read_text())
        block = base["parameters"]["PLAYER_RATING_SCORING"]
        expected = block["MULTIPLIERS"][tier] ** block["WEIGHT"]
        assert multiplier == pytest.approx(expected)


class TestInvalidValueRaisesAtLoad:
    def test_typo_raises_rather_than_degrading_to_neutral(self, data_root):
        """A silently-ignored typo would restore the old behaviour invisibly."""
        root = _write(
            data_root,
            lambda p: p["PLAYER_RATING_SCORING"].update({"MISSING_VALUE_TIER": "VERYPOOR"}),
        )
        with pytest.raises(ValueError, match="MISSING_VALUE_TIER"):
            ConfigManager(root)

    def test_the_raise_names_the_offending_factor_and_value(self, data_root):
        root = _write(
            data_root,
            lambda p: p["PLAYER_RATING_SCORING"].update({"MISSING_VALUE_TIER": "bogus"}),
        )
        with pytest.raises(ValueError) as excinfo:
            ConfigManager(root)
        message = str(excinfo.value)
        assert "PLAYER_RATING_SCORING" in message
        assert "bogus" in message
