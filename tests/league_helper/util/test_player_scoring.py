"""
Comprehensive Unit Tests for player_scoring.py

Tests the PlayerScoringCalculator class which handles the 9-step scoring algorithm:
1. Normalization
2. ADP Multiplier
3. Player Rating Multiplier
4. Team Quality Multiplier
5. Performance Multiplier (actual vs projected deviation)
6. Matchup Multiplier
7. Draft Order Bonus
8. Bye Week Penalty
9. Injury Penalty

Author: Kai Mizuno
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from typing import List

# Imports work via conftest.py which adds the necessary paths
from util.player_scoring import PlayerScoringCalculator
from util.ConfigManager import ConfigManager
from util.ProjectedPointsManager import ProjectedPointsManager
from util.TeamDataManager import TeamDataManager
from util.SeasonScheduleManager import SeasonScheduleManager
from utils.FantasyPlayer import FantasyPlayer


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def mock_data_folder(tmp_path):
    """Create temporary data folder with test config"""
    data_folder = tmp_path / "data"
    data_folder.mkdir()

    # Create minimal league_config.json
    config_content = """{
  "config_name": "Test Config",
  "description": "Test configuration for player_scoring unit tests",
  "parameters": {
    "CURRENT_NFL_WEEK": 6,
    "NFL_SEASON": 2025,
    "NFL_SCORING_FORMAT": "ppr",
    "NORMALIZATION_MAX_SCALE": 100.0,
    "DRAFT_NORMALIZATION_MAX_SCALE": 163,
    "SAME_POS_BYE_WEIGHT": 1.0,
            "DIFF_POS_BYE_WEIGHT": 1.0,
    "DIFFERENT_PLAYER_BYE_OVERLAP_PENALTY": 5.0,
    "INJURY_PENALTIES": {
      "LOW": 0,
      "MEDIUM": 10.0,
      "HIGH": 75.0
    },
    "DRAFT_ORDER_BONUSES": {
      "PRIMARY": 50,
      "SECONDARY": 30
    },
    "DRAFT_ORDER": [
      {"FLEX": "P", "QB": "S"},
      {"FLEX": "P", "QB": "S"}
    ],
    "MAX_POSITIONS": {
      "QB": 2,
      "RB": 4,
      "WR": 4,
      "FLEX": 2,
      "TE": 1,
      "K": 1,
      "DST": 1
    },
    "FLEX_ELIGIBLE_POSITIONS": ["RB", "WR"],
    "ADP_SCORING": {
      "THRESHOLDS": {"EXCELLENT": 20, "GOOD": 50, "POOR": 100, "VERY_POOR": 150},
      "MULTIPLIERS": {"EXCELLENT": 1.20, "GOOD": 1.10, "POOR": 0.90, "VERY_POOR": 0.70},
      "WEIGHT": 1.0
    },
    "PLAYER_RATING_SCORING": {
      "THRESHOLDS": {"EXCELLENT": 80, "GOOD": 60, "POOR": 40, "VERY_POOR": 20},
      "MULTIPLIERS": {"EXCELLENT": 1.25, "GOOD": 1.15, "POOR": 0.95, "VERY_POOR": 0.75},
      "WEIGHT": 1.0
    },
    "TEAM_QUALITY_SCORING": {
      "THRESHOLDS": {"EXCELLENT": 5, "GOOD": 10, "POOR": 20, "VERY_POOR": 25},
      "MULTIPLIERS": {"EXCELLENT": 1.30, "GOOD": 1.15, "POOR": 0.85, "VERY_POOR": 0.70},
      "WEIGHT": 1.0
    },
    "PERFORMANCE_SCORING": {
      "MIN_WEEKS": 3,
      "THRESHOLDS": {"VERY_POOR": -0.2, "POOR": -0.1, "GOOD": 0.1, "EXCELLENT": 0.2},
      "MULTIPLIERS": {"VERY_POOR": 0.60, "POOR": 0.80, "GOOD": 1.20, "EXCELLENT": 1.50},
      "WEIGHT": 1.0
    },
    "CONSISTENCY_SCORING": {
      "MIN_WEEKS": 3,
      "THRESHOLDS": {"EXCELLENT": 0.2, "GOOD": 0.4, "POOR": 0.6, "VERY_POOR": 0.8},
      "MULTIPLIERS": {"EXCELLENT": 1.50, "GOOD": 1.20, "POOR": 0.80, "VERY_POOR": 0.60},
      "WEIGHT": 1.0
    },
    "MATCHUP_SCORING": {
      "IMPACT_SCALE": 150.0,
      "THRESHOLDS": {"EXCELLENT": 15, "GOOD": 6, "POOR": -6, "VERY_POOR": -15},
      "MULTIPLIERS": {"EXCELLENT": 1.25, "GOOD": 1.10, "POOR": 0.90, "VERY_POOR": 0.75},
      "WEIGHT": 1.0
    },
    "SCHEDULE_SCORING": {
      "IMPACT_SCALE": 80.0,
      "THRESHOLDS": {"EXCELLENT": 24, "GOOD": 20, "POOR": 12, "VERY_POOR": 8},
      "MULTIPLIERS": {"EXCELLENT": 1.0, "GOOD": 1.0, "POOR": 1.0, "VERY_POOR": 1.0},
      "WEIGHT": 0.0
    }
  }
}"""

    config_file = data_folder / "league_config.json"
    config_file.write_text(config_content)

    return data_folder


@pytest.fixture
def config_manager(mock_data_folder):
    """Create ConfigManager with test configuration"""
    return ConfigManager(mock_data_folder)


@pytest.fixture
def mock_player_manager():
    """Create mock PlayerManager with projected points methods"""
    # Mock PlayerManager to provide get_projected_points() method
    # Spec: sub_feature_05_projected_points_manager_consolidation_spec.md
    pm = Mock()
    pm.get_projected_points = Mock(return_value=None)
    return pm


@pytest.fixture
def mock_team_data_manager():
    """Create mock TeamDataManager"""
    tdm = Mock(spec=TeamDataManager)
    tdm.get_team_offensive_rank = Mock(return_value=10)
    tdm.get_team_defensive_rank = Mock(return_value=15)
    return tdm


@pytest.fixture
def mock_season_schedule_manager():
    """Create mock SeasonScheduleManager"""
    ssm = Mock(spec=SeasonScheduleManager)
    ssm.get_opponent = Mock(return_value='DAL')
    ssm.get_future_opponents = Mock(return_value=['DAL', 'NYG', 'PHI'])
    ssm.is_schedule_available = Mock(return_value=True)
    return ssm


@pytest.fixture
def scoring_calculator(config_manager, mock_player_manager, mock_team_data_manager, mock_season_schedule_manager):
    """Create PlayerScoringCalculator for testing"""
    return PlayerScoringCalculator(
        config_manager,
        mock_player_manager,
        max_projection=250.0,
        team_data_manager=mock_team_data_manager,
        season_schedule_manager=mock_season_schedule_manager,
        current_nfl_week=6
    )


@pytest.fixture
def test_player():
    """Create a test player with all attributes set (UPDATED for Sub-feature 2)"""
    # Set weekly points arrays - all weeks = 20.0
    projected = [20.0] * 17
    actual = projected.copy()

    player = FantasyPlayer(
        id=12345,
        name="Test Player",
        team="KC",
        position="RB",
        bye_week=7,
        fantasy_points=200.0,
        average_draft_position=15.0,
        player_rating=85.0,
        injury_status="ACTIVE",
        drafted_by="",
        locked=0,
        projected_points=projected,
        actual_points=actual
    )

    player.weighted_projection = 80.0
    player.team_offensive_rank = 1
    player.matchup_score = 10

    return player


# ============================================================================
# INITIALIZATION TESTS
# ============================================================================

class TestInitialization:
    """Test PlayerScoringCalculator initialization"""

    def test_initialization_with_valid_parameters(self, config_manager, mock_player_manager, mock_team_data_manager, mock_season_schedule_manager):
        """Test successful initialization with valid parameters"""
        calculator = PlayerScoringCalculator(
            config_manager,
            mock_player_manager,
            250.0,
            mock_team_data_manager,
            mock_season_schedule_manager,
            6
        )

        assert calculator.config == config_manager
        assert calculator.player_manager == mock_player_manager
        assert calculator.max_projection == 250.0
        assert calculator.team_data_manager == mock_team_data_manager
        assert calculator.season_schedule_manager == mock_season_schedule_manager
        assert calculator.current_nfl_week == 6
        assert calculator.logger is not None

    def test_initialization_with_zero_max_projection(self, config_manager, mock_player_manager, mock_team_data_manager, mock_season_schedule_manager):
        """Test initialization with max_projection = 0"""
        calculator = PlayerScoringCalculator(
            config_manager,
            mock_player_manager,
            0.0,
            mock_team_data_manager,
            mock_season_schedule_manager,
            6
        )

        assert calculator.max_projection == 0.0

    def test_initialization_with_negative_max_projection(self, config_manager, mock_player_manager, mock_team_data_manager, mock_season_schedule_manager):
        """Test initialization with negative max_projection"""
        calculator = PlayerScoringCalculator(
            config_manager,
            mock_player_manager,
            -100.0,
            mock_team_data_manager,
            mock_season_schedule_manager,
            6
        )

        # Should allow negative (edge case)
        assert calculator.max_projection == -100.0


# ============================================================================
# WEEKLY PROJECTION TESTS
# ============================================================================

class TestWeeklyProjection:
    """Test get_weekly_projection() method"""

    def test_get_weekly_projection_valid_week(self, scoring_calculator, test_player):
        """Test getting weekly projection for a valid week (UPDATED for Sub-feature 2)"""
        # Set week 6 projection (index 5) - UPDATED for array-based format
        test_player.projected_points[5] = 25.0  # Week 6
        test_player.actual_points[5] = 25.0
        # Set max weekly projection for week 6 (weekly normalization uses this, not ROS max)
        scoring_calculator.max_weekly_projection = 30.0

        orig_pts, weighted_pts = scoring_calculator.get_weekly_projection(test_player, week=6)

        assert orig_pts == 25.0
        # Weekly normalization: (25.0 / 30.0) * 100.0 = 83.33...
        expected_weighted = (25.0 / 30.0) * 100.0
        assert abs(weighted_pts - expected_weighted) < 0.01

    def test_get_weekly_projection_uses_current_week_when_zero(self, scoring_calculator, test_player):
        """Test that week=0 defaults to current week (UPDATED for Sub-feature 2)"""
        # Set week 6 projection (index 5) - Current week is 6
        test_player.projected_points[5] = 30.0
        test_player.actual_points[5] = 30.0

        orig_pts, weighted_pts = scoring_calculator.get_weekly_projection(test_player, week=0)

        assert orig_pts == 30.0

    def test_get_weekly_projection_uses_current_week_when_out_of_range(self, scoring_calculator, test_player):
        """Test that week=99 defaults to current week (UPDATED for Sub-feature 2)"""
        # Set week 6 projection (index 5)
        test_player.projected_points[5] = 35.0
        test_player.actual_points[5] = 35.0

        orig_pts, weighted_pts = scoring_calculator.get_weekly_projection(test_player, week=99)

        assert orig_pts == 35.0

    def test_get_weekly_projection_missing_data_returns_zero(self, scoring_calculator, test_player):
        """Test that missing weekly data returns (0.0, 0.0) (UPDATED for Sub-feature 2)"""
        # Simulate missing data by setting array element to None
        test_player.projected_points[9] = None  # Week 10 (index 9)
        test_player.actual_points[9] = None

        orig_pts, weighted_pts = scoring_calculator.get_weekly_projection(test_player, week=10)

        assert orig_pts == 0.0
        assert weighted_pts == 0.0

    def test_get_weekly_projection_none_value_returns_zero(self, scoring_calculator, test_player):
        """Test that None weekly points returns (0.0, 0.0) (UPDATED for Sub-feature 2)"""
        # Set week 7 projection (index 6) to None
        test_player.projected_points[6] = None
        test_player.actual_points[6] = None

        orig_pts, weighted_pts = scoring_calculator.get_weekly_projection(test_player, week=7)

        assert orig_pts == 0.0
        assert weighted_pts == 0.0

    def test_get_weekly_projection_zero_value_returns_zero(self, scoring_calculator, test_player):
        """Test that zero weekly points returns (0.0, 0.0) (UPDATED for Sub-feature 2)"""
        # Set week 8 projection (index 7) to 0.0
        test_player.projected_points[7] = 0.0
        test_player.actual_points[7] = 0.0

        orig_pts, weighted_pts = scoring_calculator.get_weekly_projection(test_player, week=8)

        assert orig_pts == 0.0
        assert weighted_pts == 0.0

    def test_get_weekly_projection_with_zero_max_projection(self, config_manager, mock_player_manager, mock_team_data_manager, mock_season_schedule_manager, test_player):
        """Test weekly projection when max_projection is 0 (UPDATED for Sub-feature 2)"""
        calculator = PlayerScoringCalculator(
            config_manager,
            mock_player_manager,
            0.0,
            mock_team_data_manager,
            mock_season_schedule_manager,
            6
        )
        # Set week 6 projection (index 5)
        test_player.projected_points[5] = 25.0
        test_player.actual_points[5] = 25.0

        orig_pts, weighted_pts = calculator.get_weekly_projection(test_player, week=6)

        assert orig_pts == 25.0
        # With max_projection=0, weighted should be 0 (not crash with division by zero)
        assert weighted_pts == 0.0


# ============================================================================
# WEIGHT PROJECTION TESTS
# ============================================================================

class TestWeightProjection:
    """Test weight_projection() method"""

    def test_weight_projection_normal_value(self, scoring_calculator):
        """Test weight_projection with normal value"""
        result = scoring_calculator.weight_projection(125.0)

        expected = (125.0 / 250.0) * 100.0
        assert abs(result - expected) < 0.01

    def test_weight_projection_zero_input(self, scoring_calculator):
        """Test weight_projection with zero input"""
        result = scoring_calculator.weight_projection(0.0)

        assert result == 0.0

    def test_weight_projection_max_value(self, scoring_calculator):
        """Test weight_projection with max_projection value"""
        result = scoring_calculator.weight_projection(250.0)

        assert abs(result - 100.0) < 0.01

    def test_weight_projection_over_max(self, scoring_calculator):
        """Test weight_projection with value > max_projection"""
        result = scoring_calculator.weight_projection(500.0)

        expected = (500.0 / 250.0) * 100.0
        assert abs(result - expected) < 0.01
        assert result > 100.0  # Can exceed 100


# ============================================================================
# ============================================================================
# PERFORMANCE DEVIATION TESTS
# ============================================================================

class TestPerformanceDeviation:
    """Test calculate_performance_deviation() method"""

    def test_calculate_performance_deviation_with_sufficient_data(self, scoring_calculator, test_player, mock_player_manager):
        """Test performance deviation with sufficient data (UPDATED for Sub-feature 2)"""
        # Set up actual points for weeks 1-5 (current_week = 6, so weeks 1-5 are past)
        test_player.actual_points[0] = 22.0  # Week 1
        test_player.actual_points[1] = 18.0  # Week 2
        test_player.actual_points[2] = 21.0  # Week 3
        test_player.actual_points[3] = 19.0  # Week 4
        test_player.actual_points[4] = 23.0  # Week 5

        # Mock projected points (all 20.0)
        mock_player_manager.get_projected_points = Mock(return_value=20.0)

        deviation = scoring_calculator.calculate_performance_deviation(test_player)

        assert deviation is not None
        # Average deviation: [(22-20)/20, (18-20)/20, (21-20)/20, (19-20)/20, (23-20)/20]
        # = [0.1, -0.1, 0.05, -0.05, 0.15] => average = 0.03
        assert abs(deviation - 0.03) < 0.05

    def test_calculate_performance_deviation_returns_none_for_dst(self, scoring_calculator, test_player):
        """Test that DST players return None"""
        test_player.position = "DST"

        deviation = scoring_calculator.calculate_performance_deviation(test_player)

        assert deviation is None

    def test_calculate_performance_deviation_insufficient_data(self, scoring_calculator, test_player, mock_player_manager):
        """Test performance deviation with insufficient data (< MIN_WEEKS) (UPDATED for Sub-feature 2)"""
        # Set all weeks to None, then set only 2 weeks of data
        test_player.actual_points = [None] * 17
        test_player.projected_points = [None] * 17
        test_player.actual_points[0] = 20.0  # Week 1
        test_player.actual_points[1] = 22.0  # Week 2
        mock_player_manager.get_projected_points = Mock(return_value=20.0)

        deviation = scoring_calculator.calculate_performance_deviation(test_player)

        assert deviation is None  # Insufficient data

    def test_calculate_performance_deviation_skips_zero_actual(self, scoring_calculator, test_player, mock_player_manager):
        """Test that weeks with actual=0 are skipped (UPDATED for Sub-feature 2)"""
        test_player.actual_points[0] = 20.0  # Week 1
        test_player.actual_points[1] = 0.0   # Week 2 - should be skipped
        test_player.actual_points[2] = 22.0  # Week 3
        test_player.actual_points[3] = 18.0  # Week 4
        test_player.actual_points[4] = 21.0  # Week 5
        mock_player_manager.get_projected_points = Mock(return_value=20.0)

        deviation = scoring_calculator.calculate_performance_deviation(test_player)

        # Should calculate based on 4 weeks (skipping week 2)
        assert deviation is not None

    def test_calculate_performance_deviation_skips_zero_projected(self, scoring_calculator, test_player, mock_player_manager):
        """Test that weeks with projected=0 are skipped"""
        test_player.actual_points[0] = 20.0  # Week 1
        test_player.actual_points[1] = 22.0  # Week 2
        test_player.actual_points[2] = 18.0  # Week 3
        test_player.actual_points[3] = 21.0  # Week 4
        test_player.actual_points[4] = 19.0  # Week 5

        # Mock to return 0 for week 2
        def get_proj(player, week):
            return 0.0 if week == 2 else 20.0

        mock_player_manager.get_projected_points = Mock(side_effect=get_proj)

        deviation = scoring_calculator.calculate_performance_deviation(test_player)

        # Should calculate based on 4 weeks (skipping week 2)
        assert deviation is not None

    def test_calculate_performance_deviation_dynamic_lookback_with_bye_week(self, scoring_calculator, test_player, mock_player_manager):
        """Test dynamic lookback skips bye weeks and finds MIN_WEEKS valid data"""
        # current_nfl_week=6, MIN_WEEKS=3, max_lookback=6 (2x MIN_WEEKS)
        # Player had bye week 4 (actual=0)
        # Old behavior: window [3,4,5] -> only weeks 3,5 valid -> returns None
        # New behavior: looks back, skips week 4, uses weeks 5,3,2 -> returns deviation
        test_player.actual_points[0] = 18.0  # Week 1
        test_player.actual_points[1] = 19.0  # Week 2
        test_player.actual_points[2] = 21.0  # Week 3
        test_player.actual_points[3] = 0.0   # Bye week - should be skipped  # Week 4
        test_player.actual_points[4] = 22.0  # Week 5

        mock_player_manager.get_projected_points = Mock(return_value=20.0)

        deviation = scoring_calculator.calculate_performance_deviation(test_player)

        # Should find 3 valid weeks (5, 3, 2) by looking back past bye week
        assert deviation is not None
        # Deviations: week5=(22-20)/20=0.1, week3=(21-20)/20=0.05, week2=(19-20)/20=-0.05
        # Average = (0.1 + 0.05 + -0.05) / 3 = 0.0333
        assert abs(deviation - 0.0333) < 0.01

    def test_calculate_performance_deviation_dynamic_lookback_multiple_bye_weeks(self, scoring_calculator, test_player, mock_player_manager):
        """Test dynamic lookback handles multiple consecutive zero weeks"""
        # Player had two zero weeks (weeks 3 and 4)
        test_player.actual_points[0] = 18.0  # Week 1
        test_player.actual_points[1] = 19.0  # Week 2
        test_player.actual_points[2] = 0.0   # Zero - should be skipped  # Week 3
        test_player.actual_points[3] = 0.0   # Zero - should be skipped  # Week 4
        test_player.actual_points[4] = 22.0  # Week 5

        mock_player_manager.get_projected_points = Mock(return_value=20.0)

        deviation = scoring_calculator.calculate_performance_deviation(test_player)

        # Should find 3 valid weeks (5, 2, 1) by looking back past zero weeks
        assert deviation is not None

    def test_calculate_performance_deviation_respects_max_lookback_limit(self, mock_data_folder):
        """Test that lookback respects 2x MIN_WEEKS limit"""
        from util.ConfigManager import ConfigManager
        from util.TeamDataManager import TeamDataManager
        from util.SeasonScheduleManager import SeasonScheduleManager

        # Create a new config with CURRENT_NFL_WEEK=10
        config_content = """{
  "config_name": "Test Config",
  "description": "Test config for max lookback limit test",
  "parameters": {
    "CURRENT_NFL_WEEK": 10,
    "NFL_SEASON": 2025,
    "NFL_SCORING_FORMAT": "ppr",
    "NORMALIZATION_MAX_SCALE": 100.0,
    "DRAFT_NORMALIZATION_MAX_SCALE": 163,
    "SAME_POS_BYE_WEIGHT": 1.0,
    "DIFF_POS_BYE_WEIGHT": 1.0,
    "INJURY_PENALTIES": {"LOW": 0, "MEDIUM": 10.0, "HIGH": 75.0},
    "DRAFT_ORDER_BONUSES": {"PRIMARY": 50, "SECONDARY": 30},
    "DRAFT_ORDER": [{"FLEX": "P"}],
    "MAX_POSITIONS": {"QB": 2, "RB": 4, "WR": 4, "FLEX": 2, "TE": 1, "K": 1, "DST": 1},
    "FLEX_ELIGIBLE_POSITIONS": ["RB", "WR"],
    "ADP_SCORING": {"THRESHOLDS": {"EXCELLENT": 20}, "MULTIPLIERS": {"EXCELLENT": 1.0}, "WEIGHT": 1.0},
    "PLAYER_RATING_SCORING": {"THRESHOLDS": {"EXCELLENT": 80}, "MULTIPLIERS": {"EXCELLENT": 1.0}, "WEIGHT": 1.0},
    "TEAM_QUALITY_SCORING": {"THRESHOLDS": {"EXCELLENT": 5}, "MULTIPLIERS": {"EXCELLENT": 1.0}, "WEIGHT": 1.0},
    "PERFORMANCE_SCORING": {"MIN_WEEKS": 3, "THRESHOLDS": {"EXCELLENT": 0.2}, "MULTIPLIERS": {"EXCELLENT": 1.5}, "WEIGHT": 1.0},
    "MATCHUP_SCORING": {"IMPACT_SCALE": 150.0, "THRESHOLDS": {"EXCELLENT": 15}, "MULTIPLIERS": {"EXCELLENT": 1.0}, "WEIGHT": 1.0},
    "SCHEDULE_SCORING": {"IMPACT_SCALE": 80.0, "THRESHOLDS": {"EXCELLENT": 24}, "MULTIPLIERS": {"EXCELLENT": 1.0}, "WEIGHT": 0.0}
  }
}"""
        config_file = mock_data_folder / "league_config.json"
        config_file.write_text(config_content)

        config = ConfigManager(mock_data_folder)
        mock_ppm = Mock()
        mock_ppm.get_projected_points = Mock(return_value=20.0)
        mock_tdm = Mock(spec=TeamDataManager)
        mock_ssm = Mock(spec=SeasonScheduleManager)

        calculator = PlayerScoringCalculator(config, mock_ppm, 250.0, mock_tdm, mock_ssm, 10)

        # Create player with valid data only in weeks 1-3 (too old)
        # current_week=10, MIN_WEEKS=3, max_lookback=6 -> earliest_week = 10-6 = 4
        # Data in weeks 1-3 is outside the lookback window
        player = FantasyPlayer(id=1, name="Test", team="KC", position="QB")
        for week in range(1, 18):
            setattr(player, f"week_{week}_points", None)
        player.week_1_points = 20.0
        player.week_2_points = 22.0
        player.week_3_points = 18.0
        # Weeks 4-9 are all zeros or None (simulating long injury)

        deviation = calculator.calculate_performance_deviation(player)

        # Should return None because valid data (weeks 1-3) is outside max lookback window
        assert deviation is None

    def test_calculate_performance_deviation_uses_most_recent_valid_weeks(self, scoring_calculator, test_player, mock_player_manager):
        """Test that dynamic lookback uses most recent valid weeks first"""
        # All weeks have data, but we should use weeks 5, 4, 3 (most recent 3)
        test_player.actual_points[0] = 10.0  # Old - shouldn't be used  # Week 1
        test_player.actual_points[1] = 12.0  # Old - shouldn't be used  # Week 2
        test_player.actual_points[2] = 21.0  # Should be used (3rd most recent valid)  # Week 3
        test_player.actual_points[3] = 19.0  # Should be used (2nd most recent valid)  # Week 4
        test_player.actual_points[4] = 22.0  # Should be used (most recent valid)  # Week 5

        mock_player_manager.get_projected_points = Mock(return_value=20.0)

        deviation = scoring_calculator.calculate_performance_deviation(test_player)

        assert deviation is not None
        # Should use weeks 5, 4, 3 (most recent 3 valid weeks)
        # Deviations: week5=(22-20)/20=0.1, week4=(19-20)/20=-0.05, week3=(21-20)/20=0.05
        # Average = (0.1 + -0.05 + 0.05) / 3 = 0.0333
        assert abs(deviation - 0.0333) < 0.01


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestScoringIntegration:
    """Integration tests for score_player() method"""

    def test_score_player_with_all_flags_disabled(self, scoring_calculator, test_player):
        """Test scoring with all multipliers/penalties disabled"""
        # Set ROS projection to 250 for weighted = 100
        for i in range(5, 17):  # indices 5-16 = weeks 6-17
            test_player.projected_points[i] = 250.0 / 12
            test_player.actual_points[i] = 250.0 / 12

        result = scoring_calculator.score_player(
            test_player,
            team_roster=[],
            adp=False,
            player_rating=False,
            team_quality=False,
            performance=False,
            matchup=False,
            schedule=False,
            draft_round=-1,
            bye=False,
            injury=False
        )

        # Should only have normalization
        assert abs(result.score - 100.0) < 0.01

    def test_score_player_with_adp_multiplier(self, scoring_calculator, test_player):
        """Test scoring with only ADP multiplier enabled"""
        test_player.average_draft_position = 15.0  # EXCELLENT
        for i in range(5, 17):  # indices 5-16 = weeks 6-17
            test_player.projected_points[i] = 250.0 / 12
            test_player.actual_points[i] = 250.0 / 12

        result = scoring_calculator.score_player(
            test_player,
            team_roster=[],
            adp=True,
            player_rating=False,
            team_quality=False,
            performance=False,
            matchup=False,
            schedule=False,
            draft_round=-1,
            bye=False,
            injury=False
        )

        # 100 * 1.20 = 120
        assert abs(result.score - 120.0) < 0.01

    def test_score_player_with_bye_penalty(self, scoring_calculator, test_player):
        """Test scoring with median-based bye week penalty"""
        for i in range(5, 17):  # indices 5-16 = weeks 6-17
            test_player.projected_points[i] = 250.0 / 12
            test_player.actual_points[i] = 250.0 / 12
        test_player.bye_week = 7

        # Create roster with 2 same-position players on bye week 7 (UPDATED for Sub-feature 2)
        projected_rb1 = [0.0] * 17
        projected_rb1[0], projected_rb1[1], projected_rb1[2] = 10.0, 12.0, 14.0  # Weeks 1-3, Median = 12.0
        other_rb1 = FantasyPlayer(
            id=99, name="RB1", team="BUF", position="RB", bye_week=7, fantasy_points=100.0,
            projected_points=projected_rb1, actual_points=projected_rb1.copy()
        )

        projected_rb2 = [0.0] * 17
        projected_rb2[0], projected_rb2[1], projected_rb2[2] = 8.0, 10.0, 9.0  # Weeks 1-3, Median = 9.0
        other_rb2 = FantasyPlayer(
            id=98, name="RB2", team="PHI", position="RB", bye_week=7, fantasy_points=100.0,
            projected_points=projected_rb2, actual_points=projected_rb2.copy()
        )

        result = scoring_calculator.score_player(
            test_player,
            team_roster=[other_rb1, other_rb2],
            adp=False,
            player_rating=False,
            team_quality=False,
            performance=False,
            matchup=False,
            schedule=False,
            draft_round=-1,
            bye=True,
            injury=False
        )

        # Bye week penalty calculation (median-based):
        # Penalty = (12.0 + 9.0) ** 1.0 = 21.0
        # Score = 100 - 21.0 = 79.0
        assert abs(result.score - 79.0) < 0.01

    def test_score_player_with_injury_penalty(self, scoring_calculator, test_player):
        """Test scoring with injury penalty"""
        for i in range(5, 17):  # indices 5-16 = weeks 6-17
            test_player.projected_points[i] = 250.0 / 12
            test_player.actual_points[i] = 250.0 / 12
        test_player.injury_status = "OUT"  # MEDIUM risk (changed from HIGH)

        result = scoring_calculator.score_player(
            test_player,
            team_roster=[],
            adp=False,
            player_rating=False,
            team_quality=False,
            performance=False,
            matchup=False,
            schedule=False,
            draft_round=-1,
            bye=False,
            injury=True
        )

        # Get actual penalty from config based on current risk level
        risk_level = test_player.get_risk_level()
        expected_penalty = scoring_calculator.config.get_injury_penalty(risk_level)
        expected_score = 100.0 - expected_penalty
        assert abs(result.score - expected_score) < 0.01

    def test_score_player_with_weekly_projection(self, scoring_calculator, test_player):
        """Test scoring with use_weekly_projection=True (UPDATED for Sub-feature 2)"""
        # Week 6 is current week (current_nfl_week = 6), so use projected_points
        test_player.projected_points[5] = 25.0  # Week 6
        test_player.actual_points[5] = 25.0
        # Set max weekly projection for week 6 (weekly normalization uses this, not ROS max)
        scoring_calculator.max_weekly_projection = 30.0

        result = scoring_calculator.score_player(
            test_player,
            team_roster=[],
            use_weekly_projection=True,
            adp=False,
            player_rating=False,
            team_quality=False,
            performance=False,
            matchup=False,
            schedule=False,
            draft_round=-1,
            bye=False,
            injury=False
        )

        # Weekly normalization: (25/30) * 100 = 83.33...
        expected = (25.0 / 30.0) * 100.0
        assert abs(result.score - expected) < 0.01

    def test_score_player_returns_scored_player_object(self, scoring_calculator, test_player):
        """Test that score_player returns a ScoredPlayer object (UPDATED for Sub-feature 2)"""
        # Weeks 6-17 are current/future (current_nfl_week = 6), so use projected_points
        for i in range(5, 17):  # indices 5-16 = weeks 6-17
            test_player.projected_points[i] = 250.0 / 12
            test_player.actual_points[i] = 250.0 / 12

        result = scoring_calculator.score_player(
            test_player,
            team_roster=[],
            draft_round=-1,
            schedule=False
        )

        assert result.player == test_player
        assert isinstance(result.score, float)
        assert isinstance(result.reason, list)
        assert len(result.reason) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
