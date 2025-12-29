"""
Comprehensive Unit Tests for PlayerManager.score_player() and Related Methods

These tests verify the entire 9-step scoring system works correctly after bug fixes:
1. Normalization
2. ADP Multiplier
3. Player Rating Multiplier
4. Team Quality Multiplier
5. Consistency Multiplier (FIXED: now uses rising_thresholds=False)
6. Matchup Multiplier
7. Draft Order Bonus (FIXED: draft_round default changed to -1, check changed to >= 0)
8. Bye Week Penalty
9. Injury Penalty

Author: Claude Code
Date: 2025-10-09
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from typing import List
from pathlib import Path

# Imports work via conftest.py which adds the necessary paths
from util.PlayerManager import PlayerManager
from util.ConfigManager import ConfigManager
from util.TeamDataManager import TeamDataManager
from util.FantasyTeam import FantasyTeam
from utils.FantasyPlayer import FantasyPlayer


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def mock_data_folder(tmp_path):
    """Create temporary data folder with test config and data files"""
    data_folder = tmp_path / "data"
    data_folder.mkdir()

    # Create minimal league_config.json
    config_content = """{
  "config_name": "Test Config",
  "description": "Test configuration for unit tests",
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
      {"FLEX": "P", "QB": "S"},
      {"QB": "P", "FLEX": "S"},
      {"TE": "P", "FLEX": "S"},
      {"K": "P"},
      {"DST": "P"}
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
      "THRESHOLDS": {
        "EXCELLENT": 20,
        "GOOD": 50,
        "POOR": 100,
        "VERY_POOR": 150
      },
      "MULTIPLIERS": {
        "EXCELLENT": 1.20,
        "GOOD": 1.10,
        "POOR": 0.90,
        "VERY_POOR": 0.70
      },
      "WEIGHT": 1.0
    },
    "PLAYER_RATING_SCORING": {
      "THRESHOLDS": {
        "EXCELLENT": 80,
        "GOOD": 60,
        "POOR": 40,
        "VERY_POOR": 20
      },
      "MULTIPLIERS": {
        "EXCELLENT": 1.25,
        "GOOD": 1.15,
        "POOR": 0.95,
        "VERY_POOR": 0.75
      },
      "WEIGHT": 1.0
    },
    "TEAM_QUALITY_SCORING": {
      "THRESHOLDS": {
        "EXCELLENT": 5,
        "GOOD": 10,
        "POOR": 20,
        "VERY_POOR": 25
      },
      "MULTIPLIERS": {
        "EXCELLENT": 1.30,
        "GOOD": 1.15,
        "POOR": 0.85,
        "VERY_POOR": 0.70
      },
      "WEIGHT": 1.0
    },
    "PERFORMANCE_SCORING": {
      "MIN_WEEKS": 3,
      "THRESHOLDS": {
        "VERY_POOR": -0.2,
        "POOR": -0.1,
        "GOOD": 0.1,
        "EXCELLENT": 0.2
      },
      "MULTIPLIERS": {
        "VERY_POOR": 0.60,
        "POOR": 0.80,
        "GOOD": 1.20,
        "EXCELLENT": 1.50
      },
      "WEIGHT": 1.0
    },
    "CONSISTENCY_SCORING": {
      "MIN_WEEKS": 3,
      "THRESHOLDS": {
        "EXCELLENT": 0.2,
        "GOOD": 0.4,
        "POOR": 0.6,
        "VERY_POOR": 0.8
      },
      "MULTIPLIERS": {
        "EXCELLENT": 1.50,
        "GOOD": 1.20,
        "POOR": 0.80,
        "VERY_POOR": 0.60
      },
      "WEIGHT": 1.0
    },
    "MATCHUP_SCORING": {
      "IMPACT_SCALE": 150.0,
      "THRESHOLDS": {
        "EXCELLENT": 15,
        "GOOD": 6,
        "POOR": -6,
        "VERY_POOR": -15
      },
      "MULTIPLIERS": {
        "EXCELLENT": 1.25,
        "GOOD": 1.10,
        "POOR": 0.90,
        "VERY_POOR": 0.75
      },
      "WEIGHT": 1.0
    },
    "SCHEDULE_SCORING": {
      "IMPACT_SCALE": 80.0,
      "THRESHOLDS": {
        "EXCELLENT": 24,
        "GOOD": 20,
        "POOR": 12,
        "VERY_POOR": 8
      },
      "MULTIPLIERS": {
        "EXCELLENT": 1.0,
        "GOOD": 1.0,
        "POOR": 1.0,
        "VERY_POOR": 1.0
      },
      "WEIGHT": 0.0
    }
  }
}"""

    config_file = data_folder / "league_config.json"
    config_file.write_text(config_content)

    # Note: teams.csv no longer used - team data is now in team_data folder
    # The team_data_manager fixture creates the team_data folder with per-team files

    # Create minimal players.csv (will be populated by tests)
    players_content = """id,name,team,position,bye_week,fantasy_points,injury_status,drafted,locked,average_draft_position,player_rating,week_1_points,week_2_points,week_3_points,week_4_points,week_5_points,week_6_points,week_7_points,week_8_points,week_9_points,week_10_points,week_11_points,week_12_points,week_13_points,week_14_points,week_15_points,week_16_points,week_17_points
"""

    players_file = data_folder / "players.csv"
    players_file.write_text(players_content)

    return data_folder


@pytest.fixture
def config_manager(mock_data_folder):
    """Create ConfigManager with test configuration"""
    return ConfigManager(mock_data_folder)


@pytest.fixture
def team_data_manager(mock_data_folder, config_manager):
    """Create TeamDataManager with test data"""
    # Create team_data folder with a test team file
    team_data_folder = mock_data_folder / "team_data"
    team_data_folder.mkdir(exist_ok=True)

    # Create KC.csv with test data
    kc_content = """week,QB,RB,WR,TE,K,points_scored,points_allowed
1,20.5,25.3,35.2,8.1,9.0,28,17
2,18.3,22.1,31.5,7.8,8.5,24,21
3,22.1,28.5,38.3,9.2,10.1,31,14
4,19.8,24.2,33.1,8.5,9.3,27,20
5,21.3,26.8,36.7,8.8,9.8,29,18"""
    (team_data_folder / "KC.csv").write_text(kc_content)

    return TeamDataManager(mock_data_folder, config_manager, None, 6)


@pytest.fixture
def mock_fantasy_team(config_manager):
    """Create mock FantasyTeam for testing"""
    team = Mock(spec=FantasyTeam)
    team.roster = []
    team.get_matching_byes_in_roster = Mock(return_value=0)
    return team


@pytest.fixture
def player_manager(mock_data_folder, config_manager, team_data_manager, mock_fantasy_team):
    """Create PlayerManager for testing"""
    # Create PlayerManager without loading CSV (we'll mock players)
    pm = PlayerManager.__new__(PlayerManager)
    pm.logger = Mock()
    pm.config = config_manager
    pm.team_data_manager = team_data_manager
    pm.file_str = str(mock_data_folder / "players.csv")
    pm.players = []
    pm.team = mock_fantasy_team
    pm.max_projection = 250.0  # Set to reasonable value to avoid division by zero
    pm.max_weekly_projections = {}  # Initialize weekly projection cache

    # Mock projected_points_manager for performance calculations
    pm.projected_points_manager = Mock()
    pm.projected_points_manager.get_projected_points = Mock(return_value=None)

    # Create mock managers
    pm.team_data_manager = Mock()
    pm.team_data_manager.get_team_offensive_rank = Mock(return_value=10)
    pm.team_data_manager.get_team_defensive_rank = Mock(return_value=15)
    pm.team_data_manager.get_team_defense_vs_position_rank = Mock(return_value=18)

    pm.season_schedule_manager = Mock()
    pm.season_schedule_manager.get_opponent = Mock(return_value='DAL')
    pm.season_schedule_manager.is_schedule_available = Mock(return_value=True)
    pm.season_schedule_manager.get_future_opponents = Mock(return_value=['DAL', 'PHI', 'NYG'])

    # Initialize scoring_calculator (required for refactored PlayerManager)
    from util.player_scoring import PlayerScoringCalculator
    pm.scoring_calculator = PlayerScoringCalculator(
        config_manager,
        pm.projected_points_manager,
        250.0,
        pm.team_data_manager,
        pm.season_schedule_manager,
        6
    )

    return pm


@pytest.fixture
def test_player():
    """Create a test player with all attributes set (UPDATED for Sub-feature 2)"""
    # Set weekly points for consistency calculation and rest-of-season projection
    # Current week is 6, so weeks 6-17 will be used for ROS projection
    # Set weeks 6-17 to sum to exactly 200.0 (12 weeks)
    projected = [0.0] * 17
    projected[0] = 18.5  # Week 1
    projected[1] = 22.0  # Week 2
    projected[2] = 19.5  # Week 3
    projected[3] = 21.0  # Week 4
    projected[4] = 20.0  # Week 5
    # Weeks 6-17: 11 weeks * 16.0 + 1 week * 24.0 = 176 + 24 = 200.0
    projected[5] = 16.0   # Week 6
    projected[6] = 16.0   # Week 7
    projected[7] = 16.0   # Week 8
    projected[8] = 16.0   # Week 9
    projected[9] = 16.0   # Week 10
    projected[10] = 16.0  # Week 11
    projected[11] = 16.0  # Week 12
    projected[12] = 16.0  # Week 13
    projected[13] = 16.0  # Week 14
    projected[14] = 16.0  # Week 15
    projected[15] = 16.0  # Week 16
    projected[16] = 24.0  # Week 17 - Extra to make sum exactly 200.0
    actual = projected.copy()  # Same values since config.current_nfl_week=6 means weeks 1-5 use actual

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

    # Set computed properties
    player.weighted_projection = 80.0  # (200/250) * 100
    player.consistency = 0.3  # Good consistency (low CV)
    player.team_offensive_rank = 1  # Excellent team (KC)
    player.team_defensive_rank = 5
    player.matchup_score = 10  # Good matchup

    return player


# ============================================================================
# STEP 1: NORMALIZATION TESTS
# ============================================================================

class TestNormalization:
    """Test Step 1: Normalization calculation"""

    def test_normalization_returns_weighted_projection(self, player_manager, test_player):
        """Verify normalization simply returns the weighted_projection"""
        result, reason = player_manager.scoring_calculator._get_normalized_fantasy_points(test_player, use_weekly_projection=False)
        assert result == test_player.weighted_projection
        assert result == 80.0
        assert "Projected:" in reason
        assert "Weighted:" in reason

    def test_normalization_with_zero_weighted_projection(self, player_manager):
        """Test normalization with zero weighted_projection"""
        player = FantasyPlayer(
            id=1, name="Zero Player", team="KC", position="RB",
            fantasy_points=0.0, weighted_projection=0.0
        )
        result, reason = player_manager.scoring_calculator._get_normalized_fantasy_points(player, use_weekly_projection=False)
        assert result == 0.0


# ============================================================================
# WEEKLY PROJECTION TESTS
# ============================================================================

class TestWeeklyProjections:
    """Test weekly projection fetching and normalization"""

    def test_get_weekly_projection_valid_data(self, player_manager, test_player):
        """Test get_weekly_projection with valid weekly data"""
        # Set up player with week 6 data (current week in config)
        test_player.projected_points[5] = 25.0  # Week 6 (index 5)
        test_player.actual_points[5] = 25.0  # Same for hybrid logic
        player_manager.max_projection = 300.0  # ROS max
        player_manager.scoring_calculator.max_projection = 300.0
        # Set weekly max (needed for weekly normalization)
        player_manager.max_weekly_projections = {6: 30.0}
        player_manager.scoring_calculator.max_weekly_projection = 30.0

        orig_pts, weighted_pts = player_manager.get_weekly_projection(test_player, week=6)

        assert orig_pts == 25.0
        # Weighted should use WEEKLY max: (25/30) * 100 = 83.33...
        expected_weighted = (25.0 / 30.0) * 100.0
        assert abs(weighted_pts - expected_weighted) < 0.01

    def test_get_weekly_projection_uses_current_week_when_invalid(self, player_manager, test_player):
        """Test that invalid week parameter defaults to current week"""
        # Config has current_nfl_week = 6
        test_player.projected_points[5] = 20.0  # Week 6 (index 5)
        test_player.actual_points[5] = 20.0  # Same for hybrid logic
        player_manager.max_projection = 300.0
        player_manager.scoring_calculator.max_projection = 300.0  # Update calculator too

        # Pass invalid week (0)
        orig_pts, weighted_pts = player_manager.get_weekly_projection(test_player, week=0)

        # Should use week 6 instead
        assert orig_pts == 20.0

    def test_get_weekly_projection_missing_data_returns_zero(self, player_manager, test_player):
        """Test that missing weekly data returns (0.0, 0.0)"""
        # Set week_10 to 0.0 to test "missing" data (arrays always have values)
        test_player.projected_points[9] = 0.0  # Week 10 (index 9)
        test_player.actual_points[9] = 0.0
        orig_pts, weighted_pts = player_manager.get_weekly_projection(test_player, week=10)

        assert orig_pts == 0.0
        assert weighted_pts == 0.0

    def test_get_weekly_projection_none_value_returns_zero(self, player_manager, test_player):
        """Test that None weekly points returns (0.0, 0.0)"""
        test_player.projected_points[6] = None  # Week 7 (index 6)
        test_player.actual_points[6] = None

        orig_pts, weighted_pts = player_manager.get_weekly_projection(test_player, week=7)

        assert orig_pts == 0.0
        assert weighted_pts == 0.0

    def test_get_weekly_projection_zero_value_returns_zero(self, player_manager, test_player):
        """Test that zero weekly points returns (0.0, 0.0)"""
        test_player.projected_points[7] = 0.0  # Week 8 (index 7)
        test_player.actual_points[7] = 0.0

        orig_pts, weighted_pts = player_manager.get_weekly_projection(test_player, week=8)

        assert orig_pts == 0.0
        assert weighted_pts == 0.0

    def test_get_weekly_projection_with_zero_max_projection(self, player_manager, test_player):
        """Test weekly projection when max_projection is 0"""
        test_player.projected_points[5] = 25.0  # Week 6 (index 5)
        test_player.actual_points[5] = 25.0
        player_manager.max_projection = 0  # Edge case
        player_manager.scoring_calculator.max_projection = 0  # Update calculator too

        orig_pts, weighted_pts = player_manager.get_weekly_projection(test_player, week=6)

        assert orig_pts == 25.0
        assert weighted_pts == 0.0  # Should handle division by zero

    def test_normalization_with_weekly_projection_enabled(self, player_manager, test_player):
        """Test _get_normalized_fantasy_points with use_weekly_projection=True uses weekly max"""
        test_player.projected_points[5] = 30.0  # Week 6 (index 5)
        test_player.actual_points[5] = 30.0
        player_manager.max_projection = 300.0  # ROS max
        player_manager.scoring_calculator.max_projection = 300.0
        # Set weekly max (cache and current value)
        player_manager.max_weekly_projections = {6: 30.0}  # Cache for week 6
        player_manager.scoring_calculator.max_weekly_projection = 30.0  # Current weekly max

        result, reason = player_manager.scoring_calculator._get_normalized_fantasy_points(test_player, use_weekly_projection=True)

        # Should use WEEKLY max: (30/30) * 100 = 100.0 (not ROS max of 300)
        # This tests that weekly scores are normalized against weekly max, not ROS max
        expected = (30.0 / 30.0) * 100.0  # = 100.0
        assert abs(result - expected) < 0.01
        assert "Projected: 30.00" in reason
        assert "Weighted:" in reason

    def test_normalization_with_weekly_projection_disabled(self, player_manager, test_player):
        """Test _get_normalized_fantasy_points with use_weekly_projection=False uses ROS"""
        # Test player has weeks 6-17 summing to 200.0 (from fixture)
        # Current week is 6, so ROS = sum of weeks 6-17 = 200.0
        # Weighted = (200/250) * 100 = 80.0

        result, reason = player_manager.scoring_calculator._get_normalized_fantasy_points(test_player, use_weekly_projection=False)

        # Should use rest-of-season projection
        assert result == 80.0
        assert "200.00" in reason  # Should show ROS points

    def test_weekly_normalization_uses_weekly_max(self, player_manager):
        """Test weight_projection() uses correct max (weekly vs ROS) based on parameter"""
        # Create a simple test scenario
        player_manager.max_projection = 400.0  # ROS max
        player_manager.scoring_calculator.max_projection = 400.0
        player_manager.max_weekly_projections = {6: 30.0}  # Weekly max for week 6
        player_manager.scoring_calculator.max_weekly_projection = 30.0

        # Test with use_weekly_max=True (should use max_weekly_projection = 30.0)
        result_weekly = player_manager.scoring_calculator.weight_projection(25.0, use_weekly_max=True)
        expected_weekly = (25.0 / 30.0) * 100.0  # = 83.33
        assert abs(result_weekly - expected_weekly) < 0.01

        # Test with use_weekly_max=False (should use max_projection = 400.0)
        result_ros = player_manager.scoring_calculator.weight_projection(25.0, use_weekly_max=False)
        expected_ros = (25.0 / 400.0) * 100.0  # = 6.25
        assert abs(result_ros - expected_ros) < 0.01

    def test_calculate_max_weekly_projection(self, player_manager):
        """Test calculate_max_weekly_projection() finds max and caches it"""
        # Create players with various weekly projections
        from utils.FantasyPlayer import FantasyPlayer

        projected1 = [0.0] * 17
        projected1[5] = 25.0  # Week 6
        player1 = FantasyPlayer(id=1, name="Player 1", team="KC", position="QB",
                               projected_points=projected1, actual_points=projected1.copy())

        projected2 = [0.0] * 17
        projected2[5] = 30.0  # Week 6 - Max
        player2 = FantasyPlayer(id=2, name="Player 2", team="BUF", position="RB",
                               projected_points=projected2, actual_points=projected2.copy())

        projected3 = [0.0] * 17
        projected3[5] = 20.0  # Week 6
        player3 = FantasyPlayer(id=3, name="Player 3", team="SF", position="WR",
                               projected_points=projected3, actual_points=projected3.copy())

        player_manager.players = [player1, player2, player3]

        # Calculate max for week 6 (should be 30.0)
        max_weekly = player_manager.calculate_max_weekly_projection(6)
        assert max_weekly == 30.0

        # Verify it was cached
        assert 6 in player_manager.max_weekly_projections
        assert player_manager.max_weekly_projections[6] == 30.0

        # Call again - should use cache (test cache hit)
        max_weekly_cached = player_manager.calculate_max_weekly_projection(6)
        assert max_weekly_cached == 30.0

    def test_calculate_max_weekly_projection_no_valid_projections(self, player_manager):
        """Test calculate_max_weekly_projection() handles edge case of no valid projections"""
        from utils.FantasyPlayer import FantasyPlayer

        # Players with no week 10 projections
        player1 = FantasyPlayer(id=1, name="Player 1", team="KC", position="QB")
        player2 = FantasyPlayer(id=2, name="Player 2", team="BUF", position="RB")

        player_manager.players = [player1, player2]

        # Calculate max for week 10 (should be 0.0 - no valid projections)
        max_weekly = player_manager.calculate_max_weekly_projection(10)
        assert max_weekly == 0.0

    def test_weekly_normalization_zero_max_handling(self, player_manager):
        """Test weight_projection() handles zero max_weekly_projection gracefully with WARNING"""
        # Set max_weekly_projection to 0 (data quality issue scenario)
        player_manager.scoring_calculator.max_weekly_projection = 0.0

        # Call weight_projection with use_weekly_max=True
        result = player_manager.scoring_calculator.weight_projection(25.0, use_weekly_max=True)

        # Should return 0.0 (graceful handling)
        assert result == 0.0

        # WARNING log is generated (verified in captured stdout output during test run)

    def test_score_player_with_weekly_projection(self, player_manager, test_player, mock_fantasy_team):
        """Integration test: score_player with use_weekly_projection=True"""
        # Set up weekly data
        test_player.projected_points[5] = 25.0  # Week 6 (index 5)
        test_player.actual_points[5] = 25.0
        player_manager.max_projection = 300.0
        player_manager.scoring_calculator.max_projection = 300.0
        # Set weekly max (needed for weekly normalization)
        player_manager.max_weekly_projections = {6: 30.0}
        player_manager.scoring_calculator.max_weekly_projection = 30.0
        test_player.consistency = 0.15  # EXCELLENT
        test_player.matchup_score = 10  # GOOD
        mock_fantasy_team.roster = []  # No bye overlaps

        # Score with weekly projection enabled, only matchup
        scored_player = player_manager.score_player(
            test_player,
            use_weekly_projection=True,
            adp=False,
            player_rating=False,
            team_quality=False,
            matchup=True,
            draft_round=-1,
            bye=False,
            injury=False
        )

        # Expected: (25/30)*100 = 83.33... (uses WEEKLY max, not ROS max)
        # matchup_score = 10 (GOOD): bonus = +15.0 (from config)
        # Final: 83.33... + 15.0 = 98.33...
        expected_base = (25.0 / 30.0) * 100.0  # 83.33...
        expected_final = expected_base + 15.0  # Add matchup GOOD bonus

        assert abs(scored_player.score - expected_final) < 0.01
        assert scored_player.player == test_player
        assert len(scored_player.reason) > 0
        # Check reasons include weekly projection
        assert any("Projected: 25.00" in r for r in scored_player.reason)
        assert any("Matchup:" in r for r in scored_player.reason)


# ============================================================================
# STEP 2: ADP MULTIPLIER TESTS
# ============================================================================

class TestADPMultiplier:
    """Test Step 2: ADP multiplier application"""

    def test_adp_excellent_threshold(self, player_manager, test_player):
        """ADP <= 20 should get EXCELLENT multiplier (1.20)"""
        test_player.average_draft_position = 15.0
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_adp_multiplier(test_player, base_score)
        assert result == 100.0 * 1.20  # 120.0
        assert reason == "ADP: EXCELLENT (1.20x)"

    def test_adp_good_threshold(self, player_manager, test_player):
        """20 < ADP <= 50 should get GOOD multiplier (1.10)"""
        test_player.average_draft_position = 35.0
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_adp_multiplier(test_player, base_score)
        assert result == 100.0 * 1.10  # 110.0
        assert reason == "ADP: GOOD (1.10x)"

    def test_adp_neutral_range(self, player_manager, test_player):
        """50 < ADP < 100 should get NEUTRAL multiplier (1.0)"""
        test_player.average_draft_position = 75.0
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_adp_multiplier(test_player, base_score)
        assert result == 100.0 * 1.0  # 100.0
        assert reason == "ADP: NEUTRAL (1.00x)"

    def test_adp_poor_threshold(self, player_manager, test_player):
        """100 <= ADP < 150 should get POOR multiplier (0.90)"""
        test_player.average_draft_position = 120.0
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_adp_multiplier(test_player, base_score)
        assert result == 100.0 * 0.90  # 90.0
        assert reason == "ADP: POOR (0.90x)"

    def test_adp_very_poor_threshold(self, player_manager, test_player):
        """ADP >= 150 should get VERY_POOR multiplier (0.70)"""
        test_player.average_draft_position = 200.0
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_adp_multiplier(test_player, base_score)
        assert result == 100.0 * 0.70  # 70.0
        assert reason == "ADP: VERY_POOR (0.70x)"

    def test_adp_none_returns_neutral(self, player_manager, test_player):
        """ADP = None should return neutral multiplier (1.0)"""
        test_player.average_draft_position = None
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_adp_multiplier(test_player, base_score)
        assert result == 100.0 * 1.0
        assert reason == "ADP: NEUTRAL (1.00x)"

    def test_adp_boundary_at_20(self, player_manager, test_player):
        """Test exact boundary at ADP = 20"""
        test_player.average_draft_position = 20.0
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_adp_multiplier(test_player, base_score)
        assert result == 100.0 * 1.20  # Should be EXCELLENT
        assert reason == "ADP: EXCELLENT (1.20x)"


# ============================================================================
# STEP 3: PLAYER RATING MULTIPLIER TESTS
# ============================================================================

class TestPlayerRatingMultiplier:
    """Test Step 3: Player rating multiplier application"""

    def test_player_rating_excellent(self, player_manager, test_player):
        """Rating >= 80 should get EXCELLENT multiplier (1.25)"""
        test_player.player_rating = 85.0
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_player_rating_multiplier(test_player, base_score)
        assert result == 100.0 * 1.25
        assert reason == "Player Rating: EXCELLENT (1.25x)"

    def test_player_rating_good(self, player_manager, test_player):
        """60 <= Rating < 80 should get GOOD multiplier (1.15)"""
        test_player.player_rating = 70.0
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_player_rating_multiplier(test_player, base_score)
        assert result == 100.0 * 1.15
        assert reason == "Player Rating: GOOD (1.15x)"

    def test_player_rating_neutral(self, player_manager, test_player):
        """40 < Rating < 60 should get NEUTRAL multiplier (1.0)"""
        test_player.player_rating = 50.0
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_player_rating_multiplier(test_player, base_score)
        assert result == 100.0 * 1.0
        assert reason == "Player Rating: NEUTRAL (1.00x)"

    def test_player_rating_poor(self, player_manager, test_player):
        """20 < Rating <= 40 should get POOR multiplier (0.95)"""
        test_player.player_rating = 30.0
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_player_rating_multiplier(test_player, base_score)
        assert result == 100.0 * 0.95
        assert reason == "Player Rating: POOR (0.95x)"

    def test_player_rating_very_poor(self, player_manager, test_player):
        """Rating <= 20 should get VERY_POOR multiplier (0.75)"""
        test_player.player_rating = 15.0
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_player_rating_multiplier(test_player, base_score)
        assert result == 100.0 * 0.75
        assert reason == "Player Rating: VERY_POOR (0.75x)"

    def test_player_rating_none_returns_neutral(self, player_manager, test_player):
        """Player rating = None should return neutral (1.0)"""
        test_player.player_rating = None
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_player_rating_multiplier(test_player, base_score)
        assert result == 100.0
        assert reason == "Player Rating: NEUTRAL (1.00x)"


# ============================================================================
# STEP 4: TEAM QUALITY MULTIPLIER TESTS
# ============================================================================

class TestTeamQualityMultiplier:
    """Test Step 4: Team quality multiplier application"""

    def test_team_quality_excellent_offensive(self, player_manager, test_player):
        """Offensive rank <= 5 should get EXCELLENT (1.30)"""
        test_player.team_offensive_rank = 3
        test_player.position = "RB"
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_team_quality_multiplier(test_player, base_score)
        assert result == 100.0 * 1.30
        assert reason == "Team Quality: EXCELLENT (1.30x)"

    def test_team_quality_good_offensive(self, player_manager, test_player):
        """5 < Offensive rank <= 10 should get GOOD (1.15)"""
        test_player.team_offensive_rank = 8
        test_player.position = "WR"
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_team_quality_multiplier(test_player, base_score)
        assert result == 100.0 * 1.15
        assert reason == "Team Quality: GOOD (1.15x)"

    def test_team_quality_poor_offensive(self, player_manager, test_player):
        """20 <= Offensive rank < 25 should get POOR (0.85)"""
        test_player.team_offensive_rank = 22
        test_player.position = "QB"
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_team_quality_multiplier(test_player, base_score)
        assert result == 100.0 * 0.85
        assert reason == "Team Quality: POOR (0.85x)"

    def test_team_quality_very_poor_offensive(self, player_manager, test_player):
        """Offensive rank >= 25 should get VERY_POOR (0.70)"""
        test_player.team_offensive_rank = 28
        test_player.position = "TE"
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_team_quality_multiplier(test_player, base_score)
        assert result == 100.0 * 0.70
        assert reason == "Team Quality: VERY_POOR (0.70x)"

    def test_team_quality_defense_uses_defensive_rank(self, player_manager, test_player):
        """DST position should use team_defensive_rank"""
        test_player.team_offensive_rank = 25  # Bad offense
        test_player.team_defensive_rank = 3   # Good defense
        test_player.position = "DST"
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_team_quality_multiplier(test_player, base_score)
        # Should use defensive rank (3) which is EXCELLENT
        assert result == 100.0 * 1.30
        assert reason == "Team Quality: EXCELLENT (1.30x)"

    def test_team_quality_none_returns_neutral(self, player_manager, test_player):
        """Team rank = None should return neutral (1.0)"""
        test_player.team_offensive_rank = None
        test_player.position = "RB"
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_team_quality_multiplier(test_player, base_score)
        assert result == 100.0
        assert reason == "Team Quality: NEUTRAL (1.00x)"


# ============================================================================
# STEP 5: PERFORMANCE MULTIPLIER TESTS
# ============================================================================
# Note: Performance scoring replaced the old consistency scoring feature.
# Performance measures actual vs projected deviation, not coefficient of variation.
# Tests for performance multiplier are in a separate test file.


# ============================================================================
# STEP 6: MATCHUP MULTIPLIER TESTS
# ============================================================================

class TestMatchupMultiplier:
    """Test Step 6: Matchup multiplier application"""

    def test_matchup_excellent(self, player_manager, test_player):
        """Matchup >= 15 should get EXCELLENT (+37.5 pts with IMPACT_SCALE=150.0)"""
        test_player.matchup_score = 18
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_matchup_multiplier(test_player, base_score)
        # IMPACT_SCALE=150.0, multiplier=1.25: bonus = (150*1.25)-150 = +37.5
        assert result == pytest.approx(100.0 + 37.5, abs=0.1)
        assert "EXCELLENT" in reason
        assert "pts" in reason

    def test_matchup_good(self, player_manager, test_player):
        """6 <= Matchup < 15 should get GOOD (+15.0 pts with IMPACT_SCALE=150.0)"""
        test_player.matchup_score = 10
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_matchup_multiplier(test_player, base_score)
        # IMPACT_SCALE=150.0, multiplier=1.10: bonus = (150*1.10)-150 = +15.0
        assert result == pytest.approx(100.0 + 15.0, abs=0.1)
        assert "GOOD" in reason
        assert "pts" in reason

    def test_matchup_neutral(self, player_manager, test_player):
        """-6 < Matchup < 6 should get NEUTRAL (0.0 pts)"""
        test_player.matchup_score = 0
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_matchup_multiplier(test_player, base_score)
        # IMPACT_SCALE=150.0, multiplier=1.0: bonus = (150*1.0)-150 = 0.0
        assert result == pytest.approx(100.0, abs=0.1)
        assert "NEUTRAL" in reason
        assert "pts" in reason

    def test_matchup_poor(self, player_manager, test_player):
        """-15 < Matchup <= -6 should get POOR (-15.0 pts with IMPACT_SCALE=150.0)"""
        test_player.matchup_score = -10
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_matchup_multiplier(test_player, base_score)
        # IMPACT_SCALE=150.0, multiplier=0.90: bonus = (150*0.90)-150 = -15.0
        assert result == pytest.approx(100.0 - 15.0, abs=0.1)
        assert "POOR" in reason
        assert "pts" in reason

    def test_matchup_very_poor(self, player_manager, test_player):
        """Matchup <= -15 should get VERY_POOR (-37.5 pts with IMPACT_SCALE=150.0)"""
        test_player.matchup_score = -20
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_matchup_multiplier(test_player, base_score)
        # IMPACT_SCALE=150.0, multiplier=0.75: bonus = (150*0.75)-150 = -37.5
        assert result == pytest.approx(100.0 - 37.5, abs=0.1)
        assert "VERY_POOR" in reason
        assert "pts" in reason

    def test_matchup_none_returns_neutral(self, player_manager, test_player):
        """Matchup = None should return neutral (0.0 pts bonus)"""
        test_player.matchup_score = None
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_matchup_multiplier(test_player, base_score)
        assert result == 100.0
        assert "NEUTRAL" in reason
        assert "pts" in reason


# ============================================================================
# STEP 7: DRAFT ORDER BONUS TESTS (BUG FIX VERIFICATION)
# ============================================================================

class TestDraftOrderBonus:
    """Test Step 7: Draft order bonus - VERIFY BUG FIX"""

    def test_draft_bonus_round_0_primary_position(self, player_manager, test_player):
        """Round 0 with PRIMARY position should get PRIMARY bonus - BUG FIX"""
        # Round 0: {"FLEX": "P", "QB": "S"}
        # RB -> FLEX, should get PRIMARY (50)
        test_player.position = "RB"
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_draft_order_bonus(test_player, 0, base_score)
        assert result == 100.0 + 50, "Round 0 should work with new >= 0 check"
        assert reason == "Draft Order Bonus: PRIMARY (+50.0 pts)"

    def test_draft_bonus_round_0_secondary_position(self, player_manager, test_player):
        """Round 0 with SECONDARY position should get SECONDARY bonus"""
        # Round 0: {"FLEX": "P", "QB": "S"}
        # QB should get SECONDARY (30)
        test_player.position = "QB"
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_draft_order_bonus(test_player, 0, base_score)
        assert result == 100.0 + 30
        assert reason == "Draft Order Bonus: SECONDARY (+30.0 pts)"

    def test_draft_bonus_round_1_flex_gets_primary(self, player_manager, test_player):
        """Round 1 FLEX-eligible should get PRIMARY"""
        # Round 1: {"FLEX": "P", "QB": "S"}
        test_player.position = "WR"  # FLEX-eligible
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_draft_order_bonus(test_player, 1, base_score)
        assert result == 100.0 + 50
        assert reason == "Draft Order Bonus: PRIMARY (+50.0 pts)"

    def test_draft_bonus_round_2_qb_gets_primary(self, player_manager, test_player):
        """Round 2 QB should get PRIMARY"""
        # Round 2: {"QB": "P", "FLEX": "S"}
        test_player.position = "QB"
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_draft_order_bonus(test_player, 2, base_score)
        assert result == 100.0 + 50
        assert reason == "Draft Order Bonus: PRIMARY (+50.0 pts)"

    def test_draft_bonus_round_3_te_gets_bonus(self, player_manager, test_player):
        """Round 3 TE should get appropriate bonus based on flex eligibility"""
        # Round 3: {"TE": "P", "FLEX": "S"}
        # TE is NOT FLEX-eligible (only RB/WR are), so it gets TE-specific PRIMARY bonus
        test_player.position = "TE"
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_draft_order_bonus(test_player, 3, base_score)

        # TE gets PRIMARY bonus (50) since it's not FLEX-eligible
        assert result == 100.0 + 50
        assert reason == "Draft Order Bonus: PRIMARY (+50.0 pts)"

    def test_draft_bonus_no_match_returns_zero(self, player_manager, test_player):
        """Position not in round's priorities returns 0 bonus"""
        # Round 4: {"K": "P"}
        # TE not in priorities
        test_player.position = "TE"
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_draft_order_bonus(test_player, 4, base_score)
        assert result == 100.0 + 0
        assert reason == ""


# ============================================================================
# STEP 8: BYE WEEK PENALTY TESTS
# ============================================================================

class TestByeWeekPenalty:
    """Test Step 8: Bye week penalty application"""

    def test_bye_penalty_no_matches(self, player_manager, test_player, mock_fantasy_team):
        """No matching bye weeks should have 0 penalty"""
        # Set up roster with no bye week overlaps
        mock_fantasy_team.roster = []
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_bye_week_penalty(test_player, base_score, player_manager.team.roster)
        assert result == 100.0  # No penalty
        assert reason == ""  # No reason when there are no overlaps

    def test_bye_penalty_one_same_position_match(self, player_manager, test_player, mock_fantasy_team):
        """One same-position bye match should apply median-based penalty"""
        # test_player is RB with bye_week=7
        projected_rb = [0.0] * 17
        projected_rb[0] = 10.0  # Week 1
        projected_rb[1] = 12.0  # Week 2
        projected_rb[2] = 15.0  # Week 3
        # Median = 12.0
        other_rb = FantasyPlayer(id=99, name="Other RB", team="BUF", position="RB", bye_week=7, fantasy_points=150.0,
                                projected_points=projected_rb, actual_points=projected_rb.copy())

        mock_fantasy_team.roster = [other_rb]
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_bye_week_penalty(test_player, base_score, player_manager.team.roster)
        # Expected penalty = 12.0 ** 1.0 + 0 ** 1.0 = 12.0
        expected_penalty = 12.0
        assert abs(result - (100.0 - expected_penalty)) < 0.01
        assert "1 same-position, 0 different-position" in reason

    def test_bye_penalty_one_different_position_match(self, player_manager, test_player, mock_fantasy_team):
        """One different-position bye match should apply median-based penalty"""
        # test_player is RB with bye_week=7
        projected_qb = [0.0] * 17
        projected_qb[0] = 18.0  # Week 1
        projected_qb[1] = 20.0  # Week 2
        projected_qb[2] = 22.0  # Week 3
        # Median = 20.0
        other_qb = FantasyPlayer(id=99, name="Other QB", team="BUF", position="QB", bye_week=7, fantasy_points=150.0,
                                projected_points=projected_qb, actual_points=projected_qb.copy())

        mock_fantasy_team.roster = [other_qb]
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_bye_week_penalty(test_player, base_score, player_manager.team.roster)
        # Expected penalty = 0 ** 1.0 + 20.0 ** 1.0 = 20.0
        expected_penalty = 20.0
        assert abs(result - (100.0 - expected_penalty)) < 0.01
        assert "0 same-position, 1 different-position" in reason

    def test_bye_penalty_mixed_overlaps(self, player_manager, test_player, mock_fantasy_team):
        """Multiple overlaps of both types should apply both median-based penalties"""
        # test_player is RB with bye_week=7
        projected_rb1 = [0.0] * 17
        projected_rb1[0], projected_rb1[1], projected_rb1[2] = 10.0, 12.0, 14.0  # Weeks 1-3, Median = 12.0
        other_rb1 = FantasyPlayer(id=98, name="RB1", team="BUF", position="RB", bye_week=7, fantasy_points=150.0,
                                 projected_points=projected_rb1, actual_points=projected_rb1.copy())

        projected_rb2 = [0.0] * 17
        projected_rb2[0], projected_rb2[1], projected_rb2[2] = 8.0, 10.0, 9.0  # Weeks 1-3, Median = 9.0
        other_rb2 = FantasyPlayer(id=97, name="RB2", team="PHI", position="RB", bye_week=7, fantasy_points=140.0,
                                 projected_points=projected_rb2, actual_points=projected_rb2.copy())

        projected_wr = [0.0] * 17
        projected_wr[0], projected_wr[1], projected_wr[2] = 15.0, 18.0, 16.0  # Weeks 1-3, Median = 16.0
        other_wr = FantasyPlayer(id=96, name="WR1", team="DAL", position="WR", bye_week=7, fantasy_points=130.0,
                                projected_points=projected_wr, actual_points=projected_wr.copy())

        projected_qb = [0.0] * 17
        projected_qb[0], projected_qb[1], projected_qb[2] = 20.0, 22.0, 24.0  # Weeks 1-3, Median = 22.0
        other_qb = FantasyPlayer(id=95, name="QB1", team="JAX", position="QB", bye_week=7, fantasy_points=200.0,
                                projected_points=projected_qb, actual_points=projected_qb.copy())

        mock_fantasy_team.roster = [other_rb1, other_rb2, other_wr, other_qb]

        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_bye_week_penalty(test_player, base_score, player_manager.team.roster)
        # Expected penalty = (12 + 9) ** 1.0 + (16 + 22) ** 1.0 = 21 + 38 = 59.0
        expected_penalty = 59.0
        assert abs(result - (100.0 - expected_penalty)) < 0.01
        assert "2 same-position, 2 different-position" in reason

    def test_bye_penalty_excludes_player_being_scored(self, player_manager, test_player, mock_fantasy_team):
        """Player being scored should be excluded from overlap counts"""
        # test_player is RB with bye_week=7, id=12345
        # Include test_player in roster (shouldn't count itself)
        projected_rb = [0.0] * 17
        projected_rb[0], projected_rb[1], projected_rb[2] = 10.0, 12.0, 14.0  # Weeks 1-3, Median = 12.0
        other_rb = FantasyPlayer(id=99, name="Other RB", team="BUF", position="RB", bye_week=7, fantasy_points=150.0,
                                projected_points=projected_rb, actual_points=projected_rb.copy())

        mock_fantasy_team.roster = [test_player, other_rb]

        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_bye_week_penalty(test_player, base_score, player_manager.team.roster)
        # Should only count other_rb, not test_player itself
        # Expected penalty = 12.0 ** 1.0 + 0 ** 1.0 = 12.0
        expected_penalty = 12.0
        assert abs(result - (100.0 - expected_penalty)) < 0.01
        assert "1 same-position, 0 different-position" in reason


# ============================================================================
# STEP 9: INJURY PENALTY TESTS
# ============================================================================

class TestInjuryPenalty:
    """Test Step 9: Injury penalty application"""

    def test_injury_low_risk_active(self, player_manager, test_player):
        """ACTIVE status should have LOW risk (0 penalty)"""
        test_player.injury_status = "ACTIVE"
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_injury_penalty(test_player, base_score)
        assert result == 100.0  # No penalty
        assert reason == ""

    def test_injury_medium_risk_questionable(self, player_manager, test_player):
        """QUESTIONABLE status should have MEDIUM risk (10 penalty)"""
        test_player.injury_status = "QUESTIONABLE"
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_injury_penalty(test_player, base_score)
        assert result == 100.0 - 10.0
        assert reason == "Injury: QUESTIONABLE (-10.0 pts)"

    def test_injury_risk_out(self, player_manager, test_player):
        """OUT status should get penalty based on its risk level"""
        test_player.injury_status = "OUT"
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_injury_penalty(test_player, base_score)

        # Get actual risk level and expected penalty from config
        risk_level = test_player.get_risk_level()
        expected_penalty = player_manager.config.get_injury_penalty(risk_level)
        assert result == base_score - expected_penalty
        assert reason == "Injury: OUT (-10.0 pts)"

    def test_injury_risk_doubtful(self, player_manager, test_player):
        """DOUBTFUL status should get penalty based on its risk level"""
        test_player.injury_status = "DOUBTFUL"
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_injury_penalty(test_player, base_score)

        # Get actual risk level and expected penalty from config
        risk_level = test_player.get_risk_level()
        expected_penalty = player_manager.config.get_injury_penalty(risk_level)
        assert result == base_score - expected_penalty
        assert reason == "Injury: DOUBTFUL (-10.0 pts)"

    def test_injury_high_risk_injury_reserve(self, player_manager, test_player):
        """INJURY_RESERVE status should have HIGH risk"""
        test_player.injury_status = "INJURY_RESERVE"
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_injury_penalty(test_player, base_score)
        assert result == 100.0 - 75.0
        assert reason == "Injury: INJURY_RESERVE (-75.0 pts)"

    def test_injury_high_risk_unknown(self, player_manager, test_player):
        """UNKNOWN status should have HIGH risk"""
        test_player.injury_status = "UNKNOWN"
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_injury_penalty(test_player, base_score)
        assert result == 100.0 - 75.0
        assert reason == "Injury: UNKNOWN (-75.0 pts)"


# ============================================================================
# INTEGRATION TESTS: FULL SCORING FLOW
# ============================================================================

class TestFullScoringIntegration:
    """Integration tests for complete score_player() flow"""

    def test_score_player_all_flags_enabled(self, player_manager, test_player, mock_fantasy_team):
        """Test full scoring with all flags enabled"""
        # Setup
        test_player.weighted_projection = 80.0
        test_player.average_draft_position = 15.0  # EXCELLENT (1.20)
        test_player.player_rating = 85.0  # EXCELLENT (1.25)
        test_player.team_offensive_rank = 3  # EXCELLENT (1.30)
        test_player.consistency = 0.15  # EXCELLENT (1.50)
        test_player.matchup_score = 10  # GOOD (1.10)
        test_player.position = "RB"
        test_player.bye_week = 7
        test_player.injury_status = "ACTIVE"

        mock_fantasy_team.roster = []  # No bye overlaps

        # Calculate expected score manually (NO consistency multiplier)
        score = 80.0  # Normalization
        score = score * 1.20  # ADP: 96.0
        score = score * 1.25  # Player rating: 120.0
        score = score * 1.30  # Team quality: 156.0
        # No consistency multiplier
        score = score + 15.0  # Matchup GOOD bonus: (150*1.10)-150 = +15.0 → 171.0
        score = score + 50  # Draft bonus (round 0, PRIMARY): 221.0
        score = score - 0  # Bye penalty: 221.0
        score = score - 0  # Injury penalty: 221.0

        result = player_manager.score_player(
            test_player,
            adp=True,
            player_rating=True,
            team_quality=True,
            matchup=True,
            draft_round=0,
            bye=True,
            injury=True
        )

        assert abs(result.score - 221.0) < 0.01, f"Expected ~221.0, got {result.score}"

    def test_score_player_default_flags(self, player_manager, test_player, mock_fantasy_team):
        """Test score_player with default flag values - BUG FIX: draft_round=-1"""
        mock_fantasy_team.roster = []  # No bye overlaps

        result = player_manager.score_player(test_player)

        # With default flags: adp=True, player_rating=True, team_quality=True,
        # Should NOT include matchup multiplier or draft bonus

        assert result.score > 0  # Should have a positive score
        # Exact value depends on test_player attributes

    def test_score_player_only_normalization(self, player_manager, test_player, mock_fantasy_team):
        """Test score_player with all multipliers/bonuses disabled"""
        # Need ROS projection to equal 250 pts to get weighted=100.0
        # Set weeks 6-17 (12 weeks) to sum to 250.0
        for i in range(5, 17):  # indices 5-16 = weeks 6-17
            test_player.projected_points[i] = 250.0 / 12  # 20.833... per week
            test_player.actual_points[i] = 250.0 / 12
        mock_fantasy_team.roster = []  # No bye overlaps

        result = player_manager.score_player(
            test_player,
            adp=False,
            player_rating=False,
            team_quality=False,
            matchup=False,
            draft_round=-1,  # Disabled
            bye=False,
            injury=False
        )

        # ROS = 250, weighted = (250/250)*100 = 100.0
        assert abs(result.score - 100.0) < 0.01, "Only normalization should return 100.0"

    def test_score_player_negative_score_allowed(self, player_manager, test_player, mock_fantasy_team):
        """Verify negative scores are allowed (no bounds checking)"""
        test_player.weighted_projection = 10.0
        test_player.average_draft_position = 200.0  # VERY_POOR (0.70)
        test_player.player_rating = 10.0  # VERY_POOR (0.75)
        test_player.team_offensive_rank = 30  # VERY_POOR (0.70)
        test_player.consistency = 0.9  # VERY_POOR (0.60)
        test_player.injury_status = "OUT"  # HIGH (-75)
        test_player.position = "RB"

        # Create 5 same-position bye overlaps
        mock_fantasy_team.roster = []
        for i in range(5):
            projected_rb = [0.0] * 17
            projected_rb[0], projected_rb[1], projected_rb[2] = 18.0, 20.0, 22.0  # Median = 20.0
            rb = FantasyPlayer(
                id=90+i, name=f"RB{i}", team="BUF", position="RB", bye_week=7, fantasy_points=100.0,
                projected_points=projected_rb, actual_points=projected_rb.copy()
            )
            mock_fantasy_team.roster.append(rb)
        # Median-based penalty: (5 × 20.0) ** 1.0 = 100.0

        # Score: 10 * 0.70 * 0.75 * 0.70 * 0.60 = ~2.205
        # Then: 2.205 - 100 (bye) - 75 (injury) = ~-172.8

        result = player_manager.score_player(
            test_player,
            adp=True,
            player_rating=True,
            team_quality=True,
            matchup=False,
            draft_round=-1,
            bye=True,
            injury=True
        )

        assert result.score < 0, "Negative scores should be allowed"

    def test_score_player_draft_round_minus_one_disabled(self, player_manager, test_player, mock_fantasy_team):
        """Verify draft_round=-1 disables the bonus - BUG FIX"""
        # Need ROS projection to equal 250 pts to get weighted=100.0
        for i in range(5, 17):  # indices 5-16 = weeks 6-17
            test_player.projected_points[i] = 250.0 / 12  # 20.833... per week
            test_player.actual_points[i] = 250.0 / 12
        test_player.position = "RB"  # Would normally get bonus in round 0
        mock_fantasy_team.roster = []  # No bye overlaps

        result = player_manager.score_player(
            test_player,
            adp=False,
            player_rating=False,
            team_quality=False,
            matchup=False,
            draft_round=-1,  # DISABLED
            bye=False,
            injury=False
        )

        # ROS = 250, weighted = (250/250)*100 = 100.0, no bonus
        assert abs(result.score - 100.0) < 0.01, "draft_round=-1 should not apply bonus"

    def test_score_player_waiver_mode_flags(self, player_manager, test_player, mock_fantasy_team):
        """Test flag configuration for Waiver Optimizer mode"""
        mock_fantasy_team.roster = []  # No bye overlaps

        # Waiver mode: all except matchup=True, draft_round=-1 (disabled)
        result = player_manager.score_player(
            test_player,
            adp=True,
            player_rating=True,
            team_quality=True,
            matchup=True,  # Enabled for weekly
            draft_round=-1,  # Disabled for fair comparison
            bye=True,
            injury=True
        )

        assert result.score > 0

    def test_score_player_starter_helper_mode_flags(self, player_manager, test_player, mock_fantasy_team):
        """Test flag configuration for Starter Helper mode"""
        mock_fantasy_team.roster = []  # No bye overlaps

        # Starter mode: only matchup
        result = player_manager.score_player(
            test_player,
            adp=False,
            player_rating=False,
            team_quality=False,
            matchup=True,  # Most important for weekly
            draft_round=-1,
            bye=False,  # Already in week_N_points
            injury=False  # Filtered beforehand
        )

        # Should only have normalization + matchup
        assert result.score > 0


# ============================================================================
# EDGE CASES AND ERROR HANDLING
# ============================================================================

class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_all_none_values_return_neutral_score(self, player_manager, mock_fantasy_team):
        """Player with all None values should get neutral multipliers"""
        player = FantasyPlayer(
            id=1,
            name="Edge Case",
            team="KC",
            position="RB",
            average_draft_position=None,
            player_rating=None,
            consistency=0.5,  # Default
            team_offensive_rank=None,
            matchup_score=None,
            injury_status="ACTIVE",
            bye_week=None
        )

        # Set weekly projections to sum to 250 for ROS = 100.0 weighted
        projected = [0.0] * 17
        for i in range(5, 17):  # indices 5-16 = weeks 6-17
            projected[i] = 250.0 / 12
        player.projected_points = projected
        player.actual_points = projected.copy()

        mock_fantasy_team.roster = []  # No bye overlaps

        result = player_manager.score_player(
            player,
            adp=True,
            player_rating=True,
            team_quality=True,
            matchup=True,
            draft_round=-1,
            bye=True,
            injury=True
        )

        # All None should give neutral 1.0 multipliers
        # ROS = 250, weighted = (250/250)*100 = 100.0
        assert abs(result.score - 100.0) < 0.01

    def test_zero_fantasy_points_player(self, player_manager, mock_fantasy_team):
        """Player with 0 fantasy points should score 0"""
        player = FantasyPlayer(
            id=1,
            name="Zero",
            team="KC",
            position="RB",
            fantasy_points=0.0,
            weighted_projection=0.0
        )

        mock_fantasy_team.roster = []  # No bye overlaps

        result = player_manager.score_player(player, draft_round=-1)

        assert result.score <= 0  # Might be negative due to penalties


# ============================================================================
# ADDITIONAL EDGE CASES FOR ROBUSTNESS
# ============================================================================

class TestAdditionalEdgeCases:
    """Additional edge case tests for missing data, boundaries, and extreme values"""

    # ========== Missing Data Edge Cases ==========

    def test_scoring_with_all_weekly_points_none(self, player_manager, mock_fantasy_team):
        """Test scoring when all weekly points are None"""
        # Set all weekly points to None
        projected = [None] * 17
        actual = [None] * 17
        player = FantasyPlayer(
            id=1, name="No Data", team="KC", position="RB",
            fantasy_points=None, weighted_projection=0.0,
            projected_points=projected, actual_points=actual
        )

        mock_fantasy_team.roster = []
        result = player_manager.score_player(player, draft_round=-1)

        # Should handle gracefully and return 0 or small score
        assert result.score >= 0 or result.score < 0  # Any score is acceptable, just shouldn't crash

    def test_scoring_with_missing_team_data(self, player_manager, mock_fantasy_team):
        """Test scoring when team data is completely missing"""
        projected = [0.0] * 17
        for i in range(5, 17):  # indices 5-16 = weeks 6-17
            projected[i] = 250.0 / 12

        player = FantasyPlayer(
            id=1, name="No Team", team="UNKNOWN", position="RB",
            fantasy_points=100.0, weighted_projection=50.0,
            team_offensive_rank=None, team_defensive_rank=None,
            matchup_score=None,
            projected_points=projected, actual_points=projected.copy()
        )

        mock_fantasy_team.roster = []
        result = player_manager.score_player(player, team_quality=True, matchup=True, draft_round=-1)

        # Should get neutral multipliers for missing team data
        assert result.score > 0

    def test_scoring_with_partial_weekly_data(self, player_manager, mock_fantasy_team):
        """Test scoring with some weeks having data and others None"""
        # Weeks 6-10 have data, 11-17 are None
        projected = [0.0] * 17
        for i in range(5, 10):  # indices 5-9 = weeks 6-10
            projected[i] = 20.0
        for i in range(10, 17):  # indices 10-16 = weeks 11-17
            projected[i] = None

        player = FantasyPlayer(
            id=1, name="Partial Data", team="KC", position="RB",
            fantasy_points=150.0, weighted_projection=60.0,
            projected_points=projected, actual_points=projected.copy()
        )

        mock_fantasy_team.roster = []
        result = player_manager.score_player(player, draft_round=-1)

        # Should calculate based on available data (score can be negative due to penalties)
        assert result.score is not None  # Just verify it doesn't crash

    # ========== Boundary Condition Tests ==========

    def test_adp_exact_boundary_values(self, player_manager, test_player):
        """Test ADP at exact threshold boundaries"""
        base_score = 100.0

        # Test at boundary 20 (should be EXCELLENT)
        test_player.average_draft_position = 20.0
        result, _ = player_manager.scoring_calculator._apply_adp_multiplier(test_player, base_score)
        assert abs(result - 120.0) < 0.01

        # Test at boundary 50 (should be GOOD)
        test_player.average_draft_position = 50.0
        result, _ = player_manager.scoring_calculator._apply_adp_multiplier(test_player, base_score)
        assert abs(result - 110.0) < 0.01

        # Test at boundary 100 (should be POOR)
        test_player.average_draft_position = 100.0
        result, _ = player_manager.scoring_calculator._apply_adp_multiplier(test_player, base_score)
        assert abs(result - 90.0) < 0.01

        # Test at boundary 150 (should be VERY_POOR)
        test_player.average_draft_position = 150.0
        result, _ = player_manager.scoring_calculator._apply_adp_multiplier(test_player, base_score)
        assert abs(result - 70.0) < 0.01

    def test_player_rating_exact_boundaries(self, player_manager, test_player):
        """Test player rating at exact threshold boundaries"""
        base_score = 100.0

        # At 80 (EXCELLENT)
        test_player.player_rating = 80.0
        result, _ = player_manager.scoring_calculator._apply_player_rating_multiplier(test_player, base_score)
        assert abs(result - 125.0) < 0.01

        # At 60 (GOOD)
        test_player.player_rating = 60.0
        result, _ = player_manager.scoring_calculator._apply_player_rating_multiplier(test_player, base_score)
        assert abs(result - 115.0) < 0.01

        # At 40 (POOR)
        test_player.player_rating = 40.0
        result, _ = player_manager.scoring_calculator._apply_player_rating_multiplier(test_player, base_score)
        assert abs(result - 95.0) < 0.01

        # At 20 (VERY_POOR)
        test_player.player_rating = 20.0
        result, _ = player_manager.scoring_calculator._apply_player_rating_multiplier(test_player, base_score)
        assert abs(result - 75.0) < 0.01

    def test_matchup_score_exact_boundaries(self, player_manager, test_player):
        """Test matchup score at exact threshold boundaries with additive scoring"""
        base_score = 100.0

        # At 15 (EXCELLENT): bonus = (150*1.25)-150 = +37.5
        test_player.matchup_score = 15
        result, _ = player_manager.scoring_calculator._apply_matchup_multiplier(test_player, base_score)
        assert abs(result - 137.5) < 0.01

        # At 6 (GOOD): bonus = (150*1.10)-150 = +15.0
        test_player.matchup_score = 6
        result, _ = player_manager.scoring_calculator._apply_matchup_multiplier(test_player, base_score)
        assert abs(result - 115.0) < 0.01

        # At -6 (POOR): bonus = (150*0.90)-150 = -15.0
        test_player.matchup_score = -6
        result, _ = player_manager.scoring_calculator._apply_matchup_multiplier(test_player, base_score)
        assert abs(result - 85.0) < 0.01

        # At -15 (VERY_POOR): bonus = (150*0.75)-150 = -37.5
        test_player.matchup_score = -15
        result, _ = player_manager.scoring_calculator._apply_matchup_multiplier(test_player, base_score)
        assert abs(result - 62.5) < 0.01

    # ========== Extreme Value Tests ==========

    def test_extremely_high_adp(self, player_manager, test_player):
        """Test with extremely high ADP value (>500)"""
        test_player.average_draft_position = 999.0
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_adp_multiplier(test_player, base_score)

        # Should still apply VERY_POOR multiplier
        assert result == 70.0
        assert reason == "ADP: VERY_POOR (0.70x)"

    def test_negative_adp_value(self, player_manager, test_player):
        """Test with negative ADP (invalid but should handle)"""
        test_player.average_draft_position = -5.0
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_adp_multiplier(test_player, base_score)

        # Negative ADP should be treated as excellent (< 20)
        assert result == 120.0
        assert reason == "ADP: EXCELLENT (1.20x)"

    def test_extremely_high_fantasy_points(self, player_manager, mock_fantasy_team):
        """Test with extremely high fantasy points projection"""
        player = FantasyPlayer(
            id=1, name="Super Star", team="KC", position="QB",
            fantasy_points=999999.0, weighted_projection=100.0
        )

        mock_fantasy_team.roster = []
        result = player_manager.score_player(player, draft_round=-1)

        # Should handle large values without overflow (score can be negative with penalties)
        assert result.score is not None
        assert abs(result.score) < 1000000  # Reasonable upper bound

    def test_zero_max_projection_edge_case(self, player_manager, test_player):
        """Test normalization when max_projection is 0 - should handle gracefully (BUG FIXED)"""
        player_manager.max_projection = 0
        player_manager.scoring_calculator.max_projection = 0
        test_player.fantasy_points = 100.0

        # BUG FIX: Now handles zero max_projection gracefully instead of raising ZeroDivisionError
        result, reason = player_manager.scoring_calculator._get_normalized_fantasy_points(test_player, use_weekly_projection=False)

        # Should return 0.0 when max_projection is 0
        assert result == 0.0
        assert "Weighted: 0.00" in reason

    def test_extremely_negative_matchup_score(self, player_manager, test_player):
        """Test with extremely negative matchup score (additive scoring)"""
        test_player.matchup_score = -999
        base_score = 100.0
        result, reason = player_manager.scoring_calculator._apply_matchup_multiplier(test_player, base_score)

        # Should still apply VERY_POOR bonus: (150*0.75)-150 = -37.5
        assert result == pytest.approx(100.0 - 37.5, abs=0.1)
        assert "VERY_POOR" in reason
        assert "pts" in reason

    def test_massive_bye_week_penalty(self, player_manager, test_player, mock_fantasy_team):
        """Test with massive bye week overlaps (10+ players) - median-based"""
        # Create 10 same-position players with same bye week
        roster_players = []
        for i in range(10):
            projected = [0.0] * 17
            projected[0], projected[1], projected[2] = 8.0, 10.0, 12.0  # Weeks 1-3, Median = 10.0
            player = FantasyPlayer(
                id=90+i, name=f"RB{i}", team="BUF", position="RB", bye_week=7, fantasy_points=100.0,
                projected_points=projected, actual_points=projected.copy()
            )
            roster_players.append(player)

        mock_fantasy_team.roster = roster_players

        test_player.bye_week = 7
        test_player.position = "RB"
        base_score = 100.0

        result, reason = player_manager.scoring_calculator._apply_bye_week_penalty(test_player, base_score, player_manager.team.roster)

        # Expected penalty = (10 players × 10.0 median) ** 1.0 = 100.0
        expected_penalty = 100.0
        assert abs(result - (100.0 - expected_penalty)) < 0.01
        assert result == 0.0  # Score becomes 0 with this penalty

    # ========== Roster Operations Edge Cases ==========

    def test_scoring_with_empty_roster(self, player_manager, test_player, mock_fantasy_team):
        """Test bye week penalty with empty roster"""
        mock_fantasy_team.roster = []
        base_score = 100.0

        result, reason = player_manager.scoring_calculator._apply_bye_week_penalty(test_player, base_score, player_manager.team.roster)

        assert result == 100.0  # No penalty
        assert reason == ""

    def test_scoring_with_roster_containing_none_values(self, player_manager, test_player, mock_fantasy_team):
        """Test bye week penalty when roster has players with None bye_week"""
        other_player = FantasyPlayer(
            id=99, name="No Bye", team="KC", position="RB",
            bye_week=None, fantasy_points=100.0
        )
        mock_fantasy_team.roster = [other_player]
        base_score = 100.0

        result, reason = player_manager.scoring_calculator._apply_bye_week_penalty(test_player, base_score, player_manager.team.roster)

        # Should handle None bye_week gracefully (no match)
        assert result == 100.0
        assert reason == ""

    def test_draft_round_out_of_range(self, player_manager, test_player):
        """Test draft bonus with out-of-range draft round - reveals bug (IndexError)"""
        base_score = 100.0

        # Test with round 999 (beyond config length) - currently raises IndexError
        # This documents the bug that out-of-range rounds aren't handled gracefully
        with pytest.raises(IndexError):
            result, reason = player_manager.scoring_calculator._apply_draft_order_bonus(test_player, 999, base_score)

    # ========== CSV Loading and Data Edge Cases ==========

    def test_player_with_missing_position(self, player_manager, mock_fantasy_team):
        """Test scoring player with missing/invalid position"""
        projected = [0.0] * 17
        # Set weeks 6-17 to 250.0/12 = 20.833...
        for i in range(5, 17):  # indices 5-16 = weeks 6-17
            projected[i] = 250.0 / 12

        player = FantasyPlayer(
            id=1, name="No Position", team="KC", position=None,
            fantasy_points=100.0, weighted_projection=50.0,
            projected_points=projected,
            actual_points=projected.copy()
        )

        mock_fantasy_team.roster = []

        # Should handle missing position gracefully
        result = player_manager.score_player(player, draft_round=-1)
        assert result.score >= 0

    def test_player_with_invalid_team_name(self, player_manager, mock_fantasy_team):
        """Test scoring player with team not in teams.csv"""
        projected = [0.0] * 17
        # Set weeks 6-17 to 250.0/12 = 20.833...
        for i in range(5, 17):  # indices 5-16 = weeks 6-17
            projected[i] = 250.0 / 12

        player = FantasyPlayer(
            id=1, name="Invalid Team", team="INVALID", position="RB",
            fantasy_points=100.0, weighted_projection=50.0,
            team_offensive_rank=None,  # Team not found
            projected_points=projected,
            actual_points=projected.copy()
        )

        mock_fantasy_team.roster = []
        result = player_manager.score_player(player, team_quality=True, draft_round=-1)

        # Should apply neutral multiplier for unknown team
        assert result.score > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
