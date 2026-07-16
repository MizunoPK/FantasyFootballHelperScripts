"""
Test coverage for T50 D4-B: win-rate per-week matchup_score refresh.

Tests the SimulatedLeague._refresh_matchup_scores() method and its integration
into the run_season per-week loop. Covers the helper method, the hasattr guard,
the per-week refresh ordering (after _update_team_rankings), and per-week
correctness as the week advances.
"""

import pytest
import inspect
from unittest.mock import Mock

from simulation.win_rate.SimulatedLeague import SimulatedLeague
from league_helper.util.TeamDataManager import TeamDataManager
from league_helper.util.PlayerManager import PlayerManager
from utils.FantasyPlayer import FantasyPlayer


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


class TestRefreshMatchupScoresHelper:
    def test_refreshes_each_team_projected_pm(self):
        league = SimulatedLeague.__new__(SimulatedLeague)
        team_a = Mock()
        team_b = Mock()
        league.teams = [team_a, team_b]

        league._refresh_matchup_scores()

        team_a.projected_pm.refresh_matchup_scores.assert_called_once()
        team_b.projected_pm.refresh_matchup_scores.assert_called_once()

    def test_skips_team_without_projected_pm(self):
        league = SimulatedLeague.__new__(SimulatedLeague)

        class _NoPM:
            projected_pm = None    # falsy -> guard skips; refresh on None would AttributeError

        league.teams = [_NoPM()]

        league._refresh_matchup_scores()   # must not raise (team skipped by the guard)


class TestRunSeasonOrdering:
    def test_refresh_runs_after_update_team_rankings(self):
        src = inspect.getsource(SimulatedLeague.run_season)
        assert "_refresh_matchup_scores()" in src
        assert src.index("_update_team_rankings(week_num)") < src.index("_refresh_matchup_scores()")


class TestPerWeekRecompute:
    def test_refresh_reads_advanced_week(self):
        tdm = TeamDataManager.__new__(TeamDataManager)
        tdm.logger = Mock()
        tdm.offensive_ranks = {"DAL": 5, "PHI": 20}          # is_matchup_available() -> True
        tdm.position_ranks = {"DAL": {"RB": 3}, "PHI": {"RB": 30}}
        tdm.season_schedule_manager = Mock()                 # assign BEFORE setting .get_opponent
        tdm.season_schedule_manager.get_opponent = Mock(
            side_effect=lambda team, week: {("KC", 6): "DAL", ("KC", 7): "PHI"}.get((team, week))
        )

        pm = PlayerManager.__new__(PlayerManager)
        pm.team_data_manager = tdm
        pm.players = [_make_player("KC", "RB")]

        tdm.current_nfl_week = 6
        pm.refresh_matchup_scores()
        score_wk6 = pm.players[0].matchup_score              # DAL -> position_ranks["DAL"]["RB"] = 3

        tdm.current_nfl_week = 7
        pm.refresh_matchup_scores()
        score_wk7 = pm.players[0].matchup_score              # PHI -> position_ranks["PHI"]["RB"] = 30

        assert score_wk6 == 3
        assert score_wk7 == 30
        assert score_wk6 != score_wk7                        # per-week correct, not frozen at construction
