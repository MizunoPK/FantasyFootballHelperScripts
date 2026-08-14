"""
Test coverage for the win-rate per-week team-context refresh.

Tests the SimulatedLeague._refresh_team_context() method (D6.1; T50 D4-B
covered its matchup-only predecessor) and its integration into the run_season
per-week loop.
Covers the helper method, the hasattr guard, the per-week refresh ordering
(after _update_team_rankings), and per-week correctness of all three refreshed
fields as the week advances.
"""

import pytest
import inspect
from unittest.mock import Mock

from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.simulation.win_rate.SimulatedLeague import SimulatedLeague
from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.league_helper.util.TeamDataManager import TeamDataManager
from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.league_helper.util.PlayerManager import PlayerManager
from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.utils.FantasyPlayer import FantasyPlayer


def _make_player(team, position, name="P"):
    """Minimal FantasyPlayer; matchup_score defaults to None after the D3 widening."""
    return FantasyPlayer.from_json({
        "id": 1,
        "name": name,
        "team": team,
        "position": position,
        "projected_points": [10.0] * 17,
        "actual_points": [0.0] * 17,
    })


class TestRefreshTeamContextHelper:
    def test_refreshes_each_team_projected_pm(self):
        league = SimulatedLeague.__new__(SimulatedLeague)
        team_a = Mock()
        team_b = Mock()
        league.teams = [team_a, team_b]

        league._refresh_team_context()

        team_a.projected_pm.refresh_team_context.assert_called_once()
        team_b.projected_pm.refresh_team_context.assert_called_once()

    def test_skips_team_without_projected_pm(self):
        league = SimulatedLeague.__new__(SimulatedLeague)

        class _NoPM:
            projected_pm = None    # falsy -> guard skips; refresh on None would AttributeError

        league.teams = [_NoPM()]

        league._refresh_team_context()   # must not raise (team skipped by the guard)


class TestRunSeasonOrdering:
    def test_refresh_runs_after_update_team_rankings(self):
        src = inspect.getsource(SimulatedLeague.run_season)
        assert "_refresh_team_context()" in src
        assert src.index("_update_team_rankings(week_num)") < src.index("_refresh_team_context()")


class TestPerWeekRecompute:
    def test_refresh_reads_advanced_week(self):
        tdm = TeamDataManager.__new__(TeamDataManager)
        tdm.logger = Mock()
        tdm.offensive_ranks = {"DAL": 5, "PHI": 20}          # is_matchup_available() -> True
        tdm.position_ranks = {"DAL": {"RB": 3}, "PHI": {"RB": 30}}
        # refresh_team_context reads the player's OWN-team rank dicts too, so a fixture
        # seeding only offensive_ranks/position_ranks would AttributeError:
        tdm.defensive_ranks = {"DAL": 24, "PHI": 11}
        tdm.dst_fantasy_ranks = {"DAL": 26, "PHI": 2}
        tdm.season_schedule_manager = Mock()                 # assign BEFORE setting .get_opponent
        tdm.season_schedule_manager.get_opponent = Mock(
            side_effect=lambda team, week: {("KC", 6): "DAL", ("KC", 7): "PHI"}.get((team, week))
        )

        pm = PlayerManager.__new__(PlayerManager)
        pm.team_data_manager = tdm
        pm.players = [_make_player("KC", "RB")]

        tdm.current_nfl_week = 6
        pm.refresh_team_context()
        score_wk6 = pm.players[0].matchup_score              # DAL -> position_ranks["DAL"]["RB"] = 3

        tdm.current_nfl_week = 7
        pm.refresh_team_context()
        score_wk7 = pm.players[0].matchup_score              # PHI -> position_ranks["PHI"]["RB"] = 30

        assert score_wk6 == 3
        assert score_wk7 == 30
        assert score_wk6 != score_wk7                        # per-week correct, not frozen at construction

    def test_refresh_reads_advanced_week_ranks(self):
        """D6.1: the two team-rank fields track the advanced week too, not matchup_score alone.

        _update_team_rankings -> set_current_week -> _calculate_rankings rewrites the rank
        dicts in place; this fixture reproduces that by reassigning them between the two
        refresh calls. A populate that cached, or that ran only at load, would leave the
        week-6 values in place and fail here.
        """
        tdm = TeamDataManager.__new__(TeamDataManager)
        tdm.logger = Mock()
        tdm.position_ranks = {"DAL": {"RB": 3}, "PHI": {"RB": 30}}
        tdm.season_schedule_manager = Mock()
        tdm.season_schedule_manager.get_opponent = Mock(
            side_effect=lambda team, week: {("KC", 6): "DAL", ("KC", 7): "PHI"}.get((team, week))
        )

        pm = PlayerManager.__new__(PlayerManager)
        pm.team_data_manager = tdm
        pm.players = [_make_player("KC", "RB")]

        tdm.current_nfl_week = 6
        tdm.offensive_ranks = {"KC": 3, "DAL": 5, "PHI": 20}   # is_matchup_available() -> True
        tdm.defensive_ranks = {"KC": 7, "DAL": 24, "PHI": 11}
        tdm.dst_fantasy_ranks = {"KC": 17, "DAL": 26, "PHI": 2}
        pm.refresh_team_context()
        off_wk6 = pm.players[0].team_offensive_rank
        def_wk6 = pm.players[0].team_defensive_rank

        tdm.current_nfl_week = 7
        tdm.offensive_ranks = {"KC": 27, "DAL": 5, "PHI": 20}
        tdm.defensive_ranks = {"KC": 19, "DAL": 24, "PHI": 11}
        tdm.dst_fantasy_ranks = {"KC": 17, "DAL": 26, "PHI": 2}
        pm.refresh_team_context()
        off_wk7 = pm.players[0].team_offensive_rank
        def_wk7 = pm.players[0].team_defensive_rank

        assert (off_wk6, def_wk6) == (3, 7)
        assert (off_wk7, def_wk7) == (27, 19)
        assert off_wk6 != off_wk7                            # read live per week, never cached
        assert def_wk6 != def_wk7
