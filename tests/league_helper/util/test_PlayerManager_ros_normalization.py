"""
Regression tests for the JSON-load normalization denominator (T47).

Story: ros-normalization-denominator-mismatch. Guards the fix that aligns the score-
normalization DENOMINATOR (PlayerManager.load_players_from_json -> max_projection) with the
rest-of-season (ROS) NUMERATOR used by scoring Step 1 (weight_projection), so the two share
the same current_week..17 week window.

Covers:
- AC1: at a mid-season week the max-ROS player's Step-1 normalized base == scale (within 1%),
       materially above the ~scale/2 the old full-season denominator produced.
- AC2: that base stays == scale across weeks 4, 8, 12 (additive-bonus-to-base ratio stable).
- AC3: the weekly path (use_weekly_max=True, max_weekly_projection) is invariant to max_projection.
- AC4: at week 1 the fix is a no-op (ROS == full-season -> denominator unchanged).

Fixtures use two synthetic players whose full-season and rest-of-season leaders DIFFER at
mid-season, so a revert to `max(p.fantasy_points ...)` breaks AC1/AC2:
- "Steady Star"  : projected_points = [10.0]*17           -> full-season 170.0; the mid-season ROS leader.
- "Front Loaded" : projected_points = [30.0]*6 + [2.0]*11 -> full-season 202.0 (the season leader),
                   but a small ROS mid-season.

Author: Kai Mizuno
"""

import json
from unittest.mock import Mock

import pytest

from league_helper.util.PlayerManager import PlayerManager
from league_helper.util.player_scoring import PlayerScoringCalculator


DRAFT_SCALE = 163.0
SEASON_SCALE = 100.0


# FIXTURES

@pytest.fixture
def mock_config():
    """A minimal config exposing only what the load + scoring paths read."""
    config = Mock()
    config.current_nfl_week = 1
    config.draft_normalization_max_scale = DRAFT_SCALE
    config.normalization_max_scale = SEASON_SCALE
    return config


@pytest.fixture
def player_data_folder(tmp_path):
    """Write the 6 position JSON files load_players_from_json() expects, with two QBs
    whose full-season vs rest-of-season leaders diverge at mid-season."""
    data_folder = tmp_path / "data"
    data_folder.mkdir()
    player_data_dir = data_folder / "player_data"
    player_data_dir.mkdir()

    qb_data = {
        "qb_data": [
            {
                "id": "1",
                "name": "Steady Star",
                "team": "KC",
                "position": "QB",
                "projected_points": [10.0] * 17,
                "actual_points": [0.0] * 17,
            },
            {
                "id": "2",
                "name": "Front Loaded",
                "team": "BUF",
                "position": "QB",
                "projected_points": [30.0] * 6 + [2.0] * 11,
                "actual_points": [0.0] * 17,
            },
        ]
    }
    (player_data_dir / "qb_data.json").write_text(json.dumps(qb_data))

    for position in ["rb", "wr", "te", "k", "dst"]:
        (player_data_dir / f"{position}_data.json").write_text(
            json.dumps({f"{position}_data": []})
        )

    return data_folder


def _make_player_manager(data_folder, config):
    """Build a PlayerManager wired for load_players_from_json() with a REAL scoring calculator.

    Bypasses the heavy __init__; load_team is stubbed (roster scaffolding is out of scope).
    """
    pm = PlayerManager.__new__(PlayerManager)
    pm.data_folder = data_folder
    pm.config = config
    pm.players = []
    pm.max_projection = 0.0
    pm.logger = Mock()
    pm.load_team = Mock()
    pm.scoring_calculator = PlayerScoringCalculator(
        config,
        pm,
        max_projection=0.0,
        team_data_manager=Mock(),
        season_schedule_manager=Mock(),
        current_nfl_week=config.current_nfl_week,
    )
    return pm


def _load_at_week(data_folder, config, week):
    """Reload players at a given current NFL week and return the PlayerManager."""
    config.current_nfl_week = week
    pm = _make_player_manager(data_folder, config)
    pm.load_players_from_json()
    return pm


def _player(pm, name):
    return next(p for p in pm.players if p.name == name)


# TESTS

class TestRosNormalizationDenominator:
    """T47: the JSON-load denominator shares the ROS numerator's week window."""

    def test_ac1_mid_season_base_equals_scale(self, player_data_folder, mock_config):
        # Arrange: mid-season week 10; Steady Star is the ROS leader, Front Loaded the season leader.
        pm = _load_at_week(player_data_folder, mock_config, week=10)
        steady = _player(pm, "Steady Star")
        steady_ros = steady.get_rest_of_season_projection(mock_config)

        # Act: Step-1 normalized base for the max-ROS player in draft/Add-to-Roster mode.
        pm.scoring_calculator.is_draft_mode = True
        base = pm.scoring_calculator.weight_projection(steady_ros)

        # Assert: denominator is the ROS max (80.0), NOT the full-season max (202.0).
        assert pm.max_projection == pytest.approx(80.0)
        assert pm.max_projection < max(p.fantasy_points for p in pm.players)
        # Max-ROS player normalizes to pts/max == 1 -> base == full scale (within 1%)...
        assert base == pytest.approx(DRAFT_SCALE, rel=0.01)
        # ...materially above the ~scale/2 the old full-season denominator produced.
        assert base > DRAFT_SCALE / 2

    def test_ac2_base_stable_across_weeks(self, player_data_folder, mock_config):
        # The max-ROS player's base stays == scale as the current week advances.
        for week in (4, 8, 12):
            pm = _load_at_week(player_data_folder, mock_config, week=week)
            steady = _player(pm, "Steady Star")
            steady_ros = steady.get_rest_of_season_projection(mock_config)

            pm.scoring_calculator.is_draft_mode = True
            base = pm.scoring_calculator.weight_projection(steady_ros)

            assert base == pytest.approx(DRAFT_SCALE, rel=0.01), f"week {week}"

    def test_ac3_weekly_path_invariant_to_max_projection(self, player_data_folder, mock_config):
        # The weekly path normalizes by max_weekly_projection and must ignore max_projection.
        pm = _load_at_week(player_data_folder, mock_config, week=10)
        calc = pm.scoring_calculator
        calc.is_draft_mode = False
        calc.max_weekly_projection = 50.0

        calc.max_projection = 999.0
        weekly_before = calc.weight_projection(25.0, use_weekly_max=True)

        calc.max_projection = 111.0  # simulate the fix changing the ROS denominator
        weekly_after = calc.weight_projection(25.0, use_weekly_max=True)

        assert weekly_before == weekly_after
        assert weekly_before == pytest.approx((25.0 / 50.0) * SEASON_SCALE)

    def test_ac4_week_1_is_noop(self, player_data_folder, mock_config):
        # At week 1, ROS == full-season, so the new denominator equals the old max(fantasy_points).
        pm = _load_at_week(player_data_folder, mock_config, week=1)

        old_denominator = max(p.fantasy_points for p in pm.players)
        assert pm.max_projection == pytest.approx(old_denominator)
        assert pm.max_projection == pytest.approx(202.0)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
