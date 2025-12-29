"""
Unit Tests for Game Conditions Scoring (Steps 11-13)

Tests the temperature, wind, and location scoring adjustments added to
PlayerScoringCalculator:
- Step 11: Temperature scoring (all positions)
- Step 12: Wind scoring (QB, WR, K only)
- Step 13: Location scoring (home/away/international)

Author: Kai Mizuno
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path
import tempfile
import json

import sys
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
sys.path.append(str(Path(__file__).parent.parent.parent.parent / "league_helper"))
sys.path.append(str(Path(__file__).parent.parent.parent.parent / "league_helper" / "util"))

from util.player_scoring import PlayerScoringCalculator
from util.ConfigManager import ConfigManager
from util.ProjectedPointsManager import ProjectedPointsManager
from util.TeamDataManager import TeamDataManager
from util.SeasonScheduleManager import SeasonScheduleManager
from util.GameDataManager import GameDataManager
from util.upcoming_game_model import UpcomingGame
from utils.FantasyPlayer import FantasyPlayer


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def mock_config():
    """Create mock ConfigManager with game conditions scoring."""
    config = Mock()

    # Basic attributes
    config.current_nfl_week = 6
    config.normalization_max_scale = 100.0

    # Temperature scoring config
    config.temperature_scoring = {
        "IDEAL_TEMPERATURE": 60,
        "IMPACT_SCALE": 50.0,
        "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 10},
        "MULTIPLIERS": {"VERY_POOR": 0.95, "POOR": 0.975, "GOOD": 1.025, "EXCELLENT": 1.05},
        "WEIGHT": 1.0
    }

    # Wind scoring config
    config.wind_scoring = {
        "IMPACT_SCALE": 60.0,
        "THRESHOLDS": {"BASE_POSITION": 0, "DIRECTION": "DECREASING", "STEPS": 8},
        "MULTIPLIERS": {"VERY_POOR": 0.95, "POOR": 0.975, "GOOD": 1.025, "EXCELLENT": 1.05},
        "WEIGHT": 1.0
    }

    # Location modifiers config
    config.location_modifiers = {
        "HOME": 2.0,
        "AWAY": -2.0,
        "INTERNATIONAL": -5.0
    }

    # Mock ConfigKeys
    config.keys = Mock()
    config.keys.IDEAL_TEMPERATURE = "IDEAL_TEMPERATURE"
    config.keys.IMPACT_SCALE = "IMPACT_SCALE"
    config.keys.LOCATION_HOME = "HOME"
    config.keys.LOCATION_AWAY = "AWAY"
    config.keys.LOCATION_INTERNATIONAL = "INTERNATIONAL"

    # Mock methods
    def get_temperature_distance(temp):
        ideal = 60
        return abs(temp - ideal)

    def get_temperature_multiplier(temp_distance):
        # DECREASING: low distance = EXCELLENT, high distance = VERY_POOR
        if temp_distance <= 10:
            return 1.05, "EXCELLENT"
        elif temp_distance <= 20:
            return 1.025, "GOOD"
        elif temp_distance <= 30:
            return 0.975, "POOR"
        else:
            return 0.95, "VERY_POOR"

    def get_wind_multiplier(wind_gust):
        # DECREASING: low wind = EXCELLENT, high wind = VERY_POOR
        if wind_gust <= 8:
            return 1.05, "EXCELLENT"
        elif wind_gust <= 16:
            return 1.025, "GOOD"
        elif wind_gust <= 24:
            return 0.975, "POOR"
        else:
            return 0.95, "VERY_POOR"

    def get_location_modifier(is_home, is_international):
        if is_international:
            return -5.0
        elif is_home:
            return 2.0
        else:
            return -2.0

    config.get_temperature_distance = get_temperature_distance
    config.get_temperature_multiplier = get_temperature_multiplier
    config.get_wind_multiplier = get_wind_multiplier
    config.get_location_modifier = get_location_modifier

    # Additional methods needed for score_player integration tests
    config.get_player_rating_multiplier = Mock(return_value=(1.0, 50))
    config.get_adp_multiplier = Mock(return_value=(1.0, 50))
    config.get_team_quality_multiplier = Mock(return_value=(1.0, "GOOD"))
    config.get_performance_multiplier = Mock(return_value=(1.0, "GOOD"))
    config.get_matchup_multiplier = Mock(return_value=(1.0, "GOOD"))
    config.get_schedule_multiplier = Mock(return_value=(1.0, "GOOD"))
    config.get_draft_order_bonus = Mock(return_value=(0.0, ""))
    config.get_injury_penalty = Mock(return_value=0.0)

    # Additional attributes
    config.performance_min_weeks = 5
    config.team_quality_min_weeks = 5
    config.matchup_min_weeks = 5
    config.matchup_scoring = {"IMPACT_SCALE": 50.0, "WEIGHT": 1.0}
    config.schedule_scoring = {"IMPACT_SCALE": 50.0, "WEIGHT": 1.0}
    config.performance_scoring = {"MIN_WEEKS": 5}
    config.keys.MIN_WEEKS = "MIN_WEEKS"

    return config


@pytest.fixture
def mock_game_data_manager():
    """Create mock GameDataManager."""
    manager = Mock(spec=GameDataManager)
    return manager


@pytest.fixture
def scoring_calculator(mock_config, mock_game_data_manager):
    """Create PlayerScoringCalculator with mock dependencies."""
    # Mock PlayerManager to provide get_projected_points() method
    # Spec: sub_feature_05_projected_points_manager_consolidation_spec.md
    mock_pm = Mock()
    mock_pm.get_projected_points.return_value = 300.0
    mock_pm.get_actual_points.return_value = 310.0

    mock_tdm = Mock()
    mock_tdm.get_team_ranking_for_position.return_value = 16.0  # Average

    mock_ssm = Mock()
    mock_ssm.get_remaining_opponents.return_value = []

    calc = PlayerScoringCalculator(
        config=mock_config,
        player_manager=mock_pm,
        max_projection=400.0,
        team_data_manager=mock_tdm,
        season_schedule_manager=mock_ssm,
        current_nfl_week=6,
        game_data_manager=mock_game_data_manager
    )
    calc.max_weekly_projection = 30.0
    return calc


@pytest.fixture
def qb_player():
    """Create test QB player (UPDATED for Sub-feature 2)."""
    projected = [25.0] * 17  # All weeks = 25.0
    actual = projected.copy()
    player = FantasyPlayer(
        id=1, name="Patrick Mahomes", team="KC", position="QB",
        fantasy_points=350.0, average_draft_position=5.0,
        projected_points=projected, actual_points=actual
    )
    return player


@pytest.fixture
def rb_player():
    """Create test RB player (UPDATED for Sub-feature 2)."""
    projected = [18.0] * 17  # All weeks = 18.0
    actual = projected.copy()
    player = FantasyPlayer(
        id=2, name="Travis Etienne", team="JAX", position="RB",
        fantasy_points=280.0, average_draft_position=15.0,
        projected_points=projected, actual_points=actual
    )
    return player


@pytest.fixture
def wr_player():
    """Create test WR player (UPDATED for Sub-feature 2)."""
    projected = [20.0] * 17  # All weeks = 20.0
    actual = projected.copy()
    player = FantasyPlayer(
        id=3, name="CeeDee Lamb", team="DAL", position="WR",
        fantasy_points=320.0, average_draft_position=8.0,
        projected_points=projected, actual_points=actual
    )
    return player


@pytest.fixture
def k_player():
    """Create test K player (UPDATED for Sub-feature 2)."""
    projected = [9.0] * 17  # All weeks = 9.0
    actual = projected.copy()
    player = FantasyPlayer(
        id=4, name="Justin Tucker", team="BAL", position="K",
        fantasy_points=150.0, average_draft_position=120.0,
        projected_points=projected, actual_points=actual
    )
    return player


# ============================================================================
# TEMPERATURE SCORING TESTS (Step 11)
# ============================================================================

class TestTemperatureScoring:
    """Tests for temperature scoring adjustments."""

    def test_temperature_scoring_ideal_temp(self, scoring_calculator, qb_player, mock_game_data_manager):
        """Test no penalty at ideal temperature (60°F)."""
        game = UpcomingGame(
            week=6, home_team='KC', away_team='BAL',
            temperature=60, wind_gust=5, indoor=False,
            neutral_site=False, country='USA'
        )
        mock_game_data_manager.get_game.return_value = game

        score, reason = scoring_calculator._apply_temperature_scoring(qb_player, 100.0)

        # At ideal temp, should get EXCELLENT multiplier
        # bonus = (50.0 * 1.05) - 50.0 = 2.5
        assert score > 100.0
        assert "Temp" in reason

    def test_temperature_scoring_cold_weather(self, scoring_calculator, qb_player, mock_game_data_manager):
        """Test penalty for cold weather."""
        game = UpcomingGame(
            week=6, home_team='KC', away_team='BAL',
            temperature=20, wind_gust=5, indoor=False,
            neutral_site=False, country='USA'
        )
        mock_game_data_manager.get_game.return_value = game

        score, reason = scoring_calculator._apply_temperature_scoring(qb_player, 100.0)

        # 40 degrees from ideal - should get VERY_POOR
        # bonus = (50.0 * 0.95) - 50.0 = -2.5
        assert score < 100.0
        assert "20°F" in reason

    def test_temperature_scoring_hot_weather(self, scoring_calculator, qb_player, mock_game_data_manager):
        """Test penalty for hot weather."""
        game = UpcomingGame(
            week=6, home_team='KC', away_team='BAL',
            temperature=100, wind_gust=5, indoor=False,
            neutral_site=False, country='USA'
        )
        mock_game_data_manager.get_game.return_value = game

        score, reason = scoring_calculator._apply_temperature_scoring(qb_player, 100.0)

        # 40 degrees from ideal - should get VERY_POOR
        assert score < 100.0
        assert "100°F" in reason

    def test_temperature_scoring_indoor_game(self, scoring_calculator, qb_player, mock_game_data_manager):
        """Test no temperature adjustment for indoor games."""
        game = UpcomingGame(
            week=6, home_team='DAL', away_team='NYG',
            temperature=None, wind_gust=None, indoor=True,
            neutral_site=False, country='USA'
        )
        mock_game_data_manager.get_game.return_value = game

        score, reason = scoring_calculator._apply_temperature_scoring(qb_player, 100.0)

        assert score == 100.0  # No change
        assert reason == ""

    def test_temperature_scoring_no_game_data(self, scoring_calculator, qb_player, mock_game_data_manager):
        """Test no adjustment when game data is unavailable (bye week)."""
        mock_game_data_manager.get_game.return_value = None

        score, reason = scoring_calculator._apply_temperature_scoring(qb_player, 100.0)

        assert score == 100.0
        assert reason == ""

    def test_temperature_scoring_affects_all_positions(self, scoring_calculator, rb_player, mock_game_data_manager):
        """Test that temperature affects all positions (not just QB/WR/K)."""
        game = UpcomingGame(
            week=6, home_team='JAX', away_team='MIA',
            temperature=95, wind_gust=5, indoor=False,
            neutral_site=False, country='USA'
        )
        mock_game_data_manager.get_game.return_value = game

        score, reason = scoring_calculator._apply_temperature_scoring(rb_player, 100.0)

        # RB should also be affected by temperature
        assert score != 100.0
        assert "Temp" in reason


# ============================================================================
# WIND SCORING TESTS (Step 12)
# ============================================================================

class TestWindScoring:
    """Tests for wind scoring adjustments."""

    def test_wind_scoring_calm_conditions(self, scoring_calculator, qb_player, mock_game_data_manager):
        """Test bonus for calm wind conditions."""
        game = UpcomingGame(
            week=6, home_team='KC', away_team='BAL',
            temperature=65, wind_gust=0, indoor=False,
            neutral_site=False, country='USA'
        )
        mock_game_data_manager.get_game.return_value = game

        score, reason = scoring_calculator._apply_wind_scoring(qb_player, 100.0)

        # Low wind = EXCELLENT
        # bonus = (60.0 * 1.05) - 60.0 = 3.0
        assert score > 100.0
        assert "Wind" in reason

    def test_wind_scoring_high_wind(self, scoring_calculator, qb_player, mock_game_data_manager):
        """Test penalty for high wind."""
        game = UpcomingGame(
            week=6, home_team='KC', away_team='BAL',
            temperature=65, wind_gust=35, indoor=False,
            neutral_site=False, country='USA'
        )
        mock_game_data_manager.get_game.return_value = game

        score, reason = scoring_calculator._apply_wind_scoring(qb_player, 100.0)

        # High wind = VERY_POOR
        # bonus = (60.0 * 0.95) - 60.0 = -3.0
        assert score < 100.0
        assert "35mph" in reason

    def test_wind_scoring_affects_qb(self, scoring_calculator, qb_player, mock_game_data_manager):
        """Test that wind affects QB."""
        game = UpcomingGame(
            week=6, home_team='KC', away_team='BAL',
            temperature=65, wind_gust=30, indoor=False,
            neutral_site=False, country='USA'
        )
        mock_game_data_manager.get_game.return_value = game

        score, reason = scoring_calculator._apply_wind_scoring(qb_player, 100.0)

        assert score != 100.0
        assert "Wind" in reason

    def test_wind_scoring_affects_wr(self, scoring_calculator, wr_player, mock_game_data_manager):
        """Test that wind affects WR."""
        game = UpcomingGame(
            week=6, home_team='DAL', away_team='NYG',
            temperature=65, wind_gust=30, indoor=False,
            neutral_site=False, country='USA'
        )
        mock_game_data_manager.get_game.return_value = game

        score, reason = scoring_calculator._apply_wind_scoring(wr_player, 100.0)

        assert score != 100.0
        assert "Wind" in reason

    def test_wind_scoring_affects_k(self, scoring_calculator, k_player, mock_game_data_manager):
        """Test that wind affects K."""
        game = UpcomingGame(
            week=6, home_team='BAL', away_team='CLE',
            temperature=65, wind_gust=30, indoor=False,
            neutral_site=False, country='USA'
        )
        mock_game_data_manager.get_game.return_value = game

        score, reason = scoring_calculator._apply_wind_scoring(k_player, 100.0)

        assert score != 100.0
        assert "Wind" in reason

    def test_wind_scoring_does_not_affect_rb(self, scoring_calculator, rb_player, mock_game_data_manager):
        """Test that wind does NOT affect RB."""
        game = UpcomingGame(
            week=6, home_team='JAX', away_team='MIA',
            temperature=65, wind_gust=30, indoor=False,
            neutral_site=False, country='USA'
        )
        mock_game_data_manager.get_game.return_value = game

        score, reason = scoring_calculator._apply_wind_scoring(rb_player, 100.0)

        assert score == 100.0  # No change for RB
        assert reason == ""

    def test_wind_scoring_indoor_game(self, scoring_calculator, qb_player, mock_game_data_manager):
        """Test no wind adjustment for indoor games."""
        game = UpcomingGame(
            week=6, home_team='DAL', away_team='NYG',
            temperature=None, wind_gust=None, indoor=True,
            neutral_site=False, country='USA'
        )
        mock_game_data_manager.get_game.return_value = game

        score, reason = scoring_calculator._apply_wind_scoring(qb_player, 100.0)

        assert score == 100.0
        assert reason == ""


# ============================================================================
# LOCATION SCORING TESTS (Step 13)
# ============================================================================

class TestLocationScoring:
    """Tests for location scoring adjustments."""

    def test_location_scoring_home_game(self, scoring_calculator, qb_player, mock_game_data_manager):
        """Test home game bonus."""
        game = UpcomingGame(
            week=6, home_team='KC', away_team='BAL',
            temperature=65, wind_gust=10, indoor=False,
            neutral_site=False, country='USA'
        )
        mock_game_data_manager.get_game.return_value = game

        score, reason = scoring_calculator._apply_location_modifier(qb_player, 100.0)

        # Home bonus = +2.0
        assert score == 102.0
        assert "Home" in reason

    def test_location_scoring_away_game(self, scoring_calculator, qb_player, mock_game_data_manager):
        """Test away game penalty."""
        game = UpcomingGame(
            week=6, home_team='BAL', away_team='KC',  # KC is away
            temperature=65, wind_gust=10, indoor=False,
            neutral_site=False, country='USA'
        )
        mock_game_data_manager.get_game.return_value = game

        score, reason = scoring_calculator._apply_location_modifier(qb_player, 100.0)

        # Away penalty = -2.0
        assert score == 98.0
        assert "Away" in reason

    def test_location_scoring_international_game(self, scoring_calculator, qb_player, mock_game_data_manager):
        """Test international game penalty."""
        game = UpcomingGame(
            week=6, home_team='JAX', away_team='KC',  # KC is away in London
            temperature=55, wind_gust=10, indoor=False,
            neutral_site=True, country='UK'
        )
        mock_game_data_manager.get_game.return_value = game

        score, reason = scoring_calculator._apply_location_modifier(qb_player, 100.0)

        # International penalty = -5.0
        assert score == 95.0
        assert "International" in reason
        assert "UK" in reason

    def test_location_scoring_neutral_site_usa(self, scoring_calculator, qb_player, mock_game_data_manager):
        """Test neutral site in USA (no international penalty)."""
        game = UpcomingGame(
            week=6, home_team='KC', away_team='BAL',
            temperature=70, wind_gust=5, indoor=True,
            neutral_site=True, country='USA'  # Super Bowl in USA
        )
        mock_game_data_manager.get_game.return_value = game

        score, reason = scoring_calculator._apply_location_modifier(qb_player, 100.0)

        # Neutral site in USA = away penalty (-2.0)
        assert score == 98.0
        assert "Away" in reason

    def test_location_scoring_bye_week(self, scoring_calculator, qb_player, mock_game_data_manager):
        """Test no location adjustment for bye week."""
        mock_game_data_manager.get_game.return_value = None

        score, reason = scoring_calculator._apply_location_modifier(qb_player, 100.0)

        assert score == 100.0
        assert reason == ""


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestGameConditionsIntegration:
    """Integration tests for game conditions scoring with score_player."""

    def test_score_player_with_all_game_conditions(self, scoring_calculator, qb_player, mock_game_data_manager):
        """Test score_player with all game condition flags enabled."""
        game = UpcomingGame(
            week=6, home_team='KC', away_team='BAL',
            temperature=60, wind_gust=5, indoor=False,
            neutral_site=False, country='USA'
        )
        mock_game_data_manager.get_game.return_value = game

        # Score with game conditions enabled
        result = scoring_calculator.score_player(
            qb_player,
            team_roster=[],
            draft_round=-1,
            temperature=True,
            wind=True,
            location=True,
            schedule=False,
            adp=False,
            player_rating=False,
            team_quality=False,
            performance=False,
            matchup=False,
            bye=False,
            injury=False
        )

        # Check that reasons include game conditions
        reason_str = ' '.join(result.reason)
        assert "Temp" in reason_str or "Wind" in reason_str or "Location" in reason_str

    def test_score_player_game_conditions_disabled_by_default(self, scoring_calculator, qb_player, mock_game_data_manager):
        """Test that game conditions are disabled by default."""
        game = UpcomingGame(
            week=6, home_team='KC', away_team='BAL',
            temperature=60, wind_gust=5, indoor=False,
            neutral_site=False, country='USA'
        )
        mock_game_data_manager.get_game.return_value = game

        # Score with default parameters
        result = scoring_calculator.score_player(
            qb_player,
            team_roster=[],
            draft_round=-1,
            schedule=False
        )

        # Game conditions should NOT appear in reasons
        reason_str = ' '.join(result.reason)
        assert "Temp" not in reason_str
        assert "Wind" not in reason_str
        assert "Location" not in reason_str

    def test_score_player_no_game_data_manager(self, mock_config, qb_player):
        """Test scoring works without GameDataManager."""
        # Mock PlayerManager to provide get_projected_points() method
        mock_pm = Mock()
        mock_pm.get_projected_points.return_value = 300.0
        mock_pm.get_actual_points.return_value = 310.0

        mock_tdm = Mock()
        mock_tdm.get_team_ranking_for_position.return_value = 16.0

        mock_ssm = Mock()
        mock_ssm.get_remaining_opponents.return_value = []

        # Create calculator WITHOUT game_data_manager
        calc = PlayerScoringCalculator(
            config=mock_config,
            player_manager=mock_pm,
            max_projection=400.0,
            team_data_manager=mock_tdm,
            season_schedule_manager=mock_ssm,
            current_nfl_week=6,
            game_data_manager=None  # Explicitly None
        )
        calc.max_weekly_projection = 30.0

        # Should not raise error even with game conditions enabled
        result = calc.score_player(
            qb_player,
            team_roster=[],
            draft_round=-1,
            temperature=True,
            wind=True,
            location=True,
            schedule=False
        )

        assert result is not None
        assert result.score > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
