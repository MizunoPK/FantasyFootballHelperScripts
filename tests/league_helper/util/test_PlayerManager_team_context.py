"""
Test coverage for PlayerManager team-context population from TeamDataManager.

Tests the PlayerManager.refresh_team_context() method (D6.1; T50 covered its
matchup-only predecessor), which recomputes each player's team_offensive_rank,
team_defensive_rank and matchup_score from the current TeamDataManager week.
Covers load-path population, the DST rank-source fork, Optional[int] handling,
reload re-population, and the multi-tier team-quality distribution the populate
makes reachable.
"""

import pytest
import json
from unittest.mock import Mock

from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.league_helper.util.PlayerManager import PlayerManager
from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.league_helper.util.TeamDataManager import TeamDataManager
from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.league_helper.util.ConfigManager import ConfigManager, ConfigKeys
from FantasyFootballHelperScriptsWorkspace.FantasyFootballHelperScripts.league_helper.util.player_scoring import PlayerScoringCalculator
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


@pytest.fixture
def seeded_team_data_manager():
    """Real TeamDataManager (via __new__ + attribute seeding) so the real getters run.

    Non-defense read path: player_team --(season_schedule_manager.get_opponent, current week)-->
    opponent --(position_ranks[opponent][position])--> rank 1-32, or None on a bye (get_opponent -> None).

    The three rank dicts are seeded PAIRWISE DIVERGENTLY -- no team carries the same value
    in any two of them -- so a test taking the wrong source fails rather than passing by
    coincidence. On real data the two defensive sources rank a team up to 21 places apart.
    """
    tdm = TeamDataManager.__new__(TeamDataManager)
    tdm.logger = Mock()
    tdm.current_nfl_week = 6
    # is_matchup_available() == bool(self.offensive_ranks) -> must be non-empty. KC/BUF/LAR/
    # SEA/GB (3 / 9 / 15 / 21 / 28) straddle every band of the team-quality ladder seeded in
    # TestTeamQualityTierDistribution below:
    tdm.offensive_ranks = {
        "DAL": 5, "PHI": 20, "NYG": 12, "SF": 8,
        "KC": 3, "BUF": 9, "LAR": 15, "SEA": 21, "GB": 28,
    }
    # opponent defense-vs-position ranks (the values the matchup assertions read):
    tdm.position_ranks = {
        "DAL": {"RB": 3, "WR": 25, "QB": 12, "TE": 9, "K": 15},
        "PHI": {"RB": 30, "WR": 4, "QB": 22, "TE": 18, "K": 6},
        "NYG": {"RB": 16, "WR": 11, "QB": 28, "TE": 2, "K": 20},
    }
    # the player's OWN-team defensive sources, read by refresh_team_context; divergent from
    # offensive_ranks and from each other, per team:
    tdm.defensive_ranks = {
        "DAL": 24, "PHI": 11, "NYG": 29, "SF": 2,
        "KC": 7, "BUF": 14, "LAR": 22, "SEA": 4, "GB": 30,
    }
    tdm.dst_fantasy_ranks = {
        "DAL": 26, "PHI": 2, "NYG": 31, "SF": 19,
        "KC": 17, "BUF": 25, "LAR": 6, "SEA": 11, "GB": 1,
    }
    # get_team_opponent(team) -> season_schedule_manager.get_opponent(team, current_nfl_week);
    # assign the Mock BEFORE setting .get_opponent. MIA is deliberately present HERE and
    # absent from the three rank dicts above -- the per-team None-tolerance case:
    tdm.season_schedule_manager = Mock()
    tdm.season_schedule_manager.get_opponent = Mock(
        side_effect=lambda team, week: {
            "KC": "DAL", "BUF": "PHI", "LAR": "NYG", "SEA": None, "MIA": "DAL",
        }.get(team)
    )
    return tdm


@pytest.fixture
def loaded_pm(tmp_path, seeded_team_data_manager):
    """A PlayerManager pointed at a tmp data dir (one KC/QB and one GB/DST player; rb/wr/te/k
    empty) wired to the seeded TeamDataManager. Call pm.load_players_from_json() to load +
    populate. Mirrors the __new__ + attribute-seeding load idiom of
    tests/league_helper/util/test_PlayerManager_json_loading.py.
    """
    data_folder = tmp_path / "data"
    data_folder.mkdir()
    player_data_dir = data_folder / "player_data"
    player_data_dir.mkdir()
    (player_data_dir / "qb_data.json").write_text(json.dumps({"qb_data": [{
        "id": "1", "name": "KC QB", "team": "KC", "position": "QB",
        "projected_points": [10.0] * 17, "actual_points": [0.0] * 17,
    }]}))
    (player_data_dir / "dst_data.json").write_text(json.dumps({"dst_data": [{
        "id": "2", "name": "GB DST", "team": "GB", "position": "DST",
        "projected_points": [8.0] * 17, "actual_points": [0.0] * 17,
    }]}))
    for pos in ["rb", "wr", "te", "k"]:
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


class TestRefreshTeamContextPopulation:
    def test_populates_real_non_uniform_ranks(self, seeded_team_data_manager):
        pm = PlayerManager.__new__(PlayerManager)
        pm.team_data_manager = seeded_team_data_manager
        pm.players = [_make_player("KC", "RB"), _make_player("BUF", "WR"), _make_player("LAR", "TE")]

        pm.refresh_team_context()

        assert pm.players[0].matchup_score == 3    # KC -> DAL, position_ranks["DAL"]["RB"]
        assert pm.players[1].matchup_score == 4    # BUF -> PHI, position_ranks["PHI"]["WR"]
        assert pm.players[2].matchup_score == 2    # LAR -> NYG, position_ranks["NYG"]["TE"]
        assert all(isinstance(p.matchup_score, int) and 1 <= p.matchup_score <= 32 for p in pm.players)
        assert len({p.matchup_score for p in pm.players}) > 1   # non-uniform

    def test_bye_team_populates_none(self, seeded_team_data_manager):
        pm = PlayerManager.__new__(PlayerManager)
        pm.team_data_manager = seeded_team_data_manager
        pm.players = [_make_player("SEA", "RB")]    # SEA -> get_opponent returns None (bye)

        pm.refresh_team_context()

        assert pm.players[0].matchup_score is None

    def test_load_players_from_json_populates_matchup_scores(self, loaded_pm):
        loaded_pm.load_players_from_json()

        kc_qb = next(p for p in loaded_pm.players if p.team == "KC" and p.position == "QB")
        assert kc_qb.matchup_score == 12    # load path invoked refresh -> KC -> DAL, position_ranks["DAL"]["QB"]


class TestRefreshTeamContextRanks:
    """D6.1: the two team-rank fields the populate newly assigns."""

    def test_non_dst_player_takes_offensive_and_defensive_ranks(self, seeded_team_data_manager):
        pm = PlayerManager.__new__(PlayerManager)
        pm.team_data_manager = seeded_team_data_manager
        pm.players = [_make_player("KC", "RB")]

        pm.refresh_team_context()

        # offensive_ranks["KC"] == 3 and defensive_ranks["KC"] == 7 differ, so a swapped
        # source fails rather than passing by coincidence.
        assert pm.players[0].team_offensive_rank == 3
        assert pm.players[0].team_defensive_rank == 7

    def test_dst_player_takes_dst_fantasy_rank_not_defensive_rank(self, seeded_team_data_manager):
        pm = PlayerManager.__new__(PlayerManager)
        pm.team_data_manager = seeded_team_data_manager
        pm.players = [_make_player("GB", "DST")]

        pm.refresh_team_context()

        # dst_fantasy_ranks["GB"] == 1, defensive_ranks["GB"] == 30: taking the wrong
        # source fails.
        assert pm.players[0].team_defensive_rank == 1
        assert pm.players[0].team_defensive_rank != seeded_team_data_manager.defensive_ranks["GB"]
        assert pm.players[0].team_offensive_rank == 28

    def test_team_absent_from_rank_dicts_yields_none_without_raising(self, seeded_team_data_manager):
        pm = PlayerManager.__new__(PlayerManager)
        pm.team_data_manager = seeded_team_data_manager
        # MIA is in the opponent map but in none of the three rank dicts; KC is in all of
        # them and is the discriminator -- without the populate its rank stays None too,
        # so this test cannot pass by restating the dataclass default.
        pm.players = [_make_player("MIA", "RB"), _make_player("KC", "RB")]

        pm.refresh_team_context()                  # must not raise

        assert pm.players[0].team_offensive_rank is None
        assert pm.players[0].team_defensive_rank is None
        assert pm.players[0].matchup_score == 3    # its other field still populates
        assert pm.players[1].team_offensive_rank == 3   # the populate really ran
        assert pm.players[1].team_defensive_rank == 7

    def test_load_players_from_json_populates_both_rank_fields(self, loaded_pm):
        loaded_pm.load_players_from_json()

        kc_qb = next(p for p in loaded_pm.players if p.team == "KC" and p.position == "QB")
        gb_dst = next(p for p in loaded_pm.players if p.team == "GB" and p.position == "DST")

        assert kc_qb.team_offensive_rank == 3      # non-DST branch
        assert kc_qb.team_defensive_rank == 7
        assert gb_dst.team_offensive_rank == 28    # DST branch
        assert gb_dst.team_defensive_rank == 1


class TestTeamQualityTierDistribution:
    """D6.1 (U3 half 2): the durable exact-set regression guard.

    Population: the seeded fixture pool below -- deliberately NOT the
    simulation/sim_data/2024 pool of the build-time capture, and no number is compared
    across the two.
    """

    def test_populated_ranks_produce_all_five_tiers(self, seeded_team_data_manager):
        config = ConfigManager.__new__(ConfigManager)
        config.logger = Mock()
        config.keys = ConfigKeys()
        # Seeded here rather than read from data/configs/, so the assertion stays valid when
        # the live config is retuned. The values happen to coincide with today's expanded live
        # ladder (BASE_POSITION 0 / DECREASING / STEPS 6 -> 6/12/18/24). DECREASING: a lower
        # rank is better.
        config.team_quality_scoring = {
            ConfigKeys.THRESHOLDS: {
                ConfigKeys.EXCELLENT: 6, ConfigKeys.GOOD: 12,
                ConfigKeys.POOR: 18, ConfigKeys.VERY_POOR: 24,
            },
            ConfigKeys.MULTIPLIERS: {
                ConfigKeys.EXCELLENT: 1.05, ConfigKeys.GOOD: 1.025,
                ConfigKeys.POOR: 0.975, ConfigKeys.VERY_POOR: 0.95,
            },
            ConfigKeys.WEIGHT: 1.0,
        }

        pm = PlayerManager.__new__(PlayerManager)
        pm.team_data_manager = seeded_team_data_manager
        pm.players = [_make_player(t, "RB") for t in ("KC", "BUF", "LAR", "SEA", "GB")]
        # One DST player, so the CONSUMER side of the Constants.DEFENSE_POSITIONS fork in
        # PlayerScoringCalculator._apply_team_quality_multiplier is exercised alongside the
        # PRODUCER side in refresh_team_context.
        pm.players.append(_make_player("GB", "DST", name="GB DST"))

        pm.refresh_team_context()

        # Derive each label through the real scoring step 4 rather than calling the config
        # directly: a mutation swapping the two rank reads inside _apply_team_quality_multiplier
        # would leave a direct-config assertion green. Only .config is read by that method.
        calc = PlayerScoringCalculator.__new__(PlayerScoringCalculator)
        calc.config = config

        def _tier(player):
            _, reason = calc._apply_team_quality_multiplier(player, 100.0)
            return reason.split(":")[1].split("(")[0].strip()

        labels = {_tier(p) for p in pm.players}

        assert labels == {"EXCELLENT", "GOOD", "NEUTRAL", "POOR", "VERY_POOR"}
        assert labels != {"NEUTRAL"}    # the pre-D6.1 end state, stated explicitly
        # The DST player's tier must come from dst_fantasy_ranks["GB"] == 1 (EXCELLENT), never
        # from offensive_ranks["GB"] == 28 (VERY_POOR). The set assertion above cannot catch a
        # swapped read here -- both labels are already members -- so assert the fork directly.
        assert _tier(pm.players[-1]) == "EXCELLENT"


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
        pm.refresh_team_context()

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
