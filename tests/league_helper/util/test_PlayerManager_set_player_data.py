"""
Unit tests for PlayerManager.set_player_data — the D1 in-place array swap.

Story: winrate-sim-lookahead-frozen-snapshot. Verifies the array-contract behavior the
win-rate point-in-time data swap depends on:
- projected_points / actual_points arrays are replaced in place (padded to 17)
- fantasy_points is recomputed as sum(projected_points)
- draft state (drafted_by / locked) is preserved across the swap
- the stale weekly-projection cache is invalidated
- only players present in the incoming dataset are updated
- an empty dataset is a no-op

Author: Kai Mizuno
"""

import pytest
from unittest.mock import Mock

from league_helper.util.PlayerManager import PlayerManager
from utils.FantasyPlayer import FantasyPlayer


def _make_player(player_id, projected=None, actual=None, drafted_by="", locked=False):
    """Build a real FantasyPlayer with the given arrays (padded to 17)."""
    proj = (list(projected or []) + [0.0] * 17)[:17]
    act = (list(actual or []) + [0.0] * 17)[:17]
    return FantasyPlayer(
        id=player_id,
        name=f"Player {player_id}",
        team="KC",
        position="RB",
        drafted_by=drafted_by,
        locked=locked,
        projected_points=proj,
        actual_points=act,
        fantasy_points=sum(proj),
    )


def _make_bare_pm(players):
    """
    Construct a minimal PlayerManager exposing only the attributes set_player_data touches,
    bypassing the heavy __init__ (file loading, config, schedule, team-data scaffolding).
    """
    pm = PlayerManager.__new__(PlayerManager)
    pm.logger = Mock()
    pm.players = players
    pm.max_projection = 0.0
    pm.max_weekly_projections = {5: 999.0}  # pre-seeded stale cache — must be cleared
    pm.scoring_calculator = Mock()
    pm.scoring_calculator.max_projection = 0.0
    pm.scoring_calculator.max_weekly_projection = 999.0  # stale — must be reset
    pm.scoring_calculator.weight_projection = lambda fp: fp / 100.0
    return pm


class TestSetPlayerDataArrayContract:
    """D1: set_player_data replaces arrays in place and refreshes derived state."""

    def test_replaces_projected_and_actual_arrays_in_place(self):
        player = _make_player(1, projected=[5.0] * 17, actual=[0.0] * 17)
        pm = _make_bare_pm([player])

        pm.set_player_data({1: {
            'projected_points': [15.0] * 17,
            'actual_points': [12.0] + [0.0] * 16,
        }})

        assert player.projected_points == [15.0] * 17
        assert player.actual_points == [12.0] + [0.0] * 16

    def test_recomputes_fantasy_points_as_sum_projected(self):
        player = _make_player(1, projected=[5.0] * 17)
        pm = _make_bare_pm([player])

        pm.set_player_data({1: {
            'projected_points': [2.0] * 17,
            'actual_points': [0.0] * 17,
        }})

        assert player.fantasy_points == pytest.approx(34.0)  # 2.0 * 17

    def test_pads_short_arrays_to_17(self):
        player = _make_player(1)
        pm = _make_bare_pm([player])

        pm.set_player_data({1: {
            'projected_points': [7.0, 8.0, 9.0],
            'actual_points': [1.0],
        }})

        assert player.projected_points == [7.0, 8.0, 9.0] + [0.0] * 14
        assert player.actual_points == [1.0] + [0.0] * 16

    def test_preserves_drafted_by_and_locked(self):
        player = _make_player(1, projected=[5.0] * 17, drafted_by="Team A", locked=True)
        pm = _make_bare_pm([player])

        pm.set_player_data({1: {
            'projected_points': [15.0] * 17,
            'actual_points': [0.0] * 17,
        }})

        assert player.drafted_by == "Team A"
        assert player.locked is True

    def test_invalidates_weekly_projection_cache(self):
        player = _make_player(1, projected=[5.0] * 17)
        pm = _make_bare_pm([player])

        pm.set_player_data({1: {
            'projected_points': [15.0] * 17,
            'actual_points': [0.0] * 17,
        }})

        assert pm.max_weekly_projections == {}
        assert pm.scoring_calculator.max_weekly_projection == 0.0

    def test_updates_only_players_present_in_dataset(self):
        p1 = _make_player(1, projected=[5.0] * 17)
        p2 = _make_player(2, projected=[6.0] * 17)
        pm = _make_bare_pm([p1, p2])

        pm.set_player_data({1: {
            'projected_points': [15.0] * 17,
            'actual_points': [0.0] * 17,
        }})

        assert p1.projected_points == [15.0] * 17
        assert p2.projected_points == [6.0] * 17  # untouched

    def test_refreshes_max_projection(self):
        p1 = _make_player(1, projected=[5.0] * 17)
        p2 = _make_player(2, projected=[6.0] * 17)
        pm = _make_bare_pm([p1, p2])

        pm.set_player_data({
            1: {'projected_points': [10.0] * 17, 'actual_points': [0.0] * 17},
            2: {'projected_points': [20.0] * 17, 'actual_points': [0.0] * 17},
        })

        assert pm.max_projection == pytest.approx(340.0)  # 20.0 * 17
        assert pm.scoring_calculator.max_projection == pytest.approx(340.0)

    def test_empty_dataset_is_noop(self):
        player = _make_player(1, projected=[5.0] * 17)
        pm = _make_bare_pm([player])

        pm.set_player_data({})

        assert player.projected_points == [5.0] * 17
        assert pm.max_weekly_projections == {5: 999.0}  # untouched on no-op

    def test_all_zero_swap_resets_max_projection_and_weighted_projection(self):
        """T42 Polish fix: an all-zero-value swap must not leave the PRIOR week's
        max_projection / weighted_projection stale. Pre-fix, the refresh was guarded by
        `if new_max_projection > 0`, so a swap where every incoming player has
        fantasy_points == 0 skipped the refresh entirely and left both values stuck at
        their previous (positive) week's numbers."""
        player = _make_player(1, projected=[10.0] * 17)  # positive prior week
        pm = _make_bare_pm([player])
        pm.max_projection = 170.0  # stale prior-week max
        pm.scoring_calculator.max_projection = 170.0
        player.weighted_projection = 42.0  # stale prior-week weighted value

        pm.set_player_data({1: {
            'projected_points': [0.0] * 17,
            'actual_points': [0.0] * 17,
        }})

        assert pm.max_projection == 0.0
        assert pm.scoring_calculator.max_projection == 0.0
        assert player.weighted_projection == 0.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
