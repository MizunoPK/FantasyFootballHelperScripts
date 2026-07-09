"""
Regression tests for the naive-opponents draft path (T42 fix: point-in-time
positive-value pool exhaustion).

Background: the D3 point-in-time swap (SimulatedLeague.run_draft calling
_load_week_data(1) before the draft loop) makes the DraftHelperTeam draft against
week-1 projections instead of the season-end (week_18) snapshot. Week-1 projections
are legitimately sparser than season-end ones (many bench/backup players carry a
true zero season-long projection before the season starts), and SimulatedOpponent
(the --naive-opponents field) drafts with no per-position roster-limit enforcement,
so it can hoard more than its fair share of the scarce positive-value players at a
position. Combined, this could exhaust the positive-value pool for a position before
every team's roster need for that position was met, leaving
AddToRosterModeManager.get_recommendations() with zero candidates for a still-open
roster slot -> DraftHelperTeam.get_draft_recommendation() raised ValueError ->
SimulatedLeague.run_draft() crashed, dropping the whole league to a 0.000 win rate.

Confirmed pre-fix reproduction: simulation/sim_data/2022 and simulation/sim_data/2024
(naive_opponents=True, seed=1) both raised "No draft recommendations available -
roster may be full" before this fix; simulation/sim_data/2021 and .../2025 did not
(both seasons happened to retain enough week-1 positive-value QBs). This file guards
both the exact reproduction (real committed season data) and the underlying fallback
mechanism (PlayerManager.get_player_list(require_positive_points=False) /
AddToRosterModeManager.get_recommendations()) directly, so the mechanism stays
covered even if the committed historical data is later recompiled.

Author: Kai Mizuno
"""

from pathlib import Path
from unittest.mock import Mock

import pytest

from league_helper.add_to_roster_mode.AddToRosterModeManager import AddToRosterModeManager
from league_helper.util.ConfigManager import ConfigManager
from league_helper.util.PlayerManager import PlayerManager
from league_helper.util.TeamDataManager import TeamDataManager
from simulation.win_rate.SimulatedLeague import SimulatedLeague
from utils.FantasyPlayer import FantasyPlayer


# FIXTURES

@pytest.fixture
def base_config_dict():
    """Full reference config dict (merged ConfigManager shape, as CombinationEvaluator builds it)."""
    cm = ConfigManager(Path("data"))
    return {
        "config_name": cm.config_name,
        "description": cm.description,
        "parameters": dict(cm.parameters),
    }


# HELPERS

def _make_player(player_id, position="QB", fantasy_points=0.0, drafted_by=""):
    """Build a real FantasyPlayer with a single-value-repeated 17-week projected array."""
    return FantasyPlayer(
        id=player_id,
        name=f"Player {player_id}",
        team="KC",
        position=position,
        bye_week=None,
        drafted_by=drafted_by,
        locked=False,
        projected_points=[fantasy_points] + [0.0] * 16,
        actual_points=[0.0] * 17,
        fantasy_points=fantasy_points,
        average_draft_position=50.0,
        player_rating=50.0,
    )


def _make_bare_pm(players, can_draft_result=True):
    """
    Construct a minimal PlayerManager exposing only what get_player_list touches,
    bypassing the heavy __init__ (file loading, config, schedule scaffolding).
    can_draft is stubbed directly (FantasyTeam.can_draft's own position-limit logic
    is covered elsewhere) so this isolates get_player_list's own filtering.
    """
    pm = PlayerManager.__new__(PlayerManager)
    pm.logger = Mock()
    pm.players = players
    pm.can_draft = Mock(return_value=can_draft_result)
    return pm


class TestNaiveModeDraftCompletion:
    """
    Full naive-opponents draft-to-completion regression, on real committed season
    data known to have reproduced the T42 crash pre-fix (naive_opponents=True,
    seed=1 on the 2022 and 2024 sim_data seasons).
    """

    @pytest.mark.parametrize("season", ["2022", "2024"])
    def test_naive_draft_completes_all_rosters(self, base_config_dict, season):
        """All 10 teams reach exactly 15 players; run_draft() raises nothing."""
        data_folder = Path(f"simulation/sim_data/{season}")
        league = SimulatedLeague(base_config_dict, data_folder, naive_opponents=True, seed=1)
        try:
            league.run_draft()

            assert len(league.teams) == 10
            for team in league.teams:
                assert len(team.roster) == 15

            assert league.draft_helper_team is not None
            assert len(league.draft_helper_team.roster) == 15
        finally:
            league.cleanup()


class TestPositiveValuePoolExhaustionFallback:
    """
    Deterministic, data-independent coverage of the fallback mechanism itself:
    PlayerManager.get_player_list(..., require_positive_points=False) and
    AddToRosterModeManager.get_recommendations() falling back to zero-value
    roster-legal candidates when the positive-value pool is exhausted.
    """

    def test_get_player_list_default_excludes_zero_value_players(self):
        """Default (require_positive_points=True) behavior is unchanged: zero/None-value
        players are excluded from the can_draft-filtered list."""
        positive_player = _make_player(1, fantasy_points=100.0)
        zero_player = _make_player(2, fantasy_points=0.0)
        pm = _make_bare_pm([positive_player, zero_player])

        result = pm.get_player_list(drafted_vals=[0], can_draft=True)

        assert result == [positive_player]

    def test_get_player_list_fallback_includes_zero_value_players(self):
        """require_positive_points=False surfaces roster-legal zero-value players too."""
        positive_player = _make_player(1, fantasy_points=100.0)
        zero_player = _make_player(2, fantasy_points=0.0)
        pm = _make_bare_pm([positive_player, zero_player])

        result = pm.get_player_list(drafted_vals=[0], can_draft=True, require_positive_points=False)

        assert positive_player in result
        assert zero_player in result
        assert len(result) == 2

    def test_get_player_list_fallback_excludes_roster_illegal_players(self):
        """require_positive_points=False still respects can_draft (roster legality)."""
        zero_player = _make_player(1, fantasy_points=0.0)
        pm = _make_bare_pm([zero_player], can_draft_result=False)

        result = pm.get_player_list(drafted_vals=[0], can_draft=True, require_positive_points=False)

        assert result == []

    def test_get_recommendations_falls_back_when_positive_pool_empty(self):
        """
        AddToRosterModeManager.get_recommendations() must not return [] (which
        DraftHelperTeam.get_draft_recommendation() turns into a hard ValueError) when
        the positive-value pool is empty but roster-legal zero-value candidates exist.
        """
        zero_value_qb = _make_player(1, position="QB", fantasy_points=0.0)

        player_manager = Mock(spec=PlayerManager)
        player_manager.team = Mock()
        player_manager.team.roster = []  # roster not full -> a current round exists
        call_log = []

        def get_player_list_side_effect(drafted_vals=None, can_draft=False, require_positive_points=True):
            call_log.append(require_positive_points)
            if require_positive_points:
                return []  # positive-value pool exhausted
            return [zero_value_qb]

        player_manager.get_player_list = Mock(side_effect=get_player_list_side_effect)
        player_manager.score_player = Mock(
            return_value=Mock(score=0.0, player=zero_value_qb)
        )

        team_data_manager = Mock(spec=TeamDataManager)
        config = Mock()
        config.max_players = 15

        manager = AddToRosterModeManager(config, player_manager, team_data_manager)
        # Roster not full (1 of 15 slots filled) so _get_current_round() returns a round.
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(manager, "_get_current_round", lambda: 2)
            recommendations = manager.get_recommendations()

        assert len(recommendations) == 1
        assert recommendations[0].player is zero_value_qb
        # Confirms the fallback path was actually exercised: first call requires
        # positive points (default True), second call relaxes it (False).
        assert call_log == [True, False]

    def test_get_recommendations_returns_empty_when_truly_no_candidates(self):
        """When even the fallback finds nothing (position genuinely exhausted /
        roster-illegal), get_recommendations() still returns [] rather than crashing
        itself — DraftHelperTeam.get_draft_recommendation() is the one that raises."""
        player_manager = Mock(spec=PlayerManager)
        player_manager.team = Mock()
        player_manager.team.roster = []
        player_manager.get_player_list = Mock(return_value=[])

        team_data_manager = Mock(spec=TeamDataManager)
        config = Mock()
        config.max_players = 15

        manager = AddToRosterModeManager(config, player_manager, team_data_manager)
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(manager, "_get_current_round", lambda: 2)
            recommendations = manager.get_recommendations()

        assert recommendations == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
