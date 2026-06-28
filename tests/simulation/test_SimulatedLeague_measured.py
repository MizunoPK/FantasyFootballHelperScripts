"""
Unit Tests for SimulatedLeague measured-vs-reference per-team config.

Covers the measured_config_dict capability: the measured DraftHelperTeam scores with its own config
while every other team holds the reference config (divergence), the D2 fail-fast guard (measured
config supplied but no draft_helper team), the D3 load-failure handling (malformed measured dict ->
clear attributed error), and back-compat (measured_config_dict=None preserves legacy behavior).

Unlike test_SimulatedLeague.py, these tests run the REAL _initialize_teams against the committed
simulation/sim_data/2025/ data, so they do NOT patch _initialize_teams.

Author: Kai Mizuno
"""

import copy
from pathlib import Path

import pytest
from unittest.mock import patch

from league_helper.util.ConfigManager import ConfigManager
from simulation.win_rate.SimulatedLeague import SimulatedLeague


# FIXTURES

REAL_DATA_FOLDER = Path("simulation/sim_data/2025")


@pytest.fixture
def base_config_dict():
    """Full reference config dict (merged ConfigManager shape, as CombinationEvaluator builds it)."""
    cm = ConfigManager(Path("data"))
    return {
        "config_name": cm.config_name,
        "description": cm.description,
        "parameters": dict(cm.parameters),
    }


@pytest.fixture
def measured_config_dict(base_config_dict):
    """A copy of base_config_dict with a draft-side param bumped so it provably differs."""
    measured = copy.deepcopy(base_config_dict)
    measured["parameters"]["DRAFT_NORMALIZATION_MAX_SCALE"] = (
        base_config_dict["parameters"]["DRAFT_NORMALIZATION_MAX_SCALE"] + 999
    )
    return measured


class TestMeasuredVsReferenceDivergence:
    """Headline test: measured team's draft params provably differ from the reference team's."""

    def test_measured_team_draft_params_differ_from_reference_team(
        self, base_config_dict, measured_config_dict
    ):
        # Arrange: force a self-play composition (2 draft_helper teams, no opponents).
        self_play = {"draft_helper": 2}

        league = None
        try:
            with patch.object(SimulatedLeague, "TEAM_STRATEGIES", self_play):
                # Act
                league = SimulatedLeague(
                    base_config_dict,
                    REAL_DATA_FOLDER,
                    measured_config_dict=measured_config_dict,
                )

            measured_team = league.draft_helper_team
            reference_teams = [t for t in league.teams if t is not measured_team]

            # Assert: two teams total; one measured + one reference draft_helper.
            assert len(league.teams) == 2
            assert measured_team is not None
            assert len(reference_teams) == 1
            reference_team = reference_teams[0]

            # The measured team carries the measured draft-side param; the reference team carries
            # the reference value; the two provably differ.
            assert (
                measured_team.config.draft_normalization_max_scale
                == measured_config_dict["parameters"]["DRAFT_NORMALIZATION_MAX_SCALE"]
            )
            assert (
                reference_team.config.draft_normalization_max_scale
                == base_config_dict["parameters"]["DRAFT_NORMALIZATION_MAX_SCALE"]
            )
            assert (
                measured_team.config.draft_normalization_max_scale
                != reference_team.config.draft_normalization_max_scale
            )
        finally:
            if league is not None:
                league.cleanup()


class TestMeasuredConfigZeroDraftHelperGuard:
    """D2: measured_config_dict provided + zero draft_helper teams -> ValueError."""

    def test_zero_draft_helper_with_measured_config_raises(
        self, base_config_dict, measured_config_dict
    ):
        # Arrange: a composition with NO draft_helper team.
        no_draft_helper = {"adp_aggressive": 2}

        league = None
        try:
            with patch.object(SimulatedLeague, "TEAM_STRATEGIES", no_draft_helper):
                # Act / Assert
                with pytest.raises(ValueError) as exc_info:
                    league = SimulatedLeague(
                        base_config_dict,
                        REAL_DATA_FOLDER,
                        measured_config_dict=measured_config_dict,
                    )

            assert "no 'draft_helper' team" in str(exc_info.value)
        finally:
            if league is not None:
                league.cleanup()


class TestMeasuredConfigLoadFailure:
    """D3: malformed/invalid measured_config_dict -> clear ValueError raised (re-raised, not swallowed)."""

    def test_malformed_measured_config_raises_value_error(self, base_config_dict):
        # Arrange: a measured dict missing required parameters (ConfigManager will reject it).
        bad_measured = {
            "config_name": "bad",
            "description": "malformed measured config",
            "parameters": {"CURRENT_NFL_WEEK": 1},
        }

        league = None
        try:
            # Act / Assert: ConfigManager raises ValueError for missing required params; the D3 wrap
            # logs an attributed message and re-raises the same exception.
            with pytest.raises(ValueError) as exc_info:
                league = SimulatedLeague(
                    base_config_dict,
                    REAL_DATA_FOLDER,
                    measured_config_dict=bad_measured,
                )

            assert "missing required parameters" in str(exc_info.value)
        finally:
            if league is not None:
                league.cleanup()


class TestMeasuredConfigBackCompat:
    """Back-compat: measured_config_dict=None preserves legacy single-config behavior."""

    def test_none_preserves_legacy_last_draft_helper(self, base_config_dict):
        # Arrange / Act: default composition (1 draft_helper + 9 opponents), no measured config.
        league = None
        try:
            league = SimulatedLeague(base_config_dict, REAL_DATA_FOLDER)

            # Assert: legacy behavior unchanged — the league builds, a measured (draft_helper) team
            # exists, and it shares the reference config draft params (no separate measured config).
            assert len(league.teams) == 10
            assert league.draft_helper_team is not None
            assert (
                league.draft_helper_team.config.draft_normalization_max_scale
                == base_config_dict["parameters"]["DRAFT_NORMALIZATION_MAX_SCALE"]
            )
        finally:
            if league is not None:
                league.cleanup()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
