"""
Unit tests for PlayerManager.get_player_list — the mutable-default-argument fix.

Background (PR-Copilot finding, T42 Polish): get_player_list previously declared
`drafted_vals: List[int] = []` and `min_scores: Dict[str, float] = {}` as default
argument values. Python binds default argument objects once, at function-definition
time, and reuses the SAME object on every call that omits the argument. The method
body additionally mutated `min_scores` in place (filling in any position missing from
the dict with a 0.0 threshold), so:
  - every call that omitted `min_scores` shared and mutated the same dict object, and
  - every call that passed its OWN `min_scores` dict had that caller-owned dict mutated
    too (missing positions silently added), leaking state back out to the caller.

The fix switches both defaults to `None` and builds a fresh list/dict inside the method
each call, copying any caller-supplied `min_scores` before filling in missing positions.

Author: Kai Mizuno
"""

import inspect

import pytest
from unittest.mock import Mock

from league_helper.util.PlayerManager import PlayerManager
from utils.FantasyPlayer import FantasyPlayer


# FIXTURES / HELPERS

def _make_player(player_id, position="QB", score=0.0, fantasy_points=10.0, locked=False):
    """Build a real FantasyPlayer, free-agent by default (drafted_by="")."""
    return FantasyPlayer(
        id=player_id,
        name=f"Player {player_id}",
        team="KC",
        position=position,
        drafted_by="",
        locked=locked,
        score=score,
        fantasy_points=fantasy_points,
    )


def _make_bare_pm(players, can_draft_result=True):
    """
    Construct a minimal PlayerManager exposing only what get_player_list touches,
    bypassing the heavy __init__ (file loading, config, schedule scaffolding).
    """
    pm = PlayerManager.__new__(PlayerManager)
    pm.logger = Mock()
    pm.players = players
    pm.can_draft = Mock(return_value=can_draft_result)
    return pm


class TestGetPlayerListMutableDefaultArguments:
    """Regression coverage for the mutable-default-argument bug in get_player_list."""

    def test_defaults_are_none_not_mutable_objects(self):
        """Structural guard: drafted_vals/min_scores must default to None, never a shared
        list/dict literal, so no default object can ever accumulate mutation across calls."""
        params = inspect.signature(PlayerManager.get_player_list).parameters

        assert params["drafted_vals"].default is None
        assert params["min_scores"].default is None

    def test_calling_with_omitted_min_scores_does_not_mutate_the_functions_default(self):
        """Pre-fix, calling get_player_list() with min_scores omitted would fill the SHARED
        default {} object with every position's 0.0 threshold, mutating the function's own
        default parameter value in place (visible via introspection) so it was no longer a
        pristine {} for the next omitted-argument call. Post-fix the default stays None
        (immutable) no matter how many times the method is called with it omitted."""
        default_before = inspect.signature(PlayerManager.get_player_list).parameters["min_scores"].default

        player = _make_player(1, position="QB", score=5.0)
        pm = _make_bare_pm([player])

        # First call omits min_scores (uses the default) and can_draft=True forces the
        # per-position fill-in loop to run.
        pm.get_player_list(drafted_vals=[0], can_draft=True)
        # Second call, also omitting min_scores, to prove no accumulated state affects it.
        second_result = pm.get_player_list(drafted_vals=[0], can_draft=True)

        default_after = inspect.signature(PlayerManager.get_player_list).parameters["min_scores"].default

        assert default_before is None
        assert default_after is None  # unchanged; pre-fix this would have gained position keys
        assert second_result == [player]

    def test_passed_in_min_scores_dict_is_not_mutated(self):
        """A caller-supplied min_scores dict must come back exactly as passed - the method
        fills in missing positions on an internal copy, never the caller's own object."""
        qb = _make_player(1, position="QB", score=10.0)
        rb = _make_player(2, position="RB", score=10.0)
        pm = _make_bare_pm([qb, rb])
        caller_min_scores = {"QB": 5.0}

        result = pm.get_player_list(drafted_vals=[0], can_draft=True, min_scores=caller_min_scores)

        # Untouched: no RB/WR/TE/K/DST keys silently injected by the internal fill-in loop.
        assert caller_min_scores == {"QB": 5.0}
        assert qb in result
        assert rb in result  # RB's 10.0 score clears the internal (copy-only) 0.0 fill

    def test_passed_in_drafted_vals_list_is_not_mutated(self):
        """A caller-supplied drafted_vals list must also come back unchanged."""
        player = _make_player(1, position="QB", score=10.0)
        pm = _make_bare_pm([player])
        caller_drafted_vals = [0]

        pm.get_player_list(drafted_vals=caller_drafted_vals, can_draft=True)

        assert caller_drafted_vals == [0]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
