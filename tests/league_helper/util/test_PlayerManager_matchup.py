"""
Test coverage for T50: matchup_score population from TeamDataManager.

Tests the PlayerManager.refresh_matchup_scores() method, which recomputes
each player's matchup_score from opponent-defense ranks. Covers load-path
population, Optional[int] handling, and reload re-population.
"""

import pytest
import json
from unittest.mock import Mock

from league_helper.util.PlayerManager import PlayerManager
from league_helper.util.TeamDataManager import TeamDataManager
from league_helper.util.ConfigManager import ConfigManager, ConfigKeys
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


@pytest.fixture
def seeded_team_data_manager():
    """Real TeamDataManager (via __new__ + attribute seeding) so the real get_rank_difference runs.

    Non-defense read path: player_team --(season_schedule_manager.get_opponent, current week)-->
    opponent --(position_ranks[opponent][position])--> rank 1-32, or None on a bye (get_opponent -> None).
    """
    tdm = TeamDataManager.__new__(TeamDataManager)
    tdm.logger = Mock()
    tdm.current_nfl_week = 6
    # is_matchup_available() == bool(self.offensive_ranks) -> must be non-empty:
    tdm.offensive_ranks = {"DAL": 5, "PHI": 20, "NYG": 12, "SF": 8}
    # opponent defense-vs-position ranks (the values the assertions read):
    tdm.position_ranks = {
        "DAL": {"RB": 3, "WR": 25, "QB": 12, "TE": 9, "K": 15},
        "PHI": {"RB": 30, "WR": 4, "QB": 22, "TE": 18, "K": 6},
        "NYG": {"RB": 16, "WR": 11, "QB": 28, "TE": 2, "K": 20},
    }
    # seeded for completeness; NOT read on the non-defense path:
    tdm.defensive_ranks = {"DAL": 5, "PHI": 20, "NYG": 12, "SF": 8}
    tdm.dst_fantasy_ranks = {"DAL": 5, "PHI": 20, "NYG": 12, "SF": 8}
    # get_team_opponent(team) -> season_schedule_manager.get_opponent(team, current_nfl_week);
    # assign the Mock BEFORE setting .get_opponent:
    tdm.season_schedule_manager = Mock()
    tdm.season_schedule_manager.get_opponent = Mock(
        side_effect=lambda team, week: {"KC": "DAL", "BUF": "PHI", "LAR": "NYG", "SEA": None}.get(team)
    )
    return tdm


@pytest.fixture
def loaded_pm(tmp_path, seeded_team_data_manager):
    """A PlayerManager pointed at a tmp data dir (one KC/QB player; rb/wr/te/k/dst empty) wired to the
    seeded TeamDataManager. Call pm.load_players_from_json() to load + populate. Mirrors the
    __new__ + attribute-seeding load idiom of tests/league_helper/util/test_PlayerManager_json_loading.py.
    """
    data_folder = tmp_path / "data"
    data_folder.mkdir()
    player_data_dir = data_folder / "player_data"
    player_data_dir.mkdir()
    (player_data_dir / "qb_data.json").write_text(json.dumps({"qb_data": [{
        "id": "1", "name": "KC QB", "team": "KC", "position": "QB",
        "projected_points": [10.0] * 17, "actual_points": [0.0] * 17,
    }]}))
    for pos in ["rb", "wr", "te", "k", "dst"]:
        (player_data_dir / f"{pos}_data.json").write_text(json.dumps({f"{pos}_data": []}))

    pm = PlayerManager.__new__(PlayerManager)
    pm.data_folder = data_folder
    pm.config = Mock(current_nfl_week=6, max_positions={"QB": 2, "RB": 4, "WR": 4, "TE": 1, "K": 1, "DST": 1})
    pm.team_data_manager = seeded_team_data_manager
    pm.season_schedule_manager = seeded_team_data_manager.season_schedule_manager
    pm.players = []
    pm.max_projection = 0.0
    pm.logger = Mock()
    pm.load_team = Mock()
    return pm


class TestRefreshMatchupScoresPopulation:
    def test_populates_real_non_uniform_ranks(self, seeded_team_data_manager):
        pm = PlayerManager.__new__(PlayerManager)
        pm.team_data_manager = seeded_team_data_manager
        pm.players = [_make_player("KC", "RB"), _make_player("BUF", "WR"), _make_player("LAR", "TE")]

        pm.refresh_matchup_scores()

        assert pm.players[0].matchup_score == 3    # KC -> DAL, position_ranks["DAL"]["RB"]
        assert pm.players[1].matchup_score == 4    # BUF -> PHI, position_ranks["PHI"]["WR"]
        assert pm.players[2].matchup_score == 2    # LAR -> NYG, position_ranks["NYG"]["TE"]
        assert all(isinstance(p.matchup_score, int) and 1 <= p.matchup_score <= 32 for p in pm.players)
        assert len({p.matchup_score for p in pm.players}) > 1   # non-uniform

    def test_bye_team_populates_none(self, seeded_team_data_manager):
        pm = PlayerManager.__new__(PlayerManager)
        pm.team_data_manager = seeded_team_data_manager
        pm.players = [_make_player("SEA", "RB")]    # SEA -> get_opponent returns None (bye)

        pm.refresh_matchup_scores()

        assert pm.players[0].matchup_score is None

    def test_load_players_from_json_populates_matchup_scores(self, loaded_pm):
        loaded_pm.load_players_from_json()

        kc_qb = next(p for p in loaded_pm.players if p.team == "KC" and p.position == "QB")
        assert kc_qb.matchup_score == 12    # load path invoked refresh -> KC -> DAL, position_ranks["DAL"]["QB"]


class TestMatchupScoreOptionalNoneNeutral:
    def test_none_matchup_multiplier_is_neutral(self):
        config = ConfigManager.__new__(ConfigManager)
        config.logger = Mock()
        config.keys = ConfigKeys()
        config.matchup_scoring = {ConfigKeys.WEIGHT: 1.0}

        multiplier, label = config.get_matchup_multiplier(None)

        assert multiplier == 1.0                 # NEUTRAL -> zero matchup bonus (T44 preserved via Optional[int])
        assert label == config.keys.NEUTRAL

    def test_widened_field_defaults_none_and_stores_int_verbatim(self, seeded_team_data_manager):
        player = _make_player("KC", "RB")
        assert player.matchup_score is None      # Optional[int] default after the D3 widening

        pm = PlayerManager.__new__(PlayerManager)
        pm.team_data_manager = seeded_team_data_manager
        pm.players = [player]
        pm.refresh_matchup_scores()

        assert isinstance(player.matchup_score, int)   # get_rank_difference's int stored verbatim
        assert player.matchup_score == 3


class TestReloadRepopulatesMatchupScores:
    def test_second_load_repopulates_matchup_score(self, loaded_pm):
        loaded_pm.load_players_from_json()
        kc_qb = next(p for p in loaded_pm.players if p.team == "KC" and p.position == "QB")
        assert kc_qb.matchup_score == 12          # first load populated

        kc_qb.matchup_score = None                # simulate a reset to the unpopulated default

        loaded_pm.load_players_from_json()        # the method reload_player_data() re-invokes (PlayerManager.py:562)
        kc_qb = next(p for p in loaded_pm.players if p.team == "KC" and p.position == "QB")
        assert kc_qb.matchup_score == 12          # re-populated on reload, not reset
