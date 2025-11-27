"""
Integration Tests for Game Conditions Scoring

Tests the complete integration of game conditions (temperature, wind, location)
scoring across the league helper and simulation systems.

Author: Kai Mizuno
"""

import pytest
from pathlib import Path
import sys
import json
import tempfile
import shutil

sys.path.append(str(Path(__file__).parent.parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent / "league_helper"))
sys.path.append(str(Path(__file__).parent.parent.parent / "league_helper" / "util"))

from league_helper.util.ConfigManager import ConfigManager
from league_helper.util.PlayerManager import PlayerManager
from league_helper.util.TeamDataManager import TeamDataManager
from league_helper.util.SeasonScheduleManager import SeasonScheduleManager
from league_helper.util.GameDataManager import GameDataManager
from league_helper.util.player_scoring import PlayerScoringCalculator
from league_helper.starter_helper_mode.StarterHelperModeManager import StarterHelperModeManager
from utils.FantasyPlayer import FantasyPlayer


def get_player_by_name(player_manager, name: str):
    """Helper function to get player by name from PlayerManager."""
    for player in player_manager.players:
        if player.name == name:
            return player
    return None


class TestGameConditionsLeagueHelperIntegration:
    """Integration tests for game conditions in League Helper."""

    @pytest.fixture
    def integration_data_folder(self, tmp_path):
        """Create a complete data folder for integration testing."""
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        # Create league_config.json with game conditions scoring
        config = {
            "config_name": "Integration Test Config",
            "description": "Config for game conditions integration tests",
            "parameters": {
                "CURRENT_NFL_WEEK": 6,
                "NFL_SEASON": 2025,
                "NFL_SCORING_FORMAT": "ppr",
                "NORMALIZATION_MAX_SCALE": 100.0,
                "SAME_POS_BYE_WEIGHT": 1.0,
                "DIFF_POS_BYE_WEIGHT": 1.0,
                "INJURY_PENALTIES": {"LOW": 0, "MEDIUM": 10.0, "HIGH": 75.0},
                "DRAFT_ORDER_BONUSES": {"PRIMARY": 50, "SECONDARY": 30},
                "DRAFT_ORDER": [],
                "MAX_POSITIONS": {"QB": 2, "RB": 4, "WR": 4, "TE": 2, "K": 1, "DST": 1, "FLEX": 1},
                "FLEX_ELIGIBLE_POSITIONS": ["RB", "WR", "TE"],
                "ADP_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 37.5}
                },
                "PLAYER_RATING_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 20.0}
                },
                "TEAM_QUALITY_SCORING": {
                    "MIN_WEEKS": 5,
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 6.25}
                },
                "PERFORMANCE_SCORING": {
                    "MIN_WEEKS": 5,
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "BI_EXCELLENT_HI", "STEPS": 0.1}
                },
                "MATCHUP_SCORING": {
                    "MIN_WEEKS": 5,
                    "WEIGHT": 1.0,
                    "IMPACT_SCALE": 50.0,
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 6.25}
                },
                "SCHEDULE_SCORING": {
                    "WEIGHT": 1.0,
                    "IMPACT_SCALE": 50.0,
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 6.25}
                },
                "TEMPERATURE_SCORING": {
                    "IDEAL_TEMPERATURE": 60,
                    "IMPACT_SCALE": 50.0,
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 10},
                    "MULTIPLIERS": {"VERY_POOR": 0.95, "POOR": 0.975, "GOOD": 1.025, "EXCELLENT": 1.05},
                    "WEIGHT": 1.0
                },
                "WIND_SCORING": {
                    "IMPACT_SCALE": 60.0,
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 8},
                    "MULTIPLIERS": {"VERY_POOR": 0.95, "POOR": 0.975, "GOOD": 1.025, "EXCELLENT": 1.05},
                    "WEIGHT": 1.0
                },
                "LOCATION_MODIFIERS": {
                    "HOME": 2.0,
                    "AWAY": -2.0,
                    "INTERNATIONAL": -5.0
                }
            }
        }
        with open(data_folder / "league_config.json", "w") as f:
            json.dump(config, f)

        # Create players.csv with test players
        players_csv = """id,name,team,position,bye_week,fantasy_points,injury_status,drafted,locked,average_draft_position,player_rating,week_1_points,week_2_points,week_3_points,week_4_points,week_5_points,week_6_points,week_7_points,week_8_points,week_9_points,week_10_points,week_11_points,week_12_points,week_13_points,week_14_points,week_15_points,week_16_points,week_17_points
1,Patrick Mahomes,KC,QB,10,350.0,ACTIVE,0,0,5.0,95.0,25.0,22.0,28.0,20.0,24.0,26.0,23.0,25.0,27.0,24.0,22.0,26.0,25.0,24.0,23.0,25.0,24.0
2,Josh Allen,BUF,QB,12,340.0,ACTIVE,0,0,8.0,93.0,24.0,26.0,22.0,25.0,23.0,27.0,24.0,22.0,25.0,26.0,23.0,24.0,25.0,23.0,24.0,22.0,25.0
3,Jahmyr Gibbs,DET,RB,8,280.0,ACTIVE,0,0,6.0,90.0,18.0,20.0,22.0,16.0,19.0,21.0,20.0,18.0,17.0,22.0,19.0,20.0,18.0,19.0,20.0,21.0,18.0
4,CeeDee Lamb,DAL,WR,7,300.0,ACTIVE,0,0,10.0,92.0,20.0,18.0,22.0,19.0,21.0,17.0,20.0,22.0,19.0,18.0,21.0,20.0,19.0,20.0,21.0,18.0,20.0
5,Justin Tucker,BAL,K,14,150.0,ACTIVE,0,0,120.0,85.0,10.0,8.0,12.0,9.0,11.0,10.0,9.0,11.0,10.0,8.0,12.0,9.0,10.0,11.0,9.0,10.0,11.0
"""
        with open(data_folder / "players.csv", "w") as f:
            f.write(players_csv)

        # Create players_projected.csv (same structure for simplicity)
        with open(data_folder / "players_projected.csv", "w") as f:
            f.write(players_csv)

        # Create game_data.csv with various conditions
        game_data_csv = """week,home_team,away_team,temperature,gust,indoor,neutral_site,country
6,KC,BUF,60,5,False,False,USA
6,DET,DAL,,5,True,False,USA
6,BAL,CIN,40,25,False,False,USA
6,JAX,ATL,55,10,False,True,UK
"""
        with open(data_folder / "game_data.csv", "w") as f:
            f.write(game_data_csv)

        # Create team_data folder with minimal team files
        team_data_folder = data_folder / "team_data"
        team_data_folder.mkdir()
        for team in ["KC", "BUF", "DET", "DAL", "BAL", "CIN", "JAX", "ATL"]:
            team_csv = f"""week,off_rank,def_rank_qb,def_rank_rb,def_rank_wr,def_rank_te,def_rank_k,def_rank_dst
1,16.0,16.0,16.0,16.0,16.0,16.0,16.0
2,16.0,16.0,16.0,16.0,16.0,16.0,16.0
3,16.0,16.0,16.0,16.0,16.0,16.0,16.0
4,16.0,16.0,16.0,16.0,16.0,16.0,16.0
5,16.0,16.0,16.0,16.0,16.0,16.0,16.0
6,16.0,16.0,16.0,16.0,16.0,16.0,16.0
"""
            with open(team_data_folder / f"{team}.csv", "w") as f:
                f.write(team_csv)

        return data_folder

    def test_game_data_manager_loads_correctly(self, integration_data_folder):
        """Test that GameDataManager loads game_data.csv correctly."""
        manager = GameDataManager(integration_data_folder, current_week=6)

        assert manager.has_game_data() is True

        # Test KC home game
        kc_game = manager.get_game("KC")
        assert kc_game is not None
        assert kc_game.home_team == "KC"
        assert kc_game.away_team == "BUF"
        assert kc_game.temperature == 60
        assert kc_game.wind_gust == 5
        assert kc_game.indoor is False

        # Test DET indoor game
        det_game = manager.get_game("DET")
        assert det_game is not None
        assert det_game.indoor is True
        assert det_game.temperature is None

        # Test BAL cold/windy game
        bal_game = manager.get_game("BAL")
        assert bal_game is not None
        assert bal_game.temperature == 40
        assert bal_game.wind_gust == 25

        # Test JAX international game
        jax_game = manager.get_game("JAX")
        assert jax_game is not None
        assert jax_game.neutral_site is True
        assert jax_game.country == "UK"
        assert jax_game.is_international() is True

    def test_player_manager_creates_game_data_manager(self, integration_data_folder):
        """Test that PlayerManager creates GameDataManager internally."""
        config = ConfigManager(integration_data_folder)
        team_data_manager = TeamDataManager(integration_data_folder, config)
        season_schedule_manager = SeasonScheduleManager(integration_data_folder)

        player_manager = PlayerManager(
            integration_data_folder, config, team_data_manager, season_schedule_manager
        )

        # Verify GameDataManager was created
        assert player_manager.game_data_manager is not None
        assert player_manager.game_data_manager.has_game_data() is True

    def test_scoring_with_temperature_bonus(self, integration_data_folder):
        """Test that temperature scoring applies correctly."""
        config = ConfigManager(integration_data_folder)
        team_data_manager = TeamDataManager(integration_data_folder, config)
        season_schedule_manager = SeasonScheduleManager(integration_data_folder)
        player_manager = PlayerManager(
            integration_data_folder, config, team_data_manager, season_schedule_manager
        )

        # Get Mahomes (KC - ideal temp 60°F)
        mahomes = get_player_by_name(player_manager, "Patrick Mahomes")
        assert mahomes is not None

        # Score with temperature enabled vs disabled
        score_with_temp = player_manager.score_player(
            mahomes, [], temperature=True, wind=False, location=False,
            adp=False, player_rating=False, team_quality=False,
            performance=False, matchup=False, schedule=False, bye=False, injury=False
        )

        score_without_temp = player_manager.score_player(
            mahomes, [], temperature=False, wind=False, location=False,
            adp=False, player_rating=False, team_quality=False,
            performance=False, matchup=False, schedule=False, bye=False, injury=False
        )

        # At ideal temp, should get bonus
        assert score_with_temp.score > score_without_temp.score
        # Check reason includes temperature
        reason_str = " ".join(score_with_temp.reason)
        assert "Temp" in reason_str or "60" in reason_str

    def test_scoring_with_wind_penalty_qb(self, integration_data_folder):
        """Test that wind scoring applies to QB."""
        config = ConfigManager(integration_data_folder)
        team_data_manager = TeamDataManager(integration_data_folder, config)
        season_schedule_manager = SeasonScheduleManager(integration_data_folder)
        player_manager = PlayerManager(
            integration_data_folder, config, team_data_manager, season_schedule_manager
        )

        # Get Tucker (BAL - high wind 25mph)
        tucker = get_player_by_name(player_manager, "Justin Tucker")
        assert tucker is not None
        assert tucker.position == "K"

        # Score with wind enabled vs disabled
        score_with_wind = player_manager.score_player(
            tucker, [], temperature=False, wind=True, location=False,
            adp=False, player_rating=False, team_quality=False,
            performance=False, matchup=False, schedule=False, bye=False, injury=False
        )

        score_without_wind = player_manager.score_player(
            tucker, [], temperature=False, wind=False, location=False,
            adp=False, player_rating=False, team_quality=False,
            performance=False, matchup=False, schedule=False, bye=False, injury=False
        )

        # High wind should cause penalty for kicker
        assert score_with_wind.score < score_without_wind.score
        # Check reason includes wind
        reason_str = " ".join(score_with_wind.reason)
        assert "Wind" in reason_str

    def test_scoring_wind_does_not_affect_rb(self, integration_data_folder):
        """Test that wind scoring does NOT affect RB."""
        config = ConfigManager(integration_data_folder)
        team_data_manager = TeamDataManager(integration_data_folder, config)
        season_schedule_manager = SeasonScheduleManager(integration_data_folder)
        player_manager = PlayerManager(
            integration_data_folder, config, team_data_manager, season_schedule_manager
        )

        # Get Gibbs (DET - indoor, but let's test wind flag)
        gibbs = get_player_by_name(player_manager, "Jahmyr Gibbs")
        assert gibbs is not None
        assert gibbs.position == "RB"

        # Score with wind enabled vs disabled
        score_with_wind = player_manager.score_player(
            gibbs, [], temperature=False, wind=True, location=False,
            adp=False, player_rating=False, team_quality=False,
            performance=False, matchup=False, schedule=False, bye=False, injury=False
        )

        score_without_wind = player_manager.score_player(
            gibbs, [], temperature=False, wind=False, location=False,
            adp=False, player_rating=False, team_quality=False,
            performance=False, matchup=False, schedule=False, bye=False, injury=False
        )

        # RB should not be affected by wind
        assert score_with_wind.score == score_without_wind.score

    def test_scoring_with_home_location_bonus(self, integration_data_folder):
        """Test that home location bonus applies correctly."""
        config = ConfigManager(integration_data_folder)
        team_data_manager = TeamDataManager(integration_data_folder, config)
        season_schedule_manager = SeasonScheduleManager(integration_data_folder)
        player_manager = PlayerManager(
            integration_data_folder, config, team_data_manager, season_schedule_manager
        )

        # Get Mahomes (KC - home game)
        mahomes = get_player_by_name(player_manager, "Patrick Mahomes")

        # Score with location enabled vs disabled
        score_with_loc = player_manager.score_player(
            mahomes, [], temperature=False, wind=False, location=True,
            adp=False, player_rating=False, team_quality=False,
            performance=False, matchup=False, schedule=False, bye=False, injury=False
        )

        score_without_loc = player_manager.score_player(
            mahomes, [], temperature=False, wind=False, location=False,
            adp=False, player_rating=False, team_quality=False,
            performance=False, matchup=False, schedule=False, bye=False, injury=False
        )

        # Home game should get +2.0 bonus
        assert score_with_loc.score == score_without_loc.score + 2.0
        reason_str = " ".join(score_with_loc.reason)
        assert "Home" in reason_str

    def test_scoring_with_away_location_penalty(self, integration_data_folder):
        """Test that away location penalty applies correctly."""
        config = ConfigManager(integration_data_folder)
        team_data_manager = TeamDataManager(integration_data_folder, config)
        season_schedule_manager = SeasonScheduleManager(integration_data_folder)
        player_manager = PlayerManager(
            integration_data_folder, config, team_data_manager, season_schedule_manager
        )

        # Get Josh Allen (BUF - away at KC)
        allen = get_player_by_name(player_manager, "Josh Allen")

        # Score with location enabled vs disabled
        score_with_loc = player_manager.score_player(
            allen, [], temperature=False, wind=False, location=True,
            adp=False, player_rating=False, team_quality=False,
            performance=False, matchup=False, schedule=False, bye=False, injury=False
        )

        score_without_loc = player_manager.score_player(
            allen, [], temperature=False, wind=False, location=False,
            adp=False, player_rating=False, team_quality=False,
            performance=False, matchup=False, schedule=False, bye=False, injury=False
        )

        # Away game should get -2.0 penalty
        assert score_with_loc.score == score_without_loc.score - 2.0
        reason_str = " ".join(score_with_loc.reason)
        assert "Away" in reason_str

    def test_scoring_indoor_no_weather_effects(self, integration_data_folder):
        """Test that indoor games have no weather effects."""
        config = ConfigManager(integration_data_folder)
        team_data_manager = TeamDataManager(integration_data_folder, config)
        season_schedule_manager = SeasonScheduleManager(integration_data_folder)
        player_manager = PlayerManager(
            integration_data_folder, config, team_data_manager, season_schedule_manager
        )

        # Get Gibbs (DET - indoor)
        gibbs = get_player_by_name(player_manager, "Jahmyr Gibbs")

        # Score with all weather enabled vs disabled
        score_with_weather = player_manager.score_player(
            gibbs, [], temperature=True, wind=True, location=False,
            adp=False, player_rating=False, team_quality=False,
            performance=False, matchup=False, schedule=False, bye=False, injury=False
        )

        score_without_weather = player_manager.score_player(
            gibbs, [], temperature=False, wind=False, location=False,
            adp=False, player_rating=False, team_quality=False,
            performance=False, matchup=False, schedule=False, bye=False, injury=False
        )

        # Indoor game should have no weather effects
        assert score_with_weather.score == score_without_weather.score

    def test_all_game_conditions_combined(self, integration_data_folder):
        """Test scoring with all game conditions enabled."""
        config = ConfigManager(integration_data_folder)
        team_data_manager = TeamDataManager(integration_data_folder, config)
        season_schedule_manager = SeasonScheduleManager(integration_data_folder)
        player_manager = PlayerManager(
            integration_data_folder, config, team_data_manager, season_schedule_manager
        )

        # Get Mahomes (KC - ideal temp, low wind, home)
        mahomes = get_player_by_name(player_manager, "Patrick Mahomes")

        # Score with all conditions enabled
        score_all = player_manager.score_player(
            mahomes, [], temperature=True, wind=True, location=True,
            adp=False, player_rating=False, team_quality=False,
            performance=False, matchup=False, schedule=False, bye=False, injury=False
        )

        # Score with no conditions
        score_none = player_manager.score_player(
            mahomes, [], temperature=False, wind=False, location=False,
            adp=False, player_rating=False, team_quality=False,
            performance=False, matchup=False, schedule=False, bye=False, injury=False
        )

        # All conditions favorable: temp bonus + wind bonus + home bonus
        # Should be significantly higher
        assert score_all.score > score_none.score

        # Check reasons include all game conditions
        reason_str = " ".join(score_all.reason)
        assert "Temp" in reason_str or "60" in reason_str
        assert "Wind" in reason_str
        assert "Home" in reason_str


class TestGameConditionsSimulationIntegration:
    """Integration tests for game conditions in Simulation."""

    @pytest.fixture
    def simulation_data_folder(self, tmp_path):
        """Create simulation data folder structure."""
        sim_data = tmp_path / "sim_data"
        sim_data.mkdir()

        # Copy the same config structure
        config = {
            "config_name": "Simulation Test Config",
            "description": "Config for simulation integration tests",
            "parameters": {
                "CURRENT_NFL_WEEK": 1,
                "NFL_SEASON": 2025,
                "NFL_SCORING_FORMAT": "ppr",
                "NORMALIZATION_MAX_SCALE": 100.0,
                "SAME_POS_BYE_WEIGHT": 1.0,
                "DIFF_POS_BYE_WEIGHT": 1.0,
                "INJURY_PENALTIES": {"LOW": 0, "MEDIUM": 10.0, "HIGH": 75.0},
                "DRAFT_ORDER_BONUSES": {"PRIMARY": 50, "SECONDARY": 30},
                "DRAFT_ORDER": [],
                "MAX_POSITIONS": {"QB": 2, "RB": 4, "WR": 4, "TE": 2, "K": 1, "DST": 1, "FLEX": 1},
                "FLEX_ELIGIBLE_POSITIONS": ["RB", "WR", "TE"],
                "ADP_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 37.5}
                },
                "PLAYER_RATING_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 20.0}
                },
                "TEAM_QUALITY_SCORING": {
                    "MIN_WEEKS": 5,
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 6.25}
                },
                "PERFORMANCE_SCORING": {
                    "MIN_WEEKS": 5,
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "BI_EXCELLENT_HI", "STEPS": 0.1}
                },
                "MATCHUP_SCORING": {
                    "MIN_WEEKS": 5,
                    "WEIGHT": 1.0,
                    "IMPACT_SCALE": 50.0,
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 6.25}
                },
                "SCHEDULE_SCORING": {
                    "WEIGHT": 1.0,
                    "IMPACT_SCALE": 50.0,
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 6.25}
                },
                "TEMPERATURE_SCORING": {
                    "IDEAL_TEMPERATURE": 60,
                    "IMPACT_SCALE": 50.0,
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 10},
                    "MULTIPLIERS": {"VERY_POOR": 0.95, "POOR": 0.975, "GOOD": 1.025, "EXCELLENT": 1.05},
                    "WEIGHT": 1.0
                },
                "WIND_SCORING": {
                    "IMPACT_SCALE": 60.0,
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 8},
                    "MULTIPLIERS": {"VERY_POOR": 0.95, "POOR": 0.975, "GOOD": 1.025, "EXCELLENT": 1.05},
                    "WEIGHT": 1.0
                },
                "LOCATION_MODIFIERS": {
                    "HOME": 2.0,
                    "AWAY": -2.0,
                    "INTERNATIONAL": -5.0
                }
            }
        }
        with open(sim_data / "league_config.json", "w") as f:
            json.dump(config, f)

        # Create game_data.csv with multi-week data
        game_data_csv = """week,home_team,away_team,temperature,gust,indoor,neutral_site,country
1,KC,BUF,65,8,False,False,USA
1,DET,DAL,,5,True,False,USA
2,BUF,KC,55,15,False,False,USA
2,DAL,DET,,3,True,False,USA
3,KC,DET,60,5,False,False,USA
3,BUF,DAL,50,20,False,False,USA
"""
        with open(sim_data / "game_data.csv", "w") as f:
            f.write(game_data_csv)

        return sim_data

    def test_game_data_manager_multiweek_lookup(self, simulation_data_folder):
        """Test GameDataManager can lookup games across different weeks."""
        manager = GameDataManager(simulation_data_folder, current_week=1)

        # Week 1: KC home vs BUF
        week1_kc = manager.get_game("KC", week=1)
        assert week1_kc is not None
        assert week1_kc.away_team == "BUF"
        assert week1_kc.is_home_game("KC") is True

        # Week 2: KC away at BUF
        week2_kc = manager.get_game("KC", week=2)
        assert week2_kc is not None
        assert week2_kc.home_team == "BUF"
        assert week2_kc.is_home_game("KC") is False

        # Week 3: KC home vs DET
        week3_kc = manager.get_game("KC", week=3)
        assert week3_kc is not None
        assert week3_kc.away_team == "DET"

    def test_game_data_manager_set_current_week(self, simulation_data_folder):
        """Test GameDataManager.set_current_week updates correctly."""
        manager = GameDataManager(simulation_data_folder, current_week=1)

        # Week 1 default lookup
        game = manager.get_game("KC")
        assert game.away_team == "BUF"

        # Change to week 2
        manager.set_current_week(2)
        game = manager.get_game("KC")
        assert game.home_team == "BUF"  # KC is away in week 2

        # Change to week 3
        manager.set_current_week(3)
        game = manager.get_game("KC")
        assert game.away_team == "DET"


class TestConfigManagerGameConditions:
    """Integration tests for ConfigManager game conditions methods."""

    @pytest.fixture
    def config_with_game_conditions(self, tmp_path):
        """Create ConfigManager with game conditions config."""
        data_folder = tmp_path / "data"
        data_folder.mkdir()

        config = {
            "config_name": "Test",
            "description": "Test config",
            "parameters": {
                "CURRENT_NFL_WEEK": 6,
                "NFL_SEASON": 2025,
                "NFL_SCORING_FORMAT": "ppr",
                "NORMALIZATION_MAX_SCALE": 100.0,
                "SAME_POS_BYE_WEIGHT": 1.0,
                "DIFF_POS_BYE_WEIGHT": 1.0,
                "INJURY_PENALTIES": {"LOW": 0, "MEDIUM": 10.0, "HIGH": 75.0},
                "DRAFT_ORDER_BONUSES": {"PRIMARY": 50, "SECONDARY": 30},
                "DRAFT_ORDER": [],
                "MAX_POSITIONS": {"QB": 2, "RB": 4, "WR": 4, "TE": 2, "K": 1, "DST": 1, "FLEX": 1},
                "FLEX_ELIGIBLE_POSITIONS": ["RB", "WR", "TE"],
                "ADP_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 37.5}
                },
                "PLAYER_RATING_SCORING": {
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "INCREASING", "STEPS": 20.0}
                },
                "TEAM_QUALITY_SCORING": {
                    "MIN_WEEKS": 5,
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 6.25}
                },
                "PERFORMANCE_SCORING": {
                    "MIN_WEEKS": 5,
                    "WEIGHT": 1.0,
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "BI_EXCELLENT_HI", "STEPS": 0.1}
                },
                "MATCHUP_SCORING": {
                    "MIN_WEEKS": 5,
                    "WEIGHT": 1.0,
                    "IMPACT_SCALE": 50.0,
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 6.25}
                },
                "SCHEDULE_SCORING": {
                    "WEIGHT": 1.0,
                    "IMPACT_SCALE": 50.0,
                    "MULTIPLIERS": {"EXCELLENT": 1.05, "GOOD": 1.025, "POOR": 0.975, "VERY_POOR": 0.95},
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 6.25}
                },
                "TEMPERATURE_SCORING": {
                    "IDEAL_TEMPERATURE": 60,
                    "IMPACT_SCALE": 50.0,
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 10},
                    "MULTIPLIERS": {"VERY_POOR": 0.95, "POOR": 0.975, "GOOD": 1.025, "EXCELLENT": 1.05},
                    "WEIGHT": 1.0
                },
                "WIND_SCORING": {
                    "IMPACT_SCALE": 60.0,
                    "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 8},
                    "MULTIPLIERS": {"VERY_POOR": 0.95, "POOR": 0.975, "GOOD": 1.025, "EXCELLENT": 1.05},
                    "WEIGHT": 1.0
                },
                "LOCATION_MODIFIERS": {
                    "HOME": 2.0,
                    "AWAY": -2.0,
                    "INTERNATIONAL": -5.0
                }
            }
        }
        with open(data_folder / "league_config.json", "w") as f:
            json.dump(config, f)

        # Create empty players files
        players_csv = "id,name,team,position,bye_week,fantasy_points,injury_status,drafted,locked,average_draft_position,player_rating\n"
        with open(data_folder / "players.csv", "w") as f:
            f.write(players_csv)
        with open(data_folder / "players_projected.csv", "w") as f:
            f.write(players_csv)

        return ConfigManager(data_folder)

    def test_get_temperature_distance(self, config_with_game_conditions):
        """Test ConfigManager.get_temperature_distance calculation."""
        config = config_with_game_conditions

        # Ideal temperature = 60
        assert config.get_temperature_distance(60) == 0
        assert config.get_temperature_distance(70) == 10
        assert config.get_temperature_distance(50) == 10
        assert config.get_temperature_distance(100) == 40
        assert config.get_temperature_distance(20) == 40

    def test_get_temperature_multiplier(self, config_with_game_conditions):
        """Test ConfigManager.get_temperature_multiplier calculation."""
        config = config_with_game_conditions

        # DECREASING thresholds with BASE=0, STEPS=10:
        # EXCELLENT <= 10, GOOD <= 20, POOR >= 30, VERY_POOR >= 40

        # Distance 0 = EXCELLENT (0 <= 10)
        mult, tier = config.get_temperature_multiplier(0)
        assert tier == "EXCELLENT"
        assert mult == 1.05

        # Distance 5 = EXCELLENT (5 <= 10)
        mult, tier = config.get_temperature_multiplier(5)
        assert tier == "EXCELLENT"
        assert mult == 1.05

        # Distance 15 = GOOD (10 < 15 <= 20)
        mult, tier = config.get_temperature_multiplier(15)
        assert tier == "GOOD"
        assert mult == 1.025

        # Distance 25 = NEUTRAL (20 < 25 < 30)
        mult, tier = config.get_temperature_multiplier(25)
        assert tier == "NEUTRAL"
        assert mult == 1.0

        # Distance 35 = POOR (30 <= 35 < 40)
        mult, tier = config.get_temperature_multiplier(35)
        assert tier == "POOR"
        assert mult == 0.975

        # Distance 40 = VERY_POOR (40 >= 40)
        mult, tier = config.get_temperature_multiplier(40)
        assert tier == "VERY_POOR"
        assert mult == 0.95

    def test_get_wind_multiplier(self, config_with_game_conditions):
        """Test ConfigManager.get_wind_multiplier calculation."""
        config = config_with_game_conditions

        # DECREASING thresholds with BASE=0, STEPS=8:
        # EXCELLENT <= 8, GOOD <= 16, POOR >= 24, VERY_POOR >= 32

        # Wind 0 = EXCELLENT (0 <= 8)
        mult, tier = config.get_wind_multiplier(0)
        assert tier == "EXCELLENT"
        assert mult == 1.05

        # Wind 5 = EXCELLENT (5 <= 8)
        mult, tier = config.get_wind_multiplier(5)
        assert tier == "EXCELLENT"
        assert mult == 1.05

        # Wind 12 = GOOD (8 < 12 <= 16)
        mult, tier = config.get_wind_multiplier(12)
        assert tier == "GOOD"
        assert mult == 1.025

        # Wind 20 = NEUTRAL (16 < 20 < 24)
        mult, tier = config.get_wind_multiplier(20)
        assert tier == "NEUTRAL"
        assert mult == 1.0

        # Wind 28 = POOR (24 <= 28 < 32)
        mult, tier = config.get_wind_multiplier(28)
        assert tier == "POOR"
        assert mult == 0.975

        # Wind 35 = VERY_POOR (35 >= 32)
        mult, tier = config.get_wind_multiplier(35)
        assert tier == "VERY_POOR"
        assert mult == 0.95

    def test_get_location_modifier(self, config_with_game_conditions):
        """Test ConfigManager.get_location_modifier calculation."""
        config = config_with_game_conditions

        # Home game
        assert config.get_location_modifier(is_home=True, is_international=False) == 2.0

        # Away game
        assert config.get_location_modifier(is_home=False, is_international=False) == -2.0

        # International game (overrides home/away)
        assert config.get_location_modifier(is_home=True, is_international=True) == -5.0
        assert config.get_location_modifier(is_home=False, is_international=True) == -5.0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
